#!/usr/bin/env python3
"""Иллюстрации главы 5 «Соответствие» → nandu_n2_kombinatorika_uchebnik.vis.json.

Цветовой язык: шар (ракушка, пирожок, день отдыха) и его 0 — золотой, перегородка и её 1 — синяя,
пустое — серое; у вида мороженого свой цвет; тренировка — зелёная; в маршруте Г — синие звенья, В — зелёные.
Анимируется только переход (правило 15): шкатулки съезжаются и стенки становятся перегородками;
перегородки опускаются в промежутки между пирожками; маршрут идёт звено за звеном и дописывает слово.

Запуск: python3 26-27/nandu_level2/kombinatorika/vis/glava_5.py
"""
import json, os, re

from glava_2 import svg, fig, t, g, GOLD, BLUE, GREEN, VIOLET, RED, GREY
from glava_3 import DARK

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.vis.json')

S = 40          # ширина одной позиции кода


def ball(cx, cy, r=13):
    return f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{GOLD}'/>"


def bar(cx, y0, y1, w=7):
    return f"<rect x='{cx - w / 2}' y='{y0}' width='{w}' height='{y1 - y0}' rx='3' fill='{BLUE}'/>"


def tile(x, y, ch, w=32):
    one = ch == '1'
    fill = BLUE if one else GOLD
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{w}' rx='6' fill='{fill}'/>"
            + t(x + w / 2, y + w * 0.7, ch, DARK, min(17, round(w * 0.6)), weight=700))


def code_row(x0, y0, code, w=32, gap=8):
    return ''.join(tile(x0 + k * (w + gap), y0, ch, w) for k, ch in enumerate(code))


# ——— 1. Пример 1: шкатулки съезжаются, стенки на стыках — перегородки, раскладка → код ———

def shells():
    x0, y0, h = 30, 40, 52
    counts = [2, 1, 1]
    # итог: шкатулки вплотную, стык первой и второй — на месте 3 кода, второй и третьей — на месте 5
    edges = [(0, 2.5), (2.5, 4.5), (4.5, 6)]
    balls = [[0, 1], [3], [5]]
    shift = [0, 60, 120]           # в начале шкатулки стоят врозь
    b = [t(x0, 20, 'три шкатулки, раскладка 2, 1, 1', 'var(--ink)', 14, anchor='start', weight=700)]
    for i, ((a, z), bs) in enumerate(zip(edges, balls)):
        x = x0 + a * S + shift[i]
        body = (f"<rect x='{x}' y='{y0}' width='{(z - a) * S}' height='{h}' rx='4' fill='none' "
                f"stroke='var(--muted)' stroke-width='2'/>"
                + ''.join(ball(x0 + k * S + S / 2 + shift[i], y0 + h / 2) for k in bs)
                + t(x + (z - a) * S / 2, y0 + h + 18, f'{i + 1}-я', 'var(--muted)', 13))
        b.append(g('sl', 0.6, body, f';--to:translate({-shift[i]}px,0)') if shift[i] else body)
    for s in (2, 4):
        b.append(g('fi', 2.1, bar(x0 + s * S + S / 2, y0 - 8, y0 + h + 8)))
    b.append(t(x0 + 6 * S + 28, y0 + h / 2 - 4, 'стыки шкатулок —', BLUE, 14, anchor='start', cls='fi', d=2.1))
    b.append(t(x0 + 6 * S + 28, y0 + h / 2 + 14, 'две перегородки', BLUE, 14, anchor='start', weight=700,
               cls='fi', d=2.1))
    cy = y0 + h + 44
    b.append(g('fi', 3.0, ''.join(tile(x0 + k * S + 4, cy, ch) for k, ch in enumerate('001010'))))
    b.append(t(x0 + 6 * S + 28, cy + 22, 'код 001010', 'var(--ink)', 16, anchor='start', weight=700,
               cls='fi', d=3.0))
    b.append(t(x0, cy + 66, 'ракушка — 0, перегородка — 1', size=13, anchor='start', cls='fi', d=3.0))
    return fig(svg(560, cy + 78, ''.join(b), maxw=560), fx=True)


# ——— 2. Пример 1: коды с единицей в начале и с единицами рядом — тоже раскладки ———

def mini_boxes(x, y, counts, w=66, h=32, r=6, step=15, label=True):
    """Шкатулки вплотную: общий контур, на стыках синие перегородки — как единицы кода."""
    n = len(counts)
    b = [f"<rect x='{x}' y='{y}' width='{n * w}' height='{h}' rx='4' fill='none' stroke='var(--muted)' "
         f"stroke-width='1.5'/>"]
    for i, c in enumerate(counts):
        bx = x + i * w
        b.append(''.join(ball(bx + (w - (c - 1) * step) / 2 + k * step, y + h / 2, r=r) for k in range(c)))
        if c == 0 and label:
            b.append(t(bx + w / 2, y + h / 2 + 4, 'пусто', GREY, 12))
    for i in range(1, n):
        b.append(bar(x + i * w, y - 4, y + h + 4, w=max(3, round(w / 14))))
    return ''.join(b)


