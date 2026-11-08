# E14: доска 2×2 (клетки c1..c4), в каждой карточка с цифрой 2, 3, 4 или 6 (повторы можно),
# произведение четырёх цифр — квадрат целого числа.
from itertools import product
from math import isqrt, prod

vse = list(product((2, 3, 4, 6), repeat=4))
good = [r for r in vse if isqrt(prod(r)) ** 2 == prod(r)]
print('перебрано заполнений:', len(vse))
n36 = lambda r: sum(d in (3, 6) for d in r)
for k in range(5):
    print(f'N(3 или 6 в {k} клетках) =', sum(n36(r) == k for r in good))
print('ОТВЕТ N =', len(good))
print('мир 4 клеток:', [r for r in good if n36(r) == 4])
print('наборов цифр (ловушка 1):', len({tuple(sorted(r)) for r in good}))
# ловушка 2: без выбора мест для двух клеток с 3 или 6 — 8 + 4 · 2 + 8
print('без выбора мест (ловушка 2):', 8 + 4 * 2 + 8)
