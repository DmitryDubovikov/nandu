import json, sys
GOLD,GREEN,RED,BLUE='#f0a83c','#5fd38d','#f2686c','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
MUTE='#4a5866'
W=14
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# полоска числа: первая цифра закреплена, остальные места пустые; справа — запас оставшихся цифр
def strip(first, pool):
    s=''
    for i in range(6):
        x=i*W
        s+=f"<rect x='{x}' y='4' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        s+=f"<text x='{x+W/2}' y='2' fill='{DIM}' font-size='3.4' text-anchor='middle'>{i+1}</text>"
        if i==0: s+=f"<text x='{x+W/2}' y='{4+W/2+2}' fill='{GOLD}' font-size='5.6' text-anchor='middle' font-weight='700'>{first}</text>"
    x0=6*W+10
    s+=f"<text x='{x0}' y='2' fill='{DIM}' font-size='3.4'>остаются</text>"
    for j,d in enumerate(pool):
        x=x0+j*10
        s+=f"<rect x='{x}' y='7' width='8' height='8' rx='1.5' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        s+=f"<text x='{x+4}' y='12.8' fill='{BLUE}' font-size='4.6' text-anchor='middle' font-weight='700'>{d}</text>"
    w=x0+len(pool)*10
    return f"<svg viewBox='-1 -1 {w+2} 21' role='img' aria-label='Число списка' style='max-width:520px'>{s}</svg>"

# полоса блоков: ширина блока пропорциональна числу чисел (или одинаковая, если числа ещё неизвестны)
def bar(x0,y,width,labels,sizes=None,texts=None,hl=None,h=10,fs=4.2):
    s=''
    n=len(labels)
    tot=sum(sizes) if sizes else n
    x=x0
    xs=[]
    for i,lab in enumerate(labels):
        w=width*(sizes[i] if sizes else 1)/tot
        on = hl is None or i==hl
        fill = GOLD if (hl is not None and i==hl) else 'none'
        s+=f"<rect x='{x:.2f}' y='{y}' width='{w:.2f}' height='{h}' fill='{fill}' fill-opacity='0.18' stroke='{GOLD if (hl is not None and i==hl) else INK}' stroke-width='{0.8 if (hl is not None and i==hl) else 0.5}'/>"
        col = LAB if on else DIM
        s+=f"<text x='{x+w/2:.2f}' y='{y+h/2+1.5}' fill='{col}' font-size='{fs}' text-anchor='middle' font-weight='600'>{lab}</text>"
        if texts: s+=f"<text x='{x+w/2:.2f}' y='{y+h+4.6}' fill='{DIM}' font-size='3.4' text-anchor='middle'>{texts[i]}</text>"
        xs.append((x,x+w))
        x+=w
    return s,xs

def marker(x,y,lab,col=GREEN,above=True):
    if above:
        return (f"<line x1='{x:.2f}' y1='{y-4}' x2='{x:.2f}' y2='{y+11}' stroke='{col}' stroke-width='0.9'/>"
                f"<text x='{x:.2f}' y='{y-5.2}' fill='{col}' font-size='3.6' text-anchor='middle' font-weight='700'>{lab}</text>")
    return (f"<line x1='{x:.2f}' y1='{y-1}' x2='{x:.2f}' y2='{y+14}' stroke='{col}' stroke-width='0.9'/>"
            f"<text x='{x:.2f}' y='{y+18.4}' fill='{col}' font-size='3.6' text-anchor='middle' font-weight='700'>{lab}</text>")

def bloki_idea():
    s,_=bar(0,2,180,['начало 1','начало 2','начало 3','начало 4','начало 5'],texts=['?']*5)
    return f"<svg viewBox='-1 0 182 19' role='img' aria-label='Блоки списка' style='max-width:600px'>{s}</svg>"

# б): лестница увеличений — блок, где лежит место, растягивается в следующую строку
def zoom():
    L=58; Wd=170; s=''
    rows=[
        (['1','2','3','4','5'],[60,60,120,60,60],['60','60','120','60','60'],2,200/360,'место 200 в списке'),
        (['31','32','33','34','35'],[24]*5,['24']*5,3,80/120,'место 80 в блоке 3'),
        (['341','342','343','345'],[6]*4,['6']*4,1,8/24,'место 8 в блоке 34'),
        (['342135','342153','342315','342351','342513','342531'],[1]*6,None,1,None,'место 2 в блоке 342'),
    ]
    y=8; prev=None
    for k,(labs,sz,tx,hl,frac,cap) in enumerate(rows):
        s+=f"<text x='0' y='{y+6.4}' fill='{LAB}' font-size='3.8' font-weight='600'>{cap}</text>"
        if prev:
            a,b=prev
            s+=f"<line x1='{a:.2f}' y1='{y-10}' x2='{L}' y2='{y}' stroke='{MUTE}' stroke-width='0.5' stroke-dasharray='1.4 1'/>"
            s+=f"<line x1='{b:.2f}' y1='{y-10}' x2='{L+Wd}' y2='{y}' stroke='{MUTE}' stroke-width='0.5' stroke-dasharray='1.4 1'/>"
        r,xs=bar(L,y,Wd,labs,sz,tx,hl,fs=3.6 if k==3 else 4.2)
        s+=r
        if frac is not None:
            s+=f"<line x1='{L+Wd*frac:.2f}' y1='{y-1.5}' x2='{L+Wd*frac:.2f}' y2='{y+11.5}' stroke='{GREEN}' stroke-width='0.9'/>"
        prev=xs[hl]
        y+=26 if k<3 else 0
    return f"<svg viewBox='-1 0 {L+Wd+2} {y+16}' role='img' aria-label='Поиск числа на месте 200' style='max-width:720px'>{s}</svg>"

def obzor():
    s,xs=bar(0,10,180,['1','2','3','4','5'],[60,60,120,60,60],['60','60','120','60','60'])
    s+=marker(180*200/360,10,'место 200: 342153')
    s+=marker(180*260/360,10,'423513: место 260',BLUE,above=False)
    return f"<svg viewBox='-1 0 182 36' role='img' aria-label='Обзор решения' style='max-width:600px'>{s}</svg>"

V={}
V['список идёт блоками по первой цифре']=fig(bloki_idea(),'Список Пабло.')
V['После 1 на пять оставшихся мест']=fig(strip('1',['2','3','3','4','5']),'Числа с 1 в начале.')
V['Сумма блоков по первой цифре с начала списка']=fig(zoom(),'Блок, в котором лежит место, растягиваем в строку ниже.')
V['Место(423513) = 259 + 1 = 260']=fig(obzor(),'Обзор решения: блоки по первой цифре.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
