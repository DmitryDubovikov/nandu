import json, sys
GOLD,GREEN='#f0a83c','#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
RED='#ff7a7a'
W=10
def sq(r,c): return (r//2, c//2)
def board(empty=None, quads=False, ficha=None, closed=(), free=(), pair=False, mw=200, nums=False):
    # empty — пустой квадрат 2×2 (строка, столбец квадрата); ficha — клетка фишки левого верхнего квадрата;
    # closed — закрытые клетки (красный крест); free — свободные клетки (зелёные); pair — запрещённая пара у центра
    s=''
    for r in range(4):
        for c in range(4):
            x,y=c*W,r*W
            if empty is not None and sq(r,c)==empty:
                s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{DIM}' fill-opacity='0.28'/>"
            elif quads:
                col=GREEN if (sq(r,c)[0]+sq(r,c)[1])%2==0 else GOLD
                s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{col}' fill-opacity='0.16'/>"
            if (r,c) in free:
                s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.30'/>"
            s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.4'/>"
            if (r,c) in closed:
                d=2.6
                s+=f"<path d='M{x+d} {y+d}L{x+W-d} {y+W-d}M{x+W-d} {y+d}L{x+d} {y+W-d}' stroke='{RED}' stroke-width='0.9' stroke-linecap='round'/>"
    if quads or empty is not None or ficha is not None:
        s+=f"<line x1='{2*W}' y1='0' x2='{2*W}' y2='{4*W}' stroke='{LAB}' stroke-width='1.2'/>"
        s+=f"<line x1='0' y1='{2*W}' x2='{4*W}' y2='{2*W}' stroke='{LAB}' stroke-width='1.2'/>"
    s+=f"<rect x='0' y='0' width='{4*W}' height='{4*W}' fill='none' stroke='{LAB}' stroke-width='1.2'/>"
    if nums:
        for k,(qr,qc) in enumerate(((0,0),(0,1),(1,0),(1,1)),1):
            s+=f"<text x='{qc*2*W+W}' y='{-1.8 if qr==0 else 4*W+5.4}' fill='{LAB}' font-size='4' text-anchor='middle' font-weight='700'>{k}</text>"
    if pair:
        s+=f"<line x1='{2.5*W}' y1='{1.5*W}' x2='{1.5*W}' y2='{2.5*W}' stroke='{RED}' stroke-width='1' stroke-dasharray='1.6 1.2'/>"
        for (r,c) in ((1,2),(2,1)):
            s+=f"<circle cx='{c*W+W/2}' cy='{r*W+W/2}' r='2.6' fill='none' stroke='{RED}' stroke-width='0.8'/>"
    if ficha is not None:
        r,c=ficha
        s+=f"<circle cx='{c*W+W/2}' cy='{r*W+W/2}' r='3.2' fill='{GOLD}'/>"
    vb=f"-1 -7 {4*W+2} {4*W+15}" if nums else f"-1 -1 {4*W+2} {4*W+2}"
    return f"<svg viewBox='{vb}' role='img' aria-label='Доска 4×4' style='max-width:{mw}px'>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s,t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>",cap)
def rt_lb(): return [(r,c) for r in range(2) for c in range(2,4)]+[(r,c) for r in range(2,4) for c in range(2)]
def sub(f):
    cl=[p for p in rt_lb() if max(abs(p[0]-f[0]),abs(p[1]-f[1]))<=1]
    fr=[p for p in rt_lb() if p not in cl]
    return board(empty=(1,1),ficha=f,closed=cl,free=fr,pair=(f==(0,0)),mw=170,nums=True)
V={}
V['Способ — набор из трёх клеток доски']=fig(board(mw=320),'Доска 4×4.')
V['доска 4×4 разрезается на четыре квадрата 2×2']=fig(board(quads=True,mw=240,nums=True),'Квадраты 2×2 с номерами 1–4.')
V['1. Миры N(пуст 1), N(пуст 2), N(пуст 3), N(пуст 4).']=grid([
    (board(empty=(0,0),mw=150,nums=True),'N(пуст 1)'),(board(empty=(0,1),mw=150,nums=True),'N(пуст 2)'),
    (board(empty=(1,0),mw=150,nums=True),'N(пуст 3)'),(board(empty=(1,1),mw=150,nums=True),'N(пуст 4)')])
V['N(пуст 4) = N(в углу доски)']=grid([
    (sub((0,0)),'N(в углу доски)'),(sub((0,1)),'N(у квадрата 2)'),
    (sub((1,0)),'N(у квадрата 3)'),(sub((1,1)),'N(у центра доски)')],
    'Зелёные клетки свободны, крестом закрыты фишкой квадрата 1.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
