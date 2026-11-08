# E08: стеллаж, полки из 2, 3, 4 ячеек; четыре одинаковые коробки, на каждой полке хотя бы одна.
from itertools import combinations

polka = [1, 1, 2, 2, 2, 3, 3, 3, 3]          # номер полки каждой из девяти ячеек
vse = list(combinations(range(9), 4))
def pustye(r):
    return {p for p in (1, 2, 3) if all(polka[i] != p for i in r)}

good = [r for r in vse if not pustye(r)]
print('N(всех) =', len(vse))
for p in (1, 2, 3):
    print(f'N(пустая {p}) =', sum(p in pustye(r) for r in vse))
for a, b in ((1, 2), (1, 3), (2, 3)):
    print(f'N(пустые {a} и {b}) =', sum({a, b} <= pustye(r) for r in vse))
print('ОТВЕТ N =', len(good))
print('без возврата пересечения было бы', len(vse) - sum(len(pustye(r)) for r in vse if pustye(r)) )
