"""Часть A — десятичные дроби: ритуалы и главы 1–11."""
from desyatichnye_geom_prim import *


# ——— Ритуалы ———

def r1_tails():
    has('3,5 = 3,50 = 3,500')
    assert D('3.5') == D('3.50') == D('3.500')
    G = Grid(70, step=64)
    b = [t(G.cx(p), 22, PNAME[p] if p else 'единицы', pcol(p), 12.5) for p in (0, -1, -2, -3)]
    for k, s in enumerate(['3,5', '3,50', '3,500']):
        y = 36 + k * 56
        n = len(s.split(',')[1])
        zeros = tuple(range(-2, -n - 1, -1))
        b.append(G.number(y, s, dim=zeros, dashed=zeros))
        if k:
            b.append(t(40, y + 30, '=', INK, 22))
    return fig(svg(320, 200, ''.join(b)))


def r3_estimate():
    has('19,8 + 4,95', '20 + 5 = 25', '2,475', '247,5')
    assert round(D('19.8')) == 20 and round(D('4.95')) == 5
    b = [arrow_defs_p('r3', [GREEN])]
    for (a, z, v, x0) in [(19, 20, '19,8', 30), (4, 5, '4,95', 250)]:
        f = nline(x0, x0 + 180, 56, a, z)
        b.append(line(x0, 56, x0 + 180, 56, MUTED, 2))
        for k in range(11):
            xx = f(F(a) + F(k, 10))
            b.append(line(xx, 50 if k % 5 else 46, xx, 62 if k % 5 else 66, MUTED, 1.3))
        b.append(t(x0, 84, str(a), MUTED, 14) + t(x0 + 180, 84, str(z), MUTED, 14))
        xv = f(F(D(v.replace(',', '.'))))
        b.append(t(xv, 34, v, GOLD, 15, weight=700))
        b.append(f"<circle cx='{xv}' cy='56' r='7' fill='{GOLD}' fill-opacity='0.3'/>")
        b.append(slide(0.6, x0 + 180 - xv, 0, dot(xv, 56, GOLD, 7)))
        b.append(fi(1.9, t(x0 + 180, 84, str(z), GREEN, 15, weight=700)))
    b.append(t(226, 120, '19,8 + 4,95 ≈', INK, 18, anchor='end', weight=700))
    b.append(fi(2.4, t(234, 120, '20 + 5 = 25', GREEN, 18, anchor='start', weight=700)))
    f = nline(30, 430, 190, 0, 250)
    b.append(line(30, 190, 430, 190, MUTED, 2))
    for v in (0, 50, 100, 150, 200, 250):
        b.append(line(f(v), 184, f(v), 196, MUTED, 1.3))
    b.append(t(f(0) - 10, 195, '0', MUTED, 13, anchor='end') + t(f(250), 214, '250', MUTED, 13))
    b.append(fi(2.8, f"<rect x='{f(18)}' y='180' width='{f(32)-f(18)}' height='20' rx='4' fill='{GREEN}' "
                     f"fill-opacity='0.25'/>" + dot(f(25), 190, GREEN) + t(f(25), 172, '25', GREEN, 15, weight=700)))
    b.append(fi(3.6, dot(f(F(2475, 1000)), 190, RED) + t(f(F(2475, 1000)), 220, '2,475', RED, 14, weight=700)
                + dot(f(F(2475, 10)), 190, RED) + t(f(F(2475, 10)), 172, '247,5', RED, 14, anchor='end', weight=700)))
    return fig(svg(460, 232, ''.join(b)), fx=True)


# ——— Глава 1 ———

def g1_places():
    G = Grid(60, step=76)
    s = '3,472'
    b = [G.number(14, s, h=50, size=28)]
    for p, name in [(0, 'целые'), (-1, 'десятые'), (-2, 'сотые'), (-3, 'тысячные')]:
        b.append(t(G.cx(p), 92, name, pcol(p), 14, weight=600))
    return fig(svg(380, 106, ''.join(b)))


def g1_sum():
    has('3 + 4/10 + 7/100 + 2/1000')
    assert D('3.472') == 3 + D(4) / 10 + D(7) / 100 + D(2) / 1000
    G = Grid(20, step=40, gap=12)
    y = 40
    b = [G.number(y, '3,472')]
    srcy = y + CH / 2 + 22 * 0.36
    ybar, size = 74, 22
    b.append(t(214, ybar + 8, '=', INK, 24))
    xs = {0: 246, -1: 296, -2: 361, -3: 441}
    dens = {-1: '10', -2: '100', -3: '1000'}
    for p, ch in digits('3,472').items():
        c = pcol(p)
        ty = ybar + 8 if p == 0 else ybar - 6
        b.append(slide(0.5, xs[p] - G.cx(p), ty - srcy, t(G.cx(p), srcy, ch, c, size, weight=700)))
        if p:
            w = len(dens[p]) * size * 0.62 + 8
            b.append(fi(1.9, line(xs[p] - w / 2, ybar, xs[p] + w / 2, ybar, c, 2)
                        + t(xs[p], ybar + size + 2, dens[p], c, size, weight=700)))
    for xp in (266, 326, 398):
        b.append(fi(1.9, t(xp, ybar + 8, '+', INK, 22)))
    return fig(svg(490, 124, ''.join(b), maxw=490), fx=True)


def g1_both_sides():
    has('12,008', 'Пойдёшь влево', 'Пойдёшь вправо')
    G = Grid(30 + 2 * 66, step=66, gap=16)
    b = [arrow_defs_p('g1b', [MUTED])]
    b.append(cell(G.x(2), 40, '', pcol(2), dashed=True))
    b.append(G.number(40, '12,008'))
    for p in range(2, -4, -1):
        b.append(t(G.cx(p), 104, PNAME[p], pcol(p), 12.5, weight=600))
    cx = G.comma_x()
    b.append(line(cx, 14, cx, 30, INK, 2))
    b.append(arrow(cx - 8, 22, G.x(2) + 4, 22, 'g1b0', MUTED, 1.8) + t((cx + G.x(2)) / 2, 16, 'влево', MUTED, 13))
    b.append(arrow(cx + 8, 22, G.x(-3) + CW - 4, 22, 'g1b0', MUTED, 1.8)
             + t((cx + G.x(-3) + CW) / 2, 16, 'вправо', MUTED, 13))
    return fig(svg(440, 116, ''.join(b)))


