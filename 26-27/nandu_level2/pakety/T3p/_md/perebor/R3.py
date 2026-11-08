# R3 (ритуал, пример 3): шесть окон в ряд; жёлтых 3 или 4, голубых 1 или 2, красных 1 или 2; окно может быть тёмным (Т).
from itertools import product

def ok(r):
    return r.count('Ж') in (3, 4) and r.count('Г') in (1, 2) and r.count('К') in (1, 2)

vse = [''.join(r) for r in product('ЖГКТ', repeat=6)]
good = [r for r in vse if ok(r)]
print('перебрано рядов:', len(vse), ' подходят:', len(good))

# наблюдение: сверх 3 жёлтых, 1 голубого, 1 красного ровно одно окно
def sverh(r):
    return r.count('Т') + (r.count('Ж') - 3) + (r.count('Г') - 1) + (r.count('К') - 1)
assert all(sverh(r) == 1 for r in good), 'наблюдение ложно'
print('наблюдение верно для всех', len(good), 'подходящих: сверх наименьших ровно одно окно')

mir = {
    'N(тёмное окно)': [r for r in good if 'Т' in r],
    'N(два голубых)': [r for r in good if r.count('Г') == 2],
    'N(два красных)': [r for r in good if r.count('К') == 2],
    'N(четыре жёлтых)': [r for r in good if r.count('Ж') == 4],
}
for k, v in mir.items():
    print(k, '=', len(v))
# миры не пересекаются и покрывают всё
assert sum(len(v) for v in mir.values()) == len(good)
assert len(set().union(*map(set, mir.values()))) == len(good)
print('сумма операндов =', sum(len(v) for v in mir.values()), '= N =', len(good))

primery = ['ЖТЖГЖК', 'ГЖЖКЖГ', 'ЖКЖЖГК', 'ЖЖГЖЖК']
neprim = 'ЖГТЖКТ'
assert all(ok(r) for r in primery), 'пример не подходит'
assert not ok(neprim)
assert neprim.count('Ж') == 2 and neprim.count('Г') in (1, 2) and neprim.count('К') in (1, 2)
print('примеры подходят:', primery, '; неподходящий нарушает только «жёлтых 3 или 4»:', neprim)
# каждый мир представлен в примерах
print('миры примеров:', [[k for k, v in mir.items() if r in v] for r in primery])
