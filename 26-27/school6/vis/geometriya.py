#!/usr/bin/env python3
"""Иллюстрации учебника «Геометрия» (6 класс) → math6_1_geometriya_uchebnik.vis.json (пишется целиком).

План рисунков и мысль каждого движения: 26-27/school6/vis/plan_geometriya.md.
Рисунки: geometriya_a.py (главы 1–6), geometriya_b.py (главы 7–10), geometriya_c.py (главы 11–13); помощники и solid — geometriya_lib.py.
Геометрия строится из координат; числа на рисунках сверяются через need() с текстом MD.

Запуск: python3 26-27/school6/vis/geometriya.py
"""
import json, os, re

from geometriya_lib import FIGS, MD, VIS, norm, ascii_tokens, svg_text, fig
import geometriya_a  # noqa: F401  (регистрирует рисунки)
import geometriya_b  # noqa: F401
import geometriya_c  # noqa: F401

BLOCKS = [norm(b) for b in re.split(r'\n\s*\n', MD)]

if __name__ == '__main__':
    out = {}
    for anchor, (f, fx, zam) in FIGS.items():
        assert not re.search(r'[*`>#|\\]', anchor), anchor
        hits = [b for b in BLOCKS if anchor in b]
        assert hits, f'якорь «{anchor}» не найден'
        body, cap = f()
        if zam:
            miss = ascii_tokens(anchor) - set(re.findall(r'[A-Za-zА-Яа-яЁё0-9₀-₉]+', svg_text(body)))
            assert not miss, f'замена «{anchor}»: на SVG нет {miss}'
        out[anchor] = fig(body, cap, fx=fx, zamena=zam)
    json.dump(out, open(VIS, 'w'), ensure_ascii=False, indent=2)
    print(len(out), 'рисунков,', sum(1 for _, fx, _ in FIGS.values() if fx), 'анимаций →', os.path.relpath(VIS))
