# E10: пять скворечников в ряд; жёлтых 1 или 2, голубых 1 или 2, фиолетовых 2 или 3; можно оставить непокрашенным.
from itertools import product

vse = list(product('ЖГФ-', repeat=5))       # '-' = непокрашенный
good = [r for r in vse if r.count('Ж') in (1, 2) and r.count('Г') in (1, 2) and r.count('Ф') in (2, 3)]
print('перебрано раскрасок:', len(vse))
print('N(непокрашенный скворечник) =', sum('-' in r for r in good))
print('N(два жёлтых) =', sum(r.count('Ж') == 2 for r in good))
print('N(два голубых) =', sum(r.count('Г') == 2 for r in good))
print('N(три фиолетовых) =', sum(r.count('Ф') == 3 for r in good))
print('ОТВЕТ N =', len(good))
print('без непокрашенных (ловушка 1):', sum('-' not in r for r in good))
