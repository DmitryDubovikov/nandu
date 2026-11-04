sols = []
for a in range(0, 51):
    for c in range(0, 51):
        for u in range(0, 51):
            if a + c + u == 50 and a + c == 44 and a + u == 3 * (c + u):
                sols.append((a, c, u))
print("решений:", len(sols))
for a, c, u in sols:
    print("Аргентина", a, "Чили", c, "Уругвай", u)
