import json, sys
# Рисунки к Т2′ национал 2022 день II №5. Координаты задачи — в см (y вверх), F = (0, 0), B = (72, 0), E = (0, 15),
# C = (72, 15), D = (72, 36), A = (72, −54), G — отражение B относительно AF. Чертёж оригинала выдержан в этом масштабе.
# SVG: X = U·x, Y = U(36 − y).
U = 0.8
def xy(p): return round(U*p[0], 2), round(U*(36-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'F':(0,0),'B':(72,0),'E':(0,15),'C':(72,15),'D':(72,36),'A':(72,-54),'G':(20.16,-69.12)}
OFF = {'F':(-3.4,1.2),'B':(3.4,1.6),'E':(-3.2,-1.4),'C':(3.4,1.2),'D':(3.0,-1.4),'A':(3.4,3.2),'G':(-1.6,4.6)}
ALL = list(PT)

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
def svg(inner, label, vb='-9 -6 80 96'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:420px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def full(col=DIM, w=0.45):   # весь чертёж условия
    P_ = PT
    s = line(P_['A'],P_['D'],col,w) + line(P_['D'],P_['E'],col,w) + line(P_['E'],P_['C'],col,w)
    s += line(P_['E'],P_['F'],col,w) + line(P_['F'],P_['B'],col,w) + line(P_['F'],P_['A'],col,w)
    s += line(P_['A'],P_['G'],col,w) + line(P_['G'],P_['F'],col,w)
    return s
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def T(*n): return [PT[k] for k in n]
def xmark():   # кирпич x — отрезок EF
    return line(PT['E'],PT['F'],GOLD,1.4) + at((0,7.5), 'x', -3.4, 1.0, GOLD, 3.2)
def dimAD(col=GOLD, s='6x'):   # размер AD выноской справа, чтобы не мешать подписям C и B
    return (line((82,-54),(82,36),col,0.5) + line((80,-54),(84,-54),col,0.5) + line((80,36),(84,36),col,0.5)
            + at((82,-9), s, 3.6, 1.0, col))
L_AF = lambda col=GOLD, s='6x': at((36,-27), s, 3.6, -1.6, col)          # над AF, внутри ABF
L_DE = lambda col=GOLD, s='5x': at((36,25.5), s, -1.0, -2.4, col)        # над DE
L_FB = lambda col=RED: at((36,0), 'FB', 0, 3.8, col, 2.8)                 # под FB
L_CE = lambda col=RED: at((36,15), 'FB', 0, 3.8, col, 2.8)                # под EC, внутри BCEF
L_CD = lambda col=RED: at((72,25.5), 'CD', -4.4, 1.0, col, 2.8)           # слева от CD
L_BC = lambda col=GOLD: at((72,7.5), 'x', -2.6, 1.0, col, 3.2)            # слева от BC

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['точки A, B, C, D лежат на одной прямой AD.'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы
s = full() + xmark() + line(PT['B'],PT['C'],GOLD,1.0) + L_BC() + dimAD() + L_AF() + L_DE()
s += line(PT['F'],PT['B'],RED,0.9) + L_FB() + line(PT['C'],PT['D'],RED,0.9) + L_CD() + names()
V['FB и CD — неизвестные отрезки.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = EF; <b style='color:#f2686c'>FB</b> и <b style='color:#f2686c'>CD</b> пока неизвестны.")

# 3. а) периметр ACEF
s = full() + poly(T('A','C','E','F'), GOLD, 1.2)
s += at((72,-19.5), '6x − CD', 7.2, 1.0, GOLD, 2.8) + L_CE(GOLD) + xmark() + L_AF() + names()
V['AC = 6x − CD'] = fig(svg(s, 'Контур ACEF'), 'а) периметр ACEF: AC, CE, EF и FA.')

# 4. б) площадь CDEF = CDE + CEF
s = full() + tri(T('C','D','E'), GOLD, 0.4) + tri(T('C','E','F'), BLUE, 0.4) + line(PT['C'],PT['F'],BLUE,0.8,True)
s += L_CD(GOLD) + at((36,15), 'FB', 0, -1.4, GOLD, 2.8) + at((24,10), '540', 0, 1.0, BLUE, 2.8) + xmark() + names()
V['площадь BEF дана.'] = fig(svg(s, 'CDEF = CDE + CEF'),
  "б) площадь CDEF: <b style='color:#f0a83c'>CDE</b> и <b style='color:#5ba8f5'>CEF</b>; CEF и BEF — половины BCEF.")

# 5. в) площадь ADEFG = трапеция ADEF + AGF, AGF = ABF
s = full() + tri(T('A','D','E','F'), GOLD, 0.35) + tri(T('A','G','F'), BLUE, 0.45) + poly(T('A','B','F'), BLUE, 0.9, 'none', 1)
s += dimAD() + xmark() + line(PT['F'],PT['B'],RED,0.9,True) + L_FB() + names()
s += at((72,-27), '5x − CD', -7.6, 1.0, BLUE, 2.6)
V['AB = AD − BC − CD = 5x − CD'] = fig(svg(s, 'ADEFG = ADEF + AGF'),
  "в) площадь ADEFG: <b style='color:#f0a83c'>трапеция ADEF</b> и <b style='color:#5ba8f5'>AGF</b>, равный ABF.")

# 6. г) площадь ABE: основание AB, высота EC
s = full() + tri(T('A','B','E'), GOLD, 0.4) + line(PT['B'],PT['C'],GOLD,0.8,True) + line(PT['E'],PT['C'],RED,1.0,True)
s += L_CE() + at((72,-27), '5x − CD', 7.6, 1.0, GOLD, 2.6) + xmark() + names()
V['AB = 5x − CD'] = fig(svg(s, 'ABE: основание AB, высота EC'),
  "г) площадь ABE: основание AB, <b style='color:#f2686c'>высота EC</b>.")

# 7. раздел «Найдём x»: ADEF
s = full() + tri(T('A','D','E','F'), RED, 0.3) + dimAD(RED) + L_AF(RED) + L_DE(RED) + at((0,7.5), 'x', -3.4, 1.0, RED, 3.2) + names()
V['стороны ADEF — это'] = fig(svg(s, 'Контур ADEF'), 'Периметр ADEF: 6x + 5x + x + 6x.')

# 8. раздел «Найдём FB»: BEF
s = full() + tri(T('B','E','F'), RED, 0.45) + xmark() + L_FB() + names()
V['BEF — прямоугольный треугольник с катетами'] = fig(svg(s, 'Треугольник BEF'), 'Прямоугольный треугольник BEF.')

# 9. раздел «Найдём CD»: CDE
s = full() + tri(T('C','D','E'), RED, 0.45) + L_CD() + L_DE(RED) + L_CE() + names()
V['стороны CDE — это CD'] = fig(svg(s, 'Треугольник CDE'), 'Стороны CDE: CD, 5x и FB.')

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
