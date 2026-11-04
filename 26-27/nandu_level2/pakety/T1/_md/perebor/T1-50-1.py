# Перебор: r - рубашка, b - брюки, s - свитер (целые положительные, $)
def cost(r, b, s, nr, nb, ns):
    sw = ns * s * (9 if ns >= 10 else 10)  # в десятых долях
    return 10 * (nr * r + nb * b) + sw      # стоимость * 10

sols = []
for r in range(1, 501):
    for b in range(1, 501):
        for s in range(1, 501):
            if (cost(r,b,s,4,4,5) == 5000 and cost(r,b,s,4,4,10) == 7400
                    and cost(r,b,s,4,0,2) == cost(r,b,s,0,6,0)):
                sols.append((r, b, s))
print("решений:", len(sols))
for x in sols: print("r,b,s =", x)
