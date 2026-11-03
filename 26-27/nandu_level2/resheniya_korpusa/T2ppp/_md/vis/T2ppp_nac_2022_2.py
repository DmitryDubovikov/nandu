import json, sys
# Рисунки к Т2‴ национал 2022 день I №2. Пять вложенных прямоугольников, координаты — как на чертеже условия
# (масштаб чертежа, не истинный: на чертеже площади не вдвое). SVG: y вниз, R5 = (0, 0)–(62, 43).
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
R = {1: (23.1,16.2,38.6,26.8), 2: (20.6,13.4,41.2,29.5), 3: (15.5,10.7,46.3,32.2),
     4: (10.0,5.3,51.4,37.8), 5: (0,0,62,43)}
LABPOS = {1: (35.8,20.2), 2: (43.4,22.6), 3: (48.4,27.9), 4: (54.4,31.4), 5: (59.0,36.6)}

def sub(k):                     # контур прямоугольника Rk как кусок пути
    x0,y0,x1,y1 = R[k]; return f'M{x0},{y0}H{x1}V{y1}H{x0}Z'
def area(ks, fill, op):         # заливка с чётностью: кольца получаются сами
    return f"<path d='{''.join(sub(k) for k in ks)}' fill='{fill}' fill-opacity='{op}' fill-rule='evenodd' stroke='none'/>"
def rect(k, col=INK, w=0.6, dash=False):
    x0,y0,x1,y1 = R[k]; d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<rect x='{x0}' y='{y0}' width='{round(x1-x0,2)}' height='{round(y1-y0,2)}' fill='none' stroke='{col}' stroke-width='{w}'{d}/>"
def line(a, b, col, w=0.5, dash=False):
    d = " stroke-dasharray='1.2 1.0'" if dash else ''
    return f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def txt(x, y, s, col=LAB, size=2.6):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def dots(col=INK):
    return ''.join(f"<circle cx='{x}' cy='{y}' r='0.55' fill='{col}'/>" for k in R
                   for x in (R[k][0], R[k][2]) for y in (R[k][1], R[k][3]))
def names(col=LAB, ks=(1,2,3,4,5)):
    return ''.join(txt(*LABPOS[k], f'R{k}', col, 2.4) for k in ks)
def frame(col=DIM, w=0.5):      # весь чертёж условия тусклым
    return ''.join(rect(k, col, w) for k in R) + dots(DIM) + names(MUT)
def box(cx, cy, s, col=GOLD, wd=22):
    return (f"<rect x='{cx-wd/2}' y='{cy-3.6}' width='{wd}' height='5.6' rx='1.2' fill='#0e1116' fill-opacity='0.88'/>"
            + txt(cx, cy+0.4, s, col, 3.0))
