import json, sys
# Рисунки к Т2′ регионал 2025 №2. Координаты задачи — в см (y вверх), B = (0, 0); масштаб как в оригинале.
# BH = x = 12, GH = h = 20, BC = w = 28, AB = 24. SVG: X = x + 24, Y = 32 − y.
P = {'A':(-24,0),'B':(0,0),'C':(28,0),'H':(0,12),'I':(12,12),'D':(28,12),'G':(0,32),'F':(12,32),'E':(28,32)}
def xy(n): x, y = P[n] if isinstance(n, str) else n; return x+24, 32-y
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
SEGS = [('A','C'),('C','E'),('E','G'),('G','B'),('A','G'),('H','D'),('I','F')]
OFF = {'A':(-2.4,3.4),'B':(0,4.2),'C':(2.4,3.4),'H':(-2.6,-0.8),'I':(1.6,-1.0),'D':(2.8,1.0),
       'G':(-2.2,-1.4),'F':(0,-1.8),'E':(2.4,-1.4)}

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
def right_angle(col=INK):   # прямой угол ABG при B
    X, Y = xy('B'); return f"<path d='M{X-2} {Y}V{Y-2}H{X}' fill='none' stroke='{col}' stroke-width='0.35'/>"
def base(col=INK, w=0.5): return ''.join(line(a, b, col, w) for a, b in SEGS)
def full(): return base(DIM, 0.45) + right_angle(DIM)
def names(): return labels(MUT)
def svg(inner, label, vb='-6 -6 64 45'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"

V = {}
# 1. рисунок условия
V['вместе составляют прямоугольник BCEG'] = fig(svg(base() + right_angle() + labels(), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x — золото, h — синий, w — зелёный
s = full()
for a, b in [('B','H'),('H','I')]: s += line(a, b, GOLD, 1.3)
for a, b in [('H','G'),('D','E'),('I','F')]: s += line(a, b, BLUE, 1.3)
for a, b in [('B','C'),('H','D'),('G','E')]: s += line(a, b, GREEN, 1.3)
s += at((0,6), 'x', -2.2, 1.0, GOLD) + at((6,12), 'x', 0, -1.2, GOLD)
s += at((0,22), 'h', 2.0, 1.0, BLUE) + at((28,22), 'h', 2.2, 1.0, BLUE) + at((12,22), 'h', 2.0, 1.0, BLUE)
s += at((14,0), 'w', 0, 3.6, GREEN) + at((20,12), 'w', 0, -1.2, GREEN) + at((20,32), 'w', 0, -1.4, GREEN)
s += at((-12,0), '2x', 0, 3.6, GOLD) + at((-12,16), '2h', -2.8, 0, BLUE)
s += names()
V['h = GH = DE = FI'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = BH = HI, AB = 2x; <b style='color:#5ba8f5'>h</b> = GH = DE = FI, AG = 2h; <b style='color:#5fd38d'>w</b> = BC = HD = GE.")

# 3–5. артефакт: каждое спрошенное на чертеже
s = full() + line('A','C',GOLD,1.2) + line('C','E',GOLD,1.2) + line('E','G',GOLD,1.2) + line('G','A',RED,1.2,True)
s += at((-10,0), '2x + w', 0, 3.6) + at((28,16), 'x + h', 4.4, 1.0) + at((20,32), 'w', 0, -1.4) + at((-12,16), '2h', -2.8, 0, RED)
s += names()
V['а наклонная AG = 2 GH дана'] = fig(svg(s, 'Контур ACEG'), "а) периметр <b style='color:#f0a83c'>ACEG</b>; наклонная <b style='color:#f2686c'>AG = 2h</b>.")
s = full() + poly(['A','B','G'], VIO, 1.0, VIO, 0.35) + poly(['B','C','D','G'], GOLD, 1.0, GOLD, 0.3)
s += at((-12,0), '2x', 0, 3.6, VIO) + at((0,20), 'x + h', -4.0, 1.0, VIO) + at((28,6), 'x', 2.0, 1.0) + at((14,0), 'w', 0, 3.6)
s += names()
V['BCDG — трапеция с основаниями BG и CD'] = fig(svg(s, 'ABG и BCDG'),
  "б) площадь ACDG: <b style='color:#c58af9'>ABG</b> и <b style='color:#f0a83c'>трапеция BCDG</b>: основания BG = x + h и CD = x, высота BC = w.")
s = full() + poly(['A','E','G'], GOLD, 1.0, GOLD, 0.35) + line('B','G',BLUE,1.2,True)
s += at((20,32), 'w', 0, -1.4) + at((0,6), 'x + h', 4.6, 1.0, BLUE)
s += names()
V['высота от A до GE равна BG'] = fig(svg(s, 'AEG: основание GE, высота BG'),
  "в) площадь <b style='color:#f0a83c'>AEG</b>: основание GE = w, высота <b style='color:#5ba8f5'>BG</b> = x + h.")

# 6. раздел «Найдём x, h и w»: три обхода
s = full() + poly(['B','C','D','H'], GOLD, 1.2) + at((14,0), 'w', 0, 3.6) + at((0,6), 'x', -2.2, 1.0) + names()
V['стороны BC = w и BH = x'] = fig(svg(s, 'Обход BCDH'), 'P(BCDH) = 80.')
s = full() + poly(['B','C','E','G'], BLUE, 1.2) + at((14,0), 'w', 0, 3.6, BLUE) + at((28,16), 'x + h', 4.4, 1.0, BLUE) + names()
V['стороны BC = w и BG = x + h'] = fig(svg(s, 'Обход BCEG'), 'P(BCEG) = 120.')
s = full() + poly(['I','D','E','F'], GREEN, 1.2) + line('H','I',GOLD,1.3) + at((6,12), 'x', 0, -1.2, GOLD)
s += at((20,12), 'w − x', 0, 3.6, GREEN) + at((28,22), 'h', 2.2, 1.0, GREEN) + names()
V['стороны ID = HD − HI'] = fig(svg(s, 'Обход DEFI'), 'P(DEFI) = 72; HD = w, от неё отрезана HI = x.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
