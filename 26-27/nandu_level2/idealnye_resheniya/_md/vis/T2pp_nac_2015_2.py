import json, sys
# Рисунки к Т2″ национал 2015 день I №2. Координаты задачи — в кирпичах x (y вверх):
# A = (0, 0), O = (4, 0), D = (9, 0), E = (9, 6), C = (9, −4), B = (5, −4).  SVG: X = U·x, Y = U·(6 − y).
U = 7
def xy(p): return round(U*p[0], 2), round(U*(6-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'O':(4,0),'D':(9,0),'E':(9,6),'C':(9,-4),'B':(5,-4)}
OFF = {'A':(-3.4,1.2),'O':(-2.4,4.6),'D':(3.4,1.2),'E':(3.2,-1.2),'C':(3.2,3.6),'B':(-1.0,4.8)}
ALL = ['A','O','D','E','C','B']
SEG = [('A','E'),('O','E'),('D','E'),('A','O'),('O','D'),('A','B'),('O','B'),('O','C'),('B','C'),('C','D')]

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
def svg(inner, label, vb='-9 -7 82 84'): return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner, cap, fx=False): return f"<figure class='st{' fx' if fx else ''}'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def fill(pts, col, op=0.4): return poly([PT[n] for n in pts], col, 1.0, col, op)
def outline(pts, col, w=1.1): return poly([PT[n] for n in pts], col, w)
def rangle(p, sx, sy, col=INK, s=0.7):   # прямой угол в вершине p, стороны по направлениям sx, sy
    a, b, c = (p[0]+sx*s, p[1]), (p[0]+sx*s, p[1]+sy*s), (p[0], p[1]+sy*s)
    return f"<polyline points='{'%s,%s' % xy(a)} {'%s,%s' % xy(b)} {'%s,%s' % xy(c)}' fill='none' stroke='{col}' stroke-width='0.4'/>"
def tick(p, vertical, col=GOLD):   # штрих равенства посередине отрезка
    a, b = ((p[0], p[1]-0.35), (p[0], p[1]+0.35)) if vertical else ((p[0]-0.35, p[1]), (p[0]+0.35, p[1]))
    return line(a, b, col, 0.6)
def ticks(col=GOLD): return tick((2,0), True, col) + tick((7,-4), True, col) + tick((9,-2), False, col)

V = {}
# цвет треугольника — один во всех рисунках
TC = {'AOE': RED, 'ODE': GREEN, 'AOB': BLUE, 'OBC': GOLD, 'CDO': VIO}
TP = {'AOE': ['A','O','E'], 'ODE': ['O','D','E'], 'AOB': ['A','O','B'], 'OBC': ['O','B','C'], 'CDO': ['C','D','O']}
def tri_(n, op=0.42): return fill(TP[n], TC[n], op)
def cname(n): return f"<b style='color:{TC[n]}'>{n}</b>"
def hgt(a, b, lab, dx=0, dy=0):   # высота пунктиром с подписью
    (x1,y1),(x2,y2) = xy(a), xy(b)
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{LAB}' stroke-width='0.7' stroke-dasharray='1.4 1.1'/>"
            + at(((a[0]+b[0])/2, (a[1]+b[1])/2), lab, dx, dy, LAB, 2.8))

# 1. рисунок условия
V['Чему равна площадь BCEO?'] = fig(svg(full(INK, 0.55) + labels(ALL), 'Рисунок условия'), 'Рисунок из условия.')

# 2. посылки: прямые углы, высота ED и расстояние CD между параллельными
s = full(INK, 0.5) + rangle(PT['D'], -1, 1, GOLD) + rangle(PT['D'], -1, -1, GOLD) + rangle(PT['C'], -1, 1, GOLD)
s += line(PT['D'],PT['E'],GOLD,1.1) + line(PT['C'],PT['D'],GOLD,1.1) + at((9,3), 'ED', 4.4, 1.0) + at((9,-2), 'CD', 4.4, 1.0) + labels(ALL)
V['ED — высота из E на прямую AD'] = fig(svg(s, 'Прямые углы, высоты'), "Углы при C и D прямые; <b style='color:#f0a83c'>ED</b> и <b style='color:#f0a83c'>CD</b> перпендикулярны AD.")

