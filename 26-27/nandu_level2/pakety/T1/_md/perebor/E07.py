# Пример раздела 6: кафе, три чека, спрошенный заказ 2 чая + 2 лимонада + вафля + кекс
sols = [(t, l, w, k) for t in range(1, 100) for l in range(1, 100) for w in range(1, 100) for k in range(1, 100)
        if 3*t + l + w == 210 and 3*t + l + k == 200 and t + 3*l + 3*k == 280]
print(len(sols), 'наборов цен; стоимость заказа:', {2*t + 2*l + w + k for t, l, w, k in sols})   # 79 наборов; {250}
