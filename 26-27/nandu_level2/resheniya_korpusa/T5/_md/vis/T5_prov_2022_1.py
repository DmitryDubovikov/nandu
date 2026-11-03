import json, sys
# Рисунки к Т5 провинциал 2022 №1: квадрат из палочек 1, 2, …, 11 см.
# Каждый рисунок — четыре стороны квадрата, вытянутые в ряд: строка = сторона, палочки в масштабе.
# Самая длинная палочка стороны — золотом, её напарники — синим; лишняя палочка — тускло.
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

def svg(inner, aria, vb, mw=440):
    return f"<svg viewBox='{vb}' role='img' aria-label='{aria}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

def rod(x0, y, L, u, col, h=7, op=1.0):
    w = L*u
    s = (f"<rect x='{x0:.2f}' y='{y}' width='{w-0.6:.2f}' height='{h}' rx='1' fill='{col}' fill-opacity='{0.22*op:.2f}' "
         f"stroke='{col}' stroke-width='0.6' stroke-opacity='{op}'/>")
    s += (f"<text x='{x0+w/2-0.3:.2f}' y='{y+h/2+1.5:.2f}' fill='{col}' fill-opacity='{op}' font-size='4.2' "
          f"text-anchor='middle' font-weight='700'>{L}</text>")
    return s

def rows(sides, x, u, X0=4, Y0=4, gap=4, h=7):
    s = ''
    for i, side in enumerate(sides):
        y = Y0 + i*(h+gap)
        x0 = X0
        for j, L in enumerate(side):
            s += rod(x0, y, L, u, GOLD if L == max(side) else BLUE, h)
            x0 += L*u
    # конец каждой стороны на одной вертикали: стороны равны x
    xe = X0 + x*u - 0.3
    yb = Y0 + len(sides)*(h+gap) - gap
    s += f"<line x1='{xe:.2f}' y1='{Y0-2}' x2='{xe:.2f}' y2='{yb+2}' stroke='{MUT}' stroke-width='0.5' stroke-dasharray='1.4 1'/>"
    s += f"<text x='{xe:.2f}' y='{yb+7}' fill='{LAB}' font-size='4.2' text-anchor='middle' font-weight='700'>{x}</text>"
    return s, yb

V = {}

# 1. x = 11: одна палочка 11 и три пары с суммой 11
s, yb = rows([[11], [1, 10], [2, 9], [3, 8]], 11, 9)
V['x = 11: (11), (1 + 10), (2 + 9), (3 + 8)'] = fig(svg(s, 'Квадрат со стороной 11', f'0 0 110 {yb+10}', 420),
  'Квадрат со стороной 11: четыре стороны в ряд.')

# 2. x = 16: пары с напарниками, 8 добрана палочками 1, 3, 4; палочка 2 лишняя
s, yb = rows([[11, 5], [10, 6], [9, 7], [8, 1, 3, 4]], 16, 6)
y = yb + 12
s += rod(4, y, 2, 6, MUT, op=0.6)
s += f"<text x='19' y='{y+5}' fill='{MUT}' font-size='3.8' font-weight='600'>лишняя</text>"
V['8 + 1 + 3 + 4 = 16'] = fig(svg(s, 'Квадрат со стороной 16', f'0 0 110 {y+10}', 440),
  'Квадрат со стороной 16 и лишняя палочка 2.')

# 3. x = 13: четыре самые длинные палочки 8, 9, 10, 11 и их напарники
s, yb = rows([[8, 5], [9, 4], [10, 3], [11, 2]], 13, 7.5)
V['(8 + (x − 8)), (9 + (x − 9)), (10 + (x − 10)), (11 + (x − 11))'] = fig(
  svg(s, 'Квадрат со стороной 13', f'0 0 110 {yb+10}', 420),
  'Квадрат со стороной 13: палочки 8, 9, 10, 11, каждая с напарником.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
