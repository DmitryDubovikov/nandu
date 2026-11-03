"""Рисунки нац 2020 I №1 (Т1″, конфеты Хуана): таблица дней.

Строка — день, столбец — что происходит с мешком за день; между строками — переход «день 1 → 2», справа — номер уравнения.
План — пустая таблица. Раздел k: «заполним строку» — строки 1…k, новые клетки строки k золотом;
«запишем уравнение» — в строке k золотом обведены «съел» и «подарил», под ними дуга «+», справа «= d».
Запуск: python3 vis/T1pp_nac_2020_1.py T1pp_nac_2020_1.vis.json
"""
import json, sys
GOLD, BLUE, GREEN, RED, WHITE = '#f0a83c', '#5ba8f5', '#5fd38d', '#f2686c', '#dfe6ee'
INK, DIM, LAB = '#cfdae6', '#4a5866', '#e8eef6'

def txt(x, y, s, col=LAB, size=3.6, w='600', anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

COLS = [('утром в мешке', BLUE), ('съел', RED), ('осталось', WHITE), ('подарил', GREEN)]
CW, CH, GAP = 50, 14, 30
X0 = 78
LX = X0 - 3                          # правый край подписей первой колонки
def cx(i): return X0 + i * (CW + 2)
EQX = cx(4) + 22
HEAD = 8
ROW0 = 12
def rowy(r): return ROW0 + r * (CH + GAP)

DAYS = [('день 1', 'съел 1 + подарил', '= вынул за день'), ('день 2', 'съел 2 + подарил', '= вынул за день')]
CELLS = [['b', '1', 'b − 1', '(b − 1) : 10'],
         ['b − d', '2', 'b − d − 2', '(b − d − 2) : 10']]

def eq_marks(y):
    s = ''
    for k in (1, 3):
        s += f"<rect x='{cx(k) - 1.2}' y='{y - 1.2}' width='{CW + 2.4}' height='{CH + 2.4}' rx='2' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
    x1, x2, yb, d = cx(1) + CW / 2, cx(3) + CW / 2, y + CH + 1.4, 7
    s += f"<path d='M{x1} {yb} C{x1} {yb + d} {x2} {yb + d} {x2} {yb + 0.6}' fill='none' stroke='{GOLD}' stroke-width='0.8'/>"
    s += txt((x1 + x2) / 2, yb + 0.75 * d + 4.6, '+', GOLD, 5.2, '700')
    s += txt(cx(3) + CW + 3, y + CH / 2 + 1.3, '= d', GOLD, 5.0, '700', anchor='start')
    return s

def table(step=None, eq=False):
    mid = f'{step}{"e" if eq else "f"}'
    s = (f"<defs><marker id='mv{mid}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
         f"<path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>")
    for i, (name, c) in enumerate(COLS):
        s += txt(cx(i) + CW / 2, HEAD, name, c, 5.0)
    for r, day in enumerate(DAYS):
        y = rowy(r)
        filled = step is not None and r < step
        cur = step is not None and r == step - 1
        lc = GOLD if cur else (INK if filled or step is None else DIM)
        s += txt(LX, y + CH / 2 - 3.6, day[0], lc, 4.8, '700', anchor='end')
        s += txt(LX, y + CH / 2 + 1.4, day[1], lc, 4.2, anchor='end')
        s += txt(LX, y + CH / 2 + 6.0, day[2], lc, 4.2, anchor='end')
        s += txt(EQX, y + CH / 2 + 1.3, f'({r + 1})', lc, 4.6)
        for i, (_, c) in enumerate(COLS):
            if filled:
                s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='{c}' fill-opacity='0.12' stroke='{c}' stroke-width='0.5'/>"
                s += txt(cx(i) + CW / 2, y + CH / 2 + 1.8, CELLS[r][i], GOLD if cur and not eq else LAB, 5.2, '700')
            else:
                s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='none' stroke='{DIM}' stroke-width='0.4' stroke-dasharray='1.2 1'/>"
        if cur and eq:
            s += eq_marks(y)
    # переход день 1 → 2: утром дня 2 в мешке на d меньше
    y = rowy(0) + CH
    hot = step == 2 and not eq
    c = GOLD if hot else (INK if step is None or step >= 2 else DIM)
    xa = cx(0) + CW / 2
    s += f"<path d='M{xa} {y + 3}V{y + GAP - 3}' fill='none' stroke='{c}' stroke-width='{1.0 if hot else 0.6}' marker-end='url(#mv{mid})'/>"
    s += txt(xa + 3, y + GAP / 2 + 1.3, '− d', c, 4.6, '700', anchor='start')
    s += txt(LX, y + GAP / 2 - 0.4, 'день 1 → 2', c, 4.6, '700', anchor='end')
    s += txt(LX, y + GAP / 2 + 3.8, 'за день ушло d', c, 4.2, anchor='end')
    h = rowy(1) + CH + (12 if step == 2 and eq else 2)
    return f"<svg viewBox='0 0 {EQX + 8} {h}' role='img' aria-label='Таблица дней' style='max-width:760px'>{s}</svg>"

V = {}
V['Хуан съел 2 конфеты и подарил'] = fig(table(), 'Два дня.')
V['подарил 1/10 того, что осталось после еды дня 1'] = fig(table(1))
V['Запишем уравнение дня 1'] = fig(table(1, eq=True))
V['подарил 1/10 того, что осталось после еды дня 2'] = fig(table(2))
V['Запишем уравнение дня 2'] = fig(table(2, eq=True))
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
