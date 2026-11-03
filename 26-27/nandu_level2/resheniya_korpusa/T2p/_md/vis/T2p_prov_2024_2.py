import json, sys
# Рисунки к Т2′ провинциал 2024 №2. Координаты задачи — в см (y вверх), M = (0, 0); масштаб как в ответе.
# BM = MP = x = 15, AM = MC = w = 20, DP = 2x + 3 = 33. SVG: X = x + 20, Y = 48 − y.
P = {'A':(-20,0),'B':(0,-15),'C':(20,0),'D':(0,48),'M':(0,0),'P':(0,15)}
def xy(n): x, y = P[n] if isinstance(n, str) else n; return x+20, 48-y
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
SEGS = [('A','C'),('B','D'),('D','A'),('D','C'),('A','B'),('B','C'),('A','P'),('C','P')]
OFF = {'A':(-2.6,1.0),'B':(0,4.2),'C':(2.6,1.0),'D':(0,-1.8),'M':(-2.4,-1.2),'P':(2.2,-1.2)}

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(names, col, w=1.0, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(n) for n in names)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=2.8):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=2.6):
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
def labels(col=LAB, dots=True):
    out = ''
    for n in P:
        X, Y = xy(n); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.55' fill='{col}'/>"
    return out
def right_angle(col=INK):   # прямой угол при M
    X, Y = xy('M'); return f"<path d='M{X+2} {Y}V{Y-2}H{X}' fill='none' stroke='{col}' stroke-width='0.35'/>"
def base(col=INK, w=0.5): return ''.join(line(a, b, col, w) for a, b in SEGS)
def full(): return base(DIM, 0.45) + right_angle(DIM)
def names(): return labels(MUT)
def svg(inner, label, vb='-8 -5 56 75', mw=420):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
# места подписей длин
mAB, mBC, mAP, mCP, mAD, mDC = (-10,-7.5), (10,-7.5), (-10,7.5), (10,7.5), (-10,24), (10,24)
def h4(col=GREEN, sides=('AB','BC','CP','PA')):
    pos = {'AB':(mAB,-2.4,2.4), 'BC':(mBC,2.4,2.4), 'CP':(mCP,1.8,-1.4), 'PA':(mAP,-1.8,-1.4)}
    return ''.join(at(pos[s][0], 'h', pos[s][1], pos[s][2], col) for s in sides)
def v2(col=VIO): return at(mAD, 'v', -2.6, 0.8, col) + at(mDC, 'v', 2.6, 0.8, col)
DP = at((0,22), '2x + 3', 4.6, 0.8)

V = {}
# 1. рисунок условия
V['середина BP» ⇒'] = fig(svg(base() + right_angle() + labels(), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x — золото, w — синий, h — зелёный, v — фиолетовый
s = full()
for a, b in [('B','M'),('M','P')]: s += line(a, b, GOLD, 1.3)
for a, b in [('A','M'),('M','C')]: s += line(a, b, BLUE, 1.3)
for a, b in [('A','B'),('B','C'),('C','P'),('P','A')]: s += line(a, b, GREEN, 1.3)
for a, b in [('A','D'),('D','C')]: s += line(a, b, VIO, 1.3)
s += at((0,-7.5), 'x', 2.0, 0.8) + at((0,7.5), 'x', 2.0, 0.8)
s += at((-10,0), 'w', 0, -1.2, BLUE) + at((10,0), 'w', 0, -1.2, BLUE)
s += h4() + v2() + DP + names()
V['v = AD = CD'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = BM = MP, <b style='color:#5ba8f5'>w</b> = AM = MC, "
  "<b style='color:#5fd38d'>h</b> = AB = BC = CP = AP, <b style='color:#c58af9'>v</b> = AD = CD; PD = 2x + 3.")

# 3–6. артефакт: каждое спрошенное на чертеже
s = full() + poly(['A','B','C'], GOLD, 1.2) + h4(GOLD, ('AB','BC')) + at((10,0), '2w', 0, -1.2) + names()
V['у ABC стороны'] = fig(svg(s, 'Контур ABC'), 'а) периметр ABC')
s = full() + poly(['A','P','D'], GOLD, 1.2) + h4(GOLD, ('PA',)) + DP + at(mAD, 'v', -2.6, 0.8) + names()
V['у APD стороны'] = fig(svg(s, 'Контур APD'), 'б) периметр APD')
s = full() + poly(['A','B','D'], VIO, 1.0, VIO, 0.3) + poly(['C','B','D'], GOLD, 1.0, GOLD, 0.3)
s += line('A','M',BLUE,1.2,True) + line('M','C',BLUE,1.2,True)
s += at((-10,0), 'w', 0, -1.2, BLUE) + at((10,0), 'w', 0, -1.2, BLUE) + at('B', 'BD = 4x + 3', 0, 7.8, LAB) + names()
V['AM и MC перпендикулярны BD'] = fig(svg(s, 'ABD и CBD', vb='-8 -5 56 79'), 'в) площадь ABCD')
s = full() + poly(['A','P','D'], GOLD, 1.0, GOLD, 0.35) + line('A','M',BLUE,1.2,True) + line('M','P',BLUE,0.8,True)
s += at((-10,0), 'w', 0, -1.2, BLUE) + DP + names()
V['AM перпендикулярна прямой BD'] = fig(svg(s, 'APD: основание PD, высота AM'), 'г) площадь APD')

# 7. раздел «Найдём x, w, h и v»: четыре обхода
s = full() + poly(['A','B','C','P'], GOLD, 1.2) + h4(GOLD) + names()
V['все равны h'] = fig(svg(s, 'Обход ABCP'), 'P(ABCP) = 100.')
s = full() + poly(['A','B','P'], BLUE, 1.2) + h4(BLUE, ('AB','PA')) + at((0,-7.5), '2x', 2.6, 0.8, BLUE) + names()
V['стороны AB = AP = h и BP = 2x'] = fig(svg(s, 'Обход ABP'), 'P(ABP) = 80.')
s = full() + poly(['A','M','P'], GREEN, 1.2) + h4(GREEN, ('PA',)) + at((0,7.5), 'x', 2.0, 0.8, GREEN) + at((-10,0), 'w', 0, 3.4, GREEN) + names()
V['стороны AM = w, MP = x'] = fig(svg(s, 'Обход AMP'), 'P(AMP) = 60.')
s = full() + poly(['A','B','C','D'], VIO, 1.2) + h4(VIO, ('AB','BC')) + v2() + names()
V['стороны AB = BC = h и CD = AD = v'] = fig(svg(s, 'Обход ABCD'), 'P(ABCD) = 154.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
