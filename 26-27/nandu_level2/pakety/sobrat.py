#!/usr/bin/env python3
"""Сборка HTML учебника одного типа (этап Г): учебник + четыре страницы задач.

Запуск из корня репо:
    python3 26-27/nandu_level2/pakety/sobrat.py T1
Исходники (промпт pakety/PROMPT_uchebnik_tipa.md):
    pakety/<код>/<код>_stranica.md   — учебник: шапка, приёмы с разобранными примерами, «## Задачи» со ссылками
    pakety/<код>/_md/<код>-30.md, -50.md, -70.md — задачи с решениями, раздел «## <код>-30-1 — <сюжет>»
    pakety/<код>/_md/<код>-O.md      — условия на опознание, раздел «## <код>-O-1 — <сюжет>»
    pakety/<код>/_md/perebor/*.py    — переборы (в сборку не входят)
Выход — сплошные страницы без левой колонки:
    pakety/<код>/index.html (учебник), pakety/<код>/<код>-30.html, -50, -70, -O.
Ненулевой код, если md2html --check нашёл потерянный или дописанный текст.
"""
import glob, json, os, re, shutil, subprocess, sys, tempfile

K = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(K, '..', '..', '..'))
TOOL = os.path.join(ROOT, 'tools', 'md2html.py')

kod = sys.argv[1] if len(sys.argv) > 1 else 'T1'
P = os.path.join(K, kod)
M = os.path.join(P, '_md')
kod_ru = kod.replace('T', 'Т', 1).replace('pppp', '⁗').replace('ppp', '‴').replace('pp', '″').replace('p', '′')
LEVELS = {'30': 'задачи 30 %', '50': 'задачи 50 %', '70': 'задачи 70 %', 'O': 'условия на опознание'}

src = {'stranica': open(os.path.join(P, f'{kod}_stranica.md')).read()}
for lv in LEVELS:
    f = os.path.join(M, f'{kod}-{lv}.md')
    if os.path.exists(f):
        src[lv] = open(f).read()


def demote(t):
    """Заголовки на уровень ниже: страница md2html = раздел ##, всё внутри — ### и глубже."""
    return re.sub(r'(?m)^(#{1,5}) ', lambda m: '#' + m.group(1) + ' ', t)


def strip_comments(t):
    return re.sub(r'(?s)\n?<!--.*?-->', '', t)


# ——— ⚠-проверки: те же, что в idealnye_resheniya/_md/sobrat.py и resheniya_korpusa/sobrat.py ———
BANNED = ('Жанр ответа', 'Заметь главное', '**Обозначения', 'С чего начать', 'План готов',
          'Проверено перебором', 'перебором программой')
for k, t in src.items():
    for w in BANNED:
        if w in t:
            print(f'  ⚠ болтовня или кухня: {k} — «{w.strip("*")}»')
SENT = re.compile(r'(?<=[.!?])\s+(?=[«*(]?[А-ЯЁA-Z])')
for k, t in src.items():
    incode = False
    for ln in strip_comments(t).split('\n'):
        s = ln.strip()
        if s.startswith('```'): incode = not incode; continue
        if incode or not s or s.startswith(('- ', '|', '<small>', '**Ответ на задачу', '*Проверено', ':::', '#')): continue
        s = s.lstrip('> ').strip()
        if s.startswith('**Условие') or '?' in s or re.match(r'^\*\*\d+\.', s): continue
        s = re.sub(r'^\*\*[^*]+\*\*\s*', '', s)
        if len([x for x in SENT.split(s) if x.strip()]) > 1:
            print(f'  ⚠ склейка: {k} — «{s[:70]}…»')
for k, t in src.items():
    for ln in strip_comments(t).split('\n'):
        if re.search(r'артефакт', ln, re.I):
            print(f'  ⚠ артефакт в тексте: {k} — «{ln.strip()[:70]}»')
for k, t in src.items():
    incode = False
    for ln in t.split('\n'):
        if ln.strip().startswith('```'): incode = not incode; continue
        if not incode and re.search(r' — [0-9]', ln) and not re.match(r'^#+ ', ln):
            print(f'  ⚠ тире-минус: {k} — «{ln.strip()[:70]}»')
for k, t in src.items():
    body = strip_comments(t)
    if k == 'stranica':   # шапка учебника ссылается на образец типа нарочно (решение родителя 3.11.2026)
        body = body.split('**Образец решения:**', 1)[-1].split('\n', 1)[-1]
    if re.search(r'образе?ц', body, re.I):
        print(f'  ⚠ ссылка на образец в тексте: {k}')
