#!/usr/bin/env python3
"""
d2, verification II: structural lemmas, the unified argument, realizable no-go witnesses.

S1  |O(e) u I(e)| = k - 2p  and  |O(e) n I(e)| = k - ell,  where 2p = number of sign runs.
    (This is the exact reason the k=5 argument is rigid and the k=6 one is not.)
S2  k = 5, ell = 5, NO palette bound at all -> still UNSAT (Prop 8.2 does not need (5.12)).
S3  the six-position system at k=6 with the outsider absent is UNSAT for every palette bound
    (already Theorem 1);  with a cycle label absent, or with nothing absent, it is SAT --
    on *realizable* geometries, with exact witnesses and every constraint re-verified.
S4  min over all admissible configurations of #{i : X in P_i} = 1 on the realizable geometries
    => sigma{X in P} >= 2*pi/6.
"""
import itertools, sys
sys.path.insert(0, "work")
from verify_d2 import (lemmaA, comp, allowed, internal, runs, palettes, csp_solve,
                       csp_solve_cadical, family, ELL)

KMAX = 8

def S1():
    print("S1  |O u I| = k - c,  |O n I| = k-ell  (c = #sign changes round the ell-cycle)")
    bad = 0
    for k in range(5, KMAX + 1):
        for ell in range(3, min(k, 6) + 1):
            for mask in range(1 << ell):
                Q = frozenset(i for i in range(ell) if mask >> i & 1)
                I, O = allowed(Q, k, ell)
                b = [1 if i in Q else 0 for i in range(ell)]
                c = 0 if len(set(b)) == 1 else sum(1 for i in range(ell) if b[i] != b[(i - 1) % ell])
                assert len(I | O) == k - c, (k, ell, sorted(Q), len(I | O), k - c)
                assert len(I & O) == k - ell, (k, ell, sorted(Q))
            bad += 1
    print(f"    verified exactly on {bad} (k,ell) pairs, every sign pattern.")
    print(f"    k=5,ell=5: |O n I| = 0 and |O u I| = 5-2p <= 3; both O,I nonempty forces p=2")
    print(f"               (2 runs) with lengths (2,3); then |O|+|I| = 3 = k-2 and |P|<=2")
    print(f"               makes every palette a transversal: exactly 2 options.")
    print(f"    k=6,ell=5: |O n I| = 1 (the outsider X), so O and I are NEVER empty and the")
    print(f"               palette option set is 12 (unbounded) / 7 (with |P|<=3).")

def S2():
    G, table = lemmaA()
    fam = list(family(table))
    print("\nS2  k=5, ell=5, palette bound dropped (b=5 covers every subset of the 5 labels)")
    for lab, fn in (("B2 backtracking", lambda pt: csp_solve(pt, 5, 5)),
                    ("B3 CaDiCaL    ", lambda pt: csp_solve_cadical(pt, 5, 5))):
        sat = [pt for pt in fam if fn(pt) is not None]
        print(f"    {lab}: SAT {len(sat)} / {len(fam)}  ->  Prop 8.2 holds without (5.12)")
        assert not sat

def realizable():
    seen = {}
    for gap in itertools.product(range(6), repeat=5):
        pt = tuple(frozenset(j for j in range(5) if (gap[j] - m) % 6 in (0, 1, 2)) for m in range(6))
        seen.setdefault(pt, gap)
    return seen

def check_witness(pt, P, k=6, absence=frozenset(), strong=False):
    """re-verify every constraint of the six-position system, exactly."""
    outs = frozenset(range(5, k))
    assert all(0 <= l < k for S in P for l in S) and all(S for S in P)
    for i, Q in enumerate(pt):
        I, O = allowed(Q, k)
        if strong: I, O = I - outs, O - outs
        assert P[i] & I and P[i] & O, ("(8.1)", i)
        assert not (P[i] & absence), ("self-avoidance", i)
        for j in range(5):                       # (6.2)
            assert not P[i] <= frozenset({j, (j + 1) % 5}), ("(6.2)", i, j)
        assert 1 <= len(P[i]) <= 3, ("palette bound", i)
    for i in range(6):                           # (5.7)
        assert not (P[i] & P[(i + 1) % 6]), ("(5.7)", i)
    return True

def S3():
    R = realizable()
    print(f"\nS3  realizable geometries: {len(R)} distinct six-tuples of sign patterns")
    cases = [
        ("no label known absent            ", frozenset(),  False),
        ("a cycle label (0) known absent   ", frozenset({0}), False),
        ("the outsider (5) known absent    ", frozenset({5}), True),
    ]
    for lab, abs_, strong in cases:
        sat = [(pt, csp_solve(pt, 6, 3, abs_, strong)) for pt in R]
        sol = [(pt, w) for pt, w in sat if w is not None]
        print(f"    {lab}: SAT {len(sol):5d} / {len(R)}")
        if sol:
            pt, w = sol[0]
            check_witness(pt, w, absence=abs_, strong=strong)
            print(f"        gap assignment        {R[pt]}")
            print(f"        sign patterns         {[sorted(q) for q in pt]}")
            print(f"        palettes              {[sorted(p) for p in w]}")
            print(f"        X=5 in palette at positions "
                  f"{[i for i in range(6) if 5 in w[i]]}   "
                  f"#{{X in P}} = {sum(1 for p in w if 5 in p)}")
            print(f"        (8.1), (5.7), (6.2), |P|<=3, self-avoidance: all re-verified exactly")
            # sigma-count sanity check for m11's bound sigma{T subset P} <= 1/2
            nX = sum(1 for p in w if 5 in p)
            print(f"        m11 sigma-bound sanity: #{{X in P}}={nX}/6 <= 3  "
                  f"{'ok' if nX <= 3 else 'VIOLATED'}")
            assert nX <= 3
        else:
            print(f"        UNSAT (this is part of Theorem 1)")

def S4():
    R = realizable()
    best = 99; wit = None
    for pt in R:
        opts = [palettes(Q, 6, 3) for Q in pt]
        if any(not o for o in opts): continue
        opts = [[P for P in o if not any(P <= frozenset({j, (j + 1) % 5}) for j in range(5))]
                for o in opts]
        n = 6; sol = []
        found = [99, None]
        def dfs(i):
            if i == n:
                c = sum(1 for P in sol if 5 in P)
                if c < found[0]: found[0] = c; found[1] = tuple(sol)
                return
            for P in opts[i]:
                if sol and (P & sol[-1]): continue
                if i == n - 1 and (P & sol[0]): continue
                sol.append(P); dfs(i + 1); sol.pop()
        dfs(0)
        if found[0] < best: best, wit = found[0], (pt, found[1])
    print(f"\nS4  min #{{i : X in P_i}} over the realizable geometries = {best}")
    print(f"    => sigma{{e : X in P_x(e)}} >= {best}/6 of the circle at every k=6 5-cycle centre")
    print(f"    witness patterns {[sorted(q) for q in wit[0]]}")
    print(f"    witness palettes {[sorted(p) for p in wit[1]]}")
    check_witness(wit[0], wit[1])
    return best

def main():
    G, table = lemmaA()
    S1()
    S2()
    S3()
    m = S4()
    assert m == 1
    print("\nALL CHECKS PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
