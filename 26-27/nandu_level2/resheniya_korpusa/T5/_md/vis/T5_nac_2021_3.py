import json, sys
# Рисунки к Т5 национал 2021 день I №3: красная кнопка ×2, синяя ×5.
# Цвет множителя = цвет кнопки: 2 — красный, 5 — синий; множитель, которого кнопки не дают, — золотой.
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

def svg(inner, aria, vb, mw):
    return f"<svg viewBox='{vb}' role='img' aria-label='{aria}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def mk(col, pre):
    return (f"<marker id='{pre}{col[1:]}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'>"
            f"<path d='M0 0L6 3L0 6z' fill='{col}'/></marker>")
def chip(x, y, d, col, w=8):
    r = f"<rect x='{x}' y='{y}' width='{w}' height='8' rx='1.5' fill='{col}' fill-opacity='0.12' stroke='{col}' stroke-width='0.5'/>"
    r += f"<text x='{x+w/2}' y='{y+5.7}' fill='{col}' font-size='4.6' text-anchor='middle' font-weight='700'>{d}</text>"
    return r
def row(label, items, aria, cap):
    # items: (текст, цвет, ширина)
    s = f"<text x='2' y='9.6' fill='{LAB}' font-size='4.4' font-weight='700'>{label}</text>"
    x = 26
    for d, col, w in items:
        s += chip(x, 4, d, col, w); x += w + 2
    return fig(svg(s, aria, f'0 0 {x+2} 16', 520), cap)

V = {}

# 1. три нажатия с 21: экраны и стрелки цвета кнопок
P = 'pT5n'
s = f"<defs>{mk(RED, P)}{mk(BLUE, P)}</defs>"
nums, cols = [21, 42, 210, 420], [RED, BLUE, RED]
xs = [2, 30, 58, 86]
for x, n in zip(xs, nums):
    s += f"<rect x='{x}' y='6' width='18' height='10' rx='1.5' fill='none' stroke='{INK}' stroke-width='0.5'/>"
    s += f"<text x='{x+9}' y='12.8' fill='{LAB}' font-size='4.6' text-anchor='middle' font-weight='700'>{n}</text>"
for i, col in enumerate(cols):
    x1, x2 = xs[i]+19.5, xs[i+1]-1.5
    s += f"<line x1='{x1}' y1='11' x2='{x2}' y2='11' stroke='{col}' stroke-width='0.7' marker-end='url(#{P}{col[1:]})'/>"
    s += f"<text x='{(x1+x2)/2}' y='5' fill='{col}' font-size='3.8' text-anchor='middle' font-weight='700'>· {2 if col == RED else 5}</text>"
V['Число на экране = 21 · 2 · 5 · 2'] = fig(svg(s, 'Три нажатия', '0 0 106 20', 460),
  "Нажатия <b style='color:#f2686c'>красной</b>, <b style='color:#5ba8f5'>синей</b> и <b style='color:#f2686c'>красной</b> кнопок.")

# 2. а) 40000: шесть двоек, четыре пятёрки
V['40000 = 2 · 2 · 2 · 2 · 2 · 2 · 5 · 5 · 5 · 5'] = row('40000',
  [('2', RED, 8)]*6 + [('5', BLUE, 8)]*4, 'Простые множители 40000', 'Простые множители 840000 : 21.')

# 3. б) 84375: три тройки (кнопки их не дают), пять пятёрок
V['84375 = 3 · 3 · 3 · 5 · 5 · 5 · 5 · 5'] = row('84375',
  [('3', GOLD, 8)]*3 + [('5', BLUE, 8)]*5, 'Простые множители 84375',
  "Простые множители 1434375 : 17; <b style='color:#f0a83c'>3</b> ни одна кнопка не даёт.")

# 4. в) 284750: одна двойка, три пятёрки и 1139
V['284750 = 2 · 5 · 5 · 5 · 1139'] = row('284750',
  [('2', RED, 8)] + [('5', BLUE, 8)]*3 + [('1139', GOLD, 18)], 'Разложение 284750',
  "Разложение 284750; <b style='color:#f0a83c'>1139</b> не делится ни на 2, ни на 5.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