def codes():
    rows = [('000011', [4, 0, 0]), ('100001', [0, 4, 0]), ('110000', [0, 0, 4])]
    b = []
    for r, (cd, cnt) in enumerate(rows):
        y = 12 + r * 50
        b.append(code_row(14, y, cd, w=28, gap=6))
        b.append(t(232, y + 20, '→', 'var(--muted)', 18))
        b.append(mini_boxes(254, y - 2, cnt))
    return fig(svg(480, 162, ''.join(b), maxw=480),
               'единица в начале, в конце или рядом с другой единицей — пустая шкатулка')


# ——— 3. Пример 3: виды мороженого — ящики, код 011001 ———

def icecream():
    kinds = [('шоколадное', '#c58b5c'), ('ванильное', '#e9d9a6'), ('клубничное', '#f78fb3'), ('фисташковое', GREEN)]
    code = '011001'
    x0, y0 = 20, 92
    b = [code_row(x0 + 4, y0, code)]
    # отрезки кода между единицами: вид → какие позиции его
    segs, cur, start = [], 0, 0
    for k, ch in enumerate(code + '1'):
        if ch == '1':
            segs.append((start, k))
            start = k + 1
    for i, ((a, z), (name, col)) in enumerate(zip(segs, kinds)):
        if z > a:
            xa, xb = x0 + a * S, x0 + z * S
            cx = (xa + xb) / 2
            b.append(f"<path d='M{xa+6} {y0-10} V{y0-16} H{xb-2} V{y0-10}' fill='none' stroke='{col}' "
                     f"stroke-width='2.5'/>")
            n = z - a
        else:
            cx = x0 + a * S - 2
            n = 0
        ly = 24 if i % 2 == 0 else 52
        b.append(t(cx, ly, name, col, 13, weight=700))
        b.append(t(cx, ly + 16, f'{n} шт.' if n else 'пусто', col if n else GREY, 12))
    b.append(t(x0 + 6 * S + 20, y0 + 22, 'три 0 — стаканчики, три 1 — перегородки', size=13, anchor='start'))
    return fig(svg(620, 136, ''.join(b), maxw=620))


# ——— 4. Пример 4: перегородки опускаются в два из пяти промежутков ———

def pies():
    x0, y0 = 40, 108
    b = []
    for k in range(6):
        b.append(ball(x0 + k * S * 1.5 + 20, y0, r=15))
    gaps = [x0 + k * S * 1.5 + 20 + S * 0.75 for k in range(5)]
    for k, gx in enumerate(gaps):
        b.append(f"<rect x='{gx-6}' y='{y0+22}' width='12' height='6' rx='2' fill='{GREY}'/>")
        b.append(t(gx, y0 + 46, str(k + 1), 'var(--muted)', 12))
    ex = [x0 - 6, x0 + 5 * S * 1.5 + 46]
    for x in ex:
        b.append(t(x, y0 + 6, '✕', GREY, 16))
    b.append(t(20, 18, 'шесть пирожков в ряд, промежутков пять', 'var(--ink)', 14, anchor='start', weight=700))
    for gi, d in ((1, 0.6), (2, 1.0)):
        gx = gaps[gi]
        b.append(g('sl', d, bar(gx, y0 - 80, y0 - 44), ';--to:translate(0px,58px)'))
    groups = [(0, 2, 'Аня — 2'), (2, 3, 'Боря — 1'), (3, 6, 'Вика — 3')]
    for a, z, s in groups:
        xa = x0 + a * S * 1.5 + 4
        xb = x0 + (z - 1) * S * 1.5 + 36
        b.append(g('fi', 2.6, f"<path d='M{xa} {y0+60} V{y0+66} H{xb} V{y0+60}' fill='none' stroke='{GOLD}' "
                              f"stroke-width='2'/>" + t((xa + xb) / 2, y0 + 86, s, 'var(--ink)', 14, weight=700)))
    b.append(t(20, y0 + 116, 'ни с краю, ни рядом с другой перегородке не встать — пустых тарелок нет', size=13,
               anchor='start', cls='fi', d=2.6))
    return fig(svg(560, y0 + 128, ''.join(b), maxw=560), fx=True)


# ——— 5. Пример 5: пять дней отдыха, шесть мест для тренировок ———

