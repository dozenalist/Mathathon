"""Explicit free-label sector words: the 5-block construction.

Palettes (pairs of the five non-free labels), indexed by i in Z/5:
        p_0 = {1,3}, p_1 = {1,4}, p_2 = {2,4}, p_3 = {2,5}, p_4 = {3,5}
with  p_i cap p_j = empty  <=>  j - i = +-2 (mod 5).
(The pattern generalises: any assignment of the five labels to the ten slots of five pairs
isomorphic to this one; this is the '5-cycle in the disjointness graph'.)

Word: period P = 2m, five consecutive blocks of lengths L_0..L_4 with sum 2m carrying
p_0..p_4 in order, repeated three times around the circle of 6m sectors.  For j in block i
the offsets o with |o - m| <= K land in blocks i+2 and i+3 iff

        L_i + L_{i+1} <= m - K        and        L_i + L_{i+4} <= m - K + 1,

which for K = floor(m/5) has solutions for every m (searched below).  For 5 | m the uniform
choice L_i = 2m/5 works exactly.
"""
from itertools import product
import sector_csp as S


def palette_structure():
    p = [frozenset({1, 3}), frozenset({1, 4}), frozenset({2, 4}), frozenset({2, 5}), frozenset({3, 5})]
    # sanity: p_i cap p_j empty iff j - i = +-2 mod 5
    for i in range(5):
        for j in range(5):
            dj = (j - i) % 5
            assert (not (p[i] & p[j])) == (dj in (2, 3)), (i, j)
    assert all(len(q) in (2, 3) for q in p)
    return p


P = palette_structure()


def build(lengths):
    """The cyclic word of length 6m (period 2m, three repetitions)."""
    P0 = sum(lengths)
    word = []
    for rep in range(3):
        for i, L in enumerate(lengths):
            word.extend([P[i]] * L)
    return word


def check(m, K, lengths=None, verbose=False):
    if lengths is None:
        if m % 5 == 0:
            lengths = [2 * m // 5] * 5
        else:
            return None
    if sum(lengths) != 2 * m:
        return False
    w = build(lengths)
    if len(w) != 6 * m:
        return False
    return S.check_word(w, S.offsets(m, K)), w


def find_lengths(m, K):
    """Search block lengths near 2m/5 (a window of +-4) for the two adjacency conditions."""
    M = m - K
    base = 2 * m // 5
    window = range(max(1, base - 4), base + 6)
    for L0 in window:
        for L1 in window:
            if L0 + L1 > M:
                continue
            for L2 in window:
                if L1 + L2 > M:
                    continue
                for L3 in window:
                    if L2 + L3 > M:
                        continue
                    L4 = 2 * m - L0 - L1 - L2 - L3
                    if L4 < 1 or L4 > M:
                        continue
                    if L3 + L4 > M or L4 + L0 > M:
                        continue
                    return [L0, L1, L2, L3, L4]
    return None


if __name__ == "__main__":
    print("uniform construction for 5 | m, K = m/5:")
    for m in (5, 10, 15, 20, 25, 50, 100, 200):
        ok, w = check(m, m // 5)
        print(f"  m={m:4d} K={m//5:3d}: {ok}  sizes={sorted({len(x) for x in w})}")
    print()
    print("general m, K = floor(m/5): searched block lengths")
    bad = []
    for m in range(5, 301):
        K = m // 5
        Ls = find_lengths(m, K)
        if Ls is None:
            bad.append(m)
            continue
        ok, w = check(m, K, Ls)
        if not ok:
            bad.append((m, Ls))
    print("  m in 5..300:", "all constructions verified" if not bad else f"failures {bad}")
    print()
    print("non-vacuity: K = 0 (only (5.7)) is satisfiable for every m; witnesses from the solver")
    for m in (2, 3, 4, 7, 11, 12):
        w = S.solve(6 * m, S.offsets(m, 0))
        ok = w is not None and S.check_word(w, S.offsets(m, 0))
        print(f"  m={m:3d} K=0: witness={ok}  word={[sorted(x) for x in w][:8] if w else None}")
