import json, sys
# Рисунки к Т2″ регионал 2015 №2. Координаты задачи в см (y вверх):
# A = (0, 0), B = (56, 0), C = (56, 8), F = (0, 8), G = (8, 8), E = (0, 44), D = (8, 44).  SVG: X = U·x, Y = U·(44 − y).
U = 1.2
def xy(p): return round(U*p[0], 2), round(U*(44-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(56,0),'C':(56,8),'F':(0,8),'G':(8,8),'E':(0,44),'D':(8,44)}
OFF = {'A':(-3.0,3.6),'B':(3.0,3.6),'C':(3.4,0.4),'F':(-3.4,1.2),'G':(2.6,4.4),'E':(-3.0,-1.6),'D':(3.0,-1.6)}
ALL = ['A','B','C','D','E','F','G']
SEG = [('A','B'),('B','C'),('C','F'),('F','A'),('E','D'),('D','G'),('E','F'),('D','C')]

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
def labels(names, col=LAB):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col) + f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def full(col=DIM, w=0.45): return ''.join(line(PT[a], PT[b], col, w) for a, b in SEG)
def names(): return labels(ALL, MUT)
def svg(inner, label, vb='-8 -6 84 64', mw=None):
    st = f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def fill(pts, col, op=0.4): return poly([PT[n] for n in pts], col, 1.0, col, op)
def outline(pts, col, w=1.1): return poly([PT[n] for n in pts], col, w)
def rangle(p, sx, sy, col=INK, s=2.4):   # прямой угол в вершине p (s — в см)
    a, b, c = (p[0]+sx*s, p[1]), (p[0]+sx*s, p[1]+sy*s), (p[0], p[1]+sy*s)
    return f"<polyline points='{'%s,%s' % xy(a)} {'%s,%s' % xy(b)} {'%s,%s' % xy(c)}' fill='none' stroke='{col}' stroke-width='0.4'/>"
def angles(col=INK): return rangle(PT['G'], 1, 1, col) + rangle(PT['A'], 1, 1, col) + rangle(PT['E'], 1, -1, col)

# цвет куска — один во всех рисунках
PC = {'ABCF': BLUE, 'DEFG': GREEN, 'CDG': VIO}
PP = {'ABCF': ['A','B','C','F'], 'DEFG': ['D','E','F','G'], 'CDG': ['C','D','G']}
def piece(n, op=0.42): return fill(PP[n], PC[n], op)
def cname(n): return f"<b style='color:{PC[n]}'>{n}</b>"
def xs(col=GOLD):   # отрезки длины x: AF, FG, BC, DE
    s = ''
    for a, b in [('A','F'),('F','G'),('B','C'),('E','D')]: s += line(PT[a], PT[b], col, 1.3)
    s += at((0,4), 'x', -2.6, 1.0, col) + at((4,8), 'x', 0, -1.4, col) + at((56,4), 'x', 2.6, 1.0, col) + at((4,44), 'x', 0, -1.6, col)
    return s

V = {}
# 1. рисунок условия
V['отрезки разрезают чертёж на прямоугольники'] = fig(svg(full(INK, 0.55) + labels(ALL), 'Рисунок условия', mw=460), 'Рисунок из условия.')

# 2. три куска
s = full(INK, 0.5) + ''.join(piece(n) for n in PC) + angles()
s += at((28,4), 'ABCF', 0, 1.0, LAB, 2.8) + at((4,26), 'DEFG', 0, 1.0, LAB, 2.4) + at((20,18), 'CDG', 0, 1.0, LAB, 2.8) + labels(ALL)
V['ABCF, DEFG и треугольник CDG'] = fig(svg(s, 'Три куска'), '')

# 3. буквы
s = full() + xs() + names()
V['обозначим AF = FG = x'] = fig(svg(s, 'Буквы'), "<b style='color:#f0a83c'>x</b> — AF = FG; BC = AF и DE = FG как противоположные стороны прямоугольников.")

# 4–6. каждое спрошенное
s = full() + piece('ABCF', 0.5) + outline(PP['ABCF'], BLUE) + line(PT['A'],PT['F'],GOLD,1.3) + at((0,4), 'x', -2.6, 1.0)
s += at((32,8), 'FC = ?', 0, -1.4, LAB, 2.8) + names()
V['со сторонами AF = x и FC.'] = fig(svg(s, 'а) периметр ABCF'), 'а) периметр ABCF')
s = full() + piece('DEFG', 0.5) + piece('CDG', 0.5) + line(PT['F'],PT['G'],GOLD,1.3) + at((4,8), 'x', 0, -1.4)
s += at((8,26), 'DG', 3.4, 1.0, LAB, 2.8) + names()
V['со сторонами FG = x и DG.'] = fig(svg(s, 'б) площадь CDEF'), f"б) площадь CDEF = {cname('DEFG')} + {cname('CDG')}")
s = full() + poly([PT[n] for n in ['A','B','C','D','E']], RED, 1.2)
s += line(PT['E'],PT['F'],GREEN,1.4) + line(PT['F'],PT['A'],GOLD,1.4) + at((0,26), 'DG', -3.6, 1.0, GREEN, 2.8) + at((0,4), 'x', -2.6, 1.0)
s += at((56,4), 'x', 2.6, 1.0) + at((4,44), 'x', 0, -1.6) + at((28,0), 'AB = FC', 0, 3.6, LAB, 2.8) + at((32,26), 'CD', 3.0, -1.0, LAB, 2.8) + names()
V['EA состоит из EF = DG и FA = x'] = fig(svg(s, 'в) периметр ABCDE'), "в) периметр ABCDE: обход AB, BC, CD, DE, EA; EA = <b style='color:#5fd38d'>EF</b> + <b style='color:#f0a83c'>FA</b>")

# 7. порядок поиска длин: номер у отрезка — раздел, где найдём его длину
s = full() + ''.join(piece(n, 0.25) for n in PC)
s += line(PT['F'],PT['C'],GOLD,1.3) + line(PT['A'],PT['F'],GOLD,1.3) + line(PT['D'],PT['G'],GOLD,1.3) + line(PT['C'],PT['D'],GOLD,1.3)
s += at((32,8), 'FC ①', 0, -1.4, LAB, 2.8) + at((0,4), 'x ②', -4.4, 1.0, LAB, 2.8) + at((8,26), 'DG ③', 4.6, 1.0, LAB, 2.8) + at((32,26), 'CD ④', 4.6, -1.0, LAB, 2.8) + names()
V['FC через x → x → DG → CD'] = fig(svg(s, 'Порядок поиска длин'), 'Номер у отрезка — раздел, где найдём его длину: ① FC через x, ② x, ③ DG, ④ CD.')

# 8. раздел 1: CDG и DEFG — общая сторона DG
s = full() + piece('DEFG', 0.5) + piece('CDG', 0.5) + line(PT['D'],PT['G'],GOLD,1.5) + at((8,26), 'DG', 3.4, 1.0)
s += line(PT['F'],PT['G'],GOLD,1.3) + at((4,8), 'x', -1.0, 3.6) + at((32,8), 'GC', 0, 3.6, LAB, 2.8) + rangle(PT['G'], 1, 1) + names()
V['у CDG и DEFG общая сторона DG'] = fig(svg(s, 'CDG и DEFG, общая сторона DG'),
  f"{cname('CDG')} и {cname('DEFG')}: общая сторона DG; у {cname('CDG')} катеты DG и GC, у {cname('DEFG')} стороны x и DG.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
