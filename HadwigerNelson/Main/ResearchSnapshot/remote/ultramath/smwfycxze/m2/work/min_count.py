#!/usr/bin/env python3
"""
d2: quantitative form.  Theorem 1 says: at a k=6 centre carrying a 5-cycle with outsider X,
the six palettes on any full R-orbit cannot all avoid X.  Hence for a.e. e some rotation
R^i e has X in its palette, and

        sigma{e : X in P_x(e)}  >=  m * 2*pi/6 = m*pi/3,      m = min #orbit positions forced.

(5.7) gives the complementary upper bound sigma <= pi.  This script computes
   m        = the minimum, over admissible configurations, of #{i : X in P_i}
   m_arc    = the same minimum when the field is only required to be arc-constant (exact
              geometry, real angles), i.e. the smallest possible ANGULAR MEASURE of {X in P}
over:  (a) the geometry-free family,  (b) the 7776 gap geometries.
With (6.2) on and off, and with |P| <= 3 (the k = 6 palette bound) on and off.
"""
import itertools, sys
sys.path.insert(0, "work")
from verify_d2 import (lemmaA, comp, allowed, internal, palettes, csp_solve, csp_solve_cadical,
                       family, ELL)

def min_count(fam, k=6, b=3, use62=True):
    best = 99; witness = None
    for pt in fam:
        # search over all admissible tuples, minimising #{i : X in P_i}
        opts = [palettes(Q, k, b) for Q in pt]
        if any(not o for o in opts): continue
        if use62:
            opts = [[P for P in os_ if not any(P <= frozenset({j, (j + 1) % ELL}) for j in range(ELL))]
                     for os_ in opts]
        n = len(pt); sol = []
        found = [99, None]
        def dfs(i):
            if i == n:
                c = sum(1 for P in sol if (k - 1) in P)
                if c < found[0]:
                    found[0] = c; found[1] = tuple(sol)
                return
            for P in opts[i]:
                if sol and (P & sol[-1]): continue
                if i == n - 1 and (P & sol[0]): continue
                sol.append(P); dfs(i + 1); sol.pop()
        dfs(0)
        if found[0] < best:
            best = found[0]; witness = (pt, found[1])
    return best, witness

def main():
    G, table = lemmaA()
    fam = list(family(table))
    print("== geometry-free family (1000 six-tuples) ==")
    for b in (3, 5):
        for u62 in (True, False):
            m, w = min_count(fam, b=b, use62=u62)
            print(f"   |P|<={b}, (6.2)={u62}:  min #{{i : X in P_i}} = {m}"
                  f"   => sigma {{X in P}} >= {m}/6 of the circle")
            if w: print(f"        witness {[sorted(p) for p in w[1]]}")
    # realizable geometries
    seen = {}
    for gap in itertools.product(range(6), repeat=5):
        pt = tuple(frozenset(j for j in range(5) if (gap[j] - m) % 6 in (0, 1, 2)) for m in range(6))
        seen.setdefault(pt, gap)
    print("== 7776 gap geometries ==")
    for use62 in (True, False):
        m, w = min_count(list(seen), b=3, use62=use62)
        print(f"   |P|<=3, (6.2)={use62}:  min = {m}")
        if w:
            print(f"        patterns {[sorted(q) for q in w[0]]}")
            print(f"        palettes {[sorted(p) for p in w[1]]}")

if __name__ == "__main__":
    main()
