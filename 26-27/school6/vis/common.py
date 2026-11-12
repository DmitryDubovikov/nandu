#!/usr/bin/env python3
"""Общие примитивы рисунков учебников 6 класса (семь пар).

База — общий модуль 5 класса (26-27/school5/vis/common.py): те же цвета, svg/fig/t/g/rect/line/frac/стрелки,
чтобы школьные учебники выглядели одной книгой. Здесь — то, что нужно шестому классу: числовая прямая,
координатная плоскость, клетчатая сетка, полоса из частей, вложенные множества, геометрия по координатам.

Цвета сквозные во всех семи парах:
  GOLD  — то, на что смотрим сейчас;   RED   — запрет, ошибка, «не подходит»;
  BLUE  — выбор, действие;             GREEN — результат, «подходит»;
  GREY  — выбывшее;  VIOLET/CYAN/PINK — вторая-третья величина в одном рисунке.

Анимация — только переход (правило 15 CLAUDE.md). Классы внутри SVG у фигуры с fx=True:
  fi — проявляется к моменту --d;  fo — гаснет к моменту --d (до --o);
  sl — переезжает на --to (translate(…px,…px)) к моменту --d;  dr — линия прорисовывается (pathLength='100').
Исходник стоит неподвижно слева, движется только копия справа.

ASCII-рисунок MD заменяется рисунком: fig(..., zamena=True) с якорем — подстрокой самого блока ```…```;
конвертер ставит рисунок на место блока, а исходник прячет (текст сверки не теряется).

⚠ id маркеров стрелок общие на странице: в каждом рисунке свой префикс (arrow_defs_p('g3a', …)).
"""
import importlib.util, math, os

# модуль 5 класса грузится по пути под своим именем: этот файл тоже зовётся common, и обычный импорт зациклился бы
_spec = importlib.util.spec_from_file_location(
    'school5_common', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'school5', 'vis', 'common.py'))
_c5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_c5)
GOLD, BLUE, GREEN, RED, VIOLET, CYAN, PINK, GREY = _c5.GOLD, _c5.BLUE, _c5.GREEN, _c5.RED, _c5.VIOLET, _c5.CYAN, _c5.PINK, _c5.GREY
INK, MUTED, DARK = _c5.INK, _c5.MUTED, _c5.DARK
svg, t, g, rect, line, strike, frac = _c5.svg, _c5.t, _c5.g, _c5.rect, _c5.line, _c5.strike, _c5.frac
arrow_defs, arrow_defs_p = _c5.arrow_defs, _c5.arrow_defs_p


def fig(s, cap='', fx=False, zamena=False):
    """<figure>: fx — анимированная (кнопка «↻ ещё раз»), zamena — встаёт вместо ASCII-блока."""
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    cls = ' '.join(x for x, on in (('fx', fx), ('zamena', zamena)) if on)
    return f'<figure class="{cls}">{s}{c}</figure>' if cls else f'<figure>{s}{c}</figure>'


def row(*svgs, gap=24):
    """Несколько рисунков рядом (пример и контрпример): одна фигура, ряд переносится на узком экране."""
    cells = ''.join(f"<div style='flex:1 1 200px;min-width:0'>{s}</div>" for s in svgs)
    return f"<div style='display:flex;flex-wrap:wrap;gap:{gap}px;align-items:flex-end'>{cells}</div>"


def path(pts, stroke=MUTED, sw=2, fill='none', closed=True, dash=None, extra=''):
    """Ломаная/многоугольник по точкам [(x, y), …]."""
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + (' Z' if closed else '')
    da = f" stroke-dasharray='{dash}'" if dash else ''
    return (f"<path d='{d}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}' "
            f"stroke-linejoin='round'{da}{extra}/>")


def dot(x, y, r=4, fill=INK, extra=''):
    return f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{fill}'{extra}/>"


def circle(x, y, r, stroke=MUTED, sw=2, fill='none', dash=None, extra=''):
    da = f" stroke-dasharray='{dash}'" if dash else ''
    return (f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r:.1f}' fill='{fill}' stroke='{stroke}' "
            f"stroke-width='{sw}'{da}{extra}/>")


