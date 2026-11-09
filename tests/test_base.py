import urllib.robotparser

import pytest

from extractores.base import UA, ExtractorEtico


def _extractor_con_reglas(lineas, base="https://ejemplo.mx"):
    ex = ExtractorEtico(pausa=0)
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(lineas)
    ex.robots[base] = rp
    return ex


def test_user_agent_se_identifica():
    assert "TDL-Observatorio" in UA and "contacto" in UA


def test_respeta_rutas_prohibidas():
    ex = _extractor_con_reglas(["User-agent: *", "Disallow: /privado/"])
    assert ex.permitido("https://ejemplo.mx/precios/hoy")
    assert not ex.permitido("https://ejemplo.mx/privado/datos")


def test_get_lanza_error_si_robots_prohibe():
    ex = _extractor_con_reglas(["User-agent: *", "Disallow: /"])
    with pytest.raises(PermissionError):
        ex.get("https://ejemplo.mx/cualquier-cosa")


def test_cenace_rechaza_mas_de_7_dias():
    from datetime import date

    from extractores import cenace_precios

    with pytest.raises(ValueError):
        cenace_precios.consultar(None, date(2025, 1, 1), date(2025, 1, 9))
