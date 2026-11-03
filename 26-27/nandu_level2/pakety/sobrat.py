#!/usr/bin/env python3
"""Сборка HTML пакета одного типа (этап Г): страница приёмов → круг 1 (30, 50) → круг 2 (70) → опознание.

Запуск из корня репо:
    python3 26-27/nandu_level2/pakety/sobrat.py T1
Исходники:
    pakety/<код>/<код>_stranica.md      — страница приёмов (её читает родитель)
    pakety/<код>/_md/<код>-30-<№>.md, -50-, -70-   — задачи с решениями
    pakety/<код>/_md/<код>-O.md         — условия на опознание
    pakety/<код>/_md/perebor/*.py       — переборы (в сборку не входят)
Выход — pakety/<код>/index.html (md2html, те же ⚠-проверки, что у idealnye_resheniya/_md/sobrat.py).
Ненулевой код, если --check нашёл потерянный или дописанный текст.
"""
import json, os, re, subprocess, sys

K = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(K, '..', '..', '..'))
TOOL = os.path.join(ROOT, 'tools', 'md2html.py')

kod = sys.argv[1] if len(sys.argv) > 1 else 'T1'
P = os.path.join(K, kod)
M = os.path.join(P, '_md')

def num(f):
    m = re.match(re.escape(kod) + r'-(\d+)-(\d+)\.md$', f)
    return (int(m.group(1)), int(m.group(2))) if m else None

zadachi = sorted((f for f in os.listdir(M) if num(f)), key=num)
krug1 = [f for f in zadachi if num(f)[0] in (30, 50)]
krug2 = [f for f in zadachi if num(f)[0] == 70]
opozn = os.path.join(M, f'{kod}-O.md')

src = {}
src['stranica'] = open(os.path.join(P, f'{kod}_stranica.md')).read()
for f in zadachi:
    src[f] = open(os.path.join(M, f)).read()
if os.path.exists(opozn):
    src['O'] = open(opozn).read()

def demote(t):
    """Заголовки страницы приёмов на уровень ниже: # → ##, ## → ###."""
    return re.sub(r'(?m)^(#{1,5}) ', lambda m: '#' + m.group(1) + ' ', t)

parts = [f'# Пакет {kod}', '',
         'Olimpíada Ñandú · Segundo Nivel · этап Г · статус — `26-27/nandu_level2/nandu_n2_roadmap.md`', '',
         f'Страница приёмов · круг 1: {len(krug1)} задач (30 и 50 %) · круг 2: {len(krug2)} (70 %) · '
         f'опознание: {len(re.findall(r"(?m)^## ", src.get("O", "")))} условий', '',
         demote(src['stranica']).rstrip()]
# Пустой раздел «## Круг 1» md2html выбрасывает (страница = раздел ##), поэтому круг виден по номеру задачи
# (<код>-30-…, -50-, -70-) и по оглавлению в шапке.
parts[4:4] = ['| круг | задачи |', '|---|---|',
              '| 1 (30 и 50 %) | ' + ', '.join(f[:-3] for f in krug1) + ' |',
              '| 2 (70 %) | ' + ', '.join(f[:-3] for f in krug2) + ' |', '']
parts += [src[f].rstrip() for f in krug1 + krug2]
if 'O' in src:
    parts += [src['O'].rstrip()]
body = '\n\n'.join(parts)
body = re.sub(r'(?s)\n?<!--.*?-->', '', body)
md = os.path.join(M, f'nandu_n2_paket_{kod}.md')
open(md, 'w').write(body + '\n')

vis = {}
for f in zadachi:
    j = os.path.join(M, f[:-3] + '.vis.json')
    if os.path.exists(j):
        vis.update(json.load(open(j)))
vp = md[:-3] + '.vis.json'
json.dump(vis, open(vp, 'w'), ensure_ascii=False, indent=1)

# ——— ⚠-проверки: те же, что в idealnye_resheniya/_md/sobrat.py и resheniya_korpusa/sobrat.py ———
BANNED = ('Жанр ответа', 'Заметь главное', '**Обозначения', 'С чего начать', 'План готов')
for k, t in src.items():
    for w in BANNED:
        if w in t:
            print(f'  ⚠ болтовня: {k} — «{w.strip("*")}»')
SENT = re.compile(r'(?<=[.!?])\s+(?=[«*(]?[А-ЯЁA-Z])')
for k, t in src.items():
    t_ = re.sub(r'(?s)<!--.*?-->', '', t)
    incode = False
    for ln in t_.split('\n'):
        s = ln.strip()
        if s.startswith('```'): incode = not incode; continue
        if incode or not s or s.startswith(('- ', '|', '<small>', '**Ответ на задачу', '*Проверено', ':::', '#')): continue
        s = s.lstrip('> ').strip()
        if s.startswith('**Условие') or '?' in s or re.match(r'^\*\*\d+\.', s): continue
        s = re.sub(r'^\*\*[^*]+\*\*\s*', '', s)
        if len([x for x in SENT.split(s) if x.strip()]) > 1:
            print(f'  ⚠ склейка: {k} — «{s[:70]}…»')
for k, t in src.items():
    for ln in re.sub(r'(?s)<!--.*?-->', '', t).split('\n'):
        if re.search(r'артефакт', ln, re.I):
            print(f'  ⚠ артефакт в тексте: {k} — «{ln.strip()[:70]}»')
for k, t in src.items():
    incode = False
    for ln in t.split('\n'):
        if ln.strip().startswith('```'): incode = not incode; continue
        if not incode and re.search(r' — [0-9]', ln):
            print(f'  ⚠ тире-минус: {k} — «{ln.strip()[:70]}»')
for k, t in src.items():
    if re.search(r'образц|образе?ц', re.sub(r'(?s)<!--.*?-->', '', t), re.I):
        print(f'  ⚠ ссылка на образец в тексте: {k}')
# Сюжеты пакета не повторяются (промпт, п. 9): заголовок «## <номер> — <сюжет>»
sujety = {}
for k, t in src.items():
    for m in re.finditer(r'(?m)^## (\S+) — (.+)$', t):
        sujety.setdefault(m.group(2).strip().lower(), []).append(m.group(1))
for s, n in sujety.items():
    if len(n) > 1:
        print(f'  ⚠ один сюжет дважды: «{s}» — {", ".join(n)}')

r = subprocess.run([sys.executable, TOOL, md, P, vp], capture_output=True, text=True)
for line in (r.stdout + r.stderr).splitlines():
    if 'без якоря' in line or 'Traceback' in line:
        print('  ⚠', line)
print('сборка:', (r.stdout + r.stderr).strip().splitlines()[-3:])
c = subprocess.run([sys.executable, TOOL, '--check', md, P], capture_output=True, text=True)
print('check rc =', c.returncode, [l for l in c.stdout.splitlines() if 'потеряно' in l or 'дописано' in l])
sys.exit(c.returncode | r.returncode)
