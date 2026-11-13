"""Рисунки глав 7–10 учебника «Геометрия» (план: 26-27/school6/vis/plan_geometriya.md)."""
from geometriya_lib import *
from geometriya_a import CUBE, CI, E, cube_svg


# ═══ Глава 7 ═══

@at('точка, где сходятся рёбра')
def c7_parts():
    need('| **грань** |', '| **ребро** |', '| **вершина** |')
    W, H = 380, 240
    fills = {tuple(CI[c] for c in 'ABCD'): (GOLD, 0.35)}
    out, Q, vis, edges = cube_svg(32, 60, 215, letters=False, fills=fills, hcol=MUTED,
                                  ecol={E('B', 'F'): BLUE})
    out += seg(Q[CI['B']], Q[CI['F']], BLUE, 5)
    out += dot(*Q[CI['G']], 7, GREEN)
    gF, gB, gG = Q[CI['F']], Q[CI['B']], Q[CI['G']]
    gH, gC = Q[CI['H']], Q[CI['C']]
    out += tx((gH[0] + gC[0]) / 2 + 6, (gH[1] + gC[1]) / 2 + 12, 'грань', GOLD, 17, weight=600)
    m = mid(gB, gF)
    out += seg(add(m, (6, -2)), (m[0] + 70, m[1] - 20), BLUE, 1.2) + tx(m[0] + 74, m[1] - 16, 'ребро', BLUE, 17, 'start', 600)
    out += seg(add(gG, (8, 4)), (gG[0] + 60, gG[1] + 30), GREEN, 1.2) + tx(gG[0] + 64, gG[1] + 36, 'вершина', GREEN, 17, 'start', 600)
    return S(W, H, out), ''


PENT = [(math.cos(math.radians(90 + 72 * k)), math.sin(math.radians(90 + 72 * k))) for k in range(5)]


@at('рёбра: 5 в нижнем основании, 5 в верхнем и 5 боковых')
def c7_prism():
    need('`5 + 5 + 5 = 15`', '`5 + 5 = 10`')
    W, H = 380, 270
    V = [(x, 0, z) for x, z in PENT] + [(x, 1.6, z) for x, z in PENT]
    P = rot_proj(14, 22, 80, 170, 210)
    ec = {}
    for k in range(5):
        ec[tuple(sorted((k, (k + 1) % 5)))] = GOLD
        ec[tuple(sorted((5 + k, 5 + (k + 1) % 5)))] = VIOLET
        ec[(k, 5 + k)] = BLUE
    out, Q, vis, edges = solid(V, P, ecol=ec, sw=2.6)
    out += ''.join(dot(*Q[k], 4.5, GOLD if k < 5 else VIOLET) for k in range(10))
    out += tx(300, 250, 'нижнее основание: 5', GOLD, NS) + tx(300, 30, 'верхнее основание: 5', VIOLET, NS)
    out += tx(320, 140, 'боковые', BLUE, NS) + tx(320, 158, 'рёбра: 5', BLUE, NS)
    return S(W, H, out), ''


@at('рёбра: 5 в основании и 5 боковых')
def c7_pyramid():
    need('`5 + 1 = 6`', '`5 + 5 = 10`')
    W, H = 380, 270
    V = [(x, 0, z) for x, z in PENT] + [(0, 2.0, 0)]
    P = rot_proj(0, 25, 80, 170, 215)
    ec = {}
    for k in range(5):
        ec[tuple(sorted((k, (k + 1) % 5)))] = GOLD
        ec[(k, 5)] = BLUE
    out, Q, vis, edges = solid(V, P, ecol=ec, sw=2.6)
    out += ''.join(dot(*Q[k], 4.5, GOLD) for k in range(5)) + dot(*Q[5], 6, GREEN)
    out += tx(Q[5][0] + 14, Q[5][1] + 4, 'верхняя вершина', GREEN, NS, 'start')
    out += tx(300, 258, 'основание: 5', GOLD, NS) + tx(320, 140, 'боковые', BLUE, NS) + tx(320, 158, 'рёбра: 5', BLUE, NS)
    return S(W, H, out), ''


