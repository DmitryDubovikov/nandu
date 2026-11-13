"""Рисунки глав 11–13 учебника «Геометрия» (план: 26-27/school6/vis/plan_geometriya.md)."""
from geometriya_lib import *


# ═══ Глава 11 ═══

@at('прямоугольник 3 × 7 см не равны ✗')
def c11_table():
    need('ромб со стороной `5` см и углами `60°`/`120°`', 'прямоугольник `3 × 7` см', 'квадрат `5 × 5` см')
    W, H = 440, 200
    u = 15
    b = ''
    A = (22, 140)
    B = (A[0] + 5 * u, A[1])
    D, C = pol(A, 5 * u, 60), pol(B, 5 * u, 60)
    b += poly([A, B, C, D], INK)
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        b += ticks(p, q, 1, GOLD)
    b += angle_arc(A, B, D, 20, BLUE, 2, '60°', INK, 14) + angle_arc(D, A, C, 18, VIOLET, 2, '120°', INK, 14)
    b += tx(80, 185, 'нет', RED, NS, weight=600)
    x0, y0 = 170, 140
    R = [(x0, y0), (x0 + 7 * u, y0), (x0 + 7 * u, y0 - 3 * u), (x0, y0 - 3 * u)]
    b += poly(R, INK)
    for k in range(4):
        b += right_angle(R[k], R[(k + 1) % 4], R[k - 1], 10, BLUE)
    b += tx(x0 + 3.5 * u, y0 + 20, '7 см', MUTED, 14) + tx(x0 + 7 * u + 6, y0 - 1.5 * u + 5, '3 см', MUTED, 14, 'start')
    b += tx(x0 + 3.5 * u, 185, 'нет', RED, NS, weight=600)
    x0 = 340
    Q = [(x0, y0), (x0 + 5 * u, y0), (x0 + 5 * u, y0 - 5 * u), (x0, y0 - 5 * u)]
    b += poly(Q, INK)
    for k in range(4):
        b += right_angle(Q[k], Q[(k + 1) % 4], Q[k - 1], 10, BLUE) + ticks(Q[k], Q[(k + 1) % 4], 1, GOLD)
    b += tx(x0 + 2.5 * u, 185, 'да', GREEN, NS, weight=600)
    return S(W, H, b), 'Чёрточки — равные стороны, дуги и уголки — углы.'


@at('идёт внутри фигуры')
def c11_convex():
    W, H = 440, 200
    P = [(30, 120), (70, 40), (160, 30), (205, 95), (180, 165), (80, 170)]
    b = poly(P, INK) + seg(P[0], P[3], GREEN, 2.6, DASH) + seg(P[1], P[4], GREEN, 2.6, DASH)
    b += tx(118, 192, 'выпуклый', GREEN, NS, weight=600)
    Q = [(250, 160), (270, 40), (330, 110), (390, 35), (410, 165)]
    b += poly(Q, INK) + seg(Q[1], Q[3], RED, 2.6, DASH)
    b += tx(330, 192, 'невыпуклый', RED, NS, weight=600)
    return S(W, H, b), 'У невыпуклого угол «вдавлен» внутрь, и диагональ выходит наружу.'


POLY = {4: [(20, 150), (125, 160), (110, 50), (35, 70)],
        5: [(160, 150), (260, 160), (275, 85), (215, 40), (155, 80)],
        6: [(310, 140), (360, 165), (420, 140), (425, 75), (375, 40), (315, 70)]}


@at('Диагоналей из одной вершины')
def c11_diag():
    need('| `4` | `1` | `2` |', '| `5` | `2` | `3` |', '| `6` | `3` | `4` |')
    W, H = 440, 215
    b = ''
    for n, P in POLY.items():
        V = P[0]
        for k in range(1, n - 1):
            b += poly([V, P[k], P[k + 1]], 'none', BLUE if k % 2 else VIOLET, 0.22, 0)
        b += poly(P, INK)
        for k in range(2, n - 1):
            b += seg(V, P[k], BLUE, 2.2)
        b += dot(*V, 6, GOLD) + dot(*P[1], 5, GREY) + dot(*P[-1], 5, GREY)
        cx = sum(p[0] for p in P) / n
        b += tx(cx, 200, f'{n - 2} треугольника', INK, NS)
    return S(W, H, b), 'Из жёлтой вершины диагонали идут во все вершины, кроме неё самой и двух серых соседей.'


