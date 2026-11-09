"""Fuentes de captura diaria del Observatorio del precio de la luz en Colima."""

from extractores import cenace_demanda, cenace_precios

FUENTES = {
    "cenace_precios": cenace_precios.capturar_diario,  # API (servicio web SW-PEND)
    "cenace_demanda": cenace_demanda.capturar_diario,  # scraping (página Gráfica de Demanda)
}
