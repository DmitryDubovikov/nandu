# s, l, c: цена метра шёлка, льна, хлопка (целые положительные)
sols = []
for s in range(1, 301):
    for l in range(1, 301):
        for c in range(1, 301):
            if (12*s + 18*l + 30*c == 1032
                    and 12*s + 30*l + 18*c == 1128
                    and 15*s + 15*l + 30*c == 1095):
                sols.append((s, l, c))
print(len(sols), sols)
