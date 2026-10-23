import json, sys
# координаты задачи (y вверх) → SVG (y вниз): Y = 48 − y
P = {'A':(0,0),'B':(30,0),'C':(66,0),'F':(0,12),'G':(15,12),'H':(30,12),'E':(15,48),'D':(30,48)}
def xy(n): x,y=P[n]; return x, 48-y
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB='#cfdae6','#4a5866','#e8eef6'
SEGS=[('A','C'),('A','F'),('F','H'),('F','E'),('E','D'),('E','G'),('D','B'),('D','C')]
LABPOS={'A':(-3.5,52.5),'B':(30,53.8),'C':(69.5,52.5),'F':(-3.8,37),'G':(15,40.6),'H':(33.6,38),'E':(15,-2.6),'D':(30,-2.6)}
def line(a,b,col,w=0.6,dash=False):
    (x1,y1),(x2,y2)=xy(a),xy(b)
    d=" stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def poly(names,col,w=1.3,fill='none',op=1):
    pts=' '.join('%s,%s'%xy(n) for n in names)
    return f"<polygon points='{pts}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'/>"
def txt(x,y,s,col=LAB,size=3.6):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def base(col=INK, w=0.6):
    return ''.join(line(a,b,col,w) for a,b in SEGS)
def labels(col=LAB):
    return ''.join(txt(*LABPOS[n],n,col) for n in P)+''.join(f"<circle cx='{xy(n)[0]}' cy='{xy(n)[1]}' r='0.8' fill='{col}'/>" for n in P)
def right_angles(col=INK):
    return f"<path d='M12.6 36V33.6H15M30 45.6H32.4V48' fill='none' stroke='{col}' stroke-width='0.45'/>"
def svg(inner,label,vb='-10 -8 88 66'):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner,cap): return f"<figure class='st'>{inner}<figcaption>{cap}</figcaption></figure>"
def grid(cells,cap):
    c=''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s,t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>",cap)

V={}
# 1. рисунок условия
V['Чему равна площадь BCD?']=fig(svg(base()+right_angles()+labels(),'Рисунок условия'),
  'Рисунок из условия. ABHF и DEGH — прямоугольники, EFG и BCD — прямоугольные треугольники (прямые углы в G и B). G — середина FH; B, H, D — на одной вертикали.')
# 2. буквы
s=base(DIM,0.5)
for a,b in [('F','G'),('G','H'),('E','D'),('A','B')]: s+=line(a,b,GOLD,1.4)
for a,b in [('A','F'),('B','H')]: s+=line(a,b,BLUE,1.4)
for a,b in [('E','G'),('H','D'),('B','C')]: s+=line(a,b,GREEN,1.4)
s+=txt(7.5,39.6,'m',GOLD)+txt(22.5,39.6,'m',GOLD)+txt(22.5,3.6,'m',GOLD)+txt(15,53.8,'2m',GOLD)
s+=txt(-4.4,43.4,'a',BLUE)+txt(33.2,43.4,'a',BLUE)
s+=txt(11.8,19,'h',GREEN)+txt(27,19,'h',GREEN)+txt(48,53.8,'h',GREEN)+labels('#93a1b1')
V['Буквы на рисунке.']=fig(svg(s,'Буквы'),
  "<b style='color:#f0a83c'>m</b> — FG = GH = DE, поэтому AB = FH = 2m; <b style='color:#5ba8f5'>a</b> — AF = BH; <b style='color:#5fd38d'>h</b> — EG = DH, и BC = DH по условию.")
# 3. склейка
lab=labels('#93a1b1')
c1=svg(base(DIM,0.5)+poly('ABHF',GOLD)+line('F','H',RED,1.6)+lab,'Контур ABHF')
c2=svg(base(DIM,0.5)+poly('DEFH',BLUE)+line('F','H',RED,1.6)+lab,'Контур DEFH')
c3=svg(base(DIM,0.5)+poly('ABDEF',GREEN)+line('F','H',RED,1.2,True)+lab,'Контур ABDEF')
V['дают ABDEF (144)']=grid([(c1,'P(ABHF) = 84'),(c2,'P(DEFH) = 120'),(c3,'P(ABDEF) = 144')],
  "Красная FH входит и в обход ABHF, и в обход DEFH; в обходе ABDEF её нет — она внутри фигуры. Поэтому из суммы вычитаем 2 · FH.")
# 4. спрошенные периметры — по рисунку на вопрос
a1=svg(base(DIM,0.5)+poly('DEGH',BLUE)+poly('EFG',GOLD)+line('E','G',RED,1.6)+txt(11.8,19,'h',RED)+lab,'P(EFG)')
V['дают DEFH (120)']=fig(a1,'Красная EG = h есть в обходах EFG и DEGH, в обходе DEFH её нет.')
a2=svg(base(DIM,0.5)+poly('ABDEF',GREEN)+poly('BCD',VIO)+line('B','D',RED,1.6)+txt(25,25,'a + h',RED,3.2)+lab,'P(ACDEF)')
V['склеенные по BD, дают ACDEF']=fig(a2,'Красная BD = a + h есть в обходах ABDEF и BCD, в обходе ACDEF её нет.')
# 5. площади
f1=svg(base(DIM,0.5)+poly('ABHF',BLUE,0.9,BLUE,0.28)+poly('DEGH',GREEN,0.9,GREEN,0.28)+poly('EFG',GOLD,0.9,GOLD,0.28)
       +txt(15,45.6,'2m · a',BLUE,3.2)+txt(22.5,19,'m · h',GREEN,3.2)+txt(10.6,30.5,'m·h:2',GOLD,2.6)+lab,'Площадь ABDEF')
V['складывается из ABHF, DEGH и EFG']=fig(f1,'EFG — половина прямоугольника m × h.')
f2=svg(base(DIM,0.5)+poly('BCD',VIO,0.9,VIO,0.28)+txt(48,53.8,'h',GREEN)+txt(35.6,27,'a + h',VIO,3.2)+lab,'Площадь BCD')
V['половина прямоугольника со сторонами BC и BD']=fig(f2,'BC = h, BD = a + h.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
