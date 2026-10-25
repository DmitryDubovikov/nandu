"""Часть B — геометрия: главы 12–17."""
import math

from desyatichnye_geom_prim import *


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def arc(cx, cy, r, a1, a2, col, sw=2.5, extra=''):
    """Дуга против часовой стрелки от a1 до a2 градусов."""
    x1, y1 = pt(cx, cy, r, a1)
    x2, y2 = pt(cx, cy, r, a2)
    large = 1 if a2 - a1 > 180 else 0
    return (f"<path d='M{x1:.1f} {y1:.1f} A{r} {r} 0 {large} 0 {x2:.1f} {y2:.1f}' fill='none' stroke='{col}' "
            f"stroke-width='{sw}'{extra}/>")


def tip(x, y, deg, col, s=11):
    """Наконечник «бесконечно» на конце линии, смотрит в сторону deg."""
    p1 = pt(x, y, s, deg + 155)
    p2 = pt(x, y, s, deg - 155)
    return f"<path d='M{x} {y} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} z' fill='{col}'/>"


def bracket(x1, x2, y, col, down=True, sw=2):
    k = 7 if down else -7
    return (f"<path d='M{x1} {y} L{x1} {y+k} L{x2} {y+k} L{x2} {y}' stroke='{col}' stroke-width='{sw}' "
            f"fill='none'/>")


def vbracket(x, y1, y2, col, left=True, sw=2):
    k = -7 if left else 7
    return (f"<path d='M{x} {y1} L{x+k} {y1} L{x+k} {y2} L{x} {y2}' stroke='{col}' stroke-width='{sw}' "
            f"fill='none'/>")


# ——— Глава 12 ———

def g12_objects():
    has('бесконечна в обе стороны', 'начало есть, конца нет', 'нет концов')
    b = []
    rows = ['точка', 'прямая', 'луч', 'отрезок']
    for k, name in enumerate(rows):
        b.append(t(20, 36 + k * 50, name, MUTED, 16, anchor='start'))
    y = 31
    b.append(dot(290, y, INK, 5) + t(304, y - 8, 'A', INK, 16, anchor='start', weight=700))
    y = 81   # прямая растёт из середины сразу в обе стороны
    b.append(drpath(f'M290 {y} L140 {y}', INK, 2.5, 0.3, 1.3) + drpath(f'M290 {y} L440 {y}', INK, 2.5, 0.3, 1.3))
    b.append(fi(1.5, tip(130, y, 180, INK) + tip(450, y, 0, INK)))
    y = 131  # луч — из начала в одну сторону
    b.append(dot(150, y, INK, 5))
    b.append(drpath(f'M150 {y} L440 {y}', INK, 2.5, 2.1, 1.5) + fi(3.5, tip(450, y, 0, INK)))
    y = 181  # отрезок — от A до B и стоп
    b.append(dot(170, y, INK, 5) + t(170, y - 12, 'A', INK, 16, weight=700))
    b.append(drpath(f'M170 {y} L410 {y}', INK, 2.5, 4.1, 1.2)
             + fi(5.2, dot(410, y, INK, 5) + t(410, y - 12, 'B', INK, 16, weight=700)))
    return fig(svg(460, 200, ''.join(b)), fx=True)


def g12_parts():
    has('AB = AC + CB')
    xa, xc, xb, y = 40, 190, 420, 60
    b = [line(xa, y, xc, y, GOLD, 5), line(xc, y, xb, y, BLUE, 5)]
    for x, n in [(xa, 'A'), (xc, 'C'), (xb, 'B')]:
        b.append(dot(x, y, INK, 5) + t(x, y - 14, n, INK, 16, weight=700))
    b.append(bracket(xa, xc - 3, y + 14, GOLD) + t((xa + xc) / 2, y + 42, 'AC', GOLD, 15, weight=700))
    b.append(bracket(xc + 3, xb, y + 14, BLUE) + t((xc + xb) / 2, y + 42, 'CB', BLUE, 15, weight=700))
    b.append(bracket(xa, xb, y + 56, INK) + t((xa + xb) / 2, y + 84, 'AB = AC + CB', INK, 15, weight=700))
    return fig(svg(460, 156, ''.join(b)))


def g12_angle():
    has('∠ABC', 'вершина всегда в середине записи')
    bx, by = 90, 160
    ax, ay = pt(bx, by, 260, 38)
    cx, cy = bx + 300, by
    b = [line(bx, by, ax, ay, INK, 2.5) + tip(*pt(bx, by, 270, 38), 38, INK),
         line(bx, by, cx, cy, INK, 2.5) + tip(cx + 10, cy, 0, INK),
         arc(bx, by, 44, 0, 38, GOLD, 2.5)]
    pa = pt(bx, by, 190, 38)
    b.append(dot(*pa, INK, 5) + t(pa[0] - 8, pa[1] - 12, 'A', INK, 17, weight=700))
    b.append(dot(300, by, INK, 5) + t(300, by + 26, 'C', INK, 17, weight=700))
    b.append(dot(bx, by, GOLD, 7) + t(bx - 10, by + 26, 'B', GOLD, 18, weight=700))
    b.append(t(bx + 2, by + 46, 'вершина', GOLD, 13.5))
    sa = pt(bx, by, 120, 38)
    b.append(t(sa[0] - 14, sa[1] - 10, 'сторона', MUTED, 13.5, anchor='end'))
    b.append(t(190, by - 10, 'сторона', MUTED, 13.5))
    b.append(t(420, 44, '∠ABC', INK, 22, anchor='end', weight=700))
    return fig(svg(460, 216, ''.join(b)))


