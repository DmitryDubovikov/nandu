import json, sys
GOLD,GREEN,BLUE='#f0a83c','#5fd38d','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
CW,CH,GX,GY=12,9,4,2   # карточка: ширина, высота; промежутки между колонками и карточками
def cols_svg(cols, first_green=True, empty=(), stock=None, label='Раскладка карточек', maxw=170):
    # cols: список колонок слева направо, колонка — список букв сверху вниз; None — пустое место
    # empty: номера колонок (с 0), места которых рисуются пустыми золотом
    s=''
    for j,col in enumerate(cols):
        x=j*(CW+GX)
        for i,v in enumerate(col):
            y=i*(CH+GY)
            if j==0 and first_green:
                s+=f"<rect x='{x}' y='{y}' width='{CW}' height='{CH}' rx='1.2' fill='{GREEN}' fill-opacity='0.22'/>"
            if v is None:
                s+=f"<rect x='{x}' y='{y}' width='{CW}' height='{CH}' rx='1.2' fill='{GOLD}' fill-opacity='0.12' stroke='{GOLD}' stroke-width='0.5' stroke-dasharray='1.4 1'/>"
            else:
                s+=f"<rect x='{x}' y='{y}' width='{CW}' height='{CH}' rx='1.2' fill='none' stroke='{INK}' stroke-width='0.5'/>"
                col_=BLUE if v in 'AB' else LAB
                s+=f"<text x='{x+CW/2}' y='{y+CH/2+2}' fill='{col_}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
    w=len(cols)*(CW+GX)-GX
    h=3*(CH+GY)-GY
    if stock:
        x0=w+8
        s+=f"<text x='{x0}' y='{CH/2+2}' fill='{DIM}' font-size='4.2'>запас:</text>"
        for i,v in enumerate(stock):
            s+=f"<text x='{x0+i*7}' y='{CH+GY+CH/2+2}' fill='{GOLD}' font-size='5.6' font-weight='700'>{v}</text>"
        w=x0+len(stock)*7
    return f"<svg viewBox='-1 -1 {w+2} {h+2}' role='img' aria-label='{label}' style='max-width:{maxw}px'>{s}</svg>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    cc=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'><div class='fgrid'>{c}</div>{cc}</figure>"
V={}
V['Раскладка собирается в два хода']=grid([
    (cols_svg([['A','B'],['C','D','E'],['F']]),'в первой колонке 2 карточки'),
    (cols_svg([['E','B','A'],['D'],['F','C']]),'в первой колонке 3 карточки'),
])
V['раскладку C, D, E, F задают']=grid([
    (cols_svg([['A','B'],[None,None],[None],[None]],stock='CDEF',label='Высоты 2, 1, 1 и запас C, D, E, F',maxw=330),'высоты 2 + 1 + 1: четыре пустых места'),
])
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
