#!/usr/bin/env python3
"""Рисунки учебника «Площади» (6 класс, пара 3) → math6_3_ploshchadi_uchebnik.vis.json (пишется целиком).

План и мысль каждого движения: 26-27/school6/vis/plan_ploshchadi.md.
Геометрия строится из координат (в сантиметрах или клетках, ось y вверх); длины и площади на рисунках
вычисляются из тех же координат и сверяются assert'ами с числами текста MD.

Запуск: python3 26-27/school6/vis/ploshchadi.py
"""
import json, math, os, re

from common import (svg, fig, row, t, g, rect, line, path, dot, label, right_angle, ticks, dim, cells, bar, brace,
                    height, turn, NumLine, GOLD, BLUE, GREEN, RED, VIOLET, CYAN, PINK, GREY, INK, MUTED, DARK)

HERE = os.path.dirname(os.path.abspath(__file__))
MDP = os.path.join(HERE, '..', 'math6_3_ploshchadi_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math6_3_ploshchadi_uchebnik.vis.json')
MD = open(MDP).read()


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', s)).strip()


CODE = [b for b in re.findall(r'```\n(.*?)```', MD, re.S)]
NS = "vector-effect='non-scaling-stroke'"


def need(*ss):
    """Строка действительно стоит в тексте MD (после снятия разметки)."""
    flat = norm(MD)
    for s in ss:
        assert s in flat, f'нет в MD: {s!r}'


def ascii_cover(anchor, body):
    """Замена ASCII: все буквы и числа блока стоят на SVG."""
    blk = [b for b in CODE if anchor in norm(b)]
    assert blk, f'нет ASCII-блока с {anchor!r}'
    texts = ' '.join(re.findall(r'>([^<>]+)</text>', body))
    for tok in re.findall(r'[A-Za-z]+|\d+', blk[0]):
        assert re.search(rf'(?<![A-Za-z0-9]){tok}(?![A-Za-z0-9])', texts), f'{anchor}: на SVG нет «{tok}»'


def area(pts):
    s = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


class G:
    """Перевод математических координат (y вверх) в экранные: x → ox + k·x, y → oy − k·y."""

    def __init__(self, k, ox, oy):
        self.k, self.ox, self.oy = k, ox, oy

    def __call__(self, p):
        return (round(self.ox + self.k * p[0], 1), round(self.oy - self.k * p[1], 1))

    def ps(self, pts):
        return [self(p) for p in pts]


def poly(pts, col, op=0.3, stroke=None, sw=2, dash=None, extra=''):
    return path(pts, stroke or col, sw, col, dash=dash, extra=f" fill-opacity='{op}'{extra}")


def tri(gm, pts, col, op=0.3, stroke=INK, sw=2, dash=None, extra=''):
    return poly(gm.ps(pts), col, op, stroke, sw, dash, extra)


def L(gm, p, s, center, fill=INK, size=16, d=14):
    return label(gm(p), s, gm(center), d, fill, size)