def label(p, s, away=(0, 0), dist=14, fill=INK, size=16, weight=600):
    """Буква у точки p, отодвинутая от точки away (обычно центр фигуры) на dist."""
    x, y = p
    dx, dy = x - away[0], y - away[1]
    n = math.hypot(dx, dy) or 1
    return t(round(x + dx / n * dist, 1), round(y + dy / n * dist + size * 0.35, 1), s, fill, size,
             weight=weight)


def angle_arc(v, p1, p2, r=22, stroke=GOLD, sw=2, text=None, fill=None, size=14):
    """Дуга угла с вершиной v между лучами к p1 и p2 (меньший угол), подпись text по биссектрисе."""
    a1 = math.atan2(p1[1] - v[1], p1[0] - v[0])
    a2 = math.atan2(p2[1] - v[1], p2[0] - v[0])
    da = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    x1, y1 = v[0] + r * math.cos(a1), v[1] + r * math.sin(a1)
    x2, y2 = v[0] + r * math.cos(a1 + da), v[1] + r * math.sin(a1 + da)
    sweep = 1 if da > 0 else 0
    out = (f"<path d='M{x1:.1f},{y1:.1f} A{r},{r} 0 0 {sweep} {x2:.1f},{y2:.1f}' fill='none' "
           f"stroke='{stroke}' stroke-width='{sw}'/>")
    if text:
        am = a1 + da / 2
        out += t(round(v[0] + (r + 14) * math.cos(am), 1), round(v[1] + (r + 14) * math.sin(am) + 5, 1),
                 text, fill or stroke, size)
    return out


def right_angle(v, p1, p2, s=12, stroke=GOLD, sw=1.8):
    """Квадратик прямого угла в вершине v."""
    def u(p):
        dx, dy = p[0] - v[0], p[1] - v[1]
        n = math.hypot(dx, dy)
        return dx / n * s, dy / n * s
    (ax, ay), (bx, by) = u(p1), u(p2)
    pts = [(v[0] + ax, v[1] + ay), (v[0] + ax + bx, v[1] + ay + by), (v[0] + bx, v[1] + by)]
    return path(pts, stroke, sw, closed=False)


def ticks(p, q, n=1, stroke=GOLD, size=7, sw=2):
    """n черточек равенства посередине отрезка pq."""
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    out = ''
    for k in range(n):
        o = (k - (n - 1) / 2) * 5
        cx, cy = mx + ux * o, my + uy * o
        out += line(round(cx - nx * size, 1), round(cy - ny * size, 1), round(cx + nx * size, 1),
                    round(cy + ny * size, 1), stroke, sw)
    return out


