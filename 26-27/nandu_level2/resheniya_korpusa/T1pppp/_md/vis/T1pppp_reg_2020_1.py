import json, sys
GOLD,BLUE,GREEN='#f0a83c','#5ba8f5','#5fd38d'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def htxt(x,y,s,col,size=3.4,w='700'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}' stroke='#121821' stroke-width='1.3' paint-order='stroke'>{s}</text>"
def svg(inner,label,vb,mw=None):
    st=f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# полоса опрошенных, не в масштабе: «только метро», «оба», «только автобус», «ни одного»
X0,Y,H=5,14,14
ZONES=[('только метро','x − 32',0,26,BLUE),('оба','32',26,14,GOLD),('только автобус','2 · x − 32',40,40,GREEN),('ни одного','x − 16',80,24,MUT)]
def groups():
    s=''
    for name,val,a,w,col in ZONES:
        s+=f"<rect x='{X0+a}' y='{Y}' width='{w}' height='{H}' fill='{col}' fill-opacity='0.22' stroke='{col}' stroke-width='0.9'/>"
        s+=htxt(X0+a+w/2,Y+5.4,name,col,3.0)+htxt(X0+a+w/2,Y+10.8,val,col,3.4)
    def brace(a,w,y,up,label,col):
        x1,x2=X0+a+0.6,X0+a+w-0.6
        d=f'M{x1} {y+1.8}V{y}H{x2}V{y+1.8}' if up else f'M{x1} {y-1.8}V{y}H{x2}V{y-1.8}'
        ty=y-1.6 if up else y+4.4
        return f"<path d='{d}' fill='none' stroke='{col}' stroke-width='0.8'/>"+txt((x1+x2)/2,ty,label,col,3.6)
    s+=brace(0,40,Y-2.5,True,'метро: x',BLUE)
    s+=brace(26,54,Y+H+2.5,False,'автобус: 2 · x',GREEN)
    s+=brace(0,104,Y+H+10,False,'всего 264',INK)
    return svg(s,'Группы опрошенных','0 0 114 48',560)

# схема-план: от 264 и 32 к спрошенным; step подсвечивает текущий раздел
NODES={'264':(2,4,26,10),'М':(56,4,34,10),'А':(56,30,34,10)}
NAME={'264':'264 и 32','М':'б) N(метро)','А':'а) N(автобус)'}
ARROWS={1:[('M28 9H55','четыре группы',(41.5,6.6))],
        2:[('M73 14V29','вдвое',(80,23))]}
TARGET={1:'М',2:'А'}
def scheme(step=None):
    s=f"<defs><marker id='ahv{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done={'264'}|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ahv{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,3.3)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or n=='264') else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col,3.4)
    return svg(s,'Схема решения','0 0 94 44',380)

V={}
V['выразим все группы опрошенных через N(метро)']=fig(scheme(),'План: каждая стрелка — данное из условия.')
V['1. б) Найдём N(метро)']=fig(scheme(1))
V['четыре группы вместе дают 264']=fig(groups(),'Опрошенные жители, не в масштабе.')
V['2. а) Найдём N(автобус)']=fig(scheme(2))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
