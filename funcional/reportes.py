"""Consultas y reportes con programación funcional (filter, map, reduce, lambda)."""
# reduce sirve para acumular una colección de valores en uno solo
from functools import reduce

# Nombres de las tres modalidades de cobro
MODALIDADES = ("minuto", "diaria", "mensual")


def filtrar_por_modalidad(pagos, modalidad):
    """Devuelve solo los pagos de una modalidad (ej: solo los 'diaria')."""
    # filter recorre los pagos y se queda con los que cumplen la condición.
    # La condición es una lambda: una función corta sin nombre.
    # "lambda p: p.modalidad == modalidad" significa: para cada pago p, ¿su modalidad coincide?
    # list(...) convierte el resultado de filter en una lista normal.
    return list(filter(lambda p: p.modalidad == modalidad, pagos))


def total_recaudado(pagos) -> int:
    """Suma los montos de todos los pagos recibidos."""
    # reduce va acumulando: parte en 0 y, por cada pago, le suma su monto al acumulado.
    # lambda acumulado, p: acumulado + p.monto es la operación de cada vuelta.
    # El 0 del final es el valor inicial (así una lista vacía da 0 y no error).
    return reduce(lambda acumulado, p: acumulado + p.monto, pagos, 0)