def dim(p, q, text, off=18, stroke=MUTED, fill=None, size=14):
    """Размерная линия вдоль pq, сдвинутая на off (влево от направления p→q), с подписью длины."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = dy / L * off, -dx / L * off
    a, b = (p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny)
    out = line(round(a[0], 1), round(a[1], 1), round(b[0], 1), round(b[1], 1), stroke, 1.2)
    for e in (a, b):
        out += line(round(e[0] - nx / off * 5, 1), round(e[1] - ny / off * 5, 1),
                    round(e[0] + nx / off * 5, 1), round(e[1] + ny / off * 5, 1), stroke, 1.2)
    mx, my = (a[0] + b[0]) / 2 + nx / off * 12, (a[1] + b[1]) / 2 + ny / off * 12
    return out + t(round(mx, 1), round(my + size * 0.35, 1), text, fill or INK, size)


class NumLine:
    """Числовая прямая: значения v → x. Один вид во всех парах (координаты, модуль, дроби, проценты).

    nl = NumLine(x0=30, x1=610, v0=-5, v1=5, y=60)
    body = nl.axis(step=1, labels=range(-5, 6)) + nl.point(-3, 'A', RED) + nl.jump(-3, 2, BLUE, '+5')
    """

    def __init__(self, x0, x1, v0, v1, y):
        self.x0, self.x1, self.v0, self.v1, self.y = x0, x1, v0, v1, y

    def x(self, v):
        return self.x0 + (v - self.v0) * (self.x1 - self.x0) / (self.v1 - self.v0)

    def axis(self, step=1, labels=None, fmt=str, stroke=MUTED, zero=True, arrow=True, size=13):
        y = self.y
        out = line(self.x0 - 12, y, self.x1 + 12, y, stroke, 1.8)
        if arrow:
            out += path([(self.x1 + 6, y - 6), (self.x1 + 14, y), (self.x1 + 6, y + 6)], stroke, 1.8,
                        closed=False)
        k, v = 0, self.v0
        while v <= self.v1 + 1e-9:
            xv = self.x(v)
            out += line(round(xv, 1), y - 6, round(xv, 1), y + 6, stroke, 1.4)
            v = self.v0 + (k := k + 1) * step
        for v in (labels if labels is not None else []):
            out += t(round(self.x(v), 1), y + 24, fmt(v), INK if (v == 0 and zero) else MUTED, size)
        return out

    def point(self, v, name=None, fill=GOLD, r=5, above=True, size=15):
        xv = self.x(v)
        out = dot(xv, self.y, r, fill)
        if name:
            out += t(round(xv, 1), self.y - 14 if above else self.y + 40, name, fill, size, weight=600)
        return out

    def seg(self, a, b, stroke=GOLD, sw=5, dy=0, extra=''):
        return line(round(self.x(a), 1), self.y + dy, round(self.x(b), 1), self.y + dy, stroke, sw,
                    f" stroke-linecap='round'{extra}")

    def jump(self, a, b, stroke=BLUE, text=None, h=26, marker=None, size=13):
        """Дуга-прыжок от a к b над прямой (сложение, сдвиг)."""
        xa, xb = self.x(a), self.x(b)
        mid = (xa + xb) / 2
        m = f" marker-end='url(#{marker})'" if marker else ''
        out = (f"<path d='M{xa:.1f},{self.y - 4} Q{mid:.1f},{self.y - 2 * h} {xb:.1f},{self.y - 4}' "
               f"fill='none' stroke='{stroke}' stroke-width='2'{m}/>")
        if text:
            out += t(round(mid, 1), self.y - h - 6, text, stroke, size)
        return out


class Plane:
    """Координатная плоскость: клетка cell px, начало O в (ox, oy) px; X(x), Y(y) — пиксели."""

    def __init__(self, xmin, xmax, ymin, ymax, cell=30, pad=24):
        self.xmin, self.xmax, self.ymin, self.ymax, self.c, self.pad = xmin, xmax, ymin, ymax, cell, pad
        self.w = (xmax - xmin) * cell + 2 * pad
        self.h = (ymax - ymin) * cell + 2 * pad

    def X(self, x):
        return self.pad + (x - self.xmin) * self.c

    def Y(self, y):
        return self.pad + (self.ymax - y) * self.c

    def P(self, x, y):
        return self.X(x), self.Y(y)

    def grid(self, stroke='#26303d', labels=True, size=12):
        out = ''
        for x in range(self.xmin, self.xmax + 1):
            out += line(self.X(x), self.Y(self.ymin), self.X(x), self.Y(self.ymax), stroke, 1)
        for y in range(self.ymin, self.ymax + 1):
            out += line(self.X(self.xmin), self.Y(y), self.X(self.xmax), self.Y(y), stroke, 1)
        ax = []
        if self.ymin <= 0 <= self.ymax:
            ax.append(line(self.X(self.xmin) - 6, self.Y(0), self.X(self.xmax) + 10, self.Y(0), MUTED, 1.8))
            ax.append(t(self.X(self.xmax) + 14, self.Y(0) - 8, 'x', MUTED, 14))
        if self.xmin <= 0 <= self.xmax:
            ax.append(line(self.X(0), self.Y(self.ymin) + 6, self.X(0), self.Y(self.ymax) - 10, MUTED, 1.8))
            ax.append(t(self.X(0) + 12, self.Y(self.ymax) - 10, 'y', MUTED, 14))
        out += ''.join(ax)
        if labels:
            for x in range(self.xmin, self.xmax + 1):
                if x:
                    out += t(self.X(x), self.Y(0) + 17, x, MUTED, size)
            for y in range(self.ymin, self.ymax + 1):
                if y:
                    out += t(self.X(0) - 9, self.Y(y) + 4, y, MUTED, size, anchor='end')
            out += t(self.X(0) - 9, self.Y(0) + 17, 0, MUTED, size, anchor='end')
        return out

    def svg(self, body, maxw=None):
        return svg(self.w + 20, self.h, body, maxw)


def cells(x, y, cols, rows, c=26, stroke='#2c394c', fill=None, sw=1):
    """Клетчатое поле cols × rows с левым верхним углом (x, y); fill = {(col, row): цвет} закрашивает клетки."""
    out = ''
    for (i, j), col in (fill or {}).items():
        out += rect(x + i * c, y + j * c, c, c, col, 'none', 0)
    for i in range(cols + 1):
        out += line(x + i * c, y, x + i * c, y + rows * c, stroke, sw)
    for j in range(rows + 1):
        out += line(x, y + j * c, x + cols * c, y + j * c, stroke, sw)
    return out


def bar(x, y, w, h, n, filled=(), fill=GOLD, stroke=MUTED, labels=None, size=13, opacity=0.85):
    """Полоса-целое из n равных частей; filled — номера закрашенных частей (0…n−1), labels — подписи в частях."""
    out = ''
    pw = w / n
    for k in range(n):
        if k in filled:
            out += rect(round(x + k * pw, 1), y, round(pw, 1), h, fill, 'none', 0,
                        extra=f" fill-opacity='{opacity}'")
    out += rect(x, y, w, h, 'none', stroke, 1.8)
    for k in range(1, n):
        out += line(round(x + k * pw, 1), y, round(x + k * pw, 1), y + h, stroke, 1.2)
    for k, s in enumerate(labels or []):
        if s != '':
            out += t(round(x + (k + 0.5) * pw, 1), y + h / 2 + 5, s, DARK if k in filled else INK, size)
    return out


def sets(items, size=15):
    """Вложенные/пересекающиеся множества-овалы: items = [(cx, cy, rx, ry, цвет, подпись, (lx, ly)), …]."""
    out = ''
    for cx, cy, rx, ry, col, name, (lx, ly) in items:
        out += (f"<ellipse cx='{cx}' cy='{cy}' rx='{rx}' ry='{ry}' fill='{col}' fill-opacity='0.10' "
                f"stroke='{col}' stroke-width='2'/>")
        out += t(lx, ly, name, col, size, weight=600)
    return out


def height(v, a, b, stroke=GOLD, dash='5 4', label=None, ext=MUTED, s=11):
    """Высота из вершины v на прямую ab: пунктир со знаком прямого угла. → (svg, foot).

    Если основание высоты падает вне отрезка ab (тупой угол), продолжение ab до него дорисовывается пунктиром ext —
    общий случай рисуется общим. label — подпись у середины высоты (например 'h').
    """
    dx, dy = b[0] - a[0], b[1] - a[1]
    k = ((v[0] - a[0]) * dx + (v[1] - a[1]) * dy) / (dx * dx + dy * dy)
    foot = (a[0] + k * dx, a[1] + k * dy)
    out = ''
    if k < 0 or k > 1:
        near = a if k < 0 else b
        out += path([near, foot], ext, 1.5, closed=False, dash='4 4')
    out += path([v, foot], stroke, 2, closed=False, dash=dash)
    other = b if abs(k) < abs(k - 1) else a          # прямой угол рисуется в сторону лежащего на прямой отрезка
    if (other[0] - foot[0]) ** 2 + (other[1] - foot[1]) ** 2 < 1:
        other = a
    out += right_angle(foot, v, other, s, stroke)
    if label:
        mx, my = (v[0] + foot[0]) / 2, (v[1] + foot[1]) / 2
        nx, ny = -(foot[1] - v[1]), foot[0] - v[0]
        n = math.hypot(nx, ny) or 1
        out += t(round(mx + nx / n * 12, 1), round(my + ny / n * 12 + 5, 1), label, stroke, 15)
    return out, foot
