import json, sys
# Рисунки к Т2′ регионал 2021 №2. Координаты задачи — в кирпичах x (y вверх), F = (0, 0), A = (3, 0), D = (3, 6), E = (0, 6).
# SVG: X = U · x, Y = U · (6 − y).
U = 8
def xy(p): return U*p[0], U*(6-p[1])
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(3,0),'B':(3,2),'C':(3,3),'D':(3,6),'E':(0,6),'F':(0,0)}
OFF = {'A':(3.2,3.4),'B':(3.6,1.2),'C':(3.6,1.2),'D':(3.2,-1.6),'E':(-3.2,-1.6),'F':(-3.2,3.4)}
SEGS = [('E','D'),('D','A'),('A','F'),('F','E'),('E','C'),('E','B')]

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
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
def labels(col=LAB, dots=True):
    out = ''
    for n in PT:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри ADEF
    s = ''.join(line((i,0),(i,6),col,w) for i in range(0,4))
    return s + ''.join(line((0,j),(3,j),col,w) for j in range(0,7))
def full(col=DIM, w=0.45): return ''.join(line(PT[a],PT[b],col,w) for a, b in SEGS)
def names(): return labels(MUT)
def svg(inner, label, vb='-9 -6 42 62', mw='260px'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x — шестая часть AD, у A
    return line((3,0),(3,1),GOLD,1.4) + at((3,0.5), 'x', 2.6, 1.0, GOLD, 3.2)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels()
V['AD : AF = 2 : 1.'] = fig(svg(s, 'Рисунок условия', mw='300px'), 'Рисунок из условия.')

# 2. буквы: сетка, x — шестая часть AD
s = grid() + full() + xmark()
s += line((3,0),(3,6),GOLD,1.0) + at((3,4), '6x', 4.4, 1.0)
s += line((0,0),(3,0),GOLD,1.0) + at((1.5,0), '3x', 0, 4.4)
s += names()
V['сетка с шагом x.'] = fig(svg(s, 'Буквы', mw='300px'), "<b style='color:#f0a83c'>x</b> = AD : 6; все точки — в узлах сетки.")

# 3–5. артефакт: каждое спрошенное на сетке x
G = grid() + full()
# а) ADEF: стороны AD = 6x, AF = 3x
s = G + poly([PT['A'],PT['D'],PT['E'],PT['F']], GOLD, 1.0, GOLD, 0.35) + at((3,4), '6x', 4.4, 1.0) + at((1.5,0), '3x', 0, 4.4)
s += xmark() + names()
V['со сторонами AD и AF.'] = fig(svg(s, 'ADEF на сетке'), 'а) площадь ADEF: стороны 6x и 3x.')
# б) трапеция ABEF: основания AB = 2x, FE = 6x, высота AF = 3x
s = G + poly([PT['A'],PT['B'],PT['E'],PT['F']], GOLD, 1.0, GOLD, 0.35)
s += at((3,1.5), '2x', 4.4, 1.0) + at((0,3), '6x', -4.4, 1.0) + at((1.5,0), '3x', 0, 4.4)
s += xmark() + names()
V['и высотой AF.'] = fig(svg(s, 'Трапеция ABEF на сетке'), 'б) площадь ABEF: основания 2x и 6x, высота 3x.')
# в) BCE = BDE без CDE
s = G + tri([PT['C'],PT['D'],PT['E']], GREEN, 0.35) + tri([PT['B'],PT['C'],PT['E']], VIO, 0.55)
s += poly([PT['B'],PT['D'],PT['E']], BLUE, 0.7)
s += at((1.5,6), '3x', 0, -1.8, BLUE) + at((3,4.5), '3x', 4.4, 1.0, GREEN) + at((3,2.5), 'x', 4.4, 1.0, VIO)
s += xmark() + names()
V['без прямоугольного треугольника CDE.'] = fig(svg(s, 'BCE на сетке'),
  "в) площадь <b style='color:#c58af9'>BCE</b> = <b style='color:#5ba8f5'>BDE</b> без <b style='color:#5fd38d'>CDE</b>; общий катет DE = 3x, BD = 4x.")

# 6. раздел «Найдём x»: обход ADEF
s = grid() + full() + poly([PT['A'],PT['D'],PT['E'],PT['F']], RED, 1.2)
s += at((3,4), '6x', 4.4, 1.0, RED) + at((0,3), '6x', -4.4, 1.0, RED) + at((1.5,0), '3x', 0, 4.4, RED) + at((1.5,6), '3x', 0, -1.8, RED)
s += xmark() + names()
V['Заметим, что у ADEF'] = fig(svg(s, 'Обход ADEF'), 'P(ADEF) = 252.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