def g1_rule():
    rows = [(None, 7, 10, '0,7'), (None, 7, 100, '0,07'), (None, 7, 1000, '0,007'), (2, 3, 100, '2,03')]
    for whole, n, d, s in rows:
        assert F(D(s.replace(',', '.'))) == (whole or 0) + F(n, d)
        has(s, (f'{whole} ' if whole else '') + f'{n}/{d}')
    b = [arrow_defs_p('g1r', [MUTED])]
    size, cw = 20, 12
    for k, (whole, n, d, s) in enumerate(rows):
        yc = 44 + k * 72
        fx_ = 76
        if whole:
            b.append(t(40, yc + 8, str(whole), INK, 22, weight=700))
        den = str(d)
        x0 = fx_ - len(den) * cw / 2
        b.append(t(fx_, yc - 6, str(n), INK, size, weight=700) + line(fx_ - 26, yc, fx_ + 26, yc, INK, 2))
        zx = []
        for j, ch in enumerate(den):
            xc = x0 + cw * j + cw / 2
            b.append(t(xc, yc + size + 2, ch, INK, size, weight=700))
            if ch == '0':
                zx.append(xc)
        b.append(t(140, yc + 8, '=', INK, 24))
        ip, fp = s.split(',')
        b.append(cell(170, yc - 22, ip, pcol(0), txt=MUTED if ip == '0' else None))
        b.append(comma(170 + CW + 11, yc + 18, INK))
        sy = yc + 28
        for j, ch in enumerate(fp):
            p = -1 - j
            x = 226 + 42 * j
            b.append(cell(x, yc - 22, '', pcol(p)))
            b.append(fi(1.9 if ch != '0' else 2.4, t(x + CW / 2, yc + 8, ch, MUTED if ch == '0' else pcol(p), 22,
                                                         weight=700)))
            bar = f"<rect x='{zx[j]-5}' y='{yc+size+7}' width='10' height='3.5' rx='1' fill='{BLUE}'/>"
            b.append(f"<g opacity='0.35'>{bar}</g>")
            b.append(slide(0.5 + 0.15 * j, x + CW / 2 - zx[j], sy - (yc + size + 7), bar))
    return fig(svg(380, 316, ''.join(b)), fx=True)


# ——— Глава 2 ———

def g2_to_common():
    has('0,45', '45/100', '9/20')
    assert F(D('0.45')) == F(45, 100) == F(9, 20) and 45 // 5 == 9 and 100 // 5 == 20
    b = [arrow_defs_p('g2a', [BLUE])]
    y = 34
    b.append(cell(20, y, '0', pcol(0), txt=MUTED) + comma(20 + CW + 7, y + CH - 4)
             + cell(68, y, '4', pcol(-1)) + cell(108, y, '5', pcol(-2)))
    b.append(t(172, 64, '=', INK, 24))
    xc, yb, cw = 230, 56, 12
    b.append(t(xc, yb - 6, '45', INK, 20, weight=700) + line(xc - 24, yb, xc + 24, yb, INK, 2))
    den_x = [xc - 1.5 * cw + cw * j + cw / 2 for j in range(3)]
    for j, ch in enumerate('100'):
        b.append(t(den_x[j], yb + 22, ch, INK, 20, weight=700))
    for j, sx in enumerate([68 + CW / 2, 108 + CW / 2]):
        bar = f"<rect x='{sx-5}' y='{y+CH+6}' width='10' height='3.5' rx='1' fill='{BLUE}'/>"
        b.append(f"<g opacity='0.35'>{bar}</g>")
        b.append(slide(0.5, den_x[j + 1] - sx, (yb + 27) - (y + CH + 6), bar))
    b.append(fi(2.0, t(292, 64, '=', INK, 24)
                + arc_hop(250, 336, yb - 26, 16, 'g2a0', BLUE) + t(293, yb - 40, ': 5', BLUE, 16, weight=700)
                + f"<path d='M256 {yb+30} Q 296 {yb+50} 336 {yb+30}' fill='none' stroke='{BLUE}' stroke-width='2' "
                  f"marker-end='url(#g2a0)'/>" + t(296, yb + 62, ': 5', BLUE, 16, weight=700)))
    b.append(fi(2.6, frac(356, yb, '9', '20', GREEN, 20)))
    return fig(svg(400, 128, ''.join(b)), fx=True)


def g2_quarters():
    has('75/100', '0,75', '100 : 4 = 25')
    assert F(3, 4) == F(75, 100) and 100 // 4 == 25
    c, y0 = 16, 16

    def square(x0, fine_d=None):
        out = []
        for qi, (qx, qy) in enumerate([(0, 0), (5, 0), (0, 5)]):
            out.append(box(x0 + qx * c, y0 + qy * c, 5 * c, 5 * c, GOLD, op=0.32, sw=0))
        if fine_d is not None:
            out.append(fi(fine_d, ''.join(line(x0 + k * c, y0, x0 + k * c, y0 + 10 * c, MUTED, 0.8)
                                          + line(x0, y0 + k * c, x0 + 10 * c, y0 + k * c, MUTED, 0.8)
                                          for k in range(1, 10) if k != 5)))
        out.append(rect(x0, y0, 10 * c, 10 * c, 'none', INK, 2.5)
                   + line(x0 + 5 * c, y0, x0 + 5 * c, y0 + 10 * c, INK, 2.5)
                   + line(x0, y0 + 5 * c, x0 + 10 * c, y0 + 5 * c, INK, 2.5))
        return ''.join(out)

    xl, xr = 30, 240
    b = [square(xl), frac(xl + 5 * c, y0 + 10 * c + 26, '3', '4', GOLD, 20)]
    b.append(t(xl + 10 * c + 25, y0 + 5 * c + 8, '=', INK, 26))
    b.append(square(xr, fine_d=1.0))
    b.append(fi(1.5, ''.join(t(xr + qx * c + 2.5 * c, y0 + qy * c + 2.5 * c + 6, '25', BLUE, 17, weight=700)
                             for qx, qy in [(0, 0), (5, 0), (0, 5), (5, 5)])))
    b.append(fi(2.2, t(xr + 5 * c - 8, y0 + 10 * c + 34, '75/100', INK, 20, anchor='end', weight=700)))
    b.append(fi(2.8, t(xr + 5 * c, y0 + 10 * c + 34, '= 0,75', GREEN, 20, anchor='start', weight=700)))
    return fig(svg(440, 240, ''.join(b)), fx=True)


def chip(x, y, n, stroke=None):
    col = {2: VIOLET, 5: CYAN, 3: RED}[n]
    st = stroke or col
    return (f"<rect x='{x}' y='{y}' width='30' height='30' rx='7' fill='{col}' stroke='{st}' stroke-width='2.5'/>"
            + t(x + 15, y + 21, str(n), DARK, 17, weight=700))


def g2_factors():
    has('100 = 2 × 2 × 5 × 5', '20 = 2 × 2 × 5', 'тройку из знаменателя не убрать')
    assert 2 * 2 * 5 * 5 == 100 and 2 * 2 * 5 == 20 and 20 * 5 == 100 and 100 % 3 and 10 % 3 and 1000 % 3
    b = []
    rows = [('100 =', [2, 2, 5, 5], 16), ('20 =', [2, 2, 5], 74)]
    for lab, fs, y in rows:
        b.append(t(78, y + 21, lab, INK, 17, anchor='end', weight=600))
        for j, n in enumerate(fs):
            b.append(chip(92 + 38 * j, y, n))
    y3 = 132
    b.append(t(118, y3 + 21, '20 × 5 =', INK, 17, anchor='end', weight=600))
    for j, n in enumerate([2, 2, 5]):
        b.append(slide(0.5, 132 + 38 * j - (92 + 38 * j), y3 - 74, chip(92 + 38 * j, 74, n)))
    b.append(slide(1.3, 132 + 38 * 3 - 380, 0, chip(380, y3, 5, stroke=BLUE)))
    b.append(fi(2.6, t(290, y3 + 21, '= 100', GREEN, 18, anchor='start', weight=700)))
    y4 = 190
    b.append(t(78, y4 + 21, '3 =', INK, 17, anchor='end', weight=600) + chip(92, y4, 3))
    b.append(t(140, y4 + 21, 'тройку не убрать', RED, 16, anchor='start', weight=600))
    return fig(svg(420, 234, ''.join(b)), fx=True)