def trainings():
    x0, y0 = 20, 40
    b = [t(x0, 18, 'дни отдыха и шесть мест между ними и по краям', 'var(--ink)', 14, anchor='start', weight=700)]
    chosen = {0, 2, 5}
    x = x0
    for p in range(6):
        on = p in chosen
        b.append(f"<rect x='{x}' y='{y0}' width='30' height='34' rx='6' "
                 + (f"fill='{GREEN}'/>" if on else f"fill='none' stroke='{GREY}' stroke-dasharray='4 3'/>"))
        if on:
            b.append(t(x + 15, y0 + 23, 'Т', DARK, 14, weight=700))
        x += 36
        if p < 5:
            b.append(f"<rect x='{x}' y='{y0}' width='34' height='34' rx='6' fill='var(--bg2)' stroke='var(--line)'/>")
            b.append(t(x + 17, y0 + 23, 'о', 'var(--muted)', 14))
            x += 40
    y1 = y0 + 76
    b.append(t(x0, y1 - 10, 'дни каникул', size=13, anchor='start'))
    days = 'ТооТоооТ'
    for k, ch in enumerate(days):
        xx = x0 + k * 44
        on = ch == 'Т'
        b.append(f"<rect x='{xx}' y='{y1}' width='38' height='34' rx='6' fill='{GREEN if on else 'var(--bg2)'}' "
                 f"stroke='var(--line)'/>")
        b.append(t(xx + 19, y1 + 23, 'Т' if on else 'о', DARK if on else 'var(--muted)', 14, weight=700 if on else None))
        b.append(t(xx + 19, y1 + 52, str(k + 1), 'var(--muted)', 12))
    b.append(t(x0, y1 + 80, 'левый край, 2-й промежуток, правый край → 1-й, 4-й и 8-й дни', 'var(--ink)', 14,
               anchor='start'))
    return fig(svg(440, y1 + 92, ''.join(b), maxw=440), 'Т — тренировка, о — отдых')


# ——— 6. Пример 6: сетка, маршрут, части через M ———

C6, W6, H6 = 56, 5, 2


def grid(x0, y0, labels=True, m=True):
    b = []
    for i in range(W6 + 1):
        b.append(f"<line x1='{x0+i*C6}' y1='{y0}' x2='{x0+i*C6}' y2='{y0+H6*C6}' stroke='var(--line)'/>")
    for j in range(H6 + 1):
        b.append(f"<line x1='{x0}' y1='{y0+j*C6}' x2='{x0+W6*C6}' y2='{y0+j*C6}' stroke='var(--line)'/>")
    if labels:
        b.append(f"<circle cx='{x0}' cy='{y0+H6*C6}' r='5' fill='var(--ink)'/>"
                 + t(x0 - 14, y0 + H6 * C6 + 18, 'A', 'var(--ink)', 16, weight=700))
        b.append(f"<circle cx='{x0+W6*C6}' cy='{y0}' r='5' fill='var(--ink)'/>"
                 + t(x0 + W6 * C6 + 14, y0 - 6, 'D', 'var(--ink)', 16, weight=700))
    if m:
        mx, my = x0 + 2 * C6, y0 + (H6 - 1) * C6
        b.append(f"<circle cx='{mx}' cy='{my}' r='5' fill='{RED}'/>"
                 + t(mx - 12, my - 8, 'M', RED, 16, weight=700))
    return ''.join(b)


def route_task():
    return fig(svg(W6 * C6 + 60, H6 * C6 + 50, grid(26, 22), maxw=W6 * C6 + 60), 'сетка 5 × 2, узел M')


def route():
    x0, y0 = 26, 22
    word = 'ГГВГГВГ'
    b = [grid(x0, y0, m=False)]
    x, y = x0, y0 + H6 * C6
    for k, ch in enumerate(word):
        nx, ny = (x + C6, y) if ch == 'Г' else (x, y - C6)
        col = BLUE if ch == 'Г' else GREEN
        d = 0.4 + 0.45 * k
        b.append(f"<line x1='{x}' y1='{y}' x2='{nx}' y2='{ny}' stroke='{col}' stroke-width='5' stroke-linecap='round' "
                 f"pathLength='100' class='dr' style='--d:{d}s;--dur:.4s'/>")
        b.append(t(x0 + 14 + k * 30, y0 + H6 * C6 + 52, ch, col, 20, weight=700, cls='fi', d=d))
        x, y = nx, ny
    b.append(t(x0 + 7 * 30 + 24, y0 + H6 * C6 + 52, '— 5 букв Г, 2 буквы В', 'var(--muted)', 14,
               anchor='start', cls='fi', d=3.6))
    return fig(svg(W6 * C6 + 80, H6 * C6 + 90, ''.join(b), maxw=W6 * C6 + 80), fx=True)


def route_m():
    x0, y0 = 26, 22
    mx, my = x0 + 2 * C6, y0 + (H6 - 1) * C6
    b = [f"<rect x='{x0}' y='{my}' width='{2*C6}' height='{C6}' fill='{GOLD}' fill-opacity='.22'/>",
         f"<rect x='{mx}' y='{y0}' width='{3*C6}' height='{C6}' fill='{VIOLET}' fill-opacity='.22'/>",
         grid(x0, y0)]
    ty = y0 + H6 * C6 + 40
    b.append(t(x0, ty, 'из A в M: 2 Г и 1 В — C(3, 1) = 3', GOLD, 14, anchor='start', weight=700))
    b.append(t(x0, ty + 22, 'из M в D: 3 Г и 1 В — C(4, 1) = 4', VIOLET, 14, anchor='start', weight=700))
    b.append(t(x0, ty + 48, 'любая первая часть И любая вторая: 3 · 4 = 12', 'var(--ink)', 14, anchor='start'))
    return fig(svg(W6 * C6 + 80, ty + 60, ''.join(b), maxw=W6 * C6 + 80))



# ——— добавлено после чтения родителем: рисунки на каждую трудную мысль примера 1 и раздела ———

