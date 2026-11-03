import json, sys
# последняя цифра — фиолетовая, цифры набора — синие; зелёная заливка — места 1, 2, 3, куда идёт набор
END='#c58af9'; SETC='#5ba8f5'
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
        if v:
            col=END if i==len(vals)-1 else SETC
            fs='5.2' if len(v)==1 else '3.6'
            s+=f"<text x='{x+W/2}' y='{W/2+1.6}' fill='{col}' font-size='{fs}' text-anchor='middle' font-weight='700'>{v}</text>"
    return s
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def strip(vals,green):
    return f"<svg viewBox='-1 -6 {4*W+2} {W+7}' role='img' aria-label='Места числа' style='max-width:180px'>{cells(vals,green)}</svg>"
V={}
V['На конце 0 ⇒ на местах 1, 2, 3']=fig(strip([None,None,None,'0'],(1,2,3)))
V['N(с цифрой 0) = 2 · 2 · 1 = 4']=fig(strip(['7, 9',None,None,'8'],(2,3)))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