def cen(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def T(p, s, fill=INK, size=15, weight=600, anchor='middle'):
    return t(p[0], round(p[1] + size * 0.35, 1), s, fill, size, anchor=anchor, weight=weight)


def rsvg(w, h, body):
    """Рисунок в ряду row: не растягивать шире собственного размера (подписи не раздуваются на десктопе)."""
    return svg(w, h, body, maxw=w)


def fi(d, body):
    return g('fi', d, body)


def fo(d, body, o=0):
    return g('fo', d, body, f';--o:{o}')


def sl(d, dx, dy, body):
    return g('sl', d, body, f';--to:translate({dx}px,{dy}px)')


def wrap_to(c, d, to, body):
    """Копия body меняется CSS-преобразованием to вокруг точки c (как turn из common, но любое to)."""
    cx, cy = c
    return (f"<g transform='translate({cx:.1f},{cy:.1f})'><g class='sl' style='--d:{d}s;--to:{to}'>"
            f"<g transform='translate({-cx:.1f},{-cy:.1f})'>{body}</g></g></g>")


# ——— вводный раздел и ритуалы ———

def v1_perelozhit():
    need('Куски можно переложить по-другому: площадь от этого не меняется')
    c = 30
    A = [(i, j) for i in range(3) for j in range(2)]          # кусок 3 × 2 (клетки, j вниз)
    B = [(0, -1), (0, -2)]                                     # кусок 1 × 2 над левым столбцом
    def piece(x0, y0, cl, col):
        return ''.join(rect(x0 + i * c, y0 + j * c, c, c, col, INK, 1.2, extra=" fill-opacity='0.35'") for i, j in cl)
    def shape(x0, y0):
        return path([(x0, y0 - 2 * c), (x0 + c, y0 - 2 * c), (x0 + c, y0), (x0 + 3 * c, y0),
                     (x0 + 3 * c, y0 + 2 * c), (x0, y0 + 2 * c)], INK, 2.4)
    y0 = 84
    xl, xr = 30, 220
    cut = lambda x0: line(x0, y0, x0 + c, y0, BLUE, 3)
    b = [piece(xl, y0, A, GOLD), piece(xl, y0, B, BLUE), shape(xl, y0), cut(xl)]
    b.append(T((xl + 3 * c + 40, y0 + c), '→', MUTED, 26))
    b.append(piece(xr, y0, A, GOLD))
    # копия куска B переезжает: из столбца над левым краем — к правому краю, встаёт рядом с куском 3 × 2
    b.append(sl(0.6, 3 * c, 2 * c, piece(xr, y0, B, BLUE)))
    b.append(fi(2.0, rect(xr, y0, 4 * c, 2 * c, 'none', INK, 2.4)))
    return fig(svg(xr + 4 * c + 20, y0 + 2 * c + 16, ''.join(b)),
               'Переложили синий кусок — фигура другая, клеток столько же.', fx=True)


def r1_vysota():
    need('Наклонная сторона высотой не бывает')
    gm = G(28, 46, 140)
    A, B, C = (0, 0), (6, 0), (3.6, 3.6)
    def base(col):
        return tri(gm, [A, B, C], col, 0.12, INK, 2)
    hv, foot = height(gm(C), gm(A), gm(B), GREEN)
    ok = base(GREEN) + hv + T(gm((2.3, 0.75)), 'высота', GREEN, 15)
    ok += T((gm((3, 0))[0], 20), '✓', GREEN, 22)
    bad = base(RED) + path(gm.ps([A, C]), RED, 4, closed=False)
    mid = gm((1.8, 1.8))
    bad += T((mid[0] - 42, mid[1]), 'высота', RED, 15)
    bad += T((gm((3, 0))[0], 20), '✗', RED, 22)
    w, h = 224, 156
    return fig(row(rsvg(w, h, ok), rsvg(w, h, bad)), 'Высота встречает прямую основания под прямым углом; наклонная сторона — нет.')


# ——— глава 1 ———

def g1_diagonal():
    need('6 клеток на 3 клетки', '6 · 3 = 18')
    c, ox, oy = 40, 46, 34
    W, H = 6, 3
    assert W * H == 18
    A, B, Cc, D = (ox, oy), (ox + W * c, oy), (ox + W * c, oy + H * c), (ox, oy + H * c)
    b = [cells(ox, oy, W, H, c)]
    b.append(poly([A, B, Cc], GOLD, 0.35, INK, 2.2))
    b.append(poly([A, Cc, D], BLUE, 0.3, INK, 2.2))
    ctr = ((A[0] + Cc[0]) / 2, (A[1] + Cc[1]) / 2)
    b.append(turn(ctr, 180, poly([A, B, Cc], GOLD, 0.35, GOLD, 3, dash='7 5'), 0.6))
    for p, s in ((A, 'A'), (B, 'B'), (Cc, 'C'), (D, 'D')):
        b.append(label(p, s, ctr, 16))
    b.append(T((ox + W * c / 2, oy + H * c + 30), '6', MUTED, 15))
    b.append(T((ox + W * c + 30, oy + H * c / 2), '3', MUTED, 15))
    body = ''.join(b)
    ascii_cover('A · · · · · B', body)
    return fig(svg(ox + W * c + 50, oy + H * c + 46, body), 'Копия ABC после пол-оборота легла ровно на ACD.',
               fx=True, zamena=True)


def g1_any():
    need('Формула годится для любого прямоугольного треугольника', 'гипотенуза — диагональю')
    th = math.radians(20)
    u, v = (math.cos(th), -math.sin(th)), (-math.sin(th), -math.cos(th))
    R = (78, 206)
    a, bl = 220, 120
    P1 = (R[0] + a * u[0], R[1] + a * u[1])
    P2 = (R[0] + bl * v[0], R[1] + bl * v[1])
    P4 = (P1[0] + bl * v[0], P1[1] + bl * v[1])
    ctr = ((P1[0] + P2[0]) / 2, (P1[1] + P2[1]) / 2)
    b = [path([P1, P4, P2], BLUE, 2, closed=False, dash='7 5'),
         poly([R, P1, P2], GOLD, 0.3, INK, 2),
         path([R, P1], GOLD, 4, closed=False), path([R, P2], GOLD, 4, closed=False),
         right_angle(R, P1, P2, 14, INK)]
    ma = ((R[0] + P1[0]) / 2 + 12, (R[1] + P1[1]) / 2 + 22)
    mb = ((R[0] + P2[0]) / 2 - 44, (R[1] + P2[1]) / 2 + 4)
    b.append(T(ma, 'катет a', GOLD, 15))
    b.append(T(mb, 'катет b', GOLD, 15))
    b.append(T((ctr[0] + 4, ctr[1] - 14), 'гипотенуза', INK, 15))
    return fig(svg(330, 236, ''.join(b)), 'Вторая такая же половина достраивает любой прямоугольный треугольник до прямоугольника.')


def g1_task():
    need('Прямоугольный треугольник с катетами 8 см и 5 см', 'один катет тоже 5 см, а площадь 30 см²')
    k = 18
    def rt(a_px, b_px, la, lb, inside=None, col_a=INK, col_b=INK):
        x0, y0 = 30, 26 + 5 * k
        R, P, Q = (x0, y0), (x0 + a_px, y0), (x0, y0 - b_px)
        out = poly([R, P, Q], GOLD, 0.2, INK, 2) + right_angle(R, P, Q, 11, INK)
        out += T(((R[0] + P[0]) / 2, y0 + 18), la, col_a, 15) + T((x0 - 14, (R[1] + Q[1]) / 2), lb, col_b, 15)
        if inside:
            out += T((x0 + a_px * 0.3, y0 - b_px * 0.28), inside, GOLD, 14)
        return out
    a = t(20, 18, '(а)', MUTED, 15, anchor='start') + rt(8 * k, 5 * k, '8', '5')
    b2 = t(20, 18, '(б)', MUTED, 15, anchor='start') + rt(170, 5 * k, 'x', '5', 'S = 30', GOLD)
    h = 26 + 5 * k + 30
    return fig(row(rsvg(200, h, a), rsvg(215, h, b2)))


# ——— глава 2 ———

K2, L2, M2 = (0, 0), (2, 4), (6, 1)
W2, H2 = 6, 4
CORN = {  # угол → (вершины, цвет, катеты)
    'tl': ([(0, 4), L2, K2], VIOLET, (2, 4)),
    'tr': ([L2, (6, 4), M2], CYAN, (4, 3)),
    'br': ([M2, (6, 0), K2], PINK, (1, 6)),
}


def g2_grid(gm):
    return cells(gm((0, H2))[0], gm((0, H2))[1], W2, H2, gm.k)


def g2_task():
    need('Сторона клетки — 1 см. Найди площадь треугольника KLM')
    gm = G(40, 50, 40 + 40 * (H2 + 1))
    ctr = cen([K2, L2, M2])
    gx, gy = gm((-1, H2 + 1))
    b = [cells(gx, gy, W2 + 2, H2 + 2, gm.k), tri(gm, [K2, L2, M2], GOLD, 0.25, INK, 2.4)]
    for p, s in ((K2, 'K'), (L2, 'L'), (M2, 'M')):
        b += [dot(*gm(p), 4.5, INK), L(gm, p, s, ctr)]
    body = ''.join(b)
    ascii_cover('K · · · · · ·', body)
    return fig(svg(50 + 40 * (W2 + 1) + 20, 40 + 40 * (H2 + 2) + 10, body), zamena=True)


def g2_plan():
    need('Четвёртого нет: в левом нижнем углу стоит сама вершина K', 'Прямоугольник 6 × 4 клетки')
    gm = G(40, 56, 50 + 40 * H2)
    ctr = cen([K2, L2, M2])
    b = [g2_grid(gm), tri(gm, [K2, L2, M2], GOLD, 0.3, INK, 2.4)]
    x0, y0 = gm((0, H2))
    b.append(f"<path d='M{x0},{y0} h{W2 * 40} v{H2 * 40} h{-W2 * 40} Z' fill='none' stroke='{BLUE}' "
             f"stroke-width='3' pathLength='100' class='dr' style='--d:0.3s;--dur:1.6s'/>")
    b.append(fi(1.2, T((x0 + W2 * 20 + 40, y0 - 36), '6', BLUE, 15) + T((x0 - 44, y0 + H2 * 20), '4', BLUE, 15)))
    out = {'tl': (-24, -16), 'tr': (20, -20), 'br': (30, 12)}
    for key, (pts, col, _) in CORN.items():
        b.append(fi(2.0, sl(2.8, *out[key], tri(gm, pts, col, 0.45, col, 2))))
    for p, s in ((K2, 'K'), (L2, 'L'), (M2, 'M')):
        b.append(L(gm, p, s, ctr, size=15, d=22 if s == 'K' else 13))
    kx, ky = gm(K2)
    b.append(fi(2.0, f"<circle cx='{kx}' cy='{ky}' r='9' fill='none' stroke='{GOLD}' stroke-width='2.5'/>"
                + T((kx, ky + 32), 'угла нет', GOLD, 14)))
    return fig(svg(56 + 40 * W2 + 50, 50 + 40 * H2 + 50, ''.join(b)),
               'Обвели по сетке — между треугольником и прямоугольником три угла; вынули их — остался KLM.', fx=True)


def g2_legs():
    need('слева сверху — от L до вершины прямоугольника 2 клетки, от неё до K 4 клетки: 2 · 4 : 2 = 4',
         'справа сверху — от L до вершины прямоугольника 4 клетки, от неё до M 3 клетки: 4 · 3 : 2 = 6',
         'справа снизу — от M до вершины прямоугольника 1 клетка, от неё до K 6 клеток: 1 · 6 : 2 = 3',
         'S(KLM) = 24 − 4 − 6 − 3 = 11')
    areas = {}
    for key, (pts, col, (p, q)) in CORN.items():
        assert area(pts) == p * q / 2
        areas[key] = int(area(pts))
    assert W2 * H2 - sum(areas.values()) == area([K2, L2, M2]) == 11
    gm = G(40, 50, 40 + 40 * H2)
    ctr = cen([K2, L2, M2])
    b = [g2_grid(gm), tri(gm, [K2, L2, M2], GOLD, 0.15, INK, 2.2)]
    for key, (pts, col, _) in CORN.items():
        b.append(tri(gm, pts, col, 0.4, col, 2))
        cx, cy = gm(cen(pts))
        b.append(rect(cx - 15, cy - 13, 30, 26, DARK, col, 2, rx=5, extra=" fill-opacity='0.85'") + T((cx, cy), areas[key], INK, 17, 700))
    x0, y0 = gm((0, H2))
    b.append(rect(x0, y0, W2 * 40, H2 * 40, 'none', BLUE, 2.5))
    lab = [((1, 4), (0, 1), '2', VIOLET), ((0, 2), (-1, 0), '4', VIOLET), ((4, 4), (0, 1), '4', CYAN),
           ((6, 2.5), (1, 0), '3', CYAN), ((6, 0.5), (1, 0), '1', PINK), ((3, 0), (0, -1), '6', PINK)]
    for p, (dx, dy), s, col in lab:
        x, y = gm(p)
        b.append(T((x + dx * 16, y - dy * 16), s, col, 15, 500))
    for p, s in ((K2, 'K'), (L2, 'L'), (M2, 'M')):
        b.append(L(gm, p, s, ctr, size=15, d=13))
    return fig(svg(40 * W2 + 100, 40 * H2 + 80, ''.join(b)),
               'Катеты каждого угла лежат на сторонах прямоугольника — их длины видны по клеткам.')


def g2_trap():
    need('назвать «углом» кусок, который не прямоугольный треугольник (например, трапецию)',
         'Такой кусок сначала режут на прямоугольник и треугольник')
    P, Q, R, S = (0, 0), (6, 1), (3, 4), (3, 2)
    trap = [(0, 4), R, S, P]
    def base(gm):
        x0, y0 = gm((0, 4))
        return (cells(x0, y0, 6, 4, gm.k) + tri(gm, [P, Q, R, S], GOLD, 0.3, INK, 2.2)
                + rect(x0, y0, 6 * gm.k, 4 * gm.k, 'none', BLUE, 2))
    gl = G(30, 16, 30 + 120)
    left = base(gl) + tri(gl, trap, RED, 0.35, RED, 2.2) + T(gl((1.3, 2.8)), 'не угол', RED, 14)
    left += t(16 + 90, 20, '✗', RED, 20)
    gr = G(30, 16, 30 + 120)
    right = base(gr) + tri(gr, [(0, 4), R, S, (0, 2)], GREEN, 0.35, GREEN, 2) + tri(gr, [(0, 2), S, P], GREEN, 0.35, GREEN, 2)
    right += path(gr.ps([(0, 2), S]), BLUE, 3, closed=False)
    right += t(16 + 90, 20, '✓', GREEN, 20)
    w, h = 210, 168
    return fig(row(rsvg(w, h, left), rsvg(w, h, right)),
               'Вершина внутри прямоугольника — кусок у края не треугольник; разрез по сетке делит его на прямоугольник и угол.')


# ——— глава 3 ———

A3, H3, B3, C3 = (0, 0), (2, 0), (7, 0), (2, 4)


def g3_acute():
    need('AB = 7 см', 'CH = 4 см', 'AH = 2 см', 'HB = 5 см')
    assert dist(A3, H3) == 2 and dist(H3, B3) == 5 and dist(C3, H3) == 4 and dist(A3, B3) == 7
    gm = G(40, 40, 200)
    ctr = cen([A3, B3, C3])
    b = [tri(gm, [A3, H3, C3], GOLD, 0.3, INK, 0), tri(gm, [H3, B3, C3], BLUE, 0.28, INK, 0),
         tri(gm, [A3, B3, C3], GOLD, 0, INK, 2.2)]
    hv, foot = height(gm(C3), gm(A3), gm(B3), GOLD)
    b.append(hv)
    for p, s in ((A3, 'A'), (B3, 'B'), (C3, 'C')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(H3)[0], gm(H3)[1] + 18), 'H', INK, 16))
    b.append(dim(gm(A3), gm(H3), '2', -34))
    b.append(dim(gm(H3), gm(B3), '5', -34))
    b.append(T((gm((2, 2))[0] + 14, gm((2, 2))[1]), '4', GOLD, 16))
    body = ''.join(b)
    ascii_cover('A ──H', body)
    return fig(svg(360, 254, body), zamena=True)


