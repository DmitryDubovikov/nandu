#!/usr/bin/env python3
"""Иллюстрации главы 7 «Включения и исключения» → nandu_n2_kombinatorika_uchebnik.vis.json.

Цветовой язык: множества — круги своего цвета (море и первое множество — синий, дача и второе — зелёный, третье —
фиолетовый); пересечение — золотое; плохое, лишнее — красное; выброшенное — серое. Вершины шестиугольника — точки
с буквами A–F, диагонали — серые, выбранная пара — синяя и зелёная.
Анимируется только переход (правило 15): ребята на море и на даче отмечаются по очереди, и шестеро в общей части
получают вторую отметку — каждый из них попал и в 14, и в 17. Остальные рисунки статичны.

Запуск: python3 26-27/nandu_level2/kombinatorika/vis/glava_7.py
"""
import json, os, re
from math import cos, sin, pi

from glava_2 import svg, fig, t, g, GOLD, BLUE, GREEN, VIOLET, RED, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.vis.json')

INK = 'var(--ink)'
MUTED = 'var(--muted)'


# ——— Пример 1: все трёхзначные = без тройки + хотя бы одна тройка ———

def bar_900():
    x0, w, y = 20, 540, 46
    w1 = w * 648 / 900
    b = [t(x0 + w / 2, 24, 'все трёхзначные числа: 9 · 10 · 10 = 900', INK, 15, weight=700),
         f"<rect x='{x0}' y='{y}' width='{w1:.1f}' height='40' rx='6' fill='{GREY}' opacity='0.55'/>",
         f"<rect x='{x0 + w1:.1f}' y='{y}' width='{w - w1:.1f}' height='40' rx='6' fill='{GOLD}'/>",
         t(x0 + w1 / 2, y + 26, 'без цифры 3: 8 · 9 · 9 = 648', INK, 14, weight=700),
         t(x0 + w1 + (w - w1) / 2, y + 26, '252', '#0d1117', 15, weight=700),
         t(x0 + w1 + (w - w1) / 2, y + 66, 'хотя бы одна 3', GOLD, 14, weight=700),
         t(x0 + w1 + (w - w1) / 2, y + 86, '900 − 648', GOLD, 14, weight=700)]
    return fig(svg(580, 142, ''.join(b), maxw=580))


# ——— Пример 2: правильный шестиугольник ABCDEF ———

ANG = {'A': 120, 'B': 60, 'C': 0, 'D': -60, 'E': -120, 'F': 180}


def hp(v, cx, cy, R):
    a = ANG[v] * pi / 180
    return cx + R * cos(a), cy - R * sin(a)


def line(p, q, col, w):
    return (f"<line x1='{p[0]:.1f}' y1='{p[1]:.1f}' x2='{q[0]:.1f}' y2='{q[1]:.1f}' stroke='{col}' "
            f"stroke-width='{w}' stroke-linecap='round'/>")


def hexagon(cx, cy, R, diag=(), pair=(), ring=(), labels=True, all_diag=False, size=14):
    """Шестиугольник: стороны, серые диагонали, выбранная пара синим и зелёным, вершины в золотых кольцах."""
    vs = 'ABCDEF'
    b = []
    for i, v in enumerate(vs):
        b.append(line(hp(v, cx, cy, R), hp(vs[(i + 1) % 6], cx, cy, R), INK, 2))
    if all_diag:
        diag = [(u, v) for i, u in enumerate(vs) for v in vs[i + 2:] if not (u == 'A' and v == 'F')]
    for u, v in diag:
        b.append(line(hp(u, cx, cy, R), hp(v, cx, cy, R), GREY, 1.6))
    for (u, v), col in zip(pair, (BLUE, GREEN)):
        b.append(line(hp(u, cx, cy, R), hp(v, cx, cy, R), col, 3.5))
    for v in vs:
        x, y = hp(v, cx, cy, R)
        if v in ring:
            b.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='9' fill='none' stroke='{GOLD}' stroke-width='2.5'/>")
        b.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4' fill='{INK}'/>")
        if labels:
            lx, ly = hp(v, cx, cy, R + 17)
            b.append(t(round(lx, 1), round(ly + size * 0.35, 1), v, INK, size, weight=700))
    return ''.join(b)


def hex_task():
    return fig(svg(260, 240, hexagon(130, 120, 90, all_diag=True, size=15), maxw=260),
               'правильный шестиугольник и все его диагонали')


