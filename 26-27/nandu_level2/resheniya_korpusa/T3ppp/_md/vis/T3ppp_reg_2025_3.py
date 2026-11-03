import json, sys
# Андреа — синяя, Бруно — золотая; зелёная заливка — свободный раунд
COL={'А':'#5ba8f5','Б':'#f0a83c'}
GREEN='#5fd38d'
INK,DIM,LAB='#cfdae6','#93a1b1','#e8eef6'
W=12; HW=30
def fig(inner,cap=''):
    c=f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"
def txt(x,y,s,col=LAB,size=5.2,w='700',anchor='middle'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='{anchor}' font-weight='{w}'>{s}</text>"
def table(rows, cut=None, winners=None):
    # rows: список (подпись, [15 значений]); cut — жирная черта после раунда cut
    s=''; y=0
    allrows=[('Раунд',[str(i) for i in range(1,16)],DIM)]
    if winners: allrows.append(('Победил',winners,None))
    allrows+= [(n,v,c) for n,v,c in rows]
    for name,vals,col in allrows:
        s+=f"<rect x='0' y='{y}' width='{HW}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        s+=txt(2,y+W/2+1.8,name,DIM if name in('Раунд','Победил') else LAB,4.6,'400','start')
        for i,v in enumerate(vals):
            x=HW+i*W
            s+=f"<rect x='{x}' y='{y}' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
            if v:
                c=col if col else COL[v]
                s+=txt(x+W/2,y+W/2+1.8,v,c,5.2 if name!='Раунд' else 4.4,'700' if name!='Раунд' else '400')
        y+=W
    if cut:
        x=HW+cut*W
        s+=f"<line x1='{x}' y1='-2' x2='{x}' y2='{y+2}' stroke='{GREEN}' stroke-width='1.2'/>"
    return s,y
V={}
e=['']*15
a=e[:]; a[6]='3'; b=e[:]; b[6]='4'
s,h=table([('Андреа',a,COL['А']),('Бруно',b,COL['Б'])])
V['Способ — выбор раундов']=fig(f"<svg viewBox='-1 -1 {HW+15*W+2} {h+2}' role='img' aria-label='Таблица очков' style='max-width:560px'>{s}</svg>")
win=list('БАБАББА')+list('ААБАААБА')
A=[];B=[];x=y=0
for w in win:
    if w=='А': x+=1
    else: y+=1
    A.append(str(x)); B.append(str(y))
s,h=table([('Андреа',A,COL['А']),('Бруно',B,COL['Б'])],cut=7,winners=win)
V['Значит: таблица задаётся тем']=fig(f"<svg viewBox='-1 -3 {HW+15*W+2} {h+6}' role='img' aria-label='Победители и таблица' style='max-width:560px'>{s}</svg>",'Один из списков победителей и его таблица')
def strip(vals,green,first):
    s=''
    for i,v in enumerate(vals):
        x=i*W
        s+=txt(x+W/2,-1.5,str(first+i),DIM,4,'400')
        if i+1 in green: s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='{GREEN}' fill-opacity='0.22'/>"
        s+=f"<rect x='{x}' y='0' width='{W}' height='{W}' fill='none' stroke='{INK}' stroke-width='0.5'/>"
        if v: s+=txt(x+W/2,W/2+1.8,v,COL[v])
    return f"<svg viewBox='-1 -7 {len(vals)*W+2} {W+8}' role='img' aria-label='Раунды' style='max-width:260px'>{s}</svg>"
V['C(8, 2) = 7 + 6']=fig(strip(['Б']+['']*7,range(2,9),8))
V['C(7, 3) = 15 + 10']=fig(strip(['А']+['']*6,range(2,8),1))
json.dump(V,open(sys.argv[1],'w'),ensure_ascii=False,indent=1)
print(len(V),'figures')