def g12_straight():
    has('180 − 47 = 133°')
    assert 180 - 47 == 133
    ox, oy, L = 230, 170, 190
    b = [line(ox - L, oy, ox + L, oy, INK, 2.5), arc(ox, oy, 78, 0, 180, MUTED, 1.5, " stroke-dasharray='4 4'"),
         t(ox, oy - 86, '180°', MUTED, 14)]
    ex, ey = pt(ox, oy, L, 47)
    b.append(drpath(f'M{ox} {oy} L{ex:.1f} {ey:.1f}', BLUE, 3, 0.4, 1.0))
    b.append(fi(1.6, arc(ox, oy, 46, 0, 47, GOLD, 3) + t(*pt(ox + 4, oy + 5, 62, 22), '47°', GOLD, 15, weight=700)))
    b.append(fi(2.4, arc(ox, oy, 34, 47, 180, GREEN, 3)
                + t(*pt(ox, oy + 5, 54, 125), '133°', GREEN, 15, weight=700)))
    b.append(dot(ox, oy, INK, 5))
    b.append(fi(3.1, t(ox, oy + 36, '180 − 47 = 133°', GREEN, 17, weight=700)))
    return fig(svg(460, 218, ''.join(b)), fx=True)


def g12_kinds():
    has('Угол в 47° — острый', 'в 112° — тупой', 'прямой', 'развёрнутый')
    stops = [(47, 'острый'), (90, 'прямой'), (112, 'тупой'), (180, 'развёрнутый')]
    vx, vy, L = 250, 176, 150
    b = [line(vx, vy, vx + L, vy, INK, 3)]
    # один луч поворачивается: вложенные повороты вокруг вершины, по одному на каждую остановку
    ray = line(0, 0, L, 0, BLUE, 3.5) + tip(L + 8, 0, 0, BLUE)
    prev, d0, body = 0, 0.4, ray
    rots = []
    for k, (a, _) in enumerate(stops):
        rots.append((d0 + 1.7 * k, a - prev))
        prev = a
    for d, da in reversed(rots):
        body = g('sl', d, body, f';--to:rotate({-da}deg)')
    b.append(f"<g transform='translate({vx},{vy})'>{body}</g>")
    b.append(dot(vx, vy, GOLD, 6))
    # подпись остановки: проявляется, когда луч встал, и гаснет, когда он поехал дальше
    for k, (a, name) in enumerate(stops):
        d_in = rots[k][0] + 1.3
        lab = t(440, 60, f'{a}° — {name}', GOLD, 18, anchor='end', weight=700)
        if a == 90:
            lab += (f"<path d='M{vx} {vy-16} L{vx+16} {vy-16} L{vx+16} {vy}' fill='none' stroke='{GOLD}' "
                    f"stroke-width='2.2'/>")
        b.append(fi(d_in, fo(rots[k + 1][0], lab)) if k + 1 < len(stops) else fi(d_in, lab))
    # след-миниатюра каждой остановки — ряд под большим углом
    W, my = 116, 262
    for k, (a, name) in enumerate(stops):
        x = 6 + k * W
        mx = x + (W / 2 if a == 180 else (54 if a > 90 else 22))
        r = 44 if a == 180 else 60
        mini = line(mx, my, mx + r, my, INK, 2) + line(mx, my, *pt(mx, my, r, a), INK, 2)
        if a == 90:
            mini += (f"<path d='M{mx} {my-11} L{mx+11} {my-11} L{mx+11} {my}' fill='none' stroke='{GOLD}' "
                     f"stroke-width='2'/>")
        else:
            mini += arc(mx, my, 16, 0, a, GOLD, 2)
        mini += dot(mx, my, INK, 3)
        mini += t(x + W / 2, my + 26, name, INK, 16) + t(x + W / 2, my + 46, f'{a}°', GOLD, 16, weight=700)
        b.append(fi(rots[k][0] + 1.3, mini))
    return fig(svg(470, 318, ''.join(b), maxw=470), fx=True)


