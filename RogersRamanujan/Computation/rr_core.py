"""RR127 canonical contract (owner: Main, checkpoint 1).

Representation convention (frozen):
  A partition is a *descending tuple of positive integers*.
  The empty tuple () is the unique partition of 0.
  A_n = {p : weight(p) = n, every part % 5 in {1, 4}}         (multiplicity allowed)
  D_n = {p : weight(p) = n, p_i >= p_{i+1} + 2 for all i}     (smallest part 1 allowed)

Every entry point in this module rejects invalid input explicitly (ValueError),
never silently sorting, deduplicating or deleting non-positive parts.

Auxiliary parameters / conventions, all documented at their definition:
  * enumerate_* return a list in strictly decreasing lexicographic order.
  * staircase(lambda) returns (k, mu) with k = len(lambda) retained as data even
    when mu has trailing zeros.  mu is a weakly decreasing nonnegative vector.
  * T returns a partition; Tinv takes (k, b).
"""

from functools import lru_cache

MOD = 5
RESIDUES = (1, 4)


# --------------------------------------------------------------------------
# validators
# --------------------------------------------------------------------------
def is_partition(p):
    """True iff p is a tuple of positive ints in non-increasing order."""
    if not isinstance(p, tuple):
        return False
    for x in p:
        if not isinstance(x, int) or isinstance(x, bool) or x <= 0:
            return False
    return all(p[i] >= p[i + 1] for i in range(len(p) - 1))


def _require_partition(p, who):
    if not is_partition(p):
        raise ValueError("%s: not a partition (need descending tuple of positive ints): %r"
                         % (who, p))


def weight(p):
    """Exact integer sum; validates first."""
    _require_partition(p, "weight")
    return sum(p)


def is_residue(p):
    """Membership in A_n (n = weight(p))."""
    return is_partition(p) and all(x % MOD in RESIDUES for x in p)


def is_gap(p):
    """Membership in D_n (n = weight(p))."""
    return is_partition(p) and all(p[i] >= p[i + 1] + 2 for i in range(len(p) - 1))


def family(p):
    """(in A, in D) as a pair of booleans, for intersection studies."""
    return (is_residue(p), is_gap(p))


# --------------------------------------------------------------------------
# enumeration: direct (structural) method
# --------------------------------------------------------------------------
def enumerate_residue(n):
    """All of A_n, strictly decreasing lexicographic order.  Direct method."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("enumerate_residue: n must be a nonnegative int")
    allowed = [x for x in range(1, n + 1) if x % MOD in RESIDUES]
    out = []

    def rec(remaining, cap, acc):
        if remaining == 0:
            out.append(tuple(acc))
            return
        for x in allowed:
            if x > min(cap, remaining):
                continue
            acc.append(x)
            rec(remaining - x, x, acc)
            acc.pop()

    rec(n, n, [])
    out.sort(reverse=True)
    return out


def enumerate_gap(n):
    """All of D_n, strictly decreasing lexicographic order.  Direct method."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("enumerate_gap: n must be a nonnegative int")
    out = []

    def rec(remaining, cap, acc):
        if remaining == 0:
            out.append(tuple(acc))
            return
        for x in range(min(cap, remaining), 0, -1):
            acc.append(x)
            rec(remaining - x, x - 2, acc)
            acc.pop()

    rec(n, n, [])
    out.sort(reverse=True)
    return out


# --------------------------------------------------------------------------
# enumeration: dynamic programming (independent of the recursion above)
# --------------------------------------------------------------------------
@lru_cache(maxsize=None)
def _coin(n, i):
    """Unbounded coin change over allowed parts, using only the first i of them."""
    allowed = [x for x in range(1, n + 1) if x % MOD in RESIDUES]
    if n == 0:
        return 1
    if n < 0 or i == 0:
        return 0
    return _coin(n, i - 1) + _coin(n - allowed[i - 1], i)


