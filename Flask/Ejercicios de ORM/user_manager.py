from sqlalchemy import select

from database import SessionLocal
from models import User


class UserManager:

    def create_user(self, name, email):
        session = SessionLocal()

        try:
            # Verificar si ya existe un usuario con ese correo
            existing_user = session.scalar(
                select(User).where(User.email == email)
            )

            if existing_user is not None:
                print(f"Ya existe un usuario con el correo {email}.")
                return None

            user = User(
                name=name,
                email=email
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            print(f"Usuario creado con ID {user.id}")

            return user

        except Exception as error:
            session.rollback()
            print(f"No fue posible crear el usuario: {error}")
            return None

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

            # Verificar que el nuevo correo no pertenezca a otro usuario
            existing_user = session.scalar(
                select(User).where(
                    User.email == email,
                    User.id != user_id
                )
            )

            if existing_user is not None:
                print(f"Ya existe otro usuario con el correo {email}.")
                return

            user.name = name
            user.email = email

            session.commit()

            print("Usuario actualizado.")

        except Exception as error:
            session.rollback()
            print(f"No fue posible actualizar el usuario: {error}")

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

        except Exception as error:
            session.rollback()
            print(f"No fue posible eliminar el usuario: {error}")

        finally:
            session.close()