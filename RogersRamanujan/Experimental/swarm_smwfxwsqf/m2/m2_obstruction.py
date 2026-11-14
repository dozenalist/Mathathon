#!/usr/bin/env python3
"""m2 (swarm smwfxwsqf) -- RR127: refinement obstruction, quantified.

Companion to m2_check.py (which certifies the staircase/T inverse laws).
Stdlib only, exact integers, independent code.

Sections
  [DICT] the exact dictionary between the two contract reductions
         (staircase image mu, shift image b) -- verified for n <= 25.
  [COARS] how far the largest-part refinement is from being preservable:
         the minimum number of contiguous blocks the largest-part line must be
         cut into before the A- and D-distributions can agree (n <= 12).
         Blocks = 1 means the statistic carries *no* information.
  [SCAN] a battery of ~40 statistics; which agree for all n <= 12
         (= approved invariants a candidate bijection may claim to preserve)
         and which are banned, with the first n and a witness.
  [COARSEN] scan of binary coarsenings [f(.) in S] for every level set S of
         every base statistic: a quantitative measure of how constrained the map is.
  [FORCED] A-partitions whose largest part is unattainable on the D side,
         i.e. that a largest-part-preserving map provably cannot handle.
"""

import sys
from itertools import groupby

FAILS = []


def fail(tag, detail):
    FAILS.append((tag, detail))


# --------------------------------------------------------------------------
# generation (same canonical generators as m2_check.py, restated)
# --------------------------------------------------------------------------


def gen_A(n):
    allowed = [p for p in range(1, n + 1) if p % 5 in (1, 4)]
    out = []

    def rec(rem, cap, acc):
        if rem == 0:
            out.append(tuple(acc))
            return
        for p in allowed:
            if p > cap or p > rem:
                break
            acc.append(p)
            rec(rem - p, p, acc)
            acc.pop()

    rec(n, n, [])
    return out


def gen_D(n):
    out = []

    def rec(rem, cap, acc):
        if rem == 0:
            out.append(tuple(acc))
            return
        for p in range(min(rem, cap), 0, -1):
            acc.append(p)
            rec(rem - p, p - 2, acc)
            acc.pop()

    rec(n, n, [])
    return out


def staircase(lam):
    k = len(lam)
    return tuple(lam[i] - (2 * (k - 1 - i) + 1) for i in range(k)), k


def shiftT(lam):
    k = len(lam)
    return tuple(lam[i] - k + 2 * (i + 1) - 1 for i in range(k))


# --------------------------------------------------------------------------
# [DICT]
# --------------------------------------------------------------------------


def dict_check(N=25):
    cnt = 0
    for n in range(N + 1):
        for lam in gen_D(n):
            k = len(lam)
            mu, _ = staircase(lam)
            b = shiftT(lam)
            cnt += 1
            # mu_i = b_i - k  (componentwise), for i = 1..k
            if tuple(x - k for x in b) != mu:
                fail("dict mu=b-k", (n, lam, mu, b))
            if k >= 1:
                if mu[0] != lam[0] - 2 * k + 1:
                    fail("dict mu_1", (n, lam))
                if b[0] != lam[0] - k + 1:
                    fail("dict b_1", (n, lam))
                if mu[-1] != lam[-1] - 1:
                    fail("dict mu_k", (n, lam))
                if b[-1] != lam[-1] + k - 1:
                    fail("dict b_k", (n, lam))
                if b[-1] < k:
                    fail("dict b_k >= k", (n, lam, b))
    return cnt


def wd(k, total, lo=0, hi=None):
    """Weakly decreasing k-tuples with entries in [lo,hi] and sum total."""
    if hi is None:
        hi = total
    if k == 0:
        return [()] if total == 0 else []
    out = []
    for first in range(min(hi, total - lo * (k - 1)), lo - 1, -1):
        for rest in wd(k - 1, total - first, lo, first):
            out.append((first,) + rest)
    return out


def len_law(N=25):
    """#{lam in D_n : len = k} must equal #{partitions of n-k^2 into at most k
    parts}, for every n,k.  This is the counting constraint any candidate
    bijection A_n -> D_n has to meet, read off the (k,mu) reduction."""
    bad = []
    total = 0
    for n in range(N + 1):
        D = gen_D(n)
        for k in range(n + 1):
            lhs = sum(1 for l in D if len(l) == k)
            m = n - k * k
            rhs = len(wd(k, m)) if m >= 0 else 0     # partitions of m into <= k parts
            total += 1
            if lhs != rhs:
                bad.append((n, k, lhs, rhs))
    return total, bad


# --------------------------------------------------------------------------
# statistics battery
# --------------------------------------------------------------------------


def S(name, f):
    return (name, f)


def sum_res(r):
    return lambda lam: sum(p for p in lam if p % 5 == r)


