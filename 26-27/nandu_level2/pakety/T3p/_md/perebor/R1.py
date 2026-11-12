# R1: две кружки на четырёх крючках. а) разные: 12; б) одинаковые: 6; группы списка 3,3,3,3 и 3,2,1.
from itertools import permutations, combinations
a = list(permutations(range(1, 5), 2)); b = list(combinations(range(1, 5), 2))
assert [sum(1 for p in a if p[0] == k) for k in range(1, 5)] == [3, 3, 3, 3]
assert [sum(1 for p in b if p[0] == k) for k in range(1, 4)] == [3, 2, 1]
print("а)", len(a), "б)", len(b)); assert (len(a), len(b)) == (12, 6)
