"""Рисунки глав 1–6 учебника «Геометрия» (план: 26-27/school6/vis/plan_geometriya.md)."""
from geometriya_lib import *


# ═══ Глава 1 ═══

@at('Осталась одна геометрическая фигура')
def c1_plot():
    need('`24` м на `15` м')
    W, H = 440, 200
    sc = 6.5                                  # пикселей на метр: 24 м → 156
    w, h = 24 * sc, 15 * sc
    x0, y0 = 30, 40
    b = ''
    # участок: сетка по границе, столбики, домик, дерево
    b += poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], GREY, sw=1.6, dash='3 4')
    k = 0
    for i in range(7):
        for (px, py) in ((x0 + w * i / 6, y0), (x0 + w * i / 6, y0 + h)):
            b += rect(round(px - 2.5, 1), round(py - 2.5, 1), 5, 5, MUTED, 'none', 0)
    for j in range(1, 4):
        for px in (x0, x0 + w):
            b += rect(round(px - 2.5, 1), round(y0 + h * j / 4 - 2.5, 1), 5, 5, MUTED, 'none', 0)
    hx, hy = x0 + 30, y0 + 38
    b += rect(hx, hy, 40, 32, PINK, PINK, 1.5, extra=" fill-opacity='0.35'")
    b += poly([(hx - 5, hy), (hx + 20, hy - 20), (hx + 45, hy)], PINK, PINK, 0.6, 1.5)
    b += rect(hx + 15, hy + 14, 10, 18, DARK, 'none', 0)
    for tx_, ty in ((x0 + 102, y0 + 45), (x0 + 132, y0 + 60)):
        b += rect(tx_ - 3, ty + 10, 6, 18, '#8a6a4a', 'none', 0) + circle(tx_, ty, 15, GREEN, 1.5, GREEN,
                                                                          extra=" fill-opacity='0.45'")
    b += tx(x0 + w / 2, y0 + h + 34, 'участок', MUTED, NS)
    # то же — геометрическая фигура
    x1 = 250
    b += poly([(x1, y0), (x1 + w, y0), (x1 + w, y0 + h), (x1, y0 + h)], GOLD, GOLD, 0.12, 3)
    b += tx(x1 + w / 2, y0 - 12, '24 м', GOLD, NS)
    b += tx(x1 + w + 8, y0 + h / 2 + 5, '15 м', GOLD, NS, 'start')
    b += tx(x1 + w / 2, y0 + h + 34, 'прямоугольник', MUTED, NS)
    return S(W, H, b), 'Дом, деревья и столбики для вопроса про сетку не нужны: всё решают форма и два размера.'


@at('В разборе такая ошибка дала бы')
def c1_err():
    need('`P = 78` м', '`24 × 15 = 360`', '`360` м²')
    W, H = 440, 190
    sc = 6
    w, h = 24 * sc, 15 * sc
    b = ''
    for x0, ok in ((40, True), (256, False)):
        y0 = 35
        pts = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
        if ok:
            b += poly(pts, GREEN, sw=5)
            b += tx(x0 + w / 2, y0 + h / 2 + 6, 'P = 78 м', GREEN, 17, weight=600)
            b += tx(x0 + w / 2, y0 + h + 40, 'забор — граница', GREEN, NS)
        else:
            b += poly(pts, RED, RED, 0.3, 1.5)
            b += tx(x0 + w / 2, y0 + h / 2 + 6, '360 м²', RED, 17, weight=600)
            b += tx(x0 + w / 2, y0 + h + 40, 'площадь — не то', RED, NS)
        b += tx(x0 + w / 2, y0 - 10, '24 м', MUTED, 14) + tx(x0 - 8, y0 + h / 2 + 5, '15 м', MUTED, 14, 'end')
    return S(W, H, b), ''


# ═══ Глава 2 ═══

@at('Линия бывает прямая (бесконечная в обе стороны)')
def c2_lines():
    W, H = 420, 330
    b = arrow_defs_p('g21', [INK])
    mk = 'g210'
    y = 40
    # прямая, луч, отрезок
    b += arrow((80, y), (20, y), INK, mk) + arrow((80, y), (130, y), INK, mk)
    b += dot(160, y, 4.5, INK) + arrow((160, y), (270, y), INK, mk)
    b += seg((300, y), (400, y)) + dot(300, y, 4.5) + dot(400, y, 4.5)
    for x, s in ((75, 'прямая'), (215, 'луч'), (350, 'отрезок')):
        b += tx(x, y + 34, s, MUTED, NS)
    # ломаная, кривая
    y = 130
    zz = [(30, y + 20), (75, y - 20), (120, y + 15), (165, y - 15), (195, y + 18)]
    b += poly(zz, INK, closed=False) + ''.join(dot(x, yy, 3.5) for x, yy in zz)
    b += (f"<path d='M230,{y + 10} C270,{y - 50} 320,{y + 60} 395,{y - 10}' fill='none' stroke='{INK}' "
          f"stroke-width='2.2'/>")
    b += tx(112, y + 50, 'ломаная', MUTED, NS) + tx(312, y + 50, 'кривая', MUTED, NS)
    # замкнутые и незамкнутые
    y = 245
    b += circle(60, y, 34, GREEN, 2.4)
    b += poly(regpoly((160, y + 2), 36, 5), GREEN, sw=2.4)
    b += poly([(225, y + 25), (250, y - 30), (285, y + 10), (300, y - 25)], BLUE, closed=False, sw=2.4)
    b += arc((365, y + 14), 38, 20, 160, BLUE, 2.4)
    b += tx(110, y + 66, 'замкнутые', GREEN, NS) + tx(320, y + 66, 'незамкнутые', BLUE, NS)
    return S(W, H, b), ''


@at('тупоугольный один угол тупой')
def c2_tri_angles():
    need('`50°`, `60°`, `70°`', '`30°`, `60°`, `90°`', '`20°`, `40°`, `120°`')
    W, H = 440, 220
    b = ''
    specs = [(10, 50, 70, 'остроугольный'), (150, 90, 30, 'прямоугольный'), (290, 120, 20, 'тупоугольный')]
    for x0, a, bb, name in specs:
        c = 180 - a - bb
        x_ = x0 + (25 if a == 120 else 8)
        A, B, C = tri_angles((x_, 175), a, bb, 120)
        b += poly([A, B, C], INK, sw=2.2)
        for v, p1, p2, val in ((A, B, C, a), (B, C, A, bb), (C, A, B, c)):
            col = GOLD if val > 90 else (GREEN if val == 90 else MUTED)
            if val == 90:
                b += right_angle(v, p1, p2, 13, GREEN, 2)
                b += tx(v[0] + 34, v[1] - 8, '90°', GREEN, 14)
            else:
                r = 36 if val < 35 else (20 if val > 90 else 22)
                if a == 120 and val == 40:          # вершина у тупого угла: подпись снаружи, над вершиной
                    b += angle_arc(v, p1, p2, 22, col, 2) + tx(v[0] - 4, v[1] - 12, '40°', INK, 14)
                elif val == 120:
                    b += angle_arc(v, p1, p2, r, col, 2)
                    p = pol(v, 34, 60)
                    b += tx(p[0] + 4, p[1] + 5, '120°', col, 14)
                else:
                    b += angle_arc(v, p1, p2, r, col, 2, f'{val}°', col if val > 90 else INK, 14)
        b += tx(x0 + 68, 210, name, MUTED, NS)
    return S(W, H, b), ''


