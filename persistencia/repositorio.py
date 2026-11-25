#Este contiene las operaciones para guardar, bsucar y consultar la info
from sqlalchemy import select
from sqlalchemy.orm import Session

from persistencia.modelos import Vehiculo, Estadia, Suscripcion, Pago


class Repositorio:

    def __init__(self, sesion: Session):
        self.sesion = sesion

    def buscar_vehiculo(self, patente: str):
        consulta = select(Vehiculo).where(Vehiculo.patente == patente)
        resultados = self.sesion.scalars(consulta).all()
        if len(resultados) > 0:
            return resultados[0]
        return None

    def guardar_vehiculo(self, vehiculo: Vehiculo):
        self.sesion.add(vehiculo)
        return vehiculo

    def buscar_estadia_activa(self, patente: str):
        consulta = select(Estadia).where(
            Estadia.id_vehiculo == patente,
            Estadia.salida == None
        )
        resultados = self.sesion.scalars(consulta).all()
        if len(resultados) > 0:
            return resultados[0]
        return None

    def guardar_estadia(self, estadia: Estadia):
        self.sesion.add(estadia)
        return estadia

    def buscar_suscripciones(self, patente: str):
        consulta = select(Suscripcion).where(Suscripcion.id_vehiculo == patente)
        return list(self.sesion.scalars(consulta).all())

    def guardar_suscripcion(self, suscripcion: Suscripcion):
        self.sesion.add(suscripcion)
        return suscripcion

    def guardar_pago(self, pago: Pago):
        self.sesion.add(pago)
        return pago