def g12_protractor():
    has('47° вместо 133°', 'Острый — значит меньше 90°')
    assert 180 - 47 == 133
    cx, cy, R = 230, 196, 150
    b = [f"<path d='M{cx-R} {cy} A{R} {R} 0 0 1 {cx+R} {cy} Z' fill='{GREY}' fill-opacity='0.12' stroke='{MUTED}' "
         f"stroke-width='1.8'/>"]
    for a in range(0, 181, 10):
        big = a % 30 == 0
        b.append(line(*pt(cx, cy, R, a), *pt(cx, cy, R - (14 if big else 8), a), MUTED, 1.4 if big else 1))
    for a in range(0, 181, 30):
        lift = 10 if a in (0, 180) else 0
        x, y = pt(cx, cy, R - 30, a)
        b.append(t(x, y + 4 - lift, str(a), GREEN, 11.5))          # внутренняя шкала: 0 справа
        x, y = pt(cx, cy, R + 13, 180 - a)
        b.append(t(x, y + 4 - lift, str(a), MUTED, 11.5))          # внешняя шкала: 0 слева
    b.append(f"<circle cx='{cx+R-30}' cy='{cy-10}' r='11' fill='none' stroke='{GREEN}' stroke-width='2'/>")
    b.append(line(cx, cy, cx + R + 20, cy, INK, 3) + line(cx, cy, *pt(cx, cy, R + 20, 47), INK, 3))
    b.append(arc(cx, cy, 36, 0, 47, GOLD, 2.5) + dot(cx, cy, GOLD, 5))
    x, y = pt(cx, cy, R - 52, 47)
    b.append(t(x - 6, y + 6, '47°', GREEN, 16, anchor='end', weight=700))
    x, y = pt(cx, cy, R + 34, 47)
    b.append(t(x + 6, y, '133°', RED, 16, anchor='start', weight=700) + line(x + 2, y + 4, x + 46, y - 14, RED, 2))
    return fig(svg(460, 214, ''.join(b)))


# ——— Глава 13 ———

def g13_walk():
    has('P = 3,5 + 4,2 + 6 = 13,7')
    a, b_, c = D('6'), D('3.5'), D('4.2')
    assert b_ + c + a == D('13.7')
    u, x0, y0 = 60, 50, 190
    xa = float((a * a + c * c - b_ * b_) / (2 * a))
    ya = math.sqrt(float(c * c) - xa * xa)
    P0, P1, P2 = (x0, y0), (x0 + float(a) * u, y0), (x0 + xa * u, y0 - ya * u)
    assert abs(math.dist(P1, P2) / u - 3.5) < 1e-9 and abs(math.dist(P2, P0) / u - 4.2) < 1e-9
    b = [poly([P0, P1, P2], GREY, MUTED, 1.5, op=0.12)]
    seq = [(P1, P2, '3,5', 0.4), (P2, P0, '4,2', 1.4), (P0, P1, '6', 2.4)]
    for (p, q, s, d) in seq:
        b.append(drpath(f'M{p[0]:.1f} {p[1]:.1f} L{q[0]:.1f} {q[1]:.1f}', BLUE, 4, d, 0.9))
    b.append(t((P1[0] + P2[0]) / 2 + 14, (P1[1] + P2[1]) / 2 - 2, '3,5 см', INK, 15, anchor='start', weight=600))
    b.append(t((P2[0] + P0[0]) / 2 - 14, (P2[1] + P0[1]) / 2 - 2, '4,2 см', INK, 15, anchor='end', weight=600))
    b.append(t((P0[0] + P1[0]) / 2, y0 + 24, '6 см', INK, 15, weight=600))
    b.append(dot(*P1, GOLD, 6))
    sx, sy = 296, 40
    b.append(fi(0.4, t(sx, sy, 'P = 3,5', INK, 17, anchor='start', weight=700)))
    b.append(fi(1.4, t(sx + 66, sy, '+ 4,2', INK, 17, anchor='start', weight=700)))
    b.append(fi(2.4, t(sx + 116, sy, '+ 6', INK, 17, anchor='start', weight=700)))
    b.append(fi(3.4, t(sx + 22, sy + 30, '= 13,7 см', GREEN, 18, anchor='start', weight=700)))
    return fig(svg(460, 224, ''.join(b)), fx=True)


def g13_rect():
    has('4,5 + 2,5 = 7', 'P = 14')
    a, c = D('4.5'), D('2.5')
    assert a + c == 7 and 2 * (a + c) == 14
    u, x0, y0 = 56, 70, 40
    W, H = float(a) * u, float(c) * u
    BL, TL, TR, BR = (x0, y0 + H), (x0, y0), (x0 + W, y0), (x0 + W, y0 + H)
    b = [rect(x0, y0, W, H, GREY, MUTED, 1.5, extra=" fill-opacity='0.12'")]
    b.append(drpath(f'M{BL[0]} {BL[1]} L{TL[0]} {TL[1]} L{TR[0]} {TR[1]}', GOLD, 5, 0.3, 1.4))
    b.append(t(x0 + W / 2, y0 - 12, '4,5 м', GOLD, 15, weight=700) + t(x0 - 12, y0 + H / 2 + 5, '2,5 м', GOLD, 15,
                                                                         anchor='end', weight=700))
    b.append(fi(1.8, t(x0 + W / 2, y0 + H / 2 + 6, '4,5 + 2,5 = 7', GOLD, 17, weight=700)))
    b.append(drpath(f'M{TR[0]} {TR[1]} L{BR[0]} {BR[1]} L{BL[0]} {BL[1]}', BLUE, 5, 2.4, 1.4))
    b.append(fi(3.0, t(x0 + W / 2, y0 + H + 24, '4,5 м', BLUE, 15, weight=700)
                + t(x0 + W + 12, y0 + H / 2 + 5, '2,5 м', BLUE, 15, anchor='start', weight=700)))
    b.append(fi(3.8, t(x0 + W / 2, y0 + H + 58, 'P = 2 × 7 = 14 м', GREEN, 18, weight=700)))
    return fig(svg(460, 262, ''.join(b)), fx=True)


