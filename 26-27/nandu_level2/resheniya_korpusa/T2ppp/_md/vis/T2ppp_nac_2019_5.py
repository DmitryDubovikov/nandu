import json, sys
# Рисунки к Т2‴ национал 2019 день II №5. Координаты задачи — в кирпичах x (y вверх), A = (0, 0), C = (6, 5), O = (8, 9).
# SVG: X = 7x, Y = 7(9 − y).
U = 7
def xy(p): return U*p[0], U*(9-p[1])
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(6,0),'C':(6,5),'D':(0,5),'S':(8,0),'T':(8,5),'O':(8,9),'P':(0,2),'R':(6,2)}
LABPOS = {'A':(-3.2,67),'B':(42,68.4),'S':(59.6,67.4),'C':(39.4,25.6),'T':(59.8,29.2),'O':(56,-2.8),
          'D':(-3.4,26.4),'P':(-3.8,50.2),'R':(45.4,47.6)}
# отрезки чертежа условия
SEGS = [('A','B'),('B','C'),('C','D'),('D','A'),('P','R'),((2,2),(2,5)),((4,2),(4,5)),((3,0),(3,2)),
        ('B','S'),('S','T'),('T','C'),('T','O'),('D','O'),('C','O')]
def P_(p): return PT[p] if isinstance(p, str) else p

def line(a, b, col, w=0.5, dash=False):
    (x1,y1),(x2,y2) = xy(P_(a)), xy(P_(b))
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(pts, col, w=0.6, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(P_(p)) for p in pts)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def grid(col='#3e4b58', w=0.3):   # сетка с шагом x — только внутри ABCD
    return ''.join(line((i,0),(i,5),col,w) for i in range(1,6)) + ''.join(line((0,j),(6,j),col,w) for j in range(1,5))
def drawing(col=INK, w=0.6):
    return ''.join(line(a, b, col, w) for a, b in SEGS)
def labels(names=None, col=LAB, dots=True):
    names = names or list(PT)
    s = ''.join(txt(*LABPOS[n], n, col) for n in names)
    if dots: s += ''.join(f"<circle cx='{xy(PT[n])[0]}' cy='{xy(PT[n])[1]}' r='0.75' fill='{col}'/>" for n in names)
    return s
