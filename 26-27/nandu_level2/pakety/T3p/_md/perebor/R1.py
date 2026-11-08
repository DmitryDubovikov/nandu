# R1: пять крючков c1..c5, рюкзаки 1..8 (каждый один), c2 * c4 = 8, c1 != 2.
# Перебор всех размещений прямо по условию; проверка наблюдения и первой формулы.
from itertools import permutations
from collections import Counter

def ok(p):
    return len(set(p)) == 5 and all(1 <= v <= 8 for v in p) and p[1] * p[3] == 8 and p[0] != 2

vse = [p for p in permutations(range(1, 9), 5) if ok(p)]
miry = Counter((p[1], p[3]) for p in vse)
PARY = {(1, 8), (8, 1), (2, 4), (4, 2)}
print('N =', len(vse))
for k in sorted(miry):
    print('N%s = %d' % (k, miry[k]))
print('наблюдение (пара всегда из списка):', all((p[1], p[3]) in PARY for p in vse))
print('все четыре пары встречаются:', set(miry) == PARY)
print('сумма операндов = N:', sum(miry[k] for k in PARY) == len(vse))
GOOD = [(3, 1, 5, 8, 6), (7, 2, 6, 4, 1), (5, 8, 2, 1, 7), (1, 4, 7, 2, 3), (6, 1, 3, 8, 2)]
BAD = (5, 8, 3, 2, 6)
print('примеры подходят:', all(ok(p) for p in GOOD), '| разные:', len(set(GOOD)) == len(GOOD))
print('неподходящее не подходит:', not ok(BAD),
      '| нарушено только произведение:', BAD[1] * BAD[3] != 8 and BAD[0] != 2 and len(set(BAD)) == 5)
