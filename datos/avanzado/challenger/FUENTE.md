# Juntas tóricas de los vuelos anteriores al Challenger (datos públicos)

## Origen
- **Repositorio:** UCI Machine Learning Repository, «Challenger USA Space Shuttle O-Ring». https://archive.ics.uci.edu/dataset/92/challenger+usa+space+shuttle+o+ring
- **Ficheros originales** (descargados el 15-10-2026 en `original/`):
  - `o-ring-erosion-only.data`: juntas con erosión.
  - `o-ring-erosion-or-blowby.data`: juntas con erosión o con fuga de gases.
  - URL: https://archive.ics.uci.edu/ml/machine-learning-databases/space-shuttle/
- **Estudio de referencia:** Dalal, S. R., Fowlkes, E. B. y Hoadley, B. (1989). «Risk Analysis of the Space Shuttle: Pre-Challenger Prediction of Failure». *Journal of the American Statistical Association*, 84(408), 945-957.
- **Licencia:** el repositorio de la UCI publica sus conjuntos de datos con licencia CC BY 4.0. Atribución: «UCI Machine Learning Repository, Challenger USA Space Shuttle O-Ring; Dalal, Fowlkes y Hoadley (1989)».

## Contenido de `vuelos_previos.csv`
Hay 23 vuelos anteriores al accidente del 28-1-1986, uno por fila.

| Columna | Significado |
| --- | --- |
| `orden_vuelo` | Orden temporal del vuelo (1 a 23) |
| `temperatura_F`, `temperatura_C` | Temperatura en el lanzamiento (°F, y su conversión a °C con un decimal) |
| `presion_psi` | Presión de la prueba de estanqueidad |
| `juntas_en_riesgo` | Juntas tóricas que podían fallar (siempre 6) |
| `juntas_con_erosion` | Juntas con erosión |
| `juntas_con_erosion_o_fuga` | Juntas con erosión o fuga de gases |

## Cifras comprobadas con el fichero
- Temperaturas de lanzamiento entre 53 °F (11,7 °C) y 81 °F (27,2 °C). La noche del accidente hizo mucho más frío que en cualquier vuelo anterior: Dalal, Fowlkes y Hoadley usan unos 31 °F (−0,6 °C).
- 7 de los 23 vuelos tuvieron alguna junta con erosión o fuga.
- Los 4 vuelos por debajo de 65 °F tuvieron daños. De los que estaban por encima, solo un 16 %.

## Uso en el curso
Curso avanzado, J4, bloque 4.4: la anécdota del Challenger. La lección es que mirar solo los vuelos con daños esconde la relación. Al añadir los vuelos sin daño, el efecto del frío salta a la vista.
