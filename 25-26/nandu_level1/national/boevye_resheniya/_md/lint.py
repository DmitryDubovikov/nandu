#!/usr/bin/env python3
"""Линтер механических дефектов боевых решений (parts/*.md).

Запуск из корня репо:
    python3 25-26/nandu_level1/national/boevye_resheniya/_md/lint.py [год ...]
Коды:
  GLUE  — две непустые строки подряд без пустой между ними: markdown склеит их в один абзац
  DOT   — «·» не между множителями (разделитель, читается как умножение)
  INLINE— формула с буквами внутри абзаца текста (правило 10)
  NEED  — заголовок «Шаг N — нуж…» (правило 14)
"""
import glob, os, re, sys

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts')
years = sys.argv[1:]
BLOCK = re.compile(r'^\s*(\||>|[-*+] |\d+\. |#|```|<)')
OPND = r'[\w)²³′″]'

def lint(path):
    out = []
    lines = open(path).read().split('\n')
    fence = False
    for i, s in enumerate(lines, 1):
        if s.strip().startswith('```'):
            fence = not fence
        if fence:
            continue
        t = s.strip()
        prev = lines[i - 2].strip() if i > 1 else ''
        if t and prev and not BLOCK.match(s) and not BLOCK.match(lines[i - 2]) and not prev.endswith('  '):
            out.append((i, 'GLUE', prev[-40:] + ' ⏎ ' + t[:40]))
        for m in re.finditer(r'·', s):
            a, b = s[max(0, m.start() - 2):m.start()], s[m.end():m.end() + 2]
            if not (re.search(OPND + r'\s?$', a) and re.match(r'\s?[\w(]', b)):
                out.append((i, 'DOT', t[max(0, m.start() - 30):m.start() + 30]))
        if re.search(r'Шаг \d+ — нуж', s):
            out.append((i, 'NEED', t[:80]))
        if t and not BLOCK.match(s) and len(t) > 70 and not t.startswith('**Шаг'):
            for m in re.finditer(r'[A-Za-zА-Яа-я0-9)]+ ?[+−×·=] ?[A-Za-z0-9(]+(?: ?[+−×·=] ?[A-Za-z0-9()]+)+', t):
                if re.search(r'[a-zA-Z]', m.group()) and not re.fullmatch(r'[A-Za-zА-Я]+ ?= ?\d+', m.group()):
                    out.append((i, 'INLINE', m.group()[:60]))
                    break
    return out

tot = {}
for p in sorted(glob.glob(os.path.join(D, '*.md'))):
    name = os.path.basename(p)[:-3]
    if years and name.split('_')[0] not in years:
        continue
    for i, code, txt in lint(p):
        tot[code] = tot.get(code, 0) + 1
        print(f'{name}:{i}\t{code}\t{txt}')
print('ИТОГО', tot, file=sys.stderr)
