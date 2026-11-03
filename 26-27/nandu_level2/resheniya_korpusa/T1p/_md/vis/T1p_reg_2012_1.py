import json, sys
GOLD,BLUE,GREEN='#f0a83c','#5ba8f5','#5fd38d'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def svg(inner,label,vb,mw=None):
    st=f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def num(x,y,s,size=4.4):
    return f"<text x='{x}' y='{y}' fill='{LAB}' font-size='{size}' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>{s}</text>"

# таблица пикап × автомобиль; full=False — 1200 в строке «пикап» и в столбце «автомобиль»;
# full=True — раздел 4: строка «пикап» 4800, «только автомобиль» 6000, «без машин» — искомое
X0,Y0,CW,CH=30,8,30,12
def grid():
    s=txt(X0+CW/2,Y0-2.5,'автомобиль',MUT,3.4)+txt(X0+1.5*CW,Y0-2.5,'без автомобиля',MUT,3.4)
    s+=txt(X0-13,Y0+CH/2+1.2,'пикап',MUT,3.4)+txt(X0-13,Y0+1.5*CH+1.2,'без пикапа',MUT,3.4)
    for r in range(2):
        for c in range(2):
            s+=f"<rect x='{X0+c*CW}' y='{Y0+r*CH}' width='{CW}' height='{CH}' fill='none' stroke='{DIM}' stroke-width='0.5'/>"
    return s
def table(full=False):
    s=grid()
    if not full:
        s+=f"<rect x='{X0}' y='{Y0}' width='{CW}' height='{CH}' fill='{GOLD}' fill-opacity='0.25'/>"
        s+=txt(X0+CW/2,Y0+CH/2+1.6,'1200',GOLD,4.6,'700')
        s+=txt(X0+1.5*CW,Y0+1.5*CH+1.4,'?',MUT,4.6,'700')
        s+=f"<rect x='{X0-0.4}' y='{Y0-0.4}' width='{2*CW+0.8}' height='{CH+0.8}' fill='none' stroke='{BLUE}' stroke-width='1.1' rx='1'/>"
        s+=f"<rect x='{X0-0.8}' y='{Y0-0.8}' width='{CW+1.6}' height='{2*CH+1.6}' fill='none' stroke='{GREEN}' stroke-width='1.1' rx='1'/>"
        s+=f"<text x='{X0+2*CW+3}' y='{Y0+CH/2+1.2}' fill='{BLUE}' font-size='3.3' font-weight='600'>1/4 пикапа</text>"
        s+=txt(X0+CW/2,Y0+2*CH+6,'1/6 автомобиля',GREEN,3.3)
        return svg(s,'Пикап × автомобиль','0 0 124 42')
    s+=f"<rect x='{X0}' y='{Y0}' width='{2*CW}' height='{CH}' fill='{BLUE}' fill-opacity='0.25'/>"
    s+=f"<rect x='{X0}' y='{Y0+CH}' width='{CW}' height='{CH}' fill='{GREEN}' fill-opacity='0.25'/>"
    s+=f"<rect x='{X0+CW}' y='{Y0+CH}' width='{CW}' height='{CH}' fill='{GOLD}' fill-opacity='0.25'/>"
    s+=f"<rect x='{X0-0.4}' y='{Y0-0.4}' width='{2*CW+0.8}' height='{CH+0.8}' fill='none' stroke='{BLUE}' stroke-width='1.1' rx='1'/>"
    s+=num(X0+CW,Y0+CH/2+1.6,'4800')
    s+=num(X0+CW/2,Y0+1.5*CH+1.6,'6000')
    s+=txt(X0+1.5*CW,Y0+1.5*CH+1.6,'?',GOLD,4.6,'700')
    s+=f"<text x='{X0+2*CW+3}' y='{Y0+CH/2+1.2}' fill='{BLUE}' font-size='3.3' font-weight='600'>N(пикап)</text>"
    s+=f"<text x='{X0+2*CW+3}' y='{Y0+1.5*CH+1.2}' fill='{GOLD}' font-size='3.3' font-weight='600'>N(без машин)</text>"
    s+=txt(X0+CW/2,Y0+2*CH+6,'только автомобиль',GREEN,3.3)
    return svg(s,'Группы жителей','0 0 124 42')

