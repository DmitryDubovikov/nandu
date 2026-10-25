"""Примитивы рисунков учебника «Десятичные дроби и геометрия» поверх common.py.

Сверка с текстом: has() требует, чтобы каждая строка, написанная на рисунке как результат, стояла в MD;
dec() печатает Decimal с запятой, не трогая хвостовые нули (их число — часть записи).
"""
import os, re
from decimal import Decimal as D
from fractions import Fraction as F

from common import (GOLD, BLUE, GREEN, RED, VIOLET, CYAN, PINK, GREY, INK, MUTED, DARK, PLACE,
                    svg, fig, t, g, rect, line, strike, frac, arrow_defs_p)

HERE = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(HERE, '..', 'math5_desyatichnye_geom_uchebnik.md')
MD = open(MD_PATH).read()
PLAIN = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', MD))


def has(*ss):
    for s in ss:
        k = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', s))
        assert k in PLAIN, f'на рисунке «{s}», а в тексте MD этого нет'


def dec(x):
    return format(x, 'f').replace('.', ',')


# разряд по номеру: 0 — единицы, 1 — десятки, −1 — десятые …
PNAME = {2: 'сотни', 1: 'десятки', 0: 'единицы', -1: 'десятые', -2: 'сотые', -3: 'тысячные'}


def pcol(p):
    return PLACE[PNAME[p]]


def digits(s):
    """'12,008' → {1: '1', 0: '2', -1: '0', -2: '0', -3: '8'}"""
    ip, _, fp = s.partition(',')
    out = {k: ch for k, ch in zip(range(len(ip) - 1, -1, -1), ip)}
    out.update({-k - 1: ch for k, ch in enumerate(fp)})
    return out


CW, CH = 34, 44


def cell(x, y, s='', col=MUTED, w=CW, h=CH, size=22, dashed=False, txt=None, op=0.14, sw=1.6, weight=700):
    dash = " stroke-dasharray='4 3'" if dashed else ''
    r = (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='5' fill='{col}' fill-opacity='{op}' "
         f"stroke='{col}' stroke-width='{sw}'{dash}/>")
    if s != '':
        r += t(x + w / 2, y + h / 2 + size * 0.36, s, txt or col, size, weight=weight)
    return r


def comma(x, y, col=INK, size=30):
    """Запятая; (x, y) — точка у основания клеток."""
    return t(x, y, ',', col, size, weight=700)


class Grid:
    """Столбцы разрядов: x(p) — левый край клетки разряда p; между единицами и десятыми — щель под запятую."""

    def __init__(self, xu, step=CW + 8, gap=14):
        self.xu, self.step, self.gap = xu, step, gap

    def x(self, p):
        return self.xu - p * self.step + (self.gap if p < 0 else 0)

    def cx(self, p):
        return self.x(p) + CW / 2

    def comma_x(self):
        return self.xu + CW + (self.step - CW + self.gap) / 2

    def number(self, y, s, dim=(), col=None, dashed=(), txt=None, size=22, h=CH):
        """Число s по разрядам; dim — разряды, чья цифра тусклая (дописанный ноль)."""
        out = []
        for p, ch in digits(s).items():
            c = col or pcol(p)
            out.append(cell(self.x(p), y, ch, c, h=h, size=size, dashed=p in dashed,
                            txt=(MUTED if p in dim else (txt or c))))
        if ',' in s:
            out.append(comma(self.comma_x(), y + h - 4, INK))
        return ''.join(out)


def arrow(x1, y1, x2, y2, mid, col=MUTED, sw=2, extra=''):
    return (f"<path d='M{x1} {y1} L{x2} {y2}' stroke='{col}' stroke-width='{sw}' fill='none' "
            f"marker-end='url(#{mid})'{extra}/>")


def arc_hop(x1, x2, y, hgt, mid, col=BLUE, sw=2):
    xm = (x1 + x2) / 2
    return (f"<path d='M{x1} {y} Q {xm} {y-hgt} {x2} {y}' fill='none' stroke='{col}' stroke-width='{sw}' "
            f"marker-end='url(#{mid})'/>")


def drpath(d, col, sw=3, delay=0, dur=1.0, extra=''):
    """Линия, которая прорисовывается (класс dr)."""
    return (f"<path d='{d}' fill='none' stroke='{col}' stroke-width='{sw}' pathLength='100' class='dr' "
            f"style='--d:{delay}s;--dur:{dur}s' stroke-linecap='round' stroke-linejoin='round'{extra}/>")


def poly(pts, fill='none', stroke=MUTED, sw=2, op=1, extra=''):
    p = ' '.join(f'{x},{y}' for x, y in pts)
    return (f"<polygon points='{p}' fill='{fill}' fill-opacity='{op}' stroke='{stroke}' stroke-width='{sw}' "
            f"stroke-linejoin='round'{extra}/>")


def box(x, y, w, h, col, op=0.22, sw=2, dashed=False, rx=0):
    dash = " stroke-dasharray='6 4'" if dashed else ''
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{col}' fill-opacity='{op}' "
            f"stroke='{col}' stroke-width='{sw}'{dash}/>")


def dot(x, y, col, r=6):
    return f"<circle cx='{x}' cy='{y}' r='{r}' fill='{col}'/>"


def slide(d, dx, dy, body):
    return g('sl', d, body, f';--to:translate({dx}px,{dy}px)')


def fi(d, body):
    return g('fi', d, body)


def fo(d, body, o=0):
    return g('fo', d, body, f';--o:{o}')


def nline(x0, x1, y, v0, v1):
    """Числовая прямая: возвращает функцию значение → x."""
    v0, v1 = F(v0), F(v1)
    return lambda v: float(x0 + (F(v) - v0) / (v1 - v0) * (x1 - x0))


def ufrac(x, y, num, den, col=INK, size=18):
    """Короткая дробь в строку: num/den столбиком, (x, y) — центр черты."""
    return frac(x, y, num, den, col, size)
