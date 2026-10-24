#!/usr/bin/env python3
"""Иллюстрации главы 3 «Правило деления» → nandu_n2_kombinatorika_uchebnik.vis.json.

Язык главы 2 продолжается: у каждого ребёнка свой цвет; у буквы слова свой цвет, у номера буквы
(А₁, А₂, А₃) — свой цвет до стирания, после стирания одинаковые буквы одного цвета; склеенное гаснет.
Анимируется только переход (правило 15): два письма съезжаются в одно рукопожатие, номера стираются
и записи склеиваются, одни и те же галочки считаются по столбцам, потом по строкам.

Запуск: python3 26-27/nandu_level2/kombinatorika/vis/glava_3.py
"""
import json, os
from itertools import permutations

from glava_2 import svg, fig, t, g, GOLD, BLUE, GREEN, RED, VIOLET, GREY

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.vis.json')

CYAN, PINK, LIME = '#4fd1d9', '#f78fb3', '#a3d65c'
KIDS = [('А', BLUE), ('Б', GOLD), ('В', GREEN), ('Г', RED), ('Д', VIOLET),
        ('Е', CYAN), ('Ж', PINK), ('З', LIME), ('И', '#f5c26b'), ('К', '#8fa8ff')]
DARK = '#0d1117'


def kid(cx, cy, i, r=17, size=15):
    letter, col = KIDS[i]
    return f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{col}'/>" + t(cx, cy + size * 0.33, letter, DARK, size, weight=700)


def arrow_defs(cols):
    return '<defs>' + ''.join(
        f"<marker id='ah{k}' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'>"
        f"<path d='M0,0 L10,5 L0,10 z' fill='{c}'/></marker>" for k, c in enumerate(cols)) + '</defs>'


# ——— 1. Пример 1: два письма съезжаются в одно рукопожатие ———

def letters():
    import math
    cx, cy, R = 300, 165, 120
    order = [0, 2, 3, 4, 5, 1, 6, 7, 8, 9]       # Аня слева, Боря справа
    pos = {}
    for k, i in enumerate(order):
        a = math.pi + 2 * math.pi * k / 10
        pos[i] = (cx + R * math.cos(a), cy - R * math.sin(a))
    (ax, ay), (bx, by) = pos[0], pos[1]
    b = [arrow_defs([BLUE, GOLD])]
    up = (f"<path d='M{ax+20} {ay-8} Q {cx} {cy-80} {bx-20} {by-8}' fill='none' stroke='{BLUE}' "
          f"stroke-width='3' marker-end='url(#ah0)'/>" + t(cx, cy - 52, 'письмо А → Б', BLUE, 15, weight=700))
    down = (f"<path d='M{bx-20} {by+8} Q {cx} {cy+80} {ax+20} {ay+8}' fill='none' stroke='{GOLD}' "
            f"stroke-width='3' marker-end='url(#ah1)'/>" + t(cx, cy + 66, 'письмо Б → А', GOLD, 15, weight=700))
    b.append(g('sl', 1.2, g('fo', 2.0, up), ';--to:translate(0px,40px)'))
    b.append(g('sl', 1.2, g('fo', 2.0, down), ';--to:translate(0px,-40px)'))
    b.append(g('fi', 2.3, f"<line x1='{ax+18}' y1='{ay}' x2='{bx-18}' y2='{by}' stroke='var(--ink)' "
                          f"stroke-width='4'/>" + t(cx, cy - 10, 'одно рукопожатие', 'var(--ink)', 16, weight=700)))
    for i, (x, y) in pos.items():
        b.append(kid(x, y, i))
    b.append(t(300, 330, '90 писем : 2 = 45 рукопожатий', 'var(--ink)', 18, weight=600, cls='fi', d=3.2))
    return fig(svg(600, 344, ''.join(b), maxw=520), fx=True)


# ——— 2. Лесенка: у каждого — рукопожатия с теми, кто дальше по списку ———

