# T1-30-2 — аквариум: перебор всех наборов неотрицательных целых
# N_гуп, N_неон, N_сом от 0 до 200 (всего рыбок 56, с большим запасом).
LIMIT = 200
found = []
for gup in range(LIMIT + 1):
    for neon in range(LIMIT + 1):
        for som in range(LIMIT + 1):
            if gup + neon + som != 56:          # всего 56 рыбок
                continue
            if gup != neon + som:               # гуппи столько же, сколько неонов и сомиков вместе
                continue
            if neon != 3 * som:                 # неонов втрое больше, чем сомиков
                continue
            found.append((gup, neon, som))
print("наборов (гуппи, неоны, сомики) от 0 до", LIMIT, "каждого вида:", (LIMIT + 1) ** 3)
print("подходят:", found)