@at('(вершины минус рёбра плюс грани)')
def c7_convex():
    need('отрезок между любыми двумя его точками целиком лежит внутри тела')
    W, H = 440, 240
    out, Q, vis, edges = cube_svg(28, 30, 190, letters=False, hcol=MUTED)
    p1 = lerp(Q[CI['D']], Q[CI['B']], 0.25)
    p2 = lerp(Q[CI['E']], Q[CI['G']], 0.55)
    out += seg(p1, p2, GREEN, 3) + dot(*p1, 5, GREEN) + dot(*p2, 5, GREEN)
    out += tx(100, 228, 'выпуклый', GREEN, NS, weight=600)
    # тело с вырезом: Г-образная призма
    L = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
    V = [(x, y, 2) for x, y in L] + [(x, y, 0) for x, y in L]
    n = len(L)
    F = [list(range(n)), [n + k for k in reversed(range(n))]]
    for k in range(n):
        F.append([k, n + k, n + (k + 1) % n, (k + 1) % n])
    # грани против часовой снаружи: передняя (z = 2) — контур L против часовой, боковые — от передней к задней
    P = obl_proj(28, 0.5, 250, 190, 2)
    o2, Q2, vis2, e2 = solid(V, P, faces=F, hcol=MUTED)
    a = lerp(Q2[5], Q2[4], 0.5)
    a = (a[0], a[1] + 14)
    c = (Q2[2][0] - 10, Q2[2][1] + 30)
    o2 += seg(a, c, RED, 3) + dot(*a, 5, RED) + dot(*c, 5, RED)
    out += o2 + tx(320, 228, 'невыпуклый', RED, NS, weight=600)
    return S(W, H, out), 'У невыпуклого тела отрезок между двумя его точками проходит по вырезу — вне тела.'


# ═══ Глава 8 ═══

@at('образующих его прямой угол', fx=True)
def c8_rotate():
    W, H = 440, 440
    b = ''
    cells_ = [(110, 20, 'rect', 'цилиндр'), (330, 20, 'tri', 'конус'), (110, 230, 'semi', 'шар'), (330, 230, 'circ', 'шар')]
    for x0, y0, kind, name in cells_:
        top, bot = (x0, y0 + 10), (x0, y0 + 175)
        if kind == 'rect':
            shape = poly([(x0, y0 + 40), (x0 + 62, y0 + 40), (x0 + 62, y0 + 160), (x0, y0 + 160)], GOLD, GOLD, 0.35)
            body = cylinder(x0, y0 + 40, 62, 120)
        elif kind == 'tri':
            shape = poly([(x0, y0 + 30), (x0, y0 + 160), (x0 + 68, y0 + 160)], GOLD, GOLD, 0.35)
            body = cone(x0, y0 + 30, 68, 130)
        elif kind == 'semi':
            c = (x0, y0 + 95)
            shape = (f"<path d='M{x0},{c[1] - 66} A66,66 0 0 1 {x0},{c[1] + 66} Z' fill='{GOLD}' fill-opacity='0.35' "
                     f"stroke='{GOLD}' stroke-width='2.2'/>")
            body = sphere(x0, c[1], 66)
        else:
            c = (x0, y0 + 95)
            shape = circle(x0, c[1], 66, GOLD, 2.2, GOLD, extra=" fill-opacity='0.3'")
            body = sphere(x0, c[1], 66)
        b += g('fi', 2.0, body)
        b += shape
        copy = shape.replace(GOLD, BLUE)
        b += flip(top, bot, copy, 0.4)
        b += seg(top, bot, GOLD, 2, DASH)
        b += tx(x0, y0 + 200, name, INK, NS, weight=600)
    return S(W, H, b), 'Копия фигуры проходит пол-оборота вокруг оси; полный оборот заметает всё тело.'


@at('в теле появляется сквозная дырка')
def c8_tube():
    W, H = 420, 230
    ax = 50
    b = seg((ax, 20), (ax, 210), GOLD, 2, DASH)
    b += rect(ax, 50, 56, 140, GREY, 'none', 0, extra=" fill-opacity='0.25'")
    b += poly([(ax + 56, 50), (ax + 106, 50), (ax + 106, 190), (ax + 56, 190)], GOLD, GOLD, 0.35)
    b += tx(ax + 28, 42, 'пусто', GREY, 14)
    cx, ro, ri, ytop, h = 300, 106, 56, 50, 140
    k = 0.28
    b += seg((cx, 20), (cx, 210), GOLD, 2, DASH)
    b += (f"<path fill-rule='evenodd' d='M{cx - ro},{ytop} A{ro},{ro * k} 0 1 0 {cx + ro},{ytop} A{ro},{ro * k} 0 1 0 "
          f"{cx - ro},{ytop} Z M{cx - ri},{ytop} A{ri},{ri * k} 0 1 0 {cx + ri},{ytop} A{ri},{ri * k} 0 1 0 {cx - ri},{ytop} Z' "
          f"fill='{GOLD}' fill-opacity='0.3' stroke='none'/>")
    b += ell(cx, ytop, ro, ro * k, full=True) + ell(cx, ytop, ri, ri * k, full=True)
    b += ell(cx, ytop + h, ro, ro * k) + ell(cx, ytop + h, ri, ri * k, MUTED, 1.6)
    b += seg((cx - ro, ytop), (cx - ro, ytop + h)) + seg((cx + ro, ytop), (cx + ro, ytop + h))
    b += seg((cx - ri, ytop), (cx - ri, ytop + h), MUTED, 1.6, DASH) + seg((cx + ri, ytop), (cx + ri, ytop + h), MUTED, 1.6, DASH)
    b += tx(cx, ytop + h + 46, 'дырка вдоль оси', GREY, 14)
    return S(W, H, b), 'Промежуток до оси никто не заметает — он и становится дыркой.'