@at('Треугольник не замыкается')
def c2_no_fourth():
    W, H = 440, 210
    b = arrow_defs_p('g23', [RED])
    for x0, a, txt in ((30, 90, 'параллельны'), (250, 112, 'расходятся')):
        P, Q = (x0 + 30, 170), (x0 + 130, 170)
        b += seg(P, Q, INK, 2.6)
        p2, q2 = pol(P, 135, a), pol(Q, 135, 180 - a)
        b += arrow(P, p2, RED, 'g230') + arrow(Q, q2, RED, 'g230')
        if a == 90:
            b += right_angle(P, Q, p2, 12, GOLD) + right_angle(Q, P, q2, 12, GOLD)
        else:
            b += angle_arc(P, Q, p2, 20, GOLD) + angle_arc(Q, P, q2, 20, GOLD)
        b += tx(x0 + 80, 200, 'не встречаются' if a == 90 else txt, RED, NS)
    return S(W, H, b), ''


@at('равны только две стороны')
def c2_sides_sets():
    need('`4`, `5` и `6` см', '`3`, `3` и `2` см', '`3`, `3` и `3` см')
    W, H = 440, 270
    u = 22
    b = sets([(305, 140, 130, 118, BLUE, 'равнобедренные', (300, 54)),
              (340, 160, 78, 66, GREEN, 'равносторонние', (340, 86))])
    b += tx(76, 46, 'разносторонние', MUTED, NS, weight=600)

    def tri(P, c, s1, s2, col, labs):
        A, B, C = tri_sides(P, c * u, s1 * u, s2 * u)
        out = poly([A, B, C], col, col, 0.18, 2.2)
        cen = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
        for (p, q), s in zip(((A, B), (A, C), (B, C)), labs):
            m = mid(p, q)
            out += label(m, s, cen, 16, INK, 15, 500)
        return out, (A, B, C)
    o, _ = tri((10, 205), 6, 4, 5, MUTED, ('6', '4', '5'))
    b += o
    o, (A, B, C) = tri((200, 205), 2, 3, 3, BLUE, ('2', '3', '3'))
    b += o + ticks(A, C, 1, BLUE) + ticks(B, C, 1, BLUE)
    o, (A, B, C) = tri((307, 200), 3, 3, 3, GREEN, ('3', '3', '3'))
    b += o + ticks(A, C, 1, GREEN) + ticks(B, C, 1, GREEN) + ticks(A, B, 1, GREEN)
    return S(W, H, b), 'Равносторонний лежит внутри равнобедренных: у него равны две стороны и ещё третья.'


@at('→ ромб (все стороны равны)', zamena=True)
def c2_ladder():
    W, H = 440, 360
    b = arrow_defs_p('g25', [MUTED, BLUE])

    def box(cx, cy, name, cond, icon, col=MUTED):
        w = 212
        o = rect(cx - w / 2, cy - 24, w, 48 if not cond else 62, 'none', col, 1.6, 8)
        o += icon(cx - w / 2 + 28, cy)
        o += tx(cx - w / 2 + 58, cy + 6 - (7 if cond else 0), name, INK, NS, 'start', 600)
        if cond:
            o += tx(cx - w / 2 + 58, cy + 22, cond, MUTED, 14, 'start')
        return o

    def ic_quad(x, y): return poly([(x - 16, y + 10), (x + 14, y + 12), (x + 10, y - 11), (x - 9, y - 7)], INK, sw=1.6)
    def ic_par(x, y): return poly([(x - 18, y + 10), (x + 8, y + 10), (x + 18, y - 10), (x - 8, y - 10)], INK, sw=1.6)
    def ic_rect(x, y): return poly([(x - 18, y + 9), (x + 18, y + 9), (x + 18, y - 9), (x - 18, y - 9)], INK, sw=1.6)

    def ic_romb(x, y):
        A = (x - 18, y + 9)
        return poly([A, (A[0] + 22, A[1]), pol((A[0] + 22, A[1]), 22, 55), pol(A, 22, 55)], INK, sw=1.6)
    def ic_sq(x, y): return poly([(x - 12, y + 12), (x + 12, y + 12), (x + 12, y - 12), (x - 12, y - 12)], INK, sw=1.6)
    b += box(220, 34, 'четырёхугольник', None, ic_quad)
    b += box(220, 116, 'параллелограмм', None, ic_par, GOLD)
    b += box(112, 210, 'прямоугольник', 'все углы прямые', ic_rect, BLUE)
    b += box(328, 210, 'ромб', 'все стороны равны', ic_romb, BLUE)
    b += box(220, 316, 'квадрат', None, ic_sq, GREEN)
    b += arrow((220, 59), (220, 89), MUTED, 'g250')
    b += arrow((190, 141), (130, 183), BLUE, 'g251') + arrow((250, 141), (310, 183), BLUE, 'g251')
    b += arrow((130, 249), (190, 289), MUTED, 'g250') + arrow((310, 249), (250, 289), MUTED, 'g250')
    return S(W, H, b), 'Ветки расходятся после параллелограмма и снова сходятся в квадрате.'


@at('прямоугольник 2 × 5 см — не ромб')
def c2_counter():
    need('ромб с углами `70°` и `110°`', 'прямоугольник `2 × 5` см')
    W, H = 440, 210
    b = ''
    A = (30, 160)
    B = (A[0] + 110, A[1])
    D, C = pol(A, 110, 70), pol(B, 110, 70)
    b += poly([A, B, C, D], INK)
    for p, q in ((A, B), (B, C), (C, D), (D, A)):
        b += ticks(p, q, 1, GOLD)
    b += angle_arc(A, B, D, 24, GOLD, 2, '70°', INK, 14) + angle_arc(B, C, A, 22, GOLD, 2, '110°', INK, 14)
    b += tx(105, 198, 'не прямоугольник', RED, NS)
    s = 30
    x0, y0 = 250, 140
    P = [(x0, y0), (x0 + 5 * s, y0), (x0 + 5 * s, y0 - 2 * s), (x0, y0 - 2 * s)]
    b += poly(P, INK)
    for k in range(4):
        b += right_angle(P[k], P[(k + 1) % 4], P[k - 1], 11, GOLD)
    b += tx(x0 + 2.5 * s, y0 + 22, '5 см', MUTED, 14) + tx(x0 + 5 * s + 8, y0 - s + 5, '2 см', MUTED, 14, 'start')
    b += tx(x0 + 2.5 * s, 198, 'не ромб', RED, NS)
    return S(W, H, b), ''


