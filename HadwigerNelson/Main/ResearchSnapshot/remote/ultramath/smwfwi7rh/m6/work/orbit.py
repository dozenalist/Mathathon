"""Exact decision of the single-centre orbit system at a cycle centre, over all
pattern tuples satisfying the antipodal law S_{p+3} = [ell] \\ S_p.

At a cyclic centre x with a simple cycle of length ell, the ray v_j (j < ell) gives
the open semicircle I_j = {e : e.v_j > 0}, and sigma_j(e) = 1 on I_j.  The six
orbit directions R^p e are equally spaced, so R^{p+3} e is the antipode of R^p e;
an open semicircle contains exactly one of an antipodal pair, hence

    (A)  sigma_j(R^{p+3} e) = -sigma_j(R^p e),  i.e.  S_{p+3} = [ell] \\ S_p,

and therefore (O,I)_{p+3} = (I,O)_p.

Since the demand (8.1) "hit O and hit I" is symmetric in O and I, the domain at
position p+3 equals the domain at position p.  So the orbit system is satisfiable
at e exactly when the 3-partite disjointness graph on D_0 u D_1 u D_2 contains a
closed walk  D_0 - D_1 - D_2 - D_0 - D_1 - D_2 - D_0.  That is decided exactly by
the transfer computation below.
"""

from itertools import combinations
import s8

DISJ = None


def _build_disj(k):
    global DISJ
    DISJ = [0] * (1 << k)
    for m in range(1 << k):
        bits = 0
        for m2 in range(1 << k):
            if m & m2 == 0:
                bits |= 1 << m2
        DISJ[m] = bits


def domain_table(ell, k, w2sup):
    """(O,I) -> {i : domain, a list of palette masks} for admissible pairs."""
    out = {}
    for r in range(ell + 1):
        for S in combinations(range(ell), r):
            oc = s8.allowed_sets(frozenset(S), ell, k)
            O, I = oc
            if not O or not I or oc in out:
                continue
            out[oc] = {i: [sum(1 << x for x in P)
                           for P in s8.palettes_for(oc, ell, k, i, w2sup)]
                       for i in range(k)}
    return out


def walk_exists(d0, d1, d2):
    """Is there a closed walk d0-d1-d2-d0-d1-d2-d0 in the disjointness graph?"""
    if not d0 or not d1 or not d2:
        return False
    m1, m2 = set(d1), set(d2)
    R = {}
    for a in d0:
        s1 = [b for b in m1 if a & b == 0]
        if not s1:
            continue
        acc = 0
        for b in s1:
            acc |= DISJ[b]
        s2 = [c for c in m2 if (acc >> c) & 1]
        if not s2:
            continue
        acc2 = 0
        for c in s2:
            acc2 |= DISJ[c]
        R[a] = [x for x in d0 if (acc2 >> x) & 1]
    for a, outs in R.items():
        for x in outs:
            if a in R.get(x, ()):
                return True
    return False


def dihedral(k):
    return [tuple((j + c) % k for j in range(k)) for c in range(k)] + \
           [tuple((c - j) % k for j in range(k)) for c in range(k)]


def census(ell, k, w2sup, verbose=True):
    _build_disj(k)
    table = domain_table(ell, k, w2sup)
    keys = sorted(table)
    grp = dihedral(k)
    img = {}
    for g in grp:
        for oc in keys:
            img[(g, oc)] = (frozenset(g[x] for x in oc[0]),
                            frozenset(g[x] for x in oc[1]))
    cache = {}
    sat, unsat = [], []
    for k0 in keys:
        for k1 in keys:
            for k2 in keys:
                best = None
                for g in grp:
                    tt = (img[(g, k0)], img[(g, k1)], img[(g, k2)])
                    for i in range(k):
                        key = (tt, i)
                        if best is None or key < best:
                            best = key
                if best in cache:
                    val = cache[best]
                else:
                    tt = best[0]
                    val = None
                    for i in range(k):
                        if walk_exists(table[tt[0]][i], table[tt[1]][i], table[tt[2]][i]):
                            val = i
                            break
                    cache[best] = val
                (sat if val is not None else unsat).append((k0, k1, k2))
    if verbose:
        print(f"ell={ell} k={k} |P|<={w2sup}: {len(keys)} admissible (O,I) pairs, "
              f"{len(keys)**3} triples -> SAT {len(sat)}, UNSAT {len(unsat)}")
    return keys, sat, unsat


if __name__ == '__main__':
    import sys
    ell, k, w2 = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    keys, sat, unsat = census(ell, k, w2)
    for t in sat[:8]:
        print("   SAT", [(sorted(a[0]), sorted(a[1])) for a in t])
