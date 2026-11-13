#!/usr/bin/env python3
"""Иллюстрации учебника «Логика» (6 класс, пара 4) → math6_4_logika_uchebnik.vis.json (пишется целиком).

План рисунков и мысль единственного движения: 26-27/school6/vis/plan_logika.md.
Язык пары — множества: свойство = овал, число = подпись в овале. У каждого овала есть предикат (делимость, простота…),
и каждое число на рисунке проверяется: внутри овала ⇔ число обладает свойством. Цитаты рисунков сверяются с MD.

Цвета во всей паре: овал A (условие, «про кого говорим») — CYAN, овал B (свойство, заключение) — VIOLET,
цель главы 10 — GOLD; числа: GREEN — пример, RED — контрпример, GOLD — на что смотрим, INK — просто на своём месте.

Запуск: python3 26-27/school6/vis/logika.py
"""
import json, os, re
from fractions import Fraction as F

from common import (svg, fig, row, t, g, rect, line, frac, NumLine, GOLD, GREEN, RED, VIOLET, CYAN, INK, MUTED)

HERE = os.path.dirname(os.path.abspath(__file__))
MDP = os.path.join(HERE, '..', 'math6_4_logika_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math6_4_logika_uchebnik.vis.json')
MD = open(MDP).read()
MDP_PLAIN = re.sub(r'[`*]', '', MD)


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', s)).strip()


BLOCKS = [norm(b) for b in re.split(r'\n\s*\n', MD)]


def need(*ss):
    """Строка, которую цитирует рисунок, стоит в тексте MD (бэктики сняты)."""
    for s in ss:
        assert s in MDP_PLAIN, f'нет в MD: {s!r}'


# ——— предикаты свойств ———

def prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def dv(k):
    return lambda n: n % k == 0


# ——— овал со свойством и числа в нём ———

class Oval:
    """Овал-свойство. name может быть в две строки ('\n'); lab_in=True — подпись обязана целиком лежать внутри овала."""

    def __init__(self, cx, cy, rx, ry, col, name, lab, pred=None, size=14, lab_in=False):
        self.cx, self.cy, self.rx, self.ry, self.col, self.name, self.lab = cx, cy, rx, ry, col, name, lab
        self.pred, self.size = pred, size
        if lab_in:
            for k, s in enumerate(name.split('\n')):
                w, y = width(s, size) / 2, lab[1] + 17 * k
                for x, yy in ((lab[0] - w, y - 11), (lab[0] + w, y - 11), (lab[0] - w, y + 2), (lab[0] + w, y + 2)):
                    assert self.has(x, yy), f'подпись «{s}» вылезает из своего овала'

    def has(self, x, y, pad=0):
        return ((x - self.cx) / (self.rx - pad)) ** 2 + ((y - self.cy) / (self.ry - pad)) ** 2 < 1

    def draw(self, col=None, name=True, dx=0):
        c = col or self.col
        out = (f"<ellipse cx='{self.cx + dx}' cy='{self.cy}' rx='{self.rx}' ry='{self.ry}' fill='{c}' "
               f"fill-opacity='0.10' stroke='{c}' stroke-width='2'/>")
        if name and self.name:
            for k, s in enumerate(self.name.split('\n')):
                out += t(self.lab[0] + dx, self.lab[1] + 17 * k, s, c, self.size, weight=600)
        return out


def width(s, size):
    return len(re.sub(r'<[^>]+>', '', str(s))) * size * 0.6


def num(n, x, y, ovals, col=INK, size=16, shown=None):
    """Число n в точке (x, y): для каждого овала с предикатом — внутри ⇔ свойство есть (вся подпись, не только центр)."""
    s = shown if shown is not None else str(n)
    w = width(s, size) / 2 + 2
    for o in ovals:
        if o.pred is None:
            continue
        corners = [(x - w, y - 6), (x + w, y - 6), (x - w, y + 6), (x + w, y + 6)]
        ins = [o.has(cx, cy) for cx, cy in corners]
        assert all(ins) or not any(ins), f'число {s} лежит на контуре «{o.name}»'
        assert ins[0] == o.pred(n), f'число {s}: «{o.name}» — {o.pred(n)}, а на рисунке {ins[0]}'
    return t(x, y + size * 0.35, s, col, size, weight=700)


