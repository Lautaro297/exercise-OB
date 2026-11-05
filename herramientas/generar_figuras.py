#!/usr/bin/env python3
"""Genera las figuras SVG del temario en figuras/.

Uso: python3 herramientas/generar_figuras.py

Cada SVG usa variables CSS (--ink, --accent, --heat, --metal, --weld...) con valores de
respaldo, así se ve bien suelto (por ejemplo en GitHub) y, dentro de la página web, toma
los colores del tema claro u oscuro. Los id internos llevan el prefijo FIGID, que el
generador de la página reemplaza por uno único en cada aparición.
"""
import math
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "figuras"

STYLE = """<style>
.f-bg{fill:var(--fig-bg,#ffffff)}
.f-ln{fill:none;stroke:var(--ink,#18212a);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.f-dash{fill:none;stroke:var(--muted,#56636f);stroke-width:1;stroke-dasharray:4 3}
.f-rip{fill:none;stroke:var(--muted,#56636f);stroke-width:.8}
.f-mt{fill:var(--metal,#cdd5dc);stroke:var(--ink,#18212a);stroke-width:1.2;stroke-linejoin:round}
.f-wd{fill:var(--weld,#f1cf9f);stroke:var(--ink,#18212a);stroke-width:1;stroke-linejoin:round}
.f-wd2{fill:var(--weld2,#e6b07a);stroke:var(--ink,#18212a);stroke-width:1;stroke-linejoin:round}
.f-wd3{fill:var(--weld3,#d69356);stroke:var(--ink,#18212a);stroke-width:1;stroke-linejoin:round}
.f-hole{fill:var(--fig-bg,#ffffff);stroke:var(--ink,#18212a);stroke-width:1.2}
.f-holeh{fill:var(--fig-bg,#ffffff);stroke:var(--heat,#94500e);stroke-width:2}
.f-pore{fill:var(--fig-bg,#ffffff);stroke:var(--heat,#94500e);stroke-width:1.6}
.f-ac{fill:none;stroke:var(--accent,#1d5a86);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.f-ht{fill:none;stroke:var(--heat,#94500e);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.f-defl{fill:none;stroke:var(--heat,#94500e);stroke-width:3;stroke-linecap:round}
.f-defbox{fill:none;stroke:var(--heat,#94500e);stroke-width:1.8;stroke-dasharray:3 2}
.f-tack{fill:none;stroke:var(--heat,#94500e);stroke-width:12}
.f-zp{fill:none;stroke:var(--accent,#1d5a86);stroke-width:7}
.f-zv{fill:none;stroke:var(--muted,#56636f);stroke-width:7}
.f-zs{fill:none;stroke:var(--heat,#94500e);stroke-width:7}
.f-sp{fill:none;stroke:var(--weld2,#e6b07a);stroke-width:10}
.f-spw{fill:none;stroke:var(--heat,#94500e);stroke-width:10}
.f-spm{fill:none;stroke:var(--weld2,#e6b07a);stroke-width:6}
.f-el{fill:none;stroke:var(--ink,#18212a);stroke-width:5;stroke-linecap:round}
.f-elt{fill:none;stroke:var(--heat,#94500e);stroke-width:5;stroke-linecap:round}
.f-inkf{fill:var(--ink,#18212a)}
.f-acf{fill:var(--accent,#1d5a86)}
.f-htf{fill:var(--heat,#94500e)}
.f-tx{fill:var(--ink,#18212a);font-family:var(--font-body,system-ui,sans-serif);font-size:12px;font-weight:600}
.f-sm{fill:var(--muted,#56636f);font-family:var(--font-body,system-ui,sans-serif);font-size:11px}
.f-hd{fill:var(--ink,#18212a);font-family:var(--font-display,system-ui,sans-serif);font-size:15px;font-weight:700;letter-spacing:.06em}
.f-ach{fill:var(--accent,#1d5a86);font-family:var(--font-display,system-ui,sans-serif);font-size:13px;font-weight:700;letter-spacing:.05em}
.f-hth{fill:var(--heat,#94500e);font-family:var(--font-display,system-ui,sans-serif);font-size:13px;font-weight:700;letter-spacing:.05em}
</style>"""

AK = 'marker-end="url(#FIGID-ak)"'
AA = 'marker-end="url(#FIGID-aa)"'
AH = 'marker-end="url(#FIGID-ah)"'
TAN = math.tan(math.radians(37.5))


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def T(x, y, s, cls="f-tx", anchor="start"):
    return f'<text x="{n(x)}" y="{n(y)}" class="{cls}" text-anchor="{anchor}">{escape(s)}</text>'


def L(x1, y1, x2, y2, cls="f-ln", extra=""):
    return f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" class="{cls}" {extra}/>'


def P(pts, cls):
    return f'<polygon points="{" ".join(f"{n(x)},{n(y)}" for x, y in pts)}" class="{cls}"/>'


def D(d, cls, extra=""):
    return f'<path d="{d}" class="{cls}" {extra}/>'


def R(x, y, w, h, cls):
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" class="{cls}"/>'


def C(cx, cy, r, cls):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" class="{cls}"/>'


def E(cx, cy, rx, ry, cls, extra=""):
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" class="{cls}" {extra}/>'


def EL(xh, yh, xt, yt):
    """Electrodo desde el extremo de la pinza (xh, yh) hasta la punta (xt, yt)."""
    lx, ly = xt - xh, yt - yh
    d = math.hypot(lx, ly)
    xm, ym = xt - lx / d * 8, yt - ly / d * 8
    return L(xh, yh, xm, ym, "f-el") + L(xm, ym, xt, yt, "f-elt")


