import json, sys
# Рисунки к Т2″ национал 2015 день I №2. Координаты задачи — в кирпичах x (y вверх):
# A = (0, 0), O = (4, 0), D = (9, 0), E = (9, 6), C = (9, −4), B = (5, −4).  SVG: X = U·x, Y = U·(6 − y).
U = 7
def xy(p): return round(U*p[0], 2), round(U*(6-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'O':(4,0),'D':(9,0),'E':(9,6),'C':(9,-4),'B':(5,-4)}
OFF = {'A':(-3.4,1.2),'O':(-2.4,4.6),'D':(3.4,1.2),'E':(3.2,-1.2),'C':(3.2,3.6),'B':(-1.0,4.8)}
ALL = ['A','O','D','E','C','B']
SEG = [('A','E'),('O','E'),('D','E'),('A','O'),('O','D'),('A','B'),('O','B'),('O','C'),('B','C'),('C','D')]

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
        out += txt(round(X+dx,2), round(Y+dy,2), n, col) + f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def full(col=DIM, w=0.45): return ''.join(line(PT[a], PT[b], col, w) for a, b in SEG)
def names(): return labels(ALL, MUT)
def svg(inner, label, vb='-9 -7 82 84'): return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def fill(pts, col, op=0.4): return poly([PT[n] for n in pts], col, 1.0, col, op)
def outline(pts, col, w=1.1): return poly([PT[n] for n in pts], col, w)
def rangle(p, sx, sy, col=INK, s=0.7):   # прямой угол в вершине p, стороны по направлениям sx, sy
    a, b, c = (p[0]+sx*s, p[1]), (p[0]+sx*s, p[1]+sy*s), (p[0], p[1]+sy*s)
    return f"<polyline points='{'%s,%s' % xy(a)} {'%s,%s' % xy(b)} {'%s,%s' % xy(c)}' fill='none' stroke='{col}' stroke-width='0.4'/>"
def tick(p, vertical, col=GOLD):   # штрих равенства посередине отрезка
    a, b = ((p[0], p[1]-0.35), (p[0], p[1]+0.35)) if vertical else ((p[0]-0.35, p[1]), (p[0]+0.35, p[1]))
    return line(a, b, col, 0.6)
def ticks(col=GOLD): return tick((2,0), True, col) + tick((7,-4), True, col) + tick((9,-2), False, col)

V = {}
# 1. рисунок условия
V['Чему равна площадь BCEO?'] = fig(svg(full(INK, 0.55) + labels(ALL), 'Рисунок условия'), 'Рисунок из условия.')

# 2. посылки: прямые углы при D и C, AO = BC = CD
s = full(INK, 0.5) + rangle(PT['D'], -1, 1, GOLD) + rangle(PT['D'], -1, -1, GOLD) + rangle(PT['C'], -1, 1, GOLD)
s += line(PT['A'],PT['O'],GOLD,1.0) + line(PT['B'],PT['C'],GOLD,1.0) + line(PT['C'],PT['D'],GOLD,1.0) + ticks() + labels(ALL)
V['ABCD и OBCD — трапеции с высотой CD'] = fig(svg(s, 'Прямые углы и равные отрезки'),
  "Углы при C и D прямые; <b style='color:#f0a83c'>AO = BC = CD</b>.")

# 3–6. артефакт: каждое спрошенное
s = full() + fill(['C','D','O'], BLUE) + fill(['O','D','E'], GREEN) + line(PT['O'],PT['D'],GOLD,1.1) + names()
V['OD делит CEO на прямоугольные'] = fig(svg(s, 'CEO = CDO + ODE'),
  "<b style='color:#5ba8f5'>CDO</b> и <b style='color:#5fd38d'>ODE</b>.")
s = full() + fill(['A','D','E'], GOLD, 0.4) + rangle(PT['D'], -1, 1, LAB) + names()
V['ADE — прямоугольный треугольник с катетами'] = fig(svg(s, 'ADE'), '')
s = full() + fill(['A','B','C','D'], GOLD, 0.4) + line(PT['C'],PT['D'],LAB,1.1) + names()
V['ABCD — трапеция с основаниями'] = fig(svg(s, 'ABCD'), '')
s = full() + fill(['O','B','C','D'], BLUE) + fill(['O','D','E'], GREEN) + line(PT['O'],PT['D'],GOLD,1.1) + names()
V['OD делит BCEO на трапецию'] = fig(svg(s, 'BCEO = OBCD + ODE'),
  "<b style='color:#5ba8f5'>OBCD</b> и <b style='color:#5fd38d'>ODE</b>.")

# 7. раздел 1: AOB = ABCD без OBCD
s = full() + fill(['O','B','C','D'], BLUE, 0.3) + fill(['A','B','O'], RED, 0.5) + outline(['A','B','C','D'], GOLD) + names()
V['это трапеция ABCD без трапеции OBCD'] = fig(svg(s, 'AOB = ABCD без OBCD'),
  "<b style='color:#f2686c'>AOB</b> = <b style='color:#f0a83c'>ABCD</b> без <b style='color:#5ba8f5'>OBCD</b>; у трапеций общая высота CD.")

# 8. раздел 2: AOE = ADE без ODE
s = full() + fill(['O','D','E'], GREEN, 0.3) + fill(['A','O','E'], RED, 0.5) + outline(['A','D','E'], GOLD) + names()
V['это прямоугольный треугольник ADE без'] = fig(svg(s, 'AOE = ADE без ODE'),
  "<b style='color:#f2686c'>AOE</b> = <b style='color:#f0a83c'>ADE</b> без <b style='color:#5fd38d'>ODE</b>; у треугольников общий катет DE.")

# 9. раздел 3: длины в кирпичах x на сетке
g = ''.join(line((i,-4),(i,6),'#3e4b58',0.3) for i in range(0,10)) + ''.join(line((0,j),(9,j),'#3e4b58',0.3) for j in range(-4,7))
s = g + full(INK, 0.5)
s += line((3,0),(4,0),GOLD,1.6) + at((3.5,0), 'x', 0, -1.6, GOLD, 3.2)
s += at((1.5,0), '4x', 0, -1.6) + at((6.5,0), '5x', 0, -1.6) + at((9,3), '6x', 4.4, 1.0)
s += at((9,-2), '4x', 4.4, 1.0) + at((7,-4), '4x', 0, 4.6) + labels(ALL)
V['В кирпичах: AO = BC = CD = 4x'] = fig(svg(s, 'Длины в кирпичах x', '-9 -7 82 86'),
  "<b style='color:#f0a83c'>x</b> = AO : 4; все точки — в узлах сетки с шагом x.")

# 10–13. схема-стрелки (North Star): данное → искомое, номер стрелки = номер раздела
ROWS = [('S(CDO) = 5/4 · S(AOB)', 'OD через AO'), ('S(AOE) = 3/2 · S(AOB)', 'DE через AO'), ('S(ODE) = 735', 'длина AO')]
def scheme(hi=None):
    out = ''
    for i, (l, r) in enumerate(ROWS):
        y = 2 + 13*i; on = hi is None or hi == i
        col = GOLD if (hi == i) else (INK if on else DIM); tc = LAB if on else MUT
        out += f"<rect x='2' y='{y}' width='52' height='9' rx='1.6' fill='none' stroke='{col}' stroke-width='{0.8 if hi == i else 0.5}'/>"
        out += txt(28, y+6.1, l, tc, 3.3)
        out += f"<rect x='72' y='{y}' width='36' height='9' rx='1.6' fill='none' stroke='{col}' stroke-width='{0.8 if hi == i else 0.5}'/>"
        out += txt(90, y+6.1, r, tc, 3.3)
        out += f"<line x1='55' y1='{y+4.5}' x2='70' y2='{y+4.5}' stroke='{col}' stroke-width='{0.8 if hi == i else 0.5}'/>"
        out += f"<polygon points='70.6,{y+4.5} 68,{y+3.2} 68,{y+5.8}' fill='{col}'/>"
        out += f"<circle cx='62.5' cy='{y+4.5}' r='2.6' fill='#121821' stroke='{col}' stroke-width='0.5'/>" + txt(62.5, y+5.7, str(i+1), col, 3.0)
    return f"<svg viewBox='0 0 110 39' role='img' aria-label='Порядок разделов'>{out}</svg>"
V['сначала выразим OD и DE через AO'] = fig(scheme(), 'Слева — данное, справа — что оно даёт; номер стрелки — номер раздела.')
V['1. Выразим OD через AO.'] = fig(scheme(0), '')
V['2. Выразим DE через AO.'] = fig(scheme(1), '')
V['3. Найдём длину AO.'] = fig(scheme(2), '')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
