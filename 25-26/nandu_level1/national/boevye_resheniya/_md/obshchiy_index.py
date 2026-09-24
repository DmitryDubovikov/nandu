"""Общий index.html боевых решений: все годы и все задачи на одной странице.

Стили берутся из index.html любого года — страница остаётся самодостаточной.
Запуск из корня репо после пересборки годов:
    python3 25-26/nandu_level1/national/boevye_resheniya/_md/obshchiy_index.py
"""
import glob, html, os, re

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
years = sorted((d for d in os.listdir(B) if re.fullmatch(r'\d{4}', d)), reverse=True)
head = open(os.path.join(B, years[0], 'index.html')).read().split('<body', 1)[0]
head = re.sub(r'<title>.*?</title>', '<title>Боевые решения национала</title>', head, flags=re.S)

out = ['<body><div class="col">',
       '<h1>Национальный этап — боевые решения</h1>',
       '<p class="sub">Olimpíada Ñandú · Nivel 1 · Certamen Nacional · 2013–2025</p>',
       '<div class="pre"><p class="st">Одна страница — одна задача. До 2017 года тур был однодневный '
       '(3 задачи), с 2017 — два дня по 3 задачи. Номер года ведёт к таблице ответов и порядку решения на туре.</p></div>']
for y in years:
    out.append(f'<h2><a href="{y}/index.html">{y}</a></h2>')
    for p in sorted(glob.glob(os.path.join(B, y, '[0-9][0-9]-*.html'))):
        m = re.search(r'<h[12][^>]*>(.*?)</h[12]>', open(p).read(), re.S)
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else os.path.basename(p)
        out.append(f'<a class="ix" href="{y}/{os.path.basename(p)}"><b>{html.escape(html.unescape(title))}</b><span></span></a>')
out.append('</div></body></html>')
open(os.path.join(B, 'index.html'), 'w').write(head + '\n'.join(out) + '\n')
print('годов:', len(years))
