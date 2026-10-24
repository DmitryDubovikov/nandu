import json, sys
GOLD,GREEN,BLUE='#f0a83c','#5fd38d','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
def strip(vals, green=()):
    # vals: 4 элемента — текст в клетке или None (свободное место)
    s=''
    for i,v in enumerate(vals):
        x=i*W
        if i+1 in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v:
            col = BLUE if v=='буква' else GOLD
            size = 3.4 if v=='буква' else 5.6
            s+=f"<text x='{x+W/2}' y='{W/2+(1.2 if v=='буква' else 2)}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='700'>{v}</text>"
    return f"<svg viewBox='-1 -1 58 16' role='img' aria-label='Пароль' style='max-width:190px'>{s}</svg>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    cc=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'><div class='fgrid'>{c}</div>{cc}</figure>"
B='буква'
V={}
V['Пароль собирается в три хода']=grid([(strip([B,'7',None,None],(3,4)),''),(strip([B,None,'7',None],(2,4)),''),(strip([B,None,None,'7'],(2,3)),'')])
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