def hex_kinds():
    b = []
    kinds = [(('A', 'C'), ('B', 'D'), 'пересекаются', RED),
             (('A', 'C'), ('A', 'D'), 'смежные — общий конец A', RED),
             (('A', 'C'), ('D', 'F'), 'без общих точек', GOLD)]
    for k, (p, q, cap, col) in enumerate(kinds):
        cx = 100 + k * 200
        b.append(hexagon(cx, 100, 62, pair=(p, q)))
        b.append(t(cx, 200, f'{{{p[0]}{p[1]}, {q[0]}{q[1]}}}', INK, 14, weight=700))
        b.append(t(cx, 222, cap, col, 14, weight=700))
    return fig(svg(600, 236, ''.join(b), maxw=600))


def hex_corr():
    b = [f"<defs><marker id='a7' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' "
         f"orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='{MUTED}'/></marker></defs>",
         t(110, 22, 'четыре вершины', GOLD, 14, weight=700),
         t(390, 22, 'пара пересекающихся диагоналей', INK, 14, weight=700)]
    rows = [('ABCD', (('A', 'C'), ('B', 'D'))), ('ACDF', (('A', 'D'), ('C', 'F'))),
            ('BCEF', (('B', 'E'), ('C', 'F')))]
    for r, (four, pair) in enumerate(rows):
        cy = 96 + r * 140
        b.append(hexagon(110, cy, 50, ring=four, size=13))
        b.append(f"<line x1='190' y1='{cy}' x2='300' y2='{cy}' stroke='{MUTED}' stroke-width='2' "
                 f"marker-end='url(#a7)'/>")
        b.append(hexagon(390, cy, 50, pair=pair, size=13))
        b.append(t(510, cy + 5, f'{{{pair[0][0]}{pair[0][1]}, {pair[1][0]}{pair[1][1]}}}', INK, 14,
                   anchor='start', weight=700))
    return fig(svg(600, 70 + 3 * 140 - 40, ''.join(b), maxw=600),
               'четыре вершины, соединённые через одну, дают пару пересекающихся диагоналей — и только одну')


def hex_answer():
    b = []
    for k, (p, q) in enumerate(((('A', 'C'), ('D', 'F')), (('B', 'D'), ('E', 'A')), (('C', 'E'), ('F', 'B')))):
        cx = 100 + k * 200
        b.append(hexagon(cx, 100, 62, pair=(p, q)))
        b.append(t(cx, 200, f'{{{p[0]}{p[1]}, {q[0]}{q[1]}}}', INK, 14, weight=700))
    return fig(svg(600, 214, ''.join(b), maxw=600), 'все три пары диагоналей без общих точек')


# ——— Пример 3: море и дача — шестеро попадают и в 14, и в 17 ———

def circles2(ca, cb, r, ka, kb, lab_a, lab_b, fill=False):
    """Два пересекающихся круга со своими подписями."""
    (xa, ya), (xb, yb) = ca, cb
    op = " fill-opacity='0.10'" if fill else ''
    fa = BLUE if fill else 'none'
    fb = GREEN if fill else 'none'
    return (f"<circle cx='{xa}' cy='{ya}' r='{r}' fill='{fa}'{op} stroke='{BLUE}' stroke-width='{ka}'/>"
            f"<circle cx='{xb}' cy='{yb}' r='{r}' fill='{fb}'{op} stroke='{GREEN}' stroke-width='{kb}'/>"
            + lab_a + lab_b)


