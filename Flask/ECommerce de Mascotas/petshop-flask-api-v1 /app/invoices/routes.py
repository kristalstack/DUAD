from flask import Blueprint, g, jsonify
from sqlalchemy.orm import selectinload

from ..cache_utils import invoice_key, invalidate_invoice, invalidate_products
from ..extensions import cache, db
from ..models import Invoice, InvoiceItem, Product, Return, ReturnItem
from ..security import auth_required, owns_or_admin
from ..validation import positive_int, require_json

invoices_bp = Blueprint("invoices", __name__)


@invoices_bp.get("")
@auth_required()
def list_invoices():
    stmt = (
        db.select(Invoice)
        .options(
            selectinload(Invoice.items),
            selectinload(Invoice.returns).selectinload(Return.items),
        )
        .order_by(Invoice.created_at.desc())
    )
    if g.current_user.role != "admin":
        stmt = stmt.where(Invoice.user_id == g.current_user.id)
    return jsonify(invoices=[invoice.to_dict() for invoice in db.session.scalars(stmt).unique()])


@invoices_bp.get("/<string:number>")
@auth_required()
def get_invoice(number):
    key = invoice_key(number)
    result = cache.get(key)
    if result is None:
        invoice = db.session.scalar(db.select(Invoice).where(Invoice.number == number))
        if not invoice:
            return jsonify(error="Factura no encontrada"), 404
        result = invoice.to_dict()
        cache.set(key, result, timeout=600)
    if not owns_or_admin(result["user_id"]):
        return jsonify(error="No puedes consultar esta factura"), 403
    return jsonify(invoice=result)


@invoices_bp.patch("/<string:number>")
@auth_required(admin=True)
def update_invoice(number):
    invoice = db.session.scalar(db.select(Invoice).where(Invoice.number == number))
    if not invoice:
        return jsonify(error="Factura no encontrada"), 404
    data, error = require_json(("status",))
    if error:
        return jsonify(error=error), 400
    if data["status"] not in ("paid", "cancelled", "partially_refunded", "refunded"):
        return jsonify(error="Estado de factura inválido"), 400
    invoice.status = data["status"]
    db.session.commit()
    invalidate_invoice(number)
    return jsonify(invoice=invoice.to_dict())


@invoices_bp.delete("/<string:number>")
@auth_required(admin=True)
def delete_invoice(number):
    invoice = db.session.scalar(db.select(Invoice).where(Invoice.number == number))
    if not invoice:
        return jsonify(error="Factura no encontrada"), 404
    if invoice.status not in ("cancelled", "refunded"):
        return jsonify(error="Solo se pueden eliminar facturas canceladas o totalmente devueltas"), 409
    db.session.delete(invoice)
    db.session.commit()
    invalidate_invoice(number)
    return "", 204


@invoices_bp.post("/<string:number>/returns")
@auth_required()
def create_return(number):
    invoice = db.session.scalar(db.select(Invoice).where(Invoice.number == number))
    if not invoice:
        return jsonify(error="Factura no encontrada"), 404
    if not owns_or_admin(invoice.user_id):
        return jsonify(error="No puedes devolver productos de esta factura"), 403
    data, error = require_json(("reason", "items"))
    if error:
        return jsonify(error=error), 400
    if not isinstance(data["items"], list) or not data["items"]:
        return jsonify(error="items debe ser una lista no vacía"), 400
    requested = {}
    try:
        for raw in data["items"]:
            item_id = int(raw["invoice_item_id"])
            if item_id in requested:
                raise ValueError("No repitas invoice_item_id")
            requested[item_id] = positive_int(raw["quantity"])
    except (KeyError, ValueError, TypeError) as exc:
        return jsonify(error=f"Detalle de devolución inválido: {exc}"), 400
    invoice_items = {
        item.id: item for item in db.session.scalars(
            db.select(InvoiceItem).where(InvoiceItem.invoice_id == invoice.id).with_for_update()
        )
    }
    for item_id, quantity in requested.items():
        item = invoice_items.get(item_id)
        if not item:
            db.session.rollback()
            return jsonify(error=f"El detalle {item_id} no pertenece a la factura"), 400
        if item.returned_quantity + quantity > item.quantity:
            db.session.rollback()
            return jsonify(error=f"La devolución supera lo comprado para el detalle {item_id}"), 409
    products = {
        p.id: p for p in db.session.scalars(
            db.select(Product).where(Product.id.in_([invoice_items[i].product_id for i in requested])).with_for_update()
        )
    }
    return_record = Return(invoice_id=invoice.id, reason=data["reason"], created_by=g.current_user.id)
    db.session.add(return_record)
    for item_id, quantity in requested.items():
        item = invoice_items[item_id]
        item.returned_quantity += quantity
        products[item.product_id].stock += quantity
        return_record.items.append(ReturnItem(invoice_item_id=item.id, quantity=quantity))
    invoice.status = "refunded" if all(i.returned_quantity == i.quantity for i in invoice.items) else "partially_refunded"
    db.session.commit()
    invalidate_invoice(number)
    for item_id in requested:
        invalidate_products(invoice_items[item_id].product_id)
    return jsonify(return_record=return_record.to_dict(), invoice=invoice.to_dict()), 201
