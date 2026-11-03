"""T1-O-2, садовый магазин: пакеты семян.

b — пакетик свёклы, p — тыквы, d — укропа, r — редиса (цены, целые, $1..$200).
Пакет 1: 3b + 2p + 1d + 2r = 310
Пакет 2: 1b + 2p + 3d + 1r = 250
Пакет 3: 2b + 3p + 2d + 1r = 320
Пакет 4: 2b + 1p + 2d + 2r = x (спрошено)
"""
from collections import Counter

PACKS = [((3, 2, 1, 2), 310), ((1, 2, 3, 1), 250), ((2, 3, 2, 1), 320)]
ASKED = (2, 1, 2, 2)
LIMIT = 200


def dot(a, v):
    return sum(i * j for i, j in zip(a, v))


sols = []
for b in range(1, LIMIT + 1):
    for p in range(1, LIMIT + 1):
        for d in range(1, LIMIT + 1):
            # r из пакета 1 (коэффициент 2)
            rest = 310 - (3 * b + 2 * p + d)
            if rest <= 0 or rest % 2:
                continue
            r = rest // 2
            v = (b, p, d, r)
            if all(dot(c, v) == t for c, t in PACKS):
                sols.append(v)

print(f"Решений в целых положительных ценах до ${LIMIT}: {len(sols)}")
for v in sols:
    print("  (b, p, d, r) =", v, " пакет 4 =", dot(ASKED, v))
print("Значения цены пакета 4:", Counter(dot(ASKED, v) for v in sols))
print("Каждая цена по отдельности определена?",
      {name: len({v[i] for v in sols}) == 1 for i, name in enumerate("bpdr")})
# комбинация (1) + (2) − (3)
comb = tuple(PACKS[0][0][i] + PACKS[1][0][i] - PACKS[2][0][i] for i in range(4))
print("(1) + (2) − (3): коэффициенты", comb, "= пакет 4?", comb == ASKED,
      " сумма", PACKS[0][1] + PACKS[1][1] - PACKS[2][1])