@at('внешний угол = 180° − угол многоугольника')
def c11_ext():
    W, H = 420, 230
    U, V, Wp = (40, 200), (240, 170), (300, 50)
    rest = [(150, 20), (30, 90)]
    b = poly([U, V, Wp] + rest, GREY, sw=1.6)
    b += seg(U, V, INK, 2.6) + seg(V, Wp, INK, 2.6)
    ext = add(V, ((V[0] - U[0]) * 0.75, (V[1] - U[1]) * 0.75))
    b += seg(V, ext, MUTED, 2, DASH)
    a_in, a_out, a_back = ang_of(V, ext), ang_of(V, Wp), ang_of(V, U)
    b += sector(V, 40, a_out, a_back, GOLD, 0.4)
    b += sector(V, 52, a_in, a_out, BLUE, 0.45)
    b += tx(V[0] - 52, V[1] - 40, 'угол многоугольника', GOLD, NS, 'end')
    b += tx(V[0] + 50, V[1] - 52, 'внешний угол', BLUE, NS, 'start')
    b += dot(*V, 4)
    return S(W, H, b), 'Внешний угол и угол многоугольника вместе составляют развёрнутый угол.'


@at('всего повернулся на полный оборот', fx=True)
def c11_walk():
    W, H = 440, 260
    P = [(40, 150), (100, 230), (215, 205), (225, 85), (110, 40)]       # обход против часовой на экране
    n = len(P)
    cols = [GOLD, BLUE, GREEN, VIOLET, CYAN]
    b = arrow_defs_p('g115', [INK])
    b += poly(P, INK, sw=2.4)
    C = (345, 135)
    b += dot(*C, 4)
    tot = 0
    for k in range(n):
        A, V, B = P[k - 1], P[k], P[(k + 1) % n]
        ext = add(V, ((V[0] - A[0]) * 0.35, (V[1] - A[1]) * 0.35))
        b += seg(V, ext, MUTED, 1.6, DASH)
        a1, a2 = ang_of(V, ext), ang_of(V, B)            # поворот: от продолжения к следующей стороне
        sweep = (a2 - a1) % 360
        tot += sweep
        w = sector(V, 26, a1, a2, cols[k], 0.7)
        d = 0.3 + 0.45 * k
        m = mid(A, V)
        b += g('fi', d, arrow(lerp(A, V, 0.35), lerp(A, V, 0.6), INK, 'g1150', 2.6))
        b += g('fi', d + 0.3, w)
        b += g('fi', d + 0.3, g('sl', 2.8 + 0.3 * k, w, f';--to:translate({C[0] - V[0]:.1f}px,{C[1] - V[1]:.1f}px)'))
    assert abs(tot - 360) < 1e-6, tot
    b += g('fi', 5.4, circle(C[0], C[1], 34, INK, 2) + tx(C[0], C[1] - 46, '360°', INK, 17, weight=600))
    return S(W, H, b), 'На каждой вершине путник поворачивает на внешний угол; пять поворотов складываются в полный оборот.'


@at('четыре дают 432° — нахлёст')
def c11_tiling():
    need('`360 : 120 = 3`', 'три дают `324°` — щель', 'четыре дают `432°` — нахлёст')
    W, H = 440, 225
    b = ''
    s = 40
    P = (75, 95)
    for k in range(3):
        cen = pol(P, s, 30 + 120 * k)
        b += poly(regpoly(cen, s, 6, ang_of(cen, P)), GREEN, GREEN, 0.3)
    b += dot(*P, 4) + tx(P[0], 212, '360 : 120 = 3', GREEN, NS, weight=600)
    sp = 36
    R = sp / (2 * math.sin(math.radians(36)))
    for x0, cnt in ((222, 3), (367, 4)):
        P = (x0, 95)
        for k in range(cnt):
            bis = 288 + 54 + 108 * k
            cen = pol(P, R, bis)
            col = RED if k == 3 else GOLD
            b += poly(regpoly(cen, R, 5, ang_of(cen, P)), col, col, 0.3 if k < 3 else 0.35)
        if cnt == 3:
            b += sector(P, 2 * R * 0.9, 252, 288, RED, 0.55, RED)
            b += tx(x0, 212, '324° — щель', RED, NS, weight=600)
        else:
            b += tx(x0, 212, '432° — нахлёст', RED, NS, weight=600)
        b += dot(*P, 4)
    return S(W, H, b), ''


# ═══ Глава 12 ═══

