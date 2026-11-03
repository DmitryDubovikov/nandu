import json, sys
# Рисунки к Т2″ национал 2017, день II, №5. Координаты — как на чертеже условия (y вверх):
# A = (0, 0), B = (12, 0), C = (7.3, 4.5), D = (8, 0) (AB = 3DB), E = 3/8 · C (AE = 3/8 AC).  SVG: X = U·x, Y = U·(6 − y).
U = 6
def xy(p): return round(U*p[0], 2), round(U*(6-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

C0 = (7.3, 4.5)
PT = {'A':(0,0),'B':(12,0),'C':C0,'D':(8,0),'E':(3*C0[0]/8, 3*C0[1]/8)}
OFF = {'A':(-3.0,1.4),'B':(3.0,1.4),'C':(0,-2.6),'D':(0,4.4),'E':(-2.6,-1.6)}
ALL = ['A','B','C','D','E']
SEG = [('A','C'),('C','B'),('A','D'),('D','B'),('E','D')]   # на чертеже условия
SEG_BE = SEG + [('B','E')]                                 # после «проведём BE»

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
def full(col=DIM, w=0.45, segs=SEG_BE): return ''.join(line(PT[a], PT[b], col, w) for a, b in segs)
def names(): return labels(ALL, MUT)
def svg(inner, label, vb='-6 -3 86 44'): return f"<svg viewBox='{vb}' style='max-width:560px' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"

V = {}
# цвет треугольника — один во всех рисунках
TC = {'ADE': GREEN, 'DBE': RED, 'BCE': BLUE, 'DBC': VIO}
TP = {'ADE': ['A','D','E'], 'DBE': ['D','B','E'], 'BCE': ['B','C','E'], 'DBC': ['D','B','C'], 'ABC': ['A','B','C']}
def tri_(n, op=0.42): return poly([PT[q] for q in TP[n]], TC[n], 1.0, TC[n], op)
def cname(n): return f"<b style='color:{TC[n]}'>{n}</b>"
def hgt(a, b, lab, dx=0, dy=0):   # высота пунктиром с подписью
    (x1,y1),(x2,y2) = xy(a), xy(b)
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{LAB}' stroke-width='0.7' stroke-dasharray='1.4 1.1'/>"
            + at(((a[0]+b[0])/2, (a[1]+b[1])/2), lab, dx, dy, LAB, 2.8))
def rangle(p, u, v, col=LAB, s=0.55):   # прямой угол в вершине p, стороны по единичным направлениям u, v
    a = (p[0]+u[0]*s, p[1]+u[1]*s); b = (a[0]+v[0]*s, a[1]+v[1]*s); c = (p[0]+v[0]*s, p[1]+v[1]*s)
    return f"<polyline points='{'%s,%s' % xy(a)} {'%s,%s' % xy(b)} {'%s,%s' % xy(c)}' fill='none' stroke='{col}' stroke-width='0.4'/>"

# высоты: из E и из C на прямую AB, из B на прямую AC (основание перпендикуляра — на продолжении AC за C)
HE = (PT['E'][0], 0); HC = (C0[0], 0)
L2 = C0[0]**2 + C0[1]**2; t = 12*C0[0]/L2; HB = (t*C0[0], t*C0[1])
ac = (C0[0]/L2**0.5, C0[1]/L2**0.5); bn = ((PT['B'][0]-HB[0])/((PT['B'][0]-HB[0])**2+(HB[1])**2)**0.5, -HB[1]/((PT['B'][0]-HB[0])**2+(HB[1])**2)**0.5)

# 1. рисунок условия
V['отрезка BE на чертеже нет'] = fig(svg(full(INK, 0.55, SEG) + labels(ALL), 'Рисунок условия'), 'Рисунок из условия.')

# 2. три треугольника
CEN = {'ADE': (3.6,0.75), 'DBE': (7.6,0.55), 'BCE': (7.4,2.6)}
s = full(INK, 0.5) + ''.join(tri_(n) for n in CEN) + ''.join(at(CEN[n], n, 0, 1.0, LAB, 2.6) for n in CEN) + labels(ALL)
V['разрезают чертёж на три треугольника'] = fig(svg(s, 'Три треугольника'), 'Отрезок BE проведён.')

# 3–6. каждое спрошенное
for anc, parts, cap in (('ABE состоит из ADE и DBE', ['ADE','DBE'], None),
                        ('BCE — сам один из трёх треугольников', ['BCE'], None),
                        ('DBCE состоит из DBE и BCE', ['DBE','BCE'], None)):
    s = full() + ''.join(tri_(n, 0.5) for n in parts) + names()
    V[anc] = fig(svg(s, anc), ' + '.join(cname(n) for n in parts))
s = full() + tri_('DBC', 0.5) + line(PT['D'], PT['C'], VIO, 1.0) + poly([PT[q] for q in TP['ABC']], GOLD, 1.0) + names()
V['ABC состоит из ADE, DBE и BCE'] = fig(svg(s, 'DBC и ABC'),
  f"{cname('DBC')} — часть <b style='color:{GOLD}'>ABC</b>; ABC = {cname('ADE')} + {cname('DBE')} + {cname('BCE')}.")

# 7. врезка: пример на числах — основания 4 и 6, общая высота 5
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

# 8. порядок поиска площадей: известна S(ADE); ① DBE, ② BCE, ③ DBC — номера разделов; высота из E пунктиром
s = full() + tri_('ADE', 0.45) + tri_('DBE', 0.45) + tri_('BCE', 0.45) + line(PT['D'], PT['C'], VIO, 0.9, True)
s += hgt(PT['E'], HE, 'h', -2.0, 1.0) + rangle(HE, (1,0), (0,1))
s += at((5.0,0.55), '12', 0, 1.2, LAB, 3.4) + at((10.0,0), '? ①', 0, 4.6, RED, 3.2) + at((7.0,2.7), '? ②', 0, 1.2, LAB, 3.2)
s += at((9.4,1.9), '? ③', 2.0, 1.2, VIO, 3.2) + names()
V['S(ADE) = 12 → S(DBE) → S(BCE) → S(DBC)'] = fig(svg(s, 'Порядок поиска площадей'),
  f"Площадь {cname('ADE')} известна; номер — раздел, где найдём площадь: ① {cname('DBE')}, ② {cname('BCE')}, ③ {cname('DBC')} (пунктир DC). "
  f"Высота h из E — общая у {cname('ADE')} и {cname('DBE')}.")

# 9. раздел 2: ABE и BCE — одна высота из B на прямую AC
s = full() + tri_('ADE', 0.45) + tri_('DBE', 0.45) + tri_('BCE', 0.45) + line(C0, HB, LAB, 0.5, True)
s += hgt(PT['B'], HB, 'h', 2.2, 0.6) + rangle(HB, (-ac[0], -ac[1]), bn)
s += at(((PT['A'][0]+PT['E'][0])/2, (PT['A'][1]+PT['E'][1])/2), '3', -1.6, -0.6, GOLD) + at(((PT['E'][0]+C0[0])/2, (PT['E'][1]+C0[1])/2), '5', -1.6, -0.6, GOLD)
s += names()
V['у ABE и BCE одна и та же высота'] = fig(svg(s, 'ABE и BCE, высота из B', '-6 -6 86 47'),
  f"ABE = {cname('ADE')} + {cname('DBE')} и {cname('BCE')}: основания AE и EC — 3 и 5 восьмых AC, высота h из B общая.")

# 10. раздел 3: DBC и ABC — одна высота из C на прямую AB
s = full() + tri_('DBC', 0.5) + poly([PT[q] for q in TP['ABC']], GOLD, 1.0) + line(PT['D'], PT['C'], VIO, 1.0)
s += hgt(C0, HC, 'h', -2.0, 0.8) + rangle(HC, (-1,0), (0,1))
s += at((4,0), '2 части', 0, 4.4, GOLD, 2.6) + at((10,0), '1 часть', 0, 4.4, VIO, 2.6) + names()
V['у DBC и ABC одна и та же высота'] = fig(svg(s, 'DBC и ABC, высота из C', '-6 -3 86 46'),
  f"{cname('DBC')} и <b style='color:{GOLD}'>ABC</b>: основания DB и AB = 3DB, высота h из C общая.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
