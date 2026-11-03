import json, sys
# Рисунки к Т2′ регионал 2024 №2. Координаты задачи — в сантиметрах (y вверх), A = (0, 0), C = (30, 36);
# квадрат EFGH на AD: F = (0, 9), E = (0, 27), G = (18, 9), H = (18, 27). SVG: X = U·x, Y = U·(36 − y).
U = 1.3
def xy(p): return round(U*p[0], 2), round(U*(36-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(30,0),'C':(30,36),'D':(0,36),'E':(0,27),'F':(0,9),'G':(18,9),'H':(18,27)}
OFF = {'A':(-2.8,3.6),'B':(2.8,3.6),'C':(2.8,-1.6),'D':(-2.8,-1.6),'E':(-3.0,1.2),'F':(-3.0,1.2),
       'G':(1.2,4.0),'H':(1.4,-1.6)}

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
def svg(inner, label, vb='-8 -6 54 56'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
SEG = [('A','B'),('B','C'),('C','D'),('D','A'),('E','H'),('H','G'),('G','F'),('H','C'),('G','B')]
def full(col=DIM, w=0.45):   # весь чертёж условия тусклым — фон каждого рисунка
    return ''.join(line(PT[a],PT[b],col,w) for a,b in SEG)
ALL = list('ABCDEFGH')
def names(): return labels(ALL, MUT)
def xmark():   # кирпич x = AF, у A
    return line(PT['A'],PT['F'],GOLD,1.4) + at((0,4.5), 'x', -2.4, 1.0, GOLD, 3.0)
def tri(pts, col, op=0.45): return poly([PT[p] for p in pts], col, 0.9, col, op)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['E и F лежат на AD, EF — сторона квадрата'] = fig(svg(s, 'Рисунок условия', '-8 -6 54 58').replace("<svg ", "<svg style='max-width:420px' ", 1), 'Рисунок из условия.')

# 2. буквы: x = AF, AB и наклонная BG
s = full() + xmark()
s += line(PT['E'],PT['D'],GOLD,1.4) + at((0,31.5), 'x', -2.4, 1.0)
s += line(PT['F'],PT['E'],GOLD,0.9) + at((0,18), '2x', -3.0, 1.0)
s += line(PT['F'],PT['G'],GOLD,0.9) + at((9,9), '2x', 0, 3.6)
s += line(PT['A'],PT['B'],BLUE,1.1) + at((15,0), 'AB', 0, 4.4, BLUE)
s += line(PT['G'],PT['B'],RED,1.1) + at((24,4.5), 'BG', 2.6, -1.0, RED)
s += names()
V['x = AF, AB и наклонная BG.'] = fig(svg(s, 'Буквы', '-8 -6 54 58'),
  "<b style='color:#f0a83c'>x</b> = AF = ED; EF = FG = 2x, AD = 4x. Неизвестны ещё <b style='color:#5ba8f5'>AB</b> и <b style='color:#f2686c'>BG</b>.")

# 3–6. из каких фигур состоит каждое спрошенное
G = full()
# а) периметр ABGF
s = G + line(PT['A'],PT['B'],GOLD,1.2) + line(PT['G'],PT['F'],GOLD,1.2) + line(PT['F'],PT['A'],GOLD,1.2)
s += line(PT['B'],PT['G'],RED,1.2,True) + line(PT['B'],PT['C'],RED,0.5) + line(PT['C'],PT['H'],RED,0.5) + line(PT['H'],PT['G'],RED,0.5)
s += at((15,0), 'AB', 0, 4.4) + at((9,9), '2x', 0, -1.4) + at((0,4.5), 'x', -2.4, 1.0) + at((24,4.5), 'BG', 2.6, -1.0, RED)
s += names()
V['BG стоит в периметре BCHG, который дан'] = fig(svg(s, 'Контур ABGF', '-8 -6 54 58'),
  "а) периметр <b style='color:#f0a83c'>ABGF</b>; <b style='color:#f2686c'>BG</b> — сторона и BCHG.")
# б) площадь ABGF — трапеция
s = G + poly([PT['A'],PT['B'],PT['G'],PT['F']], GOLD, 1.0, GOLD, 0.4)
s += at((15,0), 'AB', 0, 4.4) + at((9,9), '2x', 0, -1.4) + at((0,4.5), 'x', -2.4, 1.0) + names()
V['ABGF — трапеция с основаниями AB и FG'] = fig(svg(s, 'Трапеция ABGF', '-8 -6 54 58'),
  "б) площадь трапеции ABGF; высота AF = x.")
# в) площадь CDFG — трапеция
s = G + poly([PT['C'],PT['D'],PT['F'],PT['G']], GREEN, 1.0, GREEN, 0.35)
s += at((15,36), 'AB', 0, -1.6, GREEN) + at((9,9), '2x', 0, 3.8, GREEN) + at((0,22.5), '3x', -3.0, 1.0, GREEN)
s += xmark() + names()
V['CDFG — трапеция с основаниями DC'] = fig(svg(s, 'Трапеция CDFG', '-8 -6 54 58'),
  "в) площадь трапеции CDFG; DC = AB, высота FD = 3x.")
# г) площадь BDG = ABD без ABGF и FGD
s = G + poly([PT['A'],PT['B'],PT['D']], GOLD, 1.0)
s += tri('ABGF', BLUE, 0.35) + tri('FGD', GREEN, 0.35) + tri('BDG', VIO, 0.5)
s += at((15,0), 'AB', 0, 4.4) + at((0,22.5), '3x', -3.0, 1.0, GREEN) + at((9,9), '2x', 0, 3.8, GREEN)
s += xmark() + names()
V['G лежит внутри ABD, F — на AD.'] = fig(svg(s, 'BDG внутри ABD', '-8 -6 54 58'),
  "г) площадь <b style='color:#c58af9'>BDG</b> = <b style='color:#f0a83c'>ABD</b> без <b style='color:#5ba8f5'>ABGF</b> и <b style='color:#5fd38d'>FGD</b>.")

# 7. раздел «Найдём x»: квадрат EFGH со стороной 2x
s = full() + poly([PT['E'],PT['F'],PT['G'],PT['H']], GOLD, 1.0, GOLD, 0.35)
s += at((0,18), '2x', -3.0, 1.0) + at((9,9), '2x', 0, 3.8) + at((9,18), '324', 0, 1.0, LAB, 3.2)
s += xmark() + names()
V['EFGH — квадрат со стороной EF = 2x.'] = fig(svg(s, 'Квадрат EFGH', '-8 -6 54 58'),
  "S(<b style='color:#f0a83c'>EFGH</b>) = 324; сторона 2x.")

# 8. раздел «Найдём AB»: контур ABCD
s = full() + poly([PT['A'],PT['B'],PT['C'],PT['D']], GOLD, 1.0)
s += at((15,0), 'AB', 0, 4.4, BLUE) + line(PT['A'],PT['B'],BLUE,1.1) + at((30,18), '4x', 3.4, 1.0)
s += xmark() + names()
V['ABCD — прямоугольник со сторонами AB и AD = 4x.'] = fig(svg(s, 'Контур ABCD', '-8 -6 56 58'),
  "P(<b style='color:#f0a83c'>ABCD</b>) = 132.")

# 9. раздел «Найдём BG»: симметрия, CH = BG
s = full() + line((-4,18),(34,18),MUT,0.5,True)
s += line(PT['B'],PT['C'],GOLD,1.0) + line(PT['H'],PT['G'],GOLD,1.0)
s += line(PT['C'],PT['H'],RED,1.2) + line(PT['G'],PT['B'],RED,1.2)
s += at((30,12), '4x', 3.4, 1.0) + at((18,12), '2x', 3.0, 1.0)
s += at((24,4.5), 'BG', 2.6, -1.0, RED) + at((24,31.5), 'CH', 2.6, 2.6, RED)
s += xmark() + line(PT['E'],PT['D'],GOLD,1.4) + at((0,31.5), 'x', -2.4, 1.0) + names()
V['чертёж симметричен относительно прямой'] = fig(svg(s, 'Симметрия BCHG', '-8 -6 56 58'),
  "AF = ED ⇒ пунктир — ось симметрии; <b style='color:#f2686c'>CH</b> = <b style='color:#f2686c'>BG</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
