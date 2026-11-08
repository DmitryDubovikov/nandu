# T3p-70-2: план парка 6 столбцов × 6 строк, пруд в столбцах 2 и 3, строки 4 и 5; Лиза идёт из S = (1, 1) в F = (6, 6),
# ход — в соседнюю по стороне клетку, в пруд нельзя, длина прогулки — число ходов.
# а) наименьшая длина; б) сколько прогулок такой длины.
# Перебор напрямую по условию: обход в ширину (а), затем все прогулки с этим числом ходов в любых направлениях (б).
from collections import deque
from math import comb

W, H = 6, 6
prud = {(2, 4), (3, 4), (2, 5), (3, 5)}
S, F = (1, 1), (6, 6)
kletki = {(x, y) for x in range(1, W + 1) for y in range(1, H + 1)} - prud


def sosedi(p):
    x, y = p
    for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if q in kletki:
            yield q


dist = {S: 0}
dq = deque([S])
while dq:
    p = dq.popleft()
    for q in sosedi(p):
        if q not in dist:
            dist[q] = dist[p] + 1
            dq.append(q)
L = dist[F]
print('а) наименьшая длина (ходов):', L)

# все прогулки ровно из L ходов (любые направления, клетки могут повторяться) от S до F
progulki = []


def go(p, put):
    if len(put) - 1 == L:
        if p == F:
            progulki.append(tuple(put))
        return
    for q in sosedi(p):
        go(q, put + [q])


go(S, [S])
print('б) прогулок из', L, 'ходов:', len(progulki))


def podnyalas(put, iz):
    return any(put[i] == iz and put[i + 1] == (iz[0], iz[1] + 1) for i in range(len(put) - 1))


miry = ((4, 3), (5, 3), (6, 3), (1, 5))
for iz in miry:
    print(f'N(вверх из {iz}) =', sum(podnyalas(pt, iz) for pt in progulki))
print('прогулок ровно в одном мире:', sum(sum(podnyalas(pt, iz) for iz in miry) == 1 for pt in progulki))

print('ловушка: на целом квадрате C(10, 5) =', comb(10, 5), ', через пруд', comb(10, 5) - len(progulki))
print('ловушка: после подъёма из (1, 3) считать до F как C(7, 2):', 60 + 45 + 21 + 1 * comb(7, 2))
print('ловушка: забыть мир вдоль левого и верхнего края:', len(progulki) - 1)
