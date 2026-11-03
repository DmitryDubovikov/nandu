import json, sys
# Рисунки к Т2″ провинциал 2019 №2. Координаты задачи — в кирпичах x (y вверх):
# A = (0, 0), B = (10, 0), O = (11, 0), C = (12, 0), D = (12, 8), E = (10, 8), R = (2, 8), F = (0, 8), P = (10, 4).
# SVG: X = U·x, Y = U·(8 − y).
U = 6
def xy(p): return round(U*p[0], 2), round(U*(8-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
TEAL,PINK,ORNG='#45c4b0','#f78fb3','#e07b39'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(10,0),'O':(11,0),'C':(12,0),'D':(12,8),'E':(10,8),'R':(2,8),'F':(0,8),'P':(10,4)}
OFF = {'A':(-3.0,3.4),'B':(-1.6,4.6),'O':(0,4.6),'C':(2.6,4.6),'D':(2.8,-1.4),'E':(-1.6,-1.6),
       'R':(0,-1.8),'F':(-3.0,-1.0),'P':(2.6,1.6)}
ALL = ['A','B','O','C','D','E','R','F','P']
SEG = [('A','B'),('B','O'),('O','C'),('C','D'),('D','E'),('E','R'),('R','F'),('F','A'),('B','P'),('P','E'),
       ('A','R'),('R','P'),('P','A'),('P','D'),('D','O'),('O','P')]

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=3.0):
    X, Y = xy(p); return txt(round(X+dx,2), round(Y+dy,2), s, col, size)
def labels(names, col=LAB):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col) + f"<circle cx='{X}' cy='{Y}' r='0.7' fill='{col}'/>"
    return out
def full(col=DIM, w=0.45): return ''.join(line(PT[a], PT[b], col, w) for a, b in SEG)
def names(): return labels(ALL, MUT)
def svg(inner, label, vb='-7 -7 86 63', mw=560):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def fill(pts, col, op=0.4): return poly([PT[n] for n in pts], col, 0.9, col, op)
def outline(pts, col, w=1.1): return poly([PT[n] for n in pts], col, w)

V = {}
# цвет треугольника — один во всех рисунках
TC = {'AFR': GOLD, 'APR': BLUE, 'REP': GREEN, 'ABP': TEAL, 'BOP': RED, 'ODP': VIO, 'PED': PINK, 'OCD': ORNG}
TP = {n: list(n) for n in TC}
def tri_(n, op=0.42): return fill(TP[n], TC[n], op)
def cname(n): return f"<b style='color:{TC[n]}'>{n}</b>"