def head(x, y, s, col=INK, size=14, anchor='middle'):
    return t(x, y, s, col, size, anchor=anchor, weight=600)


def span(s, col):
    return f"<tspan fill='{col}'>{s}</tspan>"


def box(w, h, name=None):
    """Рамка «все числа» вокруг рисунка."""
    out = rect(10, 30, w - 20, h - 40, 'none', MUTED, 1.4, rx=10)
    return out + (t(22, 50, name, MUTED, 14, anchor='start') if name else '')


def panel(w, h, body):
    return svg(w, h, body, maxw=w)


# ——— глава 1 ———

def f1_1():
    need('5 больше 5» — ложно', '5 не больше 5» — истинно', '5 меньше 5» — ложно',
         'На числе 8 проверка парой этой потери не ловит')
    W, H = 400, 275
    out = ''
    lines = [(62, 'больше 5', CYAN, 'right'), (142, 'не больше 5 — отрицание', GREEN, 'left'),
             (222, 'меньше 5 — не отрицание', RED, 'left')]
    nl0 = NumLine(30, 350, 0, 10, 0)
    x5, x8 = nl0.x(5), nl0.x(8)
    out += line(x5, 30, x5, 236, GOLD, 1.6, " stroke-dasharray='5 4'")
    out += line(x8, 30, x8, 236, MUTED, 1.2, " stroke-dasharray='3 4'")
    out += t(x8, 22, '8', MUTED, 15, weight=700)
    for y, name, col, side in lines:
        nl = NumLine(30, 350, 0, 10, y)
        out += t(20, y - 22, name, col, 15, anchor='start', weight=600,
                 extra=" stroke='var(--bg2)' stroke-width='5' paint-order='stroke'")   # пунктир 5 и 8 — под подписью
        out += nl.axis(1, labels=range(0, 11), size=14, zero=False)
        a, b = (5, 10.35) if side == 'right' else (-0.35, 5)
        out += nl.seg(a, b, col, 5)
        filled = col == GREEN                                # 5 закрашена только у «не больше 5»
        out += nl.point(5, None, col, 6, hollow=not filled)
    # «больше» и «меньше» не накрывают 5: золотое кольцо на нижней прямой
    out += t(x5, 268, 'потерялось 5', GOLD, 14, weight=600)
    out += f"<circle cx='{x5}' cy='222' r='11' fill='none' stroke='{GOLD}' stroke-width='2'/>"
    cap = ('Исходное и настоящее отрицание вместе накрывают прямую, каждое число — ровно один раз: 5 закрашена только '
           'у «не больше 5». «Больше 5» и «меньше 5» оставляют дырку ровно в одной точке; 8 лежит далеко от неё.')
    return fig(svg(W, H, out), cap)


# ——— глава 2 ———

def f2_1():
    need('Каждое число, делящееся на 10, чётное', 'Все простые числа нечётные', 'контрпример — число 2')
    W, H = 230, 200
    B = Oval(115, 118, 100, 68, VIOLET, 'чётные', (115, 66), lambda n: n % 2 == 0)
    A = Oval(115, 135, 60, 34, CYAN, 'делятся на 10', (115, 140), dv(10))
    left = head(115, 20, '«все» — верно', GREEN) + B.draw() + A.draw()
    B2 = Oval(88, 120, 78, 66, VIOLET, 'нечётные', (78, 44), lambda n: n % 2 == 1)
    A2 = Oval(150, 122, 70, 46, CYAN, 'простые', (180, 68), prime)
    right = (head(115, 20, '«все» — неверно', RED) + B2.draw() + A2.draw()
             + num(2, 196, 122, [A2, B2], RED) + t(176, 192, 'контрпример', RED, 14, weight=600))
    cap = ('«Все A — B» — овал A целиком внутри B. Отрицание «найдётся A без B» — у A есть кусок вне B, '
           'и контрпример лежит именно в этом куске.')
    return fig(row(panel(W, H, left), panel(W, H, right)), cap)


