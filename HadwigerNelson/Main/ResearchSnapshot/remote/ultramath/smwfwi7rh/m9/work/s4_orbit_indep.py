"""s4_orbit_indep.py -- independent count of the single-centre R-orbit words at k=6.

Completely different code path from sprint/k6/orbit_correct.py: no recursion, no
transfer matrix -- a vectorised brute force over all |A|^6 tuples with the constraint
set evaluated as boolean masks.

Constraints (as in sprint/k6/STRUCTURE.md Theorem 5, items 1-7):
  (SA)   i not in P_j                       [self-avoidance]
  (5.7)  P_j cap P_{j+1} = empty
  (TA)   |P_j| = 3 => |P_{j+1}| <= 2
  (SING) singleton label outside the cycle vertex set V
  (EDGE) P_j is not contained in a cycle edge
  (MON)  |P_j| + |P_{j+2}| = 5 and disjoint  -> forbidden
  (C1)   no two complementary triples
  (C2)   at most three ternary palettes
"""
import numpy as np
from itertools import combinations

K = 6

def enumer(ell, i):
    V = set(range(ell))
    pal = []
    for r in (1, 2, 3):
        for c in combinations([x for x in range(K) if x != i], r):
            m = 0
            for x in c: m |= 1 << x
            ok = all((m & ~((1 << j) | (1 << ((j + 1) % ell)))) != 0 for j in range(ell))
            if ok: pal.append(m)
    pal = np.array(pal, dtype=np.int64)
    n = len(pal)
    pc = np.array([bin(int(m)).count('1') for m in pal])
    # apply the position-independent filters first: EDGE (already), SING for size 1
    keep = np.array([not (pc[t] == 1 and int(pal[t]).bit_length() - 1 in V) for t in range(n)])
    ids = np.nonzero(keep)[0]
    pal, pc = pal[ids], pc[ids]
    n = len(pal)
    disj = np.zeros((n, n), dtype=bool)
    for a in range(n):
        disj[a] = (pal & pal[a]) == 0
    monbad = np.zeros((n, n), dtype=bool)     # MON: sizes sum 5 and disjoint
    for a in range(n):
        monbad[a] = disj[a] & (pc + pc[a] == 5)
    c1bad = np.zeros((n, n), dtype=bool)
    for a in range(n):
        c1bad[a] = disj[a] & (pc == 3) & (pc[a] == 3)
    ta = (pc == 3)                              # ternary positions
    # enumerate all tuples in chunks
    total = 0
    chunk = 1 << 20
    N = n ** 6
    idx = np.arange(chunk, dtype=np.int64)
    for start in range(0, N, chunk):
        t = start + idx[:min(chunk, N - start)]
        w = np.stack([(t // n ** p) % n for p in range(6)], axis=1)
        ok = np.ones(len(t), dtype=bool)
        for p in range(6):
            a, b = w[:, p], w[:, (p + 1) % 6]
            ok &= disj[a, b]
            ok &= ~(ta[a] & (pc[b] > 2))
            ok &= ~monbad[a, w[:, (p + 2) % 6]]
        for p in range(6):
            for q in range(p + 1, 6):
                ok &= ~c1bad[w[:, p], w[:, q]]
        ok &= (w[:, 0] + w[:, 1] + w[:, 2] + w[:, 3] + w[:, 4] + w[:, 5]) * 0 == 0  # no-op
        s = ta[w].sum(axis=1)
        ok &= s <= 3
        total += int(ok.sum())
    return n, total

if __name__ == "__main__":
    for ell, i, label in [(3,0,'ell=3 i in cycle'), (3,3,'ell=3 i outsider'),
                          (4,0,'ell=4 i in cycle'), (4,4,'ell=4 i outsider'),
                          (5,0,'ell=5 i in cycle'), (5,5,'ell=5 i outsider'),
                          (6,0,'ell=6 i in cycle')]:
        n, tot = enumer(ell, i)
        print(f"{label}: |A| = {n}, words = {tot}")
