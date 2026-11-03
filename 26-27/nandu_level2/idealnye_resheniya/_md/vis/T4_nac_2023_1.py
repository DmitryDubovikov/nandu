import json, sys, math
# Рисунки к Т4 национал 2023 I №1: три треугольника ABC, DEF, PQR из треугольничков, числа 1–10, равные суммы.
# Чертёж — как в PDF условия: сетка равносторонних треугольничков со стороной 20.
# X, Y, Z — точки без букв на чертеже (середины AC, EF, PQ); в тексте решения их нет.
GOLD, BLUE, GREEN, VIOLET = '#f0a83c', '#5ba8f5', '#5fd38d', '#b48ef0'
INK, DIM, LAB, MUTED = '#cfdae6', '#4a5866', '#e8eef6', '#93a1b1'
H = 20 * math.sqrt(3) / 2
PT = {'C': (20, 0), 'F': (40, 0), 'X': (10, H), 'R': (30, H), 'Y': (50, H),
      'A': (0, 2 * H), 'D': (20, 2 * H), 'B': (40, 2 * H), 'E': (60, 2 * H),
      'P': (10, 3 * H), 'Z': (30, 3 * H), 'Q': (50, 3 * H)}
CELLS = {'CXR': 'CXR', 'AXD': 'AXD', 'XRD': 'XRD', 'RDB': 'RDB', 'FRY': 'FRY',
         'RYB': 'RYB', 'YBE': 'YBE', 'DPZ': 'DPZ', 'DZB': 'DZB', 'BZQ': 'BZQ'}
BIG = {'ABC': ('CXR', 'AXD', 'XRD', 'RDB'), 'DEF': ('RDB', 'FRY', 'RYB', 'YBE'),
       'PQR': ('RDB', 'DPZ', 'DZB', 'BZQ')}
BIGCOL = {'ABC': BLUE, 'DEF': GREEN, 'PQR': VIOLET}
GIVEN = {'CXR': 2, 'AXD': 10, 'FRY': 1, 'BZQ': 3}
# буквы вершин: (dx, dy) от точки
LBL = {'C': (0, -3.2), 'F': (0, -3.2), 'R': (0, -5.6), 'A': (-4.2, 1.6), 'E': (4.2, 1.6),
       'D': (-5.2, 5.0), 'B': (5.2, 5.0), 'P': (-4.2, 2.4), 'Q': (4.2, 2.4)}

def cen(c):
    xs = [PT[v][0] for v in c]; ys = [PT[v][1] for v in c]
    return sum(xs) / 3, sum(ys) / 3

def tri(c, fill='none', op=0.0, stroke=INK, w=0.5):
    pts = ' '.join(f'{PT[v][0]:.2f},{PT[v][1]:.2f}' for v in c)
    f = f" fill='{fill}' fill-opacity='{op}'" if fill != 'none' else " fill='none'"
    return f"<polygon points='{pts}'{f} stroke='{stroke}' stroke-width='{w}' stroke-linejoin='round'/>"

def txt(c, s, col, size=6.0, italic=False, bold=True):
    x, y = cen(c)
    st = " font-style='italic'" if italic else ''
    fw = " font-weight='700'" if bold else ''
    return (f"<text x='{x:.2f}' y='{y + size * 0.36:.2f}' fill='{col}' font-size='{size}' "
            f"text-anchor='middle'{fw}{st}>{s}</text>")

def board(nums=None, letters=None, tint=None, gold=(), letters_on=True, dots=True):
    """nums — {клетка: число}; новые числа (не данные условием) золотом; letters — {клетка: буква};
    tint — (большой треугольник, цвет): его клетки подкрашены; gold — клетки с золотой заливкой."""
    nums = nums or {}; letters = letters or {}
    s = ''
    if tint:
        name, col = tint
        for c in BIG[name]:
            s += tri(c, col, 0.22, 'none', 0)
    for c in gold:
        s += tri(c, GOLD, 0.45, 'none', 0)
    for c in CELLS:
        s += tri(c)
    if dots:
        for v, (x, y) in PT.items():
            s += f"<circle cx='{x:.2f}' cy='{y:.2f}' r='0.9' fill='{INK}'/>"
    if letters_on:
        for v, (dx, dy) in LBL.items():
            x, y = PT[v]
            s += (f"<text x='{x + dx:.2f}' y='{y + dy + 1.4:.2f}' fill='{MUTED}' font-size='4.2' "
                  f"text-anchor='middle'>{v}</text>")
    for c, n in GIVEN.items():
        s += txt(c, n, LAB)
    for c, n in nums.items():
        s += txt(c, n, GOLD)
    for c, l in letters.items():
        s += txt(c, l, MUTED, 5.6, italic=True, bold=False)
    return s

VB = (-8, -7, 76, 3 * H + 12)

def svg(inner, mw=300, aria='Три треугольника'):
    x, y, w, h = VB
    return (f"<svg viewBox='{x} {y:.2f} {w} {h:.2f}' role='img' aria-label='{aria}' "
            f"style='max-width:{mw}px'>{inner}</svg>")

def row(boards, caps, mw=680, aria='Заполнения'):
    # несколько досок в одном svg, под каждой подпись
    x0, y0, w, h = VB
    gap = 6; inner = ''
    for i, (b, cap) in enumerate(zip(boards, caps)):
        dx = i * (w + gap)
        inner += f"<g transform='translate({dx:.2f},0)'>{b}"
        if cap:
            inner += (f"<text x='30' y='{3 * H + 9.5:.2f}' fill='{MUTED}' font-size='4.6' "
                      f"text-anchor='middle'>{cap}</text>")
        inner += '</g>'
    W = len(boards) * w + (len(boards) - 1) * gap
    return (f"<svg viewBox='{x0} {y0:.2f} {W:.2f} {h:.2f}' role='img' aria-label='{aria}' "
            f"style='max-width:{mw}px'>{inner}</svg>")

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

