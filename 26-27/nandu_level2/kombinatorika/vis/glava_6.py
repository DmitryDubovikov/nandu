#!/usr/bin/env python3
"""Иллюстрации главы 6 «Треугольник Паскаля» → nandu_n2_kombinatorika_uchebnik.vis.json.

Цветовой язык: перекрёсток — точка, число путей в нём — золотое; дорожка, трасса, улица — серая со стрелкой;
последний шаг двух групп путей — синий и зелёный; закрытое — красное. Игры Бори А–Д — цвета букв глав 2–4.
Анимируется только переход (правило 15): числа появляются снизу вверх, каждое вместе с дорожками, по которым в него
приходят; сетка улиц поворачивается и становится треугольником; тройки игр уходят каждая в свой столбец.

Запуск: python3 26-27/nandu_level2/kombinatorika/vis/glava_6.py
"""
import json, os, re
from itertools import combinations
from math import comb

from glava_2 import svg, fig, t, g, GOLD, BLUE, GREEN, VIOLET, RED, GREY
from glava_3 import DARK

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.vis.json')

GAMES = [('А', BLUE), ('Б', GOLD), ('В', GREEN), ('Г', RED), ('Д', VIOLET)]


def defs():
    m = ''.join(f"<marker id='a6{n}' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' "
                f"orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='{c}'/></marker>"
                for n, c in (('g', 'var(--muted)'), ('b', BLUE), ('z', GREEN), ('o', GOLD), ('v', VIOLET)))
    return f'<defs>{m}</defs>'


def road(p, q, col='var(--muted)', mk='g', w=1.8, r=8, cls='', d=None):
    """Дорожка p → q со стрелкой у конца; концы отодвинуты от точек перекрёстков."""
    (x1, y1), (x2, y2) = p, q
    L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    st = f" class='{cls}' style='--d:{d}s'" if cls else ''
    return (f"<line x1='{x1 + ux * r:.1f}' y1='{y1 + uy * r:.1f}' x2='{x2 - ux * r:.1f}' y2='{y2 - uy * r:.1f}' "
            f"stroke='{col}' stroke-width='{w}' marker-end='url(#a6{mk})'{st}/>")


def dot(x, y, r=4.5, col='var(--ink)'):
    return f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{col}'/>"


def num(x, y, n, col=GOLD, size=15, r=12):
    """Число путей в перекрёстке — на тёмной плашке поверх точки."""
    return (f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='var(--bg)' stroke='{col}' stroke-width='1.5'/>"
            + t(round(x, 1), round(y + size * 0.35, 1), str(n), col, size, weight=700))


# ——— Пример 1: парк — ромб 4 × 2, дорожки вверх-вправо (i) и вверх-влево (j) ———

PI, PJ, PS = 4, 2, 44


def pp(i, j, x0=150, y0=300):
    return x0 + PS * (i - j), y0 - PS * (i + j)


PARK_LBL = {(0, 0): ('O', 0, 22), (4, 2): ('F', 0, -14), (1, 0): ('A', 16, 6), (0, 1): ('B', -16, 6),
            (1, 1): ('C', 0, 24), (2, 0): ('D', 16, 6), (2, 1): ('M', 16, 6), (3, 2): ('P', -16, 4), (4, 1): ('Q', 16, 4)}


def park_edges(hi=None):
    b = []
    for i in range(PI + 1):
        for j in range(PJ + 1):
            if i < PI:
                b.append(road(pp(i, j), pp(i + 1, j)))
            if j < PJ:
                b.append(road(pp(i, j), pp(i, j + 1)))
    return b


def park_task():
    b = [defs()] + park_edges()
    for i in range(PI + 1):
        for j in range(PJ + 1):
            b.append(dot(*pp(i, j)))
    for (i, j), (s, dx, dy) in PARK_LBL.items():
        x, y = pp(i, j)
        b.append(t(x + dx, y + dy, s, 'var(--ink)', 15, weight=700))
    return fig(svg(350, 330, ''.join(b), maxw=350), 'схема дорожек; идти можно только по стрелкам, вверх')


