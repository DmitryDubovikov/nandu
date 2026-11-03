import json, sys
# Рисунки к Т2‴ провинциал 2013 №2. Координаты — (столбец, ряд) точек сетки, ряд 0 сверху; сетка 8 × 7 точек, 7 × 6 клеток.
# SVG: X = 8 · столбец, Y = 8 · ряд.
U = 8
def xy(p): return round(U*p[0], 2), round(U*p[1], 2)
GOLD,BLUE,GREEN,RED,VIO,TEAL='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9','#4fd1c5'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

FIG = [(5,0),(0,1),(0,2),(1,2),(1,3),(2,2),(0,6),(3,1),(4,5),(5,4),(4,1),(7,6),(6,3),(7,2),(6,1),(6,0)]
K = {1: [(0,0),(5,0),(0,1)], 2: [(6,0),(7,0),(7,2),(6,1)], 3: [(7,2),(7,6),(6,3)],
     4: [(0,6),(3,1),(4,5),(5,4),(4,1),(7,6)], 5: [(0,2),(1,2),(1,3),(2,2),(0,6)]}
KCOL = {1: GOLD, 2: GREEN, 3: VIO, 4: BLUE, 5: TEAL}
KNUM = {1: (1.45,0.36), 2: (6.5,0.62), 3: (6.68,3.9), 4: (2.5,5.2), 5: (0.5,3.5)}
TRAP = [(0,6),(3,1),(4,1),(7,6)]
FANG = [(3,1),(4,5),(5,4),(4,1)]
RECT = [(0,0),(7,0),(7,6),(0,6)]

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.4 1.1'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.0):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def lab(p, s, dx=0, dy=0, col=GOLD, size=2.8):
    X, Y = xy(p); return txt(round(X+dx,2), round(Y+dy,2), s, col, size)
def dots(col=INK, r=0.6):
    return ''.join(f"<circle cx='{U*i}' cy='{U*j}' r='{r}' fill='{col}'/>" for i in range(8) for j in range(7))
def grid(col='#3e4b58', w=0.3):
    return ''.join(line((i,0),(i,6),col,w) for i in range(8)) + ''.join(line((0,j),(7,j),col,w) for j in range(7))
def figure(col=DIM, w=0.6, fill='none', op=1):
    return poly(FIG, col, w, fill, op)
def base():     # весь чертёж условия тусклым: сетка, точки, фигура
    return grid() + dots(MUT, 0.45) + figure(INK, 0.6)
def num(k, col=None):
    X, Y = xy(KNUM[k]); col = col or KCOL[k]
    return f"<circle cx='{X}' cy='{Y}' r='2.1' fill='#0e1116' stroke='{col}' stroke-width='0.5'/>" + txt(X, Y+1.0, str(k), LAB, 2.7)
def xmark(s='x'):  # сторона одной клетки сверху слева
    return line((0,0),(1,0),GOLD,1.4) + lab((0.5,0), s, 0, -1.6, GOLD, 3.0)
