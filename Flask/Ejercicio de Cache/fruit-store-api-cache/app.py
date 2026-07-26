from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Flask, g, jsonify, request
from redis.exceptions import RedisError
from sqlalchemy.exc import IntegrityError

from auth import authenticate_user, create_user, get_user_by_username
from authorization import admin_required, login_required
from cache_service import (
    get_product_cache,
    get_products_cache,
    invalidate_product_cache,
    invalidate_products_cache,
    set_product_cache,
    set_products_cache,
)
from database import Base, SessionLocal, engine
from invoice_service import get_all_invoices, get_user_invoices
from jwt_manager import jwt_manager
from product_service import (
    create_product,
    delete_product,
    get_all_products,
    get_product_by_id,
    update_product,
)
from purchase_service import (
    InsufficientStockError,
    ProductNotFoundError,
    purchase_product,
)


app = Flask(__name__)


def create_missing_tables() -> None:
    Base.metadata.create_all(bind=engine)


def validate_credentials(data: dict | None):
    if not data:
        return None, None, (
            jsonify({"error": "A JSON body is required."}),
            400,
        )

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return None, None, (
            jsonify({"error": "Username and password are required."}),
            400,
        )

    if not isinstance(username, str) or not isinstance(password, str):
        return None, None, (
            jsonify({"error": "Username and password must be strings."}),
            400,
        )

    username = username.strip()

    if not username:
        return None, None, (
            jsonify({"error": "Username cannot be empty."}),
            400,
        )

    return username, password, None


def validate_product_data(data: dict | None):
    if not data:
        return None, (
            jsonify({"error": "A JSON body is required."}),
            400,
        )

    required_fields = {
        "name",
        "price",
        "entry_date",
        "quantity",
    }

    missing_fields = sorted(
        field
        for field in required_fields
        if field not in data
    )

    if missing_fields:
        return None, (
            jsonify(
                {
                    "error": "Missing required fields.",
                    "fields": missing_fields,
                }
            ),
            400,
        )

    name = data.get("name")
    price = data.get("price")
    entry_date_value = data.get("entry_date")
    quantity = data.get("quantity")

    if not isinstance(name, str) or not name.strip():
        return None, (
            jsonify({"error": "Name must be a non-empty string."}),
            400,
        )

    if isinstance(quantity, bool) or not isinstance(quantity, int):
        return None, (
            jsonify({"error": "Quantity must be an integer."}),
            400,
        )

    if quantity < 0:
        return None, (
            jsonify({"error": "Quantity cannot be negative."}),
            400,
        )

    try:
        price = Decimal(str(price))

        if price <= 0:
            raise ValueError

    except (InvalidOperation, ValueError):
        return None, (
            jsonify({"error": "Price must be greater than zero."}),
            400,
        )

    try:
        entry_date_value = date.fromisoformat(entry_date_value)

    except (TypeError, ValueError):
        return None, (
            jsonify(
                {
                    "error": (
                        "Entry date must use YYYY-MM-DD format."
                    )
                }
            ),
            400,
        )

    return {
        "name": name.strip(),
        "price": price,
        "entry_date": entry_date_value,
        "quantity": quantity,
    }, None


def validate_purchase_data(data: dict | None):
    if not data:
        return None, (
            jsonify({"error": "A JSON body is required."}),
            400,
        )

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if product_id is None or quantity is None:
        return None, (
            jsonify(
                {
                    "error": (
                        "product_id and quantity are required."
                    )
                }
            ),
            400,
        )

    if isinstance(product_id, bool) or not isinstance(product_id, int):
        return None, (
            jsonify({"error": "product_id must be an integer."}),
            400,
        )

    if isinstance(quantity, bool) or not isinstance(quantity, int):
        return None, (
            jsonify({"error": "Quantity must be an integer."}),
            400,
        )

    if product_id <= 0:
        return None, (
            jsonify(
                {
                    "error": (
                        "product_id must be greater than zero."
                    )
                }
            ),
            400,
        )

    if quantity <= 0:
        return None, (
            jsonify(
                {
                    "error": (
                        "Quantity must be greater than zero."
                    )
                }
            ),
            400,
        )

    return {
        "product_id": product_id,
        "quantity": quantity,
    }, None


@app.get("/liveness")
def liveness():
    return jsonify(
        {
            "status": "ok",
            "message": "Fruit Store API is running.",
        }
    ), 200


@app.post("/register")
def register():
    data = request.get_json(silent=True)

    username, password, validation_error = validate_credentials(data)

    if validation_error:
        return validation_error

    db = SessionLocal()

    try:
        if get_user_by_username(db, username):
            return jsonify(
                {"error": "Username already exists."}
            ), 409

        user = create_user(
            db=db,
            username=username,
            password=password,
            role="user",
        )

        token = jwt_manager.encode(
            {
                "user_id": user.id,
                "role": user.role,
            }
        )

        return jsonify(
            {
                "message": "User created successfully.",
                "token": token,
                "user": user.to_dict(),
            }
        ), 201

    except IntegrityError:
        db.rollback()

        return jsonify(
            {"error": "Username already exists."}
        ), 409

    except Exception as error:
        db.rollback()
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


@app.post("/login")
def login():
    data = request.get_json(silent=True)

    username, password, validation_error = validate_credentials(data)

    if validation_error:
        return validation_error

    db = SessionLocal()

    try:
        user = authenticate_user(
            db,
            username,
            password,
        )

        if user is None:
            return jsonify(
                {"error": "Invalid username or password."}
            ), 401

        token = jwt_manager.encode(
            {
                "user_id": user.id,
                "role": user.role,
            }
        )

        return jsonify(
            {
                "message": "Login successful.",
                "token": token,
                "user": user.to_dict(),
            }
        ), 200

    except Exception as error:
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