def ladder():
    b = []
    for r in range(9):
        y = 22 + r * 34
        b.append(kid(26, y, r, r=14, size=13))
        b.append(t(52, y + 5, '—', size=14))
        for k, j in enumerate(range(r + 1, 10)):
            b.append(kid(84 + (r + k) * 34, y, j, r=13, size=12))
        b.append(t(84 + 10 * 34, y + 5, str(9 - r), GOLD, 17, anchor='start', weight=700))
    b.append(t(14, 22 + 9 * 34 + 14, 'рукопожатий: 9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1 = 45', 'var(--ink)', 17,
               anchor='start', weight=600))
    return fig(svg(470, 350, ''.join(b), maxw=470),
               'каждый пожимает руку тем, кто стоит дальше в списке: тех, кто раньше, он уже встретил')


# ——— плитки букв ———

TW, TH = 24, 30
LCOL = {'Л': VIOLET, 'В': GREEN, 'У': RED, 'С': PINK, 'А': CYAN, 'Н': LIME}
NCOL = {('А', '1'): BLUE, ('А', '2'): GOLD, ('А', '3'): GREEN, ('Н', '1'): RED, ('Н', '2'): VIOLET}


def tile(x, y, tok, erase_at=None):
    """Плитка буквы. tok = 'Л' или 'А1'; erase_at — когда стирается номер (плитка перекрашивается в цвет буквы)."""
    ch, num = tok[0], tok[1:]
    if not num:
        return (f"<rect x='{x}' y='{y}' width='{TW}' height='{TH}' rx='4' fill='{LCOL[ch]}'/>"
                + t(x + TW / 2, y + 21, ch, DARK, 16, weight=700))
    numbered = (f"<rect x='{x}' y='{y}' width='{TW}' height='{TH}' rx='4' fill='{NCOL[(ch, num)]}'/>"
                + t(x + TW / 2 - 3, y + 21, ch, DARK, 16, weight=700)
                + t(x + TW - 5, y + 26, num, DARK, 10, weight=700))
    plain = (f"<rect x='{x}' y='{y}' width='{TW}' height='{TH}' rx='4' fill='{LCOL[ch]}'/>"
             + t(x + TW / 2, y + 21, ch, DARK, 16, weight=700))
    return numbered + g('fi', erase_at, plain)


def word(x, y, toks, erase=None):
    erase = erase or {}
    return ''.join(tile(x + k * (TW + 2), y, tok, erase.get(tok[0])) for k, tok in enumerate(toks))


# ——— 3. Пример 2 б: стёрли номера — каждая пара склеилась ———

