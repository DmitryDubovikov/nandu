import json, sys
# Рисунки к Т4 национал 2017 II №4: доска 3 × 4, число втрое больше соседа сверху и вдвое меньше соседа слева,
# сумма 12 чисел 2730. Чертёж — как в PDF условия: пустая сетка 3 строки × 4 столбца.
GOLD, BLUE, GREEN, VIOLET = '#f0a83c', '#5ba8f5', '#5fd38d', '#b48ef0'
INK, DIM, LAB, MUTED = '#cfdae6', '#4a5866', '#e8eef6', '#93a1b1'
CW, CH = 30, 18          # клетка
R, C = 3, 4
ROWCOL = (BLUE, GREEN, VIOLET)
XB = [['8x', '4x', '2x', 'x'], ['24x', '12x', '6x', '3x'], ['72x', '36x', '18x', '9x']]
NB = [[112, 56, 28, 14], [336, 168, 84, 42], [1008, 504, 252, 126]]


def grid(vals=None, col=LAB, gold=(), tint=False):
    s = ''
    if tint:
        for r in range(R):
            s += (f"<rect x='0' y='{r * CH}' width='{C * CW}' height='{CH}' fill='{ROWCOL[r]}' "
                  f"fill-opacity='0.14'/>")
    for (r, c) in gold:
        s += f"<rect x='{c * CW}' y='{r * CH}' width='{CW}' height='{CH}' fill='{GOLD}' fill-opacity='0.40'/>"
    for r in range(R + 1):
        s += f"<line x1='0' y1='{r * CH}' x2='{C * CW}' y2='{r * CH}' stroke='{INK}' stroke-width='0.6'/>"
    for c in range(C + 1):
        s += f"<line x1='{c * CW}' y1='0' x2='{c * CW}' y2='{R * CH}' stroke='{INK}' stroke-width='0.6'/>"
    if vals:
        for r in range(R):
            for c in range(C):
                v = vals[r][c]
                s += (f"<text x='{c * CW + CW / 2}' y='{r * CH + CH / 2 + 2.3}' fill='{col}' font-size='6.4' "
                      f"text-anchor='middle' font-weight='700'>{v}</text>")
    return s


def arrow(x1, y1, x2, y2, col=MUTED, w=0.7):
    dx, dy = x2 - x1, y2 - y1
    d = (dx * dx + dy * dy) ** 0.5; ux, uy = dx / d, dy / d
    bx, by = x2 - ux * 2.6, y2 - uy * 2.6
    return (f"<line x1='{x1}' y1='{y1}' x2='{bx:.2f}' y2='{by:.2f}' stroke='{col}' stroke-width='{w}'/>"
            f"<polygon points='{x2},{y2} {bx - uy * 1.5:.2f},{by + ux * 1.5:.2f} {bx + uy * 1.5:.2f},{by - ux * 1.5:.2f}' "
            f"fill='{col}'/>")


def lab(x, y, s, col=MUTED, size=4.6, anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}'>{s}</text>"


def svg(inner, vb, mw, aria):
    x, y, w, h = vb
    return f"<svg viewBox='{x} {y} {w} {h}' role='img' aria-label='{aria}' style='max-width:{mw}px'>{inner}</svg>"


def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"


V = {}
# условие: пустая доска, как в PDF
V['Каждое число задано через своего соседа'] = fig(
    svg(grid(), (-4, -4, C * CW + 8, R * CH + 8), 360, 'Доска 3 × 4'), 'Доска 3 × 4.')

# доска через x: стрелки «· 2» влево по строке 1, «· 3» вниз по столбцу x
s = grid(XB, LAB, gold=[(0, 3)])
for c in (3, 2, 1):           # над строкой 1: от клетки c к клетке c − 1
    x1, x2 = c * CW + CW / 2 - 3, (c - 1) * CW + CW / 2 + 3
    s += arrow(x1, -5, x2, -5) + lab((x1 + x2) / 2, -7.4, '· 2')
for r in (0, 1):              # справа от столбца 4: от строки r к строке r + 1
    y1, y2 = r * CH + CH / 2 + 2, (r + 1) * CH + CH / 2 - 2
    s += arrow(C * CW + 5, y1, C * CW + 5, y2) + lab(C * CW + 8, (y1 + y2) / 2 + 1.6, '· 3', anchor='start')
V['в строке 1 от x влево каждое число вдвое больше соседа справа'] = fig(
    svg(s, (-4, -14, C * CW + 22, R * CH + 18), 420, 'Доска через x'),
    f"<b style='color:{GOLD}'>x</b> — число в правом верхнем углу; влево вдвое больше, вниз втрое больше.")

# суммы строк
s = grid(XB, LAB, gold=[(0, 3)], tint=True)
for r, v in enumerate(('15x', '45x', '135x')):
    s += (f"<text x='{C * CW + 4}' y='{r * CH + CH / 2 + 2.3}' fill='{ROWCOL[r]}' font-size='6.4' "
          f"font-weight='700'>= {v}</text>")
V['сложим числа доски по строкам'] = fig(
    svg(s, (-4, -4, C * CW + 34, R * CH + 8), 440, 'Суммы строк'), 'Суммы строк.')

# ответ
s = grid(NB, GOLD)
V['доску заполняем так'] = fig(
    svg(s, (-4, -4, C * CW + 8, R * CH + 8), 360, 'Заполнение доски'), 'Заполнение доски: сумма 2730.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
