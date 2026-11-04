# Перебор: номера на 1,2,3,4 человека (a,b,c,d)
sols = []
for a in range(0, 147):
    for b in range(0, 147 - a):
        for c in range(0, 147 - a - b):
            d = 146 - a - b - c
            if a + 2*b + 3*c + 4*d != 306: continue
            if (2*a + b + c) * 2 + d != 183 * 2: continue   # d/2 номеров
            if 2*a + 2*b + 3*c + 4*(d/2) != 316: continue
            sols.append((a, b, c, d))
for s in sols: print("a,b,c,d =", s)
print("решений:", len(sols))
print("доход:", sorted({30*a + 50*b + 60*c + 70*d for a, b, c, d in sols}))
