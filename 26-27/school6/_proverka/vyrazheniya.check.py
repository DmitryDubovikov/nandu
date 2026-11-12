"""Проверка пары 7 «Буквенные выражения и координаты» (учебник + решебник, копии в этом каталоге).
Тождества — подстановкой нескольких значений (Fraction), таблицы — по формулам,
ASCII-графики — разбором звёздочек из самих файлов."""
import itertools
import os
import re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # md пары лежат на уровень выше
UCH = open(os.path.join(HERE, "math6_7_vyrazheniya_koordinaty_uchebnik.md"), encoding="utf-8").read()
RESH = open(os.path.join(HERE, "math6_7_vyrazheniya_koordinaty_reshebnik.md"), encoding="utf-8").read()

VALS = [F(-7, 2), F(-3), F(-1), F(0), F(1, 3), F(1), F(3, 2), F(2), F(5), F(11)]
n_checks = 0


def ident(name, lhs, rhs, nvars=1):
    """lhs == rhs при всех наборах значений."""
    global n_checks
    for args in itertools.product(VALS, repeat=nvars):
        assert lhs(*args) == rhs(*args), (name, args, lhs(*args), rhs(*args))
    n_checks += 1


def not_ident(name, lhs, rhs, nvars=1):
    global n_checks
    assert any(lhs(*a) != rhs(*a) for a in itertools.product(VALS, repeat=nvars)), name
    n_checks += 1


def eq(name, a, b):
    global n_checks
    assert a == b, (name, a, b)
    n_checks += 1


# ---------- УЧЕБНИК, часть A ----------
# ритуалы
ident("ритуал 2/3", lambda x: 12 - (5 * x - 3), lambda x: 15 - 5 * x)
eq("ритуал 2 числа", (12 - (5 - 3), 12 - 5 + 3, 12 - 5 - 3), (10, 10, 4))
eq("ритуал 3 x=2", (12 - (10 - 3), 15 - 10), (5, 5))
# глава 1
eq("гл1 плюс", (100 + (30 + 20), 100 + 30 + 20, 100 + (30 - 20), 100 + 30 - 20), (150, 150, 110, 110))
eq("гл1 минус", (100 - (50 - 20), 100 - 50 - 20, 100 - 50 + 20, 100 - (50 + 20)), (70, 30, 70, 30))
ident("a+(b-c)", lambda a, b, c: a + (b - c), lambda a, b, c: a + b - c, 3)
ident("a-(b-c)", lambda a, b, c: a - (b - c), lambda a, b, c: a - b + c, 3)
ident("-(m-n+5)", lambda m, n: -(m - n + 5), lambda m, n: -m + n - 5, 2)
eq("3(10+4)", (3 * (10 + 4), 3 * 10 + 3 * 4), (42, 42))
ident("3(x+4)", lambda x: 3 * (x + 4), lambda x: 3 * x + 12)
ident("-2(3x-5)", lambda x: -2 * (3 * x - 5), lambda x: -6 * x + 10)
eq("-2(3x-5) x=1", (-2 * (3 - 5), -6 + 10), (4, 4))
ident("-(3x-5)", lambda x: -(3 * x - 5), lambda x: -3 * x + 5)
ident("гл1 разбор А", lambda a, b: 20 - (a + 6) - (4 - b), lambda a, b: 10 - a + b, 2)
eq("гл1 разбор А проверка", (20 - (1 + 6) - (4 - 2), 10 - 1 + 2), (11, 11))
ident("гл1 разбор Б", lambda x: x - 50 + (50 - 12), lambda x: x - 12)
not_ident("гл1 ошибка 1", lambda x: 12 - (5 * x - 3), lambda x: 12 - 5 * x - 3)
eq("гл1 ошибка 1 x=2", (12 - (5 * 2 - 3), 12 - 5 * 2 - 3), (5, -1))
eq("гл1 ошибка 2 x=1", (3 * (1 + 4), 3 * 1 + 4), (15, 7))
# глава 2
ident("m/4", lambda m: m / 4, lambda m: F(1, 4) * m)
eq("m=8", (F(8) / 4, F(1, 4) * 8), (2, 2))
ident("-2·5a·(-3)", lambda a: -2 * 5 * a * (-3), lambda a: 30 * a)
ident("гл2 разбор", lambda x: F(1, 2) * (-8 * x) * 3, lambda x: -12 * x)
eq("гл2 разбор x=2", (F(1, 2) * (-16) * 3, -12 * 2), (-24, -24))
for a in (1, 2, 3, 10):
    eq("гл2 таблица 2a/6a", (6 * a) / F(2 * a), 3)
