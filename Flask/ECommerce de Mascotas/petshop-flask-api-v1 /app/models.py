from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)


class User(TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="client")
    active = db.Column(db.Boolean, nullable=False, default=True)
    addresses = db.relationship("Address", backref="user", lazy=True, cascade="all, delete-orphan")
    carts = db.relationship("Cart", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "role": self.role, "active": self.active}


class RevokedToken(db.Model):
    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)


class Product(TimestampMixin, db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(60), nullable=False, unique=True, index=True)
    name = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False, default=True)
    __table_args__ = (
        db.CheckConstraint("price >= 0", name="ck_product_price_nonnegative"),
        db.CheckConstraint("stock >= 0", name="ck_product_stock_nonnegative"),
    )

    def to_dict(self):
        return {
            "id": self.id, "sku": self.sku, "name": self.name,
            "description": self.description, "price": str(self.price),
            "stock": self.stock, "active": self.active,
        }


class Address(TimestampMixin, db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    recipient = db.Column(db.String(120), nullable=False)
    line1 = db.Column(db.String(255), nullable=False)
    line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(2), nullable=False, default="CR")

    def to_dict(self):
        return {k: getattr(self, k) for k in ("id", "user_id", "recipient", "line1", "line2", "city", "province", "postal_code", "country")}


class Cart(TimestampMixin, db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="open")
    items = db.relationship("CartItem", backref="cart", lazy=True, cascade="all, delete-orphan")
    invoice = db.relationship("Invoice", backref="cart", uselist=False)

    def to_dict(self):
        total = sum((item.product.price * item.quantity for item in self.items), Decimal("0"))
        return {
            "id": self.id, "user_id": self.user_id, "status": self.status,
            "items": [item.to_dict() for item in self.items], "estimated_total": str(total),
        }


class CartItem(db.Model):
    __tablename__ = "cart_items"
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product")
    __table_args__ = (db.CheckConstraint("quantity > 0", name="ck_cart_item_quantity_positive"),)

    def to_dict(self):
        return {"product_id": self.product_id, "quantity": self.quantity, "product": self.product.to_dict()}


class Invoice(TimestampMixin, db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(36), nullable=False, unique=True, default=lambda: str(uuid4()), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False, unique=True)
    status = db.Column(db.String(20), nullable=False, default="paid")
    total = db.Column(db.Numeric(12, 2), nullable=False)
    payment_method = db.Column(db.String(30), nullable=False)
    payment_reference = db.Column(db.String(100), nullable=False)
    billing_recipient = db.Column(db.String(120), nullable=False)
    billing_line1 = db.Column(db.String(255), nullable=False)
    billing_line2 = db.Column(db.String(255))
    billing_city = db.Column(db.String(100), nullable=False)
    billing_province = db.Column(db.String(100), nullable=False)
    billing_postal_code = db.Column(db.String(20))
    billing_country = db.Column(db.String(2), nullable=False)
    items = db.relationship("InvoiceItem", backref="invoice", lazy=True, cascade="all, delete-orphan")
    returns = db.relationship("Return", backref="invoice", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id, "number": self.number, "user_id": self.user_id,
            "cart_id": self.cart_id, "status": self.status, "total": str(self.total),
            "payment_method": self.payment_method, "payment_reference": self.payment_reference,
            "billing_address": {
                "recipient": self.billing_recipient, "line1": self.billing_line1,
                "line2": self.billing_line2, "city": self.billing_city,
                "province": self.billing_province, "postal_code": self.billing_postal_code,
                "country": self.billing_country,
            },
            "items": [item.to_dict() for item in self.items],
            "returns": [ret.to_dict() for ret in self.returns],
        }


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product_name = db.Column(db.String(160), nullable=False)
    sku = db.Column(db.String(60), nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    returned_quantity = db.Column(db.Integer, nullable=False, default=0)
    product = db.relationship("Product")

    def to_dict(self):
        return {
            "id": self.id, "product_id": self.product_id, "product_name": self.product_name,
            "sku": self.sku, "unit_price": str(self.unit_price), "quantity": self.quantity,
            "returned_quantity": self.returned_quantity,
        }


class Return(TimestampMixin, db.Model):
    __tablename__ = "returns"
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False, index=True)
    reason = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    items = db.relationship("ReturnItem", backref="return_record", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "invoice_id": self.invoice_id, "reason": self.reason, "items": [item.to_dict() for item in self.items]}


class ReturnItem(db.Model):
    __tablename__ = "return_items"
    id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, db.ForeignKey("returns.id"), nullable=False)
    invoice_item_id = db.Column(db.Integer, db.ForeignKey("invoice_items.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    invoice_item = db.relationship("InvoiceItem")

    def to_dict(self):
        return {"invoice_item_id": self.invoice_item_id, "quantity": self.quantity}

