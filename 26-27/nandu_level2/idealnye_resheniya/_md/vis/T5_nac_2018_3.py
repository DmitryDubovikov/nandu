import json, sys, math
# Рисунки к Т5 национал 2018 день I №3: кузнечик на круге из 1000 клеток, шаг 35.
# Круг: клетка 1 сверху, номера растут по часовой стрелке (одна ось во всех рисунках).
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
TEAL,PINK='#4fd1c5','#f78fb3'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
CX,CY,R=50,50,36

def pt(n, r=R):
    a = math.radians((n-1)/1000*360)
    return CX + r*math.sin(a), CY - r*math.cos(a)
def dot(n, col, rad=1.1):
    x, y = pt(n); return f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{rad}' fill='{col}'/>"
def lab(n, s, col, r, size=3.6):
    x, y = pt(n, r)
    return f"<text x='{x:.2f}' y='{y+size*0.35:.2f}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def ring():
    return f"<circle cx='{CX}' cy='{CY}' r='{R}' fill='none' stroke='{DIM}' stroke-width='0.6'/>"
def svg(inner, aria, vb='0 0 100 100', mw=380):
    return f"<svg viewBox='{vb}' role='img' aria-label='{aria}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

V = {}

# 1. схема первого круга и начала второго — не в масштабе, как рисуют от руки:
# пять золотых клеток первого круга, многоточие внизу, прыжки — дуги; синие 16 и 51 встают между 1, 36 и 71
def apt(ang, r=R):
    a = math.radians(ang); return CX + r*math.sin(a), CY - r*math.cos(a)
def adot(ang, col, rad=1.5):
    x, y = apt(ang); return f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{rad}' fill='{col}'/>"
def alab(ang, t, col, r, size=4.2):
    x, y = apt(ang, r)
    return f"<text x='{x:.2f}' y='{y+size*0.35:.2f}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='700'>{t}</text>"
def jump(a1, a2, col, mid):
    # mid > 0 — дуга снаружи круга, mid < 0 — внутри
    e = 1.8 if mid > 0 else -1.8
    (x1, y1), (x2, y2) = apt(a1, R+e), apt(a2, R+e)
    cx, cy = apt((a1+a2)/2, R+mid)
    return (f"<path d='M{x1:.2f} {y1:.2f} Q {cx:.2f} {cy:.2f} {x2:.2f} {y2:.2f}' fill='none' stroke='{col}' "
            f"stroke-width='0.6' marker-end='url(#j{col[1:]})'/>")
def mk(col):
    return (f"<marker id='j{col[1:]}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='3.5' markerHeight='3.5' orient='auto'>"
            f"<path d='M0 0L6 3L0 6z' fill='{col}'/></marker>")
G = {1: 0, 36: 44, 71: 88, 946: -88, 981: -44}     # углы золотых клеток на схеме
Bl = {16: 22, 51: 66}                              # синие — между ними
s = f"<defs>{mk(GOLD)}{mk(BLUE)}</defs>"
# верх круга сплошной, низ — пунктир с многоточием: там пропущенные прыжки первого круга
x1, y1 = apt(100); x2, y2 = apt(-100)
s += f"<path d='M{x1:.2f} {y1:.2f} A {R} {R} 0 1 0 {x2:.2f} {y2:.2f}' fill='none' stroke='{DIM}' stroke-width='0.7'/>"
s += f"<path d='M{x1:.2f} {y1:.2f} A {R} {R} 0 0 1 {x2:.2f} {y2:.2f}' fill='none' stroke='{DIM}' stroke-width='0.7' stroke-dasharray='1.5 1.5'/>"
s += f"<text x='{CX}' y='{CY+R-4}' fill='{MUT}' font-size='6' text-anchor='middle' font-weight='700'>…</text>"
# граница 1000 | 1
s += alab(-12, 1000, MUT, R+6, 3.2)
x, y = apt(-5.5, R-2.5); X, Y = apt(-5.5, R+2.5)
s += f"<line x1='{x:.2f}' y1='{y:.2f}' x2='{X:.2f}' y2='{Y:.2f}' stroke='{MUT}' stroke-width='0.5'/>"
s += jump(0, 44, GOLD, 9) + jump(44, 88, GOLD, 9) + jump(-88, -44, GOLD, 9)
s += jump(-44, 22, BLUE, -16) + jump(22, 66, BLUE, -9)
for n, a_ in G.items(): s += adot(a_, GOLD) + alab(a_, n, GOLD, R+(13 if a_ in (0, -44, 44) else 10))
for n, a_ in Bl.items(): s += adot(a_, BLUE) + alab(a_, n, BLUE, R+7)
s += alab(-12, '+35', BLUE, R-14, 3.4)
V['после 981 кузнечик встаёт на 16'] = fig(svg(s, 'Первый круг', '0 -8 100 104', 440),
  "<b style='color:#f0a83c'>Первый круг</b> и <b style='color:#5ba8f5'>начало второго</b>.")

# 2. разложение: 35 · k ⋮ 1000
def chip(x, y, d, col, struck=False):
    r = f"<rect x='{x}' y='{y}' width='8' height='8' rx='1.5' fill='none' stroke='{col}' stroke-width='0.5'/>"
    r += f"<text x='{x+4}' y='{y+5.7}' fill='{col}' font-size='4.6' text-anchor='middle' font-weight='700'>{d}</text>"
    if struck: r += f"<line x1='{x+1}' y1='{y+7}' x2='{x+7}' y2='{y+1}' stroke='{RED}' stroke-width='0.7'/>"
    return r
s = f"<text x='2' y='9.6' fill='{LAB}' font-size='4.2' font-weight='700'>35 · k</text>"
s += f"<text x='2' y='29.6' fill='{LAB}' font-size='4.2' font-weight='700'>1000</text>"
s += chip(24, 4, '5', MUT, True) + chip(34, 4, '7', MUT)
s += f"<rect x='44' y='4' width='52' height='8' rx='1.5' fill='{GOLD}' fill-opacity='0.12' stroke='{GOLD}' stroke-width='0.6'/>"
s += f"<text x='70' y='9.8' fill='{GOLD}' font-size='4.6' text-anchor='middle' font-style='italic' font-weight='700'>k</text>"
s += chip(24, 24, '5', MUT, True)
for i, d in enumerate('22255'): s += chip(46+10*i, 24, d, GOLD)
s += f"<rect x='44.5' y='22.5' width='51' height='11' rx='2' fill='none' stroke='{GOLD}' stroke-width='0.5' stroke-dasharray='1.4 1'/>"
s += f"<line x1='70' y1='22' x2='70' y2='13.6' stroke='{GOLD}' stroke-width='0.6' marker-end='url(#upT5)'/>"
mk = f"<defs><marker id='upT5' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='{GOLD}'/></marker></defs>"
V['в 7 нет ни 2, ни 5'] = fig(svg(mk+s, 'Разложение на простые множители', '0 0 100 36', 420),
  'Простые множители 35 · k и 1000.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
