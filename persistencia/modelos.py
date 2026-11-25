# Este archivo define nuestras tablas y relaciones de la base de datos
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, func
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

    # Relacion inversa para acceder a las suscripciones de un vehiculo
    suscripciones: Mapped[list["Suscripcion"]] = relationship(
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

    # Relacion inversa para acceder a los pagos de una estadia
    pagos: Mapped[list["Pago"]] = relationship(
        back_populates="estadia"
    )







# Registra las suscripciones mensuales de los vehiculos
class Suscripcion(Base):
    __tablename__ = "suscripciones"

    # Identificador unico de la suscripcion
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    # Relacion con el vehiculo que contrata la suscripcion
    id_vehiculo: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("vehiculo.patente"),
        nullable=False
    )

    # Fecha y hora en que comienza la suscripcion
    inicio: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    # Fecha y hora en que termina la suscripcion
    termino: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    # Conexion con el vehiculo
    vehiculo: Mapped["Vehiculo"] = relationship(
        back_populates="suscripciones"
    )

    # Conexion con los pagos de esta suscripcion
    pagos: Mapped[list["Pago"]] = relationship(
        back_populates="suscripcion"
    )



# Registra los pagos realizados en el estacionamiento
class Pago(Base):
    __tablename__ = "pagos"

    # Identificador unico del pago
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    # Monto del pago realizado en pesos chilenos
    monto: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Modalidad que origino el pago
    modalidad: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    # Fecha y hora en que se registro el pago
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Relacion opcional con una estadia
    id_estadia: Mapped[Optional[int]] = mapped_column(
        ForeignKey("estadias.id"),
        nullable=True
    )

    # Relacion opcional con una suscripcion
    id_suscripcion: Mapped[Optional[int]] = mapped_column(
        ForeignKey("suscripciones.id"),
        nullable=True
    )

    # Un pago debe pertenecer a una estadia o a una suscripcion,
    # pero no a ambas ni a ninguna.
    __table_args__ = (
        CheckConstraint(
            """
            (id_estadia IS NOT NULL AND id_suscripcion IS NULL)
            OR
            (id_estadia IS NULL AND id_suscripcion IS NOT NULL)
            """,
            name="check_origen_pago"
        ),
    )

    # Conexion con la estadia
    estadia: Mapped[Optional["Estadia"]] = relationship(
        back_populates="pagos"
    )

    # Conexion con la suscripcion
    suscripcion: Mapped[Optional["Suscripcion"]] = relationship(
        back_populates="pagos"
    )