def PC(cx, cy, r, th):
    """Punto en el reloj: th en grados, en sentido horario desde las 12."""
    a = math.radians(th)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def arco(cx, cy, r, a1, a2, cls, extra="", large=None, sweep=1):
    x1, y1 = PC(cx, cy, r, a1)
    x2, y2 = PC(cx, cy, r, a2)
    if large is None:
        large = 1 if abs(a2 - a1) > 180 else 0
    return D(f"M{n(x1)} {n(y1)} A{n(r)} {n(r)} 0 {large} {sweep} {n(x2)} {n(y2)}", cls, extra)


def svg(title, w, h, body):
    marcador = ('<marker id="FIGID-{k}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" '
                'markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="{c}"/></marker>')
    defs = "<defs>" + "".join(marcador.format(k=k, c=c) for k, c in
                              (("ak", "f-inkf"), ("aa", "f-acf"), ("ah", "f-htf"))) + "</defs>"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
            f'aria-labelledby="FIGID-t"><title id="FIGID-t">{escape(title)}</title>{STYLE}{defs}'
            f'<rect class="f-bg" x="0" y="0" width="{w}" height="{h}" rx="10"/>{"".join(body)}</svg>\n')


def junta(cx, ytop, t, land, hg, run, x_izq, x_der):
    izq = [(x_izq, ytop), (cx - hg - run, ytop), (cx - hg, ytop + t - land), (cx - hg, ytop + t), (x_izq, ytop + t)]
    der = [(x_der, ytop), (cx + hg + run, ytop), (cx + hg, ytop + t - land), (cx + hg, ytop + t), (x_der, ytop + t)]
    return P(izq, "f-mt") + P(der, "f-mt")


# ───────────────────────── figuras ─────────────────────────

def fig_posiciones():
    b = [T(12, 22, "PLACA", "f-hd")]
    placas = [("1G", "plana"), ("2G", "horizontal"), ("3G", "vertical"), ("4G", "sobrecabeza")]
    for i, (cod, desc) in enumerate(placas):
        x = i * 90
        if i == 0:
            b += [P([(x + 12, 88), (x + 62, 88), (x + 78, 64), (x + 28, 64)], "f-mt"),
                  L(x + 37, 88, x + 53, 64, "f-ht"), EL(x + 45, 30, x + 45, 75)]
        elif i == 1:
            b += [R(x + 18, 32, 40, 62, "f-mt"), L(x + 18, 63, x + 58, 63, "f-ht"), EL(x + 86, 52, x + 60, 63)]
        elif i == 2:
            b += [R(x + 18, 32, 40, 62, "f-mt"), L(x + 38, 32, x + 38, 94, "f-ht"),
                  L(x + 26, 90, x + 26, 42, "f-ac", AA), EL(x + 82, 86, x + 40, 66)]
        else:
            b += [P([(x + 12, 56), (x + 62, 56), (x + 78, 32), (x + 28, 32)], "f-mt"),
                  L(x + 37, 56, x + 53, 32, "f-ht"), EL(x + 45, 100, x + 45, 46)]
        b += [T(x + 45, 118, cod, "f-tx", "middle"), T(x + 45, 132, desc, "f-sm", "middle")]

    b.append(T(12, 168, "CAÑO", "f-hd"))
    cy = 226

    def cil_h(cx):
        return R(cx - 33, cy - 15, 66, 30, "f-mt") + E(cx + 33, cy, 6, 15, "f-mt") + E(cx, cy, 5, 15, "f-ht")

    canos = [("1G", "gira"), ("2G", "eje vertical"), ("5G", "eje horizontal"), ("6G", "eje a 45°")]
    for i, (cod, desc) in enumerate(canos):
        x = i * 90
        cx = x + 45
        if i == 0:
            b += [cil_h(cx), EL(cx, 180, cx, cy - 16),
                  D(f"M{x + 22} {cy + 25} Q{cx} {cy + 37} {x + 68} {cy + 25}", "f-ac", AA)]
        elif i == 1:
            b += [R(cx - 15, cy - 36, 30, 72, "f-mt"), E(cx, cy - 36, 15, 5, "f-mt"),
                  D(f"M{cx - 15} {cy} A15 5 0 0 0 {cx + 15} {cy}", "f-ht"), EL(x + 86, cy - 6, cx + 17, cy + 3)]
        elif i == 2:
            b += [cil_h(cx), EL(cx, cy + 50, cx, cy + 16),
                  D(f"M{cx + 9} {cy + 11} Q{cx + 18} {cy} {cx + 9} {cy - 11}", "f-ac", AA)]
        else:
            b += [f'<g transform="rotate(-45 {cx} {cy})">{cil_h(cx)}</g>',
                  L(x + 4, cy, x + 86, cy, "f-dash"),
                  arco(cx, cy, 27, 90, 45, "f-ac", sweep=0), T(cx + 18, cy + 17, "45°", "f-ach")]
        b += [T(cx, 290, cod, "f-tx", "middle"), T(cx, 304, desc, "f-sm", "middle")]
    return "posiciones", "Posiciones de soldadura en placa y en caño", 360, 316, b


