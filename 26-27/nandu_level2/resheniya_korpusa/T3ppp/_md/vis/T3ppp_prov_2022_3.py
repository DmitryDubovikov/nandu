import json, sys
# монеты по весу: 3 — красная, 4 — синяя, 5 — золотая, 6 — фиолетовая, 7 — зелёная
COL={3:'#f2686c',4:'#5ba8f5',5:'#f0a83c',6:'#c58af9',7:'#5fd38d'}
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
R=5.2; STEP=12.4
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def coin(x,y,w):
    c=COL[w]
    return (f"<circle cx='{x}' cy='{y}' r='{R}' fill='{c}' fill-opacity='0.18' stroke='{c}' stroke-width='0.7'/>"
            f"<text x='{x}' y='{y+2}' fill='{c}' font-size='5.6' text-anchor='middle' font-weight='700'>{w}</text>")
def brace(x1,x2,y,label,col):
    return (f"<path d='M{x1} {y} v2.4 H{x2} v-2.4' fill='none' stroke='{col}' stroke-width='0.5'/>"
            f"<text x='{(x1+x2)/2}' y='{y+8.4}' fill='{col}' font-size='4.6' text-anchor='middle'>{label}</text>")
V={}
def paket():
    obyaz=[3,4,5,6,7]; lishn=[4,4,4,7,7,7]
    s=''; x=R+1; y=R+1
    x0=x
    for w in obyaz: s+=coin(x,y,w); x+=STEP
    x1=x-STEP
    x+=7
    x2=x
    for w in lishn: s+=coin(x,y,w); x+=STEP
    x3=x-STEP
    s+=f"<line x1='{x1+R+3.5}' y1='0' x2='{x1+R+3.5}' y2='{2*R+2}' stroke='{DIM}' stroke-width='0.4' stroke-dasharray='1.2 1.2'/>"
    s+=brace(x0-R,x1+R,2*R+3,'обязательный набор: 25 г',INK)
    s+=brace(x2-R,x3+R,2*R+3,'лишние монеты: 33 г',LAB)
    W=x3+R+1
    return f"<svg viewBox='0 0 {W} {2*R+15}' role='img' aria-label='Пример пакетика' style='max-width:520px'>{s}</svg>"
V['сверх обязательного набора']=fig(paket(),'Пакетик весом 58 г.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
