"""Uniform pairs-only free-label sector word for every m >= 6.

W on Z_{2m}, repeated 3 times on Z_{6m} (2m | 6m), with the five blocks

    A = {1,3} on [0, m-3)      (m-3 >= 3 positions)
    B = {1,4} on [m-3, m-1)    (2)
    C = {2,4} on [m-1, 2m-4)   (m-3 >= 3)
    D = {2,5} on [2m-4, 2m-2)  (2)
    E = {3,5} on [2m-2, 2m)    (2)

Disjointness (perp) on the six admissible pairs avoiding 0 is checked below; it is
the 5-cycle A - C - E - B - D - A.  The required condition on Z_{6m} is
   W(i) perp W(i+delta)  for delta in {+-(m-1), +-m, +-(m+1)} mod 6m,
which since W has period 2m reduces to the same condition mod 2m, i.e.
delta in {m-1, m, m+1} (because -(m-1) = m+1 and -m = m mod 2m).
"""
from itertools import combinations
import sys

K = 6
EDGES = [frozenset((j, (j + 1) % 6)) for j in range(6)]
A, B, C, D, E = (frozenset({1, 3}), frozenset({1, 4}), frozenset({2, 4}),
                 frozenset({2, 5}), frozenset({3, 5}))


def admissible(S):
    S = frozenset(S)
    return 1 <= len(S) <= 3 and not any(S <= e for e in EDGES)


def word2m(m):
    assert m >= 6
    W = [None] * (2 * m)
    for i in range(0, m - 3):
        W[i] = A
    for i in range(m - 3, m - 1):
        W[i] = B
    for i in range(m - 1, 2 * m - 4):
        W[i] = C
    for i in range(2 * m - 4, 2 * m - 2):
        W[i] = D
    for i in range(2 * m - 2, 2 * m):
        W[i] = E
    assert all(v is not None for v in W)
    return W


def word6m(m):
    W = word2m(m)
    return [W[i % (2 * m)] for i in range(6 * m)]


def check_direct(m):
    """exact integer check of the 6m-sector word."""
    W = word6m(m)
    n = 6 * m
    offs = sorted({(m + k) % n for k in (-1, 0, 1)} | {(-m + k) % n for k in (-1, 0, 1)})
    errs = []
    for i in range(n):
        if not admissible(W[i]) or 0 in W[i]:
            errs.append(("value", i))
    for i in range(n):
        for j in offs:
            if W[i] & W[(i + j) % n]:
                errs.append(("transport", i, j, sorted(W[i]), sorted(W[(i + j) % n])))
    return errs, offs


def check_2m(m):
    W = word2m(m)
    errs = []
    for i in range(2 * m):
        for d in (m - 1, m, m + 1):
            if W[i] & W[(i + d) % (2 * m)]:
                errs.append((i, d, sorted(W[i]), sorted(W[(i + d) % (2 * m)])))
    return errs


if __name__ == "__main__":
    pairs = [frozenset(c) for c in combinations(range(1, 6), 2) if admissible(c)]
    print("admissible pairs avoiding 0:", [sorted(p) for p in pairs])
    print("disjointness (5-cycle A-C-E-B-D-A):")
    for p in [A, B, C, D, E]:
        print("   ", sorted(p), "perp", [sorted(q) for q in [A, B, C, D, E] if not (p & q)])
    print()
    bad = []
    for m in range(6, 2001):
        e1, offs = check_direct(m)
        e2 = check_2m(m)
        if e1 or e2:
            bad.append((m, e1[:2], e2[:2]))
    print("direct 6m check + reduced 2m check, m = 6..2000:", "ALL OK" if not bad else bad[:5])
    # show the words
    for m in (6, 7, 9, 12):
        e, offs = check_direct(m)
        print(f"m={m}: n={6*m} offsets={offs} violations={len(e)}; 2m-word block lengths "
              f"A{m-3} B2 C{m-3} D2 E2")
