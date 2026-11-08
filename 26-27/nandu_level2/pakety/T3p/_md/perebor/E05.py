# E05: кодовый замок, четыре колёсика с цифрами 1–6, повторы можно,
# сумма делится на 3, чётных цифр не больше одной. Перебор всех 6^4 кодов прямо по условию.
from itertools import product

codes = [c for c in product(range(1, 7), repeat=4)
         if sum(c) % 3 == 0 and sum(1 for d in c if d % 2 == 0) <= 1]
print('N =', len(codes))
w0 = [c for c in codes if all(d % 2 for d in c)]
w1 = [c for c in codes if sum(1 for d in c if d % 2 == 0) == 1]
print('N(нет чётных) =', len(w0), ' N(одна чётная) =', len(w1))
# по месту чётной цифры
for i in range(4):
    print(f'  чётная в c{i+1}:', sum(1 for c in w1 if c[i] % 2 == 0))
# свойство: при любых c1, c2, c3 число вариантов c4
from collections import Counter
cnt = Counter()
for c in product(range(1, 7), repeat=3):
    ev = sum(1 for d in c if d % 2 == 0)
    if ev > 1: continue
    k = sum(1 for d in range(1, 7) if (sum(c) + d) % 3 == 0 and ev + (d % 2 == 0) <= 1)
    cnt[(ev, k)] += 1
print('варианты c4 по (чётных в c1..c3, вариантов c4):', dict(cnt))
# ловушки
print('ровно одна чётная:', len(w1))
print('без выбора места чётной: 27 + 27 =', len(w0) + 27)
ms = {tuple(sorted(c)) for c in codes}
print('наборы цифр вместо кодов:', len(ms))
