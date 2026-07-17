from sqlalchemy import select

from database import SessionLocal
from models import User


class UserManager:

    def create_user(self, name, email):
        session = SessionLocal()

        try:
            user = User(
                name=name,
                email=email
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            print(f"Usuario creado con ID {user.id}")

            return user

        finally:
            session.close()

    def get_all_users(self):
        session = SessionLocal()

        try:
            users = session.scalars(
                select(User)
            ).all()

            return users

        finally:
            session.close()

    def update_user(self, user_id, name, email):
        session = SessionLocal()

        try:
            user = session.get(User, user_id)

            if user is None:
                print("Usuario no encontrado.")
                return

            user.name = name
            user.email = email

            session.commit()

            print("Usuario actualizado.")

        finally:
            session.close()

    def delete_user(self, user_id):
        session = SessionLocal()

        try:
            user = session.get(User, user_id)

            if user is None:
                print("Usuario no encontrado.")
                return

            session.delete(user)
            session.commit()

            print("Usuario eliminado.")

        finally:
            session.close()