def svg(inner, label, vb='-7 -7 70 62'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"

V = {}
# 1. рисунок условия — точки и фигура, как в оригинале
V['в а) и б) одна и та же фигура, меняется только сторона клетки'] = fig(
    svg(dots(INK, 0.7) + figure('#7f95ff', 0.8), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x — сторона клетки
s = grid() + dots(MUT, 0.45) + figure(DIM, 0.6) + xmark()
V['x — сторона клетки.'] = fig(svg(s, 'Буквы'), "<b style='color:#f0a83c'>x</b> — сторона клетки.")

# 3–4. прямоугольник 7 × 6 клеток без пяти кусков
def artefakt(xs):
    s = grid() + dots(MUT, 0.45)
    s += ''.join(poly(K[k], DIM, 0.5, DIM, 0.35) for k in K)
    s += figure(BLUE, 0.8, BLUE, 0.45) + poly(RECT, GOLD, 1.0)
    s += lab((3.5,6), '7x', 0, 4.4, GOLD, 3.2) + lab((7,3), '6x', 4.4, 1.0, GOLD, 3.2) + xmark(xs)
    return s
V['у фигуры нет готовой формулы площади'] = fig(svg(artefakt('x = 1 см'), 'Фигура в прямоугольнике, x = 1 см', '-7 -9 72 66'),
    'а) площадь фигуры при x = 1 см')
V['при x = 2 см фигура — тоже прямоугольник'] = fig(svg(artefakt('x = 2 см'), 'Фигура в прямоугольнике, x = 2 см', '-7 -9 72 66'),
    'б) площадь фигуры при x = 2 см')

# 5. раздел 1: пять кусков разными цветами
s = grid() + dots(MUT, 0.45) + ''.join(poly(K[k], KCOL[k], 0.7, KCOL[k], 0.45) for k in K)
s += figure(INK, 0.7) + poly(RECT, GOLD, 0.9, 'none') + ''.join(num(k) for k in K)
V['закрасим куски разными цветами'] = fig(svg(s, 'Пять кусков снаружи фигуры'), 'Пять кусков снаружи фигуры.')

# 6. кусок 1
s = base() + poly(K[1], GOLD, 0.9, GOLD, 0.5) + lab((2.5,0), '5x', 0, -1.6) + lab((0,0.5), 'x', -2.2, 1.0)
V['Кусок 1 — прямоугольный треугольник с катетами 5x и x.'] = fig(svg(s, 'Кусок 1'), 'Кусок 1.')
# 7. кусок 2
s = base() + poly([(6,0),(7,0),(7,1),(6,1)], GREEN, 0.9, GREEN, 0.5) + poly([(6,1),(7,1),(7,2)], GOLD, 0.9, GOLD, 0.5)
s += lab((6.5,0), 'x', 0, -1.6, GREEN) + lab((7,1.5), 'x', 2.2, 1.0) + lab((7,0.5), 'x', 2.2, 1.0, GREEN)
V['Кусок 2 — квадрат со стороной x'] = fig(svg(s, 'Кусок 2'),
    "Кусок 2: <b style='color:#5fd38d'>квадрат</b> и <b style='color:#f0a83c'>треугольник</b>.")
# 8. кусок 3
s = base() + poly([(7,2),(7,3),(6,3)], GOLD, 0.9, GOLD, 0.5) + poly([(6,3),(7,3),(7,6)], VIO, 0.9, VIO, 0.5)
s += lab((7,2.5), 'x', 2.2, 1.0) + lab((7,4.5), '3x', 2.8, 1.0, VIO) + lab((6.5,3), 'x', 0.6, -0.8)
V['Линия сетки режет кусок 3'] = fig(svg(s, 'Кусок 3'),
    "Кусок 3: треугольники с катетами <b style='color:#f0a83c'>x и x</b> и <b style='color:#c58af9'>3x и x</b>.")
# 9. кусок 4: трапеция
s = base() + poly([(0,6),(3,1),(3,6)], GOLD, 0.9, GOLD, 0.45) + poly([(3,1),(4,1),(4,6),(3,6)], GREEN, 0.9, GREEN, 0.45)
s += poly([(4,1),(7,6),(4,6)], GOLD, 0.9, GOLD, 0.45) + poly(FANG, RED, 0.7, 'none', 1)
s += lab((1.5,6), '3x', 0, 4.0) + lab((3.5,6), 'x', 0, 4.0, GREEN) + lab((5.5,6), '3x', 0, 4.0) + lab((3,3.6), '5x', -2.6, 1.0)
V['Линии сетки режут трапецию'] = fig(svg(s, 'Трапеция', '-7 -7 70 64'),
    "Трапеция: два <b style='color:#f0a83c'>треугольника</b> и <b style='color:#5fd38d'>прямоугольник</b>; <b style='color:#f2686c'>выступ</b> фигуры вдаётся в трапецию.")
# 10. кусок 4: выступ
s = base() + poly([(3,1),(4,1),(4,5)], GOLD, 0.9, GOLD, 0.55) + poly([(4,1),(4,4),(5,4)], BLUE, 0.9, BLUE, 0.55)
s += poly([(4,4),(4,5),(5,4)], GREEN, 0.9, GREEN, 0.55)
s += lab((3.5,1), 'x', 0, -1.2) + lab((3.2,3.2), '4x', -2.2, 1.0) + lab((4.5,4), 'x', 0.4, -1.0, BLUE)
V['Линии сетки режут выступ'] = fig(svg(s, 'Выступ'),
    "Выступ: треугольники с катетами <b style='color:#f0a83c'>x и 4x</b>, <b style='color:#5ba8f5'>3x и x</b>, <b style='color:#5fd38d'>x и x</b>.")
# 11. кусок 5
s = base() + poly([(0,2),(2,2),(0,6)], GOLD, 0.9, GOLD, 0.45) + poly([(1,2),(2,2),(1,3)], RED, 0.9, '#0e1116', 0.85)
s += lab((1,2), '2x', -3.2, -1.0) + lab((0,4), '4x', -3.0, 1.0)
V['кусок 5 — треугольник с катетами 2x и 4x'] = fig(svg(s, 'Кусок 5'),
    "Кусок 5: <b style='color:#f0a83c'>треугольник</b> без <b style='color:#f2686c'>ступеньки</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
