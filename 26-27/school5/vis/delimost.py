#!/usr/bin/env python3
"""Иллюстрации учебника «Делимость, НОД и НОК» → math5_delimost_uchebnik.vis.json (файл пишется целиком).

План рисунков: 26-27/school5/vis/plan_delimost.md. Все числа на рисунках считаются здесь
(перебор делителей, разложение, math.gcd) и сверяются assert-ами с текстом MD.
Множители-фишки нейтральные: цвет говорит о роли — общая (GOLD), в ответе (GREEN), выбыла (GREY).

Запуск: python3 26-27/school5/vis/delimost.py
"""
import json, os, re, sys
from collections import Counter
from math import gcd, prod

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import (svg, fig, t, g, rect, line, arrow_defs_p, GOLD, BLUE, GREEN, RED, VIOLET, GREY,
                    INK, MUTED, DARK, PLACE)

MD = os.path.join(HERE, '..', 'math5_delimost_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math5_delimost_uchebnik.vis.json')
PLAIN = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', open(MD).read()))


def need(*ss):
    """То, что рисунок берёт из текста, в тексте действительно написано."""
    for s in ss:
        assert s in PLAIN, f'в MD нет: {s!r}'


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def factor(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out


def is_prime(n):
    return len(divisors(n)) == 2


def lcm(a, b):
    return a * b // gcd(a, b)


def xs(nums):
    return ' × '.join(map(str, nums))


def circ(cx, cy, r, fill='none', stroke='none', sw=1.5, extra=''):
    return f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'{extra}/>"


def sl(d, dx, dy, body):
    return g('sl', d, body, f';--to:translate({dx}px,{dy}px)')


def fo(d, body, o=0):
    return g('fo', d, body, f';--o:{o}')


# ——— фишка множителя ———

R = 16


def chip(cx, cy, n, gold_at=None, green_at=None):
    b = circ(cx, cy, R, 'var(--bg)', INK, 1.6) + t(cx, cy + 6, n, INK, 16, weight=600)
    if gold_at is not None:
        b += g('fi', gold_at, circ(cx, cy, R + 1, 'none', GOLD, 3) + t(cx, cy + 6, n, GOLD, 16, weight=700))
    if green_at is not None:
        b += g('fi', green_at, circ(cx, cy, R + 3, GREEN, GREEN, 1) + t(cx, cy + 6, n, DARK, 16, weight=700))
    return b


def cell(x, y, w, h, s, fill, txt=DARK, size=22, sw=0, stroke='none'):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='6' fill='{fill}' stroke='{stroke}' "
            f"stroke-width='{sw}'/>" + t(x + w / 2, y + h / 2 + size * 0.36, s, txt, size, weight=700))


# ——— 1. Ритуал 1: 20 рядами по 4 и рядами по 3 ———

def ritual1():
    """Слева неподвижно кучка из 20 точек. Её копии укладываются рядами по 4 (без остатка),
    потом вторые копии — рядами по 3 (2 точки лишние, краснеют). Мысль: делится = раскладка без остатка."""
    import math
    need('20 делится на 4, потому что 20 : 4 = 5 ровно', '20 не делится на 3, потому что остаётся 2')
    N = 20
    assert N % 4 == 0 and N // 4 == 5 and N % 3 == 2 and N // 3 == 6
    s, r = 22, 7
    hx, hy = 64, 104
    gold = math.pi * (3 - math.sqrt(5))
    heap = [(hx + 10.5 * math.sqrt(k + 0.5) * math.cos(k * gold), hy + 10.5 * math.sqrt(k + 0.5) * math.sin(k * gold))
            for k in range(N)]
    b = [''.join(circ(x, y, r, INK) for x, y in heap), t(hx, hy + 76, N, INK, 22, weight=700)]
    y0 = 36
    for (x0, k, d0) in ((190, 4, 0.6), (452, 3, 3.8)):
        full = N // k
        d_end = d0 + (N - 1) * 0.06 + 1.3
        cx = x0 + (k - 1) * s / 2
        b.append(t(cx, y0 - 16, f'рядами по {k}', INK, 16, weight=600, cls='fi', d=d0))
        for row in range(full):
            b.append(g('fi', d_end, rect(x0 - 13, y0 + row * s - 11, (k - 1) * s + 26, 22, 'none', MUTED, 1, rx=11)))
        for i, (x, y) in enumerate(heap):
            row, col = divmod(i, k)
            tx, ty = x0 + col * s, y0 + row * s
            b.append(sl(round(d0 + i * 0.06, 2), round(tx - x, 1), round(ty - y, 1), circ(x, y, r, INK)))
            if i >= full * k:
                b.append(g('fi', d_end, circ(tx, ty, r + 0.5, RED)))
        yb = y0 + 7 * s + 26
        if k == 4:
            b.append(t(cx, yb, 'пять рядов', INK, 16, cls='fi', d=d_end))
            b.append(t(cx, yb + 24, 'без остатка — делится', GREEN, 16, weight=700, cls='fi', d=d_end + 0.2))
        else:
            b.append(t(x0 + k * s + 4, y0 + full * s + 5, f'остаётся {N % k}', RED, 16, anchor='start', weight=700,
                       cls='fi', d=d_end))
            b.append(t(cx, yb, 'шесть рядов и ещё 2', INK, 16, cls='fi', d=d_end))
            b.append(t(cx, yb + 24, 'есть остаток — не делится', RED, 16, weight=700, cls='fi', d=d_end + 0.2))
    return fig(svg(632, y0 + 7 * s + 62, ''.join(b), maxw=632), fx=True)


