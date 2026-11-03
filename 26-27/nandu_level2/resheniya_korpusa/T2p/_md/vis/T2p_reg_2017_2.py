import json, sys
# Рисунки к Т2′ регионал 2017 №2. Координаты задачи — в кирпичах x (y вверх), A = (0, 0), C = (12, 12).
# SVG: X = U·x + 9, Y = U(12 − y) + 7.
U = 4
def xy(p): return U*p[0]+9, U*(12-p[1])+7
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(12,0),'C':(12,12),'D':(0,12),'Q':(12,4),'R':(9,12),'P':(3,4)}
OFF = {'A':(-3.0,4.0),'B':(3.0,4.0),'C':(3.0,-1.6),'D':(-3.0,-1.6),'Q':(3.4,1.2),'R':(0,-2.2),'P':(-1.6,4.4)}

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
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.25):   # сетка с шагом x в квадрате ABCD
    return ''.join(line((i,0),(i,12),col,w) + line((0,i),(12,i),col,w) for i in range(13))
def svg(inner, label, vb='0 0 66 64', big=False):
    st = " style='max-width:560px'" if big else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x — двенадцатая часть стороны, у A на AB
    return line((0,0),(1,0),GOLD,1.4) + at((0.5,0), 'x', 0, 4.2, GOLD, 3.2)
def full(col=DIM, w=0.45):   # весь чертёж условия — фон каждого рисунка
    P_ = PT
    return (poly([P_['A'],P_['B'],P_['C'],P_['D']], col, w) + line(P_['D'],P_['P'],col,w)
            + line(P_['P'],P_['Q'],col,w) + line(P_['Q'],P_['R'],col,w))
ALL = ['A','B','C','D','P','Q','R']
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)

V = {}
# 1. рисунок условия
s = poly([PT['P'],PT['Q'],PT['R'],PT['D']], '#9aa4ae', 0.6, '#9aa4ae', 0.35) + full(INK, 0.55) + labels(ALL)
V['Q лежит на BC, R — на DC, P — внутри квадрата.'] = fig(svg(s, 'Рисунок условия', big=True), 'Рисунок из условия.')

# 2. буквы: сетка, x — двенадцатая часть AB
s = grid() + full() + xmark()
s += at((6,0), '12x', 0, 4.2) + line(PT['B'],PT['Q'],GOLD,1.0) + at((12,2), '4x', 3.8, 1.0)
s += line(PT['Q'],PT['C'],GOLD,1.0) + at((12,8), '8x', 3.8, 1.0)
s += line(PT['D'],PT['R'],GOLD,1.0) + at((4.5,12), '9x', 0, -1.8) + at((10.5,12), '3x', 0, -1.8)
s += line(PT['P'],PT['Q'],GOLD,1.0) + at((7.5,4), '9x', 0, 4.0)
s += names()
V['AB = BC = 12x, сетка с шагом x.'] = fig(svg(s, 'Буквы', big=True),
  "<b style='color:#f0a83c'>x</b> = BC : 12; все точки — в узлах сетки.")

G = grid() + full()
# а) QCR
s = G + tri([PT['Q'],PT['C'],PT['R']], GOLD) + at((12,8), '8x', 3.8, 1.0) + at((10.5,12), '3x', 0, -1.8) + xmark() + names()
V['QCR — прямоугольный треугольник с катетами QC и CR'] = fig(svg(s, 'а) QCR на сетке'), 'а) площадь QCR')
# б) PQRD — параллелограмм: основание DR, высота QC
s = G + poly([PT['P'],PT['Q'],PT['R'],PT['D']], VIO, 1.0, VIO, 0.35)
s += line(PT['D'],PT['R'],GOLD,1.4) + at((4.5,12), '9x', 0, -1.8)
s += line(PT['Q'],PT['C'],BLUE,1.4,True) + at((12,8), '8x', 3.8, 1.0, BLUE) + xmark() + names()
V['у параллелограмма PQRD основание DR'] = fig(svg(s, 'б) PQRD на сетке'),
  "б) площадь <b style='color:#c58af9'>PQRD</b>: основание <b style='color:#f0a83c'>DR</b>, высота <b style='color:#5ba8f5'>QC</b> пунктиром.")
# в) PBCD = PQCD + PBQ
s = G + poly([PT['P'],PT['Q'],PT['C'],PT['D']], GOLD, 1.0, GOLD, 0.3) + tri([PT['P'],PT['B'],PT['Q']], BLUE, 0.4)
s += at((7.5,4), '9x', 0, -1.4, BLUE) + at((12,2), '4x', 3.8, 1.0, BLUE)
s += at((6,12), '12x', 0, -1.8) + at((12,8), '8x', 3.8, 1.0) + xmark() + names()
V['отрезок PQ режет PBCD'] = fig(svg(s, 'в) PBCD на сетке'),
  "в) площадь PBCD: <b style='color:#f0a83c'>трапеция PQCD</b> + <b style='color:#5ba8f5'>PBQ</b>.")
# г) PBR = PBCD без BCR и PRD
s = G + poly([PT['P'],PT['B'],PT['C'],PT['D']], GOLD, 1.0)
s += tri([PT['B'],PT['C'],PT['R']], BLUE, 0.35) + tri([PT['P'],PT['R'],PT['D']], GREEN, 0.35)
s += poly([PT['P'],PT['B'],PT['R']], VIO, 1.0, VIO, 0.35)
s += line((3,4),(3,12),GREEN,0.7,True) + at((3,8), '8x', 3.8, 1.0, GREEN) + at((4.5,12), '9x', 0, -1.8, GREEN)
s += at((12,6), '12x', 4.6, 1.0, BLUE) + at((10.5,12), '3x', 0, -1.8, BLUE) + xmark() + names()
V['у PRD основание DR лежит на DC'] = fig(svg(s, 'г) PBR на сетке', '0 0 68 64'),
  "г) площадь <b style='color:#c58af9'>PBR</b>: PBCD без <b style='color:#5ba8f5'>BCR</b> и <b style='color:#5fd38d'>PRD</b>; высота PRD пунктиром.")
# раздел 1: квадрат ABCD
s = grid() + full() + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 1.0, GOLD, 0.2)
s += at((6,0), '12x', 0, 4.2) + at((12,6), '12x', 4.6, 1.0) + names()
V['ABCD — квадрат со стороной AB = 12x'] = fig(svg(s, 'Квадрат ABCD', '0 0 68 64'), 'Квадрат ABCD, площадь 2304.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
