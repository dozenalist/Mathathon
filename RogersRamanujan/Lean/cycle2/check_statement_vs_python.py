"""Statement cross-check for StaircaseOrder.lean.

The Lean file *proves* `subStair_weakDec` for all lists.  This script checks that
the statement it proves is the intended mathematical statement, by recomputing
the same objects in Python (self-contained enumeration, no repo code imported)
and by pinning down the two things the Lean file claims are essential:

  (1) `stair` of a gap partition is weakly decreasing  -- n <= 22, exhaustive;
  (2) positivity alone is not enough ([1,3] is a counterexample to the order law);
  (3) zero padding carries the length (dropping zeros changes `unstair`).

Run:  python3 check_statement_vs_python.py
"""
import sys


def partitions_gap(n):
    """Descending partitions of n with lambda_i >= lambda_{i+1} + 2."""
    out = []

    def rec(rem, cap, acc):
        if rem == 0:
            out.append(tuple(acc))
            return
        top = min(cap, rem)
        for p in range(top, 0, -1):
            acc.append(p)
            rec(rem - p, p - 2, acc)
            acc.pop()

    rec(n, n, [])
    return out


def stair(lam):
    k = len(lam)
    return tuple(lam[i] - (2 * (k - i - 1) + 1) for i in range(k))


def unstair(mu):
    k = len(mu)
    return tuple(mu[i] + (2 * (k - i - 1) + 1) for i in range(k))


def weak_dec(t):
    return all(t[i + 1] <= t[i] for i in range(len(t) - 1))


NMAX = 22
checked = 0
bad = []
for n in range(NMAX + 1):
    for lam in partitions_gap(n):
        k = len(lam)
        mu = stair(lam)
        checked += 1
        if not weak_dec(mu):
            bad.append(("order", n, lam, mu))
        if len(mu) != k:
            bad.append(("length", n, lam, mu))
        if any(m < 0 for m in mu):
            bad.append(("negative", n, lam, mu))
        if sum(mu) != n - k * k:
            bad.append(("weight", n, lam, mu))
        if unstair(mu) != lam:
            bad.append(("inverse", n, lam, mu))
print("gap partitions checked, n <= %d : %d" % (NMAX, checked))
print("violations of order / length / nonneg / weight n-k^2 / inverse:", bad)
print("max length seen:", max(len(lam) for n in range(NMAX + 1) for lam in partitions_gap(n)))
print("largest k^2 (deepest staircase) is at n =", max(
    range(NMAX + 1),
    key=lambda n: max((len(l) ** 2 for l in partitions_gap(n)), default=0)))

# (2) positivity alone does not give the order law.  Lean's `subStair` subtracts in
# `Nat`, i.e. it truncates; on a Pos+Gap partition the truncation never bites (checked
# above: no "negative" violation).  `[1,3]` is not a gap partition, so the two
# conventions differ there -- neither image is weakly decreasing.
lam = (1, 3)                     # ascending, so not a partition under the contract
print("stair(1,3) =", stair(lam), "(integer convention)",
      "| Nat convention:", tuple(max(0, m) for m in stair(lam)))
print("weakly decreasing under either convention:",
      weak_dec(stair(lam)), weak_dec(tuple(max(0, m) for m in stair(lam))))
lam = (3, 1)                     # a genuine gap partition of 4: padding witness
print("stair(3,1) =", stair(lam), "weakly decreasing:", weak_dec(stair(lam)))
lam = (5, 3, 1)                  # the Lean witness `witness_padding`
print("stair(5,3,1) =", stair(lam), "all zero after the first entry:",
      set(stair(lam)[1:]) == {0})

# (3) zero padding carries the length
print("unstair(1)   =", unstair((1,)), "   unstair(1,0) =", unstair((1, 0)))
print("dropping the trailing zero changes the object:", unstair((1,)) != unstair((1, 0)))

sys.exit(1 if bad else 0)