@at('чем ближе к вершине, тем меньше')
def c8_sections():
    need('круг радиуса `3` см')
    W, H = 440, 275
    b = ''
    cx, r, ytop, h = 110, 66, 30, 190
    b += cylinder(cx, ytop, r, h)
    for y in (ytop + 50, ytop + 100, ytop + 150):
        b += ell(cx, y, r, r * 0.28, GOLD, 2, fill=GOLD, op=0.3, full=True)
    yc = ytop + 100
    b += seg((cx, ytop), (cx + r, ytop), INK, 1.6) + dot(cx, ytop, 3) + tx(cx + r / 2, ytop - 26, '3 см', INK, 14)
    cx, r, yap, h = 330, 80, 20, 200
    b += cone(cx, yap, r, h)
    for k in (0.35, 0.6, 0.85):
        b += ell(cx, yap + h * k, r * k, r * k * 0.28, GOLD, 2, fill=GOLD, op=0.3, full=True)
    b += tx(110, 266, 'цилиндр', INK, NS) + tx(330, 266, 'конус', INK, NS)
    return S(W, H, b), ''


@at('в разрез попадают обе половины')
def c8_axial():
    need('радиуса `3` см и высоты `10` см', 'прямоугольник `6 × 10` см', '`2 × 3`')
    W, H = 340, 270
    u = 18
    cx, r, ytop, h = 150, 3 * u, 30, 10 * u
    b = cylinder(cx, ytop, r, h)
    b += rect(cx, ytop, r, h, GOLD, 'none', 0, extra=" fill-opacity='0.45'")
    b += rect(cx - r, ytop, r, h, BLUE, 'none', 0, extra=" fill-opacity='0.35'")
    b += seg((cx, ytop - 14), (cx, ytop + h + 14), GOLD, 2, DASH)
    b += dim((cx - r, ytop + h), (cx, ytop + h), '3', -34) + dim((cx, ytop + h), (cx + r, ytop + h), '3', -34)
    b += dim((cx + r, ytop + h), (cx + r, ytop), '10', -30)
    return S(W, H, b), 'В разрез попадает сама фигура и её копия по другую сторону оси: 3 + 3 = 6.'


@at('карта Земли всегда чуть-чуть врёт')
def c8_unroll():
    W, H = 420, 400
    b = arrow_defs_p('g85', [MUTED])
    r, h = 26, 110
    b += cylinder(50, 30, r, h, fill=BLUE, op=0.25)
    b += arrow((100, 85), (140, 85), MUTED, 'g850')
    w = 2 * math.pi * r
    b += rect(160, 30, w, h, BLUE, INK, 2, extra=" fill-opacity='0.25'")
    b += tx(160 + w / 2, 30 + h + 24, 'прямоугольник', INK, NS)
    r, hc = 34, 110
    l = math.hypot(r, hc)
    yap = 215
    b += cone(50, yap, r, hc, fill=BLUE, op=0.25)
    b += arrow((100, 280), (140, 280), MUTED, 'g850')
    ang = 360 * r / l
    C = (265, 220)
    b += sector(C, l, 270 - ang / 2, 270 + ang / 2, BLUE, 0.25, INK, 2)
    b += tx(C[0], 350, 'кусок круга', INK, NS)
    return S(W, H, b), 'Боковую поверхность цилиндра и конуса можно разрезать и развернуть без складок.'


@at('Пары (3; 5) и (5; 3) — разные')
def c8_two():
    need('`r = 3` см, `h = 5` см', '`r = 5` см, `h = 3` см')
    W, H = 420, 340
    u = 20
    b = arrow_defs_p('g86', [MUTED])
    # ось по стороне 5
    x0, y0 = 30, 25
    b += rect(x0, y0, 3 * u, 5 * u, GOLD, 'none', 0, extra=" fill-opacity='0.3'")
    b += seg((x0, y0 - 10), (x0, y0 + 5 * u + 10), GOLD, 3) + seg((x0, y0 + 5 * u), (x0 + 3 * u, y0 + 5 * u), BLUE, 3)
    b += seg((x0 + 3 * u, y0), (x0 + 3 * u, y0 + 5 * u)) + seg((x0, y0), (x0 + 3 * u, y0))
    b += tx(x0 + 1.5 * u, y0 + 5 * u + 20, '3', BLUE, NS) + tx(x0 - 10, y0 + 2.5 * u, '5', GOLD, NS, 'end')
    b += arrow((115, 75), (160, 75), MUTED, 'g860')
    b += cylinder(260, y0 + 12, 3 * u, 5 * u)
    b += tx(260, y0 + 5 * u + 50, 'r = 3 см, h = 5 см', INK, NS)
    # ось по стороне 3
    y0 = 210
    b += rect(x0, y0, 5 * u, 3 * u, GOLD, 'none', 0, extra=" fill-opacity='0.3'")
    b += seg((x0, y0 - 10), (x0, y0 + 3 * u + 10), GOLD, 3) + seg((x0, y0 + 3 * u), (x0 + 5 * u, y0 + 3 * u), BLUE, 3)
    b += seg((x0 + 5 * u, y0), (x0 + 5 * u, y0 + 3 * u)) + seg((x0, y0), (x0 + 5 * u, y0))
    b += tx(x0 + 2.5 * u, y0 + 3 * u + 20, '5', BLUE, NS) + tx(x0 - 10, y0 + 1.5 * u + 5, '3', GOLD, NS, 'end')
    b += arrow((145, y0 + 30), (180, y0 + 30), MUTED, 'g860')
    b += cylinder(295, y0 + 14, 5 * u, 3 * u)
    b += tx(295, y0 + 3 * u + 56, 'r = 5 см, h = 3 см', INK, NS)
    return S(W, H, b), 'Сторона на оси (жёлтая) становится высотой, отходящая (синяя) — радиусом.'


