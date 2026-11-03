import json, sys
# Рисунки к Т2′ национал 2018 день II №5. Координаты задачи — в см (y вверх), A = (0, 0), B = (21, 0), C = (84, 0),
# D = (105, 0), M = (21, 24), P = (69, 24), R = (84, 24), G = (21, 72), S = (69, 72), E = (84, 72), F = (69, 108).
# Чертёж оригинала выдержан в этом масштабе. SVG: X = U·x, Y = U(108 − y). FS на чертеже оригинала не проведён.
U = 0.7
def xy(p): return round(U*p[0], 2), round(U*(108-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(0,0),'B':(21,0),'C':(84,0),'D':(105,0),'M':(21,24),'P':(69,24),'R':(84,24),
      'G':(21,72),'S':(69,72),'E':(84,72),'F':(69,108)}
OFF = {'A':(-2.6,3.8),'B':(0,4.4),'C':(0,4.4),'D':(2.8,3.8),'M':(-3.4,1.2),'P':(2.4,3.8),'R':(3.2,3.6),
       'G':(-3.4,-1.2),'S':(-2.4,-1.8),'E':(3.4,-1.4),'F':(0,-2.4)}
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
def svg(inner, label, vb='-8 -6 90 90'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:420px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def full(col=DIM, w=0.45):   # весь чертёж условия
    P_ = PT
    s = line(P_['A'],P_['D'],col,w) + line(P_['D'],P_['E'],col,w) + line(P_['E'],P_['G'],col,w)
    s += line(P_['G'],P_['A'],col,w) + line(P_['G'],P_['F'],col,w) + line(P_['F'],P_['E'],col,w)
    s += line(P_['G'],P_['B'],col,w) + line(P_['E'],P_['C'],col,w) + line(P_['M'],P_['R'],col,w) + line(P_['S'],P_['P'],col,w)
    return s
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def T(*n): return [PT[k] for k in n]
def xmark(col=GOLD):   # кирпич x — сторона квадрата GM
    return line(PT['G'],PT['M'],col,1.4) + at((21,48), 'x', -2.6, 1.0, col, 3.2)
L_BM = lambda col=RED: line(PT['M'],PT['B'],col,1.0) + at((21,12), 'BM', -4.2, 1.0, col, 2.8)
L_SE = lambda col=RED: line(PT['S'],PT['E'],col,1.0) + at((76.5,72), 'SE', 0, 3.8, col, 2.8)
L_CD = lambda col=RED: line(PT['C'],PT['D'],col,1.0) + at((94.5,0), 'CD', 0, -1.6, col, 2.8)
L_PS = lambda col=GOLD: at((69,48), 'x', 2.4, 1.0, col, 3.2)
def dimGE(s='x + SE', col=GOLD):   # выноска GE над прямой GE, левее F
    return at((45,72), s, 0, -1.6, col, 2.8)
def dimBG(s='x + BM', col=GOLD):   # подпись BG справа от G–B, ниже M: слева мешает AG, выше — черта x
    return at((21,13), s, 6.6, 1.0, col, 2.6)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['точки A, B, C, D лежат на одной прямой.'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы
s = full() + xmark() + L_PS() + L_BM() + L_SE() + L_CD() + names()
V['BM, SE и CD — неизвестные отрезки.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = GM — сторона квадрата; <b style='color:#f2686c'>BM</b>, <b style='color:#f2686c'>SE</b> и <b style='color:#f2686c'>CD</b> пока неизвестны.")

# 3. а) GPEF = GPE + GEF
s = full() + tri(T('G','P','E'), GOLD, 0.4) + tri(T('G','E','F'), BLUE, 0.4) + line(PT['S'],PT['P'],GOLD,1.0,True)
s += dimGE() + L_PS() + at((60,84), '¾ · S(GPE)', 0, 1.0, BLUE, 2.6) + xmark() + names()
V['PS перпендикулярна GE как сторона квадрата GMPS.'] = fig(svg(s, 'GPEF = GPE + GEF'),
  "а) площадь GPEF: <b style='color:#f0a83c'>GPE</b> и <b style='color:#5ba8f5'>GEF</b> = ¾ площади GPE.")

# 4. б) BDG: катеты BD и BG
s = full() + tri(T('B','D','G'), GOLD, 0.4)
s += at((63,0), 'x + SE + CD', 0, 8.6, GOLD, 2.8) + line((21,-9),(105,-9),GOLD,0.5)
s += line((21,-7.6),(21,-10.4),GOLD,0.5) + line((105,-7.6),(105,-10.4),GOLD,0.5) + dimBG() + xmark() + names()
V['BD = BC + CD = x + SE + CD'] = fig(svg(s, 'Треугольник BDG', '-8 -6 90 96'),
  "б) площадь BDG: катеты BD и BG.")

# 5. в) AEFG = AEG + GEF
s = full() + tri(T('A','E','G'), GOLD, 0.4) + tri(T('G','E','F'), BLUE, 0.4) + line(PT['A'],PT['E'],GOLD,1.0)
s += line(PT['G'],PT['B'],RED,1.0,True) + at((21,13), 'x + BM', 6.6, 1.0, RED, 2.6) + dimGE() + xmark() + names()
s += at((60,84), '¾ · S(GPE)', 0, 1.0, BLUE, 2.6)
V['Дано: площадь GEF равна 3/4 площади GPE.'] = fig(svg(s, 'AEFG = AEG + GEF'),
  "в) площадь AEFG: <b style='color:#f0a83c'>AEG</b> с <b style='color:#f2686c'>высотой BG</b> и <b style='color:#5ba8f5'>GEF</b>.")

# 6. г) вся фигура = трапеция ADEG + GEF
s = full() + tri(T('A','D','E','G'), GOLD, 0.35) + tri(T('G','E','F'), BLUE, 0.4)
s += at((52.5,0), '2 · CD + x + SE', 0, 4.4, GOLD, 2.6) + dimGE() + dimBG() + xmark() + names()
s += at((60,84), '¾ · S(GPE)', 0, 1.0, BLUE, 2.6)
V['AD = AB + BC + CD = 2 · CD + x + SE'] = fig(svg(s, 'ADEFG = ADEG + GEF'),
  "г) площадь фигуры: <b style='color:#f0a83c'>трапеция ADEG</b> и <b style='color:#5ba8f5'>GEF</b>.")

# 7. раздел «Найдём x»: GMP
s = full() + tri(T('G','M','P'), RED, 0.45) + line(PT['G'],PT['P'],RED,1.0) + xmark(RED) + at((45,24), 'x', 0, 3.8, RED, 3.2) + names()
V['GMP — прямоугольный треугольник с катетами'] = fig(svg(s, 'Треугольник GMP'), 'Прямоугольный треугольник GMP: катеты x и x.')

# 8. раздел «Найдём BM»: BCRM и GPE
s = full() + tri(T('B','C','R','M'), RED, 0.35) + tri(T('G','P','E'), GOLD, 0.35)
s += at((52.5,12), 'BM', 0, 1.0, RED, 2.8) + at((52.5,24), 'x + SE', 0, 3.8, RED, 2.6) + dimGE() + L_PS() + names()
V['BCRM — прямоугольник со сторонами MR и BM'] = fig(svg(s, 'BCRM и GPE'),
  "<b style='color:#f2686c'>BCRM</b> и <b style='color:#f0a83c'>GPE</b>: MR и GE одной длины x + SE.")

# 9. раздел «Найдём SE»: контур BCEG
s = full() + poly(T('B','C','E','G'), RED, 1.2) + dimGE('x + SE', RED) + dimBG('x + BM', RED) + names()
V['BCEG — прямоугольник со сторонами GE = x + SE и BG'] = fig(svg(s, 'Контур BCEG'), 'Периметр BCEG: 2 · (x + SE) + 2 · (x + BM).')

# 10. раздел «Найдём CD»: GMRE и CDE
s = full() + tri(T('G','M','R','E'), RED, 0.3) + tri(T('C','D','E'), GOLD, 0.45)
s += dimGE('x + SE', RED) + xmark(RED) + L_CD(GOLD) + at((84,13), 'x + BM', -6.6, 1.0, GOLD, 2.6) + names()
V['GMRE — прямоугольник со сторонами GE и GM'] = fig(svg(s, 'GMRE и CDE'),
  "<b style='color:#f2686c'>GMRE</b> и <b style='color:#f0a83c'>CDE</b>: катеты CD и CE = x + BM.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
