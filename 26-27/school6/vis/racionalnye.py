#!/usr/bin/env python3
"""Рисунки учебника «Рациональные числа» (6 класс, пара 6) → math6_6_racionalnye_uchebnik.vis.json (пишется целиком).

План рисунков и мысль каждого движения: 26-27/school6/vis/plan_racionalnye.md.
Главный образ — числовая прямая NumLine: число = точка, сложение = прыжок, модуль = длина до нуля,
«−» перед числом = отражение в нуле. Числа рисунков — из констант, сверенных assert'ами с текстом MD.

Запуск: python3 26-27/school6/vis/racionalnye.py
"""
import json, os, re
from fractions import Fraction as F

from common import (svg, fig, g, line, rect, path, dot, circle, row, ticks, arrow_defs_p,
                    GOLD, BLUE, GREEN, RED, VIOLET, CYAN, PINK, GREY, INK, MUTED)
from common import t as _t, brace as _brace, NumLine as _NumLine

# Порог координатора: на телефоне рисунок ужимается до ~300 px из 460 единиц (×0,65), подпись должна остаться ≥ 11 px —
# значит в единицах viewBox не меньше 17. Все надписи пары идут через эти обёртки.
FS = 17


def t(x, y, s, fill=MUTED, size=None, *a, **k):
    return _t(x, y, s, fill, max(size or FS, FS), *a, **k)


def brace(*a, **k):
    k['size'] = max(k.get('size', FS), FS)
    return _brace(*a, **k)


class NumLine(_NumLine):
    def axis(self, step=1, labels=None, fmt=str, **k):
        k['size'] = max(k.get('size', FS), FS)
        return super().axis(step, labels, fmt, **k)

    def point(self, v, name=None, fill=GOLD, r=5, above=True, size=FS, hollow=False):
        return super().point(v, name, fill, r, above, max(size, FS), hollow)

    def jump(self, a, b, stroke=BLUE, text=None, h=26, marker=None, size=FS, below=False):
        # подпись отодвинута от вершины дуги (просмотр: дуги касались формул)
        out = super().jump(a, b, stroke, None, h, marker, max(size, FS), below)
        if text:
            mid = (self.x(a) + self.x(b)) / 2
            out += _t(round(mid, 1), self.y + h + 28 if below else self.y - h - 11, text, stroke, max(size, FS))
        return out

HERE = os.path.dirname(os.path.abspath(__file__))
MDP = os.path.join(HERE, '..', 'math6_6_racionalnye_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math6_6_racionalnye_uchebnik.vis.json')
MD = open(MDP).read()
W = 460


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', s)).strip()


def need(*ss):
    """Строка действительно стоит в тексте MD."""
    for s in ss:
        assert s in MD, f'нет в MD: {s!r}'


def m(v):
    """Число так, как оно набрано в MD: минус — U+2212, дробь — 3/4, десятичная — запятая."""
    if isinstance(v, F) and v.denominator != 1:
        return ('−' if v < 0 else '') + f'{abs(v.numerator)}/{v.denominator}'
    if isinstance(v, float):
        return ('−' if v < 0 else '') + f'{abs(v):g}'.replace('.', ',')
    return ('−' if v < 0 else '') + str(abs(int(v)))


def code_block(sub, avoid=None):
    """Текст блока ```…```, содержащего sub."""
    blocks = re.findall(r'```\n(.*?)\n```', MD, re.S)
    hits = [b for b in blocks if sub in b and (not avoid or avoid not in b)]
    assert len(hits) == 1, sub
    return hits[0]


def ascii_tokens_on(block, s):
    """Каждое число и слово ASCII-блока стоит на SVG отдельной надписью или внутри надписи."""
    texts = re.findall(r'>([^<>]+)</text>', s)
    for tok in re.findall(r'[−\d][\d,/]*|[A-Za-zА-Яа-яё]+|\?', block):
        assert any(tok in x for x in texts), f'ASCII: «{tok}» нет на рисунке'


def labels(nl, vals, size=14, fill=MUTED, dy=24, bold=()):
    """Подписи оси только у нужных чисел (остальные деления — без подписи)."""
    out = ''
    for v in vals:
        c = INK if v == 0 else fill
        out += t(round(nl.x(v), 1), nl.y + dy, m(v), GOLD if v in bold else c, size,
                 weight=600 if v in bold else None)
    return out


def arcs(nl, a, b, col, d=None, h=26, text=None, mk=None, below=False, size=14, extra=''):
    """Прыжок-дуга; d — проявится к моменту d (у анимации)."""
    body = nl.jump(a, b, col, text, h, mk, size, below)
    if extra:
        body = body.replace("<path ", f"<path {extra} ", 1)
    return g('fi', d, body) if d is not None else body


def grey_then(d_in, d_out, coloured, greyed):
    """Проявилось цветным к d_in, к d_out цвет гаснет и остаётся серый след."""
    inner = greyed + (g('fo', d_out, coloured) if d_out is not None else coloured)
    return g('fi', d_in, inner) if d_in is not None else inner


def unit_arrow(nl, a, b, dy, col, mk):
    """Короткая стрелка-шаг от a к b над осью (ряд шагов)."""
    xa, xb = nl.x(a), nl.x(b)
    pad = 3 if xb > xa else -3
    return line(round(xa + pad, 1), nl.y + dy, round(xb - pad, 1), nl.y + dy, col, 2.4,
                f" marker-end='url(#{mk})'")


# ——————————————————————————— вводная ———————————————————————————

def v1_line():
    """В1 — замена ASCII: прямая −5…5."""
    blk = code_block('−5  −4  −3  −2  −1   0   1')
    nl = NumLine(30, 420, -5, 5, 34)
    s = svg(W, 70, nl.axis(1, range(-5, 6), m, size=15))
    ascii_tokens_on(blk, s)
    return fig(s, zamena=True)


def v2_parts():
    """В2 — три части прямой: две стороны и ноль-граница; единичный отрезок, направление."""
    need('начало отсчёта (точка `0`), направление (вправо) и единичный отрезок',
         'Ноль не положительный и не отрицательный.** Он один такой, он граница.')
    nl = NumLine(40, 410, -5, 5, 64)
    y = nl.y
    body = nl.axis(1, range(-5, 6), m, size=14)
    body += line(nl.x0 - 12, y, nl.x(0) - 5, y, PINK, 6, " stroke-opacity='0.55' stroke-linecap='round'")
    body += line(nl.x(0) + 5, y, nl.x1 + 8, y, CYAN, 6, " stroke-opacity='0.55' stroke-linecap='round'")
    body += t(nl.x(-3.2), 30, 'отрицательные', PINK, 15, weight=600)
    body += t(nl.x(3.2), 30, 'положительные', CYAN, 15, weight=600)
    body += dot(nl.x(0), y, 6, GOLD) + t(nl.x(0), 30, 'граница', GOLD, 15, weight=600)
    body += brace(nl.x(0), nl.x(1), y + 34, None, up=False, col=GOLD)
    body += t(nl.x(0) - 6, y + 58, 'единичный отрезок', GOLD, 14, anchor='end')
    body += t(nl.x1 + 16, y + 58, 'направление →', MUTED, 14, anchor='end')
    return fig(svg(W, 140, body),
               'Ноль — отдельная точка между двумя лучами: он не входит ни в левый, ни в правый.')