def fig_angulos():
    b = [T(85, 22, "ÁNGULO DE TRABAJO", "f-ach", "middle"), T(275, 22, "ÁNGULO DE AVANCE", "f-ach", "middle")]
    b.append(junta(85, 120, 40, 6, 4, 34 * TAN, 12, 158))
    b += [EL(85, 40, 85, 117), L(85, 124, 85, 160, "f-dash")]
    b += [T(85, 180, "90° en la ranura", "f-tx", "middle"), T(85, 196, "45° en filete (bisectriz)", "f-sm", "middle")]
    b += [R(196, 150, 150, 18, "f-mt"), D("M200 150 Q234 136 268 150 Z", "f-wd")]
    s15, c15 = math.sin(math.radians(15)), math.cos(math.radians(15))
    b += [L(272, 148, 272, 68, "f-dash"), EL(272 + 80 * s15, 148 - 80 * c15, 272, 148),
          D(f"M272 108 A40 40 0 0 1 {n(272 + 40 * s15)} {n(148 - 40 * c15)}", "f-ac"),
          T(298, 104, "10–20°", "f-ach"), L(200, 178, 250, 178, "f-ac", AA), T(256, 182, "avance", "f-sm")]
    b += [T(196, 202, "Arrastre: el electrodo apunta", "f-sm"), T(196, 216, "hacia el cordón ya hecho", "f-sm")]
    return "angulos", "Ángulo de trabajo y ángulo de avance", 360, 226, b


def fig_tipos_junta():
    b = []
    nombres = ["A tope", "En T", "Esquina", "Solapada", "De borde"]
    for i, nombre in enumerate(nombres):
        x = i * 72
        if i == 0:
            b += [R(x + 8, 50, 27, 12, "f-mt"), R(x + 37, 50, 27, 12, "f-mt"), E(x + 36, 49, 6, 3, "f-htf")]
        elif i == 1:
            b += [R(x + 6, 64, 60, 12, "f-mt"), R(x + 30, 22, 12, 42, "f-mt"),
                  P([(x + 30, 64), (x + 23, 64), (x + 30, 57)], "f-htf"), P([(x + 42, 64), (x + 49, 64), (x + 42, 57)], "f-htf")]
        elif i == 2:
            b += [R(x + 14, 22, 12, 54, "f-mt"), R(x + 26, 64, 40, 12, "f-mt"), P([(x + 26, 64), (x + 33, 64), (x + 26, 57)], "f-htf")]
        elif i == 3:
            b += [R(x + 6, 52, 44, 12, "f-mt"), R(x + 22, 64, 44, 12, "f-mt"), P([(x + 50, 64), (x + 58, 64), (x + 50, 56)], "f-htf")]
        else:
            b += [R(x + 12, 44, 52, 12, "f-mt"), R(x + 12, 56, 52, 12, "f-mt"), E(x + 12, 56, 4, 9, "f-htf")]
        b.append(T(x + 36, 102, nombre, "f-tx", "middle"))
    return "tipos-junta", "Los cinco tipos de junta", 360, 116, b


def fig_junta():
    cx, ytop, t, land, hg = 180, 62, 110, 16, 13
    run = (t - land) * TAN
    vb = ytop + t - land
    b = [junta(cx, ytop, t, land, hg, run, 14, 346)]
    a = math.radians(37.5)
    b += [L(cx - hg, vb, cx - hg, 84, "f-dash"),
          D(f"M{cx - hg} {vb - 52} A52 52 0 0 0 {n(cx - hg - 52 * math.sin(a))} {n(vb - 52 * math.cos(a))}", "f-ac"),
          T(150, 100, "37,5°", "f-ach", "middle"), T(cx, 44, "ángulo de ranura 75°", "f-tx", "middle")]
    b += [L(28, ytop, 28, ytop + t), L(22, ytop, 34, ytop), L(22, ytop + t, 34, ytop + t), T(36, 121, "t (pared)")]
    b += [L(cx - hg, 186, cx + hg, 186, "f-ac"), L(cx - hg, 180, cx - hg, 192, "f-ac"), L(cx + hg, 180, cx + hg, 192, "f-ac"),
          T(cx, 205, "luz 2,4–3,2 mm", "f-tx", "middle")]
    b += [L(cx + hg + 2, 164, 262, 194, "f-dash"), T(266, 199, "talón 1,6 mm")]
    b += [L(cx + hg + run / 2 + 2, ytop + (t - land) / 2, 300, 52, "f-dash"), T(346, 48, "cara del bisel", "f-tx", "end")]
    b += [T(16, 54, "superficie exterior", "f-sm"), T(16, 190, "superficie interior", "f-sm")]
    b.append(T(cx, 226, "Proporciones aprox. de un caño 6\" Sch 80 (pared 11 mm)", "f-sm", "middle"))
    return "junta", "Partes de la junta en V preparada", 360, 236, b


