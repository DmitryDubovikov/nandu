# T3p-50-1: вышивка на салфетке — крестик из пяти кружков (l, x, r — горизонтальная линия,
# t, x, b — вертикальная), цифры 1–6 без повторов, сумма цифр горизонтальной линии = сумме вертикальной.
from itertools import permutations
from collections import Counter

alls = list(permutations(range(1, 7), 5))
good = [(l, r, t, b, x) for l, r, t, b, x in alls if l + x + r == t + x + b]
print('перебрано заполнений:', len(alls))
print('ОТВЕТ N =', len(good))
print('по мирам (общая сумма l + r):', dict(sorted(Counter(l + r for l, r, t, b, x in good).items())))
for s in sorted({l + r for l, r, t, b, x in good}):
    w = [g for g in good if g[0] + g[1] == s]
    print(f'  мир {s}: заполнений l, r, t, b = {len({g[:4] for g in w})}, цифры в x = {sorted({g[4] for g in w})}')
# ловушки
print('линии не различать:', len({(frozenset([(l, r), (t, b)]), x) for l, r, t, b, x in good}))
print('не переставлять внутри пар:', len({(frozenset([l, r]), frozenset([t, b]), x) for l, r, t, b, x in good}))
print('мир 7 считать как 16:', sum(1 for l, r, t, b, x in good if l + r != 7) + 16)
