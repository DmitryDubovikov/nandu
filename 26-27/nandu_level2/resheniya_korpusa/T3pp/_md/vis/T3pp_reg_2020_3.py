import json, sys
GOLD,GREEN,RED='#f0a83c','#5fd38d','#f2686c'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
def strip(vals):
    # vals: цифра — уже стоит, '' — свободное место; над клеткой номер места
    n=len(vals); s=''
    for i,v in enumerate(vals):
        x=i*W
        s+=f"<text x='{x+W/2}' y='-1.6' fill='{DIM}' font-size='3.4' text-anchor='middle'>{i+1}</text>"
        if not v: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v: s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
    return f"<svg viewBox='-1 -6 {n*W+2} {W+7}' role='img' aria-label='Число' style='max-width:{n*48}px'>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    return fig(f"<div class='fgrid'>{c}</div>",cap)

# годные цифры по местам числа от 201 до 999 — строка на место, 5 зачёркнута, справа сколько годных
def mesta_rows():
    rows=[('место 1',[2,3,4,5,6,7,8,9],'семь цифр'),('место 2',[0,1,2,3,4,5,6,7,8,9],'девять цифр'),('место 3',[1,3,5,7,9],'четыре цифры')]
    s=''; y=2
    for lab,ds,cnt in rows:
        s+=f"<text x='0' y='{y+5.4}' fill='{DIM}' font-size='3.6' font-weight='600'>{lab}</text>"
        x=16
        for d in ds:
            bad = d==5
            s+=f"<rect x='{x}' y='{y}' width='8' height='8' rx='1.5' fill='none' stroke='{RED if bad else INK}' stroke-width='0.5'/>"
            s+=f"<text x='{x+4}' y='{y+5.8}' fill='{RED if bad else GOLD}' font-size='4.6' text-anchor='middle' font-weight='700'>{d}</text>"
            if bad: s+=f"<line x1='{x+1}' y1='{y+7}' x2='{x+7}' y2='{y+1}' stroke='{RED}' stroke-width='0.7'/>"
            x+=10
        s+=f"<text x='118' y='{y+5.4}' fill='{LAB}' font-size='3.8' font-weight='600'>→ {cnt}</text>"
        y+=11
    return f"<svg viewBox='0 0 148 {y+1}' role='img' aria-label='Цифры по местам' style='max-width:600px'>{s}</svg>"

# дерево-обзор: N → три промежутка, в узле значение, под узлом произведение
def tree():
    def node(x,y,w,label,size=3.6):
        return (f"<rect x='{x-w/2}' y='{y}' width='{w}' height='8' rx='2' fill='#121821' stroke='{INK}' stroke-width='0.6'/>"
                f"<text x='{x}' y='{y+5.5}' fill='{LAB}' font-size='{size}' text-anchor='middle' font-weight='600'>{label}</text>")
    L1=[(28,'N(201–999) = 252','7 · 9 · 4'),(90,'N(1000–1999) = 324','9 · 9 · 4'),(152,'N(2000–2019) = 8','2 · 4')]
    s=''
    for x,_,_ in L1: s+=f"<line x1='90' y1='10' x2='{x}' y2='22' stroke='{INK}' stroke-width='0.5'/>"
    s+=node(90,2,22,'N = 584',3.8)
    for x,lab,pr in L1:
        s+=node(x,22,46,lab)
        s+=f"<text x='{x}' y='36' fill='{GOLD}' font-size='3.4' text-anchor='middle'>{pr}</text>"
    return f"<svg viewBox='0 0 180 39' role='img' aria-label='Обзор решения' style='max-width:660px'>{s}</svg>"

V={}
V['N = N(201–999) + N(1000–1999) + N(2000–2019)']=grid([(strip(['','','']),'201–999'),(strip(['1','','','']),'1000–1999'),(strip(['2','0','','']),'2000–2019')])
V['на месте 3 стоит нечётная цифра, кроме 5']=fig(mesta_rows(),'Цифры для мест числа от 201 до 999; 5 запрещена.')
V['N = 252 + 324 + 8 = 584']=fig(tree(),'Обзор решения.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