eq("гл2 a=-1", (6 * -1, 2 * -1, 6 * -1 < 2 * -1), (-6, -2, True))
# глава 3
for x, s in zip((1, 2, 3, 10), (12, 24, 36, 120)):
    eq("гл3 таблица", (7 * x + 5 * x, 12 * x), (s, s))
ident("7x+5x", lambda x: 7 * x + 5 * x, lambda x: 12 * x)
ident("4a-9a", lambda a: 4 * a - 9 * a, lambda a: -5 * a)
eq("4a-9a a=2", (8 - 18, -5 * 2), (-10, -10))
ident("гл3 разбор А", lambda a, b: 8 * a - 3 * b - 5 * a + 7 * b - 2, lambda a, b: 3 * a + 4 * b - 2, 2)
eq("гл3 разбор А проверка a=2 b=1", (16 - 3 - 10 + 7 - 2, 6 + 4 - 2), (8, 8))
ident("гл3 разбор Б", lambda x: 5 * (x - 2) - 3 * (x - 4), lambda x: 2 * x + 2)
x = F(3, 2)
eq("гл3 разбор Б значение", (5 * (x - 2) - 3 * (x - 4), 2 * x + 2, 5 * (x - 2), -3 * (x - 4)), (5, 5, F(-5, 2), F(15, 2)))
eq("гл3 ошибка 1", (3 * 1 + 4, 7 * 1, 3 * 2 + 4, 7 * 2), (7, 7, 10, 14))
ident("гл3 ошибка 3 (буква n)", lambda m: 3 * m + 8 - 7 * m + 2, lambda m: -4 * m + 10)

# ---------- УЧЕБНИК, часть B ----------
def quadrant(p):
    x, y = p
    if x == 0 or y == 0:
        return "ось"
    return {(True, True): "I", (False, True): "II", (False, False): "III", (True, False): "IV"}[(x > 0, y > 0)]


eq("четверти таблица", [quadrant(p) for p in [(3, 5), (-3, 5), (-3, -5), (3, -5)]], ["I", "II", "III", "IV"])
eq("M(-7;3)", quadrant((-7, 3)), "II")
eq("T", (quadrant((F(-3, 2), F(-1, 2))), abs(F(-1, 2))), ("III", F(1, 2)))
eq("гл4 разбор А", (3 - (-5), F(-5 + 3, 2), -1 - (-5), 3 - (-1)), (8, -1, 4, 4))
eq("гл4 вертикальный", 3 - (-1), 4)
ox = lambda p: (p[0], -p[1])
oy = lambda p: (-p[0], p[1])
o = lambda p: (-p[0], -p[1])
sh = lambda p, a, b: (p[0] + a, p[1] + b)
eq("гл4 симметрии", (ox((3, 5)), oy((3, 5))), ((3, -5), (-3, 5)))
P = (3, -2)
eq("гл5 таблица", (ox(P), oy(P), o(P), sh(P, 4, 5), sh(P, -4, -2)), ((3, 2), (-3, -2), (-3, 2), (7, 3), (-1, -4)))
eq("гл5 O = Ox∘Oy", o(P), oy(ox(P)))
M, N = (-2, 1), (3, 1)
eq("гл5 разбор", (sh(M, 5, -2), sh(N, 5, -2), N[0] - M[0], 8 - 3), ((3, -1), (8, -1), 5, 5))
# глава 6: свеча
candle = lambda t: 20 - 2 * t
eq("свеча таблица", [candle(t) for t in (0, 2, 4, 6, 8, 10)], [20, 16, 12, 8, 4, 0])
eq("свеча разбор", (candle(3), F(20 - 10, 2), F(20, 2)), (14, 5, 10))
# глава 7
eq("y=2x", [2 * x for x in range(-3, 4)], [-6, -4, -2, 0, 2, 4, 6])
xs = [-6, -3, -2, -1, 1, 2, 3, 6]
eq("y=6:x", [F(6, x) for x in xs], [-1, -2, -3, -6, 6, 3, 2, 1])
eq("6:0,5", F(6) / F(1, 2), 12)
eq("блокноты", (F(270, 6), [45 * x for x in (1, 2, 4, 8)]), (45, [45, 90, 180, 360]))
eq("конфеты", [F(36, x) for x in (2, 3, 4, 6, 9, 12)], [18, 12, 9, 6, 4, 3])
eq("гл7 ошибка 3", [x * (12 - x) for x in (1, 2, 3)], [11, 20, 27])
eq("гл7 ошибка 1", 2 * 0 + 3, 3)


