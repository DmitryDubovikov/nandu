"""Перебор для T1-70-1 — чайная лавка.

Цены килограмма — целые доллары. Из первой покупки (по 250 г каждого сорта за $1075)
каждая цена не больше 4 · 1075 = $4300.
Перебираются все целые цены чёрного и зелёного от $0 до $4300; цена мате берётся
из третьей покупки, цена ромашкового — из первой (обе обязаны выйти целыми и не меньше 0).
Все четыре покупки затем проверяются заново по граммам из условия, точными дробями.
"""
from fractions import Fraction as F

SORTA = ("ч", "з", "м", "р")


def stoimost(ceny, pokupka):
    """pokupka: {сорт: граммы}; цена — за килограмм."""
    return sum(ceny[s] * F(g, 1000) for s, g in pokupka.items())


P1 = {"ч": 250, "з": 250, "м": 250, "р": 250}           # $1075
P2 = {"ч": 100, "з": 100, "м": 100, "р": 300}           # $530
P3 = {"ч": 250, "з": 500, "м": 250}                     # $1250
P4_left = {"ч": 100, "м": 300}                          # столько же, сколько
P4_right = {"з": 200, "р": 400}

GRAN = 4 * 1075

naydeno = []
for ch in range(GRAN + 1):
    for z in range(GRAN + 1 - ch):
        # третья покупка: м/4 = 1250 − ч/4 − з/2
        m = 4 * (F(1250) - F(ch, 4) - F(z, 2))
        if m < 0 or m.denominator != 1:
            continue
        # первая покупка: р/4 = 1075 − (ч + з + м)/4
        r = 4 * F(1075) - ch - z - m
        if r < 0 or r.denominator != 1:
            continue
        ceny = {"ч": ch, "з": z, "м": int(m), "р": int(r)}
        if (stoimost(ceny, P1) == 1075
                and stoimost(ceny, P2) == 530
                and stoimost(ceny, P3) == 1250
                and stoimost(ceny, P4_left) == stoimost(ceny, P4_right)):
            naydeno.append(ceny)

print("Подходящих наборов цен:", len(naydeno))
for c in naydeno:
    print(", ".join(f"x_{s} = {c[s]}" for s in SORTA))
