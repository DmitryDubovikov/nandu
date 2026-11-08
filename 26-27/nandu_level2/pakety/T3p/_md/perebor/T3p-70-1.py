# T3p-70-1: шесть прудов, каналы со стрелками, высоты 1–7, повторы разрешены.
# Стрелки (вода течёт сверху вниз, стрелка x → y значит: x выше y):
#   c1 → c2 → c6  (левый канал),  c1 → c3 → c4 → c5 → c6  (правый канал).
# Перебор всех 7^6 = 117 649 наборов высот напрямую по условию.
from itertools import product
from collections import Counter

ARROWS = [(1, 2), (2, 6), (1, 3), (3, 4), (4, 5), (5, 6)]

def ok(c):
    return all(c[x] > c[y] for x, y in ARROWS)

worlds = Counter()
left, right = Counter(), Counter()
total = 0
distinct = 0
for h in product(range(1, 8), repeat=6):
    c = dict(zip(range(1, 7), h))
    if not ok(c):
        continue
    total += 1
    worlds[(c[1], c[6])] += 1
    if len(set(h)) == 6:
        distinct += 1

# отдельно по частям в каждом мире
for (t, b) in sorted(worlds):
    nl = sum(1 for x in range(1, 8) if t > x > b)
    nr = sum(1 for p in product(range(1, 8), repeat=3) if t > p[0] > p[1] > p[2] > b)
    left[(t, b)], right[(t, b)] = nl, nr

print('N =', total)
for w in sorted(worlds):
    print(f'N{w} = {left[w]} * {right[w]} = {worlds[w]}', 'OK' if left[w] * right[w] == worlds[w] else 'MISMATCH')
print('ловушка «все высоты разные»:', distinct)
print('ловушка «сложить вместо умножить»:', sum(left[w] + right[w] for w in worlds))
print('ловушка «тройка правого канала в любом порядке» (·6):', sum(left[w] * right[w] * 6 for w in worlds))
