# Перебор T1-70-2: x утр. (24), y дн. (36), z веч. (40)
sols = []
for x in range(0, 91):
    for y in range(0, 91 - x):
        z = 90 - x - y
        if 24*x + 36*y + 40*z != 3048:
            continue
        if 24*x + 36*y + 36*z != 2928:  # вечерний со скидкой 10 %: 40*0.9 = 36
            continue
        sols.append((x, y, z))
print("решения (утр, дн, веч):", sols)
tot = set()
for x, y, z in sols:
    x3, z3 = 2*x, z/2
    y3 = 90 - x3 - z3
    print("неделя 3: утр", x3, "дн", y3, "веч", z3, "целые" if z3 == int(z3) and y3 >= 0 else "НЕ ЦЕЛЫЕ/отриц")
    tot.add(24*x3 + 36*y3 + 40*z3)
print("суммы за 3-ю неделю (без скидки):", tot)
