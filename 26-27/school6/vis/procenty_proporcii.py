#!/usr/bin/env python3
"""Иллюстрации учебника «Проценты и пропорции» (6 класс) → math6_2_procenty_proporcii_uchebnik.vis.json (пишется целиком).

План рисунков и мысль каждого движения: 26-27/school6/vis/plan_procenty_proporcii.md.
Числа на рисунках вычисляются здесь (Fraction / Decimal) и сверяются через assert с текстом MD (need).

Запуск: python3 26-27/school6/vis/procenty_proporcii.py
"""
import json, os, re
from decimal import Decimal as D
from fractions import Fraction as F

import common
from common import (svg, fig, g, rect, line, row, path, dot, cells, NumLine, arrow_defs_p,
                    GOLD, BLUE, GREEN, RED, VIOLET, CYAN, GREY, INK, MUTED, DARK)

# Порог координатора: на телефоне (рисунок шириной 440 ужимается до ~330 px) подписи не мельче 11 px —
# значит, в единицах viewBox не меньше 15. Обёртки поднимают всё, что мельче.
MIN_FONT = 15


def t(x, y, s, fill=MUTED, size=None, *a, **k):
    return common.t(x, y, s, fill, max(size or MIN_FONT, MIN_FONT), *a, **k)


def brace(*a, **k):
    k['size'] = max(k.get('size', MIN_FONT), MIN_FONT)
    return common.brace(*a, **k)


def bar(*a, **k):
    k['size'] = max(k.get('size', MIN_FONT), MIN_FONT)
    return common.bar(*a, **k)

HERE = os.path.dirname(os.path.abspath(__file__))
MDP = os.path.join(HERE, '..', 'math6_2_procenty_proporcii_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math6_2_procenty_proporcii_uchebnik.vis.json')
MD = open(MDP).read()


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', s)).strip()


def need(*ss):
    """Строка (число, запись) действительно стоит в тексте MD."""
    for s in ss:
        assert s in MD, f'нет в MD: {s!r}'


def num(v):
    """Число так, как оно набрано в тексте: 10 000, 0,05, 9,6."""
    v = D(str(v)).normalize()
    s = format(v, 'f')
    ip, _, fp = s.partition('.')
    if len(ip) > 4:
        ip = f'{int(ip):,}'.replace(',', ' ')
    return ip + (',' + fp if fp else '')


# ——— примитивы этой книги (поверх common) ———

def fi(d, body):
    return g('fi', d, body)


def fo(d, body, o=0):
    return g('fo', d, body, f';--o:{o}')


def sl(d, dx, dy, body):
    return g('sl', d, body, f';--to:translate({dx}px,{dy}px)')


def drline(x1, y1, x2, y2, d, col=INK, sw=2, dur=0.5):
    return (f"<line class='dr' pathLength='100' x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' "
            f"stroke-width='{sw}' style='--d:{d}s;--dur:{dur}s'/>")


def box(x, y, w, h, col, op=0.35, stroke=None, sw=1.5, rx=0):
    return rect(round(x, 1), round(y, 1), round(w, 1), round(h, 1), col, stroke or col, sw, rx,
                extra=f" fill-opacity='{op}'")


def arr(x1, y1, x2, y2, col, mid, sw=2, extra=''):
    return line(round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1), col, sw,
                f" marker-end='url(#{mid})'{extra}")


def alpha(col, op):
    return col + format(round(op * 255), '02x')


