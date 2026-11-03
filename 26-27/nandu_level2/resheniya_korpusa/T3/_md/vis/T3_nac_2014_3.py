"""Рисунки: национал 2014, №3 — двузначные A > B, сумма и разность двузначные.

Запуск: python3 vis/T3_nac_2014_3.py T3_nac_2014_3.vis.json
"""
import json, sys
GOLD, GREEN, BLUE = '#f0a83c', '#5fd38d', '#5ba8f5'
INK, DIM, LAB = '#cfdae6', '#93a1b1', '#e8eef6'
X0, K, H = 34, 1.5, 9          # x числа 10, шаг на единицу, шаг строк

def x(n):
    return X0 + (n - 10) * K

def row(i, b, lo, hi, cnt):
    y = 8 + i * H
    s = (f"<text x='2' y='{y+1.6}' fill='{LAB}' font-size='4.4'>B = {b}</text>"
         f"<line x1='{x(lo)}' y1='{y}' x2='{x(hi)}' y2='{y}' stroke='{BLUE}' stroke-width='2.4' stroke-linecap='round'/>"
         f"<text x='{x(lo)-2.4}' y='{y+1.4}' fill='{INK}' font-size='3.8' text-anchor='end'>{lo}</text>"
         f"<text x='{x(hi)+2.4}' y='{y+1.4}' fill='{INK}' font-size='3.8' text-anchor='start'>{hi}</text>"
         f"<text x='{x(99)+8}' y='{y+1.6}' fill='{GOLD}' font-size='4.6' font-weight='700' text-anchor='middle'>{cnt}</text>")
    return s

def fig():
    s = f"<text x='{x(99)+8}' y='-1' fill='{DIM}' font-size='3.4' text-anchor='middle'>чисел A</text>"
    for i, b in enumerate((10, 11, 12)):
        s += row(i, b, b + 10, 99 - b, 90 - 2 * b)
    y = 8 + 3 * H
    s += f"<text x='{x(54.5)}' y='{y+1}' fill='{DIM}' font-size='5' text-anchor='middle'>⋮</text>"
    s += f"<text x='{x(99)+8}' y='{y+1}' fill='{DIM}' font-size='5' text-anchor='middle'>⋮</text>"
    s += row(4, 44, 54, 55, 2)
    vb = f'0 -5 {x(99)+16} {8+4*H+9}'
    svg = f"<svg viewBox='{vb}' role='img' aria-label='Подходящие A при разных B' style='max-width:560px'>{s}</svg>"
    return f"<figure class='st'>{svg}<figcaption>Подходящие A при B = 10, 11, 12 и 44.</figcaption></figure>"

V = {'B больше на 1': fig()}
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