def svg(inner, label, vb='-9 -8 78 82'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def lab(p, s, dx=0, dy=0, col=GOLD, size=3.0):
    X, Y = xy(p); return txt(X+dx, Y+dy, s, col, size)
def xmark():   # кирпич x — половина AP, у вершины A
    return line((0,0),(0,1),GOLD,1.4) + lab((0,0.5), 'x', 2.4, 1.0, GOLD, 3.2)
def base(): return grid() + drawing(DIM, 0.5) + labels(col=MUT)

V = {}
# 1. рисунок условия — как в оригинале
V['три стоячие детали'] = fig(svg(drawing() + labels(), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: кирпич x, стороны деталей 2x и 3x
s = grid('#5c6b7a', 0.3) + drawing(DIM, 0.5) + labels(col=MUT)
s += poly([(0,2),(2,2),(2,5),(0,5)], GOLD, 1.0, GOLD, 0.18) + poly([(0,0),(3,0),(3,2),(0,2)], GOLD, 1.0, GOLD, 0.18)
s += lab((1,5), '2x', 0, 4.2) + lab((0,3.5), '3x', 4.0, 1.0) + lab((1.5,0), '3x', 0, -1.6) + lab((3,1), '2x', -3.6, 1.0)
s += xmark()
V['x — кирпич: короткая сторона детали'] = fig(svg(s, 'Буквы'),
  "Кирпич <b style='color:#f0a83c'>x</b>; у детали стороны 2x и 3x.")

# 3–6. из каких фигур состоит каждое спрошенное
Q = BLUE   # неизвестные пока CT = BS и TO
def unk_ct(): return line('C','T',Q,1.3) + lab((7,5), '?', 0, -1.4, Q, 3.2)
def unk_to(): return line('T','O',Q,1.3) + lab((8,7), '?', 3.0, 1.0, Q, 3.2)
def unk_bs(): return line('B','S',Q,1.3) + lab((7,0), '?', 0, 4.2, Q, 3.2)
# а) BSOC = BSTC + CTO
s = base() + poly(['B','S','T','C'], GOLD, 0.9, GOLD, 0.30) + poly(['C','T','O'], GOLD, 0.9, GOLD, 0.55)
s += line('B','C',GOLD,1.2) + lab((6,3.8), '5x', -3.6, 1.0) + unk_ct() + unk_to() + xmark()
V['BSOC — прямоугольник BSTC'] = fig(svg(s, 'BSOC'), '')
# б) PSC = ASTD без PAS, STC, CDP
s = base() + poly(['A','S','T','D'], GOLD, 1.0) + poly(['P','S','C'], VIO, 1.0, VIO, 0.35)
for t in (['P','A','S'], ['S','T','C'], ['C','D','P']): s += poly(t, RED, 0.6, RED, 0.22)
s += lab((0,1), '2x', -3.6, 1.0) + lab((0,3.5), '3x', -3.6, 1.0) + lab((3,0), '6x', 0, 4.2) + lab((3,5), '6x', 0, -1.4)
s += lab((8,2.5), '5x', 3.8, 1.0) + unk_bs() + unk_ct() + xmark()
V['PSC не прямоугольный треугольник'] = fig(svg(s, 'PSC', '-9 -8 79 82'),
  "<b style='color:#f0a83c'>ASTD</b> без <b style='color:#f2686c'>трёх прямоугольных треугольников</b>.")
# в) DBO = DBSO без BSO; DBSO = DCB + BSTC + DTO
s = base() + poly(['D','C','B'], GOLD, 0.8, GOLD, 0.40) + poly(['B','S','T','C'], GOLD, 0.8, GOLD, 0.25) + poly(['D','T','O'], GOLD, 0.8, GOLD, 0.40)
s += poly(['B','S','O'], RED, 0.8, RED, 0.30) + poly(['D','B','O'], VIO, 1.3)
s += lab((3,5), '6x', 0, 4.2) + lab((0,3.8), '5x', -3.6, 1.0) + unk_bs() + unk_ct() + unk_to() + xmark()
V['DBSO — треугольник DCB'] = fig(svg(s, 'DBO'),
  "<b style='color:#c58af9'>DBO</b> = <b style='color:#f0a83c'>DCB + BSTC + DTO</b> без <b style='color:#f2686c'>BSO</b>.")
# г) ARTOD = APR + PRCD + RTC + DTO
s = base() + poly(['A','P','R'], GOLD, 0.8, GOLD, 0.45) + poly(['P','R','C','D'], BLUE, 0.8, BLUE, 0.25)
s += poly(['R','T','C'], GOLD, 0.8, GOLD, 0.45) + poly(['D','T','O'], GOLD, 0.8, GOLD, 0.30) + poly(['A','R','T','O','D'], VIO, 1.3)
s += lab((0,1), '2x', -3.6, 1.0) + lab((0,3.5), '3x', -3.6, 1.0) + lab((3,2), '6x', 0, -1.4) + lab((6,3.5), '3x', -3.6, 1.0)
s += unk_ct() + unk_to() + xmark()
V['ARTOD — прямоугольные треугольники'] = fig(svg(s, 'ARTOD'), '')

# 7. раздел «Найдём BS»
s = base() + poly(['A','B','C','D'], GOLD, 1.0, GOLD, 0.12) + poly(['B','S','T','C'], RED, 1.0, RED, 0.35)
s += lab((3,0), '6x', 0, 4.2) + lab((0,3.8), '5x', -3.6, 1.0) + lab((6,3.8), '5x', 3.6, 1.0) + unk_bs() + xmark()
V['BSTC — прямоугольник со сторонами BS и BC'] = fig(svg(s, 'BSTC и ABCD'),
  "<b style='color:#f2686c'>BSTC</b> — треть <b style='color:#f0a83c'>ABCD</b>.")
# 8. раздел «Найдём TO»
s = base() + poly(['D','T','O'], GOLD, 0.9, GOLD, 0.40) + poly(['C','T','O'], RED, 0.9, RED, 0.45) + poly(['D','C','O'], VIO, 1.3)
s += lab((3,5), '6x', 0, 4.2) + lab((7,5), '2x', 0, 4.2) + unk_to() + xmark()
V['Заметим, что DCO — это прямоугольный треугольник DTO'] = fig(svg(s, 'DCO = DTO без CTO'),
  "<b style='color:#c58af9'>DCO</b> = <b style='color:#f0a83c'>DTO</b> без <b style='color:#f2686c'>CTO</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
