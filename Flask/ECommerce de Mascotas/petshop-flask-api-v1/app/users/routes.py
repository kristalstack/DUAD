from flask import Blueprint, g, jsonify
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Address, User
from ..security import auth_required, owns_or_admin
from ..validation import country_code, require_json

users_bp = Blueprint("users", __name__)


@users_bp.get("")
@auth_required(admin=True)
def list_users():
    return jsonify(users=[u.to_dict() for u in db.session.scalars(db.select(User).order_by(User.id))])


@users_bp.get("/<int:user_id>")
@auth_required()
def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify(error="Usuario no encontrado"), 404
    if not owns_or_admin(user.id):
        return jsonify(error="No puedes consultar otro usuario"), 403
    return jsonify(user=user.to_dict())


@users_bp.patch("/<int:user_id>")
@auth_required(admin=True)
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify(error="Usuario no encontrado"), 404
    data, error = require_json()
    if error:
        return jsonify(error=error), 400
    for field in ("name", "email", "active"):
        if field in data:
            setattr(user, field, data[field].strip().lower() if field == "email" else data[field])
    if "role" in data:
        if data["role"] not in ("admin", "client"):
            return jsonify(error="role debe ser admin o client"), 400
        user.role = data["role"]
    if "password" in data:
        if len(data["password"]) < 8:
            return jsonify(error="La contraseña debe tener al menos 8 caracteres"), 400
        user.set_password(data["password"])
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="El correo ya está registrado"), 409
    return jsonify(user=user.to_dict())


@users_bp.delete("/<int:user_id>")
@auth_required(admin=True)
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify(error="Usuario no encontrado"), 404
    user.active = False
    db.session.commit()
    return "", 204


@users_bp.get("/<int:user_id>/addresses")
@auth_required()
def list_addresses(user_id):
    if not owns_or_admin(user_id):
        return jsonify(error="No puedes consultar direcciones de otro usuario"), 403
    addresses = db.session.scalars(db.select(Address).where(Address.user_id == user_id)).all()
    return jsonify(addresses=[a.to_dict() for a in addresses])


@users_bp.post("/<int:user_id>/addresses")
@auth_required()
def create_address(user_id):
    if not owns_or_admin(user_id):
        return jsonify(error="No puedes crear direcciones para otro usuario"), 403
    if not db.session.get(User, user_id):
        return jsonify(error="Usuario no encontrado"), 404
    fields = ("recipient", "line1", "city", "province")
    data, error = require_json(fields)
    if error:
        return jsonify(error=error), 400
    try:
        country = country_code(data.get("country", "CR"))
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    address = Address(
        user_id=user_id,
        **{k: data[k] for k in fields},
        line2=data.get("line2"),
        postal_code=data.get("postal_code"),
        country=country,
    )
    db.session.add(address)
    db.session.commit()
    return jsonify(address=address.to_dict()), 201


@users_bp.patch("/<int:user_id>/addresses/<int:address_id>")
@auth_required()
def update_address(user_id, address_id):
    address = db.session.get(Address, address_id)
    if not address or address.user_id != user_id:
        return jsonify(error="Dirección no encontrada"), 404
    if not owns_or_admin(user_id):
        return jsonify(error="No puedes modificar esta dirección"), 403
    data, error = require_json()
    if error:
        return jsonify(error=error), 400
    if "country" in data:
        try:
            address.country = country_code(data["country"])
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
    for field in ("recipient", "line1", "line2", "city", "province", "postal_code"):
        if field in data:
            setattr(address, field, data[field])
    db.session.commit()
    return jsonify(address=address.to_dict())


@users_bp.delete("/<int:user_id>/addresses/<int:address_id>")
@auth_required()
def delete_address(user_id, address_id):
    address = db.session.get(Address, address_id)
    if not address or address.user_id != user_id:
        return jsonify(error="Dirección no encontrada"), 404
    if not owns_or_admin(user_id):
        return jsonify(error="No puedes eliminar esta dirección"), 403
    db.session.delete(address)
    db.session.commit()
    return "", 204
