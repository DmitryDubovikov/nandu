"""Рисунки: регионал 2022, №1 (Т1″) — таблица моментов: Диего, Офелия, Пабло.

Строка — момент процесса, столбец — человек, между строками — действие из условия, справа — номер уравнения.
План — пустая таблица. Раздел k: «заполним строку» — строки 1…k, новые клетки строки k золотом;
«запишем уравнение» — в строке k золотом обведено то, что входит в равенство момента.
Действие 1 → 2 — продажа (наклейки уходят из таблицы): подписи «− 30», «− треть» под столбцами.
Действие 2 → 3 — подарки: стрелки от Диего к Офелии и к Пабло.
Запуск: python3 vis/T1pp_reg_2022_1.py [T1pp_reg_2022_1.vis.json]
"""
import json, os, sys
GOLD, BLUE, GREEN, VIOL = '#f0a83c', '#5ba8f5', '#5fd38d', '#b48ef0'
INK, DIM, LAB = '#cfdae6', '#4a5866', '#e8eef6'

def txt(x, y, s, col=LAB, size=3.6, w='600', anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

PEOPLE = [('Диего', BLUE), ('Офелия', VIOL), ('Пабло', GREEN)]
CW, CH, GAP = 40, 12, 30
X0 = 54
def cx(i): return X0 + i * (CW + 2)
EQX = cx(3) + 26
HEAD = 7
ROW0 = 10
def rowy(r): return ROW0 + r * (CH + GAP)

MOMENTS = [('момент 1', 'всего 271'), ('момент 2', 'всего 212'), ('момент 3', 'Диего = 2 · Пабло')]
CELLS = [['d', 'x', 'p'],
         ['d − 30', 'x − x : 3', 'p'],
         ['d − 50', 'x − x : 3 + 10', 'p + 10']]
# уравнение момента: какие клетки обвести ('all' — весь ряд), дуга (откуда, куда, подпись), подпись справа
EQ = [('all', None, 'всего 271'),
      ('all', None, 'всего 212'),
      ([0, 2], (2, 0, '· 2'), '')]

def eq_marks(r, y):
    boxes, arc, right = EQ[r]
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

def moves(step, eq, mid):
    s = ''
    for r, act in enumerate(['продажа', 'подарки по 10']):
        y = rowy(r) + CH
        hot = step is not None and step == r + 2 and not eq
        c = GOLD if hot else (INK if step is None or step >= r + 2 else DIM)
        sw = 1.0 if hot else 0.6
        s += txt(51, y + GAP / 2 - 0.4, f'действие {r + 1} → {r + 2}', c, 3.8, '700', anchor='end')
        s += txt(51, y + GAP / 2 + 3.8, act, c, 3.5, anchor='end')
        if r == 0:      # продажа: наклейки уходят, у Пабло без изменений
            for i, lbl in [(0, '− 30'), (1, '− треть')]:
                s += txt(cx(i) + CW / 2, y + GAP / 2 + 1.4, lbl, c, 4.0, '700')
        else:           # подарки: от Диего к Офелии и к Пабло
            for j, ya in [(1, y + 10), (2, y + 21)]:
                x1, x2 = cx(0) + CW / 2 + 2, cx(j) + CW / 2 - 2
                s += f"<path d='M{x1} {ya}H{x2}' fill='none' stroke='{c}' stroke-width='{sw}' marker-end='url(#mv{mid})'/>"
                lx = (x1 + x2) / 2 if j == 1 else (cx(1) + cx(2) + CW) / 2
                s += txt(lx, ya - 1.6, '10', c, 3.8)
    return s

def table(step=None, eq=False):
    mid = f'{step}{"e" if eq else "f"}'
    s = (f"<defs><marker id='mv{mid}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
         f"<path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker>"
         f"<marker id='arc' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
         f"<path d='M0 0L6 3L0 6z' fill='{GOLD}'/></marker></defs>")
    for i, (name, c) in enumerate(PEOPLE):
        s += txt(cx(i) + CW / 2, HEAD, name, c, 4.0)
    for r, mom in enumerate(MOMENTS):
        y = rowy(r)
        filled = step is not None and r < step
        cur = step is not None and r == step - 1
        lc = GOLD if cur else (INK if filled or step is None else DIM)
        s += txt(51, y + CH / 2 - 1.0, mom[0], lc, 3.8, '700', anchor='end')
        s += txt(51, y + CH / 2 + 3.6, mom[1], lc, 3.5, anchor='end')
        s += txt(EQX, y + CH / 2 + 1.3, f'({r + 1})', lc, 3.8)
        for i, (_, c) in enumerate(PEOPLE):
            if filled:
                s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='{c}' fill-opacity='0.12' stroke='{c}' stroke-width='0.5'/>"
                new = cur and not eq and (r == 0 or CELLS[r][i] != CELLS[r - 1][i])
                s += txt(cx(i) + CW / 2, y + CH / 2 + 1.3, CELLS[r][i], GOLD if new else LAB, 4.2, '700')
            else:
                s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='none' stroke='{DIM}' stroke-width='0.4' stroke-dasharray='1.2 1'/>"
        if cur and eq:
            s += eq_marks(r, y)
    s += moves(step, eq, mid)
    h = rowy(2) + CH + (12 if step == 3 and eq else 2)
    return f"<svg viewBox='0 0 {EQX + 12} {h}' role='img' aria-label='Таблица моментов' style='max-width:760px'>{s}</svg>"

V = {}
V['Диего подарил по 10 наклеек Офелии и Пабло'] = fig(table(), 'Три момента.')
V['d, x, p — сколько наклеек в момент 1'] = fig(table(1))
V['Запишем уравнение момента 1'] = fig(table(1, eq=True))
V['У Пабло всё как в момент 1'] = fig(table(2))
V['Запишем уравнение момента 2'] = fig(table(2, eq=True))
V['у Офелии и у Пабло стало на 10 больше'] = fig(table(3))
V['Запишем уравнение момента 3'] = fig(table(3, eq=True))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'T1pp_reg_2022_1.vis.json')
json.dump(V, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
