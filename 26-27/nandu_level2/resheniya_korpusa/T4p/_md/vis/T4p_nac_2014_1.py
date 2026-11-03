"""Рисунки к Т4′ национал 2014 I №1: полоса из 13 клеток, 3 в клетке 2, 11 в клетке 8,
любые четыре подряд дают 49, все 13 дают 166.

Запуск: python3 vis/T4p_nac_2014_1.py T4p_nac_2014_1.vis.json
"""
import json, sys
GOLD, BLUE, GREEN, VIOLET = '#f0a83c', '#5ba8f5', '#5fd38d', '#b48ef0'
INK, DIM, LAB, MUT = '#cfdae6', '#4a5866', '#e8eef6', '#93a1b1'
CLS = {1: GOLD, 2: GREEN, 3: BLUE, 0: VIOLET}          # цвет по номеру клетки mod 4
SUB = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
def vn(i): return 'v' + str(i).translate(SUB)

CW, CH, LX, TY = 10, 8, 2, 8              # клетка, левый край, верх полосы
def cx(i): return LX + (i - 1) * CW
def txt(x, y, s, col=LAB, size=3.4, w='600', cls='', extra=''):
    k = f" class='{cls}'" if cls else ''
    return f"<text{k} x='{x:.1f}' y='{y:.1f}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'{extra}>{s}</text>"
def cell(i, fill=None, op=0.25, stroke=INK, w=0.4, y=TY):
    f = f"fill='{fill}' fill-opacity='{op}'" if fill else "fill='none'"
    return f"<rect x='{cx(i):.1f}' y='{y:.1f}' width='{CW}' height='{CH}' {f} stroke='{stroke}' stroke-width='{w}'/>"
def num(i, s, col=LAB, size=3.4, y=TY):
    return txt(cx(i) + CW / 2, y + CH / 2 + 1.2, s, col, size)
def heads(n=13, y=TY - 2):
    return ''.join(txt(cx(i) + CW / 2, y, i, MUT, 2.6) for i in range(1, n + 1))
def svg(inner, label, w, h, y0=0, mw=560):
    return f"<svg viewBox='0 {y0} {w} {h}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap='', fx=False):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st{' fx' if fx else ''}'>{inner}{c}</figure>"
W13 = cx(14) + 2

V = {}

# условие: полоса, клетки пронумерованы, 3 и 11 на месте
s = heads()
for i in range(1, 14):
    s += cell(i)
s += num(2, 3) + num(8, 11)
V['Заполни полосу.'] = fig(svg(s, 'Полоса из условия', W13, TY + CH + 2), 'Полоса из условия; клетки пронумерованы.')

# четвёрка 1–4 сдвигается на одну клетку: клетка 1 уходит, клетка 5 приходит, сумма та же
def slide():
    n = 5
    s = heads(n, TY - 3.8)                                  # номера выше едущей рамки
    for i in range(1, n + 1):
        col = GOLD if i in (1, 5) else None
        s += cell(i, col, 0.2 if col else 0, GOLD if col else INK, 0.6 if col else 0.4)
        s += num(i, vn(i), GOLD if col else LAB, 3.2)
    # неподвижная рамка 1–4 и рамка, которая едет на 2–5
    y, h = TY - 0.9, CH + 1.8
    s += f"<rect x='{cx(1) - 0.6:.1f}' y='{y:.1f}' width='{4 * CW + 1.2}' height='{h}' rx='1' fill='none' stroke='{BLUE}' stroke-width='0.7' stroke-dasharray='1.4 1'/>"
    s += txt(cx(1) + 2 * CW, TY + CH + 5.5, 'сумма 49', BLUE, 3)
    s += (f"<g class='sl' style='--to:translate({CW}px,0px);--d:.4s'>"
          f"<rect x='{cx(1) - 0.6:.1f}' y='{y - 1.6:.1f}' width='{4 * CW + 1.2}' height='{h + 3.2}' rx='1.2' fill='none' stroke='{GOLD}' stroke-width='0.8'/></g>")
    s += f"<g class='fi' style='--d:1.6s'>{txt(cx(3) + CW / 2, TY + CH + 10.5, 'сдвиг на клетку: сумма снова 49', GOLD, 3)}</g>"
    s += f"<g class='fi' style='--d:1.6s'>{txt(cx(1) + CW / 2, TY + CH + 5.5, '− ' + vn(1), GOLD, 3.2, '700')}{txt(cx(5) + CW / 2, TY + CH + 5.5, '+ ' + vn(5), GOLD, 3.2, '700')}</g>"
    return svg(s, 'Четвёрки 1–4 и 2–5', cx(n + 1) + 2, TY + CH + 15, 0, 300)
