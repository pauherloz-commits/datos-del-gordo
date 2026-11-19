"""LOS DATOS DETRÁS DEL GORDO · ejecución principal.

    python main.py                 # todo: datos -> análisis -> informe HTML/PDF -> carrusel -> vídeo
    python main.py --sin-video     # igual, sin el MP4 (el vídeo es la parte más lenta: ~2-3 min)
    python main.py --solo-analisis # solo limpieza de datos y análisis (no necesita Chromium ni ffmpeg)

Funciona desde cualquier carpeta: todas las rutas se calculan a partir de la ubicación de este fichero."""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "analysis"))
sys.path.insert(0, str(ROOT / "simulations"))
sys.path.insert(0, str(ROOT / "visualizations"))


_n = [0]


def paso(total: int, texto: str):
    _n[0] += 1
    print(f"\n[{_n[0]}/{total}] {texto}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-video", action="store_true", help="no generar el MP4")
    ap.add_argument("--solo-analisis", action="store_true", help="solo datos y análisis")
    args = ap.parse_args()
    t0 = time.time()
    total = 5 if args.solo_analisis else (8 if args.sin_video else 9)

    paso(total, "Limpieza de datos y validación de calidad (duplicados, formatos, rangos, fechas, integridad de fuentes)")
    import dataset
    import validation
    dataset.build()
    validation.run(estricto=True)

    paso(total, "Análisis: números, economía, probabilidad, fiscalidad, salarios, geografía/CCAA y simulación")
    import economics
    import fiscalidad
    import geografia_ccaa
    import geography
    import lucky_numbers
    import probabilidad
    import salarios
    import simulation
    lucky_numbers.run()
    economics.run()
    geography.run()
    probabilidad.run()
    fiscalidad.run()
    salarios.run()
    geografia_ccaa.run()
    simulation.run()
    print("   data/processed/*.json y *.csv actualizados")

    paso(total, "Capa de Data Science: χ², bootstrap, modelo bayesiano, backtesting y Monte Carlo avanzado")
    import backtesting
    import bayes_terminaciones
    import bootstrap_terminaciones
    import inferencia_terminaciones
    import mitos_simulacion
    import simulation_avanzada
    inferencia_terminaciones.run()
    mitos_simulacion.run()
    bootstrap_terminaciones.run()
    bayes_terminaciones.run()
    backtesting.run()
    simulation_avanzada.run()

    paso(total, "Tests automáticos (unittest)")
    ok = ejecutar_tests()

    if args.solo_analisis:
        paso(total, "Comprobación de ficheros")
        return comprobar(solo_analisis=True, t0=t0) or (0 if ok else 1)

    if shutil.which("ffmpeg") is None and not args.sin_video:
        print("AVISO: no se encuentra ffmpeg; se omite el vídeo (usa --sin-video para silenciar este aviso).")
        args.sin_video = True
        total = 8

    paso(total, "Informe editorial (HTML interactivo + PDF + PNG de cada gráfico)")
    import build_report
    build_report.build()
    build_report.render_outputs()

    paso(total, "Carrusel de LinkedIn (10 diapositivas PNG + PDF)")
    import social_carousel
    social_carousel.build()
    social_carousel.render()

    paso(total, "Textos de publicación, guion y storyboard")
    import social_texts
    social_texts.write_all()

    if not args.sin_video:
        paso(total, "Vídeo vertical 1080x1920 (render de fotogramas + ffmpeg)")
        import social_video
        social_video.render_video()

    paso(total, "Comprobación de ficheros")
    return comprobar(solo_analisis=False, t0=t0, con_video=not args.sin_video) or (0 if ok else 1)


def ejecutar_tests() -> bool:
    """Ejecuta tests/ con unittest y guarda el resultado en data/processed/tests_resultado.json."""
    import json
    import unittest

    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))
    res = unittest.TextTestRunner(verbosity=0).run(suite)
    ok = res.wasSuccessful()
    (ROOT / "data" / "processed" / "tests_resultado.json").write_text(
        json.dumps({"n_tests": res.testsRun, "fallos": len(res.failures), "errores": len(res.errors), "ok": ok}, indent=1), encoding="utf-8")
    print(f"   {res.testsRun} tests · {'OK' if ok else 'CON FALLOS'}")
    return ok


def comprobar(solo_analisis: bool, t0: float, con_video: bool = True) -> int:
    esperados = ["data/processed/gordos_clean.csv", "data/processed/analisis_numeros.json", "data/processed/analisis_economia.json",
                 "data/processed/analisis_geografia.json", "data/processed/simulacion.json",
                 "data/processed/analisis_probabilidad.json", "data/processed/analisis_fiscalidad.json",
                 "data/processed/analisis_salarios.json", "data/processed/analisis_ccaa.json",
                 "data/processed/analisis_chi2.json", "data/processed/analisis_mitos.json", "data/processed/analisis_bootstrap.json", "data/processed/analisis_bayes.json",
                 "data/processed/analisis_backtesting.json", "data/processed/simulacion_avanzada.json",
                 "data/processed/validacion_calidad.json", "data/processed/tests_resultado.json"]
    if not solo_analisis:
        esperados += ["output/informe_loteria_navidad.html", "output/informe_loteria_navidad.pdf",
                      "social_media/linkedin/carrusel_linkedin.pdf", "social_media/linkedin/slides/slide_10.png",
                      "social_media/linkedin/post_linkedin.md", "social_media/tiktok/guion.md", "social_media/tiktok/storyboard.md",
                      "METODOLOGIA.md", "sources.md"]
        if con_video:
            esperados += ["social_media/tiktok/video_loteria_navidad.mp4", "social_media/tiktok/portada_video.png"]
    faltan = [e for e in esperados if not (ROOT / e).exists() or (ROOT / e).stat().st_size == 0]
    for e in esperados:
        print(("   OK       " if e not in faltan else "   FALTA    ") + e)
    print(f"\nTerminado en {time.time() - t0:.0f} s. {'Todo correcto.' if not faltan else 'Faltan ' + str(len(faltan)) + ' ficheros.'}")
    return 1 if faltan else 0


if __name__ == "__main__":
    raise SystemExit(main())
