#!/usr/bin/env python3
"""m2 (swarm smwfxwsqf) -- RR127: map-level / refinement-obstruction checks.

Stdlib only, written independently (does not use m1's or m4's code).
Exact integer arithmetic throughout; canonical descending tuples.

Contents
  FIX   fixtures for n <= 6 (A_n and D_n listed)
  CNT   |A_n| = |D_n| for n <= 25  (subroutine, oracle only)
  INV   exhaustive two-sided inverse-law certificate for
          staircase  s : D_n -> {(k,mu) : mu weakly decreasing, >= 0, len k, |mu| = n-k^2}
          shift  T   : D_n -> B_n = {partitions of n, length k, smallest part >= k}
        for n = 0..25, including k = 0, 1, 2.
  STS   statistics battery: for each statistic, the first n <= 12 at which the
        distributions on A_n and D_n differ, plus a concrete witness.
"""

import sys
import time
from itertools import groupby

# --------------------------------------------------------------------------
# generation (canonical descending tuples)
# --------------------------------------------------------------------------


def gen_A(n):
    """All partitions of n, every part = 1 or 4 (mod 5).  Descending tuples."""
    allowed = [p for p in range(1, n + 1) if p % 5 in (1, 4)]
    out = []

    def rec(rem, cap, acc):
        if rem == 0:
            out.append(tuple(acc))
            return
        for p in allowed:                      # increasing
            if p > cap or p > rem:
                break
            acc.append(p)
            rec(rem - p, p, acc)
            acc.pop()

    rec(n, n, [])
    return out


def gen_D(n):
    """All partitions of n with lambda_i >= lambda_{i+1} + 2.  Descending."""
    out = []

    def rec(rem, cap, acc):
        if rem == 0:
            out.append(tuple(acc))
            return
        hi = min(rem, cap)
        for p in range(hi, 0, -1):
            acc.append(p)
            rec(rem - p, p - 2, acc)
            acc.pop()

    rec(n, n, [])
    return out


def wd(k, total, lo=0, hi=None):
    """All weakly decreasing k-tuples with entries in [lo,hi], sum total."""
    if hi is None:
        hi = total
    if k == 0:
        return [()] if total == 0 else []
    out = []
    first_max = min(hi, total - lo * (k - 1))
    for first in range(first_max, lo - 1, -1):
        for rest in wd(k - 1, total - first, lo, first):
            out.append((first,) + rest)
    return out


# --------------------------------------------------------------------------
# the two maps from the contract
# --------------------------------------------------------------------------


def staircase(lam):
    """D_n -> (k, mu),  mu_i = lam_i - (2(k-i)+1).  Returns (mu, k)."""
    k = len(lam)
    return tuple(lam[i] - (2 * (k - 1 - i) + 1) for i in range(k)), k


def staircase_inv(mu, k):
    """(mu, k) -> D_n,  lam_i = mu_i + 2(k-i)+1."""
    return tuple(mu[i] + 2 * (k - 1 - i) + 1 for i in range(k))


def shiftT(lam):
    """D_n -> B_n,  b_i = lam_i - k + 2i - 1."""
    k = len(lam)
    return tuple(lam[i] - k + 2 * (i + 1) - 1 for i in range(k))


def shiftT_inv(b):
    """B_n -> D_n,  lam_i = b_i + k - 2i + 1."""
    k = len(b)
    return tuple(b[i] + k - 2 * (i + 1) + 1 for i in range(k))


def is_D(lam):
    return all(lam[i] >= lam[i + 1] + 2 for i in range(len(lam) - 1)) and all(
        p >= 1 for p in lam
    )


def is_weak_deg_nonneg(mu):
    return all(mu[i] >= mu[i + 1] for i in range(len(mu) - 1)) and all(p >= 0 for p in mu)


def is_B(b):
    k = len(b)
    if k == 0:
        return True
    return is_weak_deg_nonneg(b) and b[-1] >= 1 and b[-1] >= k


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------

FAILS = []


def fail(tag, detail):
    FAILS.append((tag, detail))