# ——— Глава 14 ———

def g14_halves():
    has('S = 4,5 × 2 = 9')
    assert D('4.5') * 2 == 9
    u, x0, y0 = 60, 50, 40
    b = []
    n = 0
    for r in range(2):
        for c in range(4):
            n += 1
            b.append(box(x0 + c * u, y0 + r * u, u, u, GOLD, op=0.3, sw=1.5)
                     + t(x0 + c * u + u / 2, y0 + r * u + u / 2 + 6, str(n), INK, 16, weight=600))
    b.append(rect(x0, y0, 4.5 * u, 2 * u, 'none', INK, 2.5))
    half = lambda y: box(x0 + 4 * u, y, u / 2, u, BLUE, op=0.45, sw=1.5)
    b.append(half(y0))
    b.append(f"<g opacity='0.5' stroke-dasharray='5 4'>{half(y0 + u)}</g>")
    b.append(slide(0.8, u / 2, -u, half(y0 + u)))
    b.append(fi(2.2, rect(x0 + 4 * u, y0, u, u, 'none', GREEN, 2.5) + t(x0 + 4.5 * u, y0 + u / 2 + 6, '9', INK, 16, weight=700)))
    b.append(t(x0 + 2.25 * u, y0 - 12, '4,5 м', INK, 15, weight=600) + t(x0 - 10, y0 + u + 5, '2 м', INK, 15,
                                                                           anchor='end', weight=600))
    b.append(fi(2.6, t(x0 + 2.25 * u, y0 + 2 * u + 36, 'S = 4,5 × 2 = 9 м²', GREEN, 18, weight=700)))
    return fig(svg(400, 210, ''.join(b)), fx=True)


def g14_units():
    has('дм² и см² в 10 × 10 = 100 раз', 'м² и см² в 100 × 100 = 10 000 раз')
    assert 10 * 10 == 100 and 100 * 100 == 10000 and 10 * 10 == 100
    c, x0, y0 = 20, 50, 34
    b = [rect(x0, y0, 10 * c, 10 * c, 'none', INK, 2.5)]
    b.append(fi(0.4, box(x0, y0, 10 * c, c, BLUE, op=0.4, sw=0)
                + ''.join(rect(x0 + k * c, y0, c, c, 'none', BLUE, 1) for k in range(10))))
    for r in range(1, 10):
        b.append(fi(1.0 + 0.2 * r, box(x0, y0 + r * c, 10 * c, c, GOLD, op=0.22, sw=0)
                    + ''.join(rect(x0 + k * c, y0 + r * c, c, c, 'none', MUTED, 0.8) for k in range(10))))
    b.append(t(x0 + 5 * c, y0 - 10, '10 см', BLUE, 14, weight=700))
    b.append(t(x0 - 10, y0 + 5 * c + 5, '10 см', GOLD, 14, anchor='end', weight=700))
    b.append(t(x0 + 10 * c + 14, y0 + c / 2 + 5, '1 см²', BLUE, 13, anchor='start'))
    b.append(fi(3.0, t(x0 + 10 * c + 14, y0 + 5 * c + 2, '1 дм²', INK, 18, anchor='start', weight=700)
                + t(x0 + 10 * c + 14, y0 + 5 * c + 28, '= 100 см²', GREEN, 18, anchor='start', weight=700)))
    return fig(svg(460, y0 + 10 * c + 20, ''.join(b)), fx=True)


U = 34
LX, LY = 50, 40


def lshape(dx=0, dy=0):
    """Г-фигура: прямоугольник 7 × 5, у которого отрезан угол 4 × 3 справа сверху."""
    p = [(0, 0), (3, 0), (3, 3), (7, 3), (7, 5), (0, 5)]
    return [(LX + dx + x * U, LY + dy + y * U) for x, y in p]


def lpts(ox, oy, u):
    """Г-фигура с левым верхним углом (ox, oy) и единицей u."""
    p = [(0, 0), (3, 0), (3, 3), (7, 3), (7, 5), (0, 5)]
    return [(ox + x * u, oy + y * u) for x, y in p]


SU, SY, SL, SR = 26, 30, 20, 262   # единица, верх, левая (неподвижная) и правая (движущаяся) фигуры


