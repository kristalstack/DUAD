from datetime import datetime, timezone

from flask import Blueprint, g, jsonify
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import RevokedToken, User
from ..security import auth_required, create_access_token
from ..validation import require_json

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data, error = require_json(("name", "email", "password"))
    if error:
        return jsonify(error=error), 400
    if len(data["password"]) < 8:
        return jsonify(error="La contraseña debe tener al menos 8 caracteres"), 400
    user = User(name=data["name"].strip(), email=data["email"].strip().lower(), role="client")
    user.set_password(data["password"])
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="El correo ya está registrado"), 409
    return jsonify(user=user.to_dict(), access_token=create_access_token(user)), 201


@auth_bp.post("/login")
def login():
    data, error = require_json(("email", "password"))
    if error:
        return jsonify(error=error), 400
    user = db.session.scalar(db.select(User).where(User.email == data["email"].strip().lower()))
    if not user or not user.active or not user.check_password(data["password"]):
        return jsonify(error="Credenciales incorrectas"), 401
    return jsonify(user=user.to_dict(), access_token=create_access_token(user))


@auth_bp.post("/logout")
@auth_required()
def logout():
    expires = datetime.fromtimestamp(g.jwt_payload["exp"], tz=timezone.utc)
    db.session.add(RevokedToken(jti=g.jwt_payload["jti"], expires_at=expires))
    db.session.commit()
    return jsonify(message="Sesión cerrada")

