import json, sys
from math import sqrt
# Рисунки к Т2′ регионал 2020 №2. Координаты задачи в см (y вверх) при x = AD = 24, CD = 17: A = (0, 0), D = (24, 0).
# G — вершина равнобедренного ADG (AG = DG = 72); DEFG — квадрат наружу вправо, GHIA — прямоугольник наружу влево.
# SVG: X = U(x + 22), Y = U(88 − y).
U = 0.62
def xy(p): return round(U*(p[0]+22), 2), round(U*(88-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

AD, DG, CD = 24, 72, 17
h = sqrt(DG**2 - (AD/2)**2)
A, D, G = (0, 0), (AD, 0), (AD/2, h)
n = (h/DG, (AD/2)/DG)                       # наружу от DG (вправо), длина 1
m = (-h/DG, (AD/2)/DG)                      # наружу от AG (влево), длина 1
PT = {'A':A, 'D':D, 'G':G, 'B':(0,-CD), 'C':(AD,-CD),
      'E':(D[0]+DG*n[0], D[1]+DG*n[1]), 'F':(G[0]+DG*n[0], G[1]+DG*n[1]),
      'I':(A[0]+CD*m[0], A[1]+CD*m[1]), 'H':(G[0]+CD*m[0], G[1]+CD*m[1])}
OFF = {'A':(2.4,-1.4),'D':(-2.4,-1.4),'G':(0.6,-2.0),'B':(-2.6,3.2),'C':(2.6,3.2),
       'E':(3.0,2.0),'F':(2.6,-1.2),'H':(-2.4,-1.4),'I':(-3.0,1.6)}
ALL = ['A','B','C','D','E','F','G','H','I']

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
def mid(a, b): return ((PT[a][0]+PT[b][0])/2, (PT[a][1]+PT[b][1])/2)
def labels(names, col=LAB, dots=True):
    out = ''
    for k in names:
        X, Y = xy(PT[k]); dx, dy = OFF[k]
        out += txt(X+dx, Y+dy+1.2, k, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def svg(inner, label, vb='-3 -4 82 77'):
    return f"<svg viewBox='{vb}' style='max-width:560px' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def T(*k): return [PT[q] for q in k]
SEG = [('H','G'),('G','F'),('F','E'),('E','D'),('D','C'),('C','B'),('B','A'),('A','I'),('I','H'),('A','G'),('D','G'),('A','D')]
def full(col=DIM, w=0.45): return ''.join(line(PT[a], PT[b], col, w) for a, b in SEG)
def names(): return labels(ALL, MUT)
def xmark():   # кирпич x — отрезок AD
    return line(A, D, GOLD, 1.4) + at(mid('A','D'), 'x', 0, 3.6, GOLD, 3.2)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['берём кирпич x = AD.'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x = AD = BC, AG = DG = 3x, CD — неизвестный отрезок, равный GH, AI, AB
s = full() + xmark() + line(PT['B'],PT['C'],GOLD,1.0) + at(mid('B','C'), 'x', 0, 3.6, GOLD, 3.2)
s += line(A, G, GOLD, 1.0) + line(D, G, GOLD, 1.0)
s += at(mid('A','G'), '3x', -3.4, 0, GOLD) + at(mid('D','G'), '3x', 3.6, 0, GOLD)
for a, b, dx, dy in [('G','H',0,-1.6), ('A','I',0,-1.8), ('A','B',-3.8,1.0), ('D','C',4.6,1.0)]:
    s += line(PT[a], PT[b], RED, 1.0) + at(mid(a, b), 'CD', dx, dy, RED, 2.6)
s += names()
V['неизвестный отрезок CD'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = AD; <b style='color:#f2686c'>CD</b> = GH = AI = AB пока неизвестна.")

# 3. а) периметр DEFG — четыре стороны по 3x
s = full() + poly(T('D','E','F','G'), GOLD, 1.2, GOLD, 0.25)
s += at(mid('D','G'), '3x', -3.4, 0) + at(mid('G','F'), '3x', 0, -1.6) + at(mid('F','E'), '3x', 3.6, 0) + at(mid('E','D'), '3x', 0, 3.6)
s += xmark() + names()
V['все четыре стороны DEFG равны DG = 3x.'] = fig(svg(s, 'Квадрат DEFG'), 'а) периметр DEFG: четыре стороны по 3x.')

# 4. б) периметр фигуры — обход по краю; AG, DG, AD внутри
s = full()
for a, b in [('G','F'),('F','E'),('E','D'),('I','H')]: s += line(PT[a], PT[b], GOLD, 1.2)
s += line(PT['C'], PT['B'], BLUE, 1.2)
for a, b in [('H','G'),('D','C'),('B','A'),('A','I')]: s += line(PT[a], PT[b], RED, 1.2)
for a, b in [('A','G'),('D','G'),('A','D')]: s += line(PT[a], PT[b], DIM, 0.6, True)
s += at(mid('G','F'), '3x', 0, -1.6) + at(mid('F','E'), '3x', 3.6, 0) + at(mid('E','D'), '3x', 0, 3.6) + at(mid('I','H'), '3x', -3.6, 0)
s += at(mid('C','B'), 'x', 0, 3.6, BLUE, 3.2)
for a, b, dx, dy in [('G','H',0,-1.6), ('A','I',0,-1.8), ('A','B',-3.8,1.0), ('D','C',4.6,1.0)]:
    s += at(mid(a, b), 'CD', dx, dy, RED, 2.6)
s += names()
V['четыре стороны по CD (GH, CD, AB, AI).'] = fig(svg(s, 'Контур фигуры'),
  "б) периметр фигуры: <b style='color:#f0a83c'>четыре по 3x</b>, <b style='color:#5ba8f5'>одна x</b>, <b style='color:#f2686c'>четыре по CD</b>; пунктир внутри не считаем.")

# 5. раздел «Найдём x»: стороны ADG
s = full() + poly(T('A','D','G'), GOLD, 1.2, GOLD, 0.3)
s += at(mid('A','G'), '3x', -3.4, 0) + at(mid('D','G'), '3x', 3.6, 0) + xmark() + names()
V['стороны ADG — это AD = x'] = fig(svg(s, 'Треугольник ADG'), 'Периметр ADG: x + 3x + 3x.')

# 6. раздел «Найдём CD»: GHIA и ABCD, у обоих сторона CD
s = full() + poly(T('G','H','I','A'), BLUE, 1.0, BLUE, 0.35) + poly(T('A','B','C','D'), GREEN, 1.0, GREEN, 0.4)
s += at(mid('A','G'), '3x', 3.4, 0, BLUE) + at(mid('G','H'), 'CD', 0, -1.6, BLUE, 2.6)
s += at(mid('B','C'), 'x', 0, 3.6, GREEN, 3.2) + at(mid('D','C'), 'CD', 4.6, 1.0, GREEN, 2.6) + names()
V['одна сторона равна CD.'] = fig(svg(s, 'GHIA и ABCD'),
  "<b style='color:#5ba8f5'>GHIA</b>: 3x и CD; <b style='color:#5fd38d'>ABCD</b>: x и CD; вместе 1632.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