def counts_of(code):
    return [len(part) for part in code.split('1')]


def nball(cx, cy, num, col=GOLD, r=13, cls=None, d=None):
    """Шар с номером; номер — отдельным текстом, чтобы его можно было стереть."""
    return (f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{col}'/>"
            + t(cx, cy + 5, str(num), DARK, 14, weight=700, cls=cls, d=d))


def distinct():
    """Вступление: 2 разных шара по 3 ящикам — все 3² = 9 раскладок."""
    cw, ch, x0, y0 = 128, 46, 92, 46
    b = [t(x0 + 1.5 * cw, 18, 'ящик шара 2', 'var(--ink)', 13, weight=700),
         t(22, y0 + 1.5 * ch, 'ящик шара 1', 'var(--ink)', 13, weight=700,
           extra=f" transform='rotate(-90 22 {y0 + 1.5 * ch})'")]
    for j in range(3):
        b.append(t(x0 + j * cw + cw / 2, 38, f'{j + 1}-й', 'var(--muted)', 12))
        b.append(t(x0 - 16, y0 + j * ch + ch / 2 + 4, f'{j + 1}-й', 'var(--muted)', 12))
    for i in range(3):
        for j in range(3):
            cx, cy = x0 + j * cw, y0 + i * ch
            b.append(f"<rect x='{cx}' y='{cy}' width='{cw}' height='{ch}' fill='none' stroke='var(--line)'/>")
            for k in range(3):
                bx = cx + 8 + k * 38
                b.append(f"<rect x='{bx}' y='{cy+9}' width='34' height='28' rx='4' fill='none' "
                         f"stroke='var(--muted)'/>")
                inside = [n for n, box in ((1, i), (2, j)) if box == k]
                for q, n in enumerate(inside):
                    b.append(nball(bx + 17 + (q - (len(inside) - 1) / 2) * 15, cy + 23, n,
                                   BLUE if n == 1 else RED, r=7.5).replace("font-size='14'", "font-size='10'")
                             .replace(f"y='{cy + 28}'", f"y='{cy + 26.5}'"))
    b.append(t(x0, y0 + 3 * ch + 26, 'у каждого шара 3 варианта ящика: 3 · 3 = 3² = 9 раскладок', 'var(--ink)', 14,
               anchor='start', weight=700))
    return fig(svg(x0 + 3 * cw + 16, y0 + 3 * ch + 38, ''.join(b), maxw=x0 + 3 * cw + 16),
               'пример на числах, не из задачи: 2 разных шара, 3 ящика')


def glue():
    """⚠ 81: два способа с номерами ракушек — номера стираются, картинки совпадают."""
    sets = [([1, 2, 3], [4], []), ([2, 3, 4], [1], [])]
    b = []
    for side, boxes in enumerate(sets):
        x0 = 20 + side * 300
        b.append(t(x0 + 126, 18, f'способ {side + 1} из 81', GOLD, 14, weight=700))
        for k, content in enumerate(boxes):
            bx = x0 + k * 86
            b.append(f"<rect x='{bx}' y='34' width='80' height='44' rx='6' fill='none' stroke='var(--muted)' "
                     f"stroke-width='2'/>")
            b.append(t(bx + 40, 96, f'{k + 1}-я', 'var(--muted)', 12))
            for q, n in enumerate(content):
                b.append(nball(bx + 16 + q * 24, 56, n, r=11, cls='fo', d=1.2))
    b.append(t(285, 62, '≠', 'var(--muted)', 24, cls='fo', d=1.2))
    b.append(t(285, 62, '=', 'var(--ink)', 24, weight=700, cls='fi', d=1.9))
    b.append(t(20, 126, 'номера у ракушек — способы разные', 'var(--muted)', 14, anchor='start', cls='fo', d=1.2))
    b.append(t(20, 126, 'ракушки одинаковые: номеров нет — это одна раскладка 3, 1, 0', 'var(--ink)', 14,
               anchor='start', weight=700, cls='fi', d=1.9))
    return fig(svg(580, 138, ''.join(b), maxw=580), fx=True)


def slide_ones():
    """Шесть мест неподвижны, две единицы переезжают — раскладка под ними меняется."""
    from itertools import combinations
    # по порядку: первая единица на месте 1, вторая едет вправо; потом первая на месте 2, …
    frames = [''.join('1' if k in pl else '0' for k in range(6)) for pl in combinations(range(6), 2)]
    x0, y0, w, gap = 24, 34, 34, 8
    b = [t(x0 + k * (w + gap) + w / 2, 22, str(k + 1), 'var(--muted)', 12) for k in range(6)]
    for k in range(6):
        b.append(f"<rect x='{x0 + k*(w+gap) - 3}' y='{y0-3}' width='{w+6}' height='{w+6}' rx='8' fill='none' "
                 f"stroke='var(--line)'/>")
    step = 0.75
    for f, cd in enumerate(frames):
        d = 0.2 + f * step
        places = [str(k + 1) for k, ch in enumerate(cd) if ch == '1']
        body = (code_row(x0, y0, cd, w=w, gap=gap)
                + t(x0 + 6 * (w + gap) + 14, y0 + 14, f'единицы на местах {places[0]} и {places[1]}', BLUE, 14,
                    anchor='start', weight=700)
                + t(x0 + 6 * (w + gap) + 14, y0 + 34, f'№ {f + 1} из 15', 'var(--muted)', 13, anchor='start')
                + mini_boxes(x0, y0 + 56, counts_of(cd)))
        last = f == len(frames) - 1
        b.append(g('fi', d, body if last else g('fo', d + step - 0.1, body)))
    b.append(t(x0, y0 + 128, 'мест всегда шесть; по порядку перебираем, где стоят две единицы', 'var(--ink)', 14,
               anchor='start'))
    return fig(svg(560, y0 + 140, ''.join(b), maxw=560), fx=True)


