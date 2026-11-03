# T1-30-1 — лодочная станция: перебор всех наборов лодок.
# b2, b4, b6 — сколько на станции 2-местных, 4-местных, 6-местных лодок.
# Условие: 38 лодок, 138 мест; если бы 2-местных было вдвое больше — 170 мест.

LODOK = 38
MEST = 138
MEST_ESLI_BY = 170

pervye_dva = []
vse_tri = []
for b2 in range(0, 171):
    for b4 in range(0, 171):
        for b6 in range(0, 171):
            if b2 + b4 + b6 != LODOK:
                continue
            if 2 * b2 + 4 * b4 + 6 * b6 != MEST:
                continue
            pervye_dva.append((b2, b4, b6))
            if 2 * (2 * b2) + 4 * b4 + 6 * b6 == MEST_ESLI_BY:
                vse_tri.append((b2, b4, b6))

print(f"наборов {LODOK} лодок на {MEST} мест: {len(pervye_dva)}")
print(f"из них подходят под «если бы» ({MEST_ESLI_BY} мест): {vse_tri}")