@at('У параллелограмма параллельны обе пары противоположных сторон')
def c2_trap():
    W, H = 440, 200
    b = ''
    P = [(20, 150), (165, 150), (205, 55), (60, 55)]
    b += poly(P, INK)
    b += chevron(P[0], P[1], 1, GOLD) + chevron(P[3], P[2], 1, GOLD)
    b += chevron(P[0], P[3], 2, BLUE) + chevron(P[1], P[2], 2, BLUE)
    b += tx(112, 188, 'обе пары параллельны', INK, NS)
    T = [(232, 150), (425, 150), (405, 55), (300, 55)]
    b += poly(T, INK)
    b += chevron(T[0], T[1], 1, GOLD) + chevron(T[3], T[2], 1, GOLD)
    b += seg(T[0], T[3], RED, 2.6) + seg(T[1], T[2], RED, 2.6)
    b += tx(330, 188, 'параллельна одна пара', INK, NS)
    return S(W, H, b), ''


# ═══ Глава 3 ═══

@at('уложился 7 раз — длина 7 см', fx=True)
def c3_measure():
    need('уложился `7` раз — длина `7` см')
    W, H = 440, 150
    u = 40
    b = ''
    src = (16, 60)
    x0 = 120
    b += seg((x0, 92), (x0 + 7 * u, 92), INK, 3) + dot(x0, 92, 4) + dot(x0 + 7 * u, 92, 4)
    brick = lambda: rect(src[0], src[1], u, 22, GOLD, GOLD, 1.5, extra=" fill-opacity='0.55'")
    b += brick() + tx(src[0] + u / 2, src[1] - 10, '1 см', GOLD, NS)
    for k in range(7):
        d = 0.3 + 0.6 * k
        b += g('sl', d, rect(src[0], src[1], u, 22, GOLD, DARK, 1.5, extra=" fill-opacity='0.8'"),
               f';--to:translate({x0 + k * u - src[0]}px,{92 - 22 - src[1]}px)')
        b += g('fi', d + 1.0, tx(x0 + k * u + u / 2, 118, str(k + 1), MUTED, 14))
    b += g('fi', 5.0, tx(x0 + 3.5 * u, 144, '7 см', GREEN, 17, weight=600))
    return S(W, H, b), ''


@at('1,25 м и 125 см — это один и тот же отрезок')
def c3_two_scales():
    need('`1,25` м и `125` см')
    W, H = 440, 170
    x0, L = 30, 300                          # 1 м = 300 px
    y = 85
    b = seg((x0, y), (x0 + 1.25 * L, y), GOLD, 6)
    for v, s in ((0, '0'), (1, '1 м'), (1.25, '1,25 м')):
        x = x0 + v * L
        b += seg((x, y - 14), (x, y - 4), MUTED, 1.6) + tx(x, y - 22, s, INK, NS)
    for cm in range(0, 126, 25):
        x = x0 + cm / 100 * L
        b += seg((x, y + 4), (x, y + 14), MUTED, 1.6)
        b += tx(x, y + 34, f'{cm}' + (' см' if cm == 125 else ''), INK, NS)
    b += tx(x0, 30, 'в метрах', MUTED, 14, 'start') + tx(x0, 150, 'в сантиметрах', MUTED, 14, 'start')
    return S(W, H, b), 'Отрезок один и тот же — поменялась только мерка, поэтому поменялось число.'


@at('Множитель сработал дважды', fx=True)
def c3_area():
    need('`1` м `= 100` см', '`100 × 100 = 10 000`')
    W, H = 420, 340
    x0, y0, s = 110, 40, 250
    c = s / 100
    b = (f"<defs><pattern id='g33p' width='{c}' height='{c}' patternUnits='userSpaceOnUse'>"
         f"<path d='M{c} 0 L0 0 0 {c}' fill='none' stroke='{DARK}' stroke-width='0.6'/></pattern>"
         f"<clipPath id='g33c'><rect x='{x0}' y='{y0}' width='{s}' height='{s}'/></clipPath></defs>")
    b += rect(x0, y0, s, s, 'none', INK, 2)
    b += tx(x0 + s / 2, y0 - 12, '1 м = 100 см', INK, NS)
    b += tx(x0 - 10, y0 + s / 2 - 4, '1 м =', INK, NS, 'end') + tx(x0 - 10, y0 + s / 2 + 16, '100 см', INK, NS, 'end')
    rowb = lambda: (rect(x0, y0 + s - c, s, c, GOLD, 'none', 0) + rect(x0, y0 + s - c, s, c, "url(#g33p)", 'none', 0))
    b += g('fi', 0.3, rect(x0, y0 + s - 3 * c, s, 3 * c, GOLD, 'none', 0) +
           tx(x0 + s / 2, y0 + s + 24, 'ряд: 100 квадратиков по 1 см²', GOLD, 14))
    fill = (rect(x0, y0 + s, s, s, GOLD, 'none', 0, extra=" fill-opacity='0.55'") +
            rect(x0, y0 + s, s, s, "url(#g33p)", 'none', 0))
    b += f"<g clip-path='url(#g33c)'>" + g('sl', 1.6, fill, f';--to:translate(0px,{-s}px)') + '</g>'
    b += g('fi', 3.1, tx(x0 + s + 10, y0 + s / 2 + 5, '100', GOLD, NS, 'start') +
           tx(x0 + s + 10, y0 + s / 2 + 23, 'рядов', GOLD, 14, 'start'))
    b += g('fi', 3.7, rect(x0 + 35, y0 + s / 2 - 22, s - 70, 40, DARK, 'none', 0, 8, " fill-opacity='0.85'") +
           tx(x0 + s / 2, y0 + s / 2 + 5, '100 × 100 = 10 000', INK, 17, weight=600))
    return S(W, H, b), 'Сто квадратиков ложатся вдоль, и таких рядов сто поперёк.'


@at('Число 0,4 меньше числа 45')
def c3_compare():
    need('`0,4` м `= 40` см', '`40 < 45`')
    W, H = 440, 160
    x0, k = 30, 7.6                      # пикселей на сантиметр
    b = rect(x0, 30, 40 * k, 26, GOLD, 'none', 0, 3, " fill-opacity='0.75'")
    b += tx(x0 + 8, 48, '0,4 м = 40 см', DARK, NS, 'start', 600)
    b += rect(x0, 66, 45 * k, 26, GREEN, 'none', 0, 3, " fill-opacity='0.75'")
    b += tx(x0 + 8, 84, '45 см', DARK, NS, 'start', 600)
    y = 112
    b += seg((x0, y), (x0 + 50 * k, y), MUTED, 1.6)
    for cm in range(0, 51, 10):
        x = x0 + cm * k
        b += seg((x, y - 5), (x, y + 5), MUTED, 1.6) + tx(x, y + 26, str(cm) + (' см' if cm == 50 else ''), INK, 14)
    return S(W, H, b), ''


