import json, sys
# Рисунки к Т2′ национал 2025 день I №2. Координаты задачи — в кирпичах x (y вверх), A = (0, 0), D = (10, 4), P = (5, 4 + 7/8).
# SVG: X = U·x, Y = U(5 − y).
U = 8
def xy(p): return round(U*p[0], 2), round(U*(5-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'M':(5,0),'B':(10,0),'H':(0,2),'I':(2,2),'N':(5,2),'J':(8,2),'C':(10,2),
      'G':(0,4),'F':(2,4),'O':(5,4),'E':(8,4),'D':(10,4),'P':(5,4.875)}
OFF = {'A':(-3.0,4.4),'M':(0,4.6),'B':(3.0,4.4),'H':(-3.4,1.2),'I':(-2.4,4.2),'N':(2.6,4.2),'J':(2.6,4.2),
       'C':(3.4,1.2),'G':(-3.0,-1.4),'F':(-2.2,-1.6),'O':(2.8,4.0),'E':(2.4,-1.6),'D':(3.0,-1.4),'P':(0,-2.0)}
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
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри ABDG
    s = ''.join(line((x,0),(x,4),col,w) for x in range(0,11))
    return s + ''.join(line((0,y),(10,y),col,w) for y in range(0,5))
def svg(inner, label, vb='-8 -5 96 52'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x — половина CD, у C
    return line((10,2),(10,3),GOLD,1.4) + at((10,2.5), 'x', -2.4, 1.0, GOLD, 3.2)
def full(col=DIM, w=0.45):   # весь чертёж условия
    P_ = PT
    s = poly([P_['A'],P_['B'],P_['D'],P_['G']], col, w)
    s += line(P_['H'],P_['C'],col,w) + line(P_['F'],P_['I'],col,w) + line(P_['E'],P_['J'],col,w)
    s += line(P_['M'],P_['P'],col,w) + line(P_['F'],P_['P'],col,w) + line(P_['P'],P_['E'],col,w)
    return s
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def T(*n): return [PT[k] for k in n]
def dimAB():   # размер AB = 10x выноской ниже чертежа
    return (line((0,-1.2),(10,-1.2),GOLD,0.5) + line((0,-1.0),(0,-1.4),GOLD,0.5) + line((10,-1.0),(10,-1.4),GOLD,0.5)
            + at((5,-1.2), '10x', 0, 4.0))
VB2 = '-8 -5 96 62'   # с выноской под AB

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['BC = CD, а AB = HC = GD'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: сетка, x — половина CD
s = grid() + full() + xmark() + line((10,2),(10,4),GOLD,1.0) + at((10,3.5), '2x', 4.0, 1.0, GOLD, 3.2)
s += line((0,0),(10,0),GOLD,1.0) + dimAB() + names()
V['AB = 10x, сетка с шагом x.'] = fig(svg(s, 'Буквы', VB2),
  "<b style='color:#f0a83c'>x</b> = CD : 2; все точки, кроме P, — в узлах сетки.")

G = grid() + full()
# 3. а) MJEPFI = IJEF + FPE + IMJ
s = G + tri(T('I','J','E','F'), GOLD, 0.35) + tri(T('F','P','E'), BLUE, 0.5) + tri(T('I','M','J'), GREEN, 0.35)
s += line(PT['M'],PT['N'],GREEN,0.8,True) + line(PT['P'],PT['O'],BLUE,0.8)
s += at((5,2), '6x', -9, -1.2, GOLD) + at((2,3), '2x', -3.0, 1.0, GOLD) + at((5,1), '2x', 2.6, 1.0, GREEN)
s += xmark() + names()
V['основание IJ, высота MN'] = fig(svg(s, 'MJEPFI на сетке'),
  "а) площадь MJEPFI: <b style='color:#f0a83c'>IJEF</b>, <b style='color:#5ba8f5'>FPE</b> и <b style='color:#5fd38d'>IMJ</b>.")
# 4. б) BEPF = FPE + FEB
s = G + tri(T('F','P','E'), BLUE, 0.5) + tri(T('F','E','B'), GOLD, 0.35) + line(PT['P'],PT['O'],BLUE,0.8)
s += line(PT['B'],PT['D'],GOLD,0.9,True) + at((5,4), '6x', -6, 4.0, GOLD) + at((10,3), '4x', 4.0, 1.0, GOLD)
s += xmark() + names()
V['основание FE, высота BD'] = fig(svg(s, 'BEPF на сетке'),
  "б) площадь BEPF: <b style='color:#5ba8f5'>FPE</b> и <b style='color:#f0a83c'>FEB</b>, высота FEB — BD.")
# 5. в) ACDE = ABDG без ABC и AGE
s = G + poly(T('A','B','D','G'), GOLD, 1.0) + tri(T('A','C','D','E'), VIO, 0.4)
s += tri(T('A','B','C'), BLUE, 0.3) + tri(T('A','G','E'), GREEN, 0.3)
s += dimAB() + at((10,1), '2x', 4.0, 1.0, BLUE) + at((0,3), '4x', -4.0, 1.0, GREEN) + at((4,4), '8x', 0, -1.6, GREEN)
s += xmark() + names()
V['это прямоугольник ABDG без'] = fig(svg(s, 'ACDE внутри ABDG', VB2),
  "в) площадь ACDE: <b style='color:#f0a83c'>ABDG</b> без <b style='color:#5ba8f5'>ABC</b> и <b style='color:#5fd38d'>AGE</b>.")
# 6. г) BPI = PIN + INB + BNP
s = G + tri(T('P','I','N'), GOLD, 0.4) + tri(T('I','N','B'), BLUE, 0.4) + tri(T('B','N','P'), GREEN, 0.4)
s += line(PT['B'],PT['C'],BLUE,0.9,True) + line(PT['M'],PT['B'],GREEN,0.9,True) + line(PT['M'],PT['N'],GREEN,0.6,True)
s += at((3.5,2), '3x', 0, -1.4, GOLD) + at((10,1), '2x', 4.0, 1.0, BLUE) + at((7.5,0), '5x', 0, 4.0, GREEN)
s += at((5,3.3), '2x + OP', 8.0, 0.6, GOLD, 2.8)
s += names()
V['основание NP, высота BM'] = fig(svg(s, 'BPI на сетке'),
  "г) площадь BPI: <b style='color:#f0a83c'>PIN</b>, <b style='color:#5ba8f5'>INB</b> и <b style='color:#5fd38d'>BNP</b>.")
# 7. раздел «Найдём x»: AMNH
s = grid() + full() + tri(T('A','M','N','H'), RED, 0.35)
s += at((2.5,0), '5x', 0, 4.0, RED) + at((0,1), '2x', -4.0, 1.0, RED) + xmark() + names()
V['AMNH — прямоугольник со сторонами'] = fig(svg(s, 'AMNH на сетке'), 'Прямоугольник AMNH.')
# 8. раздел «Найдём OP»: FOP
s = grid() + full() + tri(T('F','O','P'), RED, 0.5)
s += at((3.5,4), '3x', 0, 4.0, RED) + at((5,4.45), 'OP', 4.6, 1.0, RED, 2.8) + xmark() + names()
V['FOP — прямоугольный треугольник с катетами'] = fig(svg(s, 'FOP на сетке'), 'Прямоугольный треугольник FOP.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
