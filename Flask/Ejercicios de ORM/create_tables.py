from sqlalchemy import inspect

from database import Base, engine
from models import Address, Car, User


def create_missing_tables() -> None:
    inspector = inspect(engine)

    required_tables = {
        User.__tablename__,
        Address.__tablename__,
        Car.__tablename__,
    }

    existing_tables = set(inspector.get_table_names())
    missing_tables = required_tables - existing_tables

    if not missing_tables:
        print("Todas las tablas ya existen.")
        return

    print("Las siguientes tablas no existen:")
    for table_name in sorted(missing_tables):
        print(f"- {table_name}")

    Base.metadata.create_all(bind=engine)

    print("Las tablas faltantes fueron creadas correctamente.")


if __name__ == "__main__":
    create_missing_tables()