# ——— Глава 3 ———

def g3_compare():
    has('0,70 и 0,68', '70 > 68', '0,7 > 0,68')
    assert D('0.7') > D('0.68') and D('0.70') == D('0.7')
    L = Grid(30, step=46, gap=12)
    R = Grid(232, step=52, gap=12)
    y1, y2 = 36, 92
    b = [t(R.cx(p), 22, PNAME[p], pcol(p), 13) for p in (0, -1, -2)]
    b.append(L.number(y1, '0,7', dim=(0,)) + L.number(y2, '0,68', dim=(0,)))
    for y in (y1, y2):
        b.append(t(204, y + 30, '=', INK, 24))
    b.append(R.number(y1, '0,7', dim=(0,)) + cell(R.x(-2), y1, '', pcol(-2), dashed=True))
    b.append(fi(0.6, t(R.cx(-2), y1 + 30, '0', MUTED, 22, weight=700)))
    b.append(R.number(y2, '0,68', dim=(0,)))
    xa, xb = R.x(-1) - 6, R.x(-2) + CW + 6
    b.append(fi(1.6, ''.join(box(xa, y - 6, xb - xa, CH + 12, GOLD, op=0, sw=2.5, rx=8) for y in (y1, y2))
                + t(xb + 12, y1 + 30, '70', GOLD, 20, anchor='start', weight=700)
                + t(xb + 12, y2 + 30, '68', GOLD, 20, anchor='start', weight=700)))
    b.append(fi(2.2, t(220, 180, '70 > 68', GOLD, 19, weight=700)))
    b.append(fi(2.8, t(220, 208, '0,7 > 0,68', GREEN, 20, weight=700)))
    return fig(svg(460, 222, ''.join(b)), fx=True)


def g3_between():
    has('0,30 и 0,40', '0,31', '0,39', '0,300 и 0,310', '0,301')
    L, R_ = 50, 410
    f1 = nline(L, R_, 50, F(30, 100), F(40, 100))
    f2 = nline(L, R_, 150, F(300, 1000), F(310, 1000))
    b = [line(L, 50, R_, 50, MUTED, 2), line(L, 150, R_, 150, MUTED, 2)]
    for y in (50, 150):
        b.append(line(L, y - 8, L, y + 8, INK, 2) + line(R_, y - 8, R_, y + 8, INK, 2))
    b.append(t(L, 30, '0,30', INK, 15, weight=700) + t(R_, 30, '0,40', INK, 15, weight=700))
    b.append(t(L - 8, 155, '0,300', INK, 14, anchor='end', weight=700)
             + t(R_ + 8, 155, '0,310', INK, 14, anchor='start', weight=700))
    tk1 = ''.join(line(f1(F(k, 100)), 44, f1(F(k, 100)), 56, GREEN, 1.6)
                  + t(f1(F(k, 100)), 74, f'0,{k}', GREEN, 11.5) for k in range(31, 40))
    b.append(fi(0.6, tk1))
    b.append(fi(1.8, f"<rect x='{f1(F(30,100))}' y='45' width='{f1(F(31,100))-f1(F(30,100))}' height='10' "
                     f"fill='{GOLD}' fill-opacity='0.5'/>"
                + f"<path d='M{f1(F(30,100))} 58 L{L} 138 M{f1(F(31,100))} 80 L{R_} 138' stroke='{GOLD}' "
                  f"stroke-width='1.3' stroke-dasharray='4 4' fill='none'/>"))
    tk2 = ''.join(line(f2(F(k, 1000)), 144, f2(F(k, 1000)), 156, CYAN, 1.6)
                  + t(f2(F(k, 1000)), 174, f'0,{k}', CYAN, 11.5) for k in range(301, 310))
    b.append(fi(2.6, tk2))
    return fig(svg(460, 186, ''.join(b)), fx=True)


def g3_length():
    assert D('0.7') > D('0.68')
    b = []
    G = Grid(20, step=40, gap=12)
    f = nline(180, 460, 0, 0, 1)
    for k, s in enumerate(['0,7', '0,68']):
        y = 16 + k * 62
        b.append(G.number(y, s, dim=(0,)))
        v = F(D(s.replace(',', '.')))
        b.append(box(180, y + 10, f(v) - 180, 24, GREEN, op=0.35, sw=1.5))
        b.append(t(f(v) + 14, y + 28, s, GREEN, 15, anchor='start', weight=700))
    b.append(line(f(F(7, 10)), 18, f(F(7, 10)), 112, GREEN, 1.3, " stroke-dasharray='4 3'"))
    b.append(line(180, 136, 460, 136, MUTED, 1.5))
    for k in range(11):
        b.append(line(f(F(k, 10)), 132, f(F(k, 10)), 140, MUTED, 1.2))
    b.append(t(180, 158, '0', MUTED, 13) + t(460, 158, '1', MUTED, 13))
    return fig(svg(500, 166, ''.join(b), maxw=500))


# ——— Глава 4 ———

def g4_nearest():
    has('3,472 ≈ 3,5')
    f = nline(30, 430, 60, F(340, 100), F(350, 100))
    b = [line(30, 60, 430, 60, MUTED, 2)]
    for k in range(11):
        xx = f(F(340 + k, 100))
        big = k in (0, 5, 10)
        b.append(line(xx, 60 - (10 if big else 5), xx, 60 + (10 if big else 5), INK if big else MUTED, 2 if big else 1.2))
    b.append(t(30, 92, '3,4', INK, 16, weight=700) + t(430, 92, '3,5', INK, 16, weight=700)
             + t(230, 92, '3,45', MUTED, 14))
    b.append(line(230, 30, 230, 72, MUTED, 1.2, " stroke-dasharray='4 3'"))
    xv = f(F(3472, 1000))
    b.append(t(xv, 34, '3,472', GOLD, 15, weight=700))
    b.append(f"<circle cx='{xv}' cy='60' r='7' fill='{GOLD}' fill-opacity='0.3'/>")
    b.append(slide(0.8, 430 - xv, 0, dot(xv, 60, GOLD, 7)))
    b.append(fi(2.2, t(230, 128, '3,472 ≈ 3,5', GREEN, 19, weight=700)))
    return fig(svg(460, 142, ''.join(b)), fx=True)


def digit_swap(x, y, old, new, d, col_old, col_new, size=22):
    return (fo(d, t(x, y, old, col_old, size, weight=700)) + fi(d + 0.3, t(x, y, new, col_new, size, weight=700)))