def f2_2():
    need('3 — простое, 13 — простое, 23 — простое, 33 = 3 × 11 — составное')
    assert all(prime(n) for n in (3, 13, 23)) and 33 == 3 * 11
    W, H = 400, 222
    A = Oval(138, 118, 118, 62, CYAN, 'оканчиваются на 3', (118, 44), lambda n: n % 10 == 3)
    B = Oval(272, 118, 112, 72, VIOLET, 'простые', (318, 38), prime)
    out = A.draw() + B.draw()
    for n, x in ((3, 180), (13, 208), (23, 238)):
        out += num(n, x, 112, [A, B], GREEN)
    out += t(209, 212, 'подтверждают', GREEN, 14, weight=600)
    out += num(33, 84, 112, [A, B], RED, shown='33 = 3 × 11')
    out += t(84, 212, 'контрпример', RED, 14, weight=600)
    cap = ('Подтверждения ложатся в общую часть и ничего не говорят о том, вылезает ли A из B. '
           'Решает одно число в куске A вне B.')
    return fig(svg(W, H, out), cap)


def f2_3():
    need('Все простые числа нечётные» — ложно (2)', 'Все простые числа чётные» — тоже ложно (3)')
    W, H = 400, 260
    out = rect(10, 30, W - 20, 170, 'none', MUTED, 1.4, rx=10) + line(200, 30, 200, 200, MUTED, 1.6)
    out += t(105, 54, 'чётные', MUTED, 15, weight=600) + t(295, 54, 'нечётные', MUTED, 15, weight=600)
    P = Oval(200, 125, 120, 52, CYAN, 'простые', (150, 102), prime)
    out += P.draw()
    ev = Oval(-1000, 115, 1200, 1000, 'none', '', (0, 0), lambda n: n % 2 == 0)     # левая половина рамки
    out += num(2, 145, 136, [P, ev], RED) + num(3, 255, 136, [P, ev], RED)
    out += t(105, 222, '«все простые нечётные»', INK, 14) + t(105, 242, span('ложно: 2', RED), INK, 14, weight=600)
    out += t(295, 222, '«все простые чётные»', INK, 14) + t(295, 242, span('ложно: 3', RED), INK, 14, weight=600)
    cap = ('Овал «простые» лежит поперёк черты: в нём есть и чётное 2, и нечётное 3. '
           'Поэтому «все A — B» и «все A — не B» могут быть ложны вместе — вторая фраза не отрицание первой.')
    return fig(svg(W, H, out), cap)


# ——— глава 3 ———

def f3_1():
    need('3 простое и нечётное', 'У 6 делители 1, 2, 3, 6. У 12', 'У 18', 'Ни одно простое число не делится на 6')
    W, H = 230, 200
    A = Oval(80, 118, 70, 56, CYAN, 'простые', (52, 50), prime)
    B = Oval(152, 112, 70, 62, VIOLET, 'чётные', (176, 42), lambda n: n % 2 == 0)
    left = (head(115, 18, 'существует: 2', GREEN) + A.draw() + B.draw()
            + num(2, 118, 116, [A, B], GREEN) + num(3, 42, 118, [A, B]))
    A2 = Oval(60, 118, 48, 56, CYAN, 'простые', (60, 50), prime)
    B2 = Oval(170, 118, 52, 62, VIOLET, 'делятся на 6', (170, 44), dv(6))
    right = head(115, 18, 'не существует', RED) + A2.draw() + B2.draw()
    right += num(2, 60, 104, [A2, B2]) + num(3, 60, 134, [A2, B2])
    for n, y in ((6, 90), (12, 118), (18, 146)):
        right += num(n, 170, y, [A2, B2])
    cap = ('«Существует» — у овалов есть общая точка, одной хватает. «Ни один» — между овалами просвет, '
           'и это утверждение про весь овал сразу, а не про одно число.')
    return fig(row(panel(W, H, left), panel(W, H, right)), cap)


def f3_2():
    need('Пусть в классе 20 учеников и опоздали трое', 'остальные 17 не опоздали')
    assert 20 - 3 == 17
    W, H = 400, 270
    C = Oval(200, 118, 182, 84, MUTED, 'класс — 20 учеников', (200, 24))
    L = Oval(88, 122, 52, 40, CYAN, 'опоздали', (88, 72))
    out = C.draw() + L.draw()
    late = [(70, 112), (104, 112), (88, 140)]
    rest = [(176 + 30 * i, 86 + 30 * j) for j in range(3) for i in range(6)][:17]
    for x, y in late:
        assert L.has(x, y, 8)
        out += f"<circle cx='{x}' cy='{y}' r='7' fill='{CYAN}'/>"
    for x, y in rest:
        assert C.has(x, y, 8) and not L.has(x, y)
        out += f"<circle cx='{x}' cy='{y}' r='7' fill='{INK}' fill-opacity='0.75'/>"
    assert len(late) + len(rest) == 20
    out += t(200, 228, '«некоторые опоздали» — ' + span('истинно: 3', GREEN), INK, 14, weight=600)
    out += t(200, 252, '«некоторые не опоздали» — ' + span('истинно: 17', GREEN), INK, 14, weight=600)
    cap = ('Две фразы говорят о разных кусках одного класса, поэтому истинны вместе. '
           'Отрицание «ни один не опоздал» — это пустой малый овал.')
    return fig(svg(W, H, out), cap)


