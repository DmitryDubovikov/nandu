# E01: стоянка из пяти мест в ряд, машинки 1–6, ставят пять из них.
# Условия: на среднем месте номер больше 4; машинки 1 и 2 обе на стоянке; 1 левее 2.
from itertools import permutations
from collections import Counter

worlds = Counter()
traps = Counter()
for p in permutations(range(1, 7), 5):   # p[i] — машинка на месте i+1
    ok_mid = p[2] > 4
    both = 1 in p and 2 in p
    if ok_mid and both and p.index(1) < p.index(2):
        worlds[p[2]] += 1
    # ловушки
    if ok_mid and both:
        traps['два порядка'] += 1
    if ok_mid and both and p.index(2) - p.index(1) == 1:
        traps['рядом слева'] += 1
    if p[2] >= 4 and both and p.index(1) < p.index(2):
        traps['не меньше 4'] += 1
print('N =', sum(worlds.values()))
for v in sorted(worlds):
    print(f'N(p3 = {v}) =', worlds[v])
print('ловушки:', dict(traps))
