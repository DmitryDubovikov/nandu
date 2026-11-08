# E15: дно лотка 3×4 (3 строки, 4 столбца), два одинаковых бруска 1×3 (горизонтально или вертикально)
# и один кубик на одну клетку; детали не налезают друг на друга и не выходят за край.
# Перебор напрямую по условию: все пары мест брусков и все клетки кубика.
from itertools import combinations
from collections import Counter

R, C = 3, 4
places = []  # (клетки, горизонтальный?)
for r in range(R):
    for c in range(C):
        if c + 2 < C:
            places.append((frozenset({(r, c), (r, c + 1), (r, c + 2)}), True))
        if r + 2 < R:
            places.append((frozenset({(r, c), (r + 1, c), (r + 2, c)}), False))
cells = {(r, c) for r in range(R) for c in range(C)}

worlds = Counter()
pairs = Counter()
total = 0
for a, b in combinations(places, 2):
    if a[0] & b[0]:
        continue
    h = a[1] + b[1]
    pairs[h] += 1
    for cube in cells:
        if cube in a[0] or cube in b[0]:
            continue
        total += 1
        worlds[h] += 1

print("мест для одного бруска:", len(places))
print("N =", total)
for h in (2, 1, 0):
    print(f"N({h} гориз.): раскладок брусков {pairs[h]}, с кубиком {worlds[h]}")
print("если бруски разные:", total * 2)
# мир N(1 гориз.) по местам вертикального бруска
v = Counter()
for a, b in combinations(places, 2):
    if not (a[0] & b[0]) and a[1] + b[1] == 1:
        vert = a if not a[1] else b
        v[min(c for (_, c) in vert[0])] += 1
print("N(1 гориз.) по столбцу вертикального (0..3):", dict(v))
print("без кубика:", sum(pairs.values()))
print("пары мест без проверки налезания, умножить на 6:", len(list(combinations(places, 2))) * 6)