# ═══ Глава 9 ═══

ISO = [(110, 30), (45, 190), (175, 190)]            # равнобедренный, не равносторонний
PAR = [(255, 170), (370, 170), (405, 55), (290, 55)]


@at('повернул на пол-оборота — совпало', fx=True)
def c9_defs():
    W, H = 440, 240
    T, Bl, Br = ISO
    assert abs(dist(T, Bl) - dist(T, Br)) < 1e-9 and abs(dist(T, Bl) - dist(Bl, Br)) > 10
    ax = (T[0], 15), (T[0], 205)
    b = poly(ISO, INK) + seg(*ax, GOLD, 2, DASH)
    half = poly([T, Bl, (T[0], Bl[1])], BLUE, BLUE, 0.35) + dot(*Bl, 5, BLUE)
    b += flip(ax[0], ax[1], half, 0.4)
    c = ((PAR[0][0] + PAR[2][0]) / 2, (PAR[0][1] + PAR[2][1]) / 2)
    b += poly(PAR, INK) + dot(*c, 4.5, GOLD)
    b += turn(c, 180, poly(PAR, BLUE, BLUE, 0.3) + dot(*PAR[0], 5, BLUE), 2.0)
    b += g('fi', 1.8, tx(110, 228, 'перегнули — совпало', GREEN, NS)) + g('fi', 3.4, tx(330, 228, 'пол-оборота — совпало', GREEN, NS))
    return S(W, H, b), 'Синяя копия после перегиба или поворота легла точно на фигуру.'


@at('Центр симметрии у прямоугольника, квадрата и параллелограмма')
def c9_table():
    W, H = 440, 360
    b = ''
    cs = [(75, 80), (220, 80), (365, 80), (75, 255), (220, 255), (365, 255)]
    names = ['равносторонний', 'прямоугольник', 'квадрат', 'круг', 'равнобедренный', 'параллелограмм']

    def axis(p, q, ext=14):
        L = dist(p, q)
        u = ((q[0] - p[0]) / L, (q[1] - p[1]) / L)
        return seg((p[0] - u[0] * ext, p[1] - u[1] * ext), (q[0] + u[0] * ext, q[1] + u[1] * ext), GOLD, 2, DASH)
    # равносторонний
    c = cs[0]
    T = regpoly(c, 55, 3)
    b += poly(T, INK)
    for k in range(3):
        b += axis(T[k], mid(T[(k + 1) % 3], T[(k + 2) % 3]))
    # прямоугольник
    c = cs[1]
    R = [(c[0] - 60, c[1] + 32), (c[0] + 60, c[1] + 32), (c[0] + 60, c[1] - 32), (c[0] - 60, c[1] - 32)]
    b += poly(R, INK) + axis(mid(R[0], R[1]), mid(R[2], R[3])) + axis(mid(R[1], R[2]), mid(R[3], R[0])) + dot(*c, 5, GREEN)
    # квадрат
    c = cs[2]
    Q = [(c[0] - 42, c[1] + 42), (c[0] + 42, c[1] + 42), (c[0] + 42, c[1] - 42), (c[0] - 42, c[1] - 42)]
    b += poly(Q, INK) + axis(mid(Q[0], Q[1]), mid(Q[2], Q[3])) + axis(mid(Q[1], Q[2]), mid(Q[3], Q[0]))
    b += axis(Q[0], Q[2]) + axis(Q[1], Q[3]) + dot(*c, 5, GREEN)
    # круг
    c = cs[3]
    b += circle(c[0], c[1], 52, INK, 2.2)
    for a in (0, 30, 60, 90, 120, 150):
        b += axis(pol(c, 52, a), pol(c, 52, a + 180), 8)
    b += dot(*c, 5, GREEN)
    # равнобедренный
    c = cs[4]
    T = [(c[0], c[1] - 60), (c[0] - 38, c[1] + 50), (c[0] + 38, c[1] + 50)]
    b += poly(T, INK) + axis(T[0], mid(T[1], T[2]))
    # параллелограмм
    c = cs[5]
    Pp = [(c[0] - 66, c[1] + 34), (c[0] + 34, c[1] + 34), (c[0] + 66, c[1] - 34), (c[0] - 34, c[1] - 34)]
    b += poly(Pp, INK) + dot(*c, 5, GREEN)
    for c, n in zip(cs, names):
        b += tx(c[0], c[1] + 82, n, MUTED, 16)
    return S(W, H, b), 'Пунктир — оси симметрии, зелёная точка — центр.'


