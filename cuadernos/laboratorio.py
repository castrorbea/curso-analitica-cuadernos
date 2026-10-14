"""Laboratorio de los cuadernos interactivos del curso conceptual de analítica de datos.

Cada cuaderno importa este módulo y llama a una función `dibujar_…` con los
valores de sus controles. Así las celdas de los cuadernos quedan cortas y las
funciones se pueden probar fuera de Jupyter (`scripts/cuadernos/probar.py`).

Todas las funciones de dibujo devuelven una figura de matplotlib. El título de
la figura es la conclusión, calculada con las cifras del momento, y se guarda
también en `fig.titular` para poder comprobarlo en las pruebas.

Convenciones de color (las de `scripts/estilo.py`):
- azul: la serie que importa;
- gris: el contexto;
- naranja: los avisos (lo que falla, lo que engaña).
"""

import functools
import io
import math
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

import estilo
from estilo import GRIS, NARANJA, REJILLA, TEXTO, TEXTO_2, formato_eje, num

AZUL = estilo.SERIES[0]  # el azul principal de la paleta del curso: la serie destacada
FONDO_SUAVE = "#F2F6F8"
ROJO, VERDE = "#C8433A", "#2E8540"  # solo para el semáforo, siempre con icono y texto

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
MESES_CORTOS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
DIAS_CORTOS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]

# Letra grande para proyectar: 16 pt en ejes y etiquetas, 19 pt en el título.
RC = {
    "font.size": 16, "axes.labelsize": 16, "xtick.labelsize": 16, "ytick.labelsize": 16,
    "legend.fontsize": 16, "axes.titlesize": 17, "axes.titlepad": 12, "lines.linewidth": 3,
}
ANCHO_TITULO = 80  # caracteres por línea del título antes de partirlo


# ---------------------------------------------------------------------------
# Utilidades comunes
# ---------------------------------------------------------------------------

def con_estilo(funcion):
    """Dibuja con la letra grande de proyección (sin tocar el estilo global)."""
    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        with plt.rc_context(RC):
            return funcion(*args, **kwargs)
    return envoltura


def figura(titulo, subtitulo=None, columnas=1, anchos=None, alto=5.6, ancho=12.0):
    """Crea una figura de unas 12 × 6 pulgadas con cabecera (título y subtítulo) y `columnas` paneles."""
    lineas = textwrap.wrap(titulo, ANCHO_TITULO)
    alto_cabecera = 0.42 * len(lineas) + (0.42 if subtitulo else 0.0) + 0.12
    fig = plt.figure(figsize=(ancho, alto + alto_cabecera), layout="constrained")
    rejilla = fig.add_gridspec(2, columnas, height_ratios=[alto_cabecera, alto], width_ratios=anchos)
    cabecera = fig.add_subplot(rejilla[0, :])
    cabecera.axis("off")
    cabecera.text(0, 1, "\n".join(lineas), transform=cabecera.transAxes, va="top", ha="left",
                  fontsize=19, fontweight="bold", color=TEXTO, linespacing=1.2,
                  fontfamily=[estilo.TITULOS, "Source Sans 3", "DejaVu Sans"])
    if subtitulo:
        cabecera.text(0, 0, subtitulo, transform=cabecera.transAxes, va="bottom", ha="left",
                      fontsize=16, color=TEXTO_2)
    ejes = [fig.add_subplot(rejilla[1, i]) for i in range(columnas)]
    for ax in ejes:
        ax.tick_params(labelsize=16)
    fig.titular = titulo
    return fig, ejes


def a_png(fig, dpi=110):
    """Convierte la figura en PNG (bytes) y la cierra."""
    with plt.rc_context(RC):
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=dpi)
    plt.close(fig)
    return buffer.getvalue()


def mostrar(fig):
    """Enseña la figura en el cuaderno. Funciona sea cual sea el motor gráfico activo."""
    from IPython.display import Image, display
    display(Image(a_png(fig)))


