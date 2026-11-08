# E13: окно 4 ряда × 5 стёкол (вертикали 0..5, горизонтали 0..4), трещина — отрезок от (0, 0) до (4, 4).
# Считаем прямоугольники со сторонами на линиях решётки, у которых нет ни одной общей точки с трещиной.
from fractions import Fraction as F
from itertools import combinations

V, H = range(6), range(5)

def obshchaya_tochka(v1, v2, h1, h2, strogo=False):
    """Есть ли точка (t, t), 0 <= t <= 4, внутри или на границе прямоугольника [v1, v2] × [h1, h2].
    strogo=True — считать только точки внутри (касание границей не в счёт)."""
    # перебираем t с шагом 1/2 — для отрезков с концами в целых точках этого достаточно
    for k in range(0, 4 * 2 + 1):
        t = F(k, 2)
        if strogo:
            if v1 < t < v2 and h1 < t < h2: return True
        else:
            if v1 <= t <= v2 and h1 <= t <= h2: return True
    return False

vse = [(v1, v2, h1, h2) for v1, v2 in combinations(V, 2) for h1, h2 in combinations(H, 2)]
good = [r for r in vse if not obshchaya_tochka(*r)]
print('всех прямоугольников:', len(vse))
print('N(v₂ < h₁) =', sum(r[1] < r[2] for r in good))
print('N(h₂ < v₁) =', sum(r[3] < r[0] for r in good))
print('ОТВЕТ N =', len(good))
print('прочие:', [r for r in good if not (r[1] < r[2] or r[3] < r[0])])
# ловушки
ugol = [r for r in vse if not obshchaya_tochka(*r, strogo=False) or
        (obshchaya_tochka(*r) and not any((r[0] < F(k, 2) < r[1] or r[2] < F(k, 2) < r[3]) and r[0] <= F(k, 2) <= r[1] and r[2] <= F(k, 2) <= r[3] for k in range(9)))]
print('касание только углом допустимо (ловушка 1):', len(ugol))
print('ниже трещины без правого столбца, т. е. v₂ <= 4 (ловушка 2):', sum(r[1] < r[2] for r in good) + sum(r[3] < r[0] and r[1] <= 4 for r in good))
print('без квадратов (ловушка 3):', sum((r[1] - r[0]) != (r[3] - r[2]) for r in good))