def platonic():
    ph = (1 + 5 ** 0.5) / 2
    tet = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    cub = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    octa = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    ico = []
    for a in (-1, 1):
        for c in (-ph, ph):
            ico += [(0, a, c), (a, c, 0), (c, 0, a)]
    dod = list(cub)
    for a in (-1 / ph, 1 / ph):
        for c in (-ph, ph):
            dod += [(0, a, c), (a, c, 0), (c, 0, a)]
    return [('тетраэдр', tet, 4), ('куб', cub, 6), ('октаэдр', octa, 8), ('додекаэдр', dod, 12), ('икосаэдр', ico, 20)]


def norm_r(V):
    m = max(math.sqrt(sum(c * c for c in v)) for v in V)
    return [tuple(c / m for c in v) for v in V]


@at('а в трёх — по 4')
def c12_bipyr():
    W, H = 340, 300
    side = math.sqrt(3)
    hh = math.sqrt(2 / 3) * side
    V = [(math.cos(math.radians(90 + 120 * k)), 0, math.sin(math.radians(90 + 120 * k))) for k in range(3)]
    V += [(0, hh, 0), (0, -hh, 0)]
    P = rot_proj(20, 12, 82, 170, 150)
    out, Q, vis, edges = solid(V, P, hcol=MUTED, sw=2.4)
    cen = (sum(q[0] for q in Q) / len(Q), sum(q[1] for q in Q) / len(Q))
    F = hull_faces(V)
    assert len(F) == 6
    for k in range(3):
        assert sum(k in f for f in F) == 4
    for k in (3, 4):
        assert sum(k in f for f in F) == 3
    for k in range(3):
        out += dot(*Q[k], 7, BLUE) + label(Q[k], '4', cen, 20, BLUE, 17)
    for k in (3, 4):
        out += dot(*Q[k], 7, GOLD) + label(Q[k], '3', cen, 20, GOLD, 17)
    return S(W, H, out), 'Число у вершины — сколько граней в ней сходится.'


@at('икосаэдр равносторонний треугольник 20 12 30')
def c12_five():
    W, H = 440, 360
    b = ''
    pos = [(75, 85), (220, 85), (365, 85), (148, 255), (292, 255)]
    for (name, V, nf), (cx, cy) in zip(platonic(), pos):
        V = norm_r(V)
        F = hull_faces(V)
        assert len(F) == nf, (name, len(F))
        P = rot_proj(22, 18, 58, cx, cy)
        Q = [P(v) for v in V]

        def area(f):
            a = 0
            for k in range(len(f)):
                (x1, y1), (x2, y2) = Q[f[k]], Q[f[(k + 1) % len(f)]]
                a += x1 * (-y2) - x2 * (-y1)
            return a / 2
        best = max(range(len(F)), key=lambda i: area(F[i]))
        out, Q, vis, edges = solid(V, P, faces=F, hcol=MUTED, sw=2, fills={best: (GOLD, 0.4)})
        b += out + tx(cx, cy + 82, name, INK, NS, weight=600)
    return S(W, H, b), 'Залита одна грань — видна её форма.'


def around(P, poly_n, cnt, s, col, start, op=0.3):
    """cnt правильных poly_n-угольников со стороной s вокруг точки P, первый начинается с луча start."""
    ang = 180 - 360 / poly_n
    R = s / (2 * math.sin(math.radians(180 / poly_n)))
    out = ''
    for k in range(cnt):
        bis = start + ang * k + ang / 2
        cen = pol(P, R, bis)
        out += poly(regpoly(cen, R, poly_n, ang_of(cen, P)), col, col, op)
    return out + dot(*P, 4)


@at('треугольных граней у этих трёх 4, 8 и 20')
def c12_tri():
    need('да — тетраэдр', 'да — октаэдр', 'да — икосаэдр', 'нет — плоскость')
    W, H = 440, 170
    b = ''
    for k, (cnt, name) in enumerate(((3, 'тетраэдр'), (4, 'октаэдр'), (5, 'икосаэдр'), (6, 'плоскость'))):
        P = (55 + 110 * k, 75)
        col = GREY if cnt == 6 else GREEN
        b += around(P, 3, cnt, 46, col, 270 - 30 * cnt)
        b += tx(P[0], 160, name, col if cnt < 6 else MUTED, NS, weight=600)
    return S(W, H, b), 'Пока между гранями остаётся щель, их можно согнуть в уголок; без щели — плоскость.'


@at('так выглядит пол, выложенный плиткой')
def c12_sq():
    need('да — куб')
    W, H = 340, 190
    b = around((85, 85), 4, 3, 52, GREEN, 135) + tx(85, 180, 'куб', GREEN, NS, weight=600)
    b += around((255, 85), 4, 4, 52, GREY, 0) + tx(255, 180, 'плоскость', MUTED, NS, weight=600)
    return S(W, H, b), ''