def check_involutions(N=25):
    """Two-sided exhaustive certificate for staircase and T on D_n, n <= N."""
    stats = {"n": N, "D_states": 0, "stair_pairs": 0, "T_pairs": 0, "k_hist": {}}
    for n in range(N + 1):
        Dn = gen_D(n)
        # --- side 1: staircase forward, then inverse
        seen_pairs = set()
        for lam in Dn:
            stats["D_states"] += 1
            k = len(lam)
            stats["k_hist"][k] = stats["k_hist"].get(k, 0) + 1
            mu, k2 = staircase(lam)
            if k2 != k:
                fail("staircase-len", (n, lam, k, k2))
            if not is_weak_deg_nonneg(mu):
                fail("staircase-image-not-wd-nonneg", (n, lam, mu))
            if sum(mu) != n - k * k:
                fail("staircase-weight", (n, lam, mu, n - k * k))
            if len(mu) != k:
                fail("staircase-mu-len", (n, lam, k, len(mu)))
            back = staircase_inv(mu, k)
            if back != lam:
                fail("staircase-roundtrip-D", (n, lam, mu, back))
            if not is_D(back):
                fail("staircase-inverse-not-in-D", (n, lam, back))
            seen_pairs.add((k, mu))
            # --- side 2: every valid (k, mu) is hit
        for k in range(n + 1):
            target = n - k * k
            if target < 0:
                continue
            for mu in wd(k, target, lo=0):
                stats["stair_pairs"] += 1
                lam = staircase_inv(mu, k)
                if not is_D(lam):
                    fail("staircase-preimage-not-in-D", (n, k, mu, lam))
                if sum(lam) != n:
                    fail("staircase-preimage-weight", (n, k, mu, lam))
                got, gk = staircase(lam)
                if got != mu or gk != k:
                    fail("staircase-roundtrip-pairs", (n, k, mu, lam, got, gk))
                if (k, mu) not in seen_pairs:
                    fail("staircase-surjectivity", (n, k, mu))
        # --- shift T
        seenB = set()
        for lam in Dn:
            k = len(lam)
            b = shiftT(lam)
            if not is_B(b):
                fail("T-image-not-in-B", (n, lam, b))
            if sum(b) != n:
                fail("T-weight", (n, lam, b))
            if shiftT_inv(b) != lam:
                fail("T-roundtrip-D", (n, lam, b, shiftT_inv(b)))
            seenB.add(b)
        for k in range(n + 1):
            for b in wd(k, n, lo=k):
                stats["T_pairs"] += 1
                lam = shiftT_inv(b)
                if not is_D(lam):
                    fail("T-preimage-not-in-D", (n, k, b, lam))
                if sum(lam) != n:
                    fail("T-preimage-weight", (n, k, b, lam))
                if shiftT(lam) != b:
                    fail("T-roundtrip-B", (n, k, b, lam, shiftT(lam)))
                if b not in seenB:
                    fail("T-surjectivity", (n, k, b))
        if len(seenB) != len(Dn):
            fail("T-not-injective", (n, len(seenB), len(Dn)))
    return stats


def check_counts(N=25):
    t0 = time.time()
    rows = []
    for n in range(N + 1):
        a = len(gen_A(n))
        d = len(gen_D(n))
        rows.append((n, a, d, a == d))
        if a != d:
            fail("count-mismatch", (n, a, d))
    return rows, time.time() - t0


def check_fixtures():
    expect = {
        0: ({()}, {()}),
        1: ({(1,)}, {(1,)}),
        2: ({(1, 1)}, {(2,)}),
        3: ({(1, 1, 1)}, {(3,)}),
        4: ({(4,), (1, 1, 1, 1)}, {(4,), (3, 1)}),
        5: ({(4, 1), (1, 1, 1, 1, 1)}, {(5,), (4, 1)}),
        6: ({(6,), (4, 1, 1), (1, 1, 1, 1, 1, 1)}, {(6,), (5, 1), (4, 2)}),
    }
    lines = []
    contract = {2, 5}          # these two are fixed by the problem statement
    for n in range(0, 7):
        A, D = set(gen_A(n)), set(gen_D(n))
        lines.append((n, sorted(A, reverse=True), sorted(D, reverse=True),
                      A == expect[n][0], D == expect[n][1], n in contract))
        if A != expect[n][0]:
            fail("fixture-A", (n, sorted(A, reverse=True), sorted(expect[n][0], reverse=True)))
        if D != expect[n][1]:
            fail("fixture-D", (n, sorted(D, reverse=True), sorted(expect[n][1], reverse=True)))
    return lines


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------


