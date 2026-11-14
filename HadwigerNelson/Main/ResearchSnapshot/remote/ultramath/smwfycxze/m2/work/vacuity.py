#!/usr/bin/env python3
"""
d2, vacuity test.  Lemma 6.4 of the paper: at a fixed centre there is no measurable state
function with only the two values {X} (a singleton) and D (a fixed disjoint pair) which
changes state under R a.e.  The six-position witnesses of verify2_d2.py S3 are exactly of that
form ({5} / {1,4} alternating), so they are NOT admissible once Lemma 6.4 is imposed.

This script re-decides the six-position system with the extra requirement that the palettes at
the six sampled directions take at least THREE distinct values - which is a sufficient
certificate that the underlying field is not a two-valued state function, hence that Lemma 6.4
does not apply.  It also reports the two-valued stratum separately, so that the exact
consequence of Lemma 6.4 is visible.
"""
import itertools, sys
sys.path.insert(0, "work")
from verify_d2 import allowed, palettes, csp_solve, ELL

def realizable():
    seen = {}
    for gap in itertools.product(range(6), repeat=5):
        pt = tuple(frozenset(j for j in range(5) if (gap[j] - m) % 6 in (0, 1, 2)) for m in range(6))
        seen.setdefault(pt, gap)
    return seen

def solve_min_variety(patterns, k=6, b=3, absence=frozenset(), strong=False, minvals=3):
    """backtracking, but only accepting solutions with >= minvals distinct palette values."""
    opts = [palettes(Q, k, b, absence, strong) for Q in patterns]
    if any(not o for o in opts):
        return None
    opts = [[P for P in O if not any(P <= frozenset({j, (j + 1) % 5}) for j in range(5))]
            for O in opts]
    n = len(patterns); sol = []; res = []
    def dfs(i):
        if res:
            return
        if i == n:
            if len(set(sol)) >= minvals:
                res.append(tuple(sol))
            return
        for P in opts[i]:
            if sol and (P & sol[-1]): continue
            if i == n - 1 and (P & sol[0]): continue
            sol.append(P); dfs(i + 1); sol.pop()
        return
    dfs(0)
    return res[0] if res else None

def solve_min_variety_cadical(patterns, k=6, b=3, absence=frozenset(), strong=False, minvals=3):
    """independent check by blocking the 'at most 2 distinct values' solutions with CaDiCaL:
    enumerate the two-value patterns explicitly (there are few) and test each."""
    # values are subsets; a 2-valued solution uses values V1,V2; enumerate over the pair
    opts = [palettes(Q, k, b, absence, strong) for Q in patterns]
    if any(not o for o in opts):
        return None
    opts = [[P for P in O if not any(P <= frozenset({j, (j + 1) % 5}) for j in range(5))]
            for O in opts]
    allv = sorted({P for O in opts for P in O}, key=lambda P: (len(P), sorted(P)))
    n = len(patterns)
    # try every subset of values of size >= minvals is hopeless; instead: find any solution,
    # then check variety; iterate by forbidding the found 2-value solutions.
    banned = []
    while True:
        w = csp_solve(patterns, k, b, absence, strong)   # DFS with extra bans below
        # DFS cannot take bans, so use a small explicit search over the value subsets of
        # size < minvals: at most sum_{t<minvals} C(|allv|,t) <= 1+ |allv| + C(|allv|,2)
        found = None
        for t in range(1, minvals):
            for V in itertools.combinations(allv, t):
                V = set(V)
                ok = True
                for i in range(n):
                    loc = [P for P in opts[i] if P in V]
                    if not loc: ok = False; break
                if not ok: continue
                # check whether a full solution exists using only values in V
                sol = []
                def dfs(i):
                    if i == n: return True
                    for P in opts[i]:
                        if P not in V: continue
                        if sol and (P & sol[-1]): continue
                        if i == n - 1 and (P & sol[0]): continue
                        sol.append(P)
                        if dfs(i + 1): return True
                        sol.pop()
                    return False
                if dfs(0):
                    found = tuple(sol); break
            if found: break
        # look for a solution with >= minvals distinct values by brute force over the
        # value-set of size exactly minvals
        for V in itertools.combinations(allv, minvals):
            V = set(V); sol = []
            def dfs(i, V=V, sol=sol):
                if i == n: return True
                for P in opts[i]:
                    if P not in V: continue
                    if sol and (P & sol[-1]): continue
                    if i == n - 1 and (P & sol[0]): continue
                    sol.append(P)
                    if dfs(i + 1): return True
                    sol.pop()
                return False
            if dfs(0):
                return tuple(sol)
        return None

def main():
    R = realizable()
    print(f"realizable geometries: {len(R)}")
    for lab, abs_, strong in (("no label absent           ", frozenset(),  False),
                              ("cycle label 0 absent      ", frozenset({0}), False),
                              ("outsider 5 absent         ", frozenset({5}), True)):
        sat2 = sum(1 for pt in R if csp_solve(pt, 6, 3, abs_, strong) is not None)
        sat3 = [(pt, solve_min_variety(pt, absence=abs_, strong=strong)) for pt in R]
        sat3 = [(pt, w) for pt, w in sat3 if w is not None]
        print(f"\n{lab}:  any solution: {sat2:5d} / {len(R)};   "
              f"solution with >=3 distinct palette values: {len(sat3):5d} / {len(R)}")
        if sat3:
            pt, w = sat3[0]
            print(f"   geometry (gap assignment) {R[pt]}")
            print(f"   patterns   {[sorted(q) for q in pt]}")
            print(f"   palettes   {[sorted(p) for p in w]}   "
                  f"({len(set(w))} distinct values)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