def sotnya(x, y, c, k=0, col=GOLD, op=0.65, extra=None, outline=MUTED):
    """Сотня 10 × 10 (cells): первые k клеток закрашены по столбцам; extra = {(i, j): цвет} поверх."""
    fill = {(n // 10, n % 10): alpha(col, op) for n in range(k)}
    fill.update(extra or {})
    return cells(x, y, 10, 10, c, stroke='#3a4a60', fill=fill) + rect(x, y, 10 * c, 10 * c, 'none', outline, 1.8)


def mark(x, y, ok, size=22):
    return t(x, y, '✓' if ok else '✗', GREEN if ok else RED, size, weight=700)


def zigzag_base(x, y, w, h, label):
    """Основание столбика роста — не в масштабе: посередине излом."""
    ym = y + h / 2
    zz = [(x - 3, ym + 4)]
    n = 6
    for i in range(1, n + 1):
        zz.append((x - 3 + i * (w + 6) / n, ym + (-4 if i % 2 else 4)))
    band = path(zz + [(p[0], p[1] - 9) for p in reversed(zz)], DARK, 0, DARK)
    edge1 = path(zz, MUTED, 1.4, closed=False)
    edge2 = path([(p[0], p[1] - 9) for p in zz], MUTED, 1.4, closed=False)
    return (box(x, y, w, h, GREY, 0.45, MUTED, 1.5) + band + edge1 + edge2
            + t(x + w / 2, y + h - 8, label, INK, 14, weight=600))


def brick(x, ytop, w, h, col, label=None, op=0.45, size=14):
    out = box(x, ytop, w, h, col, op, col, 1.6)
    if label is not None:
        out += t(round(x + w / 2, 1), round(ytop + h / 2 + 5, 1), label, INK, size, weight=600)
    return out


def vbracket(x, y1, y2, col, sw=2):
    """Вертикальная скобка-охват слева от столбика (что берём за «было»)."""
    return path([(x + 6, y1), (x, y1), (x, y2), (x + 6, y2)], col, sw, closed=False)


# ——————————————————— Что такое процент ———————————————————

def v1_one():
    """В1. Сотня, одна клетка — процент."""
    need('`1% = 1/100 = 0,01`')
    c, x0, y0 = 20, 24, 40
    b = [sotnya(x0, y0, c, extra={(0, 0): alpha(GOLD, 0.9)}), arrow_defs_p('pp_v1', [GOLD])]
    b.append(path([(x0 + c / 2, y0 - 2), (x0 + c / 2, 18), (262, 18)], GOLD, 2, closed=False,
                  extra=" marker-end='url(#pp_v10)'"))
    b.append(t(272, 27, '1%', GOLD, 26, anchor='start', weight=700))
    b.append(t(272, 84, 'одна клетка', MUTED, 16, anchor='start'))
    b.append(t(272, 106, 'из 100', MUTED, 16, anchor='start'))
    b.append(t(272, 150, '1% = 1/100', INK, 18, anchor='start', weight=600))
    b.append(t(272, 178, '= 0,01', INK, 18, anchor='start', weight=600))
    return fig(svg(440, y0 + 10 * c + 16, ''.join(b), maxw=460),
               'Всё число — сто равных клеток; процент — одна из них.')


def v2_shares():
    """В2. 1/10, 1/5, 1/4, 1/2: на долю ложится сетка — граница доли идёт по её линиям."""
    shares = [F(1, 10), F(1, 5), F(1, 4), F(1, 2)]
    for q in shares:
        need(f'`{q.numerator}/{q.denominator} = {num(q.numerator / q.denominator)}` | `{int(q * 100)}%`')
    c = 17
    S = 10 * c
    pos = [(30, 34), (240, 34), (30, 270), (240, 270)]
    b = []
    for k, (q, (x, y)) in enumerate(zip(shares, pos)):
        p = int(q * 100)
        if q == F(1, 4):
            cuts = [line(x + S / 2, y, x + S / 2, y + S, MUTED, 2.2), line(x, y + S / 2, x + S, y + S / 2, MUTED, 2.2)]
            part = (x, y, S / 2, S / 2)
            cells_in = {(i, j) for i in range(5) for j in range(5)}
        else:
            n = q.denominator
            cuts = [line(round(x + i * S / n, 1), y, round(x + i * S / n, 1), y + S, MUTED, 2.2) for i in range(1, n)]
            part = (x, y, S / n, S)
            cells_in = {(i, j) for i in range(10 // n) for j in range(10)}
        assert len(cells_in) == p
        b.append(box(*part, GOLD, 0.55, GOLD, 0))
        b.append(t(x + S / 2, y - 12, f'{q.numerator}/{q.denominator}', GOLD, 17, weight=700))
        d = 0.8 + 0.7 * k
        grid = cells(x, y, 10, 10, c, stroke='#7a8aa0', sw=0.8)
        b.append(fi(d, grid))
        b.append(''.join(cuts))
        b.append(rect(x, y, S, S, 'none', MUTED, 2))
        b.append(fi(d + 0.4, t(x + S / 2, y + S + 24, f'{p} клеток = {p}%', GREEN, 16, weight=700)))
    return fig(svg(440, 500, ''.join(b), maxw=460),
               'Частые доли режут квадрат по линиям сотни — поэтому в каждой целое число клеток, то есть процентов.',
               fx=True)


def v3_over():
    """В3. 150% и 200% — больше одной сотни."""
    need('`150%` — полтора числа', '`200%` — два таких числа')
    c, x1, x2 = 13, 92, 236
    S = 10 * c
    b = []
    for y, label, k2 in ((20, '150%', 50), (196, '200%', 100)):
        b.append(t(14, y + S / 2 + 8, label, GOLD, 22, anchor='start', weight=700))
        b.append(sotnya(x1, y, c, 100))
        b.append(sotnya(x2, y, c, k2))
        b.append(t(x1 + S / 2, y + S + 20, '100%', MUTED, 14))
        b.append(t(x2 + S / 2, y + S + 20, f'{k2}%', MUTED, 14))
        b.append(t(x2 - 7, y + S / 2 + 7, '+', INK, 18))
    return fig(svg(400, 370, ''.join(b), maxw=420), 'Процентов больше ста — значит, взято больше одного целого числа.')


def v4_double():
    """В4. Одна полоса — книги сверху, проценты снизу."""
    need('**400** книг', '**60** — словари', '**15%** всех книг')
    W, P = 400, 60
    assert F(P, W) * 100 == 15
    x0, x1, y, h = 24, 404, 70, 34
    s = (x1 - x0) / W
    xp = x0 + P * s
    b = [box(x0, y, P * s, h, GOLD, 0.6, GOLD, 0), rect(x0, y, x1 - x0, h, 'none', MUTED, 1.8)]
    b.append(line(xp, y - 6, xp, y + h + 6, GOLD, 1.6))
    b.append(brace(x0, xp, y - 22, 'часть', col=GOLD))
    for xv, top, bot, anc in ((x0, '0', '0%', 'middle'), (xp, '60', '15%', 'middle'), (x1, '400 книг', '100%', 'end')):
        b.append(t(xv + (6 if anc == 'end' else 0), y - 8, top, INK, 15, anchor=anc, weight=600))
        b.append(t(xv + (6 if anc == 'end' else 0), y + h + 20, bot, GOLD if bot == '15%' else MUTED, 15, anchor=anc, weight=600))
    b.append(brace(x0, x1, y + h + 30, 'целое', up=False))
    return fig(svg(430, 175, ''.join(b), maxw=460),
               'Часть и её процент стоят в одном месте полосы: это одно количество, сосчитанное двумя способами.')


# ——————————————————— Ритуалы ———————————————————

def r1_from_what():
    """Р1. 20% от 300 и 20% от 50 — один процент, разные куски."""
    need('`20%` от `300` — это `60`', '`20%` от `50` — это `10`')
    s, x0, h = 1.0, 24, 34
    b = []
    for y, W in ((40, 300), (130, 50)):
        part = W * F(20, 100)
        w = W * s
        b.append(t(x0, y - 12, f'целое {W}', MUTED, 14, anchor='start'))
        b.append(bar(x0, y, w, h, 5, filled=(0,), fill=GOLD))
        b.append(t(x0 + w + 10, y + h / 2 + 5, f'20% → {part}', GOLD, 15, anchor='start', weight=700))
    return fig(svg(440, 180, ''.join(b), maxw=460),
               'Один и тот же процент от разных целых — куски разной длины. Пока целое не названо, кусок не измерить.')


def r3_estimate():
    """Р3. 18% от 400: около пятой части 80; 72 рядом, 720 — дальше всего целого."""
    need('`18%` от `400`', 'пятая часть — это `80`', 'Получилось `72`', 'Получилось `720`')
    assert 400 * F(18, 100) == 72 and 400 * F(1, 5) == 80
    nl = NumLine(24, 416, 0, 720, 110)
    b = [bar(nl.x(0), 50, nl.x(400) - nl.x(0), 30, 5, filled=(0,), fill=GOLD)]
    b.append(t(nl.x(400) + 8, 70, '400', INK, 15, anchor='start', weight=600))
    b.append(brace(nl.x(0), nl.x(80), 44, 'пятая часть', col=GOLD))
    b.append(nl.axis(step=80, labels=[0, 80, 400], size=MIN_FONT))
    b.append(nl.point(72, None, GREEN) + t(nl.x(72), 158, '72 ✓', GREEN, 16, weight=700))
    b.append(nl.point(720, None, RED) + t(nl.x(720), 158, '720 ✗', RED, 16, weight=700))
    return fig(svg(440, 172, ''.join(b), maxw=460),
               '720 лежит дальше всего числа 400 — так быть не может; 72 стоит у пятой части, как и обещала прикидка.')


def r4_rest():
    """Р4. Сотня: 35 израсходовано, 65 осталось."""
    need('`100% − 35% = 65%`', 'умножить целое на `0,65`')
    c, x0, y0 = 20, 20, 14
    b = [sotnya(x0, y0, c, 35, GREY, 0.85, extra={(n // 10, n % 10): alpha(GREEN, 0.55) for n in range(35, 100)})]
    b.append(box(250, 40, 18, 18, GREY, 0.85))
    b.append(t(276, 55, 'израсходовали', MUTED, 15, anchor='start'))
    b.append(t(276, 76, '35%', MUTED, 17, anchor='start', weight=700))
    b.append(box(250, 110, 18, 18, GREEN, 0.55))
    b.append(t(276, 125, 'осталось', GREEN, 15, anchor='start'))
    b.append(t(276, 146, '65% → × 0,65', GREEN, 17, anchor='start', weight=700))
    return fig(svg(440, 10 * c + 30, ''.join(b), maxw=460),
               'Остаток — это оставшиеся клетки той же сотни: его видно сразу, без вычитания рублей.')


# ——————————————————— Глава 1 ———————————————————

def c1_comma():
    """1.1. 37%, 5%, 250%, 0,4%: запятая прыгает на два места влево, пустые места — нули."""
    rows = ['37', '5', '250', '0,4']
    W, xc, size, G = 14, 318, 23, 8     # шаг цифры = её ширина; G — зазор под запятую, он едет вместе с ней
    ys = [44, 92, 140, 188]
    b = [t(150, 22, 'было', MUTED, 14), t(xc - W, 22, 'стало', MUTED, 14)]
    for s, y in zip(rows, ys):
        res = D(s.replace(',', '.')) / 100
        txt = num(res)
        need(f'`{s}% = {s}/100 = {txt}`')
        ip, _, fp = s.partition(',')
        digits = {-(len(ip) - i): ch for i, ch in enumerate(ip)}       # слот -1 — последняя цифра целой части
        digits.update({i: ch for i, ch in enumerate(fp)})
        rip, _, rfp = txt.partition(',')
        # после прыжка запятая стоит на границе слотов -2/-3: целая часть — слоты ≤ −3, дробная — от −2
        want = {-(len(rip) - i) - 2: ch for i, ch in enumerate(rip)}
        want.update({i - 2: ch for i, ch in enumerate(rfp)})
        assert all(digits[k] == v for k, v in want.items() if k in digits), s
        b.append(t(178, y, f'{s}%', INK, size, anchor='end', weight=600))
        b.append(t(206, y, '=', MUTED, size))
        for k, ch in digits.items():
            gone = k not in want                                          # лишний ноль в конце (2,50 → 2,5)
            x0_ = xc + (k + 0.5) * W + (G / 2 if k >= 0 else -G / 2)      # до прыжка зазор у старой запятой
            x1_ = xc + (k + 0.5) * W + (G / 2 if k >= -2 else -G / 2)     # после — у новой
            body = t(x0_, y, ch, INK, size, weight=600)
            if x1_ != x0_:
                body = sl(1.1, x1_ - x0_, 0, body)
            if gone:            # 2,50: ноль в конце дроби ничего не значит — бледнеет и зачёркивается, а не пропадает
                b.append(fo(2.8, body, 0.35) + fi(3.0, line(x1_ - 7, y + 2, x1_ + 7, y - 16, RED, 2.2)))
            else:
                b.append(body)
        for k, ch in want.items():
            if k not in digits:
                b.append(fi(2.6, t(xc + (k + 0.5) * W + (G / 2 if k >= -2 else -G / 2), y, ch, GOLD, size, weight=700)))
        last = max(digits) + 1
        b.append(fo(0.4, t(xc + last * W + G / 2 + 4, y, '%', INK, size, anchor='start', weight=600)))
        comma = t(xc, y + 4, ',', BLUE, size + 2, weight=700)
        b.append(sl(1.1, -2 * W, 0, comma if fp else fi(0.7, comma)))
    return fig(svg(440, 206, ''.join(b), maxw=460),
               'Нули не придуманы: это пустые места, через которые перепрыгнула запятая.', fx=True)


def c1_class():
    """1.2. 7 из 25 → каждая клетка класса дробится на 4 → 28 из 100."""
    need('`7/25 × 100 = 700/25 = 28`')
    assert F(7, 25) * 100 == 28
    C, x1, x2, y0 = 34, 20, 236, 14
    gold = {(n % 5, n // 5): alpha(GOLD, 0.65) for n in range(7)}
    b = [cells(x1, y0, 5, 5, C, stroke=MUTED, fill=gold), rect(x1, y0, 5 * C, 5 * C, 'none', MUTED, 1.8)]
    b.append(t(x1 + 2.5 * C, y0 + 5 * C + 24, '7 из 25', GOLD, 16, weight=700))
    b.append(t((x1 + 5 * C + x2) / 2, y0 + 2.5 * C + 7, '=', MUTED, 22))
    b.append(cells(x2, y0, 5, 5, C, stroke=MUTED, fill=gold) + rect(x2, y0, 5 * C, 5 * C, 'none', MUTED, 1.8))
    for i in range(5):
        xm, ym = x2 + (i + 0.5) * C, y0 + (i + 0.5) * C
        b.append(drline(xm, y0, xm, y0 + 5 * C, 0.6 + 0.15 * i, '#9fb0c6', 1))
        b.append(drline(x2, ym, x2 + 5 * C, ym, 1.4 + 0.15 * i, '#9fb0c6', 1))
    b.append(fi(2.6, t(x2 + 2.5 * C, y0 + 5 * C + 24, '28 из 100 = 28%', GREEN, 16, weight=700)))
    return fig(svg(440, y0 + 5 * C + 36, ''.join(b), maxw=460),
               'Класс дробится в сотню клеток: те же 7 учеников, а считаются теперь из ста.', fx=True)


def c1_err7():
    """1.3. 7 из 25 против 7 из 100."""
    need('написать «7%»', '`7` — это сколько из `25`')
    a = (cells(20, 10, 5, 5, 26, stroke=MUTED, fill={(n % 5, n // 5): alpha(GREEN, 0.6) for n in range(7)})
         + rect(20, 10, 130, 130, 'none', MUTED, 1.8) + t(85, 166, '7 из 25 = 28%', GREEN, 15, weight=700)
         + mark(170, 80, True))
    r = sotnya(20, 10, 13, 7, RED, 0.75) + t(85, 166, '7%', RED, 15, weight=700) + mark(170, 80, False)
    return fig(row(svg(200, 178, a, maxw=220), svg(200, 178, r, maxw=220)),
               'Квадраты одинаковые — целое одно; 7 из 25 занимают куда больше, чем 7 из ста.')


def c1_err5():
    """1.4. 5% (5 клеток) против 0,5 (50 клеток)."""
    need('`5% = 0,05`', '`0,5` — это половина')
    a = sotnya(20, 10, 13, 5, GREEN, 0.7) + t(85, 166, '5% = 0,05', GREEN, 15, weight=700) + mark(170, 80, True)
    r = sotnya(20, 10, 13, 50, RED, 0.6) + t(85, 166, '0,5 — половина', RED, 15, weight=700) + mark(170, 80, False)
    return fig(row(svg(200, 178, a, maxw=220), svg(200, 178, r, maxw=220)),
               'Запятая не на своём месте — и вместо пяти клеток половина сотни.')


# ——————————————————— Глава 2 ———————————————————

def c2_more():
    """2.1. Было 200, стало 250: прибавка 50 — одна четверть старой полосы."""
    need('Было 200, стало 250. Разность 50.', '50 : 200 = 0,25 = 25%')
    assert F(50, 200) == F(1, 4)
    pw, x0, y, h = 80, 20, 56, 38
    b = [bar(x0, y, 5 * pw, h, 5, filled=(4,), fill=GREEN, labels=['50'] * 5, size=15, opacity=0.55)]
    b.append(box(x0, y, 4 * pw, h, GOLD, 0.18, MUTED, 0))
    b.append(brace(x0, x0 + 4 * pw, y - 6, 'было 200 = 100%'))
    b.append(t(x0 + 4.5 * pw, y - 14, '+50', GREEN, 15, weight=700))
    b.append(t(x0 + 0.5 * pw, y + h + 20, '25%', MUTED, 14))
    b.append(t(x0 + 4.5 * pw, y + h + 20, '25%', GREEN, 14, weight=700))
    b.append(brace(x0, x0 + 5 * pw, y + h + 28, 'стало 250', up=False))
    return fig(svg(440, 186, ''.join(b), maxw=460),
               'Прибавку меряют кусками старой цены: 50 — ровно одна из четырёх её четвертей.')


def c2_route():
    """2.2. 18 км — 24%: кусок прикладывается к маршруту 4 раза → около 72, сам маршрут 75."""
    need('`24%` — это почти четверть', 'около `72` км', '`18 : 0,24 = 1800 : 24 = 75`')
    L, P = 75, 18
    assert P / D('0.24') == L and 4 * P == 72
    nl = NumLine(28, 403, 0, L, 112)
    y, h = 50, 34
    pw = nl.x(P) - nl.x(0)
    b = [arrow_defs_p('pp_c22', [BLUE])]
    b.append(rect(nl.x(0), y, nl.x(L) - nl.x(0), h, 'none', MUTED, 1.8))
    b.append(brace(nl.x(0), nl.x(L), y - 6, 'весь маршрут = 100%'))
    b.append(brick(nl.x(0), y, pw, h, GOLD, '18 км', 0.6))
    for k in range(1, 4):
        cp = brick(nl.x(0), y, pw, h, BLUE, '18', 0.3)
        b.append(fi(0.3 + 1.2 * (k - 1), sl(0.6 + 1.2 * (k - 1), round(k * pw, 1), 0, cp)))
    b.append(t(nl.x(P / 2), y + h + 16, '24%', GOLD, 14, weight=700))
    b.append(nl.axis(step=L, labels=[0], size=MIN_FONT))
    b.append(t(nl.x(L) + 3, nl.y + 24, '75', INK, 14, anchor='start', weight=600))
    b.append(fi(4.3, nl.point(72, None, BLUE) + t(nl.x(72) - 3, nl.y + 24, '4 × 18 = 72', BLUE, 14, anchor='end', weight=700)))
    return fig(svg(440, 146, ''.join(b), maxw=460),
               'Почти четверть укладывается в целое почти четыре раза — отсюда «около 4 × 18».', fx=True)


def c2_new_price():
    """2.3. 120 от 800 (15%) против 120 от 920 (около 13%)."""
    need('`120 : 800 = 0,15`', '`120 : 920`', 'около `13%`')
    assert F(120, 800) == F(15, 100)
    s, x0, h = 0.4, 20, 32
    b = []
    for y, W, col, ok, word, pct in ((44, 800, GREEN, True, 'старая цена 800 = 100%', '15%'),
                                     (146, 920, RED, False, 'новая цена 920 = 100%', 'около 13%')):
        b.append(t(x0, y - 10, word, col, 15, anchor='start', weight=600))
        b.append(box(x0, y, W * s, h, col, 0.25, col, 2.4))
        xs = x0 + 800 * s
        b.append(brick(xs, y, 120 * s, h, GOLD, '120', 0.6))
        b.append(t(xs + 60 * s, y + h + 18, pct, col, 14, weight=700))
        b.append(mark(x0 + 920 * s + 22, y + h / 2 + 8, ok))
    return fig(svg(440, 205, ''.join(b), maxw=460),
               'Один и тот же кусок 120 — разная доля разных целых. В вопросе «на сколько процентов» целое — то, что было до.')


# ——————————————————— Главы 3 и 4: ряды роста ———————————————————

BASE_H, YEAR = 64, ['1 год', '2 года', '3 года']


def c3_simple():
    """3.1. Простой рост: кирпич 600 считают от основания один раз, дальше копии."""
    need('`10 000 × 0,06 = 600`', '`10 600`', '`11 200`', '`11 800`')
    P0, add = 10000, 10000 * F(6, 100)
    assert add == 600
    k, w = 0.05, 64
    cx = [180, 280, 380]
    bh = float(add) * k
    base_top = 3 * bh + 40
    b = [arrow_defs_p('pp_c31', [BLUE])]
    for i, x in enumerate(cx):
        b.append(zigzag_base(x - w / 2, base_top, w, BASE_H, '10 000'))
        b.append(t(x, base_top + BASE_H + 22, YEAR[i], MUTED, 14))
    xb = cx[0] - w / 2 - 12
    b.append(fi(0.3, vbracket(xb, base_top, base_top + BASE_H, BLUE)
                + t(xb - 6, base_top + 22, '6% от', BLUE, 14, anchor='end', weight=600)
                + t(xb - 6, base_top + 40, '10 000', BLUE, 14, anchor='end', weight=600)
                + arr(xb, base_top - 2, cx[0] - w / 2 - 2, base_top - bh / 2, BLUE, 'pp_c310', 1.6)))
    one = brick(cx[0] - w / 2, base_top - bh, w, bh, GOLD, '600')
    b.append(fi(0.8, one))
    d = 1.6
    for col in (1, 2):
        for lvl in range(col + 1):
            b.append(fi(d - 0.2, sl(d, 100 * col, round(-bh * lvl, 1), one)))
        d += 1.4
    for i, x in enumerate(cx):
        b.append(fi([1.2, 2.9, 4.3][i], t(x, base_top - bh * (i + 1) - 10, num(P0 + add * (i + 1)), GREEN, 15, weight=700)))
    return fig(svg(440, base_top + BASE_H + 34, ''.join(b), maxw=460),
               'Прибавку считают один раз — от начальной суммы; каждый год ложится такой же кирпич. '
               'Основание сжато (излом), кирпичи — в одном масштабе.', fx=True)


def c4_compound():
    """4.1. Сложный рост: скобка охватывает весь столбик «было», кирпичи 1000, 1100, 1210."""
    need('Прибавка — `10%` от «было»', '| `10 000` | `1000` | `11 000` |', '| `11 000` | `1100` | `12 100` |',
         '| `12 100` | `1210` | `13 310` |')
    k, w = 0.05, 64
    cx = [180, 280, 380]
    base_top = 205
    was, adds = 10000, []
    for _ in range(3):
        a = was * F(10, 100)
        adds.append(a)
        was += a
    assert adds == [1000, 1100, 1210] and was == 13310
    hs = [float(a) * k for a in adds]
    b = [arrow_defs_p('pp_c41', [BLUE])]
    for i, x in enumerate(cx):
        b.append(zigzag_base(x - w / 2, base_top, w, BASE_H, '10 000'))
        b.append(t(x, base_top + BASE_H + 22, YEAR[i], MUTED, 14))
    stacks = []          # (ytop, h, label) кирпичей по годам
    ytop = base_top
    for a, h in zip(adds, hs):
        ytop -= h
        stacks.append((ytop, h, str(a)))
    d = 0.3
    for yr in range(3):
        x = cx[yr]
        # «было» в начале года: прежние кирпичи переезжают копией из предыдущего столбика
        if yr:
            prev = ''.join(brick(cx[yr - 1] - w / 2, yt, w, h, CYAN, lb, 0.45) for yt, h, lb in stacks[:yr])
            b.append(fi(d, sl(d + 0.1, 100, 0, prev)))
            d += 1.3
        top = stacks[yr - 1][0] if yr else base_top
        xb = x - w / 2 - 9
        lab = ''
        if yr == 0:
            lab = (t(xb - 6, base_top + 22, '10% от', BLUE, 14, anchor='end', weight=600)
                   + t(xb - 6, base_top + 40, '«было»', BLUE, 14, anchor='end', weight=600))
        b.append(fi(d, vbracket(xb, top, base_top + BASE_H, BLUE) + lab))
        yt, h, lb = stacks[yr]
        b.append(fi(d + 0.5, brick(x - w / 2, yt, w, h, GOLD, lb, 0.55)))
        b.append(fi(d + 0.8, t(x, yt - 10, num(10000 + sum(adds[:yr + 1])), GREEN, 15, weight=700)))
        d += 1.0
    assert d <= 6.5
    return fig(svg(440, base_top + BASE_H + 34, ''.join(b), maxw=460),
               'Скобка «было» каждый год охватывает весь выросший столбик — поэтому и кирпич каждый год больше.',
               fx=True)


def c4_factor():
    """4.2. +10% → 110 клеток → × 1,1; −20% → 80 клеток → × 0,8."""
    need('`110%` в виде дроби — это `1,1`', '`−20%` значит `× 0,8`')
    c = 12
    a = (sotnya(14, 10, c, 100, GOLD, 0.3) + cells(14 + 10 * c + 6, 10, 1, 10, c, stroke='#3a4a60',
                                                  fill={(0, j): alpha(GREEN, 0.7) for j in range(10)})
         + rect(14 + 10 * c + 6, 10, c, 10 * c, 'none', GREEN, 1.8)
         + t(80, 158, '+10%: 110%', GREEN, 15, weight=700) + t(80, 180, '× 1,1', GREEN, 17, weight=700))
    r = (sotnya(14, 10, c, 80, GREEN, 0.55, extra={(n // 10, n % 10): alpha(GREY, 0.85) for n in range(80, 100)})
         + t(74, 158, '−20%: 80%', GREEN, 15, weight=700) + t(74, 180, '× 0,8', GREEN, 17, weight=700))
    return fig(row(svg(180, 190, a, maxw=200), svg(180, 190, r, maxw=200)),
               'Множитель — это сколько клеток стало от сотни: 110 клеток — 1,1, 80 клеток — 0,8.')


def c4_compare():
    """4.3. Простой и сложный рост 20 000 под 10%: первый год равны, дальше сложный обгоняет."""
    need('`20000 × 1,1 = 22000`', '`22000 × 1,1 = 24200`', '`24200 × 1,1 = 26620`', '`20000 + 3 × 2000 = 26 000`')
    k, w = 0.03, 52
    simple = [2000] * 3
    comp, was = [], 20000
    for _ in range(3):
        comp.append(was * F(1, 10))
        was += comp[-1]
    assert was == 26620 and 20000 + sum(simple) == 26000
    cx = [92, 222, 352]
    base_top = 280
    b = [box(20, 14, 14, 14, CYAN, 0.5), t(40, 26, 'простой', CYAN, 14, anchor='start', weight=600),
         box(140, 14, 14, 14, VIOLET, 0.5), t(160, 26, 'сложный', VIOLET, 14, anchor='start', weight=600),
         box(262, 14, 14, 14, GOLD, 0.8), t(282, 26, 'обогнал', GOLD, 14, anchor='start', weight=600)]
    for i, x in enumerate(cx):
        for xx in (x - 28, x + 28):
            b.append(zigzag_base(xx - w / 2, base_top, w, BASE_H, '20 000'))
        b.append(t(x, base_top + BASE_H + 22, YEAR[i], MUTED, 14))
    for yr in range(3):
        x = cx[yr]
        body = ''
        ys = base_top
        for j in range(yr + 1):
            h = simple[j] * k
            ys -= h
            body += brick(x - 28 - w / 2, ys, w, h, CYAN, '2000', 0.4)
        yc = base_top
        for j in range(yr + 1):
            h = float(comp[j]) * k
            yc -= h
            body += brick(x + 28 - w / 2, yc, w, h, VIOLET, None, 0.4)
        if ys - yc > 0.5:
            body += box(x + 28 - w / 2, yc, w, ys - yc, GOLD, 0.85, GOLD, 0)
            body += line(x - 28 - w / 2, ys, x + 28 + w / 2, ys, MUTED, 1, " stroke-dasharray='3 3'")
        if yr == 0:
            body += t(x, yc - 10, '22 000', GREEN, 15, weight=700)
        elif yr == 1:
            body += t(x - 28, ys - 10, num(20000 + sum(simple[:2])), CYAN, 15, weight=700)
            body += t(x + 28, yc - 10, '24 200', VIOLET, 15, weight=700)
        else:
            body += t(x - 28, ys - 10, '26 000', CYAN, 15, weight=700)
            body += t(x + 28, yc - 10, '26 620', VIOLET, 15, weight=700)
        b.append(fi(0.4 + 1.5 * yr, body))
    return fig(svg(430, base_top + BASE_H + 34, ''.join(b), maxw=460),
               'Первый год столбики равны; дальше сложный растёт и от набежавших процентов — разрыв (золото) увеличивается.',
               fx=True)


def c4_there_back():
    """4.4. +20% от 1000 → 1200; −20% от 1200 → 960, на 40 меньше."""
    need('`1000 × 1,2 = 1200`', '`1200 × 0,8 = 960`', '`1000 − 960 = 40`')
    up = 1000 * F(12, 10); down = up * F(8, 10)
    assert (up, down, 1000 - down) == (1200, 960, 40)
    s, x0, h, y1, y2 = 0.3, 30, 36, 60, 178
    p1 = 200 * s                    # пятая часть 1000
    p2 = float(up) * s / 5          # пятая часть 1200
    b = [bar(x0, y1, 5 * p1, h, 5, filled=tuple(range(5)), fill=GOLD, opacity=0.25)]
    b.append(brace(x0, x0 + 5 * p1, y1 - 6, '1000'))
    b.append(fi(0.3, brick(x0 + 5 * p1, y1, p1, h, GREEN, None, 0.6)
                + t(x0 + 5.5 * p1, y1 + h + 18, '20% от 1000', GREEN, 14, weight=700)
                + t(x0 + 6 * p1 + 6, y1 + h / 2 + 6, '1200', INK, 15, anchor='start', weight=600)))
    copy = (box(x0, y1, 5 * p1, h, GOLD, 0.25, GOLD, 0) + box(x0 + 5 * p1, y1, p1, h, GREEN, 0.4, GREEN, 0)
            + rect(x0, y1, 6 * p1, h, 'none', MUTED, 1.8)
            + fo(2.4, ''.join(line(x0 + i * p1, y1, x0 + i * p1, y1 + h, MUTED, 1.2) for i in range(1, 6))))
    b.append(fi(0.9, sl(1.0, 0, y2 - y1, copy)))
    for i in range(1, 5):
        b.append(drline(x0 + i * p2, y2, x0 + i * p2, y2 + h, 2.7 + 0.1 * i, INK, 1.4, 0.4))
    b.append(fi(3.4, box(x0 + 4 * p2, y2, p2, h, GREY, 0.95, GREY, 0)
                + t(x0 + 4.5 * p2, y2 - 10, '20% от 1200', MUTED, 14, weight=700)))
    xk = x0 + 1000 * s
    b.append(fi(4.2, brace(x0, x0 + 4 * p2, y2 + h + 6, '960', up=False, col=GREEN)
                + line(xk, y2 - 4, xk, y2 + h + 10, INK, 1.4, " stroke-dasharray='4 4'")
                + t(xk + 6, y2 + h + 26, '40', RED, 15, anchor='start', weight=700)))
    return fig(svg(440, y2 + h + 46, ''.join(b), maxw=460),
               'Вторые 20% режут от нового целого 1200 — сброшенный кусок длиннее добавленного, и до 1000 цена не возвращается.',
               fx=True)


# ——————————————————— Глава 5 ———————————————————

def c5_how():
    """5.1. На сколько (торчащий кусок 8) и во сколько раз (мерка 4 трижды)."""
    need('`12 − 4 = 8`', '`12 : 4 = 3`')
    u, x0, h = 30, 20, 26
    b = [t(x0, 22, 'на сколько больше?', MUTED, 15, anchor='start', weight=600)]
    b.append(bar(x0, 34, 12 * u, h, 12) + t(x0 + 12 * u + 8, 34 + h / 2 + 5, '12', INK, 15, anchor='start'))
    b.append(bar(x0, 34 + h + 6, 4 * u, h, 4, filled=range(4), fill=BLUE, opacity=0.5)
             + t(x0 + 2 * u, 34 + 2 * h + 6 + 18, '4', BLUE, 15, weight=700))
    b.append(box(x0 + 4 * u, 34, 8 * u, h, GOLD, 0.6, GOLD, 0) + t(x0 + 8 * u, 34 + 2 * h + 24, '12 − 4 = 8', GOLD, 16, weight=700))
    y = 150
    b.append(t(x0, y - 12, 'во сколько раз больше?', MUTED, 15, anchor='start', weight=600))
    b.append(bar(x0, y, 12 * u, h, 12) + t(x0 + 12 * u + 8, y + h / 2 + 5, '12', INK, 15, anchor='start'))
    for k in range(3):
        b.append(bar(x0 + 4 * k * u, y + h + 6, 4 * u, h, 1, filled=(0,), fill=BLUE, opacity=0.5 - 0.1 * k)
                 + t(x0 + (4 * k + 2) * u, y + 2 * h + 6 - 7, str(k + 1), INK, 15, weight=700))
    b.append(t(x0 + 6 * u, y + 2 * h + 30, '12 : 4 = 3', BLUE, 16, weight=700))
    return fig(svg(430, y + 2 * h + 40, ''.join(b), maxw=460),
               '«На сколько» — это торчащий остаток, «во сколько раз» — сколько раз уложилась мерка.')


def c5_part():
    """5.2. 3 : 2 при 12 и 8: одна часть — 4 человека."""
    need('мальчиков `3 × 4`, девочек `2 × 4`, а всего `5 × 4 = 20`')
    pw, x0, y, h = 80, 20, 56, 52
    b = [bar(x0, y, 5 * pw, h, 5, filled=(0, 1, 2), fill=BLUE, opacity=0.35)]
    b.append(box(x0 + 3 * pw, y, 2 * pw, h, VIOLET, 0.35, VIOLET, 0) + rect(x0, y, 5 * pw, h, 'none', MUTED, 1.8))
    for p in range(5):
        col = BLUE if p < 3 else VIOLET
        for i in range(2):
            for j in range(2):
                b.append(dot(x0 + p * pw + 24 + 32 * i, y + 15 + 22 * j, 7, col))
    b.append(brace(x0, x0 + 3 * pw, y - 6, 'мальчики: 3 × 4 = 12', col=BLUE))
    b.append(brace(x0 + 3 * pw, x0 + 5 * pw, y - 6, 'девочки: 2 × 4 = 8', col=VIOLET))
    b.append(brace(x0, x0 + 5 * pw, y + h + 6, 'весь класс: 5 × 4 = 20', up=False))
    return fig(svg(440, y + h + 50, ''.join(b), maxw=460),
               'Одна часть — одна и та же группа из 4 человек; мальчикам досталось три такие группы, девочкам две.')


def c5_mix():
    """5.3. Изюм 240 = 3 части → часть 80 → орехи 400, смесь 640."""
    need('`240 : 3 = 80`', '`5 × 80 = 400`', '`8 × 80 = 640`')
    part = F(240, 3)
    assert part == 80 and 5 * part == 400 and 8 * part == 640
    pw, x0, y, h = 50, 20, 60, 40
    b = [bar(x0, y, 8 * pw, h, 8, filled=range(5), fill=BLUE, opacity=0.3)]
    b.append(box(x0 + 5 * pw, y, 3 * pw, h, VIOLET, 0.35, VIOLET, 0) + rect(x0, y, 8 * pw, h, 'none', MUTED, 1.8))
    b.append(brace(x0, x0 + 5 * pw, y - 6, 'орехи', col=BLUE))
    b.append(brace(x0 + 5 * pw, x0 + 8 * pw, y - 6, 'изюм — 240 г', col=VIOLET))
    lab = lambda p: t(x0 + (p + 0.5) * pw, y + h / 2 + 6, '80', INK, 15, weight=700)
    for p in range(5, 8):
        b.append(fi(0.6 + 0.2 * (p - 5), lab(p)))
    for i, p in enumerate(range(4, -1, -1)):
        b.append(fi(1.8 + 0.25 * i, sl(1.9 + 0.25 * i, -(5 - p) * pw, 0, lab(5))))
    b.append(fi(4.0, brace(x0, x0 + 5 * pw, y + h + 6, '5 × 80 = 400', up=False, col=BLUE)))
    b.append(fi(4.6, brace(x0, x0 + 8 * pw, y + h + 46, 'вся смесь: 8 × 80 = 640', up=False, col=GREEN)))
    return fig(svg(440, y + h + 92, ''.join(b), maxw=460),
               'Известный изюм раскладывается на свои 3 части; одна часть одинакова везде и расходится по всем восьми.',
               fx=True)


def c5_err():
    """5.4. 240 — над изюмом, а не над всей полосой."""
    need('разделить 240 на 8', 'надо на 3, число его частей')
    pw, x0, y, h = 24, 12, 44, 30

    def panel(col, ok, span):
        out = bar(x0, y, 8 * pw, h, 8, filled=range(5), fill=BLUE, opacity=0.3)
        out += box(x0 + 5 * pw, y, 3 * pw, h, VIOLET, 0.35, VIOLET, 0) + rect(x0, y, 8 * pw, h, 'none', MUTED, 1.6)
        out += brace(x0 + span[0] * pw, x0 + span[1] * pw, y - 6, '240', col=col)
        out += t(x0 + 6.5 * pw, y + h + 18, 'изюм', VIOLET, 14) + t(x0 + 2.5 * pw, y + h + 18, 'орехи', BLUE, 14)
        return out + mark(x0 + 8 * pw + 14, y + h / 2 + 8, ok)
    return fig(row(svg(230, 98, panel(GREEN, True, (5, 8)), maxw=240), svg(230, 98, panel(RED, False, (0, 8)), maxw=240)),
               'Известно не всё целое, а только изюм — значит, 240 лежит на трёх частях.')


# ——————————————————— Глава 6 ———————————————————

def c6_plan():
    """6.1. План 1 : 1000 и местность: 3 см ↔ 3000 см = 30 м."""
    need('`3` см изображает `3000` см, то есть `30` м', '`3 × 1000 = 3000`', '`3000 : 1000 = 3`')
    assert 3 * 1000 == 3000 and 3000 // 100 == 30
    b = [arrow_defs_p('pp_c61', [BLUE])]
    b.append(box(16, 50, 104, 84, INK, 0.05, MUTED, 1.6) + t(68, 40, 'план 1 : 1000', MUTED, 14))
    a1, a2, ya = 38, 68, 76
    b.append(line(a1, ya, a2, ya, GOLD, 4, " stroke-linecap='round'") + t(53, ya + 24, '3 см', GOLD, 15, weight=700))
    b.append(box(186, 30, 244, 150, GREEN, 0.07, MUTED, 1.6) + t(308, 22, 'местность', MUTED, 14))
    b1, b2, yb = 206, 410, 64
    b.append(line(b1, yb, b2, yb, GOLD, 5, " stroke-linecap='round'")
             + t(308, yb + 28, '3000 см = 30 м', GOLD, 16, weight=700))
    for p, q in ((a1, b1), (a2, b2)):
        b.append(line(p, ya, q, yb, MUTED, 1, " stroke-dasharray='4 4'"))
    b.append(arr(126, 140, 180, 140, BLUE, 'pp_c610') + t(153, 132, '× 1000', BLUE, 14, weight=700))
    b.append(arr(180, 170, 126, 170, BLUE, 'pp_c610') + t(153, 192, ': 1000', BLUE, 14, weight=700))
    return fig(svg(440, 200, ''.join(b), maxw=460),
               'План и местность — одна фигура в двух размерах: к местности умножаем, к плану делим.')


def c6_err():
    """6.2. Один и тот же лист: при 1 : 800 стена 3 см, при 1 : 8 стена 3 м уходит далеко за лист (разрыв)."""
    need('`2400 : 3 = 800`', '`3 : 24 = 1 : 8`', 'длиной 3 метра')
    assert 2400 // 3 == 800 and 2400 // 8 == 300

    def panel(ok):
        out = box(20, 30, 120, 86, INK, 0.05, MUTED, 1.5) + t(80, 136, 'лист плана', MUTED, 15)
        if ok:
            out += line(58, 76, 82, 76, GREEN, 4, " stroke-linecap='round'") + t(70, 62, '3 см', GREEN, 15, weight=700)
            out += t(70, 166, '1 : 800', GREEN, 16, weight=700) + mark(130, 167, True)
        else:
            out += line(40, 76, 170, 76, RED, 4, " stroke-linecap='round'")
            out += line(176, 86, 184, 66, MUTED, 2) + line(184, 86, 192, 66, MUTED, 2)          # разрыв: стена длиннее
            out += line(198, 76, 222, 76, RED, 4, " stroke-linecap='round'")
            out += t(170, 22, 'стена 3 м', RED, 15, weight=700)
            out += t(70, 166, '1 : 8', RED, 16, weight=700) + mark(130, 167, False)
        return out
    return fig(row(svg(230, 176, panel(True), maxw=240), svg(230, 176, panel(False), maxw=240)),
               'Лист один и тот же: при 1 : 8 стена на плане вышла бы длиной 3 метра — на лист такая не ляжет.')


# ——————————————————— Глава 7 ———————————————————

def c7_terms():
    """7.1. Замена ASCII: a : b = c : d, места 1–4, крайние и средние."""
    block = re.search(r'```\n( +a  :  b  =  c  :  d\n.*?)```', MD, re.S).group(1)
    xs = {'a': 70, 'b': 160, 'c': 250, 'd': 340}
    signs = [(115, ':'), (205, '='), (295, ':')]
    col = {'a': GOLD, 'd': GOLD, 'b': BLUE, 'c': BLUE}
    y = 90
    b = [path([(xs['a'], y - 26), (xs['a'], y - 50), (xs['d'], y - 50), (xs['d'], y - 26)], GOLD, 2, closed=False)]
    b.append(t((xs['a'] + xs['d']) / 2, y - 58, 'крайние', GOLD, 15, weight=700))
    for ch, x in xs.items():
        b.append(t(x, y, ch, col[ch], 28, weight=700, extra=" font-style='italic'"))
    for x, s in signs:
        b.append(t(x, y, s, INK, 26))
    places = {'a': '1', 'b': '2', 'c': '3', 'd': '4'}
    for ch, x in xs.items():
        b.append(t(x, y + 32, places[ch], col[ch], 18, weight=600))
    b.append(path([(xs['b'], y + 42), (xs['b'], y + 58), (xs['c'], y + 58), (xs['c'], y + 42)], BLUE, 2, closed=False))
    b.append(t((xs['b'] + xs['c']) / 2, y + 80, 'средние', BLUE, 15, weight=700))
    s = svg(410, y + 92, ''.join(b), maxw=440)
    for ch in re.findall(r'[a-z0-9]', block):
        assert f'>{ch}<' in s, ch
    return fig(s, 'Крайние члены охватывают запись снаружи, средние стоят внутри.', zamena=True)


def c7_bad():
    """7.2. 3 : 4 и 9 : 12 — закрашенное кончается на 0,75; 9 : 13 — раньше."""
    need('`3 : 4 = 0,75` и `9 : 12 = 0,75`', 'возьмём `3 : 4` и `9 : 13`', '`9 : 13` не равно `0,75`')
    x0, L, h = 84, 320, 28
    xl = x0 + 0.75 * L
    b = [t(xl, 22, '0,75', GOLD, 15, weight=700)]
    for y, (a, n, col) in zip((40, 92, 144), ((3, 4, GOLD), (9, 12, GREEN), (9, 13, RED))):
        b.append(t(x0 - 12, y + h / 2 + 6, f'{a} : {n}', col, 17, anchor='end', weight=700))
        b.append(bar(x0, y, L, h, n, filled=range(a), fill=col, opacity=0.55))
    b.append(line(xl, 28, xl, 182, GOLD, 1.6, " stroke-dasharray='5 4'"))
    b.append(mark(x0 + L + 18, 144 + h / 2 + 8, False))
    return fig(svg(440, 190, ''.join(b), maxw=460),
               'Отношения равны, когда равны доли: у верной пары закрашенное кончается в одной точке, у испорченной — раньше.')


def c7_cross():
    """7.3. 3 : 4 = 9 : 12 → 3/4 = 9/12, крайние на одной диагонали, средние на другой."""
    need('`3/4 = 9/12`', '`3 × 12 = 36` и `4 × 9 = 36`')
    assert 3 * 12 == 4 * 9 == 36
    size, y = 22, 76
    src = [(20, '3', GOLD), (38, ':', INK), (56, '4', BLUE), (80, '=', INK), (104, '9', BLUE), (122, ':', INK), (146, '12', GOLD)]
    b = [''.join(t(x, y, s, c, size, weight=700) for x, s, c in src), t(184, y, '→', MUTED, 22)]
    off = 200                                        # копия стоит справа
    L, Rx, yt, yb = 256, 368, y - 26, y + 34
    fx_ = {'3': (L, yt), '4': (L, yb), '9': (Rx, yt), '12': (Rx, yb)}
    for x, s, c in src:
        cx = x + off
        el = t(cx, y, s, c, 26, weight=700)
        if s in fx_:
            tx, ty = fx_[s]
            b.append(sl(0.6, tx - cx, ty - y, el))
        elif s == ':':
            b.append(fo(0.5, el))
        else:
            b.append(sl(0.6, 312 - cx, 0, el))
    b.append(fi(1.7, line(L - 18, y - 8, L + 18, y - 8, INK, 2) + line(Rx - 22, y - 8, Rx + 22, y - 8, INK, 2)))
    b.append(drline(L + 20, yt - 14, Rx - 22, yb - 6, 2.4, GOLD, 2.4, 0.6)
             + drline(L + 20, yb - 6, Rx - 22, yt - 14, 3.0, BLUE, 2.4, 0.6))
    b.append(fi(2.4, rect(301, y - 20, 22, 20, 'var(--bg2)', 'none', 0, 3) + t(312, y, '=', INK, 26, weight=700)))
    b.append(fi(3.7, t(312, yb + 34, '3 × 12 = 36', GOLD, 16, weight=700)))
    b.append(fi(4.1, t(312, yb + 58, '4 × 9 = 36', BLUE, 16, weight=700)))
    return fig(svg(440, yb + 70, ''.join(b), maxw=460),
               'В дробной записи крайние члены сами встают на одну диагональ, средние — на другую.', fx=True)


def c7_err():
    """7.4. На верной пропорции: диагонали дают 36 = 36, «верх с верхом» — 27 и 48."""
    need('`3 × 9 = 27`', '`4 × 12 = 48`')
    assert 3 * 9 == 27 and 4 * 12 == 48

    def panel(diag):
        out = (t(60, 50, '3', GOLD, 22, weight=700) + line(46, 58, 74, 58, INK, 2) + t(60, 84, '4', BLUE, 22, weight=700)
               + t(100, 66, '=', INK, 22) + t(140, 50, '9', BLUE, 22, weight=700) + line(124, 58, 156, 58, INK, 2)
               + t(140, 84, '12', GOLD, 22, weight=700))
        if diag:
            out += line(72, 44, 126, 78, GREEN, 2.2) + line(72, 78, 126, 44, GREEN, 2.2)
            out += rect(90, 52, 20, 18, 'var(--bg2)', 'none', 0, 3) + t(100, 66, '=', INK, 22)
            out += t(100, 118, '3 × 12 = 36', GREEN, 15, weight=700) + t(100, 140, '4 × 9 = 36', GREEN, 15, weight=700)
        else:
            out += line(72, 43, 126, 43, RED, 2.2) + line(72, 77, 124, 77, RED, 2.2)
            out += t(100, 118, '3 × 9 = 27', RED, 15, weight=700) + t(100, 140, '4 × 12 = 48', RED, 15, weight=700)
        return out + mark(186, 70, diag)
    return fig(row(svg(210, 152, panel(True), maxw=220), svg(210, 152, panel(False), maxw=220)),
               'Проверка на заведомо верной пропорции: равны только диагонали.')


# ——————————————————— Глава 8 ———————————————————

def c8_perm():
    """8.1. Записи из таблицы по местам 1–4: пара 4 и 15 (GOLD) и пара 10 и 6 (BLUE) не разлучаются; 4 : 15 = 6 : 10 — разлучает."""
    rows = [('4 : 10 = 6 : 15', True), ('4 : 6 = 10 : 15', True), ('15 : 10 = 6 : 4', True),
            ('10 : 4 = 15 : 6', True), ('4 : 15 = 6 : 10', False)]
    for r, _ in rows:
        need(f'`{r}`')
    pair = {'4': GOLD, '15': GOLD, '10': BLUE, '6': BLUE}
    xs = [110, 180, 250, 320]
    signs = [(145, ':'), (215, '='), (285, ':')]
    b = [t(40, 30, 'место', MUTED, 15, anchor='start')]
    for k, x in enumerate(xs):
        b.append(t(x, 30, str(k + 1), MUTED, 15, weight=600))
    y = 66
    for i, (r, ok) in enumerate(rows):
        a, bb, c, d = re.findall(r'\d+', r)
        q = [a, bb, c, d]
        gold_at = {j for j, v in enumerate(q) if pair[v] == GOLD}
        assert (gold_at in ({0, 3}, {1, 2})) == ok, r                 # пара по краям или в середине ⇔ пропорция верна
        assert (int(a) * int(d) == int(bb) * int(c)) == ok, r
        if not ok:
            y += 12
            b.append(line(40, y - 26, 420, y - 26, MUTED, 1, " stroke-dasharray='4 4'"))
        for v, x in zip(q, xs):
            b.append(t(x, y, v, pair[v], 22, weight=700))
        for x, sg in signs:
            b.append(t(x, y, sg, INK, 22))
        b.append(mark(380, y + 1, ok))
        y += 38
    return fig(svg(440, y - 14, ''.join(b), maxw=460),
               'Пока золотая пара стоит по краям или вместе в середине, пропорция верна; разлучили пару — неверна.')


def c8_back():
    """8.2. 2 × 18 = 4 × 9 → 2 : 4 = 9 : 18: одно произведение — по краям, другое — в середину."""
    need('`2 × 18 = 4 × 9`', '`2 : 4 = 9 : 18`')
    assert 2 * 18 == 4 * 9 and F(2, 4) == F(9, 18)
    size, ys, yf = 22, 46, 124
    src = [(40, '2', GOLD), (64, '×', INK), (92, '18', GOLD), (122, '=', INK), (150, '4', BLUE), (174, '×', INK), (198, '9', BLUE)]
    b = [''.join(t(x, ys, s, c, size, weight=700) for x, s, c in src)]
    slots = [196, 268, 340, 412]
    for x, s in ((232, ':'), (304, '='), (376, ':')):
        b.append(t(x, yf, s, INK, size))
    for x in slots:
        b.append(rect(x - 18, yf - 26, 36, 34, 'none', MUTED, 1.2, 5, " stroke-dasharray='4 3'"))
    go = {'2': (slots[0], 0.4), '18': (slots[3], 0.4), '4': (slots[1], 2.0), '9': (slots[2], 2.0)}
    for x, s, c in src:
        if s in go:
            tx, d = go[s]
            b.append(sl(d, tx - x, yf - ys, t(x, ys, s, c, size, weight=700)))
    b.append(fi(1.6, t(304, yf + 32, 'крайние — 1-е и 4-е места', GOLD, 14, weight=600)))
    b.append(fi(3.3, t(304, yf + 54, 'средние — 2-е и 3-е', BLUE, 14, weight=600)))
    return fig(svg(440, yf + 64, ''.join(b), maxw=460),
               'Числа одного произведения разъезжаются по краям, другого — в середину.', fx=True)


# ——————————————————— Глава 10 ———————————————————

def c10_arrows():
    """10.1. Прямая: × 3 и × 3; обратная: × 3 и : 3."""
    need('`y` вырос с `5` до `15`, тоже в 3 раза', '`y` упал с `60` до `20`, в 3 раза')
    assert 5 * 3 == 15 and 60 // 3 == 20

    def panel(pid, name, ys_, op, col):
        out = arrow_defs_p(pid, [BLUE, col])
        out += t(115, 18, name, MUTED, 15, weight=600)
        for (yy, lab, vals) in ((82, 'x', ('1', '3')), (126, 'y', ys_)):
            out += t(22, yy + 6, lab, INK, 17, weight=700, extra=" font-style='italic'")
            out += rect(40, yy - 18, 60, 34, 'none', MUTED, 1.2) + rect(130, yy - 18, 60, 34, 'none', MUTED, 1.2)
            out += t(70, yy + 6, vals[0], INK, 17, weight=600) + t(160, yy + 6, vals[1], INK, 17, weight=600)
        out += (f"<path d='M74,62 Q115,42 156,62' fill='none' stroke='{BLUE}' stroke-width='2' marker-end='url(#{pid}0)'/>"
                + t(115, 44, '× 3', BLUE, 15, weight=700))
        out += (f"<path d='M74,146 Q115,166 156,146' fill='none' stroke='{col}' stroke-width='2' marker-end='url(#{pid}1)'/>"
                + t(115, 176, op, col, 15, weight=700))
        return out
    a = panel('pp_c101', 'прямая', ('5', '15'), '× 3', BLUE)
    r = panel('pp_c102', 'обратная', ('60', '20'), ': 3', VIOLET)
    return fig(row(svg(210, 184, a, maxw=220), svg(210, 184, r, maxw=220)),
               'У прямой обе величины умножаются на одно число, у обратной вторая на него делится.')


def c10_fork():
    """10.2. Развилка «что постоянно?»: частное → прямая, произведение → обратная, разность/сумма → ни та ни другая."""
    need('Признак: **частное постоянно.**', 'Признак: **произведение постоянно.**', 'постоянна **разность**',
         'постоянна **сумма**', 'решать их пропорцией нельзя')
    b = [arrow_defs_p('pp_c102f', [MUTED, GREEN, RED])]
    H = 46
    ys = [10, 66, 122, 178]
    rows = [('частное', 'масса — стоимость'), ('произведение', 'рабочие — дни'),
            ('разность', 'брат и сестра'), ('сумма', 'бидон')]

    def node(x, y, w, h, lines, col):
        out = box(x, y, w, h, col, 0.12, col, 1.6, 8)
        n = len(lines)
        for i, (txt, c2, sz) in enumerate(lines):
            out += t(x + w / 2, y + h / 2 + 5 + (i - (n - 1) / 2) * 19, txt, c2, sz, weight=600 if i == 0 else None)
        return out
    rm = (ys[0] + ys[3] + H) / 2
    b.append(node(6, rm - 32, 104, 64, [('что', GOLD, 15), ('постоянно?', GOLD, 15)], GOLD))
    for y, (nm, ex) in zip(ys, rows):
        b.append(arr(110, rm, 128, y + H / 2, MUTED, 'pp_c102f0', 1.4))
        b.append(node(130, y, 152, H, [(nm, INK, 15), (ex, MUTED, 14)], MUTED))
    for y, nm in zip(ys[:2], ('прямая', 'обратная')):
        b.append(arr(282, y + H / 2, 298, y + H / 2, GREEN, 'pp_c102f1', 1.6))
        b.append(node(300, y, 132, H, [(nm, GREEN, 15)], GREEN))
    yr = ys[2]
    for y in ys[2:]:
        b.append(arr(282, y + H / 2, 298, (yr + ys[3] + H) / 2, RED, 'pp_c102f2', 1.6))
    b.append(node(300, yr, 132, ys[3] + H - yr, [('ни та', RED, 15), ('ни другая —', RED, 15), ('пропорцией', MUTED, 14),
                                                 ('нельзя', MUTED, 14)], RED))
    return fig(svg(440, ys[3] + H + 10, ''.join(b), maxw=460),
               'Пропорциональностей две — из четырёх возможных ответов на вопрос «что постоянно?».')


# ——————————————————— Глава 11 ———————————————————

def c11_flip():
    """11.1. Тетради: обе стрелки вниз; рабочие: дни читаются снизу вверх."""
    need('`6 : 10` равно отношению рублей `90 : x`, оба читаются сверху вниз',
         'Отношение рабочих `4 : 6` читается сверху вниз, а отношение дней `x : 15` — снизу вверх',
         '`4 × 15 = 6 × x`', '`4 : 6 = x : 15`')

    def panel(pid, head, a, bb, down2, prod, prop):
        out = arrow_defs_p(pid, [GREEN, BLUE])
        out += t(70, 20, head[0], MUTED, 14) + t(150, 20, head[1], MUTED, 14)
        for i, (p, q) in enumerate(zip(a, bb)):
            yy = 52 + 40 * i
            out += t(70, yy, p, INK, 20, weight=700) + t(110, yy - 6, '—', MUTED, 18) + t(150, yy, q, INK, 20, weight=700, extra=" font-style='italic'" if q == 'x' else '')
        out += arr(40, 34, 40, 92, GREEN, f'{pid}0', 2.2)
        if down2:
            out += arr(182, 34, 182, 92, GREEN, f'{pid}0', 2.2)
        else:
            out += arr(182, 92, 182, 34, BLUE, f'{pid}1', 2.4)
        if prod:
            out += t(110, 126, prod, VIOLET, 15, weight=700)
        out += t(110, 152, prop, INK, 17, weight=700)
        return out
    a = panel('pp_c111', ('тетради', 'руб.'), ('6', '10'), ('90', 'x'), True, None, '6 : 10 = 90 : x')
    r = panel('pp_c112', ('рабочие', 'дни'), ('4', '6'), ('15', 'x'), False, '4 × 15 = 6 × x', '4 : 6 = x : 15')
    return fig(row(svg(220, 164, a, maxw=230), svg(220, 164, r, maxw=230)),
               'Когда постоянно произведение, второе отношение читается снизу вверх — это и есть переворот.')


def c11_pumps():
    """11.2. 5 насосов — 12 ч; 4 насоса — 9,6 ч (✗, быстрее пяти) или 15 ч (✓)."""
    need('`5 : 4 = 12 : x` дало бы `x = 9,6` часа', '`4x = 5 × 12 = 60`, откуда `x = 15`', 'за 12 часов')
    assert F(4 * 12, 5) == D('9.6') and F(5 * 12, 4) == 15
    s, x0, h = 18, 104, 28
    b = []
    for y, nm, v, col, ok in ((24, '5 насосов', 12, MUTED, None), (74, '4 насоса', D('9.6'), RED, False),
                              (124, '4 насоса', 15, GREEN, True)):
        b.append(t(x0 - 10, y + h / 2 + 6, nm, INK, 15, anchor='end'))
        b.append(box(x0, y, float(v) * s, h, GREY if col == MUTED else col, 0.45, col, 1.5))
        b.append(t(x0 + float(v) * s - 8, y + h / 2 + 6, f'{num(v)} ч', INK, 15, anchor='end', weight=700))
        if ok is not None:
            b.append(mark(x0 + 15 * s + 24, y + h / 2 + 8, ok))
    b.append(line(x0 + 12 * s, 16, x0 + 12 * s, 112, MUTED, 1.2, " stroke-dasharray='4 4'"))
    return fig(svg(440, 166, ''.join(b), maxw=460),
               'Насосов стало меньше — время обязано вырасти; ответ короче 12 часов выдаёт неперевёрнутое отношение.')


# ——————————————————— Глава 12 ———————————————————

def c12_split():
    """12.1. 96 → 8 частей по 12 → 36 и 60."""
    need('`3 + 5 = 8`', '`96 : 8 = 12`', '`3 × 12 = 36` и `5 × 12 = 60`', '`36 + 60 = 96`')
    n = 3 + 5; part = F(96, n)
    assert part == 12 and 3 * part + 5 * part == 96
    pw, x0, y, h = 48, 24, 46, 40
    b = [bar(x0, y, n * pw, h, 1)]
    b.append(brace(x0, x0 + n * pw, y - 6, '96 конфет'))
    for i in range(1, n):
        b.append(drline(x0 + i * pw, y, x0 + i * pw, y + h, 0.4 + 0.12 * i, INK, 1.4, 0.35))
    for i in range(n):
        b.append(fi(1.6 + 0.08 * i, t(x0 + (i + 0.5) * pw, y + h / 2 + 6, '12', INK, 15, weight=700)))
    b.append(fi(2.6, bar(x0, y, 3 * pw, h, 3, filled=range(3), fill=GOLD, opacity=0.45)
                + brace(x0, x0 + 3 * pw, y + h + 6, '3 × 12 = 36', up=False, col=GOLD)))
    b.append(fi(3.4, bar(x0 + 3 * pw, y, 5 * pw, h, 5, filled=range(5), fill=BLUE, opacity=0.35)
                + brace(x0 + 3 * pw, x0 + n * pw, y + h + 6, '5 × 12 = 60', up=False, col=BLUE)))
    b.append(fi(4.2, t(x0 + n * pw / 2, y + h + 66, '36 + 60 = 96 ✓', GREEN, 16, weight=700)))
    return fig(svg(440, y + h + 78, ''.join(b), maxw=460),
               'Целое режут на сумму чисел отношения — восемь равных частей; дальше части раздаются двум кучкам.', fx=True)


def c12_err():
    """12.2. Деление на 2: 144 + 240 = 384 — вчетверо длиннее целого 96."""
    need('`3 × 48 = 144`', '`5 × 48 = 240`', '`144 + 240 = 384`')
    assert 96 // 2 == 48 and 3 * 48 + 5 * 48 == 384 == 4 * 96
    s, x0, h = 0.9375, 24, 32
    b = [t(x0, 28, 'целое — 96 конфет', GREEN, 15, anchor='start', weight=600)]
    b.append(bar(x0, 38, 96 * s, h, 8, filled=range(3), fill=GOLD, opacity=0.45)
             + box(x0 + 3 * 12 * s, 38, 5 * 12 * s, h, BLUE, 0.35, BLUE, 0) + mark(x0 + 96 * s + 18, 38 + h / 2 + 8, True))
    y = 112
    b.append(t(x0, y - 10, 'одна часть 48', RED, 15, anchor='start', weight=600))
    b.append(box(x0, y, 144 * s, h, GOLD, 0.4, GOLD, 1.4) + t(x0 + 72 * s, y + h / 2 + 6, '3 × 48 = 144', INK, 14, weight=700))
    b.append(box(x0 + 144 * s, y, 240 * s, h, BLUE, 0.3, BLUE, 1.4) + t(x0 + 264 * s, y + h / 2 + 6, '5 × 48 = 240', INK, 14, weight=700))
    b.append(rect(x0, y, 384 * s, h, 'none', RED, 2))
    b.append(brace(x0, x0 + 384 * s, y + h + 6, '384 ✗', up=False, col=RED))
    return fig(svg(440, y + h + 50, ''.join(b), maxw=460),
               'Сумма ответов обязана дать целое; здесь она вылезла вчетверо — ошибка видна сразу.')


FIGS = {
    'Процент — это сотая доля числа.': v1_one,
    'пятая часть 1/5 = 0,2 20%': v2_shares,
    'Проценты бывают больше 100': v3_over,
    'Возьмём один сюжет: в магазине': v4_double,
    'Ритуал 1 — «процент от чего?»': r1_from_what,
    'Ритуал 3 — прикидка на опорных долях': r3_estimate,
    'Ритуал 4 — целое = 100%': r4_rest,
    '0,4% = 0,4/100 = 0,004': c1_comma,
    'Шаг 3 — сборка. Нужно перевести долю в проценты': c1_class,
    'Типичная ошибка №1: написать «7%»': c1_err7,
    'Типичная ошибка №2: переводя 5% в дробь': c1_err5,
    'Было 200, стало 250. Разность 50.': c2_more,
    'Прикидка: 24% — это почти четверть': c2_route,
    'посчитать прибавку от новой цены': c2_new_price,
    'При простом росте целое не меняется ни разу': c3_simple,
    'Прибавка растёт: 1000, потом 1100, потом 1210': c4_compound,
    'Например, −20% значит × 0,8': c4_factor,
    'Для сравнения: простой рост дал бы': c4_compare,
    'считать, что +20% и −20% взаимно уничтожаются': c4_there_back,
    'во сколько раз больше? деление 12 : 4 = 3': c5_how,
    'Число, на которое сократили, — это и есть одна часть': c5_part,
    'Проверка сложением: 400 + 240 = 640': c5_mix,
    'Типичная ошибка №2: разделить 240 на 8': c5_err,
    'разделить настоящую на чертёжную, получится n': c6_plan,
    'забыть перевести единицы и написать 3 : 24 = 1 : 8': c6_err,
    'd ^ ^ ^ ^ 1 2 3 4': c7_terms,
    'Теперь испортим пропорцию': c7_bad,
    'Удобный образ: запиши пропорцию дробями': c7_cross,
    'перемножить не по диагоналям, а «верх с верхом»': c7_err,
    'А вот перестановка, которая пару разлучает': c8_perm,
    'На числах: 2 × 18 = 4 × 9': c8_back,
    'во столько же раз уменьшается другая': c10_arrows,
    'Осторожно: не всякая зависимость пропорциональна': c10_fork,
    'Вот откуда переворот: он появляется сам': c11_flip,
    'составить прямую пропорцию там, где зависимость обратная': c11_pumps,
    '36 и 60 конфет': c12_split,
    'На ошибке №1: одна часть вышла бы 96 : 2 = 48': c12_err,
}


if __name__ == '__main__':
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location('m2h', os.path.join(HERE, '..', '..', '..', 'tools', 'md2html.py'))
    m2h = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, ['x']
    spec.loader.exec_module(m2h)
    sys.argv = argv
    _, _, chapters, _ = m2h.split_chapters(MD)
    blocks = [norm(v) for c in chapters for _, v in c['blocks']]
    out = {}
    for anchor, f in FIGS.items():
        hits = [b for b in blocks if anchor in b]
        assert len(hits) == 1, f'якорь «{anchor}» встречается в {len(hits)} блоках'
        out[anchor] = f()
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(out), 'рисунков,', sum('class="fx' in v for v in out.values()), 'анимаций →', os.path.relpath(VIS))
