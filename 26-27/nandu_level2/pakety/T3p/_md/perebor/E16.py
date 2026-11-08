# E16: табло 2×3, карточки с цифрами 1–6, каждая по разу; строки читаются как трёхзначные числа.
# Условия: число первой строки чётное, число второй строки чётное; сумма двух чисел наибольшая.
# а) наибольшая сумма, б) число раскладок с ней.
from itertools import permutations
from collections import Counter

good = []
for p in permutations(range(1, 7)):          # p[0..2] — c₁ c₂ c₃, p[3..5] — c₄ c₅ c₆
    r1 = 100 * p[0] + 10 * p[1] + p[2]
    r2 = 100 * p[3] + 10 * p[4] + p[5]
    if r1 % 2 == 0 and r2 % 2 == 0:
        good.append((r1 + r2, p))
best = max(s for s, _ in good)
top = [p for s, p in good if s == best]
print('годных раскладок:', len(good))
print('а) наибольшая сумма =', best)
print('б) N =', len(top))
print('столбцы на максимуме:', Counter((frozenset((p[0], p[3])), frozenset((p[1], p[4])), frozenset((p[2], p[5]))) for p in top))
print('по (c₁, c₂, c₃):', Counter((p[0], p[1], p[2]) for p in top))
for p in top:
    print(' ', ''.join(map(str, p[:3])), '+', ''.join(map(str, p[3:])))
# ловушки
free = max(100 * p[0] + 10 * p[1] + p[2] + 100 * p[3] + 10 * p[4] + p[5] for p in permutations(range(1, 7)))
print('ловушка «без чётности»: наибольшая сумма =', free)
greedy1 = max(s for s, p in good if 100 * p[0] + 10 * p[1] + p[2] == max(100 * q[0] + 10 * q[1] + q[2] for _, q in good))
print('ловушка «первое число наибольшее»: сумма =', greedy1)
print('ловушка «пара чисел без порядка строк»:', len({frozenset((p[:3], p[3:])) for p in top}))
