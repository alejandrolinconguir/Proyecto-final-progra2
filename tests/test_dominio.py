"""Pruebas automáticas del dominio: cobros, vigencia y reportes."""
import unittest
from datetime import datetime, timedelta
# SimpleNamespace crea objetos simples con atributos, nos sirve para simular pagos sin base de datos
from types import SimpleNamespace as NS

from dominio.errores import ValidacionError
from dominio.modalidades import Diaria, Mensual, PorMinuto, crear_modalidad
from funcional.puras import esta_vigente, hay_superposicion
from funcional.reportes import resumen_recaudacion

# Fecha de referencia que usan todas las pruebas
T0 = datetime(2026, 1, 1, 10, 0, 0)


class TestCobros(unittest.TestCase):
    def test_minuto_redondea_hacia_arriba(self):
        # Caso 2 del enunciado: 1 min 10 s se cobra como 2 minutos (2 x $30 = 60)
        self.assertEqual(PorMinuto(30).calcular_importe(T0, T0 + timedelta(minutes=1, seconds=10)), 60)

    def test_minimo_un_minuto(self):
        # Si entra y sale en el mismo instante, se cobra el mínimo: 1 minuto
        self.assertEqual(PorMinuto(30).calcular_importe(T0, T0), 30)

    def test_diaria_24h_es_un_dia(self):
        # Caso 3 del enunciado: exactamente 24 horas es un día
        self.assertEqual(Diaria(1000).calcular_importe(T0, T0 + timedelta(hours=24)), 1000)

    def test_diaria_24h_1min_son_dos_dias(self):
        # Caso 3 del enunciado: 24 horas y 1 minuto son dos días
        self.assertEqual(Diaria(1000).calcular_importe(T0, T0 + timedelta(hours=24, minutes=1)), 2000)

    def test_mensual_estadia_cubierta_cuesta_cero(self):
        # Caso 4 del enunciado: la estadía cubierta cobra $0, pero contratar sí cuesta
        m = Mensual(90000)
        self.assertEqual(m.calcular_importe(T0, T0 + timedelta(days=3)), 0)
        self.assertEqual(m.importe_contratacion(), 90000)

    def test_polimorfismo_sin_condiciones(self):
        # Las tres modalidades responden al mismo método, sin if según el tipo
        for nombre in ("minuto", "diaria", "mensual"):
            self.assertGreaterEqual(crear_modalidad(nombre).calcular_importe(T0, T0 + timedelta(hours=2)), 0)

    def test_validaciones(self):
        # Caso 9 del enunciado: los datos incorrectos lanzan errores claros
        with self.assertRaises(ValidacionError):
            PorMinuto(0)  # tarifa cero
        with self.assertRaises(ValidacionError):
            Diaria(-5)  # tarifa negativa
        with self.assertRaises(ValidacionError):
            PorMinuto().calcular_importe(T0, T0 - timedelta(minutes=1))  # salida antes del ingreso


class TestVigencia(unittest.TestCase):
    def test_inicio_inclusivo_termino_exclusivo(self):
        # Caso 5 del enunciado: vigente en el inicio, vencida en el instante de término
        fin = Mensual().fecha_termino(T0)
        self.assertTrue(esta_vigente(T0, fin, T0))
        self.assertFalse(esta_vigente(T0, fin, fin))

    def test_superposicion(self):
        # Dos períodos que se cruzan se detectan; si uno parte cuando el otro termina, no hay cruce
        fin = Mensual().fecha_termino(T0)
        self.assertTrue(hay_superposicion(T0, fin, T0 + timedelta(days=10), fin + timedelta(days=10)))
        self.assertFalse(hay_superposicion(T0, fin, fin, fin + timedelta(days=30)))


class TestReportes(unittest.TestCase):
    def test_resumen(self):
        # Caso 8 del enunciado: el pago mensual se cuenta una sola vez en la recaudación
        pagos = [NS(monto=100, modalidad="minuto", fecha_registro=T0),
                 NS(monto=200, modalidad="diaria", fecha_registro=T0),
                 NS(monto=90000, modalidad="mensual", fecha_registro=T0)]
        r = resumen_recaudacion(pagos)
        self.assertEqual(r["total"], 90300)
        self.assertEqual(r["por_modalidad"]["mensual"], 90000)


if __name__ == "__main__":
    unittest.main()