#!/usr/bin/env python3
"""Actualiza las lecturas y el artículo destacado de G-Blog a partir de GoatCounter.

Se corre antes de publicar (o al regenerar el sitio):

    python3 demo/scripts/actualizar_lecturas.py --codigo TU-CODIGO
    python3 demo/scripts/actualizar_lecturas.py --desde demo/data/conteos-ejemplo.json   # sin internet

Qué hace:
  1. Lee las visitas de cada artículo (identificador fijo: ss-intro, ss-1-1, ...).
  2. Escribe "N lecturas" en cada artículo y el total de la serie.
  3. Pone en el destacado de la portada el artículo más leído (y su ícono, si existe en demo/iconos/).
  4. Guarda un registro en demo/data/lecturas.json.

Requisito en GoatCounter: activar en Settings la opción que permite mostrar los conteos
en el sitio (visitor counter); sin ella, el endpoint /counter/ no responde.
Si GoatCounter no responde, el script no cambia nada y lo avisa.
"""
import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEMO = Path(__file__).resolve().parent.parent


def articulos():
    out = []
    for f in sorted(DEMO.glob("ss-*.html")):
        s = f.read_text(encoding="utf-8")
        m = re.search(r'data-gc="([\w-]+)"', s)
        h1 = re.search(r"<h1>(.*?)</h1>", s, re.S)
        if not (m and h1):
            continue
        num = re.search(r'<span class="num">([^<]+)</span>', h1.group(1))
        titulo = re.sub(r"<[^>]+>", "", re.sub(r'<span class="num">[^<]+</span>', "", h1.group(1))).strip()
        out.append(dict(id=m.group(1), archivo=f.name, num=num.group(1) if num else "", titulo=html.unescape(titulo)))
    return out


def conteo_goatcounter(codigo, ident):
    ruta = urllib.parse.quote("/" + ident, safe="")
    url = f"https://{codigo}.goatcounter.com/counter/{ruta}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "gblog-lecturas/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            datos = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:  # GoatCounter responde 404 cuando la ruta aún no tiene visitas
            return 0
        raise
    return int(re.sub(r"\D", "", str(datos.get("count", "0"))) or 0)


def fmt(n):
    return f"{n:,} {'lectura' if n == 1 else 'lecturas'}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--codigo", help="código del sitio en GoatCounter (el subdominio)")
    ap.add_argument("--desde", type=Path, help="archivo JSON {id: visitas}, para probar sin GoatCounter")
    ap.add_argument("--minimo", type=int, default=10, help="visitas mínimas para reemplazar el destacado fijo (10)")
    a = ap.parse_args()
    if not (a.codigo or a.desde):
        ap.error("indica --codigo o --desde")

    arts = articulos()
    if not arts:
        sys.exit("No encontré artículos ss-*.html en " + str(DEMO))

    conteos = {}
    if a.desde:
        conteos = {k: int(v) for k, v in json.loads(a.desde.read_text(encoding="utf-8")).items()}
    else:
        try:
            for art in arts:
                conteos[art["id"]] = conteo_goatcounter(a.codigo, art["id"])
        except Exception as e:  # sin conexión, código incorrecto o contador no habilitado
            sys.exit(f"GoatCounter no respondió ({e}). No se cambió nada.")

    # 1. Lecturas por artículo y total de la serie, en todas las páginas
    total = sum(conteos.get(x["id"], 0) for x in arts)
    for f in DEMO.glob("*.html"):
        s = f.read_text(encoding="utf-8")
        nuevo = re.sub(
            r'<span class="label reads" data-gc="([\w-]+)"[^>]*>.*?</span>',
            lambda m: (f'<span class="label reads" data-gc="{m.group(1)}">{fmt(conteos[m.group(1)])}</span>'
                       if conteos.get(m.group(1), 0) > 0 else
                       f'<span class="label reads" data-gc="{m.group(1)}" hidden></span>'),
            s, flags=re.S)
        nuevo = re.sub(
            r'<span class="reads" data-gc-total="ss"[^>]*>.*?</span>',
            (f'<span class="reads" data-gc-total="ss"> · {fmt(total)}</span>' if total > 0 else
             '<span class="reads" data-gc-total="ss" hidden></span>'),
            nuevo, flags=re.S)
        if nuevo != s:
            f.write_text(nuevo, encoding="utf-8")

    # 2. Destacado de la portada
    candidatos = [x for x in arts if conteos.get(x["id"], 0) >= a.minimo]
    idx = DEMO / "index.html"
    s = idx.read_text(encoding="utf-8")
    if candidatos:
        top = max(candidatos, key=lambda x: conteos[x["id"]])
        etiqueta = f'Lo más leído · SS-Courses {top["num"] or "Introducción"} · {fmt(conteos[top["id"]])}'
    else:
        top = next(x for x in arts if x["id"] == "ss-1-1")
        etiqueta = "Destacado · SS-Courses 1.1"
    cap = (f'<!-- DESTACADO:inicio --><figcaption><a href="{top["archivo"]}"><span class="label accent">'
           f'{html.escape(etiqueta)}</span><strong>{html.escape(top["titulo"])}</strong></a></figcaption><!-- DESTACADO:fin -->')
    s = re.sub(r"<!-- DESTACADO:inicio -->.*?<!-- DESTACADO:fin -->", cap, s, flags=re.S)
    icono = DEMO / "iconos" / f'{top["id"]}.svg.html'
    sin_icono = not icono.exists()
    if not sin_icono:
        s = re.sub(r"<!-- ICONO:inicio -->.*?<!-- ICONO:fin -->",
                   lambda m: "<!-- ICONO:inicio -->" + icono.read_text(encoding="utf-8").strip() + "<!-- ICONO:fin -->",
                   s, flags=re.S)
    idx.write_text(s, encoding="utf-8")

    # 3. Registro
    reg = DEMO / "data" / "lecturas.json"
    reg.parent.mkdir(exist_ok=True)
    reg.write_text(json.dumps({"actualizado": dt.datetime.now().isoformat(timespec="seconds"),
                               "fuente": "archivo" if a.desde else "goatcounter",
                               "total_serie": total, "destacado": top["id"], "conteos": conteos},
                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Serie SS-Courses: {fmt(total)}")
    for x in sorted(arts, key=lambda x: -conteos.get(x["id"], 0)):
        print(f'  {x["id"]:<8} {conteos.get(x["id"], 0):>7}  {x["titulo"]}')
    print(f'Destacado: {top["titulo"]}' + ("  (sin ícono propio en demo/iconos/, se conserva el actual)" if sin_icono else ""))


if __name__ == "__main__":
    main()