@app.get("/me")
@login_required
def me():
    return jsonify(
        {
            "id": g.current_user_id,
            "username": g.current_username,
            "role": g.current_user_role,
        }
    ), 200


@app.get("/products")
@admin_required
def list_products():
    db = SessionLocal()

    try:
        try:
            cached_products = get_products_cache()

        except RedisError as error:
            app.logger.exception(error)
            cached_products = None

        if cached_products is not None:
            return jsonify(
                {
                    "products": cached_products,
                    "source": "cache",
                }
            ), 200

        products = get_all_products(db)

        products_data = [
            product.to_dict()
            for product in products
        ]

        try:
            set_products_cache(products_data)

        except RedisError as error:
            app.logger.exception(error)

        return jsonify(
            {
                "products": products_data,
                "source": "database",
            }
        ), 200

    except Exception as error:
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


@app.get("/products/<int:product_id>")
@admin_required
def get_product(product_id: int):
    db = SessionLocal()

    try:
        try:
            cached_product = get_product_cache(product_id)

        except RedisError as error:
            app.logger.exception(error)
            cached_product = None

        if cached_product is not None:
            return jsonify(
                {
                    "product": cached_product,
                    "source": "cache",
                }
            ), 200

        product = get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            return jsonify(
                {"error": "Product not found."}
            ), 404

        product_data = product.to_dict()

        try:
            set_product_cache(product_data)

        except RedisError as error:
            app.logger.exception(error)

        return jsonify(
            {
                "product": product_data,
                "source": "database",
            }
        ), 200

    except Exception as error:
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


@app.post("/products")
@admin_required
def add_product():
    data = request.get_json(silent=True)

    validated_data, validation_error = validate_product_data(data)

    if validation_error:
        return validation_error

    db = SessionLocal()

    try:
        product = create_product(
            db=db,
            **validated_data,
        )

        try:
            invalidate_products_cache()

        except RedisError as error:
            app.logger.exception(error)

        return jsonify(
            {
                "message": "Product created successfully.",
                "product": product.to_dict(),
            }
        ), 201

    except Exception as error:
        db.rollback()
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


@app.put("/products/<int:product_id>")
@admin_required
def edit_product(product_id: int):
    data = request.get_json(silent=True)

    validated_data, validation_error = validate_product_data(data)

    if validation_error:
        return validation_error

    db = SessionLocal()

    try:
        product = get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            return jsonify(
                {"error": "Product not found."}
            ), 404

        product = update_product(
            db=db,
            product=product,
            **validated_data,
        )

        try:
            invalidate_product_cache(product_id)
            invalidate_products_cache()

        except RedisError as error:
            app.logger.exception(error)

        return jsonify(
            {
                "message": "Product updated successfully.",
                "product": product.to_dict(),
            }
        ), 200

    except Exception as error:
        db.rollback()
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


@app.delete("/products/<int:product_id>")
@admin_required
def remove_product(product_id: int):
    db = SessionLocal()

    try:
        product = get_product_by_id(
            db,
            product_id,
        )

        if product is None:
            return jsonify(
                {"error": "Product not found."}
            ), 404

        delete_product(
            db=db,
            product=product,
        )

        try:
            invalidate_product_cache(product_id)
            invalidate_products_cache()

        except RedisError as error:
            app.logger.exception(error)

        return jsonify(
            {"message": "Product deleted successfully."}
        ), 200

    except IntegrityError:
        db.rollback()

        return jsonify(
            {
                "error": (
                    "The product cannot be deleted because it "
                    "is included in an invoice."
                )
            }
        ), 409

    except Exception as error:
        db.rollback()
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


@app.post("/purchase")
@login_required
def purchase():
    data = request.get_json(silent=True)

    validated_data, validation_error = validate_purchase_data(data)

    if validation_error:
        return validation_error

    db = SessionLocal()

    try:
        product_id = validated_data["product_id"]

        invoice = purchase_product(
            db=db,
            user_id=g.current_user_id,
            product_id=product_id,
            quantity=validated_data["quantity"],
        )

        # La compra modifica el inventario del producto.
        # Por eso también invalidamos sus datos almacenados.
        try:
            invalidate_product_cache(product_id)
            invalidate_products_cache()

        except RedisError as error:
            app.logger.exception(error)

        return jsonify(
            {
                "message": "Purchase completed successfully.",
                "invoice": invoice.to_dict(),
            }
        ), 201

    except ProductNotFoundError as error:
        db.rollback()

        return jsonify(
            {"error": str(error)}
        ), 404

    except InsufficientStockError as error:
        db.rollback()

        return jsonify(
            {"error": str(error)}
        ), 409

    except ValueError as error:
        db.rollback()

        return jsonify(
            {"error": str(error)}
        ), 400

    except Exception as error:
        db.rollback()
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


@app.get("/invoices")
@login_required
def list_invoices():
    db = SessionLocal()

    try:
        if g.current_user_role == "admin":
            invoices = get_all_invoices(db)

        else:
            invoices = get_user_invoices(
                db,
                g.current_user_id,
            )

        return jsonify(
            {
                "invoices": [
                    invoice.to_dict()
                    for invoice in invoices
                ]
            }
        ), 200

    except Exception as error:
        app.logger.exception(error)

        return jsonify(
            {"error": "An internal server error occurred."}
        ), 500

    finally:
        db.close()


if __name__ == "__main__":
    create_missing_tables()
    app.run(
        debug=True,
        port=5001,
    )