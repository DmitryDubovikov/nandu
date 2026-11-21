# T3p-O-9: коридор из 11 плиток, короткий рывок на 1 плитку, длинный рывок на 4 плитки.
from collections import Counter


def ways(n):
    if n == 0:
        yield ()
        return
    for step in (1, 4):
        if step <= n:
            for rest in ways(n - step):
                yield (step,) + rest


w = list(ways(11))
print('N =', len(w))
print('по числу длинных:', sorted(Counter(r.count(4) for r in w).items()))