def fig_pasadas():
    cx, ytop, t, land, hg = 180, 62, 110, 16, 13
    run = (t - land) * TAN
    vb = ytop + t - land

    def xl(y):
        return cx - hg - run * (vb - y) / (t - land) if y < vb else cx - hg

    def xr(y):
        return 2 * cx - xl(y)

    b = [junta(cx, ytop, t, land, hg, run, 14, 346)]
    capas = [(148, 151), (130, 127), (104, 100), (75, 72)]
    raiz = (f"M{cx - hg} {ytop + t} Q{cx} {ytop + t + 12} {cx + hg} {ytop + t} L{cx + hg} {vb} "
            f"L{n(xr(148))} 148 Q{cx} 151 {n(xl(148))} 148 L{cx - hg} {vb} Z")
    b.append(D(raiz, "f-wd3"))
    clases = ["f-wd2", "f-wd", "f-wd2"]
    for (y0, c0), (y1, c1), cls in zip(capas, capas[1:], clases):
        b.append(D(f"M{n(xl(y0))} {y0} Q{cx} {c0} {n(xr(y0))} {y0} L{n(xr(y1))} {y1} Q{cx} {c1} {n(xl(y1))} {y1} Z", cls))
    borde = cx - hg - run
    cap = (f"M{n(xl(75))} 75 L{n(borde)} {ytop} L{n(borde - 15)} {ytop} C{n(borde + 15)} 47 {n(2 * cx - borde - 15)} 47 "
           f"{n(2 * cx - borde + 15)} {ytop} L{n(2 * cx - borde)} {ytop} L{n(xr(75))} 75 Q{cx} 72 {n(xl(75))} 75 Z")
    b.append(D(cap, "f-wd"))
    for y, num in ((166, "1"), (143, "2"), (121, "3"), (93, "4"), (66, "5")):
        b.append(T(cx, y, num, "f-tx", "middle"))
    b += [T(cx, 40, "sobremonta ≤ 3 mm", "f-sm", "middle"), T(86, 50, "+1,5 mm", "f-sm", "middle"),
          L(281, 61, 300, 48, "f-dash"), T(346, 44, "pie del cordón", "f-sm", "end"),
          L(263, 69, 298, 86, "f-dash"), T(352, 96, "1–1,5 mm", "f-sm", "end"),
          T(cx, 200, "penetración de raíz ≤ 3 mm", "f-sm", "middle")]
    b += [T(cx, 222, "1 Raíz (E6010) · 2 Pase caliente", "f-tx", "middle"),
          T(cx, 238, "3 y 4 Rellenos (E7018) · 5 Presentación (E7018)", "f-tx", "middle")]
    return "pasadas", "Secuencia de pasadas en un caño 6\" Sch 80", 360, 250, b


def fig_simbolo():
    b = [L(90, 110, 300, 110), L(90, 110, 42, 164, "f-ln", AK), L(300, 110, 318, 94), L(300, 110, 318, 126),
         C(90, 110, 8, "f-ln"), L(90, 102, 90, 70), P([(90, 70), (110, 77), (90, 84)], "f-inkf")]
    b += [T(230, 76, "símbolo ARRIBA de la línea", "f-sm", "middle"), T(230, 99, "OTRO LADO", "f-ach", "middle"),
          T(230, 131, "LADO FLECHA", "f-hth", "middle"), T(230, 147, "símbolo ABAJO de la línea", "f-sm", "middle")]
    b += [T(84, 80, "en obra", "f-sm", "end"), T(102, 96, "todo alrededor", "f-sm"),
          T(50, 178, "flecha: toca la junta", "f-sm"), T(330, 168, "cola: proceso, WPS", "f-sm", "end")]
    b += [T(180, 200, "La línea horizontal es la línea de referencia.", "f-tx", "middle"),
          T(180, 216, "La regla vale para donde sea que apunte la flecha.", "f-sm", "middle")]
    return "simbolo", "Cómo se lee el símbolo de soldadura AWS", 360, 228, b


