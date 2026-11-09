"""Escritura en la capa bronce y bitacora de ejecuciones.

Bronce = datos tal como llegaron (sin limpiar), mas metadatos de captura:
  _fuente, _url, _capturado_utc, _ejecucion_id
La bitacora (calidad/bitacora_captura.csv) es la base para medir
fiabilidad, MTBF, MTTR y disponibilidad en E1 (Calidad).
"""

from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BRONCE = RAIZ / "data" / "bronce"
BITACORA = RAIZ / "calidad" / "bitacora_captura.csv"
CAMPOS_BITACORA = [
    "ejecucion_id", "fuente", "inicio_utc", "fin_utc", "duracion_s",
    "estado", "registros", "archivo", "error", "disparo",
]


def ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


def guardar_bronce(fuente: str, filas: list[dict], url: str, ejecucion_id: str,
                   nombre: str | None = None, modo: str = "a") -> Path:
    """Guarda filas crudas en data/bronce/<fuente>/<nombre o fecha>.csv con metadatos."""
    destino = BRONCE / fuente
    destino.mkdir(parents=True, exist_ok=True)
    capturado = ahora_utc().isoformat(timespec="seconds")
    nombre = nombre or ahora_utc().strftime("%Y-%m-%d")
    archivo = destino / f"{nombre}.csv"
    columnas: list[str] = []
    for f in filas:
        for k in f:
            if k not in columnas:
                columnas.append(k)
    columnas += ["_fuente", "_url", "_capturado_utc", "_ejecucion_id"]
    nuevo = modo == "w" or not archivo.exists()
    with archivo.open("w" if nuevo else "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, extrasaction="ignore")
        if nuevo:
            w.writeheader()
        for f in filas:
            meta = {"_fuente": fuente, "_url": url, "_capturado_utc": capturado, "_ejecucion_id": ejecucion_id}
            w.writerow({**f, **meta})
    return archivo


def registrar_ejecucion(**datos) -> None:
    BITACORA.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not BITACORA.exists()
    datos.setdefault("disparo", os.getenv("GITHUB_EVENT_NAME", "local"))
    with BITACORA.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS_BITACORA)
        if nuevo:
            w.writeheader()
        w.writerow({k: datos.get(k, "") for k in CAMPOS_BITACORA})
