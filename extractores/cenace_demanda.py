"""CENACE: demanda, generación y pronóstico por hora de la Gerencia de Control Regional Occidental.

Fuente: página pública https://www.cenace.gob.mx/GraficaDemanda.aspx (scraping).
La página dibuja la gráfica con los datos que pide a su propio método GraficaDemanda.aspx/obtieneValoresTotal;
el extractor lee esos mismos datos, como lo hace el navegador. El sitio no publica robots.txt (404).
Solo muestra el día en curso, por eso la serie se construye capturando todos los días.
Gerencias: 3 Central, 4 Noreste, 5 Noroeste, 6 Norte, 7 Occidental (incluye Colima), 8 Oriental, 9 Peninsular, 10 SIN.
"""

from __future__ import annotations

import json
from datetime import date

PAGINA = "https://www.cenace.gob.mx/GraficaDemanda.aspx"
METODO = PAGINA + "/obtieneValoresTotal"
GERENCIAS = {"7": "Occidental", "10": "SIN"}


def leer(ex, gerencia: str = "7") -> list[dict]:
    ex.get(PAGINA)  # respeta robots y la pausa; abre la página como un navegador
    ex._reglas(METODO)
    r = ex.sesion.post(METODO, data=json.dumps({"gerencia": gerencia}), timeout=ex.timeout,
                       headers={"Content-Type": "application/json; charset=utf-8", "Referer": PAGINA})
    r.raise_for_status()
    valores = json.loads(r.json()["d"])
    hoy = date.today().isoformat()
    return [{"fecha_captura": hoy, "gerencia": GERENCIAS.get(gerencia, gerencia), "hora": v.get("hora"),
             "demanda_mw": v.get("valorDemanda"), "generacion_mw": v.get("valorGeneracion"),
             "enlace_mw": v.get("valorEnlace"), "pronostico_mw": v.get("valorPronostico")} for v in valores]


def capturar_diario(ex) -> tuple[list[dict], str]:
    filas = []
    for g in GERENCIAS:
        filas += leer(ex, g)
    return filas, PAGINA