def g14_cut():
    has('Путь первый — разрезать', 'складываем')
    u = SU
    b = [poly(lpts(SL, SY, u), '#3a4657', INK, 2.5)]
    b.append(t(SL + 7 * u + 26, SY + 4 * u + 9, '=', INK, 26))
    b.append(box(SR, SY, 3 * u, 5 * u, GOLD, op=0.35, sw=2))
    b.append(slide(1.6, 36, 0, box(SR + 3 * u, SY + 3 * u, 4 * u, 2 * u, CYAN, op=0.35, sw=2)))
    b.append(fo(1.2, poly(lpts(SR, SY, u), '#3a4657', INK, 2.5)))
    b.append(drpath(f'M{SR+3*u} {SY+3*u} L{SR+3*u} {SY+5*u}', BLUE, 3, 0.4, 0.8, " stroke-dasharray='6 5'"))
    b.append(fi(2.8, t(SR + 3 * u + 18, SY + 4 * u + 9, '+', INK, 26, weight=700)))
    return fig(svg(SR + 7 * u + 50, SY + 5 * u + 24, ''.join(b), maxw=SR + 7 * u + 50), fx=True)


def g14_complete():
    has('Путь второй — достроить', 'вычитаем')
    u = SU
    b = [poly(lpts(SL, SY, u), '#3a4657', INK, 2.5)]
    b.append(t(SL + 7 * u + 26, SY + 4 * u + 9, '=', INK, 26))
    b.append(poly(lpts(SR, SY, u), GOLD, INK, 2.5, op=0.3))
    corner = box(SR + 3 * u, SY, 4 * u, 3 * u, GOLD, op=0.3, sw=2, dashed=True)
    b.append(slide(0.4, -40, 24, f"<g transform='translate(40,-24)'>{corner}</g>"))
    b.append(fi(1.9, rect(SR, SY, 7 * u, 5 * u, 'none', INK, 2.5)))
    b.append(fi(2.7, box(SR + 3 * u, SY, 4 * u, 3 * u, RED, op=0.35, sw=2.5, dashed=True)
                + t(SR + 5 * u, SY + 1.5 * u + 11, '−', RED, 34, weight=700)))
    return fig(svg(SR + 7 * u + 50, SY + 5 * u + 24, ''.join(b), maxw=SR + 7 * u + 50), fx=True)


def g14_diff():
    has('7 − 3 = 4')
    assert 7 - 3 == 4
    b = [poly(lshape(), GREY, INK, 2.5, op=0.15)]
    b.append(line(LX + 3 * U, LY + 3 * U, LX + 3 * U, LY + 5 * U, BLUE, 2, " stroke-dasharray='6 5'"))
    b.append(t(LX + 1.5 * U, LY - 10, '3 см', GOLD, 15, weight=700))
    yb = LY + 5 * U
    b.append(slide(0.6, 0, yb + 26 - (LY - 10), t(LX + 1.5 * U, LY - 10, '3 см', GOLD, 15, weight=700)))
    b.append(bracket(LX, LX + 7 * U, yb + 36, INK) + t(LX + 3.5 * U, yb + 64, '7 см', INK, 15, weight=700))
    b.append(fi(2.0, t(LX + 5 * U, yb + 26, '7 − 3 = 4 см', GREEN, 15, weight=700)))
    return fig(svg(380, 310, ''.join(b)), fx=True)


# ——— Глава 15 ———

def g15_elements():
    has('центр', 'радиус', 'диаметр', 'дуга', 'полукруг')
    R = 80
    b = []
    cx, cy = 115, 112
    b.append(f"<circle cx='{cx}' cy='{cy}' r='{R}' fill='none' stroke='{INK}' stroke-width='2'/>")
    b.append(line(cx - R, cy, cx + R, cy, BLUE, 3.5) + t(cx - R / 2, cy + 22, 'd', BLUE, 17, weight=700))
    px, py = pt(cx, cy, R, 60)
    b.append(line(cx, cy, px, py, GOLD, 3.5) + t((cx + px) / 2 - 12, (cy + py) / 2, 'r', GOLD, 17, weight=700))
    b.append(dot(cx, cy, INK, 5) + t(cx + 10, cy + 22, 'O', INK, 17, weight=700))
    cx2 = 345
    b.append(f"<path d='M{cx2-R} {cy} A{R} {R} 0 0 0 {cx2+R} {cy} Z' fill='{VIOLET}' fill-opacity='0.35' "
             f"stroke='none'/>")
    b.append(f"<circle cx='{cx2}' cy='{cy}' r='{R}' fill='none' stroke='{INK}' stroke-width='2'/>")
    b.append(line(cx2 - R, cy, cx2 + R, cy, MUTED, 1.5))
    b.append(arc(cx2, cy, R, 30, 110, GREEN, 6))
    ax, ay = pt(cx2, cy, R + 18, 70)
    b.append(t(ax, ay, 'дуга', GREEN, 15, weight=700))
    b.append(t(cx2, cy + 44, 'полукруг', VIOLET, 15, weight=700))
    return fig(svg(460, 210, ''.join(b)))


