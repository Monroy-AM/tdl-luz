"""Corre las fuentes de captura diaria, guarda en bronce y anota la bitacora.

Uso (desde la raiz del repo):
    python -m extractores.captura            # todas las fuentes
    python -m extractores.captura sniim      # solo una

Cada fuente (en extractores/fuentes.py) es una funcion que recibe el extractor
y regresa (filas, url) o (filas, url, nombre_archivo).
"""

from __future__ import annotations

import sys
import time
import traceback
import uuid

from extractores.base import ExtractorEtico
from extractores.bronce import RAIZ, ahora_utc, guardar_bronce, registrar_ejecucion
from extractores.fuentes import FUENTES


def correr(nombres: list[str] | None = None) -> int:
    ejecucion_id = ahora_utc().strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]
    ex = ExtractorEtico()
    fallas = 0
    objetivo = {n: FUENTES[n] for n in (nombres or FUENTES)}
    for nombre, funcion in objetivo.items():
        inicio = ahora_utc()
        t0 = time.time()
        estado, registros, archivo, error = "ok", 0, "", ""
        try:
            resultado = funcion(ex)
            filas, url = resultado[0], resultado[1]
            nombre_archivo = resultado[2] if len(resultado) > 2 else None
            registros = len(filas)
            if registros == 0:
                estado = "vacio"
            else:
                ruta = guardar_bronce(nombre, filas, url, ejecucion_id, nombre_archivo)
                archivo = ruta.relative_to(RAIZ).as_posix()
        except Exception as e:  # noqa: BLE001 - toda falla se registra
            estado, error = "falla", f"{type(e).__name__}: {e}"[:300]
            fallas += 1
            traceback.print_exc()
        registrar_ejecucion(
            ejecucion_id=ejecucion_id, fuente=nombre,
            inicio_utc=inicio.isoformat(timespec="seconds"),
            fin_utc=ahora_utc().isoformat(timespec="seconds"),
            duracion_s=round(time.time() - t0, 2), estado=estado,
            registros=registros, archivo=archivo, error=error,
        )
        print(f"[{nombre}] {estado} | {registros} registros {archivo} {error}")
    # Falla solo si fallaron todas, para que la bitacora se guarde siempre
    return 1 if objetivo and fallas == len(objetivo) else 0


if __name__ == "__main__":
    sys.exit(correr(sys.argv[1:] or None))
