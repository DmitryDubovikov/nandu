import json, sys
GOLD,GREEN='#f0a83c','#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
def strip(vals, big=False, green=()):
    # vals: 6 элементов; число — стоит в клетке, None — свободная клетка cᵢ
    s=''
    for i,v in enumerate(vals):
        x=i*W
        if i+1 in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v is None: s+=f"<text x='{x+W/2}' y='{W/2+1.6}' fill='{DIM}' font-size='4.4' text-anchor='middle' font-style='italic'>c{'₁₂₃₄₅₆'[i]}</text>"
        else: s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
    vb='-1 -1 86 16'
    st=" style='max-width:460px'" if big else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='Полоска'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s,t in cells)
    return fig(f"<div class='fgrid2'>{c}</div>",cap)
N=None
V={}
V['Сколькими различными способами можно заполнить полоску?']=fig(strip([N]*6,True),'cᵢ — число в i-й клетке.')
V['1. Миры N(3, 8) и N(8, 3).']=grid([(strip([N,3,N,8,N,N],False),'N(3, 8)'),(strip([N,8,N,3,N,N],False),'N(8, 3)')])
V['N(4, 6) — 4 в c₂']=fig(strip([N,4,N,6,N,N],False,(3,5,6)))
V['N(6, 4) — 4 в c₄']=fig(strip([N,6,N,4,N,N],False,(5,6)))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
