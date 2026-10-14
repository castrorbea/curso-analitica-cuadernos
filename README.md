# Cuadernos del curso de analítica de datos

Nueve cuadernos interactivos del curso conceptual de analítica de datos. Cada uno tiene un experimento con controles (deslizadores, botones, desplegables) y un gráfico que se actualiza solo. El título del gráfico dice la conclusión con las cifras del momento.

No hace falta saber programar ni instalar nada: se abren en Google Colab con una cuenta de Google.

## Cómo abrirlos

1. Pulsa el enlace del cuaderno en la tabla.
2. En Colab, menú **Entorno de ejecución → Ejecutar todo** (*Runtime → Run all*). La primera vez tarda unos segundos: descarga los datos de este repositorio.
3. Si Colab avisa de que el cuaderno no es de Google, pulsa **Ejecutar de todos modos**.
4. Mueve los controles y mira cómo cambia el gráfico.

| Cuaderno | Jornada y bloque | Qué se ve |
| --- | --- | --- |
| [`01_granularidad`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/01_granularidad.ipynb) | J1 · 1.3 Tipos y estructura del dato | Los mismos pasos de una pulsera cuentan cuatro historias según cómo se sumen |
| [`02_bill_gates`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/02_bill_gates.ipynb) | J2 · 2.2 Centro y dispersión | La media se dispara y la mediana ni se inmuta; con cola larga, mejor percentiles |
| [`03_medallero`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/03_medallero.ipynb) | J2 · 2.5 Tasas frente a conteos | El medallero se da la vuelta al dividir por la población |
| [`04_intervalos`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/04_intervalos.ipynb) | J3 · 3.2 Muestra, variabilidad e intervalos | Cuántos intervalos del 95 % fallan y qué ancho tienen |
| [`05_falsas_alarmas`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/05_falsas_alarmas.ipynb) | J3 · 3.4 Falsas alarmas | De cada N positivos de un test fiable, cuántos están enfermos |
| [`06_datos_torturados`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/06_datos_torturados.ipynb) | J3 · 3.4 Datos torturados | Veinte dados legales y alguno «confiesa» que está trucado |
| [`07_piloto_cafeteria`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/07_piloto_cafeteria.ipynb) | J3 · 3.5 Comparar con criterio | De dónde sale el «+17 %» de la tarjeta de la cafetería |
| [`08_estacionalidad`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/08_estacionalidad.ipynb) | J4 · 4.2 Series temporales a ojo | El semáforo cambia si comparas con el mes anterior o con el mismo mes del año pasado |
| [`09_eje_truncado`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/09_eje_truncado.ipynb) | J4 · 4.4 Visualización | Cuánto drama fabrica un eje vertical que no empieza en cero |

## Qué hay en el repositorio

- `cuadernos/`: los cuadernos y `laboratorio.py`, con los cálculos y los gráficos.
- `scripts/estilo.py`: colores, letra y formato numérico español de los gráficos.
- `fuentes/`: Source Sans 3 y Fira Sans, con licencia SIL Open Font License (ficheros `OFL_*.txt`).
- `datos/`: solo los ficheros que leen los cuadernos.

## Datos

Casi todos son **sintéticos**, generados para el curso: la pulsera de actividad, el bar y las incidencias, los caramelos, el test, los dados, la cadena de cafeterías Café Molienda y el servicio de bicicletas BiciCiudad. Son inventados y no proceden de ninguna organización.

La única excepción es `datos/publicos/medallero/medallero_y_poblacion.csv`. Combina dos fuentes:
- el medallero de París 2024 de Wikipedia («2024 Summer Olympics medal table», revisión 1377825167, a partir del COI; texto con licencia CC BY-SA 4.0);
- la población de 2023 del Banco Mundial (indicador SP.POP.TOTL, licencia CC BY 4.0).