# ═══ Глава 4 ═══

@at('A---------C', zamena=True)
def c4_bac():
    W, H = 400, 210
    A = (60, 175)
    C = (360, 175)
    B = pol(A, 175, 55)
    b = angmark(A, 0, 55, 34, GOLD)
    b += seg(A, C, INK, 2.6) + seg(A, B, INK, 2.6)
    b += dot(*A, 5, GOLD) + dot(*B, 4) + dot(*C, 4)
    b += pname(A, 'A', -14, 8, GOLD) + pname(B, 'B', 12, -4) + pname(C, 'C', 0, 20)
    return S(W, H, b), ''


@at('развёрнутый ровно 180°')
def c4_kinds():
    need('меньше `90°`', 'ровно `90°`', 'больше `90°`, но меньше `180°`', 'ровно `180°`', '`360°`')
    W, H = 440, 330
    b = ''
    r = 70
    specs = [((25, 120), 50, 'острый', 'меньше 90°'), ((170, 120), 90, 'прямой', '90°'),
             ((330, 120), 130, 'тупой', 'больше 90°,')]
    for V, a, name, val in specs:
        p1, p2 = pol(V, r + 20, 0), pol(V, r + 20, a)
        b += seg(V, p1) + seg(V, p2) + dot(*V, 3.5)
        if a == 90:
            b += right_angle(V, p1, p2, 16, GOLD, 2.2)
        else:
            b += angmark(V, 0, a, 26, GOLD)
        cx = 70 if a == 50 else (215 if a == 90 else 370)
        b += tx(cx, V[1] + 32, name, INK, NS, weight=600) + tx(cx, V[1] + 52, val, MUTED, 14)
        if a == 130:
            b += tx(cx, V[1] + 70, 'меньше 180°', MUTED, 14)
    V = (110, 265)
    b += seg((V[0] - 90, V[1]), (V[0] + 90, V[1])) + dot(*V, 3.5) + angmark(V, 0, 180, 30, GOLD)
    b += tx(V[0], V[1] + 30, 'развёрнутый — 180°', INK, NS)
    V = (330, 252)
    b += seg(V, (V[0] + 90, V[1])) + dot(*V, 3.5) + arc(V, 30, 0, 359.9, GOLD, 2.2)
    b += tx(V[0], V[1] + 52, 'полный — 360°', INK, NS)
    return S(W, H, b), ''


@at('на другой стоит 130°')
def c4_protractor():
    need('стоит `50°`, на другой стоит `130°`')
    W, H = 440, 310
    O = (220, 205)
    R = 190
    b = (f"<path d='M{O[0] - R},{O[1]} A{R},{R} 0 0 1 {O[0] + R},{O[1]} Z' fill='{BLUE}' fill-opacity='0.07' "
         f"stroke='{MUTED}' stroke-width='1.6'/>")
    for a in range(0, 181, 10):
        b += seg(pol(O, R, a), pol(O, R - (12 if a % 50 and a % 90 else 18), a), MUTED, 1.3)
    for a, lab in ((4, True), (50, False), (90, True), (176, True)):
        v = {4: 0, 176: 180}.get(a, a)
        if lab:
            p = pol(O, R - 32, a)
            b += tx(p[0], p[1] + 5, str(v), MUTED, 14)
            p = pol(O, R - 64, a)
            b += tx(p[0], p[1] + 5, str(180 - v), MUTED, 14)
    p = pol(O, R - 30, 44)
    b += tx(p[0], p[1] + 6, '50', GREEN, 18, weight=600)
    p = pol(O, R - 66, 42)
    b += tx(p[0], p[1] + 6, '130', RED, 18, weight=600)
    b += seg(O, pol(O, R + 12, 0), GOLD, 2.8) + seg(O, pol(O, R + 12, 50), GOLD, 2.8)
    b += angmark(O, 0, 50, 34, GOLD) + dot(*O, 4, GOLD)
    b += tx(O[0] + R - 10, O[1] + 24, 'ноль здесь', MUTED, 14)
    b += tx(O[0], O[1] + 52, '50° — по шкале, где стоит ноль', GREEN, NS)
    b += tx(O[0], O[1] + 74, '130° — по другой шкале', RED, NS)
    return S(W, H, b), ''


@at('его биссектриса даёт два угла по 27°')
def c4_bisector():
    need('`∠AOB = 54°`', 'два угла по `27°`')
    W, H = 400, 220
    O = (40, 200)
    b = seg(O, pol(O, 330, 0)) + seg(O, pol(O, 215, 54)) + seg(O, pol(O, 330, 27), GOLD, 2.6)
    b += angmark(O, 0, 27, 70, BLUE, '27°', INK, tr=92) + angmark(O, 27, 54, 70, BLUE, '27°', INK, tr=92)
    b += angmark(O, 0, 54, 150, MUTED)
    p = pol(O, 172, 44)
    b += tx(p[0], p[1] + 5, '54°', MUTED, NS)
    b += dot(*O, 4) + pname(O, 'O', -12, 10) + pname(pol(O, 330, 0), 'A', 0, 18) + pname(pol(O, 215, 54), 'B', 14, 0)
    return S(W, H, b), ''


@at('второй кусок равен 70 − 25 = 45°')
def c4_add():
    need('угол `25°`', '`70 − 25 = 45°`')
    W, H = 400, 220
    O = (40, 200)
    b = seg(O, pol(O, 330, 0)) + seg(O, pol(O, 200, 70)) + seg(O, pol(O, 320, 25), BLUE, 2.6)
    b += angmark(O, 0, 25, 80, GOLD, '25°', GOLD, tr=104) + angmark(O, 25, 70, 80, GREEN, '45°', GREEN, tr=104)
    b += angmark(O, 0, 70, 160, MUTED, '70°', MUTED, tr=178)
    return S(W, H, b), ''


@at('соседи, но не смежные')
def c4_adjacent():
    need('`180 − 40 = 140°`', 'углы `25°` и `45°`')
    W, H = 440, 200
    V = (115, 150)
    b = seg((V[0] - 100, V[1]), (V[0] + 100, V[1]), GREEN, 3) + seg(V, pol(V, 110, 40))
    b += angmark(V, 0, 40, 34, GOLD, '40°', INK) + angmark(V, 40, 180, 26, BLUE, '140°', INK, tr=48)
    b += tx(V[0], 188, 'смежные', GREEN, NS, weight=600)
    V = (290, 150)
    b += seg(V, pol(V, 140, 0), RED, 2.4) + seg(V, pol(V, 120, 70), RED, 2.4) + seg(V, pol(V, 140, 25))
    b += angmark(V, 0, 25, 60, GOLD, '25°', INK, tr=80) + angmark(V, 25, 70, 44, BLUE, '45°', INK, tr=64)
    b += tx(V[0] + 60, 188, 'соседи, не смежные', RED, NS, weight=600)
    return S(W, H, b), ''