def park_small():
    """Нижний ромбик: путь в C через A — синий, через B — зелёный."""
    P = {k: pp(*k, x0=130, y0=170) for k in [(0, 0), (1, 0), (0, 1), (1, 1)]}
    P = {k: (x, y) for k, (x, y) in P.items()}
    b = [defs(),
         road(P[(0, 0)], P[(1, 0)], BLUE, 'b', 3), road(P[(1, 0)], P[(1, 1)], BLUE, 'b', 3),
         road(P[(0, 0)], P[(0, 1)], GREEN, 'z', 3), road(P[(0, 1)], P[(1, 1)], GREEN, 'z', 3)]
    for k, (x, y) in P.items():
        b.append(dot(x, y))
    for k in [(1, 0), (0, 1)]:
        x, y = P[k]
        b.append(num(x + (26 if k == (1, 0) else -26), y, 1, BLUE if k == (1, 0) else GREEN))
    for k, (s, dx, dy) in PARK_LBL.items():
        if k in P:
            x, y = P[k]
            b.append(t(x + dx * 0.4, y + (20 if k == (0, 0) else -12), s, 'var(--ink)', 14, weight=700))
    x, y = P[(1, 1)]
    b.append(num(x, y - 34, 2))
    b.append(t(250, 60, 'через A — 1 путь', BLUE, 14, anchor='start', weight=700))
    b.append(t(250, 84, 'через B — 1 путь', GREEN, 14, anchor='start', weight=700))
    b.append(t(250, 116, 'в C: 1 + 1 = 2', GOLD, 15, anchor='start', weight=700))
    return fig(svg(420, 190, ''.join(b), maxw=420), 'последний шаг в C — либо из A, либо из B')


def paths_m():
    """✦ Все пути от входа в M по группам: через C (2) и через D (1); в каждой схеме сначала путь до C или D,
    потом дорисовывается единственная дорожка в M."""
    s_ = 40

    def mp(i, j, ox, oy):
        return ox + s_ * (i - j), oy - s_ * (i + j)

    nodes = [(i, j) for i in range(3) for j in range(2)]
    paths = [((0, 0), (1, 0), (1, 1), BLUE, 'b', 'C'), ((0, 0), (0, 1), (1, 1), BLUE, 'b', 'C'),
             ((0, 0), (1, 0), (2, 0), GREEN, 'z', 'D')]
    oxs = [100, 270, 510]
    oy = 196
    b = [defs()]
    b.append(f"<rect x='14' y='34' width='346' height='190' rx='12' fill='none' stroke='{BLUE}' stroke-width='1.5'/>")
    b.append(f"<rect x='410' y='34' width='216' height='190' rx='12' fill='none' stroke='{GREEN}' stroke-width='1.5'/>")
    b.append(t(187, 24, 'через C', BLUE, 14, weight=700))
    b.append(t(518, 24, 'через D', GREEN, 14, weight=700))
    for n_, (p0, p1, p2, col, mk, via) in enumerate(paths):
        ox = oxs[n_]
        for (i, j) in nodes:
            if i < 2:
                b.append(road(mp(i, j, ox, oy), mp(i + 1, j, ox, oy), 'var(--line)', 'g', 1.4, 5))
            if j < 1:
                b.append(road(mp(i, j, ox, oy), mp(i, j + 1, ox, oy), 'var(--line)', 'g', 1.4, 5))
            b.append(dot(*mp(i, j, ox, oy), 3.5))
        d = 0.4 + 1.3 * n_
        pre = (f"<polyline points='{' '.join('%.1f,%.1f' % mp(*q, ox, oy) for q in (p0, p1, p2))}' fill='none' "
               f"stroke='{col}' stroke-width='3' stroke-linejoin='round' stroke-opacity='.75'/>")
        b.append(g('fi', d, pre))
        b.append(g('fi', d + 0.6, road(mp(*p2, ox, oy), mp(2, 1, ox, oy), col, mk, 3.5, 4)))
        x, y = mp(*p2, ox, oy)
        b.append(t(x + (14 if via == 'D' else -14), y + 5, via, col, 13, anchor='start' if via == 'D' else 'end',
                   weight=700))
        x, y = mp(2, 1, ox, oy)
        b.append(t(x + 10, y - 6, 'M', 'var(--ink)', 13, anchor='start', weight=700))
        x, y = mp(0, 0, ox, oy)
        b.append(t(x, y + 18, 'O', 'var(--muted)', 12))
    b.append(t(187, 250, 'путей от входа в C — 2: каждый + дорожка C → M', BLUE, 13, weight=700, cls='fi', d=3.2))
    b.append(t(518, 250, 'путей от входа в D — 1: + дорожка D → M', GREEN, 13, weight=700, cls='fi', d=4.4))
    b.append(t(304, 284, 'путей от входа в M: 2 + 1 = 3', GOLD, 15, weight=700, cls='fi', d=4.8))
    return fig(svg(640, 298, ''.join(b), maxw=640), fx=True)