def g4_rule():
    has('3,472 ≈ 3,5', '5…9')
    assert D('3.472').quantize(D('0.1')) == D('3.5')
    L = Grid(20, step=46, gap=12)
    R = Grid(262, step=46, gap=12)
    y = 30
    by = y + 30
    b = [L.number(y, '3,472')]
    b.append(line(L.x(-1), y + CH + 6, L.x(-1) + CW, y + CH + 6, GOLD, 4))
    b.append(fi(0.5, box(L.x(-2) - 5, y - 5, CW + 10, CH + 10, BLUE, op=0, sw=2.5, rx=8)))
    b.append(fi(1.2, t(L.cx(-2), y + CH + 32, '5…9 → вверх', BLUE, 16, weight=700)))
    b.append(t(236, y + 31, '≈', INK, 26))
    b.append(cell(R.x(0), y, '3', pcol(0)) + comma(R.comma_x(), y + CH - 4))
    b.append(cell(R.x(-1), y, '', pcol(-1)))
    b.append(digit_swap(R.cx(-1), by, '4', '5', 2.5, pcol(-1), GREEN))
    for p, ch in [(-2, '7'), (-3, '2')]:
        b.append(fo(1.9, cell(R.x(p), y, ch, pcol(p)), o=0.12))
    b.append(fi(3.0, box(R.x(0) - 6, y - 6, R.x(-1) + CW - R.x(0) + 12, CH + 12, GREEN, op=0, sw=2.5, rx=8)))
    return fig(svg(480, 124, ''.join(b), maxw=480), fx=True)


def g4_carry():
    has('2,96 ≈ 3,0', '9 + 1 = 10', '6 ≥ 5')
    assert D('2.96').quantize(D('0.1')) == D('3.0')
    L = Grid(30, step=50, gap=12)
    R = Grid(250, step=50, gap=12)
    y = 56
    by = y + 30
    b = [arrow_defs_p('g4c', [BLUE])]
    b.append(L.number(y, '2,96'))
    b.append(fi(0.5, box(L.x(-2) - 5, y - 5, CW + 10, CH + 10, BLUE, op=0, sw=2.5, rx=8)
                + t(L.cx(-2), y + CH + 28, '6 ≥ 5', BLUE, 16, weight=700)))
    b.append(t(222, y + 31, '≈', INK, 26))
    b.append(cell(R.x(0), y, '', pcol(0)) + comma(R.comma_x(), y + CH - 4))
    b.append(digit_swap(R.cx(0), by, '2', '3', 3.4, pcol(0), GREEN))
    b.append(cell(R.x(-1), y, '', pcol(-1)))
    b.append(digit_swap(R.cx(-1), by, '9', '0', 2.3, pcol(-1), GREEN))
    b.append(fo(1.3, cell(R.x(-2), y, '6', pcol(-2)), o=0.12))
    b.append(fi(1.7, t(R.cx(-1), y + CH + 28, '9 + 1 = 10', BLUE, 16, weight=700)))
    b.append(fi(2.7, arc_hop(R.cx(-1), R.cx(0) + 4, y - 6, 34, 'g4c0', BLUE)
                + t((R.cx(-1) + R.cx(0)) / 2, y - 30, '+1', BLUE, 16, weight=700)))
    b.append(fi(4.0, box(R.x(0) - 6, y - 6, R.x(-1) + CW - R.x(0) + 12, CH + 12, GREEN, op=0, sw=2.5, rx=8)))
    return fig(svg(440, 140, ''.join(b)), fx=True)


def g4_chain():
    has('3,449', '3,449 ≈ 3,4', '3,45', '3,5')
    assert D('3.449').quantize(D('0.1')) == D('3.4') and D('3.449') < D('3.45')
    f = nline(30, 430, 50, F(340, 100), F(350, 100))
    f2 = nline(30, 430, 170, F(3440, 1000), F(3450, 1000))
    b = [arrow_defs_p('g4h', [GREEN, RED])]
    b.append(line(30, 50, 430, 50, MUTED, 2) + line(30, 170, 430, 170, MUTED, 2))
    for k in range(11):
        xx = f(F(340 + k, 100))
        big = k in (0, 5, 10)
        b.append(line(xx, 50 - (9 if big else 4), xx, 50 + (9 if big else 4), INK if big else MUTED, 1.8 if big else 1))
        x2 = f2(F(3440 + k, 1000))
        b.append(line(x2, 166, x2, 174, MUTED, 1))
    b.append(t(30, 24, '3,4', INK, 15, weight=700) + t(430, 24, '3,5', INK, 15, weight=700))
    b.append(line(230, 30, 230, 70, MUTED, 1.4, " stroke-dasharray='4 3'") + t(240, 24, '3,45', MUTED, 14,
                                                                                    anchor='start'))
    b.append(f"<rect x='{f(F(344,100))}' y='45' width='{f(F(345,100))-f(F(344,100))}' height='10' fill='{GOLD}' "
             f"fill-opacity='0.45'/>")
    b.append(f"<path d='M{f(F(344,100))} 58 L30 160 M{f(F(345,100))} 58 L430 160' stroke='{GOLD}' "
             f"stroke-width='1.2' stroke-dasharray='4 4' fill='none'/>")
    b.append(t(30, 196, '3,44', MUTED, 14) + t(430, 196, '3,45', MUTED, 14))
    xv = f2(F(3449, 1000))
    b.append(dot(xv, 170, GOLD, 7) + t(xv, 196, '3,449', GOLD, 14, anchor='end', weight=700))
    b.append(line(430, 148, 430, 182, MUTED, 1.4, " stroke-dasharray='4 3'"))
    b.append(arrow(f(F(3449, 1000)) - 8, 72, 40, 72, 'g4h0', GREEN, 2.5)
             + t(130, 98, '3,449 ≈ 3,4', GREEN, 16, weight=700))
    b.append(f"<path d='M244 72 L420 72' stroke='{RED}' stroke-width='2' stroke-dasharray='5 4' fill='none' "
             f"marker-end='url(#g4h1)'/>" + t(332, 98, '3,45 → 3,5', RED, 15, weight=600)
             + line(292, 104, 372, 88, RED, 2))
    return fig(svg(460, 210, ''.join(b)))


# ——— Глава 5 ———

def g5_add():
    has('3,45 + 12,8', '3,45 + 12,80', '16,25')
    assert D('3.45') + D('12.80') == D('16.25')
    G = Grid(296, step=56)
    head = ''.join(t(G.cx(p), 18, PNAME[p], pcol(p), 12) for p in (1, 0, -1, -2))
    b = [t(20, 106, '3,45 + 12,8 =', INK, 18, anchor='start', weight=700)]
    cx = G.comma_x()
    b.append(f"<rect x='{cx-9}' y='30' width='18' height='184' rx='6' fill='{BLUE}' fill-opacity='0.12'/>")
    b.append(G.number(34, '3,45'))
    b.append(G.number(88, '12,8'))
    b.append(cell(G.x(-2), 88, '', pcol(-2), dashed=True))
    b.append(fi(0.5, t(G.cx(-2), 88 + 30, '0', MUTED, 22, weight=700)))
    b.append(t(G.x(1) - 26, 88 + 30, '+', INK, 24))
    b.append(line(G.x(1) - 10, 146, G.x(-2) + CW + 6, 146, INK, 2))
    ry = 156
    b.append(comma(cx, ry + CH - 4, INK))
    b.append(fi(1.2, cell(G.x(-2), ry, '5', GREEN)))
    b.append(fi(2.0, cell(G.x(-1), ry, '2', GREEN) + t(G.cx(0), 30, '1', BLUE, 16, weight=700)))
    b.append(fi(2.8, cell(G.x(0), ry, '6', GREEN) + cell(G.x(1), ry, '1', GREEN)))
    return fig(svg(520, 232, head + "<g transform='translate(0,16)'>" + ''.join(b) + '</g>', maxw=520), fx=True)


