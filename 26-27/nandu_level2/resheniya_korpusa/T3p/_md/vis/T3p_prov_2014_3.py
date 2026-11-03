import json, sys
GOLD,GREEN,GREY='#f0a83c','#5fd38d','#93a1b1'
INK,DIM='#cfdae6','#93a1b1'
W=14
def strip(mid=None, left=(), right=(), big=True):
    # строка чисел 1–19; mid — среднее закрашенное (золото), left/right — годные места крайних (зелёные),
    # между ними — обязательно незакрашенные (серые)
    s=''
    for n in range(1,20):
        x=(n-1)*W
        if n==mid: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GOLD}' fill-opacity='0.35'/>"
        elif n in left or n in right: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        elif mid is not None: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREY}' fill-opacity='0.12'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        col=GOLD if n==mid else (INK if (mid is None or n in left or n in right) else DIM)
        fw=" font-weight='700'" if n==mid else ''
        s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{col}' font-size='5.6' text-anchor='middle'{fw}>{n}</text>"
    vb=f'-1 -1 {19*W+2} {W+2}'
    st=" style='max-width:560px'" if big else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='Строка чисел 1–19'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
V={}
V['выбор трёх из чисел 1–19, порядок не важен.']=fig(strip(),'Строка чисел 1–19.')
V['1. Мир N(6).']=fig(strip(6,(1,),tuple(range(11,20))),'N(6): 6 — среднее; зелёные — где могут стоять крайние.')
V['среднее закрашенное сдвигается на 1 вправо']=fig(strip(10,tuple(range(1,6)),tuple(range(15,20))),'N(10): левых пять, правых пять.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
