"""Рисунки: национал 2016, №3 — диаграмма 2 × 3 кружков со стрелками, числа 1–6 с повторами.

Запуск: python3 vis/T3p_nac_2016_3.py T3p_nac_2016_3.vis.json
"""
import json, sys
GOLD, GREEN = '#f0a83c', '#5fd38d'
INK, DIM, LAB = '#cfdae6', '#93a1b1', '#e8eef6'
R, DX, DY = 6, 24, 22          # радиус кружка, шаг по столбцам и по строкам
SUB = '₁₂₃₄₅₆'

def ctr(i):
    # кружок c_{i+1}: верхняя строка c₁ c₂ c₃, нижняя c₄ c₅ c₆
    return (R + 2 + (i % 3) * DX, R + 2 + (i // 3) * DY)

def arrow(x1, y1, x2, y2):
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{INK}' stroke-width='0.7' "
            f"marker-end='url(#ah)'/>")

def diagram(vals, green=(), big=False):
    # vals: 6 элементов; число — стоит в кружке, None — свободный кружок cᵢ
    s = (f"<defs><marker id='ah' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' "
         f"orient='auto'><path d='M0,0 L6,3 L0,6 z' fill='{INK}'/></marker></defs>")
    for i in range(6):
        x, y = ctr(i)
        if i % 3 < 2:
            s += arrow(x + R + 1.5, y, x + DX - R - 2, y)
        if i < 3:
            s += arrow(x, y + R + 1.5, x, y + DY - R - 2)
    for i, v in enumerate(vals):
        x, y = ctr(i)
        if i + 1 in green:
            s += f"<circle cx='{x}' cy='{y}' r='{R}' fill='{GREEN}' fill-opacity='0.22'/>"
        s += f"<circle cx='{x}' cy='{y}' r='{R}' fill='none' stroke='{INK}' stroke-width='0.6'/>"
        if v is None:
            s += (f"<text x='{x}' y='{y+1.6}' fill='{DIM}' font-size='4.4' text-anchor='middle' "
                  f"font-style='italic'>c{SUB[i]}</text>")
        else:
            s += (f"<text x='{x}' y='{y+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' "
                  f"font-weight='700'>{v}</text>")
    vb = f'0 0 {2*R + 4 + 2*DX} {2*R + 4 + DY}'
    st = " style='max-width:360px'" if big else " style='max-width:240px'"
    return f"<svg viewBox='{vb}' role='img' aria-label='Диаграмма'{st}>{s}</svg>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

N = None
V = {}
V['Способ — заполнение кружков'] = fig(diagram([N] * 6, big=True), 'cᵢ — число в i-м кружке.')
V['1. Мир N(2, 3).'] = fig(diagram([N, 2, N, N, 3, N], green=(1, 4, 3, 6)), 'N(2, 3)')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
