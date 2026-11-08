"""Genera los artículos de la serie SS-Courses (demo/ss-*.html) a partir de docs/*.md.

Uso: python3 demo/scripts/construir_serie.py
Requiere: pip install -r demo/scripts/requirements.txt
No modifica docs/. Respeta el texto de "Sobre esta serie" en serie-ss-courses.html y solo
actualiza su ruta de lectura.
"""
import re, sys, html
from pathlib import Path
import markdown

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
DOCS, DEMO = ROOT / "docs", ROOT / "demo"

SERIES = [
    dict(slug="ss-introduccion-que-es-swirlify", src="index.md", part="0", part_name="Introducción", num="",
         title="¿Qué es Swirlify?", date="21 sep 2026", start="### ¿Qué es Swirlify?",
         dek="El paquete de R para crear lecciones interactivas, para qué sirve y cómo está organizada esta serie."),
    dict(slug="ss-1-1-quienes-son-tus-aprendices", src="1_modelos_mentales/1-1_quienes_son_mis_aprendices.md", part="1",
         part_name="Parte 1 · Los cimientos cognitivos", num="1.1", title="¿Quiénes son tus aprendices?", date="28 sep 2026",
         dek="Damos por sentado que conocemos a nuestro público. Diseñar para todos empieza por reconocerlos."),
    dict(slug="ss-1-2-la-mente-del-aprendiz", src="1_modelos_mentales/1-2_la_mente_del_aprendiz.md", part="1",
         part_name="Parte 1 · Los cimientos cognitivos", num="1.2", title="La mente del aprendiz", date="05 oct 2026", end="### 1.2.3 ",
         dek="Modelos mentales, máquina nocional y carga cognitiva: qué pasa cuando el facilitador no los gestiona."),
    dict(slug="ss-1-3-construir-una-maquina-nocional", src="1_modelos_mentales/1-2_la_mente_del_aprendiz.md", part="1",
         part_name="Parte 1 · Los cimientos cognitivos", num="1.3", title="Construir una máquina nocional", date="12 oct 2026", start="### 1.2.3 ",
         renum={"1.2.3": "1.3.1"},
         dek="El mismo tema, ahora con una carga cognitiva bien gestionada: una sesión dividida en cinco interacciones."),
    dict(slug="ss-2-1-tuerca-tornillo-y-archivo", src="2_entranas/2-1_archivos_directorios.md", part="2",
         part_name="Parte 2 · El laboratorio técnico", num="2.1", title="Tuerca, tornillo y archivo", date="19 oct 2026", end="### 2.1.2 ",
         dek="Los archivos obligatorios de una lección de Swirlify: lesson.yaml, initLesson.R, dependson.txt y customTests.R."),
    dict(slug="ss-2-2-carpetas-especiales-y-motor-de-swirl", src="2_entranas/2-1_archivos_directorios.md", part="2",
         part_name="Parte 2 · El laboratorio técnico", num="2.2", title="Carpetas especiales y el motor de swirl", date="26 oct 2026", start="### 2.1.2 ",
         renum={"2.1.2": "2.2.1", "2.1.3": "2.2.2"},
         dek="MANIFEST, la carpeta de scripts y cómo el motor de swirl recorre una lección paso a paso."),
    dict(slug="ss-2-3-chasis-de-un-curso", src="2_entranas/2-2_geochip-r.md", part="2",
         part_name="Parte 2 · El laboratorio técnico", num="2.3", title="Chasis de un curso: GEOCHIP-R", date="02 nov 2026",
         renum={"2.2.1": "2.3.1", "2.2.2": "2.3.2"},
         dek="Un curso real de Swirlify armado archivo por archivo, de la raíz a cada subtema."),
]

ADM_ES = {"note": "Nota", "abstract": "Resumen", "info": "Información", "tip": "Consejo", "success": "Éxito",
          "question": "Pregunta", "warning": "Advertencia", "failure": "Fallo", "danger": "Peligro",
          "bug": "Error", "example": "Ejemplo", "quote": "Cita"}
ALIAS = {"nota": "note", "consejo": "tip", "advertencia": "warning", "peligro": "danger", "cita": "quote",
         "ejemplo": "example", "pregunta": "question", "resumen": "abstract", "summary": "abstract", "tldr": "abstract",
         "hint": "tip", "important": "tip", "check": "success", "done": "success", "help": "question", "faq": "question",
         "caution": "warning", "attention": "warning", "fail": "failure", "missing": "failure", "error": "danger",
         "cite": "quote", "todo": "info"}


