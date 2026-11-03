#!/usr/bin/env python3
"""Сборка HTML решений корпуса одного типа (этап В): склейка <код>/_md/*.md в порядке списка → md2html → --check.

Запуск из корня репо:
    python3 26-27/nandu_level2/resheniya_korpusa/sobrat.py T1
Список задач, ответы и расхождения агентов — <код>/_md/spisok.json:
    {"tip": "Т1", "nazvanie": "система уравнений", "obrazec": "T1_nac_2023_4",
     "zadachi": [["T1_nac_2025_1", "нац 2025 I №1", "три лагеря", "ответ", "расхождение агентов или пусто"], ...]}
Порядок задач — от свежих к старым (промпт сессии). Образец типа в список не входит: он решён идеально.
Список на чтение строится сам: все задачи с 🆕 приёмом, с расхождением агентов, с «отступлением от образца»,
плюс каждая десятая из остальных. Он стоит наверху страницы типа.
Ненулевой код, если --check нашёл потерянный или дописанный текст.
"""
import json, os, re, subprocess, sys

K = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(K, '..', '..', '..'))
TOOL = os.path.join(ROOT, 'tools', 'md2html.py')

kod = sys.argv[1] if len(sys.argv) > 1 else 'T1'
M = os.path.join(K, kod, '_md')
S = json.load(open(os.path.join(M, 'spisok.json')))
typ = S['tip']
items = S['zadachi']
src = {f: open(os.path.join(M, f + '.md')).read() for f, *_ in items}

# ——— список на чтение (промпт сессии, п. 9) ———
def pometki(t, what):
    return [re.sub(r'\s+', ' ', x).strip() for x in re.findall(r'<!--\s*' + what + r'\s*:?\s*(.*?)-->', t, re.S)]

# Отступления от образца есть почти у каждой задачи (буквы, число уравнений, ход с множителем), поэтому на чтение
# идёт не каждая задача с отступлением, а первая задача каждого вида отступления: шестой элемент строки spisok.json —
# вид отступления, который родитель читает на этой задаче (замечание по ней правится во всех задачах того же вида).
# Все отступления по задачам — отдельной таблицей ниже списка.
chtenie, ostalnye, vse_otst = [], [], []
for row in items:
    f, istochnik, sujet, otvet, rash = row[:5]
    vid = row[5] if len(row) > 5 else ''
    t = src[f]
    novye = pometki(t, '🆕 приём вне реестра') + pometki(t, '🆕 приём(?! вне)')
    otst = pometki(t, 'отступление от образца')
    if otst:
        vse_otst.append((istochnik, otst))
    why = []
    if novye: why.append('🆕 ' + '; '.join(novye))
    if rash: why.append('расхождение агентов: ' + rash)
    if vid: why.append('первая задача вида: ' + vid)
    if why:
        chtenie.append((f, istochnik, why))
    else:
        ostalnye.append((f, istochnik))
for i, (f, istochnik) in enumerate(ostalnye):
    if i % 10 == 0:
        chtenie.append((f, istochnik, ['каждая десятая из остальных']))
chtenie.sort(key=lambda x: [f for f, *_ in items].index(x[0]))

head = [f'# Решения корпуса. {typ} — {S["nazvanie"]}', '',
        f'Olimpíada Ñandú · Segundo Nivel · этап В · {len(items)} задач национала, регионала и провинциала '
        f'(образец `{S["obrazec"]}` решён идеально и сюда не входит) · статус — `26-27/nandu_level2/nandu_n2_roadmap.md`', '',
        '**Прочитать родителю.**', '',
        '| задача | почему в списке |', '|---|---|']
for f, istochnik, why in chtenie:
    head.append(f'| {istochnik} | {" · ".join(why)} |')
head += ['', '**Все задачи.**', '', '| № | задача | сюжет | ответ |', '|---|---|---|---|']
for n, row in enumerate(items, 1):
    head.append(f'| {n} | {row[1]} | {row[2]} | {row[3]} |')
if vse_otst:
    head += ['', '**Все отступления от образца.**', '', '| задача | отступления |', '|---|---|']
    for istochnik, otst in vse_otst:
        head.append(f'| {istochnik} | {" ".join(f"{k}) {o}" for k, o in enumerate(otst, 1))} |')

body = '\n'.join(src[f].rstrip() for f, *_ in items)
# 🆕 приём виден родителю на странице; отступления — в таблице «Прочитать родителю», в тексте только в исходнике
def novyi(m):
    tekst = re.sub(r'\s+', ' ', m.group(2))
    return '*🆕 Приём' + (m.group(1) or '') + ': ' + tekst + '*'
body = re.sub(r'<!--\s*🆕 приём( вне реестра)?\s*:?\s*(.*?)\s*-->', novyi, body, flags=re.S)
body = re.sub(r'(?s)\n?<!--.*?-->', '', body)
md = os.path.join(M, f'nandu_n2_korpus_{kod}.md')
open(md, 'w').write('\n'.join(head) + '\n\n' + body + '\n')

out = os.path.join(K, kod)
vis = {}
for f, *_ in items:
    j = os.path.join(M, f + '.vis.json')
    if os.path.exists(j):
        vis.update(json.load(open(j)))
vp = md[:-3] + '.vis.json'
json.dump(vis, open(vp, 'w'), ensure_ascii=False, indent=1)

