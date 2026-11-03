import json, sys
GOLD,GREEN='#f0a83c','#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=14
HOLE={(c,r) for c in (3,4,5) for r in (3,4)}
def X(c): return (c-1)*W
def Y(r): return (7-r)*W
def board(green=(), gates=(), path=False, big=False):
    # клетка (столбец, строка): строки снизу, столбцы слева;
    # green — прямоугольники (c1, r1, c2, r2), подсвеченные зелёным; gates — подъёмы из (c, r) в (c, r + 1), золотые стрелки
    s=''
    for c1,r1,c2,r2 in green:
        s+=f"<rect x='{X(c1)}' y='{Y(r2)}' width='{(c2-c1+1)*W}' height='{(r2-r1+1)*W}' fill='{GREEN}' fill-opacity='0.22'/>"
    for r in range(1,8):
        for c in range(1,8):
            if (c,r) in HOLE: continue
            s+=f"<rect x='{X(c)}' y='{Y(r)}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
    # дыра: столбцы 3–5, строки 3–4 — не клетка
    s+=f"<rect x='{X(3)}' y='{Y(4)}' width='{3*W}' height='{2*W}' fill='{DIM}' fill-opacity='0.12' stroke='{INK}' stroke-width='0.5'/>"
    for (c,r),t in (((1,1),'S'),((7,7),'L')):
        s+=f"<text x='{X(c)+W/2}' y='{Y(r)+W/2+2.2}' fill='{LAB}' font-size='6' text-anchor='middle' font-weight='700'>{t}</text>"
    for i in range(1,8):
        s+=f"<text x='-3' y='{Y(i)+W/2+1.4}' fill='{DIM}' font-size='3.6' text-anchor='middle'>{i}</text>"
        s+=f"<text x='{X(i)+W/2}' y='{7*W+5}' fill='{DIM}' font-size='3.6' text-anchor='middle'>{i}</text>"
    for c,r in gates:
        x=X(c)+W/2; y1=Y(r)+W*0.72; y2=Y(r+1)+W*0.28
        s+=(f"<line x1='{x}' y1='{y1}' x2='{x}' y2='{y2+1.6}' stroke='{GOLD}' stroke-width='1.4'/>"
            f"<path d='M{x-2},{y2+2.4} L{x},{y2} L{x+2},{y2+2.4}' fill='none' stroke='{GOLD}' stroke-width='1.2'/>")
    if path:
        pts=[(X(c)+W/2, Y(1)+W/2) for c in range(1,8)]+[(X(7)+W/2, Y(r)+W/2) for r in range(2,8)]
        p=' '.join(f'{x},{y}' for x,y in pts)
        s+=f"<polyline points='{p}' fill='none' stroke='{GREEN}' stroke-width='1.2' stroke-linejoin='round'/>"
        for x,y in pts[1:]: s+=f"<circle cx='{x}' cy='{y}' r='0.9' fill='{GREEN}'/>"
    st=" style='max-width:560px'" if big else " style='max-width:420px'"
    return f"<svg viewBox='-7 -2 108 108' role='img' aria-label='Доска'{st}>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

V={}
V['Способ — путь из ходов вправо и вверх']=fig(board(big=True),'Слева — номера строк, снизу — номера столбцов; прямоугольник посередине — не клетка.')
V['путь по строке 1 до столбца 7']=fig(board(path=True),'Путь из 12 ходов.')
V['N = N(вверх из (1, 4)) + N(вверх из (2, 4))']=fig(board(gates=((1,4),(2,4),(6,2),(7,2))),'Четыре подъёма у краёв дыры.')
V['N(вверх из (1, 4)): подъём в столбце 1']=fig(board(((1,1,1,4),(1,5,7,7)),((1,4),)))
V['N(вверх из (2, 4)): подъём в столбце 2']=fig(board(((1,1,2,4),(2,5,7,7)),((2,4),)))
V['N(вверх из (6, 2)): подъём в столбце 6']=fig(board(((1,1,6,2),(6,3,7,7)),((6,2),)))
V['N(вверх из (7, 2)): подъём в столбце 7']=fig(board(((1,1,7,2),(7,3,7,7)),((7,2),)))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
