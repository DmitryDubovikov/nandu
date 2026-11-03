import json, sys
# карточка из условия: строка букв A–D и пустая строка для чисел
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
def card():
    s=''
    for i,L in enumerate('ABCD'):
        x=i*W
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{LAB}' font-size='5.6' text-anchor='middle'>{L}</text>"
        s+=f"<rect x='{x}' y='{W}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
    return s
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def svg(inner,mw):
    return f"<svg viewBox='-1 -1 {4*W+2} {2*W+2}' role='img' aria-label='Карточка' style='max-width:{mw}px'>{inner}</svg>"
V={}
V['Способ — четвёрка чисел']=fig(svg(card(),300),'Карточка из условия.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
