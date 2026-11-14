#!/usr/bin/env python3
"""
RR127 / D3: Bressoud-Zeilberger (1982) style involution psi on signed states

    X(n) = { (j, lam) : j in Z, lam a partition (descending tuple of positive
             integers),  |lam| + j(5j-1)/2 = n }.

psi is the map whose rules are quoted in the task contract.  It is defined on

    Dom(n) = X(n) \\ F(n),      F(n) = { (0, lam) : lam in A_n }

where A_n = partitions of n all of whose parts are == 1 or 4 (mod 5).
Its rules are undefined (they demand a part of size -2) exactly on F(n).

Everything is exact integer arithmetic, python3 stdlib only.
Partitions are canonical descending tuples; trailing zeros are NOT kept
(the contract's "keep k for trailing zeros" belongs to the staircase
reduction, which this map does not use).

Conventions used below (documented decisions, see README.md):

  parts mod 5:
     t0 = #{parts p of lam : p == 0 mod 5}
     m_r = max{parts p of lam : p == r mod 5},  0 if there is none, r=0,2,3
     N  = 5*t0 + 5*j - 3        (the "candidate" that Case I inserts)

  Case I    iff (t0 + j > 0) or (m2 > 0)
    I(a)    iff N >= m2          <-- equality is taken by I(a)   [decision 1]
    I(b)    iff N <  m2
  Case II   otherwise, i.e. (t0 + j <= 0) and (m2 == 0)
    II(a)   iff m3 + 5j - 3 >= m0 <-- equality taken by II(a)    [decision 2]
    II(b)   iff m3 + 5j - 3 <  m0
  In II(a) the value m3+5j-3 may be 0; then the part is deleted  [decision 3]
"""

# ----------------------------------------------------------------------------
# basic helpers
# ----------------------------------------------------------------------------


def pent(j):
    """j(5j-1)/2, the 5-pentagonal numbers: 0,2,3,9,11,21,24,... for j=0,1,-1,2,-2,3,-3"""
    return j * (5 * j - 1) // 2


def weight(state):
    j, lam = state
    return sum(lam) + pent(j)


def parts_mod(lam, r):
    return [p for p in lam if p % 5 == r]


def cnt(lam, r):
    return len(parts_mod(lam, r))


def mx(lam, r):
    ps = parts_mod(lam, r)
    return max(ps) if ps else 0


def remove_one(lst, v):
    """remove a single copy of v from list lst (in place, returns lst)"""
    lst.remove(v)
    return lst


def canon(lst):
    out = [p for p in lst if p > 0]
    out.sort(reverse=True)
    return tuple(out)


def partitions(m, cap=None):
    """all partitions of m as descending tuples, parts <= cap (cap None: parts <= m).
    Iterative generator; m may be 0 -> yields ()."""
    if m < 0:
        return
    if m == 0:
        yield ()
        return
    if cap is None or cap > m:
        cap = m
    # standard recursion, written iteratively over the largest part
    for big in range(min(cap, m), 0, -1):
        rest = m - big
        if rest == 0:
            yield (big,)
        else:
            for tail in partitions(rest, min(big, rest)):
                yield (big,) + tail


def states(n):
    """all (j, lam) with |lam| + j(5j-1)/2 = n, j in Z, lam a partition."""
    out = []
    j = 0
    while pent(j) <= n:
        m = n - pent(j)
        for lam in partitions(m):
            out.append((j, lam))
        j += 1
    j = -1
    while pent(j) <= n:
        m = n - pent(j)
        for lam in partitions(m):
            out.append((j, lam))
        j -= 1
    return out


# ----------------------------------------------------------------------------
# the map psi
# ----------------------------------------------------------------------------

INVALID = "INVALID"


