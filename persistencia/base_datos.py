# Configuraicon de SQLite y SQLAlchemy, crear las tablas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from persistencia.modelos import Base


# Nombre y ubicacion de nuestra base de datos
URL_BASE_DATOS = "sqlite:///Sistema_estacionamiento.db"


# Creamos el motor que permite conectar Python con SQLite
engine = create_engine(
    URL_BASE_DATOS,
    echo=False
)


# Creamos las sesiones para realizar operaciones en la base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


# Funcion para crear las tablas si todavia no existen
def crear_tablas():
    Base.metadata.create_all(bind=engine)


# Funcion para obtener una sesion de la base de datos
def obtener_sesion():
    return SessionLocal()


