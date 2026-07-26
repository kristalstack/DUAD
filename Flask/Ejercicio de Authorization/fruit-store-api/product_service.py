from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Product


def get_all_products(db: Session) -> list[Product]:
    statement = select(Product).order_by(Product.id)

    return list(db.scalars(statement).all())


def get_product_by_id(
    db: Session,
    product_id: int,
) -> Product | None:
    return db.get(Product, product_id)


def create_product(
    db: Session,
    name: str,
    price: Decimal,
    entry_date,
    quantity: int,
) -> Product:
    product = Product(
        name=name,
        price=price,
        entry_date=entry_date,
        quantity=quantity,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def update_product(
    db: Session,
    product: Product,
    name: str,
    price: Decimal,
    entry_date,
    quantity: int,
) -> Product:
    product.name = name
    product.price = price
    product.entry_date = entry_date
    product.quantity = quantity

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product: Product,
) -> None:
    db.delete(product)
    db.commit()