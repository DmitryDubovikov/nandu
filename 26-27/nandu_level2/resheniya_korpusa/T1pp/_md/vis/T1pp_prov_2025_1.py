"""Рисунки: провинциал 2025, №1 (Т1″) — таблица моментов «деньги Эду в начале каждой недели».

Строка — момент (начало недели k), столбец один — деньги у Эду; между строками — стрелка недели: сколько тратит
и какая доля остаётся (множитель). Справа — номер уравнения.
План — пустая таблица. «Заполним строки» — все строки, новые множители золотом;
«Запишем уравнение» — строка 5 обведена золотом, справа «= 210»; б) — строка 3 и стрелка недели 3 золотом.
Запуск: python3 vis/T1pp_prov_2025_1.py T1pp_prov_2025_1.vis.json
"""
import json, sys
GOLD, GREEN = '#f0a83c', '#5fd38d'
INK, DIM, LAB = '#cfdae6', '#4a5866', '#e8eef6'

def txt(x, y, s, col=LAB, size=3.6, w='600', anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

CW, CH, GAP = 96, 11, 13            # ширина клетки, высота строки, высота полосы недели
X0 = 56                              # левый край клетки
EQX = X0 + CW + 22                   # центр столбца уравнений
HEAD = 7
ROW0 = 10
def rowy(r): return ROW0 + r * (CH + GAP)

MOMENTS = [('момент 1', 'подарок'), ('момент 2', 'начало недели 2'), ('момент 3', 'начало недели 3'),
           ('момент 4', 'начало недели 4'), ('момент 5', 'осталось 210')]
CELLS = ['x', 'x · 1/2', 'x · 1/2 · 2/3', 'x · 1/2 · 2/3 · 3/4', 'x · 1/2 · 2/3 · 3/4 · 5/6']
WEEKS = [('тратит 1/2', '· 1/2'), ('тратит 1/3', '· 2/3'), ('тратит 1/4', '· 3/4'), ('тратит 1/6', '· 5/6')]

def table(filled=False, eq=False, week3=False):
    mid = f'{int(filled)}{int(eq)}{int(week3)}'
    s = (f"<defs><marker id='wk{mid}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
         f"<path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>")
    s += txt(X0 + CW / 2, HEAD, 'деньги у Эду', GREEN, 4.0)
    for r, mom in enumerate(MOMENTS):
        y = rowy(r)
        hot = (eq and r == 4) or (week3 and r == 2)
        lc = GOLD if hot else INK
        s += txt(53, y + CH / 2 - 0.8, mom[0], lc, 3.8, '700', anchor='end')
        s += txt(53, y + CH / 2 + 3.6, mom[1], lc, 3.4, anchor='end')
        if r == 4:
            s += txt(EQX, y + CH / 2 + 1.3, '(1)', GOLD if eq else INK, 3.8)
        if filled:
            s += f"<rect x='{X0}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='{GREEN}' fill-opacity='0.12' stroke='{GREEN}' stroke-width='0.5'/>"
            cell = CELLS[r]
            if not eq and not week3 and r > 0:      # новый множитель строки — золотом
                head, last = cell.rsplit(' · ', 1)
                s += (f"<text x='{X0 + CW / 2}' y='{y + CH / 2 + 1.4}' font-size='4.0' text-anchor='middle' font-weight='700'>"
                      f"<tspan fill='{LAB}'>{head} · </tspan><tspan fill='{GOLD}'>{last}</tspan></text>")
            else:
                s += txt(X0 + CW / 2, y + CH / 2 + 1.4, cell, LAB, 4.0, '700')
        else:
            s += f"<rect x='{X0}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='none' stroke='{DIM}' stroke-width='0.4' stroke-dasharray='1.2 1'/>"
        if hot:
            s += f"<rect x='{X0 - 1.2}' y='{y - 1.2}' width='{CW + 2.4}' height='{CH + 2.4}' rx='2' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
        if eq and r == 4:
            s += txt(X0 + CW + 3, y + CH / 2 + 1.3, '= 210', GOLD, 4.0, '700', anchor='start')
    for r, (spend, keep) in enumerate(WEEKS):
        y = rowy(r) + CH
        hot = (week3 and r == 2) or (filled and not eq and not week3)
        c = GOLD if (week3 and r == 2) else (GOLD if hot else INK)
        xm = X0 + CW / 2
        s += f"<path d='M{xm} {y + 1.2}V{y + GAP - 1.6}' fill='none' stroke='{c}' stroke-width='{0.9 if hot else 0.6}' marker-end='url(#wk{mid})'/>"
        s += txt(xm + 3, y + GAP / 2 + 1.4, keep, c, 3.8, '700', anchor='start')
        s += txt(53, y + GAP / 2 + 1.4, f'неделя {r + 1}: {spend}', GOLD if (week3 and r == 2) else INK, 3.5, '600', anchor='end')
    h = rowy(4) + CH + 2
    return f"<svg viewBox='0 0 {EQX + 10} {h}' role='img' aria-label='Таблица моментов' style='max-width:560px'>{s}</svg>"

V = {}
V['осталось $210»: Эду потратил долю'] = fig(table(), 'Пять моментов.')
V['в каждой следующей строке деньги прошлой'] = fig(table(True))
V['Запишем уравнение момента 5'] = fig(table(True, eq=True))
V['потрачена четверть денег момента 3'] = fig(table(True, week3=True))
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
