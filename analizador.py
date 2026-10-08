"""Lee un CSV de ventas y saca un informe por consola."""

import argparse
import csv

ANCHO_BARRA = 28


def leer_ventas(ruta):
    """Devuelve la lista de ventas del CSV, con los numeros ya convertidos."""
    ventas = []
    with open(ruta, encoding="utf-8") as fichero:
        for fila in csv.DictReader(fichero):
            ventas.append(
                {
                    "mes": fila["mes"],
                    "categoria": fila["categoria"],
                    "producto": fila["producto"],
                    "unidades": int(fila["unidades"]),
                    "ingresos": float(fila["ingresos"]),
                }
            )
    return ventas


def filtrar(ventas, mes=None, categoria=None):
    """Deja solo las ventas del mes o la categoria pedidos."""
    resultado = ventas
    if mes:
        resultado = [v for v in resultado if v["mes"].lower() == mes.lower()]
    if categoria:
        resultado = [v for v in resultado if v["categoria"].lower() == categoria.lower()]
    return resultado


def agrupar_por(ventas, clave):
    """Suma unidades e ingresos agrupando por la clave indicada.

    Devuelve una lista ordenada de mayor a menor ingreso.
    """
    grupos = {}
    for venta in ventas:
        nombre = venta[clave]
        if nombre not in grupos:
            grupos[nombre] = {"nombre": nombre, "unidades": 0, "ingresos": 0.0}
        grupos[nombre]["unidades"] += venta["unidades"]
        grupos[nombre]["ingresos"] += venta["ingresos"]
    return sorted(grupos.values(), key=lambda g: g["ingresos"], reverse=True)


def totales(ventas):
    """Totales generales: ingresos, unidades y precio medio por unidad."""
    ingresos = sum(v["ingresos"] for v in ventas)
    unidades = sum(v["unidades"] for v in ventas)
    medio = ingresos / unidades if unidades else 0.0
    return {"ingresos": ingresos, "unidades": unidades, "precio_medio": medio}


def formatear_euros(valor):
    """Formato espanol: punto para los miles y coma para los decimales."""
    texto = f"{valor:,.2f}"
    return texto.replace(",", "#").replace(".", ",").replace("#", ".") + " EUR"


def barra(valor, maximo):
    """Barra de texto proporcional al valor, para ver el reparto de un vistazo."""
    if maximo <= 0:
        return ""
    bloques = round((valor / maximo) * ANCHO_BARRA)
    return "#" * bloques


def imprimir_titulo(texto):
    print()
    print(texto.upper())
    print("-" * len(texto))


def imprimir_informe(ventas):
    if not ventas:
        print("No hay ventas que cumplan ese filtro.")
        return

    resumen = totales(ventas)

    imprimir_titulo("Resumen")
    print(f"Ingresos totales ... {formatear_euros(resumen['ingresos'])}")
    print(f"Unidades vendidas .. {resumen['unidades']}")
    print(f"Precio medio ....... {formatear_euros(resumen['precio_medio'])}")

    categorias = agrupar_por(ventas, "categoria")
    mayor = categorias[0]["ingresos"]
    imprimir_titulo("Ventas por categoria")
    for grupo in categorias:
        print(
            f"{grupo['nombre']:<14} {formatear_euros(grupo['ingresos']):>14}  "
            f"{barra(grupo['ingresos'], mayor)}"
        )

    imprimir_titulo("Cinco productos mas vendidos")
    for grupo in agrupar_por(ventas, "producto")[:5]:
        print(
            f"{grupo['nombre']:<20} {grupo['unidades']:>6} ud  "
            f"{formatear_euros(grupo['ingresos']):>14}"
        )

    meses = agrupar_por(ventas, "mes")
    imprimir_titulo("Mejor mes")
    mejor = meses[0]
    print(f"{mejor['nombre']} con {formatear_euros(mejor['ingresos'])}")


def main():
    parser = argparse.ArgumentParser(description="Informe de ventas a partir de un CSV.")
    parser.add_argument("--fichero", default="ventas.csv", help="ruta del CSV (por defecto ventas.csv)")
    parser.add_argument("--mes", help="analizar solo ese mes, por ejemplo Junio")
    parser.add_argument("--categoria", help="analizar solo esa categoria, por ejemplo Calzado")
    argumentos = parser.parse_args()

    try:
        ventas = leer_ventas(argumentos.fichero)
    except FileNotFoundError:
        print(f"No se encuentra el fichero: {argumentos.fichero}")
        return

    imprimir_informe(filtrar(ventas, argumentos.mes, argumentos.categoria))


if __name__ == "__main__":
    main()
