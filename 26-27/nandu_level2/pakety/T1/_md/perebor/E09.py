# Перебор E09: морковь m, свёкла s, укроп d (пакетики, целые >= 0)
sols = []
for m in range(0, 80):
    for s in range(0, 80):
        for d in range(0, 80):
            if m + s + d == 36 and 8*m + 6*s + 4*d == 228 and m + 2*s + 2*d == 57:
                sols.append((m, s, d))
print("решений:", len(sols))
for x in sols:
    print("морковь, свёкла, укроп =", x)