def v3_halves():
    """В3 — −1/2 и −3,5 стоят посередине своих единичных отрезков."""
    need('`−1/2` стоит посередине между `−1` и `0`, а `−3,5` — посередине между `−4` и `−3`')
    nl = NumLine(30, 420, -5, 1, 58)
    y = nl.y
    body = nl.axis(1, range(-5, 2), m, size=14)
    for a, v in ((-4, -3.5), (-1, -0.5)):
        mid = a + 0.5
        body += brace(nl.x(a) + 2, nl.x(mid) - 2, y - 10, '½', up=True, col=GOLD)
        body += brace(nl.x(mid) + 2, nl.x(a + 1) - 2, y - 10, '½', up=True, col=GOLD)
        body += nl.point(v, None, GOLD, 6) + t(nl.x(v), y + 46, m(F(-1, 2)) if v == -0.5 else m(v), GOLD, 17, weight=600)
    return fig(svg(W, 120, body), 'Посередине — значит две одинаковые половинки единичного отрезка.')


def v4_thermo():
    """В4 — градус вниз на термометре = шаг влево на прямой (анимация)."""
    temps = [3, 2, 1, 0, -1, -2, -3]
    need('`3°, 2°, 1°, 0°, −1°, −2°, −3°`', '`3 > 2 > 1 > 0 > −1 > −2 > −3`')
    top, gap, tx = 26, 26, 46

    def ty(v):
        return top + (3 - v) * gap

    mk = 'r6v4a'
    body = arrow_defs_p(mk, [BLUE])
    bulb = ty(-3) + 22
    body += rect(tx - 8, top - 10, 16, bulb - top + 4, 'none', MUTED, 1.5, 8)
    body += circle(tx, bulb, 12, MUTED, 1.5, GOLD, extra=" fill-opacity='0.75'")
    body += rect(tx - 4, ty(-3), 8, bulb - ty(-3), GOLD, 'none', 0, extra=" fill-opacity='0.75'")
    for v in temps:
        body += line(tx + 8, ty(v), tx + 14, ty(v), MUTED, 1.4)
        body += t(tx + 20, ty(v) + 5, f'{m(v)}°', INK if v == 0 else MUTED, 14, anchor='start')
    nl = NumLine(150, 425, -3, 3, 120)
    body += nl.axis(1, temps, m, size=14)
    for k, v in enumerate(temps[:-1]):
        d = 0.5 + 0.8 * k
        body += g('fo', d, rect(tx - 4, ty(v), 8, gap, GOLD, 'none', 0, extra=" fill-opacity='0.75'"))
        body += arcs(nl, v, v - 1, BLUE, d, 16, mk=f'{mk}0')
    for k, v in enumerate(temps):
        d_in = 0.5 + 0.8 * (k - 1) + 0.3 if k else None
        d_out = 0.5 + 0.8 * k if k < len(temps) - 1 else None
        p = dot(nl.x(v), nl.y, 6, GOLD)
        p = g('fo', d_out, p) if d_out is not None else p
        body += g('fi', d_in, p) if d_in is not None else p
    return fig(svg(W, 228, body), 'Столбик опускается на градус — точка делает шаг влево; через ноль ход тот же.', fx=True)


def v5_far():
    """В5 — −100 дальше от нуля, чем −1, но левее, то есть меньше (ось с разрывом)."""
    need('Число `−100` дальше от нуля, чем `−1`, но оно **меньше**')
    y = 70
    nl = NumLine(170, 410, -2, 1, y)
    x100 = 50
    body = line(x100 - 14, y, 92, y, MUTED, 1.8)
    body += path([(92, y), (98, y - 7), (106, y + 7), (112, y)], MUTED, 1.8, closed=False)
    body += line(112, y, nl.x1 + 12, y, MUTED, 1.8)
    body += path([(nl.x1 + 6, y - 6), (nl.x1 + 14, y), (nl.x1 + 6, y + 6)], MUTED, 1.8, closed=False)
    for v in (-2, -1, 0, 1):
        body += line(nl.x(v), y - 6, nl.x(v), y + 6, MUTED, 1.4)
    body += line(x100, y - 6, x100, y + 6, MUTED, 1.4)
    body += t(x100, y + 24, '−100', GOLD, 14, weight=600) + labels(nl, (-1, 0, 1), bold=(-1,))
    body += dot(x100, y, 6, GOLD) + dot(nl.x(-1), y, 6, GOLD)
    body += t(x100, y - 18, 'меньше', GOLD, 14)
    body += t(nl.x(-1), y - 18, 'больше', GOLD, 14)
    body += brace(nl.x(-1), nl.x(0), y + 34, '1', up=False, col=VIOLET)
    body += brace(x100, nl.x(0), y + 70, '100 — до нуля дальше', up=False, col=VIOLET)
    return fig(svg(W, 175, body), 'Длина скобки — как далеко от нуля; «больше» решает только то, кто правее.')


def v6_warmer():
    """В6 — замена ASCII мини-задачи 1: от −6 четыре шага вправо (анимация)."""
    blk = code_block('●──→───→───→───→●')
    start, n = -6, 4
    need('`−6 → −5 → −4 → −3 → −2`')
    mk = 'r6v6a'
    nl = NumLine(40, 410, -7, 0, 70)
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(1, range(-7, 1), m, size=15)
    body += nl.point(start, None, GOLD, 6)
    for k in range(n):
        body += arcs(nl, start + k, start + k + 1, BLUE, 0.4 + 0.7 * k, 18, mk=f'{mk}0')
    body += g('fi', 0.4 + 0.7 * n, nl.point(start + n, None, GREEN, 6))
    s = svg(W, 104, body)
    ascii_tokens_on(blk, s)
    return fig(s, 'Каждая дуга — один градус потепления, то есть один шаг вправо.', fx=True, zamena=True)


def v7_lift():
    """В7 — лифт: 5 шагов от −3 до 2, ноль режет путь на 3 + 2."""
    start, n = -3, 5
    need('Он поднялся на 5 этажей', 'первые 3 подняли его от `−3` до `0`', 'оставшиеся 2 — от `0` до `2`')
    end = start + n
    mk = 'r6v7a'
    nl = NumLine(40, 410, -4, 3, 74)
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(1, range(-4, 4), m, size=14)
    for v in range(start, end):
        body += arcs(nl, v, v + 1, BLUE, None, 16, mk=f'{mk}0')
    body += nl.point(start, None, GOLD, 6) + nl.point(end, None, GREEN, 6)
    body += circle(nl.x(0), nl.y, 9, GOLD, 2) + t(nl.x(0), 26, 'этаж 0 — тоже этаж', GOLD, 14, weight=600)
    body += brace(nl.x(start), nl.x(0), nl.y + 34, f'{-start} под землёй', up=False, col=VIOLET)
    body += brace(nl.x(0), nl.x(end), nl.y + 34, f'{end} над землёй', up=False, col=VIOLET)
    body += brace(nl.x(start), nl.x(end), nl.y + 76, f'всего {n}', up=False, col=BLUE)
    return fig(svg(W, 190, body), 'Ноль — одна из отметок пути: на нём путь делится на шаги под землёй и над землёй.')


# ——————————————————————————— ритуалы ———————————————————————————

def r1_sign_modulus():
    """Р1 — у −7 два признака: сторона (знак) и расстояние (модуль)."""
    need('`−7` это «слева, на расстоянии 7»')
    v = -7
    nl = NumLine(30, 420, -8, 1, 64)
    body = nl.axis(1, range(-8, 2), m, size=14) + nl.point(v, None, GOLD, 6)
    body += t(nl.x(v) - 6, 30, 'знак «−»: слева от нуля', GOLD, 15, anchor='start', weight=600)
    body += brace(nl.x(v), nl.x(0), nl.y + 34, f'модуль {-v}: как далеко', up=False, col=VIOLET)
    return fig(svg(W, 130, body), 'Знак и модуль — два отдельных вопроса: с какой стороны и как далеко.')


