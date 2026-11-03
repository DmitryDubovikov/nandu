import json, sys
# Рисунки к Т4′ национал 2021 II №4: нечётные числа зигзагом в таблице из 7 строк.
# Таблица строится по закону рисунка: столбец c — вниз (нечётный) или вверх (чётный), пустая строка 7, 6, …, 1 по кругу.
GOLD, BLUE, GREEN = '#f0a83c', '#5ba8f5', '#5fd38d'
INK, DIM, LAB, MUT, BG = '#cfdae6', '#4a5866', '#e8eef6', '#93a1b1', '#121821'

def build(upto=2100):
    tab, n, c = {}, 1, 0
    while n <= upto:
        c += 1
        blank = 7 - (c - 1) % 7
        rows = [r for r in range(1, 8) if r != blank]
        if c % 2 == 0:
            rows.reverse()
        for r in rows:
            tab[(r, c)] = n; n += 2
    return tab
T = build()

CW, CH, LX, HY = 10, 6.5, 7, 7          # ширина и высота клетки, поле под номера строк и столбцов
def cx(c): return LX + (c - 1) * CW      # левый край столбца c (1…14 и «слоты» правее)
def cy(r): return HY + (r - 1) * CH
def txt(x, y, s, col=LAB, size=3.2, w='600', cls=''):
    k = f" class='{cls}'" if cls else ''
    return f"<text{k} x='{x:.1f}' y='{y:.1f}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def cell(x, r, fill=None, op=0.25, stroke=DIM, w=0.35, dash=False):
    f = f"fill='{fill}' fill-opacity='{op}'" if fill else "fill='none'"
    d = " stroke-dasharray='1 0.8'" if dash else ''
    return f"<rect x='{x:.1f}' y='{cy(r):.1f}' width='{CW}' height='{CH}' {f} stroke='{stroke}' stroke-width='{w}'{d}/>"
def num(x, r, s, col=LAB, size=3.2, cls=''):
    return txt(x + CW / 2, cy(r) + CH / 2 + 1.15, s, col, size, '600', cls)
def svg(inner, label, w, mw):
    h = HY + 7 * CH + 3
    return f"<svg viewBox='0 0 {w} {h:.1f}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap='', fx=False):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st{' fx' if fx else ''}'>{inner}{c}</figure>"
ARR = ("<defs><marker id='ah{0}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
       "<path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>")

def table(cols=range(1, 15), col_of=None, dots=True, heads=True):
    """Столбцы 1–14 рисунка; col_of(r, c) → цвет числа (None — обычный)."""
    s = ''
    for r in range(1, 8):
        s += txt(LX - 3.2, cy(r) + CH / 2 + 1.1, r, MUT, 2.6)
    for c in cols:
        if heads:
            s += txt(cx(c) + CW / 2, HY - 2, c, MUT, 2.6)
        for r in range(1, 8):
            v = T.get((r, c))
            col = col_of(r, c) if col_of else None
            s += cell(cx(c), r)
            if v:
                s += num(cx(c), r, v, col or (LAB if not col_of else DIM))
    if dots:
        for r in range(1, 8):
            s += txt(cx(15) + 4, cy(r) + CH / 2 + 1.1, '…', MUT, 3)
    return s

V = {}

# условие: таблица рисунка, строки и столбцы пронумерованы
V['В какой строке и каком столбце стоит 2021?'] = fig(
    svg(table(), 'Таблица из условия', cx(15) + 10, 560), 'Таблица из условия; строки и столбцы пронумерованы.')

# выписанные признаки столбцов 1–14: схема без чисел, как от руки — пустая клетка золотом, стрелка направления
def features():
    w, h, gap, y0 = 5, 3.2, 3.2, 6                # мини-клетка, промежуток между столбцами, верх клеток
    s = ARR.format('f').replace("markerWidth='4' markerHeight='4'", "markerWidth='3' markerHeight='3'")
    def lab(y, t, col):
        return f"<text x='4' y='{y:.1f}' fill='{col}' font-size='2.6' text-anchor='end' font-weight='600'>{t}</text>"
    for c in range(1, 15):
        x = 8 + (c - 1) * (w + gap)
        s += txt(x + w / 2, y0 - 2, c, MUT, 2.6)
        blank = 7 - (c - 1) % 7
        for r in range(1, 8):
            on = r == blank
            s += (f"<rect x='{x}' y='{y0 + (r - 1) * h:.1f}' width='{w}' height='{h}' "
                  f"fill='{GOLD if on else 'none'}' fill-opacity='0.55' stroke='{GOLD if on else DIM}' stroke-width='{0.6 if on else 0.3}'/>")
        a, b = (y0 + 0.8, y0 + 7 * h - 0.8) if c % 2 else (y0 + 7 * h - 0.8, y0 + 0.8)
        s += f"<path d='M{x + w / 2} {a:.1f}V{b:.1f}' stroke='{BLUE}' stroke-width='0.7' marker-end='url(#ahf)'/>"
        s += txt(x + w / 2, y0 + 7 * h + 4.4, blank, GOLD, 3, '700')
        s += txt(x + w / 2, y0 + 7 * h + 9, '↓' if c % 2 else '↑', BLUE, 3.4, '700')
    s += lab(y0 - 2, 'столбец', MUT) + lab(y0 + 7 * h + 4.4, 'пустая клетка', GOLD) + lab(y0 + 7 * h + 9, 'направление', BLUE)
    vb = f"-20 0 {8 + 14 * (w + gap) + 22:.0f} {y0 + 7 * h + 12:.0f}"
    return f"<svg viewBox='{vb}' role='img' aria-label='Столбцы 1–14' style='max-width:520px'>{s}</svg>"