# 1. рисунок условия: закрашены APR и ODP
s = (fill(['A','P','R'], BLUE, 0.45) + fill(['O','D','P'], BLUE, 0.45) + full(INK, 0.55) + labels(ALL))
V['закрашены треугольники APR и ODP'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. восемь треугольников
CEN = {'AFR': (0.9,6.0), 'APR': (4.0,4.0), 'REP': (7.4,6.2), 'ABP': (6.6,1.3),
       'BOP': (10.35,1.2), 'ODP': (11.0,3.6), 'PED': (10.6,6.8), 'OCD': (11.75,1.6)}
SMALL = {'BOP','ODP','PED','OCD','AFR'}
s = full(INK, 0.5) + ''.join(tri_(n) for n in TC)
s += ''.join(at(CEN[n], n, 0, 1.0, LAB, 1.9 if n in SMALL else 2.8) for n in TC if n in ('APR','REP','ABP'))
s += labels(ALL)
cap = 'ABEF: ' + ', '.join(cname(n) for n in ('AFR','APR','REP','ABP')) + '; BCDE: ' + ', '.join(cname(n) for n in ('BOP','ODP','PED','OCD')) + '.'
V['отрезки разрезают ABEF на четыре треугольника'] = fig(svg(s, 'Восемь треугольников'), cap)

# 3–5. каждое спрошенное
s = full() + outline(['B','C','D','E'], GOLD, 1.0) + tri_('ODP', 0.6) + ''.join(tri_(n, 0.18) for n in ('BOP','PED','OCD')) + names()
V['ODP — это BCDE без прямоугольных треугольников'] = fig(svg(s, 'а) ODP'),
  f"а) {cname('ODP')} = BCDE без {cname('BOP')}, {cname('PED')} и {cname('OCD')}")
s = full() + outline(['A','B','E','F'], GOLD, 1.0) + tri_('APR', 0.6) + ''.join(tri_(n, 0.18) for n in ('AFR','REP','ABP')) + names()
V['APR — это ABEF без прямоугольных треугольников'] = fig(svg(s, 'б) APR'),
  f"б) {cname('APR')} = ABEF без {cname('AFR')}, {cname('REP')} и {cname('ABP')}")
s = full() + outline(['A','C','D','F'], GOLD, 1.0) + line(PT['B'], PT['E'], GOLD, 1.0) + tri_('APR', 0.6) + tri_('ODP', 0.6) + names()
V['закрашенная часть состоит из APR и ODP'] = fig(svg(s, 'в) закрашенная часть'),
  f"в) закрашенная часть: {cname('APR')} и {cname('ODP')}; ACDF: ABEF и BCDE")

# 6. буквы на рисунке: длины в кирпичах, черта x на BO
def tick(p, vertical, col=GOLD):
    a, b = ((p[0], p[1]-0.3), (p[0], p[1]+0.3)) if vertical else ((p[0]-0.3, p[1]), (p[0]+0.3, p[1]))
    return line(a, b, col, 0.6)
s = full() + line(PT['B'], PT['O'], GOLD, 1.6) + at((10.5,0), 'x', 0, -1.4, GOLD, 3.0)
s += at((1,8), '2x', 0, -3.8, LAB, 2.6) + at((6,8), '8x', 0, -3.8, LAB, 2.6) + at((11,8), '2x', 0, -3.8, LAB, 2.6)
s += at((5,0), '10x', 0, 8.4, LAB, 2.6) + at((11.5,0), 'x', 0, 8.4, LAB, 2.6)
s += at((0,4), '8x', -4.6, 1.0, LAB, 2.6) + at((12,4), '8x', 4.8, 1.0, LAB, 2.6)
s += at((10,2), '4x', -2.6, 1.0, LAB, 2.4) + at((10,6), '4x', -2.6, 1.0, LAB, 2.4)
s += tick((10,2), False) + tick((10,6), False) + names()
V['BO = x — кирпич'] = fig(svg(s, 'Длины в кирпичах', '-9 -9 90 72'), 'Длины в кирпичах x.')

# 7. раздел 1: BCDE и три угла
def rangle(p, sx, sy, col=INK, r=0.5):
    a, b, c = (p[0]+sx*r, p[1]), (p[0]+sx*r, p[1]+sy*r), (p[0], p[1]+sy*r)
    return f"<polyline points='{'%s,%s' % xy(a)} {'%s,%s' % xy(b)} {'%s,%s' % xy(c)}' fill='none' stroke='{col}' stroke-width='0.4'/>"
s = full() + ''.join(tri_(n, 0.5) for n in ('BOP','PED','OCD')) + outline(['B','C','D','E'], GOLD, 0.9)
s += rangle(PT['B'], 1, 1) + rangle(PT['E'], 1, -1) + rangle(PT['C'], -1, 1)
s += at((10.5,0), 'x', 0, 4.6, RED, 2.4) + at((11.5,0), 'x', 0, 4.6, ORNG, 2.4)
s += at((10,2), '4x', -2.8, 1.0, RED, 2.4) + at((10,6), '4x', -2.8, 1.0, PINK, 2.4)
s += at((11,8), '2x', 0, -1.6, PINK, 2.4) + at((12,4), '8x', 4.6, 1.0, ORNG, 2.4) + names()
V['у треугольников BOP, PED и OCD прямые углы'] = fig(svg(s, 'BCDE и три прямоугольных треугольника', '-9 -7 92 63'),
  f"{cname('BOP')}, {cname('PED')}, {cname('OCD')}: катеты на сторонах BCDE (2x × 8x).")

# 8. раздел 2: ABEF и три угла
s = full() + ''.join(tri_(n, 0.5) for n in ('AFR','REP','ABP')) + outline(['A','B','E','F'], GOLD, 0.9)
s += rangle(PT['F'], 1, -1) + rangle(PT['E'], -1, -1) + rangle(PT['B'], -1, 1)
s += at((1,8), '2x', 0, -1.6, GOLD, 2.4) + at((6,8), '8x', 0, -1.6, GREEN, 2.4)
s += at((0,4), '8x', -4.4, 1.0, GOLD, 2.4) + at((5,0), '10x', 0, 4.6, TEAL, 2.4)
s += at((10,2), '4x', -2.8, 1.0, TEAL, 2.4) + at((10,6), '4x', -2.8, 1.0, GREEN, 2.4) + names()
V['у треугольников AFR, REP и ABP прямые углы'] = fig(svg(s, 'ABEF и три прямоугольных треугольника', '-9 -7 92 63'),
  f"{cname('AFR')}, {cname('REP')}, {cname('ABP')}: катеты на сторонах ABEF (10x × 8x).")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
