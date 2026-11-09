# Observatorio del precio de la luz en Colima · Trusted Data Lab

Integrante: Miriam Monroy Alcaraz (22460314) · Ing. en Sistemas Computacionales, Instituto Tecnológico de Colima

**Qué observa:** el precio por hora de la electricidad en el mercado eléctrico mayorista (CENACE) para las zonas de
carga de Colima y Manzanillo, comparadas con Guadalajara y Uruapan, junto con la demanda de la región Occidental.

**Fuentes:**
- API del CENACE (servicio web SW-PEND): precios marginales locales por zona de carga, por hora.
- Scraping de la página "Gráfica de Demanda" del CENACE: demanda, generación y pronóstico por hora.

**Cómo se ejecuta (Windows):**

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
python -m extractores.captura          # captura del día -> data\bronce y calidad\bitacora_captura.csv
python -m extractores.historico 2022   # serie histórica mensual (ya descargada)
pytest -q
```

**Tablero público:** (a partir de E1)

Estructura: `extractores/`, `data/bronce|plata|oro|cuarentena`, `calidad/`, `docs/E0/`, `laboratorio/`, `tablero/`,
`tests/`, `.github/workflows/` (captura programada e integración continua).

Datos: Centro Nacional de Control de Energía (CENACE), información pública.
