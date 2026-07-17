from sqlalchemy import select

from database import SessionLocal
from models import Car, User


class CarManager:

    def create_car(self, brand, model, year):
        session = SessionLocal()

        try:
            car = Car(
                brand=brand,
                model=model,
                year=year
            )

            session.add(car)
            session.commit()
            session.refresh(car)

            print(f"Automóvil creado con ID {car.id}")

            return car

        finally:
            session.close()

    def get_all_cars(self):
        session = SessionLocal()

        try:
            cars = session.scalars(
                select(Car)
            ).all()

            return cars

        finally:
            session.close()

    def update_car(self, car_id, brand, model, year):
        session = SessionLocal()

        try:
            car = session.get(Car, car_id)

            if car is None:
                print("Automóvil no encontrado.")
                return

            car.brand = brand
            car.model = model
            car.year = year

            session.commit()

            print("Automóvil actualizado.")

        finally:
            session.close()

    def delete_car(self, car_id):
        session = SessionLocal()

        try:
            car = session.get(Car, car_id)

            if car is None:
                print("Automóvil no encontrado.")
                return

            session.delete(car)
            session.commit()

            print("Automóvil eliminado.")

        finally:
            session.close()

    def assign_car_to_user(self, car_id, user_id):
        session = SessionLocal()

        try:
            car = session.get(Car, car_id)

            if car is None:
                print("Automóvil no encontrado.")
                return

            user = session.get(User, user_id)

            if user is None:
                print("Usuario no encontrado.")
                return

            car.user = user

            session.commit()

            print(
                f"Automóvil {car_id} asociado "
                f"al usuario {user_id}."
            )

        finally:
            session.close()