def r2_same_path():
    """Р2 — 7 − 3 и 7 + (−3): один и тот же путь."""
    need('`7 − 3` это то же самое, что `7 + (−3)`: и то и другое — три шага влево от `7`')
    a, b = 7, 3
    mk = 'r6r2a'
    nl = NumLine(30, 410, 0, 8, 76)
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(1, range(0, 9), m, size=14)
    for k in range(b):
        body += arcs(nl, a - k, a - k - 1, BLUE, None, 16, mk=f'{mk}0')
    body += nl.point(a, None, GOLD, 6) + nl.point(a - b, None, GREEN, 6)
    body += t(nl.x(a - b / 2), 34, '7 − 3', BLUE, 16, weight=600)
    body += brace(nl.x(a - b), nl.x(a), nl.y + 34, None, up=False, col=BLUE)
    body += t(nl.x(a - b / 2), nl.y + 70, '7 + (−3)', BLUE, 16, weight=600)
    return fig(svg(W, 156, body), 'Две записи подписывают одну и ту же дорогу.')


# ——————————————————————————— глава 1 ———————————————————————————

def c1_coord():
    """1.1 — A(−4): буква — имя точки, число под ней — координата."""
    need('пишут `A(−4)`')
    nl = NumLine(30, 330, -5, 1, 60)
    body = nl.axis(1, [v for v in range(-5, 2) if v != -4], m, size=14)
    body += labels(nl, (-4,), size=15, bold=(-4,))
    body += nl.point(-4, 'A', GOLD, 6, size=16)
    body += t(400, nl.y + 6, 'A(−4)', GOLD, 20, weight=600)
    return fig(svg(W, 96, body), 'Над точкой — её имя, под ней — её координата; запись A(−4) называет и то и другое.')


def c1_submarine():
    """1.2 — подлодка: −30, всплыла на 12 → −18, опустилась на 25 → −43 (анимация)."""
    s0, up, down = -30, 12, 25
    s1, s2 = s0 + up, s0 + up - down
    need('**старт = `−30`**', 'осталось `30 − 12 = 18`', 'стало `18 + 25 = 43`', 'Это `−43`')
    assert (s1, s2) == (-18, -43)
    mk = 'r6c1b'
    nl = NumLine(25, 415, -45, 0, 100)
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(5, None, size=14) + labels(nl, (s0, 0))
    body += g('fi', 1.0, labels(nl, (s1,))) + g('fi', 2.9, labels(nl, (s2,)))
    body += nl.point(s0, None, GOLD, 6)
    body += arcs(nl, s0, s1, BLUE, 0.5, 18, None, f'{mk}0')
    body += g('fi', 0.5, t(nl.x(s1) + 10, nl.y - 12, f'всплыла {up}', BLUE, 14, anchor='start'))
    body += g('fi', 1.0, nl.point(s1, None, BLUE, 6))
    body += arcs(nl, s1, s2, BLUE, 2.4, 60, f'опустилась {down}', f'{mk}0')
    body += g('fi', 2.9, nl.point(s2, None, GREEN, 6))
    rows = [(s0, None, 1.0), (s1, 1.0, 2.9), (s2, 2.9, None)]
    for k, (v, d_in, d_out) in enumerate(rows):
        yy = nl.y + 34 + 42 * k
        col = brace(nl.x(v), nl.x(0), yy, f'до нуля {-v}', up=False, col=VIOLET)
        grey = brace(nl.x(v), nl.x(0), yy, f'до нуля {-v}', up=False, col=GREY)
        body += grey_then(d_in, d_out, col, grey)
    return fig(svg(W, 262, body),
               'Шаг к нулю укорачивает расстояние до нуля, шаг от нуля его удлиняет.', fx=True)


# ——————————————————————————— глава 2 ———————————————————————————

def c2_opposite():
    """2.1 — пример и контрпример противоположных: 5 и −5 против 5 и −3."""
    need('`5` и `−5`', 'А вот `5` и `−3` не противоположные')

    def panel(a, ok):
        col = GREEN if ok else RED
        nl = NumLine(16, 196, -6, 6, 58)
        body = nl.axis(1, None, size=14) + labels(nl, (a, 0, 5))
        body += nl.point(a, None, col, 6) + nl.point(5, None, col, 6)
        body += brace(nl.x(a), nl.x(0), nl.y + 34, str(-a), up=False, col=VIOLET)
        body += brace(nl.x(0), nl.x(5), nl.y + 34, '5', up=False, col=VIOLET)
        head = f'{m(a)} и 5 — противоположные' if ok else f'{m(a)} и 5 — нет ✗'
        body += t(106, 22, head, col, 15, weight=600)
        return svg(220, 128, body, maxw=220)

    return fig(row(panel(-5, True), panel(-3, False)),
               'Стороны разные в обоих случаях; противоположными числа делает равная длина до нуля.')


def c2_mirror():
    """2.2 — минус = отражение в нуле; два отражения возвращают 7 на место (анимация)."""
    v = 7
    need('противоположное к `−7` — это `7`', '`−(−7) = 7`', 'два зеркала подряд возвращают число на место')
    mk = 'r6c2b'
    nl = NumLine(30, 410, -8, 8, 96)
    y = nl.y
    body = arrow_defs_p(mk, [BLUE, GREEN]) + nl.axis(1, None, size=14) + labels(nl, (-v, 0, v))
    body += line(nl.x(0), y - 70, nl.x(0), y + 8, GOLD, 1.5, " stroke-dasharray='5 4'")
    body += line(nl.x(0), y + 32, nl.x(0), y + 70, GOLD, 1.5, " stroke-dasharray='5 4'")
    body += t(nl.x(0) + 6, 18, 'зеркало', GOLD, 14, anchor='start')
    body += nl.point(v, None, GOLD, 6)
    body += arcs(nl, v, -v, BLUE, 0.4, 44, None, f'{mk}0')
    body += g('fi', 0.4, t(nl.x(-4.6), y - 52, m(-v), BLUE, 16, weight=600))
    body += g('fi', 1.0, nl.point(-v, None, BLUE, 6))
    body += arcs(nl, -v, v, GREEN, 2.0, 40, None, f'{mk}1', below=True)
    body += g('fi', 2.0, t(nl.x(4.4), y + 62, f'−({m(-v)})', GREEN, 16, weight=600))
    body += g('fi', 2.6, circle(nl.x(v), y, 10, GREEN, 2.2))
    return fig(svg(W, 196, body), 'Минус перед числом переносит его через ноль на ту же длину; второй минус переносит обратно.',
               fx=True)


def c2_four():
    """2.3 — |x| = 4: от нуля в обе стороны по 4 — ровно два места (анимация)."""
    r = 4
    need('Отмеряю 4 единичных отрезка вправо от нуля — попадаю в `4`. Отмеряю 4 влево — попадаю в `−4`.')
    nl = NumLine(30, 410, -5, 5, 64)
    body = nl.axis(1, range(-5, 6), m, size=14) + nl.point(0, None, GOLD, 6)
    grow = " class='dr' pathLength='100' style='--d:0.4s;--dur:1.6s'"
    for e in (r, -r):
        body += nl.seg(0, e, VIOLET, 6, extra=grow + " stroke-opacity='0.8'")
        body += g('fi', 2.0, nl.point(e, None, GREEN, 6) +
                  brace(nl.x(min(0, e)), nl.x(max(0, e)), nl.y + 34, str(r), up=False, col=VIOLET))
    return fig(svg(W, 120, body), 'От нуля можно отмерить 4 только вправо или влево, так что место ровно два.', fx=True)