def psi(state, tie_I="a", tie_II="a", tie_zero3="delete"):
    """Apply the contract rules.  Returns the new state, or the string INVALID
    if the rules would produce a non-positive part (i.e. the state is one of
    the excluded fixed points).  Never raises on a genuine state of X(n).

    tie_I     : "a" or "b"  -- which branch owns the equality N == m2
    tie_II    : "a" or "b"  -- which branch owns the equality m3+5j-3 == m0
    tie_zero3 : "delete"    -- m3+5j-3 == 0 is read as "the part disappears" (IIa)
                "b"         -- that case is instead handed to II(b)
    """
    j, lam = state
    lam = tuple(lam)
    t0 = cnt(lam, 0)
    m0 = mx(lam, 0)
    m2 = mx(lam, 2)
    m3 = mx(lam, 3)
    N = 5 * t0 + 5 * j - 3
    zero3 = (m3 + 5 * j - 3 == 0)

    if (t0 + j > 0) or (m2 > 0):
        # ------------------------------------------------------------------
        # Case I
        # ------------------------------------------------------------------
        take_a = (N >= m2) if tie_I == "a" else (N > m2)
        if take_a:
            # I(a): -5 from each part ==0 mod 5 (dropping 5s), insert N, j-=1
            new = [p - 5 for p in lam if p % 5 == 0 and p > 5]
            new += [p for p in lam if p % 5 != 0]
            if N > 0:
                new.append(N)
            elif N == 0:
                return INVALID          # cannot happen on the domain
            else:
                return INVALID          # cannot happen on the domain
            return (j - 1, canon(new))
        else:
            # I(b): delete one copy of m2, +5 to each part ==0 mod 5,
            #       create (m2 - 5j - 2 - 5t0)/5 parts 5, j += 1
            new = list(lam)
            remove_one(new, m2)
            new = [p + 5 if p % 5 == 0 else p for p in new]
            num = m2 - 5 * j - 2 - 5 * t0
            if num % 5 != 0:            # cannot happen: m2 == 2 mod 5
                return INVALID
            k = num // 5
            if k < 0:                   # "a negative number of parts 5"
                return INVALID
            new += [5] * k
            return (j + 1, canon(new))
    else:
        # ------------------------------------------------------------------
        # Case II:  t0 + j <= 0  and  m2 == 0
        # ------------------------------------------------------------------
        if zero3 and tie_zero3 == "b":
            take_a = False
        elif tie_II == "a":
            take_a = (m3 + 5 * j - 3 >= m0)
        else:
            take_a = (m3 + 5 * j - 3 > m0)
        if take_a:
            # II(a): replace m3 by m3+5j-3, j -= 1
            val = m3 + 5 * j - 3
            new = list(lam)
            if m3 > 0:
                remove_one(new, m3)
            if val > 0:
                new.append(val)
            elif val < 0:
                return INVALID          # cannot happen on the domain
            # val == 0: the part vanishes (decision 3)
            return (j - 1, canon(new))
        else:
            # II(b): replace m0 by m0-5j-2  (m0 = 0 -> create a part -5j-2), j += 1
            val = m0 - 5 * j - 2
            if val <= 0:
                return INVALID          # exactly the excluded fixed points
            new = list(lam)
            if m0 > 0:
                remove_one(new, m0)
            new.append(val)
            return (j + 1, canon(new))


# ----------------------------------------------------------------------------
# independent counting of A_n and D_n  (only used to check the identity)
# ----------------------------------------------------------------------------


def count_A(N):
    """|A_n| for n=0..N : unbounded coin change over parts == 1,4 mod 5."""
    c = [0] * (N + 1)
    c[0] = 1
    p = 1
    while p <= N:
        for n in range(p, N + 1):
            c[n] += c[n - p]
        p += 1
        while p % 5 not in (1, 4):
            p += 1
    return c


def count_D(N):
    """|D_n| for n=0..N : partitions of n with all adjacent gaps >= 2.

    f[n][k] = # partitions of n with gaps >= 2 and all parts <= k.
    Removing the largest part k:  f[n][k] = f[n][k-1] + f[n-k][k-2],
    with f[0][k] = 1 (empty partition) and f[n][k] = 0 for n>0, k<1.
    """
    def f_get(f, m, k):
        if m == 0:
            return 1
        if k < 1:
            return 0
        return f[m][k]

    f = [[0] * (N + 1) for _ in range(N + 1)]
    for n in range(N + 1):
        for k in range(N + 1):
            if n == 0:
                f[n][k] = 1
            elif k < 1:
                f[n][k] = 0
            elif k > n:
                f[n][k] = f[n][k - 1]
            else:
                f[n][k] = f[n][k - 1] + f_get(f, n - k, k - 2)
    return [f[n][N] for n in range(N + 1)]


def count_D_brute(N):
    """|D_n| by direct generation (independent of the DP above)."""
    out = [0] * (N + 1)
    out[0] = 1
    for n in range(1, N + 1):
        c = 0
        for lam in partitions(n):
            ok = all(lam[i] >= lam[i + 1] + 2 for i in range(len(lam) - 1))
            if ok:
                c += 1
        out[n] = c
    return out


def count_A_brute(N):
    """|A_n| by direct generation."""
    out = [0] * (N + 1)
    out[0] = 1
    for n in range(1, N + 1):
        c = 0
        for lam in partitions(n):
            if all(p % 5 in (1, 4) for p in lam):
                c += 1
        out[n] = c
    return out


def is_A(lam):
    return all(p % 5 in (1, 4) for p in lam)
