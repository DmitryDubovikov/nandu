# R2: жук, 3 хода вправо и 2 вверх. Перебор всех слов из П и В длины 5, которые приводят из S в D.
from itertools import product
ws = sorted(''.join(w) for w in product('ВП', repeat=5) if w.count('П') == 3 and w.count('В') == 2)
book = "ВВППП ВПВПП ВППВП ВПППВ ПВВПП ПВПВП ПВППВ ППВВП ППВПВ ПППВВ".split()
assert ws == book, ws
assert [sum(1 for w in ws if w.index('В') == k) for k in range(4)] == [4, 3, 2, 1]
print("N =", len(ws)); assert len(ws) == 10
