# E12: план квартала 5 столбцов × 6 строк, стройка в столбце 3, строки 2 и 3; курьер идёт из S = (1, 1) в D = (5, 6),
# ход — в соседнюю по стороне клетку, на стройку нельзя. а) наименьшее число ходов; б) сколько путей с ним.
# Перебор напрямую по условию: обход в ширину (а), затем все пути с этим числом ходов в любых направлениях (б).
from collections import deque
from math import comb

W, H = 5, 6
stroika = {(3, 2), (3, 3)}
S, D = (1, 1), (5, 6)
kletki = {(x, y) for x in range(1, W + 1) for y in range(1, H + 1)} - stroika

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
L = dist[D]
print('а) наименьшее число ходов:', L)

# все пути ровно из L ходов (любые направления, клетки могут повторяться) от S до D
puti = []
def go(p, put):
    if len(put) - 1 == L:
        if p == D:
            puti.append(tuple(put))
        return
    for q in sosedi(p):
        go(q, put + [q])
go(S, [S])
print('б) путей из', L, 'ходов:', len(puti))

def podnyalsya(put, iz):
    return any(put[i] == iz and put[i + 1] == (iz[0], iz[1] + 1) for i in range(len(put) - 1))

for iz in ((1, 3), (2, 3), (4, 1), (5, 1)):
    print(f'N(вверх из {iz}) =', sum(podnyalsya(pt, iz) for pt in puti))
v_mirah = sum(sum(podnyalsya(pt, iz) for iz in ((1, 3), (2, 3), (4, 1), (5, 1))) == 1 for pt in puti)
print('путей ровно в одном мире:', v_mirah)
print('ловушка: на целом прямоугольнике C(9, 4) =', comb(9, 4), ', через стройку', comb(9, 4) - len(puti))
print('ловушка: C(n, k) сразу после подъёма из строки 1 в столбцах 1, 2:', 1 * comb(8, 4) + 1 * comb(7, 3) + 5 + 1)