# ——————————————————————————— глава 3 ———————————————————————————

def c3_key():
    blk = code_block('  −7  −6  −5  −4  −3  −2  −1   0\n───┼───┼───┼───┼───┼───┼───┼───┼───→', avoid='●')
    return '=' + norm(blk), blk


def c3_line():
    """3.1 — замена ASCII главы 3: прямая −7…0, идём слева направо."""
    _, blk = c3_key()
    need('Идём по прямой слева направо и выписываем числа')
    mk = 'r6c3a'
    nl = NumLine(40, 410, -7, 0, 74)
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(1, range(-7, 1), m, size=15)
    body += line(nl.x(-7), 40, nl.x(0), 40, BLUE, 2, f" marker-end='url(#{mk}0)'")
    body += t(nl.x(-3.5), 28, 'идём слева направо', BLUE, 14)
    s = svg(W, 108, body)
    ascii_tokens_on(blk, s)
    return fig(s, zamena=True)


def c3_v():
    """3.2 — модули: слева от нуля убывают, справа растут (столбики-«галочка»)."""
    need('`7, 6, 5, 4, 3, 2, 1, 0`', 'в ряду `1 < 2 < 3` модули растут вместе с числами')
    vals = range(-7, 4)
    nl = NumLine(30, 410, -7, 3, 26)
    body = nl.axis(1, vals, m, size=14)
    top, k = nl.y + 34, 13
    for v in vals:
        h = abs(v) * k
        body += rect(round(nl.x(v) - 8, 1), top, 16, h, VIOLET, 'none', 0, 2, " fill-opacity='0.6'")
        body += t(nl.x(v), top + h + 18, str(abs(v)), VIOLET, 14, weight=600)
    return fig(svg(W, top + 7 * k + 30, body),
               'Под каждым числом — его модуль: слева от нуля столбики укорачиваются, справа удлиняются.')


def c3_order():
    """3.3 — шесть чисел падают на свои места; слева направо — ответ (анимация)."""
    src = [(-2, '−2'), (F(3, 4), '3/4'), (F(-5, 2), '−5/2'), (0, '0'), (-0.3, '−0,3'), (1, '1')]
    need('*Расположи в порядке возрастания: `−2`, `3/4`, `−5/2`, `0`, `−0,3`, `1`.*',
         '`−5/2 < −2 < −0,3 < 0 < 3/4 < 1`')
    assert [s for _, s in sorted(src, key=lambda p: float(p[0]))] == ['−5/2', '−2', '−0,3', '0', '3/4', '1']
    nl = NumLine(40, 410, -3, 1.5, 170)
    body = nl.axis(0.5, None, size=14) + labels(nl, (-3, -2, -1, 0, 1), dy=26)
    high = {'−0,3', '1'}
    for k, (v, s) in enumerate(src):
        x0, y0 = 50 + 72 * k, 30
        col = GOLD if v == 0 else (PINK if v < 0 else CYAN)
        body += t(x0, y0, s, INK, 16, weight=600)
        ty = nl.y - (40 if s in high else 16)
        d = 0.4 + 0.75 * k
        body += g('sl', d, t(x0, y0, s, col, 16, weight=600),
                  f';--to:translate({nl.x(float(v)) - x0:.1f}px,{ty - y0:.1f}px)')
        body += g('fi', d + 1.1, dot(nl.x(float(v)), nl.y, 6, col))
        if s in high:
            body += g('fi', d + 1.1, line(nl.x(float(v)), nl.y - 34, nl.x(float(v)), nl.y - 8, col, 1))
    body += line(20, 48, W - 20, 48, GREY, 1, " stroke-dasharray='3 4'")
    return fig(svg(W, 206, body), 'Каждое число встаёт на своё место; прочитать прямую слева направо — это и есть возрастание.',
               fx=True)


# ——————————————————————————— глава 4 ———————————————————————————

def fan(prefix, start, steps, lab, axis, cap, ok_md):
    """Веер прыжков из одной точки по строкам таблицы: конец сдвигается на шаг, прежняя дуга гаснет в серый."""
    need(*ok_md)
    mk = prefix
    nl = NumLine(30, 410, axis[0], axis[1], 132)
    body = arrow_defs_p(mk, [BLUE, GREY]) + nl.axis(1, range(axis[0], axis[1] + 1), m, size=14)
    body += nl.point(start, None, GOLD, 6)
    n = len(steps)
    for k, b in enumerate(steps):
        d_in = 0.4 + 0.75 * k
        d_out = 0.4 + 0.75 * (k + 1) if k < n - 1 else None
        end = start + b
        h = 14 + 14 * abs(b)
        if b == 0:
            col = circle(nl.x(start), nl.y, 10, GREEN, 2.2) + t(nl.x(start), nl.y - 18, lab(b), BLUE, 14, weight=600)
            grey = circle(nl.x(start), nl.y, 10, GREY, 1.6)
        else:
            col = nl.jump(start, end, BLUE, lab(b), h, f'{mk}0', 14) + dot(nl.x(end), nl.y, 6, GREEN)
            grey = nl.jump(start, end, GREY, None, h, f'{mk}1', 14) + dot(nl.x(end), nl.y, 4, GREY)
        body += grey_then(d_in, d_out, col, grey)
    return fig(svg(W, 166, body), cap, fx=True)


def c4_fan():
    """4.1 — 3 + 2, 3 + 1, …, 3 + (−4): конец прыжка ползёт влево, за нулём дуга разворачивается (анимация)."""
    steps = [2, 1, 0, -1, -2, -3, -4]
    assert [3 + b for b in steps] == [5, 4, 3, 2, 1, 0, -1]
    return fan('r6c4a', 3, steps, lambda b: f'+{b}' if b >= 0 else f'+({m(b)})', (-2, 6),
               'Второе слагаемое меньше на 1 — конец прыжка на шаг левее; после «+0» дуга просто уходит влево.',
               ['`3 + (−1) = 2`, `3 + (−2) = 1`, `3 + (−3) = 0` и `3 + (−4) = −1`'])


def c4_same():
    """4.2 — −7 + (−5) = −12: две дуги в одну сторону складываются."""
    a, b = -7, -5
    need('`−7 + (−5) = −12`', 'Два раза влево: сначала на 7, потом ещё на 5.')
    mk = 'r6c4b'
    nl = NumLine(30, 410, -13, 1, 80)
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(1, None, size=14) + labels(nl, (a + b, a, 0))
    body += nl.point(0, None, GOLD, 6)
    body += arcs(nl, 0, a, BLUE, None, 30, m(a), f'{mk}0') + arcs(nl, a, a + b, BLUE, None, 26, f'+({m(b)})', f'{mk}0')
    body += nl.point(a + b, None, GREEN, 6)
    body += brace(nl.x(a), nl.x(0), nl.y + 34, str(-a), up=False, col=VIOLET)
    body += brace(nl.x(a + b), nl.x(a), nl.y + 34, str(-b), up=False, col=VIOLET)
    body += brace(nl.x(a + b), nl.x(0), nl.y + 74, f'{-a} + {-b} = {-(a + b)}', up=False, col=VIOLET)
    return fig(svg(W, 190, body), 'Обе дуги идут влево, поэтому их длины ложатся одна за другой.')


