#!/usr/bin/env python3
"""Иллюстрации учебника «Обыкновенные дроби» (5 класс) → math5_drobi_uchebnik.vis.json (пишется целиком).

План рисунков и мысль каждого движения: 26-27/school5/vis/plan_drobi.md.
Числа на рисунках вычисляются здесь (fractions.Fraction) и сверяются через assert с текстом MD.

Запуск: python3 26-27/school5/vis/drobi.py
"""
import json, os, re
from fractions import Fraction as F
from math import gcd

from common import (svg, fig, t, g, line, GOLD, BLUE, GREEN, RED, GREY, INK, MUTED, DARK,
                    arrow_defs_p)

HERE = os.path.dirname(os.path.abspath(__file__))
MDP = os.path.join(HERE, '..', 'math5_drobi_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math5_drobi_uchebnik.vis.json')
MD = open(MDP).read()


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', s)).strip()


BLOCKS = [norm(b) for b in re.split(r'\n\s*\n', MD)]


def need(*ss):
    """Строка (число, запись) действительно стоит в тексте MD."""
    for s in ss:
        assert s in MD, f'нет в MD: {s!r}'


GL = {(1, 2): '½', (1, 3): '⅓', (2, 3): '⅔', (1, 4): '¼', (3, 4): '¾', (1, 5): '⅕', (2, 5): '⅖',
      (5, 6): '⅚', (1, 8): '⅛', (1, 6): '⅙'}


def md_mixed(q):
    """Смешанное число так, как оно набрано в MD: 3⅓, 2 8/17."""
    w, r = divmod(q.numerator, q.denominator)
    if r == 0:
        return str(w)
    gl = GL.get((r // gcd(r, q.denominator), q.denominator // gcd(r, q.denominator)))
    if w == 0:
        return gl or f'{r}/{q.denominator}'
    return f'{w}{gl}' if gl else f'{w} {r}/{q.denominator}'


def sf(q):
    return f'{q.numerator}/{q.denominator}'


# ——— примитивы этой книги ———

def cw(s, size):
    """Ширина набора цифр."""
    return len(str(s)) * size * 0.58


def fr(x, cy, n, d, fill=INK, size=22, w=None, sw=2):
    """Дробь столбиком с чертой на высоте cy."""
    w = w or max(cw(n, size), cw(d, size)) + 10
    return (t(x, ny(cy, size), n, fill, size, weight=600) + line(x - w / 2, cy, x + w / 2, cy, fill, sw)
            + t(x, dy_(cy, size), d, fill, size, weight=600))


def ny(cy, size):
    return round(cy - 0.3 * size, 1)


def dy_(cy, size):
    return round(cy + 1.0 * size, 1)


def op(x, cy, s, fill=INK, size=22, cls=None, d=None):
    """Знак действия или целое число по центру строки дробей."""
    return t(x, round(cy + 0.36 * size, 1), s, fill, size, weight=500, cls=cls, d=d)


def mixed(x, cy, q, fill=INK, size=22):
    """Смешанное число: целая часть + маленькая дробь; x — центр всей записи."""
    w_, r = divmod(q.numerator, q.denominator)
    small = size * 0.62
    wd = cw(w_, size)
    fw = max(cw(r, small), cw(q.denominator, small)) + 6
    left = x - (wd + 3 + fw) / 2
    return (t(left, round(cy + 0.36 * size, 1), w_, fill, size, anchor='start', weight=600)
            + fr(left + wd + 3 + fw / 2, cy - 0.12 * size, r, q.denominator, fill, small, fw, 1.5))


def strike(x, yb, size, w=None, d=None, col=RED):
    """Косая черта по числу с базовой линией yb — «сократили»."""
    w = w or cw('00', size) + 6
    body = line(x - w / 2, yb + 0.15 * size, x + w / 2, yb - 0.85 * size, col, 2.6)
    return g('fi', d, body) if d is not None else body


def fo(d, body, o=0):
    return g('fo', d, body, f';--o:{o}')


def fi(d, body):
    return g('fi', d, body)


def sl(d, dx, dy, body):
    return g('sl', d, body, f';--to:translate({dx}px,{dy}px)')


def brick(x, y, w, h, col=GOLD, op_=0.35, stroke=None, sw=1.5, rx=2):
    st = stroke or col
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{col}' fill-opacity='{op_}' "
            f"stroke='{st}' stroke-width='{sw}'/>")


def block(x, y, n, w, h, col, op_=0.4, sw=1.5):
    """n кирпичиков одним куском: перегородки — только у краёв, чтобы число в середине не перечёркивалось."""
    b = brick(x, y, n * w, h, col, op_, col, sw, 0)
    for i in range(1, n):
        xx = x + i * w
        b += line(xx, y, xx, y + 9, col, 1.2) + line(xx, y + h - 9, xx, y + h, col, 1.2)
    return b


def empty(x, y, w, h, stroke=MUTED, sw=1.5, rx=2, dash=None):
    da = f" stroke-dasharray='{dash}'" if dash else ''
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='none' stroke='{stroke}' "
            f"stroke-width='{sw}'{da}/>")


def drline(x1, y1, x2, y2, d, col=INK, sw=2, dur=0.6):
    return (f"<line class='dr' pathLength='100' x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' "
            f"stroke-width='{sw}' style='--d:{d}s;--dur:{dur}s'/>")


def link(x1, y1, x2, y2, d, col=RED):
    """Пунктир, связывающий пару сокращаемых чисел."""
    return fi(d, line(x1, y1, x2, y2, col, 1.6, " stroke-dasharray='4 4'"))


def brace(x1, x2, y, up=True, col=MUTED):
    """Фигурная скобка над (up) или под отрезком."""
    k = -8 if up else 8
    m = (x1 + x2) / 2
    return (f"<path d='M{x1} {y} q0 {k} 8 {k} L{m-6} {y+k} q6 0 6 {k} q0 {-k} 6 {-k} L{x2-8} {y+k} "
            f"q8 0 8 {-k}' fill='none' stroke='{col}' stroke-width='1.5'/>")


def arrow(x1, y1, x2, y2, mid, col=INK, sw=2, curve=0):
    if curve:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + curve
        return (f"<path d='M{x1} {y1} Q{mx} {my} {x2} {y2}' fill='none' stroke='{col}' stroke-width='{sw}' "
                f"marker-end='url(#{mid})'/>")
    return line(x1, y1, x2, y2, col, sw, f" marker-end='url(#{mid})'")


def cancel_pair(top, bot, d, size, new_top, new_bot):
    """Пара «число сверху — число снизу» сокращается: пунктир, зачёркивание, новые числа.
    top/bot = (x, cy) черты дроби, где стоит число. Старые числа гасит вызывающий (fo в момент d+0.4)."""
    (xt, ct), (xb, cb) = top, bot
    yt, yb = ny(ct, size), dy_(cb, size)
    b = link(xt, yt - 0.35 * size, xb, yb - 0.35 * size, d)
    b += strike(xt, yt, size, d=d + 0.4) + strike(xb, yb, size, d=d + 0.4)
    b += t(xt, yt - 0.95 * size, new_top, INK, round(size * 0.72), weight=600, cls='fi', d=d + 0.8)
    b += t(xb, yb + 0.85 * size, new_bot, INK, round(size * 0.72), weight=600, cls='fi', d=d + 0.8)
    return b


def card_css():
    """Свои движения книги: переворот дроби карточкой (scaleY вокруг черты) и поворот знака «:» в «×».
    Гейт как в шаблоне: без JS и при reduced-motion виден финал (старое скрыто, новое на месте)."""
    return ("<style>"
            ".cfo,.cfi,.rto,.rti,.sxo{transform-box:view-box}"
            ".cfo{transform:scaleY(0)} .rto{opacity:0} .sxo{transform:scaleX(0)}"
            "@keyframes sxo{from{transform:scaleX(1)}to{transform:scaleX(0)}}"
            "@keyframes cfo{from{transform:scaleY(1)}to{transform:scaleY(0)}}"
            "@keyframes cfi{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
            "@keyframes rto{from{transform:rotate(0deg);opacity:1}to{transform:rotate(90deg);opacity:0}}"
            "@keyframes rti{from{transform:rotate(-90deg);opacity:0}to{transform:rotate(0deg);opacity:1}}"
            "@media (prefers-reduced-motion:no-preference){"
            "html.anim figure.fx:not(.seen) .cfo,html.anim figure.fx:not(.seen) .sxo{transform:none}"
            "html.anim figure.fx:not(.seen) .cfi{transform:scaleY(0)}"
            "html.anim figure.fx:not(.seen) .rto{opacity:1}"
            "html.anim figure.fx:not(.seen) .rti{opacity:0}"
            "html.anim figure.fx.seen .cfo{animation:cfo .5s ease-in var(--d,0s) both}"
            "html.anim figure.fx.seen .sxo{animation:sxo .8s ease-in var(--d,0s) both}"
            "html.anim figure.fx.seen .cfi{animation:cfi .5s ease-out var(--d,0s) both}"
            "html.anim figure.fx.seen .rto{animation:rto .5s ease-in var(--d,0s) both}"
            "html.anim figure.fx.seen .rti{animation:rti .5s ease-out var(--d,0s) both}"
            "}</style>")


