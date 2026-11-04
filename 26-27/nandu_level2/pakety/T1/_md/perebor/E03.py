# E03 — посылки по 1, 2, 5 кг: перебор всех наборов из 48 посылок
sols = []
for a in range(49):              # по 1 кг
    for b in range(0, 49, 2):    # по 2 кг — вдвое меньше должно быть целым
        c = 48 - a - b           # по 5 кг
        if c < 0:
            continue
        if 1 * a + 2 * b + 5 * c != 100:
            continue
        if 1 * a + 2 * (b // 2) + 5 * (2 * c) == 129:
            sols.append((a, b, c))
print(sols)   # [(23, 16, 9)]
