import json, sys
# фишки: красные и синие кружки, блоки разделены промежутком; над блоком — буква или длина, под блоком — длина
RED,BLUE='#f0717a','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
D=11      # шаг фишки
GAP=7     # промежуток между блоками
R=4.6     # радиус фишки
def row(lengths, top, bottom=True):
    # lengths: длины блоков слева направо, первый красный; top: подписи над блоками
    s=''; x=0
    for i,n in enumerate(lengths):
        col=RED if i%2==0 else BLUE
        x0=x
        for j in range(n):
            s+=f"<circle cx='{x+D/2}' cy='19' r='{R}' fill='{col}' fill-opacity='0.85' stroke='{INK}' stroke-width='0.4'/>"
            x+=D
        cx=(x0+x)/2
        s+=f"<text x='{cx}' y='8' fill='{col}' font-size='9.5' text-anchor='middle' font-weight='700'>{top[i]}</text>"
        if bottom:
            s+=f"<text x='{cx}' y='36' fill='{DIM}' font-size='8.5' text-anchor='middle'>{n}</text>"
        x+=GAP
    return s, x-GAP
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def svg(lengths, top, bottom=True, label='Ряд фишек'):
    s,w=row(lengths,top,bottom)
    h=40 if bottom else 27
    return f"<svg viewBox='-2 -1 {w+4} {h}' role='img' aria-label='{label}' style='max-width:560px'>{s}</svg>"
V={}
LET=['r₁','b₁','r₂','b₂','r₃','b₃','r₄','b₄']
V['длины синих блоков слева направо']=fig(svg([1,2,3,3,4,5,10,8],LET),'Пример ряда.')
V['длины всех блоков — числа 1, 2, 3, 4, 5, 6, 7, 8']=fig(svg([1,3,2,4,7,5,8,6],LET),'Ряд с красными длинами 1, 2, 7, 8.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
