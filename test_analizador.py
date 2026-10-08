"""Pruebas de las funciones de calculo. Se ejecutan con: python -m unittest"""

import unittest

from analizador import agrupar_por, filtrar, formatear_euros, totales

VENTAS = [
    {"mes": "Enero", "categoria": "Camisetas", "producto": "Basica", "unidades": 10, "ingresos": 100.0},
    {"mes": "Enero", "categoria": "Calzado", "producto": "Sandalia", "unidades": 5, "ingresos": 150.0},
    {"mes": "Febrero", "categoria": "Camisetas", "producto": "Basica", "unidades": 20, "ingresos": 200.0},
]


class TestTotales(unittest.TestCase):
    def test_suma_ingresos_y_unidades(self):
        resultado = totales(VENTAS)
        self.assertEqual(resultado["ingresos"], 450.0)
        self.assertEqual(resultado["unidades"], 35)

    def test_precio_medio(self):
        self.assertAlmostEqual(totales(VENTAS)["precio_medio"], 450.0 / 35)

    def test_sin_ventas_no_divide_entre_cero(self):
        self.assertEqual(totales([])["precio_medio"], 0.0)


class TestAgrupar(unittest.TestCase):
    def test_agrupa_y_suma(self):
        grupos = agrupar_por(VENTAS, "categoria")
        camisetas = next(g for g in grupos if g["nombre"] == "Camisetas")
        self.assertEqual(camisetas["ingresos"], 300.0)
        self.assertEqual(camisetas["unidades"], 30)

    def test_ordena_de_mayor_a_menor(self):
        grupos = agrupar_por(VENTAS, "categoria")
        self.assertEqual(grupos[0]["nombre"], "Camisetas")


class TestFiltrar(unittest.TestCase):
    def test_filtra_por_mes(self):
        self.assertEqual(len(filtrar(VENTAS, mes="Enero")), 2)

    def test_no_distingue_mayusculas(self):
        self.assertEqual(len(filtrar(VENTAS, mes="enero")), 2)

    def test_combina_mes_y_categoria(self):
        resultado = filtrar(VENTAS, mes="Enero", categoria="Calzado")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["producto"], "Sandalia")


class TestFormato(unittest.TestCase):
    def test_separadores_espanoles(self):
        self.assertEqual(formatear_euros(1234.5), "1.234,50 EUR")


if __name__ == "__main__":
    unittest.main()
