import json, sys
# Рисунки к Т2′ национал 2021 день II №5. Координаты задачи — в клетках d (y вверх), A = (0, 0), C = (6, 4), E = (−3, 4), F = (6, −1).
# SVG: X = U(x + 3), Y = U(4 − y).
U = 8
def xy(p): return U*(p[0]+3), U*(4-p[1])
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(6,0),'C':(6,4),'D':(0,4),'M':(3,0),'N':(6,2),'P':(3,4),'R':(0,2),'E':(-3,4),'F':(6,-1)}
OFF = {'A':(-3.2,4.6),'B':(3.4,3.4),'C':(3.2,-1.6),'D':(0,-2.4),'M':(0,-2.0),'N':(3.6,1.2),'P':(0,-2.4),
       'R':(-3.4,1.2),'E':(-3.2,-1.6),'F':(3.4,3.0)}

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
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.3):   # сетка с шагом d: прямоугольник ABCD и полоса до E
    s = ''.join(line((x,0),(x,4),col,w) for x in range(-3,7))
    return s + ''.join(line((-3 if y > 0 else 0, y),(6,y),col,w) for y in range(0,5))
def svg(inner, label, vb='-9 -7 90 54'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def dmark():   # кирпич d — четверть BC, у B
    return line((6,0),(6,1),GOLD,1.4) + at((6,0.5), 'x', 3.0, 1.0, GOLD, 3.2)
def frame(col=DIM, w=0.5):   # отрезки чертежа условия без F
    P_ = PT
    return (line(P_['E'],P_['C'],col,w) + line(P_['C'],P_['B'],col,w) + line(P_['A'],P_['B'],col,w) +
            line(P_['A'],P_['D'],col,w) + line(P_['A'],P_['E'],col,w) + line(P_['R'],P_['P'],col,w) + line(P_['P'],P_['B'],col,w))
ALL = ['A','B','C','D','M','N','P','R','E','F']
def dimAB():   # размер AB = 6d — выноской ниже F, чтобы не пересекать AF
    return (line((0,-1.8),(6,-1.8),GOLD,0.5) + line((0,-1.6),(0,-2.0),GOLD,0.5) + line((6,-1.6),(6,-2.0),GOLD,0.5)
            + at((3,-1.8), '6x', 0, 4.4))
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    return frame(col, w) + line(PT['B'],PT['F'],col,w) + line(PT['A'],PT['F'],col,w)
def names(): return labels(ALL, MUT)

V = {}
# 1. рисунок условия
s = poly([PT['A'],PT['B'],PT['P'],PT['R']], '#c87a55', 0.7, '#c87a55', 0.25) + full(INK, 0.55) + labels(ALL)
V['Чему равна площадь AMNE?'] = fig(svg(s, 'Рисунок условия', '-9 -7 90 58'), 'Рисунок из условия.')

# 2. буквы: сетка, d — четверть BC
s = grid() + full() + dmark()
s += line((0,0),(6,0),GOLD,1.0) + dimAB()
s += line((6,0),(6,4),GOLD,1.0) + at((6,3.1), '4x', 4.6, 1.0, GOLD, 3.2)
s += names()
V['сетка с шагом x.'] = fig(svg(s, 'Буквы', '-9 -7 90 66'), "<b style='color:#f0a83c'>x</b> = BC : 4; все точки, кроме F, — в узлах сетки.")

# 3–5. артефакт: каждое спрошенное на сетке d
G = grid() + full()
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
# а) ADE: катеты AD = 4d, DE = 3d
s = G + tri([PT['A'],PT['D'],PT['E']], GOLD) + at((0,1.1), '4x', 3.6, 1.0) + at((-1.5,4), '3x', 0, -1.8) + dmark()
s += names()
V['а) площадь ADE'] = fig(svg(s, 'ADE на сетке'), '')
# б) ABCE: три стороны по сетке, AE = CF
s = G + line(PT['A'],PT['B'],GOLD,1.2) + line(PT['B'],PT['C'],GOLD,1.2) + line(PT['C'],PT['E'],GOLD,1.2)
s += line(PT['E'],PT['A'],RED,1.2,True)
s += dimAB() + at((6,3.1), '4x', 4.6, 1.0) + at((1.5,4), '9x', 0, -1.8) + at((-1.6,2), 'AE = CF', -7.5, 1.0, RED, 3.0)
s += dmark() + names()
V['б) периметр ABCE'] = fig(svg(s, 'Контур ABCE на сетке', '-9 -7 90 66'), '')
# в) AMNE = трапеция ABCE без MBN и NCE
s = G + poly([PT['A'],PT['B'],PT['C'],PT['E']], GOLD, 1.0)
s += poly([PT['A'],PT['M'],PT['N'],PT['E']], VIO, 1.0, VIO, 0.35)
s += tri([PT['M'],PT['B'],PT['N']], BLUE, 0.35) + tri([PT['N'],PT['C'],PT['E']], GREEN, 0.35)
s += dimAB() + at((4.5,0), '3x', 0, 4.4, BLUE) + at((6,1.3), '2x', 4.4, 1.0, BLUE)
s += at((6,3), '2x', 4.4, 1.0, GREEN) + at((1.5,4), '9x', 0, -1.8, GREEN) + at((-3,2), '4x', -4.0, 1.0)
s += line((-3,4),(-3,0),GOLD,0.6,True) + line((-3,0),(0,0),GOLD,0.6,True)
s += line((6,0),(6,1),GOLD,1.4) + at((6,0.5), 'x', -2.6, 1.0, GOLD, 3.2) + names()
V['в) площадь AMNE'] = fig(svg(s, 'AMNE на сетке', '-9 -7 90 66'),
  "<b style='color:#f0a83c'>Трапеция ABCE</b> без <b style='color:#5ba8f5'>MBN</b> и <b style='color:#5fd38d'>NCE</b>; высота трапеции 4x.")

# 6. раздел «Найдём d»: ABPR = ABCD без BCP и PDR
s = grid() + full() + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 1.0)
s += poly([PT['A'],PT['B'],PT['P'],PT['R']], RED, 0.8, RED, 0.35)
s += tri([PT['B'],PT['C'],PT['P']], BLUE, 0.35) + tri([PT['P'],PT['D'],PT['R']], GREEN, 0.35)
s += at((6,3.1), '4x', 4.4, 1.0, BLUE) + at((4.5,4), '3x', 0, -1.8, BLUE)
s += at((1.5,4), '3x', 0, -1.8, GREEN) + at((0,3), '2x', -4.2, 1.0, GREEN) + dmark()
s += names()
V['ABPR — это прямоугольник ABCD без'] = fig(svg(s, 'ABPR внутри ABCD', '-9 -7 90 58'),
  "<b style='color:#f2686c'>ABPR</b> = <b style='color:#f0a83c'>ABCD</b> без <b style='color:#5ba8f5'>BCP</b> и <b style='color:#5fd38d'>PDR</b>.")

# 7. раздел «Найдём CF»: CAF = ABC + BAF, общий катет AB
s = grid() + full() + tri([PT['A'],PT['B'],PT['C']], GOLD, 0.35) + tri([PT['A'],PT['B'],PT['F']], BLUE, 0.55)
s += dimAB() + at((6,3.1), '4x', 4.4, 1.0, GOLD) + at((6,-0.5), 'BF', -4.0, 1.2, BLUE, 2.8)
s += names()
V['Заметим, что CAF разбивается'] = fig(svg(s, 'CAF = ABC + BAF', '-9 -7 90 66'),
  "<b style='color:#f0a83c'>ABC</b> и <b style='color:#5ba8f5'>BAF</b> вместе — CAF; катет AB у них общий.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