def park_fill():
    """✦ Числа появляются снизу вверх; у каждого на миг вспыхивают дорожки, по которым в него приходят."""
    b = [defs()] + park_edges()
    for i in range(PI + 1):
        for j in range(PJ + 1):
            b.append(dot(*pp(i, j)))
    x, y = pp(0, 0)
    b.append(t(x, y + 24, 'O', 'var(--ink)', 14, weight=700))
    x, y = pp(4, 2)
    b.append(t(x, y - 20, 'F', 'var(--ink)', 14, weight=700))
    for lev in range(1, PI + PJ + 1):
        d = 0.3 + 0.85 * (lev - 1)
        for i in range(PI + 1):
            j = lev - i
            if not 0 <= j <= PJ:
                continue
            q = pp(i, j)
            flash = []
            if i > 0:
                flash.append(road(pp(i - 1, j), q, GOLD, 'o', 3.2))
            if j > 0:
                flash.append(road(pp(i, j - 1), q, GOLD, 'o', 3.2))
            b.append(g('fi', d, g('fo', d + 0.75, ''.join(flash))))
            b.append(g('fi', d + 0.35, num(*q, comb(i + j, i))))
    return fig(svg(350, 340, ''.join(b), maxw=350), fx=True)


def park_last():
    """У фонтана: последний шаг из P (10 путей) или из Q (5 путей)."""
    b = [defs()] + park_edges()
    for i in range(PI + 1):
        for j in range(PJ + 1):
            if (i, j) in ((3, 2), (4, 1), (4, 2)):
                continue
            b.append(num(*pp(i, j), comb(i + j, i), 'var(--muted)', 13, 11))
    b.append(road(pp(3, 2), pp(4, 2), BLUE, 'b', 4))
    b.append(road(pp(4, 1), pp(4, 2), GREEN, 'z', 4))
    b.append(num(*pp(3, 2), 10, BLUE))
    b.append(num(*pp(4, 1), 5, GREEN))
    b.append(num(*pp(4, 2), 15, GOLD, 16, 14))
    x, y = pp(3, 2)
    b.append(t(x - 20, y + 4, 'P', BLUE, 15, anchor='end', weight=700))
    x, y = pp(4, 1)
    b.append(t(x + 20, y + 4, 'Q', GREEN, 15, anchor='start', weight=700))
    x, y = pp(4, 2)
    b.append(t(x + 22, y - 8, 'F: 10 + 5 = 15', GOLD, 15, anchor='start', weight=700))
    return fig(svg(420, 330, ''.join(b), maxw=420), 'в F приходят либо из P, либо из Q')


# ——— Правило суммы: группы не пересекаются и вместе дают всё ———

