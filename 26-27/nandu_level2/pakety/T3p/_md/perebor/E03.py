# E03: пять шкафчиков c1..c5, цифры 1..6 без повторов, c2 + c4 = 8, c1 != 5.
# Перебор всех размещений напрямую по условию; счёт по мирам (c2, c4).
from itertools import permutations
from collections import Counter

vsego = 0
miry = Counter()
for p in permutations(range(1, 7), 5):
    c1, c2, c3, c4, c5 = p
    if c2 + c4 == 8 and c1 != 5:
        vsego += 1
        miry[(c2, c4)] += 1
print('N =', vsego)
for k in sorted(miry):
    print('N%s = %d' % (k, miry[k]))
# ловушки
bez_c1 = sum(1 for p in permutations(range(1, 7), 5) if p[1] + p[3] == 8)
print('без c1 != 5:', bez_c1)
from itertools import product
s44 = sum(1 for p in product(range(1, 7), repeat=5)
          if p[1] + p[3] == 8 and p[0] != 5
          and len({p[0], p[1], p[2], p[4]}) == 4 and len({p[0], p[3], p[2], p[4]}) == 4)
print('с парой (4, 4):', s44)
print('без переставленных пар:', miry[(2, 6)] + miry[(3, 5)])
