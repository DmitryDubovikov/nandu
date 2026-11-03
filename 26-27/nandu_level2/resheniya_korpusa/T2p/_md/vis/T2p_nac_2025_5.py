import json, sys
# Рисунки к Т2′ национал 2025 день II №5. Координаты задачи — в кирпичах x (y вверх), J = (0, 0), K = (3, 0), I = (0, 3).
# SVG: X = U(x + 1), Y = U(4 − y).
U = 8
def xy(p): return U*(p[0]+1), U*(4-p[1])
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,-2),'B':(3,-2),'C':(3,4),'D':(0,4),'E':(-1,0),'F':(5,0),'G':(5,3),'H':(-1,3),
      'I':(0,3),'J':(0,0),'K':(3,0),'L':(3,3),'M':(2,3),'N':(0,1),'P':(5,-2)}
OFF = {'A':(-3.0,4.4),'B':(3.2,4.4),'C':(3.0,-1.6),'D':(-3.0,-1.6),'E':(-3.2,4.0),'F':(3.4,4.0),'G':(3.4,-1.6),
       'H':(-3.4,-1.6),'I':(-2.8,-1.8),'J':(-2.8,4.2),'K':(3.0,4.2),'L':(3.0,-1.8),'M':(0,-2.2),'N':(-3.4,1.2),
       'P':(3.2,4.4)}

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
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри креста из ABCD и EFGH
    s = ''.join(line((x,-2),(x,4),col,w) for x in range(0,4))
    s += ''.join(line((x,0),(x,3),col,w) for x in (-1,4,5))
    s += ''.join(line((0,y),(3,y),col,w) for y in range(-2,5))
    s += ''.join(line((-1,y),(5,y),col,w) for y in range(0,4))
    return s
def svg(inner, label, vb='-10 -7 68 64', big=False):
    st = " style='max-width:560px'" if big else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x — треть AB, у A
    return line((0,-2),(1,-2),GOLD,1.4) + at((0.5,-2), 'x', 0, 4.4, GOLD, 3.2)
def full(col=DIM, w=0.45):   # весь чертёж условия — фон каждого рисунка
    P_ = PT
    s = poly([P_['A'],P_['B'],P_['C'],P_['D']], col, w) + poly([P_['E'],P_['F'],P_['G'],P_['H']], col, w)
    s += poly([P_['K'],P_['M'],P_['N']], col, w)
    return s
ALL = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
def names(extra=()): return labels(ALL + list(extra), MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)

V = {}
# 1. рисунок условия
s = poly([PT['K'],PT['M'],PT['N']], '#9aa4ae', 0.6, '#9aa4ae', 0.45) + full(INK, 0.55) + labels(ALL)
V['I и J лежат на AD'] = fig(svg(s, 'Рисунок условия', big=True), 'Рисунок из условия.')

# 2. буквы: сетка, x — треть AB
s = grid() + full() + xmark()
s += line(PT['A'],PT['D'],GOLD,1.0) + at((0,-1), '6x', -4.6, 1.0)
s += line(PT['H'],PT['G'],GOLD,1.0) + at((4.5,3), '6x', 0, 4.2)
s += at((2,-2), '3x', 0, 4.4)
s += names()
V['сетка с шагом x.'] = fig(svg(s, 'Буквы', big=True), "<b style='color:#f0a83c'>x</b> = AB : 3; все точки — в узлах сетки.")

