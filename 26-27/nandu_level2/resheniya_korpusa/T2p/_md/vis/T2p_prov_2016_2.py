import json, sys
# Рисунки к Т2′ провинциал 2016 №2. Координаты задачи — в сантиметрах (y вверх), A = (0, 0), C = (39, 0),
# M = (12, 0), E = (12, 9), D = (27, 9), B = (432/13, −180/13) — основание высоты из B на AC.
# SVG: X = U·x, Y = U·(9 − y).
U = 1.5
def xy(p): return round(U*p[0], 2), round(U*(9-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(432/13,-180/13),'C':(39,0),'D':(27,9),'E':(12,9),'M':(12,0)}
OFF = {'A':(-2.6,1.0),'B':(0,3.8),'C':(2.6,1.0),'D':(1.4,-1.6),'E':(-1.4,-1.6),'M':(1.8,3.4)}
H = (39,9)   # основание высоты из C на прямую ED

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
VB = '-6 -5 72 44'
def svg(inner, label, vb=VB):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
SEG = [('A','B'),('B','C'),('C','D'),('D','E'),('E','A'),('A','C'),('E','M')]
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    return ''.join(line(PT[a],PT[b],col,w) for a,b in SEG)
ALL = list('ABCDEM')
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly([PT[p] for p in pts], col, 0.9, col, op)
def mid(a, b): return ((PT[a][0]+PT[b][0])/2, (PT[a][1]+PT[b][1])/2)
def xmark():   # x = BC — у прямого угла B
    return line(PT['B'],PT['C'],GOLD,1.4) + at(mid('B','C'), 'x', 2.2, 1.0, GOLD, 2.8)
def em(col=BLUE):   # высота EM = 9
    return line(PT['E'],PT['M'],col,1.0,True) + at(((12,4.5)), '9', -1.8, 1.0, col, 2.6)
LX = {('B','C'):(2.2,1.0),('C','D'):(2.0,-0.6),('D','E'):(0,-1.4),('E','A'):(-2.0,-0.6)}

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['у четырёх сторон пятиугольника одна и та же длина'] = fig(svg(s, 'Рисунок условия').replace("<svg ", "<svg style='max-width:480px' ", 1), 'Рисунок из условия.')

# 2. буквы: x — четыре равные стороны, AB и AC — неизвестные
s = full()
for (a,b),(dx,dy) in LX.items():
    s += line(PT[a],PT[b],GOLD,1.2) + at(mid(a,b), 'x', dx, dy)
s += line(PT['A'],PT['B'],BLUE,1.0) + at(mid('A','B'), 'AB', -2.2, 3.2, BLUE)
s += line(PT['A'],PT['C'],RED,1.0) + at((22,0), 'AC', 0, 3.2, RED)
s += names()
V['AB и AC — неизвестные отрезки'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> — четыре равные стороны, <b style='color:#5ba8f5'>AB</b> и <b style='color:#f2686c'>AC</b> — неизвестные отрезки.")

# 3–5. из каких фигур состоит каждое спрошенное
G = full()
# а) ABC — прямоугольный, катеты AB и BC
s = G + tri('ABC', GOLD, 0.35) + line(PT['A'],PT['B'],BLUE,1.2) + at(mid('A','B'), 'AB', -2.2, 3.2, BLUE)
s += xmark() + names()
V['ABC — прямоугольный треугольник с катетами'] = fig(svg(s, 'Треугольник ABC'),
  "а) площадь ABC: катеты <b style='color:#5ba8f5'>AB</b> и <b style='color:#f0a83c'>BC = x</b>.")
# б) ABCDE = ABC + трапеция ACDE
s = G + tri('ABC', GOLD, 0.35) + poly([PT[p] for p in 'ACDE'], GREEN, 0.9, GREEN, 0.35)
s += at(mid('D','E'), 'x', 0, -1.4, GREEN) + at((22,0), 'AC', 0, 3.2, GREEN) + em() + names()
V['ACDE — трапеция с основаниями AC и ED'] = fig(svg(s, 'ABCDE = ABC + ACDE'),
  "б) площадь ABCDE: <b style='color:#f0a83c'>ABC</b> и <b style='color:#5fd38d'>трапеция ACDE</b>; высота <b style='color:#5ba8f5'>EM = 9</b>.")
# в) CDE: основание ED = x, высота из C равна EM
s = G + tri('CDE', VIO, 0.45) + line(PT['D'],H,VIO,0.6,True) + line(PT['C'],H,BLUE,1.0,True)
s += at((39,4.5), '9', 1.8, 1.0, BLUE) + em() + at(mid('D','E'), 'x', 0, -1.4, VIO) + names()
V['высота из C на прямую ED равна расстоянию'] = fig(svg(s, 'Треугольник CDE'),
  "в) площадь CDE: основание <b style='color:#c58af9'>ED = x</b>, высота из C — на продолжение ED, она равна <b style='color:#5ba8f5'>EM = 9</b>.")

# 6–8. раздел «Найдём x, AB и AC»: контур каждого данного периметра
def contour(pts, xs, extra, cap, key, lab):
    s = full() + poly([PT[p] for p in pts], GOLD, 0.4)
    for a,b in xs:
        s += line(PT[a],PT[b],GOLD,1.2) + at(mid(a,b), 'x', *LX[(a,b)])
    s += extra + names()
    V[key] = fig(svg(s, lab), cap)
contour('ABCDE', [('B','C'),('C','D'),('D','E'),('E','A')],
        line(PT['A'],PT['B'],BLUE,1.2) + at(mid('A','B'), 'AB', -2.2, 3.2, BLUE),
        "Периметр ABCDE: <b style='color:#5ba8f5'>AB</b> и четыре стороны <b style='color:#f0a83c'>x</b>; AC — внутри.",
        'стороны AB, BC = x, CD = x, DE = x и EA = x.', 'Контур ABCDE')
contour('ACDE', [('C','D'),('D','E'),('E','A')],
        line(PT['A'],PT['C'],RED,1.2) + at((22,0), 'AC', 0, 3.2, RED),
        "Периметр ACDE: <b style='color:#f2686c'>AC</b> и три стороны <b style='color:#f0a83c'>x</b>.",
        'стороны AC, CD = x, DE = x и EA = x.', 'Контур ACDE')
contour('ABC', [('B','C')],
        line(PT['A'],PT['B'],BLUE,1.2) + at(mid('A','B'), 'AB', -2.2, 3.2, BLUE) + line(PT['A'],PT['C'],RED,1.2) + at((22,0), 'AC', 0, 3.2, RED),
        "Периметр ABC: <b style='color:#5ba8f5'>AB</b>, <b style='color:#f0a83c'>x</b> и <b style='color:#f2686c'>AC</b>.",
        'стороны AB, BC = x и AC.', 'Контур ABC')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
