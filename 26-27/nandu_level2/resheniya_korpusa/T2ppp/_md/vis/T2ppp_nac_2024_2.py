import json, sys
# Рисунки к Т2‴ национал 2024 день I №2. Не в масштабе, как в условии: участок 0..70, белая полоса 8, серая 6.
# SVG: X, Y напрямую (y вниз). Участок (0,0)–(70,70), средний квадрат (8,8)–(62,62), сад (14,14)–(56,56).
GOLD,BLUE,GREEN,RED,VIO='#f0a83c','#5ba8f5','#5fd38d','#f2686c','#c58af9'
INK,DIM,LAB,MUT='#cfdae6','#4a5866','#e8eef6','#93a1b1'
L, W, G = 70, 8, 6
M0, M1 = W, L - W            # средний квадрат
S0, S1 = W + G, L - W - G    # сад

def rect(x0, y0, x1, y1, col, w=0.6, fill='none', op=1, dash=False):
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return (f"<rect x='{x0}' y='{y0}' width='{x1-x0}' height='{y1-y0}' fill='{fill}' fill-opacity='{op}' "
            f"stroke='{col}' stroke-width='{w}'{d}/>")
def ring(a0, a1, b0, b1, col, op):   # полоса между квадратами [a0,a1] и [b0,b1] — заливка через evenodd
    d = f"M{a0},{a0}H{a1}V{a1}H{a0}Z M{b0},{b0}H{b1}V{b1}H{b0}Z"
    return f"<path d='{d}' fill='{col}' fill-opacity='{op}' fill-rule='evenodd' stroke='none'/>"
def line(x1, y1, x2, y2, col, w=0.5, dash=False):
    d = " stroke-dasharray='1.6 1.2'" if dash else ''
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"
def txt(x, y, s, col=LAB, size=3.4):
    return f"<text x='{x}' y='{y}' fill='{col}' font-size='{size}' text-anchor='middle' font-weight='600'>{s}</text>"
def hdim(x0, x1, y, s, col, size=3.2, up=True):   # размерная линия с засечками и подписью
    return (line(x0, y, x1, y, col, 0.6) + line(x0, y-1.2, x0, y+1.2, col, 0.6) + line(x1, y-1.2, x1, y+1.2, col, 0.6)
            + txt((x0+x1)/2, y - 1.4 if up else y + 4.0, s, col, size))
def svg(inner, label, vb='-6 -12 82 94'):
    defs = ("<defs><pattern id='sad24' width='3' height='3' patternUnits='userSpaceOnUse'>"
            "<path d='M0,3 L3,0' stroke='#5fd38d' stroke-width='0.35' stroke-opacity='0.55'/></pattern></defs>")
    return f"<svg viewBox='{vb}' role='img' aria-label='{label}' style='max-width:560px'>{defs}{inner}</svg>"
def fig(inner, cap): return f"<figure class='st'>{inner}" + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"

def base(dim=False):
    """весь чертёж условия: белая полоса, серая полоса, сад с текстурой"""
    k = 0.45 if dim else 1
    s = ring(0, L, M0, M1, LAB, 0.18 * k) + ring(M0, M1, S0, S1, '#8a96a3', 0.85 * k)
    s += rect(S0, S0, S1, S1, DIM if dim else INK, 0.4, 'url(#sad24)', 1)
    s += rect(0, 0, L, L, DIM if dim else INK, 0.6) + rect(M0, M0, M1, M1, DIM if dim else INK, 0.5)
    return s

V = {}
# 1. рисунок условия — крупно, на первой строке после условия
V['квадрат 6 м × 6 м'] = fig(svg(base(), 'Рисунок условия', '-4 -4 78 78'), 'Рисунок из условия.')

