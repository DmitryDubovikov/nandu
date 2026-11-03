import json, sys
GOLD,BLUE,GREEN='#f0a83c','#5ba8f5','#5fd38d'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def htxt(x,y,s,col,size=3.4,w='700'):   # подпись поверх кирпичиков: тёмная обводка, чтобы сетка не резала буквы
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}' stroke='#121821' stroke-width='1.3' paint-order='stroke'>{s}</text>"
def svg(inner,label,vb,mw=None):
    st=f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# полоса присутствующих: 20 кирпичиков по 5 %; группы «только развлечения» 9, «оба» 3, «только спорт» 8
X0,BW,Y,H=5,5,12,14
ZONES=[('только развлечения',0,9,BLUE),('оба',9,3,GOLD),('только спорт',12,8,GREEN)]
def bricks(lit):
    s=''
    for name,a,k,col in ZONES:
        on = lit is None or name in lit
        for i in range(a,a+k):
            s+=f"<rect x='{X0+i*BW}' y='{Y}' width='{BW}' height='{H}' fill='{col if on else DIM}' fill-opacity='{0.28 if on else 0.12}' stroke='{INK if on else DIM}' stroke-width='0.35'/>"
        s+=f"<rect x='{X0+a*BW}' y='{Y}' width='{k*BW}' height='{H}' fill='none' stroke='{col if on else DIM}' stroke-width='0.9'/>"
    return s
def brace(a,k,up,label,col):
    x1,x2=X0+a*BW+0.6,X0+(a+k)*BW-0.6
    if up:
        y=Y-2.5; d=f'M{x1} {y+1.8}V{y}H{x2}V{y+1.8}'; ty=y-1.6
    else:
        y=Y+H+2.5; d=f'M{x1} {y-1.8}V{y}H{x2}V{y-1.8}'; ty=y+4.4
    return f"<path d='{d}' fill='none' stroke='{col}' stroke-width='0.8'/>"+txt((x1+x2)/2,ty,label,col,3.6)

# раздел 1: развлечения 60 % делятся на четыре четверти по 3 кирпичика; спорт = «только спорт» + «оба»
def venn():
    s=bricks(None)
    for q in (3,6):   # границы четвертей внутри развлечений (третья граница — край «оба»)
        s+=f"<line x1='{X0+q*BW}' y1='{Y}' x2='{X0+q*BW}' y2='{Y+H}' stroke='{BLUE}' stroke-width='0.9'/>"
    s+=htxt(X0+4.5*BW,Y+H/2+1.2,'только развлечения',BLUE,3.2)
    s+=htxt(X0+10.5*BW,Y+5.4,'оба',GOLD,3.2)+htxt(X0+10.5*BW,Y+10.8,'15 %',GOLD,3.6,'700')
    s+=htxt(X0+16*BW,Y+5.4,'только спорт',GREEN,3.2)+htxt(X0+16*BW,Y+10.8,'40 %',GREEN,3.6,'700')
    s+=brace(0,12,True,'развлечения 60 %',BLUE)
    s+=brace(9,11,False,'спорт 55 % = 836',GREEN)
    return svg(s,'Группы присутствующих','0 0 110 36',520)

# раздел 3: одним занятием — все присутствующие, кроме группы «оба»
def single():
    s=bricks({'только развлечения','только спорт'})
    s+=htxt(X0+4.5*BW,Y+H/2+1.2,'только развлечения',BLUE,3.2)
    s+=htxt(X0+10.5*BW,Y+H/2+1.2,'оба',MUT,3.2)
    s+=htxt(X0+16*BW,Y+H/2+1.2,'только спорт',GREEN,3.2)
    s+=brace(0,9,False,'одно занятие',INK)+brace(12,8,False,'одно занятие',INK)
    s+=brace(9,3,True,'два занятия',MUT)
    return svg(s,'Одно занятие','0 0 110 36',520)

# раздел 4: школа — 20 кирпичиков по 5 %, пришли 19
def school():
    s=''
    for i in range(20):
        on=i<19
        s+=f"<rect x='{X0+i*BW}' y='{Y}' width='{BW}' height='{H}' fill='{GOLD if on else DIM}' fill-opacity='{0.28 if on else 0.12}' stroke='{INK if on else DIM}' stroke-width='0.35'/>"
    s+=f"<rect x='{X0}' y='{Y}' width='{19*BW}' height='{H}' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
    s+=f"<text x='{X0+9.5*BW}' y='{Y+H/2+1.6}' fill='{LAB}' font-size='4.4' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>1520</text>"
    s+=brace(0,19,True,'пришли в День весны: 95 %',GOLD)
    s+=brace(19,1,False,'5 %',MUT)
    return svg(s,'Ученики школы','0 0 110 36',520)

# схема-план: от 836 к спрошенным; стрелка — данное из условия; step подсвечивает текущий раздел
NODES={'836':(2,4,16,10),'П':(40,4,40,10),'Ш':(106,4,28,10),'Р':(2,32,38,10),'О':(54,32,40,10),'Н':(100,32,40,10)}
NAME={'836':'836','П':'N(присутствующих)','Ш':'N(школы)','Р':'а) N(развлечения)','О':'б) N(одно занятие)','Н':'в) N(не пришли)'}
ARROWS={1:[('M18 9H39','60 %, 1/4',(28.5,6.6))],
        2:[('M50 14L26 31','60 %',(32,22))],
        3:[('M66 14L72 31','',None),('M40 37H53','− 1/4',(47,34.6))],
        4:[('M80 9H105','95 %',(92.5,6.6))],
        5:[('M120 14V31','20 %',(126,23.5))]}
TARGET={1:'П',2:'Р',3:'О',4:'Ш',5:'Н'}
def scheme(step=None):
    s=f"<defs><marker id='ahv{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done={'836'}|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ahv{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,3.3)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or n=='836') else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col,3.4)
    return svg(s,'Схема решения','0 0 142 46')

V={}
V['сначала выразим 836 долей присутствующих']=fig(scheme(),'План: каждая стрелка — данное из условия.')
V['1. Найдём N(присутствующих)']=fig(scheme(1))
V['спортом занимались группы «только спорт» и «оба»']=fig(venn(),'Присутствующие: 20 равных частей по 5 %.')
V['2. а) Найдём N(развлечения)']=fig(scheme(2))
V['3. б) Найдём N(одно занятие)']=fig(scheme(3))
V['N(одно занятие) = N(присутствующих) − N(оба)']=fig(single(),'Присутствующие по числу занятий.')
V['4. Найдём N(школы)']=fig(scheme(4))
V['4. Найдём N(школы).']=fig(school(),'Ученики школы: 20 равных частей по 5 %.')
V['5. в) Найдём N(не пришли)']=fig(scheme(5))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