def cancel(prefix, first, second, axis, rule_md, cap, dt):
    """Гашение шагов: ряд first (из 0), над ним ряд second; пары гаснут, остаток зеленеет (анимация)."""
    need(*rule_md)
    a, b = first, second
    end = a + b
    sa, sb = (1 if a > 0 else -1), (1 if b > 0 else -1)
    mk = prefix
    nl = NumLine(30, 410, axis[0], axis[1], 120)
    body = arrow_defs_p(mk, [BLUE, GREY, GREEN]) + nl.axis(1, None, size=14) + labels(nl, (end, 0, a))
    body += nl.point(0, None, GOLD, 6)
    row1 = [(k * sa, (k + 1) * sa) for k in range(abs(a))]
    row2 = [(a + k * sb, a + (k + 1) * sb) for k in range(abs(b))]
    pairs = min(abs(a), abs(b))
    killed1 = set(range(abs(a) - pairs, abs(a)))
    killed2 = set(range(pairs))
    order = sorted(killed1, reverse=True)
    t_pair = {}
    for j, (i1, i2) in enumerate(zip(order, sorted(killed2))):
        t_pair[('1', i1)] = t_pair[('2', i2)] = 0.8 + dt * j
    t_green = 0.8 + dt * pairs + 0.4
    for i, (u, v) in enumerate(row1):
        col = unit_arrow(nl, u, v, -22, BLUE, f'{mk}0')
        if ('1', i) in t_pair:
            body += grey_then(None, t_pair[('1', i)], col, unit_arrow(nl, u, v, -22, GREY, f'{mk}1'))
        else:
            body += grey_then(None, t_green, col, unit_arrow(nl, u, v, -22, GREEN, f'{mk}2'))
    for i, (u, v) in enumerate(row2):
        col = unit_arrow(nl, u, v, -46, BLUE, f'{mk}0')
        if ('2', i) in t_pair:
            body += grey_then(None, t_pair[('2', i)], col, unit_arrow(nl, u, v, -46, GREY, f'{mk}1'))
        else:
            body += grey_then(None, t_green, col, unit_arrow(nl, u, v, -46, GREEN, f'{mk}2'))
    for j, i2 in enumerate(sorted(killed2)):
        u, v = row2[i2]
        xm = nl.x((u + v) / 2)
        body += g('fi', t_pair[('2', i2)], line(xm, nl.y - 42, xm, nl.y - 26, GREY, 1.2, " stroke-dasharray='2 2'"))
    body += t(nl.x(a) + 8 * sa, nl.y - 17, m(a) if a < 0 else f'+{a}', BLUE, 14, anchor='start' if sa > 0 else 'end')
    body += t(round((nl.x(a) + nl.x(end)) / 2, 1), nl.y - 60, f'+{b}' if b > 0 else f'+({m(b)})', BLUE, 14)
    body += g('fi', t_green + 0.4, nl.point(end, None, GREEN, 6) +
              brace(nl.x(min(0, end)), nl.x(max(0, end)), nl.y + 34, f'осталось {abs(end)}', up=False, col=GREEN))
    return fig(svg(W, 196, body), cap, fx=True)


def c4_cancel_a():
    """4.3 — −9 + 4: четыре пары погасились, влево осталось 5 (анимация)."""
    assert -9 + 4 == -5 and 9 - 4 == 5
    return cancel('r6c4c', -9, 4, (-10, 1),
                  ['`−9 + 4 = −5`: девять шагов влево, потом четыре обратно вправо', '`9 − 4 = 5`'],
                  'Шаг вправо и шаг влево вместе никуда не ведут — такие пары гаснут; остаются шаги той стороны, где их больше.',
                  0.6)


def c4_cancel_b():
    """4.4 — 8 + (−13): восемь пар погасились, влево осталось 5, ноль проскочили (анимация)."""
    assert 8 + -13 == -5 and 13 - 8 == 5
    return cancel('r6c4d', 8, -13, (-6, 9),
                  ['`8 + (−13) = −5`: восемь вправо, тринадцать влево', '`13 − 8 = 5`'],
                  'Восемь пар погасли, пять шагов влево остались — и ушли за ноль.', 0.32)


def c4_two_paths():
    """4.5 — по записи и по кучкам: разные пути, один конец −2 (анимация)."""
    terms = [-3, 11, -8, -6, 4]
    need('`−3 + 11 − 8 + (−6) + 4`', '`−3 + 11 = 8`; `8 − 8 = 0`; `0 + (−6) = −6`; `−6 + 4 = −2`',
         '**положительные: `11`, `4`; отрицательные: `−3`, `−8`, `−6`**', '`15 + (−17)`')
    pos, neg = sum(x for x in terms if x > 0), sum(x for x in terms if x < 0)
    assert (pos, neg, sum(terms)) == (15, -17, -2)
    mk = 'r6c4e'
    nl = NumLine(56, 440, -7, 16, 0)
    rows, cur = [], 0
    for x in terms:
        rows.append((cur, cur + x, ('+' if x > 0 else '') + m(x)))
        cur += x
    piles = [(0, pos, f'+{pos}'), (pos, pos + neg, m(neg))]
    y0, dy = 46, 32
    ys = [y0 + dy * k for k in range(5)] + [y0 + dy * 5 + 30, y0 + dy * 6 + 30]
    nl.y = ys[-1] + 34
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(1, None, size=14) + labels(nl, (-6, -2, 0, 8, 15))
    body += t(10, ys[0] - 22, 'подряд:', MUTED, 14, anchor='start')
    body += t(10, ys[5] - 22, 'кучками:', MUTED, 14, anchor='start')
    for k, (u, v, s) in enumerate(rows + piles):
        y = ys[k]
        d = 0.3 + 0.55 * k
        xa, xb = nl.x(u), nl.x(v)
        a = line(round(xa, 1), y, round(xb - (3 if v > u else -3), 1), y, BLUE, 2.4, f" marker-end='url(#{mk}0)'")
        a += t(round((xa + xb) / 2, 1), y - 7, s, BLUE, 14, weight=600)
        a += dot(xa, y, 3, MUTED)
        body += g('fi', d, a)
    dg = 0.3 + 0.55 * 7 + 0.3
    body += g('fi', dg, line(nl.x(-2), ys[4], nl.x(-2), nl.y, GOLD, 1.6, " stroke-dasharray='5 4'") +
              nl.point(-2, None, GREEN, 6))
    return fig(svg(W, nl.y + 34, body), 'Порядок прыжков другой, путь другой, а конец тот же: −2.', fx=True)


# ——————————————————————————— глава 5 ———————————————————————————

def c5_fan():
    """5.1 — 5 − 2, 5 − 1, 5 − 0, 5 − (−1), 5 − (−2): дуга укорачивается и разворачивается вправо (анимация)."""
    steps = [-2, -1, 0, 1, 2]                  # сдвиг конца: 5 − b
    subs = [2, 1, 0, -1, -2]
    assert [5 - b for b in subs] == [3, 4, 5, 6, 7]
    return fan('r6c5a', 5, steps, lambda s: f'− {-s}' if s <= 0 else f'− ({m(-s)})', (0, 8),
               'Вычитаемое меньше на 1 — конец на шаг правее; за «− 0» дуга разворачивается вправо.',
               ['Во втором столбце `3`, `4`, `5` — каждый раз на 1 больше; дальше идут `6` и `7`.',
                '| `5 − (−1)` | `?` | `5 + 1` | `6` |', '| `5 − (−2)` | `?` | `5 + 2` | `7` |'])


