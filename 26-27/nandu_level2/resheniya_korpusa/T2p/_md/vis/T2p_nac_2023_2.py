import json, sys
# Рисунки к Т2′ национал 2023 день I №2. Координаты задачи — в см (y вверх): A = (0, 0), D = (74, 0), B = (0, −24), F = (32, 24).
# SVG: X = x, Y = 26 − y. Сетки нет: длины AD, AG, HD через сторону квадрата x не выражаются.
def xy(p): return round(p[0], 2), round(26 - p[1], 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'G':(32,0),'H':(56,0),'D':(74,0),'F':(32,24),'E':(56,24),'B':(0,-24),'C':(74,-24)}
OFF = {'A':(-3.4,1.2),'G':(-3.0,-1.6),'H':(3.0,-1.6),'D':(3.4,1.2),'F':(-1.6,-2.0),'E':(1.6,-2.0),
       'B':(-3.0,4.0),'C':(3.0,4.0)}
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
def svg(inner, label, vb='-8 -3 90 60'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def full(col=DIM, w=0.45):   # весь чертёж условия: ABCD, AD, квадрат EFGH, AF и ED
    P_ = PT
    s = poly([P_['A'],P_['B'],P_['C'],P_['D']], col, w)
    s += line(P_['A'],P_['F'],col,w) + line(P_['F'],P_['E'],col,w) + line(P_['E'],P_['D'],col,w)
    s += line(P_['F'],P_['G'],col,w) + line(P_['E'],P_['H'],col,w)
    return s
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def T(*n): return [PT[k] for k in n]
def xmark():   # x — сторона квадрата, на FG
    return line(PT['G'],PT['F'],GOLD,1.4) + at((32,12), 'x', 2.4, 1.0, GOLD, 3.2)
def dimAD(lab='AD'):   # размер AD выноской ниже BC
    return (line((0,-29),(74,-29),GOLD,0.5) + line((0,-28),(0,-30),GOLD,0.5) + line((74,-28),(74,-30),GOLD,0.5)
            + at((37,-29), lab, 0, 4.0))
VB2 = '-8 -3 90 66'   # с выноской под BC

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['а меньшая сторона на чертеже — AB'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x — сторона квадрата, AB = DC = x
s = full() + xmark() + line(PT['A'],PT['B'],GOLD,1.0) + at((0,-12), 'x', -3.2, 1.0, GOLD, 3.2)
s += line(PT['D'],PT['C'],GOLD,1.0) + at((74,-12), 'x', 3.2, 1.0, GOLD, 3.2)
s += line(PT['G'],PT['H'],GOLD,1.0) + at((44,0), 'x', 0, -1.4, GOLD, 3.2) + names()
V['x — сторона квадрата EFGH; AB = DC = x.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> — сторона квадрата EFGH; AB = DC = x.")

# 3. а) BCHG — трапеция
s = full() + tri(T('B','C','H','G'), GOLD, 0.35) + line(PT['A'],PT['B'],GOLD,0.9,True)
s += at((44,0), 'x', 0, -1.4) + at((0,-12), 'x', -3.2, 1.0) + dimAD('BC = AD') + xmark() + names()
V['BCHG — трапеция с основаниями'] = fig(svg(s, 'BCHG — трапеция', VB2),
  "а) площадь BCHG: трапеция, основания BC = AD и GH = x, высота AB = x.")

# 4. б) BFH = BFG + FGH + BGH
s = full() + tri(T('B','F','G'), BLUE, 0.4) + tri(T('F','G','H'), GOLD, 0.4) + tri(T('B','G','H'), GREEN, 0.4)
s += line((0,0),(32,0),BLUE,1.0,True) + at((8,0), 'AG', 0, -1.4, BLUE) + line(PT['A'],PT['B'],GREEN,0.9,True)
s += at((0,-12), 'x', -3.2, 1.0, GREEN) + at((44,0), 'x', 0, 4.2) + xmark() + names()
V['G внутри BFH.'] = fig(svg(s, 'BFH из трёх треугольников'),
  "б) площадь BFH: <b style='color:#5ba8f5'>BFG</b> (высота AG), <b style='color:#f0a83c'>FGH</b> и <b style='color:#5fd38d'>BGH</b> (высота AB).")

# 5. в) ABCDEF = ABCD + AFG + EFGH + HED
s = full() + tri(T('A','B','C','D'), GOLD, 0.3) + tri(T('A','F','G'), BLUE, 0.45) + tri(T('F','E','H','G'), VIO, 0.4)
s += tri(T('H','E','D'), GREEN, 0.45) + at((44,24), 'x', 0, -1.4, VIO) + at((65,0), 'HD', 0, 4.2, GREEN)
s += at((16,0), 'AG', 0, 4.2, BLUE) + dimAD() + at((0,-12), 'x', -3.2, 1.0) + names()
V['треугольник AFG, квадрат EFGH и треугольник HED'] = fig(svg(s, 'ABCDEF из четырёх частей', VB2),
  "в) площадь ABCDEF: <b style='color:#f0a83c'>ABCD</b>, <b style='color:#5ba8f5'>AFG</b>, <b style='color:#c58af9'>EFGH</b> и <b style='color:#5fd38d'>HED</b>.")

# 6. г) ACF = AFG + FGC + AGC
s = full() + tri(T('A','F','G'), BLUE, 0.45) + tri(T('F','G','C'), GOLD, 0.4) + tri(T('A','G','C'), GREEN, 0.4)
s += line((32,0),(74,0),GOLD,1.0,True) + at((66,0), 'GD', 0, -1.4, GOLD) + line(PT['D'],PT['C'],GREEN,0.9,True)
s += at((74,-12), 'x', 3.2, 1.0, GREEN) + at((16,0), 'AG', 0, -1.4, BLUE) + xmark() + names()
V['G внутри ACF.'] = fig(svg(s, 'ACF из трёх треугольников'),
  "г) площадь ACF: <b style='color:#5ba8f5'>AFG</b>, <b style='color:#f0a83c'>FGC</b> (высота GD) и <b style='color:#5fd38d'>AGC</b> (высота DC).")

# 7. раздел «Найдём x»: квадрат EFGH
s = full() + tri(T('F','E','H','G'), RED, 0.4) + xmark() + names()
V['EFGH — квадрат со стороной x.'] = fig(svg(s, 'Квадрат EFGH'), 'Квадрат EFGH, площадь 576.')
# 8. раздел «Найдём AD»: контур ABCD
s = full() + poly(T('A','B','C','D'), RED, 1.2) + at((0,-12), 'x', -3.2, 1.0, RED) + dimAD() + names()
V['ABCD — прямоугольник со сторонами AD и AB = x.'] = fig(svg(s, 'Контур ABCD', VB2), 'Прямоугольник ABCD, периметр 196.')
# 9. раздел «Найдём AG»: AFG
s = full() + tri(T('A','F','G'), RED, 0.45) + at((16,0), 'AG', 0, 4.2, RED) + xmark() + names()
V['AFG — прямоугольный треугольник с катетами'] = fig(svg(s, 'Треугольник AFG'), 'Прямоугольный треугольник AFG, площадь 384.')
# 10. раздел «Найдём HD»: AD = AG + GH + HD
s = full() + line((0,0),(32,0),BLUE,1.4) + line((32,0),(56,0),GOLD,1.4) + line((56,0),(74,0),GREEN,1.4)
s += at((16,0), 'AG', 0, 4.2, BLUE) + at((44,0), 'x', 0, 4.2) + at((65,0), 'HD', 0, 4.2, GREEN) + dimAD() + names()
V['AD складывается из AG, GH = x и HD.'] = fig(svg(s, 'AD из трёх отрезков', VB2),
  "AD = <b style='color:#5ba8f5'>AG</b> + <b style='color:#f0a83c'>x</b> + <b style='color:#5fd38d'>HD</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