# ——— глава 4 ———

def sq_ge(q):
    return q * q >= q


def f4_1():
    need('x умножить на x не меньше x', 'контрпример x = 1/2')
    assert not sq_ge(F(1, 2)) and all(sq_ge(F(n)) for n in (1, 2, 3))
    W, H = 230, 252

    def base():
        return Oval(95, 124, 85, 62, VIOLET, 'x умножить на x\nне меньше x', (95, 36), lambda q: sq_ge(F(q)))
    B = base()
    A = Oval(95, 136, 72, 36, CYAN, 'x — натуральное', (95, 132), lambda q: F(q).denominator == 1, lab_in=True)
    left = head(115, 16, 'натуральные: ' + span('верно', GREEN)) + B.draw() + A.draw()
    for n, x in ((1, 71), (2, 95), (3, 119)):
        left += num(n, x, 156, [A, B], GREEN)
    B2 = base()
    A2 = Oval(130, 152, 92, 52, CYAN, 'x — и дроби тоже', (130, 224), lambda q: True)
    right = head(115, 16, 'с дробями: ' + span('неверно', RED)) + B2.draw() + A2.draw()
    for n, x in ((1, 70), (2, 94), (3, 118)):
        right += num(n, x, 135, [A2, B2])
    num(F(1, 2), 198, 150, [A2, B2], shown='½')                 # проверка места — как у числа
    right += frac(198, 150, 1, 2, RED, 15) + t(175, 246, 'контрпример: ½', RED, 14, weight=600)
    cap = ('Откуда берётся переменная — это какой овал A взят. Фраза-B одна и та же, '
           'а вердикт решает, помещается ли выбранный A внутрь B.')
    return fig(row(panel(W, H, left), panel(W, H, right)), cap)


def f4_2():
    need('1 — да, 2 — да, 3 — да, 4 — да, 5 — нет', 'Беру x = 1: единица делит всё')
    W, H = 400, 235
    A = Oval(148, 120, 122, 66, CYAN, 'x от 1 до 6', (110, 44), lambda n: 1 <= n <= 6)
    B = Oval(272, 120, 112, 76, VIOLET, 'делители 12', (300, 36), lambda n: 12 % n == 0)
    out = A.draw() + B.draw()
    out += num(1, 184, 98, [A, B], GREEN)
    for n, (x, y) in ((2, (212, 98)), (3, (240, 98)), (4, (198, 136)), (6, (228, 136))):
        out += num(n, x, y, [A, B])
    out += num(5, 82, 112, [A, B], RED) + t(82, 140, 'контрпример', RED, 14, weight=600)
    out += t(110, 214, 'каждое: ' + span('ложно (5)', RED), INK, 14, weight=600)
    out += t(290, 214, 'найдётся: ' + span('истинно (1)', GREEN), INK, 14, weight=600)
    cap = ('Оба вердикта читаются с одной картинки: «найдётся» спрашивает, есть ли число в общей части, '
           '«каждое» — есть ли число в A вне B.')
    return fig(svg(W, H, out), cap)


# ——— глава 5 ———

