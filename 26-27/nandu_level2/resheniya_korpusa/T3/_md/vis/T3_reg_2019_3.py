import json, sys
GOLD,GREEN,BLUE='#f0a83c','#5fd38d','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
DAYS=['Пн','Вт','Ср','Чт','Пт','Сб']
COL={'Г':GOLD,'М':BLUE,'А':GREEN,'вых':DIM}
def strip(vals, new=()):
    # vals: 6 элементов — занятие в день или None (ещё не решено)
    s=''
    for i,v in enumerate(vals):
        x=i*W
        s+=f"<text x='{x+W/2}' y='-2' fill='{DIM}' font-size='3.6' text-anchor='middle'>{DAYS[i]}</text>"
        if i in new: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v:
            size = 3.6 if v=='вых' else 5.6
            s+=f"<text x='{x+W/2}' y='{W/2+(1.2 if v=='вых' else 2)}' fill='{COL[v]}' font-size='{size}' text-anchor='middle' font-weight='700'>{v}</text>"
    return f"<svg viewBox='-1 -7 86 22' role='img' aria-label='Неделя' style='max-width:260px'>{s}</svg>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    cc=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'><div class='fgrid'>{c}</div>{cc}</figure>"
N=None
V={}
V['Неделя собирается в три хода']=grid([
    (strip([N,'Г',N,N,'Г',N],(1,4)),'дни гимнастики'),
    (strip(['М','Г',N,N,'Г',N],(0,)),'день мастерской'),
    (strip(['М','Г','А','вых','Г','А'],(2,3,5)),'выходной, остальное — английский'),
],'Г — гимнастика, А — английский, М — мастерская, вых — выходной.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
