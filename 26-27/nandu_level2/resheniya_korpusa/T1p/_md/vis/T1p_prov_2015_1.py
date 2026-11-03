"""Рисунки: пров 2015 №1 (Т1′) — конфеты трёх вкусов.

План — схема из стрелок (36 и 84 → N(клубничных) → N(лимонных)), в каждом разделе подсвечена своя стрелка.
Полоса-целое из трёх равных кирпичиков: сначала (клубничные — один, мятные 84 и лимонные — два) и теперь
(к лимонным приставлены 36, полоса делится пополам). Обе полосы в одном масштабе.
Запуск: python3 vis/T1p_prov_2015_1.py T1p_prov_2015_1.vis.json
"""
import json, sys
GOLD,BLUE,GREEN,RED='#f0a83c','#5ba8f5','#5fd38d','#f2686c'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def svg(inner,label,vb,style=''):
    st=f" style='{style}'" if style else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# полоса конфет в масштабе: 432 конфеты = 90 единиц
U=90/432; X0=5; Y=8; H=10
def X(v): return X0+v*U
def seg(a,b,col,val=None,op=0.12):
    s=f"<rect x='{X(a)}' y='{Y}' width='{(b-a)*U}' height='{H}' fill='{col}' fill-opacity='{0.28 if val else op}' stroke='{col}' stroke-width='0.9'/>"
    if val: s+=f"<text x='{X((a+b)/2)}' y='{Y+6.4}' fill='{LAB}' font-size='4.2' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>{val}</text>"
    return s
def bracket(a,b,lab,col):
    y=Y+H+2.2
    s=f"<path d='M{X(a)+0.6} {y-1}V{y}H{X(b)-0.6}V{y-1}' fill='none' stroke='{col}' stroke-width='0.6'/>"
    return s+txt(X((a+b)/2),y+4.2,lab,col,3.6)
def bar(now=False):
    end=432 if now else 396
    s=seg(0,132,RED)+seg(132,216,GREEN,'84')+seg(216,396,GOLD)
    if now: s+=seg(396,432,GOLD,'36',0.5)
    # перегородки кирпичиков: каждый кирпичик = N(клубничных)
    for v in (132,264,396):
        s+=f"<line x1='{X(v)}' y1='{Y-1.2}' x2='{X(v)}' y2='{Y+H+1.2}' stroke='{INK}' stroke-width='0.5' stroke-dasharray='{'1 0.8' if v!=132 else '0'}'/>"
    s+=txt(X(66),Y-2.5,'клубничные',RED)+txt(X(174),Y-2.5,'мятные',GREEN)+txt(X((216+end)/2),Y-2.5,'лимонные',GOLD)
    if now:
        s+=bracket(0,216,'1/2',INK)+bracket(216,432,'1/2',GOLD)
    else:
        s+=bracket(0,132,'1/3',RED)+bracket(132,396,'2/3 = 1 − 1/3',GOLD)
    return svg(s,'Полоса конфет','0 0 100 29','max-width:560px')

# схема-план: стрелки — данные условия; step подсвечивает текущую стрелку
NODES={'src':(2,4,22,10),'К':(40,4,40,10),'Л':(100,4,38,10)}
NAME={'src':'36 и 84','К':'N(клубничных)','Л':'N(лимонных)'}
ARROWS={1:('M24 9H39','1/2',(31.5,6.6)),2:('M80 9H99','2/3',(89.5,6.6))}
TARGET={1:'К',2:'Л'}
def scheme(step=None):
    s=f"<defs><marker id='ah{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done={'src'}|{TARGET[k] for k in TARGET if step and k<step}
    for k,(d,lab,pos) in ARROWS.items():
        cur=step==k
        col=GOLD if cur else (INK if (step is None or k<step) else DIM)
        s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{1.0 if cur else 0.6}' marker-end='url(#ah{step})'/>"
        s+=txt(pos[0],pos[1],lab,col,3.4)
    for n,(x,y,w,h) in NODES.items():
        cur=step and TARGET[step]==n
        col=GOLD if (cur or n=='src') else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col,3.6)
    return svg(s,'Схема решения','0 0 140 18')

V={}
V['делают лимонные ровно половиной коробки']=fig(scheme(),'План: каждая стрелка — данное из условия.')
V['1. Найдём N(клубничных)']=fig(scheme(1))
V['мятные и лимонные вместе — две части из трёх']=fig(bar(),'Сначала: три равные части, клубничные — одна.')
V['теперь лимонных столько же, сколько клубничных и мятных вместе']=fig(bar(True),'Теперь: лимонные — половина.')
V['2. Найдём N(лимонных)']=fig(scheme(2))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
