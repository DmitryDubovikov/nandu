import json, sys
GOLD,GREEN,BLUE,VIOLET,RED='#f0a83c','#5fd38d','#5aa9e6','#b48ef0','#ef6b6b'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
R=7; D=20
POS={'l':(-D,0),'r':(D,0),'t':(0,-D),'b':(0,D),'x':(0,0)}
def cross(vals=None, fill=None, big=False):
    # vals: {кружок: цифра}; кружок без цифры подписан своей буквой; fill: {кружок: цвет подсветки}
    vals=vals or {}; fill=fill or {}
    s=''
    for sg in (-1,1):   # отрезки линий только между кружками
        s+=f"<line x1='{sg*R}' y1='0' x2='{sg*(D-R)}' y2='0' stroke='{INK}' stroke-width='0.6'/>"
        s+=f"<line x1='0' y1='{sg*R}' x2='0' y2='{sg*(D-R)}' stroke='{INK}' stroke-width='0.6'/>"
    for k,(cx,cy) in POS.items():
        f=fill.get(k)
        fl=f"fill='{f}' fill-opacity='0.25'" if f else "fill='none'"
        s+=f"<circle cx='{cx}' cy='{cy}' r='{R}' {fl} stroke='{INK}' stroke-width='0.6'/>"
        v=vals.get(k)
        if v is None: s+=f"<text x='{cx}' y='{cy+1.8}' fill='{DIM}' font-size='5' text-anchor='middle' font-style='italic'>{k}</text>"
        else: s+=f"<text x='{cx}' y='{cy+2.1}' fill='{GOLD}' font-size='6' text-anchor='middle' font-weight='700'>{v}</text>"
    st=" style='max-width:300px'" if big else " style='max-width:220px'"
    return f"<svg viewBox='-29 -29 58 58' role='img' aria-label='Крестик из пяти кружков'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# таблица произведений двух разных цифр: строка — меньшая цифра, столбец — большая
REP={6:GOLD,8:GREEN,12:BLUE,18:VIOLET,24:RED}
from collections import Counter
cnt=Counter(i*j for i in range(1,10) for j in range(i+1,10))
assert sorted(p for p,n in cnt.items() if n>1)==sorted(REP) and all(cnt[p]==2 for p in REP)
def table():
    W=10; s=''
    for j in range(2,10):
        s+=f"<text x='{(j-2)*W+W/2}' y='-2.5' fill='{DIM}' font-size='4' text-anchor='middle'>{j}</text>"
    for i in range(1,9):
        y=(i-1)*W
        s+=f"<text x='-3.5' y='{y+W/2+1.4}' fill='{DIM}' font-size='4' text-anchor='middle'>{i}</text>"
        for j in range(i+1,10):
            x=(j-2)*W; p=i*j; c=REP.get(p)
            if c: s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{c}' fill-opacity='0.3'/>"
            s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.4'/>"
            col=c if c else DIM
            fw=" font-weight='700'" if c else ''
            s+=f"<text x='{x+W/2}' y='{y+W/2+1.6}' fill='{col if c else LAB}' font-size='4.2' text-anchor='middle'{fw}>{p}</text>"
    s+=f"<text x='-3.5' y='-2.5' fill='{DIM}' font-size='3.4' text-anchor='middle'>·</text>"
    return f"<svg viewBox='-8 -7 89 88' role='img' aria-label='Произведения двух разных цифр' style='max-width:420px'>{s}</svg>"

V={}
V['Способ — размещение пяти из цифр 1–9']=fig(cross(big=True),'l, r — концы горизонтальной линии, t, b — концы вертикальной, x — центр.')
V['Выпишем произведения всех пар разных цифр']=fig(table(),'Строка — меньшая цифра пары, столбец — большая; одинаковые произведения одного цвета.')
V['В l встаёт любая из четырёх цифр 1, 2, 3, 6']=fig(cross({'l':1,'r':6,'t':2,'b':3},{'l':GOLD,'r':GOLD,'t':GREEN,'b':GREEN,'x':DIM}),'Одно из заполнений мира N(6); в x — любая из 4, 5, 7, 8, 9.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