def svg(inner, label, vb='-5 -5 72 53'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"

# x — треть короткой стороны R4 (левая сторона R4, от верхнего угла)
X4 = (R[4][3] - R[4][1]) / 3
def xmark():
    x0, y0 = R[4][0], R[4][1]
    return line((x0, y0), (x0, y0 + X4), GOLD, 1.4) + txt(x0 - 2.4, y0 + X4/2 + 1.0, 'x', GOLD, 2.8)
def sides4(all4=False):          # подписи сторон R4: 4x сверху, 3x слева (и напротив, если all4)
    x0,y0,x1,y1 = R[4]; cx, cy = (x0+x1)/2, (y0+y1)/2
    s = txt(cx, y0 - 1.0, '4x', GOLD, 2.8) + txt(x1 + 3.4, cy + 1.0, '3x', GOLD, 2.8)
    if all4: s += txt(cx, y1 + 3.4, '4x', GOLD, 2.8) + txt(x0 + 3.4, cy + 6.0, '3x', GOLD, 2.8)
    return s

V = {}
# 1. рисунок условия
s = area([1,2,3,4,5], RED, 0.5) + ''.join(rect(k) for k in R) + dots() + names()
V['каждый следующий прямоугольник вдвое больше предыдущего'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: кирпич площади S(R1), кирпич длины x на стороне R4
s = frame() + area([1], BLUE, 0.6) + rect(4, GOLD, 1.0) + sides4() + xmark()
s += txt(29.0, 22.6, 'S(R1)', LAB, 2.6)
V['S(R1) — кирпич площади'] = fig(svg(s, 'Буквы', '-6 -5 74 53'),
  "<b style='color:#5ba8f5'>S(R1)</b> — кирпич площади; <b style='color:#f0a83c'>x</b> — треть короткой стороны R4.")

# 3–5. артефакт: каждое спрошенное через кирпичи
s = frame() + area([5], GOLD, 0.25) + rect(5, GOLD, 1.0) + area([1], BLUE, 0.6) + box(31, 40.0, '16 · S(R1)')
V['площадь R5 равна 16 площадям R1'] = fig(svg(s, 'R5 через площадь R1'), 'а) площадь R5')
s = frame() + area([3], GOLD, 0.3) + rect(3, GOLD, 1.0) + area([1], BLUE, 0.6) + box(31, 40.0, '4 · S(R1)')
V['площадь R3 равна 4 площадям R1'] = fig(svg(s, 'R3 через площадь R1'), 'б) площадь R3')
s = frame() + rect(4, GOLD, 1.2) + sides4(True) + xmark()
V['две стороны 3x и две стороны 4x'] = fig(svg(s, 'Стороны R4', '-6 -5 74 53'), 'в) периметр R4')

# 6. раздел 1: закрашенное тремя цветами
s = frame() + area([1], BLUE, 0.6) + area([2,3], GOLD, 0.55) + area([4,5], GREEN, 0.5)
V['закрасим R1 и два кольца разными цветами'] = fig(svg(s, 'Закрашенное: R1 и два кольца'),
  "<b style='color:#5ba8f5'>R1</b>, <b style='color:#f0a83c'>кольцо R3 без R2</b>, <b style='color:#5fd38d'>кольцо R5 без R4</b>.")
# 7–8. кольцо = весь прямоугольник минус вырезанный
s = frame() + area([3], GOLD, 0.45) + rect(3, GOLD, 1.0) + area([2], '#0e1116', 0.9) + rect(2, RED, 0.9, True)
s += txt(31, 35.6, '4 · S(R1)', GOLD, 2.6) + txt(30.9, 22.6, '− 2 · S(R1)', RED, 2.6)
V['Из R3 вырезан R2.'] = fig(svg(s, 'Кольцо R3 без R2'), "Весь <b style='color:#f0a83c'>R3</b> минус <b style='color:#f2686c'>R2</b>.")
s = frame() + area([5], GREEN, 0.4) + rect(5, GREEN, 1.0) + area([4], '#0e1116', 0.9) + rect(4, RED, 0.9, True)
s += txt(31, 3.6, '16 · S(R1)', GREEN, 2.6) + txt(30.9, 22.6, '− 8 · S(R1)', RED, 3.0)
V['Из R5 вырезан R4.'] = fig(svg(s, 'Кольцо R5 без R4'), "Весь <b style='color:#5fd38d'>R5</b> минус <b style='color:#f2686c'>R4</b>.")

# 9. раздел 2: R4 — сетка 3 × 4 квадратов со стороной x
x0,y0,x1,y1 = R[4]; cw, ch = (x1-x0)/4, (y1-y0)/3
s = ''.join(rect(k, DIM, 0.5) for k in (1,2,3,5)) + dots(DIM) + names(MUT, (1,2,3,5))
s += f"<rect x='{x0}' y='{y0}' width='{round(cw,2)}' height='{round(ch,2)}' fill='{GOLD}' fill-opacity='0.5' stroke='none'/>"
s += ''.join(line((x0+i*cw, y0), (x0+i*cw, y1), GOLD, 0.6, True) for i in (1,2,3))
s += ''.join(line((x0, y0+j*ch), (x1, y0+j*ch), GOLD, 0.6, True) for j in (1,2))
s += rect(4, GOLD, 1.2) + sides4() + xmark() + txt(x0 + cw/2, y0 - 1.0, 'x', GOLD, 2.6)
V['разбивается на 3 · 4 = 12 квадратов со стороной x'] = fig(svg(s, 'R4: сетка квадратов', '-6 -5 74 53'),
  "В R4 три ряда по четыре <b style='color:#f0a83c'>квадрата со стороной x</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
