import json, sys
# Рисунки к Т2‴ национал 2026 день II №5. Координаты задачи — в клетках x (y вверх), большой квадрат (0, 0)–(7, 7).
# SVG: X = 9x, Y = 9(7 − y).
U = 9
def xy(p): return U*p[0], U*(7-p[1])
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

def octa(ox, oy):
    return [(ox+1,oy),(ox+2,oy),(ox+3,oy+1),(ox+3,oy+2),(ox+2,oy+3),(ox+1,oy+3),(ox,oy+2),(ox,oy+1)]
OCT_C = octa(2, 2)
OCT_W = [octa(*o) for o in [(0,0),(4,0),(0,4),(4,4)]]
SQ = [[(3,5),(4,5),(4,6),(3,6)], [(1,3),(2,3),(2,4),(1,4)], [(3,1),(4,1),(4,2),(3,2)], [(5,3),(6,3),(6,4),(5,4)]]
TR = [[(3,6),(4,6),(5,7),(2,7)], [(1,3),(1,4),(0,5),(0,2)], [(3,1),(4,1),(5,0),(2,0)], [(6,3),(6,4),(7,5),(7,2)]]
TRI = [[(0,0),(1,0),(0,1)], [(7,0),(7,1),(6,0)], [(7,7),(6,7),(7,6)], [(0,7),(0,6),(1,7)]]
SHADED = [OCT_C] + SQ + TR
WHITE = OCT_W + TRI

PT = {'A':(0,5),'B':(1,0),'C':(7,2),'D':(4,6)}
LABPOS = {'A':(-3.4,19.2),'B':(9,67.6),'C':(66.6,46.2),'D':(39.6,7.6)}

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def pill(x, y, s, col=GOLD, size=3.0):   # подпись на тёмной подложке, чтобы не путалась с отрезками
    w = 1.9*len(s) + 1.6
    return (f"<rect x='{x-w/2}' y='{y-size+0.2}' width='{w}' height='{size+1.4}' rx='0.8' fill='#0e1116' fill-opacity='0.85'/>"
            + txt(x, y, s, col, size))
def grid(col=DIM, w=0.25):
    return ''.join(line((i,0),(i,7),col,w) + line((0,i),(7,i),col,w) for i in range(1,7))
def pieces(col=INK, w=0.6, shade=RED, op=0.5):
    return (''.join(poly(p, col, w, shade, op) for p in SHADED) + ''.join(poly(p, col, w) for p in WHITE)
            + poly([(0,0),(7,0),(7,7),(0,7)], col, w))
def labels(names=None, col=LAB, dots=True):
    names = names or list(PT)
    s = ''.join(txt(*LABPOS[n], n, col) for n in names)
    if dots: s += ''.join(f"<circle cx='{xy(PT[n])[0]}' cy='{xy(PT[n])[1]}' r='0.75' fill='{col}'/>" for n in names)
    return s
def svg(inner, label, vb='-8 -8 79 79', mw=560):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def lab(p, s, dx=0, dy=0, col=GOLD, size=2.8):
    X, Y = xy(p); return pill(X+dx, Y+dy, s, col, size)
def xmark():   # черта x в исходном месте — верхняя сторона верхнего квадратика
    return line((3,6),(4,6),GOLD,1.4) + lab((3.5,6), 'x', 0, 4.0, GOLD, 3.0)

