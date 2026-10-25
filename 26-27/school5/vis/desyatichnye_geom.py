#!/usr/bin/env python3
"""Иллюстрации учебника «Десятичные дроби и геометрия» (5 класс) → math5_desyatichnye_geom_uchebnik.vis.json.

План рисунков: 26-27/school5/vis/plan_desyatichnye_geom.md.
Часть A (десятичные) — desyatichnye_geom_a.py, часть B (геометрия) — desyatichnye_geom_b.py,
примитивы и сверка чисел с текстом MD — desyatichnye_geom_prim.py.
Файл .vis.json пишется целиком: ключ — якорь (подстрока абзаца MD), значение — <figure>.

Запуск: python3 26-27/school5/vis/desyatichnye_geom.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from desyatichnye_geom_prim import PLAIN, MD_PATH
import desyatichnye_geom_a as A
import desyatichnye_geom_b as B

VIS = MD_PATH[:-3] + '.vis.json'


def main():
    figs = {}
    for mod in (A, B):
        for anchor, f in mod.FIGS.items():
            assert anchor not in figs, f'якорь дважды: {anchor}'
            n = PLAIN.count(anchor)
            assert n == 1, f'якорь «{anchor}» встречается в тексте {n} раз(а)'
            figs[anchor] = f()
    # порядок ключей — порядок абзацев в тексте
    figs = dict(sorted(figs.items(), key=lambda kv: PLAIN.index(kv[0])))
    json.dump(figs, open(VIS, 'w'), ensure_ascii=False, indent=1)
    print(len(figs), 'рисунков,', sum('class="fx"' in v for v in figs.values()), 'анимаций →',
          os.path.relpath(VIS, os.path.join(HERE, '..', '..', '..')))


if __name__ == '__main__':
    main()