def g5_sub():
    has('7,2 − 3,45', '7,20 − 3,45', '3,75')
    assert D('7.20') - D('3.45') == D('3.75')
    G = Grid(256, step=56)
    b = [t(G.cx(p), 18, PNAME[p], pcol(p), 12) for p in (0, -1, -2)]
    y1, y2, ry = 60, 114, 182
    b.append(t(20, 148, '7,2 − 3,45 =', INK, 18, anchor='start', weight=700))
    b.append(G.number(y1, '7,2'))
    b.append(cell(G.x(-2), y1, '', pcol(-2), dashed=True))
    b.append(fi(0.3, t(G.cx(-2), y1 + 30, '0', MUTED, 22, weight=700)))
    b.append(G.number(y2, '3,45'))
    b.append(t(G.x(0) - 30, y2 + 30, '−', INK, 26))
    b.append(line(G.x(0) - 12, 172, G.x(-2) + CW + 6, 172, INK, 2))
    top = y1 - 10
    b.append(fi(0.8, strike(G.cx(-2), y1 + 24, 22) + strike(G.cx(-1), y1 + 24, 22)
                + t(G.cx(-2), top, '10', BLUE, 16, weight=700)))
    b.append(g('fi', 0.8, fo(2.2, t(G.cx(-1), top, '1', BLUE, 16, weight=700))))
    b.append(fi(1.4, cell(G.x(-2), ry, '5', GREEN)) + comma(G.comma_x(), ry + CH - 4))
    b.append(fi(2.4, strike(G.cx(0), y1 + 24, 22) + t(G.cx(0), top, '6', BLUE, 16, weight=700)
                + t(G.cx(-1), top, '11', BLUE, 16, weight=700)))
    b.append(fi(3.0, cell(G.x(-1), ry, '7', GREEN)))
    b.append(fi(3.7, cell(G.x(0), ry, '3', GREEN)))
    return fig(svg(450, 236, ''.join(b)), fx=True)


def g5_mistake():
    has('3,45 + 1,28', 'выровнять числа по правому краю')
    b = []
    # слева — по правому краю: клетки одного цвета, запятые расходятся
    st = 38
    for k, s in enumerate(['3,45', '12,8']):
        y = 40 + k * 52
        ds = s.replace(',', '')
        x0 = 30 + (3 - len(ds)) * st
        for j, ch in enumerate(ds):
            b.append(cell(x0 + j * st, y, ch, MUTED, txt=INK))
        cpos = s.index(',')
        b.append(comma(x0 + cpos * st - 2, y + CH - 4, RED))
    b.append(t(90, 22, 'по правому краю', RED, 14, weight=700))
    b.append(t(90, 160, 'как 3,45 + 1,28', RED, 14))
    # справа — запятая под запятой
    G = Grid(320, step=42, gap=10)
    b.append(t(345, 22, 'запятая под запятой', GREEN, 14, weight=700))
    b.append(G.number(40, '3,45') + G.number(92, '12,8'))
    return fig(svg(470, 172, ''.join(b), maxw=470))


# ——— Глава 6 ———

def g6_corridor():
    has('1,25', '0,8', '0,45', '4,5', 'коридор', 'заведомо меньше 1')
    assert D('1.25') - D('0.80') == D('0.45')
    f = nline(30, 430, 70, 0, 5)
    b = [line(30, 70, 440, 70, MUTED, 2)]
    for v in range(6):
        b.append(line(f(v), 63, f(v), 77, MUTED, 1.4) + t(f(v), 98, str(v), MUTED, 14))
    for v, s, dx, an in [(F(125, 100), '1,25', 2, 'start'), (F(8, 10), '0,8', -2, 'end')]:
        b.append(t(f(v) + dx, 30, s, GOLD, 14, anchor=an, weight=700))
        b.append(f"<circle cx='{f(v)}' cy='70' r='6' fill='{GOLD}' fill-opacity='0.3'/>")
        b.append(slide(0.6, f(1) - f(v), 0, dot(f(v), 70, GOLD, 6)))
    b.append(fi(2.0, f"<rect x='{f(0)}' y='60' width='{f(1)-f(0)}' height='20' rx='4' fill='{GREEN}' "
                     f"fill-opacity='0.25'/>" + t(f(0) + 2, 126, 'коридор: меньше 1', GREEN, 14, anchor='start')))
    b.append(fi(2.8, dot(f(F(45, 100)), 70, GREEN, 6) + t(f(F(45, 100)), 52, '0,45 ✓', GREEN, 14, weight=700)))
    b.append(fi(3.4, dot(f(F(45, 10)), 70, RED, 6) + t(f(F(45, 10)), 52, '4,5 ✗', RED, 14, weight=700)))
    return fig(svg(460, 140, ''.join(b)), fx=True)


def g6_kg():
    has('250/1000', '0,25', '1 кг 250 г = 1,25', '1 кг = 1000 г')
    assert F(250, 1000) == F(D('0.25')) and 1 + D('0.25') == D('1.25')
    b = [box(20, 44, 180, 36, GOLD, op=0.35), t(110, 68, '1 кг', INK, 16, weight=700),
         t(110, 30, '1 кг', MUTED, 13)]
    x0, w = 230, 210
    b.append(rect(x0, 44, w, 36, 'none', MUTED, 1.5))
    b.append(box(x0, 44, w * 0.25, 36, CYAN, op=0.45, sw=0))
    for k in range(1, 10):
        b.append(line(x0 + w * k / 10, 44, x0 + w * k / 10, 80, MUTED, 0.8))
    b.append(t(x0 + w / 2, 30, '1000 г = 1 кг', MUTED, 13))
    b.append(t(x0 + w * 0.125, 102, '250 г', CYAN, 14, weight=700))
    b.append(t(x0, 128, '250/1000 кг = 0,25 кг', CYAN, 14, anchor='start'))
    b.append(t(230, 166, '1 кг 250 г = 1,25 кг', GREEN, 18, weight=700))
    return fig(svg(460, 180, ''.join(b)))