# 2. буквы: 600, 25, 550, x
s = base(True)
s += hdim(0, L, L + 5, '600', INK, up=False)
s += hdim(M0, M1, -4, '550', BLUE) + rect(M0, M0, M1, M1, BLUE, 0.7, dash=True)
s += line(0, 24, W, 24, LAB, 1.3) + txt(W/2, 22, '25', LAB, 3.0)
s += line(M0, 46, M0 + G, 46, GOLD, 1.4) + txt(M0 + G/2, 44, 'x', GOLD, 3.4)
s += txt(L/2, L/2 + 1.2, 'сад', GREEN, 3.6)
V['x — сторона серой плитки.'] = fig(svg(s, 'Буквы'),
  "Белая полоса — 25; <b style='color:#5ba8f5'>средний квадрат</b> — 550; <b style='color:#f0a83c'>x</b> — сторона серой плитки.")

# 3. а) белые плитки — белая полоса = участок без среднего квадрата; одна плитка 25 × 25 в углу
s = base(True) + ring(0, L, M0, M1, GOLD, 0.45) + rect(M0, M0, M1, M1, BLUE, 0.8, dash=True)
s += rect(0, 0, W, W, GOLD, 0.9, GOLD, 0.85) + txt(W/2, W + 4.2, '25', GOLD, 3.0)
s += hdim(0, L, L + 5, '600', GOLD, up=False) + hdim(M0, M1, -4, '550', BLUE)
V['белая полоса — участок без среднего квадрата'] = fig(svg(s, 'а) белая полоса'),
  "<b style='color:#f0a83c'>Белая полоса</b>: участок 600 × 600 без <b style='color:#5ba8f5'>среднего квадрата</b> 550 × 550; одна плитка 25 × 25.")

# 4. б) сторона серой плитки = ширина серой полосы
s = base(True) + rect(M0, M0, M0 + G, M0 + G, GOLD, 0.9, GOLD, 0.85)
s += line(M0, 46, M0 + G, 46, GOLD, 1.4) + txt(M0 + G/2, 44, 'x', GOLD, 3.4)
s += line(M0 + G + 1.5, M0, M0 + G + 1.5, M0 + G, GOLD, 0.6) + txt(M0 + G + 4.5, M0 + G/2 + 1.2, 'x', GOLD, 3.0)
V['сторона серой плитки — это x, ширина серой полосы'] = fig(svg(s, 'б) серая плитка'),
  "Серая плитка в углу серой полосы: x × x.")

# 5. в) серые плитки — серая полоса = средний квадрат без сада
s = base(True) + ring(M0, M1, S0, S1, GOLD, 0.55)
s += rect(M0, M0, M0 + G, M0 + G, GOLD, 0.9, GOLD, 0.9) + txt(M0 + G/2, M0 + G + 4.2, 'x', GOLD, 3.0)
s += hdim(M0, M1, -4, '550', BLUE) + hdim(S0, S1, L + 5, 'сторона сада ?', GREEN, up=False)
s += line(S0, S1, S0, L + 5, GREEN, 0.3, True) + line(S1, S1, S1, L + 5, GREEN, 0.3, True)
V['серая полоса — средний квадрат без сада'] = fig(svg(s, 'в) серая полоса'),
  "<b style='color:#f0a83c'>Серая полоса</b>: <b style='color:#5ba8f5'>средний квадрат</b> 550 × 550 без <b style='color:#5fd38d'>сада</b>; одна плитка x × x.")

# 6. раздел «Найдём x»: сторона среднего квадрата = x + 528 + x
s = base(True) + hdim(M0, M1, -4, '550', BLUE)
y = L / 2
s += line(M0, y, S0, y, GOLD, 1.5) + line(S0, y, S1, y, GREEN, 1.5) + line(S1, y, M1, y, GOLD, 1.5)
for X in (M0, S0, S1, M1): s += line(X, y - 1.3, X, y + 1.3, LAB, 0.6)
s += txt((M0 + S0)/2, y - 2, 'x', GOLD, 3.4) + txt((S1 + M1)/2, y - 2, 'x', GOLD, 3.4) + txt(L/2, y - 2, '528', GREEN, 3.4)
V['сторона среднего квадрата складывается из стороны сада и двух серых плиток'] = fig(svg(s, 'Сторона среднего квадрата'),
  "<b style='color:#5ba8f5'>550</b> = <b style='color:#f0a83c'>x</b> + <b style='color:#5fd38d'>528</b> + <b style='color:#f0a83c'>x</b>.")

json.dump(V, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(len(V), 'figures')
