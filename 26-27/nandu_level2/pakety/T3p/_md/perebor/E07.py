# E07: слово ТОРТ на табличке 3 × 4, переходы к соседней клетке (сторона или вершина),
# одну клетку дважды нельзя. Перебор всех упорядоченных четвёрок клеток прямо по условию.
from itertools import product
from collections import Counter

ROWS = ["ТТРТ", "ТОРТ", "ТТТТ"]
R, C = len(ROWS), len(ROWS[0])
cells = [(r, c) for r in range(R) for c in range(C)]
letter = {(r, c): ROWS[r][c] for r, c in cells}
num = {cell: i + 1 for i, cell in enumerate(cells)}  # номера по строкам

def king(a, b):
    return a != b and abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1

def side(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

def count(adj, distinct=True):
    worlds = Counter()
    for path in product(cells, repeat=4):
        if "".join(letter[p] for p in path) != "ТОРТ":
            continue
        if not all(adj(path[i], path[i + 1]) for i in range(3)):
            continue
        if distinct and len(set(path)) < 4:
            continue
        worlds[(num[path[1]], num[path[2]])] += 1
    return sum(worlds.values()), dict(sorted(worlds.items()))

print("ответ:", count(king))
print("ловушка: соседи только по стороне:", count(side))
print("ловушка: без запрета «дважды»:", count(king, distinct=False))
