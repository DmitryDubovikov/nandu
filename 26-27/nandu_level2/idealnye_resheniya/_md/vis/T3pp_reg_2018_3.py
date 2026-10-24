import json, sys
GOLD,GREEN,RED='#f0a83c','#5fd38d','#f2686c'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
def strip(vals, green=(), big=False):
    # vals: 4 элемента; цифра — закреплена, буква — свободная цифра числа
    s=''
    for i,v in enumerate(vals):
        x=i*W
        if i+1 in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v.isdigit(): s+=f"<text x='{x+W/2}' y='{W/2+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' font-weight='700'>{v}</text>"
        else: s+=f"<text x='{x+W/2}' y='{W/2+1.6}' fill='{DIM}' font-size='5' text-anchor='middle' font-style='italic'>{v}</text>"
    st=" style='max-width:240px'" if big else " style='max-width:190px'"
    return f"<svg viewBox='-1 -1 58 16' role='img' aria-label='Число'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    return fig(f"<div class='fgrid'>{c}</div>",cap)
def ostatki():
    # три столбца: остаток 0, 1, 2; 7 зачёркнута
    cols=[['0','3','6','9'],['1','4','7'],['2','5','8']]
    CW,RH,HH=22,9,9
    s=''
    for j,col in enumerate(cols):
        x=j*CW
        s+=f"<text x='{x+CW/2}' y='6' fill='{LAB}' font-size='4.2' text-anchor='middle'>остаток {j}</text>"
        for i,d in enumerate(col):
            y=HH+i*RH
            s+=f"<rect x='{x}' y='{y}' width='{CW}' height='{RH}' fill='none' stroke='{INK}' stroke-width='0.4'/>"
            if d=='7':
                s+=f"<text x='{x+CW/2}' y='{y+RH/2+1.8}' fill='{DIM}' font-size='5' text-anchor='middle'>7</text>"
                s+=f"<line x1='{x+CW/2-3}' y1='{y+RH/2+2.6}' x2='{x+CW/2+3}' y2='{y+RH/2-2.6}' stroke='{RED}' stroke-width='0.7'/>"
            else:
                s+=f"<text x='{x+CW/2}' y='{y+RH/2+1.8}' fill='{GOLD}' font-size='5' text-anchor='middle' font-weight='700'>{d}</text>"
    h=HH+4*RH
    return f"<svg viewBox='-1 -1 {3*CW+2} {h+2}' role='img' aria-label='Цифры по остаткам' style='max-width:260px'>{s}</svg>"
# тройки и остаток (как «Чётность суммы» в 25-26/nandu_level1/national/nandu_n1_nacional_1_cifry_uchebnik): 8 + 4
def troyki():
    BOX='#4a5866'
    def row(y,label,tr,ost,x0=18):
        r=f"<text x='2' y='{y+4.2}' fill='{LAB}' font-size='4.4' font-weight='700'>{label}</text>"
        x=x0
        for _ in range(tr):
            r+=f"<rect x='{x-1.6}' y='{y-1.6}' width='15.2' height='9.2' rx='2' fill='none' stroke='{BOX}' stroke-width='0.5'/>"
            for i in range(3): r+=f"<circle cx='{x+2+i*4.6}' cy='{y+3}' r='1.6' fill='{DIM}'/>"
            x+=18
        for i in range(ost): r+=f"<circle cx='{x+2+i*4.6}' cy='{y+3}' r='1.6' fill='{GOLD}'/>"
        return r
    s=row(2,'8',2,2)+row(14,'4',1,1)
    s+=f"<line x1='2' y1='25' x2='86' y2='25' stroke='{BOX}' stroke-width='0.4'/>"
    s+=f"<text x='2' y='33.2' fill='{LAB}' font-size='4.4' font-weight='700'>12</text>"
    x=18
    for _ in range(3):
        s+=f"<rect x='{x-1.6}' y='27.4' width='15.2' height='9.2' rx='2' fill='none' stroke='{BOX}' stroke-width='0.5'/>"
        for i in range(3): s+=f"<circle cx='{x+2+i*4.6}' cy='32' r='1.6' fill='{DIM}'/>"
        x+=18
    s+=f"<rect x='{x-1.6}' y='27.4' width='15.2' height='9.2' rx='2' fill='none' stroke='{GOLD}' stroke-width='0.7'/>"
    for i in range(3): s+=f"<circle cx='{x+2+i*4.6}' cy='32' r='1.6' fill='{GOLD}'/>"
    return f"<svg viewBox='0 0 92 39' role='img' aria-label='Тройки и остаток' style='max-width:420px'>{s}</svg>"

