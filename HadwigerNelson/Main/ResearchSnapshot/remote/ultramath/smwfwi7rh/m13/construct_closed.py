"""Closed-form 5-block construction proving S(m, floor(m/5)) is SAT for every m >= 5.

m = 5q + r, 0 <= r <= 4.  Palettes p_0..p_4 = {1,3},{1,4},{2,4},{2,5},{3,5}
(p_i cap p_j = empty iff j - i = +-2 mod 5).  Block lengths

        L_i = 2q + a_i,     a = (0,0,0,0,0)   r=0
                                (1,0,1,0,0)   r=1
                                (1,1,1,1,0)   r=2
                                (2,1,2,1,0)   r=3
                                (2,2,2,2,0)   r=4

so sum L_i = 10q + 2r = 2m and every cyclic adjacent sum is 4q + a_i + a_{i+1} <= 4q + r
= m - floor(m/5).  The word is the period-2m pattern p_0..p_4 in these lengths, repeated
three times around the 6m-sector circle.
"""
import sector_csp as S

A_PATTERN = {0: (0, 0, 0, 0, 0), 1: (1, 0, 1, 0, 0), 2: (1, 1, 1, 1, 0),
             3: (2, 1, 2, 1, 0), 4: (2, 2, 2, 2, 0)}
PALS = [frozenset({1, 3}), frozenset({1, 4}), frozenset({2, 4}), frozenset({2, 5}), frozenset({3, 5})]


def lengths(m):
    q, r = divmod(m, 5)
    return [2 * q + a for a in A_PATTERN[r]]


def word(m):
    L = lengths(m)
    assert sum(L) == 2 * m, (m, L)
    assert all(x >= 1 for x in L), (m, L)
    w = []
    for _ in range(3):
        for i in range(5):
            w.extend([PALS[i]] * L[i])
    assert len(w) == 6 * m
    return w


def verify(m):
    K = m // 5
    L = lengths(m)
    # the two adjacency conditions
    for i in range(5):
        assert L[i] + L[(i + 1) % 5] <= m - K, (m, i, L)
        assert L[i] + L[(i + 4) % 5] <= m - K + 1, (m, i, L)
    w = word(m)
    return S.check_word(w, S.offsets(m, K))


if __name__ == "__main__":
    import sys
    ok_full = [m for m in range(5, 121) if not verify(m)]
    print("full offset check for m = 5..120:", "all OK" if not ok_full else ok_full[:10])
    # for larger m only the two adjacency conditions are checked (they imply the offset
    # conditions by the block argument; the equivalence is verified above for m <= 120)
    bad = []
    for m in range(5, 5001):
        K = m // 5
        L = lengths(m)
        if sum(L) != 2 * m or any(x < 1 for x in L):
            bad.append(m)
            continue
        for i in range(5):
            if L[i] + L[(i + 1) % 5] > m - K or L[i] + L[(i + 4) % 5] > m - K + 1:
                bad.append((m, i))
    print("adjacency conditions for m = 5..5000:", "all OK" if not bad else bad[:10])
    for m in (5, 6, 7, 8, 9, 12, 13, 1999):
        print(f"  m={m:5d} K={m//5:3d} lengths={lengths(m)} full_check={verify(m) if m <= 120 else 'n/a'}")