A3o, B3o, H3o, C3o = (0, 0), (6, 0), (9, 0), (9, 4)


def g3_obtuse_geo(k=32, ox=30, oy=170):
    return G(k, ox, oy)


def g3_obtuse():
    need('AB = 6 см', 'CH = 4 см, BH = 3 см')
    assert dist(A3o, B3o) == 6 and dist(B3o, H3o) == 3 and dist(C3o, H3o) == 4
    gm = g3_obtuse_geo()
    ctr = cen([A3o, B3o, C3o])
    hv, foot = height(gm(C3o), gm(A3o), gm(B3o), GOLD)
    assert dist(foot, gm(H3o)) < 0.5
    b = [tri(gm, [A3o, B3o, C3o], GOLD, 0.25, INK, 2.2), hv]
    for p, s in ((A3o, 'A'), (B3o, 'B'), (C3o, 'C')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(H3o)[0] + 14, gm(H3o)[1] + 6), 'H', INK, 16))
    b.append(dim(gm(A3o), gm(B3o), '6', -30))
    b.append(dim(gm(B3o), gm(H3o), '3', -30))
    b.append(T((gm((9, 2))[0] + 16, gm((9, 2))[1]), '4', GOLD, 16))
    body = ''.join(b)
    ascii_cover('B ┄┄┄┄ H', body)
    return fig(svg(360, 222, body), zamena=True)


def g3_minus():
    need('S(ABC) = S(AHC) − S(BHC)')
    assert area([A3o, H3o, C3o]) - area([B3o, H3o, C3o]) == area([A3o, B3o, C3o]) == 12
    gm = G(32, 30, 170)
    ctr = cen([A3o, B3o, C3o])
    hv, _ = height(gm(C3o), gm(A3o), gm(B3o), GOLD)
    b = [tri(gm, [A3o, B3o, C3o], GOLD, 0.3, INK, 0)]
    b.append(fi(2.4, tri(gm, [A3o, B3o, C3o], GREEN, 0.45, GREEN, 0)))
    # копия BHC (часть большого AHC) выезжает вправо и сереет
    piece = tri(gm, [B3o, H3o, C3o], GOLD, 0.3, INK, 0)
    grey = tri(gm, [B3o, H3o, C3o], GREY, 0.45, GREY, 2, dash='6 4')
    b.append(sl(1.0, 112, 0, fo(1.0, piece) + fi(1.0, grey)))
    b.append(tri(gm, [A3o, H3o, C3o], 'none', 0, INK, 2.2) + path(gm.ps([B3o, C3o]), INK, 2.2, closed=False))
    b.append(hv)
    for p, s in ((A3o, 'A'), (B3o, 'B'), (C3o, 'C')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(H3o)[0] - 2, gm(H3o)[1] + 18), 'H', INK, 16))
    return fig(svg(450, 200, ''.join(b)), 'Из прямоугольного AHC убрали прямоугольный BHC — остался ABC.', fx=True)


