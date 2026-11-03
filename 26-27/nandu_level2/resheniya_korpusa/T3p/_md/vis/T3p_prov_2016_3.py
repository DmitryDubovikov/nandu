import json, sys
GOLD,GREEN,BLUE,VIOLET='#f0a83c','#5fd38d','#5ba8f5','#b48cf0'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
SUB='₁₂₃₄₅₆₇₈₉'
TINT={'g':GREEN,'b':BLUE,'v':VIOLET}
def board(cells, big=False, cols=None):
    # cells: 9 элементов по клеткам c₁ c₂ c₃ / c₄ c₅ c₆ / c₇ c₈ c₉;
    # None — пустая клетка с именем cᵢ, число — стоит в клетке (золотое),
    # ('g'|'b'|'v', текст) — клетка цвета своей группы с запасом чисел; ('g'|'b'|'v', None) — только цвет и cᵢ
    s=''
    for i,v in enumerate(cells):
        x=(i%3)*W; y=(i//3)*W
        if isinstance(v,tuple):
            s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{TINT[v[0]]}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v is None or (isinstance(v,tuple) and v[1] is None):
            s+=f"<text x='{x+W/2}' y='{y+W/2+1.6}' fill='{DIM}' font-size='4.4' text-anchor='middle' font-style='italic'>c{SUB[i]}</text>"
        elif isinstance(v,tuple):
            s+=f"<text x='{x+1.2}' y='{y+3.6}' fill='{DIM}' font-size='2.6' font-style='italic'>c{SUB[i]}</text>"
            s+=f"<text x='{x+W/2}' y='{y+W/2+2.4}' fill='{LAB}' font-size='3.4' text-anchor='middle'>{v[1]}</text>"
        else:
            s+=f"<text x='{x+1.2}' y='{y+3.6}' fill='{DIM}' font-size='2.6' font-style='italic'>c{SUB[i]}</text>"
            s+=f"<text x='{x+W/2}' y='{y+W/2+2.4}' fill='{GOLD}' font-size='6' text-anchor='middle' font-weight='700'>{v}</text>"
    h=3*W
    if cols:
        for j,(t,c) in enumerate(cols):
            s+=f"<text x='{j*W+W/2}' y='{h+5}' fill='{c}' font-size='3.6' text-anchor='middle' font-style='italic'>S<tspan font-size='2.6' dy='0.9'>{t}</tspan></text>"
        h+=7
    st=" style='max-width:300px'" if big else " style='max-width:220px'"
    return f"<svg viewBox='-1 -1 44 {h+2}' role='img' aria-label='Доска 3×3'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
N=None
V={}
V['Способ — расстановка чисел 1–9 по клеткам']=fig(board([N]*9,True),'cᵢ — число в i-й клетке.')
col=[('g',None),('b',None),('v',None)]*3
V['S_{строк} = 100']=fig(board(col,False,[('сот',GREEN),('дес',BLUE),('ед',VIOLET)]),
    'Первый столбец — сотни, второй — десятки, третий — единицы.')
V['в столбце десятков оставшиеся 3, 4, 6']=fig(board([('g','7 8 9'),('b','3 4 6'),5,('g','7 8 9'),('b','3 4 6'),2,('g','7 8 9'),('b','3 4 6'),1]),
    'В столбце сотен 7, 8, 9, в столбце десятков 3, 4, 6, единицы на местах.')
V['В каждом мире в c₁ и c₄']=fig(board([('g','8 9'),('b','3 6'),5,('g','8 9'),('b','3 6'),2,7,4,1]),
    'Мир N(7, 4): в зелёных клетках 8 и 9, в синих 3 и 6.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
