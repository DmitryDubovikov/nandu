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

# 3. закрашенное в треугольничках
s = grid(DIM, 0.25) + pieces(DIM, 0.5, RED, 0.5) + stubs(DIM, 0.5)
s += ''.join(line(a, b, INK, 0.35) for a, b in CUTS_TRAPS + CUTS_SQ)
s += ''.join(poly(p, GOLD, 0.9) for p in [TRAP_CORNER, [(8,3),(8,2),(6,4),(7,4)]]) + poly(SQ_CENTER, BLUE, 0.9)
V['двенадцать трапеций по три половинки клетки'] = fig(svg(s, 'Закрашенное в половинках клетки'),
  "Закрашенное, разрезанное сеткой на половинки клеток: <b style='color:#f0a83c'>трапеции</b> "
  "(угловая и боковая равны) и <b style='color:#5ba8f5'>закрашенный квадрат</b>.")

# 4–7. артефакт: каждое спрошенное на сетке d — видно, что оно меряется клетками d × d
def dmark():   # одна клетка d у D
    return line((0,8),(1,8),GOLD,1.4) + txt(4,-2.4,'d',GOLD,3.2)
def hticks(y, x0, x1, below=False):   # отметки d подряд вдоль горизонтали y, от x0 до x1
    out = ''
    for i in range(x0, x1):
        out += line((i+0.1, y), (i+0.9, y), GOLD, 1.3)
        X, Y = xy((i+0.5, y)); out += txt(X, Y + (3.6 if below else -1.3), 'd', GOLD, 2.6)
    return out
def vticks(x, y0, y1, left=False):    # отметки d подряд вдоль вертикали x, от y0 до y1
    out = ''
    for j in range(y0, y1):
        out += line((x, j+0.1), (x, j+0.9), GOLD, 1.3)
        X, Y = xy((x, j+0.5)); out += txt(X + (-2.2 if left else 2.2), Y + 0.9, 'd', GOLD, 2.6)
    return out
G = grid('#3e4b58', 0.3)
s = G + pieces(DIM, 0.5, 'none', 1) + stubs(DIM, 0.5) + poly(SQ_CENTER, BLUE, 0.9, BLUE, 0.3)
s += ''.join(line(a, b, INK, 0.35) for a, b in CUTS_SQ) + hticks(4, 2, 6) + vticks(4, 2, 6)
V['а) площадь закрашенного квадрата'] = fig(svg(s, 'Закрашенный квадрат на сетке', '-9 -9 82 82'), '')
s = G + ''.join(poly(p, DIM, 0.5, GREEN if not sh else 'none', 0.3 if not sh else 1) for p, sh in PIECES) + stubs(DIM, 0.5) + hticks(0, 0, 8, True) + vticks(0, 0, 8, True)
V['б) площадь незакрашенной части'] = fig(svg(s, 'Незакрашенная часть на сетке', '-9 -9 82 82'), '')
s = G + pieces(DIM, 0.5, 'none', 1) + stubs(DIM, 0.5) + poly([PT['M'],PT['N'],PT['P'],PT['Q']], VIO, 1.0, VIO, 0.3)
s += labels(['M','N','P','Q'], MUT) + hticks(4, 1, 7) + vticks(4, 1, 7)
V['в) площадь MNPQ'] = fig(svg(s, 'MNPQ на сетке', '-9 -9 82 82'), '')
s = G + pieces(DIM, 0.5, 'none', 1) + stubs(DIM, 0.5) + poly([(0,0),(8,0),(8,8),(0,8)], DIM, 0.8) + hticks(0, 0, 8, True) + hticks(8, 0, 8) + vticks(0, 0, 8, True) + vticks(8, 0, 8)
V['г) периметр ABCD'] = fig(svg(s, 'Контур ABCD на сетке', '-9 -9 82 82'), '')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
