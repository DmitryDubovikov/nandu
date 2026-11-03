import json, sys
# все $26 = 40 цен сообщения; звонок — синий блок из 4, интернет — золотой из 2, сообщение — фиолетовая клетка
COL={'зв':'#5ba8f5','инт':'#f0a83c','смс':'#c58af9'}
INK,DIM='#cfdae6','#93a1b1'
W=12
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def strip(blocks):
    s='';x=0
    for kind,n in blocks:
        s+=f"<rect x='{x}' y='0' width='{n*W}' height='{W}' fill='{COL[kind]}' fill-opacity='0.30'/>"
        for i in range(n):
            s+=f"<rect x='{x+i*W}' y='0' width='{W}' height='{W}' fill='none' stroke='{DIM}' stroke-width='0.3'/>"
        s+=f"<rect x='{x}' y='0' width='{n*W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.9'/>"
        x+=n*W
    return s,x
blocks=[('зв',4)]*2+[('инт',2)]*4+[('смс',1)]*24
body,wid=strip(blocks)
lab=(f"<text x='{4*W}' y='{W+7}' fill='{COL['зв']}' font-size='5' text-anchor='middle'>2 мин звонков</text>"
     f"<text x='{8*W+4*W}' y='{W+7}' fill='{COL['инт']}' font-size='5' text-anchor='middle'>4 мин интернета</text>"
     f"<text x='{16*W+12*W}' y='{W+7}' fill='{COL['смс']}' font-size='5' text-anchor='middle'>24 сообщения</text>")
svg=f"<svg viewBox='-1 -1 {wid+2} {W+11}' role='img' aria-label='Все 26 долларов в ценах сообщения' style='max-width:560px'>{body}{lab}</svg>"
V={'каждая цена — целое число цен сообщения':fig(svg,'$26 = 40 цен сообщения; один из способов')}
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
