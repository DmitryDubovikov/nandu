#!/usr/bin/env python3
"""Пересборка года боевых решений из parts/: склейка MD и vis.json → md2html → --check → общий индекс.

Запуск из корня репо:
    python3 25-26/nandu_level1/national/boevye_resheniya/_md/sobrat_god.py 2020 [2021 ...]
Шапка года (таблица ответов, порядок на туре) берётся из текущего годового MD — всё до первого «## №».
Ненулевой код, если --check нашёл потерянный или дописанный текст.
"""
import glob, json, os, re, subprocess, sys

M = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(M)
ROOT = os.path.abspath(os.path.join(B, '..', '..', '..', '..'))
TOOL = os.path.join(ROOT, 'tools', 'md2html.py')
rc = 0
for y in sys.argv[1:]:
    md = os.path.join(M, f'nandu_n1_nacional_boevye_{y}_resheniya.md')
    vis = md[:-3] + '.vis.json'
    head = re.split(r'(?m)^## №', open(md).read(), maxsplit=1)[0]
    parts = sorted(glob.glob(os.path.join(M, 'parts', f'{y}_*.md')), key=lambda p: int(p.rsplit('_', 1)[1][:-3]))
    open(md, 'w').write(head + '\n'.join(open(p).read() for p in parts) + '\n')
    v = {}
    for p in parts:
        j = p[:-3] + '.vis.json'
        if os.path.exists(j):
            v.update(json.load(open(j)))
    json.dump(v, open(vis, 'w'), ensure_ascii=False, indent=1)
    out = os.path.join(B, y)
    for f in glob.glob(os.path.join(out, '[0-9][0-9]-*.html')):
        os.remove(f)
    r = subprocess.run([sys.executable, TOOL, md, out, vis], capture_output=True, text=True)
    print(y, 'сборка:', (r.stdout + r.stderr).strip().splitlines()[-3:])
    for line in (r.stdout + r.stderr).splitlines():
        if 'без якоря' in line or 'Traceback' in line:
            print('  ⚠', line)
    c = subprocess.run([sys.executable, TOOL, '--check', md, out], capture_output=True, text=True)
    tail = [l for l in c.stdout.splitlines() if 'потеряно' in l or 'дописано' in l]
    print(y, 'check rc =', c.returncode, tail)
    rc |= c.returncode | r.returncode
subprocess.run([sys.executable, os.path.join(M, 'obshchiy_index.py')])
sys.exit(rc)
