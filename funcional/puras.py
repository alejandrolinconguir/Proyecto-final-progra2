"""Funciones puras: su resultado depende solo de sus argumentos."""
from datetime import datetime, timedelta #Traemos dos herramientas datetime y timedelta

from dominio.errores import ValidacionError # aca traemos el error que puse agregamos anteriormente 

_UN_MINUTO = timedelta(minutes=1) #Una constante que vale un minuto


def _techo_division(duracion: timedelta, bloque: timedelta) -> int:
    """Divide duracion entre bloque y redondea siempre hacia arriba."""
    return -(-(duracion // timedelta(microseconds=1))
             // (bloque // timedelta(microseconds=1)))

 
def _duracion(ingreso: datetime, salida: datetime) -> timedelta:
    if salida < ingreso:
        raise ValidacionError("La fecha de salida no puede ser anterior al ingreso.")
    return salida - ingreso

#Calcula cuánto tiempo estuvo el vehículo, en casoo la salida sea antes del ingreso lanza error, si no
 #devuelve la resta de las dos fechas.



def calcular_minutos(ingreso: datetime, salida: datetime) -> int:  #La función principal. Calcula la duración, la divide en minutos hacia arriba
    """Minutos a cobrar: fracción hacia arriba, mínimo 1. (1 min 10 s -> 2)."""
    return max(1, _techo_division(_duracion(ingreso, salida), _UN_MINUTO)) # y max(1, ...) asegura el mínimo de 1 minuto. Así 1 min 10 s da 2 minutos, como pide el caso 2.