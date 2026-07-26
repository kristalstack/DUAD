from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models import Invoice, InvoiceItem


def create_invoice(
    db: Session,
    user_id: int,
    total: Decimal,
) -> Invoice:
    invoice = Invoice(
        user_id=user_id,
        total=total,
    )

    db.add(invoice)
    db.flush()

    return invoice


def get_invoice_by_id(
    db: Session,
    invoice_id: int,
) -> Invoice | None:
    statement = (
        select(Invoice)
        .options(
            joinedload(Invoice.items).joinedload(
                InvoiceItem.product
            )
        )
        .where(Invoice.id == invoice_id)
    )

    return db.scalars(statement).unique().first()


def get_user_invoices(
    db: Session,
    user_id: int,
) -> list[Invoice]:
    statement = (
        select(Invoice)
        .options(
            joinedload(Invoice.items).joinedload(
                InvoiceItem.product
            )
        )
        .where(Invoice.user_id == user_id)
        .order_by(Invoice.id)
    )

    return list(
        db.scalars(statement).unique().all()
    )


def get_all_invoices(
    db: Session,
) -> list[Invoice]:
    statement = (
        select(Invoice)
        .options(
            joinedload(Invoice.items).joinedload(
                InvoiceItem.product
            )
        )
        .order_by(Invoice.id)
    )

    return list(
        db.scalars(statement).unique().all()
    )