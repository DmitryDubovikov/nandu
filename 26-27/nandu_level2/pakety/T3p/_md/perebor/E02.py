# E02: пол 3×3, три одинаковые дощечки 1×2 (горизонтально или вертикально), не налезают и не выходят за край.
# Перебор всех наборов из трёх мест дощечек напрямую по условию.
from itertools import combinations
from collections import Counter

n = 3
places = []  # (клетки, горизонтальная?)
for r in range(n):
    for c in range(n):
        if c + 1 < n:
            places.append((frozenset({(r, c), (r, c + 1)}), True))
        if r + 1 < n:
            places.append((frozenset({(r, c), (r + 1, c)}), False))

worlds = Counter()
total = 0
for trio in combinations(places, 3):
    cells = [p[0] for p in trio]
    if len(cells[0] | cells[1] | cells[2]) != 6:
        continue
    total += 1
    worlds[sum(p[1] for p in trio)] += 1

print("мест для одной дощечки:", len(places))
print("N =", total)
for h in range(4):
    print(f"N({h} гориз.) =", worlds[h])
print("если дощечки разные:", total * 6)
