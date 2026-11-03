import json, sys
GOLD,GREEN,BLUE='#f0a83c','#5fd38d','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=12
LANG=[BLUE,BLUE,GOLD,GOLD]+[GREEN]*6
def strip(chosen, new=()):
    # chosen: номера выбранных песен; new: выбранные этим ходом (обведены)
    s=''
    for i in range(10):
        x=i*W; n=i+1; col=LANG[i]
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{col}' fill-opacity='{0.55 if n in chosen else 0.1}'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if n in new: s+=f"<rect x='{x+0.8}' y='0.8' width='{W-1.6}' height='{W-1.6}' fill='none' stroke='{LAB}' stroke-width='0.9'/>"
        s+=f"<text x='{x+W/2}' y='{W/2+1.8}' fill='{LAB if n in chosen else DIM}' font-size='{5 if n in chosen else 4.2}' text-anchor='middle' font-weight='{700 if n in chosen else 400}'>{n}</text>"
    return f"<svg viewBox='-1 -1 122 14' role='img' aria-label='Диск' style='max-width:420px'>{s}</svg>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    cc=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'><div class='fgrid'>{c}</div>{cc}</figure>"
V={}
V['Набор собирается в три хода']=grid([
    (strip({2},{2}),'английские'),
    (strip({2,3},{3}),'французские'),
    (strip({2,3,5,7,8,10},{5,7,8,10}),'испанские на оставшиеся места'),
],'Песни диска: синие — английские, золотые — французские, зелёные — испанские.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
