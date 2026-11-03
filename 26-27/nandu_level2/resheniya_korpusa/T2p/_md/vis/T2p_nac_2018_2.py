import json, sys
# Рисунки к Т2′ национал 2018 день I №2. Координаты задачи — в сантиметрах (y вверх), A = (0, 0), D = (87, 0);
# M = (15, 0), P = (36, 0), R = (51, 0), S = (72, 0), B = (36, −15), C = (51, −15), F = (15, 36), E = (72, 36).
# SVG: X = U·x, Y = U·(36 − y).
U = 0.7
def xy(p): return round(U*p[0], 2), round(U*(36-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'M':(15,0),'P':(36,0),'R':(51,0),'S':(72,0),'D':(87,0),
      'B':(36,-15),'C':(51,-15),'F':(15,36),'E':(72,36)}
OFF = {'A':(-2.8,1.0),'D':(2.8,1.0),'M':(-2.0,-1.4),'P':(-2.0,-1.4),'R':(2.0,-1.4),'S':(2.0,-1.4),
       'B':(-1.4,3.6),'C':(1.4,3.6),'F':(-2.0,-1.6),'E':(2.0,-1.6)}

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.0):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=2.6):
    X, Y = xy(p); return txt(round(X+dx,2), round(Y+dy,2), s, col, size)
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.6' fill='{col}'/>"
    return out
VB = '-6 -5 73 45'
def svg(inner, label, vb=VB):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
SEG = [('A','B'),('B','C'),('C','D'),('D','E'),('E','F'),('F','A'),('A','D'),('M','F'),('S','E'),('B','P'),('C','R')]
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    return ''.join(line(PT[a],PT[b],col,w) for a,b in SEG)
ALL = list('AMPRSDBCFE')
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly([PT[p] for p in pts], col, 0.9, col, op)
def mid(a, b): return ((PT[a][0]+PT[b][0])/2, (PT[a][1]+PT[b][1])/2)
def xmark():   # короткий катет x = BP — у квадрата, слева
    return line(PT['B'],PT['P'],GOLD,1.4) + at(mid('B','P'), 'x', -2.0, 1.0, GOLD, 2.8)
def hmark():   # длинный катет h = MF
    return line(PT['M'],PT['F'],BLUE,1.2) + at(mid('M','F'), 'h', 2.0, 1.0, BLUE, 2.8)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['точки A, M, P, R, S и D лежат на одной прямой.'] = fig(svg(s, 'Рисунок условия').replace("<svg ", "<svg style='max-width:480px' ", 1), 'Рисунок из условия.')

# 2. буквы: x — короткие катеты, h — длинные, AB — гипотенузы
s = full()
for a,b in [('A','M'),('P','R'),('S','D'),('B','C'),('C','R')]:
    s += line(PT[a],PT[b],GOLD,1.2)
for a,b in [('A','P'),('R','D'),('S','E')]:
    s += line(PT[a],PT[b],BLUE,1.0)
for a,b in [('A','B'),('C','D'),('D','E'),('A','F')]:
    s += line(PT[a],PT[b],RED,1.0)
