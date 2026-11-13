"""Общая часть рисунков учебника «Геометрия» (6 класс): текст MD, проверки, геометрические помощники, solid.

Углы — в градусах, как в математике: 0° — вправо, против часовой — положительно (на экране y вниз, это учтено в pol).
"""
import itertools, math, os, re

from common import (svg, fig, row, t, g, rect, line, path, dot, circle, label, angle_arc, right_angle, ticks, dim,
                    cells, bar, sets, height, brace, turn, flip, arrow_defs_p,
                    GOLD, BLUE, GREEN, RED, VIOLET, CYAN, PINK, GREY, INK, MUTED, DARK)

HERE = os.path.dirname(os.path.abspath(__file__))
MDP = os.path.join(HERE, '..', 'math6_1_geometriya_uchebnik.md')
VIS = os.path.join(HERE, '..', 'math6_1_geometriya_uchebnik.vis.json')
MD = open(MDP).read()


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', s)).strip()


def need(*ss):
    """Строка (число, запись) действительно стоит в тексте MD."""
    for s in ss:
        assert s in MD, f'нет в MD: {s!r}'


CODE = re.findall(r'```\n(.*?)```', MD, re.S)


def ascii_tokens(anchor):
    """Буквы и числа ASCII-блока, в котором стоит якорь замены."""
    bl = [b for b in CODE if anchor in norm(b)]
    assert len(bl) >= 1, anchor
    return set(re.findall(r'[A-Za-zА-Яа-яЁё0-9₀-₉]+', bl[0]))


def svg_text(s):
    return ' '.join(re.findall(r'>([^<>]+)</text>', s))


DOT = '1.5 6'      # пунктир точками (с круглыми концами)
DASH = '8 6'       # пунктир чёрточками
LS = 16            # буквы точек
NS = 15            # числа и подписи


def pol(c, r, deg):
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] - r * math.sin(a))


def ang_of(c, p):
    return math.degrees(math.atan2(c[1] - p[1], p[0] - c[0])) % 360


def mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def lerp(p, q, k):
    return (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)


