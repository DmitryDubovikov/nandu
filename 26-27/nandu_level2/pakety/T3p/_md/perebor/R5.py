# R5: восемь книг трёх серий; перебор всех 8! расстановок по условию.
from itertools import permutations
books = [("ж", "А"), ("ж", "В"), ("ж", "Б"), ("з", "Г"), ("з", "Д"), ("з", "Е"), ("с", "Б"), ("с", "Г")]
def together(row, k):
    for v in {b[k] for b in row}:
        pos = [i for i, b in enumerate(row) if b[k] == v]
        if pos[-1] - pos[0] + 1 != len(pos): return False
    return True
good = [p for p in permutations(books) if together(p, 0) and together(p, 1)]
blue = lambda p: [i for i, b in enumerate(p) if b[0] == "с"]
assert all(blue(p)[0] > 0 and blue(p)[-1] < 7 for p in good)          # синий блок в середине
yl = sorted(''.join(b[1] for b in p) for p in good if p[0][0] == "ж")
assert yl == ["АВББГГДЕ", "АВББГГЕД", "ВАББГГДЕ", "ВАББГГЕД"], yl
gl = sorted(''.join(b[1] for b in p)[::-1] for p in good if p[0][0] == "з")
assert gl == yl                                                        # зелёный слева = те же строки справа налево
print("N =", len(good)); assert len(good) == 8
