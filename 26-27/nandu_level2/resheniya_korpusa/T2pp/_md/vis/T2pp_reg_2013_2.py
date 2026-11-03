import json, sys
# Рисунки к Т2″ регионал 2013 №2. Координаты задачи в см (y вверх):
# A = (0, 0), G = (28, 0), B = (77, 0), C = (77, 12), F = (28, 12), E = (0, 12), D = (0, 60).  SVG: X = U·x, Y = U·(60 − y).
U = 1
def xy(p): return round(U*p[0], 2), round(U*(60-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'G':(28,0),'B':(77,0),'C':(77,12),'F':(28,12),'E':(0,12),'D':(0,60)}
OFF = {'A':(-3.0,3.6),'G':(0,4.4),'B':(3.0,3.6),'C':(3.4,0),'F':(1.6,-1.6),'E':(-3.4,1.2),'D':(-3.2,0)}
ALL = ['A','B','C','D','E','F','G']
SEG = [('A','B'),('B','C'),('C','D'),('D','A'),('E','C'),('D','F'),('F','G')]

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1, dash=False):
    s = ' '.join('%s,%s' % xy(p) for p in pts)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'{d}/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def at(p, s, dx=0, dy=0, col=GOLD, size=3.0):
    X, Y = xy(p); return txt(round(X+dx,2), round(Y+dy,2), s, col, size)
def labels(names, col=LAB):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col) + f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def full(col=DIM, w=0.45): return ''.join(line(PT[a], PT[b], col, w) for a, b in SEG)
def names(): return labels(ALL, MUT)
def svg(inner, label, vb='-8 -5 94 74', big=False):
    st = " style='max-width:560px'" if big else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner, cap, fx=False): return f"<figure class='st{' fx' if fx else ''}'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def fill(pts, col, op=0.4): return poly([PT[n] for n in pts], col, 1.0, col, op)

V = {}
# цвет части — один во всех рисунках
TC = {'T1': RED, 'T2': GREEN, 'R1': BLUE, 'R2': GOLD}
TP = {'T1': ['D','E','F'], 'T2': ['D','F','C'], 'R1': ['A','G','F','E'], 'R2': ['G','B','C','F']}
CEN = {'T1': (8,24), 'T2': (36,22), 'R1': (14,6), 'R2': (52.5,6)}
def part(n, op=0.42): return fill(TP[n], TC[n], op)
def cname(n): return f"<b style='color:{TC[n]}'>{n}</b>"
def hgt(a, b, lab, dx=0, dy=0, col=LAB):   # высота пунктиром с подписью
    (x1,y1),(x2,y2) = xy(a), xy(b)
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='0.7' stroke-dasharray='1.4 1.1'/>"
            + at(((a[0]+b[0])/2, (a[1]+b[1])/2), lab, dx, dy, col, 2.8))

# 1. рисунок условия (буквы E, F, G добавлены — золотом)
s = full(INK, 0.55) + ''.join(at(CEN[n], n, 0, 1.0, LAB, 3.0) for n in TC) + labels(['A','B','C','D']) + labels(['E','F','G'], GOLD)
V['три точки чертежа без букв назовём E, F и G'] = fig(svg(s, 'Рисунок условия', big=True), 'Рисунок из условия; буквы E, F, G добавлены.')

# 2. четыре части
s = full(INK, 0.5) + ''.join(part(n) for n in TC) + ''.join(at(CEN[n], n, 0, 1.0, LAB, 3.0) for n in TC) + labels(ALL)
V['T1 — треугольник DEF'] = fig(svg(s, 'Четыре части'), '')

# 3. каждое спрошенное
s = full() + part('R2', 0.55) + names()
V['R2 — сама одна из четырёх частей'] = fig(svg(s, 'а) площадь R2'), f"а) площадь {cname('R2')}")
ABC_C = '#7fb8e8'
s = full() + poly([PT['A'],PT['B'],PT['C']], BLUE, 1.0, BLUE, 0.5) + line(PT['A'], PT['C'], LAB, 0.7, True)
s += poly([PT['A'],PT['B'],PT['C'],PT['E']], LAB, 0.9) + names()
V['ABC — половина прямоугольника ABCE'] = fig(svg(s, 'б) площадь ABC'), f"б) площадь ABC: половина ABCE = {cname('R1')} + {cname('R2')}")
s = full() + poly([PT['A'],PT['B'],PT['D']], VIO, 1.0, VIO, 0.5) + line(PT['B'], PT['D'], LAB, 0.7, True)
s += poly([PT['B'],PT['C'],PT['D']], LAB, 0.9, dash=True) + names()
V['ABD — это ABCD без треугольника BCD'] = fig(svg(s, 'в) площадь ABD'),
  f"в) площадь ABD: ABCD = {cname('R1')} + {cname('R2')} + {cname('T1')} + {cname('T2')} без BCD (пунктир)")

