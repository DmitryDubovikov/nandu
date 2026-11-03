import json, sys
GOLD,GREEN,BLUE='#f0a83c','#5fd38d','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
SUB='₁₂₃₄'
def board(cells, big=False):
    # cells: 4 элемента по клеткам c₁ c₂ / c₃ c₄; None — пустая клетка с именем cᵢ,
    # 'g' — любая из 2, 4, 8, 9 (зелёная), 'b' — 3 или 6 (синяя), 'last' — клетка, которая выправляет двойки (золотая)
    s=''
    for i,v in enumerate(cells):
        x=(i%2)*W; y=(i//2)*W
        if v=='g': s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        if v=='b': s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{BLUE}' fill-opacity='0.25'/>"
        s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v is None:
            s+=f"<text x='{x+W/2}' y='{y+W/2+1.6}' fill='{DIM}' font-size='4.4' text-anchor='middle' font-style='italic'>c{SUB[i]}</text>"
        else:
            s+=f"<text x='{x+1.2}' y='{y+3.6}' fill='{DIM}' font-size='2.6' font-style='italic'>c{SUB[i]}</text>"
            if v=='g': s+=f"<text x='{x+W/2}' y='{y+W/2+2.4}' fill='{LAB}' font-size='3.2' text-anchor='middle'>2 4 8 9</text>"
            if v=='b': s+=f"<text x='{x+W/2}' y='{y+W/2+2.4}' fill='{LAB}' font-size='3.6' text-anchor='middle'>3 6</text>"
            if v=='last':
                s+=f"<rect x='{x+0.8}' y='{y+0.8}' width='{W-1.6}' height='{W-1.6}' fill='none' stroke='{GOLD}' stroke-width='0.9'/>"
                s+=f"<text x='{x+W/2}' y='{y+W/2+2.6}' fill='{GOLD}' font-size='6' text-anchor='middle' font-weight='700'>?</text>"
    st=" style='max-width:220px'" if big else " style='max-width:150px'"
    return f"<svg viewBox='-1 -1 30 30' role='img' aria-label='Доска 2×2'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    return fig(f"<div class='fgrid'>{c}</div>",cap)
N=None
V={}
V['Способ — запись в клетки c₁, c₂, c₃, c₄']=fig(board([N]*4,True),'cᵢ — цифра в i-й клетке.')
V['1. N(нет 3 и 6).']=fig(board(['g','g','g','last']),'Зелёные клетки — любая из 2, 4, 8, 9; в золотой — одна из двух пар: 4, 9 или 2, 8.')
# шесть мест для двух клеток с 3 или 6; из двух других клеток последняя по номеру — золотая
pl=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
cells=[]
for p in pl:
    rest=[i for i in range(4) if i not in p]
    b=['b' if i in p else ('last' if i==rest[1] else 'g') for i in range(4)]
    cells.append((board(b),'{c'+SUB[p[0]]+', c'+SUB[p[1]]+'}'))
V['Места для двух клеток с 3 или 6']=grid(cells,'Синие клетки — 3 или 6, зелёная — любая из 2, 4, 8, 9, в золотой — две цифры, с которыми множителей 2 на доске чётное число.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
