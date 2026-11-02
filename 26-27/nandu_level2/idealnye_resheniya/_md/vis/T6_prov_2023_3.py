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
R = 5

def edge(u, v, col, w=0.7):
    (x1, y1), (x2, y2) = P[u], P[v]
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return (f"<line x1='{x1 + ux * R:.2f}' y1='{y1 + uy * R:.2f}' x2='{x2 - ux * R:.2f}' y2='{y2 - uy * R:.2f}' "
            f"stroke='{col}' stroke-width='{w}'/>")

def node(n, paint=None, ring=INK):
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

def graph(paint=None, focus=None, gold_edges=(), mw=360, aria='Восемь кружков'):
    # focus — какие кружки и отрезки яркие; остальное тусклым (весь чертёж всегда на месте)
    paint = paint or {}; focus = set(focus or P)
    s = ''
    for e in EDGES:
        on = e[0] in focus and e[1] in focus
        s += edge(e[0], e[1], GOLD if e in gold_edges else (INK if on else DIM), 0.9 if e in gold_edges else 0.7)
    for n in P:
        s += node(n, paint.get(n), INK if n in focus else DIM)
    return f"<svg viewBox='3 1 93 69' role='img' aria-label='{aria}' style='max-width:{mw}px'>{s}</svg>"

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
# два примера: F зажат между E и A
V['посмотрим на F, который соединён и с E, и с A'] = grid([
  (graph(p(A='к', B='с', C='к', D='с', E='к', F='сз'), HEX, mw=None), 'E и A одного цвета: для F два цвета'),
  (graph(p(A='к', B='с', C='з', D='к', E='с', F='з'), HEX, mw=None), 'E и A разного цвета: для F один цвет'),
], 'Половинки кружка — два возможных цвета.')
# миры по числу цветов у A, C, E
V['У каждого из B, D, F соседи одного цвета ⇒ по два цвета.'] = fig(
  graph(p(A='к', C='к', E='к', B='сз', D='сз', F='сз'), HEX, mw=300), 'Пример: A, C, E красные.')
V['ровно один стоит между кружками пары'] = fig(
  graph(p(A='с', C='к', E='к', B='з', D='сз', F='з'), HEX, mw=300), 'Пример: одиночка A синий, пара C, E красная.')
V['У каждого из B, D, F соседи разного цвета ⇒ по одному цвету.'] = fig(
  graph(p(A='к', C='с', E='з', B='з', D='к', F='с'), HEX, mw=300), 'Пример: A красный, C синий, E зелёный.')
# G и H
V['для G остаётся один, третий цвет'] = fig(
  graph(p(A='к', B='с', C='к', D='с', E='к', F='з', G='з', H='кз'), gold_edges=('BG', 'CG', 'DH'), mw=320),
  'Пример: B синий, C красный, D синий.')
for k in V:
    V[k] = V[k].replace(" style='max-width:Nonepx'", '')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
