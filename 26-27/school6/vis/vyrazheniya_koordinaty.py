#!/usr/bin/env python3
"""Иллюстрации учебника «Буквенные выражения и координаты» (6 класс, пара 7) → math6_7_…_uchebnik.vis.json (целиком).

План рисунков и мысль каждого движения: 26-27/school6/vis/plan_vyrazheniya_koordinaty.md.
Числа на рисунках берутся из констант и таблиц MD и сверяются через assert с текстом.

Запуск: python3 26-27/school6/vis/vyrazheniya_koordinaty.py
"""
import json, math, os, re, sys

from common import (svg, fig, t, g, rect, line, path, dot, circle, ticks, dim, brace, right_angle, turn,
                    NumLine, Plane, cells, bar, arrow_defs_p,
                    GOLD, BLUE, GREEN, RED, VIOLET, CYAN, GREY, INK, MUTED, DARK, row)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
MDP = os.path.join(HERE, '..', 'math6_7_vyrazheniya_koordinaty_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math6_7_vyrazheniya_koordinaty_uchebnik.vis.json')
MD = open(MDP).read()

sys.path.insert(0, os.path.join(ROOT, 'tools'))
import md2html  # noqa: E402  — разбор MD на блоки ровно так, как его видит конвертер

BLOCKS = [(k, re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', v)).strip()) for k, v in md2html.parse(MD)]
CODE = re.findall(r'```\n(.*?)```', MD, re.S)          # ASCII-блоки по порядку


def need(*ss):
    """Строка действительно стоит в тексте MD."""
    for s in ss:
        assert s in MD, f'нет в MD: {s!r}'


def num(v):
    """Число так, как оно набрано в учебнике: минус U+2212, запятая."""
    s = (f'{v:g}' if isinstance(v, float) else str(v)).replace('.', ',')
    return s.replace('-', '−')


def pt(x, y):
    return f'({num(x)}; {num(y)})'


def table_row(head):
    """Числа строки таблицы MD, у которой первая ячейка начинается с head."""
    for ln in MD.split('\n'):
        cells_ = [c.strip().strip('`').strip() for c in ln.strip().strip('|').split('|')]
        if cells_ and cells_[0].startswith(head):
            return [float(c.replace('−', '-').replace(',', '.')) if ',' in c else int(c.replace('−', '-'))
                    for c in cells_[1:]]
    raise AssertionError(f'нет строки таблицы {head!r}')


def svg_words(s):
    """Все слова и числа из <text> рисунка (минус приведён к дефису)."""
    out = set()
    for tx in re.findall(r'<text[^>]*>(.*?)</text>', s, re.S):
        tx = re.sub(r'<[^>]+>', '', tx).replace('−', '-')
        out |= set(w for w in re.split(r'[\s,;:()]+', tx) if w)
    return out


def ascii_ok(k, s):
    """У замены ASCII все буквы и числа блока стоят на SVG."""
    toks = re.findall(r'-?\d+|[A-Za-zА-Яа-яЁё]+', CODE[k])
    miss = [w for w in toks if w not in svg_words(s)]
    assert not miss, f'ASCII-блок {k + 1}: на SVG нет {miss}'


def ascii_points(k):
    """Где в ASCII-блоке стоят буквы/звёздочки: (x, y) по меткам осей (проверка, что блок и текст не расходятся)."""
    rows = CODE[k].split('\n')
    axis = next(r for r in rows if re.search(r'\bO\b', r) and re.search(r'\d', r) and '-' * 4 not in r)
    cols = {}
    for m in re.finditer(r'-?\d+|O', axis):
        cols[m.end() - 1] = 0 if m.group() == 'O' else int(m.group())
    out = {}
    for r in rows:
        m = re.match(r'\s*(-?\d+)', r)
        if not m or r is axis:
            continue
        y = int(m.group(1))
        for mm in re.finditer(r'[A-D*]', r[m.end():]):
            c = m.end() + mm.start()
            near = min(cols, key=lambda q: abs(q - c))
            out.setdefault(mm.group(), []).append((cols[near], y))
    return out


AR = lambda i: f" marker-end='url(#{i})'"


def dr(pts, col, d, dur=1.3, sw=2.4, mid=''):
    """Линия, которая прорисовывается (класс dr) к моменту d за dur секунд."""
    dd = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return (f"<path class='dr' style='--d:{d}s;--dur:{dur}s' pathLength='100' d='{dd}' fill='none' "
            f"stroke='{col}' stroke-width='{sw}' stroke-linejoin='round' stroke-linecap='round'{mid}/>")


def sl(d, body, dx, dy):
    return g('sl', d, body, f';--to:translate({dx:.1f}px,{dy:.1f}px)')


def fi(d, body):
    return g('fi', d, body)


def ptlabel(p, xy, s, col, dx=8, dy=-8, anchor='start', size=14):
    x, y = p.P(*xy)
    return t(round(x + dx, 1), round(y + dy, 1), s, col, size, anchor=anchor, weight=600)


# ——— кирпичики буквы: одна ширина на всю пару ———
U = 22          # клетка-единица в прямоугольниках 1.3–1.4
BX = 50         # длина x (и a): не кратна клетке — общий случай
TW, TS = 11, 15  # толщина полоски-кирпичика и шаг полосок в 3.1–3.2
BXs, BYs = 46, 68  # длина полоски x и полоски y в 3.1–3.2 (y ≠ x, обе не кратны квадрату-единице TW)
assert BX % U and BXs % TW and BYs % TW and BXs != BYs


# ═══════════════════════ Часть A ═══════════════════════

def f11():
    need('`100 + (30 − 20) = 100 + 10 = 110`', '`100 + 30 − 20 = 110`')
    a, p, m = 100, 30, 20
    end = a + p - m
    assert end == 110
    W = 380
    nA, nB = NumLine(26, 350, 95, 135, 92), NumLine(26, 350, 95, 135, 226)
    labs = [a, end, a + p]
    b = [arrow_defs_p('v7_11a', [GOLD, BLUE])]
    for nl, name in ((nA, 'со скобкой'), (nB, 'без скобки')):
        b.append(nl.axis(step=5, labels=labs, size=16))
        b.append(t(14, nl.y - 62, name, MUTED, 16, anchor='start'))
        b.append(nl.point(a, None, GOLD))
    b.append(fi(0.2, nA.jump(a, end, GOLD, f'+(30 − 20)', h=22, marker='v7_11a0', size=17)))
    b.append(fi(1.4, nB.jump(a, a + p, BLUE, f'+{p}', h=66, marker='v7_11a1', size=17)))
    b.append(fi(2.6, nB.jump(a + p, end, BLUE, f'−{m}', h=14, marker='v7_11a1', size=17)))
    x = nA.x(end)
    b.append(fi(3.6, line(x, nA.y + 30, x, nB.y - 8, GREEN, 1.6, " stroke-dasharray='4 4'")
                + nA.point(end, None, GREEN) + nB.point(end, None, GREEN)))
    return fig(svg(W, 262, ''.join(b)),
               'Скобка — один прыжок; без скобки её слагаемые — два прыжка подряд, каждый со своим знаком. '
               'Конец один и тот же.', fx=True)


def f12():
    need('`100 − (50 − 20) = 100 − 30 = 70`', '`100 − 50 − 20 = 30`', '`100 − 50 + 20 = 70`')
    a, p, m = 100, 50, 20
    ok, bad = a - p + m, a - p - m
    assert (ok, bad) == (70, 30) and a - (p - m) == ok
    nA, nB = NumLine(26, 350, 25, 105, 92), NumLine(26, 350, 25, 105, 226)
    labs = [bad, a - p, ok, a]
    b = [arrow_defs_p('v7_12a', [GOLD, BLUE, RED])]
    for nl, name in ((nA, 'со скобкой'), (nB, 'без скобки')):
        b.append(nl.axis(step=5, labels=labs, size=16))
        b.append(t(14, nl.y - 62, name, MUTED, 16, anchor='start'))
        b.append(nl.point(a, None, GOLD))
    b.append(fi(0.2, nA.jump(a, ok, GOLD, '−(50 − 20)', h=22, marker='v7_12a0', size=17)))
    b.append(fi(1.4, nB.jump(a, a - p, BLUE, f'−{p}', h=66, marker='v7_12a1', size=17)))
    b.append(fi(2.6, nB.jump(a - p, bad, RED, f'−{m} ✗', h=14, marker='v7_12a2', size=17)
                + nB.point(bad, None, RED)))
    b.append(fi(3.8, nB.jump(a - p, ok, BLUE, f'+{m}', h=14, marker='v7_12a1', size=17)))
    x = nA.x(ok)
    b.append(fi(4.6, line(x, nA.y + 30, x, nB.y - 8, GREEN, 1.6, " stroke-dasharray='4 4'")
                + nA.point(ok, None, GREEN) + nB.point(ok, None, GREEN)))
    return fig(svg(380, 262, ''.join(b)),
               'После −50 второй прыжок поворачивает назад и приходит туда же, куда прыжок со скобкой. '
               'Красный прыжок — скобку просто стёрли.', fx=True)


def rect_x4(x0, y0, col_x, col_4, rows_filled=3, label_out=True):
    """Прямоугольник 3 × (x + 4): кусок x гладкий, кусок 4 — клетки. Возвращает svg."""
    h = 3 * U
    out = rect(x0, y0, BX, h, col_x, col_x, 1.8, extra=" fill-opacity='0.30'")
    fill = {(i, j): col_4 for i in range(4) for j in range(rows_filled)}
    out += f"<g fill-opacity='0.30'>{cells(x0 + BX, y0, 4, 3, U, col_4, fill)}</g>"
    out += rect(x0 + BX, y0, 4 * U, h, 'none', col_4, 1.8)
    if label_out:
        out += t(x0 + BX / 2, y0 + h + 20, 'x', INK, 16, weight=600)
        out += t(x0 + BX + 2 * U, y0 + h + 20, 4, INK, 16, weight=600)
        out += t(x0 - 10, y0 + h / 2 + 6, 3, INK, 16, anchor='end', weight=600)
    return out


def f13():
    need('`3(x + 4) = 3x + 12`', 'Три раза взять сумму — то же самое, что три раза взять каждое слагаемое')
    k, n = 3, 4
    assert k * n == 12
    y0 = 52
    b = []
    # исходник — неподвижно слева; граница слагаемых пунктиром
    xs = 30
    b.append(rect_x4(xs, y0, GOLD, BLUE))
    b.append(line(xs + BX, y0 - 6, xs + BX, y0 + 3 * U + 6, INK, 1.4, " stroke-dasharray='4 3'"))
    b.append(t(xs + (BX + 4 * U) / 2, y0 - 16, '3(x + 4)', INK, 17, weight=600))
    b.append(t(192, y0 + 3 * U / 2 + 7, '=', INK, 22))
    # копия: кусок 4 отъезжает вправо по разрезу
    xc = 240
    gap = 30
    b.append(rect(xc, y0, BX, 3 * U, GOLD, GOLD, 1.8, extra=" fill-opacity='0.30'"))
    b.append(t(xc + BX / 2, y0 + 3 * U + 20, 'x', INK, 16, weight=600))
    b.append(t(xc - 10, y0 + 3 * U / 2 + 6, 3, INK, 16, anchor='end', weight=600))
    piece = (f"<g fill-opacity='0.30'>{cells(xc + BX, y0, 4, 3, U, BLUE, {(i, j): BLUE for i in range(4) for j in range(3)})}</g>"
             + rect(xc + BX, y0, 4 * U, 3 * U, 'none', BLUE, 1.8) + t(xc + BX + 2 * U, y0 + 3 * U + 20, 4, INK, 16, weight=600))
    b.append(sl(0.5, piece, gap, 0))
    b.append(fi(1.9, t(xc + BX / 2, y0 - 16, '3x', GOLD, 18, weight=700)
                + t(xc + BX + gap + 2 * U, y0 - 16, k * n, BLUE, 18, weight=700)))
    return fig(svg(420, 160, ''.join(b)),
               'Разрез по границе слагаемых: множитель 3 — высота у обоих кусков.', fx=True)


def f14():
    need('умножить множитель только на первое слагаемое', '`3(x + 4) = 3x + 4`')
    w = 230
    ok = rect_x4(36, 46, GREEN, GREEN) + t(36 + (BX + 4 * U) / 2, 26, '3x + 12 ✓', GREEN, 17, weight=700)
    bad = rect_x4(36, 46, RED, RED, rows_filled=1) + t(36 + (BX + 4 * U) / 2, 26, '3x + 4 ✗', RED, 17, weight=700)
    # две пустые строки куска 4 — пунктиром
    bad += rect(36 + BX, 46 + U, 4 * U, 2 * U, DARK, RED, 1.6, extra=" fill-opacity='0.6' stroke-dasharray='5 4'")
    return fig(row(svg(w, 160, ok), svg(w, 160, bad)),
               'В 3x + 4 четвёрка взята один раз, а в прямоугольнике 3(x + 4) её три строки.')


def f21():
    need('`6 : 2 = 3`', 'Подставлять вместо буквы числа для этого не нужно')
    big, small = 6, 2
    k = big // small
    assert big % small == 0 and k == 3
    x0, H = 70, 28
    b = [t(x0 - 12, 44, '2a', GOLD, 17, anchor='end', weight=700),
         bar(x0, 26, small * BX, H, small, filled=range(small), fill=GOLD, labels=['a'] * small, size=15, opacity=0.8),
         t(x0 - 12, 104, '6a', INK, 17, anchor='end', weight=700),
         bar(x0, 86, big * BX, H, big, labels=['a'] * big, size=15)]
    yc = 128
    for i in range(k):
        cp = (bar(x0, yc, small * BX, H, small, filled=range(small), fill=GOLD, labels=['a'] * small, size=15,
                  opacity=0.8) + t(x0 + small * BX / 2, yc + H + 22, i + 1, GOLD, 17, weight=700))
        d0 = 0.4 + 1.5 * i
        b.append(fi(d0, sl(d0 + 0.3, cp, i * small * BX, 0) if i else cp))
    b.append(fi(0.4 + 1.5 * k + 0.4, t(x0 + big * BX / 2, 214, '6 : 2 = 3', GREEN, 18, weight=700)))
    return fig(svg(440, 228, ''.join(b)),
               'Кирпичик a может быть любой длины — 2a всё равно укладывается в 6a ровно 3 раза.', fx=True)


def strips(x0, ybase, n, length, col, thick=TW, step=TS):
    """n полосок-кирпичиков длины length, стоящих на линии ybase."""
    return ''.join(rect(x0 + i * step, ybase - length, thick, length, col, col, 1.4, extra=" fill-opacity='0.45'")
                   for i in range(n))


def f31():
    need('`7x` и `−2x` подобны', '`7x` и `7y` — нет: буквы разные', '`7x` и `7` — нет')
    rows_ = [('7x', 7, BXs, GOLD, '−2x', -2, BXs, GOLD, True),
             ('7x', 7, BXs, GOLD, '7y', 7, BYs, VIOLET, False),
             ('7x', 7, BXs, GOLD, '7', 7, TW, CYAN, False)]
    b, y = [], 84
    for l1, n1, L1, c1, l2, n2, L2, c2, good in rows_:
        b.append(strips(30, y, n1, L1, c1))
        b.append(t(30 + (n1 * TS - 4) / 2, y + 20, l1, c1, 16, weight=700))
        b.append(t(158, y - 14, 'и', MUTED, 15))
        b.append(strips(180, y, abs(n2), L2, c2))
        if n2 < 0:          # кирпичики со знаком минус: знак стоит на каждом
            b.append(''.join(t(180 + i * TS + TW / 2, y - L2 - 7, '−', RED, 22, weight=700) for i in range(-n2)))
        b.append(t(180 + (abs(n2) * TS - 4) / 2, y + 20, l2, c2, 16, weight=700))
        b.append(t(400, y - 18, '✓' if good else '✗', GREEN if good else RED, 26, weight=700))
        b.append(t(400, y + 4, 'подобны' if good else 'нет', GREEN if good else RED, 14))
        y += 104
    return fig(svg(440, y - 104 + 34, ''.join(b)),
               'Буквенная часть — это форма кирпичика. Подобные слагаемые — кирпичики одной формы; '
               'знак у них может быть разным.')


def f32():
    need('`7x + 5x = (7 + 5)x = 12x`', 'вместе двенадцать иксов')
    n1, n2 = 7, 5
    yb = 112
    gap = 22
    b = []
    left = 24
    b.append(strips(left, yb, n1, BXs, GOLD))
    b.append(t(left + n1 * TS + gap / 2 - 2, yb - BXs / 2 + 6, '+', INK, 18))
    b.append(strips(left + n1 * TS + gap, yb, n2, BXs, BLUE))
    b.append(t(left + (n1 * TS - 4) / 2, yb + 22, '7x', GOLD, 16, weight=700))
    b.append(t(left + n1 * TS + gap + (n2 * TS - 4) / 2, yb + 22, '5x', BLUE, 16, weight=700))
    wl = n1 * TS + gap + n2 * TS
    b.append(t(left + wl + 22, yb - BXs / 2 + 7, '=', INK, 22))
    xc = left + wl + 44
    b.append(strips(xc, yb, n1, BXs, GOLD))
    b.append(g('fo', 0.6, t(xc + n1 * TS + gap / 2 - 2, yb - BXs / 2 + 6, '+', INK, 18)))
    b.append(sl(0.8, strips(xc + n1 * TS + gap, yb, n2, BXs, BLUE), -gap, 0))
    b.append(fi(2.2, t(xc + ((n1 + n2) * TS - 4) / 2, yb + 22, f'{n1 + n2}x', GREEN, 18, weight=700)))
    return fig(svg(460, 150, ''.join(b)),
               'Складывается число кирпичиков, а сам кирпичик x остаётся тем же — поэтому 12x, а не 12xx.', fx=True)


def f33():
    need('8a − 3b − 5a + 7b − 2', 'Ответ = (кучка с `a`) + (кучка с `b`) + (кучка чисел)')
    terms = ['8a', '−3b', '−5a', '+7b', '−2']
    kind = lambda s: 'a' if s.endswith('a') else 'b' if s.endswith('b') else 'n'
    expr = terms[0] + ''.join(' ' + s[0] + ' ' + s[1:] for s in terms[1:])
    need(expr)
    cw, ch, gp = 58, 36, 10
    x0, y0 = (460 - (len(terms) * (cw + gp) - gp)) / 2, 18
    col = {'a': GOLD, 'b': VIOLET, 'n': CYAN}
    piles = {'a': 24, 'b': 182, 'n': 360}
    yp = 128
    name = {'a': 'кучка с a', 'b': 'кучка с b', 'n': 'кучка чисел'}
    card = lambda x, y, s, c, op: (rect(x, y, cw, ch, c, c, 1.8, rx=7, extra=f" fill-opacity='{op}'")
                                   + t(x + cw / 2, y + ch / 2 + 7, s, INK, 18, weight=700))
    b = [card(x0 + i * (cw + gp), y0, s, MUTED, 0.08) for i, s in enumerate(terms)]
    used = {'a': 0, 'b': 0, 'n': 0}
    for i, s in enumerate(terms):
        kd = kind(s)
        tx, ty = piles[kd] + used[kd] * (cw + gp), yp
        used[kd] += 1
        sx = x0 + i * (cw + gp)
        d = 0.5 + 0.6 * i
        b.append(fi(d, sl(d + 0.25, card(sx, y0, s, col[kd], 0.30), tx - sx, ty - y0)))
    assert used == {'a': 2, 'b': 2, 'n': 1}
    for kd, x in piles.items():
        wpile = used[kd] * (cw + gp) - gp
        b.append(fi(4.0, t(x + wpile / 2, yp + ch + 24, name[kd], col[kd], 15, weight=600)))
    return fig(svg(460, 196, ''.join(b)),
               'Каждое слагаемое переезжает в свою кучку вместе со своим знаком: минус не остаётся на старом месте.',
               fx=True)


# ═══════════════════════ Часть B ═══════════════════════

def pl(p, xs, ys, size=15, xname='x', yname='y', origin=True, neg_right=False, negx_above=False):
    """Сетка и подписи плоскости этой пары: подписываются только xs, ys (деления, через которые идёт линия,
    выбрасываются), кегль size; neg_right — отрицательные ординаты справа от Oy, negx_above — отрицательные
    абсциссы над Ox (туда, где пустая четверть)."""
    X0, Y0 = p.P(0, 0)
    out = p.grid(labels=False, xname='', yname='')
    for x in xs:
        up = negx_above and x < 0
        out += t(round(p.X(x), 1), round(Y0 - 8 if up else Y0 + size + 5, 1), num(x), MUTED, size)
    for y in ys:
        r = neg_right and y < 0
        out += t(round(X0 + 7 if r else X0 - 7, 1), round(p.Y(y) + size * 0.35, 1), num(y), MUTED, size,
                 anchor='start' if r else 'end')
    if origin:
        out += t(round(X0 - 7, 1), round(Y0 + size + 5, 1), 0, MUTED, size, anchor='end')
    out += t(round(p.X(p.xmax) + 14, 1), round(Y0 - 8, 1), xname, MUTED, size, anchor='end')
    out += t(round(X0 + 9, 1), round(p.Y(p.ymax) - 8, 1), yname, MUTED, size, anchor='start')
    return out


def rng(a, b, *skip):
    return [v for v in range(a, b + 1) if v and v not in skip]


def O_label(p, size=14, where='ur'):
    """Буква O у начала координат: ur — справа сверху, lr — справа снизу, ul — слева сверху."""
    x, y, a = {'ur': (7, -6, 'start'), 'lr': (6, size + 5, 'start'), 'ul': (-7, -6, 'end')}[where]
    return t(p.X(0) + x, p.Y(0) + y, 'O', MUTED, size, anchor=a, weight=600)


def gpt(p, xy, col, r=5):
    return dot(*p.P(*xy), r, col)


def fB1():
    pts = {m.group(1): (int(m.group(2).replace('−', '-')), int(m.group(3).replace('−', '-')))
           for m in re.finditer(r'`([A-D])\((−?\d+); (−?\d+)\)`', MD.split('### Мини-задача 1')[0].split('## Что такое координатная плоскость')[1])}
    assert set(pts) == set('ABCD')
    need('Здесь `A(3; 5)`, `B(5; 3)`, `C(−4; 2)`, `D(−3; −4)`.')
    ap = ascii_points(0)
    assert {k: v[0] for k, v in ap.items()} == pts, (ap, pts)
    p = Plane(-6, 6, -5, 6, cell=30)
    b = [pl(p, rng(-6, 6), rng(-5, 6), 16), O_label(p, 16)]
    for k, xy in sorted(pts.items()):
        b.append(gpt(p, xy, GOLD, 5.5) + ptlabel(p, xy, k, GOLD, 8, -8, size=17))
    s = p.svg(''.join(b))
    ascii_ok(0, s)
    return fig(s, zamena=True)


def fB2():
    need('«три вправо, пять вверх» и «пять вправо, три вверх» приводят в разные места')
    A, B = (3, 5), (5, 3)
    p = Plane(0, 6, 0, 6, cell=40)
    b = [arrow_defs_p('v7_B2a', [BLUE, VIOLET]), pl(p, rng(1, 6), rng(1, 6), 15), O_label(p, 15, where='ul')]
    for (x, y), col, idx, off in ((A, BLUE, 0, -10), (B, VIOLET, 1, -4)):
        x0, y0 = p.P(0, 0)
        x1, y1 = p.P(x, 0)
        x2, y2 = p.P(x, y)
        b.append(path([(x0, y0 + off), (x1, y1 + off), (x1, y2 + 10)], col, 2.6, closed=False,
                      extra=AR(f'v7_B2a{idx}')))
    b.append(gpt(p, A, GOLD, 6) + ptlabel(p, A, 'A(3; 5)', GOLD, 9, -8, size=16))
    b.append(gpt(p, B, GOLD, 6) + ptlabel(p, B, 'B(5; 3)', GOLD, 9, -8, size=16))
    yy = p.h + 18
    b.append(t(24, yy, 'A: 3 вправо, 5 вверх', BLUE, 15, anchor='start', weight=600))
    b.append(t(24, yy + 22, 'B: 5 вправо, 3 вверх', VIOLET, 15, anchor='start', weight=600))
    return fig(svg(p.w + 20, p.h + 50, ''.join(b)),
               'Числа одни и те же, а маршруты от O разные — и концы разные.')


def fB3():
    rows_ = {}
    for q in ('I', 'II', 'III', 'IV'):
        m = re.search(rf'^\| {q} \| [^|]+\| `([+−])` \| `([+−])` \| `\((−?\d+); (−?\d+)\)` \|', MD, re.M)
        assert m, q
        sx, sy, x, y = m.groups()
        x, y = int(x.replace('−', '-')), int(y.replace('−', '-'))
        assert (x > 0) == (sx == '+') and (y > 0) == (sy == '+')
        rows_[q] = (sx, sy, (x, y))
    need('`(0; 4)` стоит на оси `Oy`', '`(−6; 0)` — на оси `Ox`')
    p = Plane(-6, 6, -6, 6, cell=28)
    b = [arrow_defs_p('v7_B3a', [MUTED]), pl(p, rng(-6, 6), rng(-6, 6), 15), O_label(p, 15)]
    for q, (sx, sy, xy) in rows_.items():
        cx, cy = (4.5 if sx == '+' else -4.5), (2.3 if sy == '+' else -2.3)
        X, Y = p.P(cx, cy)
        b.append(t(X, Y, q, INK, 22, weight=700))
        b.append(t(X, Y + 20, f'({sx}; {sy})', MUTED, 15))
        b.append(gpt(p, xy, GOLD, 5) + ptlabel(p, xy, pt(*xy), GOLD, 0, -10 if xy[1] > 0 else 22, 'middle', 13))
    # нумерация против часовой: дуга от I до IV вокруг O
    r = 3.5 * p.c          # между подписями 3 и 4 — дуга не идёт по числам осей
    ox, oy = p.P(0, 0)
    a0, a1 = math.radians(40), math.radians(320)
    sx_, sy_ = ox + r * math.cos(a0), oy - r * math.sin(a0)
    ex, ey = ox + r * math.cos(a1), oy - r * math.sin(a1)
    b.append(f"<path d='M{sx_:.1f},{sy_:.1f} A{r:.1f},{r:.1f} 0 1 0 {ex:.1f},{ey:.1f}' fill='none' "
             f"stroke='{MUTED}' stroke-width='1.6' stroke-dasharray='5 4'{AR('v7_B3a0')}/>")
    for xy in ((0, 4), (-6, 0)):
        b.append(circle(*p.P(*xy), 5, GREY, 2, DARK))
    b.append(ptlabel(p, (0, 4), '(0; 4)', MUTED, 8, -6, size=13))
    b.append(ptlabel(p, (-6, 0), '(−6; 0)', MUTED, 0, -10, 'start', 13))
    return fig(p.svg(''.join(b)),
               'Четверти нумеруют против часовой стрелки. Точки на осях — на границе, ни в одной четверти.')


C = (-4, 2)


def f41():
    need('Для `C(−4; 2)`: четыре клетки влево, потом две вверх.')
    p = Plane(-5, 2, -1, 3, cell=44)
    x, y = C
    b = [pl(p, rng(-5, 2), rng(-1, 3), 16), O_label(p, 16)]
    o = p.P(0, 0)
    h = p.P(x, 0)
    e = p.P(x, y)
    b.append(dr([o, h], BLUE, 0.4, 1.3, 3))
    b.append(dr([h, e], BLUE, 1.9, 1.0, 3))
    b.append(fi(0.9, t((o[0] + h[0]) / 2, o[1] - 10, '4 влево', BLUE, 15, weight=600)))
    b.append(fi(2.2, t(h[0] - 10, (h[1] + e[1]) / 2 + 5, '2 вверх', BLUE, 15, anchor='end', weight=600)))
    walker = sl(1.9, sl(0.4, dot(*o, 6, BLUE), h[0] - o[0], 0), 0, e[1] - h[1])
    b.append(walker)
    b.append(fi(3.1, dot(*e, 6.5, GOLD) + ptlabel(p, C, 'C(−4; 2)', GOLD, 10, -10, size=16)))
    return fig(p.svg(''.join(b)), 'Сначала первое число — по оси Ox (минус — влево), потом второе — вверх.',
               fx=True)


def f42():
    need('это её абсцисса `−4` без знака, то есть модуль: `|−4| = 4`', 'Она стоит на `2` клетки выше оси `Ox`')
    p = Plane(-5, 2, -1, 3, cell=44)
    x, y = C
    assert abs(x) == 4 and abs(y) == 2
    e, fx_, fy_ = p.P(x, y), p.P(x, 0), p.P(0, y)
    b = [pl(p, rng(-5, 2), rng(-1, 3, y), 16), O_label(p, 16),
         t(fy_[0] + 8, fy_[1] + 6, y, VIOLET, 16, anchor='start', weight=700)]
    b.append(path([e, fx_], BLUE, 2.6, closed=False, dash='6 4') + right_angle(fx_, e, p.P(0, 0), 10, BLUE))
    b.append(path([e, fy_], VIOLET, 2.6, closed=False, dash='6 4') + right_angle(fy_, e, p.P(0, 0), 10, VIOLET))
    b.append(t(e[0] - 10, (e[1] + fx_[1]) / 2 + 6, abs(y), BLUE, 17, anchor='end', weight=700))
    b.append(t((e[0] + fy_[0]) / 2, e[1] - 12, f'|{num(x)}| = {abs(x)}', VIOLET, 16, weight=700))
    b.append(dot(*e, 6, GOLD) + t(e[0] + 4, e[1] + 22, 'C', GOLD, 16, anchor='start', weight=700))
    return fig(p.svg(''.join(b)),
               'До Ox — вертикальный отрезок, его длина — модуль ординаты; до Oy — горизонтальный, '
               'его длина — модуль абсциссы.')


def f43():
    need('| отражаем относительно оси `Ox` | ордината меняет знак | `(3; 5)` → `(3; −5)` |',
         '| отражаем относительно оси `Oy` | абсцисса меняет знак | `(3; 5)` → `(−3; 5)` |')
    P0 = (3, 5)
    imgs = [((P0[0], -P0[1]), 'Ox'), ((-P0[0], P0[1]), 'Oy')]
    p = Plane(-4, 4, -6, 6, cell=28)
    s0 = p.P(*P0)
    b = [pl(p, rng(-4, 4, P0[0]), rng(-6, 6, P0[1]), 15), O_label(p, 15)]
    for k, ((x, y), ax) in enumerate(imgs):
        e = p.P(x, y)
        foot = p.P(P0[0], 0) if ax == 'Ox' else p.P(0, P0[1])
        d = 0.5 + 1.9 * k
        b.append(path([s0, e], GREY, 1.6, closed=False, dash='5 4'))
        b.append(fi(d + 1.3, ticks(s0, foot, k + 1, GREEN) + ticks(foot, e, k + 1, GREEN)
                    + right_angle(foot, s0, p.P(0, 0) if ax == 'Ox' else p.P(0, 0), 9, MUTED)))
        b.append(fi(d, sl(d + 0.15, dot(*s0, 6, GREEN), e[0] - s0[0], e[1] - s0[1])))
        b.append(fi(d + 1.3, ptlabel(p, (x, y), pt(x, y), GREEN, 0, 22 if y < 0 else -12, 'middle', 15)))
    b.append(dot(*s0, 6.5, GOLD) + ptlabel(p, P0, pt(*P0), GOLD, 0, -12, 'middle', 15))
    return fig(p.svg(''.join(b)),
               'Копия переходит ось по перпендикуляру и встаёт на том же расстоянии с другой стороны.', fx=True)


def f44():
    need('`A(−5; 2)` и `B(3; 2)`', '`3 − (−5) = 3 + 5 = 8`', '`(−5 + 3) : 2 = −2 : 2 = −1`',
         'от `−1` до `−5` четыре шага и от `−1` до `3` тоже четыре')
    A, B = (-5, 2), (3, 2)
    L = B[0] - A[0]
    M = ((A[0] + B[0]) / 2, 2)
    assert L == 8 and M[0] == -1
    p = Plane(-6, 4, -1, 4, cell=38)
    a, bb, m, o2 = p.P(*A), p.P(*B), p.P(*M), p.P(0, 2)
    b = [pl(p, rng(-6, 4), [-1, 1, 3, 4], 17), O_label(p, 17)]
    b.append(line(*a, *bb, GOLD, 3.5))
    b.append(brace(a[0], o2[0], a[1] + 10, str(0 - A[0]), up=False, col=BLUE, size=16))
    b.append(brace(o2[0], bb[0], a[1] + 10, str(B[0] - 0), up=False, col=BLUE, size=16))
    b.append(brace(a[0], m[0], a[1] - 10, str(int(M[0] - A[0])), up=True, col=GREEN, size=16))
    b.append(brace(m[0], bb[0], a[1] - 10, str(int(B[0] - M[0])), up=True, col=GREEN, size=16))
    b.append(dot(*a, 6, GOLD) + t(a[0] - 10, a[1] + 6, 'A', GOLD, 17, anchor='end', weight=700))
    b.append(dot(*bb, 6, GOLD) + t(bb[0] + 10, bb[1] + 6, 'B', GOLD, 17, anchor='start', weight=700))
    b.append(dot(*m, 6, GREEN) + t(m[0] - 6, m[1] - 52, pt(int(M[0]), M[1]), GREEN, 16, anchor='end', weight=700))
    return fig(p.svg(''.join(b)),
               'Ось Oy делит отрезок на 5 и 3 клетки, середина — на 4 и 4.')


P5 = (3, -2)


def f51():
    need('Вышло `(3; 2)`', 'Вышло `(−3; −2)`', 'стало «три влево, два вверх»: `(−3; 2)`',
         'это та же симметрия относительно начала координат, и образ тот же: `(−3; 2)`')
    x, y = P5
    ox_, oy_, oo = (x, -y), (-x, y), (-x, -y)
    assert (ox_, oy_, oo) == ((3, 2), (-3, -2), (-3, 2))
    p = Plane(-4, 4, -4, 4, cell=40)
    s0, O = p.P(*P5), p.P(0, 0)
    b = [pl(p, rng(-4, 4, P5[0]), rng(-4, 4, P5[1]), 16), O_label(p, 16)]
    for xy, ax in ((ox_, 'Ox'), (oy_, 'Oy')):
        e = p.P(*xy)
        b.append(path([s0, e], GREY, 1.5, closed=False, dash='5 4') + dot(*e, 5.5, BLUE))
        if xy[1] > 0:       # (3; 2) лежит на дуге поворота — подпись снаружи, вверх-вправо
            b.append(ptlabel(p, xy, pt(*xy), BLUE, 8, -10, 'start', 16))
        else:
            b.append(ptlabel(p, xy, pt(*xy), BLUE, 0, 26, 'middle', 16))
    e = p.P(*oo)
    b.append(line(*s0, *e, GREEN, 1.6, " stroke-dasharray='5 4'") + ticks(s0, O, 1, GREEN) + ticks(O, e, 1, GREEN))
    r = math.hypot(s0[0] - O[0], s0[1] - O[1])
    a0 = math.atan2(s0[1] - O[1], s0[0] - O[0])
    trace = (f"<path class='dr' style='--d:0.6s;--dur:1.3s' pathLength='100' d='M{s0[0]:.1f},{s0[1]:.1f} "
             f"A{r:.1f},{r:.1f} 0 0 0 {e[0]:.1f},{e[1]:.1f}' fill='none' stroke='{GREEN}' stroke-width='1.6' "
             f"stroke-dasharray='2 5' opacity='0.8'/>")
    b.append(trace)
    b.append(turn(O, -180, line(*O, *s0, GREEN, 2.4) + dot(*s0, 6, GREEN), 0.6))
    b.append(fi(2.0, ptlabel(p, oo, pt(*oo), GREEN, -8, -10, 'end', 16)))
    b.append(dot(*s0, 6.5, GOLD) + ptlabel(p, P5, pt(*P5), GOLD, 0, 26, 'middle', 16))
    return fig(p.svg(''.join(b)),
               'Пол-оборота вокруг O приводят в конец отрезка, у которого O — середина: '
               'поворот на 180° и симметрия относительно O дают одну точку.', fx=True)


def f52():
    need('`3 + 4 = 7`', '`−2 + 5 = 3`', '`3 − 4 = −1`', '`−2 − 2 = −4`')
    x, y = P5
    T1, T2 = (x + 4, y + 5), (x - 4, y - 2)
    assert T1 == (7, 3) and T2 == (-1, -4)
    p = Plane(-2, 8, -5, 4, cell=34)
    s0 = p.P(*P5)
    b = [arrow_defs_p('v7_52a', [BLUE, VIOLET]), pl(p, rng(-2, 8, T1[0]), rng(-5, 4, y), 16), O_label(p, 16)]
    for (tx, ty), col, i in ((T1, BLUE, 0), (T2, VIOLET, 1)):
        c = p.P(tx, y)
        e = p.P(tx, ty)
        sg = 1 if ty > y else -1
        b.append(path([s0, c, (e[0], e[1] + sg * 8)], col, 2.6, closed=False, extra=AR(f'v7_52a{i}')))
        b.append(dot(*e, 6, GREEN) + ptlabel(p, (tx, ty), pt(tx, ty), GREEN, 0, -12 if ty > 0 else 24, 'middle', 15))
    b.append(t((s0[0] + p.X(T1[0])) / 2, s0[1] - 10, '4 вправо', BLUE, 15, weight=600))
    b.append(t(p.X(T1[0]) - 8, p.Y(1.5) + 5, '5 вверх', BLUE, 15, anchor='end', weight=600))
    b.append(t((s0[0] + p.X(T2[0])) / 2, s0[1] - 10, '4 влево', VIOLET, 15, weight=600))
    b.append(t(p.X(T2[0]) - 8, (s0[1] + p.Y(T2[1])) / 2 + 5, '2 вниз', VIOLET, 15, anchor='end', weight=600))
    b.append(dot(*s0, 6.5, GOLD) + ptlabel(p, P5, pt(*P5), GOLD, 0, 24, 'middle', 15))
    return fig(p.svg(''.join(b)),
               'Участок вдоль Ox меняет только абсциссу, участок вдоль Oy — только ординату.')


def f53():
    need('`M(−2; 1)`, `N(3; 1)`', '**`M₁(3; −1)`**', '**`N₁(8; −1)`**', '`MN = 3 − (−2) = 5`', '`M₁N₁ = 8 − 3 = 5`')
    M, N, sh = (-2, 1), (3, 1), (5, -2)
    M1, N1 = (M[0] + sh[0], M[1] + sh[1]), (N[0] + sh[0], N[1] + sh[1])
    assert M1 == (3, -1) and N1 == (8, -1) and N[0] - M[0] == N1[0] - M1[0] == 5
    p = Plane(-3, 8, -2, 2, cell=32, pad=30)
    m, n, m1, n1 = (p.P(*q) for q in (M, N, M1, N1))
    dx, dy = m1[0] - m[0], m1[1] - m[1]
    b = [arrow_defs_p('v7_53a', [BLUE]), pl(p, rng(-3, 8), [-2, 2], 17, origin=False), O_label(p, 17, where='lr')]
    b.append(dim(m, n, '', 16, MUTED, GOLD, 17) + t(p.X(1.5), m[1] - 24, N[0] - M[0], GOLD, 17, weight=700))
    # линии стрелок прорисовываются, наконечники появляются, когда линия дошла
    for a_, z_ in ((m, m1), (n, n1)):
        e_ = (z_[0] - 5, z_[1] - 2)
        b.append(dr([a_, e_], BLUE, 0.6, 1.3, 1.8))
        b.append(fi(1.8, line(round(e_[0] - (e_[0] - a_[0]) * 0.05, 1), round(e_[1] - (e_[1] - a_[1]) * 0.05, 1),
                              round(e_[0], 1), round(e_[1], 1), BLUE, 1.8, AR('v7_53a0'))))
    seg = line(*m, *n, GREEN, 3.5) + dot(*m, 5.5, GREEN) + dot(*n, 5.5, GREEN)
    b.append(sl(0.6, seg, dx, dy))
    b.append(fi(2.0, t(m1[0] - 6, m1[1] + 22, 'M₁', GREEN, 17, anchor='end', weight=700)
                + t(n1[0] + 10, n1[1] + 5, 'N₁', GREEN, 17, anchor='start', weight=700)
                + dim(n1, m1, '', 16, MUTED, GREEN, 17) + t(p.X(5.5), m1[1] + 36, N1[0] - M1[0], GREEN, 17, weight=700)))
    b.append(line(*m, *n, GOLD, 3.5) + dot(*m, 5.5, GOLD) + dot(*n, 5.5, GOLD))
    b.append(t(m[0] - 10, m[1] + 6, 'M', GOLD, 17, anchor='end', weight=700)
             + t(n[0] + 10, n[1] + 6, 'N', GOLD, 17, anchor='start', weight=700))
    return fig(p.svg(''.join(b)),
               'Отрезок едет целиком: стрелки у концов одинаковые, поэтому длина остаётся 5.', fx=True)


# ——— графики ———

CANDLE_T = table_row('Время `t`')
CANDLE_H = table_row('Высота `h`')


def candle_plane():
    assert CANDLE_T == [0, 2, 4, 6, 8, 10] and all(h == 20 - 2 * tt for tt, h in zip(CANDLE_T, CANDLE_H))
    p = Plane(0, 11, 0, 22, cell=32, xu=1, yu=2)
    b = [pl(p, range(1, 11), range(4, 21, 4), 16, 't, ч', 'h, см'), O_label(p, 16, where='ul')]
    first, last = p.P(CANDLE_T[0], CANDLE_H[0]), p.P(CANDLE_T[-1], CANDLE_H[-1])
    b.append(line(*first, *last, GOLD, 2.6, " stroke-dasharray='0.1 7' stroke-linecap='round'"))
    for tt, h in zip(CANDLE_T, CANDLE_H):
        x, y = p.P(tt, h)
        b.append(t(x, y + 7, '★', GOLD, 20))
    return p, b


def f61():
    need('По вертикали одна клетка — `2` см, по горизонтали одна клетка — `1` час.')
    p, b = candle_plane()
    s = p.svg(''.join(b))
    ascii_ok(1, s)
    stars = sorted(ascii_points(1)['*'])
    assert stars == [(x, y // 2 * 2) for x, y in stars]
    return fig(s, zamena=True)


def f62():
    need('**`h = 14` см**', '**`t = 5` ч**', '**`t = 10` ч**', '`20 : 2 = 10`')
    q1, q2, q3 = (3, 14), (5, 10), (10, 0)
    for tt, h in (q1, q2, q3):
        assert h == 20 - 2 * tt
    p, b = candle_plane()
    o1, g1, a1 = p.P(q1[0], 0), p.P(*q1), p.P(0, q1[1])
    b.append(dr([o1, g1, a1], BLUE, 0.4, 1.8, 2.6))
    b.append(fi(2.0, dot(*g1, 5.5, BLUE) + t(a1[0] - 7, a1[1] + 6, q1[1], BLUE, 16, anchor='end', weight=700)))
    o2, g2, a2 = p.P(0, q2[1]), p.P(*q2), p.P(q2[0], 0)
    b.append(fi(2.5, t(o2[0] - 7, o2[1] + 6, q2[1], VIOLET, 16, anchor='end', weight=700)))
    b.append(dr([o2, g2, a2], VIOLET, 2.6, 1.8, 2.6))
    b.append(fi(4.2, dot(*g2, 5.5, VIOLET)))
    e = p.P(*q3)
    b.append(fi(4.8, circle(*e, 8, GREEN, 2.4) + t(e[0], p.Y(2.6), 'догорит', GREEN, 16, weight=600)))
    return fig(p.svg(''.join(b)),
               'Читаем от известной оси до графика и поворачиваем к другой оси.', fx=True)


def lin_table():
    """Таблицы главы 7: «x | −3 …» (y = 2x) и «x | −6 …» (y = 6 : x); строка y — через строку-разделитель."""
    L = MD.split('\n')
    val = lambda ln: [int(c.strip().strip('`').replace('−', '-')) for c in ln.strip().strip('|').split('|')[1:]]
    out = []
    for i, ln in enumerate(L):
        if ln.startswith('| `x` | −'):
            assert L[i + 2].startswith('| `y` |')
            out.append(list(zip(val(ln), val(L[i + 2]))))
    assert len(out) == 2
    return out


LIN, HYP = lin_table()
assert all(y == 2 * x for x, y in LIN) and len(LIN) == 7
assert all(x * y == 6 for x, y in HYP) and len(HYP) == 8


def lin_plane(xs=None, ys=None, origin=True, O='lr'):
    p = Plane(-4, 4, -6, 6, cell=32)
    b = [pl(p, rng(-4, 4) if xs is None else xs, rng(-6, 6) if ys is None else ys, 15, origin=origin),
         O_label(p, 15, where=O)]
    return p, b


def f71():
    p, b = lin_plane()
    for xy in LIN:
        b.append(gpt(p, xy, GOLD, 5.5))
    s = p.svg(''.join(b))
    ascii_ok(2, s)
    assert sorted(ascii_points(2)['*']) == sorted(LIN)
    return fig(s, zamena=True)


def f72():
    need('у `y = −2x` при `x = 1`, `2`, `3` получается `y = −2`, `−4`, `−6`')
    neg = [(x, -2 * x) for x in (0, 1, 2, 3)]
    assert neg[1:] == [(1, -2), (2, -4), (3, -6)]
    p, b = lin_plane(rng(-4, 4, -1, 1), rng(-6, 6, -1), origin=False, O='ul')
    d = 0.3
    for (xa, ya), (xb, yb) in zip(LIN, LIN[1:]):
        st = path([p.P(xa, ya), p.P(xa, yb), p.P(xb, yb)], BLUE, 2.4, closed=False)
        if xa == LIN[0][0]:
            st += t(p.X((xa + xb) / 2), p.Y(yb) - 8, xb - xa, BLUE, 15, weight=700)
            st += t(p.X(xa) - 8, p.Y((ya + yb) / 2) + 5, yb - ya, BLUE, 15, anchor='end', weight=700)
        b.append(fi(d, st))
        d += 0.35
    for (xa, ya), (xb, yb) in zip(neg, neg[1:]):
        st = path([p.P(xa, ya), p.P(xb, ya), p.P(xb, yb)], VIOLET, 2.4, closed=False)
        if xa == 0:
            st += t(p.X(xb) + 8, p.Y((ya + yb) / 2) + 5, '2 вниз', VIOLET, 14, anchor='start', weight=700)
        b.append(fi(d, st + dot(*p.P(xb, yb), 5, VIOLET)))
        d += 0.35
    b.append(dr([p.P(*LIN[0]), p.P(*LIN[-1])], GOLD, d + 0.2, 1.4, 2.4))
    for xy in LIN:
        b.append(gpt(p, xy, GOLD, 5.5))
    b.append(fi(d + 1.4, circle(*p.P(0, 0), 9, GREEN, 2.4)))
    assert d + 1.6 <= 6
    return fig(p.svg(''.join(b)),
               'Ступени одинаковые — поэтому точки ложатся на одну прямую; при k = −2 лесенка спускается.', fx=True)


def hyp_plane():
    """Пустые четверти II и IV: туда уходят подписи — отрицательные абсциссы над Ox, отрицательные ординаты справа."""
    p = Plane(-6, 6, -6, 6, cell=27)
    return p, [pl(p, rng(-6, 6), rng(-6, 6), 16, neg_right=True, negx_above=True), O_label(p, 16, where='ur')]


def f73():
    p, b = hyp_plane()
    for xy in HYP:
        b.append(gpt(p, xy, GOLD, 5.5))
    s = p.svg(''.join(b))
    ascii_ok(3, s)
    assert sorted(ascii_points(3)['*']) == sorted(HYP)
    return fig(s, zamena=True)


def f74():
    need('при `x = 0,5` получается `y = 12`', 'одна ветвь целиком в I четверти, другая — в III')
    assert 6 / 0.5 == 12
    p, b = hyp_plane()
    n = 60
    right = [p.P(1 + 5 * i / n, 6 / (1 + 5 * i / n)) for i in range(n + 1)]
    left = [p.P(-6 + 5 * i / n, 6 / (-6 + 5 * i / n)) for i in range(n + 1)]
    b.append(arrow_defs_p('v7_74a', [GREY]))
    b.append(dr(right, GOLD, 0.3, 1.8, 2.6))
    b.append(dr(left, GOLD, 2.4, 1.8, 2.6))
    top = p.P(1, 6)
    b.append(fi(4.4, line(top[0] + 2, top[1] - 2, top[0] + 4, top[1] - 14, GREY, 1.6, AR('v7_74a0'))
                + t(top[0] + 14, top[1] + 16, 'x = 0,5: y = 12', MUTED, 16, anchor='start')))
    for xy in HYP:
        b.append(gpt(p, xy, GOLD, 5.5))
    b.append(t(p.X(4.5), p.Y(4.2), 'I', INK, 22, weight=700))
    b.append(t(p.X(-4.5), p.Y(-4.4), 'III', INK, 22, weight=700))
    return fig(p.svg(''.join(b)),
               'Две отдельные линии: перо отрывается у оси Oy. Правая ветвь уходит вверх за рамку.', fx=True)


def f75():
    xs, ys = table_row('Блокнотов'), table_row('Стоимость')
    assert all(y == 45 * x for x, y in zip(xs, ys)) and xs == [1, 2, 4, 8]
    need('**`y = 45x`**', 'в самой задаче график состоит из отдельных точек этой прямой')
    p = Plane(0, 8, 0, 360, cell=40, xu=1, yu=45)
    need('| Блокнотов `x` |', '| Стоимость `y`, руб. |')
    b = [pl(p, xs, ys, 16, 'x, блокнотов', 'y, руб.'), O_label(p, 16, where='ul')]
    b.append(line(*p.P(0, 0), *p.P(8, 360), GREY, 1.8, " stroke-dasharray='6 5'"))
    for xy in zip(xs, ys):
        b.append(gpt(p, xy, GREEN, 6.5))
    return fig(p.svg(''.join(b)),
               'Точки стоят на прямой через начало координат, но между ними пусто: полутора блокнотов не бывает.')


def f76():
    need('Прямая `y = 2x + 3` через начало координат не проходит: при `x = 0` получается `y = 3`')
    p, b = lin_plane(rng(-4, 4, -2), rng(-6, 6, 1, 2), origin=False, O='ul')
    b.append(line(*p.P(-3, -6), *p.P(3, 6), GREEN, 2.6))
    b.append(line(*p.P(-4, -5), *p.P(1.5, 6), RED, 2.6))
    b.append(dot(*p.P(0, 3), 6, RED) + ptlabel(p, (0, 3), '(0; 3)', RED, -26, 5, 'end', 14))
    b.append(circle(*p.P(0, 0), 9, GREEN, 2.4))
    b.append(t(p.X(3.2), p.Y(4.8), 'y = 2x', GREEN, 15, anchor='start', weight=700))
    b.append(t(p.X(-3.9), p.Y(5.2), 'y = 2x + 3', RED, 15, anchor='start', weight=700))
    return fig(p.svg(''.join(b)),
               'Наклон тот же, но красная прямая проходит мимо начала координат — это не прямая пропорциональность.')


# якорь → (рисунок, начало блока, где он обязан встать)
FIGS = {
    '-2 -1 O 1 2 3 4 5 6 -1 -2 -3 -4 D': (fB1, 'y 6 ^ 5 A'),
    'приводят в разные места': (fB2, 'Порядок в записи'),
    'Точки на осях не лежат ни в какой четверти': (fB3, 'Точки на осях'),
    'a + (b − c) = a + b − c': (f11, 'a + (b − c) = a + b − c'),
    'значит эти 20 остались у тебя': (f12, 'Сошлось. 50 в скобке'),
    '3(x + 4) = 3x + 12': (f13, '3(x + 4) = 3x + 12'),
    'умножить множитель только на первое слагаемое': (f14, 'Типичная ошибка №2: умножить'),
    'Подставлять вместо буквы числа для этого не нужно': (f21, 'Правило: если два'),
    'Числа без букв подобны друг другу': (f31, '- 7x и −2x подобны'),
    'вместе двенадцать иксов': (f32, 'Почему это верно'),
    'Ответ = (кучка с a) + (кучка с b) + (кучка чисел)': (f33, '✅ План готов: Ответ = (кучка'),
    'четыре клетки влево, потом две вверх': (f41, 'Для C'),
    'это её абсцисса −4 без знака': (f42, 'Расстояние от точки до оси'),
    'отражаем относительно оси Oy': (f43, 'Что делаем с точкой'),
    'тоже четыре. Посередине': (f44, 'Проверка: от −1'),
    'Поворот вокруг начала координат на 180°.': (f51, '- Отражение в оси Ox'),
    'Перенос на 4 влево и 2 вниз': (f52, '- Отражение в оси Ox'),
    'как и должно быть у переноса': (f53, 'Ответ на задачу: M₁'),
    'O 1 2 3 4 5 6 7 8 9 10': (f61, 'h, см ^ 20'),
    'вдвое короче свеча станет через 5 часов': (f62, 'Ответ на задачу: через 3'),
    '3 4 -1 -2 -3 -4 -5 -6': (f71, 'y ^ 6 5 4 3 2 1 0---'),
    'каждый шаг — на 2 вниз': (f72, 'Почему прямая'),
    '5 6 -1 -2 -3 -4 -5 -6': (f73, 'y ^ 6 5 4 3 2 1 0---'),
    'Поэтому и говорят, что у графика две ветви': (f74, 'Соедини плавной'),
    'в самой задаче график состоит из отдельных точек этой прямой': (f75, 'Уточнение про эту задачу: полутора'),
    'Прямая y = 2x + 3 через начало координат не проходит': (f76, 'Типичная ошибка №1: считать'),
}

if __name__ == '__main__':
    out = {}
    for anchor, (f, head) in FIGS.items():
        hits = [v for k, v in BLOCKS if anchor in v]
        assert hits, f'якорь «{anchor}» не найден'
        assert hits[0].startswith(head), f'якорь «{anchor}» встанет не туда: {hits[0][:60]!r}'
        out[anchor] = f()
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(out), 'рисунков,', sum('class="fx' in v for v in out.values()), 'анимаций →', os.path.relpath(VIS, ROOT))
