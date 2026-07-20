from decimal import Decimal

from sqlalchemy.orm import Session

from invoice_service import create_invoice
from models import InvoiceItem, Product


class ProductNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


def purchase_product(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int,
):
    product = db.get(Product, product_id)

    if product is None:
        raise ProductNotFoundError("Product not found.")

    if product.quantity < quantity:
        raise InsufficientStockError(
            "There is not enough stock available."
        )

    subtotal = product.price * Decimal(quantity)

    invoice = create_invoice(
        db=db,
        user_id=user_id,
        total=subtotal,
    )

    invoice_item = InvoiceItem(
        invoice=invoice,
        product=product,
        quantity=quantity,
        unit_price=product.price,
        subtotal=subtotal,
    )

    product.quantity -= quantity

    db.add(invoice_item)
    db.commit()

    # Volvemos a cargar la factura antes de devolverla.
    db.refresh(invoice)

    return invoice