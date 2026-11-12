"""Проверка чисел пары 1 «Геометрия» (учебник + решебник) и предложенных замен."""
from fractions import Fraction as F
from decimal import Decimal as D
from itertools import combinations
import math

ok = 0
def chk(name, cond):
    global ok
    assert cond, name
    ok += 1

# ---- гл. 1 / блок 1
chk("u1", 2*(24+15) == 78 and 78 < 80 and 80-78 == 2 and 24*15 == 360)
chk("1.3", 2*(60+40) == 200 and 60*40 == 2400)
# ---- гл. 2 / блок 2: примеры углов в сумме 180; 2.3 — углы треугольника 5,5,6
for a in [(50,60,70),(30,60,90),(20,40,120),(53,53,74)]:
    chk("sum180", sum(a) == 180)
apex = math.degrees(math.acos((25+25-36)/50)); base = (180-apex)/2
chk("2.3", round(apex) == 74 and round(base) == 53)
chk("ромб 70/110", 70+110 == 180)
# ---- гл. 3 / блок 3
chk("u3", D("1.25")/2 == D("0.625") and D("0.625")*100 == D("62.5") and D("0.625")*1000 == 625)
chk("u3 площадь", 100*100 == 10_000 and 100**3 == 1_000_000 and D("0.4")*100 == 40 and D("1.25")*100 == 125)
chk("3.1", D("2.4")*100 == 240 and D(35)/10 == D("3.5") and D("0.7")*10 == 7)
chk("3.2", D("1.2")*100 == 120 and 120 > 95)
chk("3.3", 28*15 == 420 and D(420)/10 == 42 and D(42)/100 == D("0.42"))
# ---- гл. 4 / блок 4
chk("u4", 54/2 == 27 and 180-68 == 112 and 68+112+68+112 == 360 and 70-25 == 45 and 180-40 == 140 and 50+130 == 180)
chk("4.1", [180-x for x in (15,90,143)] == [165,90,37])
chk("4.2", 31*2 == 62)
chk("4.3", 180//3 == 60 and 60*2 == 120 and 60+120 == 180)
# ---- гл. 5 / блок 5
chk("u5 зазор", 6-2-2 == 2 and 4 > 3)
# сбитый раствор: 4 см из A, 5 см из B, AB = 6: где прямая через точки пересечения режет AB
x = F(16-25+36, 12)   # x^2 - (6-x)^2 = 16 - 25
chk("u5 сбитый раствор", x == F(9,4) and x < 3)
chk("5.1", F(7,2)*2 == 7); chk("5.2", 8-3-3 == 2 and F(8,2) == 4)
# ---- гл. 6 / блок 6: куб по рисунку, развёртка
edges = [("A","B"),("B","C"),("C","D"),("D","A"),("E","F"),("F","G"),("G","H"),("H","E"),("A","E"),("B","F"),("C","G"),("D","H")]
hidden = [e for e in edges if "H" in e]
chk("u6", len(edges) == 12 and len(hidden) == 3 and 12-3 == 9 and 6*3*3 == 54)
chk("6.3", 2*(5*3+3*2+5*2) == 62)
# ---- гл. 7 / блок 7
prism = lambda n: (2*n, 3*n, n+2); pyr = lambda n: (n+1, 2*n, n+1)
for n in range(3, 30):
    for V,E,Fc in (prism(n), pyr(n)): chk("euler", V-E+Fc == 2)
chk("u7 список", [prism(n) for n in (3,4,5)] == [(6,9,5),(8,12,6),(10,15,7)] and [pyr(n) for n in (3,4,5)] == [(4,6,4),(5,8,5),(6,10,6)])
chk("u7 разбор", 21//3 == 7 and prism(7) == (14,21,9))
chk("7.1", prism(6) == (12,18,8))
sol = [("призма",n) for n in range(3,50) if prism(n)[0]==9 and prism(n)[2]==9] + [("пирамида",n) for n in range(3,50) if pyr(n)[0]==9 and pyr(n)[2]==9]
chk("7.2", sol == [("пирамида",8)] and pyr(8)[1] == 16 == 9+9-2)
chk("7.3", prism(9)[1] == 27 and 27*8 == 216 and prism(9)[2] == 11)
# ---- гл. 8 / блок 8
chk("u8", 2*3 == 6 and {(3,5),(5,3)} == {(3,5),(5,3)} and len({(3,5),(5,3)}) == 2)
chk("8.2", 3+2 == 5); chk("8.3", 8//2 == 4)
# ---- гл. 9 / блок 9: оси правильного n-угольника перебором отражений вершин
def axes_regular(n):
    pts = [(round(math.cos(2*math.pi*k/n),9), round(math.sin(2*math.pi*k/n),9)) for k in range(n)]
    S = set(pts); cnt = 0
    for k in range(2*n):                       # оси под углом pi*k/n
        t = math.pi*k/n
        if k >= n: break
        img = {(round(x*math.cos(2*t)+y*math.sin(2*t),9), round(x*math.sin(2*t)-y*math.cos(2*t),9)) for x,y in pts}
        cnt += img == S
    return cnt
chk("оси", axes_regular(3) == 3 and axes_regular(4) == 4 and axes_regular(8) == 8 and axes_regular(6) == 6)
chk("9.3", 360//8 == 45)
# треугольник 7,7,4: какие вершины годятся для оси (равенство сторон из вершины)
sides_at = [(7,7),(7,4),(7,4)]
chk("u9", sum(a == b for a,b in sides_at) == 1)
# ---- гл. 10 / блок 10 (координаты от O: вправо +, вверх +)
cs = lambda p: (-p[0], -p[1]); sh = lambda p,d: (p[0]+d[0], p[1]+d[1]); mir = lambda p: (-p[0], p[1])
A,B = (-3,1),(2,-1)
chk("u10", cs(A) == (3,-1) and cs(B) == (-2,1) and (B[0]-A[0],B[1]-A[1]) == (5,-2) and (cs(B)[0]-cs(A)[0], cs(B)[1]-cs(A)[1]) == (-5,2))
chk("u10 ошибки", mir(A) == (3,1) and mir((-4,0)) == (4,0) and mir((2,0)) == (-2,0))
P = (4,1)
chk("10.1", cs(P) == (-4,-1) and sh(P,(-2,-3)) == (2,-2))
chk("10.2", mir((-3,0)) == (3,0) and mir((1,0)) == (-1,0) and 1-(-3) == 4 == 3-(-1))
chk("10.3", 4*2 == 8 and 2*(4+2) == 12)
# ---- гл. 11 / блок 11
ang = lambda n: F(180*(n-2), n)
chk("u11 таблица", [(180*(n-2), ang(n)) for n in (3,4,5,6,8,10,12)] == [(180,60),(360,90),(540,108),(720,120),(1080,135),(1440,144),(1800,150)])
chk("u11 список", [(n-3, n-2, 180*(n-2)) for n in (4,5,6)] == [(1,2,360),(2,3,540),(3,4,720)])
chk("u11 разбор", [n for n in range(3,1000) if ang(n) == 156] == [15] and 180-156 == 24 and 360//24 == 15 and 180*13 == 2340 and 180*(15-2) == 156*15)
chk("u11 мощение", 360 % 120 == 0 and 3*108 == 324 and 4*108 == 432)
chk("11.1", [ang(n) for n in (9,18,20)] == [140,160,162] and [180*(n-2) for n in (9,18,20)] == [1260,2880,3240])
chk("11.3", 360//60 == 6 and ang(8) == 135 and 2*135 == 270 and 3*135 == 405 and 360 % 135 != 0)
chk("11.2 домик", 90+90+150+150+60 == 180*3)
s = [2,5,2,5,2,5]   # равноугольный шестиугольник замыкается?
vx = sum(s[k]*math.cos(math.pi/3*k) for k in range(6)); vy = sum(s[k]*math.sin(math.pi/3*k) for k in range(6))
chk("11.2 шестиугольник", abs(vx) < 1e-9 and abs(vy) < 1e-9)
# ---- гл. 12 / блок 12: перебор (p-угольная грань, q в вершине)
found = [(p,q) for p in range(3,50) for q in range(3,50) if q*ang(p) < 360]
chk("u12 пять", found == [(3,3),(3,4),(3,5),(4,3),(5,3)])
def poly(p,q):
    # F из 1/p + 1/q - 1/2 = 1/E
    E = 1/(F(1,p)+F(1,q)-F(1,2)); return (2*E/q, E, 2*E/p)   # V, E, F
tab = {(3,3):(4,6,4),(4,3):(8,12,6),(3,4):(6,12,8),(5,3):(20,30,12),(3,5):(12,30,20)}
for k,v in tab.items(): chk("u12 таблица", poly(*k) == v and v[0]-v[1]+v[2] == 2)
chk("12.1", 8*3//2 == 12 and 8*3//4 == 6 and 12*5//2 == 30 and 12*5//3 == 20)
chk("12.2", 5*60 == 300 < 360 and 2*90 == 180)
chk("12.3", 12*5 == 60 and 60//2 == 30 and 30*5 == 150 and poly(3,5)[1] == 30)
# склейка двух тетраэдров: вершины a,b,c (общая грань), t,u
faces = [f for apex in "tu" for f in ({apex,"a","b"},{apex,"b","c"},{apex,"a","c"})]
deg = {v: sum(v in f for f in faces) for v in "abctu"}
chk("u12 контрпример", len(faces) == 6 and sorted(deg.values()) == [3,3,4,4,4])
# ---- гл. 13 / блок 13
chk("u13", 8/2 == 4 and 8+4 == 12 and 4*3 == 12)
chk("13.2", 15//3 == 5 and 2*5 == 10 and F(15,2) == F("7.5"))
# центр описанной окружности: пересечение двух серединных перпендикуляров лежит на третьем
def circ(A,B,C):
    ax,ay=A; bx,by=B; cx,cy=C
    d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    ux = F((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by), d)
    uy = F((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax), d)
    return ux,uy
A,B,C = (0,0),(7,1),(2,5); u = circ(A,B,C)
d2 = lambda p,q: (p[0]-q[0])**2+(p[1]-q[1])**2
chk("u13 равноудалённость", d2(u,A) == d2(u,B) == d2(u,C))
# ---- 9.1: оси симметрии многоугольника перебором (кандидаты: серединные перпендикуляры пар вершин и прямые через пары вершин)
def axes_poly(P):
    S = {(round(x,6), round(y,6)) for x,y in P}; found = set()
    def refl(p, a, d):                      # отражение p в прямой через a с направлением d
        vx, vy = p[0]-a[0], p[1]-a[1]; n = d[0]*d[0]+d[1]*d[1]
        t = (vx*d[0]+vy*d[1])/n
        return (round(2*(a[0]+t*d[0])-p[0],6), round(2*(a[1]+t*d[1])-p[1],6))
    for i in range(len(P)):
        for j in range(i+1, len(P)):
            p, q = P[i], P[j]; m = ((p[0]+q[0])/2, (p[1]+q[1])/2); d = (q[0]-p[0], q[1]-p[1])
            for a, dd in ((m, (-d[1], d[0])), (p, d)):
                if {refl(v, a, dd) for v in P} == S:
                    ang = round(math.atan2(dd[1], dd[0]) % math.pi, 5) % round(math.pi, 5)
                    off = round((a[0]*dd[1]-a[1]*dd[0])/math.hypot(*dd), 5)
                    if ang == 0: off = abs(off)
                    found.add((ang, abs(off)))
    return len(found)
chk("9.1 ромб", axes_poly([(2,0),(0,1),(-2,0),(0,-1)]) == 2)
chk("9.1 разносторонний", axes_poly([(0,0),(7,1),(2,5)]) == 0)
chk("9.1 контроль: квадрат, прямоугольник", axes_poly([(1,1),(-1,1),(-1,-1),(1,-1)]) == 4 and axes_poly([(3,1),(-3,1),(-3,-1),(3,-1)]) == 2)
# 11.2: домик — стороны и углы по координатам
h = 2*math.sqrt(3); dom = [(0,0),(4,0),(4,4),(2,4+h),(0,4)]
def side(i): a,b = dom[i], dom[(i+1)%5]; return math.dist(a,b)
def angle(i):
    a,b,c = dom[i-1], dom[i], dom[(i+1)%5]
    v1=(a[0]-b[0],a[1]-b[1]); v2=(c[0]-b[0],c[1]-b[1])
    return round(math.degrees(math.acos((v1[0]*v2[0]+v1[1]*v2[1])/(math.hypot(*v1)*math.hypot(*v2)))))
chk("11.2 домик по координатам", all(abs(side(i)-4) < 1e-9 for i in range(5)) and [angle(i) for i in range(5)] == [90,90,150,60,150])
chk("11.2 треугольник", ang(3) == 60)
chk("2.2 контрпримеры", 4 != 9 and 80+100 == 180 and 80 != 90)
chk("u13 перегиб", 6//2 == 3)
print("все проверки прошли:", ok)
