from decimal import Decimal

from flask import Blueprint, g, jsonify

from ..cache_utils import invalidate_products
from ..extensions import db
from ..models import Address, Cart, CartItem, Invoice, InvoiceItem, Product
from ..security import auth_required, owns_or_admin
from ..validation import positive_int, require_json

carts_bp = Blueprint("carts", __name__)


def get_owned_cart(cart_id):
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return None, (jsonify(error="Carrito no encontrado"), 404)
    if not owns_or_admin(cart.user_id):
        return None, (jsonify(error="No puedes administrar este carrito"), 403)
    return cart, None


@carts_bp.get("")
@auth_required()
def list_carts():
    stmt = db.select(Cart).order_by(Cart.updated_at.desc())
    if g.current_user.role != "admin":
        stmt = stmt.where(Cart.user_id == g.current_user.id)
    return jsonify(carts=[c.to_dict() for c in db.session.scalars(stmt).unique()])


@carts_bp.post("")
@auth_required()
def create_cart():
    cart = Cart(user_id=g.current_user.id)
    db.session.add(cart)
    db.session.commit()
    return jsonify(cart=cart.to_dict()), 201


@carts_bp.get("/<int:cart_id>")
@auth_required()
def get_cart(cart_id):
    cart, error = get_owned_cart(cart_id)
    return error or jsonify(cart=cart.to_dict())


@carts_bp.delete("/<int:cart_id>")
@auth_required()
def delete_cart(cart_id):
    cart, error = get_owned_cart(cart_id)
    if error:
        return error
    if cart.status != "open":
        return jsonify(error="Solo se puede eliminar un carrito abierto"), 409
    db.session.delete(cart)
    db.session.commit()
    return "", 204


@carts_bp.put("/<int:cart_id>/items/<int:product_id>")
@auth_required()
def set_cart_item(cart_id, product_id):
    cart, error = get_owned_cart(cart_id)
    if error:
        return error
    if cart.status != "open":
        return jsonify(error="El carrito ya fue finalizado"), 409
    data, error_message = require_json(("quantity",))
    if error_message:
        return jsonify(error=error_message), 400
    try:
        quantity = positive_int(data["quantity"])
    except (ValueError, TypeError) as exc:
        return jsonify(error=str(exc)), 400
    product = db.session.get(Product, product_id)
    if not product or not product.active:
        return jsonify(error="Producto no encontrado o inactivo"), 404
    if quantity > product.stock:
        return jsonify(error="La cantidad supera el stock disponible"), 409
    item = db.session.get(CartItem, (cart.id, product.id))
    if item:
        item.quantity = quantity
    else:
        db.session.add(CartItem(cart_id=cart.id, product_id=product.id, quantity=quantity))
    db.session.commit()
    return jsonify(cart=cart.to_dict())


@carts_bp.delete("/<int:cart_id>/items/<int:product_id>")
@auth_required()
def delete_cart_item(cart_id, product_id):
    cart, error = get_owned_cart(cart_id)
    if error:
        return error
    if cart.status != "open":
        return jsonify(error="El carrito ya fue finalizado"), 409
    item = db.session.get(CartItem, (cart.id, product_id))
    if not item:
        return jsonify(error="Producto no encontrado en el carrito"), 404
    db.session.delete(item)
    db.session.commit()
    return "", 204


@carts_bp.post("/<int:cart_id>/checkout")
@auth_required()
def checkout(cart_id):
    cart, error = get_owned_cart(cart_id)
    if error:
        return error
    if cart.status != "open":
        return jsonify(error="El carrito ya fue finalizado"), 409
    if not cart.items:
        return jsonify(error="El carrito está vacío"), 409
    data, error_message = require_json(("address_id", "payment_method", "payment_reference"))
    if error_message:
        return jsonify(error=error_message), 400
    address = db.session.get(Address, data["address_id"])
    if not address or address.user_id != cart.user_id:
        return jsonify(error="Dirección de facturación inválida"), 400
    product_ids = [item.product_id for item in cart.items]
    products = {
        p.id: p for p in db.session.scalars(
            db.select(Product).where(Product.id.in_(product_ids)).with_for_update()
        )
    }
    for item in cart.items:
        product = products.get(item.product_id)
        if not product or not product.active or product.stock < item.quantity:
            db.session.rollback()
            return jsonify(error=f"Stock insuficiente para el producto {item.product_id}"), 409
    total = sum((products[item.product_id].price * item.quantity for item in cart.items), Decimal("0"))
    invoice = Invoice(
        user_id=cart.user_id, cart_id=cart.id, total=total,
        payment_method=data["payment_method"], payment_reference=data["payment_reference"],
        billing_recipient=address.recipient, billing_line1=address.line1,
        billing_line2=address.line2, billing_city=address.city,
        billing_province=address.province, billing_postal_code=address.postal_code,
        billing_country=address.country,
    )
    db.session.add(invoice)
    for item in cart.items:
        product = products[item.product_id]
        product.stock -= item.quantity
        invoice.items.append(InvoiceItem(product_id=product.id, product_name=product.name, sku=product.sku, unit_price=product.price, quantity=item.quantity))
    cart.status = "completed"
    db.session.commit()
    for product_id in product_ids:
        invalidate_products(product_id)
    return jsonify(invoice=invoice.to_dict()), 201