def g6_hour():
    has('1 ч 30 мин = 1,5 ч', '1,30 ч', '0,25 ч', '0,5 ч', '1 ч = 60 мин')
    assert F(30, 60) == F(D('0.5')) and F(15, 60) == F(D('0.25'))
    x0, w, y = 30, 400, 60
    f = lambda m: x0 + w * m / 60
    b = [box(x0, y, f(30) - x0, 30, GOLD, op=0.3, sw=0), rect(x0, y, w, 30, 'none', INK, 1.8)]
    for m in range(5, 60, 5):
        big = m % 15 == 0
        b.append(line(f(m), y + (0 if big else 18), f(m), y + 30, INK if big else MUTED, 1.6 if big else 1))
    b.append(f"<path d='M{f(0)} {y-6} L{f(0)} {y-14} L{f(15)} {y-14} L{f(15)} {y-6}' stroke='{CYAN}' "
             f"stroke-width='2' fill='none'/>" + t(f(7.5), y - 22, '15 мин = 0,25 ч', CYAN, 13.5, weight=700))
    b.append(f"<path d='M{f(0)} {y+36} L{f(0)} {y+44} L{f(30)} {y+44} L{f(30)} {y+36}' stroke='{GOLD}' "
             f"stroke-width='2' fill='none'/>" + t(f(15), y + 64, '30 мин = 0,5 ч', GOLD, 14, weight=700))
    b.append(t(f(60), y - 12, '60 мин = 1 ч', MUTED, 13, anchor='end'))
    b.append(t(130, 168, '1 ч 30 мин = 1,5 ч', GREEN, 17, weight=700))
    b.append(t(350, 168, '1,30 ч', RED, 17, weight=700) + line(318, 172, 382, 156, RED, 2.2))
    return fig(svg(460, 182, ''.join(b)))


# ——— Глава 7: запятая прыгает ———

ST = 48


def plain_cell(x, y, ch, dashed=False, dim=False):
    return cell(x, y, ch, MUTED, dashed=dashed, txt=MUTED if dim else INK)


def hop_row(b, pref, x0, y, cells, c_from, c_to, d, extra_cells=(), fade_comma=None, done=None):
    """cells — {позиция: цифра}; запятая стоит после клетки c_from и прыгает за клетку c_to.
    done — (с какой клетки, по какую, когда): зелёная рамка вокруг ответа."""
    for pos, ch in cells.items():
        b.append(plain_cell(x0 + pos * ST, y, ch))
    for pos, ch, dd in extra_cells:
        b.append(fi(dd, plain_cell(x0 + pos * ST, y, ch, dashed=True, dim=True)))
    cx = lambda c: x0 + c * ST + CW + (ST - CW) / 2
    b.append(fo(d + 1.3, comma(cx(c_from), y + CH - 4, GREY)))   # слева пример цел — след не нужен
    step = 1 if c_to > c_from else -1
    for c in range(c_from, c_to, step):
        b.append(fi(d, arc_hop(cx(c), cx(c + step), y - 4, 18, pref, BLUE)))
    mv = slide(d, cx(c_to) - cx(c_from), 0, comma(cx(c_from), y + CH - 4, BLUE))
    b.append(fo(fade_comma, mv) if fade_comma else mv)
    if done:
        a, z, dd = done
        b.append(fi(dd, box(x0 + a * ST - 6, y - 6, (z - a) * ST + CW + 12, CH + 12, GREEN, op=0, sw=2.5, rx=8)))


def g7_hops():
    has('3,45 × 100', '345', '7,2 : 100', '0,072')
    assert D('3.45') * 100 == 345 and D('7.2') / 100 == D('0.072')
    b = [arrow_defs_p('g7a', [BLUE])]
    x0 = 160
    b.append(t(20, 34 + 30, '3,45 × 100 =', INK, 18, anchor='start', weight=700))
    hop_row(b, 'g7a0', x0, 34, {0: '3', 1: '4', 2: '5'}, 0, 2, 0.6, fade_comma=2.3, done=(0, 2, 2.6))
    y2 = 130
    b.append(t(20, y2 + 30, '7,2 : 100 =', INK, 18, anchor='start', weight=700))
    hop_row(b, 'g7a0', x0, y2, {2: '7', 3: '2'}, 2, 0, 1.0, extra_cells=[(1, '0', 0.4), (0, '0', 2.5)],
            done=(0, 3, 3.0))
    return fig(svg(380, 190, ''.join(b)), fx=True)


def g7_zeros_right():
    has('2,5 × 1000', '2,500 → 2500')
    assert D('2.5') * 1000 == 2500
    b = [arrow_defs_p('g7b', [BLUE])]
    x0, y = 160, 34
    b.append(t(20, y + 30, '2,5 × 1000 =', INK, 18, anchor='start', weight=700))
    hop_row(b, 'g7b0', x0, y, {0: '2', 1: '5'}, 0, 3, 1.0, extra_cells=[(2, '0', 0.4), (3, '0', 0.4)],
            fade_comma=2.6, done=(0, 3, 2.9))
    return fig(svg(380, 94, ''.join(b)), fx=True)


def g7_zeros_left():
    has('0,9 : 1000', '0,0009')
    assert D('0.9') / 1000 == D('0.0009')
    b = [arrow_defs_p('g7c', [BLUE])]
    x0, y = 160, 34
    b.append(t(20, y + 30, '0,9 : 1000 =', INK, 18, anchor='start', weight=700))
    hop_row(b, 'g7c0', x0, y, {4: '9'}, 3, 0, 1.0, extra_cells=[(2, '0', 0.4), (1, '0', 0.4), (0, '0', 2.6)],
            done=(0, 4, 3.1))
    b.append(plain_cell(x0 + 3 * ST, y, '0', dim=True))
    return fig(svg(420, 94, ''.join(b)), fx=True)


# ——— Глава 8 ———

def g8_places():
    has('1,2 × 0,35', '12 × 35', '420', '1 + 2', '0,420', '0,42')
    assert 12 * 35 == 420 and D('1.2') * D('0.35') == D('0.420')
    b = []
    y = 26
    left = [(20, '1'), (62, '2'), (146, '0'), (188, '3'), (230, '5')]
    for x, ch in left:
        b.append(cell(x, y, ch, MUTED, txt=INK))
    b.append(comma(20 + CW + 4, y + CH - 4) + comma(146 + CW + 4, y + CH - 4))
    b.append(t(119, y + 30, '×', INK, 22) + t(288, y + 31, '=', INK, 24))
    xi, xr = 312, [356, 398, 440]
    b.append(cell(xr[0], y, '4', MUTED, txt=INK) + cell(xr[1], y, '2', MUTED, txt=INK))
    b.append(fo(3.4, cell(xr[2], y, '0', MUTED, txt=INK), o=0.15))
    srcs = [62, 188, 230]
    for s, dx in zip(srcs, xr):
        bar = f"<rect x='{s+CW/2-6}' y='{y+CH+6}' width='12' height='4' rx='1' fill='{BLUE}'/>"
        b.append(f"<g opacity='0.4'>{bar}</g>")
        b.append(slide(0.8, dx - s, 0, bar))
    b.append(fi(0.4, t(146, y + CH + 34, '1 + 2 = 3 знака', BLUE, 16, weight=700)))
    b.append(t(xr[1] + CW / 2, y + CH + 34, '12 × 35 = 420', INK, 16, weight=600))
    b.append(fi(2.2, comma(xr[0] - 4, y + CH - 4, BLUE)))
    b.append(fi(2.6, cell(xi, y, '0', MUTED, dashed=True, txt=MUTED)))
    b.append(fi(3.8, box(xi - 6, y - 6, xr[1] + CW - xi + 12, CH + 12, GREEN, op=0, sw=2.5, rx=8)))
    return fig(svg(500, 116, ''.join(b), maxw=500), fx=True)