@at('Оба дополняют один и тот же', )
def c4_vertical():
    need('`∠1 + ∠2 = 180°`', '`∠3 + ∠2 = 180°`')
    W, H = 440, 240
    b = ''
    L1, L2 = 35, 115
    for cx, pair, line_a in ((110, (1, 2), L2), (330, (3, 2), L1)):
        c = (cx, 110)
        b += seg(pol(c, 100, L1), pol(c, 100, L1 + 180)) + seg(pol(c, 100, L2), pol(c, 100, L2 + 180))
        b += seg(pol(c, 100, line_a), pol(c, 100, line_a + 180), GREEN, 3.2)
        sectors = {1: (L1, L2), 2: (L2 + 180, L1 + 360), 3: (L1 + 180, L2 + 180), 4: (L2, L1 + 180)}
        for k, (a1, a2) in sectors.items():
            col = GOLD if k == pair[0] else (BLUE if k == 2 else None)
            if col:
                b += angmark(c, a1, a2, 32, col, fillop=0.25)
            am = (a1 + a2) / 2
            p = pol(c, 54, am)
            b += tx(p[0], p[1] + 5, f'∠{k}', col or MUTED, NS, weight=600 if col else None)
        b += tx(cx, 230, f'∠{pair[0]} + ∠2 = 180°', INK, NS)
    return S(W, H, b), 'Каждый из двух вертикальных вместе с ∠2 даёт развёрнутый угол.'


@at('без щелей и без нахлёста', fx=True)
def c4_tri_sum():
    need('`180°`')
    W, H = 440, 230
    A, B, C = (30, 190), (210, 190), (85, 45)
    a = ang_of(A, C)                     # угол при A от AB (0°) до AC
    bdir = ang_of(B, C)                  # у B: от BC до BA (180°)
    ca, cb = ang_of(C, A), ang_of(C, B)
    r = 34
    wA = sector(A, r, 0, a, GOLD, 0.7)
    wB = sector(B, r, bdir, 180, BLUE, 0.7)
    wC = sector(C, r, ca, cb, GREEN, 0.7)
    b = wA + wB + wC + poly([A, B, C], INK)
    P = (330, 190)
    b += seg((235, 190), (425, 190), MUTED, 1.6, DASH) + dot(*P, 3)
    b += g('sl', 0.3, wA, f';--to:translate({P[0] - A[0]}px,{P[1] - A[1]}px)')
    b += g('sl', 1.1, wB, f';--to:translate({P[0] - B[0]}px,{P[1] - B[1]}px)')
    b += g('sl', 1.9, turn(C, 180, wC, 1.9), f';--to:translate({P[0] - C[0]}px,{P[1] - C[1]}px)')
    b += g('fi', 3.4, angmark(P, 0, 180, 52, INK) + tx(P[0], P[1] - 64, '180°', INK, 17, weight=600))
    return S(W, H, b), 'Три угла ложатся рядом вершинами в одну точку и заполняют развёрнутый угол.'


@at('Обойду их по кругу и назову подряд')
def c4_razbor():
    need('верхний — `∠1` (это и есть данные `68°`)')
    W, H = 400, 250
    c = (200, 125)
    L1, L2 = 56, 124
    assert L2 - L1 == 68
    b = seg(pol(c, 120, L1), pol(c, 120, L1 + 180)) + seg(pol(c, 120, L2), pol(c, 120, L2 + 180))
    b += angmark(c, L1, L2, 40, GOLD, fillop=0.3)
    b += angmark(c, L2 + 180, L1 + 360, 30, BLUE) + angmark(c, L2, L1 + 180, 30, BLUE)
    b += angmark(c, L1 + 180, L2 + 180, 40, GOLD)
    p = pol(c, 70, 90)
    b += tx(p[0], p[1] + 5, '∠1 = 68°', GOLD, NS, weight=600)
    for k, am, col in ((2, 0, BLUE), (3, 270, GOLD), (4, 180, BLUE)):
        p = pol(c, 58, am)
        b += tx(p[0], p[1] + 5, f'∠{k}', col, NS, weight=600)
    return S(W, H, b), '∠2 и ∠4 — соседи ∠1 (смежные), ∠3 — напротив, через вершину (вертикальный).'


# ═══ Глава 5 ═══

U5 = 40                                  # 1 см = 40 px в построениях главы 5


def constr1(W=420):
    """Чертёж построения 1: AB = 6, раствор 4."""
    need('`AB = 6` см', 'например `4` см', '`AO = OB = 3` см')
    A, B = (90, 160), (90 + 6 * U5, 160)
    M, N = inter_cc(A, 4 * U5, B, 4 * U5)
    O = mid(A, B)
    return A, B, M, N, O


@at('Проведи по линейке прямую MN', fx=True)
def c5_c1():
    W, H = 420, 330
    A, B, M, N, O = constr1()
    r = 4 * U5
    aM = ang_of(A, M)
    b = seg(A, B, INK, 2.6) + dot(*A, 4) + dot(*B, 4) + pname(A, 'A', -14, 2) + pname(B, 'B', 14, 2)
    rad = seg(A, M, BLUE, 2.6)
    b += g('fi', 0.2, rad + tx(*add(mid(A, M), (-26, 0)), '4 см', BLUE, NS))
    b += arc(A, r, aM - 16, aM + 16, GOLD, 2.2, cls='dr', d=0.6, dur=0.7)
    b += arc(A, r, -aM - 16, -aM + 16, GOLD, 2.2, cls='dr', d=1.1, dur=0.7)
    b += turn(O, 180, rad, 1.8)
    b += g('fi', 3.1, tx(*add(mid(B, N), (30, 0)), '4 см', BLUE, NS))
    bM = ang_of(B, M)
    b += arc(B, r, bM - 16, bM + 16, GOLD, 2.2, cls='dr', d=3.2, dur=0.7)
    b += arc(B, r, -bM - 16, -bM + 16, GOLD, 2.2, cls='dr', d=3.7, dur=0.7)
    b += g('fi', 4.4, dot(*M, 4) + dot(*N, 4) + pname(M, 'M', 16, -4) + pname(N, 'N', 16, 6))
    b += seg(add(M, (0, -14)), add(N, (0, 14)), GREEN, 2.4, cls='dr', d=4.8)
    b += g('fi', 5.6, dot(*O, 4.5, GREEN) + pname(O, 'O', 14, 14, GREEN))
    return S(W, H, b), 'Из B дуги проводятся тем же раствором, что из A, — поэтому M и N одинаково далеки от A и B.'


