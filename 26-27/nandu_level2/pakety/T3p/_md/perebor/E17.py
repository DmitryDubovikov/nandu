# E17 (глава 15 «Предметы двух видов ⇒ миры по числу предметов одного вида»):
# ряд из восьми клеток закрыт половинками (1 клетка) и целыми кирпичами (2 клетки подряд).
# Способ — порядок кирпичей слева направо.
from collections import Counter


def rows(n):
    if n == 0:
        yield ()
        return
    for step in (1, 2):
        if step <= n:
            for rest in rows(n - step):
                yield (step,) + rest


allrows = list(rows(8))
print('N =', len(allrows))
print('по числу целых:', sorted(Counter(r.count(2) for r in allrows).items()))
print('ловушка «два места из восьми клеток»: C(8, 2) =', 8 * 7 // 2)