def cls_at(cls, d, ox, oy, body):
    return f"<g class='{cls}' style='--d:{d}s;transform-origin:{ox}px {oy}px'>{body}</g>"


def card_flip(x, cy, n, d, at, size=26, col_old=INK, col_new=BLUE, fade=None):
    """n/d сжимается к своей черте, на её месте разворачивается d/n (как карточка). Нужен card_css() в рисунке.
    fade = (момент для нового числителя, до какой яркости, момент для нового знаменателя)."""
    old = fr(x, cy, n, d, col_old, size)
    w = max(cw(n, size), cw(d, size)) + 10
    tn, td = t(x, ny(cy, size), d, col_new, size, weight=600), t(x, dy_(cy, size), n, col_new, size, weight=600)
    if fade:
        tn, td = fo(fade[0], tn, fade[1]), fo(fade[2], td, fade[1])
    new = tn + line(x - w / 2, cy, x + w / 2, cy, col_new, 2) + td
    return cls_at('cfo', at, x, cy, old) + cls_at('cfi', at + 0.5, x, cy, new)


def turn_sign(x, cy, at, size=26):
    """Знак «:» поворачивается и становится синим «×»."""
    oy = cy
    return (cls_at('rto', at, x, oy, op(x, cy, ':', INK, size))
            + cls_at('rti', at + 0.4, x, oy, op(x, cy, '×', BLUE, size)))


def turn_arrow(cx, cy, r, d, mid):
    """Синяя круговая стрелка ⟲ рядом с переворачиваемой дробью."""
    return fi(d, f"<path d='M{cx + r} {cy - 4} A{r} {r} 0 1 0 {cx + 4} {cy - r}' fill='none' stroke='{BLUE}' "
                 f"stroke-width='2.2' marker-end='url(#{mid})'/>")


def src_row(x, cy, items, size=26):
    """Исходник примера — статично слева, кончается знаком «=». Возвращает (svg, правый край)."""
    s, _, w = row(x, cy, items, size, center=False)
    return s, x + w


def c2_idea_flip():
    """2.0. Идея главы: слева 3/8 : 9/10 =; справа первая — «не трогаем», «:» поворачивается в «×»,
    вторая переворачивается карточкой — «обратная». Итог 3/8 × 10/9."""
    assert F(3, 8) / F(9, 10) == F(3, 8) * F(10, 9)
    need('Разделить на дробь = умножить на обратную ей', '`3/8 × 10/9`')
    S, cy = 26, 62
    src, xr = src_row(16, cy, [('F', 3, 8), ('o', ':'), ('F', 9, 10), ('o', '=')], S)
    xa, xs, xb = xr + 40, xr + 90, xr + 140
    b = [card_css(), arrow_defs_p('c2i', [BLUE]), src]
    b.append(fr(xa, cy, 3, 8, INK, S))
    b.append(t(xa, cy + 62, 'не трогаем', GOLD, 16, weight=600, cls='fi', d=0.5))
    b.append(turn_sign(xs, cy, 1.3, S))
    b.append(card_flip(xb, cy, 9, 10, 2.4, S))
    b.append(turn_arrow(xb + 44, cy + 6, 15, 2.4, 'c2i0'))
    b.append(t(xb, cy + 62, 'обратная', BLUE, 16, weight=600, cls='fi', d=3.4))
    w = xb + 80
    return fig(svg(w, 136, ''.join(b), maxw=w), fx=True)


# ——————————————————— Ритуалы ———————————————————

def r1_big_fraction():
    """Р1. Слева 5/2 × 4/3 =; справа копия съезжается в одну дробь (5 · 4)/(2 · 3), 4 и 2 сокращаются → 10/3."""
    a, b_ = F(5, 2), F(4, 3)
    assert a * b_ == F(10, 3) and gcd(4, 2) == 2
    need('5/2 × 4/3', '`4` превращается в `2`, `2` — в `1`', '10/3')
    S, cy = 26, 64
    src, xr = src_row(16, cy, [('F', 5, 2), ('o', '×'), ('F', 4, 3), ('o', '=')], S)
    c = xr + 74
    b = [src]
    for x, n, dd, dx in ((c - 50, 5, 2, 30), (c + 50, 4, 3, -30)):
        tn = t(x, ny(cy, S), n, INK, S, weight=600)
        td = t(x, dy_(cy, S), dd, INK, S, weight=600)
        b.append(sl(0.6, dx, 0, (fo(3.2, tn, 0.35) if n == 4 else tn) + (fo(3.2, td, 0.35) if dd == 2 else td)))
        b.append(fo(1.8, line(x - 14, cy, x + 14, cy, INK, 2)))
    b.append(fo(0.6, op(c, cy, '×', INK, S)))
    b.append(fi(1.7, line(c - 40, cy, c + 40, cy, INK, 2.2) + t(c, ny(cy, S) - 2, '·', INK, S)
                + t(c, dy_(cy, S) - 2, '·', INK, S)))
    b.append(cancel_pair((c + 20, cy), (c - 20, cy), 2.6, S, '2', '1'))
    b.append(fi(4.0, op(c + 80, cy, '=', INK, S) + fr(c + 128, cy, 10, 3, GREEN, S)))
    w = c + 160
    return fig(svg(w, 130, ''.join(b), maxw=w), fx=True)


def r2_tidy():
    """Р2. Слева 20/6 =; полоска из шестых → трети → 3 целых и ⅓; = 3⅓."""
    assert F(20, 6) == F(10, 3) == 3 + F(1, 3)
    need('`20/6` — это ещё не ответ, `3⅓` — ответ', '10/3')
    U, y0, h, gap = 108, 24, 40, 16
    cy = y0 + h / 2 - 8
    src, xr = src_row(14, cy, [('F', 20, 6), ('o', '=')], 24)
    x0 = xr + 16
    b = [src]
    for k, w in [(k, U) for k in range(3)] + [(3, U / 3)]:
        x = x0 + k * U
        body = brick(x, y0, w, h, GOLD, 0.3, GOLD, 1.5, 0)
        n6 = 6 if w == U else 2
        for j in range(1, n6):
            xx = x + j * w / n6
            ln = line(xx, y0, xx, y0 + h, GOLD, 1.5)
            body += fo(1.2, ln, 0) if j % 2 else ln
        b.append(sl(2.4, k * gap, 0, body))
    for k in range(3):
        b.append(t(x0 + k * (U + gap) + U / 2, y0 + h + 26, '1', INK, 20, weight=600, cls='fi', d=3.7))
    b.append(fi(3.7, fr(x0 + 3 * (U + gap) + U / 6, y0 + h + 16, 1, 3, INK, 16)))
    lx = x0 + 3 * U + U / 3 + 3 * gap
    b.append(fi(4.3, op(lx + 18, cy, '=', INK, 24) + mixed(lx + 62, cy + 2, F(10, 3), GREEN, 30)))
    w = lx + 100
    return fig(svg(w, y0 + h + 44, ''.join(b), maxw=min(w, 640)), fx=True)


def r3_estimate():
    """Р3. Прикидка 2⅔ × 3: окно 6…9, ближе к 9; 6/8 — у нуля."""
    q = F(8, 3)
    need('`2⅔ × 3`', 'между 6 и 9', '`6/8`')
    assert 2 * 3 == 6 and 3 * 3 == 9 and F(6, 8) < 1
    P, x0, y1, y2 = 52, 24, 40, 130
    X = lambda v: x0 + float(v) * P
    b = [arrow_defs_p('r3', [GOLD])]
    b.append(line(X(0), y1, X(3.4), y1, MUTED, 1.5) + line(X(0), y2, X(9.4), y2, MUTED, 1.5))
    for v in range(4):
        b.append(line(X(v), y1 - 5, X(v), y1 + 5, MUTED, 1.5) + (t(X(v), y1 - 12, v, INK, 14) if v != 3 else t(X(v) + 12, y1 - 12, v, INK, 14)))
    for v in range(10):
        b.append(line(X(v), y2 - 5, X(v), y2 + 5, MUTED, 1.5) + t(X(v), y2 + 22, v, INK, 14))
    b.append(brick(X(6), y2 - 9, 3 * P, 18, GOLD, 0.3, GOLD))
    b.append(f"<circle cx='{X(q)}' cy='{y1}' r='5' fill='{GOLD}'/>")
    b.append(mixed(X(q), y1 - 30, q, GOLD, 17))
    for v, w in ((2, 6), (q, q * 3), (3, 9)):
        b.append(line(X(v), y1 + 7, X(w), y2 - 12, GOLD, 1.5, " stroke-dasharray='5 4' marker-end='url(#r30)'"))
    b.append(t((X(2) + X(6)) / 2 - 20, (y1 + y2) / 2 + 4, '× 3', GOLD, 15, weight=600))
    b.append(f"<circle cx='{X(F(6, 8))}' cy='{y2}' r='5' fill='{RED}'/>")
    b.append(fr(X(F(6, 8)), y2 - 34, 6, 8, RED, 14))
    return fig(svg(X(9.4) + 20, y2 + 34, ''.join(b), maxw=560))


