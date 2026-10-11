from flask import Blueprint, g, jsonify, request
from sqlalchemy.exc import IntegrityError

from ..cache_utils import invalidate_products, product_key, products_list_key
from ..extensions import cache, db
from ..models import Product
from ..security import auth_required
from ..validation import nonnegative_money, require_json

products_bp = Blueprint("products", __name__)


@products_bp.get("")
@auth_required()
def list_products():
    include_inactive = request.args.get("include_inactive") == "true"
    # Solo un administrador puede incluir elementos dados de baja.
    include_inactive = include_inactive and g.current_user.role == "admin"
    key = f"{products_list_key()}:{'all' if include_inactive else 'active'}"
    result = cache.get(key)
    if result is None:
        stmt = db.select(Product).order_by(Product.name)
        if not include_inactive:
            stmt = stmt.where(Product.active.is_(True))
        result = [p.to_dict() for p in db.session.scalars(stmt)]
        cache.set(key, result, timeout=120)
    return jsonify(products=result)


@products_bp.get("/<int:product_id>")
@auth_required()
def get_product(product_id):
    key = product_key(product_id)
    result = cache.get(key)
    if result is None:
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify(error="Producto no encontrado"), 404
        result = product.to_dict()
        cache.set(key, result, timeout=300)
    return jsonify(product=result)


@products_bp.post("")
@auth_required(admin=True)
def create_product():
    data, error = require_json(("sku", "name", "price", "stock"))
    if error:
        return jsonify(error=error), 400
    try:
        price = nonnegative_money(data["price"])
        stock = int(data["stock"])
        if stock < 0:
            raise ValueError("stock no puede ser negativo")
    except (ValueError, TypeError) as exc:
        return jsonify(error=str(exc)), 400
    product = Product(sku=data["sku"], name=data["name"], description=data.get("description"), price=price, stock=stock, active=data.get("active", True))
    db.session.add(product)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="El SKU ya existe"), 409
    invalidate_products(product.id)
    return jsonify(product=product.to_dict()), 201


@products_bp.patch("/<int:product_id>")
@auth_required(admin=True)
def update_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify(error="Producto no encontrado"), 404
    data, error = require_json()
    if error:
        return jsonify(error=error), 400
    try:
        if "price" in data:
            product.price = nonnegative_money(data["price"])
        if "stock" in data:
            product.stock = int(data["stock"])
            if product.stock < 0:
                raise ValueError("stock no puede ser negativo")
    except (ValueError, TypeError) as exc:
        return jsonify(error=str(exc)), 400
    for field in ("sku", "name", "description", "active"):
        if field in data:
            setattr(product, field, data[field])
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="El SKU ya existe"), 409
    invalidate_products(product.id)
    return jsonify(product=product.to_dict())


@products_bp.delete("/<int:product_id>")
@auth_required(admin=True)
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify(error="Producto no encontrado"), 404
    product.active = False
    db.session.commit()
    invalidate_products(product.id)
    return "", 204