def all15():
    """Все 15 кодов столбцами по числу ракушек в первой шкатулке — те же 5 + 4 + 3 + 2 + 1."""
    cw, rh, x0, y0 = 132, 64, 10, 40
    b = []
    for c1 in range(5):
        x = x0 + c1 * cw
        b.append(t(x + cw / 2 - 6, 20, f'в первой {c1}', 'var(--ink)', 13, weight=700))
        col = [('0' * c1) + '1' + ('0' * c2) + '1' + ('0' * (4 - c1 - c2)) for c2 in range(4 - c1 + 1)]
        for r, cd in enumerate(col):
            y = y0 + r * rh
            b.append(code_row(x + 4, y, cd, w=16, gap=3))
            b.append(mini_boxes(x + 4, y + 23, counts_of(cd), w=38, h=20, r=3.2, step=7.5, label=False))
        b.append(t(x + cw / 2 - 6, y0 + len(col) * rh + 10, str(len(col)), GOLD, 17, weight=700))
    return fig(svg(x0 + 5 * cw, y0 + 5 * rh + 24, ''.join(b), maxw=x0 + 5 * cw),
               'все 15 кодов: столбец — сколько ракушек в первой шкатулке')


def equation():
    """Пример 2: решение (1, 0, 5) → шары в ящиках x, y, z → код."""
    x0, y0, h = 30, 36, 46
    edges = [(0, 1.5), (1.5, 2.5), (2.5, 8)]
    balls = [[0], [], [3, 4, 5, 6, 7]]
    names = ['x = 1', 'y = 0', 'z = 5']
    b = []
    for (a, z), bs, nm in zip(edges, balls, names):
        b.append(f"<rect x='{x0 + a*S}' y='{y0}' width='{(z-a)*S}' height='{h}' rx='4' fill='none' "
                 f"stroke='var(--muted)' stroke-width='2'/>")
        b.append(''.join(ball(x0 + k * S + S / 2, y0 + h / 2) for k in bs))
        b.append(t(x0 + (a + z) / 2 * S, 22, nm, 'var(--ink)', 14, weight=700))
    for s_ in (1, 2):
        b.append(bar(x0 + s_ * S + S / 2, y0 - 6, y0 + h + 6))
    b.append(''.join(tile(x0 + k * S + 4, y0 + h + 22, ch) for k, ch in enumerate('01100000')))
    b.append(t(x0 + 8 * S + 16, y0 + h + 44, 'код 01100000', 'var(--ink)', 15, anchor='start', weight=700))
    return fig(svg(x0 + 8 * S + 150, y0 + h + 66, ''.join(b), maxw=x0 + 8 * S + 150))


def general():
    """Общий вид кода: k нулей, n − 1 единиц, всего k + n − 1 мест."""
    seq = ['0', '0', '…', '1', '0', '…', '1', '…', '1', '0', '…']
    x0, y0, w = 20, 40, 32
    b = []
    for k, ch in enumerate(seq):
        x = x0 + k * 40
        if ch == '…':
            b.append(t(x + w / 2, y0 + 22, '…', 'var(--muted)', 20, weight=700))
        else:
            b.append(tile(x, y0, ch, w))
    xe = x0 + len(seq) * 40 - 8
    b.append(f"<path d='M{x0} {y0-8} V{y0-14} H{xe} V{y0-8}' fill='none' stroke='var(--ink)' stroke-width='1.5'/>")
    b.append(t((x0 + xe) / 2, y0 - 20, 'всего k + n − 1 мест', 'var(--ink)', 14, weight=700))
    b.append(t(x0, y0 + 62, 'нулей k — по одному на шар', GOLD, 14, anchor='start', weight=700))
    b.append(t(x0, y0 + 84, 'единиц n − 1 — по одной на стык соседних ящиков', BLUE, 14, anchor='start', weight=700))
    return fig(svg(xe + 20, y0 + 96, ''.join(b), maxw=xe + 20), 'общий вид кода')


