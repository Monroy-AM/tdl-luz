# Propuesta del observatorio · Observatorio del precio de la luz en Colima

Equipo: Miriam Monroy Alcaraz (22460314) · Data Engineer y Data Statistician (equipo de una integrante)
Fecha: 09/11/2026 · Repositorio: <URL del repositorio> · Etiqueta: `e0`

> PENDIENTE antes de entregar: la URL del repositorio. Borrar esta nota.

## 1. Ficha del observatorio

| Campo | Respuesta |
|---|---|
| Sector | Energía eléctrica: mercado eléctrico mayorista (precios por hora del CENACE) |
| Región | Zonas de carga de Colima y Manzanillo, comparadas con Guadalajara y Uruapan |
| Pregunta detonadora | ¿En qué horas, días y meses es más barata la electricidad en Colima y Manzanillo, y cuánto costará el próximo mes? |
| Cliente potencial | Empresas con alto consumo de luz: empacadoras y cámaras frigoríficas, hoteles de Manzanillo, industria y empresas ligadas al puerto; también instaladores de paneles solares que asesoran a esos clientes. (En la entrevista, un hogar con tarifa doméstica pagaría de $30 a $50 al mes solo si tuviera tarifa horaria o paneles; el cliente que paga son las empresas.) |
| Unidad de análisis | Precio marginal local por hora y por zona de carga ($/MWh) |

**Por qué importa:** el precio de la electricidad en el mercado mayorista cambia cada hora. En la zona de carga de
Colima, de 2022 a 2026, la hora más cara (21:00) promedió $1,353.2 por MWh y la más barata (10:00) $640.3, más del
doble. Una empresa que sabe cuándo es barata la energía puede mover procesos (bombeo, refrigeración, producción) a
esas horas, negociar mejor su contrato o decidir si le conviene generar con paneles solares.

## 2. Entrevista de campo (mínimo 15 minutos)
- **Entrevistado:** usuario doméstico de CFE (hogar con tarifa 1; sin nombre) · **Fecha, duración y medio:** 08/11/2026, unos 20 minutos, en persona
- **Las 5 preguntas y respuestas:**
  1. ¿Cuánto paga al mes de luz y qué tarifa tiene contratada? — Entre $800 y $1,200 al mes, más en temporada de
     calor por el aire acondicionado y los ventiladores. Tiene la tarifa doméstica 1; el costo sube si rebasa el
     límite subsidiado.
  2. ¿En qué horas usa más energía y podría mover alguna actividad a otro horario? — El consumo sube de 6:00 a
     10:30 de la noche, cuando todos están en casa (televisión, cocina, luces, aire acondicionado). Sí podría mover
     la lavadora a la mañana o al inicio de la tarde y usar menos aparatos al mismo tiempo en la noche.
  3. ¿Sabía que el precio de la energía cambia por hora? ¿Cómo se entera de esos cambios? — Sabe que existe en
     otros países y en tarifas de CFE con horarios para negocios, pero en su tarifa doméstica se cobra por bloques
     de consumo del bimestre, no por hora. Si existiera para casas, le gustaría enterarse por una app oficial o
     notificaciones con las horas caras y baratas.
  4. ¿Qué información le ayudaría a bajar su gasto de luz? — Saber qué aparatos gastan más (refrigerador,
     televisión, plancha), alertas cuando se acerca al límite en que pierde el subsidio (tarifa DAC) y
     recomendaciones de las mejores horas para usar los aparatos pesados.
  5. ¿Pagaría por un reporte semanal con el pronóstico del precio por hora? ¿Cuánto? — Con su tarifa actual no,
     porque no tiene medidor con tarifa horaria y no le sacaría provecho. Si tuviera paneles solares, auto
     eléctrico o una tarifa que cambie por hora, pagaría de $30 a $50 al mes por una app o reporte automático.
- **Lo que aprendimos:**
  - Un hogar con tarifa doméstica paga por bloques de consumo, no por hora: el precio horario del mercado no le
    afecta directo. El cliente que paga son las empresas con tarifa horaria o los usuarios con paneles solares o
    auto eléctrico; conviene confirmarlo con una segunda entrevista a un negocio.
  - Su horario de mayor consumo (6:00 a 10:30 de la noche) coincide con las horas más caras del mercado en la zona
    Colima: la hora 21 promedió $1,353.2 por MWh en 2022-2026, contra $640.3 de la hora 10. La demanda de los
    hogares ayuda a explicar los picos de precio.
  - Lo que más valora es práctico: qué aparatos gastan más, alertas antes de perder el subsidio y las mejores horas
    para usar aparatos pesados. Para hogares, el precio aceptable es bajo ($30 a $50 al mes), lo que orienta el
    modelo de negocio hacia empresas.