G = grid() + full()
# а) IJKL
s = G + poly([PT['I'],PT['J'],PT['K'],PT['L']], GOLD, 1.0, GOLD, 0.35) + at((1.5,0), '3x', 0, 4.0) + xmark() + names()
V['IJKL — квадрат со стороной JK = 3x'] = fig(svg(s, 'а) IJKL на сетке'), 'а) площадь IJKL')
# б) ABCD
s = G + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 1.2) + at((1.5,-2), '3x', 0, 4.4) + at((0,-1), '6x', -4.6, 1.0)
s += line((0,-2),(1,-2),GOLD,1.4) + names()
V['ABCD — прямоугольник со сторонами AB = 3x и AD = 6x'] = fig(svg(s, 'б) ABCD на сетке'), 'б) периметр ABCD')
# в) HNKG = HIN + (IJKL без KJN) + LKG
s = G + tri([PT['H'],PT['I'],PT['N']], BLUE, 0.4) + poly([PT['I'],PT['N'],PT['K'],PT['L']], GOLD, 1.0, GOLD, 0.35)
s += poly([PT['N'],PT['J'],PT['K']], RED, 0.8, 'none', 1, True) + tri([PT['L'],PT['K'],PT['G']], GREEN, 0.4)
s += at((-0.4,2.6), 'x', 0, 1.0, BLUE) + at((0,2), '2x', 3.4, 1.0, BLUE)
s += at((1.5,0), '3x', 0, 4.0, RED) + at((0,0.5), 'x', -2.4, 1.2, RED)
s += at((4,3), '2x', 0, -2.0, GREEN) + at((3,1.5), '3x', 3.6, 1.0, GREEN) + xmark() + names()
V['INKL — квадрат IJKL без прямоугольного треугольника KJN'] = fig(svg(s, 'в) HNKG на сетке'),
  "в) площадь HNKG: <b style='color:#5ba8f5'>HIN</b> + <b style='color:#f0a83c'>INKL</b> + <b style='color:#5fd38d'>LKG</b>; INKL — квадрат без <b style='color:#f2686c'>KJN</b>.")
# г) AMLF = AIGP без AIM, LGF, FPA
s = G + line(PT['B'],PT['P'],GOLD,0.6,True) + line(PT['F'],PT['P'],GOLD,0.6,True)
s += poly([PT['A'],PT['I'],PT['G'],PT['P']], GOLD, 1.0)
s += tri([PT['A'],PT['I'],PT['M']], BLUE, 0.35) + tri([PT['L'],PT['G'],PT['F']], GREEN, 0.35) + tri([PT['F'],PT['P'],PT['A']], RED, 0.35)
s += poly([PT['A'],PT['M'],PT['L'],PT['F']], VIO, 1.0, VIO, 0.3)
s += line(PT['A'],PT['I'],GOLD,1.0) + line(PT['I'],PT['G'],GOLD,1.0) + line(PT['G'],PT['F'],GOLD,1.0) + line(PT['F'],PT['P'],GOLD,1.0,True) + line(PT['B'],PT['P'],GOLD,1.0,True)
s += at((0,0.5), '5x', -4.6, 1.0, BLUE) + at((1,3), '2x', 0, -2.0, BLUE)
s += at((4,3), '2x', 0, -2.0, GREEN) + at((5,1.5), '3x', 3.6, 1.0, GREEN)
s += at((5,-1), '2x', 3.6, 1.0, RED) + at((2.5,-2), '5x', 0, 4.4, RED)
s += line((0,-2),(1,-2),GOLD,1.4) + names(['P'])
V['AMLF — прямоугольник AIGP без прямоугольных треугольников'] = fig(svg(s, 'г) AMLF на сетке', '-10 -7 68 64'),
  "г) площадь <b style='color:#c58af9'>AMLF</b>: <b style='color:#f0a83c'>AIGP</b> без <b style='color:#5ba8f5'>AIM</b>, <b style='color:#5fd38d'>LGF</b> и <b style='color:#f2686c'>FPA</b>.")
# раздел 1: KMN = IJKL без NIM, MLK, KJN
s = grid() + full() + poly([PT['I'],PT['J'],PT['K'],PT['L']], GOLD, 1.0)
s += tri([PT['N'],PT['I'],PT['M']], BLUE, 0.35) + tri([PT['M'],PT['L'],PT['K']], GREEN, 0.35) + tri([PT['K'],PT['J'],PT['N']], VIO, 0.35)
s += poly([PT['K'],PT['M'],PT['N']], RED, 0.9, RED, 0.35)
s += at((0,2), '2x', -4.4, 1.0, BLUE) + at((1,3), '2x', 0, -2.0, BLUE)
s += at((2.5,3), 'x', 0, -2.0, GREEN) + at((3,1.5), '3x', 3.6, 1.0, GREEN)
s += at((1.5,0), '3x', 0, 4.0, VIO) + at((0,0.5), 'x', -2.4, 1.2, VIO) + xmark() + names()
V['KMN — это квадрат IJKL без трёх'] = fig(svg(s, 'KMN внутри IJKL'),
  "<b style='color:#f2686c'>KMN</b> = <b style='color:#f0a83c'>IJKL</b> без <b style='color:#5ba8f5'>NIM</b>, <b style='color:#5fd38d'>MLK</b> и <b style='color:#c58af9'>KJN</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