def g3_bc():
    need('сторона BC = 5 см', 'перпендикуляр из A на прямую BC', 'h = 24 : 5 = 4,8')
    assert dist(B3o, C3o) == 5
    gm = G(30, 30, 140)
    ctr = cen([A3o, B3o, C3o])
    hv, foot = height(gm(A3o), gm(B3o), gm(C3o), GOLD, label='h')
    # основание высоты к BC — вне отрезка BC, на продолжении за B
    fm = ((foot[0] - gm.ox) / gm.k, (gm.oy - foot[1]) / gm.k)
    assert abs(dist(fm, A3o) - 4.8) < 0.01 and fm[1] < 0
    hc, _ = height(gm(C3o), gm(A3o), gm(B3o), GREY, ext=GREY)
    b = [tri(gm, [A3o, B3o, C3o], GOLD, 0.15, INK, 2), hc,
         path(gm.ps([B3o, C3o]), GOLD, 4.5, closed=False), hv]
    for p, s in ((A3o, 'A'), (B3o, 'B'), (C3o, 'C')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(H3o)[0] + 14, gm(H3o)[1] + 6), 'H', GREY, 15))
    mbc = gm(((B3o[0] + C3o[0]) / 2, (B3o[1] + C3o[1]) / 2))
    b.append(T((mbc[0] + 18, mbc[1] + 4), '5', GOLD, 16))
    return fig(svg(340, 240, ''.join(b)), 'Высота к BC тоже падает на продолжение — за точку B.')


# ——— глава 4 ———

def g4_general():
    need('Тогда высота у них одна и та же — перпендикуляр из общей вершины на эту прямую')
    gm = G(36, 26, 170)
    V = (8.4, 3.6)
    b1, b2 = ((0.4, 0), (3.2, 0)), ((3.8, 0), (6.8, 0))
    b = [line(gm((-0.4, 0))[0], gm((0, 0))[1], gm((10, 0))[0], gm((0, 0))[1], MUTED, 1.5)]
    b.append(tri(gm, [b1[0], b1[1], V], GOLD, 0.25, GOLD, 1.8))
    b.append(tri(gm, [b2[0], b2[1], V], CYAN, 0.22, CYAN, 1.8))
    b.append(path(gm.ps(b1), GOLD, 5, closed=False) + path(gm.ps(b2), CYAN, 5, closed=False))
    hv, _ = height(gm(V), gm((-0.4, 0)), gm((10, 0)), GREEN, label='')
    b.append(hv + dot(*gm(V), 4.5, INK))
    b.append(T((gm(V)[0] + 34, gm((0, 1.8))[1]), 'одна', GREEN, 16) + T((gm(V)[0] + 36, gm((0, 1.8))[1] + 18), 'высота', GREEN, 16))
    return fig(svg(420, 196, ''.join(b)), 'Перпендикуляр из общей вершины — высота обоих треугольников, даже если он падает мимо оснований.')


def g4_ratio():
    need('основания 2 см и 8 см, общая высота 5 см', 'S₁ : S₂ = 5 : 20 = 1 : 4', 'Возьму другую общую высоту, 3 см',
         'S₁ : S₂ = 3 : 12 = 1 : 4')
    a1, a2 = 2, 8
    h1, h2 = 5, 3
    s = lambda a, h: a * h // 2
    assert (s(a1, h1), s(a2, h1), s(a1, h2), s(a2, h2)) == (5, 20, 3, 12)
    gm = G(30, 40, 196)
    V = (3.5, h1)
    yb = gm((0, 0))[1]
    pts1, pts2 = [(0, 0), (a1, 0), V], [(a1, 0), (a1 + a2, 0), V]
    ghost = tri(gm, pts1, GREY, 0, GREY, 1.4, dash='5 4') + tri(gm, pts2, GREY, 0, GREY, 1.4, dash='5 4')
    hgt = path(gm.ps([V, (V[0], 0)]), GOLD, 2, closed=False, dash='5 4', extra=f' {NS}')
    moving = (poly(gm.ps(pts1), GOLD, 0.3, INK, 2, extra=f' {NS}') + poly(gm.ps(pts2), CYAN, 0.25, INK, 2, extra=f' {NS}')
              + hgt)
    b = [ghost, wrap_to((0, yb), 0.8, f'scale(1,{h2 / h1})', moving),
         right_angle(gm((V[0], 0)), gm(V), gm((a1 + a2, 0)), 10, GOLD)]
    b.append(T((gm((a1 / 2, 0))[0], yb + 19), '2', GOLD, 18) + T((gm((a1 + a2 / 2, 0))[0], yb + 19), '8', CYAN, 18))
    hx = gm(V)[0] + 16
    b.append(fo(0.8, T((hx, gm((0, h1 / 2))[1]), '5', GOLD, 18)) + fi(2.0, T((hx, gm((0, h2 / 2))[1]), '3', GOLD, 18)))
    yl = yb + 50
    b.append(fo(0.8, T((90, yl), f'S₁ = {s(a1, h1)}', GOLD, 18) + T((210, yl), f'S₂ = {s(a2, h1)}', CYAN, 18)))
    b.append(fi(2.0, T((90, yl), f'S₁ = {s(a1, h2)}', GOLD, 18) + T((210, yl), f'S₂ = {s(a2, h2)}', CYAN, 18)))
    b.append(T((340, yl), 'S₁ : S₂ = 1 : 4', GREEN, 18))
    return fig(svg(420, yl + 16, ''.join(b)), 'Вершину опустили: обе площади стали меньше, отношение осталось.', fx=True)


A4, C4, D4, B4 = (0, 0), (10, 0), (4, 0), (6.2, 5)


def g4_geo():
    return G(32, 30, 190)


def g4_task():
    need('AD : DC = 2 : 3')
    assert dist(A4, D4) / dist(D4, C4) == 2 / 3
    gm = g4_geo()
    ctr = cen([A4, B4, C4])
    b = [tri(gm, [A4, B4, C4], GOLD, 0.15, INK, 2.2), path(gm.ps([B4, D4]), INK, 2.2, closed=False)]
    for p, s in ((A4, 'A'), (B4, 'B'), (C4, 'C')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(D4)[0], gm(D4)[1] + 18), 'D', INK, 16))
    yb = gm(A4)[1] + 44
    b.append(T((gm((2, 0))[0], yb), '2', GOLD, 16) + T((gm(D4)[0], yb), ':', MUTED, 16) + T((gm((7, 0))[0], yb), '3', BLUE, 16))
    body = ''.join(b)
    ascii_cover('A ───── D', body)
    return fig(svg(390, 246, body), zamena=True)


def g4_plan():
    need('Сам отрезок BD наклонный, это не высота')
    gm = g4_geo()
    ctr = cen([A4, B4, C4])
    hv, foot = height(gm(B4), gm(A4), gm(C4), GREEN)
    assert abs(foot[0] - gm(D4)[0]) > 20                       # высота не совпадает с BD
    b = [tri(gm, [A4, B4, D4], GOLD, 0.3, INK, 2), tri(gm, [D4, B4, C4], BLUE, 0.28, INK, 2), hv,
         path(gm.ps([B4, D4]), RED, 3, closed=False)]
    for p, s in ((A4, 'A'), (B4, 'B'), (C4, 'C')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(D4)[0], gm(D4)[1] + 18), 'D', INK, 16))
    b.append(T(gm((3.3, 1.5)), 'не высота', RED, 14))
    b.append(T((foot[0] + 40, gm((0, 1.6))[1]), 'высота', GREEN, 14))
    return fig(svg(390, 220, ''.join(b)), 'У ABD и DBC одна высота — перпендикуляр из B на AC.')