V = {}
# условие: чертёж с данными числами и буквами x, y
V['Сколькими способами можно заполнить шесть оставшихся треугольничков?'] = fig(
    svg(board(letters={'RDB': 'x', 'XRD': 'y'}), 300),
    'x — число в треугольничке RDB, y — в пустом треугольничке ABC.')
# идея: RDB входит во все три треугольника
V['Треугольничек RDB входит во все три треугольника'] = fig(
    row([board(letters={'RDB': 'x'}, tint=(n, BIGCOL[n]), gold=('RDB',), letters_on=True) for n in BIG],
        ['ABC', 'DEF', 'PQR'], 640, 'RDB в трёх треугольниках'),
    f"<b style='color:{GOLD}'>RDB</b> входит в каждый из треугольников ABC, DEF и PQR.")
# мир x = 4: куда идут оставшиеся числа — одно в ABC, пара в DEF, пара в PQR; внутри пары числа меняются местами
def swap(c1, c2, col):
    (x1, y1), (x2, y2) = cen(c1), cen(c2)
    dx, dy = x2 - x1, y2 - y1; d = math.hypot(dx, dy); ux, uy = dx / d, dy / d
    a, b = (x1 - ux * 1.2, y1 - uy * 1.2), (x2 + ux * 1.2, y2 + uy * 1.2)
    s = f"<line x1='{a[0]:.2f}' y1='{a[1]:.2f}' x2='{b[0]:.2f}' y2='{b[1]:.2f}' stroke='{col}' stroke-width='1.1'/>"
    for (px, py), sg in ((a, -1), (b, 1)):   # наконечники с обеих сторон
        bx, by = px - sg * ux * 3.0, py - sg * uy * 3.0
        s += (f"<polygon points='{px:.2f},{py:.2f} {bx - uy * 1.8:.2f},{by + ux * 1.8:.2f} "
              f"{bx + uy * 1.8:.2f},{by - ux * 1.8:.2f}' fill='{col}'/>")
    return s

def chips(nums, x0, y0):
    s = (f"<text x='{x0 + 2:.2f}' y='{y0 - 3:.2f}' fill='{MUTED}' font-size='4.2'>остались</text>")
    for i, n in enumerate(nums):
        y = y0 + i * 9
        s += (f"<rect x='{x0:.2f}' y='{y:.2f}' width='9' height='7' rx='1.6' fill='none' stroke='{GOLD}' stroke-width='0.6'/>"
              f"<text x='{x0 + 4.5:.2f}' y='{y + 5.2:.2f}' fill='{GOLD}' font-size='5' text-anchor='middle' font-weight='700'>{n}</text>")
    return s

def places(xv, rest):
    s = ''
    for c, col in (('XRD', BLUE), ('RYB', GREEN), ('YBE', GREEN), ('DPZ', VIOLET), ('DZB', VIOLET)):
        s += tri(c, col, 0.30, 'none', 0)
    s += board({'RDB': xv}, letters={'XRD': 'y'})
    s += swap('RYB', 'YBE', LAB) + swap('DPZ', 'DZB', LAB)
    s += chips(rest, 72, 6)
    x, y, w, h = VB
    return (f"<svg viewBox='{x} {y:.2f} {w + 18} {h:.2f}' role='img' aria-label='Куда идут оставшиеся числа' "
            f"style='max-width:360px'>{s}</svg>")

V['Остались числа 5, 6, 7, 8, 9: одно встаёт в ABC'] = fig(places(4, (5, 6, 7, 8, 9)),
    f"<b style='color:{BLUE}'>y</b> — одно число в ABC, "
    f"<b style='color:{GREEN}'>пара в DEF</b>, <b style='color:{VIOLET}'>пара в PQR</b>; стрелка: числа пары меняются местами.")
# миры: раскладка по треугольникам
W4 ={'RDB': 4, 'XRD': 5, 'RYB': 7, 'YBE': 9, 'DPZ': 6, 'DZB': 8}
W7 = {'RDB': 7, 'XRD': 4, 'RYB': 6, 'YBE': 9, 'DPZ': 5, 'DZB': 8}
V['S_{PQR} = 3 + 4 + 6 + 8 = 21 ✓'] = fig(svg(board(W4), 280),
    'Раскладка при x = 4: в каждом треугольнике сумма 21.')
V['S_{PQR} = 3 + 7 + 5 + 8 = 23 ✓'] = fig(svg(board(W7), 280),
    'Раскладка при x = 7: в каждом треугольнике сумма 23.')
# ответ: все восемь заполнений

def four(w, de, pq):
    out = []
    for a, b in (de, de[::-1]):
        for c, d in (pq, pq[::-1]):
            m = dict(w); m['RYB'], m['YBE'], m['DPZ'], m['DZB'] = a, b, c, d
            out.append(board(m, letters_on=False))
    return out

V['x = 7, y = 4, в DEF 6 и 9, в PQR 5 и 8, каждая пара в любом порядке'] = (
    fig(row(four(W4, (7, 9), (6, 8)), ['', '', '', ''], 680, 'Заполнения при x = 4'), 'x = 4: четыре заполнения.')
    + fig(row(four(W7, (6, 9), (5, 8)), ['', '', '', ''], 680, 'Заполнения при x = 7'), 'x = 7: четыре заполнения.'))
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
