"""Excepciones propias del dominio del estacionamiento."""
#Que es?  un docstring: un comentario en tres comillas que describe para qué sirve el archivo. No hace nada al ejecutar, es solo documentación.

class ErrorDominio(Exception): #Creamos una clase llamada dominio quw hereda de exeption osea que es un tipo de error propio en este caso sirve como padre para todos los errores del sistema.
    """Clase base de los errores de reglas de negocio."""  # Otro docstring, ahora explicando la clase


class ValidacionError(ErrorDominio): #Creamos otra clase que hereda de ErrorDominio, se usa cuando un dato no es valido.
    """Dato inválido (patente vacía, tarifa no positiva, fechas inconsistentes...)."""#Otro docstring que explica cuando se usa.