def wrong_bars():
    """⚠ n − 1: две перегородки — три части; три перегородки — четыре части."""
    rows = [('001010', 'две перегородки — три шкатулки', None), ('0010101', 'три перегородки — четыре части', 3)]
    b = []
    for r, (cd, lbl, extra) in enumerate(rows):
        y = 34 + r * 92
        b.append(t(20, y - 12, lbl, 'var(--ink)' if extra is None else RED, 14, anchor='start', weight=700))
        b.append(code_row(20, y, cd, w=30, gap=6))
        parts, start = [], 0
        for k, ch in enumerate(cd + '1'):
            if ch == '1':
                parts.append((start, k))
                start = k + 1
        for i, (a, z) in enumerate(parts):
            xa = 20 + a * 36
            xb = 20 + z * 36 - 6 if z > a else xa + 24
            col = RED if i == extra else 'var(--muted)'
            b.append(f"<path d='M{xa} {y+38} V{y+44} H{xb} V{y+38}' fill='none' stroke='{col}' stroke-width='1.5'/>")
            b.append(t((xa + xb) / 2, y + 60, f'{i + 1}-я' if i != extra else '4-я?', col, 12,
                       weight=700 if i == extra else None))
    return fig(svg(300, 200, ''.join(b), maxw=300), 'шкатулок три — перегородок две')


def pies_first():
    """Пример 4, способ 1: сначала по одному пирожку на тарелку, остаток — как угодно."""
    names, rest = ['Аня', 'Боря', 'Вика'], [2, 1, 0]
    b = []
    for i, nm in enumerate(names):
        cx = 90 + i * 170
        b.append(f"<ellipse cx='{cx}' cy='112' rx='70' ry='18' fill='none' stroke='var(--muted)' stroke-width='2'/>")
        b.append(t(cx, 150, nm, 'var(--ink)', 14, weight=700))
        b.append(g('fi', 0.4, f"<circle cx='{cx - 36}' cy='104' r='12' fill='{GOLD}' fill-opacity='.45' "
                              f"stroke='{GOLD}' stroke-width='2'/>"))
        for q in range(rest[i]):
            x = cx - 6 + q * 28
            b.append(g('sl', 1.6 + 0.2 * q, ball(x, 40), ';--to:translate(0px,64px)'))
        b.append(t(cx, 178, f'остаток {rest[i]} → всего {rest[i] + 1}', 'var(--muted)', 13, cls='fi', d=3.0))
    b.append(t(20, 20, 'сначала по одному (бледные), потом остаток три — как угодно', 'var(--ink)', 14,
               anchor='start', cls='fi', d=0.4))
    return fig(svg(520, 192, ''.join(b), maxw=520), fx=True)



def arrow_defs():
    return ("<defs><marker id='ar5' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' "
            "orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='var(--ink)'/></marker>"
            f"<marker id='ar5r' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' "
            f"orient='auto'><path d='M0 0 L10 5 L0 10 z' fill='{RED}'/></marker></defs>")


def chairs():
    """Правило соответствия: стрелки «человек → стул»; две вещи, которые проверяет взаимная однозначность."""
    panels = [('каждому — свой стул', [0, 2, 1, 3], 4, True),
              ('двое на одном стуле', [0, 1, 1, 2], 3, False),
              ('стул пустой', [0, 1, 2], 4, False)]
    b = [arrow_defs()]
    for p_, (title, to, nchairs, ok) in enumerate(panels):
        x0 = 14 + p_ * 196
        col = GREEN if ok else RED
        b.append(t(x0 + 84, 20, ('✓ ' if ok else '✗ ') + title, col, 13, weight=700))
        b.append(t(x0 + 22, 44, 'люди', 'var(--muted)', 12))
        b.append(t(x0 + 146, 44, 'стулья', 'var(--muted)', 12))
        for i in range(len(to)):
            b.append(f"<circle cx='{x0+22}' cy='{64+i*36}' r='11' fill='{BLUE}'/>")
        for j in range(nchairs):
            used = j in to
            bad = (not ok) and (not used or to.count(j) > 1)
            stroke = RED if bad else 'var(--muted)'
            b.append(f"<rect x='{x0+136}' y='{53+j*36}' width='22' height='22' rx='3' fill='none' "
                     f"stroke='{stroke}' stroke-width='2'/>")
        for i, j in enumerate(to):
            bad = (not ok) and to.count(j) > 1
            b.append(f"<line x1='{x0+36}' y1='{64+i*36}' x2='{x0+130}' y2='{64+j*36}' "
                     f"stroke='{RED if bad else 'var(--ink)'}' stroke-width='1.6' "
                     f"marker-end='url(#{'ar5r' if bad else 'ar5'})'/>")
    return fig(svg(600, 200, ''.join(b), maxw=600), 'пример на числах, не из задачи')


