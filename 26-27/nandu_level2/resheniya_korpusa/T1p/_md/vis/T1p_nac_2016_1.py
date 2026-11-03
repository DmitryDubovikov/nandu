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

# таблица смена × уровень: спрошенные смены — строки «день» и «вечер»
def table():
    x0,y0,cw,ch=24,8,30,10
    s=''
    s+=txt(x0+cw/2,y0-2.5,'начинающие',MUT,3.4)+txt(x0+1.5*cw,y0-2.5,'продвинутые',MUT,3.4)
    for r,name in enumerate(['утро','день','вечер']):
        s+=txt(x0-10,y0+(r+0.5)*ch+1.2,name,MUT,3.4)
        for c in range(2):
            s+=f"<rect x='{x0+c*cw}' y='{y0+r*ch}' width='{cw}' height='{ch}' fill='none' stroke='{DIM}' stroke-width='0.5'/>"
    for r in (1,2):
        s+=f"<rect x='{x0-0.6}' y='{y0+r*ch+0.4}' width='{2*cw+1.2}' height='{ch-0.8}' fill='{GOLD}' fill-opacity='0.12' stroke='{GOLD}' stroke-width='1.0' rx='1'/>"
        s+=f"<text x='{x0+2*cw+3}' y='{y0+(r+0.5)*ch+1.4}' fill='{GOLD}' font-size='4' font-weight='700'>?</text>"
    return svg(s,'Смена × уровень','0 0 96 40')

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
        if val: s+=f"<text x='{x+w/2}' y='14.4' fill='{LAB}' font-size='4.2' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>{val}</text>"
        x+=w
    return svg(s,'Полоса','0 0 100 27')

# схема-план: от 1680 к клеткам таблицы; стрелка = данное из условия; step подсвечивает текущую стрелку
NODES={'1680':(2,4,16,10),'Пр':(28,4,32,10),'ДП':(76,4,42,10),'ВП':(76,24,42,10),
       'УН':(76,44,42,10),'ДН':(138,44,42,10)}
NAME={'1680':'1680','Пр':'N(продвинутые)','ДП':'N(день, продвинутые)','ВП':'N(вечер, продвинутые)',
      'УН':'N(утро, начинающие)','ДН':'N(день, начинающие)'}
ARROWS={1:[('M18 9H27','1/3',(22.5,6.6))],
        2:[('M60 9H75','1/7',(67.5,6.6))],
        3:[('M97 14V23','½ утра',(108,20))],
        4:[('M10 14V49H75','1/2',(42,47)),('M97 34V43','· 2',(102,40))],
        5:[('M118 49H137','поровну',(127.5,46.6))]}
TARGET={1:'Пр',2:'ДП',3:'ВП',4:'УН',5:'ДН'}
def scheme(step=None):
    s=f"<defs><marker id='ah{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done={'1680'}|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ah{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,3.2 if lab=='поровну' else 3.4)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or (n=='1680')) else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col if n!='1680' else GOLD,3.4)
    return svg(s,'Схема решения','0 0 182 56')

V={}
V['спрошенные смены — строки таблицы']=fig(table(),'Все ученики школы.')
V['N(вечер) = N(вечер, начинающие) + N(вечер, продвинутые)']=fig(scheme(),'План: каждая стрелка — данное из условия.')
V['1. Найдём N(продвинутые)']=fig(scheme(1))
V['1. Найдём N(продвинутые).']=fig(bar([('начинающие',2,'2/3',None,BLUE),('продвинутые',1,'1/3 = 1 − 2/3',None,GOLD)]),'Все 1680 учеников: три равные части, продвинутые — одна.')
V['2. Найдём N(день, продвинутые)']=fig(scheme(2))
V['2. Найдём N(день, продвинутые).']=fig(bar([('день',1,'1/7',None,GOLD),('утро и вечер',6,'6/7',None,BLUE)]),'Продвинутые: семь равных частей, днём — одна.')
V['3. Найдём N(вечер, продвинутые)']=fig(scheme(3))
V['3. Найдём N(вечер, продвинутые).']=fig(bar([('утро',2,'2/3',None,BLUE),('вечер',1,'1/3',None,GOLD)]),'Продвинутые утром и вечером: три равные части, вечером — одна.')
V['4. Найдём N(утро, начинающие).']=fig(scheme(4))
V['5. Найдём N(день, начинающие).']=fig(scheme(5))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
