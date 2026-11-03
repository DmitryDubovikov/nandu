import json, sys
# Рисунки к Т2″ национал 2023 день II №5. Координаты — как на рисунке PDF (y вверх):
# A = (0, 0), B = (24, 0), C = (6, 24), P = (4, 0), Q = (19.5, 6), R = (5.6, 19.2).  SVG: X = U·x, Y = U·(24 − y).
U = 3
def xy(p): return round(U*p[0], 2), round(U*(24-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(24,0),'C':(6,24),'P':(4,0),'Q':(19.5,6),'R':(5.6,19.2)}
OFF = {'A':(-3.2,3.0),'B':(3.2,3.0),'C':(0,-2.6),'P':(0,4.8),'Q':(3.8,1.4),'R':(3.4,1.6)}
ALL = ['A','B','C','P','Q','R']
SEG = [('A','B'),('B','C'),('C','A'),('P','C'),('P','Q'),('Q','R')]

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
def labels(names, col=LAB):
    out = ''
    for n in names:
        X, Y = xy(PT[n]); dx, dy = OFF[n]
        out += txt(round(X+dx,2), round(Y+dy,2), n, col) + f"<circle cx='{X}' cy='{Y}' r='0.75' fill='{col}'/>"
    return out
def full(col=DIM, w=0.45): return ''.join(line(PT[a], PT[b], col, w) for a, b in SEG)
def names(): return labels(ALL, MUT)
def svg(inner, label, vb='-8 -6 90 86'): return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:460px'>{inner}</svg>"
def fig(inner, cap, fx=False): return f"<figure class='st{' fx' if fx else ''}'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def fill(pts, col, op=0.4): return poly([PT[n] for n in pts], col, 1.0, col, op)
def outline(pts, col, w=1.1): return poly([PT[n] for n in pts], col, w)
def foot(p, a, b):   # основание перпендикуляра из p на прямую ab
    dx, dy = b[0]-a[0], b[1]-a[1]
    t = ((p[0]-a[0])*dx + (p[1]-a[1])*dy) / (dx*dx + dy*dy)
    return (a[0]+t*dx, a[1]+t*dy)
def hgt(a, b, lab, dx=0, dy=0):   # высота пунктиром с подписью
    (x1,y1),(x2,y2) = xy(a), xy(b)
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{LAB}' stroke-width='0.7' stroke-dasharray='1.4 1.1'/>"
            + at(((a[0]+b[0])/2, (a[1]+b[1])/2), lab, dx, dy, LAB, 2.8))

V = {}
# цвет треугольника — один во всех рисунках; ABQ и BPR (не куски) — фиолетовые
TC = {'APC': RED, 'PBQ': BLUE, 'PQR': GREEN, 'RQC': GOLD, 'ABQ': VIO, 'BPR': VIO}
TP = {'APC': ['A','P','C'], 'PBQ': ['P','B','Q'], 'PQR': ['P','Q','R'], 'RQC': ['R','Q','C'],
      'ABQ': ['A','B','Q'], 'BPR': ['B','P','R']}
def tri_(n, op=0.42): return fill(TP[n], TC[n], op)
def cname(n): return f"<b style='color:{TC[n]}'>{n}</b>"

# 1. рисунок условия
V['отрезки разрезают чертёж'] = fig(svg(full(INK, 0.55) + labels(ALL), 'Рисунок условия'), 'Рисунок из условия.')

# 2. четыре куска
CEN = {'APC': (3.6,6.5), 'PBQ': (15.2,2.4), 'PQR': (9.4,9.0), 'RQC': (9.6,16.5)}
s = full(INK, 0.5) + ''.join(tri_(n) for n in CEN) + ''.join(at(CEN[n], n, 0, 1.0, LAB, 2.6) for n in CEN) + labels(ALL)
V['четыре треугольника APC, PBQ, PQR и RQC'] = fig(svg(s, 'Четыре треугольника'), '')

# 3–5. каждое спрошенное — часть какого треугольника
s = full() + tri_('ABQ', 0.45) + line(PT['A'], PT['Q'], VIO, 0.9, True) + outline(['A','B','C'], GOLD, 0.9) + names()
V['ABQ — часть ABC'] = fig(svg(s, 'ABQ внутри ABC'),
  f"а) площадь {cname('ABQ')} — часть <b style='color:{GOLD}'>ABC</b>; AQ проведён пунктиром.")
s = full() + tri_('PQR', 0.5) + outline(['P','Q','C'], GOLD, 0.9) + names()
V['PQR — часть PQC'] = fig(svg(s, 'PQR внутри PQC'),
  f"б) площадь {cname('PQR')} — часть <b style='color:{GOLD}'>PQC</b>.")
s = full() + tri_('BPR', 0.45) + line(PT['B'], PT['R'], VIO, 0.9, True) + outline(['P','B','C'], GOLD, 0.9) + names()
V['BPR — часть PBC'] = fig(svg(s, 'BPR внутри PBC'),
  f"в) площадь {cname('BPR')} — часть <b style='color:{GOLD}'>PBC</b>; BR проведён пунктиром.")

# 6. врезка: пример на числах — основания 4 и 6, общая высота 5
def bx(p): return round(7*p[0]+4, 2), round(7*(5-p[1])+4, 2)
def bpoly(pts, col, op):
    return f"<polygon points='{' '.join('%s,%s' % bx(q) for q in pts)}' fill='{col}' fill-opacity='{op}' stroke='{col}' stroke-width='0.8' stroke-linejoin='round'/>"
