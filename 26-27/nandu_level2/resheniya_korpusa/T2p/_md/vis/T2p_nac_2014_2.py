import json, sys
# Рисунки к Т2′ национал 2014 №2. Координаты задачи — в кирпичах x (y вверх): катет треугольника 1, GF = 4, HA = 5
# (так выходит в решении, x = 22): A = (0, 1), B = (1, 0), C = (5, 0), D = (6, 1), E = (6, 6), F = (5, 7), G = (1, 7), H = (0, 6).
# SVG: X = U·x, Y = U(7 − y).
U = 8
def xy(p): return round(U*p[0], 2), round(U*(7-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,1),'B':(1,0),'C':(5,0),'D':(6,1),'E':(6,6),'F':(5,7),'G':(1,7),'H':(0,6)}
OFF = {'A':(-3.0,2.4),'B':(-1.2,4.2),'C':(1.2,4.2),'D':(3.0,2.4),'E':(3.0,-0.6),'F':(1.4,-1.6),'G':(-1.4,-1.6),'H':(-3.0,-0.6)}
ALL = list(PT)
# углы внутренних прямоугольников (без имён в условии)
I1,I2,I3,I4 = (1,1),(5,1),(5,6),(1,6)

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
def svg(inner, label, vb='-9 -6 66 70', mw=380):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:{mw}px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def full(col=DIM, w=0.45):   # весь чертёж условия: контур, прямые HE, AD, GB, FC
    P_ = PT
    s = poly([P_[k] for k in 'ABCDEFGH'], col, w)
    s += line(P_['H'],P_['E'],col,w) + line(P_['A'],P_['D'],col,w) + line(P_['G'],P_['B'],col,w) + line(P_['F'],P_['C'],col,w)
    return s
def pieces(col=MUT, size=3.6):   # имена прямоугольников
    return (at((3,6.5),'R',0,1.2,col,size) + at((3,0.5),'R',0,1.2,col,size) + at((0.5,3.5),'P',0,1.2,col,size)
            + at((5.5,3.5),'P',0,1.2,col,size) + at((3,3.5),'Q',0,1.2,col,size+0.6))
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def T(*n): return [PT[k] if isinstance(k,str) else k for k in n]
TRI_H = T('H','G',I4); TRI_A = T('A','B',I1); TRI_E = T('E','F',I3); TRI_D = T('D','C',I2)
P_L = [(0,1),(1,1),(1,6),(0,6)]; P_R = [(5,1),(6,1),(6,6),(5,6)]
R_T = [(1,6),(5,6),(5,7),(1,7)]; R_B = [(1,0),(5,0),(5,1),(1,1)]
Q_ = [(1,1),(5,1),(5,6),(1,6)]
def xmark():   # кирпич x — катет треугольника у H
    return line(PT['H'],I4,GOLD,1.4) + at((0.5,6),'x',0,3.6,GOLD,3.2)
L_GF = lambda col=RED: at((3,7), 'GF', 0, -1.6, col, 2.8)
L_HA = lambda col=RED: at((0,3.5), 'HA', -4.4, 1.0, col, 2.8)

V = {}
# 1. рисунок условия
s = full(INK, 0.6) + pieces() + labels(ALL)
V['треугольники прямоугольные'] = fig(svg(s, 'Рисунок условия', mw=420), 'Рисунок из условия.')

# 2. буквы
s = full() + pieces(DIM) + tri(TRI_H, GOLD, 0.3) + tri(TRI_A, GOLD, 0.3) + tri(TRI_E, GOLD, 0.3) + tri(TRI_D, GOLD, 0.3)
s += xmark() + line(PT['G'],I4,GOLD,1.4) + at((1,6.5),'x',2.4,1.0,GOLD,3.2)
s += line(PT['G'],PT['F'],RED,1.0) + line(PT['H'],PT['A'],RED,1.0) + L_GF() + L_HA() + names()
V['GF и HA — неизвестные отрезки.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> — катет треугольника; <b style='color:#f2686c'>GF</b> и <b style='color:#f2686c'>HA</b> пока неизвестны.")

# 3. а) ADEH
s = full() + poly(T('A','D','E','H'), GOLD, 1.2, GOLD, 0.25) + pieces(DIM)
s += at((3,1), 'x + GF + x', 0, -1.6, GOLD, 2.8) + L_HA(GOLD) + xmark() + names()
V['ширины Q и ширины правого P.'] = fig(svg(s, 'Прямоугольник ADEH'), 'а) площадь ADEH: стороны AD и HA.')

# 4. б) BCDEFG = вся фигура без левого P и треугольников при A и H
s = full() + poly(T('B','C','D','E','F','G'), GOLD, 1.2, GOLD, 0.25)
s += tri(P_L, RED, 0.3) + tri(TRI_A, RED, 0.3) + tri(TRI_H, RED, 0.3) + pieces(DIM) + names()
V['без левого P и треугольников при A и H.'] = fig(svg(s, 'BCDEFG'),
  "б) площадь <b style='color:#f0a83c'>BCDEFG</b>: вся фигура без <b style='color:#f2686c'>левого P и двух треугольников</b>.")

# 5. в) ABCDEFGH = 2 · Q
s = full() + poly(T('A','B','C','D','E','F','G','H'), GOLD, 1.2, GOLD, 0.2) + tri(Q_, BLUE, 0.35)
s += pieces(DIM) + L_GF() + L_HA() + names()
V['Q — прямоугольник со сторонами GF и HA.'] = fig(svg(s, 'ABCDEFGH и Q'),
  "в) площадь <b style='color:#f0a83c'>ABCDEFGH</b> — две площади <b style='color:#5ba8f5'>Q</b>.")

# 6. раздел «Найдём HA»: P и треугольник
s = full() + tri(P_L, BLUE, 0.35) + tri(TRI_H, GOLD, 0.45) + pieces(DIM) + xmark()
s += at((0.5,1), 'x', 0, 3.6, BLUE, 3.0) + L_HA(BLUE) + names()
V['Площадь P. Стороны x и HA.'] = fig(svg(s, 'P и треугольник'),
  "<b style='color:#5ba8f5'>P</b>: стороны x и HA; <b style='color:#f0a83c'>треугольник</b>: катеты x и x.")

# 7. раздел «Найдём GF»: Q против остальных кусков
s = full() + tri(Q_, BLUE, 0.4)
for p in (P_L, P_R, R_T, R_B): s += tri(p, GOLD, 0.25)
for t in (TRI_H, TRI_A, TRI_E, TRI_D): s += tri(t, GREEN, 0.35)
s += pieces(LAB) + names()
V['два P, два R и четыре треугольника.'] = fig(svg(s, 'Q и остальные куски'),
  "<b style='color:#5ba8f5'>Q</b> и остальные куски: <b style='color:#f0a83c'>два P, два R</b> и <b style='color:#5fd38d'>четыре треугольника</b>.")

# 8. раздел «Найдём x»: R
s = full() + tri(R_T, RED, 0.4) + pieces(DIM) + at((3,7), '4x', 0, -1.6, RED, 3.0) + at((5,6.5), 'x', 2.4, 1.0, RED, 3.0) + names()
V['R — прямоугольник со сторонами GF = 4x и x.'] = fig(svg(s, 'Прямоугольник R'), 'Прямоугольник R: стороны 4x и x.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
