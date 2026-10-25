#!/usr/bin/env python3
"""Иллюстрации главы 4 «Сочетания» → nandu_n2_kombinatorika_uchebnik.vis.json.

Язык глав 2–3 продолжается: у каждого ребёнка свой цвет, склеенное гаснет, m — синей плашкой,
цепочки (посчитанные) — золотом; П — золотая клетка, М — серая; сокращаемый факториал — фиолетовый.
Анимируется только переход (правило 15): нижний треугольник таблицы гаснет — пары склеились;
шесть цепочек съезжаются в одну тройку; 6! уходит сверху и снизу; рамка переезжает с мест П на места М.

Запуск: python3 26-27/nandu_level2/kombinatorika/vis/glava_4.py
"""
import json, os, re
from itertools import permutations

from glava_2 import svg, fig, t, g, GOLD, BLUE, GREEN, VIOLET, GREY
from glava_3 import kid, pill, KIDS, DARK

HERE = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.vis.json')


# ——— 1. Пример 1: 72 клетки «капитан × помощник», пара дежурных — две клетки ———

def pairs_table():
    c, x0, y0, N = 40, 70, 64, 6
    b = [t(x0 + N / 2 * c, 18, 'второй выбранный', size=14), t(18, y0 + N / 2 * c, 'первый выбранный', size=14,
                                                       extra=f" transform='rotate(-90 18 {y0 + N / 2 * c})'")]
    for i in range(N):
        b.append(kid(x0 + i * c + c / 2, 40, i, r=13, size=13))
        b.append(kid(46, y0 + i * c + c / 2, i, r=13, size=13))
    upper, lower = [], []
    for r in range(N):
        for j in range(N):
            x, y = x0 + j * c, y0 + r * c
            if r == j:
                b.append(f"<rect x='{x}' y='{y}' width='{c}' height='{c}' fill='var(--bg)' stroke='var(--line)'/>"
                         f"<line x1='{x+6}' y1='{y+6}' x2='{x+c-6}' y2='{y+c-6}' stroke='{GREY}'/>")
                continue
            cell = (f"<rect x='{x+3}' y='{y+3}' width='{c/2-3}' height='{c-6}' rx='2' fill='{KIDS[r][1]}'/>"
                    f"<rect x='{x+c/2}' y='{y+3}' width='{c/2-3}' height='{c-6}' rx='2' fill='{KIDS[j][1]}'/>"
                    f"<rect x='{x}' y='{y}' width='{c}' height='{c}' fill='none' stroke='var(--line)'/>")
            (upper if j > r else lower).append(cell)
    b.append(''.join(upper))
    b.append(g('fo', 2.4, ''.join(lower), ';--o:.12'))
    ab = f"<rect x='{x0+c}' y='{y0}' width='{c}' height='{c}' fill='none' stroke='{GOLD}' stroke-width='3'/>"
    ba = f"<rect x='{x0}' y='{y0+c}' width='{c}' height='{c}' fill='none' stroke='{GOLD}' stroke-width='3'/>"
    b.append(g('fi', 0.6, ab + ba))
    tx = x0 + N * c + 26
    b.append(t(tx, y0 + 14, '(А, Б) и (Б, А) —', GOLD, 15, anchor='start', weight=700, cls='fi', d=0.6))
    b.append(t(tx, y0 + 36, 'одна пара {А, Б}', 'var(--ink)', 15, anchor='start', weight=700, cls='fi', d=1.2))
    b.append(t(tx, y0 + 90, '6 · 5 = 30 цепочек', GOLD, 15, anchor='start', weight=700))
    b.append(t(tx, y0 + 112, 'на диагонали — никого:', 'var(--muted)', 13, anchor='start'))
    b.append(t(tx, y0 + 130, 'один человек дважды', 'var(--muted)', 13, anchor='start'))
    b.append(t(tx, y0 + 172, 'нижний треугольник —', 'var(--muted)', 14, anchor='start', cls='fi', d=2.4))
    b.append(t(tx, y0 + 192, 'те же пары наоборот', 'var(--muted)', 14, anchor='start', cls='fi', d=2.4))
    b.append(pill(tx, y0 + 232, 'm = 2', 3.0, anchor='start'))
    b.append(t(tx, y0 + 266, '30 : 2 = 15 пар', 'var(--ink)', 17, anchor='start', weight=700, cls='fi', d=3.4))
    return fig(svg(tx + 190, max(y0 + N * c + 10, y0 + 280), ''.join(b), maxw=tx + 190), fx=True)


