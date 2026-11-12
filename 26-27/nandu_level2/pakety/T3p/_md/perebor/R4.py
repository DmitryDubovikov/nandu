# R4: поезд из трёх разных вагонов 1..6, c1 * c3 = 12.
from itertools import permutations
good = [p for p in permutations(range(1, 7), 3) if p[0] * p[2] == 12]
pairs = sorted({(p[0], p[2]) for p in good})
assert pairs == [(2, 6), (3, 4), (4, 3), (6, 2)]
assert all(sum(1 for p in good if (p[0], p[2]) == q) == 4 for q in pairs)
assert sorted(p[1] for p in good if (p[0], p[2]) == (2, 6)) == [1, 3, 4, 5]
print("N =", len(good)); assert len(good) == 16
