import json, sys
GOLD,BLUE,GREEN='#f0a83c','#5ba8f5','#5fd38d'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def svg(inner,label,vb):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# таблица смена × спорт: 372 — в столбце «волейбол» и в строке «день»
def table():
    x0,y0,cw,ch=22,8,26,12
    s=''
    s+=txt(x0+cw/2,y0-2.5,'волейбол',MUT,3.4)+txt(x0+1.5*cw,y0-2.5,'хоккей',MUT,3.4)
    s+=txt(x0-11,y0+ch/2+1.2,'утро',MUT,3.4)+txt(x0-11,y0+1.5*ch+1.2,'день',MUT,3.4)
    for r in range(2):
        for c in range(2):
            s+=f"<rect x='{x0+c*cw}' y='{y0+r*ch}' width='{cw}' height='{ch}' fill='none' stroke='{DIM}' stroke-width='0.5'/>"
    s+=f"<rect x='{x0}' y='{y0+ch}' width='{cw}' height='{ch}' fill='{GOLD}' fill-opacity='0.25'/>"
    s+=txt(x0+cw/2,y0+1.5*ch+1.6,'372',GOLD,4.6,'700')
    s+=f"<rect x='{x0-0.8}' y='{y0-0.8}' width='{cw+1.6}' height='{2*ch+1.6}' fill='none' stroke='{BLUE}' stroke-width='1.1' rx='1'/>"
    s+=f"<rect x='{x0-0.4}' y='{y0+ch-0.4}' width='{2*cw+0.8}' height='{ch+0.8}' fill='none' stroke='{GREEN}' stroke-width='1.1' rx='1'/>"
    s+=txt(x0+cw/2,y0+2*ch+6,'1/3 волейболистов',BLUE,3.3)
    s+=f"<text x='{x0+2*cw+3}' y='{y0+1.5*ch+1.2}' fill='{GREEN}' font-size='3.3' font-weight='600'>3/5 дня</text>"
    return svg(s,'Смена × спорт','0 0 112 42')

# полоса-целое из равных кирпичиков: части подписаны словами сверху и долями снизу
def bar(parts):
    # parts: [(слово, кирпичиков, доля, значение или None, цвет)]
    n=sum(p[1] for p in parts); W=90; bw=W/n; x=5; s=''
    for word,k,frac,val,col in parts:
        w=k*bw
        for i in range(k):
            s+=f"<rect x='{x+i*bw}' y='8' width='{bw}' height='10' fill='{col}' fill-opacity='{0.28 if val else 0.10}' stroke='{INK if val else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x}' y='8' width='{w}' height='10' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=txt(x+w/2,5.5,word,col,3.6)
        s+=txt(x+w/2,23.5,frac,col,3.6)
        if val: s+=f"<text x='{x+w/2}' y='14.4' fill='{LAB}' font-size='4.2' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>{val}</text>"
        x+=w
    return svg(s,'Полоса','0 0 100 27')

# вертикальная полоса — целое, делённое по смене (утро сверху, день снизу), как столбец таблицы
def vbar(parts):
    n=sum(p[1] for p in parts); H=40; bh=H/n; y=3; s=''; x=40; w=16
    for word,k,frac,val,col in parts:
        h=k*bh
        for i in range(k):
            s+=f"<rect x='{x}' y='{y+i*bh}' width='{w}' height='{bh}' fill='{col}' fill-opacity='{0.28 if val else 0.10}' stroke='{INK if val else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=f"<text x='{x-3}' y='{y+h/2+1.2}' fill='{col}' font-size='3.6' text-anchor='end' font-weight='600'>{word}</text>"
        s+=f"<text x='{x+w+3}' y='{y+h/2+1.2}' fill='{col}' font-size='3.6' font-weight='600'>{frac}</text>"
        if val: s+=f"<text x='{x+w/2}' y='{y+h/2+1.5}' fill='{LAB}' font-size='4.2' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>{val}</text>"
        y+=h
    return f"<svg viewBox='12 0 76 46' role='img' aria-label='Полоса' style='max-width:400px'>{s}</svg>"

# схема-план: от 372 к целым; стрелка = доля из условия; step подсвечивает текущую стрелку
NODES={'372':(2,4,18,10),'В':(50,4,36,10),'Д':(30,32,28,10),'Вс':(76,32,28,10),'Х':(118,32,32,10)}
NAME={'372':'372','В':'N(волейбол)','Д':'N(день)','Вс':'N(всех)','Х':'N(хоккей)'}
ARROWS={1:[('M20 9H49','1/3',(34.5,6.6))],
        2:[('M11 14V37H29','3/5',(14.6,27))],
        3:[('M58 37H75','2/5',(66.5,34.6))],
        4:[('M104 37H117','',None),('M86 9H134V31','−',(138,21))]}
TARGET={1:'В',2:'Д',3:'Вс',4:'Х'}
def scheme(step=None):
    s=f"<defs><marker id='ah{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done={'372'}|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ah{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,5 if lab=='−' else 3.4)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or (n=='372')) else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col if n!='372' else GOLD,3.6)
    return svg(s,'Схема решения','0 0 152 46')

V={}
V['372 ученика в клетке «день, волейбол»']=fig(table(),'Все ученики школы.')
V['одновременно входят и в столбец']=fig(scheme(),'План: каждая стрелка — доля из условия.')
V['1. N(волейбол)']=fig(scheme(1))
V['1. N(волейбол).']=fig(vbar([('утро',2,'2/3',None,BLUE),('день',1,'1/3 = 1 − 2/3','372',GOLD)]),'Волейболисты: три равные части, днём — одна.')
V['2. N(день)']=fig(scheme(2))
V['2. N(день).']=fig(bar([('волейбол',3,'3/5 = 1 − 2/5','372',GOLD),('хоккей',2,'2/5',None,BLUE)]),'День: пять равных частей, волейбол — три.')
V['3. N(всех)']=fig(scheme(3))
V['3. N(всех).']=fig(vbar([('утро',3,'3/5',None,BLUE),('день',2,'2/5 = 1 − 3/5','620',GOLD)]),'Все ученики: пять равных частей, день — две.')
V['4. N(хоккей).']=fig(scheme(4))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