def c5_one_arc():
    """5.2 — −4 − (−10) и −4 + 10: одна дуга; проверка 6 + (−10) = −4 — она же обратно."""
    a, b = -4, -10
    need('`−4 − (−10) = −4 + 10 = 6`', '`6 + (−10) = −4`')
    r = a - b
    assert r == 6 and r + b == a
    mk = 'r6c5b'
    nl = NumLine(30, 410, -5, 7, 100)
    body = arrow_defs_p(mk, [BLUE, GREEN]) + nl.axis(1, None, size=14) + labels(nl, (0,))
    body += nl.point(a, None, GOLD, 6) + nl.point(r, None, GREEN, 6)
    body += t(nl.x(a) - 10, nl.y - 8, m(a), GOLD, 15, anchor='end', weight=600)
    body += t(nl.x(r) + 10, nl.y - 8, m(r), GREEN, 15, anchor='start', weight=600)
    body += arcs(nl, a, r, BLUE, None, 42, f'{m(a)} − ({m(b)})', f'{mk}0', size=15)
    body += t(nl.x((a + r) / 2), nl.y - 16, f'= {m(a)} + {-b}', BLUE, 15, weight=600)
    body += arcs(nl, r, a, GREEN, None, 40, f'проверка: {r} + ({m(b)}) = {m(a)}', f'{mk}1', below=True, size=14,
                 extra="stroke-dasharray='6 4'")
    return fig(svg(W, 184, body), 'Две записи — одна дуга; проверка сложением проходит ту же дугу обратно.')


def c5_slide():
    """5.3 — точка 5 стоит, вторая едет влево по строкам таблицы; скобка расстояния растёт и у нуля режется (анимация)."""
    fixed, rows = 5, [(3, 2), (1, 4), (-1, 6), (-3, 8)]
    for v, dist in rows:
        need(f'| `5` и `{m(v)}` | `{dist}` |')
        assert fixed - v == dist
    need('от `−1` до `0` один шаг, от `0` до `5` ещё пять, всего `6`')
    nl = NumLine(40, 410, -4, 6, 60)
    y = nl.y
    body = nl.axis(1, range(-4, 7), m, size=14) + nl.point(fixed, None, GOLD, 6)
    body += t(nl.x(fixed), y - 16, 'стоит', GOLD, 15)
    starts = [None, 0.6, 2.2, 3.8]          # когда точка уезжает к строке k
    arrive = [None] + [d + 1.3 for d in starts[1:]]
    for k, (v, dist) in enumerate(rows):
        if v >= 0:
            br = brace(nl.x(v), nl.x(fixed), y + 34, str(dist), up=False, col=VIOLET)
        else:
            br = (brace(nl.x(v), nl.x(0), y + 34, str(-v), up=False, col=VIOLET) +
                  brace(nl.x(0), nl.x(fixed), y + 34, str(fixed), up=False, col=VIOLET) +
                  brace(nl.x(v), nl.x(fixed), y + 74, f'{-v} + {fixed} = {dist}', up=False, col=VIOLET))
        if k + 1 < len(rows):
            br = g('fo', starts[k + 1], br)
        body += g('fi', arrive[k], br) if arrive[k] is not None else br
    mover = dot(nl.x(rows[0][0]), y, 6, BLUE)
    for k in range(len(rows) - 1, 0, -1):    # вложенные переезды: каждый — на одну строку таблицы
        dx = nl.x(rows[k][0]) - nl.x(rows[k - 1][0])
        mover = g('sl', starts[k], mover, f';--to:translate({dx:.1f}px,0px)')
    body += mover
    return fig(svg(W, y + 110, body),
               'Вторая точка уезжает влево — расстояние растёт; за нулём оно складывается из куска до нуля и куска от нуля до 5.',
               fx=True)


def c5_distance():
    """5.3 — A(−7), B(5): разности 12 и −12 — один путь в двух направлениях; 7 + 5 = 12."""
    a, b = -7, 5
    need('Точка `A` имеет координату `−7`, точка `B` — координату `5`', '`5 − (−7) = 5 + 7 = 12`',
         '`−7 − 5 = −7 + (−5)`', 'всего `7 + 5 = 12`')
    assert b - a == 12 and a - b == -12
    mk = 'r6c5c'
    nl = NumLine(90, 370, -8, 6, 92)
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(1, None, size=14) + labels(nl, (0,))
    body += nl.point(a, None, GOLD, 6) + nl.point(b, None, GOLD, 6)
    body += t(nl.x(a) - 6, nl.y - 10, f'A({m(a)})', GOLD, 16, anchor='end', weight=600)
    body += t(nl.x(b) + 6, nl.y - 10, f'B({b})', GOLD, 16, anchor='start', weight=600)
    body += arcs(nl, a, b, BLUE, None, 34, f'{b} − ({m(a)}) = {b - a}', f'{mk}0', size=15)
    body += arcs(nl, b, a, BLUE, None, 30, f'{m(a)} − {b} = {m(a - b)}', f'{mk}0', below=True, size=15)
    yb = nl.y + 82
    body += brace(nl.x(a), nl.x(0), yb, str(-a), up=False, col=VIOLET)
    body += brace(nl.x(0), nl.x(b), yb, str(b), up=False, col=VIOLET)
    body += brace(nl.x(a), nl.x(b), yb + 40, f'{-a} + {b} = {b - a}', up=False, col=VIOLET)
    return fig(svg(W, yb + 80, body), 'Обе разности — один и тот же путь, туда и обратно; его длина режется нулём на 7 и 5.')


# ——————————————————————————— глава 6 ———————————————————————————

def c6_repeat():
    """6.1 — 3 · (−2) и 5 · (−3): один прыжок, повторённый 3 и 5 раз."""
    need('`(−2) + (−2) + (−2) = −6`', 'Так же `5 · (−3)` — пять шагов влево по три, получается `−15`')
    mk = 'r6c6a'
    body = arrow_defs_p(mk, [BLUE])
    for (n, s, y, lo) in ((3, -2, 74, -7), (5, -3, 176, -16)):
        nl = NumLine(40, 410, lo, 0, y)
        body += nl.axis(1, None, size=14) + labels(nl, (n * s, 0))
        body += t(10, y - 52, f'{n} · ({m(s)})', INK, 16, anchor='start', weight=600)
        body += nl.point(0, None, GOLD, 6)
        for k in range(n):
            body += arcs(nl, k * s, (k + 1) * s, BLUE, None, 16, m(s), f'{mk}0')
        body += nl.point(n * s, None, GREEN, 6)
    return fig(svg(W, 210, body), 'Положительный множитель говорит, сколько раз прыгнуть; отрицательный — на сколько и куда.')


def c6_rhythm():
    """6.2 — ряд 3·(−4), 2·(−4), …: шаг +4 продолжается за нулём (анимация)."""
    vals = [k * -4 for k in (3, 2, 1, 0, -1, -2)]
    need('`−12`, `−8`, `−4`, `0` — каждый раз **прибавляется 4**', '`(−1) · (−4) = 4` и `(−2) · (−4) = 8`')
    assert vals == [-12, -8, -4, 0, 4, 8]
    mk = 'r6c6b'
    nl = NumLine(30, 410, -13, 9, 80)
    body = arrow_defs_p(mk, [BLUE, GREEN]) + nl.axis(1, None, size=14) + labels(nl, vals)
    body += nl.point(vals[0], None, GOLD, 6)
    for k in range(5):
        u, v = vals[k], vals[k + 1]
        new = v > 0
        col = GREEN if new else BLUE
        d = 0.4 + 0.8 * k
        body += arcs(nl, u, v, col, d, 18, '+4', f'{mk}{1 if new else 0}')
        body += g('fi', d + 0.3, nl.point(v, None, col, 6))
    body += g('fi', 0.4 + 0.8 * 3 + 0.4, t(nl.x(4), nl.y + 48, '(−1) · (−4)', GREEN, 14, weight=600))
    body += g('fi', 0.4 + 0.8 * 4 + 0.4, t(nl.x(8), nl.y + 70, '(−2) · (−4)', GREEN, 14, weight=600))
    return fig(svg(W, 160, body), 'Ряд идёт ровными прыжками по 4; тот же прыжок за нулём попадает в 4 и 8.', fx=True)


