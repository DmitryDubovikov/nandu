import json, sys
# Рисунки к Т2″ регионал 2012 №2. Координаты задачи — в четвертях x (y вверх), x = 4:
# A = (0, 0), B = (4, 0), C = (7, 0), D = (8, 0), E = (8, 4), F = (0, 4).  SVG: X = U·x, Y = U·(4 − y).
U = 8
def xy(p): return round(U*p[0], 2), round(U*(4-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(4,0),'C':(7,0),'D':(8,0),'E':(8,4),'F':(0,4)}
OFF = {'A':(-2.6,4.6),'B':(0,4.8),'C':(0,4.8),'D':(2.6,4.6),'E':(2.6,-1.6),'F':(-2.6,-1.6)}
ALL = ['A','B','C','D','E','F']
SEG = [('A','B'),('B','C'),('C','D'),('D','E'),('E','F'),('F','A'),('E','B'),('E','C')]

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1, dash=False):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'{d}/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=3.0):
    X, Y = xy(p); return txt(round(X+dx,2), round(Y+dy,2), s, col, size)
def labels(names, col=LAB):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col) + f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def full(col=DIM, w=0.45): return ''.join(line(PT[a], PT[b], col, w) for a, b in SEG)
def names(): return labels(ALL, MUT)
def svg(inner, label, vb='-9 -8 84 52'): return f"<svg viewBox='{vb}' style='max-width:560px' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def fill(pts, col, op=0.4): return poly([PT[n] for n in pts], col, 1.0, col, op)
def tick(p, vertical, col=GOLD):   # штрих равенства посередине отрезка
    a, b = ((p[0], p[1]-0.3), (p[0], p[1]+0.3)) if vertical else ((p[0]-0.3, p[1]), (p[0]+0.3, p[1]))
    return line(a, b, col, 0.6)
def ticks(col=GOLD): return tick((2,0), True, col) + tick((6,0), True, col) + tick((8,2), False, col)
def xs(col=GOLD):   # подписи x у AB, BD, DE
    return at((2,0), 'x', 0, -1.6, col, 3.2) + at((6,0), 'x', 0, -1.6, col, 3.2) + at((8,2), 'x', 3.0, 1.0, col, 3.2)
def rangle(col=INK, s=0.4):   # прямой угол в D
    a, b, c = (8-s, 0), (8-s, s), (8, s)
    return f"<polyline points='{'%s,%s' % xy(a)} {'%s,%s' % xy(b)} {'%s,%s' % xy(c)}' fill='none' stroke='{col}' stroke-width='0.4'/>"

V = {}
# цвет фигуры — один во всех рисунках
TC = {'ABEF': BLUE, 'BCE': GREEN, 'CDE': VIO}
TP = {'ABEF': ['A','B','E','F'], 'BCE': ['B','C','E'], 'CDE': ['C','D','E']}
def tri_(n, op=0.42): return fill(TP[n], TC[n], op)
def cname(n): return f"<b style='color:{TC[n]}'>{n}</b>"

# 1. рисунок условия
V['⇒ AB = BD = DE'] = fig(svg(full(INK, 0.55) + labels(ALL), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: AB = BD = DE = x
s = full(INK, 0.5) + ticks() + xs() + labels(ALL)
V['AB = BD = DE = x'] = fig(svg(s, 'Буквы на рисунке'), '')

# 3. три куска
CEN = {'ABEF': (3.0,2.3), 'BCE': (6.4,1.2), 'CDE': (7.65,1.0)}
s = full(INK, 0.5) + ''.join(tri_(n) for n in TC) + ''.join(at(CEN[n], n, 0, 1.0, LAB, 2.6 if n != 'CDE' else 2.0) for n in TC) + labels(ALL)
V['разрезают прямоугольник ADEF на трапецию ABEF'] = fig(svg(s, 'Три куска'), '')

# 4. а) периметр ADEF
s = full() + poly([PT[n] for n in ['A','D','E','F']], GOLD, 1.1)
s += at((4,0), '2x', 0, 8.6, GOLD, 3.2) + at((4,4), '2x', 0, -4.0, GOLD, 3.2) + at((0,2), 'x', -3.2, 1.0, GOLD, 3.2) + at((8,2), 'x', 3.2, 1.0, GOLD, 3.2) + names()
V['у ADEF стороны AD и FE равны 2x'] = fig(svg(s, 'Периметр ADEF', '-9 -9 84 56'), 'а) периметр ADEF')

# 5. б) площадь ACEF = ADEF без CDE
s = full() + poly([PT[n] for n in ['A','C','E','F']], GOLD, 1.0, GOLD, 0.4) + poly([PT[n] for n in ['C','D','E']], VIO, 0.8, 'none', 1, True)
s += at((4,4), '2x', 0, -4.0, GOLD, 3.2) + at((0,2), 'x', -3.2, 1.0, GOLD, 3.2) + names()
V['ACEF — это прямоугольник ADEF без треугольника CDE'] = fig(svg(s, 'Площадь ACEF', '-9 -9 84 52'),
  f"б) площадь ACEF: прямоугольник 2x × x без {cname('CDE')}")

# 6. порядок поиска: S(BCE) известна; ① S(CDE), ② x — номера разделов
s = full() + tri_('BCE', 0.45) + tri_('CDE', 0.45) + ticks() + at((6.4,1.2), '294', 0, 1.0, LAB, 3.0)
s += at((7.65,1.0), '?①', 0, 1.0, LAB, 2.2) + at((6,0), 'x ?②', -1.0, 4.8, GOLD, 2.8) + at((8,2), 'x ?②', 5.4, 1.0, GOLD, 2.8) + names()
V['S(BCE) = 294 → S(CDE) → x'] = fig(svg(s, 'Порядок поиска', '-9 -8 88 52'),
  f"Площадь {cname('BCE')} известна; номер — раздел, где найдём величину: ① площадь {cname('CDE')}, ② x.")

# 7. раздел 2: BDE = BCE + CDE, катеты x
s = full() + tri_('BCE', 0.5) + tri_('CDE', 0.5) + poly([PT[n] for n in ['B','D','E']], GOLD, 1.1) + rangle()
s += ticks() + at((6,0), 'x', 0, 4.6, GOLD, 3.2) + at((8,2), 'x', 3.0, 1.0, GOLD, 3.2) + names()
V['треугольник BDE состоит из BCE и CDE'] = fig(svg(s, 'BDE из BCE и CDE'),
  f"BDE = {cname('BCE')} + {cname('CDE')}; катеты BD и DE равны x.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