STATS = [
    S("largest part", lambda l: l[0] if l else 0),
    S("smallest part", lambda l: l[-1] if l else 0),
    S("number of parts", len),
    S("number of distinct parts", lambda l: len(set(l))),
    S("parity of number of parts", lambda l: len(l) % 2),
    S("number of parts mod 5", lambda l: len(l) % 5),
    S("parity of largest part", lambda l: (l[0] % 2) if l else 0),
    S("largest part mod 5", lambda l: (l[0] % 5) if l else 0),
    S("number of parts equal to 1", lambda l: l.count(1)),
    S("number of parts = 0 mod 5", lambda l: sum(1 for p in l if p % 5 == 0)),
    S("number of parts = 1 mod 5", lambda l: sum(1 for p in l if p % 5 == 1)),
    S("number of parts = 2 mod 5", lambda l: sum(1 for p in l if p % 5 == 2)),
    S("number of distinct residues mod 5", lambda l: len({p % 5 for p in l})),
    S("max multiplicity", lambda l: max([len(list(g)) for _, g in groupby(l)], default=0)),
    S("repeated part? 0/1", lambda l: 1 if len(set(l)) < len(l) else 0),
    S("number of odd parts", lambda l: sum(1 for p in l if p % 2)),
    S("number of even parts", lambda l: sum(1 for p in l if p % 2 == 0)),
    S("spread largest-smallest", lambda l: (l[0] - l[-1]) if l else 0),
    S("largest minus 1", lambda l: (l[0] - 1) if l else 0),
    S("number of parts >= 2", lambda l: sum(1 for p in l if p >= 2)),
    S("number of parts >= 5", lambda l: sum(1 for p in l if p >= 5)),
    S("sum of parts = 1 mod 5", sum_res(1)),
    S("sum of parts = 4 mod 5", sum_res(4)),
    S("sum of parts = 0 mod 5", sum_res(0)),
    S("multiplicity of the largest part", lambda l: (sum(1 for p in l if p == l[0]) if l else 0)),
    S("number of parts in a run of length >= 2", lambda l: sum(
        len(run) for run in [list(g) for _, g in groupby(l)] if len(run) >= 2)),
    S("second largest part (0 if none)", lambda l: (sorted(l, reverse=True) + [0, 0])[1]),
    S("largest - second largest", lambda l: ((lambda s: s[0] - s[1])(sorted(l, reverse=True) + [0, 0]))),
    S("weight mod 2 (trivial control: equals n mod 2)", lambda l: sum(l) % 2),
    S("number of parts = 4 mod 5", lambda l: sum(1 for p in l if p % 5 == 4)),
    S("number of parts = 3 mod 5", lambda l: sum(1 for p in l if p % 5 == 3)),
]


def dist(seq, f):
    d = {}
    for lam in seq:
        v = f(lam)
        d[v] = d.get(v, 0) + 1
    return d


def report_diff(name, n, da, dd, A, D, f):
    vals = sorted(set(da) | set(dd))
    over = [v for v in vals if da.get(v, 0) > dd.get(v, 0)]
    under = [v for v in vals if dd.get(v, 0) > da.get(v, 0)]
    wA = wD = None
    for v in over:
        c = sorted([l for l in A if f(l) == v], reverse=True)
        if c:
            wA = (v, c[0])
            break
    for v in under:
        c = sorted([l for l in D if f(l) == v], reverse=True)
        if c:
            wD = (v, c[0])
            break
    return over, under, wA, wD


def scan(N=12):
    A = {n: gen_A(n) for n in range(N + 1)}
    D = {n: gen_D(n) for n in range(N + 1)}
    approved, banned = [], []
    for name, f in STATS:
        first = None
        det = None
        for n in range(N + 1):
            da, dd = dist(A[n], f), dist(D[n], f)
            if da != dd:
                first = n
                det = report_diff(name, n, da, dd, A[n], D[n], f)
                break
        if first is None:
            approved.append(name)
        else:
            banned.append((name, first, det))
    return approved, banned, A, D


# --------------------------------------------------------------------------
# [COARS] minimum number of contiguous blocks
# --------------------------------------------------------------------------


def min_blocks(pa, pd):
    """Given count dicts pa, pd on integer keys, minimum number of contiguous
    blocks of the key line on which the grouped counts coincide.
    Prefix-difference criterion: a cut after r is allowed iff
    sum_{r'<=r}(pa-pd)(r') = 0."""
    keys = sorted(set(pa) | set(pd))
    run = 0
    cuts = 0                      # number of allowed cut points strictly inside
    for i, r in enumerate(keys):
        run += pa.get(r, 0) - pd.get(r, 0)
        if i < len(keys) - 1 and run == 0:
            cuts += 1
    if run != 0:
        return None               # impossible: totals differ (cannot happen)
    return cuts + 1


def coarseness(N=12):
    A = {n: gen_A(n) for n in range(N + 1)}
    D = {n: gen_D(n) for n in range(N + 1)}
    fl = STATS[0][1]            # largest part
    fk = STATS[2][1]            # number of parts
    rows = []
    for n in range(N + 1):
        da, dd = dist(A[n], fl), dist(D[n], fl)
        ea, ed = dist(A[n], fk), dist(D[n], fk)
        rows.append((n,
                     min_blocks(da, dd), len(set(da) | set(dd)),
                     min_blocks(ea, ed), len(set(ea) | set(ed))))
    return rows


