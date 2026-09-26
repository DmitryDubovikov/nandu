#!/usr/bin/env python3
"""Страница «Все задачи коротко»: условие и блок «⚡ Коротко» каждой задачи подряд, по годам.

Цель — познакомиться со всеми задачами национала чтением, не открывая полных разборов.
Условие дублируется, чтобы не листать туда-сюда; рисунок условия и рисунок с буквами
берутся из vis.json задачи. Задачи без блока «Коротко» пропускаются.
Запуск из корня репо (его же вызывает sobrat_god.py):
    python3 25-26/nandu_level1/national/boevye_resheniya/_md/tldr_stranica.py
"""
import glob, json, os, re, sys

M = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(M)
sys.path.insert(0, os.path.abspath(os.path.join(B, '..', '..', '..', '..', 'tools')))
import md2html as mh

years = sorted((d for d in os.listdir(B) if re.fullmatch(r'\d{4}', d)), reverse=True)
# стили — со страницы задачи (там описаны .task, .tldr, .frm); скрипт проявления не берём,
# поэтому всё видно сразу, а колонка одна
page = sorted(glob.glob(os.path.join(B, years[0], '[0-9][0-9]-*.html')))[0]
head = open(page).read().split('<body', 1)[0]
head = re.sub(r'<title>.*?</title>', '<title>Все задачи коротко</title>', head, flags=re.S)
head = head.replace('</head>', '<style>.col{max-width:820px;margin:0 auto;padding:40px 22px 80px}'
                    '.col h2{margin-top:56px}.col h3{margin-top:44px}.col h3 a{color:inherit;text-decoration:none}'
                    '</style></head>')

out = ['<body><div class="col">',
       '<h1>Национальный этап — все задачи коротко</h1>',
       '<p class="sub"><a href="index.html">← все боевые решения</a></p>',
       '<div class="pre"><p class="st">Условие и конспект решения каждой задачи подряд. '
       'Знак ✂ отмечает место, где рассуждение сокращено: полностью оно расписано в разборе задачи '
       '(ссылка в заголовке). Где ✂ нет, следующий шаг прямо следует из написанного.</p></div>']
n = 0
for y in years:
    parts = sorted(glob.glob(os.path.join(M, 'parts', f'{y}_*.md')),
                   key=lambda p: int(p.rsplit('_', 1)[1][:-3]))
    pages = sorted(glob.glob(os.path.join(B, y, '[0-9][0-9]-*.html')))
    body = []
    for i, p in enumerate(parts):
        blocks = mh.parse(open(p).read())
        tl = [v for k, v in blocks if k == 'quote' and mh.is_tldr(v)]
        if not tl:
            continue
        vis = json.load(open(p[:-3] + '.vis.json')) if os.path.exists(p[:-3] + '.vis.json') else {}
        title = next(v for k, v in blocks if k == 'h2')
        href = f'{y}/{os.path.basename(pages[i])}' if i < len(pages) else f'{y}/index.html'
        body.append(f'<h3 class="st"><a href="{href}">{mh.inline(title)}</a></h3>')
        used = set()
        for k, v in blocks:
            if k == 'p' and re.match(r'^\*\*Условие[.:]', v):
                body.append(mh.render_block((k, v)))
                key = re.sub(r'\s+', ' ', re.sub(r'[*`>#|]', '', v)).strip()
                body += [f for a, f in vis.items() if a in key]
                used |= {a for a in vis if a in key}
                break
        body.append(mh.render_tldr(tl[0], vis, used))
        n += 1
    if body:
        out.append(f'<h2><a href="{y}/index.html">{y}</a></h2>')
        out += body
out.append('</div></body></html>')
open(os.path.join(B, 'vse_korotko.html'), 'w').write(head + '\n'.join(out) + '\n')
print('задач с блоком «Коротко»:', n)
