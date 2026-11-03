"""Рисунки: регионал 2023, №3 — доска 2 + 4 + 6 клеток, пять чёрных, хотя бы одна в каждой секции.

Запуск: python3 vis/T3p_reg_2023_3.py T3p_reg_2023_3.vis.json
"""
import json, sys
GOLD, GREEN, RED = '#f0a83c', '#5fd38d', '#ef6f6c'
INK, DIM, LAB = '#cfdae6', '#93a1b1', '#e8eef6'
W = 10
SEC = [(0, 2), (2, 6), (6, 12)]          # секции: клетки [от, до)

def board(black=(), green=(), empty=(), big=False, labels=True):
    # black — номера чёрных клеток (с 0); green — секции, где стоят чёрные (заливка);
    # empty — секции без чёрных (красная рамка)
    s = ''
    for k in green:
        a, b = SEC[k]
        s += f"<rect x='{a*W}' y='0' width='{(b-a)*W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
    for i in range(12):
        if i in black:
            s += f"<rect x='{i*W}' y='0' width='{W}' height='{W}' fill='{GOLD}'/>"
        s += f"<rect x='{i*W}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.4'/>"
    for x in (2*W, 6*W):
        s += f"<line x1='{x}' y1='-1' x2='{x}' y2='{W+1}' stroke='{INK}' stroke-width='1.6'/>"
    s += f"<rect x='0' y='0' width='{12*W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.8'/>"
    for k in empty:
        a, b = SEC[k]
        s += f"<rect x='{a*W+0.6}' y='0.6' width='{(b-a)*W-1.2}' height='{W-1.2}' fill='none' stroke='{RED}' stroke-width='0.9'/>"
    if labels:
        for k, (a, b) in enumerate(SEC):
            s += (f"<text x='{(a+b)*W/2}' y='{W+5.5}' fill='{DIM}' font-size='3.6' text-anchor='middle'>"
                  f"секция {k+1}</text>")
    vb = f'-1 -2 {12*W+2} {W+10}'
    st = " style='max-width:560px'" if big else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='Доска'{st}>{s}</svg>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

def grid(cells, cap=''):
    c = ''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s, t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>", cap)

V = {}
V['Способ — сочетание'] = fig(board(big=True), 'Доска Даниэля.')
V['Заметим: если все пять чёрных клеток стоят в секции 3'] = fig(
    board(black=(6, 7, 8, 10, 11), empty=(0, 1), big=True),
    'Все пять чёрных клеток в секции 3: секции 1 и 2 пусты.')
V['2. N(пустая 1), N(пустая 2), N(пустая 3).'] = grid([
    (board(green=(1, 2), empty=(0,)), 'N(пустая 1): десять клеток'),
    (board(green=(0, 2), empty=(1,)), 'N(пустая 2): восемь клеток'),
    (board(green=(0, 1), empty=(2,)), 'N(пустая 3): шесть клеток'),
], 'Красная рамка — пустая секция; зелёным — клетки, где стоят все пять чёрных.')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
