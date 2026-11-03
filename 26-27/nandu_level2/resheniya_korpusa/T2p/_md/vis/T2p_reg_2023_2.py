import json, sys
# Рисунки к Т2′ регионал 2023 №2. Координаты задачи — в кирпичах x = CD (y вверх):
# H = (0, 0), C = (2, 0), D = (2, 1), G = (0, 1), F = (0, 2.5), A = (0, −1.5), B = середина AC, E = середина DF.
# SVG: X = U·x, Y = U·(2.5 − y).
U = 20
def xy(p): return round(U*p[0], 2), round(U*(2.5-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'F':(0,2.5),'E':(1,1.75),'G':(0,1),'D':(2,1),'H':(0,0),'C':(2,0),'B':(1,-0.75),'A':(0,-1.5)}
OFF = {'F':(-3.4,1.0),'E':(2.6,-1.6),'G':(-3.6,1.2),'D':(3.6,1.2),'H':(-3.6,1.2),'C':(3.6,1.6),'B':(2.4,4.0),'A':(-3.4,1.6)}
ALL = list(PT)
SEG = [('F','A'),('F','D'),('G','E'),('G','D'),('D','C'),('H','C'),('H','B'),('A','C')]

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
    X, Y = xy(p); return txt(round(X+dx,2), round(Y+dy,2), s, col, size)
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def svg(inner, label, vb='-14 -5 66 92', mw=340):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def full(col=DIM, w=0.45): return ''.join(line(PT[a],PT[b],col,w) for a,b in SEG)
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def T(*n): return [PT[k] for k in n]
def tick(m, col=BLUE):   # чёрточка равенства поперёк AC (направление AC — (0.8, 0.6))
    return line((m[0]+0.06, m[1]-0.08), (m[0]-0.06, m[1]+0.08), col, 1.0)
def xmark():   # кирпич x = CD
    return line(PT['D'],PT['C'],GOLD,1.4) + at((2,0.5), 'x', 3.0, 1.0, GOLD, 3.2)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['чтобы CD и DG были целыми кирпичами'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x = CD, вторая длина EF
s = full() + xmark() + line(PT['G'],PT['D'],GOLD,1.0) + at((1,1), '2x', 0, -1.6, GOLD, 3.2)
s += line(PT['E'],PT['F'],BLUE,1.4) + at((0.5,2.125), 'EF', 3.2, -2.6, BLUE, 3.2)
s += line(PT['E'],PT['D'],BLUE,0.9,True) + line(PT['A'],PT['B'],BLUE,0.9,True) + line(PT['B'],PT['C'],BLUE,0.9,True)
s += line(PT['F'],PT['G'],GREEN,1.2) + at((0,1.75), 'EF + 4', -8.4, 1.0, GREEN, 2.8)
s += line(PT['H'],PT['A'],GREEN,1.2) + at((0,-0.75), 'EF + 4', -8.4, 1.0, GREEN, 2.8)
s += names()
V['EF — вторая неизвестная длина.'] = fig(svg(s, 'Буквы', '-18 -5 70 92'),
  "<b style='color:#f0a83c'>x</b> = CD; <b style='color:#5ba8f5'>EF</b> = DE = AB = BC; <b style='color:#5fd38d'>FG = AH = EF + 4</b>.")

# 3. а) CDGH
s = full() + tri(T('H','C','D','G'), GOLD, 0.35) + at((1,1), '2x', 0, -1.6, GOLD, 3.2) + xmark() + names()
V['CDGH — прямоугольник со сторонами CD = x и DG = 2x.'] = fig(svg(s, 'CDGH'), 'а) площадь CDGH')

# 4. б) контур ACDEG
s = full()
for a,b in (('A','C'),('C','D'),('D','E'),('E','G'),('G','A')): s += line(PT[a],PT[b],GOLD,1.3)
s += at((0.5,-1.125), '2 · EF', 6.0, 5.0, GOLD, 2.8) + at((2,0.5), 'x', 3.0, 1.0, GOLD, 3.2)
s += at((1.5,1.375), 'EF', 4.0, -0.6, GOLD, 2.8) + at((0.5,1.375), 'EF', 0.6, 4.2, GOLD, 2.8)
s += at((0,-0.25), 'x + EF + 4', -10.0, 1.0, GOLD, 2.6) + names()
V['AC, CD, DE и GA уже выражены через x и EF'] = fig(svg(s, 'Контур ACDEG', '-22 -5 74 92'), 'б) периметр ACDEG')

# 5. в) BCDFH = BCH + HCDG + DFG; BCH — половина ACH
s = full() + tri(T('H','C','B'), BLUE, 0.5) + tri(T('H','C','D','G'), GOLD, 0.3) + tri(T('G','D','F'), GREEN, 0.4)
s += poly(T('A','B','H'), BLUE, 0.6, 'none') + line(PT['H'],PT['B'],BLUE,1.0)
s += tick((0.5,-1.125)) + tick((1.5,-0.375)) + names()
V['BCDFH не прямоугольник и не трапеция'] = fig(svg(s, 'BCDFH'),
  "в) площадь BCDFH: <b style='color:#5ba8f5'>BCH</b>, <b style='color:#f0a83c'>HCDG</b> и <b style='color:#5fd38d'>DFG</b>; AB = BC.")

# 6. г) ADE — половина AFD; высота AFD — DG
s = full() + poly(T('A','F','D'), GOLD, 1.0) + tri(T('A','E','D'), VIO, 0.45) + tri(T('A','F','E'), BLUE, 0.2)
s += line(PT['D'],PT['G'],RED,1.2,True) + at((1.5,1), 'DG', 0, 4.0, RED, 2.8) + names()
V['у AFD основание AF = FG + GH + HA'] = fig(svg(s, 'ADE в AFD'),
  "г) площадь ADE: <b style='color:#c58af9'>ADE</b> и <b style='color:#5ba8f5'>AFE</b> вместе — AFD; FE = ED; высота AFD — <b style='color:#f2686c'>DG</b>.")

# 7. врезка: пример на числах — основания 4 и 6, общая высота 5
def bx(p): return round(7*p[0]+4, 2), round(7*(5-p[1])+4, 2)
def bpoly(pts, col, op):
    return f"<polygon points='{' '.join('%s,%s' % bx(q) for q in pts)}' fill='{col}' fill-opacity='{op}' stroke='{col}' stroke-width='0.8' stroke-linejoin='round'/>"
def btxt(p, s_, col=LAB, size=3.0, dy=0): X, Y = bx(p); return txt(X, round(Y+dy,2), s_, col, size)
s = bpoly([(0,0),(4,0),(7,5)], BLUE, 0.4) + bpoly([(4,0),(10,0),(7,5)], GREEN, 0.4)
(x1,y1),(x2,y2) = bx((7,5)), bx((7,0))
s += f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{LAB}' stroke-width='0.7' stroke-dasharray='1.4 1.1'/>"
s += btxt((7.6,2.5), 'h = 5', LAB, 2.8) + btxt((2,0), '4', BLUE, 3.0, 4.4) + btxt((7,0), '6', GREEN, 3.0, 4.4)
s += btxt((3.6,1.4), '10', BLUE, 3.2) + btxt((8.6,1.4), '15', GREEN, 3.2)
V['Пример на числах, не из задачи: основания 4 и 6'] = fig(f"<svg viewBox='0 0 82 48' role='img' aria-label='Пример'>{s}</svg>",
  "4 · 5 : 2 = 10, 6 · 5 : 2 = 15; основание 6 в 3/2 раза длиннее 4, и площадь 15 в 3/2 раза больше 10.")

# 8. раздел «Найдём x»: CDGH
s = full() + tri(T('H','C','D','G'), RED, 0.35) + at((1,1), '2x', 0, -1.6, RED, 3.2) + xmark() + names()
V['в периметр CDGH входят две стороны'] = fig(svg(s, 'CDGH'), 'Прямоугольник CDGH.')

# 9. раздел «Найдём EF»: DFG
s = full() + tri(T('G','D','F'), RED, 0.4) + at((1,1), '2x', 0, 4.0, RED, 3.2)
s += at((0,1.75), 'EF + 4', -8.4, 1.0, RED, 2.8) + at((1.5,1.375), '2 · EF', 6.0, -2.4, RED, 2.8) + names()
V['стороны DFG — FG = EF + 4'] = fig(svg(s, 'DFG', '-18 -5 70 92'), 'Прямоугольный треугольник DFG.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
