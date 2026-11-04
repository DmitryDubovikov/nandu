# Цены за кг (a яблоки, b груши, c сливы), в центах (x2 для половинок) — целые доллары перебираем, половинки проверяем в полудолларах
sols = []
for a in range(1, 1001):
    for b in range(1, 1001):
        for c in range(1, 1001):
            # работаем в удвоенных ценах: полкило = цена, кило = 2*цена
            if a + b + c != 255 * 2:
                continue
            if a + b + 2 * c != 360 * 2:
                continue
            if a + 2 * b != 2 * a + c:
                continue
            sols.append((a, b, c))
print("решений:", len(sols), sols)
