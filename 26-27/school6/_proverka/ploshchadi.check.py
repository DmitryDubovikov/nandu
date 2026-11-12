"""Проверка пары 3 «Площади»: все числа примеров учебника и все ответы решебника.
Независимые пути: координаты + формула шнурков, перебор по сетке (формула Пика), Fraction."""
from fractions import Fraction as F
from math import gcd, isqrt

def shoelace(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(F(s)) / 2

def pick(pts):
    """Площадь выпуклого многоугольника с целыми вершинами перебором узлов: S = I + B/2 - 1."""
    n = len(pts)
    def side(p, a, b):
        return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    I = B = 0
    for x in range(min(xs), max(xs)+1):
        for y in range(min(ys), max(ys)+1):
            d = [side((x, y), pts[i], pts[(i+1) % n]) for i in range(n)]
            if all(v > 0 for v in d) or all(v < 0 for v in d): I += 1
            elif all(v >= 0 for v in d) or all(v <= 0 for v in d): B += 1
    return F(I) + F(B, 2) - 1

def eq(name, got, want):
    assert got == want, f"{name}: получено {got}, в тексте {want}"
    print(f"ok  {name}: {got}")

def tri(a, h): return F(a) * h / 2

# ---------- УЧЕБНИК ----------
# Гл. 1: прямоугольник 6 × 3 клетки, половина; разбор
eq("У1 клетки", (6*3, F(6*3, 2)), (18, 9))
eq("У1 рисунок ABC", shoelace([(0,3),(6,3),(6,0)]), 9)
eq("У1 (а)", tri(8, 5), 20)
eq("У1 (б)", F(30*2, 5), 12)
# Гл. 2: K(0,0) L(2,4) M(6,1)
K, L, M = (0,0), (2,4), (6,1)
eq("У2 шнурки", shoelace([K, L, M]), 11)
eq("У2 Пик", pick([K, L, M]), 11)
eq("У2 углы", (tri(2,4), tri(4,3), tri(1,6), 6*4 - 4 - 6 - 3), (4, 6, 3, 11))
# Гл. 3: показ на числах 2 + 5, h = 4; разбор A(0,0) B(6,0) C(9,4)
eq("У3 показ", (tri(2,4), tri(5,4), tri(2,4)+tri(5,4), tri(7,4)), (4, 10, 14, 14))
A, B, C, H = (0,0), (6,0), (9,4), (9,0)
eq("У3 AHC", shoelace([A, H, C]), 18)
eq("У3 BHC", shoelace([B, H, C]), 6)
eq("У3 ABC", shoelace([A, B, C]), 12)
eq("У3 BC² = 25", (C[0]-B[0])**2 + (C[1]-B[1])**2, 25)
eq("У3 высота к BC", 2*shoelace([A, B, C]) / 5, F(24, 5))
# Гл. 4: показ 2 и 8, h = 5 и 3; разбор
eq("У4 показ", (tri(2,5), tri(8,5), tri(2,5)/tri(8,5), tri(2,3), tri(8,3), tri(2,3)/tri(8,3)), (5, 20, F(1,4), 3, 12, F(1,4)))
A, C, B = (0,0), (10,0), (3,8)      # S(ABC) = 40
D = (4, 0)                          # AD : DC = 2 : 3
eq("У4 S(ABC)", shoelace([A, B, C]), 40)
eq("У4 части", (shoelace([A, B, D]), shoelace([D, B, C])), (16, 24))
# Гл. 5: AC = 10, B на 3 выше, D на 5 ниже
A, C, B, D = (0,0), (10,0), (4,3), (6,-5)
eq("У5", (shoelace([A,B,C]), shoelace([A,C,D]), shoelace([A,B,C,D]), F(15,25)), (15, 25, 40, F(3,5)))
eq("У5 галочка", shoelace([A,C,D]) - shoelace([A,B,C]), 10)
# Гл. 6: прямоугольник 10 × 6, P где угодно на BC
for p in range(0, 11):
    A, B, C, D, P = (0,0), (0,6), (10,6), (10,0), (p,6)
    assert shoelace([A,P,D]) == 30 and shoelace([A,B,P]) + shoelace([P,C,D]) == 30
print("ok  У6: S(APD) = 30 и сумма 30 при любом P")
# трапеция: S(ABO) = S(DCO) перебором
for b in range(1, 6):
    for a in range(b+1, 9):
        for p in range(0, 4):
            for h in range(1, 5):
                A, D, B, C = (F(0),F(0)), (F(a),F(0)), (F(p),F(h)), (F(p+b),F(h))
                t = F(a, a+b); O = (A[0] + t*(C[0]-A[0]), t*h)
                assert shoelace([A,B,O]) == shoelace([D,C,O])
                assert shoelace([A,B,D]) == shoelace([A,C,D])
print("ok  У6 трапеция: S(AOB) = S(COD)")
# Гл. 7
eq("У7", (5*3 - 2*1, 4*4, (5*3 - 2*1) * 4*4), (13, 16, 208))
cells = {(i, j) for i in range(5) for j in range(3)} - {(3, 0), (4, 0)}
eq("У7 клетки рисунка × 16", len(cells) * 16, 208)
eq("У7 масштаб", (3*3, 6*6, F(36, 9)), (9, 36, 4))
# Гл. 8
tab = {11:121,12:144,13:169,14:196,15:225,16:256,17:289,18:324,19:361,20:400,25:625}
assert all(k*k == v for k, v in tab.items()); print("ok  У8 таблица квадратов")
eq("У8 последние цифры", [d*d % 10 for d in range(10)], [0,1,4,9,6,5,6,9,4,1])
eq("У8 √576", isqrt(576), 24); assert 24*24 == 576 and 25*25 == 625
x2 = F(324) / (4*3 - F(2*3, 2)); x = isqrt(int(x2))
eq("У8 разбор", (4*3 - F(2*3,2), x2, x, 4*x, 3*x, 24*18 - F(12*18, 2)), (9, 36, 6, 24, 18, 324))
eq("У8 рисунок ABED", shoelace([(0,3),(4,3),(2,0),(0,0)]), 9)

# ---------- РЕШЕБНИК ----------
eq("1.1", (tri(9,4), tri(7,10), tri(15,6)), (18, 35, 45))
eq("1.2", (tri(6,8), 6*6 + 8*8 == 10*10), (24, True))
eq("1.3", (tri(12,9), F(54*2, 6)), (54, 18))
A, B, C = (0,0), (5,2), (1,4)
eq("2.1", (shoelace([A,B,C]), pick([A,B,C]), 5*4 - tri(5,2) - tri(4,2) - tri(1,4)), (9, 9, 9))
A, B, C, D = (0,0), (6,0), (6,3), (2,5)
eq("2.2", (shoelace([A,B,C,D]), pick([A,B,C,D]), 6*5 - tri(2,4) - tri(2,5)), (21, 21, 21))
q = [(10,0), (40,12), (25,30), (0,24)]
eq("2.3", (shoelace(q), pick(q), tri(10,24), tri(30,12), tri(18,15), tri(25,6), shoelace(q) > 600), (690, 690, 120, 180, 135, 75, True))
eq("3.1", (tri(10,7), F(42*2, 12)), (35, 7))
M_, N_, P_, T_ = (0,0), (11,0), (-5,8), (-5,0)   # высота PT за точкой M
eq("3.2", (shoelace([M_,N_,P_]), shoelace([N_,T_,P_]), shoelace([M_,T_,P_]), tri(11+5,8), 64 - 20), (44, 64, 20, 64, 44))
eq("3.3", (tri(12,6), F(36*2, 8), 6 <= 8, 9 <= 12), (36, 9, True, True))
N, K_, L_, M_ = (2,6), (0,0), (9,0), (3,0)       # высота 6: S(KMN) = 9
eq("4.1", (shoelace([K_,M_,N]), shoelace([M_,L_,N]), shoelace([K_,L_,N])), (9, 18, 27))
A, B, C = (1,10), (0,0), (10,0); Mid = (5,0)      # S(ABC) = 50
eq("4.2", (shoelace([A,B,C]), shoelace([A,B,Mid]), shoelace([A,Mid,C])), (50, 25, 25))
P, R, Q, A = (0,0), (14,0), (5,6), (4,0)
eq("4.3", (shoelace([P,Q,A]), shoelace([A,Q,R]), 14 - 4, shoelace([P,Q,(7,0)]), shoelace([(7,0),Q,R]), 7 - 4), (12, 30, 10, 21, 21, 3))
E, G, Fv, Hv = (0,0), (12,0), (5,4), (7,-7)
eq("5.1", (shoelace([E,Fv,G]), shoelace([E,G,Hv]), shoelace([E,Fv,G,Hv]), F(24,42)), (24, 42, 66, F(4,7)))
KL = F(18*2, 9); eq("5.2", (KL, F(6*2) / KL), (4, 3))
hC = F(45*2, 10); eq("5.3", (hC, hC/3, tri(10, hC/3)), (9, 3, 15))
eq("6.1", tri(14,8), 56)
eq("6.2", (tri(12,5), tri(6,5), F(12+6)*5/2), (30, 15, 45))
# 6.3: трапеция A(0,0) D(12,0) B(1,6) C(7,6)
A, D, B, C = (F(0),F(0)), (F(12),F(0)), (F(1),F(6)), (F(7),F(6))
t = F(12, 18); O = (t*C[0], t*C[1])
eq("6.3", (shoelace([A,O,B]), shoelace([A,O,D]), shoelace([C,O,D]), shoelace([B,O,C]), shoelace([A,B,C,D])), (12, 24, 12, 6, 54))
eq("7.1", (1 + 4 + 9, 14 * 9), (14, 126))
eq("7.2", (F(400*300, 100*100), 100*100), (12, 10000))
def tshape(x):   # перекладина 7x × x сверху, ножка x × 4x под серединой
    return [(0,4*x),(0,5*x),(7*x,5*x),(7*x,4*x),(4*x,4*x),(4*x,0),(3*x,0),(3*x,4*x)]
def perim(p): return sum(abs(p[i][0]-p[(i+1)%len(p)][0]) + abs(p[i][1]-p[(i+1)%len(p)][1]) for i in range(len(p)))
eq("7.3", (shoelace(tshape(1)), shoelace(tshape(5)), shoelace(tshape(15)), F(perim(tshape(15)), perim(tshape(5))), shoelace(tshape(15))/shoelace(tshape(5)), 11*225), (11, 275, 2475, 3, 9, 2475))
eq("8.1", [isqrt(n) for n in (81,144,225,441,676)], [9,12,15,21,26])
assert all(isqrt(n)**2 == n for n in (81,144,225,441,676,196,576))
eq("8.2", (isqrt(196), 4*isqrt(196)), (14, 56))
x2 = F(980) / (16 + F(4*2, 2)); x = isqrt(int(x2))
eq("8.3", (x2, x, 4*x, tri(4*x, 2*x), (4*x)**2 + tri(4*x, 2*x)), (49, 7, 28, 196, 980))

print("ВСЁ СХОДИТСЯ")
