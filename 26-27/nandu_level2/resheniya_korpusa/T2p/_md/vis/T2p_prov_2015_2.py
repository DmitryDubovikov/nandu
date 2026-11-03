import json, sys
# Рисунки к Т2′ провинциал 2015 №2. Координаты задачи — в кирпичах x = AB : 12 (y вверх), A = (0, 0), C = (12, 8),
# M = (6, 0), T = (0, 4), R = (3, 8). SVG: X = U·x, Y = U·(8 − y).
U = 5
def xy(p): return round(U*p[0], 2), round(U*(8-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(12,0),'C':(12,8),'D':(0,8),'M':(6,0),'T':(0,4),'R':(3,8)}
OFF = {'A':(-3.0,4.2),'B':(3.0,4.2),'C':(3.0,-1.6),'D':(-3.0,-1.6),'M':(0,4.4),'T':(-3.4,1.2),'R':(0,-2.2)}

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
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри ABCD
    return ''.join(line((i,0),(i,8),col,w) for i in range(13)) + ''.join(line((0,j),(12,j),col,w) for j in range(9))
VB = '-8 -7 77 56'
def svg(inner, label, vb=VB):
    return f"<svg style='max-width:560px' viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
SEG = [('A','B'),('B','C'),('C','D'),('D','A'),('T','R'),('T','M')]
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    return ''.join(line(PT[a],PT[b],col,w) for a,b in SEG)
ALL = list('ABCDMTR')
def names(): return labels(ALL, MUT)
def xmark():   # кирпич x — двенадцатая часть AB, у B снизу
    return line((11,0),(12,0),GOLD,1.4) + at((11.5,0), 'x', 0, 4.4, GOLD, 3.2)
def tri(pts, col, op=0.45): return poly([PT[p] for p in pts], col, 1.0, col, op)
PENT = ['M','B','C','R','T']

V = {}
# 1. рисунок условия
s = poly([PT[p] for p in PENT], '#c87a55', 0.7, '#c87a55', 0.25) + full(INK, 0.55) + labels(ALL)
V['AB : BC = 3 : 2.'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: сетка с шагом x
s = grid() + full() + line(PT['A'],PT['B'],GOLD,1.0) + line(PT['B'],PT['C'],GOLD,1.0)
s += at((3,0), '12x', 0, 4.4) + at((12,5), '8x', 4.2, 1.0) + xmark() + names()
V['AB = 12x, BC = 8x, сетка с шагом x.'] = fig(svg(s, 'Буквы'), "<b style='color:#f0a83c'>x</b> = AB : 12; все точки — в узлах сетки.")

# 3–6. из каких фигур состоит каждое спрошенное
G = grid() + full()
# а) площадь ABCD
s = G + poly([PT[p] for p in 'ABCD'], GOLD, 1.0, GOLD, 0.3)
s += at((3,0), '12x', 0, 4.4) + at((12,5), '8x', 4.2, 1.0) + xmark() + names()
V['прямоугольник со сторонами AB = 12x и BC = 8x'] = fig(svg(s, 'Прямоугольник ABCD'), "а) площадь <b style='color:#f0a83c'>ABCD</b>.")
# б) периметр ABCD
s = G + poly([PT[p] for p in 'ABCD'], GOLD, 1.2)
s += at((3,0), '12x', 0, 4.4) + at((7.5,8), '12x', 0, -1.6) + at((12,5), '8x', 4.2, 1.0) + at((0,6), '8x', -4.2, 1.0)
s += xmark() + names()
V['две стороны по 8x (BC и AD)'] = fig(svg(s, 'Контур ABCD'), "б) периметр <b style='color:#f0a83c'>ABCD</b>.")
# в) площадь MBCR — трапеция
s = G + poly([PT[p] for p in 'MBCR'], GOLD, 1.0, GOLD, 0.35) + line(PT['M'],PT['R'],GOLD,0.8,True)
s += at((9,0), '6x', 0, 4.4, BLUE) + at((7.5,8), '9x', 0, -1.6, BLUE) + at((12,5), '8x', 4.2, 1.0)
s += xmark() + names()
V['трапеция с основаниями MB = 6x, RC = 9x и высотой BC = 8x'] = fig(svg(s, 'Трапеция MBCR'),
  "в) площадь трапеции <b style='color:#f0a83c'>MBCR</b>; основания <b style='color:#5ba8f5'>MB</b> и <b style='color:#5ba8f5'>RC</b>.")
# г) площадь MRT = MBCRT без MBCR
s = G + poly([PT[p] for p in PENT], GOLD, 1.0)
s += tri(['M','B','C','R'], BLUE, 0.3) + tri(['M','R','T'], VIO, 0.45) + line(PT['M'],PT['R'],VIO,0.8,True)
s += poly([PT[p] for p in PENT], GOLD, 1.0) + xmark() + names()
V['это MBCRT без трапеции MBCR'] = fig(svg(s, 'MRT = MBCRT без MBCR'),
  "г) площадь <b style='color:#c58af9'>MRT</b> = <b style='color:#f0a83c'>MBCRT</b> (702) без <b style='color:#5ba8f5'>MBCR</b>.")

# 7. раздел «Найдём x»: MBCRT = ABCD без AMT и TDR
s = grid() + full() + poly([PT[p] for p in 'ABCD'], GOLD, 1.0)
s += poly([PT[p] for p in PENT], RED, 0.8, RED, 0.35)
s += tri(['A','M','T'], BLUE, 0.35) + tri(['T','D','R'], GREEN, 0.35)
s += at((3,0), '6x', 0, 4.4, BLUE) + at((0,2), '4x', -4.2, 1.0, BLUE)
s += at((0,6), '4x', -4.2, 1.0, GREEN) + at((1.5,8), '3x', 0, -1.6, GREEN)
s += at((12,5), '8x', 4.2, 1.0) + xmark() + names()
V['MBCRT — это прямоугольник ABCD без'] = fig(svg(s, 'MBCRT внутри ABCD'),
  "<b style='color:#f2686c'>MBCRT</b> = <b style='color:#f0a83c'>ABCD</b> без <b style='color:#5ba8f5'>AMT</b> и <b style='color:#5fd38d'>TDR</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
