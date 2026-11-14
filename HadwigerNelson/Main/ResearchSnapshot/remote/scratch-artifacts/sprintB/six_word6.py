"""6-periodic free-label word for the six-cycle transport at m=9 (shift 3 mod 6):
need W_i disjoint from W_{i+2}, W_{i+3}, W_{i+4} (indices mod 6), all W_i admissible
for C6, size 2..3, avoiding label 0."""
from itertools import combinations, product
K=6
E=[frozenset((j,(j+1)%6)) for j in range(6)]
vals=[]
for r in (2,3):
    for c in combinations(range(1,K),r):
        S=frozenset(c)
        if not any(S<=e for e in E): vals.append(S)
def ok(a,b): return not (a&b)
sols=[]
for w in product(vals,repeat=6):
    if all(ok(w[i],w[(i+d)%6]) for i in range(6) for d in (2,3,4)):
        sols.append(w)
print("6-periodic free-label words:",len(sols))
for w in sols[:8]: print("   ",[sorted(x) for x in w])
# Also try period 12 for general m (m could be != 3 mod 6); check which periods work.
