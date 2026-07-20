from sqlalchemy import select

from database import SessionLocal
from models import Address, User


class AddressManager:

    def create_address(self, street, city, country, user_id):
        session = SessionLocal()

        try:
            user = session.get(User, user_id)

            if user is None:
                print("Usuario no encontrado.")
                return

            address = Address(
                street=street,
                city=city,
                country=country,
                user=user
            )

            session.add(address)
            session.commit()
            session.refresh(address)

            print(f"Dirección creada con ID {address.id}")

            return address

        finally:
            session.close()

    def get_all_addresses(self):
        session = SessionLocal()

        try:
            addresses = session.scalars(
                select(Address)
            ).all()

            return addresses

        finally:
            session.close()

    def update_address(self, address_id, street, city, country):
        session = SessionLocal()

        try:
            address = session.get(Address, address_id)

            if address is None:
                print("Dirección no encontrada.")
                return

            address.street = street
            address.city = city
            address.country = country

            session.commit()

            print("Dirección actualizada.")

        finally:
            session.close()

    def delete_address(self, address_id):
        session = SessionLocal()

        try:
            address = session.get(Address, address_id)

            if address is None:
                print("Dirección no encontrada.")
                return

            session.delete(address)
            session.commit()

            print("Dirección eliminada.")

        finally:
            session.close()