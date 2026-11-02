import json, sys
# Рисунки к Т2‴ национал 2017 день I №2. Координаты задачи — в клетках d (y вверх), A = (0, 0), C = (8, 8).
# SVG: X = 8x, Y = 8(8 − y). Детали заданы для верхней левой части и размножены симметриями квадрата.
U = 8
def xy(p): return U*p[0], U*(8-p[1])
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

def sym(p, k):
    x, y = p
    for _ in range(k % 4): x, y = y, 8-x          # поворот на четверть оборота
    if k >= 4: x = 8-x                            # отражение
    return (x, y)
def orbit(poly):
    out, seen = [], set()
    for k in range(8):
        q = [sym(p, k) for p in poly]
        key = frozenset(q)
        if key not in seen: seen.add(key); out.append(q)
    return out

# детали: (вершины, закрашена ли)
TRAP_CORNER = [(1,8),(2,8),(0,6),(0,7)]
TRAP_SIDE   = [(2,8),(3,8),(4,7),(4,6)]
TRI_CORNER  = [(0,8),(1,8),(0,7)]
TRI_SIDE    = [(3,8),(5,8),(4,7)]
SQ_WHITE    = [(2,8),(0,6),(2,4),(4,6)]
SQ_CENTER   = [(4,6),(2,4),(4,2),(6,4)]
TRAPS = orbit(TRAP_CORNER) + orbit(TRAP_SIDE)
WHITE = orbit(TRI_CORNER) + orbit(TRI_SIDE) + orbit(SQ_WHITE)
PIECES = [(p, True) for p in TRAPS + [SQ_CENTER]] + [(p, False) for p in WHITE]

# разрезы сеткой на треугольнички (половинки клетки)
CUT_TRAP = [((1,7),(1,8)), ((0,7),(1,7)), ((3,7),(3,8)), ((3,7),(4,7))]
CUTS_TRAPS = []
for a, b in CUT_TRAP:
    seen = set()
    for k in range(8):
        s = frozenset([sym(a, k), sym(b, k)])
        if s not in seen: seen.add(s); CUTS_TRAPS.append((sym(a, k), sym(b, k)))
CUTS_SQ = [((4,2),(4,6)), ((2,4),(6,4)), ((3,3),(3,5)), ((5,3),(5,5)), ((3,3),(5,3)), ((3,5),(5,5)),
           ((4,5),(5,4)), ((5,4),(4,3)), ((4,3),(3,4)), ((3,4),(4,5))]

PT = {'A':(0,0),'B':(8,0),'C':(8,8),'D':(0,8),'E':(1,8),'F':(2,8),'G':(3,8),'H':(5,8),
      'Q':(4,7),'M':(1,4),'N':(4,1),'P':(7,4)}
LABPOS = {'A':(-3,67.5),'B':(67,67.5),'C':(67,-2.4),'D':(-3,-2.4),'E':(8,-2.6),'F':(16,-2.6),'G':(24,-2.6),
          'H':(40,-2.6),'Q':(32,4.9),'M':(3.7,33.2),'N':(32,62.4),'P':(60.3,33.2)}

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def grid(col=DIM, w=0.25):
    return ''.join(line((i,0),(i,8),col,w) + line((0,i),(8,i),col,w) for i in range(1,8))
def pieces(col=INK, w=0.6, shade=RED, op=0.5):
    return ''.join(poly(p, col, w, shade if s else 'none', op if s else 1) for p, s in PIECES)
def stubs(col=INK, w=0.6):   # короткие отрезки Q–(4,6), M–(2,4), N–(4,2), P–(6,4)
    return line((4,7),(4,6),col,w) + line((1,4),(2,4),col,w) + line((4,1),(4,2),col,w) + line((7,4),(6,4),col,w)
def labels(names=None, col=LAB, dots=True):
    names = names or list(PT)
    s = ''.join(txt(*LABPOS[n], n, col) for n in names)
    if dots: s += ''.join(f"<circle cx='{xy(PT[n])[0]}' cy='{xy(PT[n])[1]}' r='0.75' fill='{col}'/>" for n in names)
    return s
