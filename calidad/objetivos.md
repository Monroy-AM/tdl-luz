# Objetivos de calidad medibles (E0)

Alimentan el plan SQA de E1 y se comparan contra lo medido en `calidad/bitacora_captura.csv`.

| # | Objetivo | Métrica y fórmula | Meta | Cómo se mide | Primera medición |
|---|---|---|---|---|---|
| 1 | Disponibilidad de la captura | Ejecuciones con `estado = ok` / ejecuciones programadas, por fuente, en 14 días | ≥ 95% | `calidad/bitacora_captura.csv` | E1 (13 nov) |
| 2 | Completitud de cada captura | Registros de precios capturados / esperados (4 zonas × 24 horas × días consultados) | ≥ 95% | Conteo en `data/bronce/cenace_precios/` | E1 |
| 3 | Defectos que llegan a datos | Defectos tipo `datos` hallados después de pruebas / total de defectos tipo `datos` | ≤ 20% | `calidad/defectos-*.csv` | E1 y E3 (retrospectiva PSP) |

Metas que pedirá el Sello TDL más adelante: 0 secretos expuestos (gitleaks), cobertura de pruebas ≥ 60%,
completitud de la capa oro ≥ 95%.