def sum_rule():
    panels = [('✓ группы не пересекаются,', 'вместе — все: 3 + 2 = 5', GREEN,
               [(0, 3, BLUE), (3, 5, GREEN)]),
              ('✗ точка в двух группах:', '3 + 3 = 6, а точек 5', RED,
               [(0, 3, BLUE), (2, 5, GREEN)]),
              ('✗ точка вне групп:', '3 + 1 = 4, а точек 5', RED,
               [(0, 3, BLUE), (4, 5, GREEN)])]
    b = []
    for p_, (l1, l2, col, groups) in enumerate(panels):
        x0, y0 = 14 + p_ * 200, 58
        b.append(t(x0, 20, l1, col, 13, anchor='start', weight=700))
        b.append(t(x0, 38, l2, col, 13, anchor='start'))
        for k in range(5):
            b.append(dot(x0 + 18 + k * 34, y0 + 30, 7, 'var(--ink)'))
        for gi, (a, z, gc) in enumerate(groups):
            yy = y0 + (6 if gi == 0 else 14)
            hh = 48 - (0 if gi == 0 else 16)
            b.append(f"<rect x='{x0 + 4 + a * 34}' y='{yy}' width='{(z - a) * 34 - 6}' height='{hh}' rx='14' "
                     f"fill='none' stroke='{gc}' stroke-width='2.2'/>")
    return fig(svg(610, 124, ''.join(b), maxw=610), 'пример на числах, не из задачи')


# ——— Пример 2: санные трассы ———

SLED = {'S': (200, 34), 'A': (80, 110), 'B': (200, 110), 'C': (330, 110), 'D': (140, 190), 'E': (320, 190),
        'G': (80, 270), 'H': (200, 270), 'F': (200, 350)}
SLED_E = [('S', 'A'), ('S', 'B'), ('S', 'C'), ('A', 'D'), ('B', 'D'), ('B', 'E'), ('C', 'E'), ('A', 'G'),
          ('D', 'G'), ('D', 'H'), ('E', 'H'), ('G', 'F'), ('H', 'F'), ('E', 'F')]
SLED_OFF = {'A': (-24, 14), 'B': (24, 14), 'C': (24, 14), 'D': (-26, 2), 'E': (26, 2),
            'G': (-26, 0), 'H': (26, -4)}
SLED_N = {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'G': 3, 'H': 4, 'F': 9}


SLED_LBL = {'S': (-16, 5, 'end'), 'A': (-18, 5, 'end'), 'B': (18, -8, 'start'), 'C': (18, 5, 'start'),
            'D': (-18, -6, 'end'), 'E': (18, 5, 'start'), 'G': (-18, 5, 'end'), 'H': (18, 20, 'start'),
            'F': (-18, 5, 'end')}


def sled(filled=False):
    b = [defs()]
    last = {('G', 'F'): (BLUE, 'b'), ('H', 'F'): (GREEN, 'z'), ('E', 'F'): (VIOLET, 'v')}
    r = 15 if filled else 9
    for p, q in SLED_E:
        if filled and (p, q) in last:
            col, mk = last[(p, q)]
            b.append(road(SLED[p], SLED[q], col, mk, 3, r))
        else:
            b.append(road(SLED[p], SLED[q], 'var(--muted)', 'g', 2, r))
    for k, (x, y) in SLED.items():
        dx, dy, an = SLED_LBL[k]
        b.append(t(x + dx * (1.3 if filled else 1), y + dy, k, 'var(--ink)', 15, anchor=an, weight=700))
        if filled and k in SLED_N and k != 'F':
            col = {'G': BLUE, 'H': GREEN, 'E': VIOLET}.get(k, GOLD)
            b.append(num(x, y, SLED_N[k], col, 14, 12))
        elif filled and k == 'F':
            b.append(num(x, y, 9, GOLD, 15, 13))
        else:
            b.append(dot(x, y, 5))
    if filled:
        x, y = SLED['F']
        b.append(t(x + 22, y + 6, '3 + 4 + 2 = 9', GOLD, 15, anchor='start', weight=700))
        return fig(svg(440, 380, ''.join(b), maxw=440), 'в финиш ведут три трассы — из G, из H и из E')
    return fig(svg(440, 372, ''.join(b), maxw=440), 'схема трасс; ехать можно только по стрелкам, вниз')


def sled_task():
    return sled(False)


def sled_filled():
    return sled(True)


# ——— Пример 3: город 3 × 3 квартала ———

CC = 56


