"""Ayudas comunes de los cuadernos del curso avanzado (BiciCiudad).

Solo lo que se repite en varios cuadernos y no enseña nada: rutas, la descarga de
la telemetría completa y el paso de UTC a hora local. El análisis va a la vista,
en las celdas de cada cuaderno.
"""

import hashlib
import urllib.request
from pathlib import Path

import pandas as pd

# La telemetría horaria completa (unos 180 MB) no cabe en git: está publicada como
# fichero adjunto de una release del repositorio público de los cuadernos.
TELEMETRIA_URL = ("https://github.com/castrorbea/curso-analitica-cuadernos/releases/download/"
                  "datos-avanzado-v1/telemetria_horaria.parquet")
TELEMETRIA_SHA256 = "c05f76a3daadafed65e129d723ecde2c9c6f9cdfdbb56b24546d88185121aaf4"
ZONA = "Europe/Madrid"


def _sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def telemetria_completa(datos):
    """Ruta de la telemetría horaria de las 2.000 bicis; la descarga una vez si no está.

    `datos` es la carpeta datos/avanzado del proyecto.
    """
    ruta = Path(datos) / "telemetria" / "completo" / "telemetria_horaria.parquet"
    if ruta.exists():
        return ruta
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_suffix(".descargando")
    print("Descargando la telemetría completa (unos 180 MB, una sola vez)…")
    urllib.request.urlretrieve(TELEMETRIA_URL, temporal)
    if _sha256(temporal) != TELEMETRIA_SHA256:
        temporal.unlink()
        raise RuntimeError("La descarga de la telemetría no coincide con la publicada. Vuelve a intentarlo.")
    temporal.rename(ruta)
    print("Hecho.")
    return ruta


def hora_local(ts_utc):
    """Convierte una columna de horas UTC (con o sin zona) a la hora de Madrid."""
    ts = pd.to_datetime(ts_utc)
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize("UTC")
    return ts.dt.tz_convert(ZONA)
