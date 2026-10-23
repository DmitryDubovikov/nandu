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
    '1': ('Фаза 1 — Зональ', [
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
}

faza = sys.argv[1] if len(sys.argv) > 1 else '1'
title, items = FAZY[faza]
head = [f'# {title} — идеальные решения образцов', '',
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
r = subprocess.run([sys.executable, TOOL, md, out, vp], capture_output=True, text=True)
for line in (r.stdout + r.stderr).splitlines():
    if 'без якоря' in line or 'Traceback' in line:
        print('  ⚠', line)
print('сборка:', (r.stdout + r.stderr).strip().splitlines()[-3:])
c = subprocess.run([sys.executable, TOOL, '--check', md, out], capture_output=True, text=True)
print('check rc =', c.returncode, [l for l in c.stdout.splitlines() if 'потеряно' in l or 'дописано' in l])
sys.exit(c.returncode | r.returncode)
