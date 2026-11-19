# Fuentes, metodología y límites de los datos

Investigación realizada el 15-16 de noviembre de 2026. El último sorteo disponible es el de 2025 (22 de diciembre de 2025).
Regla del proyecto: **no se inventa ningún dato**. Donde no hay información fiable, la serie queda vacía y se explica aquí.

## 1. Qué hay y con qué fiabilidad

| Dato | Años | Tipo de fuente | Fiabilidad | Fichero |
|---|---|---|---|---|
| Número del primer premio (Gordo) | 1812-2025 (216 premios en 214 sorteos) | Secundaria: compilaciones contrastadas entre sí | Alta salvo los casos de la sección 3 | `data/raw/gordos_historico.csv` |
| Localidades donde se vendió el Gordo | 1812-2025 | Secundaria (The Objective hasta 2021; prensa 2023-2025) | Media. 2022 sin localidades; 2023 parcial | `data/raw/gordos_historico.csv` |
| Precio del décimo, series, números por serie, premio por décimo | 1966, 1969, 1970, 1978, 1982, 1987, 1988, 2001, 2003, 2009, 2010 | **Oficial: BOE** | Alta | `data/raw/precios_premios_anclas.csv`, `boe_estructura_premios.csv` |
| Ídem | 1960, 2002, 2011, 2024, 2025 | Secundaria (Público, El Debate, Maldita.es, RTVC/SELAE, Hispanopedia) | Media | `data/raw/precios_premios_anclas.csv` |
| Ídem | 1812, 1935 | Secundaria | Baja: unidad no verificable; **no se usa en ningún cálculo** | `data/raw/precios_premios_anclas.csv` |
| Hitos históricos | 1812-2025 | SELAE, BOE, Público, Hispanopedia, Maldita.es | Media-alta | `data/raw/hitos_sorteo.csv` |
| Inflación (IPC) | 1830-2012 | **Oficial de referencia:** Maluquer de Motes (2013), Banco de España | Alta | `data/raw/ipc_maluquer_1830_2012.csv` |
| Inflación (IPC) | 2013-2025 | **Oficial: INE** (variación diciembre sobre diciembre) | Alta | `data/raw/ipc_ine_variacion_diciembre.csv` |
| Municipio → provincia | 208 municipios | Elaboración propia (manual) | Alta; 3 municipios `sin_clasificar` por nombre ambiguo | `data/raw/municipios_provincias.csv` |

**Los datos brutos son CSV curados a mano** a partir de estas fuentes; el proyecto no descarga nada al ejecutarse (así los resultados no dependen de páginas web que cambian).

## 2. Lo que NO existe o no se ha podido obtener

- **Importes del Gordo y precio del décimo antes de 1960**: no hay datos fiables. No se calcula nada económico para 1812-1959. Solo consta (SELAE) que en 1812 el billete costaba 40 reales y el primer premio era de 8.000 pesos fuertes, pero se desconoce si es por billete o por fracción y el cambio a euros no es verificable.
- **Años 1961-1965, 1967-1968, 1971-1977, 1979-1981, 1983-1986, 1989-2000, 2004-2008, 2012-2023**: sin programa de premios revisado. En los gráficos económicos las líneas solo unen años con dato; no se interpola. Del 2012 al 2023 el Gordo es 400.000 € por décimo según SELAE/Maldita.es (sin revisar los BOE de cada año).
- **Recaudación y dinero repartido por año**: solo para los años con programa de premios (BOE) y 2024-2025 (SELAE vía prensa). Con el 70 % verificado en 9 programas del BOE (1966-2009), el reparto se usa como regla, no como dato de cada año.
- **Lugar de residencia de los ganadores**: no existe en ninguna fuente pública consultada. **Todo el análisis geográfico es de dónde se vendió el décimo, no de dónde vive el ganador**, y así se indica en cada gráfico.
- **Localidades**: hasta 1931 las compilaciones asocian una sola ciudad a cada Gordo (limitación de las fuentes, no un hecho histórico). 2022 (05490) no tiene localidades; 2023-2025 son las que cita la prensa y pueden ser incompletas porque el premio se repartió por muchos puntos de venta.
- **Mapa**: se usa un mapa de cuadrícula (una casilla por provincia) porque no se dispone de geometrías de provincias ni de conexión a internet en la ejecución; no respeta la forma real del territorio.