@at('она называется серединный перпендикуляр', fx=True)
def c5_fold():
    W, H = 420, 330
    A, B, M, N, O = constr1()
    b = seg(add(M, (0, -14)), add(N, (0, 14)), GREEN, 2.4)
    b += seg(M, B, GREY, 2) + seg(N, B, GREY, 2) + seg(O, B, GREY, 2.6)
    b += seg(M, A, BLUE, 2.2) + seg(N, A, BLUE, 2.2) + seg(A, O, GOLD, 3)
    half = (poly([M, A, N], BLUE, BLUE, 0.25, 2.2) + seg(A, O, GOLD, 3) + dot(*A, 5, BLUE))
    b += flip(M, N, half, 0.5)
    for p, s, dx, dy in ((A, 'A', -14, 2), (B, 'B', 14, 2), (M, 'M', 16, -4), (N, 'N', 16, 6), (O, 'O', -12, 16)):
        b += dot(*p, 4) + pname(p, s, dx, dy)
    b += g('fi', 2.1, ticks(A, O, 1, GOLD) + ticks(O, B, 1, GOLD) + right_angle(O, M, B, 13, GREEN, 2) +
           right_angle(O, M, A, 13, GREEN, 2) + tx(O[0] + 30, O[1] - 26, '90°', GREEN, NS))
    return S(W, H, b), 'Перегнули по MN: A легла на B, отрезок OA — на OB, а два угла у O совпали.'


@at('А вне этой прямой точек, одинаково удалённых от A и B, нет')
def c5_equi():
    W, H = 440, 230
    b = ''
    for x0, ok in ((30, True), (250, False)):
        A, B = (x0, 180), (x0 + 160, 180)
        mx = x0 + 80
        b += seg((mx, 30), (mx, 210), GOLD if ok else GREY, 2, DASH)
        b += seg(A, B, INK, 2.4) + dot(*A, 4) + dot(*B, 4) + pname(A, 'A', -12, 12) + pname(B, 'B', 12, 12)
        Pp = (mx, 60) if ok else (mx + 45, 70)
        col = GREEN if ok else RED
        b += seg(Pp, A, col, 2.2) + seg(Pp, B, col, 2.2) + dot(*Pp, 5, col)
        if ok:
            b += ticks(Pp, A, 2, GREEN) + ticks(Pp, B, 2, GREEN)
        b += tx(mx, 225, 'на прямой: равны' if ok else 'вне прямой: не равны', col, NS)
    return S(W, H, b), ''


@at('между ними останется зазор')
def c5_small():
    need('например `2` см', '`6 − 2 − 2 = 2` см')
    W, H = 420, 210
    A, B = (90, 110), (90 + 6 * U5, 110)
    r = 2 * U5
    b = arc(A, r, -70, 70, GOLD, 2.2) + arc(B, r, 110, 250, GOLD, 2.2)
    b += seg(A, B, INK, 2.4) + dot(*A, 4) + dot(*B, 4) + pname(A, 'A', -14, 2) + pname(B, 'B', 14, 2)
    y = 175
    for x1, x2, s, col in ((A[0], A[0] + r, '2', MUTED), (A[0] + r, B[0] - r, '2 — зазор', RED), (B[0] - r, B[0], '2', MUTED)):
        b += seg((x1, y), (x2, y), col, 2.4 if col == RED else 1.4) + seg((x1, y - 6), (x1, y + 6), col, 1.4) + seg((x2, y - 6), (x2, y + 6), col, 1.4)
        b += tx((x1 + x2) / 2, y - 12, s, col, NS)
    return S(W, H, b), ''


@at('Эта прямая пройдёт через P и будет перпендикулярна a')
def c5_c2():
    W, H = 420, 290
    a1, a2 = (15, 175), (405, 135)
    P = (190, 35)
    F = foot(P, a1, a2)
    R = dist(P, F) * 1.3
    hlen = math.sqrt(R * R - dist(P, F) ** 2)
    ux, uy = (a2[0] - a1[0]) / dist(a1, a2), (a2[1] - a1[1]) / dist(a1, a2)
    X, Y = (F[0] - ux * hlen, F[1] - uy * hlen), (F[0] + ux * hlen, F[1] + uy * hlen)
    r = dist(X, Y) * 0.62
    Q1, Q2 = inter_cc(X, r, Y, r)
    assert Q1[1] > 5 and Q2[1] < H - 10, (Q1, Q2)
    b = seg(a1, a2, INK, 2.4) + tx(a2[0] - 8, a2[1] - 12, 'a', INK, LS, weight=600)
    aX, aY = ang_of(P, X), ang_of(P, Y)
    b += arc(P, R, aX - 12, aY + 12, BLUE, 2)
    for C, other in ((X, Y), (Y, X)):
        for q in (Q1, Q2):
            aq = ang_of(C, q)
            b += arc(C, r, aq - 14, aq + 14, GOLD, 2)
    b += seg(lerp(Q2, P, 1.12), lerp(P, Q2, 1.1), GREEN, 2.4)
    b += right_angle(F, P, a2, 12, GREEN, 2)
    for p, s, dx, dy in ((P, 'P', -14, -4), (X, 'X', -6, 20), (Y, 'Y', 8, 20)):
        b += dot(*p, 4.5) + pname(p, s, dx, dy)
    return S(W, H, b), 'P равноудалена от X и Y, поэтому лежит на серединном перпендикуляре к XY.'


@at('Проведи луч OC — это биссектриса')
def c5_c3():
    need('например `70°`')
    W, H = 420, 270
    O = (40, 240)
    rr = 120
    K, L = pol(O, rr, 0), pol(O, rr, 70)
    kl = dist(K, L)
    C = inter_cc(K, kl, L, kl)
    C = C[0] if dist(C[0], O) > dist(C[1], O) else C[1]
    assert abs(ang_of(O, C) - 35) < 0.01
    b = seg(O, pol(O, 360, 0)) + seg(O, pol(O, 230, 70))
    b += arc(O, rr, -6, 76, BLUE, 2)
    for Cc in (K, L):
        a = ang_of(Cc, C)
        b += arc(Cc, kl, a - 12, a + 12, GOLD, 2)
    b += seg(O, pol(O, 360, 35), GREEN, 2.6)
    b += seg(K, C, GOLD, 1.6, DASH) + seg(L, C, GOLD, 1.6, DASH)
    b += ticks(O, K, 1, BLUE) + ticks(O, L, 1, BLUE) + ticks(K, C, 2, GOLD) + ticks(L, C, 2, GOLD)
    for p, s, dx, dy in ((O, 'O', -12, 8), (K, 'K', 4, 20), (L, 'L', -16, -2), (C, 'C', 24, 14),
                         (pol(O, 360, 0), 'A', 0, 18), (pol(O, 230, 70), 'B', 14, 0)):
        b += dot(*p, 4) + pname(p, s, dx, dy)
    return S(W, H, b), ''


