# T3p-50-2: слово АННА на мозаике 3 × 4 (Н в клетках 1, 4, 6, 7, 9, 12), соседи — по стороне или по вершине.
# Перебор всех упорядоченных четвёрок разных клеток напрямую по условию.
from itertools import permutations
from collections import Counter

ROWS = ["НААН", "АННА", "НААН"]
cells = {}
for r, row in enumerate(ROWS):
    for c, ch in enumerate(row):
        cells[r * 4 + c + 1] = (r, c, ch)

def adj(p, q, vertex=True):
    (r1, c1, _), (r2, c2, _) = cells[p], cells[q]
    d = (abs(r1 - r2), abs(c1 - c2))
    return d in ((0, 1), (1, 0)) or (vertex and d == (1, 1))

def count(vertex=True, distinct=True):
    tot, worlds, pairs = 0, Counter(), Counter()
    seq = permutations(cells, 4) if distinct else ((a, b, x, d) for a in cells for b in cells for x in cells for d in cells)
    for p in seq:
        if ''.join(cells[i][2] for i in p) != "АННА":
            continue
        if not all(adj(p[i], p[i + 1], vertex) for i in range(3)):
            continue
        tot += 1
        (r1, c1, _), (r2, c2, _) = cells[p[1]], cells[p[2]]
        worlds['по стороне' if abs(r1 - r2) + abs(c1 - c2) == 1 else 'по вершине'] += 1
        pairs[(p[1], p[2])] += 1
    return tot, worlds, pairs

tot, worlds, pairs = count()
print("N =", tot)
print("по мирам:", dict(worlds))
print("по парам (Н, Н):", dict(sorted(pairs.items())))
print("ловушка: соседи только по стороне ->", count(vertex=False)[0])
print("ловушка: без запрета «дважды» ->", count(distinct=False)[0])
print("ловушка: путь и обратный — один способ ->", tot // 2)
