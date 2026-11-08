# E11: пять фонарей на перекрёстке двух аллей (l, x, r — горизонтальная, t, x, b — вертикальная),
# номера 1–6 без повторов, произведение номеров горизонтальной аллеи = произведению вертикальной.
from itertools import permutations
from collections import Counter

good = [(l, r, t, b, x) for l, r, t, b, x in permutations(range(1, 7), 5)
        if l * x * r == t * x * b]
print('перебрано нумераций:', len(list(permutations(range(1, 7), 5))))
print('ОТВЕТ N =', len(good))
print('по мирам (общее произведение l·r):', dict(sorted(Counter(l * r for l, r, t, b, x in good).items())))
print('номера в x в мире 6:', sorted({x for l, r, t, b, x in good if l * r == 6}))
print('номера в x в мире 12:', sorted({x for l, r, t, b, x in good if l * r == 12}))
# ловушки
print('аллеи не различать:', len({(frozenset([(l, r), (t, b)]), x) for l, r, t, b, x in good}))
print('не переставлять внутри пар:', len({(frozenset([l, r]), frozenset([t, b]), x) for l, r, t, b, x in good}))
print('без мира 6:', sum(1 for l, r, t, b, x in good if l * r != 6))
