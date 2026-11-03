import json, os, sys
GOLD,BLUE,GREEN,VIOL='#f0a83c','#5ba8f5','#5fd38d','#b48ef0'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def svg(inner,label,vb):
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# полоса-целое из равных кирпичиков: части подписаны словами сверху и долями снизу
def bar(parts):
    # parts: [(слово, кирпичиков, доля, значение или None, цвет)]
    n=sum(p[1] for p in parts); W=120; bw=W/n; x=8; s=''
    for word,k,frac,val,col in parts:
        w=k*bw
        for i in range(k):
            s+=f"<rect x='{x+i*bw}' y='8' width='{bw}' height='10' fill='{col}' fill-opacity='{0.28 if val else 0.10}' stroke='{INK if val else DIM}' stroke-width='0.4'/>"
        s+=f"<rect x='{x}' y='8' width='{w}' height='10' fill='none' stroke='{col}' stroke-width='0.9'/>"
        s+=txt(x+w/2,5.5,word,col,3.6)
        s+=txt(x+w/2,23.5,frac,col,3.6)
        if val: s+=f"<text x='{x+w/2}' y='14.4' fill='{LAB}' font-size='4.2' text-anchor='middle' font-weight='700' stroke='#3b3222' stroke-width='1.6' paint-order='stroke'>{val}</text>"
        x+=w
    return svg(s,'Полоса','0 0 144 27')

V={}
V['1/12 всех билетов заполняют добавки']=fig(
    bar([('A',6,'1/2',None,BLUE),('B',2,'1/6',None,GREEN),('C',3,'1/4',None,VIOL),('10 + 20 + 30',1,'1/12','60',GOLD)]),
    'Все проданные билеты: двенадцать равных частей.')
out=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','T1_prov_2019_1.vis.json')
json.dump(V,open(out,'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