def add(p, v):
    return (p[0] + v[0], p[1] + v[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def reflect(p, a, b):
    """Отражение точки p в прямой ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    k = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    f = (a[0] + k * dx, a[1] + k * dy)
    return (2 * f[0] - p[0], 2 * f[1] - p[1])


def rot(p, c, deg):
    """Поворот точки p вокруг c на deg (против часовой — положительно, как в pol)."""
    a = math.radians(deg)
    dx, dy = p[0] - c[0], -(p[1] - c[1])
    return (c[0] + dx * math.cos(a) - dy * math.sin(a), c[1] - (dx * math.sin(a) + dy * math.cos(a)))


def foot(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    k = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    return (a[0] + k * dx, a[1] + k * dy)


def inter_cc(c1, r1, c2, r2):
    """Точки пересечения двух окружностей (сначала верхняя на экране)."""
    d = dist(c1, c2)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    m = lerp(c1, c2, a / d)
    ux, uy = (c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d
    p1, p2 = (m[0] - uy * h, m[1] + ux * h), (m[0] + uy * h, m[1] - ux * h)
    return (p1, p2) if p1[1] < p2[1] else (p2, p1)


def inter_ll(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / den, (a * (y3 - y4) - (y1 - y2) * b) / den)


def tri_angles(A, a, b, L):
    """Треугольник на основании A→(A.x+L) с углами a (у A) и b (у второго конца): (A, B, C)."""
    B = (A[0] + L, A[1])
    ac = L * math.sin(math.radians(b)) / math.sin(math.radians(a + b))
    return A, B, pol(A, ac, a)


def tri_sides(P, c, b, a):
    """Треугольник на основании P→(P.x+c): сторона от P до вершины = b, от второго конца = a."""
    x = (b * b + c * c - a * a) / (2 * c)
    y = math.sqrt(b * b - x * x)
    return P, (P[0] + c, P[1]), (P[0] + x, P[1] - y)


def regpoly(c, R, n, start=90):
    return [pol(c, R, start + 360 * k / n) for k in range(n)]


# ——— рисование ———

def tx(x, y, s, fill=INK, size=NS, anchor='middle', weight=None, extra=''):
    return t(round(x, 1), round(y, 1), s, fill, size, anchor, weight, extra=extra)


def seg(p, q, col=INK, sw=2.2, dash=None, cls=None, d=None, extra=''):
    da = f" stroke-dasharray='{dash}'" if dash else ''
    lc = " stroke-linecap='round'" if dash == DOT else ''
    c = f" class='{cls}' pathLength='100' style='--d:{d}s'" if cls else ''
    return (f"<line x1='{p[0]:.1f}' y1='{p[1]:.1f}' x2='{q[0]:.1f}' y2='{q[1]:.1f}' stroke='{col}' "
            f"stroke-width='{sw}'{da}{lc}{c}{extra}/>")


def arrow(p, q, col, mk, sw=2.2, dash=None):
    """Отрезок со стрелкой на конце q; mk — id маркера (из arrow_defs_p)."""
    return seg(p, q, col, sw, dash, extra=f" marker-end='url(#{mk})'")


def poly(pts, stroke=INK, fill='none', op=0.3, sw=2.2, dash=None, closed=True):
    ex = f" fill-opacity='{op}'" if fill != 'none' else ''
    return path(pts, stroke, sw, fill, closed, dash, ex)


def arc(c, r, a1, a2, col=GOLD, sw=2.2, dash=None, cls=None, d=None, dur=None):
    """Дуга окружности (c, r) от угла a1 до a2 против часовой."""
    sweep = (a2 - a1) % 360 or 360
    if sweep >= 359.99:
        a2 = a1 + 359.9
        sweep = 359.9
    p1, p2 = pol(c, r, a1), pol(c, r, a1 + sweep)
    large = 1 if sweep > 180 else 0
    da = f" stroke-dasharray='{dash}'" if dash else ''
    st = ''
    if cls:
        st = f" class='{cls}' pathLength='100' style='--d:{d}s" + (f";--dur:{dur}s'" if dur else "'")
    return (f"<path d='M{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 {large} 0 {p2[0]:.1f},{p2[1]:.1f}' "
            f"fill='none' stroke='{col}' stroke-width='{sw}'{da}{st}/>")


def sector(c, r, a1, a2, col=GOLD, op=0.35, stroke=None, sw=1.5):
    sweep = (a2 - a1) % 360
    p1, p2 = pol(c, r, a1), pol(c, r, a1 + sweep)
    large = 1 if sweep > 180 else 0
    return (f"<path d='M{c[0]:.1f},{c[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f} A{r:.1f},{r:.1f} 0 {large} 0 "
            f"{p2[0]:.1f},{p2[1]:.1f} Z' fill='{col}' fill-opacity='{op}' stroke='{stroke or col}' "
            f"stroke-width='{sw}'/>")


def angmark(c, a1, a2, r=26, col=GOLD, text=None, tcol=None, size=NS, tr=None, fillop=None):
    """Дуга угла от луча a1 до луча a2 (против часовой) и подпись по биссектрисе."""
    out = sector(c, r, a1, a2, col, fillop, 'none', 0) if fillop else ''
    out += arc(c, r, a1, a2, col)
    if text:
        am = a1 + ((a2 - a1) % 360) / 2
        p = pol(c, tr or r + 17, am)
        out += tx(p[0], p[1] + size * 0.35, text, tcol or col, size)
    return out


def pname(p, s, dx=0, dy=0, col=INK, size=LS):
    """Имя точки со сдвигом (dx, dy) от неё."""
    return tx(p[0] + dx, p[1] + dy + size * 0.35, s, col, size, weight=600)


def chevron(p, q, n=1, col=GOLD, size=7, sw=2):
    """Значок параллельности: n шевронов «>» посередине pq, остриём к q."""
    m = mid(p, q)
    L = dist(p, q)
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    out = ''
    for k in range(n):
        o = (k - (n - 1) / 2) * 7
        tip = (m[0] + ux * (o + size / 2), m[1] + uy * (o + size / 2))
        b1 = (tip[0] - ux * size - uy * size, tip[1] - uy * size + ux * size)
        b2 = (tip[0] - ux * size + uy * size, tip[1] - uy * size - ux * size)
        out += path([b1, tip, b2], col, sw, closed=False)
    return out


PHONE = 328        # ширина колонки рисунка на телефоне, px
MIN_PX = 11        # подпись на телефоне не мельче


def S(w, h, body):
    """svg с проверкой шрифта: на телефоне viewBox w ужимается до PHONE px — мелкие подписи поднимаются до MIN_PX."""
    lo = math.ceil(MIN_PX * w / PHONE * 10) / 10

    def fix(m):
        v = float(m.group(1))
        return f"font-size='{max(v, lo):g}'"
    body = re.sub(r"font-size='([\d.]+)'", fix, body)
    return svg(w, h, body)


# ——— пространственные фигуры ———

def hull_faces(V):
    """Грани выпуклого многогранника по вершинам: [(индексы против часовой снаружи), …]."""
    n = len(V)
    cen = [sum(v[i] for v in V) / n for i in range(3)]
    faces, seen = [], set()

    def subv(a, b): return [a[i] - b[i] for i in range(3)]
    def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    def dotv(a, b): return sum(a[i] * b[i] for i in range(3))

    for i, j, k in itertools.combinations(range(n), 3):
        nrm = cross(subv(V[j], V[i]), subv(V[k], V[i]))
        L = math.sqrt(dotv(nrm, nrm))
        if L < 1e-9:
            continue
        nrm = [x / L for x in nrm]
        if dotv(nrm, subv(V[i], cen)) < 0:
            nrm = [-x for x in nrm]
        ds = [dotv(nrm, subv(V[m], V[i])) for m in range(n)]
        if max(ds) > 1e-6:
            continue
        on = frozenset(m for m in range(n) if abs(ds[m]) < 1e-6)
        if on in seen:
            continue
        seen.add(on)
        fc = [sum(V[m][q] for m in on) / len(on) for q in range(3)]
        u = subv(V[next(iter(on))], fc)
        w = cross(nrm, u)

        def key(m):
            r = subv(V[m], fc)
            return math.atan2(dotv(r, w), dotv(r, u))
        faces.append(sorted(on, key=key))       # против часовой, если смотреть снаружи (с конца nrm)
    return faces


def rot_proj(yaw, pitch, s, ox, oy):
    """Параллельная проекция после поворота: yaw вокруг вертикали, pitch — наклон к зрителю (сверху)."""
    cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def P(v):
        x, y, z = v
        x1, z1 = x * cy_ + z * sy_, -x * sy_ + z * cy_
        y2 = y * cp - z1 * sp
        return (ox + s * x1, oy - s * y2)
    return P


def obl_proj(s, depth, ox, oy, zfront, deg=45):
    """Кабинетная проекция главы 6: z = zfront — передняя грань; глубина уходит вверх-вправо под deg, укорочена в depth раз."""
    c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg))

    def P(v):
        x, y, z = v
        k = depth * (zfront - z)
        return (ox + s * (x + k * c), oy - s * (y + k * sn))
    return P


def solid(V, P, faces=None, col=INK, sw=2.2, hcol=None, hdash=DASH, ecol=None, estyle=None, fills=None):
    """Многогранник: видимые рёбра сплошные, невидимые пунктиром.

    Грани против часовой снаружи (для выпуклого считаются сами). Видимая грань при параллельной проекции сохраняет
    знак площади; ребро видимо, если принадлежит хотя бы одной видимой грани.
    ecol {(i, j): цвет}, estyle {(i, j): dash} — подсветка рёбер; fills {номер грани или кортеж вершин: (цвет, op)}.
    → (svg, экранные точки, видимые грани, рёбра {(i, j): видно?}).
    """
    faces = faces or hull_faces(V)
    Q = [P(v) for v in V]

    def area(f):
        a = 0
        for k in range(len(f)):
            (x1, y1), (x2, y2) = Q[f[k]], Q[f[(k + 1) % len(f)]]
            a += x1 * (-y2) - x2 * (-y1)        # в математических координатах (y вверх)
        return a / 2
    vis = [area(f) > 1e-6 for f in faces]
    edges = {}
    for f, v in zip(faces, vis):
        for k in range(len(f)):
            e = tuple(sorted((f[k], f[(k + 1) % len(f)])))
            edges[e] = edges.get(e, False) or v
    out = ''
    for key, (c, op) in (fills or {}).items():
        f = faces[key] if isinstance(key, int) else list(key)
        out += poly([Q[m] for m in f], 'none', c, op, 0)
    ecol, estyle = ecol or {}, estyle or {}
    for e, v in sorted(edges.items(), key=lambda kv: kv[1]):
        c = ecol.get(e, col if v else (hcol or col))
        dsh = estyle.get(e, None if v else hdash)
        out += seg(Q[e[0]], Q[e[1]], c, sw if v else sw * 0.8, dsh)
    return out, Q, [f for f, v in zip(faces, vis) if v], edges


# ——— тела вращения ———

def ell(cx, cy, rx, ry, col=INK, sw=2.2, back_dash=DASH, fill='none', op=0.3, full=False):
    """Эллипс-окружность тела: передняя половина сплошная, задняя пунктиром (или вся сплошная при full)."""
    if full:
        fo = f" fill-opacity='{op}'" if fill != 'none' else ''
        return (f"<ellipse cx='{cx:.1f}' cy='{cy:.1f}' rx='{rx:.1f}' ry='{ry:.1f}' fill='{fill}'{fo} stroke='{col}' "
                f"stroke-width='{sw}'/>")
    fr = (f"<path d='M{cx - rx:.1f},{cy:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {cx + rx:.1f},{cy:.1f}' fill='none' "
          f"stroke='{col}' stroke-width='{sw}'/>")
    bk = (f"<path d='M{cx - rx:.1f},{cy:.1f} A{rx:.1f},{ry:.1f} 0 0 1 {cx + rx:.1f},{cy:.1f}' fill='none' "
          f"stroke='{col}' stroke-width='{sw * 0.8}' stroke-dasharray='{back_dash}'/>")
    return fr + bk


def cylinder(cx, ytop, r, h, k=0.28, col=INK, fill=None, op=0.18):
    ry = r * k
    out = ''
    if fill:
        out += (f"<path d='M{cx - r:.1f},{ytop:.1f} L{cx - r:.1f},{ytop + h:.1f} A{r:.1f},{ry:.1f} 0 0 0 "
                f"{cx + r:.1f},{ytop + h:.1f} L{cx + r:.1f},{ytop:.1f} A{r:.1f},{ry:.1f} 0 0 1 {cx - r:.1f},{ytop:.1f}Z' "
                f"fill='{fill}' fill-opacity='{op}' stroke='none'/>")
    out += ell(cx, ytop, r, ry, col, full=True)
    out += ell(cx, ytop + h, r, ry, col)
    out += seg((cx - r, ytop), (cx - r, ytop + h), col) + seg((cx + r, ytop), (cx + r, ytop + h), col)
    return out


def cone(cx, yapex, r, h, k=0.28, col=INK, fill=None, op=0.18):
    ry = r * k
    yb = yapex + h
    out = ''
    if fill:
        out += (f"<path d='M{cx:.1f},{yapex:.1f} L{cx - r:.1f},{yb:.1f} A{r:.1f},{ry:.1f} 0 0 0 {cx + r:.1f},{yb:.1f} Z' "
                f"fill='{fill}' fill-opacity='{op}' stroke='none'/>")
    out += ell(cx, yb, r, ry, col)
    out += seg((cx, yapex), (cx - r, yb), col) + seg((cx, yapex), (cx + r, yb), col)
    return out


def sphere(cx, cy, r, k=0.28, col=INK, fill=None, op=0.18):
    out = circle(cx, cy, r, col, 2.2, fill or 'none', extra=f" fill-opacity='{op}'" if fill else '')
    return out + ell(cx, cy, r, r * k, col)


FIGS = {}


def at(anchor, fx=False, zamena=False):
    """Регистрация рисунка: якорь → функция, возвращающая (svg, подпись)."""
    def deco(f):
        FIGS[anchor] = (f, fx, zamena)
        return f
    return deco
