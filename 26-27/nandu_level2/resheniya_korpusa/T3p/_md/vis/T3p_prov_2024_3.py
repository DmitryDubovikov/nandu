import json, sys
GOLD='#f0a83c'
INK,DIM='#cfdae6','#93a1b1'
RED,BLUE,WHITE='#e5636b','#5b9cf0','#e8eef6'
W=14
def strip(vals, colors=None, big=False):
    # vals: 12 элементов; число — стоит в клетке, None — свободная клетка
    # colors: 12 цветов блоков (None — без заливки)
    s=''
    for i,v in enumerate(vals):
        x=i*W
        if colors and colors[i]: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{colors[i]}' fill-opacity='0.25'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v is not None: s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
    if colors:  # жирные стыки блоков
        for i in range(1,12):
            if colors[i]!=colors[i-1]: s+=f"<line x1='{i*W}' y1='-1' x2='{i*W}' y2='{W+1}' stroke='{INK}' stroke-width='1.4'/>"
    vb=f'-1 -2 {12*W+2} {W+4}'
    st=" style='max-width:560px'" if big else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='Полоска'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
N=None
V={}
V['расстановка двенадцати фишек по клеткам полоски.']=fig(strip([N]*12,big=True),'Полоска.')
left =[N,N,N,6, 6,N,N,N,9, 9,N,N]
cl   =[RED]*4+[BLUE]*5+[WHITE]*3
right=[N,N,9, 9,N,N,N,6, 6,N,N,N]
cr   =[WHITE]*3+[BLUE]*5+[RED]*4
V['1. Миры N(красный слева) и N(белый слева).']=fig(strip(left,cl,True)+"<p class='ccap'>N(красный слева)</p>"+strip(right,cr,True)+"<p class='ccap'>N(белый слева)</p>")
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
