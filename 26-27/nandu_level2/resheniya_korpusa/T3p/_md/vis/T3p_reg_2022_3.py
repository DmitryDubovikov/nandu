import json, sys
INK,DIM='#cfdae6','#93a1b1'
COL={'К':'#e0605a','З':'#5fd38d','С':'#5aa0e6'}
W=14
def strip(vals, big=False):
    # vals: 7 элементов; 'К', 'З', 'С' — цвет клетки, None — клетка пустая
    s=''
    for i,v in enumerate(vals):
        x=i*W
        if v is not None:
            s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{COL[v]}' fill-opacity='0.55'/>"
            s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{INK}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
    vb='-1 -1 100 16'
    st=" style='max-width:560px'" if big else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='Доска 7 × 1'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s,t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>",cap)
N=None
K,Z,C='К','З','С'
V={}
V['Способ — раскраска семи клеток доски']=fig(strip([N]*7,True),'Доска 7 × 1.')
V['1. N(пустая клетка).']=fig(strip([K,C,C,N,Z,C,C]),'Пример: К — красная, З — зелёная, С — синяя.')
V['2. Миры N(две красные) и N(две зелёные).']=grid([(strip([C,K,C,Z,K,C,C]),'N(две красные)'),(strip([Z,C,K,C,C,Z,C]),'N(две зелёные)')],'Примеры.')
V['3. N(пять синих).']=fig(strip([C,C,K,C,Z,C,C]),'Пример.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