@at('бывает ось без центра и центр без оси')
def c9_counter():
    W, H = 440, 240
    T, Bl, Br = ISO
    c = (T[0], (T[1] + Bl[1]) / 2)
    img = [rot(p, c, 180) for p in ISO]
    b = poly(ISO, INK) + poly(img, RED, RED, 0.18, 2, DASH) + dot(*c, 4.5, GOLD)
    m1, m2 = mid(PAR[0], PAR[1]), mid(PAR[2], PAR[3])
    fl = [reflect(p, m1, m2) for p in PAR]
    b += poly(PAR, INK) + poly(fl, RED, RED, 0.18, 2, DASH) + seg(m1, m2, GOLD, 2, DASH)
    b += tx(110, 232, 'пол-оборота — не совпало', RED, NS) + tx(330, 232, 'перегиб — не совпало', RED, NS)
    return S(W, H, b), 'Красное — где оказалась фигура после проверки: у треугольника нет центра, у параллелограмма нет оси.'


@at('у Р — ни оси, ни центра')
def c9_letters():
    need('у `А` — одна вертикальная ось', 'у `Н` — две оси и центр', 'у `О` — две оси и центр', 'у `Р` — ни оси, ни центра')
    W, H = 420, 160
    b = ''
    for k, (ch, v, hz) in enumerate((('А', 1, 0), ('Н', 1, 1), ('О', 1, 1), ('Р', 0, 0))):
        x, y = 60 + k * 100, 108
        b += tx(x, y, ch, INK, 84, weight=500)
        cy_ = y - 30
        if v:
            b += seg((x, cy_ - 52), (x, cy_ + 52), GOLD, 2, DASH)
        if hz:
            b += seg((x - 42, cy_), (x + 42, cy_), GOLD, 2, DASH) + dot(x, cy_, 5, GREEN)
    return S(W, H, b), ''


@at('между сторонами 7 и 4 (вторая)')
def c9_razbor():
    need('`7` см, `7` см и `4` см')
    W, H = 380, 270
    u = 24
    A, B, C = tri_sides((130, 225), 4 * u, 7 * u, 7 * u)
    b = poly([A, B, C], INK, sw=2.4)
    cen = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    for (p, q), s in zip(((A, C), (B, C)), ('7', '7')):
        b += label(mid(p, q), s, cen, 14, INK, NS, 600)
    b += tx(mid(A, B)[0] - 16, A[1] + 22, '4', INK, NS, weight=600)
    M = mid(A, B)
    b += seg(lerp(C, M, -0.08), lerp(C, M, 1.15), GREEN, 2.4, DASH)
    for V, P1, P2 in ((A, B, C), (B, A, C)):
        L1, L2 = dist(V, P1), dist(V, P2)
        F = lerp(P1, P2, L1 / (L1 + L2))       # основание биссектрисы угла V
        b += seg(lerp(V, F, -0.1), lerp(V, F, 1.12), RED, 2, DASH)
    b += tx(C[0] + 18, C[1] + 20, '7 = 7', GREEN, NS, 'start', 600)
    for V, P1, P2, side in ((A, B, C, 1), (B, A, C, -1)):
        L1, L2 = dist(V, P1), dist(V, P2)
        e = lerp(V, lerp(P1, P2, L1 / (L1 + L2)), 1.12)
        b += tx(e[0] + 8 * side, e[1] - 6, '7 ≠ 4', RED, NS, 'start' if side > 0 else 'end', 600)
    return S(W, H, b), 'Ось через вершину переводит одну выходящую из неё сторону в другую — они обязаны быть равны.'


