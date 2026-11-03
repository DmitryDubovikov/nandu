import json, sys
GOLD,BLUE,GREEN='#f0a83c','#5ba8f5','#5fd38d'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
def txt(x,y,s,col=LAB,size=3.6,w='600'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def htxt(x,y,s,col,size=3.4,w='700'):   # подпись поверх кирпичиков: тёмная обводка, чтобы сетка не резала буквы
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}' stroke='#121821' stroke-width='1.3' paint-order='stroke'>{s}</text>"
def svg(inner,label,vb,mw=None):
    st=f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}'{st}>{inner}</svg>"
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def sub(word):   # S с индексом-словом внутри SVG
    return f"S<tspan baseline-shift='sub' font-size='2.6'>{word}</tspan>"

# две полосы в кирпичиках по 2 % сбережений: сверху сбережения (подарок 10 + остаток 40),
# снизу деньги теперь (остаток 40 + бабушка 8 + мама 5) = 53 кирпичика = 106 %
X0,BW,H=4,1.85,10
def row(y,zones,splits=()):
    s=''; a=0
    for name,k,col in zones:
        for i in range(a,a+k):
            s+=f"<rect x='{X0+i*BW}' y='{y}' width='{BW}' height='{H}' fill='{col}' fill-opacity='0.28' stroke='{INK}' stroke-width='0.2'/>"
        s+=f"<rect x='{X0+a*BW}' y='{y}' width='{k*BW}' height='{H}' fill='none' stroke='{col}' stroke-width='0.9'/>"
        a+=k
    for q,col in splits:   # границы равных частей внутри части: пятые доли остатка, половины подарка
        s+=f"<line x1='{X0+q*BW}' y1='{y}' x2='{X0+q*BW}' y2='{y+H}' stroke='{col}' stroke-width='0.8'/>"
    return s
def brace(a,k,y,up,label,col,size=3.4):
    x1,x2=X0+a*BW+0.5,X0+(a+k)*BW-0.5
    if up:
        d=f'M{x1} {y+1.8}V{y}H{x2}V{y+1.8}'; ty=y-1.4
    else:
        d=f'M{x1} {y-1.8}V{y}H{x2}V{y-1.8}'; ty=y+4.2
    return f"<path d='{d}' fill='none' stroke='{col}' stroke-width='0.8'/>"+txt((x1+x2)/2,ty,label,col,size)

def bars():
    s=''
    # сбережения
    s+=row(9,[('подарок',10,GOLD),('остаток',40,BLUE)],[(5,GOLD)])
    s+=brace(0,10,6.5,True,'подарок 20 %',GOLD,3.1)+brace(10,40,6.5,True,'остаток 80 %',BLUE)
    s+=htxt(X0+30*BW,15.2,'сбережения',INK,3.4)
    # теперь
    y2=31
    s+=row(y2,[('остаток',40,BLUE),('бабушка',8,GREEN),('мама',5,GOLD)],[(8,BLUE),(16,BLUE),(24,BLUE),(32,BLUE)])
    s+=txt(X0+20*BW,y2-2,'остаток 80 %',BLUE,3.2)
    s+=txt(X0+44*BW,y2-6.2,'бабушка',GREEN,3.0)+txt(X0+44*BW,y2-2,'16 %',GREEN,3.0)
    s+=txt(X0+50.5*BW,y2-6.2,'мама',GOLD,3.0)+txt(X0+50.5*BW,y2-2,'10 %',GOLD,3.0)
    s+=brace(0,53,y2+H+2.5,False,'теперь 106 % = $2067',GOLD,3.6)
    return svg(s,'Сбережения и деньги теперь','0 0 108 52',540)

# схема-план: от 2067 к спрошенным; стрелка — данное из условия; step подсвечивает текущий раздел
NODES={'2067':(2,8,16,10),'С':(50,8,42,10),'П':(106,8,34,10)}
NAME={'2067':'$2067','С':'б) '+sub('сбережений'),'П':'а) '+sub('подарка')}
ARROWS={1:[('M18 13H49','20 %, 20 %, 1/2',(33.5,10.6))],
        2:[('M92 13H105','20 %',(98.5,10.6))]}
TARGET={1:'С',2:'П'}
def scheme(step=None):
    s=f"<defs><marker id='ahp{step}' viewBox='0 0 6 6' refX='5' refY='3' markerWidth='4' markerHeight='4' orient='auto'><path d='M0 0L6 3L0 6z' fill='context-stroke'/></marker></defs>"
    done={'2067'}|{TARGET[k] for k in TARGET if step and k<step}
    for k,arr in ARROWS.items():
        cur = step==k
        col = GOLD if cur else (INK if (step is None or k<step) else DIM)
        w = 1.0 if cur else 0.6
        for d,lab,pos in arr:
            s+=f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{w}' marker-end='url(#ahp{step})'/>"
            if lab: s+=txt(pos[0],pos[1],lab,col,3.1)
    for n,(x,y,w,h) in NODES.items():
        cur = step and TARGET[step]==n
        col = GOLD if (cur or n=='2067') else (INK if (step is None or n in done) else DIM)
        s+=f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='2' fill='{GOLD if cur else '#121821'}' fill-opacity='{0.22 if cur else 1}' stroke='{col}' stroke-width='{1.0 if cur else 0.6}'/>"
        s+=txt(x+w/2,y+h/2+1.3,NAME[n],col,3.4)
    return svg(s,'Схема решения','0 0 142 22')

V={}
V['выразим $2067 долей сбережений']=fig(scheme(),'План: каждая стрелка — данное из условия.')
V['1. б) Найдём S_{сбережений}']=fig(scheme(1))
V['вместе 106 % сбережений']=fig(bars(),'Кирпичик — 2 % сбережений. Деньги бабушки — одна пятая остатка, деньги мамы — половина подарка.')
V['2. а) Найдём S_{подарка}']=fig(scheme(2))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
