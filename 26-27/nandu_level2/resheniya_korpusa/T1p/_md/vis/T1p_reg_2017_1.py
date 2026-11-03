import json, sys
GOLD,BLUE,GREEN='#f0a83c','#5ba8f5','#5fd38d'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def sub(word):   # S с индексом-словом внутри SVG
    return f"S<tspan baseline-shift='sub' font-size='2.6'>{word}</tspan>"
def svg(inner,label,vb,mw=None):
    st=f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# полоса-целое из равных кирпичиков: части подписаны словами сверху и долями снизу;
# brace — скобка под частями с номерами от i до j и подпись под ней
def bar(parts,brace=None,W=120):
    # parts: [(слово, кирпичиков, доля, закрашена ли, цвет)]
    n=sum(p[1] for p in parts); bw=W/n; x=5; s=''; xs=[]
    for word,k,frac,on,col in parts:
        w=k*bw; xs.append((x,x+w))
        for i in range(k):
            s+=f"<rect x='{x+i*bw}' y='8' width='{bw}' height='10' fill='{col}' fill-opacity='{0.28 if on else 0.10}' stroke='{INK if on else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x}' y='8' width='{w}' height='10' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=txt(x+w/2,5.5,word,col,3.4)
        s+=txt(x+w/2,23.5,frac,col,3.4)
        x+=w
    H=27
    if brace:
        i,j,lab=brace; a,b=xs[i][0]+0.5,xs[j][1]-0.5; m=(a+b)/2
        s+=f"<path d='M{a} 26.5V28.5H{b}V26.5M{m} 28.5V30' fill='none' stroke='{GOLD}' stroke-width='0.7'/>"
        s+=txt(m,34.5,lab,GOLD,3.8,'700'); H=37
    return svg(s,'Полоса',f'0 0 {W+10} {H}')

# схема-план: от 37400 к искомым; стрелка = данное из условия; step подсвечивает текущую стрелку
NODES={'37400':(2,4,20,10),'Вс':(40,4,26,10),'П':(86,4,36,10),'S':(142,4,46,10)}
NAME={'37400':'$37400','Вс':'N(всех)','П':'N(проданных)','S':sub('по полной цене')}
ARROWS={1:[('M22 9H39','1/3, 1/5',(31,6.6))],
        2:[('M66 9H85','2/3',(75.5,6.6))],
        3:[('M122 9H141','· 200',(131.5,6.6))]}
TARGET={1:'Вс',2:'П',3:'S'}
def scheme(step=None):
    s=f"<defs><marker id='ah{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done={'37400'}|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ah{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,3.2)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or (n=='37400')) else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col if n!='37400' else GOLD,3.6)
    return svg(s,'Схема решения','0 0 190 18')

V={}
V['запишем 37400 через N(всех)']=fig(scheme(),'План: каждая стрелка — данное из условия.')
V['1. а) Найдём N(всех)']=fig(scheme(1))
V['по полной цене продали остальные 7/15']=fig(bar([('непроданы',5,'1/3 = 5/15',False,BLUE),
    ('за полцены, $100',3,'1/5 = 3/15',True,GREEN),
    ('по полной, $200',7,'7/15 = 1 − 1/3 − 1/5',True,GOLD)],(1,2,'выручка $37400')),
    'Все билеты: пятнадцать равных частей.')
V['2. Найдём N(проданных)']=fig(scheme(2))
V['продали 2/3 всех билетов']=fig(bar([('непроданы',1,'1/3',False,BLUE),('проданы',2,'2/3 = 1 − 1/3',True,GOLD)],W=90),
    'Все 330 билетов: три равные части, проданы две.')
V['3. б) Найдём S_{по полной цене}']=fig(scheme(3))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
