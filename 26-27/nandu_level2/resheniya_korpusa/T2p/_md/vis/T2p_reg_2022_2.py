import json, sys
# Рисунки к Т2′ регионал 2022 №2. Координаты задачи — в сантиметрах (y вверх), F = (0, 0), C = (60, 0);
# G = (15, 0), H = (45, 0), E = (15, 36), D = (45, 36), A = (0, −27), B = (60, −27). SVG: X = U·x, Y = U·(36 − y).
U = 0.8
def xy(p): return round(U*p[0], 2), round(U*(36-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,-27),'B':(60,-27),'C':(60,0),'D':(45,36),'E':(15,36),'F':(0,0),'G':(15,0),'H':(45,0)}
OFF = {'A':(-2.6,3.4),'B':(2.6,3.4),'C':(3.0,-1.2),'D':(2.0,-1.6),'E':(-2.0,-1.6),'F':(-3.0,-1.2),
       'G':(-1.8,3.8),'H':(1.8,3.8)}

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.0):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=2.8):
    X, Y = xy(p); return txt(round(X+dx,2), round(Y+dy,2), s, col, size)
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.65' fill='{col}'/>"
    return out
VB = '-7 -6 62 62'
def svg(inner, label, vb=VB):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
SEG = [('A','B'),('B','C'),('C','F'),('F','A'),('F','E'),('E','D'),('D','C'),('E','G'),('D','H')]
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    return ''.join(line(PT[a],PT[b],col,w) for a,b in SEG)
ALL = list('ABCDEFGH')
def names(): return labels(ALL, MUT)
def xmark():   # кирпич x = FG, у F
    return line(PT['F'],PT['G'],GOLD,1.4) + at((7.5,0), 'x', 0, -1.4, GOLD, 3.0)
def tri(pts, col, op=0.45): return poly([PT[p] for p in pts], col, 0.9, col, op)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['F, G, H и C лежат на одной прямой.'] = fig(svg(s, 'Рисунок условия').replace("<svg ", "<svg style='max-width:440px' ", 1), 'Рисунок из условия.')