V = {}
# 1. рисунок условия — как в оригинале (закрашенная копия с точками A, B, C, D)
V['а меньшее основание — сторона квадратика'] = fig(svg(pieces() + labels(), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: сетка x × x, x на стороне квадратика, 3x на большем основании, 7x на стороне
s = grid('#5c6b7a', 0.3) + pieces(DIM, 0.5, RED, 0.22) + labels(None, MUT)
s += xmark() + line((2,7),(5,7),GOLD,1.2) + txt(31.5,-2.4,'3x',GOLD,3.2)
s += line((7,0),(7,7),GOLD,1.0) + txt(67.6,32.6,'7x',GOLD,3.2)
V['x — сторона квадратика, шаг сетки.'] = fig(svg(s, 'Буквы', '-8 -8 80 80'),
  "<b style='color:#f0a83c'>x</b> — сторона квадратика; большее основание трапеции — 3x, сторона большого квадрата — 7x.")

G = grid('#3e4b58', 0.3)
# а) сторона квадратика
s = G + pieces(DIM, 0.5, 'none', 1) + labels(None, MUT) + poly(SQ[0], BLUE, 0.9, BLUE, 0.45) + xmark()
V['сторона квадратика — это и есть x'] = fig(svg(s, 'Сторона квадратика на сетке'), '')

# б) закрашенное: восьмиугольник дан, 4 квадратика, 4 трапеции = квадратик + 2 треугольника
s = G + pieces(DIM, 0.5, 'none', 1) + labels(None, MUT)
s += poly(OCT_C, RED, 0.8, RED, 0.45) + ''.join(poly(p, BLUE, 0.8, BLUE, 0.45) for p in SQ)
s += ''.join(poly(p, GOLD, 0.8, GOLD, 0.45) for p in TR)
s += line((3,6),(3,7),GOLD,0.6,True) + line((4,6),(4,7),GOLD,0.6,True)
s += lab((2.5,7), 'x', 0, -1.6) + lab((3,6.5), 'x', -2.4, 1.0)
X, Y = xy((3.5,3.5)); s += pill(X, Y+1.4, '252', RED, 4.0)
s += xmark()
V['закрашенное — центральный восьмиугольник'] = fig(svg(s, 'Закрашенное на сетке'),
  "<b style='color:#f2686c'>Восьмиугольник — 252, дано в условии</b>; <b style='color:#5ba8f5'>4 квадратика x × x</b>; "
  "<b style='color:#f0a83c'>4 трапеции</b> — квадратик и два треугольника с катетами x. Белое не считаем.")

# в) ABCD = прямоугольник 7x × 6x без четырёх треугольников
s = G + pieces(DIM, 0.5, 'none', 1)
s += poly([(0,0),(7,0),(7,6),(0,6)], GOLD, 0.8, 'none', 1).replace("stroke-linejoin", "stroke-dasharray='1.6 1.2' stroke-linejoin")
s += poly([PT['A'],PT['B'],PT['C'],PT['D']], VIO, 1.0, VIO, 0.3)
for t in [[(0,0),(1,0),(0,5)], [(1,0),(7,0),(7,2)], [(7,2),(7,6),(4,6)], [(4,6),(0,6),(0,5)]]:
    s += poly(t, GOLD, 0.6, GOLD, 0.35)
s += lab((0.5,0), 'x', 0, 4.4) + lab((0,2.5), '5x', -4.0, 1.0)
s += lab((4,0), '6x', 0, 4.4) + lab((7,1), '2x', 4.0, 1.0)
s += lab((7,4), '4x', 4.0, 1.0) + lab((5.5,6), '3x', 0, -1.6)
s += lab((2,6), '4x', 0, -1.6) + lab((0,5.5), 'x', -3.4, 1.0)
s += labels(None, LAB) + xmark()
V['ABCD не прямоугольник и не трапеция'] = fig(svg(s, 'ABCD на сетке', '-9 -9 81 81'),
  "<b style='color:#f0a83c'>Прямоугольник 7x × 6x</b> (пунктир) без четырёх <b style='color:#f0a83c'>треугольников</b> — остаётся <b style='color:#c58af9'>ABCD</b>.")

# раздел «Найдём x»: восьмиугольник = 5 квадратиков + 4 треугольника
s = G + pieces(DIM, 0.5, 'none', 1) + labels(None, MUT)
for c in [(3,2),(2,3),(3,3),(4,3),(3,4)]:
    s += poly([c, (c[0]+1,c[1]), (c[0]+1,c[1]+1), (c[0],c[1]+1)], BLUE, 0.8, BLUE, 0.45)
for t in [[(3,2),(3,3),(2,3)], [(4,2),(5,3),(4,3)], [(5,4),(4,5),(4,4)], [(3,5),(2,4),(3,4)]]:
    s += poly(t, GOLD, 0.8, GOLD, 0.5)
s += lab((3,2.5), 'x', 2.6, 1.0) + lab((2.5,3), 'x', 0, -1.6)
s += xmark()
V['закрасим квадратики и треугольники разными цветами'] = fig(svg(s, 'Восьмиугольник: квадратики и треугольники'),
  "<b style='color:#5ba8f5'>5 квадратиков x × x</b> и <b style='color:#f0a83c'>4 треугольника с катетами x</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
