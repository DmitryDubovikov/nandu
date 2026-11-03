import json, sys
# Рисунки к Т2′ регионал 2016 №2. Координаты задачи — в кирпичах x (y вверх), A = (0, 0), B = (9, 0), C = (14, 0), D = (23, 0),
# F = (9, 12), E = (14, 12). SVG: X = U · x, Y = U · (12 − y).
U = 4
def xy(p): return round(U*p[0], 2), round(U*(12-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(9,0),'C':(14,0),'D':(23,0),'E':(14,12),'F':(9,12)}
OFF = {'A':(-3.0,3.6),'B':(0,4.4),'C':(0,4.4),'D':(3.0,3.6),'E':(2.4,-1.8),'F':(-2.4,-1.8)}
SEGS = [('A','B'),('B','C'),('C','D'),('A','F'),('F','E'),('E','D'),('F','B'),('E','C')]

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{round(x,2)}' y='{round(y,2)}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=3.0):
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
def labels(col=LAB, dots=True):
    out = ''
    for n in PT:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(X+dx, Y+dy, n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри BCEF
    s = ''.join(line((i,0),(i,12),col,w) for i in range(9,15))
    return s + ''.join(line((9,j),(14,j),col,w) for j in range(0,13))
def full(col=DIM, w=0.45): return ''.join(line(PT[a],PT[b],col,w) for a, b in SEGS)
def names(): return labels(MUT)
def svg(inner, label, vb='-8 -7 108 62', mw='480px'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x — пятая часть FE, у F
    return line((9,12),(10,12),GOLD,1.4) + at((9.5,12), 'x', 0, -2.0, GOLD, 3.2)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
P = PT
G = grid() + full()

V = {}
# 1. рисунок условия
s = full(INK, 0.6) + labels()
V['FE : FB : AF = 5 : 12 : 15.'] = fig(svg(s, 'Рисунок условия', mw='560px'), 'Рисунок из условия.')

# 2. буквы
s = G + line(P['F'],P['E'],GOLD,1.0) + line(P['F'],P['B'],GOLD,1.0) + line(P['A'],P['F'],GOLD,1.0) + line(P['E'],P['D'],GOLD,1.0)
s += at((11.5,12), '5x', 0, -2.0) + at((9,6), '12x', -4.0, 1.0) + at((4.5,6), '15x', -4.4, 0) + at((18.5,6), '15x', 4.4, 0)
s += xmark() + names()
V['сетка с шагом x внутри BCEF.'] = fig(svg(s, 'Буквы', mw='560px'),
  "<b style='color:#f0a83c'>x</b> = AF : 15; все точки, кроме A и D, — в узлах сетки.")

# 3. а) периметр ADEF
s = G + poly([P['A'],P['D'],P['E'],P['F']], GOLD, 1.1)
s += line(P['A'],P['B'],RED,1.4) + line(P['C'],P['D'],RED,1.4)
s += at((4.5,0), 'AB', 0, 4.4, RED) + at((18.5,0), 'AB', 0, 4.4, RED) + at((11.5,0), '5x', 0, 4.4)
s += at((11.5,12), '5x', 0, -2.0) + at((4.5,6), '15x', -4.4, 0) + at((18.5,6), '15x', 4.4, 0) + xmark() + names()
V['неизвестна только AB.'] = fig(svg(s, 'Контур ADEF'), "а) периметр <b style='color:#f0a83c'>ADEF</b>; AD = AB + BC + CD.")

# 4. б) площадь BDEF
s = G + poly([P['B'],P['C'],P['E'],P['F']], BLUE, 1.0, BLUE, 0.35) + tri([P['C'],P['D'],P['E']], GREEN, 0.4)
s += at((11.5,12), '5x', 0, -2.0, BLUE) + at((14,6), '12x', 4.2, 1.0, GREEN) + at((18.5,0), 'AB', 0, 4.4, GREEN)
s += xmark() + names()
V['а D лежит на прямой BC.'] = fig(svg(s, 'BDEF = BCEF + CDE'),
  "б) площадь BDEF: <b style='color:#5ba8f5'>BCEF</b> и <b style='color:#5fd38d'>CDE</b>.")

# 5. в) площадь ABEF
s = G + tri([P['A'],P['B'],P['F']], GOLD, 0.4) + tri([P['B'],P['E'],P['F']], RED, 0.35)
s += at((4.5,0), 'AB', 0, 4.4) + at((9,6), '12x', -4.0, 1.0) + at((10.6,8.6), '270', 0, 1.0, RED, 3.0) + xmark() + names()
V['а A лежит на прямой BC.'] = fig(svg(s, 'ABEF = ABF + BEF'),
  "в) площадь ABEF: <b style='color:#f0a83c'>ABF</b> и <b style='color:#f2686c'>BEF</b> (дана).")

# 6. г) площадь DEF
s = G + tri([P['D'],P['E'],P['F']], VIO, 0.4) + line(P['C'],P['E'],GOLD,1.0,True)
s += at((11.5,12), '5x', 0, -2.0, VIO) + at((14,6), '12x', -4.0, 1.0) + xmark() + names()
V['сколько от C до FE.'] = fig(svg(s, 'DEF на сетке'),
  "г) площадь <b style='color:#c58af9'>DEF</b>: основание FE = 5x, высота CE = 12x.")

# 7. раздел «Найдём x»: BEF — прямоугольный, катеты FE и FB
s = G + tri([P['B'],P['E'],P['F']], RED, 0.4)
s += at((11.5,12), '5x', 0, -2.0, RED) + at((9,6), '12x', -4.0, 1.0, RED) + xmark() + names()
V['Заметим, что BEF — прямоугольный треугольник'] = fig(svg(s, 'BEF на сетке'), 'S(BEF) = 270: катеты 5x и 12x.')

# 8. раздел «Найдём AB»: стороны ABF
s = G + poly([P['A'],P['B'],P['F']], GOLD, 1.1, GOLD, 0.2)
s += at((4.5,0), 'AB', 0, 4.4, RED) + at((9,6), '12x', 4.2, 1.0) + at((4.5,6), '15x', -4.4, 0) + xmark() + names()
V['Заметим, что стороны ABF'] = fig(svg(s, 'Контур ABF'), 'P(ABF) = 108: стороны AB, 12x и 15x.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
