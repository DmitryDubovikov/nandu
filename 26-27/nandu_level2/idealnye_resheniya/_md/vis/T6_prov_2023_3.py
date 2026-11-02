import json, sys, math
# Рисунки к Т6 провинциал 2023 №3: восемь кружков, девять отрезков, три цвета.
# Расположение — как на чертеже условия: шестиугольник 1–6 по часовой стрелке от левого верхнего,
# 7 справа от 2 на той же высоте (соединён с 2 и 3), 8 в центре (соединён только с 4).
RED, BLUE, GREEN, GOLD = '#f2686c', '#5ba8f5', '#5fd38d', '#f0a83c'
INK, DIM, LAB, BG = '#cfdae6', '#4a5866', '#e8eef6', '#0d1117'
COL = {'к': RED, 'с': BLUE, 'з': GREEN}
P = {'1': (26, 8), '2': (57, 8), '7': (89, 8), '6': (10, 35.5), '8': (41.5, 35.5),
     '3': (73, 35.5), '5': (26, 63), '4': (57, 63)}
EDGES = ['12', '23', '34', '45', '56', '61', '27', '37', '48']
HEX = set('123456')
ODD = set('135')
R = 5

def edge(u, v, col, w=0.7):
    (x1, y1), (x2, y2) = P[u], P[v]
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return (f"<line x1='{x1 + ux * R:.2f}' y1='{y1 + uy * R:.2f}' x2='{x2 - ux * R:.2f}' y2='{y2 - uy * R:.2f}' "
            f"stroke='{col}' stroke-width='{w}'/>")

def node(n, paint=None, ring=INK, mark=False):
    # paint: None — не закрашен; 'к' — один цвет; 'сз' — два возможных цвета (половинки); mark — золотое кольцо
    x, y = P[n]; s = ''
    if mark:
        s += f"<circle cx='{x}' cy='{y}' r='{R + 1.6}' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
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

def graph(paint=None, focus=None, gold_edges=(), marks=(), mw=360, aria='Восемь кружков'):
    # focus — какие кружки и отрезки яркие; остальное тусклым (весь чертёж всегда на месте)
    paint = paint or {}; focus = set(focus or P)
    s = ''
    for e in EDGES:
        on = e[0] in focus and e[1] in focus
        s += edge(e[0], e[1], GOLD if e in gold_edges else (INK if on else DIM), 0.9 if e in gold_edges else 0.7)
    for n in P:
        s += node(n, paint.get(n), INK if n in focus else DIM, n in marks)
    st = f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='2 0 95 71' role='img' aria-label='{aria}'{st}>{s}</svg>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

def grid(cells, cap=''):
    c = ''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s, t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>", cap)

def p(**kw): return {k[1:]: v for k, v in kw.items()}   # p(_1='к', _2='с') → {'1': 'к', '2': 'с'}

V = {}
# условие: чертёж с номерами кружков
V['Сколькими различными способами Пабло может закрасить восемь кружков?'] = fig(graph(mw=380),
  'Кружки пронумерованы 1, …, 8.')
# шестиугольник и приклеенные 7, 8
V['а кружки 7 и 8 приклеены к нему сбоку'] = fig(graph(gold_edges=('27', '37', '48'), mw=340, aria='Шестиугольник и кружки 7, 8'),
  f"Шестиугольник 1–6 и <b style='color:{GOLD}'>приклеенные к нему кружки 7 и 8</b>.")
# два примера: кружок 6 зажат между 5 и 1
V['ему два цвета, если 5 и 1 одного цвета'] = grid([
  (graph(p(_1='к', _2='с', _3='к', _4='с', _5='к', _6='сз'), HEX, mw=None), '5 и 1 одного цвета: для кружка 6 два цвета'),
  (graph(p(_1='к', _2='с', _3='з', _4='к', _5='с', _6='з'), HEX, mw=None), '5 и 1 разного цвета: для кружка 6 один цвет'),
], 'Половинки кружка — два возможных цвета.')
# нечётные и чётные
V['Пусть тогда сначала красятся кружки'] = fig(graph(focus=HEX, marks=ODD, mw=300),
  f"<b style='color:{GOLD}'>Нечётные кружки 1, 3, 5</b>; после нечётных каждый чётный зажат.")
# миры по числу цветов у нечётных
V['У каждого чётного кружка соседи одного цвета ⇒ по два цвета.'] = fig(
  graph(p(_1='к', _3='к', _5='к', _2='сз', _4='сз', _6='сз'), HEX, marks=ODD, mw=300), 'Пример: 1, 3 и 5 красные.')
V['Соседи одного цвета только у чётного кружка между двумя нечётными одного цвета'] = fig(
  graph(p(_1='с', _3='к', _5='к', _2='з', _4='сз', _6='з'), HEX, marks=ODD, mw=300), 'Пример: 3 и 5 красные, 1 синий.')
V['У каждого чётного кружка соседи разного цвета ⇒ по одному цвету.'] = fig(
  graph(p(_1='к', _3='с', _5='з', _2='з', _4='к', _6='с'), HEX, marks=ODD, mw=300), 'Пример: 1 красный, 3 синий, 5 зелёный.')
# кружки 7 и 8
V['для кружка 7 остаётся один, третий цвет'] = fig(
  graph(p(_1='к', _2='с', _3='к', _4='с', _5='к', _6='з', _7='з', _8='кз'), gold_edges=('27', '37', '48'), mw=320),
  'Пример: 2 синий, 3 красный, 4 синий.')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
