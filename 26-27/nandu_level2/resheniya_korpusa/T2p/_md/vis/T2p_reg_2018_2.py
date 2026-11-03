import json, sys, math
# Рисунки к Т2′ регионал 2018 №2. Координаты задачи — в кирпичах x (y вверх), A = (0, 0), C = (5, 0), E = (5, 6), F = (0, 6), B = (2, 0),
# D = (5 + 3√3, 3) — вершина равностороннего CDE. SVG: X = U · x, Y = U · (6 − y).
U = 8
def xy(p): return round(U*p[0], 2), round(U*(6-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(2,0),'C':(5,0),'D':(5+3*math.sqrt(3),3),'E':(5,6),'F':(0,6)}
OFF = {'A':(-3.2,3.4),'B':(0,4.4),'C':(3.2,3.4),'D':(3.6,1.2),'E':(3.2,-1.6),'F':(-3.2,-1.6)}
SEGS = [('F','A'),('A','C'),('C','E'),('E','F'),('F','B'),('B','E'),('E','D'),('D','C')]

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{round(x,2)}' y='{round(y,2)}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=3.0):
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
def labels(col=LAB, dots=True):
    out = ''
    for n in PT:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри ACEF
    s = ''.join(line((i,0),(i,6),col,w) for i in range(0,6))
    return s + ''.join(line((0,j),(5,j),col,w) for j in range(0,7))
def full(col=DIM, w=0.45): return ''.join(line(PT[a],PT[b],col,w) for a, b in SEGS)
def names(): return labels(MUT)
def svg(inner, label, vb='-8 -6 100 62', mw='480px'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x — половина AB, у A
    return line((0,0),(1,0),GOLD,1.4) + at((0.5,0), 'x', 0, 4.4, GOLD, 3.2)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels()
V['AB : AC : AF = 2 : 5 : 6.'] = fig(svg(s, 'Рисунок условия', mw='560px'), 'Рисунок из условия.')

# 2. буквы: сетка, x — половина AB
s = grid() + full() + xmark()
s += line((0,0),(0,6),GOLD,1.0) + at((0,3), '6x', -4.4, 1.0)
s += line((1,0),(2,0),GOLD,1.0) + at((1,0.5), '2x', 0, 1.0, GOLD, 3.0)
s += names()
V['сетка с шагом x.'] = fig(svg(s, 'Буквы', mw='560px'), "<b style='color:#f0a83c'>x</b> = AB : 2; все точки, кроме D, — в узлах сетки.")

G = grid() + full()
# а) CDE: три стороны по CE = 6x
s = G + tri([PT['C'],PT['D'],PT['E']], GOLD, 0.4)
s += at((5,3), '6x', 4.2, 1.0) + at(((5+PT['D'][0])/2, 4.5), '6x', 2.4, -1.4) + at(((5+PT['D'][0])/2, 1.5), '6x', 2.4, 3.4)
s += xmark() + names()
V['все три стороны CDE равны CE = 6x.'] = fig(svg(s, 'CDE на сетке'), 'а) периметр CDE: три стороны по 6x.')
# б) BCEF = ACEF без ABF
s = G + tri([PT['B'],PT['C'],PT['E'],PT['F']], VIO, 0.4) + tri([PT['A'],PT['B'],PT['F']], RED, 0.4)
s += poly([PT['A'],PT['C'],PT['E'],PT['F']], GOLD, 1.2)
s += at((0.7,2), '294', 0, 1.0, LAB, 3.0) + at((2.5,6), '5x', 0, -1.8) + at((0,3), '6x', -4.4, 1.0)
s += xmark() + names()
V['а площадь ABF дана.'] = fig(svg(s, 'BCEF внутри ACEF'),
  "б) площадь BCEF: <b style='color:#f0a83c'>ACEF</b> 5x × 6x без <b style='color:#f2686c'>ABF</b> = 294.")
# в) BEF: основание FE = 5x, высота AF = 6x
s = G + tri([PT['B'],PT['E'],PT['F']], BLUE, 0.4)
s += line((2,0),(2,6),GOLD,0.8,True) + line(PT['A'],PT['F'],GOLD,1.0)
s += at((2.5,6), '5x', 0, -1.8, BLUE) + at((0,3), '6x', -4.4, 1.0) + at((2,3.2), '6x', 3.2, 1.0, GOLD, 2.8)
s += xmark() + names()
V['высота из B равна AF = 6x.'] = fig(svg(s, 'BEF на сетке'),
  "в) площадь BEF: основание FE = 5x, высота — пунктир от B до FE, равна AF = 6x.")

# 4. раздел «Найдём x»: ABF — катеты AB = 2x, AF = 6x
s = grid() + full() + tri([PT['A'],PT['B'],PT['F']], RED, 0.45)
s += at((1,0), '2x', 0, 4.4, RED) + at((0,3), '6x', -4.4, 1.0, RED)
s += names()
V['Заметим, что ABF — прямоугольный треугольник'] = fig(svg(s, 'ABF на сетке'), 'S(ABF) = 294: катеты 2x и 6x.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
