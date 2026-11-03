"""Рисунки: регионал 2015, №1 (Т1″) — таблица моментов: мужчины, женщины, дети.

Строка — момент процесса, столбец — кто на празднике, между строками — действие из условия, справа — номера уравнений.
План — пустая таблица. Раздел k: «заполним строку» — строки 1…k, новые клетки строки k золотом;
«запишем уравнение» — в строке k золотом обведено то, что входит в уравнение.
У момента 2 два уравнения: (2) — весь ряд «всего 380», (3) — мужчины и женщины с дугой «· 2».
Действие 1 → 2 — пришли гости: подписи «+ 27», «+ 37», «+ n» под столбцами.
Запуск: python3 vis/T1pp_reg_2015_1.py [T1pp_reg_2015_1.vis.json]
"""
import json, os, sys
GOLD, BLUE, GREEN, VIOL = '#f0a83c', '#5ba8f5', '#5fd38d', '#b48ef0'
INK, DIM, LAB = '#cfdae6', '#4a5866', '#e8eef6'

def txt(x, y, s, col=LAB, size=3.6, w='600', anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

PEOPLE = [('мужчины', BLUE), ('женщины', VIOL), ('дети', GREEN)]
CW, CH, GAP = 40, 14, 30
X0 = 58
LX = 55                              # правый край подписей моментов
def cx(i): return X0 + i * (CW + 2)
EQX = cx(3) + 34
HEAD = 7
ROW0 = 10
def rowy(r): return ROW0 + r * (CH + GAP)

MOMENTS = [('момент 1', 'всего 260', 'мужчины = 3 · женщины', '(1)'),
           ('момент 2', 'всего 380', 'мужчины = 2 · женщины', '(2), (3)')]
CELLS = [['3w', 'w', 'x'],
         ['3w + 27', 'w + 37', 'x + n']]
# уравнение: (строка, какие клетки обвести ('all' — весь ряд), дуга (откуда, куда, подпись), подпись справа)
EQ = {'1': (0, 'all', None, 'всего 260'),
      '2': (1, 'all', None, 'всего 380'),
      '3': (1, [0, 1], (1, 0, '· 2'), '')}

def eq_marks(key, y):
    _, boxes, arc, right = EQ[key]
    s = ''
    if boxes == 'all':
        s += f"<rect x='{cx(0) - 1.2}' y='{y - 1.2}' width='{cx(2) + CW - cx(0) + 2.4}' height='{CH + 2.4}' rx='2' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
    else:
        for k in boxes:
            s += f"<rect x='{cx(k) - 1.2}' y='{y - 1.2}' width='{CW + 2.4}' height='{CH + 2.4}' rx='2' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
    if right:
        s += txt(cx(2) + CW + 3, y + CH / 2 + 1.3, right, GOLD, 3.8, '700', anchor='start')
    if not arc:
        return s
    i, j, lbl = arc
    x1, x2, yb, d = cx(i) + CW / 2, cx(j) + CW / 2, y + CH + 1.4, 7
    s += f"<path d='M{x1} {yb} C{x1} {yb + d} {x2} {yb + d} {x2} {yb + 0.6}' fill='none' stroke='{GOLD}' stroke-width='0.8' marker-end='url(#arc)'/>"
    s += txt((x1 + x2) / 2, yb + 0.75 * d + 4.0, lbl, GOLD, 4.0, '700')
    return s

def moves(step, eq):
    y = rowy(0) + CH
    hot = step == 2 and eq is None
    c = GOLD if hot else (INK if step is None or step >= 2 else DIM)
    s = txt(LX, y + GAP / 2 - 0.4, 'действие 1 → 2', c, 3.8, '700', anchor='end')
    s += txt(LX, y + GAP / 2 + 3.8, 'пришли ещё', c, 3.5, anchor='end')
    for i, lbl in enumerate(['+ 27', '+ 37', '+ n']):
        s += txt(cx(i) + CW / 2, y + GAP / 2 + 1.4, lbl, c, 4.0, '700')
    return s

def table(step=None, eq=None):
    s = (f"<defs><marker id='arc' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
         f"<path d='M0 0L6 3L0 6z' fill='{GOLD}'/></marker></defs>")
    for i, (name, c) in enumerate(PEOPLE):
        s += txt(cx(i) + CW / 2, HEAD, name, c, 4.0)
    for r, (m, l1, l2, nums) in enumerate(MOMENTS):
        y = rowy(r)
        filled = step is not None and r < step
        cur = step is not None and r == step - 1
        lc = GOLD if cur else (INK if filled or step is None else DIM)
        s += txt(LX, y + CH / 2 - 3.0, m, lc, 3.8, '700', anchor='end')
        s += txt(LX, y + CH / 2 + 1.4, l1, lc, 3.5, anchor='end')
        s += txt(LX, y + CH / 2 + 5.4, l2, lc, 3.5, anchor='end')
        s += txt(EQX, y + CH / 2 + 1.3, nums, lc, 3.8)
        for i, (_, c) in enumerate(PEOPLE):
            if filled:
                s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='{c}' fill-opacity='0.12' stroke='{c}' stroke-width='0.5'/>"
                new = cur and eq is None and (r == 0 or CELLS[r][i] != CELLS[r - 1][i])
                s += txt(cx(i) + CW / 2, y + CH / 2 + 1.3, CELLS[r][i], GOLD if new else LAB, 4.2, '700')
            else:
                s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='none' stroke='{DIM}' stroke-width='0.4' stroke-dasharray='1.2 1'/>"
        if eq is not None and EQ[eq][0] == r:
            s += eq_marks(eq, y)
    s += moves(step, eq)
    h = rowy(1) + CH + (12 if eq == '3' else 2)
    return f"<svg viewBox='0 0 {EQX + 14} {h}' role='img' aria-label='Таблица моментов' style='max-width:760px'>{s}</svg>"

V = {}
V['пришли 27 мужчин, 37 женщин и несколько детей'] = fig(table(), 'Два момента.')
V['3w'] = fig(table(1))
V['«всего 260 человек»'] = fig(table(1, '1'))
V['детей стало на n больше'] = fig(table(2))
V['Запишем уравнения момента 2'] = fig(table(2, '2'))
V['(2) (3w + 27) + (w + 37) + (x + n) = 380'] = fig(table(2, '3'))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'T1pp_reg_2015_1.vis.json')
json.dump(V, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
