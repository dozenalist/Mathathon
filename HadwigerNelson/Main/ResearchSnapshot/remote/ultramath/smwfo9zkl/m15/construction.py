"""A uniform palette system at k = 6 whose cycle loci accumulate, for every
cycle length ell in {3,4,5,6}.

THE OBJECT
----------
Labels I = {0,...,5}.  A simple cycle C_ell on the labels 0,1,...,ell-1 in
cyclic order (edges {i,i+1} mod ell); the remaining labels are unused by the
cycle.

For each ell we fix three pairwise disjoint admissible palettes A_0,A_1,A_2:

    ell = 6 :  A_0={0,3}  A_1={1,4}  A_2={2,5}
    ell = 5 :  A_0={0,2}  A_1={1,3}  A_2={5}
    ell = 4 :  A_0={0,2}  A_1={4}    A_2={5}
    ell = 3 :  A_0={3}    A_1={4}    A_2={5}

"Admissible" means 1 <= |A| <= k-3 = 3 and A is contained in no cycle edge.
For m >= 6 with 3 | m put n = 6m, Delta = 2*pi/n, L = 2m/3 and

    sigma(i) = A_{ floor(i/L) mod 3 }         (i in Z/n),
    P_z(theta) = sigma( floor(theta/Delta) )  for every z in the plane.

All palettes are nonempty, of size <= 3, and none lies in a cycle edge.  The
family is translation invariant.

THE CENTRES
-----------
d0 = Delta/3 = pi/(9m).  Any infinite set of centres in a disc of radius d0
works; take y_k = (d0/3) 2^-k (3/5, 4/5).  For every pair z != z' of centres
and almost every f,

    P_z(f) cap P_{z'}(s_pm(f)) = empty,

s_pm being the two exact unit decompositions (z'-z) + f = s + t, |s|=|t|=1
(Lemma G, proved in verify.py).  Each y_k is a C_ell-centre in the sense that
P_{y_k} avoids all ell cycle edges, which is conclusion (6.2) of the paper's
Lemma 6.2 from "the edge belongs to Gamma_{y_k}".

WHY IT WORKS (the block lemma)
------------------------------
floor((i+t)/L) - floor(i/L) lies in {1,2} for every i in Z/n and every
t in {+-(m-1), +-m, +-(m+1)} (mod n), because (m+2)/2 <= L <= m-2, and that
double inequality holds exactly when m >= 6.  So the two block indices differ
by 1 or 2, hence modulo 3 the two palettes are two different members of a
pairwise disjoint triple.
"""
import itertools
import sys

K = 6
A = {6: [{0, 3}, {1, 4}, {2, 5}],
     5: [{0, 2}, {1, 3}, {5}],
     4: [{0, 2}, {4}, {5}],
     3: [{3}, {4}, {5}]}


def cycle_edges(ell):
    return [frozenset((i, (i + 1) % ell)) for i in range(ell)]


def admissible(k, ell):
    """(P0)+(P1): 1 <= |S| <= k-3 and S inside no cycle edge."""
    edges = cycle_edges(ell)
    return [frozenset(c) for r in range(1, k - 2)
            for c in itertools.combinations(range(k), r)
            if not any(frozenset(c) <= e for e in edges)]


def allowed_values(k=6, cycle_len=6):
    """Alias kept for the SAT scripts: the admissible palettes as frozensets."""
    return admissible(k, cycle_len)


def max_clique_size(values):
    """Exact maximum clique of the disjointness graph (branch and bound)."""
    vs = list(values)
    best = [0]

    def rec(cands, cur):
        if not cands:
            best[0] = max(best[0], cur)
            return
        if cur + len(cands) <= best[0]:
            return
        for k in range(len(cands)):
            if cur + len(cands) - k <= best[0]:
                return
            v = cands[k]
            rec([w for w in cands[k + 1:] if not (w & v)], cur + 1)

    rec(vs, 0)
    return best[0]


def system(ell, m):
    assert m >= 6 and m % 3 == 0
    n, L = 6 * m, 2 * m // 3
    assert 3 * L == 2 * m and n % (3 * L) == 0
    sig = [A[ell][(i // L) % 3] for i in range(n)]
    return n, L, sig


def offsets(m, n):
    D = set()
    for base in (m - 1, m, m + 1):
        D.add(base % n)
        D.add((-base) % n)
    D.discard(0)
    return sorted(D)


def check(ell, m, verbose=True):
    n, L, sig = system(ell, m)
    D = offsets(m, n)
    errs = []
    for i in range(n):
        s = sig[i]
        if not (1 <= len(s) <= K - 3):
            errs.append(("P0", i, s))
        for e in cycle_edges(ell):
            if s <= e:
                errs.append(("P1", i, tuple(sorted(s)), tuple(sorted(e))))
        for t in D:
            if s & sig[(i + t) % n]:
                errs.append(("P2/P4", i, t))
    used = set(map(frozenset, sig))
    for u in used:
        if len(u) == 3 and frozenset(set(range(K)) - set(u)) in used:
            errs.append(("P3", tuple(sorted(u))))
    blocks = [(i // L) % 3 for i in range(n)]
    for i in range(n):
        for t in D:
            if (blocks[(i + t) % n] - blocks[i]) % 3 not in (1, 2):
                errs.append(("block", i, t))
    if verbose:
        print("ell=%d m=%2d n=%3d L=%2d  values=%s  |D|=%d  violations=%d"
              % (ell, m, n, L,
                 sorted({tuple(sorted(s)) for s in used}), len(D), len(errs)))
    return errs


def block_inequality():
    """The block lemma needs m/2 < L <= m-1 (see WRITEUP.md 3.2); with
    L = 2m/3 that is exactly m >= 3.  Theorem 1 assumes m >= 6 only because
    Lemma G's stated constants 1.6 / 0.66 / 1.69 need d0 = pi/(9m) <= pi/54."""
    ok = [m for m in range(1, 400) if m / 2 < 2 * m / 3 <= m - 1]
    print("block conditions m/2 < 2m/3 <= m-1 hold exactly for m >= 3:",
          ok == list(range(3, 400)))
    assert ok == list(range(3, 400))
    return True


if __name__ == "__main__":
    print("=== the uniform construction, exact integer checks ===")
    tot = 0
    for ell in (3, 4, 5, 6):
        for m in (6, 9, 12, 15, 21, 30, 60, 201, 600):
            tot += len(check(ell, m))
    print()
    block_inequality()
    print()
    print("=== admissibility of the three palettes, and their disjointness ===")
    for ell in (3, 4, 5, 6):
        adm = admissible(K, ell)
        for v in A[ell]:
            assert frozenset(v) in adm, (ell, v)
        assert all(not (a & b) for a, b in itertools.combinations(A[ell], 2))
        print("  ell=%d  A=%s  admissible=yes  pairwise disjoint=yes  "
              "max clique of the %d-value disjointness graph = %d"
              % (ell, [sorted(v) for v in A[ell]], len(adm),
                 max_clique_size(adm)))
    print()
    print("TOTAL VIOLATIONS:", tot)
    sys.exit(0 if tot == 0 else 1)
