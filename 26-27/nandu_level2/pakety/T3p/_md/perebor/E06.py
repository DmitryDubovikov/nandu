# E06: луг 2×6 участков, три одинаковых улья, ульи не на участках с общей стороной или общей вершиной.
from itertools import combinations
from collections import Counter

cells = [(r, col) for r in range(2) for col in range(6)]   # r — ряд 0/1, col — столбец 0..5


def king(p, q):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1])) == 1


def side(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1]) == 1


N = 0
worlds = Counter()
side_only = 0
for s in combinations(cells, 3):
    if not any(side(p, q) for p, q in combinations(s, 2)):
        side_only += 1
    if any(king(p, q) for p, q in combinations(s, 2)):
        continue
    N += 1
    squares = sorted(col // 2 for _, col in s)
    assert squares == [0, 1, 2], s           # в каждом квадрате ровно один улей
    mid = [p for p in s if p[1] // 2 == 1][0]
    worlds['слева' if mid[1] == 2 else 'справа'] += 1

print('N =', N)
print('N(в квадрате 2 слева) =', worlds['слева'])
print('N(в квадрате 2 справа) =', worlds['справа'])
# ловушка: улей квадрата 2 закрывает в соседнем квадрате только участок своего ряда
row_only = 0
for s in combinations(cells, 3):
    if sorted(col // 2 for _, col in s) != [0, 1, 2]:
        continue
    if any(side(p, q) for p, q in combinations(s, 2)):
        continue
    row_only += 1
print('ловушки: ульи разные =', N * 6, '; только общая сторона =', side_only,
      '; закрыт только участок своего ряда =', row_only)
