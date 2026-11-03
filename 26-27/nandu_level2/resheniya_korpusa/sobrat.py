#!/usr/bin/env python3
"""Проверка решений корпуса одного типа (этап В): те же ⚠, что в idealnye_resheniya/_md/sobrat.py. HTML не собирается.

Запуск из корня репо:
    python3 26-27/nandu_level2/resheniya_korpusa/sobrat.py T1
Список задач — <код>/_md/spisok.json:
    {"tip": "Т1", "nazvanie": "…", "obrazec": "T1_nac_2023_4",
     "zadachi": [["T1_nac_2025_1", "нац 2025 I №1", "сюжет", "ответ", "расхождение агентов или пусто", "вид отступления"], ...]}
После ⚠ печатает 🆕 приёмы и отступления от образца по задачам — вход для страницы приёмов этапа Г.
Ненулевой код, если есть ⚠.
"""
import json, os, re, sys

K = os.path.dirname(os.path.abspath(__file__))
kod = sys.argv[1] if len(sys.argv) > 1 else 'T1'
M = os.path.join(K, kod, '_md')
S = json.load(open(os.path.join(M, 'spisok.json')))
typ = S['tip']
items = S['zadachi']
src = {f: open(os.path.join(M, f + '.md')).read() for f, *_ in items}

WARN = []
def warn(s):
    WARN.append(s); print(s)

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
            warn(f'  ⚠ артефакт: {f} — нет формулы «N = …»'); continue
        pre = [x for x in paras[q + 1:k] if not x.startswith('<small>') and not x.startswith('<!--')]
        if len(pre) > 9:
            warn(f'  ⚠ артефакт: {f} — до «N = …» {len(pre)} абзацев (больше 9)')
        for w in BANNED:
            if any(w in x for x in paras[:k]):
                warn(f'  ⚠ артефакт: {f} — до «N = …» стоит «{w.strip("*")}»')
        art = re.sub(r'[⟪⟫⦃⦄⦅⦆⟬⟭]', '', paras[k])
        for w in ('сумма', 'по всем', '…', '...', 'для каждого'):
            if w in art:
                warn(f'  ⚠ артефакт: {f} — первая формула — заглушка («{w}»): операнды должны быть названы сразу')
        heads = ' '.join(re.sub(r'[⟪⟫⦃⦄⦅⦆⟬⟭]', '', x) for x in paras[k:] if re.match(r'^\*\*\d+\.', x))
        for op in re.findall(r'N\([^)]*\)', art.split('=', 1)[1]):
            if op not in heads:
                warn(f'  ⚠ артефакт: {f} — операнд {op} первой формулы не стоит в заголовке раздела')
        for x in paras[k:]:
            m = re.match(r'^\*\*(\d+)\. (.+?)\*\*', x)
            if m and 'N(' not in m.group(2):
                warn(f'  ⚠ артефакт: {f} — заголовок «{m.group(1)}. {m.group(2)}» не называет операнд')
# Запрещённые слова болтовни — во всех типах
for f, *_ in items:
    for w in BANNED:
        if w in src[f]:
            warn(f'  ⚠ болтовня: {f} — «{w.strip("*")}»')
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
            warn(f'  ⚠ склейка: {f} — {len(parts)} мысли в строке: «{t[:70]}…»')
# Формула без левой части — строка из одних чисел и знаков с «=» вне кода (кроме систем: там проверка подстановкой)
if not typ.startswith(LINT_SKIP):
    for f, *_ in items:
        incode = False
        for ln in src[f].split('\n'):
            if ln.strip().startswith('```'): incode = not incode; continue
            if not incode and '=' in ln and re.fullmatch(r'[0-9][0-9 ·+−×:()=]*', ln.strip()):
                warn(f'  ⚠ формула без левой части: {f} — «{ln.strip()[:70]}»')
# «Артефакт» — внутренняя кухня
for f, *_ in items:
    for ln in re.sub(r'(?s)<!--.*?-->', '', src[f]).split('\n'):
        if re.search(r'артефакт', ln, re.I):
            warn(f'  ⚠ артефакт в тексте: {f} — «{ln.strip()[:70]}»')
# Тире перед числом читается как минус
for f, *_ in items:
    incode = False
    for ln in src[f].split('\n'):
        if ln.strip().startswith('```'): incode = not incode; continue
        if not incode and re.search(r' — [0-9]', ln):
            warn(f'  ⚠ тире-минус: {f} — «{ln.strip()[:70]}»')
# Ссылок «как в образце» в тексте нет (промпт сессии, п. 4)
for f, *_ in items:
    t = re.sub(r'(?s)<!--.*?-->', '', src[f])
    if re.search(r'образц|образе?ц', t, re.I):
        warn(f'  ⚠ ссылка на образец в тексте: {f}')


def pometki(t, what):
    return [re.sub(r'\s+', ' ', x).strip() for x in re.findall(r'<!--\s*' + what + r'\s*:?\s*(.*?)-->', t, re.S)]

print(f'{typ}: {len(items)} задач')
for row in items:
    f, istochnik, rash = row[0], row[1], row[4]
    novye = pometki(src[f], '🆕 приём вне реестра') + pometki(src[f], '🆕 приём(?! вне)')
    otst = pometki(src[f], 'отступление от образца')
    if not (novye or otst or rash): continue
    print(f'\n{istochnik} ({f})')
    for x in novye: print('  🆕', x)
    if rash: print('  расхождение агентов:', rash)
    for x in otst: print('  отступление:', x)
sys.exit(1 if WARN else 0)
