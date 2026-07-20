from functools import wraps

import jwt
from flask import g, jsonify, request

from auth import get_user_by_id
from database import SessionLocal
from jwt_manager import JWTManager


jwt_manager = JWTManager(
    "private_key.pem",
    "public_key.pem",
)


def get_bearer_token() -> str | None:
    authorization_header = request.headers.get("Authorization")

    if not authorization_header:
        return None

    parts = authorization_header.split()

    if len(parts) != 2:
        return None

    token_type, token = parts

    if token_type.lower() != "bearer":
        return None

    return token


def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        token = get_bearer_token()

        if token is None:
            return jsonify(
                {
                    "error": "Authentication token is required.",
                }
            ), 401

        try:
            payload = jwt_manager.decode(token)

        except jwt.ExpiredSignatureError:
            return jsonify(
                {
                    "error": "The authentication token has expired.",
                }
            ), 401

        except jwt.InvalidTokenError:
            return jsonify(
                {
                    "error": "The authentication token is invalid.",
                }
            ), 401

        user_id = payload.get("user_id")

        if user_id is None:
            return jsonify(
                {
                    "error": "The authentication token is invalid.",
                }
            ), 401

        db = SessionLocal()

        try:
            user = get_user_by_id(db, user_id)

            if user is None:
                return jsonify(
                    {
                        "error": "The authenticated user no longer exists.",
                    }
                ), 401

            # Guardamos los datos para que la ruta pueda utilizarlos.
            g.current_user_id = user.id
            g.current_username = user.username
            g.current_user_role = user.role

            return route_function(*args, **kwargs)

        except Exception as error:
            print(error)

            return jsonify(
                {
                    "error": "An internal server error occurred.",
                }
            ), 500

        finally:
            db.close()

    return decorated_function


def admin_required(route_function):
    @wraps(route_function)
    @login_required
    def decorated_function(*args, **kwargs):
        if g.current_user_role != "admin":
            return jsonify(
                {
                    "error": "Administrator access is required.",
                }
            ), 403

        return route_function(*args, **kwargs)

    return decorated_function