# --------------------------------------------------------------------------
# [COARSEN] binary coarsenings
# --------------------------------------------------------------------------


def coarsening_scan(N=12):
    A = {n: gen_A(n) for n in range(N + 1)}
    D = {n: gen_D(n) for n in range(N + 1)}
    tested = 0
    agree = []
    for name, f in STATS:
        levels = set()
        for n in range(N + 1):
            levels |= set(dist(A[n], f)) | set(dist(D[n], f))
        for t in sorted(levels):
            g = (lambda f, t: lambda l: 1 if f(l) == t else 0)(f, t)
            tested += 1
            ok = True
            for n in range(N + 1):
                if dist(A[n], g) != dist(D[n], g):
                    ok = False
                    break
            if ok:
                agree.append((name, "== %s" % t))
        # also cumulative indicators f <= t (interior thresholds)
        lv = sorted(levels)
        for t in lv[:-1]:
            g = (lambda f, t: lambda l: 1 if f(l) <= t else 0)(f, t)
            tested += 1
            ok = True
            for n in range(N + 1):
                if dist(A[n], g) != dist(D[n], g):
                    ok = False
                    break
            if ok:
                agree.append((name, "<= %s" % t))
    return tested, agree


# --------------------------------------------------------------------------
# [FORCED]
# --------------------------------------------------------------------------


def forced(N=12):
    rows = []
    for n in range(N + 1):
        A, D = gen_A(n), gen_D(n)
        dmax = {l[0] for l in D if l} | ({0} if any(not l for l in D) else set())
        forcedset = [l for l in A if l and l[0] not in dmax]
        rows.append((n, len(A), len(forcedset), sorted(forcedset, reverse=True)[:6]))
    return rows


# --------------------------------------------------------------------------


def main():
    print("=" * 74)
    print("m2 / swarm smwfxwsqf -- RR127 refinement obstruction (quantified)")
    print("=" * 74)

    cnt = dict_check(25)
    print("\n[DICT] staircase/shift dictionary, %d D-partitions, n <= 25" % cnt)
    print("  verified: mu_i = b_i - k (all i);  mu_1 = lam_1-2k+1;  mu_k = lam_k-1;")
    print("            b_1 = lam_1-k+1;  b_k = lam_k+k-1 >= k")
    print("  so the two contract reductions differ only by the constant shift k,")
    print("  i.e. b = mu + k componentwise and lam = mu + staircase(k).")

    print("\n[COARS] minimum number of contiguous blocks of the value line")
    print("        needed before the A- and D-distributions can agree")
    print("        (min=1 with max>1 means the statistic must be thrown away)")
    print("   n   largest part      number of parts")
    print("       min/max levels    min/max levels")
    for n, blp, mlp, bnp, mnp in coarseness(12):
        print("  %2d      %2d / %-3d         %2d / %-3d" % (n, blp, mlp, bnp, mnp))

    print("\n[LEN] enforced length law: #{lam in D_n : len = k} = p(n-k^2 into <= k parts)")
    for n in range(0, 16):
        D = gen_D(n)
        row = []
        for k in range(0, n + 1):
            m = n - k * k
            row.append(sum(1 for l in D if len(l) == k) if m >= 0 else None)
        print("  n=%2d  k=0..%2d : %s" % (n, n, [x for x in row if x is not None]))
    tot, bad = len_law(25)
    print("  pairs (n,k) with n<=25 tested: %d ; violations: %s" % (tot, bad if bad else "none"))
    if bad:
        fail("len-law", bad[:5])

    print("\n[SCAN] %d statistics, full-distribution agreement on n = 0..12" % len(STATS))
    approved, banned, A, D = scan(12)
    print("  APPROVED invariants (may be claimed preserved): %s" % (approved or "NONE",))
    print("  BANNED (first divergent n, witnesses):")
    for name, first, det in banned:
        over, under, wA, wD = det
        print("    %-44s n=%2d" % (name, first))
        print("        A side %s (value %s) has no partner with that value;"
              % (wA[1] if wA else "-", wA[0] if wA else "-"))
        print("        D side %s (value %s) is unmatched" % (wD[1] if wD else "-", wD[0] if wD else "-"))

    tested, agree = coarsening_scan(12)
    print("\n[COARSEN] binary coarsenings 1_{f(.) = t} and 1_{f(.) <= t}:")
    print("  tested %d such statistics; agree on all n <= 12: %d" % (tested, len(agree)))
    for a in agree[:40]:
        print("    agrees: %s %s" % a)

    print("\n[FORCED] A-partitions whose largest part never occurs in D_n")
    print("   n  |A_n|  #forced   examples")
    for n, na, k, ex in forced(12):
        print("  %2d  %5d  %7d   %s" % (n, na, k, ex))

    print("\n" + "=" * 74)
    if FAILS:
        print("FAILURES: %d" % len(FAILS))
        for t, d in FAILS:
            print("  %-24s %s" % (t, d))
    else:
        print("ALL CHECKS PASSED")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