# ---------- ASCII-графики: звёздочки из файлов ----------
def blocks(text):
    return re.findall(r"```\n(.*?)```", text, flags=re.S)


def points(block, unit, step_rows=None):
    """Точки (x, y) по символам * и буквам A–D; unit — знакомест на единицу x.
    Строка с числовой меткой задаёт y; строки без метки — на step_rows ниже предыдущей."""
    lines = block.split("\n")
    lab = next(l for l in lines if re.search(r"\bO\b", l))
    x0 = lab.index("O")
    pts, y = {}, None
    for l in lines:
        if l is lab:
            continue
        m = re.match(r"\s*(-?\d+)", l[:x0])
        if m:
            y = int(m.group(1))
        elif y is not None and step_rows:
            y -= step_rows
        else:
            continue
        for i, ch in enumerate(l):
            if i >= x0 - 30 and (ch in "*·" or (ch in "ABCD" and i > 3)):
                assert (i - x0) % unit == 0, (l, i)
                pts.setdefault(ch, set()).add(((i - x0) // unit, y))
    return pts


ub = blocks(UCH)
eq("число рисунков учебника", len(ub), 4)
p = points(ub[0], 3)
eq("рисунок точек", (p["A"], p["B"], p["C"], p["D"]), ({(3, 5)}, {(5, 3)}, {(-4, 2)}, {(-3, -4)}))
p = points(ub[1], 3, step_rows=2)
eq("свеча звёздочки", p["*"], {(t, candle(t)) for t in (0, 2, 4, 6, 8, 10)})
eq("свеча линия", p["·"], {(t, candle(t)) for t in (1, 3, 5, 7, 9)})
p = points(ub[2], 3)
eq("график y=2x", p["*"], {(x, 2 * x) for x in range(-3, 4)})
p = points(ub[3], 3)
eq("график y=6:x", p["*"], {(x, 6 // x) for x in xs})

rb = blocks(RESH)
eq("число рисунков решебника", len(rb), 1)
p = points(rb[0], 3)
temp = {0: -4, 2: -3, 4: -1, 6: 0, 8: 2, 10: 4, 12: 5}
eq("6.2 график", p["*"], set(temp.items()))

# ---------- РЕШЕБНИК ----------
ident("1.1а", lambda x: 8 + (x - 3), lambda x: x + 5)
ident("1.1б", lambda x: 10 - (x + 6), lambda x: 4 - x)
ident("1.1в", lambda y: -(4 - y) + 9, lambda y: y + 5)
ident("1.2а", lambda a, b: -(a - b + 7), lambda a, b: -a + b - 7, 2)
ident("1.2б", lambda c: 2 - (-3 + c) - 5, lambda c: -c)
ident("1.2в", lambda m: (m - 4) - (m + 4), lambda m: F(-8))
ident("1.3 склад", lambda m: 90 - (m - 7) + 12, lambda m: 109 - m)
eq("1.3 m=30", (109 - 30, 30 - 7, 90 - 23, 67 + 12), (79, 23, 67, 79))
ident("2.1 a/5", lambda a: a / 5, lambda a: F(1, 5) * a)
ident("2.2а", lambda a: 2 * 3 * a, lambda a: 6 * a)
ident("2.2б", lambda x: -5 * (-4 * x), lambda x: 20 * x)
ident("2.2в", lambda a: -a * 7, lambda a: -7 * a)
ident("2.2г", lambda y: F(1, 2) * (-6 * y), lambda y: -3 * y)
ident("2.3", lambda a: 4 * (2 * a), lambda a: 8 * a)
eq("2.3 отношение", F(8, 4), 2)
ident("3.1а", lambda x: 6 * x + 9 * x - 4 * x, lambda x: 11 * x)
ident("3.1б", lambda a: 5 * a - 12 * a, lambda a: -7 * a)
ident("3.1в", lambda m: 2 * m + 7 - 5 * m + 1, lambda m: -3 * m + 8)
ident("3.2а", lambda x, y: 3 * x + 2 * y - x + 5 * y, lambda x, y: 2 * x + 7 * y, 2)
ident("3.2б", lambda a: 6 * a - (2 * a - 5), lambda a: 4 * a + 5)
ident("3.2в", lambda b: 5 * b + 3 - (b + 3), lambda b: 4 * b)
ident("3.3", lambda x: x + (x + 6) + 2 * x, lambda x: 4 * x + 6)
eq("3.3 x=9", (4 * 9 + 6, 9 + 15 + 18), (42, 42))
pts = dict(A=(2, 6), B=(6, 2), C=(-5, 3), D=(-4, -4), E=(0, -3), F=(4, 0))
eq("4.1", [quadrant(pts[k]) for k in "ABCDEF"], ["I", "I", "II", "III", "ось", "ось"])
Np = (-6, 5)
eq("4.2", (ox(Np), quadrant(ox(Np)), oy(Np), quadrant(oy(Np)), quadrant(Np)), ((-6, -5), "III", (6, 5), "I", "II"))
A, B, C = (-2, 1), (4, 1), (4, -3)
D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
eq("4.3", (D, B[0] - A[0], B[1] - C[1], (B[0] - A[0]) * (B[1] - C[1])), ((-2, -3), 6, 4, 24))
eq("5.1", (o((4, -3)), sh((4, -3), -6, 2)), ((-4, 3), (-2, -1)))
M, M1, N = (-4, 3), (1, -2), (2, 3)
d = (M1[0] - M[0], M1[1] - M[1])
eq("5.2", (d, sh(N, *d)), ((5, -5), (7, -2)))
tri = [(1, 2), (5, 2), (1, 5)]
eq("5.3", ([o(q) for q in tri], 5 - 1, -1 - (-5)), ([(-1, -2), (-5, -2), (-1, -5)], 4, 4))
eq("5.3 два отражения", [oy(ox(q)) for q in tri], [o(q) for q in tri])
eq("6.1 таблица", [5 * t for t in range(5)], [0, 5, 10, 15, 20])
eq("6.1", (5 * F(5, 2), F(30, 5)), (F(25, 2), 6))
eq("6.2", (temp[6], [t for t, v in temp.items() if v == -1], temp[12] - temp[0]), (0, [4], 9))
taxi = lambda km: 100 + 20 * km
eq("6.3", ([taxi(k) for k in (0, 1, 2, 5)], taxi(8), F(240 - 100, 20), taxi(2), taxi(4), F(140, 2), F(180, 4)),
   ([100, 120, 140, 200], 260, 7, 140, 180, 70, 45))
eq("7.1", ([3 * x for x in (-2, -1, 0, 1, 2)], 3 * 4, F(-9, 3)), ([-6, -3, 0, 3, 6], 12, -3))
eq("7.2", [F(12, a) for a in (1, 2, 3, 4, 6, 12)], [12, 6, 4, 3, 2, 1])
sq = [(s, s * s) for s in (1, 2, 3)]
eq("7.3в", ([b for a, b in sq], [F(b, a) for a, b in sq], [a * b for a, b in sq]), ([1, 4, 9], [1, 2, 3], [1, 8, 27]))
eq("7.3а,б", (len({F(30 * n, n) for n in range(1, 9)}), len({p * F(60, p) for p in (1, 2, 3, 4, 5, 6, 10)})), (1, 1))

# ---------- состав задач и непересечение с учебником ----------
for s in ("`90` мешков", "за `240` рублей", "со скоростью `30` км/ч", "109 − m", "`s = 30t`"):
    assert s in RESH, s
for s in ("турист", "пирожн", "за `200` рублей"):
    assert s not in RESH, s
for s in ("мешк", "складе", "мопед", "грузовик"):
    assert s not in UCH, s
assert "3n + 8 − 7n + 2" in UCH and "3m + 8" not in UCH
assert UCH.count("Ответ на задачу:") == 6 and "Шаг 5 — сборка.**\n\n**Ответ" not in UCH and UCH.count("План готов") == 9
n_checks += 5

print(f"OK: {n_checks} проверок прошло")