## 3. Discrepancias entre fuentes y decisión adoptada

| Caso | Qué dicen las fuentes | Decisión |
|---|---|---|
| 1837 | SELAE: hubo dos primeros premios de igual cuantía. Las compilaciones solo recogen un número (10998, Jerez); el 03616 aparece en una sola | Se incluyen ambos, el segundo marcado en la columna `nota` y sin localidad |
| 1900 | Una compilación da 25285; dos dan 26285 | 26285 (mayoría; ambos acaban en 85, así que no cambia el análisis de terminaciones) |
| 1938 | Dos sorteos el mismo día (Barcelona y Burgos) según SELAE | Se incluyen los dos (22655 y 36758) |
| 1969 | Una compilación repite 43758 (que es el de 1967) | 59536, Sabadell (resto de fuentes) |
| 2005 | Una compilación da 60657 | 20085 (tres fuentes coinciden) |
| 1987 | El BOE consultado no deja leer el importe del primer premio | Se usan series, precio y números por serie; el importe del Gordo queda vacío |
| Primer sorteo de Navidad | SELAE sitúa el origen en 1812; Público sitúa el primer sorteo especial en 1818 y su regularidad en 1839; el nombre «Sorteo de Navidad» aparece en 1892 | Se muestran las tres fechas como hitos distintos. La serie de números empieza en 1812 por la tradición de SELAE |
| Primer sorteo televisado | Dos artículos de Público dan 1957 y 1962 | No se usa como hito en el carrusel ni en el vídeo |
| Terminaciones «que nunca han salido» | SELAE (página antigua) lista 16 terminaciones de dos cifras; con los datos hasta 2025 algunas ya han salido | Se calcula con los 216 premios; el resultado difiere de la lista antigua de SELAE |

**Verificación interna:** en 9 de los programas del BOE revisados (1966, 1969, 1970, 1978, 1982, 1987, 2001, 2003 y 2009) los premios son exactamente el 70,0 % de lo emitido (`data/processed/validacion_dataset.json`); además, la emisión de 2024 (3.860 M€) y los premios de 2025 (2.772 M€) calculados con series × números × precio coinciden con las cifras publicadas por SELAE.

## 4. Cómo se ajusta por inflación

- **Euros constantes de 2025.** Para cada año, importe × (IPC 2025 / IPC del año).
- **Serie de IPC enlazada:** Maluquer de Motes (media anual, base 2000 = 100) hasta 2012 y, desde 2013, el índice se prolonga con las variaciones diciembre-diciembre del INE. Son medidas ligeramente distintas (media anual vs. diciembre); en 1966-2012, contra las tasas del INE, la correlación es 0,968 y la desviación media 1,05 puntos porcentuales (`validacion_dataset.json`).
- **Pesetas → euros:** 166,386 pts/€ (tipo irrevocable de 1998). Todas las cifras en pesetas se convierten antes de ajustar.
- **Importe por décimo ≠ importe por billete:** el Gordo de 2025 son 4.000.000 € por billete (serie) y 400.000 € por décimo. Todos los gráficos usan el importe **por décimo** y el precio **del décimo**.
- **Neto tras impuestos:** se aplica a cada año su propia norma (`data/raw/fiscalidad_premios.csv`), nunca la de hoy al pasado. Solo se calcula desde 2006; antes, el régimen no está verificado. 2025: 328.000 € = 400.000 € − 20 % del exceso sobre 40.000 €.
- **Premio histórico máximo en euros constantes:** 1969, 1.245.109 € (entre los años con dato; no se afirma que sea el máximo absoluto de la historia).

## 5. Estadística: qué se afirma y qué no

