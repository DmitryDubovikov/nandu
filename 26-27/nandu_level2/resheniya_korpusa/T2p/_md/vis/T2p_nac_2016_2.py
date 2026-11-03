import json, sys
# Рисунки к Т2′ национал 2016 день I №2. Координаты задачи — в кирпичах x = EF : 2 (y вверх), H = (0, 0):
# D = (−7, 0), G = (−3, 0), B = (5, 0), E = (−5, −6), F = (−3, −6), A = (0, −6), C = (0, 7.2).
# SVG: X = U(x + 9), Y = U(8.5 − y).
U = 6
def xy(p): return round(U*(p[0]+9), 2), round(U*(8.5-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,-6),'B':(5,0),'C':(0,7.2),'D':(-7,0),'E':(-5,-6),'F':(-3,-6),'G':(-3,0),'H':(0,0)}
OFF = {'A':(2.6,4.4),'B':(3.6,1.2),'C':(0,-2.0),'D':(-3.6,1.2),'E':(-1.6,4.4),'F':(0,4.4),'G':(-2.6,-1.6),'H':(2.6,-1.6)}
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
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x в полосе между BD и AE
    s = ''.join(line((x,-6),(x,0),col,w) for x in range(-7,6))
    return s + ''.join(line((-7,y),(5,y),col,w) for y in range(-6,1))
def svg(inner, label, vb='0 0 96 96'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def T(*n): return [PT[k] for k in n]
def full(col=DIM, w=0.45):   # весь чертёж условия: контур ABCDEF... и отрезки DB, AC, FG
    s = ''
    for a, b in (('D','C'),('C','B'),('B','A'),('A','F'),('F','E'),('E','D'),('D','B'),('A','C'),('F','G')):
        s += line(PT[a],PT[b],col,w)
    return s
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def xmark():   # кирпич x — половина EF
    return line((-5,-6),(-4,-6),GOLD,1.6) + at((-4.5,-6), 'x', 0, -1.6, GOLD, 3.2)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['AC и FG перпендикулярны обеим прямым BD и AE.'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: сетка с шагом x = EF : 2
s = grid() + full() + xmark()
s += line(PT['G'],PT['F'],GOLD,1.0) + at((-3,-3), '6x', -3.6, 1.0)
s += line(PT['F'],PT['A'],GOLD,1.0) + at((-1.5,-6), '3x', 0, -1.6)
s += at((-1.5,0), '3x', 0, -1.6) + at((2.5,0), '5x', 0, -1.6)
s += at((-4,-6), '2x', 0, 4.6)
s += names()
V['сетка с шагом x.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = EF : 2; EF = 2x, FA = GH = 3x, GF = AH = 6x, HB = 5x.")

G = grid() + full()
# 3. а) AHGF — прямоугольник
s = G + poly(T('A','H','G','F'), GOLD, 1.2, GOLD, 0.25) + at((0,-3), '6x', 3.6, 1.0) + at((-1.5,-6), '3x', 0, -1.6) + xmark() + names()
V['AHGF — прямоугольник со сторонами'] = fig(svg(s, 'AHGF на сетке'), 'а) периметр AHGF: стороны 6x и 3x.')
# 4. б) ABCD = ABD + CBD на общем основании DB
s = G + tri(T('A','B','D'), GOLD, 0.35) + tri(T('C','B','D'), BLUE, 0.35)
s += line(PT['A'],PT['H'],GOLD,1.0,True) + line(PT['H'],PT['C'],BLUE,1.0,True)
s += at((0,-3), 'AH', 4.4, 1.0) + at((0,3.6), 'HC', 4.4, 1.0, BLUE) + xmark() + names()
V['высота CBD — HC.'] = fig(svg(s, 'ABCD из двух треугольников'),
  "б) площадь ABCD: <b style='color:#f0a83c'>ABD</b> и <b style='color:#5ba8f5'>CBD</b> на общем основании DB.")
# 5. в) ABE: основание AE, высота GF
s = G + tri(T('A','B','E'), GOLD, 0.4) + line(PT['G'],PT['F'],GREEN,1.0,True)
s += at((-2.5,-6), '5x', 0, 8.2) + at((-3,-3), '6x', -3.6, 1.0, GREEN) + names()
V['то есть GF = 6x.'] = fig(svg(s, 'ABE на сетке'), "в) площадь ABE: основание AE = 5x, <b style='color:#5fd38d'>высота GF</b> = 6x.")
# 6. г) ABCDF = ABCD + DFA
s = G + poly(T('A','B','C','D'), GOLD, 1.0, GOLD, 0.2) + tri(T('D','F','A'), GREEN, 0.45)
s += at((-1.5,-6), '3x', 0, 4.6, GREEN) + line(PT['G'],PT['F'],GREEN,0.9,True) + at((-3,-2), '6x', 3.6, 1.0, GREEN) + xmark() + names()
V['с основанием FA = 3x и высотой GF = 6x.'] = fig(svg(s, 'ABCDF = ABCD + DFA'),
  "г) площадь ABCDF: <b style='color:#f0a83c'>ABCD</b> плюс <b style='color:#5fd38d'>DFA</b>.")

# 7. раздел «Найдём DB»: ABD и EFG
s = G + tri(T('A','B','D'), GOLD, 0.35) + tri(T('E','F','G'), BLUE, 0.55) + line(PT['A'],PT['H'],GOLD,1.0,True)
s += at((0,-3), '6x', 3.6, 1.0) + at((-4,-6), '2x', 0, 4.6, BLUE) + at((-3,-4.5), '6x', 3.6, 1.0, BLUE) + at((-1,0), 'DB', 0, -1.6) + names()
V['«площадь ABD = 6 · площадь EFG»'] = fig(svg(s, 'ABD и EFG'),
  "<b style='color:#f0a83c'>ABD</b>: основание DB, высота AH; <b style='color:#5ba8f5'>EFG</b>: катеты 2x и 6x.")

# 8. раздел «Найдём x»: DFH
s = G + tri(T('D','F','H'), RED, 0.4) + line(PT['G'],PT['F'],RED,1.0,True)
s += at((-5,0), '7x', 0, -1.6, RED) + at((-3,-3), '6x', 3.6, 1.0, RED) + xmark() + names()
V['«площадь DFH равна 525 см²»'] = fig(svg(s, 'DFH'),
  "<b style='color:#f2686c'>DFH</b>: основание DH = 7x, высота FG = 6x; площадь 525.")

# 9. раздел «Найдём HC»: DEFG и BCH
s = G + poly(T('D','E','F','G'), GOLD, 1.0, GOLD, 0.4) + tri(T('B','C','H'), BLUE, 0.4)
s += at((-5,0), '4x', 0, -1.6) + at((-4,-6), '2x', 0, 4.6) + at((-3,-3), '6x', 3.6, 1.0)
s += at((2.5,0), '5x', 0, 4.6, BLUE) + at((0,3.6), 'HC', -4.4, 1.0, BLUE) + names()
V['«площадь DEFG = площадь BCH»'] = fig(svg(s, 'DEFG и BCH'),
  "<b style='color:#f0a83c'>DEFG</b> и <b style='color:#5ba8f5'>BCH</b> равны по площади.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
