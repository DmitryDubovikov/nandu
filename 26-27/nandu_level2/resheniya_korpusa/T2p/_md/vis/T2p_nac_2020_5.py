import json, sys
# Рисунки к Т2′ национал 2020 день II №5. Координаты задачи — в см (y вверх), H = (0, 0), AC — ось x:
# A = (−20, 0), G = (−8, 0), J = (16, 0), C = (28, 0), F = (−8, 32), E = (0, 32), D = (16, 32), B = (0, −26).
# Чертёж оригинала выдержан в этом масштабе. SVG: X = U(x + 20), Y = U(32 − y).
U = 1.0
def xy(p): return round(U*(p[0]+20), 2), round(U*(32-p[1]), 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'

PT = {'A':(-20,0),'G':(-8,0),'H':(0,0),'J':(16,0),'C':(28,0),'F':(-8,32),'E':(0,32),'D':(16,32),'B':(0,-26)}
OFF = {'A':(-3.4,1.2),'G':(-2.2,-1.4),'H':(2.4,-1.4),'J':(2.4,-1.4),'C':(3.4,1.2),
       'F':(-2.0,-2.0),'E':(0,-2.4),'D':(2.2,-2.0),'B':(0,4.6)}
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
def svg(inner, label, vb='-7 -6 62 70'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:420px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def full(col=DIM, w=0.45):   # весь чертёж условия
    P_ = PT
    s = line(P_['A'],P_['C'],col,w) + line(P_['F'],P_['D'],col,w) + line(P_['A'],P_['F'],col,w) + line(P_['D'],P_['C'],col,w)
    s += line(P_['F'],P_['G'],col,w) + line(P_['E'],P_['B'],col,w) + line(P_['D'],P_['J'],col,w)
    s += line(P_['A'],P_['B'],col,w) + line(P_['B'],P_['C'],col,w)
    return s
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def T(*n): return [PT[k] for k in n]
def xmark():   # кирпич x — отрезок EF
    return line(PT['F'],PT['E'],GOLD,1.4) + at((-4,32), 'x', 0, -1.6, GOLD, 3.2)
L_GH = lambda col=GOLD: at((-4,0), 'x', 0, 3.4, col, 3.0)          # под GH
L_FG = lambda col=GOLD: at((-8,16), '4x', -3.0, 1.0, col)           # слева от FG
L_EH = lambda col=GOLD: at((0,16), '4x', 3.0, 1.0, col)             # справа от EH
L_DJ = lambda col=GOLD: at((16,16), '4x', 3.0, 1.0, col)            # справа от DJ
L_HJ = lambda col=GOLD: at((8,0), '2x', 0, 3.4, col)                # под HJ
L_ED = lambda col=GOLD: at((8,32), '2x', 0, -1.6, col)              # над ED
L_AG = lambda col=RED: at((-14.5,0), 'AG', 0, -1.4, col, 2.8)         # над AG
L_CJ = lambda col=RED: at((23,0), 'AG', 0, -1.4, col, 2.8)          # над CJ
L_HB = lambda col=RED, dx=3.6: at((0,-13), 'HB', dx, 1.0, col, 2.8)   # справа от HB (в «в)» — слева: справа идёт BD)

V = {}
# 1. рисунок условия
s = full(INK, 0.55) + labels(ALL)
V['точки G, H, J — на AC.'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы
s = full() + xmark() + L_GH() + L_FG() + L_EH() + L_DJ() + L_HJ() + L_ED()
s += line(PT['A'],PT['G'],RED,0.9) + line(PT['J'],PT['C'],RED,0.9) + line(PT['H'],PT['B'],RED,0.9)
s += L_AG() + L_CJ() + L_HB() + names()
V['AG = CJ и HB — неизвестные отрезки.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = EF; <b style='color:#f2686c'>AG</b> = CJ и <b style='color:#f2686c'>HB</b> пока неизвестны.")

# 3. а) периметр DFGJ
s = full() + poly(T('D','F','G','J'), GOLD, 1.2) + at((4,32), '3x', 0, -1.6) + L_FG() + names()
V['FD = FE + ED = x + 2x = 3x'] = fig(svg(s, 'Прямоугольник DFGJ'), 'а) периметр DFGJ: стороны FD = 3x и FG = 4x.')

# 4. б) площадь BCDE = трапеция HCDE + BHC
s = full() + tri(T('H','C','D','E'), GOLD, 0.35) + tri(T('B','H','C'), BLUE, 0.4)
s += L_ED() + L_EH() + at((14,0), '2x + AG', 0, 3.6, GOLD, 2.6) + L_HB(BLUE) + xmark() + names()
V['HC = HJ + JC = 2x + AG'] = fig(svg(s, 'BCDE = HCDE + BHC'),
  "б) площадь BCDE: <b style='color:#f0a83c'>трапеция HCDE</b> и <b style='color:#5ba8f5'>BHC</b>.")

# 5. в) площадь ABD = ABJ + AJD − BJD
s = full() + tri(T('A','B','J'), BLUE, 0.3) + tri(T('A','J','D'), GOLD, 0.3) + tri(T('B','J','D'), RED, 0.35)
s += poly(T('A','B','D'), VIO, 1.2)
s += at((-2,0), 'AG + 3x', -6.0, 3.4, BLUE, 2.6) + L_HB(BLUE, -3.8) + L_DJ(RED) + at((12,0), '2x', 0, 3.4, RED) + xmark() + names()
V['AJ = AG + GH + HJ = AG + 3x'] = fig(svg(s, 'ABD = ABJD без BJD'),
  "в) площадь <b style='color:#c58af9'>ABD</b>: <b style='color:#5ba8f5'>ABJ</b> и <b style='color:#f0a83c'>AJD</b> без <b style='color:#f2686c'>BJD</b>.")

# 6. раздел «Найдём x»: GHE
s = full() + tri(T('G','H','E'), RED, 0.45) + L_GH(RED) + L_EH(RED) + names()
V['GHE — прямоугольный треугольник с катетами'] = fig(svg(s, 'Треугольник GHE'), 'Прямоугольный треугольник GHE.')

# 7. раздел «Найдём AG»: ABC и BJH, общая высота HB
s = full() + tri(T('A','B','C'), GOLD, 0.3) + tri(T('B','J','H'), BLUE, 0.5) + line(PT['H'],PT['B'],RED,1.0,True)
s += L_HB() + L_AG(GOLD) + L_CJ(GOLD) + L_HJ(BLUE) + L_GH() + names()
V['у ABC и BJH одна и та же высота HB'] = fig(svg(s, 'ABC и BJH: общая высота HB'),
  "<b style='color:#f0a83c'>ABC</b> и <b style='color:#5ba8f5'>BJH</b>: основания на AC, <b style='color:#f2686c'>высота HB</b> общая.")

# 8. раздел «Найдём HB»: AGB
s = full() + tri(T('A','G','B'), RED, 0.4) + line(PT['G'],PT['H'],RED,0.8,True) + line(PT['H'],PT['B'],RED,1.0,True)
s += L_AG() + L_HB() + names()
V['у AGB основание AG'] = fig(svg(s, 'AGB: основание AG, высота HB'),
  "AGB: основание AG, <b style='color:#f2686c'>высота HB</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
