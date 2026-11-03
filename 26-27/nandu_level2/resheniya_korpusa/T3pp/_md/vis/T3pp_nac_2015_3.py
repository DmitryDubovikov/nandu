import json, sys
GOLD,GREEN,RED='#f0a83c','#5fd38d','#f2686c'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
BLUE,VIO='#5ba8f5','#c58af9'
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

# набор цифр → возрастающее число: ряд 1…9, выбранные цифры подсвечены, справа число из них по порядку
def nabory(rows):
    W=9; s=''; y=0
    for chosen,num in rows:
        for d in range(1,10):
            x=(d-1)*W
            on = d in chosen
            if on: s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
            s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.4'/>"
            col = GOLD if on else DIM
            fw = " font-weight='700'" if on else ''
            s+=f"<text x='{x+W/2}' y='{y+W/2+1.8}' fill='{col}' font-size='5'{fw} text-anchor='middle'>{d}</text>"
        s+=f"<text x='{9*W+4}' y='{y+W/2+1.8}' fill='{LAB}' font-size='5'>→</text>"
        s+=f"<text x='{9*W+11}' y='{y+W/2+1.8}' fill='{GOLD}' font-size='5.4' font-weight='700'>{num}</text>"
        y+=W+4
    return f"<svg viewBox='-1 -1 {9*W+36} {y-2}' role='img' aria-label='Набор цифр и число' style='max-width:440px'>{s}</svg>"

# дерево-обзор: N → шесть операндов по числу цифр
def tree():
    def node(x,y,w,label,col=INK):
        return (f"<rect x='{x}' y='{y}' width='{w}' height='8' rx='2' fill='#121821' stroke='{col}' stroke-width='0.6'/>"
                f"<text x='{x+w/2}' y='{y+5.6}' fill='{LAB}' font-size='4.2' text-anchor='middle' font-weight='600'>{label}</text>")
    kids=['N(4 цифры, больше 2015) = 70','N(5 цифр) = 126','N(6 цифр) = 84','N(7 цифр) = 36','N(8 цифр) = 9','N(9 цифр) = 1']
    s=''
    ys=[2+i*10 for i in range(len(kids))]
    for y in ys: s+=f"<line x1='36' y1='31' x2='60' y2='{y+4}' stroke='{INK}' stroke-width='0.5'/>"
    s+=node(4,27,32,'N = 326')
    for y,l in zip(ys,kids): s+=node(60,y,72,l)
    return f"<svg viewBox='0 0 136 62' role='img' aria-label='Обзор решения' style='max-width:480px'>{s}</svg>"

V={}
V['цифры набора записываются в порядке возрастания только одним способом']=fig(nabory([({2,4,5,8},'2458'),({1,3,6,7},'1367')]),'Набор цифр и возрастающее число из них.')
V['N = 70 + 126 + 84 + 36 + 9 + 1 = 326']=fig(tree(),'Обзор решения.')
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
