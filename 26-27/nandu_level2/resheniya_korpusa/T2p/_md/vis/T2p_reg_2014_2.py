import json, sys
# Рисунки к Т2′ регионал 2014 №2. Координаты задачи — в клетках x (y вверх), A = (0, 0), C = (10, 2), N = (5/3, 2).
# SVG: X = U·x, Y = U(2 − y).
U = 8
def xy(p): return round(U*p[0], 2), round(U*(2-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(10,0),'C':(10,2),'D':(0,2),'M':(10,1),'N':(5/3,2)}
OFF = {'A':(-3.2,3.6),'B':(3.2,3.6),'C':(3.2,-1.6),'D':(-3.2,-1.6),'M':(3.6,1.2),'N':(0,-2.4)}

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
ALL = ['A','B','C','D','M','N']
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри ABCD
    return ''.join(line((x,0),(x,2),col,w) for x in range(0,11)) + ''.join(line((0,y),(10,y),col,w) for y in range(0,3))
def svg(inner, label, vb='-10 -8 100 34'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x = BM, у B
    return line((10,0),(10,1),GOLD,1.4) + at((10,0.5), 'x', 3.0, 1.0, GOLD, 3.2)
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    P_ = PT
    return poly([P_['A'],P_['B'],P_['C'],P_['D']], col, w) + poly([P_['A'],P_['M'],P_['N']], col, w)
def names(): return labels(ALL, MUT)
def dimAB(col=GOLD):   # размер AB = 10x — выноской ниже AB, чтобы не налезать на подписи A и B
    return (line((0,-1.0),(10,-1.0),col,0.5) + line((0,-0.8),(0,-1.2),col,0.5) + line((10,-0.8),(10,-1.2),col,0.5)
            + at((5,-1.0), '10x', 0, 4.0, col))
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
VB2 = '-10 -8 100 40'

V = {}
# 1. рисунок условия
s = poly([PT['A'],PT['M'],PT['N']], '#c87a55', 0.7, '#c87a55', 0.35) + poly([PT['A'],PT['B'],PT['C'],PT['D']], INK, 0.55)
s += poly([PT['A'],PT['M'],PT['N']], INK, 0.55) + labels(ALL)
V['чтобы стороны AD, AB и половины BM, MC'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: сетка, x = BM
s = grid() + full() + xmark() + line((0,0),(10,0),GOLD,1.0) + dimAB()
s += line((0,0),(0,2),GOLD,1.0) + at((0,1), '2x', -4.4, 1.0, GOLD, 3.2) + names()
V['сетка с шагом x.'] = fig(svg(s, 'Буквы', VB2),
  "<b style='color:#f0a83c'>x</b> = BM; все точки, кроме N, — в узлах сетки.")

G = grid() + full()
# а) AB = 10x
s = G + line((0,0),(10,0),GOLD,1.4) + dimAB() + xmark() + names()
V['вся сторона AB идёт по сетке'] = fig(svg(s, 'AB на сетке', VB2), 'а) длина AB')
# б) DN — катет AND
s = G + tri([PT['A'],PT['N'],PT['D']], GOLD) + at((0,1), '2x', -4.4, 1.0) + line(PT['D'],PT['N'],RED,1.2)
s += at((5/6,2), 'DN', 0, -4.6, RED, 3.0) + xmark() + names()
V['DN — катет прямоугольного треугольника AND'] = fig(svg(s, 'AND на сетке', '-10 -12 100 38'),
  "б) длина DN: катет <b style='color:#f0a83c'>AND</b>, площадь AND дана.")
# в) AMN = ABCD без ABM, MCN, AND
s = grid() + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 1.0)
s += tri([PT['A'],PT['B'],PT['M']], BLUE, 0.35) + tri([PT['M'],PT['C'],PT['N']], GREEN, 0.35) + tri([PT['N'],PT['D'],PT['A']], VIO, 0.35)
s += poly([PT['A'],PT['M'],PT['N']], INK, 0.8)
s += dimAB(BLUE) + at((10,0.5), 'x', 3.0, 1.0, BLUE, 3.0) + at((10,1.5), 'x', 3.0, 1.0, GREEN, 3.0)
s += at((0,1), '2x', -4.4, 1.0, VIO) + at((5/6,2), 'DN', 0, -4.6, VIO, 2.8) + at((35/6,2), 'NC', 0, -4.6, GREEN, 2.8)
s += line((10,0),(10,1),GOLD,1.4) + names()
V['без трёх прямоугольных треугольников'] = fig(svg(s, 'AMN внутри ABCD', '-10 -12 100 42'),
  "в) площадь AMN: <b style='color:#f0a83c'>ABCD</b> без <b style='color:#5ba8f5'>ABM</b>, "
  "<b style='color:#5fd38d'>MCN</b> и <b style='color:#c58af9'>AND</b>.")

# 6. раздел «Найдём x»: ABM с катетами 10x и x
s = grid() + full() + tri([PT['A'],PT['B'],PT['M']], BLUE, 0.5)
s += dimAB(BLUE) + at((10,0.5), 'x', 3.0, 1.0, BLUE, 3.2) + names()
V['ABM — прямоугольный треугольник с катетами'] = fig(svg(s, 'ABM на сетке', VB2),
  "<b style='color:#5ba8f5'>ABM</b>: катеты AB = 10x и BM = x, площадь дана.")

# 7. раздел «Найдём DN»: AND с катетами 2x и DN
s = grid() + full() + tri([PT['A'],PT['N'],PT['D']], VIO, 0.5)
s += at((0,1), '2x', -4.4, 1.0, VIO, 3.2) + at((5/6,2), 'DN', 0, -4.6, VIO, 3.0) + xmark() + names()
V['AND — прямоугольный треугольник с катетами'] = fig(svg(s, 'AND на сетке', '-10 -12 100 38'),
  "<b style='color:#c58af9'>AND</b>: катеты AD = 2x и DN, площадь дана.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
