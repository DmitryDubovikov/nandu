import json, sys
# Рисунки к Т2′ провинциал 2014 №2. Координаты задачи — в см (y вверх), A = (0, 0); масштаб как в оригинале.
# x = 6, h = 15: AB = FC = 72, BC = 15, DE = 54, DP = 12. SVG: X = x + 8, Y = 33 − y.
P = {'A':(0,0),'B':(72,0),'C':(72,15),'F':(0,15),'D':(63,27),'E':(9,27),'P':(63,15)}
def xy(n): x, y = P[n] if isinstance(n, str) else n; return x+8, 33-y
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
SEGS = [('A','B'),('B','C'),('C','F'),('F','A'),('C','D'),('D','E'),('E','F'),('D','P')]
OFF = {'A':(-2.4,3.4),'B':(2.4,3.4),'C':(3.0,1.2),'F':(-3.0,1.2),'D':(2.2,-1.6),'E':(-2.2,-1.6),'P':(0,4.2)}

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(names, col, w=1.0, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(n) for n in names)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.2):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=3.0):
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
def labels(col=LAB, dots=True):
    out = ''
    for n in P:
        X, Y = xy(n); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.6' fill='{col}'/>"
    return out
def right_angle(col=INK):   # прямой угол DPC при P
    X, Y = xy('P'); return f"<path d='M{X} {Y-2}H{X+2}V{Y}' fill='none' stroke='{col}' stroke-width='0.35'/>"
def base(col=INK, w=0.5): return ''.join(line(a, b, col, w) for a, b in SEGS)
def full(): return base(DIM, 0.45) + right_angle(DIM)
def names(): return labels(MUT)
def xmark():   # кирпич x = AB : 12, у A
    return line((0,0),(6,0),GOLD,1.4) + at((3,0), 'x', 0, -1.4, GOLD, 3.0)
def svg(inner, label, vb='-2 -1 92 41'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"

V = {}
# 1. рисунок условия
V['FC = AB и FA = BC'] = fig(svg(base() + labels(), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x — золото, h — синий
s = full()
for a, b in [('A','B'),('F','C'),('E','D'),('D','P')]: s += line(a, b, GOLD, 1.0)
for a, b in [('B','C'),('C','D'),('E','F'),('F','A')]: s += line(a, b, BLUE, 1.3)
s += xmark() + at((40,0), '12x', 0, 3.6) + at((36,15), '12x', 0, -1.3) + at((36,27), '9x', 0, -1.3) + at((63,21), '2x', -2.6, 1.0)
s += at((72,7.5), 'h', 2.2, 1.0, BLUE) + at((0,7.5), 'h', -2.2, 1.0, BLUE) + at((67.5,21), 'h', 2.2, 1.0, BLUE) + at((4.5,21), 'h', -2.2, 1.0, BLUE)
s += names()
V['x = AB : 12, h = BC = CD = EF = FA'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = AB : 12: AB = FC = 12x, DE = 9x, DP = 2x; <b style='color:#5ba8f5'>h</b> = BC = CD = EF = FA.")

# 3–6. каждое спрошенное на чертеже
s = full() + poly(['A','B','C','D','E','F'], GOLD, 1.2)
s += at((40,0), '12x', 0, 3.6) + at((36,27), '9x', 0, -1.3)
s += at((72,7.5), 'h', 2.2, 1.0) + at((0,7.5), 'h', -2.2, 1.0) + at((67.5,21), 'h', 2.2, 1.0) + at((4.5,21), 'h', -2.2, 1.0)
s += xmark() + names()
V['шесть сторон ABCDEF'] = fig(svg(s, 'Контур ABCDEF'), 'а) периметр ABCDEF')
s = full() + poly(['A','B','C','F'], GOLD, 1.0, GOLD, 0.35) + at((40,0), '12x', 0, 3.6) + at((72,7.5), 'h', 2.2, 1.0)
s += xmark() + names()
V['ABCF — прямоугольник со сторонами'] = fig(svg(s, 'Прямоугольник ABCF'), 'б) площадь ABCF')
s = full() + poly(['C','D','E','F'], GOLD, 1.0, GOLD, 0.35) + line('D','P',RED,1.0,True)
s += at((36,15), '12x', 0, 3.6) + at((36,27), '9x', 0, -1.3) + at((63,21), '2x', -2.6, 1.0, RED)
s += xmark() + names()
V['CDEF — трапеция с основаниями'] = fig(svg(s, 'Трапеция CDEF'), 'в) площадь CDEF')
s = full() + poly(['A','B','C','F'], GOLD, 1.0, GOLD, 0.3) + poly(['F','P','D'], BLUE, 1.0, BLUE, 0.4) + poly(['D','P','C'], GREEN, 1.0, GREEN, 0.45)
s += at((40,0), '12x', 0, 3.6) + at((72,7.5), 'h', 2.2, 1.0) + at((63,21), '2x', -2.6, 1.0, LAB)
s += xmark() + names()
V['FP + PC = FC = 12x'] = fig(svg(s, 'ABCF, FPD и DPC'),
  "г) площадь ABCDF: <b style='color:#f0a83c'>ABCF</b>, <b style='color:#5ba8f5'>FPD</b> и <b style='color:#5fd38d'>DPC</b>.")

# 7. раздел «Найдём x и h»: два обхода
s = full() + poly(['A','B','C','F'], GOLD, 1.2) + at((40,0), '12x', 0, 3.6) + at((72,7.5), 'h', 2.2, 1.0) + xmark() + names()
V['стороны AB = FC = 12x и BC = FA = h'] = fig(svg(s, 'Обход ABCF'), 'P(ABCF) = 174.')
s = full() + poly(['C','D','E','F'], BLUE, 1.2) + at((36,15), '12x', 0, 3.6, BLUE) + at((36,27), '9x', 0, -1.3, BLUE)
s += at((67.5,21), 'h', 2.2, 1.0, BLUE) + at((4.5,21), 'h', -2.2, 1.0, BLUE) + xmark() + names()
V['стороны CD = h, DE = 9x, EF = h и FC = 12x'] = fig(svg(s, 'Обход CDEF'), 'P(CDEF) = 156.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
