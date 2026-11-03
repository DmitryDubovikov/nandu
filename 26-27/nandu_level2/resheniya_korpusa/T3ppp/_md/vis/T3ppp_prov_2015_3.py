import json, sys
# доска: числа с последней цифрой 2 или 7 в две строки по 10; под каждым числом — его x (сколько пятёрок сверх 2)
NUM='#e8eef6'; XCOL='#f0a83c'
INK,DIM='#cfdae6','#93a1b1'
W=20; H=14
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def board():
    s=''
    for r in range(2):
        y0=r*(H+12)
        for i in range(10):
            x_=r*10+i; n=2+5*x_; x0=i*W
            s+=f"<rect x='{x0}' y='{y0}' width='{W}' height='{H}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
            s+=f"<text x='{x0+W/2}' y='{y0+H/2+2}' fill='{NUM}' font-size='6' text-anchor='middle' font-weight='700'>{n}</text>"
            s+=f"<text x='{x0+W/2}' y='{y0+H+7}' fill='{XCOL}' font-size='5' text-anchor='middle'>x = {x_}</text>"
    return f"<svg viewBox='-1 -1 {10*W+2} {2*H+12+10}' role='img' aria-label='Числа на доске' style='max-width:560px'>{s}</svg>"
V={}
V['x — сколько пятёрок в числе доски сверх 2']=fig(board(),'Доска: под каждым числом его x.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
