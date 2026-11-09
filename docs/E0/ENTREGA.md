# Entrega E0 · Observatorio del precio de la luz en Colima

Equipo: Miriam Monroy Alcaraz (22460314) · Etiqueta: `e0` · Tablero: (a partir de E1)
Repositorio: https://github.com/Monroy-AM/tdl-luz · Quality Lead de esta entrega: Miriam Monroy Alcaraz

## Resumen en tres líneas
1. Qué observamos y para quién: el precio por hora de la electricidad en el mercado mayorista (CENACE) en las zonas de Colima y Manzanillo, para empresas con alto consumo de luz.
2. Qué vamos a demostrar: en qué horas y meses es más barata la energía, con pronóstico mensual (E1), un experimento sobre el extractor (E2) y la comparación multivariada de 4 zonas de carga (E3).
3. Estado de la captura: captura diaria de 2 fuentes (API SW-PEND y scraping de la Gráfica de Demanda) probada el 09/11/2026; serie histórica de 59 meses (ene 2022 a nov 2026) en `data/bronce/cenace_precios_historico/`.

> E0 tiene una sola rúbrica que vale igual en las tres materias. Cada fila lleva a la evidencia.

## Ingeniería de Datos
| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Plan de recopilación (20) | `docs/E0/propuesta.md` sección 4 | |
| Captura y serie histórica (25) | `.github/workflows/captura.yml`, ejecuciones: https://github.com/Monroy-AM/tdl-luz/actions, `data/bronce/` | |

## Análisis Estadístico
| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Pregunta y cliente (20) | `docs/E0/propuesta.md` secciones 1 y 2 (entrevista) | |
| Preguntas analíticas (20) | `docs/E0/propuesta.md` sección 3 | |
| Serie histórica identificada | `data/bronce/cenace_precios_historico/` (59 periodos mensuales, 170,304 registros) | |

## Calidad en los Sistemas de Información
| Criterio de la rúbrica | Evidencia (enlace) | Nota del equipo |
|---|---|---|
| Arranque de calidad (15) | `calidad/defectos-miriam-monroy.csv`, `calidad/tiempo-miriam-monroy.csv`, `calidad/bitacora_captura.csv`, `calidad/objetivos.md` | |

## Checklist de entrega
- [ ] Repositorio con commits de la integrante
- [ ] Los 3 docentes agregados como colaboradores
- [ ] Captura programada corriendo sola (al menos una ejecución automática exitosa en GitHub Actions)
- [x] Serie histórica de 36 periodos o más en `data/bronce` (59 meses)
- [ ] Etiqueta `e0` creada antes del lunes 9 de noviembre, 17:59
- [ ] Enlace registrado en el formulario oficial del proyecto integrador
- [ ] Tarea de Classroom (Ingeniería de Datos) marcada como entregada con el enlace al repo

## Uso de IA generativa
Se usó Claude (Anthropic) para armar la estructura del repositorio, los extractores y borradores de la propuesta y de esta ficha. La entrevista, la redacción final y la revisión del código las hizo la integrante.
