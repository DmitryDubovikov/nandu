#!/usr/bin/env python3
"""Рисунки учебника «Дроби вместе, движение по реке, среднее арифметическое» (6 класс, пара 5)
→ math6_5_drobi_dvizhenie_srednee_uchebnik.vis.json (пишется целиком).

План и мысль каждого движения: 26-27/school6/vis/plan_drobi_dvizhenie_srednee.md.
Числа на рисунках считаются здесь (Fraction) и сверяются assert'ами с текстом MD.

Запуск: python3 26-27/school6/vis/drobi_dvizhenie_srednee.py
"""
import json, os, re
from fractions import Fraction as F

from common import (svg, fig, row, t, g, rect, line, path, dot, NumLine, brace, arrow_defs_p,
                    GOLD, BLUE, GREEN, RED, VIOLET, CYAN, GREY, INK, MUTED, DARK)

HERE = os.path.dirname(os.path.abspath(__file__))
MDP = os.path.join(HERE, '..', 'math6_5_drobi_dvizhenie_srednee_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math6_5_drobi_dvizhenie_srednee_uchebnik.vis.json')
MD = open(MDP).read()


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', s)).strip()


NMD = norm(MD)


def need(*ss):
    """Цитируемая строка действительно стоит в тексте MD."""
    for s in ss:
        assert s in MD or s in NMD, f'нет в MD: {s!r}'