V['вычтем из второго равенства первое'] = fig(slide(), 'Четвёрки 1–4 и 2–5: ушла клетка 1, пришла клетка 5.', fx=True)

# все равенства соседних четвёрок: дуги «через 4» в каждом классе, цвет — класс
def chains(vals=None):
    s = ''
    for i in range(1, 14):
        col = CLS[i % 4]
        s += cell(i, col, 0.22, col, 0.6)
        s += num(i, vals[i] if vals else vn(i), LAB, 3.2)
    for i in range(1, 10):
        col = CLS[i % 4]
        up = i % 2 == 1                                    # классы 1 и 3 — дуги сверху, 2 и 4 — снизу
        lvl = 4.5 if i % 4 in (1, 2) else 8.5
        a, b = cx(i) + CW / 2 + 1.2, cx(i + 4) + CW / 2 - 1.2      # концы дуг не сливаются в одну линию
        if up:
            y0, y1 = TY, TY - lvl
        else:
            y0, y1 = TY + CH, TY + CH + lvl
        s += f"<path d='M{a:.1f} {y0}V{y1}H{b:.1f}V{y0}' fill='none' stroke='{col}' stroke-width='0.6'/>"
        s += txt((a + b) / 2 + CW / 2, y1 - 0.8 if up else y1 + 3, '=', col, 3, '700')   # между клетками, мимо вертикалей
    return s
V['для каждых двух соседних четвёрок полосы'] = fig(
    svg(chains(), 'Равенства через 4 клетки', W13, TY + CH + 20, -6), 'Равные числа через 4 клетки; цвет — клетки с одинаковым числом.')

# полоса через две буквы: v₁ золотом, v₃ синим, данные 3 и 11 — белым
LET = {1: vn(1), 2: '3', 3: vn(3), 0: '11'}
def strip(vals, hl=None):
    s = heads()
    for i in range(1, 14):
        r = i % 4
        col = {1: GOLD, 3: BLUE}.get(r)
        on = hl is None or i in hl
        s += cell(i, col if on else None, 0.25, (col or INK) if on else DIM, 0.6 if col and on else 0.4)
        s += num(i, vals[r], (col or LAB) if on else DIM, 3.2)
    return s
V['Осталось найти v₁ и v₃'] = fig(svg(strip(LET), 'Полоса через v₁ и v₃', W13, TY + CH + 2), 'Полоса по (*): неизвестны только v₁ и v₃.')

# 13 клеток = три четвёрки по 49 и клетка 13
def split():
    s = strip(LET)
    yb = TY + CH + 1.5
    for k in range(3):
        a, b = cx(4 * k + 1) + 0.8, cx(4 * k + 5) - 0.8
        s += f"<path d='M{a:.1f} {yb}v2H{b:.1f}v-2' fill='none' stroke='{MUT}' stroke-width='0.6'/>"
        s += txt((a + b) / 2, yb + 6, '49', MUT, 3.2, '700')
    s += f"<rect x='{cx(13) - 0.8:.1f}' y='{TY - 0.8:.1f}' width='{CW + 1.6}' height='{CH + 1.6}' rx='1' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
    s += txt(cx(13) + CW / 2, yb + 6, vn(1), GOLD, 3.2, '700')
    return svg(s, 'Три четвёрки и клетка 13', W13, TY + CH + 10)
V['тринадцать клеток — это три четвёрки подряд'] = fig(split(), 'Сумма всех клеток: три четвёрки по 49 и клетка 13.')

# заполненная полоса
FIN = {1: '19', 2: '3', 3: '16', 0: '11'}
V['Полоса: 19, 3, 16, 11'] = fig(svg(strip(FIN), 'Заполненная полоса', W13, TY + CH + 2), 'Заполненная полоса.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