def stat_largest(lam):
    return lam[0] if lam else 0


def stat_smallest(lam):
    return lam[-1] if lam else 0


def stat_len(lam):
    return len(lam)


def stat_ndistinct(lam):
    return len(set(lam))


def stat_len_parity(lam):
    return len(lam) % 2


def stat_largest_parity(lam):
    return (lam[0] % 2) if lam else 0


def stat_num_ones(lam):
    return sum(1 for p in lam if p == 1)


def stat_num_mult5(lam):
    return sum(1 for p in lam if p % 5 == 0)


def stat_num_eq4(lam):
    return sum(1 for p in lam if p % 5 == 4)


def stat_max_mult(lam):
    if not lam:
        return 0
    return max(len(list(g)) for _, g in groupby(lam))


def stat_repeat(lam):
    return 1 if len(set(lam)) < len(lam) else 0


def stat_len_mod5(lam):
    return len(lam) % 5


def stat_part_parity_count(lam):
    return sum(1 for p in lam if p % 2 == 1)


STATS = [
    ("largest part", stat_largest),
    ("smallest part", stat_smallest),
    ("number of parts", stat_len),
    ("number of distinct parts", stat_ndistinct),
    ("parity of number of parts", stat_len_parity),
    ("parity of largest part", stat_largest_parity),
    ("number of parts equal to 1", stat_num_ones),
    ("number of parts = 0 mod 5", stat_num_mult5),
    ("number of parts = 4 mod 5", stat_num_eq4),
    ("max multiplicity", stat_max_mult),
    ("repeated part? (0/1)", stat_repeat),
    ("number of parts mod 5", stat_len_mod5),
    ("number of odd parts", stat_part_parity_count),
]


def dist(S, f):
    d = {}
    for lam in S:
        v = f(lam)
        d[v] = d.get(v, 0) + 1
    return d


def check_stats(N=12):
    """For each statistic: first n where the distributions on A_n, D_n differ."""
    A = {n: gen_A(n) for n in range(N + 1)}
    D = {n: gen_D(n) for n in range(N + 1)}
    out = []
    for name, f in STATS:
        first = None
        detail = None
        for n in range(N + 1):
            da, dd = dist(A[n], f), dist(D[n], f)
            if da != dd:
                vals = sorted(set(da) | set(dd))
                over = [v for v in vals if da.get(v, 0) > dd.get(v, 0)]
                under = [v for v in vals if dd.get(v, 0) > da.get(v, 0)]
                # lexicographically smallest A-partition carrying an over-represented
                # value, and smallest D-partition carrying an under-represented value
                wA = None
                for v in over:
                    cands = sorted([lam for lam in A[n] if f(lam) == v], reverse=True)
                    if cands:
                        wA = (v, cands[0])
                        break
                wD = None
                for v in under:
                    cands = sorted([lam for lam in D[n] if f(lam) == v], reverse=True)
                    if cands:
                        wD = (v, cands[0])
                        break
                first = n
                detail = (da, dd, over, under, wA, wD)
                break
        out.append((name, first, detail))
    return out


def largest_part_table(N=12):
    rows = []
    for n in range(N + 1):
        A, D = gen_A(n), gen_D(n)
        da, dd = dist(A, stat_largest), dist(D, stat_largest)
        rows.append((n, len(A), len(D), da, dd, da == dd))
    return rows


# --------------------------------------------------------------------------


