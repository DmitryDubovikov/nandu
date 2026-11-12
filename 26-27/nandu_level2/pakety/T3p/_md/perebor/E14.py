# E14: доска 2×2 (клетки c1..c4), в каждой карточка с цифрой 2, 4 или 9 (повторы можно),
# произведение четырёх цифр — квадрат целого числа. Миры — по числу клеток с цифрой 2.
from itertools import product
from math import isqrt
good = [p for p in product((2, 4, 9), repeat=4) if isqrt(p[0]*p[1]*p[2]*p[3])**2 == p[0]*p[1]*p[2]*p[3]]
w = {k: sum(1 for p in good if p.count(2) == k) for k in range(5)}
assert w == {0: 16, 1: 0, 2: 24, 3: 0, 4: 1}, w
assert sum(1 for p in good if p[0] == p[1] == 2 and p.count(2) == 2) == 4
assert len({tuple(sorted(p)) for p in good}) == 9          # ловушка: наборы вместо заполнений
assert 16 + 4 + 1 == 21 and 3 * 3 * 3 == 27                 # ловушки
# ход «в последней клетке всегда одна цифра» не проходит:
assert {sum(1 for d in (2, 4, 9) if (a, b, c, d) in set(good)) for a, b, c in product((2, 4, 9), repeat=3)} == {1, 2}
print("N =", len(good)); assert len(good) == 41
