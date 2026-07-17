from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    cars: Mapped[list["Car"]] = relationship(
        back_populates="user",
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, "
            f"name='{self.name}', "
            f"email='{self.email}')"
        )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    street: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="addresses",
    )

    def __repr__(self) -> str:
        return (
            f"Address(id={self.id}, "
            f"street='{self.street}', "
            f"city='{self.city}', "
            f"country='{self.country}', "
            f"user_id={self.user_id})"
        )


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    user: Mapped[Optional["User"]] = relationship(
        back_populates="cars",
    )

    def __repr__(self) -> str:
        return (
            f"Car(id={self.id}, "
            f"brand='{self.brand}', "
            f"model='{self.model}', "
            f"year={self.year}, "
            f"user_id={self.user_id})"
        )