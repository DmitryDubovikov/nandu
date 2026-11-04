# Перебор: точилка s, линейка r, пенал p (целые положительные)
sols = []
for s in range(1, 106):
    for r in range(1, 106):
        for p in range(1, 106):
            if 2 * s == r and p == r + s and p + 2 * r == 105:
                sols.append((s, r, p))
print("решений:", len(sols))
for s, r, p in sols:
    print("точилка", s, "линейка", r, "пенал", p)
