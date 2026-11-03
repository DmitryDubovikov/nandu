import json, sys, math
# Рисунки к Т6 национал 2022 I №3: цветок из семи кружков, четыре цвета.
# Расположение — как на чертеже условия: кружки 1–6 по часовой стрелке от левого верхнего, 7 в середине;
# соседние по кругу кружки касаются, 7 касается всех шести; стебель — от кружка 4.
RED, BLUE, GREEN, WHITE, GOLD = '#f2686c', '#5ba8f5', '#5fd38d', '#eef2f6', '#f0a83c'
INK, DIM, LAB, BG = '#cfdae6', '#4a5866', '#e8eef6', '#0d1117'
COL = {'к': RED, 'с': BLUE, 'з': GREEN, 'б': WHITE}
R = 10
C0 = (50, 40)
ANG = {'1': 120, '2': 60, '3': 0, '4': -60, '5': -120, '6': 180}
P = {n: (C0[0] + 2 * R * math.cos(math.radians(a)), C0[1] - 2 * R * math.sin(math.radians(a))) for n, a in ANG.items()}
P['7'] = C0
HEX = set('123456')
ODD = set('135')

def node(n, paint=None, ring=INK, mark=False):
    # paint: None — не закрашен; 'к' — один цвет; 'сз' — два возможных цвета (половинки); mark — золотое кольцо
    x, y = P[n]; s = ''; r = R - 0.35
    if paint and len(paint) == 2:
        a, b = COL[paint[0]], COL[paint[1]]
        s += f"<path d='M{x:.2f} {y - r:.2f} A {r} {r} 0 0 0 {x:.2f} {y + r:.2f} Z' fill='{a}'/>"
        s += f"<path d='M{x:.2f} {y - r:.2f} A {r} {r} 0 0 1 {x:.2f} {y + r:.2f} Z' fill='{b}'/>"
        s += f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{r}' fill='none' stroke='{ring}' stroke-width='0.7'/>"
        tc = BG
    elif paint:
        s += f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{r}' fill='{COL[paint]}' stroke='{ring}' stroke-width='0.7'/>"
        tc = BG
    else:
        s += f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{r}' fill='none' stroke='{ring}' stroke-width='0.8'/>"
        tc = ring if ring != INK else LAB
    if mark:
        s += f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{r - 1.6}' fill='none' stroke='{GOLD}' stroke-width='1.3'/>"
    s += f"<text x='{x:.2f}' y='{y + 2.2:.2f}' fill='{tc}' font-size='6.2' text-anchor='middle' font-weight='700'>{n}</text>"
    return s

def flower(paint=None, focus=None, marks=(), stem=False, mw=300, aria='Цветок из семи кружков'):
    # focus — какие кружки яркие; остальные тусклым (весь цветок всегда на месте)
    paint = paint or {}; focus = set(focus or P)
    s = ''
    if stem:
        x, y = P['4']
        s += (f"<path d='M{x + 3:.2f} {y + R - 0.8:.2f} C {x + 8:.2f} {y + 16:.2f}, {x + 6:.2f} {y + 26:.2f}, {x + 1:.2f} {y + 36:.2f}' "
              f"fill='none' stroke='{INK}' stroke-width='2.4' stroke-linecap='round'/>")
    for n in P:
        s += node(n, paint.get(n), INK if n in focus else DIM, n in marks)
    h = 106 if stem else 71
    st = f" style='max-width:{mw}px'" if mw else ''
    return f"<svg viewBox='18 8 64 {h - 8}' role='img' aria-label='{aria}'{st}>{s}</svg>"

def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

def p(**kw): return {k[1:]: v for k, v in kw.items()}   # p(_1='к', _2='с') → {'1': 'к', '2': 'с'}

V = {}
# условие: цветок с номерами кружков
V['Способ — цвет для каждого из кружков'] = fig(flower(stem=True, mw=300), 'Кружки пронумерованы 1, …, 7.')
# кружок 7 касается всех шести
V['а кружок 7 в середине касается всех шести'] = fig(flower(p(_7='б'), marks=('7',), mw=260, aria='Кружок 7 и шестиугольник'),
  f"Пример: <b style='color:{GOLD}'>кружок 7</b> белый ⇒ кружкам 1–6 остаются красный, зелёный и синий.")
# нечётные и чётные
V['каждые два касающихся кружка — нечётный и чётный'] = fig(flower(focus=HEX, marks=ODD, mw=260),
  f"<b style='color:{GOLD}'>Нечётные кружки 1, 3, 5</b> друг друга не касаются; по кругу касаются только нечётный и чётный.")
# миры по числу цветов у нечётных (7 белый)
V['2.1. N(один цвет у 1, 3, 5).'] = fig(
  flower(p(_7='б', _1='к', _3='к', _5='к', _2='сз', _4='сз', _6='сз'), HEX, marks=ODD, mw=260), 'Пример: 7 белый; 1, 3 и 5 красные.')
V['2.2. N(два цвета у 1, 3, 5).'] = fig(
  flower(p(_7='б', _1='с', _3='к', _5='к', _2='з', _4='сз', _6='з'), HEX, marks=ODD, mw=260),
  'Пример: 7 белый; 3 и 5 красные, 1 синий; два цвета у 4.')
V['2.3. N(три цвета у 1, 3, 5).'] = fig(
  flower(p(_7='б', _1='к', _3='с', _5='з', _2='з', _4='к', _6='с'), HEX, marks=ODD, mw=260),
  'Пример: 7 белый; 1 красный, 3 синий, 5 зелёный.')
json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