# ——— 2. Глава 1: лесенка прямоугольников из 24 клеток ———

PAIRS24 = [(d, 24 // d) for d in divisors(24) if d * d <= 24]


def rects24():
    """Верхний ряд 1 × 24 неподвижен; копии клеток каждого прямоугольника переезжают в следующий
    (24 клетки складываются, количество то же), каждая стадия остаётся следом. Мысль: пары = прямоугольники одной площади."""
    need('1, 2, 3, 4, 6, 8, 12, 24', '1 × 24', '2 × 12', '3 × 8', '4 × 6')
    assert PAIRS24 == [(1, 24), (2, 12), (3, 8), (4, 6)]
    assert ', '.join(map(str, divisors(24))) == '1, 2, 3, 4, 6, 8, 12, 24'
    c, x0 = 15, 78
    ys, y = [], 14
    for a, _ in PAIRS24:
        ys.append(y)
        y += a * c + 18
    H = y - 4

    def pos(stage, i):
        a, bb = PAIRS24[stage]
        return x0 + (i % bb) * c, ys[stage] + (i // bb) * c

    def sq(x, y_):
        return (f"<rect x='{x}' y='{y_}' width='{c}' height='{c}' fill='{BLUE}' fill-opacity='.45' "
                f"stroke='var(--bg2)' stroke-width='1.5'/>")

    def label(stage, d=None):
        a, bb = PAIRS24[stage]
        assert a * bb == 24
        return t(x0 - 14, ys[stage] + a * c / 2 + 6,
                 f"<tspan fill='{GOLD}' font-weight='700'>{a}</tspan> × <tspan fill='{GREEN}' "
                 f"font-weight='700'>{bb}</tspan>", INK, 16, anchor='end', cls='fi' if d else None, d=d)

    b = [''.join(sq(*pos(0, i)) for i in range(24)), label(0)]
    for stage, d in ((1, 0.6), (2, 2.4), (3, 4.2)):
        cells = ''.join(sl(d, pos(stage, i)[0] - pos(stage - 1, i)[0], pos(stage, i)[1] - pos(stage - 1, i)[1],
                           sq(*pos(stage - 1, i))) for i in range(24))
        b.append(g('fi', round(d - 0.5, 1), cells))
        b.append(label(stage, round(d + 1.2, 1)))
    chain = ' = '.join(f'{a} × {bb}' for a, bb in PAIRS24) + ' = 24'
    b.append(t(x0 + 12 * c, H + 22, chain, MUTED, 16, cls='fi', d=5.6))
    return fig(svg(x0 + 24 * c + 8, H + 34, ''.join(b), maxw=x0 + 24 * c + 8), fx=True)


# ——— 3. Глава 1: дуги к напарникам сходятся к середине ———

def arcs24():
    need('5 не подходит', 'следующая была бы 6 × 4, та же самая')
    assert 24 % 5 != 0
    S, y0 = 26, 190
    X = lambda n: 22 + (n - 1) * S
    b = [line(X(1) - 10, y0, X(24) + 10, y0, MUTED, 1.5)]
    for n in range(1, 25):
        big = 24 % n == 0
        b.append(line(X(n), y0 - (6 if big else 3), X(n), y0 + (6 if big else 3), MUTED, 1.5 if big else 1))
    for n in divisors(24):
        if n * n > 24:
            continue
        b.append(t(X(n), y0 + 24, n, INK, 14, weight=600))
    b.append(t(X(5), y0 + 24, 5, MUTED, 14))
    for n in divisors(24):
        if n * n > 24:
            b.append(t(X(n), y0 + 24, n, INK, 14, weight=600))
    for k, (a, bb) in enumerate(PAIRS24):
        d = 0.4 + k * 1.0
        h = 16 + (bb - a) * S * 0.26
        mid = (X(a) + X(bb)) / 2
        b.append(f"<path class='dr' pathLength='100' style='--d:{d}s;--dur:.8s' d='M{X(a)} {y0 - 7} Q {mid} "
                 f"{y0 - 7 - 2 * h} {X(bb)} {y0 - 7}' fill='none' stroke='{BLUE}' stroke-width='2.5'/>")
        b.append(g('fi', d - 0.2, circ(X(a), y0, 6, GOLD) + t(X(a), y0 + 24, a, GOLD, 14, weight=700)))
        b.append(g('fi', d + 0.75, circ(X(bb), y0, 6, GREEN) + t(X(bb), y0 + 24, bb, GREEN, 14, weight=700)))
    d5 = 4.4
    b.append(g('fi', d5, line(X(5) - 6, y0 - 6, X(5) + 6, y0 + 6, RED, 2.5) + line(X(5) - 6, y0 + 6, X(5) + 6, y0 - 6, RED, 2.5)))
    d6 = 5.2
    b.append(arrow_defs_p('dl3_', [INK]))
    b.append(f"<path class='dr' pathLength='100' style='--d:{d6}s;--dur:.7s' d='M{X(6)} {y0 + 36} Q {X(5)} "
             f"{y0 + 76} {X(4) + 2} {y0 + 40}' fill='none' stroke='{INK}' stroke-width='2.2' stroke-dasharray='6 4' "
             f"marker-end='url(#dl3_0)'/>")
    b.append(t(X(6) + 24, y0 + 66, '6 × 4 — та же пара 4 × 6: стоп', INK, 16, anchor='start', weight=600, cls='fi', d=d6 + 0.7))
    return fig(svg(X(24) + 24, y0 + 84, ''.join(b), maxw=640), fx=True)


# ——— 4. Глава 1: делители слева от 24, кратные справа ———

def divs_vs_mults():
    need('делители числа 24 — это 24, 48, 72…', 'Делители меньше самого числа (или равны ему), кратные — больше (или равны)')
    small = [d for d in divisors(24) if d < 24]
    mults = [24 * k for k in (2, 3)]
    assert mults == [48, 72]
    w, gap, y = 30, 4, 52
    b = []
    x = 10
    for d in small:
        b.append(cell(x, y, w, 30, d, GOLD, size=15))
        x += w + gap
    xl_end = x - gap
    xc = x + 6
    b.append(cell(xc, y - 4, 40, 38, 24, INK, DARK, 18))
    x = xc + 40 + 10
    xr0 = x
    for m in mults:
        b.append(cell(x, y, 38, 30, m, BLUE, size=15))
        x += 38 + gap
    b.append(t(x + 12, y + 21, '…', BLUE, 20, weight=700))
    xr_end = x + 24
    # скобки
    yb = y + 46
    b.append(f"<path d='M10 {yb} v8 H{xc + 40} v-8' fill='none' stroke='{GOLD}' stroke-width='2'/>")
    b.append(t((10 + xc + 40) / 2, yb + 28, 'делители 24: не больше 24', GOLD, 15, weight=700))
    b.append(f"<path d='M{xc} {y - 12} v-8 H{xr_end} v8' fill='none' stroke='{BLUE}' stroke-width='2'/>")
    b.append(t((xc + xr_end) / 2 + 20, y - 28, 'кратные 24: не меньше 24', BLUE, 15, weight=700))
    return fig(svg(max(xr_end, 300) + 70, yb + 40, ''.join(b), maxw=480))


# ——— 5. Глава 2: разрез на круглые десятки и последнюю цифру ———

PL = [PLACE['тысячи'], PLACE['сотни'], PLACE['десятки'], PLACE['единицы']]


def digits_cells(x, y, num, w=40, h=48, gap=4, dim=False, last_gold=False):
    s = str(num)
    cols = PL[-len(s):]
    out = []
    for i, ch in enumerate(s):
        fill = cols[i]
        if dim:
            fill = GREY if not (last_gold and i == len(s) - 1) else GOLD
        out.append(cell(x + i * (w + gap), y, w, h, ch, fill))
    return out


def cut_last():
    need('275 = 270 + 5', '916 = 910 + 6', '270 = 27 × 10')
    W, Hc, G = 40, 48, 4
    b = []
    for row, num in enumerate((275, 916)):
        head, last = num // 10, num % 10
        assert num == head * 10 + last
        y = 30 + row * 118
        x0, SH = 92, 88
        cells = digits_cells(x0, y, num)
        b.append(t(x0 - 12, y + 32, f'{num} =', INK, 20, anchor='end', weight=700))   # неподвижная левая часть
        left = ''.join(cells[:-1]) + g('fi', 1.2, cell(x0 + 2 * (W + G), y, W, Hc, 0, GREY, INK))
        b.append(fo(2.8, left, 0.3))
        b.append(sl(0.6, SH, 0, cells[-1] + g('fi', 3.3, rect(x0 + 2 * (W + G) - 4, y - 4, W + 8, Hc + 8, 'none', GOLD, 3, rx=9))))
        b.append(t(x0 + 3 * W + 2 * G + (SH - W - G) / 2, y + 33, '+', INK, 24, weight=700, cls='fi', d=1.2))
        b.append(t(x0 + 1.5 * W + G, y + Hc + 24, f'{head * 10} = {head} × 10', INK, 16, cls='fi', d=1.8))
        b.append(t(x0 + 2 * (W + G) + SH + W + 16, y + 32, 'решает', GOLD, 16, anchor='start', weight=700, cls='fi', d=3.5))
    b.append(t(92 + 1.5 * W + G, 30 + 2 * 118 - 4, 'круглые десятки делятся на 2, на 5 и на 10', MUTED, 16, cls='fi', d=3.0))
    return fig(svg(440, 266, ''.join(b)), fx=True)


# ——— 6. Глава 2: последняя цифра — один взгляд ———

def last_column():
    nums = [4380, 275, 916, 1002]
    need('4380', '275', '916', '1002', 'число 1002 длинное, а решение заняло один взгляд')
    W, H, G = 34, 40, 4
    xr = 130
    b = [t(xr + W / 2, 18, 'последняя цифра', GOLD, 14, weight=700)]
    for k, n in enumerate(nums):
        s = str(n)
        y = 30 + k * (H + 8)
        x = xr - (len(s) - 1) * (W + G)
        for i, cc in enumerate(digits_cells(x, y, n, W, H, G, dim=True, last_gold=True)):
            b.append(cc)
    return fig(svg(xr + W + 70, 30 + 4 * (H + 8) + 2, ''.join(b), maxw=xr + W + 70))


# ——— 7. Глава 3: от каждого 100 и 10 — хвостик 1, хвостики = сумма цифр ———

def tails852():
    """Слева неподвижно «852 =», правее — столбики, от которых отрываются хвостики (правило родителя 25.10.2026)."""
    n = 852
    a, bb, c = map(int, str(n))
    need('852 = 8 × 100 + 5 × 10 + 2', '852 = 8 × 99 + 5 × 9 + (8 + 5 + 2)', '792 + 45 + 15 = 852',
         'а оно и есть сумма цифр')
    assert n == a * 100 + bb * 10 + c
    assert n == a * 99 + bb * 9 + (a + bb + c) and a * 99 == 792 and bb * 9 == 45 and a + bb + c == 15
    assert (a * 99 + bb * 9) % 9 == 0
    VC, BC, UC = PLACE['сотни'], PLACE['десятки'], PLACE['единицы']
    bw, step, th, base, X0 = 26, 33, 13, 178, 104
    xh, xt, xu = X0, X0 + a * step + 18, X0 + a * step + 18 + bb * step + 18
    b = [t(X0 - 14, base - 48, f'{n} =', INK, 24, anchor='end', weight=700)]
    bars, tails = [], []
    xs_ = [xh + i * step for i in range(a)] + [xt + i * step for i in range(bb)] + [xu + i * step for i in range(c)]
    kinds = ['h'] * a + ['t'] * bb + ['u'] * c
    right = xu + (c - 1) * step + bw
    mid = (X0 + right) / 2
    row_x0, row_y = mid - (a + bb + c) * 30 / 2, base + 52
    for k, (x, kind) in enumerate(zip(xs_, kinds)):
        col = {'h': VC, 't': BC, 'u': UC}[kind]
        bh = {'h': 112, 't': 34, 'u': 0}[kind]
        if bh:
            bars.append(f"<rect x='{x}' y='{base - bh}' width='{bw}' height='{bh}' rx='3' fill='{col}'/>"
                        + fo(0.7, t(x + bw / 2, base - bh / 2 + 5, '100' if kind == 'h' else '10', DARK, 12, weight=700))
                        + g('fi', 1.0, t(x + bw / 2, base - bh / 2 + 5, '99' if kind == 'h' else '9', DARK, 13, weight=700)))
        ty = base - bh - th - (1 if bh else 0)
        tail = (f"<rect x='{x}' y='{ty}' width='{bw}' height='{th}' rx='2' fill='{col}' stroke='var(--bg2)' "
                f"stroke-width='1'/>" + t(x + bw / 2, ty + 10.5, 1, DARK, 10, weight=700, cls='fi' if bh else None,
                                          d=1.0 if bh else None))
        tx = row_x0 + k * 30
        if bh:
            tails.append(sl(0.7, 0, -9, sl(2.0, tx - x, row_y - ty + 9, tail)))
        else:
            tails.append(sl(2.0, tx - x, row_y - ty, tail))
    b.append(fo(3.6, ''.join(bars), 0.3))
    b += tails
    for cx, s in ((xh + (a - 1) * step / 2 + bw / 2, f'{a} × 100'), (xt + (bb - 1) * step / 2 + bw / 2, f'{bb} × 10'),
                  (xu + (c - 1) * step / 2 + bw / 2, str(c))):
        b.append(t(cx, base + 24, s, MUTED, 16))
    for x in (xt - 9, xu - 9):
        b.append(t(x, base + 24, '+', MUTED, 16))
    b.append(t(mid, 22, f'{a} × 99 + {bb} × 9 — делится и на 3, и на 9', MUTED, 16, cls='fi', d=3.8))
    b.append(t(mid, row_y + th + 28, f'{a} + {bb} + {c} = {a + bb + c} — сумма цифр', INK, 18, weight=700,
               cls='fi', d=3.2))
    W = right + 12
    return fig(svg(W, row_y + th + 40, ''.join(b), maxw=min(W, 640)), fx=True)


# ——— 8. Глава 3: всё, что делится на 9, делится и на 3 ———

def euler39():
    need('всё, что делится на 9, делится и на 3', '8 + 5 + 2 = 15', '6 + 9 + 3 = 18')
    assert 852 % 3 == 0 and 852 % 9 and 693 % 9 == 0
    b = [f"<ellipse cx='230' cy='118' rx='212' ry='102' fill='{BLUE}' fill-opacity='.08' stroke='{BLUE}' stroke-width='2'/>",
         f"<ellipse cx='300' cy='128' rx='112' ry='62' fill='var(--bg2)'/>",
         f"<ellipse cx='300' cy='128' rx='112' ry='62' fill='{GOLD}' fill-opacity='.12' stroke='{GOLD}' stroke-width='2'/>",
         t(150, 60, 'делятся на 3', BLUE, 15, weight=700),
         t(300, 98, 'делятся на 9', GOLD, 15, weight=700),
         t(108, 130, 852, INK, 22, weight=700), t(108, 152, '8 + 5 + 2 = 15', MUTED, 13),
         t(300, 136, 693, INK, 22, weight=700), t(300, 158, '6 + 9 + 3 = 18', MUTED, 13)]
    return fig(svg(460, 232, ''.join(b)))


# ——— 9. Глава 4: проверка одного числа делением на простые подряд ———

def trial_division():
    """Ровно ход абзаца: делим на 2, 3, 5, 7, … пока p × p не перевалит за число. Пример не из текста."""
    need('Пробуй делить его на простые подряд', 'Нашёлся делитель — число составное',
         'умноженное само на себя, перевалило за наше число')
    for n in (97, 91):
        assert not re.search(rf'(?<!\d){n}(?!\d)', PLAIN), f'{n} есть в тексте — нужен пример не из текста'
    primes = [p for p in range(2, 20) if is_prime(p)]

    def run(n):
        """Шаги проверки: (p, остаток) до первого делителя или до p × p > n."""
        steps = []
        for p in primes:
            if p * p > n:
                return steps, ('стоп', p)
            steps.append((p, n % p))
            if n % p == 0:
                return steps, ('делитель', p)

    s97, end97 = run(97)
    assert [p for p, _ in s97] == [2, 3, 5, 7] and all(r for _, r in s97) and end97 == ('стоп', 11)
    assert 11 * 11 == 121 > 97 and is_prime(97)
    s91, end91 = run(91)
    assert [p for p, _ in s91] == [2, 3, 5, 7] and end91 == ('делитель', 7) and 91 == 7 * 13

    CW, CH, STEP, X0, SW = 86, 74, 92, 76, 144
    b = []

    def card(x, y, p, mid, low, col, d, ring=None, cw=CW):
        body = (f"<rect x='{x}' y='{y}' width='{cw}' height='{CH}' rx='8' fill='var(--bg)' stroke='{col}' "
                f"stroke-width='{3 if ring else 1.6}'/>"
                + t(x + cw / 2, y + 26, p, col, 22, weight=700)
                + t(x + cw / 2, y + 47, mid, MUTED, 12.5)
                + t(x + cw / 2, y + 65, low, ring or MUTED, 12.5, weight=700 if ring else None))
        return g('fi', d, body)

    rows = [(97, s97, end97, 18, 0.4), (91, s91, end91, 18 + CH + 70, 4.6)]
    for n, steps, (kind, pe), y, d0 in rows:
        b.append(t(X0 - 16, y + CH / 2 + 9, n, INK, 26, anchor='end', weight=700))
        d = d0
        for k, (p, r) in enumerate(steps):
            x = X0 + k * STEP
            if r:
                b.append(card(x, y, p, f'{p} × {p} = {p * p}', f'остаток {r}', BLUE, d))
            else:
                b.append(card(x, y, p, f'{p} × {p} = {p * p}', 'делится', GOLD, d, ring=GOLD))
            d += 0.7
        if kind == 'стоп':
            x = X0 + len(steps) * STEP
            b.append(card(x, y, pe, f'{pe} × {pe} = {pe * pe}', f'{pe * pe} больше {n}: стоп', GOLD, d, ring=GOLD, cw=SW))
            b.append(t(X0, y + CH + 28, f'делителя не нашлось — {n} простое', GREEN, 16, anchor='start',
                       weight=700, cls='fi', d=d + 0.6))
        else:
            b.append(t(X0, y + CH + 28, f'{n} = {pe} × {n // pe} — составное', GREEN, 16, anchor='start',
                       weight=700, cls='fi', d=d))
    W = X0 + 4 * STEP + SW + 8
    return fig(svg(W, 18 + 2 * CH + 70 + 44, ''.join(b), maxw=W), 'пример на числах, не из текста', fx=True)


# ——— 10. Глава 4: дерево разложения 90 ———

def tree90():
    need('90 = 2 × 45', '45 = 3 × 15', '15 = 3 × 5', '90 = 2 × 3 × 3 × 5')
    steps, n = [], 90
    while not is_prime(n):
        p = factor(n)[0]
        steps.append((n, p, n // p))
        n //= p
    assert steps == [(90, 2, 45), (45, 3, 15), (15, 3, 5)]
    assert factor(90) == [2, 3, 3, 5] and prod(factor(90)) == 90
    W, H = 46, 32

    def node(cx, cy, v, d=None):
        if is_prime(v):
            body = cell(cx - W / 2, cy - H / 2, W, H, v, GREEN, DARK, 17)
        else:
            body = (f"<rect x='{cx - W / 2}' y='{cy - H / 2}' width='{W}' height='{H}' rx='6' fill='var(--bg)' "
                    f"stroke='{GOLD if v != 90 else INK}' stroke-width='2'/>"
                    + t(cx, cy + 6, v, GOLD if v != 90 else INK, 17, weight=700))
        return body if d is None else g('fi', d, body)

    b = [node(90, 30, 90)]
    cx, cy = 90, 30
    leaves = []
    for k, (v, p, q) in enumerate(steps):
        d = 0.5 + k * 1.3
        lx, rx_, ny = cx - 46, cx + 46, cy + 72
        for xx in (lx, rx_):
            b.append(f"<line class='dr' pathLength='100' style='--d:{d}s;--dur:.5s' x1='{cx}' y1='{cy + H / 2}' "
                     f"x2='{xx}' y2='{ny - H / 2}' stroke='{MUTED}' stroke-width='1.8'/>")
        b.append(node(lx, ny, p, d + 0.4))
        leaves.append((lx, ny, p, d + 0.4))
        if k == len(steps) - 1:
            b.append(node(rx_, ny, q, d + 0.4))
            leaves.append((rx_, ny, q, d + 0.4))
        else:
            b.append(node(rx_, ny, q, d + 0.4))
        cx, cy = rx_, ny
    yr = cy + 70
    rx0 = 120
    b.append(t(rx0 - 30, yr + 6, '90 =', INK, 18, anchor='end', weight=700, cls='fi', d=5.6))
    for k, (x, y, v, d) in enumerate(leaves):
        tx = rx0 + k * 68
        b.append(g('fi', d + 0.01, sl(4.3, tx - x, yr - y, cell(x - W / 2, y - H / 2, W, H, v, GREEN, DARK, 17))))
        if k:
            b.append(t(tx - 34, yr + 6, '×', INK, 18, weight=700, cls='fi', d=5.6))
    return fig(svg(400, yr + 26, ''.join(b), maxw=400), fx=True)


# ——— корзинки множителей (НОД, НОК) ———
# Анимированные сцены: слева неподвижно «НОД(72, 120) =», овалы сдвинуты вправо на OX (правило родителя 25.10.2026).

CXA, CXB, CY, RX, RY = 145, 305, 128, 135, 88
VW, OX = 450, 176                      # ширина пары овалов; сдвиг овалов вправо от неподвижной левой части


def baskets(la, lb):
    return (f"<ellipse cx='{CXA}' cy='{CY}' rx='{RX}' ry='{RY}' fill='none' stroke='{MUTED}' stroke-width='1.8'/>"
            f"<ellipse cx='{CXB}' cy='{CY}' rx='{RX}' ry='{RY}' fill='none' stroke='{MUTED}' stroke-width='1.8'/>"
            + t(CXA - 60, CY - RY - 10, la, INK, 18, weight=700) + t(CXB + 60, CY - RY - 10, lb, INK, 18, weight=700))


def own_slots(side, k):
    """Место k-й фишки в своей (не общей) части корзинки: верхний ряд из трёх, нижний из двух."""
    row, col = (0, k) if k < 3 else (1, k - 3)
    x = (40 + col * 38 + row * 18) if side == 'a' else (330 + col * 38 + row * 18)
    return x, CY - 22 + row * 48


MC = (CXA + CXB) / 2
MID = [(MC - 18, CY - 22), (MC + 18, CY - 22), (MC - 18, CY + 26), (MC + 18, CY + 26)]


def basket_scene(a, b_, mode, d_gold=0.7, d_slide=1.6):
    """mode='nod': в ответ только середина; mode='nok': в ответ всё. Возвращает (тело, общие, ответ)."""
    fa, fb = factor(a), factor(b_)
    common = sorted((Counter(fa) & Counter(fb)).elements())
    answer = common if mode == 'nod' else sorted((Counter(fa) | Counter(fb)).elements())
    d_dim, d_green = d_slide + 1.6, d_slide + 2.1
    body = [baskets(a, b_)]
    layers = {'b': [], 'a': []}
    for side, fs in (('a', fa), ('b', fb)):
        used = Counter()
        for k, v in enumerate(fs):
            x, y = own_slots(side, k)
            if used[v] < common.count(v):
                # j-я одинаковая общая фишка каждой корзинки едет в j-е место середины под это число
                slot = (MC, CY - 14) if len(common) == 1 else MID[[i for i, c in enumerate(common) if c == v][used[v]]]
                used[v] += 1
                layers[side].append(sl(d_slide, slot[0] - x, slot[1] - y,
                                       chip(x, y, v, gold_at=d_gold, green_at=d_green)))
            else:
                if mode == 'nod':
                    layers[side].append(fo(d_dim, chip(x, y, v), 0.3))
                else:
                    layers[side].append(chip(x, y, v, green_at=d_green))
    body += layers['b'] + layers['a']
    return body, common, answer


def left_static(label, h):
    """Неподвижная левая часть: то, что считаем, и знак «=»."""
    return t(OX - 12, h / 2 + 7, label, INK, 20, anchor='end', weight=700)


def nod72():
    need('НОД(72, 120)', '72 = 2 × 2 × 2 × 3 × 3', '120 = 2 × 2 × 2 × 3 × 5', 'НОД = 2 × 2 × 2 × 3 = 24')
    body, common, ans = basket_scene(72, 120, 'nod')
    assert factor(72) == [2, 2, 2, 3, 3] and factor(120) == [2, 2, 2, 3, 5]
    assert ans == [2, 2, 2, 3] and prod(ans) == gcd(72, 120) == 24
    body.append(t(MC, CY + RY + 34, f'{xs(ans)} = {prod(ans)}', GREEN, 20, weight=700, cls='fi', d=3.9))
    body.append(t(MC, CY + RY + 60, 'в НОД — только общие: пара сливается в одну', MUTED, 16, cls='fi', d=2.0))
    H = CY + RY + 72
    return fig(svg(OX + VW, H, left_static('НОД(72, 120) =', CY * 2) + f"<g transform='translate({OX},0)'>"
                   + ''.join(body) + '</g>', maxw=OX + VW), fx=True)


def coprime89():
    need('8 = 2 × 2 × 2', '9 = 3 × 3', 'НОД равен 1')
    assert factor(8) == [2, 2, 2] and factor(9) == [3, 3] and gcd(8, 9) == 1
    body = [baskets(8, 9)]
    for side, fs in (('a', factor(8)), ('b', factor(9))):
        for k, v in enumerate(fs):
            body.append(chip(*own_slots(side, k), v))
    body.append(t(MC, CY + 6, 'пусто', MUTED, 16))
    body.append(t(MC, CY + RY + 34, 'общих множителей нет: НОД(8, 9) = 1', GREEN, 18, weight=700))
    return fig(svg(VW, CY + RY + 46, ''.join(body), maxw=VW))


def nok68():
    need('НОК(6, 8)', '6 = 2 × 3', '8 = 2 × 2 × 2', 'НОК = 8 × 3 = 24')
    body, common, ans = basket_scene(6, 8, 'nok')
    assert common == [2] and ans == [2, 2, 2, 3] and prod(ans) == lcm(6, 8) == 24
    body.append(t(MC, CY + 22, 'общая 2 —', GOLD, 16, weight=700, cls='fi', d=2.8))
    body.append(t(MC, CY + 42, 'один раз', GOLD, 16, weight=700, cls='fi', d=2.8))
    body.append(t(MC, CY + RY + 34, f'{xs(ans)} = {prod(ans)}', GREEN, 20, weight=700, cls='fi', d=4.1))
    body.append(t(MC, CY + RY + 60, 'в НОК идут все множители', MUTED, 16, cls='fi', d=3.7))
    H = CY + RY + 72
    return fig(svg(OX + VW, H, left_static('НОК(6, 8) =', CY * 2) + f"<g transform='translate({OX},0)'>"
                   + ''.join(body) + '</g>', maxw=OX + VW), fx=True)


# ——— 14. Глава 6: НОК(10, 15) — общая 5 сливается ———

def nok1015():
    """Слева неподвижно «10 × 15 =» и «НОК(10, 15) =»; правее фишки. Исходная строка не исчезает:
    вниз съезжают копии фишек, две 5 сливаются в одну."""
    need('НОК(10, 15) — хочется ответить 150', '10 = 2 × 5', '15 = 3 × 5', '2 × 3 × 5 = 30')
    fa, fb = factor(10), factor(15)
    assert fa == [2, 5] and fb == [3, 5] and 10 * 15 == 150 and lcm(10, 15) == 30
    ans = sorted((Counter(fa) | Counter(fb)).elements())
    assert ans == [2, 3, 5] and prod(ans) == 30
    yt, yb, dx, X0 = 50, 170, 52, 168
    top = [(X0 + k * dx, v) for k, v in enumerate(fa + fb)]
    target = {k: (X0 + ans.index(v) * dx, yb) for k, (_, v) in enumerate(top)}
    b = [t(X0 - 30, yt + 7, '10 × 15 =', INK, 20, anchor='end', weight=700),
         t(X0 - 30, yb + 7, 'НОК(10, 15) =', INK, 20, anchor='end', weight=700)]
    for k, (x, v) in enumerate(top):
        b.append(chip(x, yt, v, gold_at=0.7 if v == 5 else None))
        if k:
            b.append(t(x - dx / 2, yt + 6, '×', INK, 18, weight=700))
    for i, lab in ((0, 10), (2, 15)):
        x1 = X0 + i * dx
        b.append(f"<path d='M{x1 - 18} {yt + 24} v6 H{x1 + dx + 18} v-6' fill='none' stroke='{MUTED}' stroke-width='1.5'/>")
        b.append(t(x1 + dx / 2, yt + 48, lab, MUTED, 16, weight=700))
    xe = X0 + 3 * dx + 30
    b.append(t(xe, yt + 7, '= 150', INK, 20, anchor='start', weight=700))
    b.append(g('fi', 1.5, line(xe - 4, yt + 10, xe + 66, yt - 12, RED, 3)))
    b.append(t(xe + 2, yt + 48, '5 взята дважды', RED, 16, anchor='start', cls='fi', d=1.5))
    for k in sorted(target, key=lambda k: top[k][1] == 5 and k == 1):
        (x, v), (tx, ty) = top[k], target[k]
        b.append(g('fi', 2.3, sl(2.4, tx - x, ty - yt, chip(x, yt, v, gold_at=0.7 if v == 5 else None, green_at=3.9))))
    for k in range(1, len(ans)):
        b.append(t(X0 + k * dx - dx / 2, yb + 6, '×', INK, 18, weight=700, cls='fi', d=3.9))
    xr = X0 + (len(ans) - 1) * dx + 30
    b.append(t(xr, yb + 7, f'= {prod(ans)}', GREEN, 20, anchor='start', weight=700, cls='fi', d=3.9))
    b.append(t(X0 - 16, yb + 48, 'общая 5 — один раз', GOLD, 16, anchor='start', cls='fi', d=4.2))
    W = xe + 130
    return fig(svg(W, yb + 60, ''.join(b), maxw=W), fx=True)


# ——— 15. Глава 6: прыжки по 6 и по 8 впервые встречаются на 24 ———

def jumps68():
    need('НОК(6, 8) = 48 — неверно', '48 действительно делится на оба, но оно не наименьшее')
    A, B, END = 6, 8, 48
    assert A * B == END and lcm(A, B) == 24 and END % A == 0 and END % B == 0
    common = [n for n in range(1, END + 1) if n % A == 0 and n % B == 0]
    assert common == [24, 48]
    S, y0, x0 = 9, 120, 24
    X = lambda n: x0 + n * S
    T = lambda n: 0.3 + n * 0.1          # момент, когда прыжок долетает до n: оба шага идут в одном темпе
    b = [line(X(0) - 6, y0, X(END) + 14, y0, MUTED, 1.5), line(X(0), y0 - 6, X(0), y0 + 6, MUTED, 1.5),
         t(X(0), y0 + 5, '', MUTED)]
    b.append(t(X(0) - 10, y0 + 5, 0, MUTED, 14, anchor='end'))
    for step, col, sign in ((A, BLUE, -1), (B, VIOLET, 1)):
        for a in range(0, END, step):
            z = a + step
            h = 24
            b.append(f"<path class='dr' pathLength='100' style='--d:{T(a):.2f}s;--dur:{step * 0.1:.1f}s' "
                     f"d='M{X(a)} {y0 + sign * 3} Q {(X(a) + X(z)) / 2} {y0 + sign * (3 + 2 * h)} {X(z)} {y0 + sign * 3}' "
                     f"fill='none' stroke='{col}' stroke-width='2.4'/>")
            b.append(line(X(z), y0 - 6, X(z), y0 + 6, MUTED, 1.5))
            ly = y0 + sign * (h + 22) + (5 if sign > 0 else 0)
            b.append(t(X(z), ly, z, col, 14, weight=700, cls='fi', d=round(T(z), 2)))
    b.append(t(X(0) + 4, y0 - 54, 'по 6', BLUE, 14, anchor='start', weight=700))
    b.append(t(X(0) + 4, y0 + 66, 'по 8', VIOLET, 14, anchor='start', weight=700))
    b.append(g('fi', round(T(24), 2), circ(X(24), y0, 9, GREEN)))
    b.append(t(X(24), 22, 'впервые вместе: НОК = 24', GREEN, 16, weight=700, cls='fi', d=round(T(24), 2)))
    b.append(g('fi', round(T(48), 2), circ(X(48), y0, 9, 'none', RED, 3)))
    b.append(t(X(48) + 8, y0 + 100, '48 = 6 × 8 — общее, но не наименьшее', RED, 15, anchor='end', cls='fi',
               d=round(T(48) + 0.2, 2)))
    return fig(svg(X(END) + 26, y0 + 112, ''.join(b), maxw=500), fx=True)


FIGS = {
    '«делится» значит без остатка': ritual1,
    'дальше пары начнут повторяться': rects24,
    'каждый делитель ходит с напарником': arcs24,
    'сказать «делители числа 24': divs_vs_mults,
    'Почему так: любое число можно разрезать': cut_last,
    'Заметь: число 1002 длинное': last_column,
    'а оно и есть сумма цифр': tails852,
    'Важная связь': euler39,
    'Как узнать про незнакомое число': trial_division,
    '45 на 2 не делится, беру 3': tree90,
    'двоек: в первом три, во втором три': nod72,
    'Взаимно простые числа': coprime89,
    'двоек: одна и три → беру три': nok68,
    'Но сперва убедись, что числа правда взаимно простые': nok1015,
    'считать НОК произведением чисел всегда': jumps68,
}

if __name__ == '__main__':
    for anchor in FIGS:
        assert PLAIN.count(anchor) == 1, f'якорь не один раз в тексте: {anchor!r}'
    out = {anchor: f() for anchor, f in FIGS.items()}
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(out), 'рисунков →', os.path.relpath(VIS))