def g4_bar():
    need('S(ABD) — это 2 равные части, S(DBC) — 3 такие же части', 'На одну часть приходится 40 : 5 = 8')
    S, n, part = 40, 5, 40 // 5
    assert part * 2 == 16 and part * 3 == 24
    x, y, w, h = 20, 50, 330, 40
    b = [bar(x, y, w, h, n, filled=(2, 3, 4), fill=BLUE), bar(x, y, w, h, n, filled=(0, 1), fill=GOLD)]
    pw = w / n
    b += [T((x + (k + 0.5) * pw, y + h / 2), part, DARK, 16, 700) for k in range(n)]
    b.append(brace(x, x + w, y - 4, str(S), up=True, col=MUTED, fill=INK, size=16))
    b.append(brace(x, x + 2 * pw, y + h + 4, '2 части', up=False, col=GOLD, fill=GOLD, size=16))
    b.append(brace(x + 2 * pw, x + w, y + h + 4, '3 части', up=False, col=BLUE, fill=BLUE, size=16))
    return fig(svg(370, 140, ''.join(b)))


def g4_median():
    need('Отрезок из вершины треугольника в середину противоположной стороны называется медианой')
    gm = G(24, 20, 172)
    A, C, B = (0, 0), (8, 0), (5.6, 5)
    def one(Dx, col, ok):
        D = (Dx, 0)
        ctr = cen([A, B, C])
        out = tri(gm, [A, B, D], col, 0.3 if ok else 0.3, INK, 2)
        out += tri(gm, [D, B, C], col if ok else BLUE, 0.3 if ok else 0.25, INK, 2)
        out += path(gm.ps([B, D]), col, 3.2, closed=False)
        for p, s in ((A, 'A'), (B, 'B'), (C, 'C')):
            out += L(gm, p, s, ctr, size=15)
        out += T((gm(D)[0], gm(D)[1] + 18), 'D', INK, 15)
        if ok:
            out += ticks(gm(A), gm(D), 1, GREEN) + ticks(gm(D), gm(C), 1, GREEN)
            out += t(110, 20, '✓ медиана', GREEN, 15)
        else:
            yb = gm(A)[1] + 38
            out += T((gm((Dx / 2, 0))[0], yb), '2', col, 15) + T((gm(D)[0], yb), ':', MUTED, 15) + T((gm(((Dx + 8) / 2, 0))[0], yb), '3', BLUE, 15)
            out += t(110, 20, '✗ не медиана', RED, 15)
        return out
    assert abs(3.2 / (8 - 3.2) - 2 / 3) < 1e-9
    return fig(row(rsvg(220, 220, one(4, GREEN, True)), rsvg(220, 220, one(3.2, RED, False))),
               'Медиана приходит в середину стороны — две половины с равными основаниями и общей высотой.')


def g4_two_lines():
    need('Высота одна только тогда, когда вершина общая, а основания на одной прямой')
    gm = G(32, 20, 170)
    V = (5, 4.2)
    l1 = ((-0.3, 0), (6, 0))
    l2 = ((5.6, -0.4), (8.2, 4.8))
    b1 = ((0.6, 0), (3.6, 0))
    def on2(s):
        return (l2[0][0] + s * (l2[1][0] - l2[0][0]), l2[0][1] + s * (l2[1][1] - l2[0][1]))
    b2 = (on2(0.25), on2(0.75))
    b = [path(gm.ps(l1), MUTED, 1.5, closed=False), path(gm.ps(l2), MUTED, 1.5, closed=False)]
    b.append(tri(gm, [b1[0], b1[1], V], GOLD, 0.25, GOLD, 1.8) + tri(gm, [b2[0], b2[1], V], CYAN, 0.22, CYAN, 1.8))
    b.append(path(gm.ps(b1), GOLD, 5, closed=False) + path(gm.ps(b2), CYAN, 5, closed=False))
    h1, f1 = height(gm(V), gm(l1[0]), gm(l1[1]), RED)
    h2, f2 = height(gm(V), gm(l2[0]), gm(l2[1]), RED)
    assert abs(dist(f1, gm(V)) - dist(f2, gm(V))) > 25          # высоты видимо разные
    b += [h1, h2, dot(*gm(V), 4.5, INK)]
    return fig(svg(400, 200, ''.join(b)), 'Основания на разных прямых — из общей вершины две разные высоты.')


# ——— глава 5 ———

def g5_general():
    need('При общем основании площади относятся как высоты')
    gm = G(36, 30, 160)
    P, Q = (0, 0), (6, 0)
    V1, V2 = (1.6, 3.6), (8.2, 2.0)
    b = [tri(gm, [P, Q, V1], GOLD, 0.25, GOLD, 1.8), tri(gm, [P, Q, V2], CYAN, 0.22, CYAN, 1.8),
         path(gm.ps([P, Q]), INK, 4, closed=False)]
    h1, f1 = height(gm(V1), gm(P), gm(Q), GOLD)
    h2, f2 = height(gm(V2), gm(P), gm(Q), CYAN, ext=MUTED)
    b += [h1, h2]
    b.append(T((gm(V1)[0] - 20, (gm(V1)[1] + f1[1]) / 2), 'h₁', GOLD, 19))
    b.append(T((gm(V2)[0] + 22, (gm(V2)[1] + f2[1]) / 2), 'h₂', CYAN, 19))
    b.append(T((gm((3, 0))[0], gm(P)[1] + 20), 'a', INK, 16))
    return fig(svg(400, 190, ''.join(b)), 'Основание одно, высоты две: вторая падает на продолжение основания.')


A5, C5, B5, D5 = (0, 0), (10, 0), (3.4, 3), (6.4, -5)


def g5_quad(gm, Bp=B5, numbers=True):
    ctr = cen([A5, Bp, C5, D5])
    b = [path(gm.ps([A5, Bp, C5, D5]), INK, 2.2), path(gm.ps([A5, C5]), INK, 2, closed=False)]
    h1, f1 = height(gm(Bp), gm(A5), gm(C5), GOLD)
    h2, f2 = height(gm(D5), gm(A5), gm(C5), CYAN)
    b += [h1, h2]
    if numbers:
        b.append(T((f1[0] - 14, (gm(Bp)[1] + f1[1]) / 2), '3', GOLD, 17))
        b.append(T((f2[0] + 14, (gm(D5)[1] + f2[1]) / 2), '5', CYAN, 17))
    for p, s in ((A5, 'A'), (Bp, 'B'), (C5, 'C'), (D5, 'D')):
        b.append(L(gm, p, s, ctr if p != Bp or Bp[1] > 0 else (Bp[0], Bp[1] - 3), size=15))
    return ''.join(b)


def g5_task():
    need('диагональ AC = 10 см', 'Вершина B отстоит от прямой AC на 3 см, вершина D — на 5 см, по другую сторону')
    assert dist(A5, C5) == 10 and B5[1] == 3 and D5[1] == -5
    gm = G(30, 34, 124)
    body = g5_quad(gm) + T((gm((4.4, 0))[0], gm((0, 0))[1] + 18), 'AC = 10', INK, 16)
    ascii_cover('A ────┴─┬', body)
    return fig(svg(380, 300, body), zamena=True)