def f5_1():
    need('| 2n + 1 | 3 | 5 | 7 | 9 | 11 |')
    vals = [2 * n + 1 for n in range(1, 6)]
    assert vals == [3, 5, 7, 9, 11] and all(v % 4 for v in vals)
    W, H = 400, 215
    out = rect(10, 30, W - 20, 175, 'none', MUTED, 1.4, rx=10) + line(200, 30, 200, 205, MUTED, 1.6)
    out += t(105, 54, 'чётные', MUTED, 15, weight=600) + t(295, 54, 'нечётные', MUTED, 15, weight=600)
    D = Oval(105, 130, 76, 46, VIOLET, 'делятся на 4', (105, 135), dv(4))
    O = Oval(295, 132, 84, 54, CYAN, '2n + 1', (295, 108), lambda n: n in vals)
    ev = Oval(-1000, 115, 1200, 1000, 'none', '', (0, 0), lambda n: n % 2 == 0)
    out += D.draw() + O.draw()
    for v, x in zip(vals, (243, 268, 293, 318, 347)):
        out += num(v, x, 146, [D, O, ev])
    cap = ('Общая причина как расположение: все числа 2n + 1 по нечётную сторону черты, все кратные 4 — по чётную. '
           'Общей точки нет ни при каком n, а не только среди пяти проверенных.')
    return fig(svg(W, H, out), cap)


# ——— глава 6 ———

def f6_1():
    need('| 3 | нет | да | не нарушено |', '| 6 | да | да | выполнено |')
    W, H = 400, 240
    out = box(W, H, 'числа')
    B = Oval(240, 132, 132, 88, VIOLET, 'B: делятся на 3', (226, 76), dv(3), lab_in=True)
    A = Oval(290, 140, 70, 56, CYAN, 'A:\nделятся на 6', (290, 116), dv(6), lab_in=True)
    assert B.cx + B.rx <= W - 10 - 16                       # от рамки «числа» справа — не меньше 16
    out += B.draw() + A.draw()
    out += num(6, 290, 156, [A, B], GREEN) + t(290, 180, 'выполнено', GREEN, 14, weight=600)
    out += num(3, 165, 128, [A, B], GOLD) + t(165, 154, 'не нарушено', GOLD, 14, weight=600)
    for n, (x, y) in ((1, (40, 112)), (2, (80, 112)), (4, (40, 152)), (5, (80, 152))):
        out += num(n, x, y, [A, B])
    out += t(62, 196, 'не нарушено', MUTED, 14, weight=600)
    cap = ('Каждая строка таблицы — своё место на картинке: 6 — в A и в B, 3 — в B вне A, 1, 2, 4, 5 — вне обоих. '
           'Строка «A — да, B — нет» — это кусок A вне B; ни одно из шести чисел туда не попало.')
    return fig(svg(W, H, out), cap)


def f6_2():
    need('число 2 чётное, а на 4 не делится', '2 — контрпример (годятся и 6, 10)')
    W, H = 400, 215
    A = Oval(200, 118, 182, 84, CYAN, 'A: чётные', (200, 56), lambda n: n % 2 == 0)
    B = Oval(282, 128, 84, 46, VIOLET, 'B: делятся на 4', (282, 133), dv(4))
    out = A.draw() + B.draw()
    for n, x in ((2, 72), (6, 112), (10, 152)):
        out += num(n, x, 118, [A, B], RED)
    out += t(112, 148, 'контрпримеры', RED, 14, weight=600)
    cap = 'Следование неверно: овал A не помещается в B. Все три контрпримера лежат в одном куске — A вне B.'
    return fig(svg(W, H, out), cap)


# ——— глава 7 ———

def f7_1():
    need('Если число делится на 3, то оно делится на 9» — ложно, контрпример 3 (годится и 6)',
         'то оно не делится на 9» — тоже ложно, контрпример 9')
    W, H = 230, 250

    def pic(red_ring, title, verdict):
        A = Oval(115, 118, 105, 76, CYAN, 'A: делятся на 3', (112, 74), dv(3), lab_in=True)
        B = Oval(148, 132, 64, 44, VIOLET, 'B:\nделятся на 9', (148, 116), dv(9), lab_in=True)
        out = A.draw() + B.draw()
        out += num(3, 40, 118, [A, B], RED if red_ring else INK)
        out += num(6, 58, 156, [A, B], RED if red_ring else INK)
        out += num(9, 148, 158, [A, B], INK if red_ring else RED)
        out += t(115, 220, title, INK, 14, weight=600) + t(115, 242, verdict, RED, 14, weight=600)
        return out
    left = pic(True, '«если на 3, то на 9»', 'ложно: 3, 6')
    right = pic(False, '«если на 3, то не на 9»', 'ложно: 9')
    cap = ('У A есть числа и внутри B, и вне его. Поэтому «если A, то B» и '
           '«если A, то не B» ломаются вместе.')
    return fig(row(panel(W, H, left), panel(W, H, right)), cap)


