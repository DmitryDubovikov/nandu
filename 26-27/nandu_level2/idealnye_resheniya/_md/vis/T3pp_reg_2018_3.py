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
    c=''.join(f"<div class='cell'>{s}<p class='ccap'>{t}</p></div>" for s,t in cells)
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
V={}
V['остальные цифры a, b, c — любые, 0 тоже']=fig(strip(['1','a','b','c'],big=True),'Числа от 1000 до 1999.')
V['в блоке 7 стоит на одном из мест a, b, c']=grid([(strip(['1','7','b','c'],(3,4)),'a = 7'),(strip(['1','a','7','c'],(2,4)),'b = 7'),(strip(['1','a','b','7'],(2,3)),'c = 7')],
  'Зелёные — свободные цифры.')
V['Делимость суммы на 3 решают остатки слагаемых']=fig(ostatki(),'Цифры по остаткам при делении на 3.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
