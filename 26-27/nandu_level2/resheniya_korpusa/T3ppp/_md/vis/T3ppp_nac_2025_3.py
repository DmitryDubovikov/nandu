import json, sys
# цифры: 1 — синяя, 2 — золотая, 3 — красная, 4 — фиолетовая; зелёная заливка — свободное место
COL={'1':'#5ba8f5','2':'#f0a83c','3':'#ef6f6c','4':'#c58af9'}
GREEN='#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=12
N=7
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
    return f"<svg viewBox='-1 -1 {N*W+2} {W+2}' role='img' aria-label='Места числа' style='max-width:250px'>{cells(vals,0,0,green)}</svg>"
V['N(мест для 2) = 6']=fig(strip(['1',None,None,None,None,None,None],(2,3,4,5,6,7)))
V['N(мест для двух 2) = C(5, 2)']=fig(strip(['1','1',None,None,None,None,None],(3,4,5,6,7)))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
