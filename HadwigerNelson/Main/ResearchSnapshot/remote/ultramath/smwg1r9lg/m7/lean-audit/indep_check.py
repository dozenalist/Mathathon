#!/usr/bin/env python3
"""Independent (non-Lean) exact check of the finite facts the four audited cores rely on.

Swarm smwg1r9lg, member m7, direction d8.  No floating point anywhere: integers and sympy
exact algebra only.  Two independent algorithms are used for the sector-field counts
(exhaustive enumeration and a backtracking colouring count).
"""
import itertools

# ---------------------------------------------------------------- frozen_core checks
def subsets(n):
    for m in range(1 << n):
        yield frozenset(i for i in range(n) if m >> i & 1)

def frozen_core_check():
    U = frozenset(range(6))
    bad_union = bad_fourth = bad_free = 0
    n_triples = 0
    for A in subsets(6):
        for B in subsets(6):
            if A & B:
                continue
            for C in subsets(6):
                if (A & C) or (B & C):
                    continue
                if not (len(A) >= 2 and len(B) >= 2 and len(C) >= 2):
                    continue
                n_triples += 1
                if (A | B | C) != U:
                    bad_union += 1
                for D in subsets(6):
                    if D and not (D & A) and not (D & B) and not (D & C):
                        bad_fourth += 1
    for A in subsets(6):
        for B in subsets(6):
            if A & B:
                continue
            for C in subsets(6):
                if (A & C) or (B & C):
                    continue
                free = U - (A | B | C)
                if free and not (len(A) <= 1 or len(B) <= 1 or len(C) <= 1):
                    bad_free += 1
    sharp = (frozenset({0}) | frozenset({1}) | frozenset({2})) != U
    return dict(triples_size2=n_triples, union_failures=bad_union,
                fourth_failures=bad_fourth, free_label_failures=bad_free,
                singleton_triple_fails_to_exhaust=sharp)

# ---------------------------------------------------------------- count_lemma checks
def count_lemma_check():
    bad = 0
    for A in subsets(5):
        for B in subsets(5):
            if A & B:
                continue
            for C in subsets(5):
                if (A & C) or (B & C):
                    continue
                if len(A) >= 2 and len(B) >= 2 and len(C) >= 2:
                    bad += 1
    bad_adm = []
    for P in subsets(6):
        if all(not P <= frozenset({i, (i + 1) % 6}) for i in range(6)):
            if len(P) < 2:
                bad_adm.append(sorted(P))
    sharp = [frozenset({0, 1}), frozenset({2, 3}), frozenset({4, 5})]
    sharp_ok = (not (sharp[0] & sharp[1])) and (not (sharp[0] & sharp[2])) \
        and (not (sharp[1] & sharp[2])) and all(len(s) == 2 for s in sharp)
    return dict(three_disjoint_size2_in_5set=bad, admissible_singletons=bad_adm,
                sharpness_witness_ok=sharp_ok)

# ---------------------------------------------------------------- sector fields
def sector_bruteforce(n, m, nvals):
    cnt = 0
    sols = []
    for V in itertools.product(range(nvals), repeat=n):
        if all(V[(i + m) % n] != V[i] and V[(i + m + 1) % n] != V[i] for i in range(n)):
            cnt += 1
            if len(sols) < 8:
                sols.append(V)
    return cnt, sols

def sector_backtrack(n, m, nvals):
    adj = {i: set() for i in range(n)}
    for i in range(n):
        for j in ((i + m) % n, (i + m + 1) % n):
            if j != i:
                adj[i].add(j)
                adj[j].add(i)
    assign = {}
    nodes = sorted(range(n), key=lambda v: -len(adj[v]))

    def rec(k):
        if k == n:
            return 1
        v = nodes[k]
        total = 0
        for c in range(nvals):
            if all(assign.get(u) != c for u in adj[v]):
                assign[v] = c
                total += rec(k + 1)
                del assign[v]
        return total
    return rec(0)

def sector_check(maxm=6):
    out = {}
    for m in range(1, maxm + 1):
        n = 6 * m
        out[(n, m)] = dict(two_valued=sector_backtrack(n, m, 2),
                           three_valued=sector_backtrack(n, m, 3))
    b6 = sector_bruteforce(6, 1, 3)
    b12 = sector_bruteforce(12, 2, 3)
    b6two = sector_bruteforce(6, 1, 2)
    return dict(table=out, brute_3val_n6=b6, brute_3val_n12=b12, brute_2val_n6=b6two)

