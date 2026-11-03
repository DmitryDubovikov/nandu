"""Рисунки: национал 2017, день I, №1 — монеты моряков Альдо и Бето и пирата Джека.

Таблица дней: строка — день, столбцы — Альдо, Бето, Джек; между строками — сколько отдал и получил каждый
(словами условия: «−2» у того, у кого больше, «+3» у того, у кого меньше). Строки повтора обведены золотом,
справа дуга «+1 каждому» / «−1 каждому».
Запуск: python3 vis/T1pp_nac_2017_1.py T1pp_nac_2017_1.vis.json
"""
import json, sys
GOLD, BLUE, GREEN, RED = '#f0a83c', '#5ba8f5', '#5fd38d', '#f2686c'
INK, DIM, LAB = '#cfdae6', '#7d8b99', '#e8eef6'

def txt(x, y, s, col=LAB, size=3.6, w='600', anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

COLS = [('Альдо', BLUE), ('Бето', GREEN), ('Джек', RED)]
CW, CH, GAP = 26, 10, 6
X0 = 26
def cx(i): return X0 + i * (CW + 2)

def run():
    a, b, p, d = 20, 6, 50, 0
    rows = {0: (a, b, p)}
    while p > 0:
        if a > b: a, b = a - 2, b + 3
        else: a, b = a + 3, b - 2
        p -= 1; d += 1; rows[d] = (a, b, p)
    while (a if a > b else b) >= 3:
        if a > b: a, b = a - 3, b + 2
        else: a, b = a + 2, b - 3
        p += 1; d += 1; rows[d] = (a, b, p)
    return rows
ROWS = run()

def table(days, gold=(), sign=+1, stop=None, label='день'):
    s = (f"<defs><marker id='ar{days[0]}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
         f"<path d='M0 0L6 3L0 6z' fill='{GOLD}'/></marker></defs>")
    for i, (n, c) in enumerate(COLS):
        s += txt(cx(i) + CW / 2, 6, n, c, 4.0)
    y0 = 9
    ys = {}
    for k, d in enumerate(days):
        y = y0 + k * (CH + GAP)
        ys[d] = y
        hot = d in gold
        s += txt(X0 - 3, y + CH / 2 + 1.3, f'{label} {d}', GOLD if hot else INK, 3.6, '700', anchor='end')
        for i, (_, c) in enumerate(COLS):
            s += f"<rect x='{cx(i)}' y='{y}' width='{CW}' height='{CH}' rx='1' fill='{c}' fill-opacity='0.12' stroke='{c}' stroke-width='0.5'/>"
            s += txt(cx(i) + CW / 2, y + CH / 2 + 1.4, ROWS[d][i], LAB, 4.2, '700')
        if hot:
            s += f"<rect x='{cx(0) - 1.2}' y='{y - 1.2}' width='{cx(1) + CW - cx(0) + 2.4}' height='{CH + 2.4}' rx='2' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
        if k and days[k - 1] == d - 1:   # изменение за день — в промежутке над строкой
            pa, pb, _ = ROWS[d - 1]
            for i in range(3):
                ch = ROWS[d][i] - ROWS[d - 1][i]
                t = f'+{ch}' if ch > 0 else f'−{-ch}'
                s += txt(cx(i) + CW / 2, y - GAP / 2 + 1.2, t, DIM, 3.2, '600')
        elif k:
            s += txt(cx(1) + CW / 2, y - GAP / 2 + 1.4, '…', DIM, 4.0)
    xr = cx(2) + CW + 3
    g = sorted(gold)
    for d1, d2 in zip(g, g[1:]):
        y1, y2 = ys[d1] + CH / 2, ys[d2] + CH / 2
        s += f"<path d='M{xr} {y1} C{xr + 7} {y1} {xr + 7} {y2} {xr + 1} {y2}' fill='none' stroke='{GOLD}' stroke-width='0.8' marker-end='url(#ar{days[0]})'/>"
        s += txt(xr + 8, (y1 + y2) / 2 + 1.2, '+1 каждому моряку' if sign > 0 else '−1 каждому моряку', GOLD, 3.4, '700', anchor='start')
    if stop is not None:
        y = ys[stop]
        s += txt(cx(2) + CW + 3, y + CH / 2 + 1.3, 'у Бето больше, но 2 < 3', RED, 3.4, '700', anchor='start')
    h = y0 + len(days) * (CH + GAP) - GAP + 2
    w = cx(2) + CW + 52
    return f"<svg viewBox='0 0 {w} {h}' role='img' aria-label='Таблица дней' style='max-width:520px'>{s}</svg>"

V = {}
V['Выпишем первые дни правила 1'] = fig(table(list(range(0, 8)), gold=(2, 4, 6)), 'Первые дни правила 1.')
V['Выпишем первые дни правила 2'] = fig(table(list(range(50, 55)), gold=(50, 52, 54), sign=-1), 'Первые дни правила 2.')
V['Выпишем дни 122 и 123'] = fig(table([122, 123], stop=123), 'Последние дни правила 2.')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