def f8_1():
    need('если число делится на 3, то делится на 6 | нет, контрпример 3 (годится и 9)')
    W, H = 230, 236
    outer = Oval(115, 124, 106, 82, VIOLET, 'делятся на 3', (115, 64), dv(3), lab_in=True)
    inner = Oval(148, 140, 66, 46, CYAN, 'делятся на 6', (148, 132), dv(6), lab_in=True)
    TAG_IN, TAG_OUT = (148, 150), (82, 88)          # где стоит ярлык у малого и у большого овала

    def tag(p, s, col):
        return t(p[0], p[1], s, col, 14, weight=600)

    def nums(col_ring):
        return (num(6, 148, 172, [outer, inner]) + num(3, 34, 124, [outer, inner], col_ring)
                + num(9, 52, 162, [outer, inner], col_ring))

    left = (head(118, 18, 'прямое:', anchor='end') + head(124, 18, 'верно', GREEN, anchor='start') + outer.draw() + inner.draw() + nums(INK)
            + tag(TAG_IN, 'условие', CYAN) + tag(TAG_OUT, 'заключение', VIOLET))
    dx, dy = TAG_OUT[0] - TAG_IN[0], TAG_OUT[1] - TAG_IN[1]
    right = head(118, 18, 'обратное:', anchor='end') + g('fi', 3.6, head(124, 18, 'неверно', RED, anchor='start'))
    # цвета контуров меняются вместе с ролями: исходные гаснут, переставленные проявляются
    right += g('fo', 1.4, outer.draw() + inner.draw()) + g('fi', 1.6, outer.draw(CYAN) + inner.draw(VIOLET))
    right += nums(INK)
    right += g('fi', 3.0, num(3, 34, 124, [outer, inner], RED) + num(9, 52, 162, [outer, inner], RED)
               + t(70, 228, 'контрпримеры', RED, 14, weight=600))
    right += g('sl', 1.2, tag(TAG_IN, 'условие', CYAN), f';--to:translate({dx}px,{dy}px)')
    right += g('sl', 1.2, tag(TAG_OUT, 'заключение', VIOLET), f';--to:translate({-dx}px,{-dy}px)')
    cap = ('Обратное — те же два овала, у которых поменялись ярлыки «условие» и «заключение». Условием стал большой '
           'овал, а он в маленький не влезает: числа 3 и 9, безвредные для прямого, — контрпримеры обратному.')
    return fig(row(panel(W, H, left), panel(W, H, right)), cap, fx=True)


def f8_2():
    need('оканчивается на 0, то делится на 10 | да | если число делится на 10, то оканчивается на 0 | да',
         'контрпример: прямоугольник 2 на 5',
         'прямое «если число делится на 5, то оно делится на 25» ложно (контрпример 5)',
         'и обратное «если число делится на 5, то оно делится на 3» тоже ложно (контрпример 5)',
         'прямое «если число делится на 3, то оно делится на 5» ложно (контрпример 3)')
    W, H = 230, 200
    V, N = span('верно', GREEN), span('неверно', RED)

    # совпали: один овал, два контура вплотную
    A = Oval(115, 118, 100, 58, CYAN, 'оканчиваются на 0', (115, 110), lambda n: n % 10 == 0)
    p1 = head(115, 20, f'{V} и {V}') + A.draw()
    p1 += (f"<ellipse cx='115' cy='118' rx='105' ry='63' fill='none' stroke='{VIOLET}' stroke-width='2'/>"
           + t(115, 136, 'делятся на 10', VIOLET, 14, weight=600))

    # квадраты внутри прямоугольников; прямоугольник 2 на 5 — в кольце
    Bo = Oval(115, 118, 105, 68, VIOLET, 'прямоугольники', (115, 74), lab_in=True)
    Ai = Oval(150, 130, 52, 40, CYAN, 'квадраты', (150, 112), lab_in=True)
    p2 = head(115, 20, f'{V}, а обратное {N}') + Bo.draw() + Ai.draw()
    p2 += rect(136, 122, 28, 28, CYAN, CYAN, 1.6, extra=" fill-opacity='0.35'")
    u = 9                                                        # 1 единица = 9 px: 2 на 5 → 18 × 45
    p2 += rect(30, 112, 5 * u, 2 * u, RED, RED, 1.6, extra=" fill-opacity='0.35'")
    p2 += t(52, 148, '2 на 5', RED, 14, weight=600)
    for x, y in ((30, 112), (30 + 5 * u, 112 + 2 * u)):
        assert Bo.has(x, y) and not Ai.has(x, y)

    Ao = Oval(115, 118, 105, 68, CYAN, 'делятся на 5', (110, 74), dv(5), lab_in=True)
    Bi = Oval(150, 132, 58, 38, VIOLET, 'делятся на 25', (150, 136), dv(25), lab_in=True)
    p3 = head(115, 20, f'{N}, а обратное {V}') + Ao.draw() + Bi.draw() + num(5, 50, 124, [Ao, Bi], RED)

    A4 = Oval(80, 120, 68, 58, CYAN, 'делятся на 3', (62, 52), dv(3))
    B4 = Oval(152, 120, 68, 58, VIOLET, 'делятся на 5', (170, 194), dv(5))
    p4 = (head(115, 20, f'{N} и {N}') + A4.draw() + B4.draw()
          + num(3, 46, 122, [A4, B4], RED) + num(5, 186, 122, [A4, B4], RED))
    cap = ('Четыре сочетания — четыре способа, как могут лежать два овала: совпали, первый внутри второго, '
           'второй внутри первого, нахлёст.')
    p = [panel(W, H, b) for b in (p1, p2, p3, p4)]
    return fig(row(p[0], p[1]) + "<div style='height:16px'></div>" + row(p[2], p[3]), cap)


