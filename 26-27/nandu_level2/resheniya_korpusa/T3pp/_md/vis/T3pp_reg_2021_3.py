import json, sys
GOLD,GREEN,RED='#f0a83c','#5fd38d','#f2686c'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
BLUE='#5ba8f5'
W=14
def strip(vals, green=()):
    # vals: 2–4 элемента; цифра — закреплена, буква — свободная цифра числа
    s=''
    for i,v in enumerate(vals):
        x=i*W
        if i+1 in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v.isdigit(): s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
        else: s+=f"<text x='{x+W/2}' y='{W/2+1.6}' fill='{DIM}' font-size='5' text-anchor='middle' font-style='italic'>{v}</text>"
    n=len(vals)
    return f"<svg viewBox='-1 -1 {n*W+2} 16' role='img' aria-label='Число' style='max-width:{n*48}px'>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    return fig(f"<div class='fgrid'>{c}</div>",cap)

def place(pat):
    # свободное место (буква) — зелёным
    return strip(list(pat),tuple(i+1 for i,ch in enumerate(pat) if not ch.isdigit()))

# цифры для a: на месте 2 или 3 — без 1 и 9; на месте 1 — ещё и без 0
def cifry_rows():
    rows=[('a на месте 2 или 3',{1,9},'восемь цифр'),('a на месте 1',{0,1,9},'семь цифр')]
    s=''; y=2
    for lab,bad_set,cnt in rows:
        s+=f"<text x='0' y='{y+5.4}' fill='{DIM}' font-size='3.6' font-weight='600'>{lab}</text>"
        x=36
        for d in range(10):
            bad = d in bad_set
            s+=f"<rect x='{x}' y='{y}' width='8' height='8' rx='1.5' fill='none' stroke='{RED if bad else INK}' stroke-width='0.5'/>"
            s+=f"<text x='{x+4}' y='{y+5.8}' fill='{RED if bad else GOLD}' font-size='4.6' text-anchor='middle' font-weight='700'>{d}</text>"
            if bad: s+=f"<line x1='{x+1}' y1='{y+7}' x2='{x+7}' y2='{y+1}' stroke='{RED}' stroke-width='0.7'/>"
            x+=10
        s+=f"<text x='{x+2}' y='{y+5.4}' fill='{LAB}' font-size='3.8' font-weight='600'>→ {cnt}</text>"
        y+=11
    return f"<svg viewBox='0 0 172 {y+1}' role='img' aria-label='Цифры для a' style='max-width:600px'>{s}</svg>"

# обзор: N → четыре операнда по длине; N(3 цифры) → три пары миров по месту a; N(1000–1999) → три мира по месту 9
def tree():
    def node(x,y,w,label,col=INK,fill=None,size=3.6):
        f = fill or '#121821'
        op = 0.22 if fill else 1
        tc = col if col!=INK else LAB
        return (f"<rect x='{x-w/2}' y='{y}' width='{w}' height='8' rx='2' fill='{f}' fill-opacity='{op}' stroke='{col}' stroke-width='0.6'/>"
                f"<text x='{x}' y='{y+5.5}' fill='{tc}' font-size='{size}' text-anchor='middle' font-weight='600'>{label}</text>")
    def edge(x1,y1,x2,y2,dash=False):
        d = " stroke-dasharray='1.4 1'" if dash else ''
        return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{INK}' stroke-width='0.5'{d}/>"
    L1=[(22,'N(2 цифры) = 2',34),(76,'N(3 цифры) = 46',36),(150,'N(1000–1999) = 192',46),(208,'N(2000–2020) = 1',40)]
    s=''
    for x,_,_ in L1: s+=edge(115,10,x,22)
    k3=[(48,'19a, 91a: 16',BLUE),(76,'1a9, 9a1: 16',GOLD),(104,'a19, a91: 14',GREEN)]
    for x,_,_ in k3: s+=edge(76,30,x,42)
    k4=[(134,'19bc: 64'),(160,'1a9c: 64'),(186,'1ab9: 64')]
    for x,_ in k4: s+=edge(150,30,x,42)
    s+=node(115,2,22,'N = 241',INK,None,3.8)
    for x,lab,w in L1: s+=node(x,22,w,lab)
    for x,lab,col in k3: s+=node(x,42,25,lab,col,col,3.2)
    for x,lab in k4: s+=node(x,42,23,lab,INK,None,3.2)
    s+=f"<text x='76' y='57' fill='{LAB}' font-size='3.2' text-anchor='middle'>место a</text>"
    s+=f"<text x='173' y='57' fill='{LAB}' font-size='3.2' text-anchor='middle'>= как N(19bc)</text>"
    s+=f"<line x1='149' y1='52' x2='197' y2='52' stroke='{DIM}' stroke-width='0.4' stroke-dasharray='1.4 1'/>"
    return f"<svg viewBox='0 0 232 60' role='img' aria-label='Дерево решения' style='max-width:700px'>{s}</svg>"

V={}
V['1 и 9 занимают два места из трёх']=grid([(place(p),'') for p in ['19a','91a','1a9','9a1','a19','a91']])
V['На первом месте a ещё и не 0']=fig(cifry_rows(),'Цифры для a.')
V['9 стоит ровно на одном из мест 2, 3, 4']=grid([(place(p),'') for p in ['19bc','1a9c','1ab9']])
V['N = 2 + 46 + 192 + 1 = 241']=fig(tree(),'Обзор решения.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
