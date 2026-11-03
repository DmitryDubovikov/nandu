import json, sys
# Рисунки к Т2′ национал 2020 день I №2. Координаты задачи — в клетках x (y вверх), A = (0, 0), C = (8, 6).
# SVG: X = U·x, Y = U(6 − y).
U = 8
def xy(p): return U*p[0], U*(6-p[1])
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(8,0),'C':(8,6),'D':(0,6),'M':(4,0),'P':(8,4),'Q':(1,6),'R':(0,1)}
OFF = {'A':(-3.2,4.4),'B':(3.2,4.4),'C':(3.2,-1.8),'D':(-3.2,-1.8),'M':(0,4.6),'P':(3.6,1.2),
       'Q':(0,-2.4),'R':(-3.6,1.2)}

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
ALL = ['A','B','C','D','M','P','Q','R']
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри ABCD
    return ''.join(line((x,0),(x,6),col,w) for x in range(0,9)) + ''.join(line((0,y),(8,y),col,w) for y in range(0,7))
def svg(inner, label, vb='-10 -7 84 66'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x = AR, у A
    return line((0,0),(0,1),GOLD,1.4) + at((0,0.5), 'x', -3.0, 1.0, GOLD, 3.2)
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    P_ = PT
    return poly([P_['A'],P_['B'],P_['C'],P_['D']], col, w) + poly([P_['M'],P_['P'],P_['Q'],P_['R']], col, w)
def names(): return labels(ALL, MUT)
def dimAB(col=GOLD):   # размер AB = 8x — выноской ниже AB, чтобы не налезать на подписи A, M, B
    return (line((0,-1.2),(8,-1.2),col,0.5) + line((0,-1.0),(0,-1.4),col,0.5) + line((8,-1.0),(8,-1.4),col,0.5)
            + at((4,-1.2), '8x', 0, 4.0, col))
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)

V = {}
# 1. рисунок условия
s = poly([PT['M'],PT['P'],PT['Q'],PT['R']], '#c87a55', 0.7, '#c87a55', 0.35) + full(INK, 0.55) + labels(ALL)
V['все отрезки выражаются через AR'] = fig(svg(s, 'Рисунок условия', '-10 -7 84 62'), 'Рисунок из условия.')

# 2. буквы: сетка, x = AR
s = grid() + full() + xmark() + line((0,0),(8,0),GOLD,1.0) + dimAB()
s += line((8,0),(8,6),GOLD,1.0) + at((8,3), '6x', 4.6, 1.0, GOLD, 3.2) + names()
V['AB = 8x, BC = 6x, сетка с шагом x.'] = fig(svg(s, 'Буквы', '-10 -7 84 70'),
  "<b style='color:#f0a83c'>x</b> = AR; все точки — в узлах сетки.")

G = grid() + full()
# а) PCQ: катеты PC = 2x, CQ = 7x
s = G + tri([PT['P'],PT['C'],PT['Q']], GOLD) + at((8,5), '2x', 4.4, 1.0) + at((4.5,6), '7x', 0, -1.8) + xmark() + names()
V['PCQ — прямоугольный треугольник с катетами'] = fig(svg(s, 'PCQ на сетке'), 'а) площадь PCQ')
# б) ABPR: прямоугольная трапеция
s = G + poly([PT['A'],PT['B'],PT['P'],PT['R']], GOLD, 1.0, GOLD, 0.4)
s += at((0,0.5), 'x', -3.0, 1.0, GOLD, 3.2) + line((0,0),(0,1),GOLD,1.4)
s += at((8,2), '4x', 4.6, 1.0) + dimAB() + names()
V['ABPR — прямоугольная трапеция'] = fig(svg(s, 'ABPR на сетке', '-10 -7 84 70'), 'б) площадь ABPR')
# в) MPQR = ABCD без четырёх угловых треугольников
s = grid() + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 1.0)
s += poly([PT['M'],PT['P'],PT['Q'],PT['R']], INK, 0.8)
s += tri([PT['A'],PT['M'],PT['R']], BLUE, 0.35) + tri([PT['M'],PT['B'],PT['P']], GREEN, 0.35)
s += tri([PT['P'],PT['C'],PT['Q']], RED, 0.35) + tri([PT['Q'],PT['D'],PT['R']], VIO, 0.35)
s += at((2,0), '4x', 0, 4.4, BLUE) + at((6,0), '4x', 0, 4.4, GREEN) + at((8,2), '4x', 4.6, 1.0, GREEN)
s += at((8,5), '2x', 4.6, 1.0, RED) + at((4.5,6), '7x', 0, -1.8, RED) + at((0,3.5), '5x', -4.0, 1.0, VIO)
s += xmark() + names()
V['без четырёх прямоугольных треугольников'] = fig(svg(s, 'MPQR внутри ABCD', '-10 -7 84 66'),
  "в) площадь MPQR: <b style='color:#f0a83c'>ABCD</b> без <b style='color:#5ba8f5'>AMR</b>, <b style='color:#5fd38d'>MBP</b>, "
  "<b style='color:#f2686c'>PCQ</b> и <b style='color:#c58af9'>QDR</b>.")

# 6. раздел «Найдём x»: MBP с катетами 4x и 4x
s = grid() + full() + tri([PT['M'],PT['B'],PT['P']], GREEN, 0.5)
s += at((6,0), '4x', 0, 4.4, GREEN) + at((8,2), '4x', 4.6, 1.0, GREEN) + xmark() + names()
V['MBP — прямоугольный треугольник с катетами'] = fig(svg(s, 'MBP на сетке'),
  "<b style='color:#5fd38d'>MBP</b>: катеты MB = 4x и BP = 4x, площадь дана.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