# ——— глава 9 ———

def f9_1():
    need('5 × 3 = 15', '5 × 6 = 30', 'Проверь на числе 60', '«делится на 2 и на 6» → «делится на 12» уже ложно, контрпример 6')
    W, H = 230, 225
    # половины условия — CYAN обе, заключение («на 15») — VIOLET: общая часть двух кругов
    A = Oval(80, 120, 70, 70, CYAN, 'делятся на 3', (62, 40), dv(3))
    B = Oval(152, 120, 70, 70, CYAN, 'делятся на 5', (168, 212), dv(5))
    d = B.cx - A.cx
    hy = (A.rx ** 2 - (d / 2) ** 2) ** 0.5                 # полувысота общей части (круги равного радиуса)
    mx, y1, y2 = A.cx + d / 2, A.cy - hy, A.cy + hy
    lens = (f"<path d='M{mx:.1f},{y1:.1f} A{A.rx},{A.rx} 0 0 1 {mx:.1f},{y2:.1f} A{A.rx},{A.rx} 0 0 1 {mx:.1f},{y1:.1f} Z' "
            f"fill='{VIOLET}' fill-opacity='0.22' stroke='{VIOLET}' stroke-width='2.5'/>")
    left = (head(115, 16, 'общая часть = ' + span('делятся на 15', VIOLET), INK, 14)
            + A.draw() + B.draw() + lens)
    for n, y in ((15, 94), (30, 120), (60, 146)):
        assert n % 15 == 0
        left += num(n, 116, y, [A, B], VIOLET)
    for n, (x, y) in ((5, (172, 104)), (10, (200, 104)), (20, (172, 138)), (25, (200, 138))):
        left += num(n, x, y, [A, B])
    for n, y in ((3, 104), (9, 138)):
        left += num(n, 44, y, [A, B])
    O2 = Oval(115, 116, 105, 82, CYAN, 'делятся на 2', (115, 60), lambda n: n % 2 == 0, lab_in=True)
    O6 = Oval(126, 130, 82, 58, CYAN, 'делятся на 6', (126, 94), dv(6))
    O12 = Oval(140, 146, 58, 30, VIOLET, 'делятся на 12', (140, 151), dv(12))
    right = (head(115, 16, 'общая часть — весь «на 6»', RED, 14) + O2.draw() + O6.draw() + O12.draw()
             + num(6, 70, 130, [O2, O6, O12], RED) + t(115, 216, '6 — контрпример', RED, 14, weight=600))
    cap = ('«Делится на 3 и на 5» — общая часть двух овалов; у взаимно простых 3 и 5 она совпадает с «делятся на 15». '
           'У 2 и 6 общая часть — весь овал «на 6», и он больше овала «на 12».')
    return fig(row(panel(W, H, left), panel(W, H, right)), cap)


