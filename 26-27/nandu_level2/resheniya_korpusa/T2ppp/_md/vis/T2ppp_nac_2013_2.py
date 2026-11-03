import json, sys
# Рисунки к Т2‴ национал 2013 день I №2. Три фигуры в ряд, координаты в см при x = 28 (истинные пропорции):
# C3 = [0, 44]², C2 = [4, 40]², C1 = [8, 36]²; фигура k сдвинута вправо на OX[k]. SVG: y вниз.
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
OX = {1: 0, 2: 54, 3: 108}
SQ = {1: (8, 36), 2: (4, 40), 3: (0, 44)}          # C1, C2, C3: от и до по обеим осям

def P(f, p): return (OX[f] + p[0], p[1])
def line(a, b, col, w=0.5, dash=False):
    d = " stroke-dasharray='1.4 1.0'" if dash else ''
    return f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % p for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.0):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def corners(f, k):
    a, b = SQ[k]; return [P(f, (a, a)), P(f, (b, a)), P(f, (b, b)), P(f, (a, b))]
def ring(f, k):                                     # полоса между C(k−1) и Ck, заливка через evenodd
    o, i = corners(f, k), corners(f, k-1)
    d = 'M' + 'L'.join('%s,%s' % p for p in o) + 'Z M' + 'L'.join('%s,%s' % p for p in i) + 'Z'
    return d
def fillpath(d, col, op):
    return f"<path d='{d}' fill='{col}' fill-opacity='{op}' fill-rule='evenodd' stroke='none'/>"
def diags(f, k, col, w=0.35):                       # диагонали в углах полосы между C(k−1) и Ck
    return ''.join(line(o, i, col, w) for o, i in zip(corners(f, k), corners(f, k-1)))
def trap(f, k, side):                               # трапеция полосы k: side 0 верх, 1 право, 2 низ, 3 лево
    o, i = corners(f, k), corners(f, k-1)
    return [o[side], o[(side+1) % 4], i[(side+1) % 4], i[side]]
def drawing(col=INK, w=0.7, shade=RED, op=0.5, dots=True, sub=True):
    """весь чертёж условия: три фигуры, закраска как в оригинале"""
    s = ''
    if shade:
        s += poly(corners(1, 1), 'none', 0, shade, op)
        s += fillpath(ring(2, 2), shade, op) + fillpath(ring(3, 3), shade, op)
    s += diags(2, 2, '#e8964a' if shade else col, 0.35) + diags(3, 3, '#e8964a' if shade else col, 0.35)
    for f in OX:
        for k in SQ: s += poly(corners(f, k), col, w)
        if dots: s += ''.join(f"<circle cx='{x}' cy='{y}' r='0.6' fill='{col}'/>" for k in SQ for x, y in corners(f, k))
        if sub: s += txt(OX[f] + 22, 51, f'Fig {f}', MUT if col != INK else LAB, 3.0)
    return s
def names(col=MUT):                                 # C1, C2, C3 — посередине левой стороны, внутри своей полосы
    return ''.join(txt(OX[f] + SQ[k][0] + 2.0 + (0.6 if k == 1 else 0), 23, f'C{k}', col, 2.0) for f in OX for k in SQ)
def svg(inner, label, vb='-3 -6 158 60'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:640px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def box(cx, cy, s, col=GOLD, wd=14):
    return (f"<rect x='{cx-wd/2}' y='{cy-3.4}' width='{wd}' height='5.2' rx='1.0' fill='#0e1116' fill-opacity='0.88'/>"
            + txt(cx, cy + 0.4, s, col, 3.0))
def topmark(f, k, lab, col=GOLD, w=1.3):            # верхняя сторона Ck жирно + подпись над ней
    a, b = SQ[k]
    return line(P(f, (a, a)), P(f, (b, a)), col, w) + txt(OX[f] + 22, a - 0.9, lab, col, 2.8)

DIMD = drawing(DIM, 0.5, None, dots=True) + names()
V = {}
# 1. рисунок условия
V['x — сторона C1.'] = fig(svg(drawing() + names(LAB), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: стороны C1, C2, C3 на Fig 1
s = DIMD + topmark(1, 1, 'x') + topmark(1, 2, 'x + 8') + topmark(1, 3, 'x + 16')
V['x + 8 и x + 16'] = fig(svg(s, 'Буквы', '-3 -7 158 61'),
  "Стороны <b style='color:#f0a83c'>x</b>, <b style='color:#f0a83c'>x + 8</b>, <b style='color:#f0a83c'>x + 16</b> — на Fig 1, на Fig 2 и Fig 3 они те же.")

# 3. артефакт: спрошенное — квадрат C1 на Fig 1
s = DIMD + poly(corners(1, 1), GOLD, 1.1, GOLD, 0.3) + topmark(1, 1, 'x') + box(22, 23, 'x × x')
V['квадрат C1 со стороной x'] = fig(svg(s, 'Закрашенное в Fig 1'), 'площадь закрашенной части Fig 1')

# 4. раздел «Найдём x»: трапеции Fig 2 золотом, Fig 3 синим
s = DIMD
for side in range(4):
    s += poly(trap(2, 2, side), GOLD, 0.6, GOLD, 0.5) + poly(trap(3, 3, side), BLUE, 0.6, BLUE, 0.5)
V['закрасим трапеции Fig 2 и трапеции Fig 3'] = fig(svg(s, 'Закрашенное: трапеции'),
  "<b style='color:#f0a83c'>4 трапеции Fig 2</b> и <b style='color:#5ba8f5'>4 трапеции Fig 3</b>.")

# 5–6. трапеция = прямоугольник шириной 4 + два треугольника с катетами 4
def trap_split(f, k, lab, col):
    a, b = SQ[k-1]; o = SQ[k][0]                    # внутренняя сторона [a, b] на высоте a, внешняя — на высоте o
    s = poly([P(f, (a, o)), P(f, (b, o)), P(f, (b, a)), P(f, (a, a))], col, 1.0, col, 0.5)
    s += poly([P(f, (o, o)), P(f, (a, o)), P(f, (a, a))], GREEN, 1.0, GREEN, 0.5)
    s += poly([P(f, (b, o)), P(f, (SQ[k][1], o)), P(f, (b, a))], GREEN, 1.0, GREEN, 0.5)
    s += txt(OX[f] + (o + a) / 2, o - 0.9, '4', GREEN, 2.6) + txt(OX[f] + (b + SQ[k][1]) / 2, o - 0.9, '4', GREEN, 2.6)
    s += txt(OX[f] + 22, o - 0.9, lab, col, 2.8)
    return s
V['вдоль стороны C1'] = fig(svg(DIMD + trap_split(2, 2, 'x', GOLD), 'Трапеция Fig 2'),
  "<b style='color:#f0a83c'>Прямоугольник</b> со сторонами x и 4 и <b style='color:#5fd38d'>два треугольника с катетами 4</b>.")
V['вдоль стороны C2'] = fig(svg(DIMD + trap_split(3, 3, 'x + 8', BLUE), 'Трапеция Fig 3', '-3 -7 158 61'),
  "<b style='color:#5ba8f5'>Прямоугольник</b> со сторонами x + 8 и 4 и <b style='color:#5fd38d'>два треугольника с катетами 4</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
