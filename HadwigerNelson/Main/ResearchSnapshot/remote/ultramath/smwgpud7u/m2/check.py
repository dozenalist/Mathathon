"""Exact (rational) checker for the three exclusion principles on six-cycle
common-interface direction data alpha_0..alpha_5 (angles in degrees mod 360).

Reduced form (proved by hand in proof.md):
  P1  (CC60)          : d(a_i,a_j) > 60      for every NON-adjacent index pair
  P2  (MC120)         : d(a_G) >= 120        for every G in MC_MIN
  P3  (EMPTY-RESIDUAL): d(a_G) >= 180        for every G in E_MIN
where d(S) = 360 - (largest circular gap of S) is the circular diameter.
"""
from fractions import Fraction as F
from itertools import combinations

E = [frozenset({i, (i + 1) % 6}) for i in range(6)]


def cov(G):
    s = set()
    for i in G:
        s |= E[i]
    return len(s)


def d(S):
    pts = sorted({F(x) % 360 for x in S})
    if len(pts) <= 1:
        return F(0)
    gaps = [pts[k + 1] - pts[k] for k in range(len(pts) - 1)]
    gaps.append(pts[0] + 360 - pts[-1])
    return 360 - max(gaps)


MC_MIN = [(0, 2, 4), (1, 3, 5)] + \
         [(i, (i + 1) % 6, (i + 3) % 6) for i in range(6)] + \
         [(i, (i + 1) % 6, (i + 4) % 6) for i in range(6)]
E_MIN = [(0, 2, 4), (1, 3, 5), (0, 1, 3, 4), (0, 2, 3, 5), (1, 2, 4, 5)]


def minimal_sets(thresh):
    """All inclusion-minimal G with cov(G) >= thresh (brute force, 64 subsets)."""
    out = []
    for r in range(1, 7):
        for G in combinations(range(6), r):
            if cov(G) >= thresh and all(cov(tuple(x for x in G if x != g)) < thresh
                                        for g in G):
                out.append(G)
    return out


def check(alpha, verbose=False):
    a = [F(x) for x in alpha]
    bad = []
    for i in range(6):
        for j in range(i + 1, 6):
            if (j - i) % 6 in (2, 3, 4) and d([a[i], a[j]]) <= 60:
                bad.append(('P1', i, j, d([a[i], a[j]])))
    for G in MC_MIN:
        if d([a[i] for i in G]) < 120:
            bad.append(('P2', G, d([a[i] for i in G])))
    for G in E_MIN:
        if d([a[i] for i in G]) < 180:
            bad.append(('P3', G, d([a[i] for i in G])))
    if verbose:
        for b in bad:
            print('   VIOLATION', b)
    return bad


if __name__ == '__main__':
    assert set(tuple(sorted(G)) for G in minimal_sets(5)) == \
           set(tuple(sorted(G)) for G in MC_MIN), 'MC minimal family mismatch'
    assert set(tuple(sorted(G)) for G in minimal_sets(6)) == \
           set(tuple(sorted(G)) for G in E_MIN), 'EMPTY minimal family mismatch'
    print('minimal G with cov>=5 :', sorted(minimal_sets(5)))
    print('minimal G with cov>=6 :', sorted(minimal_sets(6)))
    print('MC_MIN size', len(set(map(lambda g: tuple(sorted(g)), MC_MIN))))
    print('E_MIN  size', len(set(map(lambda g: tuple(sorted(g)), E_MIN))))
    tests = {
        'orbitA_core (0,0,120,120,240,240)': [0, 0, 120, 120, 240, 240],
        'orbitB_core (0,60,120,180,240,300)': [0, 60, 120, 180, 240, 300],
        '5dist CaseI  (0,0,120,150,210,240)': [0, 0, 120, 150, 210, 240],
        '5dist flat   (0,0,120,180,180,240)': [0, 0, 120, 180, 180, 240],
        '6dist        (0,119,179,239,299,359)': [0, 119, 179, 239, 299, 359],
    }
    for k, v in tests.items():
        print(('PASS ' if not check(v) else 'FAIL '), k)
