"""Modalidades de cobro: una clase abstracta y tres clases concretas."""
# ABC y abstractmethod sirven para crear clases abstractas
from abc import ABC, abstractmethod
from datetime import datetime

from dominio.errores import ValidacionError

# Tarifas en pesos chilenos (Ojo que podemos cambiarlas pero, es más entendible asi y hay que anotarlas en el README)
TARIFA_MINUTO = 30
TARIFA_DIARIA = 12000
TARIFA_MENSUAL = 90000


class ModalidadCobro(ABC):
    """Contrato común de todas las modalidades de cobro."""

    def __init__(self, nombre: str, tarifa: int):
        # Creamos los atributos privados (con doble guion bajo) vacíos
        self.__nombre = None
        self.__tarifa = None
        # Los asignamos usando los setters, para que se validen
        self.nombre = nombre
        self.tarifa = tarifa

    @property
    def nombre(self) -> str:
        # Getter: lo que nos permite leer el nombre con modalidad.nombre
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        # Setter: valida antes de guardar. No acepta nombres vacíos.
        if not isinstance(valor, str) or not valor.strip():
            raise ValidacionError("El nombre de la modalidad no puede estar vacío.")
        self.__nombre = valor.strip().lower()

    @property
    def tarifa(self) -> int:
        # Getter: permite leer la tarifa con modalidad.tarifa
        return self.__tarifa

    @tarifa.setter
    def tarifa(self, valor) -> None:
        # Setter: la tarifa debe ser un número positivo (y no un True o un False)
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            raise ValidacionError("La tarifa debe ser un número positivo (pesos).")
        self.__tarifa = int(valor)

    @abstractmethod
    def calcular_importe(self, ingreso: datetime, salida: datetime) -> int:
        """Importe a cobrar al FINALIZAR una estadía. Cada subclase lo define."""