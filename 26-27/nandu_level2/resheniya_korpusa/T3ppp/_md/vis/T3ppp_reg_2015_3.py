import json, sys
# карточка: строка букв A–E и строка чисел; синие — числа мира (B и D), зелёная заливка — свободная клетка
BLUE='#5ba8f5'
GREEN='#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
def card(vals=None, green=()):
    s=''
    for i,L in enumerate('ABCDE'):
        x=i*W
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{LAB}' font-size='5.6' text-anchor='middle'>{L}</text>"
        if i+1 in green: s+=f"<rect x='{x}' y='{W}' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='{W}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        v=vals[i] if vals else None
        if v: s+=f"<text x='{x+W/2}' y='{W+W/2+2}' fill='{BLUE}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
    return s
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def svg(inner,mw):
    return f"<svg viewBox='-1 -1 {5*W+2} {2*W+2}' role='img' aria-label='Карточка' style='max-width:{mw}px'>{inner}</svg>"
V={}
V['Способ — набор пяти чисел']=fig(svg(card(),360),'Карточка из условия.')
V['A < 2 ⇒ A = 1']=fig(svg(card(['1','2',None,'13',None],(3,5)),260),'Мир B = 2: свободны C и E.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