def shells_codes():
    """Ракушки: стрелки «способ → код». Способы по порядку: в первой 0, во второй 0, 1, 2, …; коды — следом."""
    left = [[0, c2, 4 - c2] for c2 in range(5)]
    code = lambda c: '1'.join('0' * x for x in c)
    b = [arrow_defs(), t(120, 18, 'способы', 'var(--ink)', 14, weight=700),
         t(458, 18, 'коды', 'var(--ink)', 14, weight=700)]
    rh, y0 = 46, 34
    for i, c in enumerate(left):
        y = y0 + i * rh
        cd = code(c)
        b.append(mini_boxes(14, y, c))
        b.append(code_row(370, y + 2, cd, w=26, gap=4))
        pl = [str(k + 1) for k, ch in enumerate(cd) if ch == '1']
        b.append(t(556, y + 21, f'места {pl[0]} и {pl[1]}', BLUE, 12, anchor='start'))
        b.append(f"<line x1='240' y1='{y+16}' x2='362' y2='{y+16}' stroke='var(--ink)' stroke-width='1.6' "
                 f"marker-end='url(#ar5)' pathLength='100' class='dr' style='--d:{0.4 + 0.5*i}s;--dur:.5s'/>")
    yd = y0 + 5 * rh
    b.append(t(120, yd + 8, '⋮', 'var(--muted)', 20, weight=700))
    b.append(t(458, yd + 8, '⋮', 'var(--muted)', 20, weight=700))
    b.append(t(14, yd + 36, 'дальше по порядку: в первой 1, 2, 3, 4 — всего 15 стрелок;', 'var(--ink)', 13,
               anchor='start', cls='fi', d=3.0))
    b.append(t(14, yd + 56, 'от каждого способа одна стрелка, к каждому коду одна', 'var(--ink)', 13,
               anchor='start', cls='fi', d=3.0))
    return fig(svg(640, yd + 68, ''.join(b), maxw=640), fx=True)



def pies_codes():
    """Пример 4, способ 1: раскладка всех пирожков → остаток (убрали по одному) → код. Все 10 по порядку."""
    rows = [(a, b, 6 - a - b) for a in range(1, 5) for b in range(1, 6 - a) if 6 - a - b >= 1]
    w, h, rh, y0 = 50, 26, 36, 52
    x1, x2, x3 = 14, 240, 436
    b = [arrow_defs(),
         t(x1 + 75, 18, 'все 6 пирожков', 'var(--ink)', 13, weight=700),
         t(x2 + 75, 18, 'остаток 3', 'var(--ink)', 13, weight=700),
         t(x3 + 60, 18, 'код остатка', 'var(--ink)', 13, weight=700)]
    for k, nm in enumerate(['Аня', 'Боря', 'Вика']):
        b.append(t(x1 + k * w + w / 2, 38, nm, 'var(--muted)', 11))
        b.append(t(x2 + k * w + w / 2, 38, nm, 'var(--muted)', 11))
    for i, c in enumerate(rows):
        y = y0 + i * rh
        rest = [x - 1 for x in c]
        # все пирожки: первый в каждом отделении бледный — его убираем
        b.append(mini_boxes(x1, y, c, w=w, h=h, r=5, step=11, label=False))
        for k in range(3):
            first = x1 + k * w + (w - (c[k] - 1) * 11) / 2
            b.append(f"<circle cx='{first}' cy='{y + h / 2}' r='5' fill='var(--bg)' stroke='{GOLD}' stroke-width='1.5'/>")
        b.append(f"<line x1='{x1+3*w+8}' y1='{y+h/2}' x2='{x2-8}' y2='{y+h/2}' stroke='var(--muted)' "
                 f"stroke-width='1.4' marker-end='url(#ar5)'/>")
        b.append(mini_boxes(x2, y, rest, w=w, h=h, r=5, step=11, label=False))
        b.append(f"<line x1='{x2+3*w+8}' y1='{y+h/2}' x2='{x3-8}' y2='{y+h/2}' stroke='var(--ink)' "
                 f"stroke-width='1.6' marker-end='url(#ar5)'/>")
        b.append(code_row(x3, y + 1, '1'.join('0' * x for x in rest), w=24, gap=4))
    yb = y0 + len(rows) * rh + 20
    b.append(t(x1, yb, 'кружок без заливки — пирожок, который убрали: по одному с каждой тарелки', 'var(--muted)', 12, anchor='start'))
    b.append(t(x1, yb + 26, '10 раскладок ↔ 10 остатков ↔ 10 кодов из трёх 0 и двух 1', 'var(--ink)', 14,
               anchor='start', weight=700))
    return fig(svg(590, yb + 38, ''.join(b), maxw=590))



