# R3: коврик из 4 плиток в ряду из 6.
pos = [set(range(l, l + 4)) for l in range(1, 7) if l + 3 <= 6]
assert len(pos) == 3 and set.intersection(*pos) == {3, 4}
print("N =", len(pos), "всегда закрыты", sorted(set.intersection(*pos)))
