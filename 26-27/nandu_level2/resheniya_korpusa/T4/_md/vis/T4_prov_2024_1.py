"""Рисунки: провинциал 2024, №1 — шесть кружков A…F, разные цифры, A + B = D, B + C = E, D + E = F.

Запуск: python3 vis/T4_prov_2024_1.py T4_prov_2024_1.vis.json
Чертёж — как в PDF условия: нижний ряд A, B, C; над ними D (между A и B) и E (между B и C); F над B.
"""
import json, sys, math
GOLD, BLUE, GREEN, VIOLET = '#f0a83c', '#5ba8f5', '#5fd38d', '#b48ef0'
INK, DIM, LAB, MUTED = '#cfdae6', '#4a5866', '#e8eef6', '#93a1b1'
U, V_ = 16, 20
PT = {'A': (0, 2 * V_), 'B': (2 * U, 2 * V_), 'C': (4 * U, 2 * V_),
      'D': (U, V_), 'E': (3 * U, V_), 'F': (2 * U, 0)}
EDGES = [('A', 'D'), ('B', 'D'), ('B', 'E'), ('C', 'E'), ('D', 'F'), ('E', 'F')]
R = 7.0
VB = (-10, -10, 4 * U + 26, 2 * V_ + 20)

def edge(p, q, col=INK, w=0.6):
    (x1, y1), (x2, y2) = PT[p], PT[q]
    dx, dy = x2 - x1, y2 - y1; d = math.hypot(dx, dy); ux, uy = dx / d, dy / d
    return (f"<line x1='{x1 + ux * R:.2f}' y1='{y1 + uy * R:.2f}' x2='{x2 - ux * R:.2f}' y2='{y2 - uy * R:.2f}' "
            f"stroke='{col}' stroke-width='{w}'/>")

def graph(nums=None, letters=True, hi=(), fill=None, hedges=()):
    """nums — {кружок: цифра} золотом; letters — буквы в пустых кружках (с цифрой — мелко сбоку);
    hi — выделенные кружки (обводка золотом); fill — {кружок: цвет} заливка; hedges — выделенные отрезки."""
    nums = nums or {}; fill = fill or {}
    s = ''
    for p, q in EDGES:
        s += edge(p, q, GOLD if (p, q) in hedges else INK, 1.1 if (p, q) in hedges else 0.6)
    for v, (x, y) in PT.items():
        st, w = (GOLD, 1.2) if v in hi else (INK, 0.6)
        f = f"fill='{fill[v]}' fill-opacity='0.30'" if v in fill else "fill='none'"
        s += f"<circle cx='{x}' cy='{y}' r='{R}' {f} stroke='{st}' stroke-width='{w}'/>"
        if v in nums:
            s += (f"<text x='{x}' y='{y + 2.3:.2f}' fill='{GOLD}' font-size='6.4' text-anchor='middle' "
                  f"font-weight='700'>{nums[v]}</text>")
            if letters:
                s += (f"<text x='{x + R + 1.2:.2f}' y='{y - R + 2.5:.2f}' fill='{MUTED}' font-size='4'>{v}</text>")
        elif letters:
            s += (f"<text x='{x}' y='{y + 2.1:.2f}' fill='{MUTED}' font-size='5.8' text-anchor='middle' "
                  f"font-style='italic'>{v}</text>")
    return s

def svg(inner, mw=300, aria='Шесть кружков', extra_w=0):
    x, y, w, h = VB
    return (f"<svg viewBox='{x} {y} {w + extra_w} {h}' role='img' aria-label='{aria}' "
            f"style='max-width:{mw}px'>{inner}</svg>")

def row(gs, caps, mw=640, aria='Заполнения'):
    x0, y0, w, h = VB
    gap = 4; inner = ''
    for i, (g, cap) in enumerate(zip(gs, caps)):
        dx = i * (w + gap)
        inner += f"<g transform='translate({dx},0)'>{g}"
        if cap:
            inner += (f"<text x='{2 * U}' y='{2 * V_ + 14}' fill='{MUTED}' font-size='4.6' "
                      f"text-anchor='middle'>{cap}</text>")
        inner += '</g>'
    W = len(gs) * w + (len(gs) - 1) * gap
    return (f"<svg viewBox='{x0} {y0} {W} {h + 4}' role='img' aria-label='{aria}' "
            f"style='max-width:{mw}px'>{inner}</svg>")

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

