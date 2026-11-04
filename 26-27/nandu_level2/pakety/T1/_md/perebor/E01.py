sols = []
for p in range(0, 21):
    for s in range(0, 21):
        for w in range(0, 21):
            if p + s + w != 20: continue
            if 2 * (p / 2 + 3 * s + 8 * w) != 90: continue  # рыба 45 кг, без дробей
            if p + 2 * s != 22: continue
            sols.append((p, s, w))
print(len(sols), sols)
