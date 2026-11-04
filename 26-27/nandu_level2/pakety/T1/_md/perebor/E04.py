from fractions import Fraction as F
sols = []
for v in range(0, 21):
    for m in range(0, 21):
        for p in range(0, 21):
            if v + m + p != 20:
                continue
            S = 8*v + 12*m + 16*p
            if S - F(1, 4)*12*m != 238:
                continue
            if S - F(1, 4)*16*p != 220:
                continue
            sols.append((v, m, p))
print("решений:", len(sols))
for v, m, p in sols:
    print(f"овощных={v}, грибных={m}, пепперони={p}")