def svg(inner, label, vb='-8 -8 80 80'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"

V = {}
# 1. рисунок условия — как в оригинале, MNPQ не проведён
V['Чему равен периметр ABCD?'] = fig(svg(pieces() + stubs() + labels(), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: сетка d × d, d на DE, EF, FG
s = grid('#5c6b7a', 0.3) + pieces(DIM, 0.5, RED, 0.22) + stubs(DIM, 0.5)
for a, b in [((0,8),(1,8)), ((1,8),(2,8)), ((2,8),(3,8))]: s += line(a, b, GOLD, 1.4)
s += txt(4,-2.4,'d',GOLD) + txt(12,-2.4,'d',GOLD) + txt(20,-2.4,'d',GOLD)
s += line((0,0),(0,8),GOLD,1.0) + txt(-4.4,33.2,'8d',GOLD,3.2)
s += ''.join(txt(x, y, n, MUT) for n, (x, y) in
            {'D':(-3,-6.6),'E':(8,-6.6),'F':(16,-6.6),'G':(24,-6.6),'H':(40,-6.6),'C':(67,-2.4),'A':(-3,67.5),'B':(67,67.5)}.items())
V['DE = d — шаг сетки.'] = fig(svg(s, 'Буквы', '-9 -11 81 83'),
  "<b style='color:#f0a83c'>d</b> = DE = EF = FG; DC = 8d.")

# 3. раздел «Найдём d»: закрашенное двумя цветами; трапеция; квадрат
def lab(p, s, dx=0, dy=0, col=GOLD, size=2.8):
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
s = grid('#3e4b58', 0.3) + stubs(DIM, 0.5)
s += ''.join(poly(p, GOLD, 0.6, GOLD, 0.55) for p in TRAPS) + poly(SQ_CENTER, BLUE, 0.8, BLUE, 0.55)
s += ''.join(poly(p, DIM, 0.5) for p in WHITE)
V['закрасим их разными цветами'] = fig(svg(s, 'Закрашенное: трапеции и квадрат'),
  "<b style='color:#f0a83c'>12 трапеций</b> и <b style='color:#5ba8f5'>1 квадрат</b>.")
s = grid('#3e4b58', 0.3) + pieces(DIM, 0.5, 'none', 1) + stubs(DIM, 0.5)
for tris in [[[(1,8),(2,8),(1,7)], [(1,8),(1,7),(0,7)], [(0,7),(1,7),(0,6)]],
             [[(8,2),(8,3),(7,3)], [(8,3),(7,3),(7,4)], [(7,3),(7,4),(6,4)]]]:
    s += ''.join(poly(t, GOLD, 0.8, GOLD, 0.5) for t in tris)
s += lab((1.5,8), 'd', 0, -1.4) + lab((1,7.5), 'd', 2.0, 1.0)
s += lab((7.5,3), 'd', 0, 3.4) + lab((8,2.5), 'd', 2.2, 1.0)
V['Трапеция — три треугольника с катетами d.'] = fig(svg(s, 'Трапеция'),
  "Угловая и боковая трапеции — по <b style='color:#f0a83c'>три треугольника с катетами d</b>.")
s = grid('#3e4b58', 0.3) + pieces(DIM, 0.5, 'none', 1) + stubs(DIM, 0.5) + poly(SQ_CENTER, BLUE, 0.9, BLUE, 0.15)
s += line((2,4),(6,4),BLUE,0.6,True) + line((4,2),(4,6),BLUE,0.6,True)
s += poly([(4,4),(4,6),(2,4)], BLUE, 1.0, BLUE, 0.5) + lab((3,4), '2d', 0, 4.0, BLUE, 3.0) + lab((4,5), '2d', 4.0, 1.0, BLUE, 3.0)
V['Квадрат — четыре треугольника с катетами 2d.'] = fig(svg(s, 'Квадрат'), "Четыре одинаковых треугольника с катетами 2d.")

# 4–7. артефакт: каждое спрошенное на сетке d — видно, что оно меряется клетками d × d
def dmark():   # одна клетка d у D
    return line((0,8),(1,8),GOLD,1.4) + txt(4,-2.4,'d',GOLD,3.2)
def hspan(y, x0, x1, lab, below=False):   # один отрезок длины (x1 − x0)d с подписью
    X, Y = xy(((x0+x1)/2, y))
    return line((x0, y), (x1, y), GOLD, 1.3) + txt(X, Y + (4.0 if below else -1.6), lab, GOLD, 3.0)
def vspan(x, y0, y1, lab, left=False):
    X, Y = xy((x, (y0+y1)/2))
    return line((x, y0), (x, y1), GOLD, 1.3) + txt(X + (-4.2 if left else 4.2), Y + 1.0, lab, GOLD, 3.0)
def tri2(pts, labs, col):   # один прямоугольный треугольник: заливка + подписи катетов
    out = poly(pts, col, 1.0, col, 0.45)
    for p, s_, dx, dy in labs: out += lab(p, s_, dx, dy, col, 3.0)
    return out
G = grid('#3e4b58', 0.3)
# а) закрашенный квадрат = 4 треугольника с катетами 2d
s = G + pieces(DIM, 0.5, 'none', 1) + stubs(DIM, 0.5) + poly(SQ_CENTER, BLUE, 0.9, BLUE, 0.15)
s += line((2,4),(6,4),BLUE,0.6,True) + line((4,2),(4,6),BLUE,0.6,True)
s += tri2([(4,4),(4,6),(2,4)], [((3,4),'2d',0,4.0), ((4,5),'2d',4.0,1.0)], GOLD) + dmark()
V['а) площадь закрашенного квадрата'] = fig(svg(s, 'Закрашенный квадрат на сетке', '-9 -9 82 82'), '')
# б) незакрашенное = ABCD 8d × 8d без закрашенного
s = G + pieces(DIM, 0.5, RED, 0.45) + stubs(DIM, 0.5) + poly([(0,0),(8,0),(8,8),(0,8)], GOLD, 1.0)
s += hspan(0, 0, 8, '8d', True) + vspan(0, 0, 8, '8d', True) + dmark()
s += f"<rect x='14' y='26' width='36' height='13' rx='2' fill='#0e1116' fill-opacity='0.88'/>" + txt(32, 31.4, '8d × 8d', GOLD, 4.2) + txt(32, 37, '− 416', '#f2686c', 4.2)
V['б) площадь незакрашенной части'] = fig(svg(s, 'Незакрашенная часть на сетке', '-9 -9 82 82'),
  "<b style='color:#f0a83c'>Весь ABCD</b> минус <b style='color:#f2686c'>закрашенное — 416, дано в условии</b>. Треугольники не считаем.")
# в) MNPQ = 4 треугольника с катетами 3d
s = G + pieces(DIM, 0.5, 'none', 1) + stubs(DIM, 0.5) + poly([PT['M'],PT['N'],PT['P'],PT['Q']], VIO, 1.0, VIO, 0.15)
s += line((1,4),(7,4),VIO,0.6,True) + line((4,1),(4,7),VIO,0.6,True) + labels(['M','N','P','Q'], MUT)
s += tri2([(4,4),(4,7),(1,4)], [((2.5,4),'3d',0,4.0), ((4,5.5),'3d',4.0,1.0)], GOLD) + dmark()
V['в) площадь MNPQ'] = fig(svg(s, 'MNPQ на сетке', '-9 -9 82 82'), '')
# г) периметр — четыре стороны по 8d
s = G + pieces(DIM, 0.5, 'none', 1) + stubs(DIM, 0.5) + poly([(0,0),(8,0),(8,8),(0,8)], GOLD, 1.0) + hspan(0, 0, 8, '8d', True) + vspan(0, 0, 8, '8d', True) + dmark()
V['г) периметр ABCD'] = fig(svg(s, 'Контур ABCD на сетке', '-9 -9 82 82'), '')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