def g8_grid():
    has('0,4 × 0,5', '4 × 5', '0,20', '0,2')
    assert D('0.4') * D('0.5') == D('0.20')
    c, x0, y0 = 20, 60, 16
    b = []
    b.append(fi(0.4, box(x0, y0, 4 * c, 10 * c, BLUE, op=0.28, sw=0)))
    b.append(fi(1.3, box(x0, y0, 10 * c, 5 * c, GOLD, op=0.28, sw=0)))
    b.append(fi(2.2, box(x0, y0, 4 * c, 5 * c, GREEN, op=0.75, sw=2.5)))
    for k in range(1, 10):
        b.append(line(x0 + k * c, y0, x0 + k * c, y0 + 10 * c, MUTED, 0.6)
                 + line(x0, y0 + k * c, x0 + 10 * c, y0 + k * c, MUTED, 0.6))
    b.append(rect(x0, y0, 10 * c, 10 * c, 'none', INK, 2))
    b.append(fi(0.4, t(x0 + 2 * c, y0 + 10 * c + 22, '0,4', BLUE, 16, weight=700)))
    b.append(fi(1.3, t(x0 - 10, y0 + 2.5 * c + 6, '0,5', GOLD, 16, anchor='end', weight=700)))
    b.append(t(x0 + 10 * c, y0 + 10 * c + 22, '1', MUTED, 14) + t(x0 - 10, y0 + 10 * c + 4, '1', MUTED, 14,
                                                                     anchor='end'))
    b.append(t(300, 76, '0,4 × 0,5 =', INK, 18, anchor='start', weight=700))
    b.append(fi(2.4, t(300, 106, '4 × 5 = 20', MUTED, 16, anchor='start', weight=600)))
    b.append(fi(2.8, t(300, 136, '= 0,20 = 0,2', GREEN, 18, anchor='start', weight=700)))
    return fig(svg(430, 250, ''.join(b)), fx=True)


# ——— Глава 9 ———

def g9_corner():
    has('7,35 : 5', '23 : 5 = 4', '35 : 5 = 7', '1,47')
    assert D('7.35') / 5 == D('1.47')
    s = 21
    cx = {'7': 40, ',': 51, '3': 62, '5': 80}
    b = []
    yb = 40
    for k, xx in cx.items():
        b.append(t(xx, yb, k, INK, s, weight=700))
    b.append(line(100, 18, 100, 66, INK, 2) + line(100, 48, 190, 48, INK, 2) + t(122, yb, '5', INK, s, weight=700))
    qy = 72
    b.append(fi(0.3, t(118, qy, '1', GREEN, s, weight=700) + t(24, 60, '−', MUTED, 18)
                + t(40, 64, '5', MUTED, s) + line(30, 70, 52, 70, MUTED, 1.5) + t(40, 92, '2', INK, s)))
    b.append(fi(1.2, t(51, yb, ',', BLUE, s + 6, weight=700) + t(129, qy, ',', BLUE, s + 6, weight=700)))
    b.append(fi(2.2, t(62, 92, '3', INK, s) + t(140, qy, '4', GREEN, s, weight=700) + t(24, 110, '−', MUTED, 18)
                + t(40, 116, '2', MUTED, s) + t(62, 116, '0', MUTED, s) + line(30, 122, 74, 122, MUTED, 1.5)
                + t(62, 144, '3', INK, s)))
    b.append(fi(3.4, t(80, 144, '5', INK, s) + t(154, qy, '7', GREEN, s, weight=700) + t(46, 162, '−', MUTED, 18)
                + t(62, 168, '3', MUTED, s) + t(80, 168, '5', MUTED, s) + line(52, 174, 92, 174, MUTED, 1.5)
                + t(80, 196, '0', INK, s)))
    b.append(t(220, 120, '7,35 : 5 =', INK, 19, anchor='start', weight=700))
    b.append(fi(4.2, t(318, 120, '1,47', GREEN, 19, anchor='start', weight=700)))
    return fig(svg(400, 208, ''.join(b)), fx=True)


def g9_zeros():
    has('3 : 4 = 0,75', '30 : 4 = 7', '20 : 4 = 5')
    assert F(3, 4) == F(D('0.75')) and divmod(30, 4) == (7, 2) and divmod(20, 4) == (5, 0)
    s = 21
    b = []
    yb, qy = 40, 72
    b.append(t(40, yb, '3', INK, s, weight=700))
    b.append(line(100, 18, 100, 66, INK, 2) + line(100, 48, 190, 48, INK, 2) + t(122, yb, '4', INK, s, weight=700))
    b.append(fi(0.4, t(118, qy, '0', GREEN, s, weight=700) + t(129, qy, ',', BLUE, s + 6, weight=700)))
    b.append(fi(1.2, t(51, yb, ',', MUTED, s + 6, weight=700) + t(62, yb, '0', MUTED, s, weight=700)))
    b.append(fi(1.8, t(140, qy, '7', GREEN, s, weight=700) + t(24, 60, '−', MUTED, 18) + t(40, 64, '2', MUTED, s)
                + t(62, 64, '8', MUTED, s) + line(30, 70, 74, 70, MUTED, 1.5) + t(62, 92, '2', INK, s)))
    b.append(fi(2.8, t(80, yb, '0', MUTED, s, weight=700) + t(80, 92, '0', INK, s)))
    b.append(fi(3.3, t(160, qy, '5', GREEN, s, weight=700) + t(46, 110, '−', MUTED, 18) + t(62, 116, '2', MUTED, s)
                + t(80, 116, '0', MUTED, s) + line(52, 122, 92, 122, MUTED, 1.5) + t(80, 144, '0', INK, s)))
    b.append(t(220, 100, '3 : 4 =', INK, 19, anchor='start', weight=700))
    b.append(fi(4.0, t(292, 100, '0,75', GREEN, 19, anchor='start', weight=700)))
    return fig(svg(380, 158, ''.join(b)), fx=True)


def g9_mean():
    has('4,2 + 5,1 + 3,9 = 13,2', '13,2 : 3 = 4,4', '3,9 < 4,4 < 5,1')
    vals = [D('4.2'), D('5.1'), D('3.9')]
    m = sum(vals) / 3
    assert sum(vals) == D('13.2') and m == D('4.4')
    k, base, w = 36, 220, 64
    Y = lambda v: base - float(v) * k
    xs = [60, 170, 280]
    b = []
    for x, v in zip(xs, vals):
        top = min(v, m) if x == xs[1] else v
        b.append(box(x, Y(top), w, base - Y(top), GOLD, op=0.3, sw=1.5))
        b.append(t(x + w / 2, base + 22, dec(v), INK, 16, weight=700))
    # излишек среднего столбика: [4,4; 4,6] → первому, [4,6; 5,1] → третьему
    pa = (m, m + (m - vals[0]))
    pb = (pa[1], vals[1])
    assert pb[1] - pb[0] == m - vals[2]
    for (lo, hi), tx, ty_lo, dd in [(pa, xs[0], vals[0], 0.8), (pb, xs[2], vals[2], 1.4)]:
        piece = box(xs[1], Y(hi), w, Y(lo) - Y(hi), BLUE, op=0.55, sw=1.5)
        b.append(f"<g opacity='0.25'>{piece}</g>")
        b.append(slide(dd, tx - xs[1], Y(hi - lo + ty_lo) - Y(hi), piece))
    b.append(fi(2.8, line(40, Y(m), 364, Y(m), GREEN, 2.2, " stroke-dasharray='7 5'")
                + t(370, Y(m) + 5, '4,4', GREEN, 17, anchor='start', weight=700)))
    b.append(line(40, base, 364, base, MUTED, 1.5))
    return fig(svg(420, 252, ''.join(b)), fx=True)


