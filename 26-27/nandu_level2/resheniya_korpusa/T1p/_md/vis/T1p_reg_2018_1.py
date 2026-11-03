"""Рисунки: регионал 2018, №1 — деньги Аны, Беатрис и Карлы в понедельник и во вторник.

Запуск: python3 vis/T1p_reg_2018_1.py [T1p_reg_2018_1.vis.json]
"""
import json, os, sys
GOLD, BLUE, GREEN = '#f0a83c', '#5ba8f5', '#5fd38d'
INK, DIM, LAB, MUT = '#cfdae6', '#4a5866', '#e8eef6', '#93a1b1'
COL = {'Ана': BLUE, 'Беатрис': GOLD, 'Карла': GREEN}

def txt(x, y, s, col=LAB, size=3.6, w='600', anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"
def svg(inner, label, vb, mw=480):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

BW, BH, X0 = 11, 8, 34   # кирпичик x: ширина, высота; начало полос

def bricks(y, groups):
    """Полоса из кирпичиков x: groups = [(чьи, сколько)], каждый кирпичик подписан x."""
    s, x = '', X0
    for who, k in groups:
        col = COL[who]
        for i in range(k):
            s += f"<rect x='{x + i*BW}' y='{y}' width='{BW}' height='{BH}' fill='{col}' fill-opacity='0.22' stroke='{INK}' stroke-width='0.4'/>"
            s += txt(x + i*BW + BW/2, y + BH/2 + 1.3, 'x', LAB, 3.6)
        s += f"<rect x='{x}' y='{y}' width='{k*BW}' height='{BH}' fill='none' stroke='{col}' stroke-width='0.9'/>"
        x += k * BW
    return s

def row_label(y, word, col):
    return txt(X0 - 3, y + BH/2 + 1.3, word, col, 3.6, '600', 'end')

# 1/5: Беатрис — пять кирпичиков, у Аны один такой
def fifth():
    s = row_label(4, 'Беатрис', GOLD) + bricks(4, [('Беатрис', 5)])
    s += row_label(17, 'Ана', BLUE) + bricks(17, [('Ана', 1)])
    s += txt(X0 + BW + 3, 17 + BH/2 + 1.3, '1/5 Беатрис', BLUE, 3.4, '600', 'start')
    return svg(s, 'Беатрис и Ана в понедельник', '0 0 100 28', 420)

# 1/2: Ана и Беатрис вместе — шесть кирпичиков, у Карлы половина
def half():
    s = row_label(4, 'Ана и Беатрис', MUT) + bricks(4, [('Ана', 1), ('Беатрис', 5)])
    s += row_label(17, 'Карла', GREEN) + bricks(17, [('Карла', 3)])
    s += txt(X0 + 3*BW + 3, 17 + BH/2 + 1.3, '1/2 Аны и Беатрис', GREEN, 3.4, '600', 'start')
    return svg(s, 'Карла — половина Аны и Беатрис вместе', '0 0 108 28', 460)

# таблица моментов: понедельник → вторник
def moments():
    x0, cw, ch = 30, 26, 10
    heads = ['Ана', 'Беатрис', 'Карла']
    mon = ['x', '5x', '3x']
    tue = ['x + 225', '5x − 360', '3x + 135']
    s = ''
    for i, h in enumerate(heads):
        s += txt(x0 + i*cw + cw/2, 5, h, COL[h], 3.6)
    y1, y2 = 8, 30
    s += txt(x0 - 3, y1 + ch/2 + 1.3, 'понедельник', MUT, 3.4, '600', 'end')
    s += txt(x0 - 3, y2 + ch/2 + 1.3, 'вторник', MUT, 3.4, '600', 'end')
    for i in range(3):
        s += f"<rect x='{x0 + i*cw}' y='{y1}' width='{cw}' height='{ch}' fill='none' stroke='{DIM}' stroke-width='0.5'/>"
        s += txt(x0 + i*cw + cw/2, y1 + ch/2 + 1.3, mon[i], LAB, 3.8)
        s += f"<rect x='{x0 + i*cw}' y='{y2}' width='{cw}' height='{ch}' fill='{GOLD}' fill-opacity='0.18' stroke='{DIM}' stroke-width='0.5'/>"
        s += txt(x0 + i*cw + cw/2, y2 + ch/2 + 1.3, tue[i], GOLD, 3.6)
    ym = (y1 + ch + y2) / 2
    s += f"<defs><marker id='ahm' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='{INK}'/></marker></defs>"
    s += f"<path d='M{x0 - 14} {y1 + ch + 2}V{y2 - 2}' fill='none' stroke='{INK}' stroke-width='0.6' marker-end='url(#ahm)'/>"
    s += txt(x0 + 1.5*cw, ym + 1.2, 'Беатрис даёт 225 Ане и 135 Карле', INK, 3.3, '500')
    return svg(s, 'Деньги в понедельник и во вторник', '0 0 112 42', 520)

# 3/4 во вторник: Ана и Карла вместе — четыре равные части, у Беатрис три такие
def quarter():
    pw = 16; x0 = 34; s = ''
    s += txt(x0 - 3, 4 + 4 + 1.3, 'Ана и Карла', MUT, 3.6, '600', 'end')
    for i in range(4):
        s += f"<rect x='{x0 + i*pw}' y='4' width='{pw}' height='8' fill='{BLUE}' fill-opacity='0.12' stroke='{DIM}' stroke-width='0.4'/>"
    s += f"<rect x='{x0}' y='4' width='{4*pw}' height='8' fill='none' stroke='{INK}' stroke-width='0.9'/>"
    s += f"<text x='{x0 + 2*pw}' y='9.4' fill='{LAB}' font-size='4' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>4x + 360</text>"
    s += txt(x0 - 3, 17 + 4 + 1.3, 'Беатрис', GOLD, 3.6, '600', 'end')
    for i in range(3):
        s += f"<rect x='{x0 + i*pw}' y='17' width='{pw}' height='8' fill='{GOLD}' fill-opacity='0.25' stroke='{INK}' stroke-width='0.4'/>"
    s += f"<rect x='{x0}' y='17' width='{3*pw}' height='8' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
    s += f"<text x='{x0 + 1.5*pw}' y='22.4' fill='{LAB}' font-size='4' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>5x − 360</text>"
    s += txt(x0 + 3*pw + 3, 17 + 4 + 1.3, '3/4', GOLD, 3.6, '600', 'start')
    return svg(s, 'Вторник: Беатрис — 3/4 Аны и Карлы вместе', '0 0 104 28', 480)

V = {}
V['у Беатрис пять кирпичиков x'] = fig(fifth(), 'Понедельник: Беатрис и Ана.')
V['у Карлы половина: три кирпичика x'] = fig(half(), 'Понедельник: Ана и Беатрис вместе, Карла.')
V['у Беатрис стало на 225 + 135 = 360 меньше'] = fig(moments(), 'Деньги по дням.')
V['у Беатрис три части'] = fig(quarter(), 'Вторник: Ана и Карла вместе, Беатрис.')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'T1p_reg_2018_1.vis.json')
json.dump(V, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