# 3. пять треугольников
CEN = {'AOE': (4.3,2.0), 'ODE': (7.3,2.0), 'AOB': (3.0,-1.4), 'OBC': (6.0,-2.7), 'CDO': (7.9,-1.2)}
s = full(INK, 0.5) + ''.join(tri_(n) for n in TC) + ''.join(at(CEN[n], n, 0, 1.0, LAB, 2.6) for n in TC) + labels(ALL)
V['отрезки разрезают чертёж на пять треугольников'] = fig(svg(s, 'Пять треугольников'), '')

# 4–7. каждое спрошенное — из каких треугольников
for anc, parts in (('CEO состоит из CDO и ODE', ['CDO','ODE']), ('ADE состоит из AOE и ODE', ['AOE','ODE']),
                   ('ABCD состоит из AOB, OBC и CDO', ['AOB','OBC','CDO']), ('BCEO состоит из OBC, CDO и ODE', ['OBC','CDO','ODE'])):
    s = full() + ''.join(tri_(n, 0.5) for n in parts) + names()
    V[anc] = fig(svg(s, anc), ' + '.join(cname(n) for n in parts))

# 8. врезка: пример на числах — основания 4 и 6, общая высота 5
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

# 9. раздел 1: CDO и AOB — одна высота CD
s = full() + tri_('AOB', 0.5) + tri_('CDO', 0.5) + hgt(PT['B'], (5,0), 'CD', 3.4, 1.0)
s += line(PT['C'],PT['D'],GOLD,1.1) + at((9,-2), 'CD', 4.4, 1.0) + at((2,0), 'AO', 0, -1.5, BLUE) + at((6.5,0), 'OD', 0, -1.5, VIO) + names()
V['основания OD и AO есть ещё у треугольников CDO и AOB'] = fig(svg(s, 'CDO и AOB, высота CD'),
  f"{cname('CDO')} и {cname('AOB')}: высота у обоих CD, основания OD и AO.")
# 10. порядок поиска площадей: известна S(ODE); ① AOE, ② AOB, ③ CDO, ④ OBC — номера разделов
s = full() + ''.join(tri_(n, 0.45) for n in TC)
s += line(PT['E'],PT['D'],GOLD,1.6) + at((9,3), 'высота ED', 9.0, 1.0, GOLD, 2.8)
s += at((7.6,1.6), '735', 0, 1.2, LAB, 3.4) + at((4.6,1.9), '? ①', 0, 1.2, LAB, 3.4) + at((3.0,-1.3), '? ②', 0, 1.2, LAB, 3.4)
s += at((7.9,-1.2), '? ③', 0, 1.2, LAB, 3.4) + at((6.0,-2.7), '? ④', 0, 1.2, LAB, 3.4) + names()
V['S(ODE) = 735 → S(AOE) → S(AOB)'] = fig(svg(s, 'Порядок поиска площадей', '-9 -7 92 84'),
  f"Площадь {cname('ODE')} известна; номер в треугольнике — раздел, где найдём его площадь: ① {cname('AOE')}, ② {cname('AOB')}, ③ {cname('CDO')}, ④ {cname('OBC')}.")

# 11. раздел 4: OBC и AOB — равные основания, одна высота
s = full() + tri_('AOB', 0.5) + tri_('OBC', 0.5) + hgt(PT['B'], (5,0), 'CD', 3.4, 1.0) + hgt(PT['O'], (4,-4), 'CD', -3.6, 1.0)
s += line(PT['A'],PT['O'],GOLD,1.0) + line(PT['B'],PT['C'],GOLD,1.0) + tick((2,0), True) + tick((7,-4), True) + names()
V['у треугольников OBC и AOB одна высота CD'] = fig(svg(s, 'OBC и AOB'),
  f"{cname('AOB')} и {cname('OBC')}: основания AO = BC, высота у обоих CD.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
