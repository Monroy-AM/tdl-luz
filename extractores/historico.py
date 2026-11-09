"""Descarga la serie histórica de precios (MDA) a la capa bronce, un archivo por mes.

    python -m extractores.historico 2022

Es reanudable: los meses ya descargados (excepto el actual) no se vuelven a pedir.
"""

from __future__ import annotations

import sys
import uuid
from datetime import date, timedelta

from extractores import cenace_precios
from extractores.base import ExtractorEtico
from extractores.bronce import BRONCE, ahora_utc, guardar_bronce


def meses(desde: int):
    d = date(desde, 1, 1)
    hoy = date.today()
    while d <= hoy:
        siguiente = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        yield d, min(siguiente - timedelta(days=1), hoy)
        d = siguiente


def main(desde: int = 2022) -> None:
    ex = ExtractorEtico()
    ejecucion = "hist-" + ahora_utc().strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:4]
    hoy = date.today()
    for inicio, fin in meses(desde):
        nombre = f"pml_mda_{inicio:%Y_%m}"
        ya_existe = (BRONCE / "cenace_precios_historico" / f"{nombre}.csv").exists()
        if (inicio.year, inicio.month) != (hoy.year, hoy.month) and ya_existe:
            continue
        filas, url = [], ""
        d = inicio
        while d <= fin:
            f, url = cenace_precios.consultar(ex, d, min(d + timedelta(days=6), fin))
            filas += f
            d += timedelta(days=7)
        if filas:
            guardar_bronce("cenace_precios_historico", filas, url, ejecucion, nombre, modo="w")
        print(f"{inicio:%Y-%m}: {len(filas)} filas", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2022)