def gp(i, j, x0=40, y0=200, c=CC):
    return x0 + c * i, y0 - c * j


def city(n_w, n_h, x0, y0, c=CC, lbl=True, end='D'):
    b = []
    for i in range(n_w + 1):
        b.append(f"<line x1='{x0 + i * c}' y1='{y0}' x2='{x0 + i * c}' y2='{y0 - n_h * c}' stroke='var(--line)' "
                 f"stroke-width='2'/>")
    for j in range(n_h + 1):
        b.append(f"<line x1='{x0}' y1='{y0 - j * c}' x2='{x0 + n_w * c}' y2='{y0 - j * c}' stroke='var(--line)' "
                 f"stroke-width='2'/>")
    if lbl:
        b.append(dot(x0, y0, 5) + t(x0 - 12, y0 + 20, 'A', 'var(--ink)', 16, weight=700))
        b.append(dot(x0 + n_w * c, y0 - n_h * c, 5)
                 + t(x0 + n_w * c + 14, y0 - n_h * c - 8, end, 'var(--ink)', 16, weight=700))
    return ''.join(b)


def city_task():
    b = city(3, 3, 40, 200)
    b += (f"<path d='M{40 + 3 * CC + 34} 196 h0' />" + t(40 + 3 * CC + 30, 120, '→ вправо', 'var(--muted)', 13,
                                                           anchor='start')
          + t(40 + 3 * CC + 30, 142, '↑ вверх', 'var(--muted)', 13, anchor='start'))
    return fig(svg(330, 232, b, maxw=330), 'город 3 × 3 квартала')


def city_fill():
    b = [defs(), city(3, 3, 40, 200, lbl=False)]
    b.append(road(gp(2, 3), gp(3, 3), BLUE, 'b', 4, 13))
    b.append(road(gp(3, 2), gp(3, 3), GREEN, 'z', 4, 13))
    for i in range(4):
        for j in range(4):
            if (i, j) == (3, 3):
                continue
            col = BLUE if (i, j) == (2, 3) else GREEN if (i, j) == (3, 2) else GOLD
            b.append(num(*gp(i, j), comb(i + j, i), col, 14, 13))
    b.append(num(*gp(3, 3), 20, GOLD, 15, 14))
    b.append(t(22, 222, 'A', 'var(--ink)', 15, weight=700))
    x, y = gp(3, 3)
    b.append(t(x + 22, y - 10, 'D', 'var(--ink)', 15, anchor='start', weight=700))
    b.append(t(x + 22, y + 26, '10 + 10 = 20', GOLD, 15, anchor='start', weight=700))
    b.append(t(x + 22, y + 50, 'слева — синее', BLUE, 13, anchor='start'))
    b.append(t(x + 22, y + 70, 'снизу — зелёное', GREEN, 13, anchor='start'))
    return fig(svg(380, 232, ''.join(b), maxw=380), 'число в перекрёстке — число слева плюс число снизу')


# ——— Треугольник: сетка поворачивается, A сверху; дорисовываются строки до 6 ———

AX, AY, TX, TY, TS = 150, 250, 260, 40, CC


def tri_pos(n, k, x0=TX, y0=TY, h=TS * 0.7071):
    """Место k строки n после поворота: строка — вниз, место — вправо."""
    return x0 + h * (2 * k - n), y0 + h * n


