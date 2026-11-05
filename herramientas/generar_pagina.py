#!/usr/bin/env python3
"""Genera la versión web del temario: una sola página pensada para leer en el celular.

Uso:
    pip install markdown==3.7
    python3 herramientas/generar_pagina.py salida.html

La página se arma a partir de README.md y de temario/NN-*.md. Si editás un
capítulo, volvé a correr este script para regenerarla.
"""
import html
import re
import sys
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parent.parent
EXTENSIONES = ["tables", "fenced_code", "md_in_html", "sane_lists"]

AVISO = "⚠️?"  # ⚠️ con o sin selector de variante
ETIQUETAS = {
    "\U0001F4A1": ("tip", "Dato"),         # 💡
    "\U0001F4CC": ("tip", "Importante"),   # 📌
    "✅": ("ok", "Control"),           # ✅
}


def md_a_html(texto: str) -> str:
    texto = texto.replace("<details>", '<details markdown="1">')
    return markdown.markdown(texto, extensions=EXTENSIONES)


def texto_plano(fragmento: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", fragmento)).strip()


def pulir(cuerpo: str, cid: str) -> tuple[str, list[tuple[str, str]]]:
    """Ajusta el HTML generado: enlaces, tablas, diagramas, avisos y listas tildables."""
    # Enlaces entre capítulos -> rutas internas de la página.
    cuerpo = re.sub(r'href="(?:temario/)?(\d\d)-[^"]+\.md"', r'href="#cap-\1"', cuerpo)
    # Enlaces externos en pestaña nueva.
    cuerpo = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', cuerpo)
    # Tablas y diagramas con desplazamiento horizontal propio.
    cuerpo = cuerpo.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    cuerpo = cuerpo.replace("<pre><code>", '<div class="pre"><pre><code>').replace("</code></pre>", "</code></pre></div>")

    # Recuadros: citas que empiezan con un emoji pasan a ser recuadros con etiqueta.
    def recuadro(m: re.Match) -> str:
        marca = m.group(1)
        if marca.startswith("⚠"):
            clase, etiqueta = "warn", "Atención"
        else:
            clase, etiqueta = ETIQUETAS[marca]
        return f'<blockquote class="callout {clase}"><p class="callout-label">{etiqueta}</p><p>'

    patron_emoji = "|".join(re.escape(k) for k in ETIQUETAS) + "|" + AVISO
    cuerpo = re.sub(rf"<blockquote>\s*<p>({patron_emoji})\s*", recuadro, cuerpo)
    cuerpo = cuerpo.replace("<blockquote>", '<blockquote class="callout">')

    # Marcas ⚠️ dentro del texto -> etiqueta "verificar".
    chip = '<span class="verify" title="Verificar contra la WPS o la edición vigente del código">verificar</span>'
    cuerpo = re.sub(rf"{AVISO}\s?[Vv]erificar\b", chip, cuerpo)
    cuerpo = re.sub(AVISO, chip, cuerpo)
    # Emojis que quedaron sueltos (dentro de recuadros ya etiquetados o en listas).
    cuerpo = re.sub("(?:\U0001F449|\U0001F4A1|\U0001F4CC|✅) ", "", cuerpo)

    # Listas de tareas "- [ ]" -> casillas tildables.
    contador = iter(range(1, 10_000))

    def tarea(m: re.Match) -> str:
        n = next(contador)
        return (f'<li class="task"><label><input type="checkbox" id="{cid}-t{n}">'
                f"<span>{m.group(1)}</span></label></li>")

    cuerpo = re.sub(r"<li>\[ \] (.*?)</li>", tarea, cuerpo, flags=re.S)
    cuerpo = cuerpo.replace('<ul>\n<li class="task">', '<ul class="tasks">\n<li class="task">')

    # Subtítulos con id para el índice del capítulo.
    secciones: list[tuple[str, str]] = []

    def subtitulo(m: re.Match) -> str:
        sid = f"{cid}-s{len(secciones) + 1}"
        secciones.append((sid, texto_plano(m.group(1))))
        return f'<h2 id="{sid}">{m.group(1)}</h2>'

    cuerpo = re.sub(r"<h2>(.*?)</h2>", subtitulo, cuerpo)
    return cuerpo, secciones


def leer_readme():
    texto = (RAIZ / "README.md").read_text(encoding="utf-8")
    capitulos = {}
    for num, titulo, descripcion in re.findall(
        r"^\| (\d\d) \| \[(.+?)\]\(temario/.+?\) \| (.+?) \|$", texto, flags=re.M
    ):
        capitulos[num] = (titulo, descripcion)
    bloques = {}
    for bloque in re.split(r"^## ", texto, flags=re.M)[1:]:
        titulo, _, cuerpo = bloque.partition("\n")
        bloques[titulo.strip()] = cuerpo.strip().strip("-").strip()
    intro = texto.split("\n---", 1)[0]
    intro = re.sub(r"^# .*\n", "", intro).strip()
    return capitulos, bloques, intro


def armar_capitulos(resumen):
    archivos = sorted((RAIZ / "temario").glob("[0-9][0-9]-*.md"))
    capitulos = []
    for archivo in archivos:
        num = archivo.name[:2]
        cid = f"cap-{num}"
        texto = archivo.read_text(encoding="utf-8")
        h1 = re.match(r"# (.+)\n", texto)
        titulo_largo = h1.group(1).split("·", 1)[-1].strip() if h1 else archivo.stem
        texto = texto[h1.end():] if h1 else texto
        cuerpo, secciones = pulir(md_a_html(texto), cid)
        corto, descripcion = resumen.get(num, (titulo_largo, ""))
        capitulos.append(dict(num=num, cid=cid, titulo=titulo_largo, corto=corto,
                              descripcion=descripcion, cuerpo=cuerpo, secciones=secciones))
    return capitulos


def vista_capitulo(cap, anterior, siguiente) -> str:
    toc = "".join(
        f'<li><button type="button" data-target="{sid}">{html.escape(nombre)}</button></li>'
        for sid, nombre in cap["secciones"]
    )
    toc_html = (f'<details class="toc"><summary>En este capítulo</summary><ol>{toc}</ol></details>'
                if toc else "")

    def enlace(c, rotulo, clase):
        if not c:
            return '<span class="pager-empty" aria-hidden="true"></span>'
        return (f'<a class="{clase}" href="#{c["cid"]}"><small>{rotulo}</small>'
                f'<span>{c["num"]} · {html.escape(c["corto"])}</span></a>')

    return f"""
<article data-view="{cap['cid']}" class="view chapter" data-title="{cap['num']} · {html.escape(cap['corto'])}" hidden>
  <header class="chap-head">
    <p class="chap-num"><span>Capítulo</span>{cap['num']}</p>
    <h1>{html.escape(cap['titulo'])}</h1>
    <p class="chap-sub">{html.escape(cap['descripcion'])}</p>
  </header>
  {toc_html}
  <div class="prose">{cap['cuerpo']}</div>
  <nav class="pager" aria-label="Navegación entre capítulos">
    {enlace(anterior, "Anterior", "prev")}
    {enlace(siguiente, "Siguiente", "next")}
  </nav>
  <p class="back"><a href="#inicio">Volver al índice</a></p>
</article>"""


def vista_inicio(capitulos, bloques, intro) -> str:
    lista = "".join(
        f'<li><a href="#{c["cid"]}"><span class="num">{c["num"]}</span>'
        f'<span class="t">{html.escape(c["corto"])}</span>'
        f'<span class="d">{html.escape(c["descripcion"])}</span></a></li>'
        for c in capitulos
    )
    regla, _ = pulir(md_a_html(bloques.get("La regla de oro", "")), "inicio-regla")
    como, _ = pulir(md_a_html(bloques.get("Cómo usar este temario", "")), "inicio-como")
    ruta, _ = pulir(md_a_html(bloques.get("Ruta resumida", "")), "inicio-ruta")
    aviso, _ = pulir(md_a_html(bloques.get("Aviso", "")), "inicio-aviso")
    intro_html, _ = pulir(md_a_html(intro), "inicio-intro")
    return f"""
<section data-view="inicio" class="view home" data-title="Temario SMAW">
  <header class="hero">
    <p class="eyebrow">SMAW · electrodo revestido · cañería</p>
    <h1>Soldador de cañerías</h1>
    <p class="hero-sub">Temario práctico para rendir la calificación (AWS D1.1 · ASME IX · API 1104)</p>
    <dl class="tag" aria-label="Escenario base del examen">
      <div><dt>Proceso</dt><dd>SMAW (111)</dd></div>
      <div><dt>Posición</dt><dd>6G · 45° ± 5°</dd></div>
      <div><dt>Raíz</dt><dd>E6010 ascendente</dd></div>
      <div><dt>Relleno y presentación</dt><dd>E7018</dd></div>
      <div><dt>Material</dt><dd>A106 Gr. B · P-No. 1</dd></div>
      <div><dt>Ensayo</dt><dd>Visual + doblado</dd></div>
      <div class="wide"><dt>Junta</dt><dd>V 37,5° · talón 1,6 mm · luz 2,4–3,2 mm</dd></div>
    </dl>
    <div class="actions">
      <a class="btn" href="#cap-00">Empezar por el capítulo 00</a>
      <a class="btn secondary" id="seguir" href="#cap-00" hidden>Seguir leyendo</a>
    </div>
  </header>
  <div class="prose">
    <div class="intro">{intro_html}</div>
    <h2>La regla de oro</h2>
    {regla}
    <h2>Capítulos</h2>
    <ol class="chapters">{lista}</ol>
    <h2>Cómo usar este temario</h2>
    {como}
    <h2>Ruta resumida</h2>
    {ruta}
    <h2>Aviso</h2>
    {aviso}
  </div>
</section>"""


ESTILOS = """
/* Layout: manual de bolsillo para el taller. Una columna de lectura (~68ch), barra fija con el
   capítulo actual y, en la portada, una chapa de identificación como la que se ata al cupón. */
:root {
  --bg: #eef1f3; --surface: #ffffff; --ink: #18212a; --muted: #56636f; --line: #d2d9df;
  --accent: #1d5a86; --accent-ink: #ffffff; --heat: #94500e; --heat-bg: #f7ebdc; --heat-line: #e2c4a0;
  --tip-bg: #e6eff6; --tip-line: #bdd2e4; --ok-bg: #e7f2ea; --ok-line: #b9d8c1; --ok: #2b6b3d;
  --code-bg: #e4e9ed; --row: #f4f6f8;
  --font-display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", system-ui, sans-serif;
  --font-body: "Source Sans 3", "Segoe UI", Roboto, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, Menlo, Consolas, monospace;
  --font-diagram: ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", "Roboto Mono", monospace;
  --fs: 17px;
  --bar-h: 56px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #11161b; --surface: #182028; --ink: #e3e8ed; --muted: #9ba8b4; --line: #2b3540;
    --accent: #84b8df; --accent-ink: #0c1822; --heat: #e6a865; --heat-bg: #2a2016; --heat-line: #5b4229;
    --tip-bg: #16232f; --tip-line: #29435b; --ok-bg: #15251a; --ok-line: #2c4c35; --ok: #8fcf9f;
    --code-bg: #0c1115; --row: #1d262f;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #11161b; --surface: #182028; --ink: #e3e8ed; --muted: #9ba8b4; --line: #2b3540;
  --accent: #84b8df; --accent-ink: #0c1822; --heat: #e6a865; --heat-bg: #2a2016; --heat-line: #5b4229;
  --tip-bg: #16232f; --tip-line: #29435b; --ok-bg: #15251a; --ok-line: #2c4c35; --ok: #8fcf9f;
  --code-bg: #0c1115; --row: #1d262f;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body { background: var(--bg); color: var(--ink); font: 400 var(--fs)/1.6 var(--font-body); -webkit-text-size-adjust: 100%; }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 30; background: var(--surface); }
a { color: var(--accent); text-underline-offset: .18em; }
:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; border-radius: 4px; }

/* Barra superior */
.bar {
  position: sticky; top: env(safe-area-inset-top, 0px); z-index: 20; height: var(--bar-h);
  display: flex; align-items: center; gap: 10px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  background: var(--surface); border-bottom: 1px solid var(--line); font-size: 16px;
}
.bar button { font: 600 15px/1 var(--font-body); color: var(--accent); background: transparent; border: 1px solid var(--line); border-radius: 8px; min-height: 40px; min-width: 44px; padding: 0 12px; cursor: pointer; }
.bar-title { flex: 1; min-width: 0; font: 600 19px/1.1 var(--font-display); letter-spacing: .02em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar-tools { display: flex; gap: 6px; }

/* Columna de lectura */
main { width: 100%; max-width: 48rem; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 8px 64px; }
.prose { max-width: 68ch; }
.prose > * + * { margin-top: 0; }
p, ul, ol { margin: 0 0 .9em; }
ul, ol { padding-left: 1.35em; }
li { margin: .3em 0; }
li > ul, li > ol { margin: .3em 0 0; }
h1, h2, h3 { text-wrap: balance; }
h2 { font: 700 1.6em/1.1 var(--font-display); letter-spacing: .01em; margin: 1.9em 0 .6em; padding-top: .7em; border-top: 1px solid var(--line); scroll-margin-top: calc(var(--bar-h) + env(safe-area-inset-top, 0px) + 12px); }
h3 { font: 700 1.12em/1.3 var(--font-body); margin: 1.5em 0 .5em; }
.prose hr { display: none; }
strong { font-weight: 700; }
code { font: 500 .86em/1.4 var(--font-mono); background: var(--code-bg); padding: .1em .35em; border-radius: 4px; overflow-wrap: anywhere; }

/* Tablas y diagramas */
.tbl { overflow-x: auto; margin: 1.1em 0 1.3em; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); -webkit-overflow-scrolling: touch; }
table { border-collapse: collapse; width: 100%; font-size: .9em; line-height: 1.45; font-variant-numeric: tabular-nums; }
th, td { text-align: left; vertical-align: top; padding: .6em .75em; border-bottom: 1px solid var(--line); min-width: 8.5em; }
th { background: var(--row); font-weight: 700; }
tr:last-child td { border-bottom: 0; }
td:first-child { font-weight: 600; }
.pre { overflow-x: auto; margin: 1.1em 0 1.3em; background: var(--code-bg); border-radius: 10px; -webkit-overflow-scrolling: touch; }
.pre pre { margin: 0; padding: .9em 1em; width: max-content; min-width: 100%; }
.pre code { font: 400 12.5px/1.4 var(--font-diagram); background: none; padding: 0; white-space: pre; overflow-wrap: normal; color: var(--ink); }
.scroll-hint { margin: 1.1em 0 -.8em; font: 600 .74em/1 var(--font-mono); letter-spacing: .05em; text-transform: uppercase; color: var(--muted); text-align: right; }

/* Recuadros */
.callout { margin: 1.2em 0; padding: .85em 1em; background: var(--tip-bg); border: 1px solid var(--tip-line); border-radius: 10px; }
.callout p { margin: .25em 0; }
.callout p + p { margin-top: .5em; }
.callout-label { font: 700 .8em/1 var(--font-display); letter-spacing: .1em; text-transform: uppercase; color: var(--accent); margin: 0 0 .45em !important; }
.callout.warn { background: var(--heat-bg); border-color: var(--heat-line); }
.callout.warn .callout-label { color: var(--heat); }
.callout.ok { background: var(--ok-bg); border-color: var(--ok-line); }
.callout.ok .callout-label { color: var(--ok); }
.verify { display: inline-block; font: 600 .66em/1 var(--font-mono); letter-spacing: .05em; text-transform: uppercase; color: var(--heat); background: var(--heat-bg); border: 1px solid var(--heat-line); border-radius: 4px; padding: .28em .4em .22em; vertical-align: .12em; white-space: nowrap; }

/* Respuestas desplegables e índice del capítulo */
details { margin: 1.1em 0; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); padding: 0 1em; }
details[open] { padding-bottom: .6em; }
summary { cursor: pointer; font-weight: 700; min-height: 46px; display: flex; align-items: center; color: var(--accent); }
.toc { margin: 0 0 1.6em; }
.toc ol { margin: 0 0 .4em; padding-left: 1.6em; }
.toc li { margin: 0; }
.toc button { font: inherit; color: var(--ink); background: none; border: 0; padding: .5em 0; text-align: left; cursor: pointer; width: 100%; min-height: 44px; }
.toc button:hover { color: var(--accent); }

/* Listas tildables */
ul.tasks { list-style: none; padding-left: 0; }
li.task { margin: 0; }
li.task label { display: flex; gap: .7em; align-items: flex-start; padding: .45em 0; cursor: pointer; border-bottom: 1px dashed var(--line); }
li.task input { flex: none; width: 1.3em; height: 1.3em; margin: .15em 0 0; accent-color: var(--accent); }
li.task input:checked + span { color: var(--muted); }

/* Encabezado de capítulo */
.chap-head { padding-block: 1.4em 1em; }
.chap-num { display: flex; align-items: baseline; gap: .5em; margin: 0; font: 700 3.4em/1 var(--font-display); color: var(--accent); letter-spacing: .02em; }
.chap-num span { font: 600 .26em/1 var(--font-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.chap-head h1 { font: 700 clamp(1.9rem, 7.5vw, 2.6rem)/1.05 var(--font-display); margin: .15em 0 .35em; }
.chap-sub { color: var(--muted); margin: 0; }

/* Navegación entre capítulos */
.pager { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 2.6em; }
.pager a { display: flex; flex-direction: column; gap: .2em; padding: .8em .9em; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); color: var(--ink); text-decoration: none; min-width: 0; }
.pager a.next { text-align: right; }
.pager small { font: 600 .72em/1 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.pager span { font-weight: 700; color: var(--accent); overflow-wrap: anywhere; }
.back { margin-top: 1.4em; text-align: center; }

/* Portada */
.hero { padding-block: 1.6em .4em; }
.eyebrow { font: 600 .74em/1.3 var(--font-mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 0; }
.hero h1 { font: 700 clamp(2.6rem, 13vw, 4rem)/.92 var(--font-display); text-transform: uppercase; letter-spacing: .01em; margin: .2em 0 .25em; }
.hero-sub { font-size: 1.05em; color: var(--muted); margin: 0 0 1.2em; }
.tag { position: relative; margin: 0 0 1.3em; padding: 1em 1em 1em 2.4em; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; display: grid; grid-template-columns: repeat(auto-fit, minmax(7.6em, 1fr)); gap: .85em 1.2em; }
.tag::before { content: ""; position: absolute; left: .8em; top: 1.15em; width: .85em; height: .85em; border-radius: 50%; border: 2px solid var(--line); background: var(--bg); }
.tag div { min-width: 0; }
.tag .wide { grid-column: 1 / -1; }
.tag dt { font: 600 .78em/1.1 var(--font-display); letter-spacing: .09em; text-transform: uppercase; color: var(--muted); }
.tag dd { margin: .2em 0 0; font: 500 .88em/1.35 var(--font-mono); }
.actions { display: flex; flex-wrap: wrap; gap: 10px; }
.btn { display: inline-flex; align-items: center; min-height: 46px; padding: 0 1.1em; border-radius: 10px; background: var(--accent); color: var(--accent-ink); font-weight: 700; text-decoration: none; border: 1px solid var(--accent); }
.btn.secondary { background: transparent; color: var(--accent); }
.intro { margin-top: 1.2em; }
.intro p { margin: 0 0 .6em; }
ol.chapters { list-style: none; padding: 0; margin: 0; border-top: 1px solid var(--line); }
ol.chapters li { margin: 0; }
ol.chapters a { display: grid; grid-template-columns: 2.6em 1fr; column-gap: .7em; padding: .8em 0; border-bottom: 1px solid var(--line); color: var(--ink); text-decoration: none; }
ol.chapters .num { grid-row: span 2; font: 700 1.7em/1 var(--font-display); color: var(--accent); }
ol.chapters .t { font-weight: 700; }
ol.chapters .d { color: var(--muted); font-size: .9em; line-height: 1.4; }
footer.foot { margin-top: 3em; color: var(--muted); font-size: .85em; }
@media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; } }
"""

SCRIPT = """
(function () {
  var views = Array.prototype.slice.call(document.querySelectorAll('.view'));
  var barTitle = document.getElementById('bar-title');
  var seguir = document.getElementById('seguir');
  var reducir = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function leer(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function guardar(k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }

  function marcarDesplazables(raiz) {
    raiz.querySelectorAll('.tbl, .pre').forEach(function (el) {
      var prev = el.previousElementSibling;
      var tiene = prev && prev.classList.contains('scroll-hint');
      var desborda = el.scrollWidth > el.clientWidth + 4;
      if (desborda && !tiene) {
        var p = document.createElement('p');
        p.className = 'scroll-hint';
        p.textContent = 'Deslizá para ver todo →';
        el.parentNode.insertBefore(p, el);
      } else if (!desborda && tiene) {
        prev.parentNode.removeChild(prev);
      }
    });
  }

  function actualizarSeguir() {
    var ultimo = leer('temario:ultimo');
    var vista = ultimo && document.querySelector('[data-view="' + ultimo.replace(/[^a-z0-9-]/gi, '') + '"]');
    if (vista && vista.classList.contains('chapter')) {
      seguir.hidden = false;
      seguir.href = '#' + ultimo;
      seguir.textContent = 'Seguir leyendo: ' + vista.getAttribute('data-title');
    } else {
      seguir.hidden = true;
    }
  }

  function mostrar() {
    var id = (window.location.hash || '').slice(1);
    var destino = views.filter(function (v) { return v.getAttribute('data-view') === id; })[0] || views[0];
    views.forEach(function (v) { v.hidden = v !== destino; });
    barTitle.textContent = destino.getAttribute('data-title');
    if (destino.classList.contains('chapter')) guardar('temario:ultimo', destino.getAttribute('data-view'));
    actualizarSeguir();
    window.scrollTo(0, 0);
    marcarDesplazables(destino);
  }

  document.getElementById('btn-indice').addEventListener('click', function () {
    if (window.location.hash === '#inicio') { mostrar(); } else { window.location.hash = 'inicio'; }
  });

  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-target]') : null;
    if (!b) return;
    var t = document.getElementById(b.getAttribute('data-target'));
    if (t) t.scrollIntoView({ behavior: reducir ? 'auto' : 'smooth', block: 'start' });
  });

  document.querySelectorAll('li.task input').forEach(function (cb) {
    cb.checked = leer('temario:chk:' + cb.id) === '1';
    cb.addEventListener('change', function () { guardar('temario:chk:' + cb.id, cb.checked ? '1' : '0'); });
  });

  var fs = parseInt(leer('temario:fs'), 10) || 17;
  function aplicarLetra() {
    document.documentElement.style.setProperty('--fs', fs + 'px');
    var visible = views.filter(function (v) { return !v.hidden; })[0];
    if (visible) marcarDesplazables(visible);
  }
  document.getElementById('fs-down').addEventListener('click', function () { fs = Math.max(14, fs - 1); guardar('temario:fs', fs); aplicarLetra(); });
  document.getElementById('fs-up').addEventListener('click', function () { fs = Math.min(24, fs + 1); guardar('temario:fs', fs); aplicarLetra(); });

  window.addEventListener('hashchange', mostrar);
  window.addEventListener('resize', function () {
    var visible = views.filter(function (v) { return !v.hidden; })[0];
    if (visible) marcarDesplazables(visible);
  });
  aplicarLetra();
  mostrar();
})();
"""


def main():
    salida = Path(sys.argv[1] if len(sys.argv) > 1 else "temario.html")
    resumen, bloques, intro = leer_readme()
    capitulos = armar_capitulos(resumen)
    vistas = [vista_inicio(capitulos, bloques, intro)]
    for i, cap in enumerate(capitulos):
        anterior = capitulos[i - 1] if i > 0 else None
        siguiente = capitulos[i + 1] if i + 1 < len(capitulos) else None
        vistas.append(vista_capitulo(cap, anterior, siguiente))

    pagina = f"""<title>Temario Soldador de Cañerías</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=JetBrains+Mono:wght@500;600&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>{ESTILOS}</style>
<header class="bar">
  <button type="button" id="btn-indice" aria-label="Ir al índice de capítulos">Índice</button>
  <div class="bar-title" id="bar-title" aria-live="polite">Temario SMAW</div>
  <div class="bar-tools">
    <button type="button" id="fs-down" aria-label="Achicar la letra">A−</button>
    <button type="button" id="fs-up" aria-label="Agrandar la letra">A+</button>
  </div>
</header>
<main>
{''.join(vistas)}
<footer class="foot"><p>Temario de estudio armado a partir de fuentes públicas (ver capítulo 11). No reemplaza la WPS del examen ni las normas originales.</p></footer>
</main>
<script>{SCRIPT}</script>
"""
    salida.write_text(pagina, encoding="utf-8")
    print(f"Página generada: {salida} ({salida.stat().st_size // 1024} KB, {len(capitulos)} capítulos)")


if __name__ == "__main__":
    main()
