"""Рисунки: регионал 2014, №3 — 9 одинаковых шариков по 5 мешочкам, перегородки в промежутках.

Запуск: python3 vis/T3_reg_2014_3.py T3_reg_2014_3.vis.json
"""
import json, sys
BLUE = '#5ba8f5'
INK, DIM, LAB = '#cfdae6', '#93a1b1', '#e8eef6'
BAGS = ['#ff7a7a', '#f0a83c', '#f5d76e', '#5fd38d', '#93a1b1']   # красный, оранжевый, жёлтый, зелёный, серый
S, R = 9, 3                      # шаг шариков, радиус шарика
X0, ROW = 44, 16                 # начало ряда (слева подпись раскладки), высота строки

def bx(i):                       # центр шарика i = 0..8
    return X0 + S / 2 + i * S

def row(parts, y, gaps=False):
    s = (f"<text x='{X0 - 4}' y='{y + 1.6}' fill='{LAB}' font-size='4.6' text-anchor='end' "
         f"font-weight='700'>{', '.join(map(str, parts))}</text>")
    i = 0
    for k, n in enumerate(parts):
        s += (f"<rect x='{X0 + i * S}' y='{y - S / 2}' width='{n * S}' height='{S}' rx='1.5' "
              f"fill='{BAGS[k]}' fill-opacity='0.28'/>")
        i += n
    for i in range(9):
        s += f"<circle cx='{bx(i)}' cy='{y}' r='{R}' fill='{LAB}' stroke='{INK}' stroke-width='0.4'/>"
    i = 0
    for n in parts[:-1]:
        i += n
        x = X0 + i * S
        s += f"<line x1='{x}' y1='{y - S / 2 - 1.5}' x2='{x}' y2='{y + S / 2 + 1.5}' stroke='{BLUE}' stroke-width='1.3'/>"
    if gaps:
        for j in range(1, 9):
            s += (f"<text x='{X0 + j * S}' y='{y + S / 2 + 6}' fill='{DIM}' font-size='3.6' "
                  f"text-anchor='middle'>{j}</text>")
    return s

def fig():
    rows = [((2, 1, 3, 2, 1), True), ((5, 1, 1, 1, 1), False), ((1, 1, 1, 1, 5), False)]
    s, y = '', 8
    for parts, g in rows:
        s += row(parts, y, g)
        y += ROW + (6 if g else 0)
    h = y - ROW + 8
    svg = (f"<svg viewBox='0 0 {X0 + 9 * S + 2} {h}' role='img' aria-label='Раскладки шариками в ряд' "
           f"style='max-width:460px'>{s}</svg>")
    return (f"<figure class='st'>{svg}<figcaption>Раскладки шариками в ряд; "
            f"под первой — номера промежутков.</figcaption></figure>")

V = {}
V['Раскладки (2, 1, 3, 2, 1)'] = fig()
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
