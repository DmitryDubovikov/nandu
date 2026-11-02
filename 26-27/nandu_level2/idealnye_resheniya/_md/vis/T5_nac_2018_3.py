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

# 1. первый круг (золото) и начало второго (синие)
s = ring()
lap1 = [1+35*k for k in range(29)]          # 1 … 981
lap2 = [16, 51, 86]
for n in lap1: s += dot(n, GOLD)
for n in lap2: s += dot(n, BLUE)
for n in (1, 36, 71, 106): s += lab(n, n, GOLD, R+6.5)
s += lab(970, 981, GOLD, R+6.5)   # подпись чуть левее точки 981, чтобы не слипалась с 1
for n in lap2: s += lab(n, n, BLUE, R-5.5, 3.3)
V['после 981 кузнечик встаёт на 16'] = fig(svg(s, 'Первый круг'),
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

# 3. все клетки на 1 и на 6: строка — сотня, в квадрате — номер круга, на котором кузнечик туда наступил
COL = [GOLD, BLUE, GREEN, RED, VIO, TEAL, PINK]
lap = {}
for k in range(200):
    lap.setdefault(1+(35*k) % 1000, (35*k)//1000 + 1)
Q, X0, Y0 = 5, 22, 7
s = ''
for j in range(20):
    s += f"<text x='{X0+j*Q+Q/2}' y='{Y0-1.6}' fill='{MUT}' font-size='2.3' text-anchor='middle'>{1+5*j}</text>"
for i in range(10):
    y = Y0 + i*Q
    s += f"<text x='{X0-1.5}' y='{y+Q/2+1}' fill='{MUT}' font-size='2.6' text-anchor='end'>{100*i+1}–{100*i+96}</text>"
    for j in range(20):
        n = 100*i + 1 + 5*j; L = lap[n]; c = COL[L-1]; x = X0 + j*Q
        s += f"<rect x='{x+0.3}' y='{y+0.3}' width='{Q-0.6}' height='{Q-0.6}' rx='0.8' fill='{c}' fill-opacity='0.25' stroke='{c}' stroke-width='0.3'/>"
        s += f"<text x='{x+Q/2}' y='{y+Q/2+1.1}' fill='{c}' font-size='3' text-anchor='middle' font-weight='700'>{L}</text>"
V['кузнечик побывал на каждой'] = fig(svg(s, 'Клетки на 1 и на 6', '0 0 124 58', 640),
  'Все клетки с номерами на 1 и на 6; в клетке — номер круга, на котором кузнечик на неё наступил.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