# ——————————————————— Глава 1 ———————————————————

def half_disc(cx, cy, r, left=True):
    s = 1 if left else 0
    return (f"<path d='M{cx} {cy-r} A{r} {r} 0 0 {0 if left else 1} {cx} {cy+r} Z' fill='{GOLD}' "
            f"fill-opacity='0.3' stroke='{GOLD}' stroke-width='1.8'/>")


def c1_pizzas():
    """1.1. Слева 2½ =; пиццы режутся пополам, половинки считаются → 5/2."""
    q = 2 + F(1, 2)
    assert q == F(5, 2) and 2 * 2 + 1 == 5
    need('две целые пиццы и половина', '`4` половинки', '`5/2`')
    r, cy = 44, 64
    src, xr = src_row(14, cy, [('m', q), ('o', '=')], 26)
    cxs = [xr + 64, xr + 172, xr + 280]
    b = [src]
    for cx in cxs[:2]:
        b.append(f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{GOLD}' fill-opacity='0.3' stroke='{GOLD}' stroke-width='1.8'/>")
    b.append(half_disc(cxs[2], cy, r))
    b.append(drline(cxs[0], cy - r, cxs[0], cy + r, 0.6, GOLD, 2))
    b.append(drline(cxs[1], cy - r, cxs[1], cy + r, 1.1, GOLD, 2))
    pos = [cxs[0] - r / 2, cxs[0] + r / 2, cxs[1] - r / 2, cxs[1] + r / 2, cxs[2] - r / 2]
    for k, x in enumerate(pos):
        b.append(t(x, cy + 7, k + 1, INK, 20, weight=700, cls='fi', d=1.9 + 0.4 * k))
    b.append(t(cxs[1] - 2, cy + r + 30, '2 + ', MUTED, 18, anchor='end'))
    b.append(fr(cxs[1] + 8, cy + r + 24, 1, 2, MUTED, 16))
    b.append(fi(4.0, op(cxs[2] + 56, cy, '=', INK, 26) + fr(cxs[2] + 100, cy - 6, 5, 2, GREEN, 26)))
    w = cxs[2] + 132
    return fig(svg(w, 156, ''.join(b), maxw=w), fx=True)


def c1_example_b():
    """1.2. Слева 15/4 × 12/5 =; справа пары 15–5 и 12–4 сокращаются по диагонали → 9."""
    a, b_ = F(15, 4), F(12, 5)
    assert a == 3 + F(3, 4) and b_ == 2 + F(2, 5) and a * b_ == 9
    assert (15 // 5, 5 // 5, 12 // 4, 4 // 4) == (3, 1, 3, 1)
    need('`15/4 × 12/5`', '`3/1 × 3/1`', '`9` ✅')
    S, cy = 26, 70
    src, xr = src_row(16, cy, [('F', 15, 4), ('o', '×'), ('F', 12, 5), ('o', '=')], S)
    xa, xb = xr + 44, xr + 144
    b = [src]
    b.append(t(xa, ny(cy, S), 15, INK, S, weight=600, cls='fo', extra=" style='--d:1.0s;--o:0.35'"))
    b.append(t(xa, dy_(cy, S), 4, INK, S, weight=600, cls='fo', extra=" style='--d:2.8s;--o:0.35'"))
    b.append(t(xb, ny(cy, S), 12, INK, S, weight=600, cls='fo', extra=" style='--d:2.8s;--o:0.35'"))
    b.append(t(xb, dy_(cy, S), 5, INK, S, weight=600, cls='fo', extra=" style='--d:1.0s;--o:0.35'"))
    b.append(line(xa - 22, cy, xa + 22, cy, INK, 2) + line(xb - 22, cy, xb + 22, cy, INK, 2))
    b.append(op((xa + xb) / 2, cy, '×', INK, S))
    b.append(cancel_pair((xa, cy), (xb, cy), 0.6, S, '3', '1'))
    b.append(cancel_pair((xb, cy), (xa, cy), 2.4, S, '3', '1'))
    b.append(fi(4.2, op(xb + 52, cy, '=', INK, S) + op(xb + 92, cy, '9', GREEN, 30)))
    w = xb + 124
    return fig(svg(w, 140, ''.join(b), maxw=w), fx=True)


def c1_error1():
    """1.3. Ошибка №1 на числовой оси: 2⅙ левее 2½, а должно быть правее."""
    a, k = 2 + F(1, 2), 1 + F(1, 3)
    wrong = 2 * 1 + F(1, 2) * F(1, 3)
    assert wrong == 2 + F(1, 6) and a * k == 3 + F(1, 3) and wrong < a < a * k and k > 1
    need('`2½ × 1⅓ = 2⅙`', '`3⅓`')
    P, x0, y = 140, -110, 134
    X = lambda v: x0 + float(v) * P
    b = [arrow_defs_p('e1', [GOLD])]
    b.append(line(X(1.6), y, X(3.8), y, MUTED, 1.5))
    for v in (2, 3):
        b.append(line(X(v), y - 6, X(v), y + 6, MUTED, 1.5))
    b.append(f"<circle cx='{X(a)}' cy='{y}' r='6' fill='{GOLD}'/>")
    b.append(mixed(X(a), y - 26, a, GOLD, 18))
    b.append(arrow(X(a) + 4, y - 50, X(a * k) - 2, y - 50, 'e10', GOLD, 2, curve=-56))
    b.append(t((X(a) + X(a * k)) / 2 - 20, y - 94, '×', GOLD, 17, weight=600))
    b.append(mixed((X(a) + X(a * k)) / 2 + 6, y - 100, k, GOLD, 17))
    b.append(f"<circle cx='{X(a*k)}' cy='{y}' r='6' fill='{GREEN}'/>")
    b.append(mixed(X(a * k), y - 26, a * k, GREEN, 18))
    b.append(f"<circle cx='{X(wrong)}' cy='{y}' r='6' fill='{RED}'/>")
    b.append(mixed(X(wrong), y + 28, wrong, RED, 18))
    b.append(t(X(wrong) + 28, y + 36, '✗', RED, 18, weight=700))
    return fig(svg(X(3.8) + 16, y + 50, ''.join(b), maxw=460))


def c1_error2():
    """1.4. Ошибка №2: целые полоски 3¾ режутся на четверти, четверти считаются 1…12, +3 → 15/4; 7/4 короче (статично)."""
    q = 3 + F(3, 4)
    assert q == F(15, 4) and 4 * 3 + 3 == 15 and F(7, 4) < q
    need('`3¾` написать `7/4`', '`4 × 3 + 3`', '`15/4`')
    Q, x0, y1, y2, h = 26, 60, 26, 132, 34
    b = []
    b.append(mixed(30, y1 + h / 2, q, INK, 26))
    for k in range(3):
        b.append(brick(x0 + 4 * k * Q, y1, 4 * Q, h, GOLD, 0.3, GOLD, 1.2, 0))
        for j in range(1, 4):
            xx = x0 + (4 * k + j) * Q
            b.append(drline(xx, y1, xx, y1 + h, 0.5 + 0.35 * k, GOLD, 1.2, 0.4))
    for j in range(12, 15):
        b.append(brick(x0 + j * Q, y1, Q, h, GOLD, 0.3, GOLD, 1.2, 0))
    for k in range(1, 4):
        b.append(line(x0 + 4 * k * Q, y1 - 4, x0 + 4 * k * Q, y1 + h + 4, INK, 2.5))
    for j in range(15):
        d = 1.7 + 0.16 * j if j < 12 else 4.0 + 0.2 * (j - 12)
        b.append(t(x0 + j * Q + Q / 2, y1 + h / 2 + 6, j + 1, INK, 16 if j < 9 else 15, weight=600, cls='fi', d=round(d, 2)))
    b.append(fi(3.7, brace(x0, x0 + 12 * Q, y1 + h + 6, up=False) + t(x0 + 6 * Q, y1 + h + 34, '4 × 3 = 12', INK, 16, weight=600)))
    b.append(fi(4.7, brace(x0 + 12 * Q, x0 + 15 * Q, y1 + h + 6, up=False) + t(x0 + 13.5 * Q, y1 + h + 34, '+ 3', INK, 16, weight=600)))
    b.append(fi(5.2, op(x0 + 15 * Q + 22, y1 + h / 2 - 8, '=', INK, 22) + fr(x0 + 15 * Q + 58, y1 + h / 2 - 8, 15, 4, GREEN, 22)))
    for k in range(7):
        b.append(brick(x0 + k * Q, y2, Q, h, RED, 0.25, RED, 1.2, 0))
    b.append(fr(30, y2 + h / 2 - 8, 7, 4, RED, 22))
    b.append(t(x0 + 7 * Q + 16, y2 + h / 2 + 7, '✗', RED, 20, weight=700))
    w = x0 + 15 * Q + 88
    return fig(svg(w, y2 + h + 12, ''.join(b), maxw=w), fx=True)


# ——————————————————— Глава 2 ———————————————————

def c2_reciprocal():
    """2.1. Обратное число: копия переворачивается карточкой вокруг своей черты."""
    assert F(3, 5) * F(5, 3) == 1 and F(4) * F(1, 4) == 1
    need('обратное к `3/5` — это `5/3`', '`3/5 × 5/3 = 15/15 = 1`', 'Обратное к `4` — это `¼`, ведь `4 = 4/1`')
    S, c1, c2 = 26, 46, 146
    b = [card_css(), arrow_defs_p('c2r', [BLUE])]
    b.append(fr(40, c1, 3, 5, INK, S))
    b.append(arrow(68, c1 + 8, 140, c1 + 8, 'c2r0', BLUE, 2))
    b.append(card_flip(172, c1, 3, 5, 0.8, S))
    b.append(turn_arrow(218, c1 + 6, 14, 0.8, 'c2r0'))
    b.append(t(256, c1 + 8, f"3/5 × 5/3 = 15/15 = <tspan fill='{GREEN}' font-weight='700'>1</tspan>", INK, 18,
               anchor='start', cls='fi', d=2.2))
    src, xr = src_row(16, c2, [('o', '4'), ('o', '='), ('F', 4, 1)], S)
    b.append(src)
    b.append(arrow(xr + 10, c2 + 8, 140, c2 + 8, 'c2r0', BLUE, 2))
    b.append(card_flip(172, c2, 4, 1, 3.2, S))
    b.append(turn_arrow(218, c2 + 6, 14, 3.2, 'c2r0'))
    return fig(svg(490, 196, ''.join(b), maxw=490), fx=True)


def c2_halves():
    """2.2. Слева 3 : ½ =; каждая единица режется на 2 половинки, мерка укладывается 6 раз."""
    assert F(3) / F(1, 2) == 6 == 3 * 2
    need('шесть раз, ведь в каждой единице две половинки', '`3 : ½ = 3 × 2 = 6`')
    U, y, h = 110, 70, 40
    src, xr = src_row(14, y + h / 2, [('o', '3'), ('o', ':'), ('f', 1, 2), ('o', '=')], 26)
    x0 = xr + 16
    b = [src]
    b.append(brick(x0, 18, U / 2, 24, BLUE, 0.3, BLUE, 1.5, 0))
    b.append(t(x0 + U / 2 + 12, 36, 'мерка', MUTED, 16, anchor='start'))
    b.append(fr(x0 + U / 2 + 76, 30, 1, 2, BLUE, 16))
    for k in range(3):
        b.append(empty(x0 + k * U, y, U, h, INK, 2, 0))
        b.append(t(x0 + k * U + U / 2, y + h + 22, '1', MUTED, 16))
    for k in range(3):
        b.append(drline(x0 + k * U + U / 2, y, x0 + k * U + U / 2, y + h, 0.5 + 0.35 * k, BLUE, 2, 0.4))
    for j in range(6):
        x = x0 + j * U / 2
        b.append(fi(1.8 + 0.4 * j, brick(x + 3, y + 3, U / 2 - 6, h - 6, BLUE, 0.3, BLUE, 1, 2)
                    + t(x + U / 4, y + h / 2 + 7, j + 1, INK, 18, weight=700)))
    b.append(fi(4.4, op(x0 + 3 * U + 22, y + h / 2, '=', INK, 26) + op(x0 + 3 * U + 58, y + h / 2, '6', GREEN, 30)))
    w = x0 + 3 * U + 86
    return fig(svg(w, y + h + 32, ''.join(b), maxw=min(w, 640)), fx=True)


def c2_example_a():
    """2.3. Слева 3/8 : 9/10 =; справа 3/8 × 10/9 сокращается: 3–9, 10–8 → 5/12. Переворот — в рисунке идеи главы."""
    assert F(3, 8) / F(9, 10) == F(5, 12) == F(1, 4) * F(5, 3)
    need('`3/8 × 10/9`', '`1/8 × 10/3`', '`1/4 × 5/3`', '`5/12` ✅')
    S, cy = 26, 70
    src, xr = src_row(16, cy, [('F', 3, 8), ('o', ':'), ('F', 9, 10), ('o', '=')], S)
    xa, xb = xr + 46, xr + 150
    b = [src]
    b.append(t(xa, ny(cy, S), 3, INK, S, weight=600, cls='fo', extra=" style='--d:1.0s;--o:0.35'"))
    b.append(t(xa, dy_(cy, S), 8, INK, S, weight=600, cls='fo', extra=" style='--d:2.2s;--o:0.35'"))
    b.append(line(xa - 16, cy, xa + 16, cy, INK, 2))
    b.append(op((xa + xb) / 2, cy, '×', BLUE, S))
    b.append(t(xb, ny(cy, S), 10, BLUE, S, weight=600, cls='fo', extra=" style='--d:2.2s;--o:0.35'"))
    b.append(t(xb, dy_(cy, S), 9, BLUE, S, weight=600, cls='fo', extra=" style='--d:1.0s;--o:0.35'"))
    b.append(line(xb - 20, cy, xb + 20, cy, BLUE, 2))
    b.append(cancel_pair((xa, cy), (xb, cy), 0.6, S, '1', '3'))
    b.append(cancel_pair((xb, cy), (xa, cy), 1.8, S, '5', '4'))
    b.append(fi(3.2, op(xb + 52, cy, '=', INK, S) + fr(xb + 96, cy, 5, 12, GREEN, S)))
    w = xb + 130
    return fig(svg(w, 140, ''.join(b), maxw=w), fx=True)


def row(x, cy, items, size=24, fill=INK, center=True, gap=12):
    """Запись в строку. items: ('m', q) смешанное, ('f', n, d) маленькая дробь (как ⅚ в тексте),
    ('F', n, d) дробь столбиком, ('o', s) знак или целое; у любого пункта последним может стоять цвет.
    Возвращает (svg, центры пунктов, ширина)."""
    small = size * 0.62
    ws = []
    for it in items:
        k = it[0]
        if k == 'm':
            q = it[1]
            w_, r = divmod(q.numerator, q.denominator)
            ws.append(cw(w_, size) + 3 + max(cw(r, small), cw(q.denominator, small)) + 6)
        elif k == 'f':
            ws.append(max(cw(it[1], small), cw(it[2], small)) + 6)
        elif k == 'F':
            ws.append(max(cw(it[1], size), cw(it[2], size)) + 10)
        else:
            ws.append(max(cw(it[1], size), size * 0.55))
    total = sum(ws) + gap * (len(items) - 1)
    cur = x - total / 2 if center else x
    out, cs = [], []
    for it, w in zip(items, ws):
        c = cur + w / 2
        k = it[0]
        if k == 'm':
            col = it[2] if len(it) > 2 else fill
            out.append(mixed(c, cy, it[1], col, size))
        elif k == 'f':
            col = it[3] if len(it) > 3 else fill
            out.append(fr(c, cy - 0.12 * size, it[1], it[2], col, small, w, 1.5))
        elif k == 'F':
            col = it[3] if len(it) > 3 else fill
            out.append(fr(c, cy, it[1], it[2], col, size, w))
        else:
            col = it[2] if len(it) > 2 else fill
            out.append(op(c, cy, it[1], col, size))
        cs.append(c)
        cur += w + gap
    return ''.join(out), cs, total


# ——————————————————— Глава 3 ———————————————————

def c3_piles():
    """3.1. Слева 6/7 : 3 =; полоска стоит, копии шести седьмых съезжают в три кучки по две."""
    assert F(6, 7) / 3 == F(2, 7)
    need('шесть седьмых разложили на три равные кучки. В каждой две седьмых')
    W, y, h, dyp = 44, 30, 36, 96
    src, xr = src_row(14, y + h / 2 - 2, [('F', 6, 7), ('o', ':'), ('o', '3'), ('o', '=')], 24)
    x0 = xr + 16
    b = [src]
    for i in range(7):
        b.append(brick(x0 + i * W, y, W, h, GOLD, 0.45, GOLD, 1.5, 0) if i < 6 else empty(x0 + i * W, y, W, h, MUTED, 1.5, 0))
    for i in range(6):
        k, slot = divmod(i, 2)
        tx = x0 + k * 120 + slot * W
        b.append(fi(0.4 + 0.6 * k, sl(0.6 + 0.6 * k, tx - (x0 + i * W), dyp,
                                       brick(x0 + i * W + 2, y + 2, W - 4, h - 4, GOLD, 0.45, GOLD))))
    for k in range(3):
        b.append(fi(2.8, fr(x0 + k * 120 + W, y + dyp + h + 22, 2, 7, GREEN, 18)))
    w = x0 + 2 * 120 + 2 * W + 20
    return fig(svg(w, y + dyp + h + 52, ''.join(b), maxw=w), fx=True)


def c3_grid():
    """3.2. Слева 3/4 : 5 =; каждую четверть режем на 5 — частей 20, взятых 3."""
    assert F(3, 4) / 5 == F(3, 4) * F(1, 5) == F(3, 20)
    need('`3/4 : 5 = 3/4 × 1/5 = 3/20`', '`3/20` ✅')
    y0, cwid, rh = 50, 64, 34
    src, xr = src_row(14, y0 + 2.5 * rh - 8, [('F', 3, 4), ('o', ':'), ('o', '5'), ('o', '=')], 24)
    x0 = xr + 18
    b = [src]
    for c in range(3):
        b.append(brick(x0 + c * cwid, y0, cwid, 5 * rh, GOLD, 0.22, GOLD, 0, 0))
    b.append(empty(x0, y0, 4 * cwid, 5 * rh, INK, 2, 0))
    for c in range(1, 4):
        b.append(line(x0 + c * cwid, y0, x0 + c * cwid, y0 + 5 * rh, INK, 2))
    b.append(brace(x0, x0 + 3 * cwid, y0 - 6, up=True))
    b.append(fr(x0 + 1.5 * cwid, y0 - 36, 3, 4, GOLD, 16))
    for r in range(1, 5):
        b.append(drline(x0, y0 + r * rh, x0 + 4 * cwid, y0 + r * rh, 0.6 + 0.3 * r, BLUE, 1.6, 0.5))
    b.append(fi(2.6, brick(x0 + 2, y0 + 2, 3 * cwid - 4, rh - 4, GOLD, 0.85, GOLD, 1, 2)))
    b.append(fi(3.2, op(x0 + 4 * cwid + 26, y0 + rh / 2 - 6, '=', INK, 22)
                + fr(x0 + 4 * cwid + 66, y0 + rh / 2 - 6, 3, 20, GREEN, 22)))
    w = x0 + 4 * cwid + 100
    return fig(svg(w, y0 + 5 * rh + 14, ''.join(b), maxw=w), fx=True,
               cap='каждая четверть разрезана на 5 частей: в целом их стало 4 · 5 = 20, а пятая доля трёх четвертей — 3 такие части')


def c3_equal():
    """3.3. 2/7 стоит; внизу каждая седьмая режется на 3 — закрашенное не меняет длины: 2/7 = 6/21."""
    assert F(6, 7) / 3 == F(2, 7) == F(6, 21)
    need('`6/7 : 3 = 6/21`', 'те же `2/7`')
    L, x0, y1, y2, h = 336, 80, 20, 86, 36
    w7, w21 = L / 7, L / 21
    b = []
    for y in (y1, y2):
        for i in range(7):
            b.append(brick(x0 + i * w7, y, w7, h, GOLD, 0.45, GOLD, 1.2, 0) if i < 2 else empty(x0 + i * w7, y, w7, h, MUTED, 1.2, 0))
    for i in range(7):
        for j in (1, 2):
            xx = x0 + i * w7 + j * w21
            b.append(drline(xx, y2, xx, y2 + h, round(0.6 + 0.25 * i, 2), GOLD if i < 2 else MUTED, 1.2, 0.4))
    b.append(fr(40, y1 + h / 2 - 8, 2, 7, INK, 22))
    b.append(fi(2.6, fr(40, y2 + h / 2 - 8, 6, 21, INK, 22)))
    xe = x0 + 2 * w7
    b.append(line(xe, y1 - 8, xe, y2 + h + 8, GREEN, 2, " stroke-dasharray='5 4'"))
    return fig(svg(x0 + L + 20, y2 + h + 14, ''.join(b), maxw=460), fx=True)


# ——————————————————— Глава 4 ———————————————————

def c4_example_a():
    """4.1. Слева 3⅓ : 1⅔ =; справа копия: перевод в 10/3 : 5/3, «:» → «×», 5/3 переворачивается карточкой,
    сокращаются 10–5 и 3–3 → 2."""
    a, b_ = 3 + F(1, 3), 1 + F(2, 3)
    assert a == F(10, 3) and b_ == F(5, 3) and a / b_ == 2
    need('`10/3 : 5/3`', '`10/3 × 3/5`', '`2/1 × 1/1`', '`2` ✅')
    S, cy = 26, 74
    src, xr = src_row(16, cy, [('m', a), ('o', ':'), ('m', b_), ('o', '=')], S)
    xa, xs, xb = xr + 50, xr + 100, xr + 150
    b = [card_css(), src]
    b.append(fo(0.8, mixed(xa, cy, a, INK, S) + mixed(xb, cy, b_, INK, S)))
    b.append(fi(1.1, t(xa, ny(cy, S), 10, INK, S, weight=600, cls='fo', extra=" style='--d:4.1s;--o:0.35'")
                + t(xa, dy_(cy, S), 3, INK, S, weight=600, cls='fo', extra=" style='--d:5.1s;--o:0.35'")
                + line(xa - 22, cy, xa + 22, cy, INK, 2)))
    b.append(fo(0.8, op(xs, cy, ':', INK, S)) + fi(1.1, turn_sign(xs, cy, 2.0, S)))
    b.append(fi(1.1, card_flip(xb, cy, 5, 3, 2.2, S, fade=(5.1, 0.35, 4.1))))
    b.append(cancel_pair((xa, cy), (xb, cy), 3.7, S, '2', '1'))
    b.append(cancel_pair((xb, cy), (xa, cy), 4.7, S, '1', '1'))
    b.append(fi(5.8, op(xb + 52, cy, '=', INK, S) + op(xb + 92, cy, '2', GREEN, 30)))
    w = xb + 124
    return fig(svg(w, 144, ''.join(b), maxw=w), fx=True)


def c4_measure():
    """4.2. Сколько раз 2⅛ помещается в 5¼: дважды, остаток 1, а пол-мерки — чуть больше 1."""
    big, m = 5 + F(1, 4), 2 + F(1, 8)
    assert 2 * m == 4 + F(1, 4) and big - 2 * m == 1 and m / 2 > 1 and big / m == F(42, 17) == 2 + F(8, 17)
    need('Два раза по `2⅛` — это `4¼`', 'до `5¼` остаётся ещё `1`', 'около `2½`', '`2 8/17`')
    U, x0, y, h = 100, 30, 74, 32
    X = lambda v: x0 + float(v) * U
    b = []
    b.append(empty(X(0), y, float(big) * U, h, INK, 2, 0))
    for v in range(6):
        b.append(line(X(v), y + h, X(v), y + h + 6, MUTED, 1.2) + t(X(v), y + h + 20, v, MUTED, 12))
    b.append(mixed(X(big), y - 14, big, INK, 16))
    for k in range(2):
        d = 0.6 + 1.1 * k
        stick = brick(X(k * m) + 1, 22, float(m) * U - 2, h - 6, BLUE, 0.35, BLUE, 1.5, 3) + mixed(X(k * m + m / 2), 22 + (h - 6) / 2, m, INK, 16)
        b.append(fi(d - 0.4, sl(d, 0, y + 3 - 22, stick)))
    b.append(fi(3.0, brick(X(2 * m) + 2, y + 3, U - 4, h - 6, GOLD, 0.55, GOLD, 1.5, 3)
                + t(X(2 * m + F(1, 2)), y + h / 2 + 6, '1', DARK, 17, weight=700)))
    hx = X(2 * m)
    b.append(fi(3.9, empty(hx, y + h + 30, float(m / 2) * U, 18, BLUE, 1.6, 3, '5 3')
                + t(hx - 8, y + h + 44, 'половина 2⅛', BLUE, 14, anchor='end')))
    b.append(fi(3.9, line(X(big), y - 4, X(big), y + h + 52, MUTED, 1, " stroke-dasharray='3 3'")))
    b.append(fi(4.9, t(X(0), y + h + 82, 'около', GOLD, 17, anchor='start', weight=600)
                + mixed(X(0) + 70, y + h + 76, F(5, 2), GOLD, 20)))
    return fig(svg(X(big) + 30, y + h + 96, ''.join(b), maxw=600), fx=True)


# ——————————————————— Глава 5 ———————————————————

NUM5 = [('m', 1 + F(2, 3)), ('o', '+'), ('f', 5, 6)]
DEN5 = [('m', 2 + F(1, 2)), ('o', '−'), ('f', 3, 4)]


def c5_expression():
    """5.1. Дробное выражение — вместо ASCII-блока; длинная черта золотом."""
    need('1⅔ + ⅚', '2½ − ¾')
    cx, S = 150, 26
    top, _, wt = row(cx, 40, NUM5, S)
    bot, _, wb = row(cx, 108, DEN5, S)
    wl = max(wt, wb) + 36
    return fig(svg(300, 146, top + line(cx - wl / 2, 74, cx + wl / 2, 74, GOLD, 3) + bot))


def c5_collapse():
    """5.2. Слева выражение статично; справа копия: числитель → 5/2, знаменатель → 7/4; = 10/7 = 1 3/7."""
    n, d = 1 + F(2, 3) + F(5, 6), 2 + F(1, 2) - F(3, 4)
    assert n == F(5, 2) and d == F(7, 4) and n / d == F(10, 7) == 1 + F(3, 7)
    need('`5/2`', '`7/4`', '`5/2 × 4/7 = 10/7`', '`1 3/7` ✅')
    S = 26
    def expr(cx):
        top, _, wt = row(cx, 40, NUM5, S)
        bot, _, wb = row(cx, 112, DEN5, S)
        return top, bot, wt, wb, max(wt, wb) + 24
    top, bot, wt, wb, wl = expr(16 + 72)
    b = [top, bot, line(88 - wl / 2, 76, 88 + wl / 2, 76, GOLD, 3)]
    b.append(op(88 + wl / 2 + 22, 76, '=', INK, S))
    cx = 88 + wl + 44
    top, bot, wt, wb, wl = expr(cx)
    b.append(line(cx - wl / 2, 76, cx + wl / 2, 76, GOLD, 3))
    b.append(fi(0.4, fo(2.0, empty(cx - wt / 2 - 10, 14, wt + 20, 52, GOLD, 2, 8))))
    b.append(fo(1.4, top) + fi(1.7, fr(cx, 38, 5, 2, INK, 24)))
    b.append(fi(2.4, fo(4.0, empty(cx - wb / 2 - 10, 86, wb + 20, 52, GOLD, 2, 8))))
    b.append(fo(3.4, bot) + fi(3.7, fr(cx, 104, 7, 4, INK, 24)))
    chain, _, cwid = row(cx + wl / 2 + 14, 76, [('o', '='), ('F', 10, 7), ('o', '='), ('m', n / d, GREEN)], 26, center=False)
    b.append(fi(4.6, chain))
    w = cx + wl / 2 + 14 + cwid + 14
    return fig(svg(w, 150, ''.join(b), maxw=min(w, 640)), fx=True)


def c5_storey():
    """5.3. Слева двухэтажная 2/3 над 4/9; справа копия: длинная черта сжимается в «:», этажи расходятся в строку."""
    assert F(2, 3) / F(4, 9) == F(3, 2)
    need('`(2/3) / (4/9)`', '`2/3 × 9/4 = 3/2 = 1½`')
    S, cy = 24, 72
    b = [card_css()]
    b.append(fr(50, 36, 2, 3, INK, S) + line(14, cy, 86, cy, GOLD, 3) + fr(50, 102, 4, 9, INK, S))
    b.append(op(112, cy, '=', INK, S))
    c = 250
    b.append(sl(0.8, -60, cy - 36, fr(c, 36, 2, 3, INK, S)))
    b.append(sl(0.8, 60, cy - 102, fr(c, 102, 4, 9, INK, S)))
    b.append(cls_at('sxo', 0.6, c, cy, line(c - 36, cy, c + 36, cy, GOLD, 3)))
    b.append(fi(1.9, op(c, cy, ':', GOLD, 30)))
    for x in (c - 60, c + 60):
        b.append(fi(2.4, op(x - 21, cy, '(', INK, 30) + op(x + 21, cy, ')', INK, 30)))
    b.append(fi(2.9, t(c - 60, cy + 52, 'дробь', MUTED, 16) + t(c, cy + 52, 'деление', GOLD, 16, weight=600)
                + t(c + 60, cy + 52, 'дробь', MUTED, 16)))
    return fig(svg(c + 100, 140, ''.join(b), maxw=c + 100), fx=True)


def c5_error():
    """5.4. Ошибка: вычеркнуть 5 из слагаемого. Верно: сначала досчитать этажи."""
    need('`5/3 + 5/6`', '`5/2 − 3/4`')
    assert F(5, 3) + F(5, 6) == F(5, 2) and F(5, 2) - F(3, 4) == F(7, 4)
    cx, S = 120, 22
    top, ct, wt = row(cx, 36, [('F', 5, 3), ('o', '+'), ('F', 5, 6)], S)
    bot, cb, wb = row(cx, 112, [('F', 5, 2), ('o', '−'), ('F', 3, 4)], S)
    wl = max(wt, wb) + 24
    b = [top, bot, line(cx - wl / 2, 76, cx + wl / 2, 76, INK, 2.5)]
    b.append(line(ct[0], ny(36, S) - 8, cb[0], ny(112, S) - 8, RED, 1.6, " stroke-dasharray='4 4'"))
    b.append(strike(ct[0], ny(36, S), S) + strike(cb[0], ny(112, S), S))
    b.append(t(cx + wl / 2 + 16, 88, '✗', RED, 30, anchor='start', weight=700))
    gx = 330
    b.append(fr(gx, 36, 5, 2, GREEN, S) + line(gx - 30, 76, gx + 30, 76, GREEN, 2.5) + fr(gx, 104, 7, 4, GREEN, S))
    b.append(t(gx + 44, 88, '✓', GREEN, 26, anchor='start', weight=700))
    return fig(svg(400, 150, ''.join(b)))


# ——————————————————— Глава 6 ———————————————————

def c6_move():
    """6.1. Слева x : 2¼ = 1⅓ статично; справа копия: «: 2¼» переезжает за «=» и становится «× 2¼»; = 3."""
    q, k = 1 + F(1, 3), 2 + F(1, 4)
    assert q * k == F(4, 3) * F(9, 4) == 3
    need('`x = 1⅓ × 2¼`', '`x = 3` ✅')
    S, cy = 24, 72
    src, cs, ws = row(14, cy, [('o', 'x', GOLD), ('o', ':'), ('m', k), ('o', '='), ('m', q)], S, center=False)
    b = [src, t(cs[0], cy + 42, 'делимое', GOLD, 16)]
    o = 14 + ws + 48
    b.append(op(o - 24, cy, '⇒', MUTED, 22))
    X = lambda v: o + v
    b.append(op(X(14), cy, 'x', GOLD, S))
    grp = fo(4.4, op(X(46), cy, ':', BLUE, S)) + mixed(X(86), cy, k, BLUE, S)
    b.append(sl(3.0, 0, 40, sl(1.7, 88, 0, sl(0.4, 0, -40, grp))))
    b.append(fi(4.4, op(X(134), cy, '×', BLUE, S)))
    b.append(sl(1.7, -84, 0, op(X(130), cy, '=', INK, S) + mixed(X(174), cy, q, INK, S)))
    b.append(fi(5.0, op(X(218), cy, '=', INK, S) + op(X(250), cy, '3', GREEN, 28)))
    w = X(276)
    return fig(svg(w, 124, ''.join(b), maxw=min(w, 640)), fx=True)


def c6_substitute():
    """6.2. Слева x × 3/5 = 9/10 статично; справа на место x опускается 1½; под копией проверка ✓."""
    x = F(3, 2)
    assert x * F(3, 5) == F(9, 10)
    need('`x × 3/5 = 9/10`', '`3/2 × 3/5 = 9/10` — сошлось')
    S, cy, cy2 = 24, 66, 146
    src, _, ws = row(14, cy, [('o', 'x', GOLD), ('o', '×'), ('F', 3, 5), ('o', '='), ('F', 9, 10)], S, center=False)
    o = 14 + ws + 50
    b = [src, op(o - 25, cy, '⇒', MUTED, 22)]
    b.append(fo(0.8, op(o + 18, cy, 'x', GOLD, S)))
    b.append(fi(0.3, sl(1.0, 0, 44, mixed(o + 18, cy - 44, x, GREEN, S))))
    rest, _, wr = row(o + 44, cy, [('o', '×'), ('F', 3, 5), ('o', '='), ('F', 9, 10)], S, center=False)
    b.append(rest)
    chk, _, wc = row(o, cy2, [('F', 3, 2), ('o', '×'), ('F', 3, 5), ('o', '='), ('F', 9, 10)], S, center=False)
    b.append(fi(2.6, chk))
    b.append(t(o + wc + 16, cy2 + 9, '✓', GREEN, 26, anchor='start', weight=700, cls='fi', d=3.4))
    w = max(o + 44 + wr, o + wc + 40) + 14
    return fig(svg(w, 190, ''.join(b), maxw=min(w, 640)), fx=True)


def c6_sides():
    """6.3. С какой стороны от «:» стоит x — делимое или делитель."""
    need('`x : 5 = 3`', '`12 : x = 3`', '`x = 12 : 3 = 4`')
    S = 24
    b = []
    for cy, items, word, rule in ((40, [('o', 'x', GOLD), ('o', ':', INK), ('o', '5'), ('o', '='), ('o', '3')], 'делимое', 'x = 3 × 5'),
                                  (110, [('o', '12'), ('o', ':', INK), ('o', 'x', GOLD), ('o', '='), ('o', '3')], 'делитель', 'x = 12 : 3')):
        r, cs, _ = row(30, cy, items, S, center=False, gap=14)
        b.append(r)
        b.append(t(240, cy + 8, word, GOLD, 17, anchor='start', weight=600))
        b.append(t(330, cy + 8, '→  ' + rule, INK, 18, anchor='start'))
    return fig(svg(470, 150, ''.join(b)))


# ——————————————————— Глава 7 ———————————————————

def c7_bar(known_whole):
    """7.1 / 7.2. Класс = 8 кирпичиков, мальчики = 3 из них; в кирпичике 5."""
    whole, part, k, n = 40, 15, 3, 8
    assert whole * F(k, n) == part and F(part) / F(k, n) == whole and whole // n == part // k == 5
    need('`40/1 × 3/8 = 5/1 × 3/1`', '`15` мальчиков', '`5 × 8 = 40` учеников')
    W, x0, y, h = 52, 30, 76, 40
    one = whole // n
    b = []
    for i in range(n):
        b.append(brick(x0 + i * W, y, W, h, GOLD, 0.5, GOLD) if i < k else empty(x0 + i * W, y, W, h, MUTED, 1.5, 2))
    cxw = x0 + n * W / 2
    b.append(brace(x0, x0 + n * W, 50, up=True))
    b.append(t(cxw + 4, 22, 'весь класс —', MUTED, 16, anchor='end'))
    b.append(t(x0 + k * W / 2, 68, 'мальчики', MUTED, 15))
    b.append(fr(x0 + k * W / 2, y + h + 22, k, n, GOLD, 16))
    if known_whole:
        b.append(t(cxw + 12, 22, whole, INK, 18, anchor='start', weight=700))
        for i in range(n):
            b.append(t(x0 + i * W + W / 2, y + h / 2 + 6, one, INK, 17, weight=600, cls='fi', d=0.6 + 0.2 * i))
        b.append(fi(2.6, brace(x0, x0 + k * W, y + h + 50, up=False)
                    + t(x0 + k * W / 2, y + h + 90, part, GREEN, 22, weight=700)))
        hgt = y + h + 100
    else:
        b.append(fo(3.6, t(cxw + 12, 22, '?', INK, 18, anchor='start', weight=700)))
        b.append(t(cxw + 12, 22, whole, GREEN, 20, anchor='start', weight=700, cls='fi', d=3.8))
        b.append(fo(1.0, t(x0 + k * W / 2, y + h / 2 + 7, part, INK, 20, weight=700)))
        for i in range(n):
            d = 1.3 if i < k else 2.0 + 0.2 * (i - k)
            b.append(t(x0 + i * W + W / 2, y + h / 2 + 6, one, INK, 17, weight=600, cls='fi', d=d))
        # данное остаётся в финальном кадре: скобка под тремя кирпичиками
        b.append(brace(x0, x0 + k * W, y + h + 50, up=False)
                 + t(x0 + k * W / 2 + 4, y + h + 90, 'мальчики —', MUTED, 16, anchor='end')
                 + t(x0 + k * W / 2 + 12, y + h + 90, part, GOLD, 20, anchor='start', weight=700))
        hgt = y + h + 100
    return fig(svg(x0 + n * W + 30, hgt, ''.join(b)), fx=True)


# ——————————————————— Глава 8 ———————————————————

def c8_chain():
    """8.1. 240 → первый день 1/4 (60) → остаток 180 становится новым целым → 2/5 (72) → осталось 108."""
    book = 240
    d1 = book * F(1, 4); rest = book - d1; d2 = rest * F(2, 5); left = rest - d2
    assert (d1, rest, d2, left) == (60, 180, 72, 108) and book * F(3, 4) == rest and rest * F(3, 5) == left
    need('`240 × 1/4 = 60`', '`240 − 60 = 180`', '`180 × 2/5 = 72`', '`180 − 72 = 108`', '`180 × 3/5 = 108`')
    Q, x0, y1, y2, h = 100, 40, 60, 190, 40
    q2 = Q * 3 / 5
    b = []
    for i in range(4):
        b.append(brick(x0 + i * Q, y1, Q, h, GOLD, 0.3, GOLD, 1.5, 0))
    b.append(t(x0 + 2 * Q, 22, f'книга — {book}', MUTED, 15))
    b.append(fi(0.6, t(x0 + Q / 2, y1 - 10, '1-й день', MUTED, 14) + t(x0 + Q / 2, y1 + h / 2 + 6, int(d1), INK, 17, weight=600)
                + fr(x0 + Q / 2, y1 + h + 20, 1, 4, INK, 15)))
    b.append(fi(1.0, brick(x0, y1, Q, h, GREY, 0.75, GREY, 1.5, 0) + t(x0 + Q / 2, y1 + h / 2 + 6, int(d1), INK, 17, weight=600)))
    b.append(fi(1.4, t(x0 + 2.5 * Q, y1 - 10, 'остаток', MUTED, 14) + t(x0 + 2.5 * Q, y1 + h / 2 + 6, int(rest), INK, 17, weight=600)
                + fr(x0 + 2.5 * Q, y1 + h + 20, 3, 4, INK, 15)))
    copy = brick(x0 + Q, y1, 3 * Q, h, GOLD, 0.3, GOLD, 2, 0) + fo(3.9, t(x0 + 2.5 * Q, y1 + h / 2 + 6, int(rest), INK, 17, weight=600))
    b.append(fi(2.0, sl(2.2, -Q, y2 - y1, copy)))
    for k in range(1, 5):
        if k == 1:
            b.append(drline(x0 + q2, y2, x0 + q2, y2 + 9, 3.6, GOLD, 1.5, 0.4)
                     + drline(x0 + q2, y2 + h - 9, x0 + q2, y2 + h, 3.6, GOLD, 1.5, 0.4))
        else:
            b.append(drline(x0 + k * q2, y2, x0 + k * q2, y2 + h, 3.6 + 0.12 * k, GOLD, 1.5, 0.4))
    b.append(fi(4.4, brick(x0, y2, 2 * q2, h, GREY, 0.75, GREY, 1.5, 0) + t(x0 + q2, y2 - 10, '2-й день', MUTED, 14)
                + t(x0 + q2, y2 + h / 2 + 6, int(d2), INK, 17, weight=600) + fr(x0 + q2, y2 + h + 20, 2, 5, INK, 15)))
    b.append(fi(5.2, brick(x0 + 2 * q2, y2, 3 * q2, h, GREEN, 0.35, GREEN, 2, 0) + t(x0 + 3.5 * q2, y2 - 10, 'осталось', MUTED, 14)
                + t(x0 + 3.5 * q2, y2 + h / 2 + 7, int(left), INK, 19, weight=700) + fr(x0 + 3.5 * q2, y2 + h + 20, 3, 5, INK, 15)))
    return fig(svg(x0 + 4 * Q + 40, y2 + h + 50, ''.join(b), maxw=480), fx=True)


def c8_error():
    """8.2. 2/5 от 240 (96) против 2/5 от остатка 180 (72) — в одном масштабе."""
    assert 240 * F(2, 5) == 96 and 180 * F(2, 5) == 72
    need('`240 × 2/5 = 96` вместо 72')
    s, x0, y1, y2, h = F(400, 240), 30, 40, 150, 40
    b = []
    for y, tot, col, mark, word in ((y1, 240, RED, '✗', 'вся книга — 240'), (y2, 180, GREEN, '✓', 'остаток — 180')):
        w = float(tot * s) / 5
        for i in range(5):
            if i >= 2:
                b.append(empty(x0 + i * w, y, w, h, MUTED, 1.5, 0))
        b.append(block(x0, y, 2, w, h, col))
        b.append(t(x0, y - 12, word, MUTED, 15, anchor='start'))
        b.append(t(x0 + w, y + h / 2 + 7, int(tot * F(2, 5)), INK, 19, weight=700))
        b.append(fr(x0 + w, y + h + 25, 2, 5, col, 15))
        b.append(t(x0 + 5 * w + 14, y + h / 2 + 8, mark, col, 22, anchor='start', weight=700))
    return fig(svg(x0 + 400 + 50, y2 + h + 52, ''.join(b), maxw=480))


# ——————————————————— Глава 9 ———————————————————

def c9_backwards():
    """9.1. С конца: 10 —+4→ 14 —:2/3→ 21; сверху — как действовали вперёд."""
    assert 21 * F(2, 3) == 14 and 14 - 4 == 10 and (10 + 4) / F(2, 3) == 21
    need('`10 + 4 = 14`', '`14 : 2/3 = 21`')
    xs, cy, bw, bh = [60, 245, 430], 70, 64, 38
    b = [arrow_defs_p('c9b', [MUTED, BLUE])]
    for x in xs:
        b.append(empty(x - bw / 2, cy - bh / 2, bw, bh, INK, 1.8, 8))
    b.append(op(xs[2], cy, '10', INK, 20))
    b.append(fo(1.8, op(xs[1], cy, '?', MUTED, 20)) + fi(1.9, op(xs[1], cy, '14', BLUE, 20)))
    b.append(fo(3.6, op(xs[0], cy, '?', MUTED, 20)) + fi(3.7, op(xs[0], cy, '21', GREEN, 22)))
    for (xa, xb), lab in (((xs[0], xs[1]), '× 2/3'), ((xs[1], xs[2]), '− 4')):
        b.append(arrow(xa + bw / 2 + 4, cy, xb - bw / 2 - 6, cy, 'c9b0', MUTED, 1.8))
        b.append(t((xa + xb) / 2, cy - 12, lab, MUTED, 16))
    for (xa, xb), lab, d in (((xs[2], xs[1]), '+ 4', 0.8), ((xs[1], xs[0]), ': 2/3', 2.6)):
        b.append(fi(d, arrow(xa - 10, cy + bh / 2 + 4, xb + 10, cy + bh / 2 + 6, 'c9b1', BLUE, 2.2, curve=46)
                    + t((xa + xb) / 2, cy + bh / 2 + 52, lab, BLUE, 17, weight=700)))
    return fig(svg(490, 150, ''.join(b)), fx=True)


def c9_tank():
    """9.2. Бак = 12 кирпичиков: 1/3 и 1/4 взяли, осталось 5/12 — это 25 л; бак 60 л."""
    left = 1 - F(1, 3) - F(1, 4)
    assert left == F(5, 12) and 25 / left == 60 and 12 * F(1, 3) == 4 and 12 * F(1, 4) == 3
    need('`1 − 1/3 − 1/4 = 5/12`', '`25 : 5/12 = 60`')
    W, x0, y, h = 36, 30, 84, 40
    b = []
    for i in range(7):
        b.append(brick(x0 + i * W, y, W, h, GOLD, 0.3, GOLD, 1.2, 0))
    b.append(block(x0 + 7 * W, y, 5, W, h, GOLD, 0.3, 1.2))
    b.append(brace(x0, x0 + 12 * W, 54, up=True))
    b.append(t(x0 + 6 * W + 4, 26, 'бак —', MUTED, 16, anchor='end'))
    b.append(fo(3.5, t(x0 + 6 * W + 12, 26, '?', INK, 18, anchor='start', weight=700)))
    b.append(t(x0 + 6 * W + 12, 26, '60 л', GREEN, 19, anchor='start', weight=700, cls='fi', d=3.7))
    for (a, n), (fn, fd), d in (((0, 4), (1, 3), 0.6), ((4, 3), (1, 4), 1.5)):
        b.append(fi(d, brick(x0 + a * W, y, n * W, h, GREY, 0.8, GREY, 1.2, 0)
                    + t(x0 + (a + n / 2) * W, y - 8, 'взяли', MUTED, 14) + fr(x0 + (a + n / 2) * W, y + h + 20, fn, fd, INK, 15)))
    b.append(fi(2.5, empty(x0 + 7 * W, y, 5 * W, h, GOLD, 3, 0) + t(x0 + 9.5 * W, y - 8, 'осталось', MUTED, 14)
                + t(x0 + 9.5 * W, y + h / 2 + 7, '25 л', INK, 19, weight=700) + fr(x0 + 9.5 * W, y + h + 20, 5, 12, GOLD, 15)))
    return fig(svg(x0 + 12 * W + 30, y + h + 50, ''.join(b), maxw=500), fx=True)


def c9_times():
    """9.3. Во сколько раз 2¼ больше ¾: мерка ¾ укладывается 3 раза."""
    a, m = 2 + F(1, 4), F(3, 4)
    assert a / m == 3
    need('`9/4 : 3/4 = 9/4 × 4/3 = 3` раза')
    U, x0, y, h = 160, 70, 96, 34
    X = lambda v: x0 + float(v) * U
    b = []
    b.append(empty(X(0), y, float(a) * U, h, INK, 2, 0))
    for j in range(1, 9):
        b.append(line(X(F(j, 4)), y, X(F(j, 4)), y + h, INK if j % 4 == 0 else MUTED, 2 if j % 4 == 0 else 0.8))
    b.append(mixed(36, y + h / 2, a, INK, 22))
    b.append(brick(x0, 18, float(m) * U / 3, 18, BLUE, 0.35, BLUE, 1.2, 2) + t(x0 + float(m) * U / 3 + 10, 32, 'мерка', MUTED, 14, anchor='start')
             + fr(x0 + float(m) * U / 3 + 70, 26, 3, 4, BLUE, 13))
    for k in range(3):
        d = 0.6 + 0.9 * k
        stick = brick(X(k * m) + 2, 50, float(m) * U - 4, h - 8, BLUE, 0.7, BLUE, 1.5, 3) + t(X(k * m + m / 2), 50 + (h - 8) / 2 + 6, k + 1, INK, 17, weight=700)
        b.append(fi(d - 0.3, sl(d, 0, y + 4 - 50, stick)))
    b.append(t(X(a) + 16, y + h / 2 + 7, 'в 3 раза', GREEN, 19, anchor='start', weight=700, cls='fi', d=3.6))
    return fig(svg(X(a) + 110, y + h + 14, ''.join(b), maxw=560), fx=True)


def c9_error():
    """9.4. 1/4 бака и 1/4 остатка — разные куски."""
    assert 12 * F(1, 4) == 3 and (12 - 4) * F(1, 4) == 2
    need('`1/3` бака и `1/4` **остатка** складывать нельзя')
    W, x0, y1, y2, h = 30, 130, 34, 96, 34
    b = [t(x0 + 2 * W, y1 - 10, '1/3 бака', MUTED, 14)]
    for y, n, col, lab in ((y1, 3, GOLD, '1/4 бака'), (y2, 2, BLUE, '1/4 остатка')):
        for i in range(12):
            if i < 4:
                b.append(brick(x0 + i * W, y, W, h, GREY, 0.8, GREY, 1.2, 0))
            elif i < 4 + n:
                b.append(brick(x0 + i * W, y, W, h, col, 0.5, col, 1.2, 0))
            else:
                b.append(empty(x0 + i * W, y, W, h, MUTED, 1.2, 0))
        b.append(t(x0 - 14, y + h / 2 + 6, lab, col, 16, anchor='end', weight=600))
        b.append(line(x0 + (4 + n) * W, y - 6, x0 + (4 + n) * W, y + h + 6, col, 2.5))
    return fig(svg(x0 + 12 * W + 20, y2 + h + 14, ''.join(b), maxw=520))


FIGS = {
    'Важно: в произведении дробей сокращать можно любое верхнее число с любым нижним': r1_big_fraction,
    'Ритуал 3 — причеши ответ': r2_tidy,
    'Ритуал 4 — прикидка': r3_estimate,
    'Что такое смешанное число.': c1_pizzas,
    'сокращаю 12 и 4 (оба на 4)': c1_example_b,
    'Типичная ошибка №1: перемножить отдельно целые': c1_error1,
    'Типичная ошибка №2: при переводе': c1_error2,
    'Что такое взаимно обратные числа.': c2_reciprocal,
    'Почему так: «сколько раз': c2_halves,
    'Разделить на дробь = умножить на обратную ей': c2_idea_flip,
    'сокращаю 10 и 8 (оба на 2)': c2_example_a,
    'Смысл: 6/7 : 3': c3_piles,
    'умножаю знаменатель на 5': c3_grid,
    'Если числитель делится на n нацело': c3_equal,
    'перевожу оба 10/3 : 5/3': c4_example_a,
    'Прикидка: вопрос «сколько раз': c4_measure,
    'Это дробь, у которой в числителе или знаменателе стоит не одно число': c5_expression,
    'причёсываю 1 3/7': c5_collapse,
    'Многоэтажная дробь.': c5_storey,
    'Типичная ошибка: сокращать с отдельным слагаемым': c5_error,
    'x — делимое, значит умножаю': c6_move,
    'Ритуал 5 — проверка подстановкой': c6_substitute,
    'Последние два легко перепутать': c6_sides,
    'ищу часть → умножаю': lambda: c7_bar(True),
    'ищу целое → делю': lambda: c7_bar(False),
    'второй день: 2/5 от остатка': c8_chain,
    'Типичная ошибка: взять вторую дробь от исходного числа': c8_error,
    'Идём с конца.': c9_backwards,
    'потом 1/4 от всего бака': c9_tank,
    '9/4 : 3/4 = 9/4 × 4/3 = 3 раза': c9_times,
    'Типичная ошибка: складывать доли, взятые от разного целого': c9_error,
}


if __name__ == '__main__':
    out = {}
    for anchor, f in FIGS.items():
        hits = [b for b in BLOCKS if anchor in b]
        assert len(hits) == 1, f'якорь «{anchor}» встречается в {len(hits)} абзацах'
        out[anchor] = f()
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(out), 'рисунков,', sum('class="fx"' in v for v in out.values()), 'анимаций →', os.path.relpath(VIS))
