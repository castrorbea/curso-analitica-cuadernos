# Cuadernos del curso de analítica de datos

Cuadernos de los dos cursos de analítica de datos: el conceptual y el avanzado. Se abren en Google Colab con una cuenta de Google, sin instalar nada.

## Curso conceptual

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
| [`04_intervalos`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/04_intervalos.ipynb) | J3 · 3.3 Muestra, variabilidad e intervalos | Cuántos intervalos del 95 % fallan y qué ancho tienen |
| [`05_falsas_alarmas`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/05_falsas_alarmas.ipynb) | J3 · 3.5 Falsas alarmas | De cada N positivos de un test fiable, cuántos están enfermos |
| [`06_datos_torturados`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/06_datos_torturados.ipynb) | J3 · 3.5 Datos torturados | Veinte dados legales y alguno «confiesa» que está trucado |
| [`07_piloto_cafeteria`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/07_piloto_cafeteria.ipynb) | J3 · 3.6 Comparar con criterio | De dónde sale el «+17 %» de la tarjeta de la cafetería |
| [`08_estacionalidad`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/08_estacionalidad.ipynb) | J4 · 4.2 Series temporales a ojo | El semáforo cambia si comparas con el mes anterior o con el mismo mes del año pasado |
| [`09_eje_truncado`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/09_eje_truncado.ipynb) | J4 · 4.4 Visualización | Cuánto drama fabrica un eje vertical que no empieza en cero |

## Curso avanzado

Trece cuadernos de Python con el caso de BiciCiudad, uno o varios por bloque. El código está a la vista y comentado: si no programas, cambia los valores marcados con `# ←` y vuelve a ejecutar; si programas, completa los huecos marcados con `# COMPLETAD`. Empieza por `av00_preparar_datos`: descarga una vez la telemetría completa (unos 180 MB, adjunta a la [release `datos-avanzado-v1`](https://github.com/castrorbea/curso-analitica-cuadernos/releases/tag/datos-avanzado-v1)).

| Cuaderno | Jornada y bloque | Qué se ve |
| --- | --- | --- |
| [`av00_preparar_datos`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av00_preparar_datos.ipynb) | Avanzado · Jornada 1 · Bloque 1.1 | Punto de partida: descarga la telemetría completa y repasa los nueve juegos de datos con su señal. |
| [`av01_calidad_telemetria`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av01_calidad_telemetria.ipynb) | Avanzado · Jornada 1 · Bloque 1.2 | Huecos, duplicados, reinicios, valores imposibles y cambio de hora; informe de calidad de 200 bicis. |
| [`av02_anatomia_series`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av02_anatomia_series.ipynb) | Avanzado · Jornada 1 · Bloque 1.3 | Tres ritmos del uso, ACF y PACF, STL, mínimo nocturno cada 15 minutos y CUSUM para fechar una avería. |
| [`av03_inferencia_dependiente`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av03_inferencia_dependiente.ipynb) | Avanzado · Jornada 1 · Bloque 1.4 | Demo de la tarifa (t ingenuo frente a HAC), bootstrap por bloques, Holm y FDR en 40 bases, y la DiD de B-17. |
| [`av04_prevision_demanda`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av04_prevision_demanda.ipynb) | Avanzado · Jornada 2 · Bloque 2.2 | Ingenuo, ETS y boosting con origen móvil; validación aleatoria, MAPE, pinball y P90. |
| [`av05_fallo_baterias`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av05_fallo_baterias.ipynb) | Avanzado · Jornada 2 · Bloques 2.3 y 2.5 | Fuga de información, desbalance, umbral por coste, Kaplan-Meier, Cox, permutación y Shapley. |
| [`av06_anomalias`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av06_anomalias.ipynb) | Avanzado · Jornada 2 · Bloque 2.4 | Contexto, mediana y MAD, presupuesto de alarmas y tres detectores con averías sembradas. |
| [`av07_espacial_h3`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av07_espacial_h3.ipynb) | Avanzado · Jornada 3 · Bloque 3.2 | Malla H3-8: MAUP, tasas frente a conteos, suavizado bayesiano empírico, Moran, LISA y puntos calientes. |
| [`av08_red_grafo`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av08_red_grafo.ipynb) | Avanzado · Jornada 3 · Bloque 3.3 | Red de carriles con networkx: intermediación, puntos de articulación, demo de los cortes y tres tramos nuevos. |
| [`av09_cuaderno_produccion`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av09_cuaderno_produccion.ipynb) | Avanzado · Jornada 3 · Bloque 3.4 | Deriva de la telemetría, viajes como datos personales y un cuaderno «de producción» con cinco defectos. |
| [`av10_spc_xmr`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av10_spc_xmr.ipynb) | Avanzado · Jornada 4 · Bloque 4.2 | Embudo de Deming, gráfico XmR, reglas de detección, fases y objetivos con tres indicadores mensuales. |
| [`av11_spc_avanzado`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av11_spc_avanzado.ipynb) | Avanzado · Jornada 4 · Bloque 4.3 | Gráficos p y u, funnel plot, CUSUM, EWMA, ARL, demo bruto frente a residuos y ejercicio en 40 bases. |
| [`av12_caso_b23`](https://colab.research.google.com/github/castrorbea/curso-analitica-cuadernos/blob/main/cuadernos/avanzado/av12_caso_b23.ipynb) | Avanzado · Jornada 4 · Bloque 4.5 | Caso integrador: la base B-23 pierde energía desde marzo. ¿Cargadores o baterías? Nota de decisión de una página. |

## Qué hay en el repositorio

- `cuadernos/`: los cuadernos del curso conceptual y `laboratorio.py`, con los cálculos y los gráficos.
- `cuadernos/avanzado/`: los cuadernos del curso avanzado y `bici.py`, con las rutas y la descarga de la telemetría.
- `scripts/estilo.py`: colores, letra y formato numérico español de los gráficos.
- `fuentes/`: Source Sans 3 y Fira Sans, con licencia SIL Open Font License (ficheros `OFL_*.txt`).
- `datos/`: solo los ficheros que leen los cuadernos.

## Datos

Casi todos son **sintéticos**, generados para el curso: la pulsera de actividad, el bar y las incidencias, los caramelos, el test, los dados, la cadena de cafeterías Café Molienda y el servicio de bicicletas BiciCiudad. Son inventados y no proceden de ninguna organización.

La única excepción es `datos/publicos/medallero/medallero_y_poblacion.csv`. Combina dos fuentes:
- el medallero de París 2024 de Wikipedia («2024 Summer Olympics medal table», revisión 1377825167, a partir del COI; texto con licencia CC BY-SA 4.0);
- la población de 2023 del Banco Mundial (indicador SP.POP.TOTL, licencia CC BY 4.0).

En el curso avanzado, todo `datos/avanzado/` es sintético (BiciCiudad, semilla 2026; las coordenadas están en pleno Atlántico a propósito) salvo `datos/avanzado/challenger/`: las juntas tóricas de los 23 vuelos anteriores al accidente del Challenger, del UCI Machine Learning Repository (CC BY 4.0; Dalal, Fowlkes y Hoadley, 1989). Su `FUENTE.md` da los detalles.