def c6_flip():
    """6.3 — каждый отрицательный множитель перебрасывает произведение через ноль."""
    prods, p = [], 1
    for _ in range(5):
        p *= -2
        prods.append(p)
    assert prods == [-2, 4, -8, 16, -32]
    need('| 5 | `16 · (−2) = −32` |', 'Знаки идут по очереди: минус, плюс, минус, плюс, минус.')
    x0, k = 296, 6
    top, dy = 46, 28
    body = t(16, top - 18, 'минусов', MUTED, 14, anchor='start')
    body += line(x0, top - 26, x0, top + dy * 4 + 14, GOLD, 1.6, " stroke-dasharray='5 4'")
    body += t(x0, top + dy * 4 + 34, '0', INK, 14)
    for i, v in enumerate(prods):
        y = top + dy * i
        col = PINK if v < 0 else CYAN
        xe = x0 + v * k
        body += t(36, y + 5, str(i + 1), INK, 15, weight=600)
        body += rect(round(min(x0, xe), 1), y - 8, abs(v) * k, 16, col, 'none', 0, 2, " fill-opacity='0.7'")
        body += t(round(xe + (-6 if v < 0 else 6), 1), y + 5, m(v), col, 15,
                  anchor='end' if v < 0 else 'start', weight=600)
    return fig(svg(W, top + dy * 4 + 44, body),
               'Каждый новый множитель −2 перебрасывает произведение на другую сторону нуля; при чётном числе минусов оно справа.')


# ——————————————————————————— глава 7 ———————————————————————————

def c7_zero():
    """7.1 — умножение на 0 стягивает всё в 0: в −5 не попадает ничто."""
    need('Чему равно `−5 : 0`?', 'любое число, умноженное на ноль, даёт ноль')
    mk = 'r6c7a'
    nl = NumLine(30, 410, -6, 3, 112)
    body = arrow_defs_p(mk, [BLUE]) + nl.axis(1, None, size=14) + labels(nl, (-5, 0))
    for v in (-6, -3, -1.5, 1, 2.5):
        body += dot(nl.x(v), nl.y, 4, MUTED)
        body += nl.jump(v, 0, BLUE, None, 8 + 6 * abs(v), f'{mk}0')
    body += t(nl.x(-3), nl.y - 54, '· 0', BLUE, 15, weight=600)
    body += t(nl.x(2.5), nl.y - 34, '· 0', BLUE, 15, weight=600)
    body += nl.point(0, None, GOLD, 6)
    body += nl.point(-5, None, RED, 7, hollow=True)
    body += t(nl.x(-5), nl.y + 48, '−5 : 0 — ?', RED, 15, weight=600)
    return fig(svg(W, 170, body), 'Что ни умножь на ноль — попадёшь в ноль; в −5 не ведёт ни одна стрелка, поэтому ответа нет.')


def c7_rate():
    """7.2 — от −2 до −20 шестью равными прыжками по −3; стрелка «стало − было» смотрит влево."""
    was, now, hours, rate = -2, -20, 6, -3
    need('в 8 утра было `−2°`, в 14 часов стало `−20°`', '`−20 − (−2) = −20 + 2 = −18`', '`14 − 8 = 6`',
         'за 6 часов по `−3` градуса — это `−18`')
    assert now - was == hours * rate == -18 and 14 - 8 == hours
    mk = 'r6c7b'
    nl = NumLine(40, 410, -21, 0, 76)
    body = arrow_defs_p(mk, [BLUE, VIOLET]) + nl.axis(1, None, size=14) + labels(nl, (now, was, 0))
    for k in range(hours):
        body += arcs(nl, was + k * rate, was + (k + 1) * rate, BLUE, None, 14, m(rate), f'{mk}0')
    body += nl.point(was, None, GOLD, 6) + nl.point(now, None, GREEN, 6)
    body += t(nl.x(was), 22, 'было, 8 ч', GOLD, 14, weight=600)
    body += t(nl.x(now), 22, 'стало, 14 ч', GREEN, 14, weight=600)
    yy = nl.y + 46
    body += line(nl.x(was), yy, nl.x(now) + 3, yy, VIOLET, 2.2, f" marker-end='url(#{mk}1)'")
    body += t(nl.x((was + now) / 2), yy + 24, f'стало − было = {m(now - was)}', VIOLET, 15, weight=600)
    return fig(svg(W, yy + 36, body), 'Равномерно — значит шесть одинаковых прыжков; от «было» к «стало» путь идёт влево, поэтому со знаком минус.')


# ——————————————————————————— глава 8 ———————————————————————————

def c8_stock():
    """8.1 — запас чисел как точки на прямой: 3 − 5 и 3 : 2 падают туда, где точки нет."""
    need('у `3 − 5` ответа среди натуральных чисел нет', '`3 : 2` не имеет ответа среди целых чисел')
    mk = 'r6c8a'
    body = arrow_defs_p(mk, [BLUE])
    top = NumLine(40, 410, -3, 7, 72)
    body += t(10, 22, 'натуральные', GREEN, 15, anchor='start', weight=600)
    body += top.axis(1, range(-3, 8), m, size=14)
    for v in range(1, 8):
        body += dot(top.x(v), top.y, 5, CYAN)
    body += top.jump(3, 3 - 5, BLUE, '3 − 5', 24, f'{mk}0', 15)
    body += top.point(-2, None, RED, 7, hollow=True)
    bot = NumLine(40, 410, -3, 7, 168)
    body += t(10, bot.y - 40, 'целые', BLUE, 15, anchor='start', weight=600)
    body += bot.axis(1, range(-3, 8), m, size=14)
    for v in range(-3, 8):
        body += dot(bot.x(v), bot.y, 5, GOLD if v == 0 else (PINK if v < 0 else CYAN))
    body += bot.point(1.5, '3 : 2', RED, 7, hollow=True)
    return fig(svg(W, 206, body), 'Запас чисел — точки на прямой; ответ падает туда, где точки нет.')


def frames(o, m_, i, lab=True):
    out = rect(*o, VIOLET, VIOLET, 2, 10, " fill-opacity='0.08'")
    out += rect(*m_, BLUE, BLUE, 2, 10, " fill-opacity='0.10'")
    out += rect(*i, GREEN, GREEN, 2, 10, " fill-opacity='0.14'")
    return out


def c8_nested():
    """8.2 — замена ASCII: вложенные рамки и числа в них."""
    blk = code_block('натуральные:   7')
    rat, integ, nat = ['−3/4', '2,7', '−12', '0', '7'], ['−12', '0', '7'], ['7']
    for s in rat:
        assert s in blk
    body = frames((8, 8, 444, 176), (28, 52, 404, 120), (48, 96, 384, 62))

    col_x = {s: 196 + 54 * k for k, s in enumerate(rat)}      # одно число — один столбец во всех рамках

    def put(y, x, name, nums, col):
        o = t(x, y, f'{name}:', col, 15, anchor='start', weight=600)
        for s in nums:
            o += t(col_x[s], y, s, INK, 16, weight=600)
        return o

    body += put(36, 22, 'рациональные', rat, VIOLET) + put(80, 42, 'целые', integ, BLUE)
    body += put(132, 62, 'натуральные', nat, GREEN)
    s = svg(W, 192, body)
    ascii_tokens_on(blk, s)
    return fig(s, zamena=True)