# ═══ Глава 13 ═══

def centroid(A, B, C):
    return ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)


def incenter(A, B, C):
    a, b_, c = dist(B, C), dist(A, C), dist(A, B)
    s = a + b_ + c
    return ((a * A[0] + b_ * B[0] + c * C[0]) / s, (a * A[1] + b_ * B[1] + c * C[1]) / s)


def circumcenter(A, B, C):
    m1, m2 = mid(A, B), mid(B, C)
    d1, d2 = (-(B[1] - A[1]), B[0] - A[0]), (-(C[1] - B[1]), C[0] - B[0])
    return inter_ll(m1, add(m1, d1), m2, add(m2, d2))


def orthocenter(A, B, C):
    return inter_ll(A, foot(A, B, C), B, foot(B, A, C))


def bis_foot(V, P1, P2):
    L1, L2 = dist(V, P1), dist(V, P2)
    return lerp(P1, P2, L1 / (L1 + L2))


def TRI(ox, oy, k=1.0):
    """Разносторонний остроугольный треугольник: вершина A сверху, BC — основание."""
    A, B, C = (90, 30), (20, 190), (250, 190)
    return tuple((ox + k * p[0], oy + k * p[1]) for p in (A, B, C))


def perp_line(M, P, Q, L1, L2):
    """Прямая через M перпендикулярно PQ: от M на L1 в одну сторону и L2 в другую."""
    d = dist(P, Q)
    nx, ny = -(Q[1] - P[1]) / d, (Q[0] - P[0]) / d
    return (M[0] + nx * L1, M[1] + ny * L1), (M[0] - nx * L2, M[1] - ny * L2)