# Один сюжет — один раз на учебник с наборами (промпт, п. 9): «## <номер> — <сюжет>»
sujety = {}
for k, t in src.items():
    for m in re.finditer(r'(?m)^## (\S+) — (.+)$', t):
        sujety.setdefault(m.group(2).strip().lower(), []).append(m.group(1))
for s, n in sujety.items():
    if len(n) > 1:
        print(f'  ⚠ один сюжет дважды: «{s}» — {", ".join(n)}')
# Номера задач идут подряд и совпадают с уровнем файла
for lv in LEVELS:
    if lv in src:
        nums = re.findall(rf'(?m)^## {re.escape(kod)}-{lv}-(\d+) — ', src[lv])
        if [int(x) for x in nums] != list(range(1, len(nums) + 1)):
            print(f'  ⚠ нумерация {kod}-{lv}: {nums}')

# ——— сборка: каждая страница — отдельный документ md2html из одной главы ———
def title_and_rest(t, fallback):
    """Первая строка «# …» — титул страницы; без неё титул — fallback."""
    t = strip_comments(t).lstrip()
    if t.startswith('# '):
        first, rest = (t.split('\n', 1) + [''])[:2]
        return first[2:].strip(), rest
    return fallback, t


def hide_solutions(t, lv):
    """Наборы: условие видно, решение и ответ — под свёрнутым блоком (решение родителя 4.11.2026).

    Раздел задачи «## <номер> — <сюжет>»: всё от первого «### …» (у опознания — от «**Приём:**») до конца
    раздела уходит в <details>, который md2html рисует свёрнутым.
    """
    start = r'^\*\*Приём:\*\*' if lv == 'O' else r'^### '
    summary = 'Приём и формула' if lv == 'O' else 'Решение и ответ'
    parts = re.split(r'(?m)^(?=## )', t)
    out = []
    for p in parts:
        m = re.search(start, p, re.M)
        if p.startswith('## ') and m:
            body = p[m.start():].rstrip()
            p = p[:m.start()] + f'<details>\n<summary>{summary}</summary>\n\n{body}\n\n</details>\n\n'
        out.append(p)
    return ''.join(out)


pages = {'index.html': title_and_rest(src['stranica'], f'Учебник {kod_ru}')}
for lv, name in LEVELS.items():
    if lv in src:
        title, rest = title_and_rest(src[lv], f'{kod_ru} · {name}')
        pages[f'{kod}-{lv}.html'] = (title, f'[← учебник {kod_ru}](index.html)\n\n' + hide_solutions(rest, lv))

for stale in glob.glob(os.path.join(P, '*.html')):
    os.remove(stale)
rc = 0
for out, (title, rest) in pages.items():
    tag = out[:-5].replace('index', 'uchebnik')
    md = os.path.join(M, f'nandu_n2_paket_{tag}.md')
    # одна глава на страницу: титул документа отдельно, весь текст — внутри одного «##»
    body = f'# Учебник {kod_ru}\n\n---\n\n## {title}\n\n{demote(rest).strip()}\n'
    open(md, 'w').write(body)
    vis = {}
    for j in glob.glob(os.path.join(M, '**', '*.vis.json'), recursive=True):
        if not os.path.basename(j).startswith('nandu_n2_paket_'):
            vis.update(json.load(open(j)))
    vp = md[:-3] + '.vis.json'
    json.dump(vis, open(vp, 'w'), ensure_ascii=False, indent=1)
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, TOOL, md, tmp, vp], capture_output=True, text=True)
        for line in (r.stdout + r.stderr).splitlines():
            if 'без якоря' in line or 'Traceback' in line:
                print('  ⚠', out, line)
        made = sorted(f for f in os.listdir(tmp) if f != 'index.html')
        if len(made) != 1:
            print(f'  ⚠ {out}: md2html дал {len(made)} страниц вместо одной')
        html = open(os.path.join(tmp, made[0])).read()
        open(os.path.join(P, out), 'w').write(html)
        c = subprocess.run([sys.executable, TOOL, '--check', md, os.path.join(P, out)],
                           capture_output=True, text=True)
        bad = [l for l in c.stdout.splitlines() if l.startswith('  ✗') or l.startswith('  +')]
        print(f'{out}: check rc = {c.returncode}', bad[:6])
        rc |= c.returncode | r.returncode

# Ссылки учебника ведут на существующие страницы
for href in re.findall(r'\]\(([^)\s#]+\.html)', src['stranica']):
    if not os.path.exists(os.path.normpath(os.path.join(P, href))):
        print(f'  ⚠ битая ссылка в учебнике: {href}')
sys.exit(rc)