def g5_side():
    need('S(ABCD) = 15 + 25 = 40', 'площади вычитают, 25 − 15 = 10')
    Bin = (4.6, -3)
    # Bin — по ту же сторону от AC, что D, и внутри треугольника ACD
    yAD = D5[1] / D5[0] * Bin[0]
    assert Bin[1] < 0 and yAD < Bin[1]
    assert area([A5, C5, B5]) == 15 and area([A5, C5, D5]) == 25 and area([A5, Bin, C5, D5]) == 10
    gm = G(18, 16, 96)
    left = (tri(gm, [A5, B5, C5], GOLD, 0.35, GOLD, 0) + tri(gm, [A5, C5, D5], BLUE, 0.3, BLUE, 0) + g5_quad(gm, numbers=False)
            + T(gm((6.2, 1.0)), '15', GOLD, 15, 700) + T(gm(cen([A5, C5, D5])), '25', BLUE, 15, 700)
            + T((106, 214), '15 + 25 = 40', GREEN, 15))
    right = (tri(gm, [A5, Bin, C5, D5], GOLD, 0.35, INK, 2.2)
             + tri(gm, [A5, C5, Bin], GREY, 0.35, GREY, 1.8, dash='5 4') + path(gm.ps([A5, C5]), GREY, 1.4, closed=False)
             + T(gm((5.6, -1.0)), '15', INK, 15, 700) + T(gm((6.4, -3.6)), '10', GOLD, 15, 700)
             + T((106, 214), '25 − 15 = 10', RED, 15))
    for p, s in ((A5, 'A'), (Bin, 'B'), (C5, 'C'), (D5, 'D')):
        right += L(gm, p, s, (5, -1) if p != Bin else (Bin[0], -10), size=15)
    return fig(row(rsvg(212, 226, left), rsvg(212, 226, right)),
               'Справа B и D по одну сторону от AC: диагональ не режет фигуру, и ABC вырезан из ACD.')


# ——— глава 6 ———

def g6_slide():
    need('Все точки прямой, параллельной основанию, отстоят от основания на одно и то же расстояние',
         'куда бы ни уехала вершина')
    gm = G(32, 30, 150)
    P, Q, V = (0, 0), (4.4, 0), (1.2, 3.2)
    shift = 6.0
    yb = gm(P)[1]
    b = [path(gm.ps([(-0.4, 3.2), (11.6, 3.2)]), MUTED, 1.5, closed=False),
         path(gm.ps([(-0.4, 0), (11.6, 0)]), MUTED, 1.2, closed=False, dash='3 5')]
    b.append(tri(gm, [P, Q, V], GREY, 0.12, GREY, 1.6, dash='5 4'))
    b.append(path(gm.ps([V, (V[0], 0)]), GREY, 1.4, closed=False, dash='5 4'))
    # сдвиг вдоль основания: skewX вокруг прямой основания двигает вершину по параллельной, основание стоит
    ang = -math.degrees(math.atan(shift / V[1]))
    b.append(wrap_to((0, yb), 0.6, f'skewX({ang:.2f}deg)', poly(gm.ps([P, Q, V]), GOLD, 0.35, INK, 2, extra=f' {NS}')))
    hgt = path(gm.ps([V, (V[0], 0)]), GOLD, 2.2, closed=False, dash='5 4') + right_angle(gm((V[0], 0)), gm(V), gm(Q), 10, GOLD)
    b.append(sl(0.6, round(shift * gm.k, 1), 0, hgt))
    b.append(path(gm.ps([P, Q]), INK, 4, closed=False))
    return fig(svg(430, 176, ''.join(b)), 'Вершина едет по параллельной прямой — высота не меняется, площадь тоже.', fx=True)


A6, D6, C6, B6, P6 = (0, 0), (10, 0), (10, 6), (0, 6), (3.2, 6)


def g6_rect(gm):
    ctr = (5, 3)
    b = [path(gm.ps([A6, B6, C6, D6]), INK, 2.2), path(gm.ps([A6, P6, D6]), INK, 2, closed=False)]
    for p, s in ((A6, 'A'), (B6, 'B'), (C6, 'C'), (D6, 'D')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(P6)[0], gm(P6)[1] - 16), 'P', INK, 16))
    return ''.join(b)


def g6_task():
    need('Прямоугольник ABCD со сторонами AD = 10 см и AB = 6 см. Точка P — где угодно на стороне BC')
    gm = G(30, 40, 216)
    body = g6_rect(gm) + dim(gm(D6), gm(A6), '10', 22) + dim(gm(A6), gm(B6), '6', 22)
    ascii_cover('B ───── P', body)
    return fig(svg(380, 270, body), zamena=True)


def g6_plan():
    need('поэтому это расстояние равно AB = 6', 'S(APD) = 10 · 6 : 2 = 30', 'S(ABP) + S(PCD) = 60 − 30 = 30')
    assert area([A6, P6, D6]) == 30 and area([A6, B6, P6]) + area([P6, C6, D6]) == 30
    gm = G(30, 40, 216)
    hv, foot = height(gm(P6), gm(A6), gm(D6), GOLD)
    b = [tri(gm, [A6, P6, D6], GOLD, 0.3, INK, 0), tri(gm, [A6, B6, P6], BLUE, 0.25, INK, 0),
         tri(gm, [P6, C6, D6], BLUE, 0.25, INK, 0), g6_rect(gm), hv,
         path(gm.ps([A6, B6]), GOLD, 4, closed=False),
         ticks(gm(A6), gm(B6), 2, GOLD), ticks(foot, gm(P6), 2, GOLD), dim(gm(A6), gm(B6), '6', 22)]
    return fig(svg(380, 250, ''.join(b)), 'Высота APD из P и сторона AB — оба отрезка между параллельными BC и AD.')


A6t, D6t, B6t, C6t = (0, 0), (10, 0), (2, 5), (6.6, 5)


def inter(p1, p2, p3, p4):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a, b = x1 * y2 - y1 * x2, x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / den, (a * (y3 - y4) - (y1 - y2) * b) / den)


O6 = inter(A6t, C6t, B6t, D6t)


def g6_trap_task():
    need('У трапеции ABCD основания AD и BC параллельны. Диагонали AC и BD пересекаются в точке O')
    assert B6t[1] == C6t[1] and B6t[0] != D6t[0] - C6t[0]            # AD ∥ BC, трапеция не равнобокая
    assert abs(area([A6t, O6, B6t]) - area([C6t, O6, D6t])) < 1e-9
    gm = G(32, 36, 200)
    ctr = (5, 2.5)
    b = [path(gm.ps([A6t, B6t, C6t, D6t]), INK, 2.2), path(gm.ps([A6t, C6t]), INK, 1.8, closed=False),
         path(gm.ps([B6t, D6t]), INK, 1.8, closed=False), dot(*gm(O6), 4, INK)]
    for p, s in ((A6t, 'A'), (B6t, 'B'), (C6t, 'C'), (D6t, 'D')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(O6)[0], gm(O6)[1] - 16), 'O', INK, 16))
    body = ''.join(b)
    ascii_cover("' O '", body)
    return fig(svg(400, 230, body), zamena=True)


def g6_trap_minus():
    need('S(AOB) = S(ABD) − S(AOD) = S(ACD) − S(AOD) = S(COD)')
    def one(which):
        gm = G(20, 16, 130)
        ctr = (5, 2.5)
        keep, was, now = (([A6t, B6t, O6], 'S(ABD)', 'S(AOB)') if which == 'B'
                          else ([C6t, D6t, O6], 'S(ACD)', 'S(COD)'))
        out = tri(gm, keep, GOLD, 0.35, GOLD, 0)
        out += fo(1.0, tri(gm, [A6t, O6, D6t], GOLD, 0.35, GOLD, 0), 0)
        out += fi(1.0, tri(gm, [A6t, O6, D6t], GREY, 0, GREY, 1.8, dash='5 4'))
        out += fi(2.2, tri(gm, keep, GREEN, 0.5, GREEN, 2.2))
        out += path(gm.ps([A6t, B6t, C6t, D6t]), INK, 2) + path(gm.ps([A6t, C6t]), MUTED, 1.2, closed=False)
        out += path(gm.ps([B6t, D6t]), MUTED, 1.2, closed=False)
        for p, s in ((A6t, 'A'), (B6t, 'B'), (C6t, 'C'), (D6t, 'D')):
            out += L(gm, p, s, ctr, size=15, d=13)
        out += T((gm(O6)[0], gm(O6)[1] + (16 if which == 'B' else -15)), 'O', INK, 14)
        x = gm((5, 0))[0]
        out += fo(1.0, T((x, 162), was, GOLD, 15), 0) + fi(2.2, T((x, 162), now, GREEN, 15))
        return rsvg(232, 176, out)
    return fig(row(one('B'), one('C'), gap=32),
               'Из равных ABD и ACD убрали общий AOD — остались AOB и COD, равные по площади.', fx=True)