def fm(v):
    """Число так, как оно набрано в MD: десятичная запятая, без лишних нулей."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = f'{float(v):.4f}'.rstrip('0').rstrip('.')
    assert F(s) == v, v
    return s.replace('.', ',')


class NL(NumLine):
    """NumLine с точными значениями (Fraction): координата на экране — float."""

    def x(self, v):
        return float(super().x(v))


def sl(d, dx, dy, body):
    return g('sl', d, body, f';--to:translate({dx:.1f}px,{dy:.1f}px)')


def head(x, y, direction, col):
    """Наконечник стрелки в точке (x, y), direction = +1 вправо, −1 влево."""
    k = 9 * direction
    return path([(x - k, y - 6), (x, y), (x - k, y + 6)], col, 2.2, closed=False)


def chevrons(x1, x2, y, direction, col=CYAN, step=34):
    """Полоса течения: шевроны по направлению воды."""
    out, x = '', x1
    while x <= x2:
        k = 5 * direction
        out += path([(x - k, y - 5), (x + k, y), (x - k, y + 5)], col, 1.6, closed=False,
                    extra=" stroke-opacity='0.7'")
        x += step
    return out


def cell_col(x, base, n, c, col=VIOLET, w=None):
    """Столбик из n клеток (одно число ряда) от основания base вверх."""
    w = w or c
    return ''.join(rect(x, base - (j + 1) * c, w, c, col, MUTED, 1,
                        extra=" fill-opacity='0.35'") for j in range(n))


# ——— Ритуалы ———

def r2_chips():
    need('внутри одни двойки и пятёрки', '8 × 125 = 1000', '6 = 2 × 3', 'не получается')
    top = [2, 2, 2, 5, 5, 5]
    p = 1
    for k in top:
        p *= k
    assert p == 1000 and 8 * 125 == 1000 and 5 * 5 * 5 == 125

    C, S, X0 = 30, 50, 92
    Y1, Y2, Y3 = 22, 72, 156             # строка 1000, строка пар, строка знаменателя

    def chip(i, y, k, col=MUTED, fill=None):
        x = X0 + i * S
        return (rect(x, y, C, C, fill or 'none', col, 1.8, rx=6,
                     extra=" fill-opacity='0.25'" if fill else '')
                + t(x + C / 2, y + C / 2 + 6, k, INK, 17, weight=600))

    def times(n, y):
        return ''.join(t(X0 + i * S + C + (S - C) / 2, y + C / 2 + 5, '×', MUTED, 16) for i in range(n - 1))

    def panel(den, fac, ok):
        assert eval(' * '.join(map(str, fac))) == den
        out = t(X0 - 12, Y1 + C / 2 + 6, '1000 =', INK, 17, anchor='end', weight=600)
        out += ''.join(chip(i, Y1, k) for i, k in enumerate(top)) + times(6, Y1)
        out += t(X0 - 12, Y3 + C / 2 + 6, f'{den} =', INK, 17, anchor='end', weight=600)
        out += ''.join(chip(i, Y3, k, GREY) for i, k in enumerate(fac)) + times(len(fac), Y3)
        used = []
        for i, k in enumerate(fac):
            if k in (2, 5) and (slot := next(j for j, v in enumerate(top) if v == k and j not in used)) is not None:
                used.append(slot)
                out += sl(0.4 + 0.25 * i, (slot - i) * S, Y2 - Y3, chip(i, Y3, k))
                out += g('fi', 2.0, rect(X0 + slot * S - 3, Y1 - 3, C + 6, Y2 - Y1 + C + 6, 'none', GREEN, 2, rx=8))
            else:                                       # множителю места нет: поднимается и останавливается
                out += sl(0.9, 0, (Y2 - Y3) / 2, chip(i, Y3, k))
                yy = Y3 + (Y2 - Y3) / 2
                out += g('fi', 2.4, rect(X0 + i * S - 3, yy - 3, C + 6, C + 6, 'none', RED, 2, rx=8) + t(X0 + i * S + C + 16, Y3 + (Y2 - Y3) / 2 + C / 2 + 6, '✗', RED, 20, weight=700))
        rest = [j for j in range(6) if j not in used]
        if ok:
            x1, x2 = X0 + rest[0] * S - 3, X0 + rest[-1] * S + C + 3
            out += g('fi', 2.6, rect(x1, Y1 - 3, x2 - x1, C + 6, 'none', GOLD, 2, rx=8)
                     + t((x1 + x2) / 2, Y2 + C / 2 + 6, '5 × 5 × 5 = 125', GOLD, 16, weight=600))
            out += g('fi', 3.2, t(X0 + 3 * S + 10, Y3 + C / 2 + 6, '8 × 125 = 1000', GREEN, 16,
                                  anchor='start', weight=600))
        else:
            out += g('fi', 3.0, t(X0 + 3 * S - 10, Y3 + C / 2 + 6, 'не получается', RED, 16,
                                  anchor='start', weight=600))
        return svg(X0 + 6 * S + 4, Y3 + C + 10, out, maxw=X0 + 6 * S + 4)

    cap = ('Перевести дробь в десятичную — достроить множители знаменателя до множителей 1000. '
           'Недостающие фишки и есть домножитель; тройке среди двоек и пятёрок встать некуда.')
    return fig(row(panel(8, [2, 2, 2], True), panel(6, [2, 3], False)), cap, fx=True)


def r4_estimate():
    need('Четверть от 0,4 — это 0,1', '2/5 = 0,4', '1/3 — это примерно 0,3', 'Вместе выходит около 0,4',
         'Ответ 1,3 тогда отбрасывается сразу', 'меньше половины')
    est = F(3, 10) + F(1, 4) * F(2, 5)
    assert F(2, 5) == F(4, 10) and est == F(4, 10) and est < F(1, 2) < 1 < F(13, 10)
    nl = NL(24, 380, 0, F(14, 10), 132)
    out = nl.axis(step=F(1, 10), labels=[0, 1], fmt=fm, arrow=False, size=16)
    # отрезок 2/5 = 0,4 и его четверть — своя подпись у отрезка
    bx, bw = nl.x(0), nl.x(F(2, 5)) - nl.x(0)
    out += t(bx + bw / 2, 26, '2/5 = 0,4', INK, 16, weight=600)
    out += bar(bx, 34, bw, 24, 4, filled=(0,))
    out += t(bx + bw + 10, 52, 'четверть от 0,4 — это 0,1', MUTED, 16, anchor='start')
    # прикидка суммы: 0,3 + 0,1 — своя подпись у точки
    out += nl.jump(F(3, 10), F(4, 10), BLUE, '+ 0,1', h=14, below=True, size=16)
    out += nl.point(F(3, 10), '0,3', GOLD, size=16)
    out += nl.point(est, None, GREEN) + t(nl.x(est) + 2, nl.y - 38, 'около 0,4', GREEN, 16, weight=600)
    out += nl.point(F(1, 2), None, MUTED, r=4) + t(nl.x(F(1, 2)) + 6, nl.y - 14, 'половина', MUTED, 16, anchor='start')
    out += nl.point(F(13, 10), '1,3 ✗', RED, size=17)
    return fig(svg(420, 176, out),
               'Прикидка ставит ответ около 0,4 — левее половины. Число 1,3 лежит за единицей: таким ответ быть не может.')


def bar(x, y, w, h, n, filled=(), fill=GOLD):
    from common import bar as _bar
    return _bar(x, y, w, h, n, filled=filled, fill=fill)


# ——— Глава 1 ———

def c1_check():
    need('Прикидка обещала около 0,4', 'Половина — это 15/30', 'вышло 13/30')
    ans = F(1, 3) + F(1, 4) * F(2, 5)
    assert ans == F(13, 30) and F(4, 10) < ans < F(15, 30)
    nl = NL(24, 356, 0, F(1, 2), 96)
    out = nl.axis(step=F(1, 30), labels=[0], fmt=fm, arrow=False, size=16)
    out += nl.point(F(4, 10), None, GOLD) + t(nl.x(F(4, 10)) - 8, nl.y - 16, 'прикидка 0,4', GOLD, 16,
                                               anchor='end', weight=600)
    out += nl.point(ans, None, GREEN) + t(nl.x(ans), nl.y - 42, '13/30', GREEN, 17, weight=600)
    out += line(nl.x(ans), nl.y - 36, nl.x(ans), nl.y - 8, GREEN, 1.2, " stroke-dasharray='3 3'")
    out += nl.point(F(1, 2), None, MUTED, r=4)
    out += t(nl.x(F(1, 2)), nl.y + 26, '15/30', MUTED, 16) + t(nl.x(F(1, 2)) - 12, nl.y + 46, 'половина', MUTED, 16)
    return fig(svg(420, 152, out),
               'Деления — тридцатые. Ответ на одно деление правее прикидки и на два левее половины: «чуть меньше половины».')


def c1_halves():
    need('1,25 : 0,5 = 1,25 × 2 = 2,5', 'сколько половинок помещается в числе', 'В каждой единице их две')
    a, m = F(5, 4), F(1, 2)
    assert a / m == F(5, 2)
    A = arrow_defs_p('d5c1h', [BLUE])
    nl = NL(24, 350, 0, F(3, 2), 92)
    out = A + nl.axis(step=F(1, 4), labels=[0, F(1, 2), 1, F(3, 2)], fmt=fm, arrow=False, size=16)
    out += nl.seg(0, a, GOLD, 6)
    out += nl.point(a, None, GOLD) + t(nl.x(a), nl.y + 46, '1,25', GOLD, 17, weight=600)
    out += brace(nl.x(0), nl.x(1), nl.y + 34, 'в единице — две', up=False, size=16)
    jumps = [(0, m, '1'), (m, 2 * m, '2'), (2 * m, a, '½')]
    for k, (p, q, s) in enumerate(jumps):
        out += g('fi', 0.4 + 0.9 * k, nl.jump(p, q, BLUE, s, h=24, marker='d5c1h0', size=18))
    ghost = nl.jump(a, 3 * m, GREY, None, h=24).replace("stroke-width='2'", "stroke-width='2' stroke-dasharray='4 4'")
    out += g('fi', 2.2, ghost)
    out += g('fi', 3.0, t(nl.x(F(3, 2)) + 14, nl.y - 30, '= 2,5', GREEN, 19, anchor='start', weight=700))
    return fig(svg(420, 176, out),
               'Сколько раз мерка 0,5 уложилась в 1,25 — таково и частное: две целые мерки и ещё половина третьей.', fx=True)


# ——— Глава 2 ———

def boat(x, y, col=BLUE):
    return path([(x - 13, y - 5), (x + 13, y - 5), (x + 8, y + 5), (x - 8, y + 5)], col, 1.8, fill=col,
                extra=" fill-opacity='0.8'")


def c2_hour():
    need('Своим ходом лодка отходит по воде на 8 км', 'сносит лодку вниз по реке на 2 км',
         '8 + 2 = 10 км за час', '8 − 2 = 6 км за час')
    own, cur = 8, 2
    out = ''
    rows = [('по течению', +1, own + cur, f'8 + 2 = {own + cur}'), ('против течения', -1, own - cur, f'8 − 2 = {own - cur}')]
    assert rows[0][2] == 10 and rows[1][2] == 6
    for r, (name, sgn, res, formula) in enumerate(rows):
        y0 = 6 + r * 156
        nl = NL(30, 366, 0, 10, y0 + 118)
        out += t(14, y0 + 16, name, INK, 17, anchor='start', weight=600)
        out += t(406, y0 + 16, f'с берега: {formula}', GREEN, 16, anchor='end', weight=600, cls='fi', d=4.0)
        out += rect(14, y0 + 28, 392, 70, CYAN, 'none', 0, extra=" fill-opacity='0.10'")
        out += chevrons(46 if sgn > 0 else 50, 390, y0 + 88, sgn)
        out += nl.axis(step=1, labels=[0, 2, 4, 6, 8, 10], arrow=False, size=16)
        out += t(nl.x(10) + 14, nl.y + 5, 'км', MUTED, 16, anchor='start')
        yb, yc = y0 + 52, y0 + 70                       # стрелка своего хода и стрелка сноса
        x0, x8, xr = nl.x(0), nl.x(own), nl.x(res)
        out += line(x0, yb, x8, yb, BLUE, 3, " class='dr' pathLength='100' style='--d:0.3s;--dur:1.3s'")
        out += g('fi', 1.6, head(x8, yb, 1, BLUE) + t(nl.x(3), yb - 9, 'своим ходом 8', BLUE, 16, weight=600))
        out += line(x8, yc, xr, yc, CYAN, 3, " class='dr' pathLength='100' style='--d:2.2s;--dur:1.2s'")
        lx, anc = (x8 - 10, 'end') if sgn > 0 else (x8 + 10, 'start')   # подпись — по другую сторону от 8
        out += g('fi', 3.4, head(xr, yc, sgn, CYAN) + t(lx, yc + 6, 'снос 2', CYAN, 16, anchor=anc, weight=600))
        out += sl(0.3, x8 - x0, 0, sl(2.2, xr - x8, 0, boat(x0, y0 + 36)))
        out += g('fi', 4.0, line(xr, y0 + 28, xr, nl.y - 6, GREEN, 1.5, " stroke-dasharray='4 3'"))
    return fig(svg(420, 310, out),
               'Синяя стрелка в обеих строках одна и та же — лодка своим ходом проходит 8 км. '
               'Течение лишь добавляет к ней свои 2 км или отнимает их.', fx=True)


def c2_fan():
    need('Поставь три скорости в ряд: 6, 8, 10', 'на два течения')
    own = 8
    nl = NL(24, 356, 4, 12, 92)
    out = nl.axis(step=1, labels=range(4, 13), arrow=False, size=16)
    out += t(nl.x(own), nl.y + 66, 'собственная', GOLD, 16, weight=600)
    u = nl.x(1) - nl.x(0)
    for sgn in (-1, 1):
        out += sl(0.4, sgn * u, 0, sl(2.0, sgn * u, 0, dot(nl.x(own), nl.y, 6, GREEN)))
    out += nl.point(own, None, GOLD, r=6)
    out += g('fi', 3.4, t(nl.x(6), nl.y + 46, 'против течения', GREEN, 16, weight=600)
             + t(nl.x(10), nl.y + 46, 'по течению', GREEN, 16, weight=600))
    arcs = ''.join(nl.jump(own, q, CYAN, 'течение', h=26, size=16) for q in (own - 2, own + 2))
    out += g('fi', 3.9, arcs)
    out += g('fi', 4.6, brace(nl.x(6), nl.x(10), nl.y + 76, 'два течения', up=False, col=CYAN, size=16))
    return fig(svg(420, 208, out),
               'Течение отодвигает две скорости от собственной поровну в разные стороны: середина остаётся на 8, '
               'а между крайними — два течения.', fx=True)


def c2_task():
    need('Собственная скорость лодки `8` км/ч, скорость течения `2` км/ч', 'по течению', 'за `3` часа')
    A = arrow_defs_p('d5c2t', [GOLD, BLUE])
    xl, xr = 46, 374
    out = A
    out += rect(12, 52, 396, 92, CYAN, 'none', 0, extra=" fill-opacity='0.10'")
    out += chevrons(250, 350, 122, 1)
    out += t(76, 128, 'течение 2 км/ч', CYAN, 17, anchor='start', weight=600)
    for x in (xl, xr):
        out += rect(x - 6, 40, 12, 112, GREY, 'none', 0, extra=" fill-opacity='0.9'")
    out += boat(xl + 34, 84)
    out += t(xl + 56, 90, 'собственная 8 км/ч', BLUE, 17, anchor='start', weight=600)
    out += (f"<line x1='{xl}' y1='28' x2='{xr - 4}' y2='28' stroke='{GOLD}' stroke-width='2.5' marker-end='url(#d5c2t0)'/>"
            + t((xl + xr) / 2, 18, 'туда — по течению, 3 ч', GOLD, 17, weight=600))
    out += (f"<line x1='{xr}' y1='166' x2='{xl + 4}' y2='166' stroke='{BLUE}' stroke-width='2.5' marker-end='url(#d5c2t1)'/>"
            + t((xl + xr) / 2, 192, 'обратно — против течения, ? ч', BLUE, 17, weight=600))
    return fig(svg(420, 202, out), 'Обратно лодка идёт по тому же отрезку между пристанями, но течение теперь ей навстречу.')


def c2_hours():
    need('обратно должно выйти дольше', '10 × 3 = 30', '30 : 6 = 5', 'скорость против течения = `6` км/ч')
    dist, v1, v2 = 30, 10, 6
    assert v1 * 3 == dist and v2 * 5 == dist
    A = arrow_defs_p('d5c2h', [GOLD, BLUE])
    nl = NL(30, 352, 0, dist, 94)
    out = A + nl.axis(step=2, labels=[], arrow=False)
    out += t(nl.x(0) - 12, nl.y + 6, '0', MUTED, 16, anchor='end') + t(nl.x(dist) + 12, nl.y + 6, '30 км', MUTED, 16, anchor='start')
    out += t(nl.x(0), 18, 'туда — по 10 км за час', GOLD, 17, anchor='start', weight=600)
    out += t(nl.x(0), 166, 'обратно — по 6 км за час', BLUE, 17, anchor='start', weight=600)
    for k in range(dist // v1):
        out += g('fi', 0.3 + 0.5 * k, nl.jump(k * v1, (k + 1) * v1, GOLD, f'{k + 1} ч', h=24, size=17,
                                              marker='d5c2h0'))
    for k in range(dist // v2):
        out += g('fi', 2.0 + 0.55 * k, nl.jump(dist - k * v2, dist - (k + 1) * v2, BLUE, f'{k + 1} ч', h=22,
                                               below=True, size=17, marker='d5c2h1'))
    return fig(svg(420, 176, out),
               'Время — число часовых отрезков на одном и том же пути. Против течения часовой отрезок короче, '
               'поэтому их уходит больше.', fx=True)


def c2_error():
    need('разность равна `24 − 16 = 8`', '«течение `8` км/ч»', 'эти `8` — это **два** течения',
         'собственная скорость = `20` км/ч', 'скорость течения = `4` км/ч')
    up, down = 24, 16
    own, cur = (up + down) // 2, (up - down) // 2
    assert own == 20 and cur == 4
    nl = NL(24, 380, 14, 26, 72)
    out = nl.axis(step=1, labels=[down, own, up], arrow=False, size=16)
    out += nl.point(down, None, GREEN) + nl.point(up, None, GREEN) + nl.point(own, None, GOLD, r=6)
    out += t(nl.x(down), nl.y + 46, 'против течения', GREEN, 16) + t(nl.x(up), nl.y + 46, 'по течению', GREEN, 16)
    out += t(nl.x(own), nl.y + 66, 'собственная', GOLD, 16, weight=600)
    for p, q in ((down, own), (own, up)):
        out += nl.jump(p, q, CYAN, f'течение {cur}', h=24, size=17)
    out += brace(nl.x(down), nl.x(up), nl.y + 76, '24 − 16 = 8', up=False, size=17)
    yb = nl.y + 146
    xr = 92
    out += t(xr, yb, 'течение 8 км/ч', RED, 16, weight=600) + line(xr - 62, yb - 5, xr + 62, yb - 5, RED, 2.2)
    out += t(298, yb, '8 = 4 + 4 — два течения', GREEN, 16, weight=600)
    return fig(svg(420, 228, out),
               'Разность скоростей занимает два одинаковых промежутка: одно течение река добавила, второе отняла.')


# ——— Глава 3 ———

def c3_petya():
    need('оценки `5`, `4`, `4`, `3`, `4`', 'Их сумма `20`', '20 : 5 = 4')
    vals = [5, 4, 4, 3, 4]
    s, n = sum(vals), len(vals)
    avg = F(s, n)
    assert s == 20 and avg == 4
    c, st, base = 22, 30, 140

    def labels(x0, vs, col, cls=None, d=None):
        body = ''.join(t(x0 + i * st + c / 2, base + 22, v, col, 15, weight=600) for i, v in enumerate(vs))
        return g(cls, d, body) if cls else body

    x0 = 46
    src = ''.join(cell_col(x0 + i * st, base, v, c) for i, v in enumerate(vals))
    src += labels(x0, vals, INK) + t(x0 + 2 * st + c / 2, base + 46, 'сумма 20', MUTED, 14)
    left = svg(x0 + 5 * st + 30, base + 56, src, maxw=x0 + 5 * st + 30)

    x1 = 46
    hi = vals.index(max(vals))
    lo = vals.index(min(vals))
    cp = t(16, base - 50, '=', INK, 26, weight=600)
    for i, v in enumerate(vals):
        cp += cell_col(x1 + i * st, base, v - (1 if i == hi else 0), c)
    mover = rect(x1 + hi * st, base - vals[hi] * c, c, c, GOLD, GOLD, 1.5, extra=" fill-opacity='0.75'")
    cp += sl(0.5, (lo - hi) * st, (vals[hi] - vals[lo] - 1) * c, mover)
    yl = base - int(avg) * c
    cp += g('fi', 2.0, line(x1 - 6, yl, x1 + 4 * st + c + 6, yl, GREEN, 2.2, " stroke-dasharray='6 4'")
            + t(x1 + 4 * st + c + 12, yl + 5, fm(avg), GREEN, 16, anchor='start', weight=700))
    cp += g('fo', 1.9, labels(x1, vals, INK))
    cp += labels(x1, [fm(avg)] * n, GREEN, 'fi', 2.2)
    cp += t(x1 + 2 * st + c / 2, base + 46, 'сумма 20', MUTED, 14)
    right = svg(x1 + 5 * st + 30, base + 56, cp, maxw=x1 + 5 * st + 30)
    return fig(row(left, right),
               'Клетки только переезжают: ни одна не появилась и не пропала, сумма осталась 20. '
               'Уровень, на котором столбики сравнялись, — среднее.', fx=True)


def c3_minmax():
    need('не больше `5 × 5 = 25`', 'не меньше `3 × 5 = 15`', '3 ≤ 4 ≤ 5')
    vals = [5, 4, 4, 3, 4]
    mx, mn, n = max(vals), min(vals), len(vals)
    assert mx * n == 25 and mn * n == 15 and mn <= sum(vals) / n <= mx
    c, st, base, x0 = 28, 36, 166, 36
    out = ''
    for i, v in enumerate(vals):
        x = x0 + i * st
        for j in range(mx):
            y = base - (j + 1) * c
            if j >= v:
                out += rect(x, y, c, c, 'none', GREY, 1.2, extra=" stroke-dasharray='3 3'")
            else:
                out += rect(x, y, c, c, GOLD if j < mn else VIOLET, MUTED, 1,
                            extra=f" fill-opacity='{0.55 if j < mn else 0.35}'")
        out += t(x + c / 2, base + 24, v, INK, 17, weight=600)
    xe = x0 + (n - 1) * st + c
    for lev, col, text in ((mx, GREY, 'не больше 5 × 5 = 25'), (sum(vals) // n, GREEN, 'среднее 4'),
                           (mn, GOLD, 'не меньше 3 × 5 = 15')):
        y = base - lev * c
        out += line(x0 - 8, y, xe + 8, y, col, 2, " stroke-dasharray='6 4'")
        out += t(xe + 14, y + 6, text, col, 16, anchor='start', weight=600)
        out += t(x0 - 14, y + 6, lev, col, 16, anchor='end')
    return fig(svg(400, base + 34, out),
               'Столбики целиком внутри пунктирной рамки из 25 клеток и целиком накрывают золотые 15: '
               'выровняются они где-то между 3 и 5.')


def c3_katya():
    need('`4,25 × 4 = 17`', '`4,4 × 5 = 22`', '`22 − 17 = 5`', 'те же четыре плюс одна новая')
    a4, a5 = F(17, 4), F(22, 5)
    s4, s5 = a4 * 4, a5 * 5
    assert (s4, s5, s5 - s4) == (17, 22, 5)
    X0, U = 16, F(388, 22)
    X = lambda v: float(X0 + v * U)
    out = t(X0, 22, 'сумма четырёх = 4,25 × 4 = 17', INK, 17, anchor='start', weight=600)
    out += bar(X(0), 32, X(s4) - X(0), 28, 4)
    out += t(X0, 100, 'сумма пяти = 4,4 × 5 = 22', INK, 17, anchor='start', weight=600)
    out += bar(X(0), 110, X(s4) - X(0), 28, 4)
    out += rect(X(s4), 110, X(s5) - X(s4), 28, GREEN, GREEN, 1.8, extra=" fill-opacity='0.55'")
    out += line(X(s4), 60, X(s4), 110, GREY, 1.4, " stroke-dasharray='4 3'")
    out += t(X(s4) + 6, 84, '17', MUTED, 16, anchor='start')
    out += brace(X(0), X(s4), 146, 'те же четыре', up=False, size=16)
    out += brace(X(s4), X(s5), 146, None, up=False, col=GREEN)
    xm = (X(s4) + X(s5)) / 2
    out += t(xm - 6, 182, 'пятая оценка', GREEN, 16, weight=600) + t(xm - 6, 202, '22 − 17 = 5', GREEN, 17, weight=700)
    return fig(svg(420, 210, out),
               'Сумма пяти — та же сумма четырёх и пристроенный хвост; хвост и есть новая оценка.')


def c3_speed():
    need('`36 : 12 = 3`', '`36 : 18 = 2`', '`72 : 5 = 14,4`', '`(12 + 18) : 2 = 15`', 'медленная скорость «весит» больше')
    hours = [12] * (36 // 12) + [18] * (36 // 18)
    total = sum(hours)
    avg = F(total, len(hours))
    naive = F(12 + 18, 2)
    assert total == 72 and avg == F(72, 5) and naive == 15 and avg < naive
    k, w, st, base = 9, 28, 36, 186
    Y = lambda v: float(base - v * k)

    def cols(x0):
        return ''.join(rect(x0 + i * st, Y(v), w, float(v * k), VIOLET, MUTED, 1, extra=" fill-opacity='0.35'")
                       for i, v in enumerate(hours))

    def under(x0, cls=None, d=None):
        vals = ''.join(t(x0 + i * st + w / 2, base + 20, v, INK, 15, weight=600) for i, v in enumerate(hours))
        return g(cls, d, vals) if cls else vals

    def braces(x0):
        n12 = hours.count(12)
        return (brace(x0, x0 + (n12 - 1) * st + w, base + 30, '3 ч', up=False, size=15)
                + brace(x0 + n12 * st, x0 + (len(hours) - 1) * st + w, base + 30, '2 ч', up=False, size=15))

    x0 = 44
    left = svg(x0 + 4 * st + w + 50, base + 66, cols(x0) + under(x0) + braces(x0), maxw=x0 + 4 * st + w + 50)

    x1 = 44
    cp = t(16, Y(9), '=', INK, 26, weight=600)
    # в начале столбики целые; разрез по уровню проявляется только вместе с переездом своего столбика
    start = {3: 0.5, 4: 0.95}
    for i, v in enumerate(hours):
        x = x1 + i * st
        if v == 12:
            cp += rect(x, Y(v), w, float(v * k), VIOLET, MUTED, 1, extra=" fill-opacity='0.35'")
            continue
        d0 = start[i]
        cp += g('fo', d0, rect(x, Y(v), w, float(v * k), VIOLET, MUTED, 1, extra=" fill-opacity='0.35'"))
        cp += g('fi', d0, rect(x, Y(avg), w, float(avg * k), VIOLET, MUTED, 1, extra=" fill-opacity='0.35'"))
    # излишек столбиков 18 над 14,4 (по 3,6) режется на куски 2,4 и 1,2 и переезжает в недостачи столбиков 12 (по 2,4)
    moves = [(3, avg, F(12, 5), 0, 12), (4, avg, F(12, 5), 1, 12),
             (3, avg + F(12, 5), F(6, 5), 2, 12), (4, avg + F(12, 5), F(6, 5), 2, 12 + F(6, 5))]
    assert all(hours[s] == 18 for s, *_ in moves) and sum(h for _, _, h, *_ in moves) == 2 * (18 - avg)
    for d, (src, bot, h, dst, dbot) in enumerate(moves):
        piece = rect(x1 + src * st, Y(bot + h), w, float(h * k), GOLD, GOLD, 1.2, extra=" fill-opacity='0.75'")
        cp += g('fi', start[src], sl(0.5 + 0.45 * d, (dst - src) * st, float((bot - dbot) * k), piece))
    for i in (0, 1, 2):
        assert sum(h for _, _, h, dd, _ in moves if dd == i) == avg - 12
    xe = x1 + 4 * st + w
    cp += g('fi', 3.4, line(x1 - 6, Y(avg), xe + 6, Y(avg), GREEN, 2.2, " stroke-dasharray='6 4'")
            + t(xe + 10, Y(avg) + 15, fm(avg), GREEN, 16, anchor='start', weight=700))
    cp += g('fi', 4.0, line(x1 - 6, Y(naive), xe + 6, Y(naive), RED, 1.8, " stroke-dasharray='3 3'")
            + t(xe + 10, Y(naive) - 4, fm(naive), RED, 15, anchor='start', weight=600))
    cp += g('fo', 0.4, under(x1)) + braces(x1)
    right = svg(xe + 50, base + 66, cp, maxw=xe + 50)
    return fig(row(left, right),
               'Столбик — километры за один час. Излишек двух быстрых часов засыпает недостачу трёх медленных: '
               'медленных часов больше, и уровень встаёт ниже 15.', fx=True)


def c3_classes():
    need('`20` учеников со средним баллом `4`', '`30` учеников со средним `3,5`', '`(4 + 3,5) : 2 = 3,75`',
         '`185 : 50 = 3,7`')
    n1, a1, n2, a2 = 20, F(4), 30, F(7, 2)
    tot = n1 * a1 + n2 * a2
    avg = tot / (n1 + n2)
    naive = (a1 + a2) / 2
    assert tot == 185 and avg == F(37, 10) and naive == F(15, 4) and abs(avg - a2) < abs(avg - a1)
    nl = NL(24, 380, F(34, 10), F(41, 10), 124)
    out = nl.axis(step=F(1, 10), labels=[a2, a1], fmt=fm, arrow=False, size=17)

    def stack(v, n, col):
        o, xc = '', nl.x(v)
        for j in range(n):
            r_, c_ = divmod(j, 10)
            o += dot(xc + (c_ - 4.5) * 8, nl.y - 14 - r_ * 9, 3, col)
        return o

    out += stack(a2, n2, VIOLET) + t(nl.x(a2), nl.y - 56, '30 учеников', VIOLET, 16, weight=600)
    out += stack(a1, n1, VIOLET) + t(nl.x(a1), nl.y - 47, '20 учеников', VIOLET, 16, weight=600)
    out += nl.point(naive, None, RED)
    out += t(nl.x(naive) + 8, nl.y - 40, '3,75 ✗', RED, 17, weight=600) + t(nl.x(naive) + 8, nl.y - 16, '(4 + 3,5) : 2', RED, 16)
    out += nl.point(avg, None, GREEN)
    out += t(nl.x(avg), nl.y + 48, '3,7', GREEN, 17, weight=700) + t(nl.x(avg), nl.y + 68, '185 : 50', GREEN, 16)
    return fig(svg(420, 200, out), 'Учеников со средним 3,5 больше — туда и сдвинут верный ответ, левее середины 3,75.')


def c3_zeros():
    need('`70`, `0`, `50`, `0`, `0`, `90`, `0`', '`210 : 7 = 30`', '`210 : 3 = 70`')
    days = [70, 0, 50, 0, 0, 90, 0]
    s = sum(days)
    nz = [v for v in days if v]
    assert s == 210 and s // len(days) == 30 and s // len(nz) == 70
    w, st, base, x0 = 22, 28, 150, 14

    def panel(good):
        col = GREEN if good else RED
        lev = F(s, len(days)) if good else F(s, len(nz))
        out = t(x0 + 3.5 * st, 20, f'{s} : {len(days) if good else len(nz)} = {fm(lev)}', col, 16, weight=700)
        for i, v in enumerate(days):
            x = x0 + i * st
            out += line(x - 2, base + 2, x + w + 2, base + 2, GREY, 3)
            if v:
                out += rect(x, base - v, w, v, VIOLET, MUTED, 1, extra=" fill-opacity='0.35'")
            lab = t(x + w / 2, base + 22, v, INK if (v or good) else GREY, 14, weight=600)
            out += lab
            if not v and not good:
                out += t(x + w / 2, base - 8, '✗', RED, 16, weight=700)
            if good or v:
                out += line(x - 3, base - float(lev), x + w + 3, base - float(lev), col, 2.4, " stroke-dasharray='5 3'")
        return svg(x0 + 7 * st + 6, base + 30, out, maxw=x0 + 7 * st + 6)

    return fig(row(panel(False), panel(True)),
               'День без трат — пустое, но место в ряду: верный уровень стоит над всеми семью днями.')


FIGS = {
    'внутри одни двойки и пятёрки, сколько нулей ни приписывай': r2_chips,
    'Ответ 1,3 тогда отбрасывается сразу': r4_estimate,
    'Прикидка обещала около 0,4': c1_check,
    '1,25 : 0,5 = 1,25 × 2 = 2,5': c1_halves,
    'Река не меняет собственную скорость лодки': c2_hour,
    'Поставь три скорости в ряд': c2_fan,
    'По течению лодка прошла путь от пристани до пристани': c2_task,
    'Проверка на здравый смысл: обратно должно выйти дольше': c2_hours,
    'назвать течением всю разность скоростей': c2_error,
    'у Пети за неделю оценки': c3_petya,
    'Откуда третья строка': c3_minmax,
    'пятой оценкой должна быть': c3_katya,
    'Сравни с 15 км/ч, которые дало бы': c3_speed,
    'ровно потому, что учеников со средним 3,5 больше': c3_classes,
    'включая те, когда расход был нулевой': c3_zeros,
}


if __name__ == '__main__':
    import sys
    sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'tools'))
    import md2html
    _, _, chapters, _ = md2html.split_chapters(MD)
    BLOCKS = [norm(v) for c in chapters for _, v in c['blocks']]
    out = {}
    for anchor, f in FIGS.items():
        hits = [b for b in BLOCKS if anchor in b]
        assert len(hits) == 1, f'якорь «{anchor}» встречается в {len(hits)} блоках'
        out[anchor] = f()
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(out), 'рисунков,', sum('fx' in v.split('>', 1)[0] for v in out.values()), 'анимаций →', os.path.relpath(VIS))
