#!/usr/bin/env python3
"""Иллюстрации главы 2 «Без повторов» → nandu_n2_kombinatorika_uchebnik.vis.json.

Один язык на всю главу: у каждого ребёнка (буквы, ладьи) свой цвет, выбывшее — серое,
свободное — подсвечено. Анимируется только переход (правило 15): ребёнок уходит из кружка
в роль, ладья вычёркивает горизонталь, хвост 5 · 4 · 3 · 2 · 1 дописывается сверху и снизу.

Запуск: python3 26-27/nandu_level2/kombinatorika/vis/glava_2.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.vis.json')

GOLD, BLUE, GREEN, RED, VIOLET = '#f0a83c', '#5ba8f5', '#5fd38d', '#f2686c', '#b48cf2'
GREY = '#5d6b7c'
KIDS = [('А', BLUE), ('Б', GOLD), ('В', GREEN), ('Г', RED),
        ('Д', VIOLET), ('Е', '#4fd1d9'), ('Ж', '#f78fb3'), ('З', '#a3d65c')]
LETTERS = [('А', BLUE), ('Б', GOLD), ('В', GREEN), ('Г', RED), ('Д', VIOLET)]


def svg(w, h, body, maxw=None):
    st = f" style='max-width:{maxw}px'" if maxw else ''
    return (f"<svg viewBox='0 0 {w} {h}' width='{w}' height='{h}' font-family='inherit' "
            f"font-size='15'{st}>{body}</svg>")


def fig(s, cap='', fx=False):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    cls = ' class="fx"' if fx else ''
    return f'<figure{cls}>{s}{c}</figure>'


def t(x, y, s, fill='var(--muted)', size=None, anchor='middle', weight=None, cls=None, d=None, extra=''):
    a = f" font-size='{size}'" if size else ''
    a += f" font-weight='{weight}'" if weight else ''
    a += f" class='{cls}'" if cls else ''
    a += f" style='--d:{d}s'" if d is not None else ''
    return f"<text x='{x}' y='{y}' text-anchor='{anchor}' fill='{fill}'{a}{extra}>{s}</text>"


def kid(cx, cy, i, r=17, grey=False):
    letter, col = KIDS[i]
    if grey:
        return (f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='var(--bg)' stroke='{GREY}' stroke-width='1.5'/>"
                + t(cx, cy + 5, letter, GREY, 15, weight=700))
    return (f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{col}'/>"
            + t(cx, cy + 5, letter, '#0d1117', 15, weight=700))


def g(cls, d, body, extra=''):
    return f"<g class='{cls}' style='--d:{d}s{extra}'>{body}</g>"


# ——— 1. Пример 1: ребёнок уходит из кружка в роль, меню короче на один ———

def roles():
    sx = [120, 300, 480]
    px = [76 + i * 64 for i in range(8)]
    py, sy = 205, 48
    roles_ = ['ведущий', '1-й помощник', '2-й помощник']
    chosen = [1, 5, 2]
    b = []
    for x, r in zip(sx, roles_):
        b.append(f"<rect x='{x-70}' y='18' width='140' height='60' rx='10' fill='none' "
                 f"stroke='var(--muted)' stroke-width='1.5' stroke-dasharray='5 4'/>")
        b.append(t(x, 100, r, size=14))
    for x in px:
        b.append(f"<circle cx='{x}' cy='{py}' r='17' fill='none' stroke='{GREY}' stroke-dasharray='4 3'/>")
    b.append(t(300, 250, 'кружок: 8 ребят', size=13))
    taken = []
    for s, c in enumerate(chosen):
        a = 0.3 + 2.0 * s
        left = [i for i in range(8) if i not in taken]
        rings = ''.join(f"<circle cx='{px[i]}' cy='{py}' r='23' fill='none' stroke='{GOLD}' stroke-width='2'/>"
                        for i in left)
        b.append(g('fi', a, g('fo', a + 1.0, rings)))
        b.append(t(sx[s], 126, f'{len(left)} вариантов', GOLD, 15, weight=700, cls='fi', d=a))
        taken.append(c)
    for i in range(8):
        k = kid(px[i], py, i)
        if i in chosen:
            s = chosen.index(i)
            k = g('sl', 1.3 + 2.0 * s, k, f';--to:translate({sx[s]-px[i]}px,{sy-py}px)')
        b.append(k)
    b.append(t(300, 284, '8 · 7 · 6 = 336', 'var(--ink)', 19, weight=600, cls='fi', d=7.0))
    return fig(svg(600, 296, ''.join(b)), fx=True)


# ——— 2. ⚠ Почему n − k + 1: серых в строке на одну меньше её номера ———

def grid():
    rows = [('1-й выбор — ведущий', []), ('2-й выбор — 1-й помощник', [1]),
            ('3-й выбор — 2-й помощник', [1, 5]), ('4-й выбор — лишний', [1, 5, 2])]
    b = []
    for r, (lab, taken) in enumerate(rows):
        y = 34 + r * 54
        bad = r == 3
        b.append(t(14, y + 6, lab, RED if bad else 'var(--ink)', 17, anchor='start'))
        for j in range(8):
            b.append(kid(262 + j * 40, y, j, r=15, grey=j in taken))
        b.append(t(590, y + 6, f'занято {len(taken)}', GREY, 16, anchor='start'))
        b.append(t(680, y + 6, f'осталось {8-len(taken)}', RED if bad else GOLD, 17, anchor='start', weight=700))
    y3 = 34 + 3 * 54
    b.append(f"<rect x='6' y='{y3-24}' width='790' height='48' rx='8' fill='none' stroke='{RED}' "
             f"stroke-dasharray='6 4' stroke-width='1.5'/>")
    b.append(t(400, y3 + 50, '8 − 3 = 5 — это уже четвёртый выбор: четыре роли, а не три', RED, 17))
    return fig(svg(800, 270, ''.join(b)))


# ——— 3. 8 · 7 · 6 → умножить и разделить на 5! → 8! / 5! ———

def fraction():
    b = [t(18, 84, 'A(8, 3) =', 'var(--ink)', 20, anchor='start')]
    b.append(g('sl', 0.6, t(232, 84, '8 · 7 · 6', GOLD, 22, anchor='end', weight=600), ';--to:translate(0px,-26px)'))
    b.append(t(236, 58, '· 5 · 4 · 3 · 2 · 1', VIOLET, 22, anchor='start', weight=600, cls='fi', d=1.4))
    b.append(f"<line x1='128' y1='76' x2='424' y2='76' stroke='var(--ink)' stroke-width='2' "
             f"pathLength='100' class='dr' style='--d:1.0s;--dur:.8s'/>")
    b.append(t(330, 106, '5 · 4 · 3 · 2 · 1', VIOLET, 22, weight=600, cls='fi', d=1.8))
    eq = (t(452, 84, '=', 'var(--ink)', 22)
          + t(500, 58, '8!', 'var(--ink)', 22, weight=600)
          + "<line x1='478' y1='76' x2='522' y2='76' stroke='var(--ink)' stroke-width='2'/>"
          + t(500, 106, '5!', VIOLET, 22, weight=600))
    b.append(g('fi', 2.8, eq))
    return fig(svg(560, 124, ''.join(b)), fx=True)


# ——— 4. Три подсчёта слов: что происходит с меню под каждым местом ———

def strips():
    rows = [('буквы любые — размещения с повторениями', 'БАБ', False, '5 · 5 · 5 = 125'),
            ('буквы разные — размещения', 'БГА', True, '5 · 4 · 3 = 60'),
            ('каждая буква ровно один раз — перестановки', 'БГАДВ', True, '5 · 4 · 3 · 2 · 1 = 120')]
    idx = {l: i for i, (l, _) in enumerate(LETTERS)}
    b = []
    for r, (title, word, distinct, formula) in enumerate(rows):
        y = 10 + r * 128
        b.append(t(14, y + 14, title, 'var(--ink)', 14, anchor='start'))
        for k, ch in enumerate(word):
            x = 40 + k * 76
            col = LETTERS[idx[ch]][1]
            b.append(f"<rect x='{x-20}' y='{y+26}' width='40' height='40' rx='7' fill='{col}'/>")
            b.append(t(x, y + 53, ch, '#0d1117', 19, weight=700))
            used = set(word[:k]) if distinct else set()
            for m, (l, c) in enumerate(LETTERS):
                mx = x - 28 + m * 14
                if l in used:
                    b.append(t(mx, y + 88, l, GREY, 13))
                    b.append(f"<line x1='{mx-5}' y1='{y+84}' x2='{mx+5}' y2='{y+84}' stroke='{GREY}'/>")
                else:
                    b.append(t(mx, y + 88, l, c, 13, weight=700))
            b.append(t(x, y + 110, str(5 - len(used)), GOLD, 16, weight=700))
        b.append(t(436, y + 58, formula, 'var(--ink)', 17, anchor='start', weight=600))
    b.append(t(14, 400, 'под каждым местом — меню из пяти букв; серые уже стоят раньше', size=13, anchor='start'))
    return fig(svg(640, 410, ''.join(b)))


# ——— 5. Пример 4: шесть слов, в каждом все три цвета ———

def tiles():
    words = ['АБВ', 'АВБ', 'БАВ', 'БВА', 'ВАБ', 'ВБА']
    idx = {l: c for l, c in LETTERS}
    b = []
    for w, word in enumerate(words):
        x0 = 10 + w * 104
        for k, ch in enumerate(word):
            x = x0 + k * 30
            b.append(f"<rect x='{x}' y='10' width='27' height='27' rx='5' fill='{idx[ch]}'/>")
            b.append(t(x + 13.5, 29, ch, '#0d1117', 15, weight=700))
    return fig(svg(624, 46, ''.join(b)))


# ——— доски 4 × 4 ———

C = 46


def board(x0, y0, c=C, labels=True):
    b = []
    for i in range(4):
        for j in range(4):
            fill = 'var(--bg2)' if (i + j) % 2 else 'var(--bg)'
            b.append(f"<rect x='{x0+i*c}' y='{y0+j*c}' width='{c}' height='{c}' fill='{fill}' "
                     f"stroke='var(--line)'/>")
    if labels:
        for i, col in enumerate('abcd'):
            b.append(t(x0 + i * c + c / 2, y0 + 4 * c + 18, col, size=13))
        for r in range(1, 5):
            b.append(t(x0 - 12, y0 + (4 - r) * c + c / 2 + 5, str(r), size=13))
    return ''.join(b)


def cell(x0, y0, col, row, c=C):
    """Левый верхний угол клетки: col 0..3 (a..d), row 1..4."""
    return x0 + col * c, y0 + (4 - row) * c


def rook(x0, y0, col, row, c=C, num=None):
    x, y = cell(x0, y0, col, row, c)
    s = t(x + c / 2, y + c * 0.74, '♜', 'var(--ink)', int(c * 0.66))
    if num:
        s += (f"<circle cx='{x+c-9}' cy='{y+9}' r='8' fill='{BLUE}'/>"
              + t(x + c - 9, y + 13, str(num), '#0d1117', 11, weight=700))
    return s


PLACE = {0: 2, 1: 4, 2: 1, 3: 3}          # a2, b4, c1, d3


def board_task():
    x0, y0 = 30, 10
    b = [board(x0, y0)] + [rook(x0, y0, col, row) for col, row in PLACE.items()]
    return fig(svg(228, 222, ''.join(b), maxw=260), 'одна из расстановок: a2, b4, c1, d3')


# ——— 6. Пример 5 а): вертикаль за вертикалью, каждая теряет горизонталь ———

def columns():
    x0, y0 = 40, 14
    b = [board(x0, y0)]
    used = []
    for col in range(4):
        a = 0.3 + 1.9 * col
        free = [r for r in range(1, 5) if r not in used]
        hi = ''.join(f"<rect x='{cell(x0,y0,col,r)[0]+3}' y='{cell(x0,y0,col,r)[1]+3}' width='{C-6}' "
                     f"height='{C-6}' rx='5' fill='{GREEN}' fill-opacity='.35' stroke='{GREEN}'/>" for r in free)
        b.append(g('fi', a, g('fo', a + 1.2, hi)))
        b.append(t(x0 + col * C + C / 2, y0 + 4 * C + 42, str(len(free)), GOLD, 18, weight=700, cls='fi', d=a))
        row = PLACE[col]
        b.append(g('fi', a + 0.8, rook(x0, y0, col, row)))
        if col < 3:
            x, y = cell(x0, y0, col + 1, row)
            b.append(f"<rect x='{x}' y='{y}' width='{(3-col)*C}' height='{C}' fill='{GREY}' fill-opacity='.45' "
                     f"class='fi' style='--d:{a+1.2}s'/>")
        used.append(row)
    b.append(t(x0 - 30, y0 + 4 * C + 42, 'клеток:', size=13, anchor='start'))
    b.append(t(300, 110, '4 · 3 · 2 · 1 = 24', 'var(--ink)', 19, anchor='start', weight=600, cls='fi', d=8.0))
    return fig(svg(520, 262, ''.join(b)), fx=True)


# ——— 7. Пример 5 б): цепочка Бени — ладьи с номерами, вычёркивают вертикаль и горизонталь ———

CHAIN = [(2, 1), (0, 2), (3, 3), (1, 4)]   # c1, a2, d3, b4


def benya():
    x0, y0 = 40, 14
    b = [board(x0, y0)]
    ucol, urow = [], []
    for s, (col, row) in enumerate(CHAIN):
        a = 0.3 + 2.1 * s
        free = [(c, r) for c in range(4) for r in range(1, 5) if c not in ucol and r not in urow]
        hi = ''.join(f"<rect x='{cell(x0,y0,c,r)[0]+3}' y='{cell(x0,y0,c,r)[1]+3}' width='{C-6}' height='{C-6}' "
                     f"rx='5' fill='{GOLD}' fill-opacity='.3' stroke='{GOLD}'/>" for c, r in free)
        b.append(g('fi', a, g('fo', a + 1.3, hi)))
        b.append(t(262, 40 + s * 34, f'{s+1}-я ладья: {len(free)} клет{"ок" if len(free) > 4 else "ки" if len(free) > 1 else "ка"}',
                   GOLD, 15, anchor='start', weight=700, cls='fi', d=a))
        if s < 3:
            x, y = cell(x0, y0, col, row)
            cross = (f"<rect x='{x0}' y='{y}' width='{4*C}' height='{C}' fill='{GREY}' fill-opacity='.4'/>"
                     f"<rect x='{x}' y='{y0}' width='{C}' height='{4*C}' fill='{GREY}' fill-opacity='.4'/>")
            b.append(g('fi', a + 1.3, g('fo', 8.4, cross)))
        b.append(g('fi', a + 0.8, rook(x0, y0, col, row, num=s + 1)))
        ucol.append(col); urow.append(row)
    b.append(t(262, 40 + 4 * 34 + 8, '16 · 9 · 4 · 1 = 576', 'var(--ink)', 19, anchor='start', weight=600, cls='fi', d=8.8))
    return fig(svg(520, 230, ''.join(b)), fx=True)


# ——— 8. Пример 5 б): одна расстановка — две разные цепочки ———

def two_orders():
    c = 38
    orders = [CHAIN, [(0, 2), (1, 4), (2, 1), (3, 3)]]
    names = ['c1, a2, d3, b4', 'a2, b4, c1, d3']
    b = []
    for k, (order, name) in enumerate(zip(orders, names)):
        x0, y0 = 30 + k * 360, 10
        b.append(board(x0, y0, c))
        for s, (col, row) in enumerate(order):
            b.append(rook(x0, y0, col, row, c, num=s + 1))
        b.append(t(x0 + 2 * c, y0 + 4 * c + 44, f'цепочка Бени: {name}', BLUE, 14))
    b.append(t(290, 92, 'та же', 'var(--ink)', 15))
    b.append(t(290, 112, 'расстановка', 'var(--ink)', 15))
    return fig(svg(580, 222, ''.join(b)), 'на доске номеров нет: одна расстановка — две разные цепочки Бени')


FIGS = {
    'Ведущим можно выбрать любого из восьми ребят': roles,
    'Из n вычитаем не номер выбора': grid,
    'Формулу для A(n, k) можно записать короче': fraction,
    'Одни и те же рассуждения можно сформулировать': strips,
    'В обоих случаях получаются ровно те же слова': tiles,
    'ставят 4 одинаковые ладьи': board_task,
    'Ладье вертикали a — четыре клетки': columns,
    'в его цепочке ладьи пронумерованы': benya,
    'На доске номеров нет': two_orders,
}

if __name__ == '__main__':
    d = json.load(open(VIS))
    d.pop('Ладей четыре, вертикалей четыре', None)
    for anchor, f in FIGS.items():
        d[anchor] = f()
    json.dump(d, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(FIGS), 'рисунков →', os.path.relpath(VIS))
