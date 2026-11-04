sols = []
for r in range(0, 37):
    for t in range(0, 37):
        for c in range(0, 37):
            if r + t + c != 36: continue
            if r + c != 25: continue
            if r % 2 != 0: continue  # половина роз - целое
            if t + c + r - r // 2 != 28: continue
            sols.append((r, t, c))
print(len(sols), sols)