- Las frecuencias de terminaciones, repeticiones y números son **descriptivas**. El espacio de números cambió (12.000 en 1832; 66.000 en 1982-2003; 85.000 en 2009-2010; 100.000 desde 2011) y para 1812-1959 no hay espacio documentado.
- **No se afirma que una terminación tenga más probabilidades en el futuro**: cada sorteo es independiente. Se contrastan las frecuencias con el azar puro (banda binomial del 95 %, chi-cuadrado y 20.000 simulaciones Monte Carlo en `analysis/lucky_numbers.py`).
- **Simulación de rentabilidad (`analysis/simulation.py`):** 500.000 jugadores ficticios, un décimo por Navidad durante 24 años a 20 €, con el cuadro de premios vigente (no el de 2001) y semilla fija (2026). Es **ilustrativa**. Hipótesis y verificación exacta en `METODOLOGIA.md`.
- Correlación no es causalidad: que el Gordo no haya subido desde 2011 mientras suben los precios describe una situación, no explica por qué.

## 6. Referencias

**Oficiales**
- BOE, programas de premios del Sorteo Extraordinario de Navidad (documentos consultados):
  - 1966 · https://www.boe.es/boe/dias/1966/12/16/pdfs/A15789-15789.pdf
  - 1969 · https://boe.es/boe/dias/1969/12/17/pdfs/A19651-19652.pdf
  - 1970 · https://boe.es/boe/dias/1970/12/16/pdfs/A20368-20368.pdf
  - 1978 · https://www.boe.es/boe/dias/1978/12/18/pdfs/A28426-28426.pdf
  - 1982 · https://boe.es/boe/dias/1982/12/13/pdfs/A34117-34117.pdf
  - 1987 · https://www.boe.es/boe/dias/1987/12/14/pdfs/A36665-36665.pdf
  - 1988 · https://www.boe.es/boe/dias/1988/12/12/pdfs/A34948-34948.pdf
  - 2001 · https://www.boe.es/boe/dias/2001/12/20/pdfs/A48737-48737.pdf
  - 2003 · https://www.boe.es/boe/dias/2003/12/20/pdfs/A45375-45375.pdf
  - 2009 · https://www.boe.es/boe/dias/2009/12/18/pdfs/BOE-A-2009-20316.pdf
  - 2010 · https://boe.es/boe/dias/2010/12/20/pdfs/BOE-A-2010-19540.pdf
- Maluquer de Motes, J. (2013), *La inflación en España. Un índice de precios de consumo, 1830-2012*, Banco de España, Estudios de Historia Económica nº 64 · https://repositorio.bde.es/bitstream/123456789/7400/1/roja64.pdf
- INE, notas de prensa del IPC (diciembre 2025) · https://ine.es/dyngs/Prensa/IPC1225.htm
- SELAE, curiosidades del Sorteo de Navidad · https://www.loteriasyapuestas.es/es/paginas-informativas/curiosidades

**Secundarias**
- The Objective, histórico de premios con localidades · https://theobjective.com/loterias/loteria-navidad/2022-12-01/premios-loteria-navidad/
- LotoCrack, historial de números del Gordo · https://lotocrack.com/resultados-historicos/loteria-de-navidad/ganadores/
- Loterías Perolo, histórico de números del Gordo · https://www.loteriasperolo.es/blog/historico-numeros-gordo-loteria-navidad.htm
- El Español, «cuál fue el Gordo el año que naciste» · https://elespanol.com/loterias/loteria-navidad/cual-fue-gordo-loteria-navidad-ano-naciste/813918798_0.html
- Público, origen e historia de la Lotería de Navidad · https://www.publico.es/sociedad/verdadero-origen-loteria-navidad.html y https://www.publico.es/culturas/loteria-era-historia-origen-recorrido.html
- Maldita.es, el Gordo y la inflación desde 2011 · https://maldita.es/malditodato/20231222/gordo-valor-inflacion-2011/
- Hispanopedia, Sorteo Extraordinario de Navidad · https://es.hispanopedia.com/wiki/Sorteo_Extraordinario_de_Navidad
- El Debate (precio del décimo e inflación, 2025) · https://www.eldebate.com/loteria-de-navidad/20251208/cuanto-sube-precio-real-decimo-loteria-navidad-inflacion-2025-cns_362112.html
- RTVC (emisión y premios 2024, datos SELAE) · https://rtvc.es/la-loteria-de-navidad-repartira-2-702-millones-de-euros-en-premios-2024/
- Voz Pópuli, números que nunca han tocado · https://www.vozpopuli.com/loterias/loteria-navidad/los-numeros-de-la-loteria-de-navidad-que-nunca-han-tocado.html
- invertirenbolsa.info, histórico del IPC de España (recopilación de datos del INE, 1965-2022) · https://invertirenbolsa.info/historico-ipc-espana/datos-historicos-del-ipc-en-espana.htm