def rotate():
    to = f';--to:translate({TX}px,{TY}px) rotate(135deg) translate({-AX}px,{-AY}px)'
    inner = [city(3, 3, AX, AY, lbl=False)]
    for i in range(4):
        for j in range(4):
            x, y = AX + CC * i, AY - CC * j
            # число поворачивается обратно вокруг своей точки — остаётся прямым
            back = f';--to:translate({x}px,{y}px) rotate(-135deg) translate({-x}px,{-y}px)'
            inner.append(g('sl', 0.6, num(x, y, comb(i + j, i), GOLD, 14, 13), back))
    b = [g('sl', 0.6, ''.join(inner), to),
         g('fo', 0.4, t(AX - 14, AY + 22, 'A', 'var(--ink)', 15, weight=700)),
         g('fi', 2.0, t(TX - 24, TY + 5, 'A', 'var(--ink)', 15, weight=700))]
    # строки, которых в сетке 3 × 3 нет: в 4-й — края, в 5-й и 6-й — всё недостающее
    for n in range(4, 7):
        d = 2.4 + 0.6 * (n - 4)
        part = []
        for k in range(n + 1):
            j, i = k, n - k
            if i <= 3 and j <= 3:
                continue
            x, y = tri_pos(n, k)
            for pk in (k - 1, k):
                if 0 <= pk <= n - 1:
                    px, py = tri_pos(n - 1, pk)
                    L = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
                    ux, uy = (x - px) / L * 13, (y - py) / L * 13
                    part.append(f"<line x1='{px + ux:.1f}' y1='{py + uy:.1f}' x2='{x - ux:.1f}' y2='{y - uy:.1f}' "
                                f"stroke='var(--line)' stroke-width='2'/>")
            part.append(num(x, y, comb(n, k), GOLD, 14, 13))
        b.append(g('fi', d, ''.join(part)))
    b.append(t(14, 322, 'та же сетка улиц, повёрнутая: A сверху; ниже — те же сложения', 'var(--muted)', 13,
               anchor='start', cls='fi', d=2.0))
    return fig(svg(520, 334, ''.join(b), maxw=520), fx=True)


def lines_first(b):
    """Линии решётки — под числами: иначе линия к соседу сверху перечёркивает его плашку."""
    return [x for x in b if x.startswith('<line')] + [x for x in b if not x.startswith('<line')]


def tri_numbered():
    b = []
    for n in range(7):
        b.append(t(18, TY + TS * 0.7071 * n + 5, f'строка {n}', 'var(--muted)', 12, anchor='start'))
        for k in range(n + 1):
            x, y = tri_pos(n, k, x0=330)
            hi = (n, k) == (6, 2)
            if n:
                for pk in (k - 1, k):
                    if 0 <= pk <= n - 1:
                        px, py = tri_pos(n - 1, pk, x0=330)
                        b.append(f"<line x1='{px}' y1='{py}' x2='{x}' y2='{y}' stroke='var(--line)'/>")
            b.append(num(x, y, comb(n, k), BLUE if hi else GOLD, 14, 13))
    for k in range(7):
        x, y = tri_pos(6, k, x0=330)
        b.append(t(x, y + 32, f'место {k}', BLUE if k == 2 else 'var(--muted)', 11, weight=700 if k == 2 else None))
    b.append(t(18, 340, 'C(6, 2) = 15: строка 6, место 2', BLUE, 14, anchor='start', weight=700))
    return fig(svg(600, 352, ''.join(lines_first(b)), maxw=560))


def tri_c():
    b = []
    for n in range(5):
        for k in range(n + 1):
            x, y = 230 + 44 * (2 * k - n), 26 + 40 * n
            b.append(t(x, y, f'C({n}, {k})', GOLD, 14, weight=700))
    b.append(t(20, 236, 'строка n, место k — C(n, k): n шагов, из них k вниз-вправо', 'var(--ink)', 13,
               anchor='start'))
    return fig(svg(470, 248, ''.join(b), maxw=470))


