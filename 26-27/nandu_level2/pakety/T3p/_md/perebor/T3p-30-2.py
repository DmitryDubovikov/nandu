"""T3p-30-2: дни смены 1–12, три дня дежурства, между любыми двумя днями дежурства
два или больше дней без дежурства. Перебор всех выборов трёх дней прямо по условию."""
from itertools import combinations
from collections import Counter

DAYS = range(1, 13)


def ok(choice, gap):
    s = set(choice)
    for p, q in combinations(sorted(choice), 2):
        free = sum(1 for d in range(p + 1, q) if d not in s)
        if free < gap:
            return False
    return True


good = [c for c in combinations(DAYS, 3) if ok(c, 2)]
by_mid = Counter(c[1] for c in good)
print('всего выборов трёх дней:', len(list(combinations(DAYS, 3))))
print('N =', len(good))
print('по среднему дежурству:', dict(sorted(by_mid.items())))
print('мир 4:', [c for c in good if c[1] == 4])
# ловушки
print('ловушка «хватит одного дня между» (gap 1):', sum(ok(c, 1) for c in combinations(DAYS, 3)))
print('ловушка «больше двух» (gap 3):', sum(ok(c, 3) for c in combinations(DAYS, 3)))
print('ловушка «порядок назначения важен»:', len(good) * 6)