## 3. Las tres preguntas analíticas

| # | Técnica (entrega) | Pregunta medible | Variables |
|---|---|---|---|
| 1 | Pronóstico (E1) | ¿Cuál será el precio promedio mensual de la energía (MDA) en la zona de carga Colima en los próximos 6 meses? | Promedio mensual $/MWh, **59 meses** (ene 2022 a nov 2026); diario: más de 1,700 días |
| 2 | Experimento factorial (E2), ruta ingeniería | ¿Qué combinación de días por consulta (1 vs 7), zonas por consulta (1 vs 4) y formato de escritura (CSV vs Parquet) minimiza el tiempo y los errores del extractor del CENACE? | Respuestas: segundos por mes descargado y porcentaje de consultas fallidas |
| 3 | Multivariado (E3) | ¿Las zonas de carga Colima, Manzanillo, Guadalajara y Uruapan se comportan distinto en precio total, componente de energía, pérdidas, congestión y diferencia entre la hora más cara y la más barata? | 4 grupos, 5 variables por zona-día |

## 4. Plan de recopilación de datos

| Fuente | Qué ofrece | Estructura y formato | Actualización | Acceso | Captura |
|---|---|---|---|---|---|
| CENACE, servicio web SW-PEND (precios marginales locales por zona de carga) | Precio por hora: total, energía, pérdidas y congestión, por zona | JSON | Diaria (MDA del día siguiente) | **API** pública sin llave; máximo 7 días por consulta | Programada diaria (últimos 7 días) |
| CENACE, página "Gráfica de Demanda" | Demanda, generación y pronóstico por hora de la región Occidental y del sistema nacional | Página web; los datos se leen del JSON que carga la propia página | Cada hora (solo el día en curso) | **Scraping** | Programada diaria |

### Análisis ético y legal
- **API SW-PEND del CENACE:** es un servicio web público y documentado. Se respeta el límite de 7 días por consulta,
  se usa un User-Agent con contacto y una pausa de al menos 1.5 s entre peticiones. Datos públicos de gobierno, sin
  datos personales.
- **Página "Gráfica de Demanda":** el sitio `www.cenace.gob.mx` no publica robots.txt (responde 404), por lo que no hay
  rutas prohibidas. El extractor lee solo los datos que la página carga para dibujar su gráfica, una vez al día, con
  pausa e identificación. Son totales de la red eléctrica, sin datos personales.
- Términos: información pública del CENACE; se cita la fuente en el tablero y en el dataset.

### Serie histórica (ya en `data/bronce/cenace_precios_historico/`)
- Precios por hora del MDA de 4 zonas de carga, del 1 de enero de 2022 al 9 de noviembre de 2026: **170,304 registros**,
  **59 meses** sin huecos (un archivo por mes).
- La demanda no tiene historia en la página (solo el día en curso): su serie se forma con la captura diaria.

## 5. Máquina de captura (capa bronce)
- `python -m extractores.captura` → `data/bronce/cenace_precios/<fecha>.csv` y `data/bronce/cenace_demanda/<fecha>.csv`,
  con metadatos `_fuente`, `_url`, `_capturado_utc`, `_ejecucion_id`.
- Programada en `.github/workflows/captura.yml` (17:30 hora de Colima). Bitácora: `calidad/bitacora_captura.csv`.

## 6. Sistema de calidad inicial
- Registros PSP: `calidad/tiempo-miriam-monroy.csv` y `calidad/defectos-miriam-monroy.csv`.
- Objetivos medibles: `calidad/objetivos.md`.

## 7. Riesgos y plan B
| Riesgo | Plan B |
|---|---|
| El servicio del CENACE (puerto 8082) rechaza conexiones desde algunos servidores en la nube; puede fallar en GitHub Actions | La bitácora lo registra; si falla, la captura corre desde la PC con `capturar.bat` y se sube el resultado |
| La página de demanda cambia su estructura | Prueba automática del formato y alerta en la bitácora |
| El servicio limita a 7 días por consulta | El histórico se descarga por semanas y es reanudable |
