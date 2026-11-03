import json, sys
GOLD,GREEN,BLUE,VIOL='#f0a83c','#5fd38d','#5aa9e6','#b48cf0'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
LET=['EEEE','ERRE','ERRE','EEEE']
def board(fills=None, big=False):
    # fills: {номер клетки: цвет}; номер клетки — по строкам, 1–16
    fills=fills or {}
    s=''
    for r in range(4):
        for c in range(4):
            n=r*4+c+1; x,y=c*W,r*W
            if n in fills: s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{fills[n]}' fill-opacity='0.30'/>"
            s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
            col=GOLD if fills.get(n)==GOLD else LAB
            s+=f"<text x='{x+W/2}' y='{y+W/2+2.4}' fill='{col}' font-size='6' text-anchor='middle' font-weight='700'>{LET[r][c]}</text>"
            s+=f"<text x='{x+1.2}' y='{y+3.6}' fill='{DIM}' font-size='2.8'>{n}</text>"
    st=" style='max-width:300px'" if big else " style='max-width:220px'"
    return f"<svg viewBox='-1 -1 58 58' role='img' aria-label='Доска 4 × 4'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def nb(a):
    ra,ca=(a-1)//4,(a-1)%4
    return {r*4+c+1 for r in range(4) for c in range(4) if (r,c)!=(ra,ca) and abs(r-ra)<=1 and abs(c-ca)<=1 and LET[r][c]=='E'}
def world(r1,r2):
    f={}
    for n in nb(r1): f[n]=BLUE
    for n in nb(r2): f[n]=VIOL if n in f else GREEN
    f[r1]=GOLD; f[r2]=GOLD
    return f
V={}
V['путь E → R → R → E']=fig(board(big=True),'Номера клеток — по строкам.')
V['N(R, R по стороне): пара (6, 7)']=fig(board(world(6,7)),'синие — соседки-E клетки 6, зелёные — клетки 7, фиолетовые — общие соседки-E')
V['N(R, R по вершине): пара (6, 11)']=fig(board(world(6,11)),'синие — соседки-E клетки 6, зелёные — клетки 11')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
