sols = []
for a in range(1, 346):
    for b in range(1, 661):
        if 2*a + b >= 690 or a + 2*b >= 660:
            continue
        for c in range(1, 231):
            if 2*a + b + 3*c == 690 and a + 2*b + 3*c == 660:
                sols.append((a, b, c))
print("решений:", len(sols))
print("значения a+b+2c:", sorted({a + b + 2*c for a, b, c in sols}))
print("пример:", sols[:3])
print("a-b:", sorted({a-b for a,b,c in sols}))
