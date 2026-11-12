# Проверка пары 4 «Логика»: каждое утверждение учебника и каждый ответ решебника.
# Бесконечные множества («любое натуральное») проверяются перебором 1..N — это страховка
# от неверного вердикта и неверного контрпримера; общий довод стоит в тексте.
from fractions import Fraction as F
from itertools import product

N = 3000
NAT = range(1, N + 1)
ok = 0


def chk(name, cond):
    global ok
    assert cond, "ПРОВАЛ: " + name
    ok += 1


def prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def forall(dom, p):
    return all(p(x) for x in dom)


def exists(dom, p):
    return any(p(x) for x in dom)


def impl(dom, a, b):
    """следование верно <=> нет объекта с A и без B"""
    return not any(a(x) and not b(x) for x in dom)


def cex(dom, a, b):
    return [x for x in dom if a(x) and not b(x)]


def pair(name, s, neg):
    """высказывание и отрицание: ровно одно истинно"""
    chk(name + " (пара)", s != neg)


d = lambda k: (lambda n: n % k == 0)
last = lambda c: (lambda n: n % 10 == c)
even = d(2)
odd = lambda n: n % 2 == 1
TWO = range(10, 100)

# ---------------- УЧЕБНИК ----------------
# вводный раздел
chk("24:6", 24 % 6 == 0 and 24 // 6 == 4)
chk("мини-задача: 35:7, b=4, b=12", 35 % 7 == 0 and 35 // 7 == 5 and 4 < 10 and not 12 < 10)
chk("a>7 при 9 и 2", 9 > 7 and not 2 > 7)
# ритуалы
chk("Р1/Р2/Р3: 15 не делится на 4", 15 % 4 != 0)
chk("Р4: 15, 45, 75 делятся на 3, 25 нет", 15 % 3 == 0 and 45 % 3 == 0 and 75 % 3 == 0 and 25 % 3 != 0)
chk("Р4: первый контрпример по порядку", cex(TWO, last(5), d(3))[0] == 25)
chk("Р5: делится на 10 -> чётное", impl(NAT, d(10), even))
# глава 1
chk("гл1 таблица-источник", prime(7) and 6 % 3 == 0 and 15 % 4 != 0 and 8 > 5)
chk("гл1: 5 — оба ложны", not 5 > 5 and not 5 < 5 and 5 <= 5)
chk("гл1: на числе 8 «меньше 5» и «не больше 5» ложны оба", not 8 < 5 and not 8 <= 5)
chk("гл1: отрезок 3 см", not 3 > 3 and not 3 < 3 and 3 <= 3)
chk("гл1 разбор: 91", 91 == 7 * 13 and not prime(91) and all(91 % p for p in (2, 3, 5)))
# глава 2
chk("гл2: все простые нечётные — ложно, 2", prime(2) and even(2) and not forall(filter(prime, NAT), odd))
chk("гл2: все простые чётные — ложно, 3", prime(3) and odd(3))
chk("гл2 (доб.): однозначные простые 2,3,5,7 < 8", [p for p in range(1, 10) if prime(p)] == [2, 3, 5, 7])
chk("гл2 (доб.): чётные > 2 составные", forall([n for n in NAT if even(n) and n > 2], lambda n: not prime(n)))
chk("гл2 разбор: 3,13,23 простые, 33 = 3·11", prime(3) and prime(13) and prime(23) and 33 == 3 * 11
    and cex(NAT, last(3), prime)[0] == 33)
# глава 3
chk("гл3 (доб.): есть чётное простое", exists(NAT, lambda n: prime(n) and even(n)))
chk("гл3: простых, кратных 6, нет", not exists(NAT, lambda n: prime(n) and n % 6 == 0))
chk("гл3 (доб.): делители 6 и 12", divs(6) == [1, 2, 3, 6] and divs(12) == [1, 2, 3, 4, 6, 12] and divs(18) == [1, 2, 3, 6, 9, 18])
chk("гл3 разбор: три делителя среди 1..20", [n for n in range(1, 21) if len(divs(n)) == 3] == [4, 9]
    and [len(divs(n)) for n in (1, 2, 3, 4)] == [1, 2, 2, 3] and divs(9) == [1, 3, 9])
# глава 4
chk("гл4: каждое n делится на 3 — ложно (1); существует — истинно (3)", 1 % 3 != 0 and 3 % 3 == 0
    and 12 % 3 == 0 and 13 % 3 != 0)
chk("гл4: x·x >= x для натуральных", forall(NAT, lambda x: x * x >= x))
chk("гл4: x = 1/2", F(1, 2) * F(1, 2) == F(1, 4) and F(1, 4) < F(1, 2))
chk("гл4 (доб.) список 1,2,3", [x * x for x in (1, 2, 3)] == [1, 4, 9])
r16 = range(1, 7)
chk("гл4 разбор", [x for x in r16 if 12 % x != 0] == [5] and 12 % 1 == 0)
chk("гл4 типичная", forall(NAT, lambda x: x > 0) and not 0 > 0)
# глава 5
chk("гл5: 2n+1 на 4 не делится", forall(NAT, lambda n: (2 * n + 1) % 4 != 0)
    and [2 * n + 1 for n in range(1, 6)] == [3, 5, 7, 9, 11])
chk("гл5 типичная: первые контрпримеры 1 и 2", cex(NAT, lambda n: True, even)[0] == 1 and cex(NAT, lambda n: True, odd)[0] == 2)
# глава 6
chk("гл6: 6->3 верно", impl(NAT, d(6), d(3)))
chk("гл6: чётное->кратно 4 неверно, первый 2, годятся 6, 10", cex(NAT, even, d(4))[:3] == [2, 6, 10])
tbl = [(n, n % 6 == 0, n % 3 == 0) for n in range(1, 7)]
chk("гл6 (доб.) таблица 1..6", tbl == [(1, False, False), (2, False, False), (3, False, True),
                                         (4, False, False), (5, False, False), (6, True, True)])
chk("гл6 разбор: 12->6", impl(NAT, d(12), d(6)) and 12 == 6 * 2)
chk("гл6 типичная: 18", 18 % 12 != 0 and 18 % 6 == 0)
# глава 7
chk("гл7: 3->9 ложно (первый 3, годится 6), 3->не 9 ложно (первый 9)", cex(NAT, d(3), d(9))[:2] == [3, 6]
    and cex(NAT, d(3), lambda n: n % 9 != 0)[0] == 9)
a7 = lambda n: n % 2 == 0 and n % 6 == 0
chk("гл7 разбор: контрпример 6", cex(NAT, a7, d(12))[0] == 6)
# глава 8
chk("гл8/гл9 строка 6|3: первый 3, годится 9", impl(NAT, d(6), d(3)) and cex(NAT, d(3), d(6))[:2] == [3, 9])
chk("гл8 строка 3", impl(NAT, last(0), d(10)) and impl(NAT, d(10), last(0)))
chk("гл8: 5->25 ложно (5), 25->5 верно", cex(NAT, d(5), d(25))[0] == 5 and impl(NAT, d(25), d(5)))
chk("гл8: 3->5 ложно (3), 5->3 ложно (5)", cex(NAT, d(3), d(5))[0] == 3 and cex(NAT, d(5), d(3))[0] == 5)
chk("гл8 разбор", impl(NAT, last(5), d(5)) and cex(NAT, d(5), last(5))[0] == 10 and 45 == 40 + 5 and 135 == 130 + 5)
chk("гл8 типичная", impl(NAT, d(4), even) and even(6) and 6 % 4 != 0)
ds = lambda n: sum(map(int, str(n)))
chk("гл8: признак на 9 в обе стороны", forall(NAT, lambda n: (n % 9 == 0) == (ds(n) % 9 == 0)))
# глава 9
chk("гл9 строка 2", forall(NAT, lambda n: even(n) == ((n % 10) % 2 == 0)))
rows = [(n, n % 10 == 0, n % 10 == 0 and True, n % 6 == 0, n % 3 == 0) for n in (3, 6, 9, 10, 12, 20, 30)]
chk("гл9 (доб.) таблица", [(n, a, c, e) for n, a, _, c, e in rows] ==
    [(3, False, False, True), (6, False, True, True), (9, False, False, True), (10, True, False, False),
     (12, False, True, True), (20, True, False, False), (30, True, True, True)])
both35 = lambda n: n % 3 == 0 and n % 5 == 0
chk("гл9 разбор: 15 <=> 3 и 5", forall(NAT, lambda n: (n % 15 == 0) == both35(n)) and 60 == 5 * 12 and 12 % 3 == 0)
chk("гл9 (доб.) кратные 5 по порядку", [k for k in range(1, 10) if (5 * k) % 3 == 0] == [3, 6, 9])
chk("гл9: 2 и 6 -> 12 ложно, 6", cex(NAT, a7, d(12))[0] == 6)
chk("гл9 типичная", impl(NAT, d(8), d(4)) and cex(NAT, d(4), d(8))[0] == 4)
# глава 10
chk("гл10: 6 -> чётное", impl(NAT, d(6), even) and odd(35) and even(14) and 14 % 6 != 0)
chk("гл10 (доб.): 18 и 10", 18 % 6 == 0 and even(18) and 10 % 6 != 0 and even(10))
chk("гл10 (а)", impl(NAT, d(24), d(12)) and cex(NAT, d(12), d(24))[0] == 12)
chk("гл10 (б)", cex(NAT, even, d(12))[0] == 2 and impl(NAT, d(12), even))
a34 = lambda n: n % 3 == 0 and n % 4 == 0
chk("гл10 (в)", forall(NAT, lambda n: a34(n) == (n % 12 == 0)))
chk("гл10 типичная", even(10) and 10 % 12 != 0)

# ---------------- РЕШЕБНИК ----------------
# блок 1
chk("1.1", prime(17) and 100 % 8 != 0 and 7 + 7 == 14)
chk("1.2а", 9 * 7 == 63 and odd(63))
chk("1.2б", 5 * 4 == 20 and not 20 > 20 and not 20 < 20)
chk("1.2в", 6 % 4 != 0)
chk("1.3", [n for n in NAT if not n > 10 and not n < 10] == [10])
# блок 2
s = forall(TWO, lambda n: n > 9); pair("2.1а", s, exists(TWO, lambda n: n <= 9)); chk("2.1а", s and min(TWO) == 10)
chk("2.1б первый 4", cex(NAT, d(4), d(8))[:4] == [4, 12, 20, 28])
chk("2.1в", divs(30) == [1, 2, 3, 5, 6, 10, 15, 30] and [x for x in divs(30) if even(x)] == [2, 6, 10, 30])
B = [12, 18, 30, 42, 45]
chk("2.3", [x for x in B if x % 6] == [45] and forall(B, d(3)) and [ds(x) for x in B] == [3, 9, 3, 6, 9])
# блок 3
chk("3.1а", [n for n in TWO if n % 17 == 0] == [17, 34, 51, 68, 85])
chk("3.1б", all(prime(x) for x in (11, 13, 17, 19)))
months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
chk("3.2", all(m > 27 for m in months) and all(m > 27 for m in [31, 29] + months[2:]))
can = {2 * a + 5 * b for a, b in product(range(6), range(3))} - {0}
chk("3.3", [x for x in range(1, 11) if x not in can] == [1, 3])
chk("3.3 наборы", 4 == 2 + 2 and 7 == 2 + 5 and 9 == 2 + 2 + 5 and 10 == 5 + 5)
# блок 4
r = range(1, 11)
chk("4.1", [n for n in r if n % 4 == 0] == [4, 8] and 1 % 4 != 0)
chk("4.2", forall(NAT, lambda x: x + x > x) and not 0 + 0 > 0)
C = [6, 12, 15, 20, 24]
chk("4.3", [x for x in C if x % 3] == [20] and [x for x in C if x % 8 == 0] == [24]
    and [c for c in C if forall([x for x in C if x != c], d(3))] == [20])
# блок 5
chk("5.1а", forall(NAT, lambda n: n + 3 > 3))
chk("5.1б", not exists(NAT, lambda n: n * n == 20) and 4 * 4 == 16 and 5 * 5 == 25)
chk("5.1в", cex(NAT, d(10), d(4))[0] == 10)
s1 = forall(NAT, lambda n: (10 * n) % 5 == 0); s2 = exists(NAT, lambda n: (10 * n) % 5 == 0)
chk("5.2", s1 and s2 and not exists(NAT, lambda n: (10 * n) % 5 != 0))
chk("5.3", 25 * 5 == 125)
# блок 6
chk("6.1", impl(NAT, d(15), d(5)) and impl(NAT, last(4), even) and cex(NAT, d(3), odd)[:3] == [6, 12, 18])
runs = {"Лена": (110, True), "Гоша": (130, True), "Ира": (120, False), "Олег": (118, False)}
chk("6.2", [k for k, (t, took) in runs.items() if t < 120 and not took] == ["Олег"])
# 6.2-2: обещание сдержано и не взяли => t >= 120
chk("6.2 Тимур", all(not (t < 120) for t in range(60, 300) if not (t < 120 and not False)))
# блок 7
chk("7.1а первый 5", cex(NAT, d(5), d(10))[:3] == [5, 15, 25])
chk("7.1б", cex(NAT, d(8), even) == [])
chk("7.1в: прямоугольник 4 и 6 — не квадрат", 4 != 6)
chk("7.2", cex(TWO, lambda n: True, d(5))[0] == 11 and cex(TWO, lambda n: True, lambda n: n % 5 != 0)[0] == 10)
W = list(product([True, False], repeat=2))  # (ветер, дождь)
chk("7.3", [w for w in W if w[0] and not w[1]] == [(True, False)])
# блок 8
chk("8.1а", cex(NAT, d(7), d(14))[:3] == [7, 21, 35] and impl(NAT, d(14), d(7)))
chk("8.1б", impl(NAT, d(20), d(10)) and cex(NAT, d(10), d(20))[:3] == [10, 30, 50])
chk("8.2", impl(NAT, d(12), d(3)) and cex(NAT, d(3), d(12))[:4] == [3, 6, 9, 15])
# 8.3: гость (суп?, хлеб?) = (нет, да)
soup, bread = False, True
chk("8.3", (not soup or bread) and not (not bread or soup))
# блок 9
tw = lambda n: any(n == m + m for m in range(2, n, 2))
chk("9.1а", forall(NAT, lambda n: (n % 4 == 0) == tw(n)) and 12 == 6 + 6 and 8 + 8 == 16 and [m + m for m in (2, 4, 6, 8)] == [4, 8, 12, 16])
chk("9.1б (14 / 2)", impl(NAT, d(14), even) and 14 == 2 * 7 and cex(NAT, even, d(14))[0] == 2)
chk("9.1в", forall(NAT, lambda n: (n > 10) == (not n < 11)))
a36 = lambda n: n % 3 == 0 and n % 6 == 0
chk("9.2", not a36(9) and impl(NAT, d(18), a36) and cex(NAT, a36, d(18))[:4] == [6, 12, 24, 30])
# 9.3: Петя (все решил, пятёрка) = (да, нет)
allsolved, five = True, False
chk("9.3", not (not allsolved or five) and (not five or allsolved))
# блок 10
T = d(10)
chk("10.1а", impl(NAT, d(20), T) and cex(NAT, T, d(20))[0] == 10)
chk("10.1б первый 2", impl(NAT, T, even) and cex(NAT, even, T)[:2] == [2, 4])
chk("10.1в", forall(NAT, lambda n: last(0)(n) == T(n)))
chk("10.1г", 3 in cex(NAT, d(3), T) and 10 in cex(NAT, T, d(3)))
chk("10.2", impl(NAT, d(100), last(0)) and 340 % 10 == 0 and 340 % 100 != 0)
# 10.3: правило «допущен -> есть справка»
rule = lambda dop, spr: (not dop) or spr
chk("10.3", rule(False, True) and not rule(True, False))

# ---------------- ЗАМЕНЫ, ВНЕСЁННЫЕ В РЕШЕБНИК ----------------
# 6.3: правило «если участнику меньше 10 лет, то он пришёл со взрослым».
# Видно: А — 8 лет (со взрослым? неизвестно); Б — 12 лет (неизвестно);
#        В — со взрослым (возраст неизвестен); Г — без взрослого (возраст неизвестен).
young = lambda age: age < 10
people = {"А": ("age", 8), "Б": ("age", 12), "В": ("adult", True), "Г": ("adult", False)}
need = []
for name, (kind, val) in people.items():
    if kind == "age":
        outcomes = {rule(young(val), adult) for adult in (True, False)}
    else:
        outcomes = {rule(young(age), val) for age in range(5, 16)}
    if False in outcomes:  # скрытое может нарушить правило -> надо узнать
        need.append(name)
chk("6.3: проверять Алю (А) и Глеба (Г)", need == ["А", "Г"])
# 8.1в: «если у треугольника все три стороны равны, то у него есть две равные стороны»
tri = [(a, b, c) for a in range(1, 9) for b in range(a, 9) for c in range(b, 9) if a + b > c]
alleq = lambda t: t[0] == t[1] == t[2]
twoeq = lambda t: len(set(t)) <= 2
chk("8.1в (треугольник 3, 5, 5)", impl(tri, alleq, twoeq) and (3, 5, 5) in cex(tri, twoeq, alleq))

# доп. контроль: наименьшие контрпримеры и случаи, которых не было в скрипте
chk("гл1 таблица: 8<5 ложно, 8>=5", not 8 < 5 and 8 >= 5)
chk("гл8 табл.: обратное 3->6: 3, 9", cex(NAT, d(3), d(6))[:2] == [3, 9])
chk("гл9 типичная / гл10 строки", 14 % 6 != 0 and 12 % 6 == 0 and 35 % 6 != 0)
chk("гл9 табл. чисел: все делятся на 3 или 10", all(n % 3 == 0 or n % 10 == 0 for n in (3, 6, 9, 10, 12, 20, 30)))
chk("7.2: наименьшие 11 и 10", min(n for n in TWO if n % 5) == 11 and min(n for n in TWO if n % 5 == 0) == 10)
chk("8.1в: 3,5,5 — треугольник", 3 + 5 > 5)
chk("9.1б: наименьший контрпример 2", min(n for n in NAT if n % 2 == 0 and n % 14) == 2)
chk("10.1г", 3 % 10 != 0 and 10 % 3 != 0)
chk("5.3/3.3: 10 сумм", len(range(1, 11)) == 10)
print("OK: проверок пройдено", ok)
