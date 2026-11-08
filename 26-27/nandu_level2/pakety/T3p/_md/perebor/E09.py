# E09: одиннадцать флажков трёх цветов на верёвке; перебор всех расстановок прямо по условию.
# Ряд строится слева направо; ветка обрывается, как только нарушено условие «подряд» по цвету или по номеру:
# флажок, чей цвет (номер) уже встречался, обязан стоять сразу после флажка того же цвета (номера).
from collections import Counter

flags = [("з", 1), ("з", 2), ("з", 3), ("з", 5),
         ("к", 7), ("к", 8), ("к", 9),
         ("ж", 4), ("ж", 5), ("ж", 6), ("ж", 7)]

def ok_append(row, f):
    if not row:
        return True
    last = row[-1]
    for k in (0, 1):
        seen = any(g[k] == f[k] for g in row)
        if seen and last[k] != f[k]:
            return False
    return True

total = 0
worlds = Counter()
used = [False] * len(flags)
row = []
def go():
    global total
    if len(row) == len(flags):
        total += 1
        worlds[row[0][0]] += 1
        return
    for i, f in enumerate(flags):
        if not used[i] and ok_append(row, f):
            used[i] = True; row.append(f)
            go()
            row.pop(); used[i] = False
go()
print("N =", total)
print("по мирам (цвет слева):", dict(worlds))