def count_residue_dp(n):
    """|A_n| by unbounded coin change on the allowed parts <= n."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("count_residue_dp: n must be a nonnegative int")
    allowed = [x for x in range(1, n + 1) if x % MOD in RESIDUES]
    tbl = [0] * (n + 1)
    tbl[0] = 1
    for c in allowed:
        for s in range(c, n + 1):
            tbl[s] += tbl[s - c]
    return tbl[n]


@lru_cache(maxsize=None)
def _gap(n, m):
    """d(n,m): weight n, parts <= m, gaps >= 2.

    d(0,m) = 1 for every m (including m <= 0): the empty partition.
    d(n,m) = 0 for n > 0 and m <= 0.
    d(n,m) = d(n,m-1) + d(n-m,m-2) for m >= 1.
    """
    if n == 0:
        return 1
    if n < 0 or m <= 0:
        return 0
    return _gap(n, m - 1) + _gap(n - m, m - 2)


def count_gap_dp(n):
    """|D_n| by the stranger-free recurrence with an explicit part cap."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("count_gap_dp: n must be a nonnegative int")
    return _gap(n, n)


# --------------------------------------------------------------------------
# established reductions: staircase and shift T
# --------------------------------------------------------------------------
def staircase(lam):
    """lambda in D_n of length k  |->  (k, mu), mu_i = lambda_i - (2(k-i)+1).

    mu is weakly decreasing, nonnegative, of length exactly k, of weight
    weight(lambda) - k^2.  k is returned separately so trailing zeros are data.
    """
    _require_partition(lam, "staircase")
    if not is_gap(lam):
        raise ValueError("staircase: input not in D_n: %r" % (lam,))
    k = len(lam)
    mu = tuple(lam[i] - (2 * (k - (i + 1)) + 1) for i in range(k))
    assert all(m >= 0 for m in mu), "gap condition must force mu >= 0"
    return (k, mu)


def unstaircase(k, mu):
    """(k, mu) |-> lambda, lambda_i = mu_i + (2(k-i)+1).  Inverse of staircase."""
    if not isinstance(k, int) or k < 0:
        raise ValueError("unstaircase: k must be a nonnegative int")
    if not isinstance(mu, tuple) or len(mu) != k:
        raise ValueError("unstaircase: mu must be a tuple of length k")
    for x in mu:
        if not isinstance(x, int) or isinstance(x, bool) or x < 0:
            raise ValueError("unstaircase: mu entries must be nonnegative ints")
    if any(mu[i] < mu[i + 1] for i in range(k - 1)):
        raise ValueError("unstaircase: mu must be weakly decreasing")
    return tuple(mu[i] + (2 * (k - (i + 1)) + 1) for i in range(k))


def T(lam):
    """Same-weight bijection D_n -> B_n = {length k, smallest part >= k}.

    T(lambda)_i = lambda_i - k + 2i - 1, 1-based i; equals mu_i + k.
    """
    _require_partition(lam, "T")
    if not is_gap(lam):
        raise ValueError("T: input not in D_n: %r" % (lam,))
    k = len(lam)
    b = tuple(lam[i] - k + 2 * (i + 1) - 1 for i in range(k))
    assert all(b[i] >= k for i in range(k)) if k else True
    assert sum(b) == sum(lam)
    return b


def Tinv(b):
    """Inverse of T: lambda_i = b_i + k - 2i + 1.  Requires b_i >= k."""
    _require_partition(b, "Tinv")
    k = len(b)
    if k == 0:
        return ()
    if any(b[i] < k for i in range(k)):
        raise ValueError("Tinv: input not in B_n (smallest part must be >= length): %r" % (b,))
    return tuple(b[i] + k - 2 * (i + 1) + 1 for i in range(k))


# --------------------------------------------------------------------------
# reference counts, for cross-checking only (OEIS A003114)
# --------------------------------------------------------------------------
A003114 = [1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 9, 10, 12, 14, 17, 19, 23,
           26, 31, 35, 41, 46, 55, 62, 71, 82, 94, 106, 121]


if __name__ == "__main__":
    for n in range(7):
        print(n, enumerate_residue(n), enumerate_gap(n))
    print("counts:")
    for n in range(31):
        a, d = len(enumerate_residue(n)), len(enumerate_gap(n))
        a2, d2 = count_residue_dp(n), count_gap_dp(n)
        flag = "OK" if a == d == a2 == d2 == A003114[n] else "MISMATCH"
        print(n, a, d, a2, d2, A003114[n], flag)
