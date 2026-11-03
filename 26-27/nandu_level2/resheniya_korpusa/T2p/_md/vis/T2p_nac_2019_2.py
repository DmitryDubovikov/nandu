import json, sys
# Рисунки к Т2′ национал 2019 день I №2. Координаты задачи — в см (y вверх): A = (0, 0), B = (180, 0), C = (90, 120), T = (0, −75).
# SVG: X = x : 2, Y = (125 − y) : 2. Сетки нет: кирпич x = CM : 10 только на CM.
def xy(p): return round(p[0] / 2, 2), round((125 - p[1]) / 2, 2)
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
SHADE = '#8a96a3'

PT = {'A':(0,0),'B':(180,0),'C':(90,120),'M':(90,0),'R':(108,0),'S':(132,0),'D':(90,60),'E':(90,24),'T':(0,-75)}
OFF = {'A':(-3.4,1.2),'B':(3.4,1.2),'C':(0,-1.8),'M':(-2.4,4.2),'R':(0.6,-1.8),'S':(2.6,-1.8),'D':(-3.0,-1.4),
       'E':(-2.8,3.4),'T':(-2.6,3.6)}
ALL = list(PT)
SH = ['A','D','S','T','R','E']   # закрашенная фигура

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
def svg(inner, label, vb='-8 -3 108 108'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
def T(*n): return [PT[k] for k in n]
def full(col=DIM, w=0.45):   # весь чертёж условия: ABC, CM, AT, BT, AD, AE, DS, ER, TR, TS
    P_ = PT
    s = poly(T('A','B','C'), col, w) + line(P_['C'],P_['M'],col,w)
    s += line(P_['A'],P_['T'],col,w) + line(P_['T'],P_['B'],col,w)
    for a, b in (('A','D'),('A','E'),('D','S'),('E','R'),('T','R'),('T','S')):
        s += line(P_[a],P_[b],col,w)
    return s
def names(): return labels(ALL, MUT)
def tri(pts, col, op=0.45): return poly(pts, col, 1.0, col, op)
def xmark():   # кирпич x — десятая часть CM, под D
    return line((90,60),(90,48),GOLD,1.6) + at((90,54), 'x', -2.4, 1.0, GOLD, 3.2)
V = {}
# 1. рисунок условия
s = poly(T(*SH), SHADE, 0.5, SHADE, 0.55) + full(INK, 0.55) + labels(ALL)
V['чтобы CM и её части DM, DE, EM были целыми кирпичами'] = fig(svg(s, 'Рисунок условия'), 'Рисунок из условия.')

# 2. буквы: x = CM : 10 на CM
s = full() + line(PT['D'],PT['E'],GOLD,1.0) + line(PT['C'],PT['D'],GOLD,1.0) + xmark()
s += line(PT['M'],PT['E'],GOLD,1.0)
s += at((90,42), '3x', 3.6, 1.0) + at((90,90), '5x', 3.6, 1.0) + at((90,12), '2x', 3.6, 1.0) + names()
V['x = CM : 10; на CM: DM = 5x, DE = 3x, EM = 2x.'] = fig(svg(s, 'Буквы'),
  "<b style='color:#f0a83c'>x</b> = CM : 10; CD = DM = 5x, DE = 3x, EM = 2x.")

# 3. а) периметр ATBC
s = full() + poly(T('A','T','B','C'), GOLD, 1.2)
s += at((0,-37.5), 'AT', -4.0, 1.0) + at((90,-37.5), 'BT', 3.0, 4.2) + at((135,60), 'BC', 4.0, -0.6) + at((45,60), 'AC', -4.0, -0.6)
s += names()
V['C стоит над серединой AB ⇒ равны AC и BC.'] = fig(svg(s, 'Контур ATBC'), 'а) периметр ATBC: AT + TB + BC + CA.')

# 4. б) закрашенная = ADS без AER + RST
s = full() + tri(T('A','D','S'), GOLD, 0.35) + tri(T('A','E','R'), BLUE, 0.3) + tri(T('R','S','T'), GREEN, 0.45)
s += line(PT['D'],PT['M'],GOLD,0.9,True) + at((90,42), '5x', 3.6, 1.0) + at((90,6), '2x', -3.4, 1.0, BLUE)
s += at((0,-37.5), 'AT', -4.0, 1.0, GREEN) + line(PT['A'],PT['T'],GREEN,0.9,True) + names()
V['высота RST равна AT.'] = fig(svg(s, 'Закрашенная фигура: ADS без AER и RST'),
  "б) площадь закрашенной: <b style='color:#f0a83c'>ADS</b> без <b style='color:#5ba8f5'>AER</b> и <b style='color:#5fd38d'>RST</b>.")

# 5. в) ATRC = ATR + ARC
s = full() + tri(T('A','T','R'), BLUE, 0.4) + tri(T('A','R','C'), GOLD, 0.35)
s += line(PT['C'],PT['M'],GOLD,0.9,True) + at((90,96), '10x', -4.6, 1.0) + at((0,-37.5), 'AT', -4.0, 1.0, BLUE)
s += at((54,0), 'AR', 0, 4.2, BLUE) + names()
V['и треугольник ARC с основанием AR и высотой CM = 10x.'] = fig(svg(s, 'ATRC из двух треугольников'),
  "в) площадь ATRC: <b style='color:#5ba8f5'>ATR</b> и <b style='color:#f0a83c'>ARC</b>.")

# 6. г) DMTS = DMS + MTS
s = full() + tri(T('D','M','S'), GOLD, 0.4) + tri(T('M','T','S'), BLUE, 0.4)
s += at((90,36), '5x', 3.6, 1.0) + at((111,0), 'MS', 0, 4.2) + at((0,-37.5), 'AT', -4.0, 1.0, BLUE)
s += line(PT['A'],PT['T'],BLUE,0.9,True) + names()
V['и треугольник MTS с основанием MS и высотой AT.'] = fig(svg(s, 'DMTS из двух треугольников'),
  "г) площадь DMTS: <b style='color:#f0a83c'>DMS</b> и <b style='color:#5ba8f5'>MTS</b>.")

# 7. раздел «Найдём AC»: контур ABC
s = full() + poly(T('A','B','C'), RED, 1.2) + at((45,60), 'AC', -4.0, -0.6, RED) + at((135,60), 'AC', 4.0, -0.6, RED)
s += at((150,0), 'AC + 30', 0, 4.2, RED) + names()
V['периметр ABC — сумма сторон AB, BC и CA.'] = fig(svg(s, 'Контур ABC'), 'Треугольник ABC, периметр 480.')

# 8. раздел «Отрезки на AB»
s = full() + line((0,0),(90,0),VIO,1.4) + line((90,0),(108,0),BLUE,1.4) + line((108,0),(132,0),RED,1.4)
s += line((132,0),(180,0),GREEN,1.4)
s += at((45,0), '90', 0, 4.2, VIO) + at((99,0), '18', 0, 4.2, BLUE) + at((120,0), '24', 0, 4.2, RED) + at((156,0), '48', 0, 4.2, GREEN)
s += names()
V['MS = MR + RS = 18 + 24 = 42'] = fig(svg(s, 'Отрезки на AB'),
  "AM = <b style='color:#c58af9'>90</b>, MR = <b style='color:#5ba8f5'>18</b>, RS = <b style='color:#f2686c'>24</b>, SB = <b style='color:#5fd38d'>48</b>.")

# 9. раздел «Найдём x»: EM = RS
s = full() + line(PT['E'],PT['M'],RED,1.4) + line(PT['R'],PT['S'],RED,1.4)
s += at((90,12), '2x', -3.4, 1.0, RED) + at((120,0), '24', 0, 4.2, RED) + names()
V['EM = 2x, а RS = 24 из раздела 2.'] = fig(svg(s, 'EM = RS'), 'EM = RS: 2x = 24.')

# 10. раздел «Найдём AT и BT»
s = full() + line(PT['A'],PT['T'],BLUE,1.4) + line(PT['T'],PT['B'],RED,1.4) + line(PT['C'],PT['M'],GOLD,1.2)
s += at((0,-37.5), '75', -3.6, 1.0, BLUE) + at((90,-37.5), 'BT', 3.0, 4.2, RED) + at((90,90), '10x', 4.4, 1.0) + names()
V['а MC = 10x.'] = fig(svg(s, 'AT и BT'),
  "BT = <b style='color:#5ba8f5'>AT</b> + <b style='color:#f0a83c'>MC</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
