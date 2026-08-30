from datetime import datetime, timedelta, timezone
from functools import wraps
from uuid import uuid4

import jwt
from flask import current_app, g, jsonify, request

from .extensions import db
from .models import RevokedToken, User


def create_access_token(user):
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=current_app.config["JWT_EXPIRES_MINUTES"])
    payload = {"sub": str(user.id), "role": user.role, "jti": str(uuid4()), "iat": now, "exp": expires}
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])


def auth_required(admin=False):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return jsonify(error="Token de autenticación requerido"), 401
            try:
                payload = decode_token(header[7:])
                if db.session.scalar(db.select(RevokedToken).where(RevokedToken.jti == payload["jti"])):
                    return jsonify(error="Token revocado"), 401
                user = db.session.get(User, int(payload["sub"]))
                if not user or not user.active:
                    return jsonify(error="Usuario inválido o inactivo"), 401
                if admin and user.role != "admin":
                    return jsonify(error="Se requiere rol de administrador"), 403
                g.current_user = user
                g.jwt_payload = payload
            except jwt.ExpiredSignatureError:
                return jsonify(error="El token ha expirado"), 401
            except (jwt.InvalidTokenError, KeyError, ValueError):
                return jsonify(error="Token inválido"), 401
            return view(*args, **kwargs)
        return wrapped
    return decorator


def owns_or_admin(owner_id):
    return g.current_user.role == "admin" or g.current_user.id == owner_id