@at('Пол-оборота разворачивает отрезок в обратную сторону, но наклон его не меняет', fx=True)
def c9_halfturn():
    W, H = 440, 230
    b = ''
    # центр — середина стороны: копия ложится на себя, концы меняются местами
    P, Q = (30, 160), (190, 70)
    M = mid(P, Q)
    b += seg(P, Q, GOLD, 4) + dot(*P, 5, GOLD) + dot(*Q, 5, GOLD) + dot(*M, 5, GREEN)
    b += turn(M, 180, seg(P, Q, BLUE, 2.4) + dot(*P, 6, BLUE), 0.4)
    b += g('fi', 1.8, tx(110, 215, 'центр в середине', GREEN, NS, weight=600))
    # центр не в середине: копия уезжает, оставаясь параллельной
    P, Q = (260, 150), (390, 80)
    nx, ny = -(Q[1] - P[1]), Q[0] - P[0]
    L = math.hypot(nx, ny)
    O = add(mid(P, Q), (-30 * nx / L, -30 * ny / L))     # центр в стороне от середины
    P2, Q2 = rot(P, O, 180), rot(Q, O, 180)
    assert abs((Q2[1] - P2[1]) * (Q[0] - P[0]) - (Q2[0] - P2[0]) * (Q[1] - P[1])) < 1e-6    # параллельна
    assert 0 < min(P2[1], Q2[1]) and max(P2[1], Q2[1]) < 200, (P2, Q2)
    b += seg(P, Q, GOLD, 4) + dot(*P, 5, GOLD) + dot(*Q, 5, GOLD) + dot(*O, 5, INK)
    b += turn(O, 180, seg(P, Q, RED, 2.4) + dot(*P, 6, RED), 2.2)
    b += g('fi', 3.6, tx(330, 215, 'центр не в середине', RED, NS, weight=600))
    return S(W, H, b), ('Пол-оборота переворачивает отрезок, не меняя наклона. На себя он ложится, только если центр — '
                        'его середина.')


@at('Перегни бумажный прямоугольник 6 × 3 см по диагонали', fx=True)
def c9_diag():
    need('прямоугольник `6 × 3` см')
    W, H = 400, 290
    u = 50
    A, B, C, D = (50, 270), (50 + 6 * u, 270), (50 + 6 * u, 270 - 3 * u), (50, 270 - 3 * u)
    b = poly([A, B, C, D], INK) + seg(A, C, GOLD, 2, DASH)
    half = poly([A, B, C], BLUE, BLUE, 0.3)
    b += flip(A, C, half, 0.5)
    Bf = reflect(B, A, C)
    assert Bf[1] > 0
    X = inter_ll(A, Bf, D, C)                   # где сторона копии пересекает верхнюю сторону
    b += g('fi', 2.1, poly([A, D, X], RED, RED, 0.3, 1.5) + tx(Bf[0] + 10, Bf[1] + 6, 'торчит', RED, NS, 'start', 600) +
           tx(D[0], D[1] - 10, 'не закрыто', RED, NS, 'start', 600))
    return S(W, H, b), ''


# ═══ Глава 10 ═══

def node(x0, y0, c):
    return lambda i, j: (x0 + i * c, y0 + j * c)


FLAG = [(1, 1), (3, 1.75), (1, 2.5)]
POLE = [(1, 1), (1, 4)]


def flag_svg(N, pts, pole, col, op=0.35):
    return poly([N(*p) for p in pts], col, col, op, 2) + seg(N(*pole[0]), N(*pole[1]), col, 3)


