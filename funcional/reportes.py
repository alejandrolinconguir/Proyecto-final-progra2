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




def filtrar_por_fechas(pagos, desde=None, hasta=None):
    """Pagos registrados entre dos fechas: desde inclusive, hasta exclusive."""
    # Usamos filter con una lambda que revisa la fecha de registro de cada pago.
    # Si "desde" es None, no se aplica límite inferior; si "hasta" es None, tampoco el superior.
    # Para los reportes por período se considera la fecha de registro del pago, como pide el enunciado.
    return list(filter(
        lambda p: (desde is None or p.fecha_registro >= desde)
        and (hasta is None or p.fecha_registro < hasta),
        pagos))


def recaudacion_por_modalidad(pagos) -> dict:
    """Devuelve cuánto se recaudó en cada modalidad, por ejemplo {'minuto': 150, ...}."""
    # Para cada modalidad: filtramos sus pagos y sumamos sus montos con las funciones de arriba.
    # Es un diccionario por comprensión: arma una entrada por cada modalidad.
    return {m: total_recaudado(filtrar_por_modalidad(pagos, m)) for m in MODALIDADES}


def resumen_recaudacion(pagos, desde=None, hasta=None) -> dict:
    """Resumen para el reporte: total, distribución por modalidad y cantidad de pagos."""
    # Primero nos quedamos con los pagos del período pedido.
    del_periodo = filtrar_por_fechas(pagos, desde, hasta)
    # Luego armamos el resumen reutilizando las funciones anteriores.
    return {"total": total_recaudado(del_periodo),
            "por_modalidad": recaudacion_por_modalidad(del_periodo),
            "cantidad_pagos": len(del_periodo)}