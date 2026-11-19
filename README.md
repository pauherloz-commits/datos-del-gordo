# LOS DATOS DETRÁS DEL GORDO
### 200 años de Lotería de Navidad · La historia de la suerte en España, contada a través de los datos

Proyecto personal de **Data Analytics y Data Engineering**: reconstruye los números premiados con el Gordo entre 1812 y 2025, los precios y premios
documentados en el BOE, la inflación desde 1830 y la geografía de las ventas, y los convierte en un reportaje de datos (informe HTML interactivo y PDF),
un carrusel para LinkedIn y un vídeo vertical (sin subtítulos) para TikTok / Reels. El reportaje se organiza en 8 bloques, cada uno abierto por una pregunta.

Todo se genera con **un solo comando** a partir de los CSV de `data/raw/`.

## Qué contiene

| Carpeta / archivo | Contenido |
|---|---|
| `main.py` | Ejecuta el proyecto completo (datos → análisis → informe → carrusel → vídeo) |
| `data/raw/` | Datos históricos recopilados (CSV curados a mano; ver `sources.md`) |
| `data/processed/` | Datos limpios y resultados de los análisis (CSV y JSON) |
| `analysis/` | Análisis estadístico: `dataset.py` (limpieza), `validation.py` (calidad de datos), `lucky_numbers.py`, `economics.py`, `geography.py`, `probabilidad.py`, `fiscalidad.py`, `salarios.py`, `geografia_ccaa.py`, y la capa de Data Science: `inferencia_terminaciones.py` (χ²), `bootstrap_terminaciones.py`, `bayes_terminaciones.py`, `backtesting.py`, `mitos_simulacion.py` |
| `simulations/` | Simulaciones Monte Carlo: `simulation.py` (24 años, un décimo al año) y `simulation_avanzada.py` (riesgo, estrategias, sensibilidad) |
| `tests/` | 50 tests unitarios (`unittest`): estadística, backtesting sin fuga, simulación, validación de datos |
| `logs/` | `pipeline.log` (registro de cada ejecución; no se versiona) |
| `visualizations/` | Gráficos SVG propios (`charts.py`), maquetación del informe (`build_report.py`), carrusel, vídeo y textos |
| `output/informe_loteria_navidad.html` | Informe interactivo (tooltips, tablas de datos desplegables) |
| `output/informe_loteria_navidad.pdf` | Informe en PDF (A4) |
| `output/charts/` | Cada gráfico del informe como PNG independiente |
| `social_media/linkedin/` | Carrusel de 10 diapositivas (1080×1350), PDF del carrusel, texto de publicación, titular y descripción |
| `social_media/tiktok/` | Vídeo MP4 «mitos contrastados con simulación» (1080×1920, 59,5 s, sin subtítulos ni música; gancho rápido, mito del 5 y la sorpresa del 1, el Gordo que no se repite, mapa, veredicto fuera de muestra, «más barato pero más difícil» (precio frente al salario mínimo y números por sorteo), ¿compensa jugar? y cierre), guion visual, storyboard, portada, recursos y texto de publicación |
| `sources.md` | Fuentes, qué es oficial y qué secundario, lagunas y discrepancias |
| `METODOLOGIA.md` | Cálculos, hipótesis de la simulación y verificaciones |

## Cómo ejecutarlo

Necesitas **Python 3.10 o superior**. Los comandos funcionan desde cualquier carpeta; las rutas se calculan a partir de la ubicación de los scripts.

**Windows (PowerShell)**
```powershell
cd RUTA\A\LOS_DATOS_DETRAS_DEL_GORDO
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
winget install Gyan.FFmpeg        # solo para el vídeo MP4; reinicia la terminal después
python main.py
```

**macOS / Linux**
```bash
cd /ruta/a/LOS_DATOS_DETRAS_DEL_GORDO
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python main.py
```

Opciones de `main.py`:

- `python main.py --sin-video` · todo menos el MP4 (más rápido; no necesita ffmpeg).
- `python main.py --solo-analisis` · solo limpieza, validación, análisis y tests (no necesita Chromium ni ffmpeg).
- `python -m unittest discover -s tests -t .` · solo los tests unitarios.

Cada script también se puede ejecutar por separado, por ejemplo `python analysis/economics.py` o `python visualizations/build_report.py`.
Tras la ejecución, `main.py` comprueba que existen todos los ficheros esperados y devuelve un error si falta alguno.

Duración aproximada: unos segundos para el informe y 2-3 min para el vídeo, más el tiempo de instalación la primera vez.

## Capa de Data Science

Cada técnica responde a una pregunta concreta sobre los 216 primeros premios del Gordo y se explica en `METODOLOGIA.md`. Ninguna se usa para «predecir» el Gordo: el objetivo es cuantificar incertidumbre y comprobar si lo observado se sostiene fuera de muestra.

