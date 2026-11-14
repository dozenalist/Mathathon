"""Implementation B: the same decision by a different algorithm (dynamic programming
over the six-position cycle instead of depth-first backtracking), plus a geometric
reconstruction of the cell walk from explicit rational rays.

Independence from implementation A:
  * the per-cell decision is a transfer computation (state = last two palettes),
    not a backtracking search;
  * the orbit tuples are generated from the sign sets directly, with the antipodal
    law imposed as a constraint (A derives it from the row model);
  * the cell walk is re-derived from explicit rational ray directions (geom.py).
"""
from itertools import combinations
import implA


def palettes(ell, k, i):
    out = []
    for size in range(1, min(3, k - 3) + 1):
        for c in combinations(range(k), size):
            m = 0
            for x in c:
                m |= 1 << x
            if i in c:
                continue
            if any(set(c) <= {j, (j + 1) % ell} for j in range(ell)):
                continue
            out.append((m, frozenset(c)))
    return out


def cell_sat_dp(ocs, i, k, ell):
    """Transfer computation on the 6-cycle.  No extras: baseline system only."""
    doms = []
    for (O, I) in ocs:
        d = [m for (m, s) in palettes(ell, k, i) if (s & O) and (s & I)]
        if not d:
            return False
        doms.append(d)
    # fix P_0 = v, propagate the set of feasible P_p
    for v in doms[0]:
        cur = {v}
        for p in range(1, 6):
            nxt = set()
            for a in cur:
                for b in doms[p]:
                    if not (a & b):
                        nxt.add(b)
            cur = nxt
            if not cur:
                break
        if not cur:
            continue
        for a in cur:
            if not (a & v):
                return True
    return False


def sign_sets(ell):
    """All tuples (S_0..S_5) of positive-edge sets satisfying the antipodal law."""
    N = 1 << ell
    fs = [frozenset(j for j in range(ell) if (m >> j) & 1) for m in range(N)]
    full = frozenset(range(ell))
    for m0 in range(N):
        S0, S3 = fs[m0], full - fs[m0]
        for m1 in range(N):
            S1, S4 = fs[m1], full - fs[m1]
            for m2 in range(N):
                S2, S5 = fs[m2], full - fs[m2]
                yield (S0, S1, S2, S3, S4, S5)


def decide(ell, k, verbose=False, mode='choices'):
    cache = {}
    sat = {}
    T6 = implA.intervals()
    for i in range(k):
        ok = set()
        if mode == 'choices':
            gen = []
            for idx in range(6 ** ell):
                c = []
                t = idx
                for _ in range(ell):
                    c.append(t % 6)
                    t //= 6
                gen.append(tuple(frozenset(j for j in range(ell) if p in T6[c[j]])
                                 for p in range(6)))
        else:
            gen = sign_sets(ell)
        for S in gen:
            ocs = tuple(implA.allowed_sets(s, ell, k) for s in S)
            if any(not o[0] or not o[1] for o in ocs):
                continue
            key = (ocs, i)
            if key not in cache:
                cache[key] = cell_sat_dp(ocs, i, k, ell)
            if cache[key]:
                ok.add(S)
        sat[i] = ok
        if verbose:
            print(f"  B: ell={ell} k={k} label={i}: {len(ok)} satisfiable sign tuples")
    # walks: a weak order of the ell rays together with a starting sign tuple
    orders = implA.weak_orders(ell)
    T = implA.intervals()
    good = []
    for i in range(k):
        ok = sat[i]
        for S0 in ok:
            # a starting sign tuple; convert to a choice vector (row model) for the walk
            ch = []
            for j in range(ell):
                row = {p for p in range(6) if j in S0[p]}
                m = [mm for mm in range(6) if T[mm] == row]
                if not m:
                    ch = None
                    break
                ch.append(m[0])
            if ch is None:
                continue
            ch = tuple(ch)
            for order in orders:
                cur = list(ch)
                fine = True
                for _ in range(6):
                    for blk in order:
                        for j in blk:
                            cur[j] = (cur[j] - 1) % 6
                        St = tuple(frozenset(j for j in range(ell) if p in T[cur[j]])
                                   for p in range(6))
                        if St not in ok:
                            fine = False
                            break
                    if not fine:
                        break
                if fine and tuple(cur) == ch:
                    good.append((i, S0, order))
    return good, sat


if __name__ == '__main__':
    import sys, time
    ell = int(sys.argv[1]); k = int(sys.argv[2])
    t = time.time()
    good, sat = decide(ell, k, verbose=True)
    print(f"B: ell={ell} k={k}: surviving (sign tuple, order, label) "
          f"{len(good)}   [{time.time()-t:.1f}s]")