def fig_simbolo_ejemplos():
    b = []
    casos = [("Filete de 6 mm", "lado de la flecha"), ("Filete", "del otro lado"),
             ("Filete intermitente", "tramos de 50 cada 150 mm"), ("V con luz 3 mm y 75°", "+ penetración visible (caño)"),
             ("Doble V", "(ambos lados)"), ("Bisel en obra (bandera)", "flecha quebrada: pieza biselada")]
    for k, (tit, sub) in enumerate(casos):
        x, y = (k % 2) * 180, 10 + (k // 2) * 115
        yl, sx = y + 38, x + 100
        b.append(L(x + 40, yl, x + 160, yl))
        if k == 5:
            b += [D(f"M{x + 40} {yl} L{x + 26} {yl + 14} L{x + 26} {yl + 36}", "f-ln", AK),
                  L(x + 40, yl, x + 40, yl - 22), P([(x + 40, yl - 22), (x + 54, yl - 17), (x + 40, yl - 12)], "f-inkf"),
                  L(sx - 4, yl, sx - 4, yl + 18), L(sx - 4, yl, sx + 9, yl + 18)]
        else:
            b.append(L(x + 40, yl, x + 16, yl + 26, "f-ln", AK))
        if k in (0, 2):
            b += [P([(sx - 6, yl), (sx - 6, yl + 16), (sx + 10, yl)], "f-ln"), T(sx - 12, yl + 14, "6", "f-tx", "end")]
            if k == 2:
                b.append(T(sx + 15, yl + 14, "50-150", "f-tx"))
        elif k == 1:
            b.append(P([(sx - 6, yl), (sx - 6, yl - 16), (sx + 10, yl)], "f-ln"))
        elif k == 3:
            b += [D(f"M{sx - 10} {yl + 20} L{sx} {yl} L{sx + 10} {yl + 20}", "f-ln"),
                  T(sx, yl + 18, "3", "f-sm", "middle"), T(sx, yl + 34, "75°", "f-tx", "middle"),
                  D(f"M{sx - 7} {yl} A7 7 0 0 1 {sx + 7} {yl} Z", "f-inkf")]
        elif k == 4:
            b += [D(f"M{sx - 9} {yl + 17} L{sx} {yl} L{sx + 9} {yl + 17}", "f-ln"),
                  D(f"M{sx - 9} {yl - 17} L{sx} {yl} L{sx + 9} {yl - 17}", "f-ln")]
        b += [T(x + 90, y + 88, tit, "f-tx", "middle"), T(x + 90, y + 103, sub, "f-sm", "middle")]
    return "simbolo-ejemplos", "Ejemplos de símbolos de soldadura", 360, 355, b


def fig_respaldo():
    cx, ytop, t, hg = 180, 50, 60, 18
    run = t * math.tan(math.radians(22.5))
    izq = [(14, ytop), (cx - hg - run, ytop), (cx - hg, ytop + t), (14, ytop + t)]
    der = [(346, ytop), (cx + hg + run, ytop), (cx + hg, ytop + t), (346, ytop + t)]
    b = [P(izq, "f-mt"), P(der, "f-mt"), R(105, ytop + t, 150, 60, "f-mt")]
    b += [T(cx, 36, "ranura de 45° (22,5° por lado)", "f-tx", "middle"), T(60, 84, "chapa 10 mm", "f-tx", "middle"),
          L(cx - hg, 102, cx + hg, 102, "f-ac"), L(cx + hg + 2, 100, 258, 82, "f-dash"),
          T(346, 80, "luz 6 mm (1/4\")", "f-tx", "end"), T(14, 128, "bisel a filo", "f-sm"),
          T(cx, 146, "respaldo 10 × 25 mm", "f-tx", "middle"),
          T(cx, 198, "El respaldo va bien pegado: sin luz entre chapa y respaldo", "f-sm", "middle")]
    return "respaldo", "Cupón de placa con respaldo (tipo AWS D1.1)", 360, 212, b


def fig_punteado():
    cx, cy = 92, 112
    b = [C(cx, cy, 72, "f-mt"), C(cx, cy, 56, "f-hole")]
    for h in (10, 2, 4, 8):
        th = h * 30
        b.append(arco(cx, cy, 64, th - 12, th + 12, "f-tack"))
        x, y = PC(cx, cy, 87, th)
        b.append(T(x, y + 4, str(h), "f-tx", "middle"))
    for th, lab in ((0, "12 · no"), (180, "6 · no")):
        x, y = PC(cx, cy, 64, th)
        b += [L(x - 5, y - 5, x + 5, y + 5, "f-ht"), L(x - 5, y + 5, x + 5, y - 5, "f-ht")]
        x2, y2 = PC(cx, cy, 86, th)
        b.append(T(x2, y2 + 4, lab, "f-sm", "middle"))
    b += [T(cx, 222, "Puntos a las 10, 2, 4 y 8", "f-tx", "middle"), T(cx, 237, "(no en las 6 ni en las 12)", "f-sm", "middle")]
    jx, run = 276, 56 * TAN
    b.append(junta(jx, 60, 70, 14, 12, run, 196, 356))
    b += [C(jx, 123, 11, "f-inkf"), T(jx, 152, "el alma del electrodo", "f-tx", "middle"),
          T(jx, 167, "sirve de galga de luz", "f-sm", "middle"), T(jx, 192, "último punto: +0,3 a 0,5 mm", "f-tx", "middle"),
          T(jx, 207, "(la contracción cierra la luz)", "f-sm", "middle")]
    return "punteado", "Puntos de armado y luz con galga", 360, 248, b


def fig_movimientos():
    filas = [("Recto (cordón recto)", "Presentación en 2G, sobrecabeza, raíz con respaldo"),
             ("Zigzag (tejido)", "Relleno y presentación: pausa en los costados"),
             ("Media luna", "Vertical ascendente (3G): el centro no cuelga"),
             ("Triángulo", "Filete vertical (3F) en una pasada"),
             ("Latigueo", "Raíz con 6010: avanza, vuelve al charco y pausa")]
    b = []
    for i, (tit, sub) in enumerate(filas):
        y = 36 + i * 52
        b += [T(12, y + 4, tit), T(12, y + 24, sub, "f-sm")]
        puntos = []
        if i == 0:
            b.append(L(150, y, 336, y, "f-ac", AA))
            continue
        if i == 1:
            pts, x, k = [(150, y)], 150, 0
            while x < 316:
                x += 14
                k += 1
                pts.append((x, y - 8 if k % 2 else y + 8))
                puntos.append(pts[-1])
            d = "M" + " L".join(f"{n(a)} {n(c)}" for a, c in pts)
        elif i == 2:
            d, x = f"M150 {y}", 150
            while x < 314:
                d += f" Q{x + 11} {y - 16} {x + 22} {y}"
                x += 22
                puntos.append((x, y))
        elif i == 3:
            d, x = f"M150 {y}", 150
            while x < 318:
                d += f" L{x + 9} {y - 9} L{x + 9} {y + 9} L{x + 18} {y}"
                puntos += [(x + 9, y - 9), (x + 9, y + 9)]
                x += 18
        else:
            d, x = f"M150 {y}", 150
            while x < 306:
                d += f" L{x + 24} {y} Q{x + 18} {y - 14} {x + 12} {y}"
                x += 12
                puntos.append((x, y))
        b.append(D(d, "f-ac", AA))
        b += [C(a, c, 2.6, "f-htf") for a, c in puntos]
    b += [C(16, 278, 2.8, "f-htf"), T(24, 282, "pausa breve", "f-sm"), L(110, 278, 140, 278, "f-ac", AA), T(146, 282, "sentido de avance", "f-sm")]
    return "movimientos", "Movimientos del electrodo", 360, 292, b


def fig_keyhole():
    b = [R(10, 40, 340, 56, "f-mt"), R(10, 144, 340, 56, "f-mt"),
         D("M10 90 L196 90 Q212 120 196 150 L10 150 Z", "f-wd")]
    b += [D(f"M{x} 92 Q{x + 10} 120 {x} 148", "f-rip") for x in range(36, 196, 22)]
    b += [E(220, 120, 30, 32, "f-wd2"), E(252, 120, 10, 28, "f-hole"),
          L(290, 120, 340, 120, "f-ac", AA), T(315, 112, "avance", "f-sm", "middle")]
    b += [L(252, 93, 300, 34, "f-dash"), T(350, 28, "ojo de cerradura", "f-tx", "end"),
          L(212, 92, 176, 34, "f-dash"), T(180, 28, "charco (líquido)", "f-tx", "end"),
          T(100, 124, "cordón de raíz", "f-tx", "middle"), T(340, 90, "talón", "f-sm", "end"), T(340, 162, "talón", "f-sm", "end")]
    estados = [("Bien", "1–1,5 × Ø, funde los dos", 7, 14), ("Muy grande", "se va a perforar", 14, 20), ("Cerrado", "no penetra", 3, 5)]
    for i, (tit, sub, rx, ry) in enumerate(estados):
        x = i * 120
        b += [R(x + 15, 222, 90, 12, "f-mt"), R(x + 15, 258, 90, 12, "f-mt"), E(x + 60, 246, rx, ry, "f-hole"),
              T(x + 60, 288, tit, "f-tx", "middle"), T(x + 60, 302, sub, "f-sm", "middle")]
    return "keyhole", "El ojo de cerradura en la raíz (vista desde afuera)", 360, 312, b


def fig_reloj():
    cx, cy = 180, 170
    b = [C(cx, cy, 96, "f-mt"), C(cx, cy, 80, "f-hole")]
    b += [arco(cx, cy, 107, 315, 405, "f-zp"), arco(cx, cy, 107, 45, 135, "f-zv"),
          arco(cx, cy, 107, 135, 225, "f-zs"), arco(cx, cy, 107, 225, 315, "f-zv")]
    for h in range(12):
        x1, y1 = PC(cx, cy, 96, h * 30)
        x2, y2 = PC(cx, cy, 88, h * 30)
        b.append(L(x1, y1, x2, y2))
    for h, lab in ((0, "12"), (90, "3"), (180, "6"), (270, "9")):
        x, y = PC(cx, cy, 124, h)
        b.append(T(x, y + 5, lab, "f-tx", "middle"))
    b += [T(cx, 24, "PLANO", "f-ach", "middle"), T(cx, 334, "SOBRECABEZA", "f-hth", "middle"),
          T(10, 150, "VERTICAL", "f-sm"), T(350, 150, "VERTICAL", "f-sm", "end")]
    x1, y1 = PC(cx, cy, 66, 195)
    x2, y2 = PC(cx, cy, 66, 345)
    b.append(D(f"M{n(x1)} {n(y1)} A66 66 0 1 0 {n(x2)} {n(y2)}", "f-ac", AA))
    x1, y1 = PC(cx, cy, 50, 195)
    x2, y2 = PC(cx, cy, 50, 356)
    b.append(D(f"M{n(x1)} {n(y1)} A50 50 0 0 1 {n(x2)} {n(y2)}", "f-ht", AH))
    x, y = PC(cx, cy, 40, 100)
    b.append(T(x, y + 4, "1", "f-ach", "middle"))
    x, y = PC(cx, cy, 34, 262)
    b.append(T(x, y + 4, "2", "f-hth", "middle"))
    x, y = PC(cx, cy, 58, 195)
    b.append(C(x, y, 4, "f-inkf"))
    x, y = PC(cx, cy, 140, 200)
    b.append(T(x, y + 4, "inicio ~6:30", "f-sm", "end"))
    x, y = PC(cx, cy, 136, 332)
    b.append(T(x, y, "fin de 1: ~11:30", "f-sm", "end"))
    b += [T(cx, 356, "1: arranca ~6:30, sube por un lado y termina ~11:30.", "f-sm", "middle"),
          T(cx, 371, "2: arranca sobre el inicio amolado y cierra arriba.", "f-sm", "middle")]
    return "reloj", "El caño como un reloj: zonas y mitades (5G/6G ascendente)", 360, 382, b


def fig_electrodo_zonas():
    b = [L(120, 12, 120, 226, "f-dash"), L(240, 12, 240, 226, "f-dash")]
    b += [T(60, 24, "ABAJO 6 → 5", "f-ach", "middle"), T(60, 39, "sobrecabeza", "f-sm", "middle"),
          R(10, 52, 100, 26, "f-mt"), P([(53, 78), (60, 70), (67, 78)], "f-hole"), EL(60, 162, 60, 81),
          L(72, 94, 104, 94, "f-ac", AA), T(88, 110, "avance", "f-sm", "middle"),
          T(60, 190, "Radial, empujado", "f-tx", "middle"), T(60, 205, "dentro de la junta,", "f-sm", "middle"),
          T(60, 219, "casi sin latigueo", "f-sm", "middle")]
    s10, c10 = math.sin(math.radians(10)), math.cos(math.radians(10))
    b += [T(180, 24, "LADOS 5 → 1", "f-ach", "middle"), T(180, 39, "vertical", "f-sm", "middle"),
          R(126, 50, 26, 124, "f-mt"), P([(152, 103), (144, 110), (152, 117)], "f-hole"),
          L(156, 110, 228, 110, "f-dash"), EL(156 + 70 * c10, 110 + 70 * s10, 156, 110),
          D(f"M200 110 A44 44 0 0 1 {n(156 + 44 * c10)} {n(110 + 44 * s10)}", "f-ac"),
          T(206, 140, "5–15°", "f-ach", "middle"), L(166, 166, 166, 132, "f-ac", AA), T(172, 170, "avance", "f-sm"),
          T(180, 190, "5–15° hacia arriba", "f-tx", "middle"), T(180, 205, "(empuje),", "f-sm", "middle"),
          T(180, 219, "latigueo corto", "f-sm", "middle")]
    s15, c15 = math.sin(math.radians(15)), math.cos(math.radians(15))
    b += [T(300, 24, "ARRIBA 1 → 12", "f-ach", "middle"), T(300, 39, "plano", "f-sm", "middle"),
          R(250, 112, 100, 26, "f-mt"), P([(293, 112), (300, 120), (307, 112)], "f-hole"),
          L(300, 110, 300, 46, "f-dash"), EL(300 - 70 * s15, 110 - 70 * c15, 300, 110),
          D(f"M300 70 A40 40 0 0 0 {n(300 - 40 * s15)} {n(110 - 40 * c15)}", "f-ac"), T(306, 72, "10–20°", "f-ach"),
          L(336, 154, 272, 154, "f-ac", AA), T(304, 170, "avance", "f-sm", "middle"),
          T(300, 190, "Arrastre 10–20°", "f-tx", "middle"), T(300, 205, "más latigueo", "f-sm", "middle"),
          T(300, 219, "y más velocidad", "f-sm", "middle")]
    return "electrodo-zonas", "Ángulo del electrodo en la raíz ascendente, por zona", 360, 232, b


def mini_defecto(ox, oy, tipo):
    cx, ytop, t, land, hg = ox + 90, oy + 28, 46, 8, 5
    run = (t - land) * TAN
    vb = ytop + t - land
    eL, eR = cx - hg - run, cx + hg + run

    def xl(y):
        return cx - hg - run * (vb - y) / (t - land)

    raiz_c = {"concavidad": ytop + t - 7, "exceso": ytop + t + 20}.get(tipo, ytop + t + 7)
    toeR = eR + (1 if tipo == "socavacion" else 5)
    if tipo == "penetracion":
        cuerpo = (f"M{n(eL - 5)} {ytop} Q{cx} {ytop - 11} {n(eR + 5)} {ytop} L{n(eR)} {ytop} "
                  f"L{cx + hg} {vb - 1} Q{cx} {vb + 3} {cx - hg} {vb - 1} L{n(eL)} {ytop} Z")
    else:
        cuerpo = (f"M{n(eL - 5)} {ytop} Q{cx} {ytop - 11} {n(toeR)} {ytop} L{n(eR)} {ytop} L{cx + hg} {vb} "
                  f"L{cx + hg} {ytop + t} Q{cx} {n(raiz_c)} {cx - hg} {ytop + t} L{cx - hg} {vb} L{n(eL)} {ytop} Z")
    b = [junta(cx, ytop, t, land, hg, run, ox + 10, ox + 170), D(cuerpo, "f-wd")]
    if tipo == "socavacion":
        b.append(D(f"M{n(eR + 1)} {ytop} Q{n(eR + 6)} {ytop + 8} {n(eR + 11)} {ytop} Z", "f-holeh"))
    elif tipo == "fusion":
        b.append(L(eL + 3, ytop + 4, cx - hg + 1, vb - 3, "f-defl"))
    elif tipo == "penetracion":
        b.append(R(cx - hg, vb, 2 * hg, land, "f-defbox"))
    elif tipo in ("concavidad", "exceso"):
        b.append(D(f"M{cx + hg} {ytop + t} Q{cx} {n(raiz_c)} {cx - hg} {ytop + t}", "f-defl"))
    elif tipo == "porosidad":
        b += [C(cx - 6, ytop + 12, 2.6, "f-pore"), C(cx + 6, ytop + 20, 2.1, "f-pore"),
              C(cx - 2, ytop + 29, 2.6, "f-pore"), C(cx + 9, ytop + 7, 1.9, "f-pore"), C(cx - 10, ytop + 3, 1.8, "f-pore")]
    elif tipo == "escoria":
        yy = vb - 8
        b += [E(xl(yy) + 4, yy, 5, 1.9, "f-htf", f'transform="rotate(52.5 {n(xl(yy) + 4)} {n(yy)})"'),
              E(2 * cx - xl(yy) - 4, yy, 5, 1.9, "f-htf", f'transform="rotate(-52.5 {n(2 * cx - xl(yy) - 4)} {n(yy)})"')]
    elif tipo == "solape":
        b += [D(f"M{n(toeR - 4)} {ytop - 4} Q{n(toeR + 10)} {ytop - 10} {n(toeR + 17)} {ytop} L{n(toeR - 4)} {ytop} Z", "f-wd"),
              L(toeR, ytop, toeR + 16, ytop, "f-defl")]
    return b


def fig_defectos():
    casos = [("socavacion", "Socavación", "canaleta en el pie"), ("fusion", "Falta de fusión", "no se fundió con la pared"),
             ("penetracion", "Falta de penetración", "la raíz no atravesó"), ("concavidad", "Concavidad de raíz", "raíz hundida por dentro"),
             ("exceso", "Exceso de penetración", "raíz que cuelga"), ("porosidad", "Porosidad", "poros de gas"),
             ("escoria", "Inclusión de escoria", "\"vías\" sin limpiar"), ("solape", "Solape", "metal frío sin fundir")]
    b = []
    for k, (tipo, tit, sub) in enumerate(casos):
        ox, oy = (k % 2) * 180, 8 + (k // 2) * 130
        b += mini_defecto(ox, oy, tipo)
        b += [T(ox + 90, oy + 106, tit, "f-tx", "middle"), T(ox + 90, oy + 121, sub, "f-sm", "middle")]
    return "defectos", "Defectos más comunes en corte transversal (el defecto, en naranja)", 360, 530, b


def fig_probetas():
    cx, cy = 105, 112
    b = [C(cx, cy, 76, "f-mt"), C(cx, cy, 60, "f-hole")]
    for th in (0, 90, 180, 270):
        a = math.radians(th)
        ux, uy = math.sin(a), -math.cos(a)
        px, py = -uy, ux
        p1 = (cx + ux * 54, cy + uy * 54)
        p2 = (cx + ux * 82, cy + uy * 82)
        b.append(P([(p1[0] + px * 7, p1[1] + py * 7), (p2[0] + px * 7, p2[1] + py * 7),
                    (p2[0] - px * 7, p2[1] - py * 7), (p1[0] - px * 7, p1[1] - py * 7)], "f-wd2"))
    b += [T(cx, 20, "12 · cierre", "f-sm", "middle"), T(cx, 214, "6 · inicio", "f-sm", "middle"),
          T(194, 116, "3", "f-tx", "middle"), T(16, 116, "9", "f-tx", "middle")]
    lineas = [("AUTOEVALUACIÓN", "f-ach", 56), ("Cortá en los empalmes", "f-tx", 78), ("(6 y 12) y en los", "f-tx", 94),
              ("verticales (3 y 9).", "f-tx", 110), ("En el examen las ubica", "f-sm", 138), ("el inspector según", "f-sm", 153),
              ("el código.", "f-sm", 168), ("Marcá la hora con tiza", "f-sm", 192), ("antes de cortar.", "f-sm", 207)]
    b += [T(210, y, s, cls) for s, cls, y in lineas]
    return "probetas", "Dónde cortar las probetas de autoevaluación", 360, 224, b


def fig_doblado():
    b = [D("M80 30 L120 30 L120 104 A20 20 0 0 1 80 104 Z", "f-mt"),
         D("M75 44 L75 104 A25 25 0 0 0 125 104 L125 44", "f-sp"),
         D(f"M{n(100 - 25 * math.sin(math.radians(20)))} {n(104 + 25 * math.cos(math.radians(20)))} "
           f"A25 25 0 0 0 {n(100 + 25 * math.sin(math.radians(20)))} {n(104 + 25 * math.cos(math.radians(20)))}", "f-spw"),
         C(58, 96, 12, "f-mt"), C(142, 96, 12, "f-mt")]
    b += [T(126, 22, "émbolo Ø 38 mm (4 × t)"), T(50, 126, "rodillo", "f-sm", "middle"),
          L(148, 77, 131, 70, "f-dash"), T(150, 80, "probeta", "f-sm"),
          L(70, 152, 130, 152, "f-ac"), L(70, 146, 70, 158, "f-ac"), L(130, 146, 130, 158, "f-ac"),
          T(100, 170, "abertura ≈ 60 mm", "f-tx", "middle"), T(100, 188, "zona soldada (afuera = estirada)", "f-sm", "middle")]
    filas = [("Cara", "la presentación", "queda afuera"), ("Raíz", "la raíz", "queda afuera"), ("Lateral", "rebanada de 10 mm,", "se dobla de costado")]
    for i, (tit, l1, l2) in enumerate(filas):
        y = 70 + i * 62
        b += [D(f"M210 {y - 22} L210 {y} A12 12 0 0 0 234 {y} L234 {y - 22}", "f-spm"),
              D(f"M206.5 {y} A15.5 15.5 0 0 0 237.5 {y}", "f-ht"),
              T(248, y - 10, tit), T(248, y + 5, l1, "f-sm"), T(248, y + 19, l2, "f-sm")]
    b += [T(180, 258, "La probeta puede saltar: poné una pantalla", "f-sm", "middle"),
          T(180, 273, "delante y no te pares en su línea.", "f-sm", "middle")]
    return "doblado", "Ensayo de doblado guiado y tipos de probeta", 360, 286, b


def fig_nickbreak():
    b = [R(30, 46, 300, 40, "f-mt"), R(170, 46, 20, 40, "f-wd"),
         P([(173, 46), (180, 56), (187, 46)], "f-holeh"), P([(173, 86), (180, 76), (187, 86)], "f-holeh"),
         T(180, 34, "ranura ≈ 3 mm en ambos costados", "f-tx", "middle"),
         T(30, 102, "cordón al centro", "f-sm"), T(330, 102, "tira de ≈ 25 mm de ancho", "f-sm", "end")]
    b += [P([(30, 140), (170, 140), (166, 147), (172, 153), (167, 160), (171, 170), (30, 170)], "f-mt"),
          P([(191, 140), (187, 147), (193, 153), (188, 160), (192, 170), (330, 170), (330, 140)], "f-mt"),
          L(150, 186, 110, 186, "f-ac", AA), L(210, 186, 250, 186, "f-ac", AA),
          T(180, 202, "romper con maza o prensa", "f-sm", "middle")]
    b += [R(130, 214, 100, 30, "f-wd"), C(152, 226, 2.6, "f-pore"), C(206, 233, 2.1, "f-pore"),
          T(124, 227, "cara de", "f-sm", "end"), T(124, 241, "fractura", "f-sm", "end"),
          T(236, 227, "pareja = bien", "f-sm"), T(236, 241, "poros = mal", "f-sm")]
    return "nickbreak", "Ensayo de rotura con entalla (nick-break)", 360, 256, b


FIGURAS = [fig_posiciones, fig_angulos, fig_tipos_junta, fig_junta, fig_pasadas, fig_simbolo, fig_simbolo_ejemplos,
           fig_respaldo, fig_punteado, fig_movimientos, fig_keyhole, fig_reloj, fig_electrodo_zonas, fig_defectos,
           fig_probetas, fig_doblado, fig_nickbreak]


def main():
    DEST.mkdir(exist_ok=True)
    for f in FIGURAS:
        nombre, titulo, w, h, cuerpo = f()
        (DEST / f"{nombre}.svg").write_text(svg(titulo, w, h, cuerpo), encoding="utf-8")
        print(f"figuras/{nombre}.svg")


if __name__ == "__main__":
    main()
