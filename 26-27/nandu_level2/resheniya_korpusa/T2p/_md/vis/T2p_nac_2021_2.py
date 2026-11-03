import json, sys
# Рисунки к Т2′ национал 2021 день I №2. Координаты задачи — в кирпичах x (y вверх), E = (0, 0), C = (6, 0), G = (0, −12), A = (0, −21), B = (15, −12).
# SVG: X = U(x + 3), Y = −U·y.
U = 4
def xy(p): return round(U*(p[0]+3), 2), round(-U*p[1], 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'F':(-3,0),'E':(0,0),'D':(3,0),'C':(6,0),'L':(0,-2),'K':(3,-2),'M':(0,-6),'J':(3,-6),'I':(6,-6),
      'G':(0,-12),'H':(6,-12),'B':(15,-12),'A':(0,-21)}
OFF = {'F':(-2.6,-2.0),'E':(-2.4,-2.0),'D':(2.4,-2.0),'C':(2.6,-2.0),'L':(-3.0,1.2),'K':(3.0,1.2),
       'M':(-3.4,1.2),'J':(3.0,-1.4),'I':(3.2,-1.4),'G':(-3.4,1.2),'H':(3.0,4.2),'B':(3.4,1.2),'A':(0,4.8)}
ALL = list(PT)

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=3.0):
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.7' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.25):   # сетка с шагом x по всему чертежу
    s = ''.join(line((x,0),(x,-21),col,w) for x in range(-3,16))
    return s + ''.join(line((-3,y),(15,y),col,w) for y in range(-21,1))
def svg(inner, label, vb='-8 -12 88 103', mw=480):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def T(*n): return [PT[k] for k in n]
def xmark():   # кирпич x — шестая часть EC, у C
    return line((5,0),(6,0),GOLD,1.4) + at((5.5,0), 'x', 0, -1.8, GOLD, 3.2)
def frame(col=DIM, w=0.45):   # отрезки прямоугольников и прямых условия
    P_ = PT
    return (line(P_['F'],P_['C'],col,w) + line(P_['E'],P_['A'],col,w) + line(P_['C'],P_['H'],col,w) +
            line(P_['G'],P_['B'],col,w) + line(P_['L'],P_['K'],col,w) + line(P_['D'],P_['J'],col,w) +
            line(P_['M'],P_['I'],col,w))
def full(col=DIM, w=0.45):   # весь чертёж условия: прямоугольники и треугольники AJF, ABC
    P_ = PT
    return (frame(col, w) + line(P_['A'],P_['F'],col,w) + line(P_['F'],P_['J'],col,w) + line(P_['J'],P_['A'],col,w) +
            line(P_['A'],P_['B'],col,w) + line(P_['B'],P_['C'],col,w) + line(P_['C'],P_['A'],col,w))
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)

V = {}
# 1. рисунок условия: закрашены AJF и ABC, как в оригинале
s = tri(T('A','J','F'), '#c87a55', 0.22) + tri(T('A','B','C'), '#c87a55', 0.22) + full(INK, 0.55) + labels(ALL)
V['I лежит на стороне CH'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: сетка, x — шестая часть EC
s = grid() + full() + xmark()
s += line(PT['E'],PT['C'],GOLD,1.0) + at((3,0), '6x', 0, -7.0, GOLD, 3.2)
s += line(PT['E'],PT['G'],GOLD,1.0) + at((0,-9), '12x', -4.6, 1.0, GOLD, 3.2)
s += names()
V['EG = 12x, сетка с шагом x.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = EC : 6; все точки — в узлах сетки.")

G = grid() + full()
# 3. а) CFMI — трапеция
s = G + tri(T('C','F','M','I'), GOLD, 0.4) + line(PT['E'],PT['M'],GOLD,1.0,True)
s += at((1.5,0), '9x', 0, -7.0) + at((3,-6), '6x', 0, 4.0) + at((0,-4), '6x', 3.6, 1.0)
s += xmark() + names()
V['CFMI — трапеция'] = fig(svg(s, 'CFMI на сетке'),
  "а) площадь CFMI: трапеция, основания CF и MI, высота EM.")
# 4. б) AJF = прямоугольник 6x × 21x без трёх прямоугольных треугольников
R1 = [(-3,0),(3,0),(3,-21),(-3,-21)]
s = G + poly(R1, GOLD, 1.0) + tri(T('A','J','F'), VIO, 0.4)
s += tri([PT['F'],(-3,-21),PT['A']], BLUE, 0.3) + tri([PT['A'],(3,-21),PT['J']], GREEN, 0.3) + tri([PT['F'],PT['D'],PT['J']], RED, 0.3)
s += at((-3,-12), '21x', -4.4, 1.0, BLUE) + at((-1.5,-21), '3x', 0, 4.2, BLUE)
s += at((1.5,-21), '3x', 0, 4.2, GREEN) + at((3,-14), '15x', 4.6, 1.0, GREEN)
s += at((0,0), '6x', 0, -7.0, RED) + at((3,-3.5), '6x', 3.6, 1.0, RED)
s += xmark() + names()
V['это прямоугольник 6x × 21x'] = fig(svg(s, 'AJF внутри прямоугольника'),
  "б) площадь AJF: <b style='color:#f0a83c'>прямоугольник</b> без <b style='color:#5ba8f5'>синего</b>, "
  "<b style='color:#5fd38d'>зелёного</b> и <b style='color:#f2686c'>красного</b> треугольников.")
# 5. в) ABC = прямоугольник 15x × 21x без трёх прямоугольных треугольников
R2 = [(0,0),(15,0),(15,-21),(0,-21)]
s = G + poly(R2, GOLD, 1.0) + tri(T('A','B','C'), VIO, 0.4)
s += tri(T('A','C','E'), BLUE, 0.3) + tri([PT['C'],(15,0),PT['B']], RED, 0.3) + tri([PT['B'],(15,-21),PT['A']], GREEN, 0.3)
s += at((0,-16), '21x', -4.4, 1.0, BLUE) + at((3,0), '6x', 0, -7.0, BLUE)
s += at((10.5,0), '9x', 0, -7.0, RED) + at((15,-6), '12x', 4.6, 1.0, RED)
s += at((15,-16.5), '9x', 4.0, 1.0, GREEN) + at((7.5,-21), '15x', 0, 4.4, GREEN)
s += xmark() + names()
V['это прямоугольник 15x × 21x'] = fig(svg(s, 'ABC внутри прямоугольника'),
  "в) площадь ABC: <b style='color:#f0a83c'>прямоугольник</b> без <b style='color:#5ba8f5'>ACE</b>, "
  "<b style='color:#f2686c'>красного</b> и <b style='color:#5fd38d'>зелёного</b> треугольников.")
# 6. раздел «Найдём x»: DELK
s = grid() + full() + tri(T('D','E','L','K'), RED, 0.5)
s += at((1.5,0), '3x', 0, -1.6, RED) + at((0,-1), '2x', -3.8, 1.0, RED) + xmark() + names()
V['DELK — прямоугольник со сторонами'] = fig(svg(s, 'DELK на сетке'), 'Прямоугольник DELK.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
