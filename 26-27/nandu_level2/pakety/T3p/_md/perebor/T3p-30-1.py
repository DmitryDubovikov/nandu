# T3p-30-1: пять ячеек камеры хранения в ряд, жетоны 1–7, в ячейки кладут пять разных жетонов.
# Условия: c2 · c4 = 12; жетоны 3 и 5 оба лежат в ячейках; номер ячейки жетона 3 меньше номера ячейки жетона 5.
from itertools import permutations
from collections import Counter

worlds = Counter()
traps = Counter()
for c in permutations(range(1, 8), 5):   # c[i] — жетон в ячейке i+1
    prod = c[1] * c[3] == 12
    both = 3 in c and 5 in c
    if prod and both and c.index(3) < c.index(5):
        worlds[(c[1], c[3])] += 1
    # ловушки
    if prod and both:                               # «номер жетона 3 меньше номера 5» — всегда верно
        traps['3 < 5 как числа'] += 1
    if prod and both and c.index(3) < c.index(5) and (c[1], c[3]) in [(2, 6), (3, 4)]:
        traps['только два мира (2,6),(3,4)'] += 1
N = sum(worlds.values())
print('N =', N)
for w in [(2, 6), (6, 2), (3, 4), (4, 3)]:
    print(f'N{w} =', worlds[w])
print('все пары (c2, c4):', sorted(worlds))
two = N + worlds[(2, 6)] + worlds[(6, 2)]   # пара 3, 5 двумя порядками удваивает миры (2,6), (6,2)
print('ловушки:', {'3 < 5 как числа': traps['3 < 5 как числа'],
                   'два порядка у 3 и 5 в мирах (2,6),(6,2)': two,
                   'только два мира (2,6),(3,4)': traps['только два мира (2,6),(3,4)']})