@at('сдвигает всю плоскость целиком')
def c10_four():
    W, H = 440, 440
    b = arrow_defs_p('g101', [GREEN])
    c = 24
    titles = ['осевая симметрия', 'центральная симметрия', 'поворот', 'параллельный перенос']
    for k, ttl in enumerate(titles):
        x0, y0 = 14 + (k % 2) * 220, 20 + (k // 2) * 220
        b += cells(x0, y0, 8, 6, c)
        N = node(x0, y0, c)
        b += flag_svg(N, FLAG, POLE, GOLD)
        if k == 0:
            m = lambda p: (8 - p[0], p[1])
            b += seg(N(4, -0.3), N(4, 6.3), GOLD, 2.2, DASH)
        elif k == 1:
            m = lambda p: (8 - p[0], 5 - p[1])
            b += dot(*N(4, 2.5), 5, GOLD)
        elif k == 2:
            m = lambda p: (4 + (p[1] - 2.5), 2.5 - (p[0] - 4))       # четверть оборота против часовой
            b += dot(*N(4, 2.5), 5, GOLD)
        else:
            m = lambda p: (p[0] + 4, p[1] + 1)
            b += arrow(N(2, 4.6), N(6, 5.6), GREEN, 'g1010', 2)
        b += flag_svg(N, [m(p) for p in FLAG], [m(p) for p in POLE], GREEN)
        b += tx(x0 + 4 * c, y0 + 6 * c + 26, ttl, INK, NS, weight=600)
    return S(W, H, b), 'Жёлтый флажок — исходный, зелёный — образ.'


@at('каждая точка едет на 5 клеток вправо и на 2 вниз')
def c10_rules():
    need('на `3` клетки левее оси → образ на `3` клетки правее оси', 'на `3` клетки правее `O` и на `1` выше',
         'перенос на `5` клеток вправо и `2` вниз')
    W, H = 380, 470
    c = 28
    b = arrow_defs_p('g102', [BLUE, GREEN])

    def stepped(N, p, legs, col, mk):
        """Ходы по линиям сетки от точки p: legs = [(dx, dy), …] в клетках."""
        out = ''
        for dx, dy in legs:
            q = (p[0] + dx, p[1] + dy)
            out += arrow(N(*p), N(*q), col, mk, 2.4)
            m = mid(N(*p), N(*q))
            out += tx(m[0] + (0 if dx else 12), m[1] + (-8 if dx else 5), str(abs(dx or dy)), col, NS, weight=600)
            p = q
        return out
    # осевая
    x0, y0 = 50, 30
    N = node(x0, y0, c)
    b += tx(x0, y0 - 10, 'осевая симметрия', INK, NS, 'start', 600) + cells(x0, y0, 10, 3, c)
    b += seg(N(5, -0.2), N(5, 3.2), GOLD, 2.4, DASH)
    b += stepped(N, (2, 2), [(3, 0)], BLUE, 'g1020') + stepped(N, (5, 2), [(3, 0)], GREEN, 'g1021')
    b += dot(*N(2, 2), 5, GOLD) + dot(*N(8, 2), 5, GREEN)
    # центральная
    y0 = 180
    N = node(x0, y0, c)
    b += tx(x0, y0 - 10, 'центральная симметрия', INK, NS, 'start', 600) + cells(x0, y0, 10, 4, c)
    O = (5, 2)
    b += stepped(N, O, [(3, 0), (0, -1)], BLUE, 'g1020') + stepped(N, O, [(-3, 0), (0, 1)], GREEN, 'g1021')
    b += dot(*N(*O), 5, INK) + pname(N(*O), 'O', -10, -12) + dot(*N(8, 1), 5, GOLD) + dot(*N(2, 3), 5, GREEN)
    # перенос
    y0 = 350
    N = node(x0, y0, c)
    b += tx(x0, y0 - 10, 'перенос', INK, NS, 'start', 600) + cells(x0, y0, 10, 3, c)
    b += stepped(N, (2, 0.5), [(5, 0), (0, 2)], GREEN, 'g1021')
    b += dot(*N(2, 0.5), 5, GOLD) + dot(*N(7, 2.5), 5, GREEN)
    return S(W, H, b), ''


C10 = 40
G10 = (30, 22)


def grid10(extra_rows=0):
    N = node(G10[0], G10[1], C10)
    return N, cells(G10[0], G10[1], 8, 4, C10)


@at('· · · · · · B · ·', zamena=True)
def c10_grid1():
    W, H = 380, 210
    N, b = grid10()
    for (i, j), s, col in (((1, 1), 'A', GOLD), ((4, 2), 'O', INK), ((6, 3), 'B', GOLD)):
        b += dot(*N(i, j), 6, col) + pname(N(i, j), s, 13, -13, col)
    assert (1 - 4, 1 - 2) == (-3, -1) and (6 - 4, 3 - 2) == (2, 1)
    return S(W, H, b), ''


@at('B A₁', zamena=True, fx=True)
def c10_grid2():
    W, H = 380, 210
    N, b = grid10()
    b += arrow_defs_p('g104', [GOLD, GREEN])
    O = (4, 2)

    def legs(p, mk, col):
        mid_ = (p[0], O[1])
        return (seg(N(*O), N(*mid_), col, 2.6) + arrow(N(*mid_), N(*p), col, mk, 2.6))
    b += legs((1, 1), 'g1040', GOLD) + legs((6, 3), 'g1040', GOLD)
    b += turn(N(*O), 180, legs((1, 1), 'g1041', GREEN), 0.4) + turn(N(*O), 180, legs((6, 3), 'g1041', GREEN), 2.2)
    for (i, j), s, col, d in (((1, 1), 'A', GOLD, None), ((6, 3), 'B', GOLD, None), ((4, 2), 'O', INK, None),
                              ((7, 3), 'A₁', GREEN, 1.8), ((2, 1), 'B₁', GREEN, 3.6)):
        p = dot(*N(i, j), 6, col) + pname(N(i, j), s, 14, -13, col)
        b += g('fi', d, p) if d else p
    return S(W, H, b), 'Пол-оборота вокруг O разворачивает оба хода сразу: «влево» становится «вправо», «вверх» — «вниз».'


@at('Оба отрезка — диагонали одинаковых прямоугольников')
def c10_compare():
    need('`5` клеток вправо и `2` вниз', '`5` клеток влево и `2` вверх')
    W, H = 380, 230
    N, b = grid10()
    A, B, A1, B1 = (1, 1), (6, 3), (7, 3), (2, 1)
    b += poly([N(1, 1), N(6, 1), N(6, 3), N(1, 3)], GOLD, sw=1.8, dash=DASH)
    b += poly([N(2, 1), N(7, 1), N(7, 3), N(2, 3)], GREEN, sw=1.8, dash='3 5')
    b += seg(N(*A), N(*B), GOLD, 3) + seg(N(*A1), N(*B1), GREEN, 3)
    b += tx(*add(N(3.5, 1), (0, -8)), '5', GOLD, NS, weight=600) + tx(*add(N(1, 2), (-12, 5)), '2', GOLD, NS, weight=600)
    b += tx(*add(N(4.5, 3), (0, 22)), '5', GREEN, NS, weight=600) + tx(*add(N(7, 2), (12, 5)), '2', GREEN, NS, weight=600)
    for p, s, col, dx in ((A, 'A', GOLD, -14), (B, 'B', GOLD, -14), (A1, 'A₁', GREEN, 16), (B1, 'B₁', GREEN, 16)):
        b += dot(*N(*p), 5, col) + pname(N(*p), s, dx, -12 if p[1] == 1 else 14, col)
    return S(W, H, b), ''


@at('и A, и B съедут на 2 клетки вправо')
def c10_err1():
    need('От `A` до `B`: `5` клеток вправо и `2` вниз')
    W, H = 440, 200
    c = 22
    b = ''
    for k, ok in enumerate((False, True)):
        x0 = 12 + k * 220
        N = node(x0, 20, c)
        b += cells(x0, 20, 9, 4, c)
        A, B = (1, 1), (6, 3)
        b += seg(N(*A), N(*B), GOLD, 3) + dot(*N(*A), 5, GOLD) + dot(*N(*B), 5, GOLD)
        b += pname(N(*A), 'A', -12, -10, GOLD) + pname(N(*B), 'B', -12, 14, GOLD)
        col = GREEN if ok else RED
        A2 = (A[0] + 2, A[1]) if ok else A
        B2 = (B[0] + 2, B[1])
        b += seg(N(*A2), N(*B2), col, 3, None if ok else DASH) + dot(*N(*B2), 5, col)
        if ok:
            b += dot(*N(*A2), 5, col)
        b += tx(x0 + 4.5 * c, 155, 'обе точки на 2 вправо' if ok else 'сдвинута только B', col, NS, weight=600)
    return S(W, H, b), ''


@at('Верный образ — «3 вправо, 1 вниз»')
def c10_err2():
    need('«`3` вправо, `1` вверх»', '«`3` вправо, `1` вниз»')
    W, H = 380, 220
    N, b = grid10()
    b += dot(*N(4, 2), 6, INK) + pname(N(4, 2), 'O', -12, -14)
    b += dot(*N(1, 1), 6, GOLD) + pname(N(1, 1), 'A', -12, -14, GOLD)
    b += dot(*N(7, 1), 6, RED) + tx(*add(N(7, 1), (0, -14)), 'ошибка', RED, NS, weight=600)
    b += dot(*N(7, 3), 6, GREEN) + tx(*add(N(7, 3), (0, 28)), 'верно', GREEN, NS, weight=600)
    b += seg(N(4, -0.2), N(4, 4.2), RED, 1.4, DOT)
    return S(W, H, b), 'Красная точка — отражение в вертикальной оси: поменяли только «влево» на «вправо».'


@at('отрезок лёг на ту же линию и снова пересекает ось')
def c10_err3():
    need('на `4` клетки левее оси и на `2` клетки правее', 'на `4` клетки правее оси и на `2` клетки левее')
    W, H = 440, 220
    c = 28
    x0, y0 = 24, 26
    N = node(x0, y0, c)
    b = cells(x0, y0, 14, 5, c)
    ax = 6
    b += seg(N(ax, -0.3), N(ax, 5.3), GOLD, 2.4, DASH)
    y = 1.5
    b += seg(N(ax - 4, y), N(ax + 2, y), GOLD, 7) + dot(*N(ax - 4, y), 6, GOLD) + dot(*N(ax + 2, y), 6, GOLD)
    b += seg(N(ax - 2, y), N(ax + 4, y), GREEN, 3) + dot(*N(ax - 2, y), 5, GREEN) + dot(*N(ax + 4, y), 5, GREEN)
    b += tx(*add(N(ax - 2, y), (0, -14)), '4', GOLD, NS, weight=600) + tx(*add(N(ax + 1, y), (0, -14)), '2', GOLD, NS, weight=600)
    b += tx(*add(N(ax + 2, y), (0, 26)), '4', GREEN, NS, weight=600) + tx(*add(N(ax - 1, y), (0, 26)), '2', GREEN, NS, weight=600)
    y = 4
    b += seg(N(ax + 2, y), N(ax + 8, y), RED, 3, DASH) + dot(*N(ax + 2, y), 5, RED) + dot(*N(ax + 8, y), 5, RED)
    b += tx(*add(N(ax + 5, y), (0, 26)), 'ошибка: целиком справа', RED, NS, weight=600)
    return S(W, H, b), 'Жёлтый — отрезок, зелёный — его образ: каждый конец отразился сам, и отрезок снова пересекает ось.'
