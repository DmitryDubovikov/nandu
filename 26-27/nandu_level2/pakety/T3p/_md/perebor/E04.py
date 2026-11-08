# E04: пять площадок, высоты 1..6, повторы разрешены.
# Схема: верхний ряд c1 -> c2 -> c3, снизу c4 (под c1) и c5 (под c3).
# Стрелки (лесенки вверх): c1->c2, c2->c3, c4->c1, c5->c3.
# Стрелка x -> y значит: высота x меньше высоты y.
from itertools import product
from collections import Counter

ARROWS = [(1, 2), (2, 3), (4, 1), (5, 3)]

def ok(h, distinct=False):
    if distinct and len(set(h.values())) < 5:
        return False
    return all(h[x] < h[y] for x, y in ARROWS)

def run(distinct=False):
    total, worlds = 0, Counter()
    left, right = {}, {}
    for t in product(range(1, 7), repeat=5):
        h = dict(zip(range(1, 6), t))
        if ok(h, distinct):
            total += 1
            worlds[h[2]] += 1
    return total, dict(sorted(worlds.items()))

print("ответ:", run())
print("разные высоты:", run(True))
# Отдельно левый и правый столбцы при каждом c2 (прямо по стрелкам)
s_sum = 0
for m in range(1, 7):
    L = sum(1 for c1, c4 in product(range(1, 7), repeat=2) if c4 < c1 < m)
    R = sum(1 for c3, c5 in product(range(1, 7), repeat=2) if m < c3 and c5 < c3)
    if L * R:
        print(f"c2={m}: левый {L}, правый {R}, мир {L*R}, сумма вместо произведения {L+R}")
        s_sum += L + R
print("ловушка «сложить»:", s_sum)
