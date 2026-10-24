import json, sys
GOLD,BLUE,GREEN,RED='#f0a83c','#5ba8f5','#5fd38d','#f2686c'
WHITE='#dfe6ee'
INK,DIM,LAB='#cfdae6','#4a5866','#e8eef6'
def txt(x,y,s,col=LAB,size=3.6,w='600',anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"
def lab(x,y,s,size=3.8):
    # подпись внутри столбика: светлая с тёмной обводкой, читается на любом цвете
    return f"<text x='{x}' y='{y}' fill='{LAB}' font-size='{size}' text-anchor='middle' font-weight='700' stroke='#1a2230' stroke-width='1.4' paint-order='stroke'>{s}</text>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# коробки — столбики в порядке условия: синяя, белая, красная, зелёная; высота ∝ числу фишек (по ответу)
K=40/450; BASE=50; BW=16
X={'с':8,'б':32,'к':56,'з':80}
COL={'с':BLUE,'б':WHITE,'к':RED,'з':GREEN}
def h(n): return n*K
def seg(box,lo,hi,label=None,ghost=False,hl=False):
    # кусок столбика от lo до hi фишек (снизу вверх)
    x=X[box]; y=BASE-h(hi); hh=h(hi)-h(lo); c=COL[box]
    if ghost:
        return f"<rect x='{x}' y='{y}' width='{BW}' height='{hh}' fill='none' stroke='{c}' stroke-width='0.5' stroke-dasharray='1.2 1'/>"
    fc=GOLD if hl else c
    s=f"<rect x='{x}' y='{y}' width='{BW}' height='{hh}' fill='{fc}' fill-opacity='{0.45 if hl else 0.28}' stroke='{fc}' stroke-width='0.7'/>"
    if label: s+=lab(x+BW/2,y+hh/2+1.3,label)
    return s
def arrow(x1,y1,x2,y2,lift,mid):
    return (f"<path d='M{x1} {y1} C{x1} {lift} {x2} {lift} {x2} {y2}' fill='none' stroke='{GOLD}' stroke-width='0.7' marker-end='url(#bx)'/>"
            + txt((x1+x2)/2,lift+1.2,mid,GOLD,3.4))
DEFS=f"<defs><marker id='bx' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='{GOLD}'/></marker></defs>"
def level(n,x1,x2):
    y=BASE-h(n)
    return f"<line x1='{x1}' y1='{y}' x2='{x2}' y2='{y}' stroke='{GOLD}' stroke-width='0.5' stroke-dasharray='1.5 1'/>"
def boxes(inner,label):
    s=DEFS+f"<line x1='4' y1='{BASE}' x2='100' y2='{BASE}' stroke='{DIM}' stroke-width='0.5'/>"+inner
    return f"<svg viewBox='0 0 116 53' role='img' aria-label='{label}' style='max-width:460px'>{s}</svg>"

a,b,v=165,420,450
def state1():
    s=seg('с',0,a,'a')+seg('б',0,b,'b')+seg('к',0,a,'a')+seg('з',0,v,'v')
    return boxes(s,'Коробки сначала')
def state2():
    s=seg('с',0,a-30,'a − 30')+seg('с',a-30,a,ghost=True)
    s+=seg('б',0,b,'b')+seg('б',b,b+30,hl=True)
    s+=seg('к',0,a,'a')+seg('з',0,v,'v')
    s+=level(v,X['б'],X['з']+BW)
    s+=arrow(X['с']+BW/2,BASE-h(a)-1,X['б']+BW/2-3,BASE-h(b+30)-1,BASE-h(v)-6,'30')
    return boxes(s,'Коробки после 30')
def state3():
    m=v//2
    s=seg('с',0,a-30,'a − 30')
    s+=seg('б',0,m,'v : 2')+seg('б',m,v,ghost=True)
    s+=seg('к',0,a,'a')+seg('к',a,a+m,'v : 2',hl=True)
    s+=seg('з',0,v,'v')
    s+=level(a+m,X['к'],X['з']+BW+3)
    y1,y2=BASE-h(v),BASE-h(a+m)
    s+=f"<path d='M{X['з']+BW+1.5} {y1}H{X['з']+BW+3}V{y2}H{X['з']+BW+1.5}' fill='none' stroke='{GOLD}' stroke-width='0.6'/>"
    s+=txt(X['з']+BW+4.5,(y1+y2)/2+1.2,'60',GOLD,3.6,anchor='start')
    s+=arrow(X['б']+BW/2,BASE-h(v)-1,X['к']+BW/2,BASE-h(a+m)-1,BASE-h(v)-6,'половина')
    return boxes(s,'Коробки в конце')

# схема-план: три момента, стрелка = перенос из условия, под моментом — его уравнение; step подсвечивает текущий
NODES=[(2,'сначала','(1)'),(82,'после 30','(2)'),(162,'в конце','(3)')]
ARR=[(30,80,'30 из синей в белую'),(110,160,'половина белой в красную')]
def scheme(step=None):
    s=f"<defs><marker id='ah{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    def col(k):
        if step is None or k<step: return INK
        return GOLD if k==step else DIM
    for i,(x1,x2,t) in enumerate(ARR):
        c=col(i+2)
        s+=f"<path d='M{x1} 11H{x2}' fill='none' stroke='{c}' stroke-width='{1.0 if c==GOLD else 0.6}' marker-end='url(#ah{step})'/>"
        s+=txt((x1+x2)/2,8,t,c,3.2)
    for i,(x,name,eq) in enumerate(NODES):
        c=col(i+1); cur=c==GOLD
        s+=f"<rect x='{x}' y='6' width='28' height='10' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{c}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+14,12.3,name,c,3.6)
        s+=txt(x+14,21.5,eq,c,3.4)
    return f"<svg viewBox='0 2 192 22' role='img' aria-label='Схема решения'>{s}</svg>"

V={}
V['Каждое «теперь» — равенство']=fig(scheme(),'План: стрелка — перенос из условия, под моментом — его уравнение.')
V['1. Коробки сначала']=fig(scheme(1))
V['по a фишек']=fig(state1(),'Коробки сначала: a — azul, b — blanco, v — verde.')
V['2. Коробки после 30']=fig(scheme(2))
V['на 30 меньше, в белой']=fig(state2(),'Коробки после 30.')
V['3. Коробки в конце']=fig(scheme(3))
V['уходит половина зелёной, и столько же']=fig(state3(),'Коробки в конце.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
