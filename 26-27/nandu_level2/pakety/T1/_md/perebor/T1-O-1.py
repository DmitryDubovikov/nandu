"""T1-O-1, магазин игрушек: перебор цен без скидки.

x — машинка, b — мяч, p — пазл (цены без скидки, целые, $1..$1000).
Скидки на вторую единицу: машинка 50 %, мяч 25 %, пазл 40 %.
Суббота — все три акции, воскресенье — только машинки, понедельник — мячи и пазлы.
Покупка: 4 машинки, 2 мяча, 6 пазлов (2, 1 и 3 пары).
Суммы: суббота 670, воскресенье 740, понедельник 790.
"""
from fractions import Fraction as F

PAY = {"x": F(50, 100), "b": F(75, 100), "p": F(60, 100)}  # доля цены второй единицы
QTY = {"x": 4, "b": 2, "p": 6}
DAYS = {  # день: (товары с акцией, сумма)
    "суббота": ({"x", "b", "p"}, 670),
    "воскресенье": ({"x"}, 740),
    "понедельник": ({"b", "p"}, 790),
}
LIMIT = 1000


def cost_pairs(price, day_set):
    """Верное прочтение: скидка в каждой паре."""
    s = F(0)
    for g, v in price.items():
        pair = v + v * PAY[g] if g in day_set else 2 * v
        s += (QTY[g] // 2) * pair
    return s


def cost_once(price, day_set):
    """Неверное прочтение: скидка один раз на товар."""
    s = F(0)
    for g, v in price.items():
        s += QTY[g] * v - (v - v * PAY[g] if g in day_set else 0)
    return s


def search_fast(cost):
    # p вычисляется из субботы (уравнение линейно по p), затем проверка всех дней
    sols = []
    sat_set, sat_sum = DAYS["суббота"]
    for x in range(1, LIMIT + 1):
        for b in range(1, LIMIT + 1):
            c0 = cost({"x": x, "b": b, "p": 0}, sat_set)
            c1 = cost({"x": x, "b": b, "p": 1}, sat_set) - c0
            p = (sat_sum - c0) / c1
            if p.denominator == 1 and 1 <= p <= LIMIT:
                pr = {"x": x, "b": b, "p": int(p)}
                if all(cost(pr, s) == t for s, t in DAYS.values()):
                    sols.append((x, b, int(p)))
    return sols


if __name__ == "__main__":
    good = search_fast(cost_pairs)
    print("Скидка в каждой паре, цены 1..%d: решения (x, b, p) =" % LIMIT, good)
    bad = search_fast(cost_once)
    print("Скидка один раз на товар: решения =", bad)
    for x, b, p in good:
        for day, (s, t) in DAYS.items():
            print(f"  {day}: {cost_pairs({'x': x, 'b': b, 'p': p}, s)} (дано {t})")