@at('Мы перенесли не сам угол, а три расстояния', fx=True)
def c5_c4():
    W, H = 440, 250
    A = (30, 135)
    rr = 95
    P, Q = pol(A, rr, 0), pol(A, rr, 50)
    B = (230, 225)
    sh = (B[0] - A[0], B[1] - A[1])
    P1, Q1 = add(P, sh), add(Q, sh)
    b = seg(A, pol(A, 180, 0)) + seg(A, pol(A, 135, 50)) + arc(A, rr, -8, 60, GREY, 1.6)
    b += seg(B, (430, B[1])) + pname((430, B[1]), 'K', 0, 18) + dot(*B, 4) + pname(B, 'B', -12, 10)
    for p, s, dx, dy in ((A, 'A', -12, 10), (P, 'P', 2, 18), (Q, 'Q', -14, -4)):
        b += dot(*p, 4) + pname(p, s, dx, dy)
    tri = [seg(A, P, BLUE, 3), seg(A, Q, BLUE, 3), seg(P, Q, GOLD, 3)]
    for k, s in enumerate(tri):
        b += s + g('sl', 0.4 + 0.8 * k, s, f';--to:translate({sh[0]}px,{sh[1]}px)')
    b += g('fi', 1.0, arc(B, rr, -8, 60, GREY, 1.6))
    b += g('fi', 3.3, dot(*P1, 4) + dot(*Q1, 4) + pname(P1, 'P₁', 4, 18) + pname(Q1, 'Q₁', -16, -6))
    b += seg(Q1, pol(B, 135, 50), INK, 2.2, cls='dr', d=3.7)
    b += g('fi', 4.6, angmark(B, 0, 50, 30, GREEN) + angmark(A, 0, 50, 30, GREEN))
    return S(W, H, b), 'Переехали три отрезка — значит и треугольник APQ, и угол при вершине.'


@at('Прямая через них пересечёт AB не в середине')
def c5_err():
    need('раствором `4` см, а из `B` — уже `5` см')
    W, H = 420, 330
    A, B = (60, 165), (60 + 6 * U5, 165)
    M, N = inter_cc(A, 4 * U5, B, 5 * U5)
    assert abs(M[0] - (A[0] + 2.25 * U5)) < 1e-6
    b = ''
    for C, r in ((A, 4 * U5), (B, 5 * U5)):
        for q in (M, N):
            a = ang_of(C, q)
            b += arc(C, r, a - 14, a + 14, GOLD, 2)
    b += seg(add(M, (0, -12)), add(N, (0, 12)), RED, 2.4)
    b += seg(A, B, INK, 2.4) + seg(A, M, BLUE, 1.6, DASH) + seg(B, M, BLUE, 1.6, DASH)
    b += tx(*add(mid(A, M), (-24, 0)), '4 см', BLUE, NS) + tx(*add(mid(B, M), (26, 0)), '5 см', BLUE, NS)
    Om = mid(A, B)
    b += dot(*Om, 4.5, GREY) + tx(Om[0] + 8, Om[1] + 24, 'середина', GREY, 14, 'start')
    b += dot(M[0], A[1], 4.5, RED)
    for p, s, dx, dy in ((A, 'A', -14, 2), (B, 'B', 14, 2)):
        b += dot(*p, 4) + pname(p, s, dx, dy)
    return S(W, H, b), ''


# ═══ Глава 6 ═══

CUBE = [(0, 4, 4), (4, 4, 4), (4, 0, 4), (0, 0, 4), (0, 4, 0), (4, 4, 0), (4, 0, 0), (0, 0, 0)]
CN = 'ABCDEFGH'
CI = {s: k for k, s in enumerate(CN)}


def E(a, b_):
    return tuple(sorted((CI[a], CI[b_])))


def cube_svg(s, ox, oy, depth=0.5, letters=True, **kw):
    P = obl_proj(s, depth, ox, oy, 4)
    out, Q, vis, edges = solid(CUBE, P, **kw)
    if letters:
        off = {'A': (-12, -6), 'B': (6, 14), 'C': (12, 10), 'D': (-12, 8), 'E': (-10, -10), 'F': (10, -10),
               'G': (12, 4), 'H': (12, -10)}
        for k, n in enumerate(CN):
            out += pname(Q[k], n, *off[n], size=LS)
    return out, Q, vis, edges


@at('E---------F', zamena=True)
def c6_cube():
    W, H = 320, 230
    out, Q, vis, edges = cube_svg(30, 50, 205, hcol=GOLD,
                                  estyle={E('E', 'H'): DOT, E('H', 'D'): DOT, E('H', 'G'): DASH})
    hidden = sorted(e for e, v in edges.items() if not v)
    assert hidden == sorted([E('H', 'E'), E('H', 'G'), E('H', 'D')]), hidden
    return S(W, H, out + dot(*Q[CI['H']], 4.5, GOLD)), ''


@at('идущие «в глубину» AE, BF, CG, DH')
def c6_quartets():
    need('`AB`, `DC`, `EF`, `HG`', '`AD`, `BC`, `EH`, `FG`', '`AE`, `BF`, `CG`, `DH`')
    b = ''
    for k, (quad, col) in enumerate((('AB DC EF HG', GOLD), ('AD BC EH FG', VIOLET), ('AE BF CG DH', CYAN))):
        ec = {E(p[0], p[1]): col for p in quad.split()}
        out, Q, vis, edges = cube_svg(18, 22 + k * 146, 160, ecol=ec, hcol=MUTED)
        out += ''.join(seg(Q[CI[p[0]]], Q[CI[p[1]]], col, 4, None if edges[E(p[0], p[1])] else DASH)
                       for p in quad.split())
        b += out + tx(76 + k * 146, 200, ', '.join(quad.split()), col, NS, weight=600)
    return S(440, 215, b), 'В каждой четвёрке рёбра параллельны и на рисунке.'


@at('нарисованы скошенными параллелограммами')
def c6_faces():
    W, H = 380, 230
    fills = {tuple(CI[c] for c in 'ABCD'): (GREEN, 0.3), tuple(CI[c] for c in 'ABFE'): (GOLD, 0.35),
             tuple(CI[c] for c in 'BCGF'): (GOLD, 0.35)}
    out, Q, vis, edges = cube_svg(30, 50, 205, fills=fills, hcol=MUTED)
    out += tx(110, 225, 'квадрат', GREEN, NS) + tx(Q[CI['F']][0] + 18, (Q[CI['F']][1] + Q[CI['G']][1]) / 2, 'скошены', GOLD, NS, 'start')
    return S(W, H, out), ''


def dr_path(pts, col, sw, d, dur, closed=False):
    """Ломаная, которая прорисовывается (класс dr) к моменту d за dur секунд."""
    dd = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + (' Z' if closed else '')
    return (f"<path class='dr' pathLength='100' style='--d:{d}s;--dur:{dur}s' d='{dd}' fill='none' "
            f"stroke='{col}' stroke-width='{sw}' stroke-linejoin='round'/>")