def prepare(md, start=None, end=None, renum=None):
    if start:
        md = md[md.index(start):]
    if end:
        md = md[:md.index(end)]
    for o, n in (renum or {}).items():
        md = re.sub(r"^(#{3,4} )" + re.escape(o), lambda m: m.group(1) + n, md, flags=re.M)
    out, fence, dropped_h1 = [], False, False
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.lstrip().startswith("```"):
            fence = not fence
        if not fence:
            m = re.match(r"^(\s*)(!!!|\?\?\?\+?)\s+(\w+)(.*)$", ln)
            if m:
                t = m.group(3).lower()
                ln = f"{m.group(1)}{m.group(2)} {ALIAS.get(t, t)}{m.group(4)}"
            if not dropped_h1 and re.match(r"^# ", ln):
                dropped_h1 = True
                if i + 1 < len(lines) and re.match(r"^\s*(-{3,}|_{3,})\s*$", lines[i + 1]):
                    i += 1
                i += 1
                continue
            ln = re.sub(r"^### ", "## ", ln)
            ln = re.sub(r"^#### ", "### ", ln)
        out.append(ln)
        i += 1
    return "\n".join(out)


def render(md):
    h = markdown.markdown(md, extensions=["admonition", "pymdownx.details", "pymdownx.superfences", "attr_list",
                                          "md_in_html", "tables", "toc"],
                          extension_configs={"toc": {"slugify": lambda v, s: re.sub(r"[^\w]+", "-", v.lower()).strip("-")}})
    def title_fix(m):
        kind, title = m.group(1).split()[0], m.group(2)
        if title.strip().lower() in (kind, kind.capitalize().lower()):
            title = ADM_ES.get(kind, title)
        return f'<div class="admonition {m.group(1)}"><p class="admonition-title"><i aria-hidden="true"></i>{title}</p>'
    h = re.sub(r'<div class="admonition ([\w ]+)">\s*<p class="admonition-title">(.*?)</p>', title_fix, h, flags=re.S)
    h = re.sub(r'<details class="([\w ]+)">\s*<summary>(.*?)</summary>',
               lambda m: f'<details class="admonition {m.group(1)}"><summary class="admonition-title"><i aria-hidden="true"></i>{m.group(2)}</summary>', h, flags=re.S)
    return h


def lab(a):
    return a["num"] or "Intro"

def full(a):
    return (a["num"] + " · " if a["num"] else "") + a["title"]

def step_html(s, cur):
    on = s is cur
    cls = "step on" if on else "step"
    extra = ' aria-current="step"' if on else ""
    return '<a href="' + s["slug"] + '.html" class="' + cls + '" aria-label="' + full(s) + '"' + extra + '></a>'

def num_html(a):
    return f'<span class="num">{a["num"]}</span> ' if a["num"] else ""

def words(h):
    return len(re.sub(r"<[^>]+>", " ", h).split())


tpl = (DEMO / "archivo.html").read_text()
HEAD = tpl[: tpl.index('<main id="main">') + len('<main id="main">')]
FOOT = tpl[tpl.index("</main>"):]

def page(title, body, current="Archivo", gc=None):
    h = HEAD.replace("<title>Archivo · G-Blog</title>", f"<title>{html.escape(title)} · G-Blog</title>")
    h = h.replace(' aria-current="page"', "")
    if current:
        h = h.replace(f'><strong>{current}</strong>', f' aria-current="page"><strong>{current}</strong>', 1)
    foot = FOOT
    if gc:
        foot = foot.replace("</body>", f'<script>window.goatcounter = {{path: "/{gc}"}};</script>\n<script data-goatcounter="https://TU-CODIGO.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n</body>')
    return h + body + foot

for a in SERIES:
    a["id"] = "ss-" + (a["num"].replace(".", "-") if a["num"] else "intro")

for i, a in enumerate(SERIES):
    raw = (DOCS / a["src"]).read_text()
    body = render(prepare(raw, a.get("start"), a.get("end"), a.get("renum")))
    a["min"] = max(1, round(words(body) / 200))
    toc = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    toc_html = ""
    if len(toc) > 1:
        toc_html = '<nav class="toc-inline" aria-label="En este artículo"><span class="label">En este artículo</span><ol>' + \
            "".join(f'<li><a href="#{i_}">{re.sub("<[^>]+>", "", t)}</a></li>' for i_, t in toc) + "</ol></nav>"
    prev = SERIES[i - 1] if i else None
    nxt = SERIES[i + 1] if i + 1 < len(SERIES) else None
    pager = '<nav class="pager wrap narrow" aria-label="Artículos de la serie">'
    pager += (f'<a href="{prev["slug"]}.html"><span class="label">← Anterior · {lab(prev)}</span><h3>{prev["title"]}</h3></a>'
              if prev else '<a href="serie-ss-courses.html"><span class="label">← Serie</span><h3>SS-Courses: ruta de lectura</h3></a>')
    pager += (f'<a class="next" href="{nxt["slug"]}.html"><span class="label">Siguiente · {lab(nxt)} →</span><h3>{nxt["title"]}</h3></a>'
              if nxt else '<a class="next" href="serie-ss-courses.html"><span class="label">Fin de la serie →</span><h3>Volver a la ruta de lectura</h3></a>')
    pager += "</nav>"
    progress = "".join(step_html(s_, a) for s_ in SERIES)
    a["_body"] = body
    a["_toc"], a["_pager"], a["_progress"] = toc_html, pager, progress