# цифры для b и c по остатку при делении на 3 — строка на остаток, справа сколько годных цифр
def ostatki_rows():
    rows=[('res(·, 3) = 0',[0,3,6,9],'четыре цифры'),('res(·, 3) = 1',[1,4,7],'две цифры'),('res(·, 3) = 2',[2,5,8],'три цифры')]
    s=''; y=2
    for lab,ds,cnt in rows:
        s+=f"<text x='0' y='{y+5.4}' fill='{DIM}' font-size='3.6' font-weight='600'>{lab}</text>"
        x=27
        for d in ds:
            bad = d==7
            s+=f"<rect x='{x}' y='{y}' width='8' height='8' rx='1.5' fill='none' stroke='{RED if bad else INK}' stroke-width='0.5'/>"
            s+=f"<text x='{x+4}' y='{y+5.8}' fill='{RED if bad else GOLD}' font-size='4.6' text-anchor='middle' font-weight='700'>{d}</text>"
            if bad: s+=f"<line x1='{x+1}' y1='{y+7}' x2='{x+7}' y2='{y+1}' stroke='{RED}' stroke-width='0.7'/>"
            x+=10
        s+=f"<text x='69' y='{y+5.4}' fill='{LAB}' font-size='3.8' font-weight='600'>→ {cnt}</text>"
        y+=11
    return f"<svg viewBox='0 0 100 {y+1}' role='img' aria-label='Цифры по остаткам' style='max-width:440px'>{s}</svg>"

# дерево-план: N → четыре операнда; N(17bc) → три мира по (res(b, 3), res(c, 3)); N(1a7c), N(1ab7) = как N(17bc)
BLUE,VIO='#5ba8f5','#c58af9'
def tree(step=None, vals=False):
    def on(k): return step is None or step==k
    def node(x,y,w,label,col,k,size=3.4,fill=None):
        cur = step==k and fill is None
        c = GOLD if cur else (col if on(k) else '#4a5866')
        f = GOLD if cur else (fill if (fill and on(k)) else '#121821')
        op = 0.22 if (cur or (fill and on(k))) else 1
        r=f"<rect x='{x-w/2}' y='{y}' width='{w}' height='8' rx='2' fill='{f}' fill-opacity='{op}' stroke='{c}' stroke-width='{1.0 if cur else 0.6}'/>"
        tc = c if (cur or (on(k) and col!=INK)) else (LAB if on(k) else '#4a5866')
        return r+f"<text x='{x}' y='{y+5.5}' fill='{tc}' font-size='{size}' text-anchor='middle' font-weight='600'>{label}</text>"
    def edge(x1,y1,x2,y2,k,dash=False):
        c = INK if on(k) else '#4a5866'
        d = " stroke-dasharray='1.4 1'" if dash else ''
        return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{c}' stroke-width='0.5'{d}/>"
    L1=[(26,'N(17bc)',1),(70,'N(1a7c)',2),(112,'N(1ab7)',2),(156,'N(2000–2017)',3)]
    if vals: L1=[(x,l+' = '+v,k) for (x,l,k),v in zip(L1,['25','25','25','1'])]
    s=''
    for x,_,k in L1: s+=edge(90,10,x,22,k)
    kids=[(9,'(0, 1)',BLUE),(26,'(1, 0)',GOLD),(43,'(2, 2)',GREEN)]
    if vals: kids=[(x,l+': '+v,c) for (x,l,c),v in zip(kids,['8','8','9'])]
    for x,_,_ in kids: s+=edge(26,30,x,42,1)
    # «= как N(17bc)»: пунктирные дуги к уже посчитанному узлу
    c2 = GOLD if step==2 else (INK if step is None else '#4a5866')
    for x in (70,112):
        s+=f"<path d='M{x} 30 Q {(x+26)/2} {38 if x==70 else 46} 36 29' fill='none' stroke='{c2}' stroke-width='0.6' stroke-dasharray='1.4 1' marker-end='url(#tr{step})'/>"
    s+=f"<text x='84' y='45' fill='{c2}' font-size='3.5' text-anchor='middle'>= как N(17bc)</text>"
    s+=node(90,2,22 if vals else 10,'N = 76' if vals else 'N',INK,0,3.8)
    for x,lab,k in L1: s+=node(x,22,(36 if k!=3 else 42) if vals else (26 if k!=3 else 32),lab,INK,k,3.8)
    for x,lab,col in kids: s+=node(x,42,16 if vals else 13,lab,col,1,3.3,col)
    s+=f"<text x='26' y='57' fill='{LAB if on(1) else '#4a5866'}' font-size='3.2' text-anchor='middle'>(res(b, 3), res(c, 3))</text>"
    mk=f"<defs><marker id='tr{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='{c2}'/></marker></defs>"
    return f"<svg viewBox='0 0 180 60' role='img' aria-label='Дерево решения' style='max-width:660px'>{mk}{s}</svg>"

V={}
V['7 стоит ровно на одном из мест 2, 3, 4']=grid([(strip(['1','7','b','c'],(3,4)),''),(strip(['1','a','7','c'],(2,4)),''),(strip(['1','a','b','7'],(2,3)),'')])
V['N = 25 + 25 + 25 + 1 = 76']=fig(tree(vals=True),'Обзор решения.')
V['сумма делится на 3 ровно тогда']=fig(troyki(),'Пример на числах, не из задачи: 8 + 4 = 12 — остатки 2 и 1 складываются в тройку.')
V['(8 + b + c) ⋮ 3 ⇔']=fig(ostatki_rows(),'Цифры для b и c по остатку от деления на 3; 7 занята.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
