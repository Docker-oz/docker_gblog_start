#!/usr/bin/env python3
"""Arma el sitio publicable de G-Blog en site/ a partir de demo/.

Uso:
    python3 demo/scripts/construir_sitio.py                      # sin contador
    python3 demo/scripts/construir_sitio.py --goatcounter CODIGO # con GoatCounter

Pasos: regenera los artículos desde docs/, actualiza lecturas y destacado (si hay código
de GoatCounter) y copia solo lo publicable (páginas .html y assets/) a site/.
"""
import argparse, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO, SITE, SCRIPTS = ROOT / "demo", ROOT / "site", Path(__file__).resolve().parent
TAG = re.compile(r'\s*<script>window\.goatcounter = [^<]*</script>|\s*<script data-goatcounter="[^"]*"[^>]*></script>')

ap = argparse.ArgumentParser()
ap.add_argument("--goatcounter", default="", help="código del sitio en GoatCounter")
a = ap.parse_args()

subprocess.run([sys.executable, str(SCRIPTS / "construir_serie.py"), str(ROOT)], check=True)
if a.goatcounter:
    r = subprocess.run([sys.executable, str(SCRIPTS / "actualizar_lecturas.py"), "--codigo", a.goatcounter])
    if r.returncode:
        print("Aviso: no se actualizaron las lecturas; se publica sin cambios en el destacado.")

if SITE.exists():
    shutil.rmtree(SITE)
SITE.mkdir()
shutil.copytree(DEMO / "assets", SITE / "assets")
for f in DEMO.glob("*.html"):
    s = f.read_text(encoding="utf-8")
    s = s.replace("TU-CODIGO", a.goatcounter) if a.goatcounter else TAG.sub("", s)
    (SITE / f.name).write_text(s, encoding="utf-8")
(SITE / ".nojekyll").write_text("")
print(f"Sitio listo en {SITE} ({len(list(SITE.glob('*.html')))} páginas)")
