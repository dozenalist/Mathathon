"""Exact decision of the six-position palette system at a cycle centre.

Constraints used (all available at *every* centre, no typicality needed):

  (P)   palette bound     1 <= |P_p| <= k-3
  (6.2) P_p is not a subset of an edge of the cycle
  (8.1) P_p meets O_p and I_p
  (5.7) P_p cap P_{p+1} = empty                    (consecutive orbit positions)
  (5.2) P_p union P_{p'} != [k] for every pair of non-parallel orbit directions
        (if the union were all of [k], the sum x + R^p e + R^{p'} e would carry no
        colour at all, contradicting (5.2) on a positive-measure product set)

For four or more colours, (5.2) is a real constraint only between two ternary
palettes whose union is [k].  The non-parallel pairs among the six orbit positions
are exactly those with p' - p = 1,2,4,5 mod 6.

Optionally (SA): the centre's own colour i is in no palette (needs the centre to be a
density-one point of its own colour class).
"""

from itertools import combinations, product
import s8
import orbit


def domains(ell, k, w2sup, sa_label):
    out = {}
    for r in range(ell + 1):
        for S in combinations(range(ell), r):
            oc = s8.allowed_sets(frozenset(S), ell, k)
            if not oc[0] or not oc[1] or oc in out:
                continue
            out[oc] = [sum(1 << x for x in P)
                       for P in s8.palettes_for(oc, ell, k, sa_label, w2sup)
                       if sa_label is None or sa_label not in P]
    return out


def solve6(doms, k):
    """doms: list of 6 lists of masks, positions 0..5, with the period-3 domain
    pattern already applied by the caller.  Exact backtracking."""
    full = (1 << k) - 1
    order = [0, 1, 2, 3, 4, 5]
    assign = {}

    def ok(p, m):
        for q, mq in assign.items():
            d = (q - p) % 6
            if d in (1, 5):
                if m & mq:
                    return False
            elif d in (2, 4):
                if (m | mq) == full:
                    return False
        return True

    def bt(t):
        if t == 6:
            return True
        p = order[t]
        for m in doms[p]:
            if ok(p, m):
                assign[p] = m
                if bt(t + 1):
                    return True
                del assign[p]
        return False

    return bt(0)


def status(S, ell, k, w2sup, dtab, sa_label, cache):
    ocs = tuple(s8.allowed_sets(s, ell, k) for s in S)
    for oc in ocs:
        if not oc[0] or not oc[1]:
            return 'L81'
        if oc not in dtab:
            return 'L81'
    dm = (dtab[ocs[0]], dtab[ocs[1]], dtab[ocs[2]])
    key = (''.join(map(str, sorted(map(sorted, ocs)))), sa_label)
    if key in cache:
        return cache[key]
    doms = list(dm) + list(dm)
    val = 'OK' if solve6(doms, k) else 'CSP'
    cache[key] = val
    return val


def decide(ell, k, w2sup, use_sa, verbose=True):
    orbit._build_disj(k)
    cache = {}
    stats = {}
    sat = {}
    for sa_label in ([None] if not use_sa else range(k)):
        dtab = domains(ell, k, w2sup, sa_label)
        for choice, S in _rows(ell):
            st = status(S, ell, k, w2sup, dtab, sa_label, cache)
            stats[st] = stats.get(st, 0) + 1
            if st == 'OK':
                sat[(sa_label, choice)] = S
    if verbose:
        print(f"ell={ell} k={k} |P|<={w2sup} SA={use_sa}: {stats}; SAT rows {len(sat)}")
    # slippage adjacency among SAT states (same avoided label, or any if not use_sa)
    def slip(c1, c2):
        d = [j for j in range(ell) if c1[j] != c2[j]]
        if not d:
            return False
        ds = [(c2[j] - c1[j]) % 6 for j in d]
        return all(x == 1 for x in ds) or all(x == 5 for x in ds)

    groups = {}
    for (sa, choice) in sat:
        groups.setdefault(sa, []).append(choice)
    pairs = []
    for sa, lst in groups.items():
        for i, a in enumerate(lst):
            for b in lst[i + 1:]:
                if slip(a, b):
                    pairs.append((sa, a, b))
    if verbose:
        print(f"   slip-adjacent SAT pairs: {len(pairs)}")
        for p in pairs[:5]:
            print("     ", p)
    return stats, sat, pairs


from rows import achievable as _rows

if __name__ == '__main__':
    import sys
    ell, k, w2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    sa = sys.argv[4] == 'sa' if len(sys.argv) > 4 else True
    decide(ell, k, w2, sa)
