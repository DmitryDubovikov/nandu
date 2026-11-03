import json, sys
# Рисунки к Т2′ провинциал 2023 №2. Координаты задачи — в см (y вверх), C = (0, 0); CD = 15, DE = 21, EF = 9, HI = 21.
# SVG: X = U·x, Y = U(30 − y).
U = 2
def xy(p): return round(U*p[0], 2), round(U*(30-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'C':(0,0),'D':(15,0),'E':(36,0),'B':(0,9),'J':(15,9),'I':(27,9),'F':(36,9),'H':(27,30),'G':(36,30),'A':(0,24)}
OFF = {'A':(-3.4,1.2),'B':(-3.4,1.2),'C':(-3.0,4.0),'D':(0,4.6),'E':(3.0,4.0),'F':(3.4,1.2),'I':(1.6,4.4),
       'J':(-1.4,-2.0),'H':(0,-2.2),'G':(3.0,-1.6)}
ALL = list(PT)
SEGS = [('A','B'),('B','C'),('C','E'),('D','J'),('B','F'),('F','E'),('F','G'),('G','H'),('H','I'),
        ('A','H'),('J','H'),('H','E'),('J','E')]

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
def full(col=DIM, w=0.45): return ''.join(line(PT[a],PT[b],col,w) for a,b in SEGS)
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def T(*n): return [PT[k] for k in n]
def seg(a, b, col, w=1.3): return line(PT[a], PT[b], col, w)
def svg(inner, label, vb='-8 -6 90 72'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def b(col, s): return f"<b style='color:{col}'>{s}</b>"

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['вместе составляют прямоугольник BCEF'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x, w, h
s = full()
for a,c in [('C','D'),('B','J'),('A','B')]: s += seg(a,c,GOLD)
for a,c in [('D','E'),('J','I'),('H','I')]: s += seg(a,c,BLUE)
for a,c in [('E','F'),('B','C'),('D','J')]: s += seg(a,c,GREEN)
s += line(PT['I'],PT['F'],GREEN,1.3)
# JF = w целиком: JI синим, IF зелёным; подпись JF = w выноской над BF
s += at((7.5,0), 'x', 0, 4.4, GOLD, 3.2) + at((7.5,9), 'x', 0, -1.4, GOLD, 3.2) + at((0,16.5), 'x', -3.0, 1.0, GOLD, 3.2)
s += at((25.5,0), 'w', 0, 4.4, BLUE, 3.2) + at((27,19.5), 'w', 2.6, 1.0, BLUE, 3.2)
s += at((36,4.5), 'h', 3.0, 1.0, GREEN, 3.2) + at((0,4.5), 'h', -3.0, 1.0, GREEN, 3.2) + at((31.5,9), 'h', 0, -1.4, GREEN, 3.2)
s += names()
V['h = EF = BC = JD = IF'] = fig(svg(s, 'Буквы'),
  f"{b(GOLD,'x')} = CD, {b(BLUE,'w')} = DE, {b(GREEN,'h')} = EF.")

# 3. а) BCEJ — трапеция
s = full() + tri(T('B','C','E','J'), GOLD, 0.35)
s += at((7.5,9), 'x', 0, -1.4, GOLD) + at((21,0), 'x + w', 0, 4.4, GOLD) + at((0,4.5), 'h', -3.0, 1.0, GOLD)
s += names()
V['BCEJ — прямоугольная трапеция'] = fig(svg(s, 'BCEJ'), "а) площадь BCEJ.")

# 4. б) EHJ = JHI + HEI + EJI
s = full() + tri(T('J','H','I'), GOLD, 0.4) + tri(T('H','E','I'), BLUE, 0.4) + tri(T('E','J','I'), GREEN, 0.4)
s += line(PT['I'],PT['E'],INK,0.7,True) + line(PT['I'],PT['F'],BLUE,0.9,True) + line(PT['F'],PT['E'],GREEN,0.9,True)
s += at((21,9), 'w − h', 0, -1.4, GOLD) + at((27,19.5), 'w', -2.6, 1.0, GOLD)
s += at((31.5,9), 'h', 0, -1.4, BLUE) + at((36,4.5), 'h', 3.0, 1.0, GREEN)
s += names()
V['HE пересекает JF между I и F'] = fig(svg(s, 'EHJ'),
  f"б) площадь EHJ: {b(GOLD,'JHI')}, {b(BLUE,'HEI')} и {b(GREEN,'EJI')}.")

# 5. в) ABJH = трапеция ABIH без JIH
s = full() + tri(T('A','B','J','H'), VIO, 0.35) + tri(T('J','I','H'), BLUE, 0.35) + poly(T('A','B','I','H'), GOLD, 1.0)
s += at((0,16.5), 'x', -3.0, 1.0, GOLD) + at((27,19.5), 'w', 2.6, 1.0, GOLD) + at((13.5,9), 'x + w − h', 0, 4.4, GOLD)
s += at((21,9), 'w − h', 0, -1.4, BLUE)
s += names()
V['это прямоугольная трапеция ABIH без'] = fig(svg(s, 'ABJH внутри ABIH'),
  f"в) площадь ABJH: {b(GOLD,'трапеция ABIH')} без {b(BLUE,'JIH')}.")

# 6–8. раздел «Найдём x, w и h»: три прямоугольника
def rect(n, lab_bottom, p_bottom, cap, key):
    s = full() + tri(T(*n), RED, 0.3)
    s += at(p_bottom, lab_bottom, 0, 4.4, RED) + at((PT[n[0]][0], 4.5), 'h', -3.0, 1.0, RED) + names()
    V[key] = fig(svg(s, cap), cap)
rect(('J','D','E','F'), 'w', (25.5,0), 'Прямоугольник DEFJ.', 'стороны DE = w и EF = h')
rect(('B','C','D','J'), 'x', (7.5,0), 'Прямоугольник BCDJ.', 'стороны CD = x и BC = h')
rect(('B','C','E','F'), 'x + w', (21,0), 'Прямоугольник BCEF.', 'стороны CE = x + w и BC = h')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
