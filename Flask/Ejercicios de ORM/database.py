from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Base de datos SQLite
DATABASE_URL = "sqlite:///orm_database.db"

# Motor de conexión
engine = create_engine(DATABASE_URL, echo=False)

# Sesiones
SessionLocal = sessionmaker(bind=engine)


# Clase base para todos los modelos
class Base(DeclarativeBase):
    pass