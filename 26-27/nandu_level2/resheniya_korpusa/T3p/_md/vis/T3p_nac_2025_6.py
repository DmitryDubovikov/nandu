import json, sys
GOLD,GREEN,BLUE='#f0a83c','#5fd38d','#6cb6ff'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
def board(strips=(), sq=None, free=False, rows=4, mid=False, big=False):
    # strips: (строка, столбец, 'H'|'V') — левая/верхняя клетка полоски, счёт с 0
    covered=set()
    for r,c,o in strips:
        for i in range(3): covered.add((r,c+i) if o=='H' else (r+i,c))
    s=''
    for r in range(rows):
        for c in range(4):
            x,y=c*W,r*W
            if free and (r,c) not in covered: s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
            if mid and c in (1,2): s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
            s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
    for r,c,o in strips:
        w,h=(3*W,W) if o=='H' else (W,3*W)
        s+=f"<rect x='{c*W+1.6}' y='{r*W+1.6}' width='{w-3.2}' height='{h-3.2}' rx='2' fill='{GOLD}' fill-opacity='0.35' stroke='{GOLD}' stroke-width='0.9'/>"
    if sq:
        r,c=sq
        s+=f"<rect x='{c*W+2.6}' y='{r*W+2.6}' width='{W-5.2}' height='{W-5.2}' rx='1.5' fill='{BLUE}' fill-opacity='0.45' stroke='{BLUE}' stroke-width='0.9'/>"
    vb=f'-1 -1 {4*W+2} {rows*W+2}'
    mw=280 if big else (200 if rows==4 else 160)
    st=f" style='max-width:{mw}px'"
    return f"<svg viewBox='{vb}' role='img' aria-label='Доска'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s,t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>",cap)
def rot(strips):
    # поворот на четверть оборота по часовой: клетка (r, c) -> (c, 3 - r)
    out=[]
    for r,c,o in strips:
        if o=='H': out.append((c,3-r,'V'))
        else: out.append((c,3-(r+2),'H'))
    return out
V={}
V['Способ — набор мест трёх одинаковых полосок']=fig(board(big=True),'Доска.')
V['Полоски закрывают 3 · 3 = 9 клеток']=fig(board([(0,0,'H'),(1,3,'V'),(3,0,'H')],sq=(1,1),free=True),'Одна раскладка полосок и семь мест для квадратной фишки.')
ex=[(0,0,'H'),(1,1,'H'),(3,0,'H')]
V['1. Миры N(три гориз.) и N(без гориз.).']=grid([(board(ex),'N(три гориз.)'),(board(rot(ex)),'N(без гориз.)')])
V['горизонтальная полоска лежит в строке слева или справа']=grid([(board([(0,0,'H')],rows=1,mid=True),'слева'),(board([(0,1,'H')],rows=1,mid=True),'справа')])
V['Две строки из трёх строк вертикальной']=fig(board([(0,0,'V'),(0,1,'H'),(2,1,'H')]))
V['Вторая горизонтальная — в одной из трёх строк']=fig(board([(0,0,'V'),(1,1,'H'),(3,0,'H')]))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