def trainings_codes():
    """Пример 5: выбор трёх мест из шести → расписание. Выборы по порядку {1, 2, 3}, {1, 2, 4}, …"""
    from itertools import combinations
    choices = list(combinations(range(6), 3))[:5]
    x1, x2, y0, rh = 14, 330, 40, 40
    b = [arrow_defs(), t(x1 + 140, 18, 'выбраны три места из шести', 'var(--ink)', 13, weight=700),
         t(x2 + 130, 18, 'дни каникул 1–8', 'var(--ink)', 13, weight=700)]
    for i, ch in enumerate(choices):
        y = y0 + i * rh
        seq, x = [], x1
        for p_ in range(6):
            on = p_ in ch
            b.append(f"<rect x='{x}' y='{y}' width='18' height='26' rx='4' "
                     + (f"fill='{GREEN}'/>" if on else f"fill='none' stroke='{GREY}' stroke-dasharray='3 3'/>"))
            if on:
                seq.append('Т')
            x += 22
            if p_ < 5:
                b.append(f"<rect x='{x}' y='{y}' width='24' height='26' rx='4' fill='var(--bg2)' stroke='var(--line)'/>")
                b.append(t(x + 12, y + 18, 'о', 'var(--muted)', 12))
                seq.append('о')
                x += 28
        b.append(f"<line x1='{x+4}' y1='{y+13}' x2='{x2-8}' y2='{y+13}' stroke='var(--ink)' stroke-width='1.6' "
                 f"marker-end='url(#ar5)'/>")
        for d_, c_ in enumerate(seq):
            on = c_ == 'Т'
            xx = x2 + d_ * 30
            b.append(f"<rect x='{xx}' y='{y}' width='26' height='26' rx='4' "
                     f"fill='{GREEN if on else 'var(--bg2)'}' stroke='var(--line)'/>")
            b.append(t(xx + 13, y + 18, str(d_ + 1), DARK if on else 'var(--muted)', 12, weight=700 if on else None))
    yd = y0 + 5 * rh
    b.append(t(x1 + 140, yd + 6, '⋮', 'var(--muted)', 20, weight=700))
    b.append(t(x2 + 120, yd + 6, '⋮', 'var(--muted)', 20, weight=700))
    b.append(t(x1, yd + 32, 'дальше по порядку — всего C(6, 3) = 20 выборов и 20 расписаний;', 'var(--ink)', 13,
               anchor='start'))
    b.append(t(x1, yd + 52, 'между выбранными местами всегда есть день отдыха — тренировки не рядом', 'var(--ink)', 13,
               anchor='start'))
    return fig(svg(580, yd + 64, ''.join(b), maxw=580), 'зелёное — тренировка, о — отдых, пунктир — свободное место')


def same_boxes():
    """Ошибка 3: одинаковые коробки — разные коды дают одну раскладку; все четыре раскладки списком."""
    b = [t(14, 18, 'коробки разные: два разных кода', 'var(--ink)', 13, anchor='start', weight=700)]
    for r, cd in enumerate(['001010', '010100']):
        y = 32 + r * 40
        b.append(code_row(14, y, cd, w=24, gap=4))
        b.append(t(190, y + 18, '→', 'var(--muted)', 16))
        b.append(mini_boxes(208, y - 2, counts_of(cd), w=50, h=28, r=5, step=12, label=False))
    b.append(t(380, 66, 'коробки одинаковые:', 'var(--ink)', 13, anchor='start'))
    b.append(t(380, 86, 'одна раскладка 2 + 1 + 1', RED, 14, anchor='start', weight=700))
    b.append(t(14, 136, 'все раскладки 4 ракушек по 3 одинаковым коробкам — списком', 'var(--ink)', 13, anchor='start',
               weight=700))
    for i, c in enumerate([[4, 0, 0], [3, 1, 0], [2, 2, 0], [2, 1, 1]]):
        x = 14 + i * 140
        b.append(mini_boxes(x, 150, c, w=40, h=26, r=4.5, step=9.5, label=False))
        b.append(t(x + 60, 196, ' + '.join(str(v) for v in c if v), 'var(--ink)', 13, weight=700))
    return fig(svg(580, 208, ''.join(b), maxw=580), 'одинаковые коробки: формулы нет, считаем списком')


FIGS = {
    'Каждый выбор трёх мест из шести даёт расписание': trainings_codes,
    'коды 001010 и 010100 дают одну и ту же раскладку': same_boxes,
    'остатку «Ане 2, Боре 1, Вике 0» соответствует код 00101': pies_codes,
    'ни один стул не пустой': chairs,
    'каждый код — какой-то способ, даже 100001 и 110000': shells_codes,
    'способами: у каждого шара n вариантов ящика': distinct,
    'Оба способа входят в 81': glue,
    'Код задаётся выбором двух мест из шести для единиц': slide_ones,
    'N(способов) = 5 + 4 + 3 + 2 + 1 = 15': all15,
    'Например, решению (1, 0, 5) соответствует код 01100000': equation,
    'Шаров k, перегородок n − 1 — получается код': general,
    'Получилось 35 вместо 15': wrong_bars,
    'Например, раскладка «Ане 3, Боре 2, Вике 1»': pies_first,
    'Например, код 001010 означает': shells,
    '110000 — первая и вторая пусты': codes,
    'Например, код 011001 означает': icecream,
    'Промежутков пять, перегородок две': pies,
    'Например, тренировки с левого края': trainings,
    'Маршруты идут по сетке 5 × 2 клетки': route_task,
    'Возможный маршрут из A в D показан на рисунке': route,
    'Каждый маршрут через M состоит из двух частей': route_m,
}

if __name__ == '__main__':
    d = json.load(open(VIS))
    md = open(os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.md')).read()
    plain = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', md))
    new = {anchor: f() for anchor, f in FIGS.items()}
    missing = [a for a in new if a not in plain]
    if missing:
        raise SystemExit(f'якоря не найдены в тексте: {missing}')
    d = {k: v for k, v in d.items() if k in plain and (k in new or v not in new.values())}
    d.update(new)
    json.dump(d, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(FIGS), 'рисунков →', os.path.relpath(VIS))