def c8_value():
    """8.3 — 100/4 = 25 едет в натуральные, −1,25 = −5/4 — только в рациональные (анимация)."""
    need('число `100/4` записано дробью, но это `25`', '`−1,25` записано десятичной дробью, но это `−5/4`')
    assert F(100, 4) == 25 and F(-125, 100) == F(-5, 4)
    body = frames((8, 70, 444, 160), (24, 100, 270, 122), (40, 136, 150, 78))
    body += t(442, 92, 'рациональные', VIOLET, 14, anchor='end', weight=600)
    body += t(34, 122, 'целые', BLUE, 14, anchor='start', weight=600)
    body += t(50, 156, 'натуральные', GREEN, 14, anchor='start', weight=600)
    y0 = 40
    body += t(40, y0, '100/4', INK, 18, anchor='start', weight=600) + g('fi', 0.4, t(98, y0, '=', MUTED, 18))
    body += g('fi', 0.4, t(124, y0, '25', GREEN, 18, weight=600))
    body += g('fi', 0.4, g('sl', 1.0, t(124, y0, '25', GREEN, 18, weight=600),
                            f';--to:translate({115 - 124}px,{190 - y0}px)'))
    body += t(250, y0, '−1,25', INK, 18, anchor='start', weight=600) + g('fi', 2.6, t(312, y0, '=', MUTED, 18))
    body += g('fi', 2.6, t(346, y0, '−5/4', VIOLET, 18, weight=600))
    body += g('fi', 2.6, g('sl', 3.2, t(346, y0, '−5/4', VIOLET, 18, weight=600),
                            f';--to:translate({372 - 346}px,{170 - y0}px)'))
    return fig(svg(W, 240, body), 'Рамку выбирает само число: сначала перепиши его, потом клади.', fx=True)


def c8_square():
    """8.4 — замена ASCII: единичный квадрат и его диагональ."""
    blk = code_block('диагональ = ?')
    x, y, a = 70, 16, 130
    body = rect(x, y, a, a, 'none', MUTED, 2)
    body += line(x, y + a, x + a, y, GOLD, 3)
    body += t(x + a + 30, y + a / 2 - 10, 'сторона = 1', INK, 16, anchor='start')
    body += t(x + a + 30, y + a / 2 + 18, 'диагональ = ?', GOLD, 16, anchor='start', weight=600)
    s = svg(W, a + 32, body)
    ascii_tokens_on(blk, s)
    return fig(s, zamena=True)


def c8_four():
    """8.5 — квадрат на диагонали = четыре половинки единичных клеток: 4 · 1/2 = 2."""
    need('два треугольника площадью `1/2` каждый', 'значит его площадь `4 · 1/2 = 2`')
    assert 4 * F(1, 2) == 2
    x0, y0, c = 40, 16, 90
    body = ''
    for i in range(2):
        for j in range(2):
            body += rect(x0 + c * i, y0 + c * j, c, c, 'none', GREY, 1.4, extra=" stroke-dasharray='4 4'")
    body += rect(x0 + c, y0 + c, c, c, 'none', MUTED, 2)
    ctr = (x0 + c, y0 + c)
    v = [(x0 + c, y0), (x0 + 2 * c, y0 + c), (x0 + c, y0 + 2 * c), (x0, y0 + c)]
    for k in range(4):
        p, q = v[k], v[(k + 1) % 4]
        body += path([ctr, p, q], GOLD, 1.5, GOLD, extra=f" fill-opacity='{0.45 if k % 2 else 0.25}'")
        cx, cy = (ctr[0] + p[0] + q[0]) / 3, (ctr[1] + p[1] + q[1]) / 3
        body += t(round(cx, 1), round(cy + 5, 1), '1/2', INK, 15, weight=600)
    body += path(v, GOLD, 2.4)
    body += line(v[2][0], v[2][1], v[1][0], v[1][1], GOLD, 4)          # «/» — как диагональ на 8.4
    body += t(x0 + 1.5 * c, y0 + 2 * c + 22, '1', MUTED, 15)
    body += t(x0 + 2 * c + 30, y0 + c - 6, 'квадрат на диагонали:', MUTED, 15, anchor='start')
    body += t(x0 + 2 * c + 30, y0 + c + 22, '4 · 1/2 = 2', GOLD, 18, anchor='start', weight=600)
    return fig(svg(W, y0 + 2 * c + 32, body),
               'Каждый жёлтый треугольник — половина своей клетки; квадрат на диагонали собран из четырёх таких половинок.')


# ——————————————————————————— сборка ———————————————————————————

FIGS = {
    '−5 −4 −3 −2 −1 0 1 2 3 4 5': v1_line,
    'Ноль не положительный и не отрицательный.': v2_parts,
    '−1/2 стоит посередине между': v3_halves,
    '3 2 1 0 −1 −2 −3': v4_thermo,
    'Число −100 дальше от нуля, чем −1': v5_far,
    '●──→───→───→───→●': v6_warmer,
    'этаж 0 на уровне земли лифт проехал': v7_lift,
    '−7 это «слева, на расстоянии 7»': r1_sign_modulus,
    '7 − 3 это то же самое, что 7 + (−3)': r2_same_path,
    'пишут A(−4)': c1_coord,
    'От −18 влево на 25': c1_submarine,
    'А вот 5 и −3 не противоположные': c2_opposite,
    'два зеркала подряд возвращают число на место': c2_mirror,
    'Отмеряю 4 единичных отрезка вправо от нуля': c2_four,
    c3_key()[0]: c3_line,
    'Справа от нуля наоборот': c3_v,
    '−5/2 < −2 < −0,3 < 0 < 3/4 < 1': c3_order,
    'Прибавить −1 — сдвинуться от 3 на один шаг влево': c4_fan,
    'Два раза влево: сначала на 7, потом ещё на 5': c4_same,
    'девять шагов влево, потом четыре обратно вправо': c4_cancel_a,
    'восемь вправо, тринадцать влево': c4_cancel_b,
    'Проверка другим путём — подряд слева направо': c4_two_paths,
    'Во втором столбце 3, 4, 5 — каждый раз на 1 больше': c5_fan,
    'Правило работает и для отрицательного вычитаемого': c5_one_arc,
    'Расстояние в третьей строке по шагам': c5_slide,
    'Проверь по картинке: от −7 до 0 семь единиц': c5_distance,
    'Три шага влево по два': c6_repeat,
    'Закономерность ровная, ломать её не за что': c6_rhythm,
    'Знаки идут по очереди: минус, плюс, минус': c6_flip,
    'Чему равно −5 : 0': c7_zero,
    'Проверка: за 6 часов по −3 градуса': c7_rate,
    '3 : 2 не имеет ответа среди целых чисел': c8_stock,
    'натуральные: 7': c8_nested,
    'число 100/4 записано дробью, но это 25': c8_value,
    'диагональ = ?': c8_square,
    'складывается из четырёх таких треугольников': c8_four,
}


if __name__ == '__main__':
    keys = [norm(b) for b in re.split(r'\n\s*\n', MD)]
    out = {}
    for anchor, f in FIGS.items():
        if anchor.startswith('='):
            assert sum(k == anchor[1:] for k in keys) == 1, anchor
        else:
            assert any(anchor in k for k in keys), f'якоря «{anchor}» нет в тексте'
        out[anchor] = f()
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(out), 'рисунков,', sum('class="fx' in v for v in out.values()), 'анимаций →', os.path.relpath(VIS))
