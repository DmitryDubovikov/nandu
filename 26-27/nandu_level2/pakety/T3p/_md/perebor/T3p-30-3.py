# T3p-30-3: гирлянда из шести фонариков в ряд; каждый горит красным, зелёным или синим;
# красных 1 или 2, зелёных 1 или 2, синих 2, 3 или 4; погасших фонариков нет.
from itertools import product

vse = list(product('КЗС', repeat=6))
good = [r for r in vse if r.count('К') in (1, 2) and r.count('З') in (1, 2) and r.count('С') in (2, 3, 4)]
sostav = lambda r: (r.count('К'), r.count('З'), r.count('С'))
print('перебрано раскрасок:', len(vse))
print('N(две красные и две зелёные) =', sum(sostav(r) == (2, 2, 2) for r in good))
print('N(две красные и три синих) =', sum(sostav(r) == (2, 1, 3) for r in good))
print('N(две зелёные и три синих) =', sum(sostav(r) == (1, 2, 3) for r in good))
print('N(четыре синих) =', sum(sostav(r) == (1, 1, 4) for r in good))
print('другие составы:', sorted({sostav(r) for r in good} - {(2, 2, 2), (2, 1, 3), (1, 2, 3), (1, 1, 4)}))
print('ОТВЕТ N =', len(good))
# ловушка: разрешить фонарику не гореть
vse2 = product('КЗС-', repeat=6)
print('если фонарик может не гореть (ловушка):',
      sum(1 for r in vse2 if r.count('К') in (1, 2) and r.count('З') in (1, 2) and r.count('С') in (2, 3, 4)))
