import json, sys
GOLD,GREEN='#f0a83c','#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
RED='#ff7a7a'
BOLD=" font-weight='700'"
W=10            # клетка
NC,NR=7,6       # столбцов, строк
X0,Y0=8,4       # левый верхний угол сетки
def gx(v): return X0+v*W
def gy(h): return Y0+(NR-h)*W
def grid(rect=None, line=False):
    # rect = (v1, v2, h1, h2) — пример прямоугольника; line — числовая прямая с двумя промежутками под сеткой
    s=''
    if rect:
        v1,v2,h1,h2=rect
        s+=f"<rect x='{gx(v1)}' y='{gy(h2)}' width='{(v2-v1)*W}' height='{(h2-h1)*W}' fill='{GREEN}' fill-opacity='0.18'/>"
    for v in range(NC+1):
        hl = rect and v in rect[:2]
        s+=f"<line x1='{gx(v)}' y1='{gy(0)}' x2='{gx(v)}' y2='{gy(NR)}' stroke='{GREEN if hl else INK}' stroke-width='{1.1 if hl else 0.4}'/>"
        s+=f"<text x='{gx(v)}' y='{gy(0)+5.2}' fill='{GREEN if hl else DIM}' font-size='4' text-anchor='middle'{BOLD if hl else ''}>{v}</text>"
    for h in range(NR+1):
        hl = rect and h in rect[2:]
        s+=f"<line x1='{gx(0)}' y1='{gy(h)}' x2='{gx(NC)}' y2='{gy(h)}' stroke='{GOLD if hl else INK}' stroke-width='{1.1 if hl else 0.4}'/>"
        s+=f"<text x='{gx(0)-2.5}' y='{gy(h)+1.4}' fill='{GOLD if hl else DIM}' font-size='4' text-anchor='end'{BOLD if hl else ''}>{h}</text>"
    s+=f"<line x1='{gx(0)}' y1='{gy(0)}' x2='{gx(6)}' y2='{gy(6)}' stroke='{RED}' stroke-width='1.3' stroke-linecap='round'/>"
    hgt=gy(0)+8
    if rect and line:
        v1,v2,h1,h2=rect
        ly=gy(0)+14
        s+=f"<line x1='{gx(0)}' y1='{ly}' x2='{gx(NC)}' y2='{ly}' stroke='{DIM}' stroke-width='0.5'/>"
        for t in range(NC+1):
            s+=f"<line x1='{gx(t)}' y1='{ly-1.2}' x2='{gx(t)}' y2='{ly+1.2}' stroke='{DIM}' stroke-width='0.5'/>"
            s+=f"<text x='{gx(t)}' y='{ly+5.6}' fill='{DIM}' font-size='3.6' text-anchor='middle'>{t}</text>"
        s+=f"<line x1='{gx(v1)}' y1='{ly}' x2='{gx(v2)}' y2='{ly}' stroke='{GREEN}' stroke-width='1.6' stroke-linecap='round'/>"
        s+=f"<line x1='{gx(h1)}' y1='{ly}' x2='{gx(h2)}' y2='{ly}' stroke='{GOLD}' stroke-width='1.6' stroke-linecap='round'/>"
        s+=f"<text x='{(gx(v1)+gx(v2))/2}' y='{ly-3.6}' fill='{GREEN}' font-size='3.4' text-anchor='middle'>от v₁ до v₂</text>"
        s+=f"<text x='{(gx(h1)+gx(h2))/2}' y='{ly-3.6}' fill='{GOLD}' font-size='3.4' text-anchor='middle'>от h₁ до h₂</text>"
        hgt=ly+8
    vb=f"0 0 {gx(NC)+4} {hgt}"
    return f"<svg viewBox='{vb}' role='img' aria-label='Сетка 6×7 с отрезком' style='max-width:{560 if not rect else 300}px'>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
V={}
V['номер — сколько клеток от линии']=fig(grid(),'Сетка 6×7 и наклонный отрезок.')
V['N(v₂ < h₁): прямоугольник выше отрезка']=fig(grid((0,2,3,5),True),'Вертикали 0 и 2, горизонтали 3 и 5.')
V['N(h₂ < v₁): прямоугольник ниже отрезка']=fig(grid((4,7,1,3),True),'Горизонтали 1 и 3, вертикали 4 и 7.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
