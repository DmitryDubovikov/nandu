"""Рисунки образца №8 (Т1″, национал 2025 II №4): таблица моментов.

Строка — момент процесса, столбец — коробка, между строками — стрелка переноса из условия, справа — номер уравнения.
План — пустая таблица; в разделе k заполнены строки 1…k, строка k выделена, изменившиеся в ней клетки — золотом.
Запуск: python3 vis/T1pp_nac_2025_4.py T1pp_nac_2025_4.vis.json
"""
import json, sys
GOLD, BLUE, GREEN, RED, WHITE = '#f0a83c', '#5ba8f5', '#5fd38d', '#f2686c', '#dfe6ee'
INK, DIM, LAB = '#cfdae6', '#4a5866', '#e8eef6'

def txt(x, y, s, col=LAB, size=3.6, w='600', anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

BOXES = [('синяя', BLUE), ('белая', WHITE), ('красная', RED), ('зелёная', GREEN)]
CW, CH, GAP = 32, 10, 14            # ширина клетки, высота строки, высота полосы переноса
X0 = 32                              # левый край первой коробки
def cx(i): return X0 + i * (CW + 2)
EQX = cx(4) + 12                     # центр столбца уравнений
HEAD = 7                             # базовая линия заголовков
ROW0 = 10                            # верх первой строки
def rowy(r): return ROW0 + r * (CH + GAP)

MOMENTS = ['сначала', 'после 30', 'в конце']
CELLS = [['a', 'b', 'a', 'v'],
         ['a − 30', 'b + 30', 'a', 'v'],
         ['a − 30', 'v : 2', 'a + v : 2', 'v']]
MOVES = [(0, 1, '30'), (1, 2, 'половина')]   # из какой коробки в какую, подпись

def table(step=None):
    s = (f"<defs><marker id='mv{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
         f"<path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>")
    for i, (name, c) in enumerate(BOXES):
        s += txt(cx(i) + CW / 2, HEAD, name, c, 4.0)
    for r, mom in enumerate(MOMENTS):
        y = rowy(r)
        filled = step is not None and r < step
        cur = step is not None and r == step - 1
        lc = GOLD if cur else (INK if filled else DIM)
        if cur:
            s += f"<rect x='1' y='{y - 1.2}' width='{EQX + 9}' height='{CH + 2.4}' rx='2' fill='{GOLD}' fill-opacity='0.10' stroke='{GOLD}' stroke-width='0.8'/>"
        s += txt(29, y + CH / 2 + 1.4, mom, lc, 3.8, anchor='end')
        s += txt(EQX, y + CH / 2 + 1.3, f'({r + 1})', lc, 3.8)
        for i, (_, c) in enumerate(BOXES):
            if filled:
                s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='{c}' fill-opacity='0.12' stroke='{c}' stroke-width='0.5'/>"
                changed = cur and r > 0 and CELLS[r][i] != CELLS[r - 1][i]
                s += txt(cx(i) + CW / 2, y + CH / 2 + 1.3, CELLS[r][i], GOLD if changed else LAB, 4.2, '700')
            else:
                s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='none' stroke='{DIM}' stroke-width='0.4' stroke-dasharray='1.2 1'/>"
    for r, (a, b, lbl) in enumerate(MOVES):
        y = rowy(r) + CH
        hot = step is not None and step == r + 2
        c = GOLD if hot else (INK if step is not None and step > r + 2 else DIM if step is not None else INK)
        x1, x2 = cx(a) + CW / 2 + 2, cx(b) + CW / 2 - 2
        s += f"<path d='M{x1} {y + 9.8}H{x2}' fill='none' stroke='{c}' stroke-width='{1.0 if hot else 0.6}' marker-end='url(#mv{step})'/>"
        s += txt((x1 + x2) / 2, y + 6.4, lbl, c, 3.8)
    h = rowy(2) + CH + 2
    return f"<svg viewBox='0 0 {EQX + 12} {h}' role='img' aria-label='Таблица моментов' style='max-width:760px'>{s}</svg>"

V = {}
V['Про каждый момент условие говорит'] = fig(table(), 'Коробки по моментам.')
V['Запишем уравнение момента «сначала»'] = fig(table(1))
V['Запишем уравнение момента «после 30»'] = fig(table(2))
V['Запишем уравнение момента «в конце»'] = fig(table(3))
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
