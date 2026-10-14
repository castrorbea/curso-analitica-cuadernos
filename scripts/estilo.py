"""Estilo común de los gráficos del curso y utilidades de guardado.

Todos los scripts importan este módulo para que los gráficos tengan el mismo
aspecto: fondo claro, rejilla discreta, una sola paleta categórica en orden fijo
y números con formato español (1.234,5).
"""

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "datos"

# Paleta del curso: azul como color principal, turquesa y morado (oscurecido para
# que se distinga del azul con daltonismo) y gris azulado para el contexto.
# El naranja es el complementario del azul y se usa para
# destacar. Orden validado para daltonismo (series adyacentes); en gráficos de
# dispersión o pequeños múltiplos, usar como máximo dos colores más el gris.
AZUL = "#0084C9"
NARANJA = "#E07B39"
TURQUESA = "#009CA6"
MORADO = "#7E57A8"
CIAN = "#00C1D5"  # decorativo; poco contraste sobre blanco, no usar para datos
SERIES = [AZUL, NARANJA, TURQUESA, MORADO]
GRIS = "#A6BBC8"  # gris azulado: series de contexto o atenuadas
SUPERFICIE = "#FFFFFF"
TEXTO = "#1B1B1B"
TEXTO_2 = "#4F5B66"
REJILLA = "#E3E9ED"

# Tipografía: la misma de las presentaciones (Source Sans 3 para texto, Fira Sans
# para cifras destacadas), incluida en fuentes/ con licencia OFL. Si faltara, Arial.
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
for _f in (RAIZ / "fuentes").glob("*.ttf"):
    from matplotlib import font_manager as _fm

    _fm.fontManager.addfont(str(_f))
TITULOS = "Fira Sans"

plt.rcParams.update(
    {
        "figure.figsize": (8, 4.5),
        "figure.dpi": 100,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "axes.edgecolor": REJILLA,
        "axes.labelcolor": TEXTO_2,
        "axes.titlecolor": TEXTO,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 24,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "axes.prop_cycle": plt.cycler(color=SERIES),
        "grid.color": REJILLA,
        "grid.linewidth": 0.8,
        "xtick.color": TEXTO_2,
        "ytick.color": TEXTO_2,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "lines.linewidth": 2,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "font.family": ["Source Sans 3", "Arial", "DejaVu Sans"],
        "font.size": 10,
    }
)


def num(x, decimales=0):
    """Formatea un número al estilo español: 1.234,5."""
    texto = f"{x:,.{decimales}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def formato_eje(ax, eje="y", decimales=0, sufijo=""):
    """Aplica formato español a las etiquetas de un eje."""
    f = FuncFormatter(lambda v, _: num(v, decimales) + sufijo)
    (ax.yaxis if eje == "y" else ax.xaxis).set_major_formatter(f)


def subtitulo(ax, texto):
    """Línea de contexto bajo el título, en gris."""
    ax.text(0, 1.015, texto, transform=ax.transAxes, color=TEXTO_2, fontsize=9.5, va="bottom")


def fuente(fig, texto):
    """Nota de fuente al pie del gráfico."""
    fig.text(0.01, -0.02, texto, color=TEXTO_2, fontsize=8, ha="left", va="top")


def guardar_grafico(fig, carpeta, nombre):
    carpeta = Path(carpeta) / "graficos"
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"{nombre}.png"
    fig.savefig(ruta)
    plt.close(fig)
    return ruta


def guardar_tablas(carpeta, nombre, hojas):
    """Guarda cada tabla como CSV y todas juntas en un Excel con una hoja por tabla.

    `hojas` es un dict {nombre_hoja: DataFrame}.
    """
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    for hoja, df in hojas.items():
        df.to_csv(carpeta / f"{hoja}.csv", index=False, encoding="utf-8-sig")
    with __import__("pandas").ExcelWriter(carpeta / f"{nombre}.xlsx") as xl:
        for hoja, df in hojas.items():
            df.to_excel(xl, sheet_name=hoja[:31], index=False)
            ws = xl.sheets[hoja[:31]]
            for col in ws.columns:
                ancho = max(len(str(c.value)) if c.value is not None else 0 for c in col)
                ws.column_dimensions[col[0].column_letter].width = min(max(10, ancho + 2), 50)


# ---------------------------------------------------------------------------
# Gráficos para diapositivas (lienzo de 1920×1080; la zona útil mide 1664 px)
# ---------------------------------------------------------------------------

def figura_diapositiva(ancho_px=1664, alto_px=620, filas=1, columnas=1, **kwargs):
    """Figura al tamaño exacto que ocupará en la diapositiva, con letra legible.

    Se guarda a 2× con `guardar_diapositiva`. Los textos de 18 pt equivalen a unos
    25 px en la diapositiva. Sin título: el título va en la diapositiva.
    """
    escala = {
        "font.size": 22, "axes.labelsize": 21, "xtick.labelsize": 20, "ytick.labelsize": 20,
        "legend.fontsize": 20, "axes.titlesize": 22, "lines.linewidth": 3,
    }
    with plt.rc_context(escala):
        fig, ax = plt.subplots(filas, columnas, figsize=(ancho_px / 100, alto_px / 100), dpi=100, **kwargs)
    fig.patch.set_facecolor("#F5F8FA")
    for a in (ax.flat if hasattr(ax, "flat") else [ax]):
        a.set_facecolor("#F5F8FA")
        a.tick_params(labelsize=20)
    return fig, ax


def guardar_diapositiva(fig, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=200, facecolor=fig.get_facecolor(), bbox_inches=None)
    plt.close(fig)
    return ruta
