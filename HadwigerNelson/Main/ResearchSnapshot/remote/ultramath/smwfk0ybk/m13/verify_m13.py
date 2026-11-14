"""m13 verifier.  Independent decision procedures for the k=6 interface CSP and the
agreement checks for the sliver-profile report.

CHECK 0  m5's sliver formula == the paper's set definition (labels left after deleting
         endpoints of positive edges), and == m2 Lemma 1.1's cardinality formula.
CHECK 1  rotation symmetry: sat(l,c) = sat(l,c+s) for every shift s (so 6^l / 6^(l-1)).
CHECK 2  agreement of my DFS with m5's bitmask DP on EVERY (l, geometry), k=6.
CHECK 3  the two-outsider theorem: for l in {3,4} every geometry has the alternating
         singleton model; it satisfies (C1)-(C5) (verified, not assumed).
CHECK 4  (C4)+(C5) never remove the last model: brute-force (no pruning) agreement of
         "exists model of C1-C3" and "exists model of C1-C5" over ALL geometries.
CHECK 5  every satisfiable instance has a TERNARY-FREE model (so no constraint that only
         constrains 3-element palettes can ever bite at k=6).
"""
from itertools import product, combinations
import sys, json, random

sys.path.insert(0, "../../smwfhd5sl/m5")
import interface_csp as m5

K = 6

def paper_slivers(ell, k, c):
    """O_i = T minus endpoints of positive edges, plus U.  Direct from the paper's words."""
    U = set(range(ell, k))
    T = set(range(ell))
    rows = m5.sign_matrix(ell, c)
    out = []
    for i in range(6):
        row = rows[i]
        pos_endpoints = set()
        neg_endpoints = set()
        for j in range(ell):
            (pos_endpoints if row[j] == 1 else neg_endpoints).add(j)
            (pos_endpoints if row[(j + 1) % ell] == 1 else neg_endpoints).add((j + 1) % ell)
        O = (T - pos_endpoints) | U
        I = (T - neg_endpoints) | U
        out.append((frozenset(O), frozenset(I)))
    return out

def formula_slivers(ell, k, c):
    """m2 Lemma 1.1's cardinality formula, computed as sets: O = U + {both -}."""
    U = frozenset(range(ell, k))
    rows = m5.sign_matrix(ell, c)
    out = []
    for i in range(6):
        row = rows[i]
        O = set(U); I = set(U)
        for j in range(ell):
            if row[(j - 1) % ell] == -1 and row[j] == -1: O.add(j)
            if row[(j - 1) % ell] == 1 and row[j] == 1: I.add(j)
        out.append((frozenset(O), frozenset(I)))
    return out

def models(ell, k, c, tightened, ternary_free=False, limit=None):
    """No-pruning product enumeration: every six-tuple of admissible palettes, filtered."""
    sl = paper_slivers(ell, k, c)
    adm = [[frozenset(s) for r in range(1, k - 2) for s in combinations(range(k), r)
            if set(s) & O and set(s) & I] for (O, I) in sl]
    if any(not a for a in adm):
        return []
    full = frozenset(range(k))
    out = []
    for tup in product(*adm):
        if any(tup[i] & tup[(i + 1) % 6] for i in range(6)):
            continue
        if tightened:
            if sum(1 for p in tup if len(p) == 3) > 3:
                continue
            if any((tup[a] | tup[b]) == full
                   for a in range(6) for b in range(a + 1, 6)):
                continue
        if ternary_free and any(len(p) == 3 for p in tup):
            continue
        out.append(tup)
        if limit and len(out) >= limit:
            return out
    return out

def main():
    log = []
    def say(s):
        print(s, flush=True); log.append(s)

    # CHECK 0
    bad = 0
    for ell in range(3, K + 1):
        for c in product(range(6), repeat=ell):
            if paper_slivers(ell, K, c) != formula_slivers(ell, K, c):
                bad += 1
    say(f"CHECK 0  paper definition vs m2 size formula: mismatches = {bad}")

    # CHECK 1 rotation symmetry (all l, all shifts)
    rot_bad = 0
    for ell in range(3, K + 1):
        base = {}
        for c in product(range(6), repeat=ell):
            base[c] = m5.sat_geometry(ell, K, c)
        for c in base:
            for s in range(1, 6):
                cs = tuple((x + s) % 6 for x in c)
                if base[cs] != base[c]:
                    rot_bad += 1
    say(f"CHECK 1  rotation invariance of the C1-C3 decision: violations = {rot_bad}")

    # CHECK 2  my DFS vs m5 DP on every instance
    dis = 0; n = 0; sat_m5 = {}
    from profile2 import first_model
    for ell in range(3, K + 1):
        s = 0
        for c in product(range(6), repeat=ell):
            n += 1
            a = m5.sat_geometry(ell, K, c)
            b = first_model(ell, K, c, False) is not None
            s += a
            if a != b:
                dis += 1
        sat_m5[ell] = s
        say(f"CHECK 2  l={ell}: m5 DP SAT = {s}/{6**ell}")
    say(f"CHECK 2  disagreements between m5's DP and my DFS over {n} instances: {dis}")

    # CHECK 3 two-outsider theorem, l = 3,4
    th_bad = 0
    for ell in (3, 4):
        for c in product(range(6), repeat=ell):
            P = [frozenset([ell]) if i % 2 == 0 else frozenset([ell + 1]) for i in range(6)]
            sl = paper_slivers(ell, K, c)
            ok = all(1 <= len(P[i]) <= K - 3 for i in range(6))
            ok &= all((P[i] & sl[i][0]) and (P[i] & sl[i][1]) for i in range(6))
            ok &= all(not (P[i] & P[(i + 1) % 6]) for i in range(6))
            ok &= not any((P[a] | P[b]) == frozenset(range(K))
                          for a in range(6) for b in range(a + 1, 6))
            ok &= sum(1 for p in P if len(p) == 3) <= 3
            if not ok:
                th_bad += 1
    say(f"CHECK 3  two-outsider alternating model fails on {th_bad} geometries (l=3,4)")

    # CHECK 4  no instance killed by (C4)+(C5); brute force, all geometries
    killed = 0; tot = {ell: [0, 0] for ell in range(3, K + 1)}
    for ell in range(3, K + 1):
        for c in product(range(6), repeat=ell):
            a = bool(models(ell, K, c, tightened=False, limit=1))
            b = bool(models(ell, K, c, tightened=True, limit=1))
            tot[ell][0] += a; tot[ell][1] += b
            if a and not b:
                killed += 1
    for ell in range(3, K + 1):
        say(f"CHECK 4  l={ell}: C1-C3 SAT {tot[ell][0]}/{6**ell}, "
            f"C1-C5 SAT {tot[ell][1]}/{6**ell}")
    say(f"CHECK 4  instances satisfiable before but not after the tightening: {killed}")

    # CHECK 5  ternary-free models
    tf = {ell: 0 for ell in range(3, K + 1)}
    for ell in range(3, K + 1):
        for c in product(range(6), repeat=ell):
            if models(ell, K, c, tightened=True, ternary_free=True, limit=1):
                tf[ell] += 1
    for ell in range(3, K + 1):
        say(f"CHECK 5  l={ell}: instances with a ternary-free C1-C5 model: {tf[ell]}/{6**ell}")

    open("verify_m13.log", "w").write("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
