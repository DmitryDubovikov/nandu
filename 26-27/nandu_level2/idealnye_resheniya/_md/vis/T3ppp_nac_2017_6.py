import json, sys
# цифры: 4 — синяя, 5 — золотая, 6 — фиолетовая; зелёная заливка — свободное место
COL={'4':'#5ba8f5','5':'#f0a83c','6':'#c58af9'}
GREEN='#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=12
def cells(vals, x0=0, y0=0, green=()):
    s=''
    for i,v in enumerate(vals):
        x=x0+i*W
        if i+1 in green: s+=f"<rect x='{x}' y='{y0}' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='{y0}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v: s+=f"<text x='{x+W/2}' y='{y0+W/2+1.8}' fill='{COL[v]}' font-size='5.2' text-anchor='middle' font-weight='700'>{v}</text>"
    return s
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
V={}
def strip(vals,green):
    return f"<svg viewBox='-1 -1 {6*W+2} {W+2}' role='img' aria-label='Места числа' style='max-width:220px'>{cells(vals,0,0,green)}</svg>"
V['N(мест для двух 6) = C(4, 2)']=fig(strip(['4','4',None,None,None,None],(3,4,5,6)))
V['N(мест для 6) = 5']=fig(strip(['4',None,None,None,None,None],(2,3,4,5,6)))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