@at('Остальные 9 рёбер обведи сплошной линией', fx=True)
def c6_build():
    need('квадрат `ABCD` со стороной `4` см', 'одинаковые отрезки длиной `2` см', 'примерно `45°`',
         'Остальные `9` рёбер обведи сплошной линией')
    W, H = 380, 250
    s = 34                                     # 1 см = 34 px; глубина 4 · 0,5 = 2 см
    P = obl_proj(s, 0.5, 90, 215, 4)
    _, Q, vis, edges = solid(CUBE, P)
    q = {n: Q[CI[n]] for n in CN}
    assert abs(dist(q['A'], q['E']) - 2 * s) < 1e-6 and abs(dist(q['A'], q['B']) - 4 * s) < 1e-6
    b = ''
    # шаг 1: квадрат ABCD тонко
    b += dr_path([q['A'], q['B'], q['C'], q['D']], MUTED, 1.3, 0.2, 0.9, True)
    b += g('fi', 0.9, ''.join(pname(q[n], n, *o) for n, o in (('A', (-12, -4)), ('B', (6, 14)), ('C', (12, 8)),
                                                              ('D', (-12, 8)))) +
           tx(*add(mid(q['D'], q['C']), (0, 22)), '4 см', MUTED, NS))
    # шаг 2: четыре отрезка по 2 см под 45°
    for k, (f, t_) in enumerate((('A', 'E'), ('B', 'F'), ('C', 'G'), ('D', 'H'))):
        b += dr_path([q[f], q[t_]], BLUE, 1.6, 1.4 + 0.25 * k, 0.5)
    b += g('fi', 2.5, tx(*add(mid(q['A'], q['E']), (-26, -2)), '2 см', BLUE, NS) +
           angle_arc(q['A'], q['B'], q['E'], 22, GOLD, 1.8) + tx(*add(pol(q['A'], 31, 16), (4, 5)), '45°', GOLD, NS) +
           ''.join(pname(q[n], n, *o) for n, o in (('E', (-10, -10)), ('F', (10, -10)), ('G', (12, 4)), ('H', (12, -10)))))
    # шаг 3: второй квадрат EFGH тонко
    b += dr_path([q['E'], q['F'], q['G'], q['H']], MUTED, 1.3, 2.9, 0.8, True)
    # шаг 4: обвести начисто — 9 рёбер сплошные, 3 ребра у H штрихами
    vis_e = [e for e, v in edges.items() if v]
    hid_e = [e for e, v in edges.items() if not v]
    assert len(vis_e) == 9 and sorted(hid_e) == sorted([E('H', 'E'), E('H', 'G'), E('H', 'D')])
    for e in vis_e:
        b += dr_path([Q[e[0]], Q[e[1]]], INK, 2.6, 3.9, 0.8)
    b += g('fi', 4.9, ''.join(seg(Q[e[0]], Q[e[1]], GOLD, 2.2, DASH) for e in hid_e))
    return S(W, H, b), 'Сначала тонкий каркас, потом начисто: девять рёбер сплошные, три ребра у H — штрихами.'


@at('+---+---+---+---+', zamena=True)
def c6_net():
    W, H = 320, 230
    s = 70
    x0, y0 = 20, 10
    b = ''
    for k in range(4):
        b += rect(x0 + k * s, y0 + s, s, s, BLUE, INK, 2, extra=" fill-opacity='0.2'")
    b += rect(x0 + s, y0, s, s, GOLD, INK, 2, extra=" fill-opacity='0.25'")
    b += rect(x0 + s, y0 + 2 * s, s, s, GOLD, INK, 2, extra=" fill-opacity='0.25'")
    return S(W, H, b), 'Четыре квадрата ряда свернутся в боковые грани, верхний и нижний закроют куб.'


@at('Шесть квадратов в один ряд в куб не свернуть')
def c6_row6():
    W, H = 420, 170
    s = 62
    x0, y0 = 24, 50
    b = brace(x0, x0 + 4 * s, y0 - 4, 'кольцо', True, BLUE, NS)
    for k in range(6):
        col = BLUE if k < 4 else RED
        b += rect(x0 + k * s, y0, s, s, col, INK, 2, extra=" fill-opacity='0.22'")
        b += tx(x0 + k * s + s / 2, y0 + s / 2 + 7, str(k + 1), INK, 19, weight=600)
    b += tx(x0 + 4.5 * s, y0 + s + 26, 'на 1', RED, NS) + tx(x0 + 5.5 * s, y0 + s + 26, 'на 2', RED, NS)
    b += tx(x0 + 2 * s, y0 + s + 26, 'верх и низ открыты', MUTED, 14)
    return S(W, H, b), ''


@at('ребро EF перестанет быть параллельным ребру AB')
def c6_err():
    need('квадрат `ABCD` со стороной `4` см', 'одинаковые отрезки длиной `2` см', 'из `B` — `3` см')
    W, H = 440, 250
    s = 25
    b = ''
    # верно
    P = obl_proj(s, 0.5, 40, 200, 4)
    out, Q, vis, edges = solid(CUBE, P, hcol=MUTED)
    b += out
    for n in 'ABCD':
        b += ticks(Q[CI[n]], Q[CI['EFGH'['ABCD'.index(n)]]], 1, BLUE)
    b += seg(Q[CI['E']], Q[CI['F']], GREEN, 3) + seg(Q[CI['A']], Q[CI['B']], GREEN, 3)
    b += tx(*add(mid(Q[CI['D']], Q[CI['C']]), (0, 20)), '4 см', MUTED, 14)
    b += tx(*add(mid(Q[CI['B']], Q[CI['F']]), (34, 14)), '2 см', BLUE, 14)
    b += angle_arc(Q[CI['D']], Q[CI['C']], Q[CI['H']], 18, GOLD, 1.8) + tx(*add(pol(Q[CI['D']], 30, 14), (4, 5)), '45°', GOLD, 14)
    b += tx(115, 245, 'верно', GREEN, NS, weight=600)
    # ошибка: из A — 2 см, из B — 3 см
    A, B, C, D = (260, 100), (360, 100), (360, 200), (260, 200)
    u = (math.cos(math.radians(45)), -math.sin(math.radians(45)))
    Ee = add(A, (2 * s * u[0], 2 * s * u[1]))
    F = add(B, (3 * s * u[0], 3 * s * u[1]))
    b += poly([A, B, C, D], INK) + seg(A, Ee, BLUE, 2.4) + seg(B, F, BLUE, 2.4)
    b += seg(Ee, F, RED, 3) + seg(A, B, GREEN, 3)
    b += tx(*add(mid(A, Ee), (-22, 0)), '2 см', BLUE, 14) + tx(*add(mid(B, F), (24, 6)), '3 см', BLUE, 14)
    for p, n, dx, dy in ((A, 'A', -12, 6), (B, 'B', 4, 16), (Ee, 'E', -10, -10), (F, 'F', 10, -8)):
        b += pname(p, n, dx, dy)
    b += tx(310, 245, 'EF не параллельно AB', RED, NS, weight=600)
    return S(W, H, b), ''
