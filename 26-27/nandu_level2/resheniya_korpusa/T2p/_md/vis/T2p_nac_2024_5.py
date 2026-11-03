import json, sys
# Рисунки к Т2′ национал 2024 день II №5. Координаты задачи — в сантиметрах (y вверх), A = (0, 0), C = (45, 60).
# SVG: X = K · x, Y = K · (60 − y).
K = 1.2
def xy(p): return round(K*p[0], 2), round(K*(60-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO,TEAL='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9','#4fd1c5'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(45,0),'C':(45,60),'D':(0,60),'M':(18,0),'N':(27,0),'P':(45,40),'Q':(30,60),'R':(0,45)}
OFF = {'A':(-3.2,4.4),'B':(3.4,4.4),'C':(3.4,-1.6),'D':(-3.4,-1.6),'M':(0,4.6),'N':(0,4.6),'P':(3.8,1.2),
       'Q':(0,-2.4),'R':(-3.8,1.2)}

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
def labels(names, col=LAB, dots=True):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col)
        if dots: out += f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def svg(inner, label, vb='-11 -7 78 88', mw=None):
    st = f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
ALL = ['A','B','C','D','M','N','P','Q','R']
def full(col=DIM, w=0.45):   # весь чертёж условия — фон каждого рисунка
    P_ = PT
    s = poly([P_['A'],P_['B'],P_['C'],P_['D']], col, w)
    for a, b in [('R','Q'),('Q','P'),('R','P'),('R','M'),('P','N')]:
        s += line(P_[a], P_[b], col, w)
    return s
def names(): return labels(ALL, MUT)
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x = 15 см
    return (''.join(line((X,0),(X,60),col,w) for X in (15,30)) +
            ''.join(line((0,Y),(45,Y),col,w) for Y in (15,30,45)))
def xmark():   # кирпич x — треть AB, у A, выноской под AB
    return line((0,-6),(15,-6),GOLD,1.4) + at((7.5,-6), 'x', 0, 4.0, GOLD, 3.2)
def dimAB(lab='3x'):
    return line((0,-6),(45,-6),GOLD,0.5) + line((0,-5),(0,-7),GOLD,0.5) + line((45,-5),(45,-7),GOLD,0.5) + at((30,-6), lab, 0, 4.0)
def dimBC(lab='4x'):
    return line((51,0),(51,60),GOLD,0.5) + line((50,0),(52,0),GOLD,0.5) + line((50,60),(52,60),GOLD,0.5) + at((51,30), lab, 4.4, 1.0)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['AB : BC = 3 : 4.'] = fig(svg(s, 'Рисунок условия', '-9 -6 72 86', 340), 'Рисунок из условия.')

# 2. буквы: сетка x, AB = 3x, BC = 4x
s = grid() + full() + dimAB() + xmark() + dimBC() + names()
V['сетка с шагом x.'] = fig(svg(s, 'Буквы', '-9 -6 78 92', 360), "<b style='color:#f0a83c'>x</b> = AB : 3; стороны AB и BC — целые кирпичи.")

# 3–6. что такое каждое спрошенное
G = full()
s = G + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 1.2) + dimAB() + xmark() + dimBC() + names()
V['ABCD — прямоугольник со сторонами AB = 3x и BC = 4x.'] = fig(svg(s, 'Периметр ABCD', '-9 -6 78 92'), 'а) периметр ABCD')

CORN = {'AMR':(['A','M','R'],BLUE), 'NBP':(['N','B','P'],GREEN), 'PCQ':(['P','C','Q'],RED), 'QDR':(['Q','D','R'],TEAL)}
def corner(n): pts, col = CORN[n]; return tri([PT[p] for p in pts], col, 0.35)
s = G + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 2.4)
s += poly([PT[p] for p in 'MNPQR'], VIO, 1.0, VIO, 0.35) + ''.join(corner(n) for n in CORN) + names()
V['это ABCD без четырёх прямоугольных треугольников'] = fig(svg(s, 'MNPQR внутри ABCD'),
  "б) площадь MNPQR: <b style='color:#f0a83c'>ABCD</b> без <b style='color:#5ba8f5'>AMR</b>, <b style='color:#5fd38d'>NBP</b>, "
  "<b style='color:#f2686c'>PCQ</b> и <b style='color:#4fd1c5'>QDR</b>.")

s = G + poly([PT['R'],PT['P'],PT['C'],PT['D']], GOLD, 2.4)
s += poly([PT[p] for p in 'PQR'], VIO, 1.0, VIO, 0.35) + corner('PCQ') + corner('QDR') + names()
V['это трапеция RPCD без'] = fig(svg(s, 'PQR внутри трапеции RPCD'),
  "в) площадь PQR: <b style='color:#f0a83c'>трапеция RPCD</b> без <b style='color:#f2686c'>PCQ</b> и <b style='color:#4fd1c5'>QDR</b>; основания DR и PC, высота CD.")

s = G + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 2.4)
s += tri([PT[p] for p in 'AMQD'], BLUE, 0.35) + corner('NBP')
s += poly([PT[p] for p in 'MNPCQ'], VIO, 1.0, VIO, 0.35) + line(PT['M'], PT['Q'], VIO, 1.0, True) + names()
V['это ABCD без трапеции AMQD'] = fig(svg(s, 'MNPCQ внутри ABCD'),
  "г) площадь MNPCQ: <b style='color:#f0a83c'>ABCD</b> без <b style='color:#5ba8f5'>трапеции AMQD</b> и <b style='color:#5fd38d'>NBP</b>; основания AM и DQ, высота AD.")

# 7. раздел 2: отрезки на сторонах в сантиметрах
s = full(INK, 0.5)
for a, b, lab, dx, dy in [((0,0),(18,0),'18',0,9.2), ((18,0),(27,0),'9',0,9.2), ((27,0),(45,0),'18',0,9.2),
                          ((45,0),(45,40),'40',4.6,1.0), ((45,40),(45,60),'20',4.6,1.0),
                          ((0,60),(30,60),'30',0,-2.2), ((30,60),(45,60),'15',0,-2.2),
                          ((0,0),(0,45),'45',-4.6,1.0), ((0,45),(0,60),'15',-4.6,1.0)]:
    s += line(a, b, GOLD, 1.0) + at(((a[0]+b[0])/2, (a[1]+b[1])/2), lab, dx, dy, GOLD, 3.0)
s += labels(ALL, MUT)
V['DR = AD − AR = 60 − 45 = 15'] = fig(svg(s, 'Отрезки на сторонах', '-12 -7 80 92', 380), 'Отрезки на сторонах ABCD, см.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