@at('прямая через середину стороны, перпендикулярная ей')
def c13_lines():
    W, H = 440, 450
    b = ''
    names = ['медиана', 'биссектриса', 'высота', 'серединный перпендикуляр']
    for k, name in enumerate(names):
        ox, oy = 2 + (k % 2) * 220, 12 + (k // 2) * 222
        A, B, C = TRI(ox, oy, 0.82)
        b += poly([A, B, C], INK)
        if k == 0:
            M = mid(B, C)
            b += seg(A, M, GOLD, 2.6) + ticks(B, M, 1, GOLD) + ticks(M, C, 1, GOLD)
        elif k == 1:
            L = bis_foot(A, B, C)
            b += seg(A, L, GOLD, 2.6)
            b += angle_arc(A, B, L, 26, BLUE, 2) + angle_arc(A, L, C, 30, BLUE, 2)
        elif k == 2:
            h, Fh = height(A, B, C, GOLD, None)
            b += h
        else:
            M = mid(B, C)
            p1, p2 = perp_line(M, B, C, -150, -14)
            b += seg(p1, p2, GOLD, 2.6) + ticks(B, M, 1, GOLD) + ticks(M, C, 1, GOLD) + right_angle(M, p1, C, 11, GOLD)
        b += pname(A, 'A', 0, -14) + pname(B, 'B', -2, 16) + pname(C, 'C', 2, 16)
        b += tx(ox + 110, oy + 200, name, INK, NS, weight=600)
    return S(W, H, b), 'Все четыре линии идут к одной стороне BC — и все четыре разные.'


@at('центр описанной окружности точка одинаково удалена от всех трёх вершин')
def c13_points():
    W, H = 440, 450
    b = ''
    names = ['медианы', 'биссектрисы', 'высоты', 'серединные перпендикуляры']
    for k, name in enumerate(names):
        ox, oy = 2 + (k % 2) * 220, 12 + (k // 2) * 222
        A, B, C = TRI(ox, oy, 0.82)
        b += poly([A, B, C], INK)
        V = [A, B, C]
        if k == 0:
            for i in range(3):
                b += seg(V[i], mid(V[(i + 1) % 3], V[(i + 2) % 3]), BLUE, 1.8)
            X = centroid(A, B, C)
        elif k == 1:
            for i in range(3):
                b += seg(V[i], bis_foot(V[i], V[(i + 1) % 3], V[(i + 2) % 3]), BLUE, 1.8)
            X = incenter(A, B, C)
        elif k == 2:
            for i in range(3):
                h, _ = height(V[i], V[(i + 1) % 3], V[(i + 2) % 3], BLUE, None, s=8)
                b += h
            X = orthocenter(A, B, C)
        else:
            X = circumcenter(A, B, C)
            for i in range(3):
                P_, Q_ = V[(i + 1) % 3], V[(i + 2) % 3]
                M = mid(P_, Q_)
                L = dist(M, X) + 18
                d = (X[0] - M[0], X[1] - M[1])
                n_ = dist(M, X) or 1
                b += seg(M, (M[0] + d[0] / n_ * L, M[1] + d[1] / n_ * L), BLUE, 1.8) + right_angle(M, X, Q_, 8, BLUE, 1.4)
        b += dot(*X, 6, GOLD)
        b += tx(ox + 110, oy + 200, name, INK, NS, weight=600)
    return S(W, H, b), 'В каждой картинке три линии встречаются в одной жёлтой точке; у разных наборов точки разные.'


@at('Вот почему третья линия проходит через ту же точку')
def c13_circum():
    W, H = 420, 300
    A, B, C = (60, 250), (150, 40), (380, 250)
    X = circumcenter(A, B, C)
    b = poly([A, B, C], INK)
    for (P_, Q_), col, dsh in (((A, B), GOLD, None), ((B, C), GOLD, None), ((A, C), BLUE, DASH)):
        M = mid(P_, Q_)
        n_ = dist(M, X)
        d = ((X[0] - M[0]) / n_, (X[1] - M[1]) / n_) if n_ > 1 else (0, -1)
        b += seg(lerp(M, add(M, d), -16), add(M, (d[0] * (n_ + 40), d[1] * (n_ + 40))), col, 2.2, dsh)
        b += right_angle(M, add(M, d), Q_, 9, col, 1.6)
    for P_ in (A, B, C):
        b += seg(X, P_, GREEN, 2) + ticks(X, P_, 2, GREEN)
    b += dot(*X, 6, GOLD)
    for P_, s, dx, dy in ((A, 'A', -14, 6), (B, 'B', 0, -16), (C, 'C', 14, 6)):
        b += pname(P_, s, dx, dy)
    return S(W, H, b), 'Жёлтые — серединные перпендикуляры к AB и BC, синий пунктир — к AC; он проходит через ту же точку.'


@at('Расстояние от точки до стороны меряют по перпендикуляру')
def c13_bis():
    W, H = 400, 250
    V = (40, 225)
    b = seg(V, pol(V, 350, 0)) + seg(V, pol(V, 280, 50)) + seg(V, pol(V, 340, 25), GOLD, 2.4)
    X = pol(V, 230, 25)
    F1, F2 = foot(X, V, pol(V, 10, 0)), foot(X, V, pol(V, 10, 50))
    b += seg(X, F1, BLUE, 2.4) + seg(X, F2, BLUE, 2.4) + ticks(X, F1, 1, BLUE) + ticks(X, F2, 1, BLUE)
    b += right_angle(F1, X, V, 10, BLUE) + right_angle(F2, X, V, 10, BLUE)
    b += angle_arc(V, pol(V, 10, 0), X, 52, GOLD, 2) + angle_arc(V, X, pol(V, 10, 50), 58, GOLD, 2)
    b += dot(*X, 6, GOLD)
    return S(W, H, b), 'Расстояния до сторон — синие перпендикуляры; у точки биссектрисы они равны.'


@at('фонарь на равном расстоянии от трёх заборов')
def c13_well():
    W, H = 440, 230
    b = ''
    for k in range(2):
        A, B, C = TRI(4 + 220 * k, 6, 0.85)
        b += poly([A, B, C], INK if k == 0 else GOLD, sw=2.2 if k == 0 else 3)
        if k == 0:
            X = circumcenter(A, B, C)
            for P_ in (A, B, C):
                b += seg(X, P_, GREEN, 2) + ticks(X, P_, 2, GREEN) + rect(P_[0] - 6, P_[1] - 6, 12, 12, GOLD, 'none', 0)
            b += dot(*X, 6, GREEN)
            b += tx(114, 222, 'колодец: от домов', GREEN, NS, weight=600)
        else:
            X = incenter(A, B, C)
            for P_, Q_ in ((A, B), (B, C), (A, C)):
                F = foot(X, P_, Q_)
                b += seg(X, F, BLUE, 2) + ticks(X, F, 1, BLUE) + right_angle(F, X, Q_, 8, BLUE, 1.4)
            b += dot(*X, 6, BLUE)
            b += tx(334, 222, 'фонарь: от заборов', BLUE, NS, weight=600)
    return S(W, H, b), 'Слева дома — в вершинах, справа заборы — стороны: точки получаются разные.'


@at('а вся медиана 12 см')
def c13_median():
    need('до этой точки `8` см, то оставшийся кусок `4` см, а вся медиана `12` см')
    W, H = 420, 255
    A, B, C = (120, 25), (30, 235), (390, 235)
    M = mid(B, C)
    G = centroid(A, B, C)
    assert abs(dist(A, G) - 2 * dist(G, M)) < 1e-6
    b = poly([A, B, C], INK)
    b += seg(B, mid(A, C), GREY, 1.4, DASH) + seg(C, mid(A, B), GREY, 1.4, DASH)
    b += seg(A, G, GOLD, 3.4) + seg(G, M, BLUE, 3.4) + ticks(B, M, 1, MUTED) + ticks(M, C, 1, MUTED)
    b += dot(*G, 6, INK)
    b += label(mid(A, G), '8 см', (0, 60), 26, GOLD, NS, 600)
    b += label(mid(G, M), '4 см', (0, 160), 26, BLUE, NS, 600)
    am = math.degrees(math.atan2(M[1] - A[1], M[0] - A[0]))       # подпись вдоль медианы, слева от неё
    L = dist(A, M)
    c = (mid(A, M)[0] + (M[1] - A[1]) / L * -24, mid(A, M)[1] - (M[0] - A[0]) / L * -24)
    b += tx(c[0], c[1], 'вся медиана 12 см', INK, NS, extra=f" transform='rotate({am:.1f} {c[0]:.1f} {c[1]:.1f})'")
    return S(W, H, b), ''


EQ = 40          # 1 см = 40 px в разборе главы 13


@at('одна прямая работает за все четыре линии', fx=True)
def c13_fold():
    need('сторона `6` см', 'на `6` см от `A` и на `3` см от `M`')
    W, H = 420, 300
    s = 6 * EQ
    B, C = (90, 270), (90 + s, 270)
    A = pol(B, s, 60)
    M = mid(B, C)
    b = seg(A, M, GOLD, 2.4) + poly([A, B, C], INK)
    b += flip(A, M, poly([A, B, M], BLUE, BLUE, 0.3) + dot(*B, 6, BLUE), 0.5)
    b += label(mid(A, B), '6 см', M, 34, MUTED, NS) + label(mid(A, C), '6 см', M, 34, MUTED, NS)
    b += tx(*add(mid(B, M), (0, 22)), '3 см', MUTED, NS) + tx(*add(mid(M, C), (0, 22)), '3 см', MUTED, NS)
    b += g('fi', 2.1, angle_arc(A, B, M, 34, GREEN, 2.2) + angle_arc(A, M, C, 40, GREEN, 2.2) +
           right_angle(M, A, C, 13, GREEN, 2) + ticks(B, M, 1, GREEN) + ticks(M, C, 1, GREEN))
    for P_, n, dx, dy in ((A, 'A', 0, -16), (B, 'B', -14, 4), (C, 'C', 14, 4), (M, 'M', 0, 18)):
        b += pname(P_, n, dx, dy)
    return S(W, H, b), 'Перегнули по AM: B легла на C, половинки угла A совпали, углы у M стали прямыми.'


@at('все четыре замечательные точки лежат в одном месте')
def c13_center():
    W, H = 340, 290
    s = 240
    B, C = (50, 260), (50 + s, 260)
    A = pol(B, s, 60)
    b = poly([A, B, C], INK)
    V = [A, B, C]
    for i in range(3):
        P_ = V[i]
        M = mid(V[(i + 1) % 3], V[(i + 2) % 3])
        b += seg(P_, lerp(P_, M, 1.1), GOLD, 2)
    b += dot(*centroid(A, B, C), 7, GREEN)
    return S(W, H, b), 'Три прямые — каждая сразу медиана, биссектриса, высота и серединный перпендикуляр.'


@at('в середину попадает только в особых случаях')
def c13_err():
    W, H = 420, 270
    A, B, C = (80, 30), (30, 230), (390, 230)
    M = mid(B, C)
    h, F = height(A, B, C, GREEN, None)
    b = poly([A, B, C], INK) + h + seg(A, M, RED, 2.4) + ticks(B, M, 1, RED) + ticks(M, C, 1, RED)
    b += tx(F[0] - 6, 255, 'высота', GREEN, NS, 'end', 600) + tx(M[0] + 6, 255, 'медиана — не высота', RED, NS, 'start', 600)
    return S(W, H, b), ''
