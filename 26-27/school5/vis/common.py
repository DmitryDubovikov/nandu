#!/usr/bin/env python3
"""Общие примитивы рисунков учебников 5 класса (дроби, десятичные и геометрия, делимость).

Один цветовой язык на все три книги:
  GOLD   — то, на что смотрим сейчас;
  BLUE   — действие: перевёрнутый делитель, переносимая запятая, проводимая линия;
  RED    — сокращённое, зачёркнутое, ошибка;
  GREEN  — результат;
  GREY   — выбывшее, уже не участвует;
  PLACE  — у каждого разряда свой цвет во всех рисунках (тысячи … тысячные).

Анимация — только переход (правило 15). Классы шаблона внутри SVG фигуры с fx=True:
  fi — проявляется к моменту --d;  fo — гаснет к моменту --d (до --o);
  sl — переезжает на --to (translate(…px,…px)) к моменту --d;  dr — линия прорисовывается (pathLength='100').
Без fx=True фигура статична, классы ничего не делают.
"""

GOLD, BLUE, GREEN, RED, VIOLET = '#f0a83c', '#5ba8f5', '#5fd38d', '#f2686c', '#b48cf2'
CYAN, PINK = '#4fd1d9', '#f78fb3'
GREY = '#5d6b7c'
INK, MUTED = 'var(--ink)', 'var(--muted)'
DARK = '#0d1117'

PLACE = {                       # разряд → цвет, сквозной во всех рисунках
    'тысячи': PINK, 'сотни': VIOLET, 'десятки': BLUE, 'единицы': GOLD,
    'десятые': GREEN, 'сотые': CYAN, 'тысячные': RED,
}


def svg(w, h, body, maxw=None):
    st = f" style='max-width:{maxw}px'" if maxw else ''
    return (f"<svg viewBox='0 0 {w} {h}' width='{w}' height='{h}' font-family='inherit' "
            f"font-size='15'{st}>{body}</svg>")


def fig(s, cap='', fx=False):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    cls = ' class="fx"' if fx else ''
    return f'<figure{cls}>{s}{c}</figure>'


def t(x, y, s, fill=MUTED, size=None, anchor='middle', weight=None, cls=None, d=None, extra=''):
    a = f" font-size='{size}'" if size else ''
    a += f" font-weight='{weight}'" if weight else ''
    a += f" class='{cls}'" if cls else ''
    a += f" style='--d:{d}s'" if d is not None else ''
    return f"<text x='{x}' y='{y}' text-anchor='{anchor}' fill='{fill}'{a}{extra}>{s}</text>"


def g(cls, d, body, extra=''):
    return f"<g class='{cls}' style='--d:{d}s{extra}'>{body}</g>"


def rect(x, y, w, h, fill='none', stroke=MUTED, sw=1.5, rx=0, extra=''):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}' "
            f"stroke='{stroke}' stroke-width='{sw}'{extra}/>")


def line(x1, y1, x2, y2, stroke=MUTED, sw=1.5, extra=''):
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{stroke}' stroke-width='{sw}'{extra}/>"


def strike(x, y, w, d=None, col=RED):
    """Косая черта поверх числа шириной w с центром (x, y) — «сократили»."""
    body = line(x - w / 2, y + 8, x + w / 2, y - 14, col, 2.5)
    return g('fi', d, body) if d is not None else body


def frac(x, y, num, den, fill=INK, size=20, w=None, cls=None, d=None):
    """Обыкновенная дробь столбиком: числитель над чертой, знаменатель под ней; (x, y) — центр черты."""
    w = w or max(len(str(num)), len(str(den))) * size * 0.62 + 8
    body = (t(x, y - 6, num, fill, size, weight=600) + line(x - w / 2, y, x + w / 2, y, fill, 2)
            + t(x, y + size + 2, den, fill, size, weight=600))
    return g(cls, d, body) if cls else body


def arrow_defs(cols):
    """Маркеры-наконечники ah0, ah1, … по списку цветов: marker-end='url(#ah0)'.
    ⚠ id маркеров общие на странице — в каждом рисунке давай свой префикс через arrow_defs_p."""
    return arrow_defs_p('ah', cols)


def arrow_defs_p(prefix, cols):
    return '<defs>' + ''.join(
        f"<marker id='{prefix}{k}' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' "
        f"orient='auto'><path d='M0,0 L10,5 L0,10 z' fill='{c}'/></marker>" for k, c in enumerate(cols)) + '</defs>'