# ——— глава 7 ———

def g7_cells():
    need('Прямоугольник 5x × 3x складывается из квадратиков x × x: 5 штук в ряду, 3 ряда', '5x · 3x = 15x²')
    c, x0, y0 = 40, 50, 40
    b = [cells(x0, y0, 5, 3, c, '#4a5a70', {(0, 0): GOLD}), rect(x0, y0, 5 * c, 3 * c, 'none', INK, 2.2)]
    b.append(T((x0 + c / 2, y0 + c / 2), 'x²', DARK, 16, 700))
    b.append(T((x0 + 5 * c / 2, y0 - 16), '5x', INK, 16) + T((x0 - 20, y0 + 3 * c / 2), '3x', INK, 16))
    b.append(T((x0 + c / 2, y0 + 3 * c + 16), 'x', GOLD, 15))
    b.append(line(x0, y0 + 3 * c + 4, x0 + c, y0 + 3 * c + 4, GOLD, 3))
    return fig(svg(300, 200, ''.join(b)))


def g7_half():
    need('Прямоугольный треугольник с катетами 2x и 2x — половина квадрата 2x × 2x, а в нём 2 · 2 = 4 квадратика',
         '2x · 2x : 2 = 4x² : 2 = 2x²')
    c, x0, y0 = 54, 60, 24
    b = [cells(x0, y0, 2, 2, c, '#4a5a70'), poly([(x0, y0), (x0, y0 + 2 * c), (x0 + 2 * c, y0 + 2 * c)], GOLD, 0.4, INK, 2.2),
         poly([(x0, y0), (x0 + 2 * c, y0), (x0 + 2 * c, y0 + 2 * c)], GREY, 0.15, GREY, 1.5),
         right_angle((x0, y0 + 2 * c), (x0, y0), (x0 + 2 * c, y0 + 2 * c), 11, INK)]
    b.append(T((x0 + 0.62 * c, y0 + 1.42 * c), '2x²', DARK, 16, 700))
    b.append(T((x0 + c, y0 + 2 * c + 18), '2x', INK, 15) + T((x0 - 20, y0 + c), '2x', INK, 15))
    return fig(svg(240, 160, ''.join(b)))


def g7_task():
    need('прямоугольник со сторонами 5x и 3x, у которого в правом нижнем углу вырезан прямоугольник 2x × x',
         'в прямоугольнике 15 клеток, вырезано 2')
    blk = [b for b in CODE if 'L' not in b and 'A' not in b and 'K' not in b]
    assert len(blk) == 1
    rows = [r.split() for r in blk[0].strip('\n').split('\n')]
    assert [len(r) for r in rows] == [6, 6, 6, 4]          # узлы: 5 × 3 клетки, вырезан угол 2 × 1
    c, x0, y0 = 40, 50, 40
    keep = {(i, j): GOLD for i in range(5) for j in range(3) if not (j == 2 and i >= 3)}
    assert 5 * 3 - len(keep) == 2
    b = [cells(x0, y0, 5, 3, c, '#4a5a70', keep).replace(f"fill='{GOLD}'", f"fill='{GOLD}' fill-opacity='0.3'"),
         rect(x0 + 3 * c, y0 + 2 * c, 2 * c, c, GREY, GREY, 1.8, extra=" fill-opacity='0.25' stroke-dasharray='5 4'"),
         path([(x0, y0), (x0 + 5 * c, y0), (x0 + 5 * c, y0 + 2 * c), (x0 + 3 * c, y0 + 2 * c), (x0 + 3 * c, y0 + 3 * c),
               (x0, y0 + 3 * c)], INK, 2.4)]
    b.append(T((x0 + 2.5 * c, y0 - 16), '5x', INK, 16) + T((x0 - 20, y0 + 1.5 * c), '3x', INK, 16))
    b.append(T((x0 + 4 * c, y0 + 3 * c + 16), '2x', GREY, 15) + T((x0 + 5 * c + 16, y0 + 2.5 * c), 'x', GREY, 15))
    return fig(svg(300, 210, ''.join(b)), zamena=True)


def g7_scale():
    need('Квадрат со стороной 3 см имеет площадь 9 см²', 'сторона станет 6 см, площадь 36 см²',
         'становится квадратом 2 × 2, а в нём 2 · 2 = 4 квадратика', '9 · 4 = 36')
    n, k, c = 3, 2, 26
    assert n * n * k * k == 36
    xl, y0, xr = 40, 40, 190
    left = cells(xl, y0, n, n, c, '#4a5a70', {(0, 0): GOLD}) + rect(xl, y0, n * c, n * c, 'none', INK, 2.2)
    left += T((xl + n * c / 2, y0 - 14), '3', INK, 15) + T((xl + n * c / 2, y0 + n * c + 22), '9 см²', MUTED, 15)
    big = (cells(xr, y0, n, n, c, '#4a5a70', {(0, 0): GOLD}).replace('<line', f'<line {NS}').replace("<rect", f"<rect {NS}")
           + f"<rect {NS} x='{xr}' y='{y0}' width='{n * c}' height='{n * c}' fill='none' stroke='{INK}' stroke-width='2.2'/>")
    b = [left, T((xl + n * c + 36, y0 + n * c / 2), '→', MUTED, 26),
         wrap_to((xr, y0), 0.6, f'scale({k})', big)]
    fine = ''.join(line(xr + i * c, y0, xr + i * c, y0 + n * k * c, '#6b7c92', 1, " stroke-dasharray='3 3'")
                   for i in range(1, n * k, 2))
    fine += ''.join(line(xr, y0 + j * c, xr + n * k * c, y0 + j * c, '#6b7c92', 1, " stroke-dasharray='3 3'")
                    for j in range(1, n * k, 2))
    # клетка-образ 2 × 2: её внутренние линии тёмные и сплошные, чтобы четыре квадратика читались на золоте
    inner = line(xr + c, y0, xr + c, y0 + 2 * c, DARK, 2.2) + line(xr, y0 + c, xr + 2 * c, y0 + c, DARK, 2.2)
    b.append(fi(2.1, fine + inner + rect(xr, y0, k * c, k * c, 'none', GOLD, 2.4)))
    b.append(fi(2.6, T((xr + n * k * c / 2, y0 - 14), '6', INK, 15)
                + T((xr + n * k * c / 2, y0 + n * k * c + 22), '36 см²', GREEN, 15)))
    return fig(svg(xr + n * k * c + 30, y0 + n * k * c + 34, ''.join(b)),
               'Растянули вдвое вдоль и поперёк — каждая клетка стала четырьмя.', fx=True)