for i, a in enumerate(SERIES):
    art = f'''<article>
<header class="post-head narrow wrap"><nav class="label" aria-label="Ruta"><a href="index.html">Inicio</a> / <a href="serie-ss-courses.html">SS-Courses</a> / {a["part_name"]}</nav>
<div class="series-progress"><span class="label">Serie SS-Courses · {i + 1} de {len(SERIES)}</span><div class="steps">{a["_progress"]}</div></div>
<h1>{('<span class="num">' + a["num"] + '</span> ') if a["num"] else ""}{a["title"]}</h1>
<p class="dek">{a["dek"]}</p>
<div class="byline"><span class="label">Por olivinöz</span><span class="label">{a["date"]}</span><span class="label">{a["min"]} min de lectura</span><span class="label reads" data-gc="{a["id"]}" hidden></span><a class="tag" href="serie-ss-courses.html">{a["part_name"]}</a></div></header>
<div class="prose narrow wrap">
{a["_toc"]}
{a["_body"]}
</div>
{a["_pager"]}
</article>'''
    (DEMO / f'{a["slug"]}.html').write_text(page(a["title"], art, gc=a["id"]))

# Página de la serie
idx = (DOCS / "index.md").read_text()
letter_md = idx[idx.index("\n", idx.index("# Bienvenida")):idx.index("### ¿Qué es Swirlify?")]
letter_md = re.sub(r'\*\*ATTE\.:.*', "", letter_md)
letter_md = re.sub(r"^\s*-{3,}\s*$", "", letter_md, flags=re.M)
letter = render(letter_md)
parts = [("0", "Introducción", "Qué es Swirlify, para qué sirve y cómo se organiza la serie."),
         ("1", "Parte 1 · Los cimientos cognitivos", "El detrás de escena pedagógico: modelos mentales y carga cognitiva."),
         ("2", "Parte 2 · El laboratorio técnico", "Archivos, sintaxis y entrañas de una lección de Swirlify, con un curso real.")]
route = ""
for p, name, desc in parts:
    items = "".join(f'<li><a href="{s["slug"]}.html"><span class="num">{lab(s)}</span><span><strong>{s["title"]}</strong><span class="label">{s["min"]} min · {s["date"]}</span></span></a></li>' for s in SERIES if s["part"] == p)
    route += f'<section class="route-part"><div class="label accent">{name}</div><p>{desc}</p><ol>{items}</ol></section>'
total = sum(s["min"] for s in SERIES)
serie = f'''<div class="wrap narrow">
<header class="post-head"><nav class="label" aria-label="Ruta"><a href="index.html">Inicio</a> / Series</nav>
<div class="label accent" style="margin-top:16px">Serie · {len(SERIES)} artículos · {total} min</div>
<h1>Self Swirl-Courses <span class="accent">(SS-Courses)</span></h1>
<p class="dek">Cómo diseñar lecciones interactivas de R con <em>Swirlify</em>, uniendo la instrucción activa de <em>Teaching Tech Together</em> con el estándar EC0366.</p>
<div class="actions"><a class="btn" href="{SERIES[0]["slug"]}.html">Empezar por la introducción</a><a class="btn ghost" href="#ruta">Ver la ruta de lectura</a></div>
<div class="rule-double" style="margin-top:32px"></div></header>
<section class="prose letter" aria-labelledby="h-carta"><h2 id="h-carta">Carta de bienvenida</h2>{letter}<p class="firma">ATTE.: "olivinöz"</p></section>
<section id="ruta" class="route" aria-labelledby="h-ruta"><h2 id="h-ruta">Ruta de lectura</h2>{route}</section>
</div>'''
import os
if os.environ.get('REBUILD_SERIE'): (DEMO / "serie-ss-courses.html").write_text(page("Self Swirl-Courses (SS-Courses)", serie, current=None))
else:
    sp = DEMO / "serie-ss-courses.html"; cur = sp.read_text()
    cur = re.sub(r'<section id="ruta".*?</section>(?=\s*</div>)', f'<section id="ruta" class="route" aria-labelledby="h-ruta"><h2 id="h-ruta">Ruta de lectura</h2>{route}</section>', cur, count=1, flags=re.S)
    cur = re.sub(r'Serie · \d+ artículos · \d+ min', f'Serie · {len(SERIES)} artículos · {total} min', cur)
    cur = re.sub(r'<a class="btn" href="[^"]+">Empezar por[^<]*</a>', f'<a class="btn" href="{SERIES[0]["slug"]}.html">Empezar por la introducción</a>', cur)
    sp.write_text(cur)

import json
(DEMO / ".series.json").write_text(json.dumps([{k: v for k, v in s.items() if not k.startswith("_")} for s in SERIES], ensure_ascii=False))
print("ok", [(s["num"], s["min"]) for s in SERIES])
