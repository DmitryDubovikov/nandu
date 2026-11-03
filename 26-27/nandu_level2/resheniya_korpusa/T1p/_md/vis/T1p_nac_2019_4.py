import json, sys
GOLD,BLUE,GREEN='#f0a83c','#5ba8f5','#5fd38d'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600',anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"
def svg(inner,label,vb,style=''):
    st=f" style='{style}'" if style else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def val(x,y,s,size=4.2):
    return f"<text x='{x}' y='{y}' fill='{LAB}' font-size='{size}' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>{s}</text>"

# полоса-целое из равных кирпичиков: части подписаны словами сверху и долями снизу
def bar(parts):
    n=sum(p[1] for p in parts); W=90; bw=W/n; x=5; s=''
    for word,k,frac,v,col in parts:
        w=k*bw
        for i in range(k):
            s+=f"<rect x='{x+i*bw}' y='8' width='{bw}' height='10' fill='{col}' fill-opacity='{0.28 if v else 0.10}' stroke='{INK if v else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x}' y='8' width='{w}' height='10' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=txt(x+w/2,5.5,word,col,3.6)
        s+=txt(x+w/2,23.5,frac,col,3.6)
        if v: s+=val(x+w/2,14.4,v)
        x+=w
    return svg(s,'Полоса','0 0 100 27')

# три продажи в кирпичиках x: шесть кирпичиков общие, сравнивается только хвост
def sales():
    x0,bw,h=24,7,7
    rows=[('Бруно',[('x',bw,GOLD,True),('1',4,GOLD,False)]),
          ('Феде',[('107',16,GREEN,False)]),
          ('Лукас',[('105',13,BLUE,False)])]
    s=''
    s+=f"<path d='M{x0} 7.5V5.5H{x0+6*bw}V7.5' fill='none' stroke='{MUT}' stroke-width='0.5'/>"
    s+=txt(x0+3*bw,4,'шесть кирпичиков x',MUT,3.2)
    for r,(name,tail) in enumerate(rows):
        y=9+r*(h+4)
        s+=txt(x0-3,y+h/2+1.2,name,LAB,3.6,'600','end')
        for i in range(6):
            s+=f"<rect x='{x0+i*bw}' y='{y}' width='{bw}' height='{h}' fill='{DIM}' fill-opacity='0.35' stroke='{INK}' stroke-width='0.4'/>"
            s+=txt(x0+i*bw+bw/2,y+h/2+1.2,'x',MUT,3.2)
        xx=x0+6*bw
        for lab,w,col,brick in tail:
            s+=f"<rect x='{xx}' y='{y}' width='{w}' height='{h}' fill='{col}' fill-opacity='{0.30 if brick else 0.20}' stroke='{col}' stroke-width='0.8'/>"
            s+=txt(xx+w/2,y+h/2+1.3,lab,LAB,3.6,'700')
            xx+=w
    return svg(s,'Продажи','0 0 100 42',"max-width:460px")

# схема-план: стрелка = данное условия; step подсвечивает текущую стрелку
NODES={'БФЛ':(2,4,32,10),'М':(54,4,26,10),'Ф':(100,4,48,10),'Л':(100,22,40,10),'1980':(2,40,18,10),'П':(54,40,34,10)}
NAME={'БФЛ':'Б &lt; Ф, Б &gt; Л','М':'N(мешок)','Ф':'N(осталось у Феде)','Л':'N(продал Лукас)','1980':'1980','П':'N(мешок Педро)'}
START={'БФЛ','1980'}
ARROWS={1:[('M34 9H53','дюжины',(43.5,6.6))],
        2:[('M80 9H99','½ и 107',(89.5,6.6))],
        3:[('M67 14V27H99','+10, ½ и 100',(84,25))],
        4:[('M20 45H53','10 из 100',(36.5,42.6))]}
TARGET={1:'М',2:'Ф',3:'Л',4:'П'}
def scheme(step=None):
    s=f"<defs><marker id='ah{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done=set(START)|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ah{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,3.2)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or n in START) else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col,3.6)
    return svg(s,'Схема решения','0 0 152 54')

V={}
V['запишем три продажи через x']=fig(scheme(),'План: каждая стрелка — данное условия.')
V['1. а) Найдём N(мешок)']=fig(scheme(1))
V['в каждой из трёх продаж есть шесть кирпичиков x']=fig(sales(),'Продажи в кирпичиках x.')
V['2. б) Найдём N(осталось у Феде)']=fig(scheme(2))
V['3. в) Найдём N(продал Лукас)']=fig(scheme(3))
V['4. г) Найдём N(мешок Педро)']=fig(scheme(4))
V['г) Найдём N(мешок Педро).']=fig(bar([('годные',9,'90/100 = 1 − 10/100','1980',GOLD),('брак',1,'10/100',None,BLUE)]),'Мешок Педро: десять равных частей, годные — девять.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