# ——— Глава 10 ———

def g10_both():
    has('4,5 : 0,15', '450 : 15', '4,50', '30')
    assert D('4.5') / D('0.15') == 30 == 450 // 15
    b = [arrow_defs_p('g10a', [BLUE])]
    y = 40
    b.append(t(20, y + 30, '4,5 : 0,15 =', INK, 18, anchor='start', weight=700))
    x1 = 150
    hop_row(b, 'g10a0', x1, y, {0: '4', 1: '5'}, 0, 2, 1.0, extra_cells=[(2, '0', 0.4)], fade_comma=2.5)
    b.append(t(x1 + 3 * ST + 6, y + 30, ':', INK, 24))
    x2 = x1 + 3 * ST + 24
    b.append(fo(2.5, plain_cell(x2, y, '0'), o=0.15))
    hop_row(b, 'g10a0', x2, y, {1: '1', 2: '5'}, 0, 2, 1.0, fade_comma=2.5)
    b.append(fi(2.9, t((x1 + x2 + 3 * ST) / 2, 136, '450 : 15 = 30', GREEN, 20, weight=700)))
    return fig(svg(480, 152, ''.join(b), maxw=480), fx=True)


def g10_tiles():
    has('450 : 15', 'укладок')
    n = D('4.5') / D('0.15')
    assert n == 30 and D(450) / 15 == n
    x0, ux = 30, 90
    b = []
    for k, (whole, piece) in enumerate([('4,5', '0,15'), ('450', '15')]):
        y = 30 + k * 82
        seg = float(D('0.15') * ux)
        for j in range(int(n)):
            col = CYAN if j % 2 == 0 else VIOLET
            b.append(box(x0 + j * seg, y, seg, 26, col, op=0.5, sw=0.8))
        b.append(f"<path d='M{x0} {y-6} L{x0} {y-12} L{x0+seg} {y-12} L{x0+seg} {y-6}' stroke='{GOLD}' "
                 f"stroke-width='1.8' fill='none'/>" + t(x0, y - 18, piece, GOLD, 14, anchor='start', weight=700))
        b.append(t(x0 + 4.5 * ux, y - 10, whole, INK, 15, anchor='end', weight=700))
        b.append(t(x0 + 4.5 * ux + 12, y + 19, '30', GREEN, 17, anchor='start', weight=700))
    return fig(svg(480, 152, ''.join(b), maxw=480))


# ——— Глава 11 ———

def g11_twelfths():
    has('1/3 + 1/4', '4/12 + 3/12', '7/12')
    assert F(1, 3) + F(D('0.25')) == F(4, 12) + F(3, 12) == F(7, 12)
    x0, W, h = 30, 360, 30
    u = W / 12
    rows = [(30, 3, VIOLET, '1/3', '4/12'), (100, 4, CYAN, '1/4', '3/12')]
    b = []
    for y, n, col, a, z in rows:
        part = W / n
        b.append(box(x0, y, part, h, col, op=0.6, sw=1.5))
        b.append(rect(x0, y, W, h, 'none', INK, 1.8))
        for k in range(1, n):
            b.append(line(x0 + k * part, y, x0 + k * part, y + h, INK, 1.8))
        b.append(fi(0.9, ''.join(line(x0 + k * u, y + 6, x0 + k * u, y + h - 6, MUTED, 1) for k in range(1, 12))))
        b.append(t(x0 + W + 12, y + 21, a, col, 16, anchor='start', weight=700))
        b.append(fi(1.5, t(x0 + W + 48, y + 21, '= ' + z, col, 16, anchor='start', weight=700)))
    y3 = 180
    b.append(rect(x0, y3, W, h, 'none', INK, 1.8))
    b.append(''.join(line(x0 + k * u, y3, x0 + k * u, y3 + h, MUTED, 1) for k in range(1, 12)))
    b.append(slide(2.2, 0, y3 - 30, box(x0, 30, 4 * u, h, VIOLET, op=0.6, sw=1.5)))
    b.append(slide(2.6, 4 * u, y3 - 100, box(x0, 100, 3 * u, h, CYAN, op=0.6, sw=1.5)))
    b.append(fi(3.9, t(x0 + W + 12, y3 + 21, '7/12', GREEN, 18, anchor='start', weight=700)))
    return fig(svg(480, 224, ''.join(b), maxw=480), fx=True)


FIGS = {
    'и это главный инструмент во всех сравнениях': r1_tails,
    'Ответ 2,475 или 247,5 тогда отбрасывается сразу': r3_estimate,
    'Знаменатель прячется в том, сколько цифр стоит после запятой': g1_places,
    '3,472 — это 3 + 4/10': g1_sum,
    'Названия похожи, а места в числе далеки': g1_both_sides,
    '7/1000 0,007': g1_rule,
    'сокращаю на 5': g2_to_common,
    '4 × 25 = 100, значит умножаю оба на 25': g2_quarters,
    'Дроби, которые не переводятся, оставляют обыкновенными': g2_factors,
    'сравниваю дробные части как числа': g3_compare,
    'Место находится всегда, надо только удлинить хвост': g3_between,
    'Длина записи ничего не значит': g3_length,
    'Заменить число ближайшим': g4_nearest,
    'смотрю на следующую цифру справа — только на неё': g4_rule,
    'в один разряд десятка не влезает': g4_carry,
    'Так нельзя: смотреть надо только на одну': g4_chain,
    'пишу запятую под запятой, складываю сотые': g5_add,
    'занимаю десятую': g5_sub,
    'выровнять числа по правому краю': g5_mistake,
    'Прикидка не называет ответ — она называет коридор': g6_corridor,
    'Ещё один приём — единицы измерения': g6_kg,
    'минуты не десятичная часть часа': g6_hour,
    '3,45 × 100': g7_hops,
    'Пример с дописыванием нулей': g7_zeros_right,
    'И то же самое при делении, только влево': g7_zeros_left,
    'отсчитываю 3 знака справа': g8_places,
    'произведение меньше каждого множителя': g8_grid,
    'целая часть делимого кончилась — ставлю запятую': g9_corner,
    'Если цифры делимого кончились, а остаток не ноль': g9_zeros,
    '13,2 : 3 = 4,4': g9_mean,
    'двигаю обе запятые на 2': g10_both,
    'дают один ответ': g10_tiles,
    'общий знаменатель 12': g11_twelfths,
}