| Pregunta | Técnica | Módulo | Resultado (resumen) |
|---|---|---|---|
| ¿Son compatibles las terminaciones con una distribución uniforme? | χ² de bondad de ajuste (+ G, p-valor Monte Carlo, w de Cohen, potencia, supuestos) | `inferencia_terminaciones.py` | χ² = 21,2 (9 g.l.), p = 0,012, w = 0,31: desvío leve respecto a la uniformidad |
| ¿Cuánta incertidumbre hay en cada proporción? | Bootstrap (20.000 remuestras), IC percentil y Clopper-Pearson | `bootstrap_terminaciones.py` | ±4 puntos por cifra; el 5 es la más frecuente solo en el 53 % de las remuestras |
| ¿Qué dicen los datos si se incorpora el conocimiento previo? | Multinomial-Dirichlet, IC creíbles, factor de Bayes, evolución, sensibilidad al prior | `bayes_terminaciones.py` | El factor de Bayes depende del prior: sin evidencia sólida en ninguna dirección |
| ¿Se sostiene el patrón fuera de muestra? | Backtesting cronológico (división temporal, walk-forward, ventana móvil, baseline aleatorio, corrección de Bonferroni, contraste de fuga) | `backtesting.py` | Entrena 1812-1960, valida 1961-2025: 29,2 % de aciertos frente al 30 % del azar; 0 de 12 configuraciones baten al azar |
| ¿Qué tan raro es lo observado con un bombo perfecto? | 200.000 historias simuladas (máximo/mínimo de las 10 cifras, repeticiones, terminaciones sin salir) | `mitos_simulacion.py` | El 5 con 32: 1 de cada 6; el 1 con 8: 1 de cada 220; 15 terminaciones sin salir: 1 de cada 8 |
| ¿Compensa jugar 24 años? | Monte Carlo avanzado (ROI, valor esperado, varianza, percentiles, P(pérdida/ganancia), CVaR, estrategias de parada, horizontes, sensibilidad, verificación exacta) | `simulation_avanzada.py` | Valor esperado: 13,09 € por cada 20 €; 1,8 % acaba con ganancia |
| ¿Son fiables los datos y los cálculos? | 50 validaciones (duplicados, faltantes, formatos, rangos, fechas, coherencia de números, huellas SHA-256 de las fuentes) y 50 tests | `validation.py`, `tests/` | 50/50 validaciones y todos los tests superados |

Reproducibilidad: una semilla global (`SEED = 2026` en `analysis/common.py`) de la que derivan las semillas de cada análisis; los resultados guardan una huella para detectar cambios. Dependencias: pandas, NumPy y SciPy bastan para todo; `statsmodels` no es necesario (los contrastes están implementados directamente con SciPy y se comprueban con tests).

## Resultados principales

Resumen; el detalle, los gráficos y las fuentes están en el informe (8 bloques).

1. **El Gordo de hoy vale un tercio del de 1969.** En euros de 2025, 1.245.109 € en 1969 frente a 400.000 € (32 %). Solo se compara entre años con dato.
2. **El décimo ha pasado del 11,1 % (1978) al 1,7 % (2025) del salario mínimo mensual.** El SMI no es el salario medio.
3. **Ganar es 8,3 veces más difícil que en 1832** (1 entre 12.000 → 1 entre 100.000) y 1,6 veces más que en 1966. Es probabilidad teórica; de 1833 a 1965 no hay número de billetes documentado y no se calcula.
4. **Ganar 400.000 € no es llevarte 400.000 €:** con la norma de 2025 (exento hasta 40.000 €, 20 % del exceso) cobras 328.000 €. En 2013 el mismo Gordo dejaba 320.500 € netos; en 2012, 400.000 €.
5. **Terminaciones:** 32 de los 216 Gordos acaban en 5 y 8 en 1. Es descriptivo; el azar no tiene memoria.
6. **Geografía (dónde se vendió, no dónde viven los ganadores):** 49 de 50 provincias han vendido algún Gordo. Con los datos de lotería vendida (2022, provisionales) ninguna comunidad se desvía de lo esperable.
7. **¿Compensa?** Simulación ilustrativa de 500.000 jugadores con el cuadro de premios actual (70 %): con un décimo cada Navidad durante 24 años gastas 480 €; el jugador mediano cobra 160 € y el 1,8 % acaba con ganancia. Cada décimo cuesta 20 € y vale, de media, 13 € (neto).

## Rigor y límites

- No se inventa ningún dato: sin fuente fiable, la serie queda vacía (no hay importes fiables antes de 1960).
- Importes **por décimo**, nunca por billete; pesetas convertidas a 166,386 pts/€; euros constantes de 2025.
- Datos oficiales (BOE, INE, Banco de España) y secundarios (compilaciones de prensa) se distinguen en cada gráfico y en `sources.md`.
- El análisis geográfico usa **dónde se vendió el décimo**; no existen datos públicos del lugar de residencia de los ganadores.
- Las estadísticas de números son descriptivas: el azar no tiene memoria.
- La simulación de rentabilidad es ilustrativa; sus hipótesis están en `METODOLOGIA.md` y se contrastó con un cálculo exacto (1,81 % simulado vs 1,79 % exacto).
- Lo que no se ha podido verificar (régimen fiscal anterior a 2006, número de billetes 1833-1965, ventas por comunidad fuera de 2022) no se usa para concluir nada; ver `sources.md`.

## Subir a GitHub

```bash
git init && git add . && git commit -m "LOS DATOS DETRÁS DEL GORDO"
```
El repositorio ya incluye un `.gitignore`. Los resultados (`output/`, `social_media/`) pueden subirse o regenerarse con `python main.py`.

## Licencia y créditos

Código: uso libre con atribución. Los datos proceden de las fuentes citadas en `sources.md`; consulta sus condiciones de uso antes de redistribuirlos.
Tipografías incluidas: Lora e Inter (licencia SIL Open Font License).
