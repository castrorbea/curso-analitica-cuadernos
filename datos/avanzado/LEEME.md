# Datos del curso avanzado (BiciCiudad)

Datos sintéticos, generados para el curso con semilla 2026. Son inventados y no proceden de ninguna organización. Las coordenadas están en pleno Atlántico a propósito: no uséis mapa de fondo. Las horas van en UTC (`ts_utc`); para presentarlas, `Europe/Madrid`.

| Carpeta | Contenido |
| --- | --- |
| `telemetria/` | Telemetría horaria de 2.000 bicis: muestra de 200, agregados y la completa, que se descarga al ejecutar `av00_preparar_datos` |
| `energia_bases/` | Energía de las 40 bases de carga cada 15 minutos, por hora y por día |
| `uso_meteo/` | Viajes por estación y hora, meteorología y calendario (36 meses) |
| `viajes_muestra/` | Viajes individuales con usuario seudónimo |
| `inventario_baterias/` | Inventario de baterías, con altas y bajas |
| `panel_baterias/` | Panel mensual de baterías con el fallo a 90 días |
| `incidencias/` | Incidencias del servicio (tres años) |
| `indicadores/` | Indicadores mensuales, bicis que comunican cada día y ARL |
| `red_carriles/` | Red de carriles bici (nodos y aristas) y tabla de estaciones |
| `malla_h3/` | Malla H3-8 con capas de contexto y pérdidas de señal |
| `embudo/` | Simulación del embudo de Deming |
| `challenger/` | Datos públicos de los 23 vuelos anteriores al Challenger (ver `FUENTE.md`) |
| `informe_comite/` | Hoja para imprimir con los cinco gráficos del ejercicio de títulos (4.4) |

Cada cuaderno explica las columnas que usa.
