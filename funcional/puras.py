"""Funciones puras: su resultado depende solo de sus argumentos."""
from datetime import datetime, timedelta #Traemos dos herramientas datetime y timedelta

from dominio.errores import ValidacionError # aca traemos el error que puse agregamos anteriormente 

_UN_MINUTO = timedelta(minutes=1) #Una constante que vale un minuto
_UN_DIA = timedelta(hours=24) # Una constante que vale un bloque de 24 horas, es el bloque que usamos para cobrar por día
DURACION_SUSCRIPCION_DIAS = 30 # Una suscripción mensual dura exactamente 30 días consecutivos


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


def calcular_dias(ingreso: datetime, salida: datetime) -> int:
    """Bloques de 24 h a cobrar, mínimo 1. (24 h -> 1; 24 h 1 min -> 2)."""
    # Es igual a calcular_minutos, pero el bloque es de 24 horas en vez de 1 minuto, que eraa el anteriorrr.
    # _duracion calcula cuánto estuvo y valida las fechas, _techo_division lo divide
    # en días redondeando hacia arriba, y max(1, ...) asegura el mínimo de 1 día.
    return max(1, _techo_division(_duracion(ingreso, salida), _UN_DIA))


def fecha_termino_suscripcion(inicio: datetime) -> datetime:
    """Fin (exclusivo) de una suscripción de 30 días que parte en `inicio`."""
    # Suma 30 días a la fecha de inicio y devuelve la fecha en que termina la suscripción.
    return inicio + timedelta(days=DURACION_SUSCRIPCION_DIAS)


def esta_vigente(inicio: datetime, termino: datetime, ahora: datetime) -> bool:
    """Vigente desde `inicio` (inclusive) hasta `termino` (exclusive)."""
    # Devuelve True si "ahora" está dentro del período de la suscripción.
    # inicio <= ahora: el inicio cuenta como vigente (inclusive).
    # ahora < termino: en la fecha exacta de término ya NO está vigente (exclusive).
    # La fecha de referencia "ahora" llega como argumento, por eso la función es pura.
    return inicio <= ahora < termino


def hay_superposicion(inicio_a: datetime, termino_a: datetime,
                      inicio_b: datetime, termino_b: datetime) -> bool:
    """True si dos períodos [inicio, termino) se superponen."""
    # Compara dos períodos, que en este caso son A y B, y devuelve True si se cruzan en el tiempo.
    # Se superponen cuando A empieza antes de que B termine Y B empieza antes de que A termine.
    # Usamos < (y no <=) porque el término es exclusivo: si uno termina justo
    # cuando el otro empieza, NO hay superposición.
    return inicio_a < termino_b and inicio_b < termino_a