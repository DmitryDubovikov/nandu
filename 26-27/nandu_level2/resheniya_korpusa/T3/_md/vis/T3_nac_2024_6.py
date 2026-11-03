import json, sys
GOLD,GREEN,BLUE='#f0a83c','#5fd38d','#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
H=17.32  # высота треугольника со стороной 20
def nums(pts, vals, col=LAB, k=0.52, size=4.6):
    cx=sum(p[0] for p in pts)/3; cy=sum(p[1] for p in pts)/3
    s=''
    for (x,y),v in zip(pts,vals):
        if v is None: continue
        c = col[v] if isinstance(col,dict) else col
        tx=x+k*(cx-x); ty=y+k*(cy-y)+size*0.36
        s+=f"<text x='{tx:.2f}' y='{ty:.2f}' fill='{c}' font-size='{size}' text-anchor='middle' font-weight='700'>{v}</text>"
    return s
def poly(pts, fill='none', op=0):
    p=' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)
    f=f" fill='{fill}' fill-opacity='{op}'" if fill!='none' else " fill='none'"
    return f"<polygon points='{p}'{f} stroke='{INK}' stroke-width='0.6' stroke-linejoin='round'/>"
UP=[(0,H),(10,0),(20,H)]            # левый нижний, верхний, правый нижний
DN=[(0,H),(20,H),(10,2*H)]          # левый, правый, нижний
def tile(l,t,r,cap='',mw=110,fill=None):
    s=poly(UP,fill or 'none',0.2 if fill else 0)+nums(UP,[l,t,r])
    lab=f"<text x='-11' y='{H}' fill='{DIM}' font-size='5'>{cap}</text>" if cap else ''
    x0=-12 if cap else -1
    return f"<svg viewBox='{x0} -1 {22-x0} {H+2}' role='img' aria-label='Фишка' style='max-width:{mw}px'>{lab}{s}</svg>"
def rhomb(top=None, bot=None, mw=90, mark=False, ftop=None, fbot=None):
    # top: (лев, верх, прав) верхнего треугольника; bot: (лев, прав, низ) нижнего
    s=poly(UP,ftop or 'none',0.18 if ftop else 0)+poly(DN,fbot or 'none',0.18 if fbot else 0)
    if mark: s+=f"<line x1='0' y1='{H}' x2='20' y2='{H}' stroke='{GOLD}' stroke-width='1.4'/>"
    if top: s+=nums(UP,list(top))
    if bot: s+=nums(DN,list(bot))
    return f"<svg viewBox='-1 -1 22 {2*H+2}' role='img' aria-label='Доска' style='max-width:{mw}px'>{s}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def grid(cells,cap=''):
    c=''.join(f"<div class='cell'>{s}"+(f"<p class='ccap'>{t}</p>" if t else '')+"</div>" for s,t in cells)
    return fig(f"<div class='fgrid'>{c}</div>",cap)
V={}
# рисунок условия: фишки как в PDF (числа по углам: левый нижний, верхний, правый нижний)
V['Фишку пишем числами']=grid([
    (tile(1,3,2,'(a)'),''),(tile(1,2,3,'(b)'),''),(tile(3,2,1,'(c)'),''),
    (rhomb(mw=70),''),(rhomb((1,1,2),(1,2,3),mw=70),'')],
    'Фишки (a), (b), (c) и доска; справа — доска, покрытая двумя фишками.')
V['третье число поворотом ставится']=grid([
    (tile(1,2,1,mw=80),''),(tile(1,1,2,mw=80),''),(tile(2,1,1,mw=80),'')],
    'Три положения фишки (1, 1, 2).')
V['наименьшее число ставится в верхний угол']=grid([
    (tile(3,1,2,mw=80),'(1, 2, 3)'),(tile(2,1,3,mw=80),'(1, 3, 2)')],
    'Набор 1, 2, 3: два порядка по кругу.')
V['в левом и правом углу доски']=fig(rhomb(('?','?','?'),(None,None,'?'),mw=110,mark=True),
    'Общая сторона и четыре угла доски.')
V['Например, сверху (1, 2, 1)']=fig(rhomb((1,2,1),(1,1,2),mw=100,ftop=GREEN,fbot=GREEN),
    'Сверху и снизу (1, 1, 2).')
V['сверху фишка (a)']=fig(rhomb((1,3,2),(1,2,3),mw=100,ftop=BLUE,fbot=GOLD),
    'Сверху (1, 3, 2), снизу (1, 2, 3).')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
