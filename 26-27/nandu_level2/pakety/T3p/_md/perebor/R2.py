# R2: восемь книг трёх серий на полке; перебор всех 8! расстановок прямо по условию.
# Проверяет: наблюдение «синий блок стоит в середине» верно для каждой подходящей расстановки;
# четыре выписанные расстановки подходят, неподходящая — нет; сумма операндов первой формулы равна N.
from itertools import permutations

books = [("ж", "А"), ("ж", "В"), ("ж", "Б"),
         ("з", "Г"), ("з", "Д"), ("з", "Е"),
         ("с", "Б"), ("с", "Г")]

def together(row, k):
    for v in {b[k] for b in row}:
        pos = [i for i, b in enumerate(row) if b[k] == v]
        if pos[-1] - pos[0] + 1 != len(pos):
            return False
    return True

def ok(row):
    return together(row, 0) and together(row, 1)

def blue_middle(row):
    pos = [i for i, b in enumerate(row) if b[0] == "с"]
    return pos[0] > 0 and pos[-1] < len(row) - 1

good = [p for p in permutations(books) if ok(p)]
N = len(good)
assert all(blue_middle(p) for p in good), "наблюдение ложно"
w_yel = sum(1 for p in good if p[0][0] == "ж")
w_grn = sum(1 for p in good if p[0][0] == "з")
assert w_yel + w_grn == N

def mk(s):
    return tuple((s[2 * i], s[2 * i + 1]) for i in range(8))
examples = ["жАжВжБсБсГзГзДзЕ", "жВжАжБсБсГзГзЕзД", "зЕзДзГсГсБжБжАжВ", "зДзЕзГсГсБжБжВжА"]
for e in examples:
    assert ok(mk(e)), e
assert len(set(examples)) == len(examples)
bad = "жАжВжБзГзДзЕсБсГ"
assert not ok(mk(bad)) and together(mk(bad), 0) and not together(mk(bad), 1)

print("N =", N)
print("N(жёлтый слева) =", w_yel, " N(зелёный слева) =", w_grn)
print("наблюдение «синий блок в середине» верно для всех", N, "расстановок")
print("четыре примера подходят, неподходящий нарушает только «одна буква рядом»")