def g15_diameter():
    has('Радиус 3,5 см → диаметр 7 см')
    assert 2 * D('3.5') == 7
    cx, cy, R = 230, 120, 100
    b = [f"<circle cx='{cx}' cy='{cy}' r='{R}' fill='none' stroke='{INK}' stroke-width='2'/>"]
    rad = line(cx, cy, cx + R, cy, GOLD, 4) + t(cx + R / 2, cy - 10, '3,5', GOLD, 15, weight=700)
    b.append(rad)
    b.append(slide(0.6, -R, 0, rad))
    b.append(dot(cx, cy, INK, 5) + t(cx, cy - 12, 'O', INK, 15, weight=700))
    b.append(fi(2.1, bracket(cx - R, cx + R, cy + 12, BLUE) + t(cx, cy + 42, 'd = 2 × 3,5 = 7 см', BLUE, 17,
                                                                  weight=700)))
    return fig(svg(460, 236, ''.join(b)), fx=True)


def g15_halves():
    has('круг распадается на две равные части', 'куски получатся разные')
    R = 78
    b = []
    cx, cy = 115, 100
    b.append(f"<path d='M{cx-R} {cy} A{R} {R} 0 0 1 {cx+R} {cy} Z' fill='{GOLD}' fill-opacity='0.4'/>")
    b.append(f"<path d='M{cx-R} {cy} A{R} {R} 0 0 0 {cx+R} {cy} Z' fill='{BLUE}' fill-opacity='0.4'/>")
    b.append(line(cx - R, cy, cx + R, cy, INK, 3) + dot(cx, cy, INK, 4.5))
    b.append(t(cx, cy + R + 28, 'через центр: равные', GREEN, 14, weight=700))
    cx2 = 345
    a1, a2 = 200, 340
    p1, p2 = pt(cx2, cy, R, a1), pt(cx2, cy, R, a2)
    b.append(f"<path d='M{p1[0]:.1f} {p1[1]:.1f} A{R} {R} 0 1 1 {p2[0]:.1f} {p2[1]:.1f} Z' fill='{GOLD}' "
             f"fill-opacity='0.4'/>")
    b.append(f"<path d='M{p1[0]:.1f} {p1[1]:.1f} A{R} {R} 0 0 0 {p2[0]:.1f} {p2[1]:.1f} Z' fill='{BLUE}' "
             f"fill-opacity='0.4'/>")
    b.append(line(*p1, *p2, INK, 3) + dot(cx2, cy, INK, 4.5))
    b.append(t(cx2, cy + R + 28, 'мимо центра: разные', RED, 14, weight=700))
    return fig(svg(460, 212, ''.join(b)))


# ——— Глава 16 ———

def g16_box():
    has('6 граней', '12 рёбер', '8 вершин', 'длина a, ширина b, высота c')
    F0 = {'BL': (60, 200), 'BR': (280, 200), 'TL': (60, 90), 'TR': (280, 90)}
    dv = (80, -56)
    Bk = {k: (x + dv[0], y + dv[1]) for k, (x, y) in F0.items()}
    b = [poly([F0['BL'], F0['BR'], F0['TR'], F0['TL']], GREY, 'none', 0, op=0.15)]
    hidden = " stroke-dasharray='6 5'"
    groups = {
        BLUE: [(F0['BL'], F0['BR'], 0), (F0['TL'], F0['TR'], 0), (Bk['TL'], Bk['TR'], 0), (Bk['BL'], Bk['BR'], 1)],
        GOLD: [(F0['BR'], Bk['BR'], 0), (F0['TL'], Bk['TL'], 0), (F0['TR'], Bk['TR'], 0), (F0['BL'], Bk['BL'], 1)],
        GREEN: [(F0['BL'], F0['TL'], 0), (F0['BR'], F0['TR'], 0), (Bk['BR'], Bk['TR'], 0), (Bk['BL'], Bk['TL'], 1)],
    }
    assert sum(len(v) for v in groups.values()) == 12 and all(len(v) == 4 for v in groups.values())
    # каркас виден с самого начала — загораются четвёрки поверх него
    for es in groups.values():
        for p, q, hid in es:
            b.append(line(*p, *q, GREY, 1.5, hidden if hid else ''))
    names = {BLUE: ('a', (170, 226)), GOLD: ('b', (332, 186)), GREEN: ('c', (44, 150))}
    lx = 390
    for k, (col, es) in enumerate(groups.items()):
        d = 0.4 + 1.2 * k
        body = ''.join(line(*p, *q, col, 2 if hid else 3.5, hidden if hid else '') for p, q, hid in es)
        n, (nx, ny) = names[col]
        body += t(nx, ny, n, col, 18, weight=700)
        y = 70 + k * 30
        body += line(lx, y - 5, lx + 22, y - 5, col, 3.5) + t(lx + 30, y, f'4 ребра {n}', col, 16, anchor='start',
                                                             weight=600)
        b.append(fi(d, body))
    pts = list(F0.values()) + list(Bk.values())
    assert len(set(pts)) == 8
    b.append(fi(4.0, ''.join(dot(*p, INK, 5) for p in pts)
                + t(lx, 70 + 3 * 30, '8 вершин', INK, 16, anchor='start', weight=600)))
    return fig(svg(510, 240, ''.join(b), maxw=510), fx=True)


