import json, sys, math
# Рисунки к Т6 национал 2022 №6: кузнечик на полоске 1 × 9, прыжки на 3 и на 5 клеток.
# Карта прыжков: клетки 4, 7, 2, 5, 8, 3, 6, 1 по кругу (1 сверху, по часовой стрелке),
# 9 — внутри, зеркально к 1 относительно линии 4–6: клетки 1 и 9 обе соединены только с 4 и 6.
RED, BLUE, GREEN, GOLD = '#f2686c', '#5ba8f5', '#5fd38d', '#f0a83c'
INK, DIM, LAB, BG = '#cfdae6', '#4a5866', '#e8eef6', '#0d1117'
ORDER = ['1', '4', '7', '2', '5', '8', '3', '6']
P = {}
for i, n in enumerate(ORDER):
    t = math.radians(45 * i)
    P[n] = (50 + 34 * math.sin(t), 48 - 34 * math.cos(t))
P['9'] = (50, 34)
EDGES = ['14', '47', '72', '25', '58', '83', '36', '61', '49', '96']
R = 5

def key(u, v): return ''.join(sorted(u + v))
EK = {key(e[0], e[1]) for e in EDGES}

def edge(u, v, col, w=0.7):
    (x1, y1), (x2, y2) = P[u], P[v]
    d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return (f"<line x1='{x1 + ux * R:.2f}' y1='{y1 + uy * R:.2f}' x2='{x2 - ux * R:.2f}' y2='{y2 - uy * R:.2f}' "
            f"stroke='{col}' stroke-width='{w}'/>")

def node(n, ring=INK, fill=None, mark=False):
    x, y = P[n]; s = ''
    if mark:
        s += f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{R + 1.6}' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
    if fill:
        s += f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{R}' fill='{fill}' stroke='{ring}' stroke-width='0.6'/>"
        tc = BG
    else:
        s += f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{R}' fill='none' stroke='{ring}' stroke-width='0.7'/>"
        tc = LAB if ring == INK else ring
    s += f"<text x='{x:.2f}' y='{y + 1.7:.2f}' fill='{tc}' font-size='4.6' text-anchor='middle' font-weight='700'>{n}</text>"
    return s

def graph(gold_edges=(), red_edges=(), marks=(), fills=None, dim_rest=False, mw=360, aria='Карта прыжков'):
    # gold_edges — подсвеченные отрезки; dim_rest — остальные отрезки тусклые (весь чертёж всегда на месте)
    fills = fills or {}
    ge = {key(*e) for e in gold_edges}; re_ = {key(*e) for e in red_edges}
    s = ''
    for e in EDGES:
        k = key(e[0], e[1])
        if k in ge: s += edge(e[0], e[1], GOLD, 1.1)
        elif k in re_: s += edge(e[0], e[1], RED, 1.1)
        else: s += edge(e[0], e[1], DIM if dim_rest else INK, 0.7)
    for n in P:
        s += node(n, INK, fills.get(n), n in marks)
    st = f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='8 6 84 84' role='img' aria-label='{aria}'{st}>{s}</svg>"

def route(seq, mw=280):
    pairs = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
    assert all(key(*p) in EK for p in pairs), seq
    return graph(gold_edges=pairs, marks=(seq[0],), dim_rest=True, mw=mw, aria='Обход ' + ', '.join(seq))

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

def grid(cells, cap=''):
    c = ''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s, t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>", cap)

def strip():
    s = ''
    for i in range(9):
        x = 1 + 10 * i
        s += f"<rect x='{x}' y='1' width='10' height='10' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        s += f"<text x='{x + 5}' y='8' fill='{LAB}' font-size='5' text-anchor='middle' font-weight='700'>{i + 1}</text>"
    return f"<svg viewBox='0 0 92 12' role='img' aria-label='Полоска 1 × 9' style='max-width:560px'>{s}</svg>"

def seqs(t): return [list(x) for x in t.split()]

V = {}
# условие: полоска
V['клетки 1, …, 9 в порядке прыжков кузнечика'] = fig(strip(), 'Полоска 1 × 9.')
# карта прыжков: цепочка 4–6 и приклеенные 1, 9
V['приклеены к цепочке сбоку'] = fig(
  graph(gold_edges=('41', '16', '49', '96'), marks=('1', '9'), mw=340, aria='Карта прыжков: цепочка и клетки 1, 9'),
  f"Клетки — кружки, прыжки — отрезки; <b style='color:{GOLD}'>клетки 1 и 9 и их прыжки</b>.")
# 1 и 9 обе между 4 и 6 — круг
V['замыкаются в круг'] = fig(
  graph(red_edges=('41', '16', '49', '96'), dim_rest=True, mw=260, aria='Клетки 4, 1, 6, 9 замкнуты в круг'),
  f"<b style='color:{RED}'>1 и 9 обе между 4 и 6</b>: круг 4, 1, 6, 9.")
def world(t):
    return grid([(route(s), ', '.join(s)) for s in seqs(t)])
V['1. N(1 и 9 на концах).'] = world('147258369 163852749')
V['2. N(9 на конце, 1 между 4 и 6).'] = world('941638527 961472583')
V['3. N(1 на конце, 9 между 4 и 6).'] = world('149638527 169472583')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
