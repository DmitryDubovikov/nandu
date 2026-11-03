import json, sys
GOLD,BLUE,GREEN,RED='#f0a83c','#5ba8f5','#5fd38d','#f07a7a'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600',anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"
def svg(inner,label,vb,style=''):
    st=f" style='{style}'" if style else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# полоса-целое из равных кирпичиков: части подписаны словами сверху и долями снизу;
# часть, о которой раздел, закрашена ярче (strong), известное число — внутри неё
def bar(parts):
    # parts: [(слово, кирпичиков, доля, значение или None, цвет, ярко)]
    n=sum(p[1] for p in parts); W=90; bw=W/n; x=5; s=''
    for word,k,frac,val,col,strong in parts:
        w=k*bw
        for i in range(k):
            s+=f"<rect x='{x+i*bw}' y='8' width='{bw}' height='10' fill='{col}' fill-opacity='{0.28 if strong else 0.10}' stroke='{INK if strong else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x}' y='8' width='{w}' height='10' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=txt(x+w/2,5.5,word,col,3.6)
        s+=txt(x+w/2,23.5,frac,col,3.6)
        if val: s+=f"<text x='{x+w/2}' y='14.4' fill='{LAB}' font-size='4.2' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>{val}</text>"
        x+=w
    return svg(s,'Полоса','0 0 100 27')

# красные и синие одними кирпичиками (шестая часть красных): синяя полоса вдвое длиннее;
# то, что ушло в среднюю коробку, обведено вместе — это 168
def sixths():
    x0,bw,h=24,7,8; s=''
    rows=[('красные',6,3,'1/2',RED,6),('синие',12,4,'1/3',BLUE,24)]
    for name,n,k,frac,col,y in rows:
        s+=txt(x0-3,y+h/2+1.3,name,col,3.6,anchor='end')
        for i in range(n):
            s+=f"<rect x='{x0+i*bw}' y='{y}' width='{bw}' height='{h}' fill='{col}' fill-opacity='{0.30 if i<k else 0.08}' stroke='{INK if i<k else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x0}' y='{y}' width='{n*bw}' height='{h}' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=f"<text x='{x0+k*bw/2}' y='{y+h/2+1.4}' fill='{LAB}' font-size='3.8' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.4' paint-order='stroke'>{frac}</text>"
    # общая рамка частей средней коробки
    s+=(f"<path d='M{x0-1} 3.2H{x0+3*bw+1}V20.4H{x0+4*bw+1}V33H{x0-1}Z' fill='none' stroke='{GOLD}' "
        f"stroke-width='0.9' stroke-dasharray='1.6 1'/>")
    s+=txt(x0+3*bw+9,19,'168',GOLD,4.6,'700')
    return svg(s,'Красные и синие кирпичиками','0 0 112 36','max-width:520px')

# схема-план: от 168 и 633 к целым; стрелка = данное условия; step подсвечивает текущие стрелки
NODES={'168':(2,4,16,10),'К':(40,4,32,10),'С':(92,4,28,10),
       '633':(2,32,16,10),'ЗО':(30,32,46,10),'З':(92,32,30,10),'ЗМ':(138,32,52,10)}
NAME={'168':'168','К':'N(красных)','С':'N(синих)','633':'633',
      'ЗО':'N(зелёных осталось)','З':'N(зелёных)','ЗМ':'N(зелёных в маленькой)'}
GIVEN={'168','633'}
ARROWS={1:[('M18 9H39','1/2 и 1/3',(28.5,6.6))],
        2:[('M72 9H91','· 2',(81.5,6.6))],
        3:[('M18 37H29','−',(23.5,35.4)),('M56 14V31','1/2',(60.5,24)),('M106 14L74 31','2/3',(99,26))],
        4:[('M76 37H91','3/4',(83.5,34.6))],
        5:[('M122 37H137','1/4',(129.5,34.6))]}
TARGET={1:'К',2:'С',3:'ЗО',4:'З',5:'ЗМ'}
def scheme(step=None):
    s=f"<defs><marker id='ah{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done=set(GIVEN)|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ah{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,5 if lab=='−' else 3.4)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or n in GIVEN) else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col,3.6)
    return svg(s,'Схема решения','0 0 192 46')

V={}
V['все 168 шариков средней коробки']=fig(scheme(),'План: каждая стрелка — данное условия.')
V['1. Найдём N(красных)']=fig(scheme(1))
V['1. Найдём N(красных).']=fig(sixths(),'Красные и синие: кирпичик — шестая часть красных.')
V['2. Найдём N(синих)']=fig(scheme(2))
V['3. Найдём N(зелёных осталось)']=fig(scheme(3))
V['3.1. N(красных осталось).']=fig(bar([('в среднюю',1,'1/2',None,RED,False),('осталось',1,'1/2 = 1 − 1/2',None,RED,True)]),'Красные: две равные части, в большой осталась одна.')
V['3.2. N(синих осталось).']=fig(bar([('в среднюю',1,'1/3',None,BLUE,False),('осталось',2,'2/3 = 1 − 1/3',None,BLUE,True)]),'Синие: три равные части, в большой остались две.')
V['4. Найдём N(зелёных)']=fig(scheme(4))
V['4. Найдём N(зелёных).']=fig(bar([('в маленькую',1,'1/4',None,GREEN,False),('осталось',3,'3/4 = 1 − 1/4','369',GREEN,True)]),'Зелёные: четыре равные части, в большой остались три.')
V['5. в) Найдём N(зелёных в маленькой)']=fig(scheme(5))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
