import json, sys, math
# Рисунки к Т6 провинциал 2023 №3: восемь кружков, девять отрезков, три цвета.
# Расположение — как на чертеже условия: шестиугольник A–F по часовой стрелке от левого верхнего,
# G справа от B на той же высоте, H в центре (соединён только с D).
RED, BLUE, GREEN, GOLD = '#f2686c', '#5ba8f5', '#5fd38d', '#f0a83c'
INK, DIM, LAB, BG = '#cfdae6', '#4a5866', '#e8eef6', '#0d1117'
COL = {'к': RED, 'с': BLUE, 'з': GREEN}
P = {'A': (26, 8), 'B': (57, 8), 'G': (89, 8), 'F': (10, 35.5), 'H': (41.5, 35.5),
     'C': (73, 35.5), 'E': (26, 63), 'D': (57, 63)}
EDGES = ['AB', 'BC', 'CD', 'DE', 'EF', 'FA', 'BG', 'CG', 'DH']
HEX = set('ABCDEF')
# перерисовка: углы A, C, E — треугольник, B, D, F — середины сторон; G у B и C, H у D (тусклые)
TRI = {'A': (50, 6), 'B': (67, 34), 'C': (84, 62), 'D': (50, 62), 'E': (16, 62), 'F': (33, 34),
       'G': (91, 34), 'H': (50, 45)}
R = 5

def edge(u, v, col, w=0.7, P=P):
    (x1, y1), (x2, y2) = P[u], P[v]
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return (f"<line x1='{x1 + ux * R:.2f}' y1='{y1 + uy * R:.2f}' x2='{x2 - ux * R:.2f}' y2='{y2 - uy * R:.2f}' "
            f"stroke='{col}' stroke-width='{w}'/>")

def node(n, paint=None, ring=INK, P=P):
    # paint: None — не закрашен; 'к' — один цвет; 'сз' — два возможных цвета (половинки)
    x, y = P[n]; s = ''
    if paint and len(paint) == 2:
        a, b = COL[paint[0]], COL[paint[1]]
        s += f"<path d='M{x} {y - R} A {R} {R} 0 0 0 {x} {y + R} Z' fill='{a}'/>"
        s += f"<path d='M{x} {y - R} A {R} {R} 0 0 1 {x} {y + R} Z' fill='{b}'/>"
        s += f"<circle cx='{x}' cy='{y}' r='{R}' fill='none' stroke='{ring}' stroke-width='0.6'/>"
        tc = BG
    elif paint:
        s += f"<circle cx='{x}' cy='{y}' r='{R}' fill='{COL[paint]}' stroke='{ring}' stroke-width='0.6'/>"
        tc = BG
    else:
        s += f"<circle cx='{x}' cy='{y}' r='{R}' fill='none' stroke='{ring}' stroke-width='0.7'/>"
        tc = ring if ring != INK else LAB
    s += f"<text x='{x}' y='{y + 1.7}' fill='{tc}' font-size='4.6' text-anchor='middle' font-weight='700'>{n}</text>"
    return s

def graph(paint=None, focus=None, gold_edges=(), mw=360, aria='Восемь кружков', P=P, vb='3 1 93 69'):
    # focus — какие кружки и отрезки яркие; остальное тусклым (весь чертёж всегда на месте)
    paint = paint or {}; focus = set(focus or P)
    s = ''
    for e in EDGES:
        on = e[0] in focus and e[1] in focus
        s += edge(e[0], e[1], GOLD if e in gold_edges else (INK if on else DIM), 0.9 if e in gold_edges else 0.7, P=P)
    for n in P:
        s += node(n, paint.get(n), INK if n in focus else DIM, P=P)
    return f"<svg viewBox='{vb}' role='img' aria-label='{aria}' style='max-width:{mw}px'>{s}</svg>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

def grid(cells, cap=''):
    c = ''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s, t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>", cap)

def p(**kw): return kw

V = {}
# условие: чертёж с буквами решения
V['Сколькими различными способами Пабло может закрасить восемь кружков?'] = fig(graph(mw=380),
  'Кружки названы буквами A, …, H.')
# шестиугольник и приклеенные G, H
V['а G и H приклеены к нему сбоку'] = fig(graph(gold_edges=('BG', 'CG', 'DH'), mw=340, aria='Шестиугольник и G, H'),
  f"Шестиугольник A–F и <b style='color:{GOLD}'>приклеенные к нему G и H</b>.")
def tri(paint=None, mw=300):
    return graph(paint, HEX, mw=mw, P=TRI, vb='8 0 90 68', aria='Треугольник ACE')
# перерисовка шестиугольника в треугольник
V['Перерисуем шестиугольник'] = grid([
  (graph(focus=HEX, mw=None), 'как на рисунке условия'),
  (tri(mw=None), 'углы A, C, E, середины сторон B, D, F'),
], 'Перерисовка: те же кружки и те же отрезки.')
# два примера для середины F стороны EA
V['Выпишем два примера для середины F стороны EA'] = grid([
  (tri(p(A='к', B='с', C='к', D='с', E='к', F='сз'), mw=None), 'E и A одного цвета: для F два цвета'),
  (tri(p(A='к', B='с', C='з', D='к', E='с', F='з'), mw=None), 'E и A разного цвета: для F один цвет'),
], 'Половинки кружка — два возможных цвета.')
# миры по числу цветов у углов
V['Концы каждой стороны одного цвета ⇒ у B, D, F по два цвета.'] = fig(
  tri(p(A='к', C='к', E='к', B='сз', D='сз', F='сз')), 'Пример: A, C, E красные.')
V['Концы одного цвета только у стороны между двумя углами одного цвета'] = fig(
  tri(p(A='с', C='к', E='к', B='з', D='сз', F='з')), 'Пример: C, E красные, A синий.')
V['Концы каждой стороны разного цвета ⇒ у B, D, F по одному цвету.'] = fig(
  tri(p(A='к', C='с', E='з', B='з', D='к', F='с')), 'Пример: A красный, C синий, E зелёный.')
# G и H
V['для G остаётся один, третий цвет'] = fig(
  graph(p(A='к', B='с', C='к', D='с', E='к', F='з', G='з', H='кз'), gold_edges=('BG', 'CG', 'DH'), mw=320),
  'Пример: B синий, C красный, D синий.')
for k in V:
    V[k] = V[k].replace(" style='max-width:Nonepx'", '')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
