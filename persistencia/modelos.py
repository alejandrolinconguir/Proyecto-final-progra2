# Este archivo define nuestras tablas y relaciones de la base de datos
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# Aqui las clases pasaran a ser tablas

class Base(DeclarativeBase):
    pass


# Los vehiculos
class Vehiculo(Base):
    # Nombre de la tabla en SQLite
    __tablename__ = "vehiculo"

    # La patente (nuestra clave primeria)
    patente: Mapped[str] = mapped_column(
        String(10),
        primary_key=True
    )

    # Los Mapped son para el tipo de dato
    # datos de contacto de la perosna responsable
    datos_contacto: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # Relación inversa opcional para acceder a estadías desde un vehículo
    estadias: Mapped[list["Estadia"]] = relationship(
        back_populates="vehiculo"
    )







# registra el ingreso, la salida y la modalidad de cobro.
class Estadia(Base):
    __tablename__ = "estadias"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    # Relacion con los vehiculos con la foranea key
    id_vehiculo: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("vehiculo.patente"),
        nullable=False
    )

    ingreso: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    salida: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    modalidad_cobro: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
    # La conexion
    vehiculo: Mapped["Vehiculo"] = relationship(
        back_populates="estadias"
    )




# de momento solamente con su id
class Suscripciones(Base):
    __tablename__ = "suscripciones"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )





# de momento solamente con su id
class Pagos(Base):
    __tablename__ = "pagos"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )


#de momento solamente con su id
class Pagos(Base):
    __tablename__ = "pagos"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key= True
    )