def tri_rule():
    """Правило Паскаля на числах: 6 и 4 над 10."""
    b = []
    hl = {(4, 2): (BLUE, 'C(4, 2)'), (4, 3): (GREEN, 'C(4, 3)'), (5, 3): (GOLD, 'C(5, 3)')}
    for n in range(6):
        for k in range(n + 1):
            x, y = tri_pos(n, k, x0=230, y0=24, h=34)
            if n:
                for pk in (k - 1, k):
                    if 0 <= pk <= n - 1:
                        px, py = tri_pos(n - 1, pk, x0=230, y0=24, h=34)
                        w = 3 if (n, k) == (5, 3) else 1
                        col = (BLUE if pk == 2 else GREEN) if (n, k) == (5, 3) else 'var(--line)'
                        b.append(f"<line x1='{px}' y1='{py}' x2='{x}' y2='{y}' stroke='{col}' stroke-width='{w}'/>")
            col, _ = hl.get((n, k), ('var(--muted)', ''))
            b.append(num(x, y, comb(n, k), col, 13, 12))
    b.append(t(14, 244, 'C(5, 3) = 10', GOLD, 14, anchor='start', weight=700))
    b.append(t(120, 244, '=', 'var(--ink)', 14, anchor='start', weight=700))
    b.append(t(140, 244, 'C(4, 2) = 6', BLUE, 14, anchor='start', weight=700))
    b.append(t(236, 244, '+', 'var(--ink)', 14, anchor='start', weight=700))
    b.append(t(256, 244, 'C(4, 3) = 4', GREEN, 14, anchor='start', weight=700))
    return fig(svg(470, 258, ''.join(lines_first(b)), maxw=470))


# ——— Пример 4: тройки игр ———

TRIPLES = list(combinations(range(5), 3))


def triple(x, y, tr, r=10, step=24, ring=None):
    b = []
    for q, i in enumerate(tr):
        s, col = GAMES[i]
        cx = x + q * step
        b.append(f"<circle cx='{cx}' cy='{y}' r='{r}' fill='{col}'/>" + t(cx, y + 4.5, s, DARK, 13, weight=700))
    if ring:
        b.append(f"<rect x='{x - r - 5}' y='{y - r - 5}' width='{2 * step + 2 * r + 10}' height='{2 * r + 10}' "
                 f"rx='8' fill='none' stroke='{ring}' stroke-width='2'/>")
    return ''.join(b)