# 2. буквы: x = FG, h = EG = DH, наклонная CD = EF, AF = BC
s = full() + xmark()
s += line(PT['H'],PT['C'],GOLD,1.4) + at((52.5,0), 'x', 0, -1.4, GOLD, 3.0)
s += line(PT['G'],PT['H'],GOLD,0.9) + at((30,0), '2x', 0, -1.4)
s += line(PT['E'],PT['G'],BLUE,1.1) + at((15,18), 'h', 2.2, 1.0, BLUE, 3.0)
s += line(PT['D'],PT['H'],BLUE,1.1) + at((45,18), 'h', -2.2, 1.0, BLUE, 3.0)
s += line(PT['C'],PT['D'],RED,1.1) + at((52.5,18), 'CD', 3.6, 1.0, RED)
s += line(PT['F'],PT['E'],RED,1.1) + at((7.5,18), 'CD', -3.6, 1.0, RED)
s += line(PT['F'],PT['A'],GREEN,1.1) + at((0,-13.5), 'AF', -3.4, 1.0, GREEN)
s += line(PT['B'],PT['C'],GREEN,1.1) + at((60,-13.5), 'AF', 3.4, 1.0, GREEN)
s += names()
V['x = FG, h = EG = DH, наклонная CD = EF и AF = BC.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = FG = HC; GH = 2x. Неизвестны ещё <b style='color:#5ba8f5'>h</b>, <b style='color:#f2686c'>CD</b> и <b style='color:#5fd38d'>AF</b>.")

# 3–6. из каких фигур состоит каждое спрошенное
G = full()
# а) периметр CDEF
s = G + poly([PT['C'],PT['D'],PT['E'],PT['F']], GOLD, 1.2)
s += line(PT['C'],PT['D'],RED,1.2) + line(PT['F'],PT['E'],RED,1.2)
s += at((30,0), '4x', 0, 3.6) + at((30,36), '2x', 0, -1.6)
s += at((52.5,18), 'CD', 3.6, 1.0, RED) + at((7.5,18), 'CD', -3.6, 1.0, RED) + xmark() + names()
V['стороны CDEF — FC = 4x, DE = 2x'] = fig(svg(s, 'Контур CDEF'),
  "а) периметр <b style='color:#f0a83c'>CDEF</b>; наклонные <b style='color:#f2686c'>CD = EF</b>.")
# б) периметр ABCDEF
s = G + poly([PT['A'],PT['B'],PT['C'],PT['D'],PT['E'],PT['F']], GOLD, 1.2)
s += line(PT['C'],PT['D'],RED,1.2) + line(PT['F'],PT['E'],RED,1.2)
s += line(PT['F'],PT['A'],GREEN,1.2) + line(PT['B'],PT['C'],GREEN,1.2)
s += at((30,-27), '4x', 0, 3.6) + at((30,36), '2x', 0, -1.6)
s += at((52.5,18), 'CD', 3.6, 1.0, RED) + at((7.5,18), 'CD', -3.6, 1.0, RED)
s += at((0,-13.5), 'AF', -3.4, 1.0, GREEN) + at((60,-13.5), 'AF', 3.4, 1.0, GREEN) + xmark() + names()
V['две стороны BC = AF прямоугольника ABCF'] = fig(svg(s, 'Контур ABCDEF'),
  "б) периметр <b style='color:#f0a83c'>ABCDEF</b>.")
# в) площадь DEFH — трапеция
s = G + poly([PT['D'],PT['E'],PT['F'],PT['H']], GOLD, 1.0, GOLD, 0.4)
s += at((30,36), '2x', 0, -1.6) + at((22.5,0), '3x', 0, 3.6) + at((15,18), 'h', 2.2, 1.0, BLUE, 3.0)
s += line(PT['E'],PT['G'],BLUE,1.1) + xmark() + names()
V['DEFH — трапеция с основаниями DE = 2x'] = fig(svg(s, 'Трапеция DEFH'),
  "в) площадь трапеции DEFH; высота <b style='color:#5ba8f5'>EG = h</b>.")
# г) площадь BDE — основание DE, высота от B до прямой ED
s = G + tri('BDE', VIO, 0.45)
s += line((45,36),(60,36),VIO,0.6,True) + line(PT['B'],(60,36),VIO,0.9,True)
s += at((30,36), '2x', 0, -1.6)
s += at((60,-13.5), 'AF', 4.4, 1.0, GREEN) + at((60,18), 'h', 3.0, 1.0, BLUE, 3.0)
s += xmark() + names()
V['высота идёт от B вверх через C'] = fig(svg(s, 'Треугольник BDE'),
  "г) площадь <b style='color:#c58af9'>BDE</b>; высота к ED — пунктир от B до продолжения ED, она равна AF + h.")

# 7. раздел «Найдём …»: склейка DEGH и CDH по DH дают CDEG
s = full() + poly([PT['D'],PT['E'],PT['G'],PT['H']], GOLD, 1.0, GOLD, 0.3) + tri('CDH', BLUE, 0.35)
s += line(PT['D'],PT['H'],RED,1.4) + at((45,18), 'h', -2.4, 1.0, RED, 3.0)
s += at((30,18), '132', 0, 1.0, LAB, 3.2) + at((50,9), '90', 0, 1.0, LAB, 3.0)
s += names()
V['склеенные по DH = h, дают CDEG (150)'] = fig(svg(s, 'Склейка DEGH и CDH'),
  "<b style='color:#f0a83c'>DEGH</b> и <b style='color:#5ba8f5'>CDH</b>, склеенные по <b style='color:#f2686c'>DH</b>, дают CDEG; DH есть в обоих обходах.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
