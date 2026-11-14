"""Final decision procedure for the pointwise section-8 system at a cycle centre.

For each cycle length ell and each colour count k, this decides, for every one of
the 6^ell achievable orbit sign-tuples (all row assignments of cyclic 3-intervals
of Z/6), whether the palette system of that tuple is satisfiable, and whether two
satisfiable tuples can be consecutive cells of one ray configuration.

Constraints (see proof.md for the derivation and for the paper references):

  (P)   1 <= |P_p| <= k-3                              [Prop 5.6 at k colours]
  (6.2) P_p is not contained in an edge of the cycle   [Lemma 6.2]
  (8.1) P_p meets O_p and I_p                          [Lemma 8.1]
  (5.7) P_p cap P_{p+1} = empty                        [Corollary 5.4]
  (5.2) P_p union P_{p'} != [k] for p'-p in {1,2,4,5}  [(5.2); parallel pairs excluded]
  (SA)  i in no P_p                                    [Lemma 1, typical centre]
  (MU)  P_p union P_{p+2} != [k] minus {i}             [Lemma 4.3 + (5.2), typical centre]
"""

from itertools import combinations
import s8
from rows import achievable

FULL = None


def domain(oc, ell, k, w2sup, sa, dtab):
    key = (frozenset(oc[0]), frozenset(oc[1]), ell, k, w2sup, sa)
    if key not in dtab:
        lst = set()
        for P in s8.palettes_for(oc, ell, k, -1, w2sup):
            if sa is not None and sa in P:
                continue
            lst.add(sum(1 << x for x in P))
        dtab[key] = sorted(lst)
    return dtab[key]


def solve(doms, k, i):
    full = (1 << k) - 1
    assign = {}

    def ok(p, m):
        for q, mq in assign.items():
            d = (q - p) % 6
            if d == 0 or d == 3:
                continue
            u = m | mq
            if u == full:
                return False
            if d in (1, 5):
                if m & mq:
                    return False
            elif i is not None and u == full ^ (1 << i):
                return False
        return True

    def bt(t):
        if t == 6:
            return True
        for m in doms[t]:
            if ok(t, m):
                assign[t] = m
                if bt(t + 1):
                    return True
                del assign[t]
        return False

    return bt(0)


def analyse(ell, k, w2sup, use_sa, cover_check=True, verbose=True):
    dtab = {}
    rows = list(achievable(ell))
    labels = list(range(k)) if use_sa else [None]
    stat = {}
    sat = set()
    coverings = set()
    for i in labels:
        for choice, S in rows:
            ocs = tuple(s8.allowed_sets(s, ell, k) for s in S)
            if any(not oc[0] or not oc[1] for oc in ocs):
                stat['L81'] = stat.get('L81', 0) + 1
                continue
            doms = [domain(oc, ell, k, w2sup, i, dtab) for oc in ocs]
            ok = solve(doms, k, i)
            stat['OK' if ok else 'CSP'] = stat.get('OK' if ok else 'CSP', 0) + 1
            if ok:
                sat.add((i, choice))
                if cover_check and i is None:
                    coverings.add(choice)
    out = dict(ell=ell, k=k, w2=w2sup, sa=use_sa, stat=stat, nsat=len(sat))

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
    out['pairs'] = pairs
    out['sat'] = sat
    if verbose:
        print(f"ell={ell} k={k} |P|<={w2sup} SA={use_sa}: {stat}")
        print(f"   SAT (label,row) pairs: {len(sat)}; consecutive-cell-compatible pairs: {len(pairs)}")
    return out


if __name__ == '__main__':
    import sys, json
    res = {}
    for (ell, k, w2) in [(5, 5, 2), (6, 6, 3)]:
        for sa in (False, True):
            r = analyse(ell, k, w2, sa)
            res[f"{ell}_{k}_{w2}_{sa}"] = dict(stat=r['stat'], nsat=r['nsat'], pairs=len(r['pairs']))
    print(json.dumps(res, indent=1))