def main():
    t_start = time.time()

    print("=" * 72)
    print("m2 / swarm smwfxwsqf  --  RR127 map-level and refinement checks")
    print("=" * 72)

    # ---- FIX
    print("\n[FIX] sets for n = 0..6")
    t = time.time()
    for n, A, D, oka, okd, ctr in check_fixtures():
        print("  n=%2d  A_n (%d) = %s" % (n, len(A), A))
        print("        D_n (%d) = %s   [A %s, D %s]%s"
              % (len(D), D, "OK" if oka else "FAIL", "OK" if okd else "FAIL",
                 "   <- contract fixture" if ctr else "   <- my own expectation"))
    print("  FIX wall time %.3fs" % (time.time() - t))

    # ---- INV
    print("\n[INV] exhaustive inverse-law certificate, n = 0..25")
    t = time.time()
    st = check_involutions(25)
    print("  D_n states traversed           : %d" % st["D_states"])
    print("  staircase (k,mu) pairs tested  : %d" % st["stair_pairs"])
    print("  T  b in B_n  pairs tested      : %d" % st["T_pairs"])
    print("  length histogram k -> #parts   : %s"
          % {k: st['k_hist'][k] for k in sorted(st['k_hist'])})
    print("  k = 0 occurs %d time(s) (n = 0 only); k = 1 %d; k = 2 %d"
          % (st["k_hist"].get(0, 0), st["k_hist"].get(1, 0), st["k_hist"].get(2, 0)))
    print("  INV wall time %.3fs" % (time.time() - t))

    # ---- CNT
    print("\n[CNT] |A_n| vs |D_n|, n = 0..25  (subroutine / oracle)")
    t = time.time()
    rows, dt = check_counts(25)
    print("   n :" + "".join("%5d" % n for n, _, _, _ in rows))
    print("  |A|:" + "".join("%5d" % a for _, a, _, _ in rows))
    print("  |D|:" + "".join("%5d" % d for _, _, d, _ in rows))
    print("  agree on all n<=25 : %s" % all(ok for *_, ok in rows))
    print("  CNT wall time %.3fs" % dt)

    # ---- STS
    print("\n[STS] largest-part distribution, n = 0..12")
    for n, na, nd, da, dd, same in largest_part_table(12):
        print("  n=%2d |A|=%3d |D|=%3d  %s" % (n, na, nd, "SAME" if same else "DIFFER"))
        if not same:
            keys = sorted(set(da) | set(dd))
            print("       largest part r : " + "".join("%5d" % k for k in keys))
            print("       A count        : " + "".join("%5d" % da.get(k, 0) for k in keys))
            print("       D count        : " + "".join("%5d" % dd.get(k, 0) for k in keys))

    print("\n[STS] battery of statistics, first divergence for n <= 12")
    res = check_stats(12)
    approved, banned = [], []
    for name, first, detail in res:
        if first is None:
            approved.append(name)
            print("  %-32s AGREES for all n <= 12" % name)
        else:
            banned.append(name)
            da, dd, over, under, wA, wD = detail
            print("  %-32s first differs at n = %d" % (name, first))
            print("      over-represented on A side : %s" % (over,))
            print("      over-represented on D side : %s" % (under,))
            if wA:
                print("      witness A-side  %s  (stat = %s)" % (wA[1], wA[0]))
            if wD:
                print("      witness D-side  %s  (stat = %s)" % (wD[1], wD[0]))
    print("\n  APPROVED (distributions agree n<=12): %s" % (approved,))
    print("  BANNED  (cannot be preserved)       : %s" % (banned,))

    # ---- uniform obstruction for the all-ones partition
    print("\n[OBS] uniform obstruction, all n >= 2")
    bad = []
    for n in range(2, 31):
        A, D = gen_A(n), gen_D(n)
        ones = tuple([1] * n)
        inA = ones in A
        # largest part 1 on the D side
        d_one = [lam for lam in D if stat_largest(lam) == 1]
        d_len_n = [lam for lam in D if len(lam) == n]
        if not inA or d_one or d_len_n:
            bad.append((n, inA, d_one, d_len_n))
    print("  1^n in A_n for all n in 2..30 : %s"
          % all(tuple([1] * n) in gen_A(n) for n in range(2, 31)))
    print("  D_n has a partition with largest part 1 for n in 2..30 : %s"
          % any(lam[0] == 1 for n in range(2, 31) for lam in gen_D(n)))
    print("  D_n has a partition of length n for n in 2..30 : %s"
          % any(len(lam) == n for n in range(2, 31) for lam in gen_D(n)))
    print("  counterexamples to the claim : %s" % (bad,))

    print("\n" + "=" * 72)
    if FAILS:
        print("FAILURES: %d" % len(FAILS))
        for tag, detail in FAILS:
            print("  %-34s %s" % (tag, detail))
    else:
        print("ALL CHECKS PASSED (no failure recorded)")
    print("total wall time %.3fs" % (time.time() - t_start))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