def lava():
    toks = ['Л', 'А1', 'В', 'А2']
    seen, pairs = set(), []
    for p in permutations(toks):
        plain = ''.join(x[0] for x in p)
        if plain in seen:
            continue
        seen.add(plain)
        q = tuple({'А1': 'А2', 'А2': 'А1'}.get(x, x) for x in p)
        pairs.append((p, q))
    pairs.sort(key=lambda pq: ''.join(x[0] for x in pq[0]))
    ww = 4 * (TW + 2)
    gap, colw = 18, 2 * ww + 18 + 34
    b = []
    for n, (p, q) in enumerate(pairs):
        x, y = 12 + (n % 3) * colw, 14 + (n // 3) * 50
        b.append(g('fo', 3.8, f"<rect x='{x-6}' y='{y-6}' width='{2*ww+gap+10}' height='{TH+12}' rx='8' "
                              f"fill='none' stroke='var(--line)' stroke-dasharray='4 3'/>"))
        b.append(word(x, y, p, {'А': 1.2}))
        b.append(g('sl', 2.4, g('fo', 3.7, word(x + ww + gap, y, q, {'А': 1.2})),
                   f';--to:translate({-(ww+gap)}px,0px)'))
        b.append(f"<rect x='{x-6}' y='{y-6}' width='{ww+8}' height='{TH+12}' rx='8' fill='none' "
                 f"stroke='{GOLD}' stroke-width='2' class='fi' style='--d:3.9s'/>")
    b.append(t(12, 14 + 4 * 50 + 14, 'было 24 записи с номерами', 'var(--muted)', 15, anchor='start'))
    b.append(t(12, 14 + 4 * 50 + 38, 'стало 12 слов: 24 : 2 = 12', GOLD, 17, anchor='start', weight=700,
               cls='fi', d=4.0))
    return fig(svg(3 * colw, 270, ''.join(b), maxw=3 * colw), fx=True)


# ——— 4. Пример 2 в: склейки одна за другой — 3! записей, потом 2! ———

def ananas():
    dx, dy = 6 * (TW + 2) + 44, 40
    x0, y0 = 14, 14
    b = []
    a_orders = list(permutations(['А1', 'А2', 'А3']))
    n_orders = [('Н1', 'Н2'), ('Н2', 'Н1')]
    for c, (n1, n2) in enumerate(n_orders):
        for r, (a1, a2, a3) in enumerate(a_orders):
            toks = [a1, n1, a2, n2, a3, 'С']
            body = word(x0 + c * dx, y0 + r * dy, toks, {'А': 0.8, 'Н': 4.0})
            if r > 0:
                body = g('sl', 1.8, g('fo', 3.1, body), f';--to:translate(0px,{-r*dy}px)')
            elif c == 1:
                body = g('sl', 5.0, g('fo', 6.3, body), f';--to:translate({-dx}px,0px)')
            b.append(body)
    lx = x0 + 2 * dx + 6
    b.append(t(lx, y0 + 20, 'стёрли номера у А:', 'var(--muted)', 15, anchor='start', cls='fi', d=0.8))
    b.append(t(lx, y0 + 44, 'склеились 3! = 6 записей', GOLD, 16, anchor='start', weight=700, cls='fi', d=3.1))
    b.append(t(lx, y0 + 84, 'стёрли номера у Н:', 'var(--muted)', 15, anchor='start', cls='fi', d=4.0))
    b.append(t(lx, y0 + 108, 'склеились 2! = 2 слова', GOLD, 16, anchor='start', weight=700, cls='fi', d=6.3))
    b.append(t(lx, y0 + 152, 'в одно слово — 3! · 2! = 12', 'var(--ink)', 17, anchor='start', weight=600,
               cls='fi', d=6.8))
    return fig(svg(lx + 250, y0 + 6 * dy, ''.join(b), maxw=lx + 250), fx=True)


# ——— 5. ⚠ суммы: у разных сумм разное число цепочек ———

def sums():
    cols = {s: [(a, s - a) for a in range(1, 6) if 1 <= s - a <= 5 and a != s - a] for s in range(3, 10)}
    W, H = 64, 26
    base = 30 + 4 * H + 30
    b = []
    for k, (s, chains) in enumerate(cols.items()):
        x = 20 + k * W
        for m, (a, c) in enumerate(chains):
            y = base - (m + 1) * (H + 2)
            b.append(f"<rect x='{x}' y='{y}' width='{W-8}' height='{H}' rx='5' fill='var(--bg2)' stroke='var(--line)'/>")
            b.append(t(x + (W - 8) / 2, y + 18, f'{a} + {c}', 'var(--ink)', 14))
        b.append(t(x + (W - 8) / 2, base - len(chains) * (H + 2) - 10, str(len(chains)), GOLD, 17, weight=700))
        b.append(t(x + (W - 8) / 2, base + 22, str(s), 'var(--ink)', 18, weight=700))
    b.append(t(20, base + 50, 'сумма', size=13, anchor='start'))
    return fig(svg(20 + 7 * W, base + 60, ''.join(b), maxw=20 + 7 * W),
               '20 цепочек: у суммы 3 их две, у суммы 5 — четыре; одного m нет')


# ——— 6. Пример 3: одни и те же галочки — по столбцам и по строкам ———

def clubs():
    c = 22
    x0, y0 = 56, 34
    member = {j: {j % 10, (j + 3) % 10, (j + 6) % 10} for j in range(20)}
    b = [t(x0 + 10 * c, 14, 'ребята 1–20', size=13), t(x0 - 8, 14, 'кружки', size=13, anchor='end')]
    for r in range(10):
        b.append(t(x0 - 8, y0 + r * c + 15, str(r + 1), size=11, anchor='end'))
        for j in range(20):
            x, y = x0 + j * c, y0 + r * c
            b.append(f"<rect x='{x}' y='{y}' width='{c}' height='{c}' fill='none' stroke='var(--line)'/>")
            if r in member[j]:
                b.append(f"<path d='M{x+5} {y+11.5} l4.5 5 l8 -10' fill='none' stroke='var(--ink)' "
                         f"stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'/>")
    yb = y0 + 10 * c
    b.append(g('fi', 0.5, f"<rect x='{x0}' y='{y0}' width='{c}' height='{10*c}' fill='none' stroke='{GOLD}' stroke-width='2.5'/>"))
    b.append(g('fi', 0.9, ''.join(t(x0 + j * c + c / 2, yb + 18, '3', GOLD, 14, weight=700) for j in range(20))))
    b.append(t(x0, yb + 44, 'по столбцам: 20 · 3 = 60 галочек', GOLD, 16, anchor='start', weight=700, cls='fi', d=1.5))
    b.append(g('fi', 2.6, f"<rect x='{x0}' y='{y0}' width='{20*c}' height='{c}' fill='none' stroke='{BLUE}' stroke-width='2.5'/>"))
    b.append(g('fi', 3.0, ''.join(t(x0 + 20 * c + 14, y0 + r * c + 16, '6', BLUE, 14, weight=700) for r in range(10))))
    b.append(t(x0, yb + 70, 'по строкам: по 6 в каждой → 60 : 6 = 10 кружков', BLUE, 16, anchor='start', weight=700,
               cls='fi', d=3.6))
    return fig(svg(x0 + 20 * c + 34, yb + 82, ''.join(b), maxw=x0 + 20 * c + 34), fx=True)


# ——— 7. Пример 4: двойка → 6 троек; тройка → 3 двойки ———

CARD = [BLUE, GOLD, GREEN, RED, VIOLET, CYAN, PINK, LIME]


def cards(x, y, nums, w=18, h=26):
    return ''.join(f"<rect x='{x+k*(w+3)}' y='{y}' width='{w}' height='{h}' rx='3' fill='{CARD[n-1]}'/>"
                   + t(x + k * (w + 3) + w / 2, y + 18, str(n), DARK, 13, weight=700) for k, n in enumerate(nums))


def pairs_triples():
    b = [t(130, 18, 'к двойке — любая из 6 оставшихся', 'var(--ink)', 14)]
    b.append(cards(20, 110, [1, 2]))
    for k, extra in enumerate(range(3, 9)):
        y = 34 + k * 34
        b.append(f"<line x1='64' y1='123' x2='150' y2='{y+13}' stroke='var(--muted)'/>")
        b.append(cards(160, y, [1, 2]) + cards(160 + 2 * 21, y, [extra]))
    b.append(t(130, 256, 'пар: N(двоек) · 6', GOLD, 15, weight=700))
    ox = 330
    b.append(t(ox + 120, 18, 'в тройке — 3 двойки', 'var(--ink)', 14))
    b.append(cards(ox + 10, 110, [1, 2, 3]))
    for k, pr in enumerate([(1, 2), (1, 3), (2, 3)]):
        y = 68 + k * 42
        b.append(f"<line x1='{ox+78}' y1='123' x2='{ox+160}' y2='{y+13}' stroke='var(--muted)'/>")
        b.append(cards(ox + 170, y, list(pr)))
    b.append(t(ox + 120, 256, 'пар: N(троек) · 3', GOLD, 15, weight=700))
    return fig(svg(600, 268, ''.join(b), maxw=600))


FIGS = {
    'Каждому рукопожатию соответствуют ровно два письма': letters,
    'Он сделает девять рукопожатий': ladder,
    'Каждые две анаграммы, которые отличались лишь перестановкой букв А₁ и А₂': lava,
    '6! / (3! · 2!) = 720 / 12 = 60': ananas,
    'Одного m нет': sums,
    'N(кружков) = 60 : 6 = 10': clubs,
    'N(троек) = N(двоек) · 2': pairs_triples,
}

if __name__ == '__main__':
    d = json.load(open(VIS))
    import re
    md = open(os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.md')).read()
    plain = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', md))
    new = {anchor: f() for anchor, f in FIGS.items()}
    # вон якоря, ушедшие из текста, и прежние якоря рисунков этой главы, переставленных на новое место
    d = {k: v for k, v in d.items() if k in plain and (k in new or v not in new.values())}
    d.update(new)
    json.dump(d, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(FIGS), 'рисунков →', os.path.relpath(VIS))
