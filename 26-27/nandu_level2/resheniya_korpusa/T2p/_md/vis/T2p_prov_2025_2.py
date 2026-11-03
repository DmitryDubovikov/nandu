import json, sys
# Рисунки к Т2′ провинциал 2025 №2. Координаты задачи в см (y вверх): A = (0, 0), C = (45, 0), E = (45, 31), F = (16.2, 52.6).
# SVG: X = U · x, Y = U · (53 − y).
U = 1.5
def xy(p): return round(U*p[0], 2), round(U*(53-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(9,0),'C':(45,0),'H':(0,22),'I':(9,22),'D':(45,22),
      'G':(0,31),'J':(9,31),'E':(45,31),'F':(16.2,52.6)}
OFF = {'A':(-3.2,4.2),'B':(0,5.0),'C':(3.2,4.2),'H':(-3.6,1.2),'I':(3.0,4.2),'D':(3.6,1.2),
       'G':(-3.6,1.2),'J':(3.4,-1.6),'E':(3.6,1.2),'F':(0,-2.4)}
SEGS = [('A','C'),('H','D'),('G','E'),('A','G'),('B','J'),('C','E'),('G','F'),('F','E')]

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
ALL = list(PT)
def full(col=DIM, w=0.45):   # весь чертёж условия — фон каждого рисунка
    return ''.join(line(PT[a], PT[b], col, w) for a, b in SEGS)
def names(): return labels(ALL, MUT)
def svg(inner, label, vb='-13 -8 92 95'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:460px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def xmark():   # кирпич x = AB, у A
    return line((0,0),(9,0),GOLD,1.4) + at((4.5,0), 'x', 0, 4.6, GOLD, 3.2)
def hmark():   # h = BI
    return line((9,0),(9,22),BLUE,1.4) + at((9,11), 'h', 2.6, 1.0, BLUE, 3.2)
def rangle(p, u, v, col=INK, s=2.2):   # значок прямого угла в p, u и v — единичные направления (в см)
    a = (p[0]+u[0]*s, p[1]+u[1]*s); b = (a[0]+v[0]*s, a[1]+v[1]*s); c = (p[0]+v[0]*s, p[1]+v[1]*s)
    return f"<polyline points='{'%s,%s' % xy(a)} {'%s,%s' % xy(b)} {'%s,%s' % xy(c)}' fill='none' stroke='{col}' stroke-width='0.4'/>"
FG_u = ((0-16.2)/27, (31-52.6)/27); FE_u = ((45-16.2)/36, (31-52.6)/36)
def tri(pts, col, op=0.4): return poly(pts, col, 1.0, col, op)

V = {}
# 1. рисунок условия
s = full(INK, 0.6) + rangle(PT['F'], FG_u, FE_u) + labels(ALL)
V['AB = HI = GJ = GH'] = fig(svg(s, 'Рисунок условия', '-9 -8 86 92'), 'Рисунок из условия.')

# 2. буквы
s = full() + xmark() + hmark()
s += line(PT['G'],PT['J'],GOLD,1.0) + at((4.5,31), 'x', 0, -1.6)
s += line(PT['H'],PT['G'],GOLD,1.0) + at((0,26.5), 'x', -2.6, 1.0)
s += line(PT['B'],PT['C'],GOLD,1.0) + at((27,0), '4x', 0, 4.6)
s += line(PT['J'],PT['E'],GOLD,1.0) + at((27,31), '4x', 0, 4.4)
s += names()
V['x = AB, h = BI.'] = fig(svg(s, 'Буквы'), "<b style='color:#f0a83c'>x</b> = AB, <b style='color:#5ba8f5'>h</b> = BI.")

# 3. а) ACEFG = прямоугольник ACEG + треугольник EFG
s = full() + tri([PT['A'],PT['C'],PT['E'],PT['G']], GOLD, 0.3) + tri([PT['G'],PT['E'],PT['F']], BLUE, 0.45)
s += at((22,15), '5x × (h + x)', 0, 1.0, GOLD, 3.2) + at((22,40), '486', 0, 1.0, BLUE, 3.6)
s += xmark() + names()
V['ACEFG состоит из прямоугольника ACEG'] = fig(svg(s, 'ACEFG'), 'а) площадь ACEFG')

# 4. б) периметр ACEFG
s = full() + line(PT['A'],PT['C'],GOLD,1.2) + line(PT['C'],PT['E'],GOLD,1.2) + line(PT['G'],PT['A'],GOLD,1.2)
s += line(PT['E'],PT['F'],GREEN,1.2) + line(PT['F'],PT['G'],RED,1.2,True)
s += at((27,0), '5x', 0, 4.6) + at((45,15.5), 'h + x', 6.0, 1.0) + at((0,15.5), 'h + x', -5.4, 1.0)
s += at((31,42), 'EF = EJ', 7.0, -1.0, GREEN) + at((8,42), 'FG ?', -5.2, -1.0, RED)
s += line((0,0),(9,0),GOLD,1.4) + names()
V['наклонная FG — катет треугольника EFG'] = fig(svg(s, 'Контур ACEFG'), 'б) периметр ACEFG')

# 5. в) ACEFJ = ACEFG без AGJ и GJF
s = full() + tri([PT['A'],PT['C'],PT['E'],PT['F'],PT['J']], VIO, 0.35)
s += tri([PT['A'],PT['G'],PT['J']], BLUE, 0.45) + tri([PT['G'],PT['J'],PT['F']], GREEN, 0.5)
s += at((0,15.5), 'h + x', -5.4, 1.0, BLUE) + at((4.5,31), 'x', 0, -1.4, BLUE)
s += xmark() + names()
V['ACEFG из а) без треугольников AGJ и GJF'] = fig(svg(s, 'ACEFJ'),
  "в) площадь <b style='color:#c58af9'>ACEFJ</b> = ACEFG без <b style='color:#5ba8f5'>AGJ</b> и <b style='color:#5fd38d'>GJF</b>")

# 6. раздел «Найдём FG»: прямоугольный EFG, катеты EF = 4x и FG
s = full() + tri([PT['G'],PT['E'],PT['F']], BLUE, 0.4) + rangle(PT['F'], FG_u, FE_u, LAB)
s += at((31,42), 'EF = 4x', 7.0, -1.0, BLUE) + at((8,42), 'FG', -4.2, -1.0, RED)
s += line(PT['F'],PT['G'],RED,1.2) + at((25,35), '486', 0, 1.0, BLUE, 3.6) + xmark() + names()
V['EFG — прямоугольный треугольник с катетами EF и FG'] = fig(svg(s, 'Прямоугольный EFG'),
  "Катеты <b style='color:#5ba8f5'>EF</b> и <b style='color:#f2686c'>FG</b>; площадь 486.")

# 7. раздел «Найдём S(GJF)»: общая высота из F на прямую GE
P = (16.2, 31)
s = full() + tri([PT['G'],PT['E'],PT['F']], BLUE, 0.25) + tri([PT['G'],PT['J'],PT['F']], GREEN, 0.55)
s += line(PT['F'], P, LAB, 0.6, True) + rangle(P, (0,1), (1,0), LAB, 1.6)
s += line(PT['G'],PT['J'],GREEN,1.4) + at((4.5,31), 'x', 0, 4.2, GREEN)
s += at((30,31), 'GE = 5x', 0, 4.4, BLUE)
s += names()
V['основания GJ и GE лежат на одной прямой'] = fig(svg(s, 'GJF и EFG с общей высотой'),
  "У <b style='color:#5fd38d'>GJF</b> и <b style='color:#5ba8f5'>EFG</b> одна высота из F (пунктир); основания GJ = x и GE = 5x.")

# 8. врезка: пример на числах
def ex():
    def p(x, y): return (round(4*x+4, 2), round(4*(6-y)+4, 2))
    def L(a, b, col, w=0.6, dash=False):
        (x1,y1),(x2,y2) = p(*a), p(*b); d = " stroke-dasharray='1.4 1'" if dash else ''
        return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}'{d}/>"
    def T(pts, col):
        s = ' '.join('%s,%s' % p(*q) for q in pts)
        return f"<polygon points='{s}' fill='{col}' fill-opacity='0.4' stroke='{col}' stroke-width='0.8'/>"
    s = T([(0,0),(4,0),(3,5)], GREEN) + T([(4,0),(10,0),(3,5)], BLUE) + L((3,5),(3,0),LAB,0.6,True)
    X, Y = p(2,0); s += txt(X, Y+4.4, '4', GREEN, 3.2)
    X, Y = p(7,0); s += txt(X, Y+4.4, '6', BLUE, 3.2)
    X, Y = p(3,2.5); s += txt(X-2.4, Y, '5', LAB, 3.2)
    return f"<figure class='st'><svg viewBox='0 0 52 34' role='img' aria-label='Пример' style='max-width:300px'>{s}</svg><figcaption>Площади 4 · 5 : 2 = 10 и 6 · 5 : 2 = 15; 10 : 15 = 4 : 6.</figcaption></figure>"
V['Пример на числах, не из задачи'] = ex()

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