def guardar(fig, ruta):
    """Guarda la figura en un PNG (para las pruebas)."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(a_png(fig, dpi=100))
    return ruta


def con_signo(x, decimales=1):
    """+16,7 / −3,2 (con el signo menos tipográfico)."""
    texto = num(abs(x), decimales)
    if round(x, decimales) > 0:
        return "+" + texto
    if round(x, decimales) < 0:
        return "−" + texto
    return texto


def casos(x):
    """Número de personas: sin decimales si es entero; si no, con uno o dos."""
    if abs(x - round(x)) < 1e-9:
        return num(round(x))
    if x < 1:  # dos cifras significativas: 0,5 / 0,05 / 0,001
        return f"{x:.2g}".replace(".", ",")
    texto = num(x, 1)
    return texto[:-2] if texto.endswith(",0") else texto


def plural(x, singular, plural_):
    """«1 positivo» / «9,5 positivos»."""
    return f"{casos(x)} {singular if casos(x) == '1' else plural_}"


def euros(x):
    """1.613 millones de € / 2,5 millones de € / 1 millón de € / 30.000 €."""
    if abs(x) >= 1e6:
        m = x / 1e6
        decimales = 0 if (abs(m - round(m)) < 1e-9 or abs(m) >= 10) else 1
        unidad = "millón" if round(m, decimales) == 1 else "millones"
        return f"{num(m, decimales)} {unidad} de €"
    return f"{num(x)} €"


def quitar_marco(ax):
    for lado in ("left", "right", "top", "bottom"):
        ax.spines[lado].set_visible(False)


# ---------------------------------------------------------------------------
# 01 · Granularidad: la pulsera de actividad
# ---------------------------------------------------------------------------

def cargar_pulsera(datos):
    base = Path(datos) / "sinteticos" / "pulsera_actividad"
    return {
        "hora": pd.read_csv(base / "pasos_por_hora.csv", parse_dates=["Fecha"]),
        "dia": pd.read_csv(base / "pasos_por_dia.csv", parse_dates=["Fecha"]),
        "mes": pd.read_csv(base / "pasos_por_mes.csv"),
    }


def etiqueta_semana(lunes):
    lunes = pd.Timestamp(lunes)
    domingo = lunes + pd.Timedelta(days=6)
    if lunes.month == domingo.month:
        return f"{lunes.day} al {domingo.day} de {MESES[lunes.month - 1]}"
    return f"{lunes.day} de {MESES[lunes.month - 1]} al {domingo.day} de {MESES[domingo.month - 1]}"


def semanas_pulsera():
    """Opciones del desplegable: todas las semanas completas (de lunes a domingo) de 2025."""
    lunes = pd.date_range("2025-01-06", "2025-12-22", freq="W-MON")
    return [(etiqueta_semana(d), d.strftime("%Y-%m-%d")) for d in lunes]


HORAS_TRABAJO = [8, 9, 18, 19]  # ida (8 y 9 h) y vuelta (18 y 19 h)


@con_estilo
def dibujar_granularidad(pulsera, nivel="hora", semana="2025-03-03"):
    """Los mismos pasos agregados por hora (una semana), por día, por semana o por mes."""
    if nivel == "hora":
        return _pulsera_por_hora(pulsera["hora"], semana)
    if nivel == "dia":
        return _pulsera_por_dia(pulsera["dia"])
    if nivel == "semana":
        return _pulsera_por_semana(pulsera["dia"])
    return _pulsera_por_mes(pulsera["mes"], pulsera["dia"])


def _pulsera_por_hora(hora, semana):
    inicio = pd.Timestamp(semana)
    sel = hora[(hora["Fecha"] >= inicio) & (hora["Fecha"] < inicio + pd.Timedelta(days=7))].reset_index(drop=True)
    laborable = (sel["Fecha"].dt.dayofweek < 5).to_numpy()
    trabajo = laborable & sel["Hora"].isin(HORAS_TRABAJO).to_numpy()
    cuota = sel["Pasos"][trabajo].sum() / max(sel["Pasos"][laborable].sum(), 1)

    etiqueta = etiqueta_semana(inicio)
    if cuota >= 0.6:
        titulo = (f"Semana del {etiqueta}: el {num(100 * cuota)} % de los pasos de lunes a viernes "
                  "se da en 4 horas, las de ir y volver del trabajo")
    else:
        titulo = (f"Semana del {etiqueta}: las horas de ir y volver del trabajo solo suman el "
                  f"{num(100 * cuota)} % de los pasos. No es una semana normal")
    fig, (ax,) = figura(titulo, "Pasos por hora, de lunes a domingo. En azul, las 8, las 9, las 18 y las 19 h "
                                 "de lunes a viernes")
    x = np.arange(len(sel))
    ax.bar(x, sel["Pasos"], width=0.9, color=np.where(trabajo, AZUL, GRIS))
    for d in range(1, 7):
        ax.axvline(24 * d - 0.5, color=REJILLA, linewidth=1.5)
    fechas = inicio + pd.to_timedelta(np.arange(7), unit="D")
    ax.set_xticks(24 * np.arange(7) + 11.5, [f"{DIAS_CORTOS[i]} {f.day}" for i, f in enumerate(fechas)])
    ax.tick_params(axis="x", length=0)
    ax.set_xlim(-1, len(sel))
    ax.set_ylim(0, max(sel["Pasos"].max() * 1.18, 1000))
    formato_eje(ax)
    ax.set_ylabel("Pasos en la hora")
    # Anotación directa sobre la hora con más pasos.
    i = int(sel["Pasos"].idxmax())
    f = sel.loc[i]
    ax.annotate(f"{DIAS_CORTOS[f['Fecha'].dayofweek]} a las {f['Hora']} h: {num(f['Pasos'])} pasos",
                (i, f["Pasos"]), xytext=(8, 4), textcoords="offset points", fontsize=15, color=TEXTO_2,
                ha="left" if i < 120 else "right", va="bottom")
    return fig


def _pulsera_por_dia(dia):
    sel = dia[dia["Fecha"] < "2025-04-01"]
    sabado = (sel["Fecha"].dt.dayofweek == 5).to_numpy()
    media_sab = sel["Pasos"][sabado].mean()
    media_lab = sel.loc[sel["Tipo de día"] == "laborable", "Pasos"].mean()
    titulo = (f"Por día, deportista de fin de semana: los sábados camina {num(media_sab)} pasos; "
              f"los días laborables, {num(media_lab)}")
    fig, (ax,) = figura(titulo, "Pasos al día, de enero a marzo de 2025. En azul, los sábados")
    ax.bar(sel["Fecha"], sel["Pasos"], width=0.85, color=np.where(sabado, AZUL, GRIS))
    ax.axhline(media_lab, color=TEXTO_2, linewidth=1.5, linestyle="--")
    ax.text(sel["Fecha"].iloc[-1] + pd.Timedelta(days=1), media_lab, f" laborable\n medio:\n {num(media_lab)}",
            va="center", fontsize=15, color=TEXTO_2)
    ax.set_xticks(pd.to_datetime(["2025-01-01", "2025-02-01", "2025-03-01"]), ["enero", "febrero", "marzo"])
    ax.set_xlim(pd.Timestamp("2024-12-30"), pd.Timestamp("2025-04-01"))
    formato_eje(ax)
    ax.set_ylabel("Pasos en el día")
    return fig


def _pulsera_por_semana(dia):
    d = dia.copy()
    d["Lunes"] = d["Fecha"] - pd.to_timedelta(d["Fecha"].dt.dayofweek, unit="D")
    semanas = d.groupby("Lunes").agg(
        pasos=("Pasos", "mean"),
        vacaciones=("Tipo de día", lambda s: s.str.contains("senderismo").sum()),
        enferma=("Tipo de día", lambda s: (s == "enferma").sum()),
    )
    colores = np.where(semanas["vacaciones"] >= 4, AZUL, np.where(semanas["enferma"] >= 4, NARANJA, GRIS))
    maxima, minima = semanas["pasos"].max(), semanas["pasos"].min()
    titulo = (f"Por semana salen dos sorpresas: agosto de vacaciones ({num(maxima)} pasos al día) "
              f"y una semana de noviembre en cama ({num(minima)})")
    fig, (ax,) = figura(titulo, "Pasos medios al día de cada semana de 2025 (de lunes a domingo)")
    ax.bar(semanas.index + pd.Timedelta(days=3), semanas["pasos"], width=6, color=colores)
    vac = semanas[semanas["vacaciones"] >= 4]
    ax.annotate("vacaciones\nde senderismo", (vac.index[0] + pd.Timedelta(days=3), vac["pasos"].max()),
                xytext=(-20, -10), textcoords="offset points", ha="right", va="top", fontsize=15, color=AZUL)
    enf = semanas[semanas["enferma"] >= 4]
    x_enf = enf.index[0] + pd.Timedelta(days=3)
    ax.annotate("semana\nen cama", (x_enf, enf["pasos"].iloc[0]), xytext=(x_enf, 10500), textcoords="data",
                ha="center", va="bottom", fontsize=15, color=NARANJA,
                arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=1.5))
    _ejes_meses(ax)
    formato_eje(ax)
    ax.set_ylabel("Pasos medios al día")
    return fig


def _pulsera_por_mes(mes, dia):
    agosto = mes["Mes"] == "ago"
    media_ago = dia.loc[dia["Fecha"].dt.month == 8, "Pasos"].mean()
    media_resto = dia.loc[dia["Fecha"].dt.month != 8, "Pasos"].mean()
    titulo = (f"Por mes, agosto lo cambia todo: {num(media_ago)} pasos al día, "
              f"{num(media_ago / media_resto, 1)} veces más que el resto del año")
    fig, (ax,) = figura(titulo, "Pasos medios al día de cada mes de 2025")
    ax.bar(range(12), mes["Pasos medios al día"], width=0.7, color=np.where(agosto, AZUL, GRIS))
    for i, v in enumerate(mes["Pasos medios al día"]):
        ax.text(i, v + 250, num(v), ha="center", va="bottom", fontsize=14, color=TEXTO_2)
    enferma = dia.loc[dia["Tipo de día"] == "enferma", "Pasos"].mean()
    ax.annotate(f"aquí dentro hay una semana en\ncama ({num(enferma)} pasos al día):\nen el mes casi no se nota",
                (10, mes["Pasos medios al día"].iloc[10] + 1000), xytext=(10, 13500), ha="center", va="bottom",
                fontsize=15, color=NARANJA, arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=1.5))
    ax.set_xticks(range(12), MESES_CORTOS)
    ax.set_ylim(0, 20000)
    formato_eje(ax)
    ax.set_ylabel("Pasos medios al día")
    return fig


def _ejes_meses(ax, anio=2025):
    inicios = pd.date_range(f"{anio}-01-01", periods=12, freq="MS")
    ax.set_xticks(inicios + pd.Timedelta(days=14), MESES_CORTOS)
    ax.tick_params(axis="x", length=0)
    ax.set_xlim(pd.Timestamp(f"{anio - 1}-12-28"), pd.Timestamp(f"{anio + 1}-01-04"))


# ---------------------------------------------------------------------------
# 02 · Bill Gates en el bar e incidencias con cola larga
# ---------------------------------------------------------------------------

def cargar_bar(datos):
    """Los 30 clientes habituales del bar (el 31.º del fichero es el milmillonario)."""
    bar = pd.read_csv(Path(datos) / "sinteticos" / "incidencias_cola_larga" / "bar_clientes.csv")
    return bar.iloc[:30, 1].to_numpy(dtype=float)


def opciones_ingresos():
    """Valores del deslizador de ingresos, de 0 a 50.000 millones en escala logarítmica."""
    valores = [0, 10_000, 30_000, 100_000, 300_000, 1e6, 3e6, 1e7, 3e7, 1e8, 3e8, 1e9, 3e9, 1e10, 5e10]
    return [(euros(v).replace(" de €", ""), float(v)) for v in valores]


@con_estilo
def dibujar_bar(clientes, ingresos_nuevo=5e10, cuantos=1):
    """Media y mediana de los ingresos del bar cuando entran `cuantos` clientes con `ingresos_nuevo` cada uno."""
    todos = np.concatenate([clientes, np.full(cuantos, float(ingresos_nuevo))])
    media, mediana = todos.mean(), np.median(todos)
    media0, mediana0 = clientes.mean(), np.median(clientes)

    if cuantos == 0:
        titulo = f"Sin recién llegados, la media ({euros(media0)}) y la mediana ({euros(mediana0)}) casi coinciden"
    else:
        quien = "un cliente" if cuantos == 1 else f"{cuantos} clientes"
        cada = "" if cuantos == 1 else " cada uno"
        verbo = "sube" if media > media0 + 0.5 else ("baja" if media < media0 - 0.5 else "se queda")
        titulo = (f"Entra{'' if cuantos == 1 else 'n'} {quien} con {euros(ingresos_nuevo)}{cada}: la media {verbo} "
                  f"a {euros(media)} y la mediana se queda en {euros(mediana)}")
    fig, (ax,) = figura(titulo, "Ingresos anuales de los clientes del bar. Cada punto es una persona")

    # Eje x: hasta 60.000 €, o más si los recién llegados caben sin aplastar al resto.
    visibles = cuantos > 0 and ingresos_nuevo <= 300_000
    xmax = max(65_000, ingresos_nuevo * 1.12) if visibles else 65_000

    # Puntos apilados como en un histograma: cada persona es un punto, en el centro de su tramo.
    ancho = xmax / 30
    def apilar(valores, base=None):
        base = {} if base is None else base
        xs, ys = [], []
        for v in valores:
            caja = int(v // ancho)
            base[caja] = base.get(caja, 0) + 1
            xs.append((caja + 0.5) * ancho)
            ys.append(base[caja])
        return np.array(xs), np.array(ys), base
    xs, ys, pilas = apilar(clientes)
    ax.scatter(xs, ys, s=420, color=GRIS, edgecolor="white", linewidth=1.5, zorder=3)
    if visibles:
        xn, yn, _ = apilar(np.full(cuantos, float(ingresos_nuevo)), pilas)
        ax.scatter(xn, yn, s=420, color=TEXTO, edgecolor="white", linewidth=1.5, zorder=3)
    techo = max(8, (max(pilas.values()) if pilas else 1) + 4)
    ax.set_ylim(0, techo)
    ax.set_xlim(-xmax * 0.02, xmax)

    # Mediana (azul) y media (naranja), con etiqueta directa.
    ax.axvline(mediana, color=AZUL, linewidth=3, zorder=2)
    ax.text(mediana, techo * 0.97, f" mediana: {euros(mediana)} ", color=AZUL, fontsize=16, va="top",
            ha="left" if mediana < xmax * 0.6 else "right", fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1), zorder=4)
    if media <= xmax:
        ax.axvline(media, color=NARANJA, linewidth=3, linestyle="--", zorder=2)
        ax.text(media, techo * 0.84, f" media: {euros(media)} ", color=NARANJA, fontsize=16, va="top",
                ha="left" if media < xmax * 0.6 else "right", fontweight="bold",
                bbox=dict(facecolor="white", edgecolor="none", pad=1), zorder=4)
    else:
        ax.annotate(f"la media se ha ido a\n{euros(media)}", (xmax, techo * 0.72), xytext=(xmax * 0.72, techo * 0.72),
                    color=NARANJA, fontsize=16, fontweight="bold", va="center", ha="center",
                    arrowprops=dict(arrowstyle="-|>", color=NARANJA, linewidth=2.5, mutation_scale=25))
    if cuantos > 0 and not visibles:
        quien = "el recién llegado" if cuantos == 1 else f"los {cuantos} recién llegados"
        ax.annotate(f"{quien}:\n{euros(ingresos_nuevo)}", (xmax, techo * 0.42), xytext=(xmax * 0.72, techo * 0.42),
                    color=TEXTO, fontsize=16, va="center", ha="center",
                    arrowprops=dict(arrowstyle="-|>", color=TEXTO, linewidth=2.5, mutation_scale=25))
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.grid(False)
    formato_eje(ax, "x", sufijo=" €")
    ax.set_xlabel("Ingresos anuales")
    return fig


def cargar_incidencias(datos):
    tabla = pd.read_csv(Path(datos) / "sinteticos" / "incidencias_cola_larga" / "incidencias.csv")
    return tabla["Horas hasta resolver"].to_numpy(dtype=float)


@con_estilo
def dibujar_incidencias(horas, percentil=90, quitar_largas=False):
    """Histograma de tiempos de resolución con media, mediana y el percentil elegido."""
    largas = horas > 24 * 7
    datos = horas[~largas] if quitar_largas else horas
    media, mediana = datos.mean(), np.median(datos)
    valor_p = np.percentile(datos, percentil)
    antes_de_la_media = (datos < media).mean()

    titulo = (f"La media ({num(media, 1)} h) engaña: el {num(100 * antes_de_la_media)} % se resuelve antes. "
              f"Mejor decir «{percentil} de cada 100, en menos de {num(valor_p, 1)} h»")
    sub = "Horas hasta resolver cada incidencia (2.000 incidencias)"
    if quitar_largas:
        sub = f"Horas hasta resolver, sin las {largas.sum()} incidencias que pasan de una semana"
    fig, (ax,) = figura(titulo, sub)

    tope = 72
    ax.hist(datos[datos <= tope], bins=np.arange(0, tope + 2, 2), color=GRIS, edgecolor="white")
    techo = ax.get_ylim()[1] * 1.15
    ax.set_ylim(0, techo)
    ax.set_xlim(0, tope + 1)
    cola = datos[datos > tope]
    if len(cola):
        ax.text(tope, techo * 0.40, f"y {len(cola)} incidencias más allá de {tope} h,\nhasta {num(cola.max())} h "
                f"({num(cola.max() / 24)} días) →", ha="right", va="center", fontsize=15, color=TEXTO_2)

    lineas = [(mediana, f"mediana: {num(mediana, 1)} h", AZUL, "-", 0.96),
              (media, f"media: {num(media, 1)} h", NARANJA, "--", 0.84),
              (valor_p, f"percentil {percentil}: {num(valor_p, 1)} h", TEXTO, ":", 0.72)]
    for x, texto, color, estilo_linea, altura in lineas:
        if x <= tope:
            ax.axvline(x, color=color, linewidth=3, linestyle=estilo_linea)
            ax.text(x + 0.6, techo * altura, texto, color=color, fontsize=16, fontweight="bold", va="top")
        else:
            ax.text(tope, techo * altura, f"{texto} →", color=color, fontsize=16, fontweight="bold",
                    va="top", ha="right")
    formato_eje(ax)
    ax.set_xlabel("Horas hasta resolver")
    ax.set_ylabel("Incidencias")
    return fig


# ---------------------------------------------------------------------------
# 03 · El medallero: total frente a por habitante
# ---------------------------------------------------------------------------

def cargar_medallero(datos):
    m = pd.read_csv(Path(datos) / "publicos" / "medallero" / "medallero_y_poblacion.csv")
    m["Por millón"] = m["Medallas totales"] / m["Población 2023"] * 1e6
    return m


OPCIONES_POBLACION = [("Sin mínimo", 0), ("100.000", 100_000), ("1 millón", 1_000_000),
                      ("5 millones", 5_000_000), ("10 millones", 10_000_000)]


def _ranking(m, criterio):
    if criterio == "total":
        return m.sort_values(["Medallas totales", "Oros", "Platas"], ascending=False).reset_index(drop=True)
    return m.dropna(subset=["Por millón"]).sort_values("Por millón", ascending=False).reset_index(drop=True)


def habitantes(p):
    if p < 1e6:
        return f"{num(round(p, -3))} hab."
    return f"{num(p / 1e6, 1 if p < 1e7 else 0)} mill. hab."


@con_estilo
def dibujar_medallero(medallero, poblacion_minima=0, criterio="total"):
    """Top 15 de París 2024 por medallas totales o por millón de habitantes."""
    m = medallero if poblacion_minima == 0 else medallero[medallero["Población 2023"] >= poblacion_minima]
    rk = _ranking(m, criterio)
    otro = _ranking(m, "por_millon" if criterio == "total" else "total")
    top, top_otro = rk.head(15), set(otro.head(15)["País"])

    def puesto(tabla, pais):
        fila = tabla.index[tabla["País"] == pais]
        return int(fila[0]) + 1 if len(fila) else None

    minimo = "" if poblacion_minima == 0 else f" (países con al menos {dict((v, k) for k, v in OPCIONES_POBLACION)[poblacion_minima].lower()} de habitantes)"
    if criterio == "total":
        a, b, c = top.iloc[0], top.iloc[1], top.iloc[2]
        titulo = (f"Por medallas totales mandan los grandes: {a['País']} ({a['Medallas totales']}), "
                  f"{b['País']} ({b['Medallas totales']}) y {c['País']} ({c['Medallas totales']})")
    else:
        a = top.iloc[0]
        titulo = (f"Por millón de habitantes gana {a['País']} ({num(a['Por millón'], 1)}) y China cae "
                  f"del puesto {puesto(otro, 'China')} al {puesto(rk, 'China')}")
    esp = puesto(rk, "España")
    sub = (f"Top 15 de París 2024{minimo}. En azul, los que también están en el top 15 del otro criterio. "
           f"España: puesto {esp} de {len(rk)}")
    fig, (ax,) = figura(titulo, sub, alto=6.4)
    if len(sub) > 115:  # el subtítulo largo se parte en dos líneas
        fig.axes[0].texts[-1].set_text(textwrap.fill(sub, 115))

    valores = top["Medallas totales"] if criterio == "total" else top["Por millón"]
    y = np.arange(len(top))[::-1]
    colores = [AZUL if p in top_otro else GRIS for p in top["País"]]
    ax.barh(y, valores, color=colores, height=0.72)
    for yi, (_, fila), v in zip(y, top.iterrows(), valores):
        if criterio == "total":
            texto = num(v)
        else:
            texto = f"{num(v, 1)}   ({fila['Medallas totales']} med. · {habitantes(fila['Población 2023'])})"
        ax.text(v + valores.max() * 0.01, yi, " " + texto, va="center", fontsize=15, color=TEXTO_2)
    ax.set_yticks(y, top["País"])
    for etiqueta in ax.get_yticklabels():
        if etiqueta.get_text() == "España":
            etiqueta.set_fontweight("bold")
    ax.set_xlim(0, valores.max() * (1.18 if criterio == "total" else 1.75))
    ax.set_ylim(-0.6, len(top) - 0.4)
    ax.xaxis.set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.grid(False)
    ax.tick_params(axis="y", length=0)
    return fig


# ---------------------------------------------------------------------------
# 04 · Cien encuestas de caramelos
# ---------------------------------------------------------------------------

P_AZULES = 0.20
SEMILLA_CARAMELOS = 67  # la de datos/sinteticos/caramelos_intervalos: fallan 5 de 100
Z = {80: 1.2816, 90: 1.6449, 95: 1.96, 99: 2.5758}
TAMANOS = [25, 50, 100, 200, 500, 1000, 2000]


def cargar_caramelos(datos):
    return pd.read_csv(Path(datos) / "sinteticos" / "caramelos_intervalos" / "intervalos_docente.csv")


def simular_encuestas(n=200, nivel=95, semilla=SEMILLA_CARAMELOS, encuestas=100):
    """Igual que scripts/sinteticos/caramelos_intervalos.py: proporción ± z errores estándar."""
    rng = np.random.default_rng(semilla)
    azules = rng.binomial(n, P_AZULES, encuestas)
    p = azules / n
    ee = np.sqrt(p * (1 - p) / n)
    inf, sup = p - Z[nivel] * ee, p + Z[nivel] * ee
    return pd.DataFrame({"p": p, "inf": inf, "sup": sup, "contiene": (inf <= P_AZULES) & (P_AZULES <= sup)})


@con_estilo
def dibujar_intervalos(n=200, nivel=95, semilla=SEMILLA_CARAMELOS):
    """La escalera de 100 intervalos: cuántos no atrapan el 20 % real y qué ancho tienen."""
    e = simular_encuestas(n, nivel, semilla)
    fallan = int((~e["contiene"]).sum())
    # Margen típico del método: z errores estándar con la proporción real (20 %). Cada
    # encuesta tiene el suyo, un poco distinto; su media sale casi igual (5,56 con 200).
    margen = 100 * Z[nivel] * math.sqrt(P_AZULES * (1 - P_AZULES) / n)
    verbo = "falla" if fallan == 1 else "fallan"
    titulo = (f"Con {num(n)} caramelos y un {nivel} % de confianza, {verbo} {fallan} de 100 encuestas "
              f"y el margen es de ±{num(margen, 1)} puntos")
    fig, (ax,) = figura(titulo, "Cada línea es una encuesta con su intervalo. En naranja, las que no atrapan "
                                "el 20 % real de azules", alto=6.4)
    y = np.arange(1, 101)
    color = np.where(e["contiene"], GRIS, NARANJA)
    ax.hlines(y, 100 * e["inf"].clip(lower=0), 100 * e["sup"], color=color, linewidth=np.where(e["contiene"], 2, 3.5))
    ax.scatter(100 * e["p"], y, s=14, color=np.where(e["contiene"], TEXTO_2, NARANJA), zorder=3)
    ax.axvline(100 * P_AZULES, color=AZUL, linewidth=3)
    ax.text(100 * P_AZULES, -3.2, "20 % real", color=AZUL, fontsize=16, fontweight="bold", ha="center", va="bottom")
    if fallan <= 12:
        for i in np.flatnonzero(~e["contiene"].to_numpy()):
            fila = e.iloc[i]
            ax.text(100 * fila["sup"] + 0.6, i + 1, f"n.º {i + 1}", color=NARANJA, fontsize=14,
                    va="center", ha="left", bbox=dict(facecolor="white", edgecolor="none", pad=0.5))
    ax.set_xlim(0, max(50, 10 * math.ceil(10 * e["sup"].max() + 0.05)))
    ax.set_ylim(102, -4)
    ax.set_yticks([1, 25, 50, 75, 100])
    ax.set_ylabel("Encuesta")
    ax.grid(axis="x", color=REJILLA)
    ax.grid(axis="y", visible=False)
    formato_eje(ax, "x", sufijo=" %")
    ax.set_xlabel("Porcentaje de caramelos azules en la muestra")
    return fig


# ---------------------------------------------------------------------------
# 05 · Falsas alarmas: el test de la enfermedad rara
# ---------------------------------------------------------------------------

def cargar_test(datos):
    return pd.read_csv(Path(datos) / "sinteticos" / "test_enfermedad_rara" / "resumen.csv")


OPCIONES_PREVALENCIA = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 30, 50]
OPCIONES_ACIERTO = [50, 60, 70, 80, 90, 95, 99, 99.9]


def frecuencias(prevalencia, sensibilidad, especificidad, personas=1000):
    """Cuántas personas caen en cada rama del árbol (los porcentajes, en %)."""
    enfermas = personas * prevalencia / 100
    sanas = personas - enfermas
    vp = enfermas * sensibilidad / 100  # enfermas con positivo
    fp = sanas * (1 - especificidad / 100)  # sanas con positivo: falsas alarmas
    return {"enfermas": enfermas, "sanas": sanas, "vp": vp, "fn": enfermas - vp, "fp": fp, "vn": sanas - fp,
            "positivos": vp + fp, "acierto_positivo": vp / (vp + fp) if vp + fp else float("nan")}


def frase_positivos(acierto):
    """«De cada 6 positivos, solo 1 está enfermo» o «De cada 10 positivos, 9 están enfermos»."""
    if acierto < 0.5:
        return f"De cada {num(1 / acierto)} positivos, solo 1 está enfermo"
    return f"De cada 10 positivos, {num(10 * acierto)} {'está' if round(10 * acierto) == 1 else 'están'} enfermos"


@con_estilo
def dibujar_falsas_alarmas(prevalencia=1, sensibilidad=95, especificidad=95):
    """Árbol de frecuencias sobre 1.000 personas y reparto de los positivos."""
    f = frecuencias(prevalencia, sensibilidad, especificidad)
    pct = lambda x: num(x, 1 if x != int(x) else 0) + " %"  # noqa: E731
    titulo = (f"{frase_positivos(f['acierto_positivo'])}: con un {pct(prevalencia)} de enfermos, "
              f"hay {plural(f['fp'], 'falsa alarma', 'falsas alarmas')} por {plural(f['vp'], 'acierto', 'aciertos')}")
    sub = (f"1.000 personas. Test con sensibilidad del {pct(sensibilidad)} (detecta a los enfermos) "
           f"y especificidad del {pct(especificidad)} (da negativo a los sanos)")
    fig, (ax, ax2) = figura(titulo, sub, columnas=2, anchos=[3.2, 1], alto=6.0)

    # --- Árbol ---
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def caja(x, y, texto, fondo=FONDO_SUAVE, color=TEXTO, borde=REJILLA):
        ax.text(x, y, texto, ha="center", va="center", fontsize=16, color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.55", facecolor=fondo, edgecolor=borde, linewidth=1.5), zorder=3)

    def rama(x0, y0, x1, y1, texto):
        ax.plot([x0, x1], [y0, y1], color=GRIS, linewidth=2.5, zorder=1)
        ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.35, texto, ha="center", va="bottom", fontsize=14, color=TEXTO_2,
                rotation=np.degrees(np.arctan2((y1 - y0) * 0.55, (x1 - x0))), rotation_mode="anchor")

    rama(1.1, 5, 4.1, 7.6, f"{pct(prevalencia)}")
    rama(1.1, 5, 4.1, 2.4, f"{pct(100 - prevalencia)}")
    rama(4.1, 7.6, 7.6, 9.1, f"{pct(sensibilidad)} detecta")
    rama(4.1, 7.6, 7.6, 6.2, f"{pct(round(100 - sensibilidad, 1))} se escapa")
    rama(4.1, 2.4, 7.6, 3.8, f"{pct(round(100 - especificidad, 1))} falsa alarma")
    rama(4.1, 2.4, 7.6, 0.9, f"{pct(especificidad)} acierta")
    caja(1.1, 5, "1.000\npersonas")
    caja(4.1, 7.6, plural(f["enfermas"], "enferma", "enfermas").replace(" ", "\n", 1))
    caja(4.1, 2.4, plural(f["sanas"], "sana", "sanas").replace(" ", "\n", 1))
    caja(8.3, 9.1, plural(f["vp"], "positivo", "positivos"), fondo=AZUL, color="white", borde=AZUL)
    caja(8.3, 6.2, plural(f["fn"], "negativo", "negativos"))
    caja(8.3, 3.8, plural(f["fp"], "positivo", "positivos"), fondo=NARANJA, color="white", borde=NARANJA)
    caja(8.3, 0.9, plural(f["vn"], "negativo", "negativos"))

    # --- Los positivos, todos juntos ---
    total = f["positivos"]
    ax2.bar([0], [f["vp"]], color=AZUL, width=0.6)
    ax2.bar([0], [f["fp"]], bottom=[f["vp"]], color=NARANJA, width=0.6)
    ax2.set_xlim(-0.5, 1.6)
    ax2.set_ylim(0, total * 1.12 if total else 1)
    ax2.text(0.35, f["vp"] / 2, f"{plural(f['vp'], 'enfermo', 'enfermos')}\n({num(100 * f['acierto_positivo'])} %)",
             color=AZUL, fontsize=15, fontweight="bold", va="center", ha="left")
    ax2.text(0.35, f["vp"] + f["fp"] / 2, f"{plural(f['fp'], 'sano', 'sanos')}\n({num(100 - 100 * f['acierto_positivo'])} %)",
             color=NARANJA, fontsize=15, fontweight="bold", va="center", ha="left")
    ax2.set_title(f"Los {casos(total)} positivos", loc="left", fontsize=17, color=TEXTO)
    ax2.axis("off")
    return fig


# ---------------------------------------------------------------------------
# 06 · Datos torturados: dados legales y comparaciones múltiples
# ---------------------------------------------------------------------------

SEMILLA_DADOS = 2  # la de datos/sinteticos/dados_trucados: 1 de 20 sale «sospechoso»
TIRADAS = 60


def cargar_dados(datos):
    return pd.read_csv(Path(datos) / "sinteticos" / "dados_trucados" / "resumen_dados.csv")


def p_ji2_5gl(x):
    """Probabilidad de superar x en una ji-cuadrado con 5 grados de libertad (fórmula cerrada)."""
    return math.erfc(math.sqrt(x / 2)) + math.sqrt(2 / math.pi) * math.exp(-x / 2) * (math.sqrt(x) + x**1.5 / 3)


def simular_dados(n=20, semilla=SEMILLA_DADOS):
    """Lanza n dados legales 60 veces cada uno y prueba si salen las seis caras por igual.

    Es la misma simulación de scripts/sinteticos/dados_trucados.py: con la semilla 2,
    los 20 primeros dados son exactamente los del caso del curso.
    """
    rng = np.random.default_rng(semilla)
    tiradas = rng.integers(1, 7, size=(n, TIRADAS))
    conteos = np.stack([(tiradas == c).sum(axis=1) for c in range(1, 7)], axis=1)
    esperado = TIRADAS / 6
    ji2 = ((conteos - esperado) ** 2 / esperado).sum(axis=1)
    return np.array([p_ji2_5gl(x) for x in ji2])


@con_estilo
def dibujar_dados(n=20, semilla=SEMILLA_DADOS):
    """p-valor de cada dado legal y probabilidad de que al menos uno salga «sospechoso»."""
    p = simular_dados(n, semilla)
    sospechosos = np.flatnonzero(p < 0.05)
    k = len(sospechosos)
    prob = 1 - 0.95**n
    pruebas = "1 prueba" if n == 1 else f"{n} pruebas"
    if k == 0:
        quien = "el dado legal no parece trucado" if n == 1 else f"ninguno de los {n} dados legales parece trucado"
        titulo = (f"Esta vez {quien}, pero con {pruebas} la probabilidad de un «hallazgo» "
                  f"era del {num(100 * prob)} %")
    else:
        dados = "dado legal" if n == 1 else "dados legales"
        parece = "parece trucado" if k == 1 else "parecen trucados"
        titulo = (f"{k} de {n} {dados} {parece} (p < 0,05): con {pruebas}, la probabilidad "
                  f"de al menos un «hallazgo» era del {num(100 * prob)} %")
    fig, (ax, ax2) = figura(titulo, "Cada dado se lanza 60 veces y se prueba si salen las seis caras por igual. "
                                    "Todos son legales", columnas=2, anchos=[1.7, 1])

    x = np.arange(1, n + 1)
    ax.axhspan(0, 0.05, color=NARANJA, alpha=0.12, linewidth=0)
    ax.axhline(0.05, color=NARANJA, linewidth=1.5, linestyle="--")
    ax.text(n + 0.5, 0.06, "p = 0,05", color=NARANJA, fontsize=15, ha="right", va="bottom")
    ax.scatter(x, p, s=90 if n <= 40 else 45, color=np.where(p < 0.05, NARANJA, GRIS), zorder=3)
    if 0 < k <= 6:
        for i in sospechosos:
            ax.annotate(f"dado {i + 1}", (i + 1, p[i]), xytext=(0, 40), textcoords="offset points", ha="center",
                        color=NARANJA, fontsize=15, fontweight="bold", zorder=5,
                        bbox=dict(facecolor="white", edgecolor="none", pad=1),
                        arrowprops=dict(arrowstyle="-", color=NARANJA, linewidth=1.2))
    ax.set_xlim(0, n + 1)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Dado")
    ax.set_ylabel("p-valor")
    ax.set_title("Cada punto, un dado", loc="left", fontsize=17)
    formato_eje(ax, decimales=1)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=6))

    ns = np.arange(1, 101)
    curva = 1 - 0.95**ns
    ax2.plot(ns, 100 * curva, color=AZUL)
    ax2.scatter([n], [100 * prob], s=120, color=AZUL, zorder=3)
    ax2.annotate(f"{num(100 * prob)} %", (n, 100 * prob), xytext=(12 if n < 70 else -12, -6),
                 textcoords="offset points", ha="left" if n < 70 else "right", va="top", color=AZUL,
                 fontsize=17, fontweight="bold")
    ax2.set_ylim(0, 105)
    ax2.set_xlim(0, 101)
    ax2.set_xlabel("Número de comparaciones")
    ax2.set_title("Probabilidad de algún «hallazgo»", loc="left", fontsize=17)
    formato_eje(ax2, sufijo=" %")
    return fig


# ---------------------------------------------------------------------------
# 07 · El piloto de la cafetería: de dónde sale el +17 %
# ---------------------------------------------------------------------------

INICIO_PILOTO = pd.Timestamp("2025-04-07")
PILOTO_REAL = ["T03", "T05", "T07", "T10"]
# Efecto real de la tarjeta en el generador (scripts/sinteticos/cafeteria.py): +3 % de tickets
# y +1,2 % de ticket medio, que entra poco a poco durante las cuatro primeras semanas.
EFECTO_TICKETS, EFECTO_TICKET_MEDIO = 0.03, 0.012
EFECTO_REAL = (1 + EFECTO_TICKETS) * (1 + EFECTO_TICKET_MEDIO) - 1  # ≈ +4,2 %
T_975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
         9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131}

METODOS = {
    "antes_despues": "Antes y después",
    "frente_resto": "Frente al resto en los mismos meses",
    "interanual": "Interanual frente al resto",
}
SELECCIONES = {
    "peores": "Las 4 peores del primer trimestre (el piloto real)",
    "azar": "4 al azar",
    "mejores": "Las 4 mejores del primer trimestre",
}


def factor_tarjeta(fechas):
    """Multiplicador de ventas de la tarjeta en cada fecha (1 antes del lanzamiento)."""
    rampa = np.clip((fechas - INICIO_PILOTO).dt.days.to_numpy() / 28, 0, 1)
    return (1 + EFECTO_TICKETS * rampa) * (1 + EFECTO_TICKET_MEDIO * rampa)


def cargar_cafeteria(datos):
    """Ventas diarias limpias, como en el análisis de la guía docente.

    La limpieza es la misma de scripts/sinteticos/cafeteria.py: se quita la fila
    duplicada, el día con el error de caja (99.999,99 €) y los días cerrados.
    Además se calcula `ventas_sin_tarjeta`: las ventas que habrían tenido las
    tiendas piloto si la tarjeta no hiciera nada (se divide por su efecto).
    """
    base = Path(datos) / "sinteticos" / "cafeteria" / "datos"
    v = pd.read_csv(base / "ventas_diarias.csv", parse_dates=["fecha"])
    tiendas = pd.read_csv(base / "tiendas.csv")
    v = v.drop_duplicates()
    v = v[v["ventas_eur"] / v["tickets"].where(v["tickets"] > 0) < 60].copy()
    es_piloto = v["tienda"].isin(PILOTO_REAL).to_numpy()
    v["ventas_sin_tarjeta"] = v["ventas_eur"] / np.where(es_piloto, factor_tarjeta(v["fecha"]), 1)
    return {"ventas": v.reset_index(drop=True), "tiendas": tiendas}


def _crecimiento(v, columna, desde, hasta, desde_base, hasta_base):
    """Crecimiento por tienda de la venta media por día entre dos periodos (como en la guía docente)."""
    def media(a, b):
        sel = v[(v["fecha"] >= a) & (v["fecha"] <= b)]
        return sel.groupby("tienda")[columna].mean()
    return media(desde, hasta) / media(desde_base, hasta_base) - 1


def _ic_diferencia(a, b):
    """Diferencia de medias con intervalo del 95 % (Welch), como en la guía docente."""
    a, b = np.asarray(a), np.asarray(b)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    se = math.sqrt(va + vb)
    gl = (va + vb) ** 2 / (va**2 / (len(a) - 1) + vb**2 / (len(b) - 1))
    t = T_975.get(int(gl), 2.0)
    d = a.mean() - b.mean()
    return d, d - t * se, d + t * se


def elegir_tiendas(cafe, seleccion="peores", sorteo=0):
    """Las 4 tiendas del piloto según el criterio. El primer trimestre es anterior a la tarjeta."""
    q1 = _crecimiento(cafe["ventas"], "ventas_eur", "2025-01-01", "2025-03-31", "2024-01-01", "2024-03-31")
    if seleccion == "peores":
        return sorted(q1.nsmallest(4).index)
    if seleccion == "mejores":
        return sorted(q1.nlargest(4).index)
    rng = np.random.default_rng(2025 + sorteo)
    return sorted(rng.choice(sorted(q1.index), 4, replace=False))


def medir_piloto(cafe, seleccion="peores", tarjeta_funciona=True, sorteo=0):
    """Las tres formas de medir el efecto, para las tiendas elegidas.

    Escenario: se parte de las ventas «sin tarjeta» y, si la tarjeta funciona, se
    aplica su efecto real (+4,2 %) a las tiendas elegidas desde el 7-4-2025. Con
    las 4 peores y la tarjeta funcionando, son exactamente los datos del caso.
    """
    v = cafe["ventas"].copy()
    elegidas = elegir_tiendas(cafe, seleccion, sorteo)
    sel = v["tienda"].isin(elegidas).to_numpy()
    v["escenario"] = v["ventas_sin_tarjeta"] * np.where(sel & tarjeta_funciona, factor_tarjeta(v["fecha"]), 1)

    es = lambda s: s.index.isin(elegidas)  # noqa: E731
    ingenuo = _crecimiento(v, "escenario", "2025-04-07", "2025-06-30", "2025-01-01", "2025-03-31")
    inter = _crecimiento(v, "escenario", "2025-04-07", "2025-12-31", "2024-04-07", "2024-12-31")
    efecto, bajo, alto = _ic_diferencia(inter[es(inter)], inter[~es(inter)])
    return {
        "elegidas": elegidas,
        "v": v,
        "antes_despues": ingenuo[es(ingenuo)].mean(),
        "frente_resto": ingenuo[es(ingenuo)].mean() - ingenuo[~es(ingenuo)].mean(),
        "interanual": efecto,
        "ic": (bajo, alto),
        "real": EFECTO_REAL if tarjeta_funciona else 0.0,
    }


def _valor_metodo(metodo, x):
    return f"{con_signo(100 * x)} %" if metodo == "antes_despues" else f"{con_signo(100 * x)} puntos"


@con_estilo
def dibujar_piloto(cafe, seleccion="peores", metodo="antes_despues", tarjeta_funciona=True, sorteo=0):
    """Serie de ventas del piloto frente al resto y las tres medidas del efecto."""
    r = medir_piloto(cafe, seleccion, tarjeta_funciona, sorteo)
    medido, real = r[metodo], r["real"]
    cifra = num(abs(100 * medido), 1)
    if metodo == "antes_despues":
        lead = f"Antes y después, las ventas del piloto {'suben' if medido >= 0 else 'bajan'} un {cifra} %"
    else:
        lead = f"{METODOS[metodo]}, el piloto crece {cifra} puntos {'más' if medido >= 0 else 'menos'}"
    cerca = abs(medido - real) <= 0.02
    if tarjeta_funciona:
        cola = (f": cerca del efecto real de la tarjeta ({con_signo(100 * real)} %)" if cerca
                else f", pero la tarjeta solo aporta un {con_signo(100 * real)} %")
    else:
        cola = (": cerca de cero, que es lo que hace esta tarjeta" if cerca
                else "… con una tarjeta que no hace nada")
    titulo = f"{lead}{cola}"
    nombres = cafe["tiendas"].set_index("tienda")["nombre"]
    lista = ", ".join(nombres[t] for t in r["elegidas"][:-1]) + " y " + nombres[r["elegidas"][-1]]
    escenario = ("Escenario real: la tarjeta sube las ventas un 4,2 %" if tarjeta_funciona
                 else "Escenario placebo: la tarjeta no hace nada")
    sub = f"Piloto: {lista}. {escenario}"
    fig, (ax, ax2) = figura(titulo, sub, columnas=2, anchos=[1.7, 1])

    # --- Serie mensual: índice de ventas por día (media de 2024 de cada tienda = 100) ---
    v = r["v"]
    v["mes"] = v["fecha"].dt.to_period("M")
    por_mes = v.groupby(["tienda", "mes"])["escenario"].mean().unstack()
    indice = 100 * por_mes.div(por_mes.loc[:, por_mes.columns.year == 2024].mean(axis=1), axis=0)
    fechas = indice.columns.to_timestamp() + pd.Timedelta(days=14)
    piloto = indice.loc[r["elegidas"]].mean()
    resto = indice.drop(index=r["elegidas"]).mean()

    if metodo == "interanual":
        base, despues = ("2024-04-07", "2024-12-31"), ("2025-04-07", "2025-12-31")
    else:
        base, despues = ("2025-01-01", "2025-03-31"), ("2025-04-07", "2025-06-30")
    ax.axvspan(pd.Timestamp(base[0]), pd.Timestamp(base[1]), color=GRIS, alpha=0.22, linewidth=0)
    ax.axvspan(pd.Timestamp(despues[0]), pd.Timestamp(despues[1]), color=AZUL, alpha=0.12, linewidth=0)
    ax.text(pd.Timestamp(base[1]) - pd.Timedelta(days=4), 0.99, "antes", transform=ax.get_xaxis_transform(),
            ha="right", va="top", fontsize=15, color=TEXTO_2)
    ax.text(pd.Timestamp(despues[0]) + pd.Timedelta(days=4), 0.99, "después", transform=ax.get_xaxis_transform(),
            ha="left", va="top", fontsize=15, color=AZUL)
    usa_resto = metodo != "antes_despues"
    ax.plot(fechas, resto, color=GRIS, linewidth=3, alpha=1 if usa_resto else 0.45)
    ax.plot(fechas, piloto, color=AZUL, linewidth=3.5)
    y_p, y_r = piloto.iloc[-1], resto.iloc[-1]
    separacion = 7  # puntos de índice entre las dos etiquetas, para que no se pisen
    if abs(y_p - y_r) < separacion:
        medio, signo = (y_p + y_r) / 2, (1 if y_p >= y_r else -1)
        y_p, y_r = medio + signo * separacion / 2, medio - signo * separacion / 2
    ax.text(fechas[-1] + pd.Timedelta(days=12), y_p, "piloto", color=AZUL, fontsize=16,
            fontweight="bold", va="center")
    ax.text(fechas[-1] + pd.Timedelta(days=12), y_r, "resto" if usa_resto else "resto\n(no se usa)",
            color=TEXTO_2, fontsize=15, va="center", linespacing=1.0)
    ax.axvline(INICIO_PILOTO, color=TEXTO_2, linewidth=1.2, linestyle="--")
    anios = pd.to_datetime(["2024-01-01", "2024-07-01", "2025-01-01", "2025-07-01"])
    ax.set_xticks(anios, ["ene 2024", "jul", "ene 2025", "jul"])
    ax.set_xlim(pd.Timestamp("2023-12-20"), pd.Timestamp("2026-03-15"))
    lo, hi = min(piloto.min(), resto.min()), max(piloto.max(), resto.max())
    ax.set_ylim(lo - 4, hi + 9)
    ax.set_ylabel("Ventas por día (2024 = 100)")
    formato_eje(ax)

    # --- Las tres medidas, con el efecto real como referencia ---
    claves = ["antes_despues", "frente_resto", "interanual"]
    valores = [100 * r[c] for c in claves]
    y = np.arange(3)[::-1]
    ax2.barh(y, valores, color=[AZUL if c == metodo else GRIS for c in claves], height=0.6)
    bajo, alto = (100 * x for x in r["ic"])
    ax2.plot([bajo, alto], [y[2], y[2]], color=TEXTO, linewidth=2)
    ax2.plot([bajo, bajo], [y[2] - 0.12, y[2] + 0.12], color=TEXTO, linewidth=2)
    ax2.plot([alto, alto], [y[2] - 0.12, y[2] + 0.12], color=TEXTO, linewidth=2)
    tope = max(max(valores), alto, 100 * real) + 9
    piso = min(0, min(valores), bajo) - 1.5
    for yi, c, val in zip(y, claves, valores):
        texto = _valor_metodo(c, val / 100).replace(" puntos", " pt")
        x_texto = max(val, alto) if c == "interanual" else max(val, 0)
        ax2.text(x_texto + 0.5, yi, texto, va="center", fontsize=15,
                 color=AZUL if c == metodo else TEXTO_2, fontweight="bold" if c == metodo else "normal")
    ax2.axvline(100 * real, color=NARANJA, linewidth=2.5, linestyle="--")
    ax2.text(100 * real, 2.55, f" efecto real\n {con_signo(100 * real) if real else '0'} %", color=NARANJA, fontsize=15,
             va="bottom", ha="left", fontweight="bold")
    ax2.axvline(0, color=TEXTO_2, linewidth=1)
    ax2.set_yticks(y, ["Antes y\ndespués", "Frente al\nresto", "Interanual\nfrente al resto"])
    ax2.set_xlim(piso, tope + 4)
    ax2.set_ylim(-0.6, 3.3)
    ax2.tick_params(axis="y", length=0)
    ax2.xaxis.set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.grid(False)
    return fig


# ---------------------------------------------------------------------------
# 08 · Estacionalidad: BiciCiudad y Café Molienda
# ---------------------------------------------------------------------------

def cargar_series(datos, cafe=None):
    """Viajes mensuales de BiciCiudad y ventas mensuales de las 12 cafeterías."""
    bici = pd.read_csv(Path(datos) / "sinteticos" / "cuadro_mando" / "datos" / "viajes_mensuales.csv")
    bici = pd.Series(bici["viajes"].to_numpy(dtype=float), index=pd.PeriodIndex(bici["mes"], freq="M"))
    cafe = cafe or cargar_cafeteria(datos)
    v = cafe["ventas"].copy()
    v["mes"] = v["fecha"].dt.to_period("M")
    # Ventas del mes de cada tienda = venta media por día con datos × días del mes. Así,
    # la semana sin datos de Riberas (un fallo de carga) no parece una caída de ventas.
    media = v.groupby(["mes", "tienda"])["ventas_eur"].mean().unstack()
    dias = media.index.days_in_month.to_numpy()
    ventas = pd.Series(media.mul(dias, axis=0).sum(axis=1).to_numpy(), index=media.index)
    return {"bici": bici, "cafe": ventas}


SERIES = {
    "bici": {"nombre": "Viajes de BiciCiudad", "unidad": "Viajes al mes (miles)", "escala": 1e3,
             "cosa": "los viajes"},
    "cafe": {"nombre": "Ventas de Café Molienda (12 tiendas)", "unidad": "Ventas al mes (miles de €)",
             "escala": 1e3, "cosa": "las ventas"},
}


def meses_disponibles(series, serie):
    """Meses que tienen el mismo mes del año anterior (para poder comparar de las dos formas)."""
    s = series[serie]
    validos = [m for m in s.index if (m - 12) in s.index]
    return [(f"{MESES[m.month - 1]} de {m.year}", str(m)) for m in validos]


def _nombre_mes(m):
    return f"{MESES[m.month - 1]} de {m.year}"


def _semaforo(variacion):
    """Regla del cuadro de mando: verde si sube o se mantiene, rojo si baja."""
    return ("verde", VERDE, "▲") if variacion >= 0 else ("rojo", ROJO, "▼")


@con_estilo
def dibujar_estacionalidad(series, serie="bici", mes="2025-11", comparacion="anterior"):
    """La serie año a año, el mes elegido y el semáforo que saldría con cada comparación."""
    s = series[serie] / SERIES[serie]["escala"]
    ref = pd.Period(mes, freq="M")
    otros = {"anterior": ref - 1, "interanual": ref - 12}
    var = {k: s[ref] / s[m] - 1 for k, m in otros.items()}
    comp = otros[comparacion]
    alternativa = "interanual" if comparacion == "anterior" else "anterior"
    color_txt, color, icono = _semaforo(var[comparacion])
    color_alt = _semaforo(var[alternativa])[0]

    def frase(v):
        return f"{'sube' if v >= 0 else 'cae'} un {num(abs(100 * v), 1)} %"
    nombre_ref = _nombre_mes(ref)
    titulo = (f"Frente a {_nombre_mes(comp)}, {nombre_ref} {frase(var[comparacion])}: semáforo {color_txt}. "
              f"Frente a {_nombre_mes(otros[alternativa])}, {frase(var[alternativa])}"
              f"{' y saldría ' + color_alt if color_alt != color_txt else ' (también ' + color_alt + ')'}")
    titulo = titulo[0].upper() + titulo[1:]
    fig, (ax, ax2) = figura(titulo, f"{SERIES[serie]['nombre']}. Cada línea es un año",
                            columnas=2, anchos=[2.4, 1])

    # --- La serie, un año encima de otro: la estacionalidad salta a la vista ---
    anios = sorted({m.year for m in s.index})
    for anio in anios:
        tramo = s[[m for m in s.index if m.year == anio]]
        x = [m.month for m in tramo.index]
        destacado = anio == ref.year
        ax.plot(x, tramo.values, color=AZUL if destacado else GRIS, linewidth=3.5 if destacado else 2.5,
                marker="o", markersize=5, zorder=3 if destacado else 2)
        ax.text(x[-1] + 0.2, tramo.values[-1], str(anio), color=AZUL if destacado else TEXTO_2, fontsize=15,
                fontweight="bold" if destacado else "normal", va="center")
    x_ref, x_comp = ref.month, comp.month + (12 * (comp.year - ref.year) if comparacion == "anterior" else 0)
    if comparacion == "anterior" and comp.year != ref.year:
        x_comp = 12  # diciembre del año anterior, en su propia línea
    ax.scatter([x_comp], [s[comp]], s=260, facecolor="white", edgecolor=TEXTO, linewidth=2.5, zorder=5)
    ax.scatter([x_ref], [s[ref]], s=260, color=color, zorder=6)
    ax.annotate("", (x_ref, s[ref]), xytext=(x_comp, s[comp]),
                arrowprops=dict(arrowstyle="-|>", color=color, linewidth=2.5, mutation_scale=22,
                                shrinkA=10, shrinkB=10), zorder=4)
    ax.set_xticks(range(1, 13), MESES_CORTOS)
    ax.set_xlim(0.6, 13.2)
    ax.set_ylabel(SERIES[serie]["unidad"])
    formato_eje(ax)

    # --- El semáforo ---
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0,rounding_size=0.05",
                                 facecolor=FONDO_SUAVE, edgecolor=REJILLA, linewidth=1.5))
    ax2.text(0.5, 0.9, f"{SERIES[serie]['cosa'].capitalize()} de\n{nombre_ref}", ha="center", va="top",
             fontsize=16, color=TEXTO_2)
    ax2.scatter([0.5], [0.52], s=9000, color=color, zorder=2)
    ax2.text(0.5, 0.52, icono, ha="center", va="center", fontsize=30, color="white", fontweight="bold", zorder=3)
    ax2.text(0.5, 0.3, f"{con_signo(100 * var[comparacion])} %", ha="center", va="center", fontsize=26,
             color=color, fontweight="bold")
    ax2.text(0.5, 0.15, f"frente a {_nombre_mes(comp)}", ha="center", va="center", fontsize=15, color=TEXTO_2)
    return fig


# ---------------------------------------------------------------------------
# 09 · El eje truncado: la satisfacción de BiciCiudad
# ---------------------------------------------------------------------------

def cargar_satisfaccion(datos):
    return pd.read_csv(Path(datos) / "sinteticos" / "cuadro_mando" / "datos" / "satisfaccion_2025.csv")


@con_estilo
def dibujar_eje(satisfaccion, inicio=7.9):
    """La misma bajada de la satisfacción con el eje Y empezando en `inicio`."""
    meses = satisfaccion["mes"].tolist()
    valores = satisfaccion["puntuacion_media"].to_numpy(dtype=float)
    antes, ahora = valores[-2], valores[-1]
    real = (antes - ahora) / antes  # caída de verdad
    vista = (antes - ahora) / (antes - inicio)  # caída que «ve» el ojo: la de la altura de las barras
    veces = vista / real

    if veces < 1.5:
        titulo = (f"Con el eje desde {num(inicio, 2 if inicio % 1 else 0)}, la bajada de la satisfacción "
                  f"({num(100 * real, 1)} %) se ve como lo que es: casi nada")
    else:
        titulo = (f"Con el eje desde {num(inicio, 2)}, una bajada del {num(100 * real, 1)} % parece un desplome "
                  f"del {num(100 * vista)} %: {num(veces)} veces más drama")
    fig, (ax, ax2) = figura(titulo, "Satisfacción media de BiciCiudad (de 0 a 10), de junio a noviembre de 2025",
                            columnas=2, anchos=[2, 1])

    x = np.arange(len(meses))
    ax.bar(x, valores - inicio, bottom=inicio, color=[GRIS] * (len(meses) - 1) + [AZUL], width=0.65)
    for xi, v in zip(x, valores):
        ax.text(xi, v, num(v, 2), ha="center", va="bottom", fontsize=16,
                color=AZUL if xi == x[-1] else TEXTO_2, fontweight="bold" if xi == x[-1] else "normal")
    ax.set_ylim(inicio, 8.1 + (8.1 - inicio) * 0.03)
    ax.set_xticks(x, [m.capitalize() for m in meses])
    ax.tick_params(axis="x", length=0)
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=6, steps=[1, 2, 5, 10]))
    formato_eje(ax, decimales=2 if inicio > 7 else (1 if inicio > 0 else 0))
    if inicio > 0:
        ax.spines["bottom"].set_color(NARANJA)
        ax.spines["bottom"].set_linewidth(3)
        ax.text(0.99, 0.99, f"ojo: el eje empieza en {num(inicio, 2)}, no en 0", transform=ax.transAxes,
                fontsize=15, color=NARANJA, va="top", ha="right", fontweight="bold")

    # --- Indicador: cuántas veces parece mayor la caída ---
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    ax2.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0,rounding_size=0.05",
                                 facecolor=FONDO_SUAVE, edgecolor=REJILLA, linewidth=1.5))
    ax2.text(0.5, 0.9, "La caída de noviembre\nparece", ha="center", va="top", fontsize=16, color=TEXTO_2)
    ax2.text(0.5, 0.62, f"×{num(veces, 0 if veces >= 10 else 1)}", ha="center", va="center", fontsize=46,
             fontweight="bold", color=NARANJA if veces >= 1.5 else AZUL)
    ax2.text(0.5, 0.45, "más grande de lo que es", ha="center", va="center", fontsize=16, color=TEXTO_2)
    for y, etiqueta, valor, col in [(0.29, "caída real", real, AZUL), (0.14, "caída que se ve", vista, NARANJA)]:
        ax2.text(0.08, y + 0.035, f"{etiqueta}: {num(100 * valor, 1)} %", fontsize=15, color=col, va="bottom")
        ax2.add_patch(FancyBboxPatch((0.08, y - 0.03), 0.84, 0.05, boxstyle="square,pad=0",
                                     facecolor="white", edgecolor=REJILLA))
        ax2.add_patch(FancyBboxPatch((0.08, y - 0.03), 0.84 * min(valor, 1), 0.05, boxstyle="square,pad=0",
                                     facecolor=col, edgecolor="none"))
    return fig
