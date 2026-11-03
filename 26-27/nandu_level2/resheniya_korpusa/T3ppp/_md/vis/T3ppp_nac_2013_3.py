import json, sys
# 7 — фиолетовая; 3 и 6 (цифра с множителем 3) — золотые; 2, 4, 8 — синие; зелёная заливка — свободное место
COL={'7':'#c58af9','3':'#f0a83c','6':'#f0a83c','2':'#5ba8f5','4':'#5ba8f5','8':'#5ba8f5'}
GREEN='#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=12
def cells(vals, green=()):
    s=''
    for i,v in enumerate(vals):
        x=i*W
        s+=f"<text x='{x+W/2}' y='-1.5' fill='{DIM}' font-size='4' text-anchor='middle'>{i+1}</text>"
        if i+1 in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v: s+=f"<text x='{x+W/2}' y='{W/2+1.8}' fill='{COL[v]}' font-size='5.2' text-anchor='middle' font-weight='700'>{v}</text>"
    return s
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def strip(vals,green):
    n=len(vals)
    return f"<svg viewBox='-1 -6 {n*W+2} {W+7}' role='img' aria-label='Места числа' style='max-width:{45*n}px'>{cells(vals,green)}</svg>"
V={}
V['N(мест для 6) = 3']=fig(strip(['7',None,None,None],(2,3,4)))
V['N(мест для 3) = 4']=fig(strip(['7',None,None,None,None],(2,3,4,5)))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