# полоса-целое из равных кирпичиков: части подписаны словами сверху и долями снизу
def bar(parts):
    n=sum(p[1] for p in parts); W=90; bw=W/n; x=5; s=''
    for word,k,frac,val,col in parts:
        w=k*bw
        for i in range(k):
            s+=f"<rect x='{x+i*bw}' y='8' width='{bw}' height='10' fill='{col}' fill-opacity='{0.28 if val else 0.10}' stroke='{INK if val else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x}' y='8' width='{w}' height='10' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=txt(x+w/2,5.5,word,col,3.6)
        s+=txt(x+w/2,23.5,frac,col,3.6)
        if val: s+=num(x+w/2,14.4,val,4.2)
        x+=w
    return svg(s,'Полоса','0 0 100 27')

# вертикальная полоса — целое-столбец таблицы (пикап сверху, без пикапа снизу)
def vbar(parts):
    n=sum(p[1] for p in parts); H=40; bh=H/n; y=3; s=''; x=40; w=16
    for word,k,frac,val,col in parts:
        h=k*bh
        for i in range(k):
            s+=f"<rect x='{x}' y='{y+i*bh}' width='{w}' height='{bh}' fill='{col}' fill-opacity='{0.28 if val else 0.10}' stroke='{INK if val else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=f"<text x='{x-3}' y='{y+h/2+1.2}' fill='{col}' font-size='3.6' text-anchor='end' font-weight='600'>{word}</text>"
        s+=f"<text x='{x+w+3}' y='{y+h/2+1.2}' fill='{col}' font-size='3.6' font-weight='600'>{frac}</text>"
        if val: s+=num(x+w/2,y+h/2+1.5,val,4.2)
        y+=h
    return f"<svg viewBox='4 0 84 46' role='img' aria-label='Полоса' style='max-width:400px'>{s}</svg>"

# схема-план: от 1200 к целым; стрелка = доля из условия; step подсвечивает текущую стрелку
NODES={'1200':(2,4,18,10),'А':(46,4,40,10),'П':(26,32,30,10),'Вс':(72,32,28,10),'Н':(116,32,38,10)}
NAME={'1200':'1200','А':'N(автомобиль)','П':'N(пикап)','Вс':'N(всех)','Н':'N(без машин)'}
ARROWS={1:[('M20 9H45','1/6',(32.5,6.6))],
        2:[('M11 14V37H25','1/4',(14.6,27))],
        3:[('M56 37H71','1/5',(63.5,34.6))],
        4:[('M100 37H115','',None),('M86 9H135V31','−',(139,21)),('M41 42V46H135V43','',None)]}
TARGET={1:'А',2:'П',3:'Вс',4:'Н'}
def scheme(step=None):
    s=f"<defs><marker id='ah{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done={'1200'}|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ah{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,5 if lab=='−' else 3.4)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or (n=='1200')) else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col if n!='1200' else GOLD,3.6)
    return svg(s,'Схема решения','0 0 156 48')

V={}
V['1200 человек в клетке «пикап, автомобиль»']=fig(table(),'Все жители города.')
V['одновременно входят и в строку']=fig(scheme(),'План: каждая стрелка — доля из условия.')
V['1. Найдём N(автомобиль)']=fig(scheme(1))
V['1/6 владельцев автомобиля» ⇒']=fig(vbar([('пикап',1,'1/6','1200',GOLD),('без пикапа',5,'5/6',None,BLUE)]),'Владельцы автомобиля: шесть равных частей, с пикапом — одна.')
V['2. Найдём N(пикап)']=fig(scheme(2))
V['имеют ещё и автомобиль» и']=fig(bar([('автомобиль',1,'1/4','1200',GOLD),('без автомобиля',3,'3/4',None,BLUE)]),'Владельцы пикапа: четыре равные части, с автомобилем — одна.')
V['3. Найдём N(всех)']=fig(scheme(3))
V['«1/5 жителей имеют пикап», а']=fig(vbar([('пикап',1,'1/5','4800',GOLD),('без пикапа',4,'4/5',None,BLUE)]),'Все жители: пять равных частей, с пикапом — одна.')
V['4. Найдём N(без машин)']=fig(scheme(4))
V['жители делятся на четыре группы']=fig(table(True),'Все 24000 жителей.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
