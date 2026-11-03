"""Рисунок условия: национал 2015, №1 — четыре сосуда с фигурками ■ ★ ⅄ ●, под сосудом общий вес.

Запуск: python3 vis/T1_nac_2015_1.py [T1_nac_2015_1.vis.json]
"""
import json, os, sys, math
INK, DIM, LAB = '#cfdae6', '#4a5866', '#e8eef6'

def txt(x, y, s, col=LAB, size=4.2, w='700'):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='{w}'>{s}</text>"
def fig(inner, cap=''):
    c = f"<figcaption>{cap}</figcaption>" if cap else ''
    return f"<figure class='st'>{inner}{c}</figure>"

R = 1.9   # полуразмер фигурки
def square(x, y):
    return f"<rect x='{x-R*0.9:.2f}' y='{y-R*0.9:.2f}' width='{2*R*0.9:.2f}' height='{2*R*0.9:.2f}' fill='{INK}'/>"
def circle(x, y):
    return f"<circle cx='{x:.2f}' cy='{y:.2f}' r='{R*0.95:.2f}' fill='{INK}'/>"
def star(x, y):
    pts = []
    for i in range(10):
        r = R * 1.2 if i % 2 == 0 else R * 0.48
        a = -math.pi / 2 + i * math.pi / 5
        pts.append(f"{x + r*math.cos(a):.2f},{y + r*math.sin(a):.2f}")
    return f"<polygon points='{' '.join(pts)}' fill='{INK}'/>"
def tripod(x, y):
    # ⅄: стержень вверх, две ножки вниз в стороны
    s = ''
    for a in (-90, 30, 150):
        t = math.radians(a)
        s += (f"<line x1='{x:.2f}' y1='{y:.2f}' x2='{x + R*1.05*math.cos(t):.2f}' y2='{y + R*1.05*math.sin(t):.2f}' "
              f"stroke='{INK}' stroke-width='0.8' stroke-linecap='round'/>")
    return s
SHAPE = {'q': square, 's': star, 't': tripod, 'r': circle}
STEP = 4.6

def row(cx, y, items):
    n = len(items)
    x0 = cx - (n - 1) * STEP / 2
    return ''.join(SHAPE[k](x0 + i * STEP, y) for i, k in enumerate(items))

VW, VH, GAP = 30, 16, 6
# сосуд: верхний ряд, нижний ряд, вес
VESSELS = [('qqq', 'ts', '211'), ('sr', 'qqq', '178'), ('ttsss', 'rrrq', '292'), ('ttss', 'rqq', '?')]

def picture():
    s = ''
    for i, (top, bot, w) in enumerate(VESSELS):
        x = 2 + i * (VW + GAP)
        cx = x + VW / 2
        s += f"<path d='M{x},2 V{2+VH} H{x+VW} V2' fill='none' stroke='{DIM}' stroke-width='0.6'/>"
        s += row(cx, 7, top) + row(cx, 13.5, bot)
        s += txt(cx, 2 + VH + 6, w)
    W = 4 + 4 * VW + 3 * GAP
    return f"<svg viewBox='0 0 {W} {VH + 10}' role='img' aria-label='Четыре сосуда с фигурками' style='max-width:560px'>{s}</svg>"

V = {}
# якорь — строка букв: рисунок крупно во всю колонку под условием, прямо перед строками «С рисунка»
V['сколько граммов весит одна фигурка'] = fig(picture(), 'Четыре сосуда, под каждым общий вес фигурок в граммах.')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'T1_nac_2015_1.vis.json')
json.dump(V, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