# ——— глава 10 ———

def f10_1():
    need('18 делится на 6 → 18 чётное', '35 нечётно → на 6 не делится', '14 чётно, а на 6 не делится; 12 чётно',
         '10 на 6 не делится, а всё равно чётное')
    W, H = 400, 215
    out = box(W, 215, 'числа')
    B = Oval(232, 120, 140, 74, VIOLET, 'чётные', (180, 70), lambda n: n % 2 == 0)
    A = Oval(282, 128, 76, 44, CYAN, 'делятся на 6', (282, 112), dv(6))
    out += B.draw() + A.draw()
    out += num(18, 262, 138, [A, B], GREEN) + num(12, 304, 138, [A, B], GOLD)
    out += num(14, 140, 108, [A, B], GOLD) + num(10, 152, 148, [A, B], GOLD)
    out += num(35, 50, 120, [A, B], RED)
    cap = ('Почему третья и четвёртая строки ничего не дают. «Чётное» — весь большой овал, а в нём есть и кольцо '
           '(14, 10), и малый овал (12). «Не делится на 6» — всё вне малого овала, а там лежат и чётное 10, и нечётное 35.')
    return fig(svg(W, H, out), cap)


def f10_2():
    need('(а) число делится на 24; (б) число чётное; (в) число делится на 3 и на 4',
         'число 12 делится на 12, но не делится на 24', '2 чётно, а на 12 не делится')
    W, H = 400, 300
    E = Oval(200, 118, 186, 96, CYAN, '(б) чётные', (200, 42), lambda n: n % 2 == 0)
    T = Oval(228, 132, 132, 66, GOLD, 'делятся на 12', (214, 90), dv(12))
    S = Oval(262, 150, 72, 30, CYAN, '(а) делятся на 24', (262, 155), dv(24))
    out = E.draw() + T.draw()
    out += (f"<ellipse cx='228' cy='132' rx='137' ry='71' fill='none' stroke='{CYAN}' stroke-width='2' "
            f"stroke-dasharray='6 4'/>" + t(214, 108, '= (в) на 3 и на 4', CYAN, 14, weight=600))
    out += S.draw()
    out += num(2, 52, 120, [E, T, S]) + num(12, 140, 150, [E, T, S])
    for k, s in enumerate(('(а) внутри «на 12» — ' + span('достаточное', GREEN),
                           '(б) содержит «на 12» — ' + span('необходимое', GREEN),
                           '(в) совпал с «на 12» — ' + span('и то и другое', GREEN))):
        out += t(20, 240 + 22 * k, s, INK, 14, anchor='start', weight=600)
    cap = ('Ответ — это где лежит овал условия относительно овала «на 12»; 2 и 12 — контрпримеры из разбора, '
           'каждый на своём месте.')
    return fig(svg(W, H, out), cap)


FIGS = {
    'Поэтому проверку парой делай на том числе': f1_1,
    'Такой найденный объект называется': f2_1,
    'Посмотри, как шёл шаг 2': f2_2,
    'Оба ложны, значит отрицанием тут и не пахнет': f2_3,
    'Ни одного примера нет, высказывание ложно': f3_1,
    'Пусть в классе 20 учеников и опоздали трое': f3_2,
    'Фраза одна и та же, вердикты разные': f4_1,
    'Из одного предложения — два высказывания с разными вердиктами': f4_2,
    'Нечётное число не может быть чётным': f5_1,
    'Посмотри на строку числа 3': f6_1,
    'Это следование неверно, 2 — контрпример': f6_2,
    'ровно одно обязано быть истинным': f7_1,
    'Из истинности прямого утверждения истинность обратного не следует': f8_1,
    'неверно, и обратное неверно': f8_2,
    'двойка у них общая': f9_1,
    'Работают только первые две строки': f10_1,
    '(в) и то и другое, то есть равносильное': f10_2,
}


if __name__ == '__main__':
    out = {}
    for anchor, f in FIGS.items():
        hits = [b for b in BLOCKS if anchor in b]
        assert len(hits) == 1, f'якорь «{anchor}» встречается в {len(hits)} абзацах'
        out[anchor] = f()
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(out), 'рисунков,', sum('class="fx"' in v for v in out.values()), 'анимаций →', os.path.relpath(VIS))
