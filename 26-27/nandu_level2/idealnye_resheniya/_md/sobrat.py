#!/usr/bin/env python3
"""Сборка HTML идеальных решений одной фазы: склейка _md/<образец>.md в порядке роадмапа → md2html → --check.

Запуск из корня репо:
    python3 26-27/nandu_level2/idealnye_resheniya/_md/sobrat.py 1
Правится исходник образца в _md/, потом фаза пересобирается целиком.
Таблица ответов в шапке — FAZY ниже: при смене ответа править и её.
Ненулевой код, если --check нашёл потерянный или дописанный текст.
"""
import os, re, subprocess, sys

M = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(M)
ROOT = os.path.abspath(os.path.join(B, '..', '..', '..'))
TOOL = os.path.join(ROOT, 'tools', 'md2html.py')

# порядок = порядок роадмапа (26-27/nandu_level2/nandu_n2_roadmap.md)
FAZY = {
    '1': ('Группа 1 — подтипы, которые встречаются уже на интересколяре и зонале', [
        ('T1_nac_2023_4', 'Т1', 'монеты $1/2/5/10', '$1 — 98, $2 — 120, $5 — 65, $10 — 136'),
        ('T2_prov_2022_2', 'Т2', 'ABDEF, пять периметров', 'P(EFG) = 90 см; P(ACDEF) = 192 см; площадь ABDEF = 1170 см²; площадь BCD = 864 см²'),
        ('T3p_nac_2019_6', 'Т3′', 'полоска 1×6, произведение 24', '384 способа'),
        ('T1p_nac_2024_4', 'Т1′', 'смена × спорт', 'волейбол 1116; дневная смена 620; школа 1550; хоккей 434'),
        ('T3_prov_2025_3', 'Т3', 'пароль с семёркой', '810 паролей'),
        ('T3pp_reg_2018_3', 'Т3″', 'четырёхзначные < 2018, одна 7, кратны 3', '76 чисел'),
        ('T2ppp_nac_2017_2', 'Т2‴', 'квадрат из трапеций, закрашено 416', 'квадрат 128 см²; незакрашенное 608 см²; MNPQ 288 см²; периметр ABCD 128 см'),
        ('T1pp_nac_2025_4', 'Т1″', '1200 фишек в четырёх коробках', 'синяя 165, белая 420, красная 165, зелёная 450'),
        ('T3ppp_nac_2017_6', 'Т3‴', 'цифры 4, 5, 6, сумма цифр 30', '170 чисел'),
    ]),
    '2': ('Группа 2 — подтипы, которые впервые нужны на провинциале и регионале', [
        ('T2p_nac_2021_5', 'Т2′', 'прямоугольник ABCD, площадь ABPR 735', 'ADE 294 см²; периметр ABCE 168 см; AMNE 882 см²'),
        ('T5_nac_2018_3', 'Т5', 'кузнечик на круге из 1000 клеток, шаг 35', '800 клеток'),
        ('T6_prov_2023_3', 'Т6', 'восемь кружков, три цвета', '132 способа'),
        ('T1ppp_nac_2024_1', 'Т1‴', '30 оценок с суммой 93', 'пять возможностей: (6, 17, 5, 2), (10, 11, 5, 4), (14, 5, 5, 6), (11, 7, 10, 2), (15, 1, 10, 4)'),
        ('T4_nac_2023_1', 'Т4', 'три треугольника, числа 1–10, равные суммы', '8 способов'),
        ('T2pp_nac_2015_2', 'Т2″', 'трапеция ABCD, площадь ODE 735', 'CEO 1225 см²; ADE 1323 см²; ABCD 1274 см²; BCEO 1617 см²'),
        ('T1pppp_reg_2013_1', 'Т1⁗', 'День весны: проценты присутствующих, 836 спортсменов', 'развлечения 912; одно занятие 1292; не пришли 320'),
    ]),
}

faza = sys.argv[1] if len(sys.argv) > 1 else '1'
title, items = FAZY[faza]
head = [f'# Идеальные решения образцов. {title}', '',
        'Olimpíada Ñandú · Segundo Nivel · сезон 26-27 · статус каждого решения — в `26-27/nandu_level2/nandu_n2_roadmap.md`', '',
        '| № | тип | задача | ответ |', '|---|---|---|---|']
for n, (_, typ, sujet, otvet) in enumerate(items, 1):
    head.append(f'| {n} | {typ} | {sujet} | {otvet} |')
body = '\n'.join(open(os.path.join(M, f + '.md')).read().rstrip() for f, *_ in items)
# авторские пометки: «новая фраза» видна родителю на странице, остальные комментарии (иллюстрации) — только в исходнике
body = re.sub(r'<!--\s*новая фраза:\s*(.*?)\s*-->', r'*🆕 Новая фраза — \1.*', body)
body = re.sub(r'(?s)\n?<!--.*?-->', '', body)
md = os.path.join(M, f'nandu_n2_idealnye_faza{faza}.md')
open(md, 'w').write('\n'.join(head) + '\n\n' + body + '\n')

out = os.path.join(B, f'faza{faza}')
os.makedirs(out, exist_ok=True)
for f in os.listdir(out):
    if f.endswith('.html'):
        os.remove(os.path.join(out, f))
# иллюстрации: _md/<образец>.vis.json (якорь — фраза из абзаца → <figure>) сливаются в один словарь фазы
import json
vis = {}
for f, *_ in items:
    j = os.path.join(M, f + '.vis.json')
    if os.path.exists(j):
        vis.update(json.load(open(j)))
