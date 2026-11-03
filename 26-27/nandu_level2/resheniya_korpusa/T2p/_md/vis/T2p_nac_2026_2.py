import json, sys
# Рисунки к Т2′ национал 2026 день I №2. Схема чертежа условия (не в масштабе: ответов два), y вверх,
# A = (0, 0), сторона ABCD 20: AE = 10, AH = 9, x = 4, GC = 6, CF = 15.
# SVG: X = U·x, Y = U·(20 − y).
U = 3
def xy(p): return U*p[0], U*(20-p[1])
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(20,0),'C':(20,20),'D':(0,20),'E':(10,0),'H':(0,9),'L':(10,9),'I':(10,5),
      'K':(14,9),'J':(14,5),'F':(20,5),'G':(14,20)}
OFF = {'A':(-3.2,4.4),'B':(3.2,4.4),'C':(3.2,-1.6),'D':(-3.2,-1.6),'E':(-2.8,4.4),'H':(-3.6,1.2),
       'L':(-2.6,-1.6),'I':(-2.6,4.2),'K':(2.8,-1.6),'J':(2.8,4.2),'F':(3.4,1.2),'G':(0,-2.4)}

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
def svg(inner, label, vb='-10 -8 82 80'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:440px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
ALL = list(PT)
P_ = PT
def full(col=DIM, w=0.45):   # весь чертёж условия: квадрат и разрезы
    return (poly([P_['A'],P_['B'],P_['C'],P_['D']], col, w) + line(P_['E'],P_['L'],col,w) + line(P_['H'],P_['K'],col,w)
            + line(P_['G'],P_['J'],col,w) + line(P_['I'],P_['F'],col,w))
def names(): return labels(ALL, MUT)
def rect(a, b, c, d, col, op=0.35, w=1.0): return poly([P_[a],P_[b],P_[c],P_[d]], col, w, col, op)
def xmark():   # x — нижняя сторона IJ квадрата IJKL
    return line(P_['I'],P_['J'],GOLD,1.4) + at((12,5), 'x', 0, 4.0, GOLD, 3.2)
def given():   # данные прямоугольники с площадями
    return (rect('A','E','L','H', GOLD, 0.22, 0.6) + at((5,4.5), '48', 0, 1.2, GOLD, 3.6)
            + rect('J','F','C','G', BLUE, 0.22, 0.6) + at((17,12.5), '133', 0, 1.2, BLUE, 3.6))
def brace_h(x1, x2, y, s, col, dy=4.2):   # размер вдоль горизонтали ниже чертежа
    return (line((x1,y),(x2,y),col,0.6) + line((x1,y+0.4),(x1,y-0.4),col,0.6) + line((x2,y+0.4),(x2,y-0.4),col,0.6)
            + at(((x1+x2)/2,y), s, 0, dy, col, 3.0))
def brace_v(y1, y2, x, s, col, dx=-1.2):   # размер вдоль вертикали левее чертежа
    return (line((x,y1),(x,y2),col,0.6) + line((x-0.4,y1),(x+0.4,y1),col,0.6) + line((x-0.4,y2),(x+0.4,y2),col,0.6)
            + f"<text x='{U*x+dx}' y='{U*(20-(y1+y2)/2)+1.0}' fill='{col}' font-size='3.0' text-anchor='end' font-weight='600'>{s}</text>")

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['E, I, L лежат на одной прямой'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x и данные прямоугольники
s = full() + given() + xmark() + names()
V['x — сторона квадрата IJKL.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> — сторона IJKL; площади <b style='color:#f0a83c'>AELH</b> и <b style='color:#5ba8f5'>JFCG</b> даны.")

# 3. а) IJKL
s = full() + rect('I','J','K','L', VIO, 0.45) + xmark() + at((14,7), 'x', 2.4, 1.0, VIO, 3.2) + names()
V['IJKL — квадрат со стороной x.'] = fig(svg(s, 'IJKL'), 'а) площадь IJKL')

# 4. б) сторона AB = AE + x + GC
s = full() + poly([P_['A'],P_['B'],P_['C'],P_['D']], INK, 0.7)
s += line(P_['A'],P_['E'],GOLD,1.4) + line(P_['I'],P_['J'],VIO,1.4) + line(P_['J'],P_['F'],BLUE,1.4)
s += line((10,0),(10,-2.4),MUT,0.35,True) + line((14,5),(14,-2.4),MUT,0.35,True) + line((20,0),(20,-2.4),MUT,0.35,True)
s += brace_h(0,10,-2.4,'AE',GOLD) + brace_h(10,14,-2.4,'x',VIO) + brace_h(14,20,-2.4,'GC',BLUE)
s += names()
V['AB складывается из AE и EB'] = fig(svg(s, 'Сторона AB', '-10 -8 82 86'), 'б) площадь ABCD')

# 5. в) HKGD: HK = AE + x, HD = KG = CF − x
s = full() + rect('H','K','G','D', GREEN, 0.3)
s += line(P_['H'],P_['L'],GOLD,1.4) + line(P_['L'],P_['K'],VIO,1.4) + line(P_['K'],P_['G'],GREEN,1.4)
s += line(P_['J'],P_['K'],VIO,1.4) + line(P_['C'],P_['F'],BLUE,1.4)
s += at((5,9), 'AE', 0, -1.4, GOLD) + at((12,9), 'x', 0, -1.4, VIO) + at((14,7), 'x', 2.4, 1.0, VIO)
s += at((14,14.5), 'CF − x', -6.0, 1.0, GREEN) + at((20,12.5), 'CF', 4.2, 1.0, BLUE)
s += names()
V['HK складывается из HL = AE'] = fig(svg(s, 'HKGD'), 'в) периметр HKGD')

# 6. раздел «Найдём x»: AB = AD
s = full() + poly([P_['A'],P_['B'],P_['C'],P_['D']], INK, 0.7)
s += line((10,0),(10,-2.4),MUT,0.35,True) + line((14,5),(14,-2.4),MUT,0.35,True) + line((20,0),(20,-2.4),MUT,0.35,True)
s += brace_h(0,10,-2.4,'AE',GOLD) + brace_h(10,14,-2.4,'x',VIO) + brace_h(14,20,-2.4,'GC',BLUE)
s += line((0,9),(-2.4,9),MUT,0.35,True) + line((0,0),(-2.4,0),MUT,0.35,True) + line((0,20),(-2.4,20),MUT,0.35,True)
s += brace_v(0,9,-2.4,'AH',GOLD) + brace_v(9,20,-2.4,'CF − x',GREEN)
s += names()
V['AD — из AH и HD = CF − x'] = fig(svg(s, 'AB = AD', '-24 -8 96 86'),
  "Сторона квадрата ABCD по низу и по левому краю.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
