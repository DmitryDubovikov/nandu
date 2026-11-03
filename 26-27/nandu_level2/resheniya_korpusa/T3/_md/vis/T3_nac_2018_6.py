import json, sys
GOLD,GREEN,BLUE='#f0a83c','#5fd38d','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
def strip(vals, green=()):
    # vals: 7 элементов — город в клетке или None (свободное место); под клеткой — номер места
    s=''
    for i,v in enumerate(vals):
        x=i*W
        if i+1 in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v:
            s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
        s+=f"<text x='{x+W/2}' y='{W+5}' fill='{DIM}' font-size='3.4' text-anchor='middle'>{i+1}</text>"
    return f"<svg viewBox='-1 -1 {7*W+2} {W+8}' role='img' aria-label='Маршрут' style='max-width:300px'>{s}</svg>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    cc=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'><div class='fgrid'>{c}</div>{cc}</figure>"
def ef(k):
    v=[None]*7; v[k-1]='E'; v[k]='F'
    return strip(v, tuple(i for i in range(1,8) if i not in (k,k+1)))
V={}
V['Маршрут собирается в три хода']=grid([(ef(1),''),(ef(3),''),(ef(6),'')])
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
