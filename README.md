# Analizador de ventas

Script de Python que lee un CSV de ventas y saca un informe por consola: totales, reparto por categoría con barras, los cinco productos más vendidos y el mejor mes.

Es el mismo análisis que hago en el panel web, pero desde la terminal y sobre un fichero, que es como suelen llegar los datos de verdad.

## Uso

Necesita Python 3, nada más. No hay que instalar ninguna librería.

```
python analizador.py
python analizador.py --mes Junio
python analizador.py --categoria Calzado
python analizador.py --fichero otras-ventas.csv
```

## Ejemplo de salida

```
RESUMEN
-------
Ingresos totales ... 65.383,00 EUR
Unidades vendidas .. 3552
Precio medio ....... 18,41 EUR

VENTAS POR CATEGORIA
--------------------
Pantalones      15.410,00 EUR  ############################
Calzado         15.368,00 EUR  ############################
Camisetas       14.685,00 EUR  ###########################
Abrigos         12.010,00 EUR  ######################
Accesorios       7.910,00 EUR  ##############
```

## Pruebas

```
python -m unittest
```

Hay nueve pruebas sobre las funciones de cálculo: que las sumas y agrupaciones salen bien, que el orden es de mayor a menor, que los filtros no distinguen mayúsculas, que no se divide entre cero cuando no hay ventas y que el formato de euros usa los separadores españoles.

## Datos

`ventas.csv` tiene datos de ejemplo inventados para la demo: una fila por producto, mes, unidades e ingresos. Para usar otro fichero basta con que tenga esas mismas columnas.
