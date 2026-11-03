import json, sys
GOLD,GREEN,RED='#f0a83c','#5fd38d','#f2686c'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
BLUE,VIO='#5ba8f5','#c58af9'
W=14
def strip(vals, green=()):
    # vals: цифра — закреплена (золото), 'ч' — чётная цифра (зелёным), буква — свободная цифра
    s=''
    for i,v in enumerate(vals):
        x=i*W
        if i+1 in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v.isdigit(): s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
        elif v=='ч': s+=f"<text x='{x+W/2}' y='{W/2+1.8}' fill='{GREEN}' font-size='4.2' text-anchor='middle' font-weight='700'>чёт</text>"
        else: s+=f"<text x='{x+W/2}' y='{W/2+1.6}' fill='{DIM}' font-size='5' text-anchor='middle' font-style='italic'>{v}</text>"
    return s
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# два случая: какое число кончается на 5
def sluchai():
    s=''
    rows=[(['·','5'],['·','·','ч']),(['·','ч'],['·','·','5'])]
    for r,(a,b) in enumerate(rows):
        y=r*24
        s+=f"<g transform='translate(0,{y})'>{strip(a)}</g>"
        s+=f"<text x='35' y='{y+W/2+2}' fill='{LAB}' font-size='6' text-anchor='middle'>·</text>"
        s+=f"<g transform='translate(42,{y})'>{strip(b)}</g>"
    s+=f"<text x='42' y='{W+7}' fill='{DIM}' font-size='4.2' text-anchor='middle'>или</text>"
    return f"<svg viewBox='-1 -1 88 40' role='img' aria-label='Два случая' style='max-width:300px'>{s}</svg>"

# врезка: 32 · 15 = (30 + 2) · (10 + 5), четыре куска
def kuski():
    X0,Y0=12,8
    WA,WB,HA,HB=48,12,30,18   # 30 | 2 по ширине, 10 | 5 по высоте (не в масштабе)
    s=''
    s+=f"<text x='{X0+WA/2}' y='5' fill='{LAB}' font-size='4.6' text-anchor='middle' font-weight='600'>30</text>"
    s+=f"<text x='{X0+WA+WB/2}' y='5' fill='{GOLD}' font-size='4.6' text-anchor='middle' font-weight='700'>2</text>"
    s+=f"<text x='{X0-3}' y='{Y0+HA/2+1.6}' fill='{LAB}' font-size='4.6' text-anchor='end' font-weight='600'>10</text>"
    s+=f"<text x='{X0-3}' y='{Y0+HA+HB/2+1.6}' fill='{GOLD}' font-size='4.6' text-anchor='end' font-weight='700'>5</text>"
    cells=[(X0,Y0,WA,HA,'300',False),(X0+WA,Y0,WB,HA,'20',False),(X0,Y0+HA,WA,HB,'150',False),(X0+WA,Y0+HA,WB,HB,'10',True)]
    for x,y,w,h,t,g in cells:
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{GOLD if g else '#121821'}' fill-opacity='{0.25 if g else 1}' stroke='{GOLD if g else INK}' stroke-width='{0.8 if g else 0.5}'/>"
        s+=f"<text x='{x+w/2}' y='{y+h/2+1.8}' fill='{GOLD if g else DIM}' font-size='4.8' text-anchor='middle' font-weight='700'>{t}</text>"
    return f"<svg viewBox='0 0 76 58' role='img' aria-label='32 · 15 по кускам' style='max-width:300px'>{s}</svg>"

# трёхзначное на 8: выбираем две цифры из 1…7, порядок навязан
def vybor():
    s=''
    for i,d in enumerate(range(1,8)):
        x=i*10; ch=d in (2,5)
        if ch: s+=f"<rect x='{x}' y='0' width='8' height='8' rx='1.5' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='8' height='8' rx='1.5' fill='none' stroke='{GREEN if ch else INK}' stroke-width='{0.8 if ch else 0.4}'/>"
        s+=f"<text x='{x+4}' y='5.8' fill='{GREEN if ch else DIM}' font-size='4.6' text-anchor='middle' font-weight='700'>{d}</text>"
    s+=f"<text x='76' y='5.8' fill='{LAB}' font-size='5' text-anchor='middle'>→</text>"
    s+=f"<g transform='translate(84,-3) scale(0.8)'>{strip(['2','5','8'],(1,2))}</g>"
    return f"<svg viewBox='-1 -4 120 16' role='img' aria-label='Выбор двух цифр' style='max-width:480px'>{s}</svg>"

# обзор решения: N → два произведения → четыре множителя; у составных — слагаемые по последней цифре
def tree():
    def node(x,y,w,label,col=INK,size=3.6,fill=None):
        f = fill or '#121821'; op = 0.22 if fill else 1
        return (f"<rect x='{x-w/2}' y='{y}' width='{w}' height='8' rx='2' fill='{f}' fill-opacity='{op}' stroke='{col}' stroke-width='0.6'/>"
                f"<text x='{x}' y='{y+5.5}' fill='{col if col!=INK else LAB}' font-size='{size}' text-anchor='middle' font-weight='600'>{label}</text>")
    def edge(x1,y1,x2,y2): return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{INK}' stroke-width='0.5'/>"
    s=''
    L1=[(55,'4 · 34 = 136'),(155,'16 · 6 = 96')]
    L2=[(30,'N(дв. на 5) = 4',None),(80,'N(тр. на чёт) = 34','t'),(130,'N(дв. на чёт) = 16','d'),(180,'N(тр. на 5) = 6',None)]
    for x,_ in L1: s+=edge(105,10,x,22)
    for (x,_,_),p in zip(L2,[55,55,155,155]): s+=edge(p,30,x,42)
    kids={'t':['0','3','10','21'],'d':['1','3','5','7']}
    cols=[BLUE,GOLD,GREEN,VIO]
    for x,_,k in L2:
        if not k: continue
        for i,(v,c) in enumerate(zip(kids[k],cols)):
            kx=x-16.5+i*11
            s+=edge(x,50,kx,60)+node(kx,60,9,v,c,3.4,c)
        s+=f"<text x='{x}' y='75' fill='{DIM}' font-size='3.2' text-anchor='middle'>на 2, 4, 6, 8</text>"
    s+=node(105,2,22,'N = 232',INK,3.8)
    for x,l in L1: s+=node(x,22,30,l,INK,3.6)
    for x,l,_ in L2: s+=node(x,42,40,l,INK,3.3)
    return f"<svg viewBox='0 0 210 78' role='img' aria-label='Обзор решения' style='max-width:680px'>{s}</svg>"

V={}
V['десятки, умноженные на что угодно']=fig(kuski(),'Пример на числах, не из задачи: 32 · 15 = 300 + 20 + 150 + 10 = 480; 300, 20 и 150 — целые десятки, ⋮ 10 решает только 2 · 5 = 10.')
V['случаев два']=fig(sluchai(),'Два случая: какое из чисел кончается на 5.')
V['трёхзначное задаёт только выбор двух цифр']=fig(vybor(),'Трёхзначное на 8: выбраны 2 и 5, число 258.')
V['N = 136 + 96 = 232']=fig(tree(),'Обзор решения.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
