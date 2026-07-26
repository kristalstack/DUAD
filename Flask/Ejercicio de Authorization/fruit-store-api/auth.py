from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import User


VALID_ROLES = {"admin", "user"}


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    statement = select(User).where(
        User.username == username
    )

    return db.scalar(statement)


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    statement = select(User).where(
        User.id == user_id
    )

    return db.scalar(statement)


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User | None:
    user = get_user_by_username(db, username)

    if user is None:
        return None

    if not check_password_hash(user.password, password):
        return None

    return user


def create_user(
    db: Session,
    username: str,
    password: str,
    role: str = "user",
) -> User:
    if role not in VALID_ROLES:
        raise ValueError("Invalid role.")

    user = User(
        username=username,
        password=generate_password_hash(password),
        role=role,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        raise