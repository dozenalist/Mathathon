"""
Exact combinatorial verification for the k=6 palette orbit constraints (m6, d8).

O_k = { (P_0,...,P_5) : P_j nonempty subset of [k], |P_j| <= k-3,
                         P_j cap P_{j+1} = empty (indices mod 6) }.

These are the pointwise consequences of
  (P)   1 <= |P_x(e)| <= k-3                (palette bound; R5, Prop 5.6 generalised)
  (5.7) P_x(f) cap P_x(f+pi/3) = empty a.e. (`palette_sixty_disjoint`, Lean)
on one R-orbit at a centre x.  All counts are exact integers:
|O_k| = trace(A_k^6), A_k the disjointness adjacency matrix of the admissible label sets.
"""
from itertools import combinations, product
from fractions import Fraction
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

def subsets(k, lo, hi):
    return [frozenset(S) for r in range(lo, hi+1) for S in combinations(range(k), r)]

def matmul(A, B):
    p = len(B)
    return [[sum(A[i][t]*B[t][j] for t in range(p)) for j in range(len(B[0]))] for i in range(len(A))]

def matpow(A, e):
    n = len(A)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    while e:
        if e & 1: R = matmul(R, A)
        A = matmul(A, A); e >>= 1
    return R

def orbit_count(k, lo, hi):
    S = subsets(k, lo, hi)
    n = len(S)
    A = [[1 if not (S[i] & S[j]) else 0 for j in range(n)] for i in range(n)]
    M = matpow(A, 6)
    return S, sum(M[i][i] for i in range(n))

def enumerate_all_top(k):
    """all 6-tuples of (k-3)-sets with consecutive disjointness, by DFS"""
    S = subsets(k, k-3, k-3)
    out = []
    def dfs(seq):
        if len(seq) == 6:
            if not (seq[5] & seq[0]): out.append(tuple(seq))
            return
        for T in S:
            if not (seq[-1] & T): dfs(seq+[T])
    for s in S: dfs([s])
    return out

report = {}
print("k  |O_k|        all-six-top-size  max_top (independent of Thm 1)")
for k in range(3, 9):
    if k >= 4:
        _, tot = orbit_count(k, 1, k-3)
        _, alltop = orbit_count(k, k-3, k-3)
        t = k-3
        mx = max(sum(1 for s in sizes if s == t)
                 for sizes in product(range(1, t+1), repeat=6)
                 if all(sizes[j] + sizes[(j+1) % 6] <= k for j in range(6)))
    else:
        tot = alltop = mx = 0
    report[k] = {"O_k": tot, "all_top_size": alltop, "max_top_size_count": mx, "top_size": k-3}
    print(k, tot, alltop, mx)

# k = 6: the 20 all-ternary orbits are exactly the alternating complementary patterns
k = 6
top = enumerate_all_top(6)
ok = len(top) == 20
for seq in top:
    A = seq[0]
    ok &= all(seq[j] == (A if j % 2 == 0 else frozenset(set(range(6))-A)) for j in range(6))
print("\nk=6: number of all-ternary orbits =", len(top),
      "; each is the alternating pattern A,A^c,A,A^c,A,A^c :", ok)
print("     each such orbit contains a complementary pair, so Theorem 1 excludes all of them")

# k = 6 sharpness model: palettes constant on the six angular cells [j pi/3,(j+1) pi/3)
A0, A2, A4 = frozenset({1,2,3}), frozenset({1,2,4}), frozenset({1,3,4})
P = {0:A0, 1:frozenset({5,6}), 2:A2, 3:frozenset({5,6}), 4:A4, 5:frozenset({5,6})}
E = [0,2,4]
assert all(P[j] and len(P[j]) <= 3 for j in range(6)), "(P)"
assert all(not (P[j] & P[(j+1) % 6]) for j in range(6)), "(5.7)"
assert all(P[i] | P[j] != frozenset(range(6)) for i in range(6) for j in range(6)), "Thm 1"
print("\nk=6 sharpness model (palettes constant on angular cells):")
for j in range(6): print("   cell", j, "palette", sorted(P[j]))
print("   ternary cells:", E, " sigma(E)/2pi =", Fraction(len(E), 6),
      " mean |P| =", Fraction(sum(len(P[j]) for j in range(6)), 6))
print("   (P):", True, " (5.7) on all six consecutive pairs:", True,
      " no complementary pair (Thm 1):", True)

# k = 5: Theorem 1 is vacuous (two 2-sets cannot cover Fin 5); the orbit system is (5.7) alone.
print("\nk=5: |P|<=2 and 2+2<5, so the pair-exclusion adds nothing; constraints reduce to (5.7)")
json.dump(report, open(os.path.join(HERE, "orbit_report.json"), "w"), indent=1)