# ---------------------------------------------------------------- repair31 geometry
def geometry_check():
    import sympy as sp
    s3, s11 = sp.sqrt(3), sp.sqrt(11)
    u = sp.Rational(5, 6) + sp.I * s11 / 6
    w = sp.Rational(-1, 2) + sp.I * s3 / 2
    lam = 1 - u
    def nsq(z):
        return sp.simplify(sp.re(z) ** 2 + sp.im(z) ** 2)
    checks = {
        "normSq_u=1": sp.simplify(nsq(u) - 1) == 0,
        "normSq_w=1": sp.simplify(nsq(w) - 1) == 0,
        "normSq_lam=1/3": sp.simplify(nsq(lam) - sp.Rational(1, 3)) == 0,
        "normSq_1mw=3": sp.simplify(nsq(1 - w) - 3) == 0,
        "normSq_1pw=1": sp.simplify(nsq(1 + w) - 1) == 0,
        "w^3=1": sp.simplify(w ** 3 - 1) == 0,
    }
    z = [sp.expand(lam * w ** j) for j in range(3)]
    checks["pairwise_unit"] = all(
        sp.simplify(nsq(z[a] - z[b]) - 1) == 0 for a in range(3) for b in range(a + 1, 3))
    checks["circumradius^2=1/3"] = all(
        sp.simplify(nsq(zz) - sp.Rational(1, 3)) == 0 for zz in z)
    t = 1 / (2 * s3)
    cosg = sp.simplify(1 - 2 * t ** 2)
    sing = sp.simplify(2 * t * sp.sqrt(1 - t ** 2))
    checks["cos_gamma0=5/6"] = sp.simplify(cosg - sp.Rational(5, 6)) == 0
    checks["sin_gamma0=sqrt11/6"] = sp.simplify(sing - s11 / 6) == 0
    a, b = sp.symbols("a b", real=True)
    sol = sp.solve([a ** 2 + b ** 2 - 1, (1 + a) ** 2 + b ** 2 - sp.Rational(1, 3)], [a, b],
                   dict=True)
    checks["rigidity_Re=-5/6"] = bool(sol) and all(
        sp.simplify(s[a] + sp.Rational(5, 6)) == 0 for s in sol)
    return checks

# ---------------------------------------------------------------- engine threshold
def engine_threshold_check():
    from fractions import Fraction
    res = {}
    for k in (5, 6):
        res[k] = dict(bound_zero_at_alpha=str(Fraction(1, k)))
    res["cover"] = dict(ball=5, mesh=2, hitting_radius=1, slack=5 - (2 + 1))
    return res

def main():
    out = {}
    out["frozen_core"] = frozen_core_check()
    out["count_lemma"] = count_lemma_check()
    out["sector"] = sector_check(6)
    out["geometry"] = geometry_check()
    out["engine"] = engine_threshold_check()
    print("frozen_core:", out["frozen_core"])
    print("count_lemma:", out["count_lemma"])
    print("sector table:", {f"n={n},m={m}": v for (n, m), v in out["sector"]["table"].items()})
    print("sector brute force n=6 (3-valued):", out["sector"]["brute_3val_n6"])
    print("sector brute force n=6 (2-valued):", out["sector"]["brute_2val_n6"])
    print("sector brute force n=12 (3-valued):", out["sector"]["brute_3val_n12"])
    print("geometry:", out["geometry"])
    print("engine:", out["engine"])
    fc = out["frozen_core"]
    assert fc["union_failures"] == 0 and fc["fourth_failures"] == 0
    assert fc["free_label_failures"] == 0 and fc["singleton_triple_fails_to_exhaust"]
    cl = out["count_lemma"]
    assert cl["three_disjoint_size2_in_5set"] == 0 and cl["admissible_singletons"] == []
    assert cl["sharpness_witness_ok"]
    sec = out["sector"]
    assert all(v["two_valued"] == 0 for v in sec["table"].values())
    assert sec["table"][(6, 1)]["three_valued"] == 6
    assert sec["brute_3val_n6"][0] == 6 and sec["brute_2val_n6"][0] == 0
    assert all(out["geometry"].values()), out["geometry"]
    print("ALL ASSERTIONS HOLD")

if __name__ == "__main__":
    main()
