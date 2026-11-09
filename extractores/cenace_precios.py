"""CENACE: Precios Marginales Locales por Zona de Carga (servicio web SW-PEND).

Fuente: https://ws01.cenace.gob.mx:8082/SWPEND/SIM/{sistema}/{proceso}/{zonas}/{aaaa}/{mm}/{dd}/{aaaa}/{mm}/{dd}/JSON
- Servicio web público del CENACE, sin llave. Máximo 7 días por consulta; acepta varias zonas separadas por coma.
- MDA = Mercado del Día en Adelanto (precios por hora, $/MWh). Campos: pz (precio total), pz_ene (energía),
  pz_per (pérdidas), pz_cng (congestión).
- Es una API documentada, por eso se consulta con api=True (no se rastrea el sitio).
"""

from __future__ import annotations

from datetime import date, timedelta

BASE = "https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN"
ZONAS = ["COLIMA", "MANZANILLO", "GUADALAJARA", "URUAPAN"]  # grupos para comparar (E3)
CAMPOS = ["pz", "pz_ene", "pz_per", "pz_cng"]


def consultar(ex, inicio: date, fin: date, proceso: str = "MDA",
              zonas: list[str] | None = None) -> tuple[list[dict], str]:
    if (fin - inicio).days > 6:
        raise ValueError("El servicio solo permite 7 días por consulta")
    zonas = zonas or ZONAS
    url = (f"{BASE}/{proceso}/{','.join(zonas)}/{inicio:%Y/%m/%d}/{fin:%Y/%m/%d}/JSON")
    r = ex.get(url, api=True)
    datos = r.json()
    if datos.get("status") not in ("OK", "ZERO_RESULTS"):
        raise RuntimeError(f"Respuesta inesperada del CENACE: {str(datos)[:200]}")
    filas = []
    for res in datos.get("Resultados", []):
        for v in res.get("Valores", []):
            filas.append({"zona_carga": res.get("zona_carga"), "proceso": proceso, "fecha": v.get("fecha"),
                          "hora": v.get("hora"), **{c: v.get(c) for c in CAMPOS}})
    return filas, url


def capturar_diario(ex) -> tuple[list[dict], str]:
    """Captura diaria: últimos 7 días del MDA (incluye el día siguiente si ya se publicó)."""
    fin = date.today() + timedelta(days=1)
    return consultar(ex, fin - timedelta(days=6), fin)
