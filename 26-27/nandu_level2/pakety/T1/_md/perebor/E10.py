sols = []
for a in range(0, 60):
    for b in range(0, 60):
        for c in range(0, 60):
            if a + b + c == 19 and 20*a + 30*b + 50*c == 590 and 20*(2*a) + 30*b + 50*c == 710:
                sols.append((a, b, c))
print(len(sols), "решений (малых, средних, больших):", sols)
