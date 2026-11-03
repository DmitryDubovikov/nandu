import json, sys
# Рисунки к Т2‴ провинциал 2014 №2. Координаты задачи — в см (y вверх), A = (0, 0); масштаб как в оригинале.
# AB = 72, BC = 15, DP = 12, PC = 9, FE по горизонтали тоже 9. SVG: X = x, Y = 27 − y.
P = {'A':(0,0),'B':(72,0),'C':(72,15),'D':(63,27),'E':(9,27),'F':(0,15),'P':(63,15)}
def xy(n): x, y = P[n] if isinstance(n, str) else n; return x, 27-y
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
SEGS = [('A','B'),('B','C'),('C','D'),('D','E'),('E','F'),('F','A'),('F','C'),('D','P')]
LABPOS = {'A':(-3,30.6),'B':(75,30.6),'C':(75.6,13.2),'D':(64.6,-2.2),'E':(7.4,-2.2),'F':(-3.4,13.2),'P':(63,16.6)}

def line(a, b, col, w=0.6, dash=False):
    (x1,y1),(x2,y2) = xy(a), xy(b)
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(names, col, w=1.2, fill='none', op=1):
    s = ' '.join('%s,%s' % xy(n) for n in names)
    return f"<polygon points='{s}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def base(col=INK, w=0.6):
    return ''.join(line(a, b, col, w) for a, b in SEGS)
def right_angle(col=INK):
    return f"<path d='M60.8 12V9.8H63' fill='none' stroke='{col}' stroke-width='0.4'/>"
def labels(col=LAB, dots=True):
    s = ''.join(txt(*LABPOS[n], n, col) for n in P)
    if dots: s += ''.join(f"<circle cx='{xy(n)[0]}' cy='{xy(n)[1]}' r='0.7' fill='{col}'/>" for n in P)
    return s
def svg(inner, label, vb='-8 -8 89 44'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def grid2(cells, cap):
    c = ''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s, t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>", cap)
def xmark():   # кирпич x — первая двенадцатая AB у A
    return line((0,0),(6,0),GOLD,1.5) + txt(3,31.4,'x',GOLD,3.2)
def dim_base(): return base(DIM, 0.5) + right_angle(DIM)

V = {}
# 1. рисунок условия
V['берём кирпич x = AB : 12'] = fig(svg(base() + right_angle() + labels(), 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x — золото, h — синий
s = dim_base() + xmark()
s += txt(40,31.4,'12x',GOLD,3.2) + line('D','E',GOLD,1.3) + txt(36,-1.6,'9x',GOLD,3.2) + line('D','P',GOLD,1.3) + txt(60.2,7.4,'2x',GOLD,3.0)
for a, b in [('B','C'),('C','D'),('E','F')]: s += line(a, b, BLUE, 1.4)
s += txt(75.6,20.4,'h',BLUE) + txt(70.6,4.8,'h',BLUE) + txt(1.6,4.8,'h',BLUE)
s += labels(MUT, False)
V['h = BC = CD = EF.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = AB : 12, тогда DE = 9x, DP = 2x; <b style='color:#5ba8f5'>h</b> = BC = CD = EF.")

# 3. артефакт: каждое спрошенное
lab = labels(MUT, False)
s = dim_base() + poly('ABCF', GOLD, 1.2) + poly('CDEF', BLUE, 1.2) + line('F','C',RED,1.6) + txt(36,10.6,'12x',RED,3.2) + xmark() + lab
V['ещё дважды FC'] = fig(svg(s, 'Периметр ABCDEF'), '')
s = dim_base() + poly('ABCF', GOLD, 1.0, GOLD, 0.3) + txt(40,31.4,'12x',GOLD,3.2) + txt(75.6,20.4,'h',BLUE) + line('B','C',BLUE,1.4) + xmark() + lab
V['прямоугольник со сторонами AB и BC'] = fig(svg(s, 'Площадь ABCF'), '')
s = dim_base() + poly('CDEF', BLUE, 1.0, BLUE, 0.3) + line('F','C',GOLD,1.3) + txt(30,10.6,'12x',GOLD,3.2) + line('D','E',GOLD,1.3) + txt(36,-1.6,'9x',GOLD,3.2)
s += line('D','P',GOLD,1.3) + txt(60.2,7.4,'2x',GOLD,3.0) + xmark() + lab
V['трапеция с основаниями FC и DE'] = fig(svg(s, 'Площадь CDEF'), '')
s = dim_base() + poly('ABCF', GOLD, 1.0, GOLD, 0.3) + poly(['F','C','D'], VIO, 1.0, VIO, 0.35) + txt(40,31.4,'12x',GOLD,3.2)
s += line('B','C',BLUE,1.4) + txt(75.6,20.4,'h',BLUE) + line('D','P',VIO,1.3, True) + txt(60.2,7.4,'2x',VIO,3.0) + xmark() + lab
V['это прямоугольник ABCF и треугольник FCD'] = fig(svg(s, 'Площадь ABCDF'), '')

# 4. раздел «Найдём x и h»: два обхода
s = dim_base() + poly('ABCF', GOLD, 1.3) + txt(40,31.4,'12x',GOLD,3.2) + txt(36,16.4,'12x',GOLD,3.2) + txt(-3.6,20.4,'h',BLUE) + txt(75.6,20.4,'h',BLUE) + lab
V['две стороны по 12x (AB и FC)'] = fig(svg(s, 'Обход ABCF'), 'P(ABCF) = 174.')
s = dim_base() + poly('CDEF', BLUE, 1.3) + txt(36,10.6,'12x',GOLD,3.2) + txt(36,-1.6,'9x',GOLD,3.2) + txt(70.6,4.8,'h',BLUE) + txt(1.6,4.8,'h',BLUE) + lab
V['CD = h, DE = 9x, EF = h, FC = 12x'] = fig(svg(s, 'Обход CDEF'), 'P(CDEF) = 156.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
