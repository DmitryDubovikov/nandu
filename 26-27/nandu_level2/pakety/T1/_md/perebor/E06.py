# цены в центах (целые), чтобы не терять дроби; c,b - машинка, мяч (целые доллары и, отдельно, любые центы)
def run(name, nd, nb, step):
    sols=[]
    for c in range(step,30001,step):
        for b in range(step,30001,step):
            sat = 4*c*100 - nd*c*40 + 6*b*100   # в сотых цента
            sun = 4*c*100 + 6*b*100 - nb*b*50
            if sat==23200*100//100*100 and False: pass
            if sat==232*10000 and sun==230*10000:
                sols.append((c,b))
    print(name, sols, "без скидок:", sorted({4*c+6*b for c,b in sols}))
# c,b в центах; сумма в центах*100 -> 232$ = 23200 центов*100
def run2(name, nd, nb, step, lim):
    sols=[]
    for c in range(step,lim,step):
        for b in range(step,lim,step):
            sat = (4*c*100 - nd*c*40 + 6*b*100)
            sun = (4*c*100 + 6*b*100 - nb*b*50)
            if sat==232*100*100 and sun==230*100*100: sols.append((c,b))
    print(name, "решения(цены в центах):", sols, "сумма без скидок (центы):", sorted({4*c+6*b for c,b in sols}))
for nm,nd,nb in [("одна вторая машинка, один второй мяч",1,1),("каждая вторая: 2 машинки, 3 мяча",2,3)]:
    run2(nm,nd,nb,1,6000)