def games_sort():
    """✦ Десять троек по порядку уходят каждая в свой столбец: с А или без А."""
    b = [t(150, 150, 'с А', BLUE, 15, weight=700), t(400, 150, 'без А', 'var(--muted)', 15, weight=700)]
    b.append(f"<rect x='86' y='160' width='128' height='{6 * 32 + 12}' rx='10' fill='none' stroke='{BLUE}' "
             f"stroke-width='2'/>")
    b.append(f"<rect x='336' y='160' width='128' height='{4 * 32 + 12}' rx='10' fill='none' stroke='{GREY}' "
             f"stroke-width='2'/>")
    na = nb = 0
    for idx, tr in enumerate(TRIPLES):
        x, y = 30 + (idx % 5) * 104, 30 + (idx // 5) * 40
        if 0 in tr:
            tx, ty = 126, 180 + na * 32
            na += 1
        else:
            tx, ty = 376, 180 + nb * 32
            nb += 1
        b.append(g('sl', 0.5 + 0.35 * idx, triple(x, y, tr), f';--to:translate({tx - x}px,{ty - y}px)'))
    b.append(t(150, 384, 'C(4, 2) = 6', BLUE, 14, weight=700, cls='fi', d=5.0))
    b.append(t(400, 320, 'C(4, 3) = 4', 'var(--muted)', 14, weight=700, cls='fi', d=5.0))
    b.append(t(280, 412, 'каждая тройка — ровно в одном столбце: 6 + 4 = 10', 'var(--ink)', 14, weight=700,
               cls='fi', d=5.0))
    return fig(svg(560, 424, ''.join(b), maxw=560), fx=True)


def games_trap():
    b = [t(110, 20, 'с А — 6', BLUE, 14, weight=700), t(330, 20, 'с Б — 6', GOLD, 14, weight=700)]
    both = [tr for tr in TRIPLES if 0 in tr and 1 in tr]
    for col, (x, key) in enumerate(((80, 0), (300, 1))):
        rows = [tr for tr in TRIPLES if key in tr]
        for r, tr in enumerate(rows):
            b.append(triple(x, 46 + r * 32, tr, ring=RED if tr in both else None))
    b.append(t(500, 80, 'красные — в обеих', RED, 13, weight=700))
    b.append(t(500, 98, 'группах: дважды', RED, 13, weight=700))
    b.append(triple(470, 160, (2, 3, 4)))
    b.append(f"<rect x='455' y='145' width='78' height='30' rx='8' fill='none' stroke='{GREY}' "
             f"stroke-dasharray='4 3' stroke-width='2'/>")
    b.append(t(500, 196, 'ни в одной', 'var(--muted)', 13, weight=700))
    b.append(t(14, 254, '6 + 6 = 12, а троек 10', RED, 15, anchor='start', weight=700))
    return fig(svg(600, 266, ''.join(b), maxw=600))


# ——— Сумма строки: 32 кода по пяти играм, столбцами по числу единиц ———

def subsets():
    b = []
    cw, x0, y0 = 100, 14, 64
    for k in range(6):
        x = x0 + k * cw
        sets = list(combinations(range(5), k))
        b.append(t(x + 38, 20, f'игр {k}', 'var(--ink)', 13, weight=700))
        b.append(t(x + 38, 40, f'C(5, {k}) = {len(sets)}', GOLD, 13, weight=700))
        for r, s in enumerate(sets):
            y = y0 + r * 22
            for q in range(5):
                on = q in s
                letter, col = GAMES[q]
                b.append(f"<rect x='{x + q * 15}' y='{y}' width='13' height='17' rx='3' "
                         + (f"fill='{col}'/>" if on else "fill='none' stroke='var(--line)'/>"))
                b.append(t(x + q * 15 + 6.5, y + 13, '1' if on else '0', DARK if on else 'var(--muted)', 11,
                           weight=700 if on else None))
    b.append(t(x0, y0 + 10 * 22 + 26, '1 + 5 + 10 + 10 + 5 + 1 = 32 = 2⁵', 'var(--ink)', 14, anchor='start',
               weight=700))
    return fig(svg(x0 + 6 * cw, y0 + 10 * 22 + 38, ''.join(b), maxw=x0 + 6 * cw),
               'места кода — игры А, Б, В, Г, Д; 1 — игра взята')


# ——— Проверь себя: город 4 × 2, K закрыт ———

def check_task():
    x0, y0 = 40, 150
    b = [city(4, 2, x0, y0)]
    kx, ky = x0 + CC, y0 - CC
    b.append(f"<circle cx='{kx}' cy='{ky}' r='12' fill='var(--bg)' stroke='{RED}' stroke-width='2.5'/>"
             f"<path d='M{kx - 6} {ky - 6} L{kx + 6} {ky + 6} M{kx + 6} {ky - 6} L{kx - 6} {ky + 6}' "
             f"stroke='{RED}' stroke-width='2.5'/>" + t(kx + 16, ky - 12, 'K', RED, 15, anchor='start', weight=700))
    return fig(svg(330, 182, ''.join(b), maxw=330), 'перекрёсток K закрыт')


FIGS = {
    'Лусия идёт по парку от входа O к фонтану F': park_task,
    'В C ведут две дорожки: из A и из B.': park_small,
    'N(путей от входа в M) = 2 + 1 = 3': paths_m,
    'Заполняем перекрёстки снизу вверх.': park_fill,
    'N(путей к фонтану) = 10 + 5 = 15': park_last,
    'ни один способ не остался вне групп — вместе группы дают все способы': sum_rule,
    'Томас катается на санках с горы': sled_task,
    'N(путей) = 3 + 4 + 2 = 9': sled_filled,
    'Аня идёт по улицам из точки A в точку D': city_task,
    'Поэтому число в перекрёстке — сумма числа слева и числа снизу.': city_fill,
    'Продолжим строки вниз тем же сложением.': rotate,
    'Строки треугольника нумеруются сверху, начиная с нуля': tri_numbered,
    'Путь задаётся тем, какие k шагов из n идут вниз-вправо': tri_c,
    'N(троек) = N(троек с А) + N(троек без А) = 6 + 4 = 10': games_sort,
    'тройки {В, Г, Д} нет ни в одной группе': games_trap,
    'два числа, стоящие над C(n, k)': tri_rule,
    'В частности, у пяти игр Бори 2⁵ = 32 подмножества': subsets,
    'Сколько у Лусии путей из A в D?': check_task,
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