def sea():
    ca, cb, r = (205, 150), (355, 150), 115
    b = [circles2(ca, cb, r, 2, 2, t(150, 22, 'море', BLUE, 15, weight=700), t(410, 22, 'дача', GREEN, 15, weight=700))]
    # 8 только на море, 6 в общей части, 11 только на даче
    left = [(118 + 32 * (i % 3), 110 + 36 * (i // 3)) for i in range(8)]
    left = [(x + (16 if i // 3 == 1 else 0), y) for i, (x, y) in enumerate(left)]
    mid = [(265 + 30 * (i % 2), 115 + 34 * (i // 2)) for i in range(6)]
    right = [(372 + 32 * (i % 3), 96 + 36 * (i // 3)) for i in range(11)]
    right = [(x + (16 if i // 3 % 2 == 1 else 0), y) for i, (x, y) in enumerate(right)]
    for x, y in left + mid + right:
        b.append(f"<circle cx='{x}' cy='{y}' r='8' fill='none' stroke='{GREY}' stroke-width='1.5'/>")
    # 1) на море — 14 точек синие
    b.append(g('fi', 0.6, ''.join(f"<circle cx='{x}' cy='{y}' r='8' fill='{BLUE}'/>" for x, y in left + mid)
               + t(150, 290, 'на море: 14', BLUE, 15, weight=700)))
    # 2) на даче — 17 точек в зелёном кольце
    b.append(g('fi', 2.2, ''.join(f"<circle cx='{x}' cy='{y}' r='11' fill='none' stroke='{GREEN}' "
                                  f"stroke-width='3'/>" for x, y in mid + right)
               + t(410, 290, 'на даче: 17', GREEN, 15, weight=700)))
    # 3) шестеро в общей части — и синие, и в зелёном кольце: посчитаны дважды
    b.append(g('fi', 3.8, ''.join(f"<circle cx='{x}' cy='{y}' r='15' fill='none' stroke='{GOLD}' "
                                  f"stroke-width='2'/>" for x, y in mid)
               + t(280, 318, 'шестеро в общей части посчитаны дважды', GOLD, 15, weight=700)))
    b.append(t(280, 346, '14 + 17 − 6 = 25', INK, 16, weight=700, cls='fi', d=5.0))
    return fig(svg(560, 360, ''.join(b), maxw=560), fx=True)


def union_fig():
    b = []
    for k, (cap, sub) in enumerate((('М ∩ Д', 'пересечение — и там, и там'),
                                    ('М ∪ Д', 'объединение — хотя бы в одном'))):
        ox = k * 290
        ca, cb, r = (ox + 105, 100), (ox + 175, 100), 62
        if k == 0:
            b.append(f"<clipPath id='c7m'><circle cx='{ca[0]}' cy='{ca[1]}' r='{r}'/></clipPath>"
                     f"<circle cx='{cb[0]}' cy='{cb[1]}' r='{r}' fill='{GOLD}' clip-path='url(#c7m)'/>")
        else:
            b.append(f"<circle cx='{ca[0]}' cy='{ca[1]}' r='{r}' fill='{GOLD}'/>"
                     f"<circle cx='{cb[0]}' cy='{cb[1]}' r='{r}' fill='{GOLD}'/>")
        b.append(circles2(ca, cb, r, 2.5, 2.5, t(ca[0] - 40, 28, 'М', BLUE, 15, weight=700),
                          t(cb[0] + 40, 28, 'Д', GREEN, 15, weight=700)))
        b.append(t(ox + 140, 190, cap, INK, 16, weight=700))
        b.append(t(ox + 140, 212, sub, MUTED, 14))
    return fig(svg(570, 222, ''.join(b), maxw=570))


def xyz():
    ca, cb, r = (170, 105), (270, 105), 80
    b = [circles2(ca, cb, r, 2.5, 2.5, t(110, 22, 'A', BLUE, 16, weight=700), t(330, 22, 'B', GREEN, 16, weight=700),
                  fill=True),
         t(130, 112, 'x', BLUE, 20, weight=700), t(220, 112, 'z', GOLD, 20, weight=700),
         t(310, 112, 'y', GREEN, 20, weight=700),
         t(150, 212, 'N(A) = x + z', BLUE, 15, weight=700), t(290, 212, 'N(B) = y + z', GREEN, 15, weight=700)]
    return fig(svg(440, 224, ''.join(b), maxw=440), 'z — в обоих кругах, поэтому в N(A) + N(B) входит дважды')


# ——— Три множества: сколько раз посчитана каждая часть ———

def venn3(ox, oy, nums, title, sub, r=52):
    """Три круга и в каждой из семи частей — сколько раз она посчитана."""
    ca, cb, cc = (ox - 30, oy - 18), (ox + 30, oy - 18), (ox, oy + 34)
    b = [f"<circle cx='{x}' cy='{y}' r='{r}' fill='none' stroke='{c}' stroke-width='2'/>"
         for (x, y), c in ((ca, BLUE), (cb, GREEN), (cc, VIOLET))]
    b += [t(ca[0] - 52, ca[1] - 42, 'A', BLUE, 14, weight=700), t(cb[0] + 52, cb[1] - 42, 'B', GREEN, 14, weight=700),
          t(cc[0] + 62, cc[1] + 44, 'C', VIOLET, 14, weight=700)]
    spots = {'a': (ox - 58, oy - 30), 'b': (ox + 58, oy - 30), 'c': (ox, oy + 66),
             'ab': (ox, oy - 42), 'ac': (ox - 30, oy + 22), 'bc': (ox + 30, oy + 22), 'abc': (ox, oy + 4)}
    for k, (x, y) in spots.items():
        n = nums[len(k) - 1]
        col = RED if n == 0 else (GOLD if len(k) > 1 else INK)
        b.append(t(x, y + 6, str(n), col, 17, weight=700))
    b.append(t(ox, oy + 120, title, INK, 14, weight=700))
    b.append(t(ox, oy + 140, sub, MUTED, 13))
    return ''.join(b)


def triple():
    b = [venn3(100, 100, (1, 2, 3), 'N(A) + N(B) + N(C)', 'двукратные — 2, трёхкратные — 3'),
         venn3(300, 100, (1, 1, 0), '− три попарных пересечения', 'трёхкратные — 0'),
         venn3(500, 100, (1, 1, 1), '+ N(A ∩ B ∩ C)', 'каждая часть — 1')]
    return fig(svg(600, 250, ''.join(b), maxw=600), 'число в части — сколько раз посчитан её элемент')


# ——— Пример 4: три инструмента — сколько учеников в каждой части ———

def instruments():
    ox, oy, r = 230, 150, 78
    cg, cf, cb = (ox - 46, oy - 26), (ox + 46, oy - 26), (ox, oy + 52)
    b = [f"<rect x='20' y='14' width='420' height='300' rx='10' fill='{GOLD}' fill-opacity='0.16' "
         f"stroke='{MUTED}' stroke-width='1.5'/>",
         t(30, 36, 'все 36 учеников', MUTED, 14, anchor='start', weight=700)]
    b += [f"<circle cx='{x}' cy='{y}' r='{r}' fill='var(--bg)' stroke='none'/>" for x, y in (cg, cf, cb)]
    b += [f"<circle cx='{x}' cy='{y}' r='{r}' fill='{c}' fill-opacity='0.08' stroke='{c}' stroke-width='2.5'/>"
          for (x, y), c in ((cg, BLUE), (cf, GREEN), (cb, VIOLET))]
    b += [t(cg[0] - 70, cg[1] - 66, 'Г', BLUE, 16, weight=700), t(cf[0] + 70, cf[1] - 66, 'Ф', GREEN, 16, weight=700),
          t(cb[0] + 88, cb[1] + 50, 'Б', VIOLET, 16, weight=700)]
    spots = [((ox - 86, oy - 40), 7, INK), ((ox + 86, oy - 40), 6, INK), ((ox, oy + 100), 4, INK),
             ((ox, oy - 62), 3, GOLD), ((ox - 44, oy + 26), 4, GOLD), ((ox + 44, oy + 26), 2, GOLD),
             ((ox, oy + 4), 2, RED)]
    for (x, y), n, col in spots:
        b.append(t(x, y + 7, str(n), col, 19, weight=700))
    b += [t(390, 286, '8', GOLD, 22, weight=700),
          t(230, 342, '7 + 6 + 4 + 3 + 4 + 2 + 2 = 28', INK, 15, weight=700),
          t(230, 366, '36 − 28 = 8 — вне всех трёх кругов', GOLD, 15, weight=700)]
    return fig(svg(460, 380, ''.join(b), maxw=460), 'число в части — сколько в ней учеников')


FIGS = {
    'N(чисел хотя бы с одной цифрой 3) = 900 − 648 = 252': bar_900,
    'Сколькими способами можно выбрать такие две диагонали?': hex_task,
    'N(пар без общих точек) = N(всех пар) − N(пересекающихся пар) − N(смежных пар)': hex_kinds,
    'каждым четырём вершинам соответствует единственная пара пересекающихся диагоналей': hex_corr,
    'N(пар без общих точек) = 36 − 15 − 18 = 3': hex_answer,
    'Например, если Лусия была и на море, и на даче': sea,
    'Объединение обозначается М ∪ Д.': union_fig,
    'z — число элементов пересечения A ∩ B': xyz,
    'Поэтому надо прибавить число элементов тройного пересечения.': triple,
    'только на барабанах: 12 − 4 − 2 − 2 = 4': instruments,
}

if __name__ == '__main__':
    d = json.load(open(VIS))
    md = open(os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.md')).read()
    plain = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', md))
    new = {anchor: f() for anchor, f in FIGS.items()}
    missing = [a for a in new if a not in plain]
    if missing:
        raise SystemExit(f'якоря не найдены в тексте: {missing}')
    d = {k: v for k, v in d.items() if k in plain and (k in new or v not in new.values())}
    d.update(new)
    json.dump(d, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(FIGS), 'рисунков →', os.path.relpath(VIS))