vp = md[:-3] + '.vis.json'
json.dump(vis, open(vp, 'w'), ensure_ascii=False, indent=1)
# ⛔ артефакт первой идеи (CLAUDE.md, верхний блок; _md/CHECKLIST.md): ловим запаздывающий артефакт и заголовки-темы.
# Геометрия (Т2…) и системы (Т1, Т1″) — исключения; Т1′ — цепочка со схемой-стрелками вместо формулы.
LINT_SKIP = ('Т2', 'Т1')
# «Способ — …» (что считается одним способом) — законная предпосылка, родитель сам её потребовал в №3
BANNED = ('Жанр ответа', 'Заметь главное', '**Обозначения', 'С чего начать', 'План готов')
for f, typ, *_ in items:
    if typ.startswith(LINT_SKIP):
        continue
    paras = [x.strip() for x in open(os.path.join(M, f + '.md')).read().split('\n\n') if x.strip()]
    q = next((i for i, x in enumerate(paras) if '?' in x and not x.startswith('**Условие')), 0)
    k = next((i for i, x in enumerate(paras) if re.match(r'^(>\s*✅\s*)?N(\([^)]*\))?\s*=', x)), None)
    if k is None:
        print(f'  ⚠ артефакт: {f} — нет формулы «N = …»'); continue
    pre = [x for x in paras[q + 1:k] if not x.startswith('<small>')]
    if len(pre) > 9:
        print(f'  ⚠ артефакт: {f} — до «N = …» {len(pre)} абзацев (больше 9)')
    for w in BANNED:
        if any(w in x for x in paras[:k]):
            print(f'  ⚠ артефакт: {f} — до «N = …» стоит «{w.strip("*")}»')
    # заглушка — не артефакт (CHECKLIST «Заглушка — не артефакт», №9 2.11.2026): операнды конкретны,
    # и каждый операнд первой формулы назван в заголовке раздела
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
# Одна мысль — одна строка (родитель 2.11.2026: «разные мысли разными абзацами»): ловим строки из двух и более предложений
# во всех образцах, включая геометрию; условие, код, списки, «Ответ на задачу» и строку проверки не трогаем.
SENT = re.compile(r'(?<=[.!?])\s+(?=[«*(]?[А-ЯЁA-Z])')
for f, typ, *_ in items:
    txt_ = open(os.path.join(M, f + '.md')).read()
    body = txt_.split('Вопросы:', 1)[-1] if 'Вопросы:' in txt_ else txt_
    incode = False
    for ln in body.split('\n'):
        t = ln.strip()
        if t.startswith('```'): incode = not incode; continue
        if incode or not t or t.startswith(('- ', '|', '<small>', '**Ответ на задачу', '*Проверено', ':::', '#')): continue
        t = t.lstrip('> ').strip()
        if t.startswith('**Условие') or '?' in t or re.match(r'^\*\*\d+\.', t): continue
        t = re.sub(r'^\*\*[^*]+\*\*\s*', '', t)      # ярлык «**Идея.**», «**⚠ Ловушки.**» — не предложение
        parts = [x for x in SENT.split(t) if x.strip()]
        if len(parts) > 1:
            print(f'  ⚠ склейка: {f} — {len(parts)} мысли в строке: «{t[:70]}…»')
# Формула без левой части (родитель 2.11.2026, №12: «формула без левой части… чем мы тут считаем?»): строка
# «3 · 3 · 2 = 18» вне кода в образцах счёта — ⚠; левая часть называет, что считается: N(раскрасок 1, 3, 5 в два цвета) = …
for f, typ, *_ in items:
    if typ.startswith(LINT_SKIP):
        continue
    incode = False
    for ln in open(os.path.join(M, f + '.md')).read().split('\n'):
        if ln.strip().startswith('```'): incode = not incode; continue
        if not incode and re.fullmatch(r'[0-9][0-9 ·+−×:()]*= *[0-9]+', ln.strip()):
            print(f'  ⚠ формула без левой части: {f} — «{ln.strip()[:70]}»')
# «Артефакт» — внутренняя кухня, в тексте решения не пишется (родитель 2.11.2026: «в математике так не принято»)
for f, *_ in items:
    t = re.sub(r'(?s)<!--.*?-->', '', open(os.path.join(M, f + '.md')).read())
    for ln in t.split('\n'):
        if re.search(r'артефакт', ln, re.I):
            print(f'  ⚠ артефакт в тексте: {f} — «{ln.strip()[:70]}»')
# Тире перед числом читается как минус («каждая цифра — 6» = «−6»; родитель 2.11.2026): «равна 6», «:», скобки
for f, *_ in items:
    incode = False
    for ln in open(os.path.join(M, f + '.md')).read().split('\n'):
        if ln.strip().startswith('```'): incode = not incode; continue
        if not incode and re.search(r' — [0-9]', ln):
            print(f'  ⚠ тире-минус: {f} — «{ln.strip()[:70]}»')
r = subprocess.run([sys.executable, TOOL, md, out, vp], capture_output=True, text=True)
for line in (r.stdout + r.stderr).splitlines():
    if 'без якоря' in line or 'Traceback' in line:
        print('  ⚠', line)
print('сборка:', (r.stdout + r.stderr).strip().splitlines()[-3:])
c = subprocess.run([sys.executable, TOOL, '--check', md, out], capture_output=True, text=True)
print('check rc =', c.returncode, [l for l in c.stdout.splitlines() if 'потеряно' in l or 'дописано' in l])
sys.exit(c.returncode | r.returncode)
