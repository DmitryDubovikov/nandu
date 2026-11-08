# R4: аллея 6 рядов × 2 площадки, две одинаковые статуи, не на площадках с общей стороной или общей вершиной.
# Наблюдение: в каждом квадрате 2×2 (ряды 1–2, 3–4, 5–6) не больше одной статуи ⇒ ровно один квадрат пуст.
from itertools import combinations
from collections import Counter

cells = [(r, col) for r in range(6) for col in range(2)]   # r — ряд 0..5 сверху, col — 0/1


def touch(p, q):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1])) == 1


def ok(s):
    return not any(touch(p, q) for p, q in combinations(s, 2))


def sq(p):
    return p[0] // 2 + 1        # квадрат 1, 2, 3 сверху вниз


N = 0
worlds = Counter()
for s in combinations(cells, 2):
    if not ok(s):
        continue
    N += 1
    used = [sq(p) for p in s]
    assert len(set(used)) == 2, s                  # не больше одной статуи в квадрате
    empty = {1, 2, 3} - set(used)
    assert len(empty) == 1, s                      # ровно один квадрат пуст
    worlds[empty.pop()] += 1

good = [((0, 0), (3, 1)), ((1, 1), (5, 0)), ((2, 0), (5, 1)), ((0, 1), (2, 1))]
bad = ((2, 0), (3, 1))
for s in good:
    assert ok(s), s
assert len({frozenset(s) for s in good}) == len(good)
assert not ok(bad)
assert sq(bad[0]) == sq(bad[1]) and abs(bad[0][0] - bad[1][0]) == 1 and bad[0][1] != bad[1][1]  # касание вершиной
assert sum(worlds.values()) == N

print('N =', N)
for k in (1, 2, 3):
    print(f'N(пуст {k}) =', worlds[k])
print('примеры: пустой квадрат', [({1, 2, 3} - {sq(p) for p in s}).pop() for s in good])
