import json, sys
# Рисунки к Т2′ регионал 2019 №2. Координаты задачи — в кирпичах x = 8 см (y вверх), A = (0, 0), C = (4, 4),
# O = (2, 1), S = (2, 4 + 30/8). SVG: X = U·x, Y = U·(7.75 − y).
U = 10
SY = 4 + 30/8
def xy(p): return round(U*p[0], 2), round(U*(SY-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(4,0),'C':(4,4),'D':(0,4),'M':(0,2),'P':(4,2),'R':(2,4),'O':(2,1),'S':(2,SY)}
OFF = {'A':(-3.0,4.2),'B':(3.0,4.2),'C':(3.2,-1.4),'D':(-3.2,-1.4),'M':(-3.4,1.2),'P':(3.4,1.2),
       'R':(2.6,-1.6),'O':(2.2,-2.6),'S':(0,-2.4)}

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
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x внутри квадрата ABCD
    return ''.join(line((i,0),(i,4),col,w) for i in range(5)) + ''.join(line((0,j),(4,j),col,w) for j in range(5))
VB = '-9 -7 58 98'
def svg(inner, label, vb=VB, mw=None):
    st = f" style='max-width:{mw}px'" if mw else ''
    return f"<svg{st} viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
SEG = [('A','B'),('B','C'),('C','D'),('D','A'),('D','S'),('S','C'),('S','R'),('A','R'),('R','B'),('A','P'),('B','M')]
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    return ''.join(line(PT[a],PT[b],col,w) for a,b in SEG)
ALL = list('ABCDMPROS')
def names(): return labels(ALL, MUT)
def xmark():   # кирпич x — четверть AB, у B снизу
    return line((3,0),(4,0),GOLD,1.4) + at((3.5,0), 'x', 0, 4.4, GOLD, 3.2)
def tri(pts, col, op=0.45): return poly([PT[p] for p in pts], col, 1.0, col, op)
SH = ['A','O','B','R']   # закрашенная часть

V = {}
# 1. рисунок условия
s = poly([PT[p] for p in SH], VIO, 0.0, VIO, 0.35) + full(INK, 0.55) + labels(ALL)
V['по чертежу M — середина AD'] = fig(svg(s, 'Рисунок условия', mw=320), 'Рисунок из условия.')

# 2. буквы: сетка с шагом x, O — центр прямоугольника ABPM
s = grid() + full() + poly([PT['A'],PT['B'],PT['P'],PT['M']], GOLD, 0.9)
s += line(PT['B'],PT['C'],GOLD,1.0) + at((4,3), '4x', 4.2, 1.0)
s += line((2,0),(2,1),BLUE,1.0,True) + at((2,0.5), 'x', -2.4, 1.0, BLUE, 3.0)
s += xmark() + names()
V['неизвестных длин три: x, RS и CS'] = fig(svg(s, 'Буквы', mw=320),
  "Сетка с шагом <b style='color:#f0a83c'>x</b> и прямоугольник <b style='color:#f0a83c'>ABPM</b>.")

# 3–6. из каких фигур состоит каждое спрошенное
G = grid() + full()
# а) периметр CSD
s = G + poly([PT['C'],PT['S'],PT['D']], GOLD, 1.2)
s += at((1,SY-(SY-4)/2), 'CS', -4.2, 1.0, RED) + at((3,SY-(SY-4)/2), 'CS', 4.2, 1.0, RED)
s += at((1,4), '4x', 0, -1.6) + xmark() + names()
V['DC = 4x, CS и SD = CS'] = fig(svg(s, 'Контур CSD'), "а) периметр <b style='color:#f0a83c'>CSD</b>.")
# б) площадь BCSR = BCR + RCS
s = G + tri(['B','C','R'], BLUE, 0.4) + tri(['R','C','S'], GREEN, 0.4)
s += at((4,1), '4x', 4.2, 1.0, BLUE) + at((3,4), '2x', 0, 4.4, LAB)
s += at((2,(4+SY)/2), 'RS', -4.0, 1.0, GREEN) + xmark() + names()
V['BCR с катетами BC = 4x и CR = 2x'] = fig(svg(s, 'BCSR = BCR + RCS'),
  "б) площадь BCSR: <b style='color:#5ba8f5'>BCR</b> и <b style='color:#5fd38d'>RCS</b>.")
# в) площадь закрашенной части = ARB без AOB
s = G + tri(['A','R','B'], GOLD, 0.15) + poly([PT[p] for p in SH], VIO, 1.0, VIO, 0.45) + tri(['A','O','B'], BLUE, 0.35)
s += line((2,0),(2,4),GOLD,0.8,True) + at((2,2.6), '4x', -4.0, 1.0)
s += at((2,0.5), 'x', 2.6, 1.0, BLUE, 3.0) + at((1,0), '4x', 0, 4.4) + xmark() + names()
V['общее основание AB = 4x'] = fig(svg(s, 'ARBO = ARB без AOB'),
  "в) площадь закрашенной части <b style='color:#c58af9'>ARBO</b> = <b style='color:#f0a83c'>ARB</b> без <b style='color:#5ba8f5'>AOB</b>.")
# г) площадь APSD = ABCD + DSC − ABP − PCS
s = G + poly([PT['A'],PT['B'],PT['C'],PT['S'],PT['D']], GOLD, 1.0)
s += poly([PT['A'],PT['P'],PT['S'],PT['D']], VIO, 1.0, VIO, 0.35)
s += tri(['A','B','P'], BLUE, 0.35) + tri(['P','C','S'], GREEN, 0.35)
s += line(PT['S'],(4,SY),GREEN,0.6,True) + line(PT['C'],(4,SY),GREEN,0.5,True) + at((3,SY), '2x', 0, -1.6, GREEN)
s += at((4,3), '2x', 4.2, 1.0, GREEN) + at((4,1), '2x', 4.2, 1.0, BLUE)
s += at((2,(4+SY)/2), 'RS', -4.0, 1.0, LAB) + xmark() + names()
V['высота от S до прямой BC равна RC = 2x'] = fig(svg(s, 'APSD = ABCSD без ABP и PCS'),
  "г) площадь <b style='color:#c58af9'>APSD</b> = <b style='color:#f0a83c'>ABCSD</b> без <b style='color:#5ba8f5'>ABP</b> и <b style='color:#5fd38d'>PCS</b>.")

# 7. раздел «Найдём …»: треугольник RCS
s = grid() + full() + tri(['R','C','S'], GOLD, 0.4)
s += at((3,4), '2x', 0, 4.4) + at((2,(4+SY)/2), 'RS', -4.0, 1.0, BLUE) + at((3,(4+SY)/2), 'CS', 4.6, 1.0, RED)
s += xmark() + names()
V['стороны RC = 2x, CS и RS'] = fig(svg(s, 'Треугольник RCS', mw=320),
  "<b style='color:#f0a83c'>RCS</b>: RC = 2x, неизвестные <b style='color:#5ba8f5'>RS</b> и <b style='color:#f2686c'>CS</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
