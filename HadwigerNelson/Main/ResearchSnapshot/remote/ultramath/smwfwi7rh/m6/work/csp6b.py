"""Exact decision of the six-position palette system at a cycle centre.

Constraints used -- all available at *every* centre, no typicality needed:

  (P)   palette bound     1 <= |P_p| <= k-3
  (6.2) P_p is not a subset of an edge of the cycle                 [Lemma 6.2]
  (8.1) P_p meets O_p and I_p                                      [Lemma 8.1]
  (5.7) P_p cap P_{p+1} = empty                                    [Cor 5.4]
  (5.2) P_p union P_{p'} != [k] for every pair of NON-PARALLEL orbit directions:
        if the union were [k], the sum x + R^p e + R^{p'} e would carry no colour.

Non-parallel pairs among the six orbit positions are those with p'-p = 1,2,4,5 mod 6.
Parity: p' - p = 0 (same) or 3 (antipodal) are parallel, so (5.2) does not apply.

Optional, and requiring the centre to be a density-one point of its own colour i:

  (SA)  i is in no P_p                                              [Lemma 1]
  (MU)  P_p union P_{p+2} != [k] \\ {i}   -- otherwise the sum x + R^p e + R^{p+2} e
        would have colour i and be at distance one from x.
"""

from itertools import combinations
import s8
import orbit
from rows import achievable

_DTAB = {}


def domain(oc, ell, k, w2sup, sa_label):
    key = (frozenset(oc), ell, k, w2sup, sa_label)
    if key not in _DTAB:
        lst = []
        for P in s8.palettes_for(oc, ell, k, -1, w2sup):   # -1: no label excluded
            if sa_label is not None and sa_label in P:
                continue
            lst.append(sum(1 << x for x in P))
        _DTAB[key] = sorted(set(lst))
    return _DTAB[key]


def solve6(doms, k, i):
    """Exact backtracking over the six orbit positions."""
    full = (1 << k) - 1
    assign = {}

    def ok(p, m):
        for q, mq in assign.items():
            d = (q - p) % 6
            if d == 0 or d == 3:
                continue
            u = m | mq
            if d in (1, 5):
                if m & mq:
                    return False
                if u == full:
                    return False
            else:                                  # d in (2,4)
                if u == full:
                    return False
                if i is not None and u == full ^ (1 << i):
                    return False
        return True

    def bt(t):
        if t == 6:
            return True
        p = t
        for m in doms[p]:
            if ok(p, m):
                assign[p] = m
                if bt(t + 1):
                    return True
                del assign[p]
        return False

    return bt(0)


def decide(ell, k, w2sup, use_sa, verbose=True):
    orbit._build_disj(k)
    stat = {}
    sat = set()
    labels = list(range(k)) if use_sa else [None]
    for i in labels:
        for choice, S in achievable(ell):
            ocs = tuple(s8.allowed_sets(s, ell, k) for s in S)
            if any(not oc[0] or not oc[1] for oc in ocs):
                stat['L81'] = stat.get('L81', 0) + 1
                continue
            doms = [domain(oc, ell, k, w2sup, i) for oc in ocs]
            st = 'OK' if solve6(doms, k, i) else 'CSP'
            stat[st] = stat.get(st, 0) + 1
            if st == 'OK':
                sat.add((i, choice))
    if verbose:
        print(f"ell={ell} k={k} |P|<={w2sup} SA={use_sa}: {stat}; SAT (label,row) pairs {len(sat)}")

    def slip(c1, c2):
        d = [j for j in range(ell) if c1[j] != c2[j]]
        if not d:
            return False
        ds = [(c2[j] - c1[j]) % 6 for j in d]
        return all(x == 1 for x in ds) or all(x == 5 for x in ds)

    groups = {}
    for (i, c) in sat:
        groups.setdefault(i, []).append(c)
    pairs = []
    for i, lst in groups.items():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                if slip(lst[a], lst[b]):
                    pairs.append((i, lst[a], lst[b]))
    if verbose:
        print(f"   slip-adjacent SAT pairs: {len(pairs)}")
        for p in pairs[:4]:
            print("     ", p)
    return stat, sat, pairs


if __name__ == '__main__':
    import sys
    ell, k, w2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    sa = len(sys.argv) > 4 and sys.argv[4] == 'sa'
    decide(ell, k, w2, sa)