# 4. T1 и T2 — одна высота DE, основания EF и FC
s = full() + part('T1', 0.5) + part('T2', 0.5) + line(PT['D'], PT['E'], GOLD, 1.4) + at((0,36), 'DE', -4.4, 1.0)
s += at((14,12), 'EF', 0, 4.0, RED) + at((52.5,12), 'FC', 0, 4.0, GREEN) + names()
V['EF и FC лежат на прямой EC'] = fig(svg(s, 'T1 и T2, высота DE'),
  f"{cname('T1')} и {cname('T2')}: общая высота DE, основания EF и FC.")

# 5. врезка: пример на числах — основания 4 и 6, общая высота 5 (как в образце)
def bx(p): return round(7*p[0]+4, 2), round(7*(5-p[1])+4, 2)
def bpoly(pts, col, op):
    return f"<polygon points='{' '.join('%s,%s' % bx(q) for q in pts)}' fill='{col}' fill-opacity='{op}' stroke='{col}' stroke-width='0.8' stroke-linejoin='round'/>"
def btxt(p, s_, col=LAB, size=3.0, dy=0): X, Y = bx(p); return txt(X, round(Y+dy,2), s_, col, size)
s = bpoly([(0,0),(4,0),(7,5)], BLUE, 0.4) + bpoly([(4,0),(10,0),(7,5)], GREEN, 0.4)
(x1,y1),(x2,y2) = bx((7,5)), bx((7,0))
s += f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{LAB}' stroke-width='0.7' stroke-dasharray='1.4 1.1'/>"
s += btxt((7.6,2.5), 'h = 5', LAB, 2.8) + btxt((2,0), '4', BLUE, 3.0, 4.4) + btxt((7,0), '6', GREEN, 3.0, 4.4)
s += btxt((3.6,1.4), '10', BLUE, 3.2) + btxt((8.6,1.4), '15', GREEN, 3.2)
V['Пример на числах, не из задачи: основания 4 и 6'] = fig(f"<svg viewBox='0 0 82 48' role='img' aria-label='Пример'>{s}</svg>",
  "4 · 5 : 2 = 10, 6 · 5 : 2 = 15; основание 6 в 3/2 раза длиннее 4, и площадь 15 в 3/2 раза больше 10.")

# 6. порядок поиска: ① FC : EF, ② EF, FC, BC, ③ S(R1), S(R2), ④ S(T1), S(T2)
s = full() + ''.join(part(n, 0.42) for n in TC)
s += at((14,12), '? ②', 0, -1.4, LAB, 3.0) + at((52.5,12), '? ②', 0, -1.4, LAB, 3.0) + at((77,6), '? ②', 5.6, 1.0, LAB, 3.0)
s += at((14,6), 'P = 80, ? ③', 0, 1.0, LAB, 3.0) + at((52.5,6), 'P = 122, ? ③', 0, 1.0, LAB, 3.0)
s += at((8,24), '? ④', 0, 1.0, LAB, 3.0) + at((36,22), '? ④', 0, 1.0, LAB, 3.0) + names()
V['FC : EF → EF, FC и BC'] = fig(svg(s, 'Порядок поиска', '-8 -5 100 74'),
  f"Числами даны периметры {cname('R1')} и {cname('R2')}; номер — раздел, где найдём: ② отрезки EF, FC и BC, ③ площади {cname('R1')} и {cname('R2')}, ④ площади {cname('T1')} и {cname('T2')}.")

# 7. буквы на рисунке: EF = 4x, FC = 7x, BC = h, черта x в исходном месте
s = full() + part('R1', 0.35) + part('R2', 0.35) + line(PT['E'], (7,12), GOLD, 1.6) + at((3.5,12), 'x', 0, -1.6, GOLD, 3.0)
s += at((14,0), '4x', 0, 4.4, LAB) + at((52.5,0), '7x', 0, 4.4, LAB) + at((77,6), 'h', 3.4, 1.0, LAB) + at((0,6), 'h', -3.4, 1.0, LAB) + names()
V['x = EF : 4, h = BC'] = fig(svg(s, 'Буквы на рисунке'), f"Ширины {cname('R1')} и {cname('R2')}: 4x и 7x; высота у обоих h.")

# 8. раздел 5: BCD и ABC — общее основание BC, высота AB
s = full() + poly([PT['A'],PT['B'],PT['C']], BLUE, 1.0, BLUE, 0.5) + poly([PT['B'],PT['C'],PT['D']], VIO, 1.0, VIO, 0.35)
s += line(PT['C'], (77,60), LAB, 0.5, True) + hgt(PT['D'], (77,60), 'AB', 0, -1.4)
s += line(PT['A'], PT['B'], GOLD, 1.4) + at((38.5,0), 'AB', 0, 4.4) + line(PT['B'], PT['C'], GOLD, 1.4) + at((77,6), 'BC', 4.4, 1.0) + names()
V['у треугольников BCD и ABC общая высота AB'] = fig(svg(s, 'BCD и ABC', '-8 -6 94 75'),
  "<b style='color:#c58af9'>BCD</b> и <b style='color:#5ba8f5'>ABC</b>: общее основание BC, общая высота AB.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
