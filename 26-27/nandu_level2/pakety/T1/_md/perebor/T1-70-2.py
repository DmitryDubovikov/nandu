"""Перебор для T1-70-2 (книжный шкаф).

f, e, x, t — сказки, энциклопедии, комиксы, учебники; все неотрицательные целые.
Условия:
  всего 336 книг;
  без всех комиксов остаётся 286;
  без половины энциклопедий остаётся 291 (половина целая);
  без всех учебников остаётся 3/4 того, что осталось бы без всех сказок.
"""

TOTAL = 336
found = []
for f in range(TOTAL + 1):
    for e in range(TOTAL + 1 - f):
        for x in range(TOTAL + 1 - f - e):
            t = TOTAL - f - e - x
            if f + e + t != 286:
                continue
            if e % 2 != 0 or f + e // 2 + x + t != 291:
                continue
            if 4 * (f + e + x) != 3 * (e + x + t):
                continue
            found.append((f, e, x, t))

for s in found:
    print("f = %d, e = %d, x = %d, t = %d" % s)
print("решений:", len(found))
