import json, sys
# числа 1–9 в ряд; зелёная заливка — самые маленькие числа, которые можно взять после x₁
GREEN='#5fd38d'
BLUE='#5ba8f5'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=12
def cells(green=(), first=None, lab=None):
    s=''
    for i in range(9):
        v=i+1; x=i*W
        if v in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        col=BLUE if v==first else (LAB if v in green else DIM)
        s+=f"<text x='{x+W/2}' y='{W/2+1.8}' fill='{col}' font-size='5.2' text-anchor='middle' font-weight='700'>{v}</text>"
        if lab and v in lab:
            s+=f"<text x='{x+W/2}' y='{W+5.5}' fill='{BLUE if v==first else GREEN}' font-size='4.4' text-anchor='middle'>{lab[v]}</text>"
    return s
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
V={}
V['5 + 6 + 7 = 18']=fig(
    f"<svg viewBox='-1 -1 {9*W+2} {W+9}' role='img' aria-label='Числа от 1 до 9' style='max-width:320px'>"
    f"{cells(green=(5,6,7),first=5,lab={5:'x₁',6:'x₂',7:'x₃'})}</svg>",
    'x₁ = 5 и самые маленькие x₂, x₃ после него.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