# ——— 2. Пример 2: шесть цепочек склеиваются в одну тройку ———

def triples():
    b = [t(150, 18, 'шесть цепочек', GOLD, 15, weight=700)]
    tx, ty = 470, 132
    for n, p in enumerate(permutations([0, 1, 2])):
        x, y = 40 + (n % 2) * 150, 50 + (n // 2) * 60
        body = (f"<rect x='{x-22}' y='{y-20}' width='124' height='40' rx='8' fill='none' stroke='{GOLD}'/>"
                + ''.join(kid(x + k * 40, y, i, r=15, size=13) for k, i in enumerate(p)))
        b.append(g('fo', 1.0, body, ';--o:.25'))
        b.append(g('sl', 1.0 + 0.15 * n, g('fo', 2.3, body), f';--to:translate({tx-x}px,{ty-y}px)'))
    b.append(g('fi', 2.5, f"<rect x='{tx-26}' y='{ty-24}' width='132' height='48' rx='24' fill='none' "
                          f"stroke='var(--ink)' stroke-width='2'/>"
               + ''.join(kid(tx + k * 40, ty, i, r=15, size=13) for k, i in enumerate([0, 1, 2]))))
    b.append(t(tx + 40, ty + 46, 'одна тройка {А, Б, В}', 'var(--ink)', 15, weight=700, cls='fi', d=2.5))
    b.append(pill(tx + 40, ty + 84, 'm = 3! = 6', 2.9))
    b.append(t(tx + 40, ty + 116, '120 : 6 = 20', 'var(--ink)', 17, weight=700, cls='fi', d=3.3))
    return fig(svg(620, 260, ''.join(b), maxw=620), fx=True)


# ——— 3. ⚠ сокращение: 9! расписан до 6!, 6! уходит сверху и снизу ———

def cancel():
    b = [t(16, 78, 'C(6, 2) =', 'var(--ink)', 20, anchor='start')]
    b.append(g('fo', 0.8, t(214, 56, '6!', 'var(--ink)', 22, weight=600)))
    top = (t(160, 56, '6 · 5 ·', GOLD, 22, anchor='start', weight=600)
           + t(232, 56, '4!', VIOLET, 22, anchor='start', weight=700))
    b.append(g('fi', 1.0, top))
    b.append("<line x1='140' y1='70' x2='280' y2='70' stroke='var(--ink)' stroke-width='2'/>")
    b.append(t(166, 98, '2! ·', 'var(--ink)', 22, anchor='start', weight=600)
             + t(210, 98, '4!', VIOLET, 22, anchor='start', weight=700))
    b.append(f"<line x1='228' y1='60' x2='260' y2='38' stroke='{VIOLET}' stroke-width='2.5' "
             f"pathLength='100' class='dr' style='--d:2.0s;--dur:.5s'/>")
    b.append(f"<line x1='206' y1='102' x2='238' y2='80' stroke='{VIOLET}' stroke-width='2.5' "
             f"pathLength='100' class='dr' style='--d:2.4s;--dur:.5s'/>")
    rest = (t(304, 78, '=', 'var(--ink)', 22)
            + t(360, 56, '6 · 5', GOLD, 22, weight=600)
            + "<line x1='326' y1='70' x2='394' y2='70' stroke='var(--ink)' stroke-width='2'/>"
            + t(360, 98, '2!', 'var(--ink)', 22, weight=600)
            + t(416, 78, '=', 'var(--ink)', 22)
            + t(460, 56, '30', 'var(--ink)', 22, weight=600)
            + "<line x1='438' y1='70' x2='482' y2='70' stroke='var(--ink)' stroke-width='2'/>"
            + t(460, 98, '2', 'var(--ink)', 22, weight=600)
            + t(500, 78, '= 15', 'var(--ink)', 22, anchor='start', weight=700))
    b.append(g('fi', 3.0, rest))
    b.append(t(16, 136, 'сократили больший факториал снизу — сверху остались два множителя', size=13,
               anchor='start', cls='fi', d=3.0))
    return fig(svg(600, 148, ''.join(b), maxw=600), fx=True)


# ——— плитки записи бросков ———

REC, CW = 'МППММПМ', 50


def strip(x0, y0):
    b = []
    for k, ch in enumerate(REC):
        x = x0 + k * CW
        b.append(t(x + 20, y0 - 8, str(k + 1), 'var(--muted)', 13))
        fill = GOLD if ch == 'П' else 'var(--bg2)'
        ink = DARK if ch == 'П' else 'var(--muted)'
        b.append(f"<rect x='{x}' y='{y0}' width='40' height='40' rx='6' fill='{fill}' stroke='var(--line)'/>")
        b.append(t(x + 20, y0 + 27, ch, ink, 19, weight=700))
    return ''.join(b)


# ——— 4. Пример 3: запись = выбор трёх мест из семи ———

def record():
    b = [t(20, 14, 'номер броска', size=13, anchor='start'), strip(20, 50)]
    b.append(t(20, 118, 'П на местах 2, 3, 6 — выбраны три места из семи', 'var(--ink)', 15, anchor='start'))
    return fig(svg(380, 130, ''.join(b), maxw=380))


# ——— 5. Симметрия: выбрать места П — то же, что выбрать места М ———

def complement():
    x0, y0 = 20, 40
    b = [strip(x0, y0)]
    p = [k for k, ch in enumerate(REC) if ch == 'П']
    m = [k for k, ch in enumerate(REC) if ch == 'М']
    b.append(t(x0, y0 + 76, 'места П: {2, 3, 6} — C(7, 3)', GOLD, 15, anchor='start', weight=700, cls='fi', d=0.5))
    b.append(g('fo', 2.2, g('fi', 0.5, ''.join(
        f"<rect x='{x0+k*CW-4}' y='{y0-4}' width='48' height='48' rx='8' fill='none' stroke='{GOLD}' "
        f"stroke-width='3'/>" for k in p))))
    b.append(g('fi', 2.4, ''.join(f"<rect x='{x0+k*CW-4}' y='{y0-4}' width='48' height='48' rx='8' fill='none' "
                                  f"stroke='{BLUE}' stroke-width='3' stroke-dasharray='6 4'/>" for k in m)))
    b.append(t(x0, y0 + 100, 'места М: {1, 4, 5, 7} — C(7, 4)', BLUE, 15, anchor='start', weight=700,
               cls='fi', d=2.4))
    b.append(t(x0, y0 + 130, 'одно слово — один выбор мест П и один выбор мест М', 'var(--ink)', 14,
               anchor='start', cls='fi', d=3.2))
    return fig(svg(380, 180, ''.join(b), maxw=380), fx=True)


# ——— 6. Второе доказательство: набор ↔ код из 1 и 0 ———

def code():
    letters = 'АБВГД'
    rows = [('{А, В}', '10100'), ('{Б, Д}', '01001')]
    b = []
    for k, ch in enumerate(letters):
        b.append(t(150 + k * 44 + 18, 22, ch, 'var(--muted)', 15, weight=700))
    for r, (name, cd) in enumerate(rows):
        y = 36 + r * 56
        b.append(t(14, y + 25, name, 'var(--ink)', 16, anchor='start', weight=700))
        b.append(t(118, y + 25, '→', 'var(--muted)', 16))
        for k, bit in enumerate(cd):
            x = 150 + k * 44
            on = bit == '1'
            fill = KIDS[k][1] if on else 'var(--bg2)'
            b.append(f"<rect x='{x}' y='{y}' width='36' height='36' rx='6' fill='{fill}' stroke='var(--line)'/>")
            b.append(t(x + 18, y + 25, bit, DARK if on else 'var(--muted)', 18, weight=700))
    b.append(t(14, 160, 'две единицы и три нуля: набор из двух букв ↔ анаграмма слова 11000', size=13,
               anchor='start'))
    return fig(svg(430, 172, ''.join(b), maxw=430))


FIGS = {
    'N(пар дежурных) = 6 · 5 : 2': pairs_table,
    'N(троек дежурных) = 6 · 5 · 4 : 3!': triples,
    'C(6, 2) = 6 · 5 · 4! / (2! · 4!)': cancel,
    'Например, слово МППММПМ означает': record,
    'Как видишь, C(7, 3) = C(7, 4)': complement,
    'Каждый набор из k элементов даёт код': code,
}

if __name__ == '__main__':
    d = json.load(open(VIS))
    md = open(os.path.join(HERE, '..', 'nandu_n2_kombinatorika_uchebnik.md')).read()
    plain = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', md))
    new = {anchor: f() for anchor, f in FIGS.items()}
    missing = [a for a in new if a not in plain]
    if missing:
        raise SystemExit(f'якоря не найдены в тексте: {missing}')
    d = {k: v for k, v in d.items() if k in plain and (k in new or v not in new.values())}
    d.update(new)
    json.dump(d, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(FIGS), 'рисунков →', os.path.relpath(VIS))
