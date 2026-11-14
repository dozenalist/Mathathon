"""D4 structural probe: can the D-side staircase level k (#parts of the
D-partition) be read off a *simple statistic of the A-partition*?

For every n <= NMAX we compute
  level(k) distribution   d(n,k) = p_{<=k}(n - k^2)
and for each candidate statistic f the distribution {value of f} -> count over
A_n.  If f is to serve as the level function, its value-distribution must equal
d(n,.) exactly (as {k: count}).  We report, per statistic, the largest n
<= NMAX for which this holds and the first n where it breaks, with witness.
"""
from explore import (enum_A, enum_D, level_counts, staircase, staircase_inv,
                     shiftT, shiftT_inv, weak_dec, NMAX)
from collections import Counter

NMAX = 14

def durfee(p):
    d = 0
    for i, v in enumerate(p):
        if v >= i + 1: d = i + 1
        else: break
    return d

STATS = {
 "len":            lambda a: len(a),
 "max":            lambda a: (a[0] if a else 0),
 "min":            lambda a: (min(a) if a else 0),
 "nparts_eq4":     lambda a: sum(1 for p in a if p % 5 == 4),
 "nparts_eq1":     lambda a: sum(1 for p in a if p % 5 == 1),
 "eq1_minus_eq4":  lambda a: sum(1 if p % 5 == 1 else -1 for p in a),
 "ndistinct":      lambda a: len(set(a)),
 "durfee":         lambda a: durfee(a),
 "sum_floor_p5":   lambda a: sum(p // 5 for p in a),
 "nparts_ge6":     lambda a: sum(1 for p in a if p >= 6),
 "nparts_ge5":     lambda a: sum(1 for p in a if p >= 5),
 "nparts_eq1s":    lambda a: sum(1 for p in a if p == 1),
 "nparts_eq4s":    lambda a: sum(1 for p in a if p == 4),
 "rank_max_minus_len": lambda a: (a[0] - len(a)) if a else 0,
 "max_minus_min":  lambda a: ((a[0] - a[-1]) if a else 0),
 "nparts_gt_2min": lambda a: sum(1 for p in a if a and p > 2 * a[-1]),
 "sum_ceil_p5":    lambda a: sum(-((-p) // 5) for p in a),
 "nparts_odd":     lambda a: sum(1 for p in a if p % 2 == 1),
 "nparts_even":    lambda a: sum(1 for p in a if p % 2 == 0),
 "floor_sqrt_len": lambda a: int(len(a) ** 0.5),
 "nparts_gt4":     lambda a: sum(1 for p in a if p > 4),
 "floor_sqrt_max": lambda a: int(a[0] ** 0.5) if a else 0,
 "greedy_eq4_carry": lambda a: sum(1 for p in a if p % 5 == 4 and p > 4),
 "nparts_mod5_1_times_p5": lambda a: sum((p - 1) // 5 for p in a if p % 5 == 1),
}

def compare(a_set, n):
    lev = level_counts(n)
    rows = []
    for name, f in STATS.items():
        c = Counter(f(x) for x in a_set)
        if dict(c) == dict(lev):
            rows.append((name, "EXACT", None))
        elif sorted(c.values()) == sorted(lev.values()):
            rows.append((name, "sizes-only", None))
        else:
            # witness: the level whose size mismatches / a value with no partner
            rows.append((name, "fail", dict(sorted(c.items()))))
    return lev, rows

def main():
    print("=== level distributions d(n,k) = p_{<=k}(n-k^2) ===")
    for n in range(NMAX + 1):
        print(f"  n={n:2d}  |A_n|={len(enum_A(n)):3d}   levels {dict(sorted(level_counts(n).items()))}")

    print("\n=== candidate A-side statistics vs the level distribution ===")
    verdict = {name: [None, None] for name in STATS}
    for n in range(NMAX + 1):
        a = enum_A(n)
        lev, rows = compare(a, n)
        for name, v, wit in rows:
            if verdict[name][0] is None:
                if v != "EXACT":
                    verdict[name][0] = (n, v, wit)
        # report first few n in detail
        if n <= 6:
            print(f"\n n={n}: levels={dict(sorted(lev.items()))}")
            for name, v, wit in rows:
                print(f"    {name:26s} {v:10s} {'' if wit is None else wit}")
    print("\n=== first n at which each statistic FAILS to be the level function ===")
    for name in STATS:
        v = verdict[name][0]
        print(f"  {name:26s} " + ("never failed on n<=%d" % NMAX if v is None else f"first fail n={v[0]} kind={v[1]} dist={v[2]}"))
    nev = [m for m in STATS if verdict[m][0] is None]
    print("\nstatistics never failing on n <= %d:" % NMAX, nev)

    # largest-part distribution test (informative for everyone)
    print("\n=== largest-part distribution: A_n vs D_n ===")
    firstbad = None
    for n in range(min(NMAX, 12) + 1):
        ca = Counter((x[0] if x else 0) for x in enum_A(n))
        cd = Counter((x[0] if x else 0) for x in enum_D(n))
        same = dict(ca) == dict(cd)
        print(f"  n={n:2d} A={dict(sorted(ca.items()))}  D={dict(sorted(cd.items()))}  {'same' if same else 'DIFFER'}")
        if not same and firstbad is None:
            firstbad = n
    print("  smallest n with differing largest-part distribution:", firstbad)
    if firstbad is not None:
        n = firstbad
        ca = sorted(enum_A(n)); cd = sorted(enum_D(n))
        print("  A_n sorted:", ca)
        print("  D_n sorted:", cd)
        sa = set(x[0] for x in ca); sd = set(x[0] for x in cd)
        print("  largest parts only in A:", sorted(sa - sd), " only in D:", sorted(sd - sa))
        for v in sorted(sa ^ sd):
            side = [x for x in ca if x[0] == v] if v in sa else [x for x in cd if x[0] == v]
            print(f"    size {v}: c_A={ca and sum(1 for x in ca if x[0]==v)}, c_D={sum(1 for x in cd if x[0]==v)}, exemplar {side[0]}")

if __name__ == "__main__":
    main()