s += xmark() + hmark()
s += at(mid('A','M'), 'x', 0, -1.2) + at(mid('P','R'), 'x', 0, -1.2) + at(mid('S','D'), 'x', 0, -1.2)
s += at(mid('A','P'), 'h', 0, 3.4, BLUE) + at(mid('R','D'), 'h', 0, 3.4, BLUE) + at(mid('S','E'), 'h', -2.0, 1.0, BLUE)
s += at(mid('A','B'), 'AB', -2.0, 3.0, RED) + at(mid('A','F'), 'AB', -3.4, 1.0, RED)
s += at(mid('C','D'), 'AB', 2.0, 3.0, RED) + at(mid('D','E'), 'AB', 3.4, 1.0, RED)
s += names()
V['Тогда AM = PR = BC = SD = x'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> — короткие катеты и сторона квадрата, <b style='color:#5ba8f5'>h</b> — длинные катеты, <b style='color:#f2686c'>AB</b> — гипотенузы.")

# 3–6. из каких фигур состоит каждое спрошенное
G = full()
# а) CDER = CDR + RDE
s = G + tri('CDR', BLUE, 0.4) + tri('RDE', GREEN, 0.4) + line(PT['S'],PT['E'],GREEN,1.0,True)
s += at(mid('R','D'), 'h', 0, 3.4, GREEN) + at(mid('S','E'), 'h', -2.0, 1.0, GREEN)
s += at(mid('C','R'), 'x', -2.0, 1.0, BLUE) + xmark() + names()
V['разрежем по RD'] = fig(svg(s, 'CDER = CDR + RDE'),
  "а) площадь CDER: <b style='color:#5ba8f5'>CDR</b> и <b style='color:#5fd38d'>RDE</b>; высота RDE — ES.")
# б) AREF — трапеция
s = G + poly([PT['A'],PT['R'],PT['E'],PT['F']], GOLD, 1.0, GOLD, 0.35)
s += at(mid('F','E'), '2h − x', 0, -1.4) + at(mid('A','R'), 'h + x', 0, 3.4) + hmark() + xmark() + names()
V['AREF — трапеция с основаниями'] = fig(svg(s, 'Трапеция AREF'),
  "б) площадь трапеции AREF; высота <b style='color:#5ba8f5'>MF = h</b>.")
# в) ABCEF = AREF + ABP + PBCR + RCE
s = G + poly([PT['A'],PT['R'],PT['E'],PT['F']], GOLD, 0.8, GOLD, 0.3) + tri('ABP', BLUE, 0.4)
s += poly([PT['P'],PT['B'],PT['C'],PT['R']], VIO, 0.8, VIO, 0.4) + tri('RCE', GREEN, 0.45)
s += line(PT['R'],PT['S'],GREEN,1.0,True) + at(mid('R','S'), 'h − x', 0, 3.4, GREEN)
s += at(mid('C','R'), 'x', -2.2, 1.0, GREEN) + xmark() + names()
V['разрежем по AR и RE'] = fig(svg(s, 'ABCEF по кускам'),
  "в) площадь ABCEF: <b style='color:#f0a83c'>AREF</b>, <b style='color:#5ba8f5'>ABP</b>, <b style='color:#c58af9'>PBCR</b> и <b style='color:#5fd38d'>RCE</b>; высота RCE — RS.")
# г) вся фигура
s = G + poly([PT['M'],PT['S'],PT['E'],PT['F']], GOLD, 0.8, GOLD, 0.3)
s += poly([PT['P'],PT['B'],PT['C'],PT['R']], VIO, 0.8, VIO, 0.4)
for t in ['AMF','ABP','CDR','SDE']: s += tri(t, BLUE, 0.4)
s += at(mid('F','E'), '2h − x', 0, -1.4) + hmark() + xmark() + names()
V['фигура — прямоугольник MSEF со сторонами'] = fig(svg(s, 'Вся фигура'),
  "г) площадь фигуры: <b style='color:#f0a83c'>MSEF</b>, <b style='color:#c58af9'>PBCR</b> и четыре равных <b style='color:#5ba8f5'>треугольника</b>.")

# 7. раздел «Найдём x и h»: обход всей фигуры
s = full() + poly([PT[p] for p in 'ABCDEF'], GOLD, 1.2)
for a,b in [('A','B'),('C','D'),('D','E'),('A','F')]:
    s += line(PT[a],PT[b],RED,1.2)
s += at(mid('A','B'), 'AB', -2.0, 3.0, RED) + at(mid('A','F'), 'AB', -3.4, 1.0, RED)
s += at(mid('C','D'), 'AB', 2.0, 3.0, RED) + at(mid('D','E'), 'AB', 3.4, 1.0, RED)
s += at(mid('B','C'), 'x', 0, 3.4) + at(mid('F','E'), '2h − x', 0, -1.4) + names()
V['обход A → B → C → D → E → F → A'] = fig(svg(s, 'Контур фигуры'),
  "Периметр фигуры: четыре <b style='color:#f2686c'>гипотенузы</b>, BC и EF; AD, MF, SE, BP и CR — внутри.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