# ——— ⚠-проверки: те же, что в idealnye_resheniya/_md/sobrat.py ———
# Артефакт первой идеи — кроме геометрии (Т2…), систем (Т1…) и Т4′ (ответ — числа и места, формулы «N = …» нет).
LINT_SKIP = ('Т2', 'Т1')
NO_N = ('Т4′',)
BANNED = ('Жанр ответа', 'Заметь главное', '**Обозначения', 'С чего начать', 'План готов')
if not typ.startswith(LINT_SKIP + NO_N):
    for f, *_ in items:
        paras = [x.strip() for x in src[f].split('\n\n') if x.strip()]
        q = next((i for i, x in enumerate(paras) if '?' in x and not x.startswith('**Условие')), 0)
        k = next((i for i, x in enumerate(paras) if re.match(r'^(>\s*✅\s*)?N(\([^)]*\))?\s*=', x)), None)
        if k is None:
            print(f'  ⚠ артефакт: {f} — нет формулы «N = …»'); continue
        pre = [x for x in paras[q + 1:k] if not x.startswith('<small>') and not x.startswith('<!--')]
        if len(pre) > 9:
            print(f'  ⚠ артефакт: {f} — до «N = …» {len(pre)} абзацев (больше 9)')
        for w in BANNED:
            if any(w in x for x in paras[:k]):
                print(f'  ⚠ артефакт: {f} — до «N = …» стоит «{w.strip("*")}»')
        art = re.sub(r'[⟪⟫⦃⦄⦅⦆⟬⟭]', '', paras[k])
        for w in ('сумма', 'по всем', '…', '...', 'для каждого'):
            if w in art:
                print(f'  ⚠ артефакт: {f} — первая формула — заглушка («{w}»): операнды должны быть названы сразу')
        heads = ' '.join(re.sub(r'[⟪⟫⦃⦄⦅⦆⟬⟭]', '', x) for x in paras[k:] if re.match(r'^\*\*\d+\.', x))
        for op in re.findall(r'N\([^)]*\)', art.split('=', 1)[1]):
            if op not in heads:
                print(f'  ⚠ артефакт: {f} — операнд {op} первой формулы не стоит в заголовке раздела')
        for x in paras[k:]:
            m = re.match(r'^\*\*(\d+)\. (.+?)\*\*', x)
            if m and 'N(' not in m.group(2):
                print(f'  ⚠ артефакт: {f} — заголовок «{m.group(1)}. {m.group(2)}» не называет операнд')
# Запрещённые слова болтовни — во всех типах
for f, *_ in items:
    for w in BANNED:
        if w in src[f]:
            print(f'  ⚠ болтовня: {f} — «{w.strip("*")}»')
# Одна мысль — одна строка
SENT = re.compile(r'(?<=[.!?])\s+(?=[«*(]?[А-ЯЁA-Z])')
for f, *_ in items:
    t_ = re.sub(r'(?s)<!--.*?-->', '', src[f])
    body_ = t_.split('Вопросы:', 1)[-1] if 'Вопросы:' in t_ else t_
    incode = False
    for ln in body_.split('\n'):
        t = ln.strip()
        if t.startswith('```'): incode = not incode; continue
        if incode or not t or t.startswith(('- ', '|', '<small>', '**Ответ на задачу', '*Проверено', ':::', '#')): continue
        t = t.lstrip('> ').strip()
        if t.startswith('**Условие') or '?' in t or re.match(r'^\*\*\d+\.', t): continue
        t = re.sub(r'^\*\*[^*]+\*\*\s*', '', t)
        parts = [x for x in SENT.split(t) if x.strip()]
        if len(parts) > 1:
            print(f'  ⚠ склейка: {f} — {len(parts)} мысли в строке: «{t[:70]}…»')
# Формула без левой части — строка из одних чисел и знаков с «=» вне кода (кроме систем: там проверка подстановкой)
if not typ.startswith(LINT_SKIP):
    for f, *_ in items:
        incode = False
        for ln in src[f].split('\n'):
            if ln.strip().startswith('```'): incode = not incode; continue
            if not incode and '=' in ln and re.fullmatch(r'[0-9][0-9 ·+−×:()=]*', ln.strip()):
                print(f'  ⚠ формула без левой части: {f} — «{ln.strip()[:70]}»')
# «Артефакт» — внутренняя кухня
for f, *_ in items:
    for ln in re.sub(r'(?s)<!--.*?-->', '', src[f]).split('\n'):
        if re.search(r'артефакт', ln, re.I):
            print(f'  ⚠ артефакт в тексте: {f} — «{ln.strip()[:70]}»')
# Тире перед числом читается как минус
for f, *_ in items:
    incode = False
    for ln in src[f].split('\n'):
        if ln.strip().startswith('```'): incode = not incode; continue
        if not incode and re.search(r' — [0-9]', ln):
            print(f'  ⚠ тире-минус: {f} — «{ln.strip()[:70]}»')
# Ссылок «как в образце» в тексте нет (промпт сессии, п. 4)
for f, *_ in items:
    t = re.sub(r'(?s)<!--.*?-->', '', src[f])
    if re.search(r'образц|образе?ц', t, re.I):
        print(f'  ⚠ ссылка на образец в тексте: {f}')

r = subprocess.run([sys.executable, TOOL, md, out, vp], capture_output=True, text=True)
for line in (r.stdout + r.stderr).splitlines():
    if 'без якоря' in line or 'Traceback' in line:
        print('  ⚠', line)
print('сборка:', (r.stdout + r.stderr).strip().splitlines()[-3:])
c = subprocess.run([sys.executable, TOOL, '--check', md, out], capture_output=True, text=True)
print('check rc =', c.returncode, [l for l in c.stdout.splitlines() if 'потеряно' in l or 'дописано' in l])
print('на чтение:', len(chtenie), 'из', len(items))
for f, istochnik, why in chtenie:
    print(f'  {istochnik}: {" · ".join(why)}')
sys.exit(c.returncode | r.returncode)