V['Выпишем строку пустой клетки и направление для столбцов 1–14'] = fig(features(), 'Столбцы 1–14: строка пустой клетки и направление.')

# правило (*): копия столбца 1 переезжает на место столбца 15, числа становятся на 168 больше
def rule():
    s = table(cols=range(1, 15), col_of=lambda r, c: GOLD if c == 1 else DIM, dots=False) + ARR.format('r')
    s += txt(cx(15) + CW / 2, HY - 2, 15, GOLD, 2.6, '700')
    for r in range(1, 8):
        s += cell(cx(15), r, dash=True, stroke=MUT)
    g = ''
    for r in range(1, 8):
        v = T.get((r, 1))
        g += cell(cx(1), r, GOLD, 0.2, GOLD, 0.7)
        if v:
            g += f"<g class='fo' style='--d:1.7s'>{num(cx(1), r, v, GOLD)}</g>"
    s += f"<g class='sl' style='--to:translate({14 * CW}px,0px);--d:.3s'>{g}</g>"
    for r in range(1, 8):
        v = T.get((r, 15))
        if v:
            s += f"<g class='fi' style='--d:1.9s'>{num(cx(15), r, v, GOLD)}</g>"
    s += f"<g class='fi' style='--d:1.9s'>{txt(cx(15) + CW + 7, cy(4) + CH / 2 + 1.1, '+ 168', GOLD, 3.4, '700')}</g>"
    return svg(s, 'Столбец 15 устроен как столбец 1', cx(16) + 16, 600)
V['Столбец c + 14 устроен как столбец c'] = fig(rule(), 'Столбец 1 через 14 столбцов: то же место, число на 168 больше.', fx=True)

# вопросы: исходный столбец или клетка в рисунке → столбец далеко справа
TX = cx(16) + 4                                   # где рисуем далёкий столбец
def far(src, tgt_col, cells, label):
    """src — список (r, c) в рисунке, cells — {r: число} в далёком столбце."""
    s = table(col_of=lambda r, c: GOLD if (r, c) in src else DIM) + ARR.format(tgt_col)
    for r, c in src:
        s += cell(cx(c), r, GOLD, 0.3, GOLD, 0.8)
    s += txt(TX + CW / 2, HY - 2, tgt_col, GOLD, 2.6, '700')
    for r in range(1, 8):
        v = cells.get(r)
        s += cell(TX, r, GOLD if v else None, 0.3, GOLD if v else MUT, 0.8 if v else 0.35, dash=not v)
        if v:
            s += num(TX, r, v, GOLD, 3.0)
    if len(src) == 1:                             # одна клетка: та же строка — пунктир вдоль строки, под числами
        r, c = src[0]
        y = cy(r) + CH / 2
        s += f"<path d='M{cx(c) + CW:.1f} {y:.1f}H{TX:.1f}' stroke='{GOLD}' stroke-opacity='0.6' stroke-width='0.6' stroke-dasharray='1.4 1'/>"
    c0 = src[0][1]
    s += (f"<path d='M{cx(c0) + CW / 2:.1f} {HY - 4.6:.1f}V-2H{TX + CW / 2:.1f}V{HY - 4.6:.1f}' fill='none' "
          f"stroke='{GOLD}' stroke-width='0.7' marker-end='url(#ah{tgt_col})'/>")
    s += txt((cx(c0) + TX + CW) / 2, -3.4, label, GOLD, 3, '700')
    return s
def far_svg(s, label):
    h = HY + 7 * CH + 3
    return f"<svg viewBox='0 -8 {TX + CW + 2:.0f} {h + 8:.1f}' role='img' aria-label='{label}' style='max-width:600px'>{s}</svg>"

c26 = {r: T[(r, 26)] for r in range(1, 8) if (r, 26) in T}
V['в столбце 12 стоят 133'] = fig(far_svg(far([(r, 12) for r in range(1, 8) if (r, 12) in T], 26, c26,
                                              '+ 14 столбцов, числа + 168'), 'Столбец 26'),
                                 'а) Столбец 12 и столбец 26.')
V['127 стоит в строке 5, столбце 11'] = fig(far_svg(far([(5, 11)], 53, {5: 631}, '+ 3 · 14 столбцов'), 'Место 631'),
                                          'б) 127 и 631 в одной строке.')
V['5 стоит в строке 3, столбце 1'] = fig(far_svg(far([(3, 1)], 169, {3: 2021}, '+ 12 · 14 столбцов'), 'Место 2021'),
                                       'в) 5 и 2021 в одной строке.')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
