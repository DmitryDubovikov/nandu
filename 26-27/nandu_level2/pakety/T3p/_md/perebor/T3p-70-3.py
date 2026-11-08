# T3p-70-3: аквариум из трёх отсеков, в ряд двенадцать домиков: 3 в отсеке 1, 4 в отсеке 2, 5 в отсеке 3.
# Пять одинаковых сомиков, в домике не больше одного; в каждом отсеке хотя бы один сомик.
from itertools import combinations

K = 5
otsek = [1] * 3 + [2] * 4 + [3] * 5          # отсек каждого домика
vse = list(combinations(range(12), K))       # расселение = какие пять домиков заняты

def pustye(r):
    return {1, 2, 3} - {otsek[i] for i in r}

N = sum(1 for r in vse if not pustye(r))
print('N =', N)
print('N(всех) =', len(vse))
n1 = {s: sum(1 for r in vse if s in pustye(r)) for s in (1, 2, 3)}
for s in (1, 2, 3):
    print(f'N(пустой {s}) =', n1[s])
n2 = {(a, b): sum(1 for r in vse if {a, b} <= pustye(r)) for a, b in ((1, 2), (1, 3), (2, 3))}
for (a, b), v in n2.items():
    print(f'N(пустые {a} и {b}) =', v)
# составы (сколько сомиков в отсеках 1, 2, 3) — для сравнения с прямым счётом
from collections import Counter
sost = Counter(tuple(sum(1 for i in r if otsek[i] == s) for s in (1, 2, 3)) for r in vse if not pustye(r))
print('составы:', dict(sorted(sost.items())))
# ловушки
print('ничего не вернуть:', len(vse) - sum(n1.values()))
d = [[i for i in range(12) if otsek[i] == s] for s in (1, 2, 3)]
print('по одному в отсек, потом два в любые свободные:',
      sum(1 for x in d[0] for y in d[1] for z in d[2]
          for w in combinations([i for i in range(12) if i not in (x, y, z)], 2)))