def g7_len_area():
    need('2x — это два куска длины, x² — один квадратик площади', 'x² = 4 · 4 = 16 см², а 2x = 8')
    x, k = 4, 20
    assert 2 * x == 8 and x * x == 16
    x0, y0 = 20, 60
    seg = (line(x0, y0, x0 + 2 * x * k, y0, CYAN, 4) + ''.join(line(x0 + i * x * k, y0 - 8, x0 + i * x * k, y0 + 8, CYAN, 2)
                                                               for i in range(3))
           + T((x0 + x * k / 2, y0 - 18), 'x', CYAN, 15) + T((x0 + 1.5 * x * k, y0 - 18), 'x', CYAN, 15)
           + T((x0 + x * k, y0 + 32), '2x = 8 см', CYAN, 15) + T((x0 + x * k, y0 + 52), 'длина', MUTED, 14))
    sq = (cells(40, 20, x, x, k, '#4a5a70') + rect(40, 20, x * k, x * k, GOLD, GOLD, 2.2, extra=" fill-opacity='0.3'")
          + T((40 + x * k / 2, 20 + x * k + 22), 'x² = 16 см²', GOLD, 15) + T((40 + x * k / 2, 20 + x * k + 42), 'площадь', MUTED, 14)
          + T((26, 20 + x * k / 2), 'x', GOLD, 15))
    return fig(row(rsvg(200, 160, seg), rsvg(170, 160, sq)))


# ——— глава 8 ———

def g8_squeeze():
    need('20² = 400, 30² = 900', 'корень кончается на 4 или на 6', '25² = 625', '24 · 24 = 576')
    assert 20 ** 2 == 400 and 30 ** 2 == 900 and 25 ** 2 == 625 and 24 ** 2 == 576 and 26 ** 2 == 676
    lo = NumLine(50, 350, 20, 30, 150)
    up = NumLine(50, 350, 400, 900, 60)
    b = [up.axis(step=500, arrow=False), lo.axis(step=10, arrow=False)]
    for v, sq in ((20, 400), (25, 625), (30, 900)):
        b.append(line(lo.x(v), lo.y - 6, up.x(sq), up.y + 6, MUTED, 1.2, " stroke-dasharray='3 4'"))
    b.append(line(lo.x(24), lo.y - 6, up.x(576), up.y + 6, GREEN, 2.2))
    for sq in (400, 625, 900):
        b.append(dot(up.x(sq), up.y, 4, MUTED) + t(round(up.x(sq), 1), up.y - 14, sq, MUTED, 17))
    b.append(dot(up.x(576), up.y, 5.5, GOLD) + t(round(up.x(576), 1) - 8, up.y - 14, 576, GOLD, 18, anchor='end', weight=700))
    for v in (20, 25, 30):
        b.append(t(round(lo.x(v), 1), lo.y + 29, v, MUTED, 17))
    b.append(lo.seg(20, 25, GOLD, 4))
    x26 = round(lo.x(26), 1) + 6
    b.append(dot(lo.x(26), lo.y, 5, GREY) + t(x26, lo.y + 29, 26, MUTED, 18, anchor='start')
             + line(x26 - 2, lo.y + 23, x26 + 24, lo.y + 23, RED, 2.2))
    b.append(dot(lo.x(24), lo.y, 6, GREEN) + t(round(lo.x(24), 1) - 6, lo.y + 29, 24, GREEN, 18, anchor='end', weight=700))
    b.append(t(20, up.y + 5, 'x²', INK, 16) + t(20, lo.y + 5, 'x', INK, 16))
    return fig(svg(380, 196, ''.join(b)), '576 меньше 625 — значит, корень левее 25; из 24 и 26 остаётся 24.')


A8, B8, C8, D8, E8 = (0, 3), (4, 3), (4, 0), (0, 0), (2, 0)


def g8_task():
    need('Отрезан треугольник BCE с катетами EC = 2x и BC = 3x, осталась фигура ABED', 'прямоугольник 4x × 3x')
    assert dist(E8, C8) == 2 and dist(B8, C8) == 3
    assert 4 * 3 - area([B8, C8, E8]) == area([A8, B8, E8, D8]) == 9
    gm = G(44, 50, 40 + 3 * 44)
    x0, y0 = gm(A8)
    ctr = (2, 1.5)
    b = [cells(x0, y0, 4, 3, gm.k, '#4a5a70'), tri(gm, [A8, B8, E8, D8], GOLD, 0.3, INK, 2.4),
         tri(gm, [B8, C8, E8], GREY, 0.2, GREY, 1.8, dash='5 4')]
    for p, s in ((A8, 'A'), (B8, 'B'), (C8, 'C'), (D8, 'D')):
        b.append(L(gm, p, s, ctr))
    b.append(T((gm(E8)[0], gm(E8)[1] + 18), 'E', INK, 16))
    b.append(T((gm((2, 3))[0], y0 - 30), '4x', INK, 15) + T((x0 - 32, gm((0, 1.5))[1]), '3x', INK, 15))
    b.append(T((gm((3, 0))[0], gm(C8)[1] + 20), '2x', GREY, 15) + T((gm(C8)[0] + 28, gm((0, 1.5))[1]), '3x', GREY, 15))
    body = ''.join(b)
    ascii_cover('D · E · C', body)
    return fig(svg(300, 240, body), zamena=True)


FIGS = {
    'Куски можно переложить по-другому': v1_perelozhit,
    'Наклонная сторона высотой не бывает': r1_vysota,
    'A · · · · · B': g1_diagonal,
    'Формула годится для любого прямоугольного треугольника': g1_any,
    'Прямоугольный треугольник с катетами 8 см и 5 см': g1_task,
    'K · · · · · ·': g2_task,
    'Четвёртого нет: в левом нижнем углу стоит сама вершина K': g2_plan,
    'справа снизу — от M до вершины прямоугольника 1 клетка': g2_legs,
    'Такой кусок сначала режут на прямоугольник и треугольник': g2_trap,
    'A ──H': g3_acute,
    'B ┄┄┄┄ H': g3_obtuse,
    'S(ABC) = S(AHC) − S(BHC)': g3_minus,
    'Возьму основанием BC, высоту к нему': g3_bc,
    'Тогда высота у них одна и та же — перпендикуляр из общей вершины': g4_general,
    'Площади другие, а отношение то же': g4_ratio,
    'A ───── D': g4_task,
    'Сам отрезок BD наклонный, это не высота': g4_plan,
    'На одну часть приходится 40 : 5 = 8': g4_bar,
    'Медиана делит треугольник на две части равной площади': g4_median,
    'Высота одна только тогда, когда вершина общая': g4_two_lines,
    'При общем основании площади относятся как высоты': g5_general,
    'A ────┴─┬': g5_task,
    'площади вычитают, 25 − 15 = 10': g5_side,
    'куда бы ни уехала вершина': g6_slide,
    'B ───── P': g6_task,
    'поэтому это расстояние равно AB = 6': g6_plan,
    "' O '": g6_trap_task,
    'S(AOB) = S(ABD) − S(AOD) = S(ACD) − S(AOD) = S(COD)': g6_trap_minus,
    '5 штук в ряду, 3 ряда': g7_cells,
    '2x · 2x : 2 = 4x² : 2 = 2x²': g7_half,
    '=' + ' '.join(['·'] * 22): g7_task,
    'Откуда 4: каждый квадратик 1 × 1 растягивается': g7_scale,
    '2x — это два куска длины, x² — один квадратик площади': g7_len_area,
    'Сравнить с серединой': g8_squeeze,
    'D · E · C': g8_task,
}


def main():
    out = {}
    for anchor, fn in FIGS.items():
        a = anchor[1:] if anchor.startswith('=') else anchor
        assert a in norm(MD), f'якорь не найден: {anchor!r}'
        out[anchor] = fn()
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=1)
    print(f'{len(out)} рисунков → {os.path.relpath(VIS)}')


if __name__ == '__main__':
    main()