def mix(col, k, bg='#131923'):
    """Непрозрачный оттенок: доля k цвета col на фоне рисунка (кубики не просвечивают друг сквозь друга)."""
    a = [int(col[i:i + 2], 16) for i in (1, 3, 5)]
    z = [int(bg[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(z[i] + (a[i] - z[i]) * k):02x}' for i in range(3))


def g16_layers():
    has('V = 5 × 4 × 2,5 = 50')
    assert 5 * 4 * D('2.5') == 50
    s, ddx, ddy = 38, 17, -13
    ox, oy = 60, 176
    layers = [(0, 1, GOLD, 0.3, '20'), (1, 1, CYAN, 1.5, '20'), (2, F(1, 2), VIOLET, 2.7, '10')]
    assert 5 * 4 + 5 * 4 + 5 * 4 * F(1, 2) == 50
    b = []
    for z, hh, col, d, lab in layers:
        h = float(hh) * s
        body = []
        for j in range(3, -1, -1):
            for i in range(5):
                x = ox + i * s + j * ddx
                y = oy - z * s + j * ddy
                front = [(x, y), (x + s, y), (x + s, y - h), (x, y - h)]
                top = [(x, y - h), (x + s, y - h), (x + s + ddx, y - h + ddy), (x + ddx, y - h + ddy)]
                side = [(x + s, y), (x + s + ddx, y + ddy), (x + s + ddx, y - h + ddy), (x + s, y - h)]
                for pp, k in [(side, 0.45), (top, 0.85), (front, 0.65)]:
                    body.append(poly(pp, mix(col, k), DARK, 1.2))
        ly = oy - z * s - h / 2 + 4 * ddy / 2 + 5
        body.append(t(ox + 5 * s + 4 * ddx + 16, ly, lab, col, 17, anchor='start', weight=700))
        b.append(fi(d, ''.join(body)))
    b.append(t(ox + 2.5 * s, oy + 24, '5 см', INK, 14, weight=600))
    b.append(t(ox + 5 * s + 2 * ddx + 14, oy + 2 * ddy + 14, '4 см', INK, 14, anchor='start', weight=600))
    b.append(t(ox - 10, oy - 1.25 * s, '2,5 см', INK, 14, anchor='end', weight=600))
    b.append(fi(3.6, t(240, oy + 56, 'V = 5 × 4 × 2,5 = 50 см³', GREEN, 18, weight=700)))
    return fig(svg(460, oy + 70, ''.join(b)), fx=True)


def g16_net():
    has('2 × (a × b + b × c + a × c)')
    A_, B_, C_ = 120, 64, 48
    x0, y0 = 26, 24
    cols = {'ab': VIOLET, 'bc': CYAN, 'ac': PINK}
    lab = {'ab': 'a × b', 'bc': 'b × c', 'ac': 'a × c'}
    faces = [(x0 + B_, y0, A_, B_, 'ab'), (x0, y0 + B_, B_, C_, 'bc'), (x0 + B_, y0 + B_, A_, C_, 'ac'),
             (x0 + B_ + A_, y0 + B_, B_, C_, 'bc'), (x0 + 2 * B_ + A_, y0 + B_, A_, C_, 'ac'),
             (x0 + B_, y0 + B_ + C_, A_, B_, 'ab')]
    b = []
    for x, y, w, h, k in faces:
        b.append(box(x, y, w, h, cols[k], op=0.35, sw=1.8) + t(x + w / 2, y + h / 2 + 5, lab[k], cols[k], 13.5,
                                                                weight=700))
    b.append(t(x0 + B_ + A_ / 2, y0 + B_ + C_ + B_ + 22, 'a', INK, 15, weight=700))
    b.append(t(x0 + B_ - 8, y0 + B_ / 2 + 5, 'b', INK, 15, anchor='end', weight=700))
    b.append(t(x0 - 8, y0 + B_ + C_ / 2 + 5, 'c', INK, 15, anchor='end', weight=700))
    return fig(svg(x0 + 2 * A_ + 2 * B_ + 20, y0 + 2 * B_ + C_ + 34, ''.join(b), maxw=x0 + 2 * A_ + 2 * B_ + 20))


# ——— Глава 17 ———

def g17_quarter():
    has('24 × ¼ = 6', '6 см × 4 см')
    assert 6 * 4 * F(1, 4) == 6
    u, x0, y0 = 34, 60, 34
    b = [box(x0, y0, 6 * u, u, GOLD, op=0.45, sw=0)]
    for r in range(4):
        for c in range(6):
            b.append(rect(x0 + c * u, y0 + r * u, u, u, 'none', MUTED, 1))
    b.append(rect(x0, y0, 6 * u, 4 * u, 'none', INK, 2.5))
    b.append(t(x0 + 3 * u, y0 - 10, '6 см', INK, 14, weight=600) + t(x0 - 10, y0 + 2 * u + 5, '4 см', INK, 14,
                                                                       anchor='end', weight=600))
    b.append(t(x0 + 6 * u + 20, y0 + u / 2 + 6, '¼', GOLD, 20, anchor='start', weight=700))
    b.append(t(x0 + 3 * u, y0 + 4 * u + 34, '24 × ¼ = 6 см²', GREEN, 17, weight=700))
    return fig(svg(400, 222, ''.join(b)))


def g17_back():
    has('12 : 3/8 = 32')
    assert 12 / F(3, 8) == 32 and 12 // 3 == 4 and 8 * 4 == 32
    w, x0, y0, h = 46, 34, 52, 70
    b = [box(x0, y0, 3 * w, h, GOLD, op=0.4, sw=0)]
    for k in range(8):
        b.append(rect(x0 + k * w, y0, w, h, 'none', MUTED, 1.2))
    b.append(rect(x0, y0, 8 * w, h, 'none', INK, 2.5))
    b.append(bracket(x0, x0 + 3 * w, y0 - 8, GOLD, down=False) + t(x0 + 1.5 * w, y0 - 22, '12 см²', GOLD, 17,
                                                                     weight=700))
    b.append(fi(1.0, ''.join(t(x0 + k * w + w / 2, y0 + h / 2 + 7, '4', GOLD, 18, weight=700) for k in range(3))))
    b.append(fi(2.0, ''.join(t(x0 + k * w + w / 2, y0 + h / 2 + 7, '4', INK, 18, weight=700) for k in range(3, 8))))
    b.append(bracket(x0, x0 + 3 * w, y0 + h + 8, GOLD) + t(x0 + 1.5 * w, y0 + h + 34, '3/8', GOLD, 16, weight=700))
    b.append(t(x0 + 6 * w - 4, y0 + h + 34, '12 : 3/8 =', INK, 17, anchor='end', weight=700))
    b.append(fi(2.8, t(x0 + 6 * w + 4, y0 + h + 34, '32 см²', GREEN, 17, anchor='start', weight=700)))
    return fig(svg(440, 172, ''.join(b)), fx=True)


def g17_scale():
    has('Увеличили обе стороны в 2 раза', 'площадь — в 2 × 2 = 4 раза', 'периметр — в 2 раза')
    w, h = 70, 44
    sx, sy = 30, 40
    bx, by = 200, 40
    b = [box(sx, sy, w, h, GOLD, op=0.45, sw=2)]
    b.append(rect(bx, by, 2 * w, 2 * h, 'none', INK, 2.5))
    for k, (qx, qy) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
        b.append(slide(0.4 + 0.5 * k, bx + qx * w - sx, by + qy * h - sy,
                       box(sx, sy, w, h, GOLD, op=0.45, sw=1.5)))
    for k in (1, 3):
        b.append(line(bx + w, by - 5 + (2 * h + 10) * (k == 3), bx + w, by + 5 + (2 * h - 10) * (k == 3), INK, 2))
    b.append(fi(2.6, t(bx + w, by + 2 * h + 30, 'периметр — в 2 раза', INK, 15, weight=600)
                + t(bx + w, by + 2 * h + 56, 'площадь — в 2 × 2 = 4 раза', GREEN, 15, weight=700)))
    return fig(svg(440, 196, ''.join(b)), fx=True)


def g17_what():
    has('часть чего — границы или внутренности')
    b = [rect(40, 30, 160, 96, 'none', GREY, 1.5, " stroke-dasharray='5 4'"),
         rect(260, 30, 160, 96, 'none', GREY, 1.5, " stroke-dasharray='5 4'")]
    b.append(drpath('M40 30 L200 30 L200 126 L40 126 Z', GOLD, 5, 0.3, 2.2))
    b.append(fi(2.5, t(120, 158, 'граница → периметр', GOLD, 16, weight=700)))
    b.append(fi(3.2, box(260, 30, 160, 96, GREEN, op=0.4, sw=1.2)))
    b.append(fi(3.8, t(340, 158, 'внутренность → площадь', GREEN, 16, weight=700)))
    return fig(svg(460, 172, ''.join(b)), fx=True)


FIGS = {
    'бесконечна в обе стороны': g12_objects,
    'AB = AC + CB': g12_parts,
    'вершина всегда в середине записи': g12_angle,
    'на второй кусок остаётся': g12_straight,
    'угол между стрелками часов в 3:00': g12_kinds,
    'прочитать по не той шкале транспортира': g12_protractor,
    'P = 3,5 + 4,2 + 6 = 13,7': g13_walk,
    'складываю соседние стороны': g13_rect,
    'S = 4,5 × 2 = 9': g14_halves,
    '1 га = 100 м × 100 м = 10 000 м²': g14_units,
    'Путь первый — разрезать': g14_cut,
    'Путь второй — достроить': g14_complete,
    'его и пишем на чертеже': g14_diff,
    'отрезок от центра до окружности': g15_elements,
    'Радиус 3,5 см → диаметр 7 см': g15_diameter,
    'Любой другой отрезок так круг не разрежет': g15_halves,
    '8 вершин': g16_box,
    'V = 5 × 4 × 2,5 = 50': g16_layers,
    'Площадь поверхности (если спросят)': g16_net,
    'закрашено 24 × ¼ = 6': g17_quarter,
    'Обратно: закрашено 12': g17_back,
    'Увеличили обе стороны в 2 раза': g17_scale,
    'часть чего — границы или внутренности': g17_what,
}
