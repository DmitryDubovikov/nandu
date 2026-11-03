import json, sys
GOLD,RED,BLUE='#f0a83c','#f2686c','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
PAINT={'1':RED,'3':RED,'5':BLUE,'7':BLUE,'9':BLUE}
CW,GAP=4.2,2.6   # ширина цифры, промежуток между числами

def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

def row(nums, y, hl=None, col=None, fade=()):
    # nums: числа подряд; hl=(i, j) — номера цифр строки (с 0), которые обводятся полоской цвета col
    s=''; x=0; k=0; pos=[]
    for n_i,n in enumerate(nums):
        for d in n:
            c=PAINT.get(d,DIM)
            op = 0.45 if (hl and not (hl[0] <= k <= hl[1])) else 1
            s+=f"<text x='{x+CW/2}' y='{y+5}' fill='{c}' fill-opacity='{op}' font-size='5' text-anchor='middle' font-weight='700'>{d}</text>"
            pos.append(x); x+=CW; k+=1
        x+=GAP
    if hl:
        i,j=hl
        x1=pos[i]-0.6; x2=pos[j]+CW+0.6
        s=f"<rect x='{x1}' y='{y-0.4}' width='{x2-x1}' height='7.4' rx='1.6' fill='{col}' fill-opacity='0.16' stroke='{col}' stroke-width='0.5'/>"+s
        s+=f"<text x='{x+1}' y='{y+5}' fill='{col}' font-size='3.8' font-weight='600'>{j-i+1} цифр</text>"
    return s, x

# начало строки
def nachalo():
    nums=[str(n) for n in range(1,40,2)]
    s,w=row(nums,0)
    return f"<svg viewBox='-1 -1 {w+2} 8' role='img' aria-label='Начало строки' style='max-width:640px'>{s}</svg>"

# схема кусков: …9 | x1 | x3 | x5 | x7 | x9 | (x + 1)1
def shema():
    BW,DW,G=13,6,2.4
    items=[(None,'9'),('x','1'),('x','3'),('x','5'),('x','7'),('x','9'),('x + 1','1')]
    s=''; x=0; edges=[]
    for pre,last in items:
        x0=x
        if pre:
            s+=f"<rect x='{x}' y='12' width='{BW}' height='8' rx='1' fill='none' stroke='{INK}' stroke-width='0.4'/>"
            s+=f"<text x='{x+BW/2}' y='17.6' fill='{DIM}' font-size='4' text-anchor='middle' font-style='italic'>{pre}</text>"
            x+=BW
        c=PAINT[last]
        s+=f"<rect x='{x}' y='12' width='{DW}' height='8' rx='1' fill='{c}' fill-opacity='0.2' stroke='{c}' stroke-width='0.5'/>"
        s+=f"<text x='{x+DW/2}' y='17.8' fill='{c}' font-size='4.6' text-anchor='middle' font-weight='700'>{last}</text>"
        x+=DW
        edges.append((x0,x)); x+=G
    # красный кусок «x1 x3 x»: от x1 до x перед 5
    rx1=edges[1][0]; rx2=edges[3][0]+BW
    s+=f"<path d='M{rx1} 22 v3 H{rx2} v-3' fill='none' stroke='{RED}' stroke-width='0.7'/>"
    s+=f"<text x='{(rx1+rx2)/2}' y='30' fill='{RED}' font-size='3.8' text-anchor='middle' font-weight='600'>кусок «x1 x3 x»</text>"
    # синий кусок «x5 x7 x9 (x + 1)»
    bx1=edges[3][0]; bx2=edges[6][0]+BW
    s+=f"<path d='M{bx1} 10 v-3 H{bx2} v3' fill='none' stroke='{BLUE}' stroke-width='0.7'/>"
    s+=f"<text x='{(bx1+bx2)/2}' y='4.6' fill='{BLUE}' font-size='3.8' text-anchor='middle' font-weight='600'>кусок «x5 x7 x9 (x + 1)»</text>"
    return f"<svg viewBox='-1 0 {x+1} 32' role='img' aria-label='Куски строки' style='max-width:620px'>{s}</svg>"

def polosy(rows, col, cap):
    s=''; W=0
    for r,(nums,hl) in enumerate(rows):
        t,w=row(nums,r*10,hl,col,fade=(0,len(nums)-1))
        s+=t; W=max(W,w)
    return fig(f"<svg viewBox='-1 -1 {W+22} {len(rows)*10}' role='img' aria-label='Полоски' style='max-width:420px'>{s}</svg>",cap)

V={}
V['Выпишем начало строки и посмотрим, что повторяется']=fig(nachalo(),'Начало строки Франа.')
V['или в одном x между последними 1 и 3']=fig(shema(),'Числа с одним x и куски между последними цифрами другого цвета.')
red=[]
for x in ('111','113','131','133'):
    prev=str(int(x)*10-1)
    red.append(([prev,x+'1',x+'3',x+'5'],(4,14)))
V['x из цифр 1 и 3: 111, 113, 131, 133']=polosy(red,RED,'Все красные полоски из 11 цифр.')
blue=[]
for x in ('55','57','75','77','95','97'):
    nxt=str(int(x)+1)+'1'
    blue.append(([x+'3',x+'5',x+'7',x+'9',nxt],(3,12)))
V['x = 55, 57, 75, 77, 95, 97']=polosy(blue,BLUE,'Все синие полоски из 10 цифр.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