def swap(p, q, col, bend):
    """двусторонняя дуга-стрелка между кружками p и q, выгнутая вниз на bend."""
    (x1, y1), (x2, y2) = PT[p], PT[q]
    a = (x1 + R * 0.8, y1 + R * 0.7); b = (x2 - R * 0.8, y2 + R * 0.7)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + bend
    s = (f"<path d='M{a[0]:.2f},{a[1]:.2f} Q{mx:.2f},{my:.2f} {b[0]:.2f},{b[1]:.2f}' fill='none' "
         f"stroke='{col}' stroke-width='0.9'/>")
    for (px, py), (cx, cy) in ((a, (mx, my)), (b, (mx, my))):
        dx, dy = px - cx, py - cy; d = math.hypot(dx, dy); ux, uy = dx / d, dy / d
        bx, by = px - ux * 3.0, py - uy * 3.0
        s += (f"<polygon points='{px:.2f},{py:.2f} {bx - uy * 1.6:.2f},{by + ux * 1.6:.2f} "
              f"{bx + uy * 1.6:.2f},{by - ux * 1.6:.2f}' fill='{col}'/>")
    return s

def fill(A, B, C):
    D, E = A + B, B + C
    return {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': D + E}

V = {}
# условие: чертёж как в PDF
V['A, B, C, D, E, F — кружки рисунка и цифры в них.'] = fig(svg(graph(), 340),
    'Рисунок условия.')
# идея: B входит и в D, и в E
V['Кружок B входит и в D, и в E'] = fig(
    svg(graph(hi=('B',), fill={'B': GOLD}, hedges=(('B', 'D'), ('B', 'E'))), 300, 'B входит в D и в E'),
    f"<b style='color:{GOLD}'>B</b> входит и в D, и в E, а D + E = F.")
# зеркальный обмен: A ↔ C вместе с D ↔ E
x, y, w, h = VB
ax = (f"<line x1='{2 * U}' y1='{R}' x2='{2 * U}' y2='{2 * V_ - R}' stroke='{DIM}' stroke-width='0.5' "
      f"stroke-dasharray='2 1.6'/>")
mir = ax + graph(fill={'A': BLUE, 'C': BLUE, 'D': GREEN, 'E': GREEN}) + swap('A', 'C', BLUE, 9) + swap('D', 'E', GREEN, 7)
V['Если поменять местами цифры в A и C'] = fig(svg(mir, 300, 'Зеркальный обмен'),
    f"<b style='color:{BLUE}'>A ↔ C</b> и вместе с ним <b style='color:{GREEN}'>D ↔ E</b>: условия остаются верными.")
# миры: годные пары в обоих порядках
G1 = [fill(2, 1, 4), fill(4, 1, 2), fill(2, 1, 5), fill(5, 1, 2)]
G2 = [fill(1, 2, 4), fill(4, 2, 1)]
G3 = [fill(1, 3, 2), fill(2, 3, 1)]
V['пары 2, 4 и 2, 5 встают в A и C двумя способами каждая'] = fig(
    row([graph(g) for g in G1], ['', '', '', ''], 640, 'Заполнения при B = 1'), 'B = 1: пары 2, 4 и 2, 5, каждая в двух порядках.')
V['1 и 4 встают в A и C двумя способами'] = fig(
    row([graph(g) for g in G2], ['', ''], 330, 'Заполнения при B = 2'), 'B = 2: пара 1, 4 в двух порядках.')
V['1 и 2 встают в A и C двумя способами'] = fig(
    row([graph(g) for g in G3], ['', ''], 330, 'Заполнения при B = 3'), 'B = 3: пара 1, 2 в двух порядках.')
# ответ: все восемь
V['B = 3, A = 1, C = 2, D = 4, E = 5, F = 9 и зеркальное'] = (
    fig(row([graph(g, letters=False) for g in G1], ['', '', '', ''], 640, 'Восемь заполнений, B = 1'), '')
    + fig(row([graph(g, letters=False) for g in G2 + G3], ['', '', '', ''], 640, 'Восемь заполнений, B = 2 и 3'),
          'Все восемь заполнений: B = 1 (верхний ряд), B = 2 и B = 3 (нижний).'))
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