Las páginas de prensa y de terceros pueden cambiar o desaparecer; por eso los datos usados están copiados en `data/raw/`.

## 7. Ampliación (rediseño): datos nuevos, discrepancias y límites

| Dato | Fuente | Fichero | Fiabilidad / límite |
|---|---|---|---|
| Números por sorteo (N) | SELAE (1832); BOE (1966-1982 y 2009-2010); secundaria (2011+) | `numeros_por_sorteo.csv` | Entre 1833 y 1965 no hay N documentado: no se calcula probabilidad (solo una cota inferior observada, que no se usa como dato) |
| Fiscalidad de premios | Leyes 35/2006, 16/2012, 6/2018, RDL 3/2020 y BOE | `fiscalidad_premios.csv` | Régimen anterior a 2006 sin verificar; el umbral de 2019 se apoya en normativa foral publicada en BOE |
| Salario mínimo mensual | BOE (RD 87/2025: 1.184 €) y serie secundaria 1976-2024 | `smi_mensual.csv` | Es SMI, no salario medio; la serie 1976-2024 es secundaria |
| Población y lotería vendida por CCAA | INE y RTVC con datos SELAE | `ccaa_poblacion_consignacion_2022.csv` | Solo 2022, provisional; no hay serie histórica |
| Cuadro de premios actual | SELAE / RTVC | `premios_estructura_actual.csv` | Suma exactamente 14.000.000 € por serie (70 % de 20 M€) |
| Hitos corregidos | SELAE, BOE | `hitos_sorteo_v2.csv` | El original `hitos_sorteo.csv` se conserva |

**Discrepancias nuevas:** (1) la página de SELAE «195 series / 85.000 números» corresponde a la estructura de 2010, no a la actual; (2) el número de premios actual da 15.304 al derivarlo del cuadro y 14.008 en una fuente secundaria, y no se ha podido reconciliar (el importe total sí cuadra); (3) la primera retransmisión por TV es 1957 (SELAE) o 1962 (prensa), por lo que no se usa; (4) el aumento a 85.000 números se fecha en 2005 (Wikipedia) y en 2009 (BOE): se usa el BOE.

**Lo que no se afirma:** que una comunidad tenga «más suerte»; que la lotería vendida indique dónde viven los ganadores; que el SMI represente el salario medio; ninguna conclusión sobre el neto antes de 2006.

## 8. Datos y reglas añadidos en la capa de Data Science
- Los resultados de χ², bootstrap, bayes, backtesting y mitos salen **solo** de los 216 primeros premios (`data/raw`, ya descritos arriba) y del número de bolas por sorteo (`numeros_por_sorteo.csv`). No se han añadido fuentes nuevas.
- Integridad: `data/raw/MANIFEST.sha256` guarda la huella SHA-256 de cada fichero original; `analysis/validation.py` la comprueba en cada ejecución. Si se modifica un dato original a propósito, se actualiza con `validation.actualizar_manifiesto()`.
- Limitación: no hay N documentado para 1812-1831; la uniformidad de las terminaciones se asume y se advierte en el informe.