def btxt(p, s_, col=LAB, size=3.0, dy=0): X, Y = bx(p); return txt(X, round(Y+dy,2), s_, col, size)
s = bpoly([(0,0),(4,0),(7,5)], BLUE, 0.4) + bpoly([(4,0),(10,0),(7,5)], GREEN, 0.4)
(x1,y1),(x2,y2) = bx((7,5)), bx((7,0))
s += f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{LAB}' stroke-width='0.7' stroke-dasharray='1.4 1.1'/>"
s += btxt((7.6,2.5), 'h = 5', LAB, 2.8) + btxt((2,0), '4', BLUE, 3.0, 4.4) + btxt((7,0), '6', GREEN, 3.0, 4.4)
s += btxt((3.6,1.4), '10', BLUE, 3.2) + btxt((8.6,1.4), '15', GREEN, 3.2)
V['Пример на числах, не из задачи: основания 4 и 6'] = fig(f"<svg viewBox='0 0 82 48' role='img' aria-label='Пример' style='max-width:360px'>{s}</svg>",
  "4 · 5 : 2 = 10, 6 · 5 : 2 = 15; основание 6 в 3/2 раза длиннее 4, и площадь 15 в 3/2 раза больше 10.")

# 7. порядок поиска площадей: известна S(APC); ① ABC, ② PBC, ③ PQC — номера разделов
H = (6, 0)
s = full() + tri_('APC', 0.5) + hgt(PT['C'], H, 'высота из C', 9.5, 0)
s += outline(['A','B','C'], GOLD, 0.9)
s += at((3.4,6.0), '48', 0, 1.2, LAB, 3.4) + at((17.5,15.5), '? ① ABC', 0, 0, GOLD, 3.0)
s += at((15.2,2.4), '? ②', 0, 1.2, LAB, 3.2) + at((9.4,9.6), '? ③', 0, 1.2, LAB, 3.2) + names()
V['S(APC) = 48 → S(ABC) → S(PBC)'] = fig(svg(s, 'Порядок поиска площадей', '-8 -6 96 86'),
  f"Площадь {cname('APC')} известна; номер — раздел, где найдём площадь: ① весь ABC, ② PBC (всё правее PC), ③ PQC (PQR и RQC вместе).")

# 8. раздел 1: APC и ABC — одна высота из C
s = full() + tri_('APC', 0.5) + outline(['A','B','C'], GOLD, 0.9) + hgt(PT['C'], H, 'h', 2.2, 0)
s += line(PT['A'], PT['P'], RED, 1.4) + at((2,0), 'AP', 0, 4.6, RED) + at((14,0), 'AB = 6 AP', 0, 4.6, GOLD) + names()
V['общая высота из C'] = fig(svg(s, 'APC и ABC, высота из C', '-8 -6 90 90'),
  f"{cname('APC')} и <b style='color:{GOLD}'>ABC</b>: вершина C общая, высота h одна, основания AP и AB.")

# 9. раздел 3: PQC и PBC — одна высота из P
F = foot(PT['P'], PT['B'], PT['C'])
s = full() + fill(['P','Q','C'], GREEN, 0.35) + outline(['P','B','C'], GOLD, 0.9) + hgt(PT['P'], F, 'h', -1.0, -2.0)
s += line(PT['Q'], PT['C'], GREEN, 1.4) + at((12.75,15), 'QC', 4.2, 0, GREEN) + at((21.75,3), 'BQ', 4.2, 0, GOLD) + names()
V['перпендикуляр из P на прямую BC'] = fig(svg(s, 'PQC и PBC, высота из P'),
  f"<b style='color:{GREEN}'>PQC</b> и <b style='color:{GOLD}'>PBC</b>: вершина P общая, высота h одна, основания QC и BC.")

# 10–12. сборка: спрошенное и его целое, общая высота
F = foot(PT['A'], PT['B'], PT['C'])
s = full() + tri_('ABQ', 0.45) + line(PT['A'], PT['Q'], VIO, 0.9, True) + outline(['A','B','C'], GOLD, 0.9) + hgt(PT['A'], F, 'h', -1.0, -2.2) + names()
V['ABQ и ABC: общая высота из A'] = fig(svg(s, 'ABQ и ABC, высота из A'),
  f"{cname('ABQ')} и <b style='color:{GOLD}'>ABC</b>: высота h из A, основания BQ и BC.")
F = foot(PT['Q'], PT['P'], PT['C'])
s = full() + tri_('PQR', 0.5) + outline(['P','Q','C'], GOLD, 0.9) + hgt(PT['Q'], F, 'h', 0, -1.6) + names()
V['PQR и PQC: общая высота из Q'] = fig(svg(s, 'PQR и PQC, высота из Q'),
  f"{cname('PQR')} и <b style='color:{GOLD}'>PQC</b>: высота h из Q, основания PR и PC.")
F = foot(PT['B'], PT['P'], PT['C'])
s = full() + tri_('BPR', 0.45) + line(PT['B'], PT['R'], VIO, 0.9, True) + outline(['P','B','C'], GOLD, 0.9) + hgt(PT['B'], F, 'h', 0, 3.4) + names()
V['BPR и PBC: общая высота из B'] = fig(svg(s, 'BPR и PBC, высота из B'),
  f"{cname('BPR')} и <b style='color:{GOLD}'>PBC</b>: высота h из B, основания PR и PC.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
