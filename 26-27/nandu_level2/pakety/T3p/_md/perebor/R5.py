# R5: кузов грузовичка 2 ряда по 4 клетки, две одинаковые коробки (каждая на две соседние клетки,
# вдоль кузова или поперёк) и один мяч на одну клетку; ничего не ставят друг на друга.
# Перебор всех раскладок прямо по условию.
from itertools import combinations

cells = [(r, s) for r in range(2) for s in range(4)]
boxes = []                       # место коробки = пара соседних клеток
for r, s in cells:
    if s + 1 < 4: boxes.append(frozenset({(r, s), (r, s + 1)}))   # вдоль
    if r + 1 < 2: boxes.append(frozenset({(r, s), (r + 1, s)}))   # поперёк
along = lambda b: len({r for r, s in b}) == 1

ways = []                        # способ = (набор мест двух коробок, место мяча)
for b1, b2 in combinations(boxes, 2):           # коробки одинаковые: набор, а не пара по порядку
    if b1 & b2: continue
    for m in cells:
        if m in b1 or m in b2: continue
        ways.append((frozenset({b1, b2}), m))
print('N =', len(ways))

# наблюдение: при любой раскладке коробок мячу остаются ровно 4 клетки
lay = {}
for bb, m in ways: lay.setdefault(bb, []).append(m)
free = {len(v) for v in lay.values()}
print('раскладок коробок:', len(lay), ' свободных клеток для мяча при раскладке:', free)
assert free == {4}

w = {'обе вдоль': 0, 'одна вдоль': 0, 'обе поперёк': 0}
for bb in lay:
    k = sum(along(b) for b in bb)
    w[{2: 'обе вдоль', 1: 'одна вдоль', 0: 'обе поперёк'}[k]] += 1
print('по мирам:', w, ' сумма:', sum(w.values()))
assert (sum(w.values())) * 4 == len(ways)
print('(', ' + '.join(map(str, w.values())), ') · 4 =', sum(w.values()) * 4)

# выписанные примеры
B = lambda *p: frozenset(p)
def way(b1, b2, m): return (frozenset({B(*b1), B(*b2)}), m)
good = [
    way([(0, 0), (0, 1)], [(0, 2), (0, 3)], (1, 2)),
    way([(0, 1), (1, 1)], [(1, 2), (1, 3)], (0, 3)),
    way([(0, 0), (1, 0)], [(0, 3), (1, 3)], (0, 1)),
    way([(0, 1), (0, 2)], [(1, 0), (1, 1)], (1, 3)),
]
S = set(ways)
for g in good: assert g in S, g
print('четыре выписанных примера подходят; миры:',
      [sum(along(b) for b in g[0]) for g in good])
bad = way([(0, 0), (1, 0)], [(0, 2), (0, 3)], (0, 3))
assert bad not in S and bad[1] in set().union(*bad[0])
print('неподходящее: мяч на клетке коробки — не подходит')
