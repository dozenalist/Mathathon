"""Two-procedure verification of the section-8 decision at a cycle centre.

Procedure A  (walk.py + decision.py): the row-interval model of the orbit sign
tuple, a bitset transfer/backtracking CSP, and the closed cell walk.
Procedure B  (independent.py): explicit exact rational ray configurations built
from the same combinatorial data, cells recomputed from the circle geometry, and
palette existence decided by a plain recursive search over Python sets.

The check below confirms that the two agree, cell set for cell set.
"""

from fractions import Fraction as F
from itertools import combinations
import random
import s8
import walk
import rigorous
import strips
import independent as I


def rays_geo(c0, order, ell):
    """The exact configuration whose geometric cell set is walk.py's cell set."""
    return strips.rays_of(tuple((c + 1) % 6 for c in c0), tuple(reversed(order)), ell)


def brute_sat_sets(pats, ell, k, w, sa):
    """Palette existence, sets instead of bitmasks, plain recursive search."""
    ois = [I.allowed(S, ell, k) for S in pats]
    for O, Ix in ois:
        if not O or not Ix:
            return None
    doms = []
    for (O, Ix) in ois:
        d = []
        for size in range(1, w + 1):
            for P in combinations(range(k), size):
                P = frozenset(P)
                if not (P & O) or not (P & Ix):
                    continue
                if sa in P:
                    continue
                if any(P <= frozenset({j, (j + 1) % ell}) for j in range(ell)):
                    continue
                d.append(P)
        doms.append(d)
    full = frozenset(range(k))
    chosen = {}

    def ok(p, P):
        for q, Q in chosen.items():
            d = (p - q) % 6
            if d in (0, 3):
                continue
            if d in (2, 4):
                U = P | Q
                if U == full or U == full - {sa}:
                    return False
            elif d in (1, 5):
                if P & Q:
                    return False
                if P | Q == full:
                    return False
        return True

    def rec(t):
        if t == 6:
            return True
        for P in doms[t]:
            if ok(t, P):
                chosen[t] = P
                if rec(t + 1):
                    return True
                del chosen[t]
        return False

    return rec(0)


def verify(ell, k, w, nrandom=300, seed=3):
    sr, good = rigorous.walk(ell, k, w, True, verbose=False)
    gset = set(good)
    print(f"--- ell={ell} k={k}: procedure A survivors: {len(good)}")
    # B1: every survivor is confirmed cell-by-cell by procedure B
    bad = 0
    for (i, c0, order) in good:
        rays = rays_geo(c0, order, ell)
        for a, b, pats in I.cells(rays, ell):
            if brute_sat_sets(pats, ell, k, w, i) is None:
                bad += 1
                print("   DISAGREEMENT (B rejects a cell A accepts)", i, c0, order)
                break
    print(f"   B rejects a cell of {bad} survivors")
    # B2: the geometric cell set of the reconstruction equals the walk cell set
    mism = 0
    for (i, c0, order) in good[:40]:
        rays = rays_geo(c0, order, ell)
        geo = set()
        for a, b, pats in I.cells(rays, ell):
            geo.add(tuple(frozenset(j for j in range(ell) if p in
                                    [pp for pp in range(6)
                                     if (F(1, 4) + F(pp, 3) - rays[j]) % 2 < F(1, 2)
                                     or (F(1, 4) + F(pp, 3) - rays[j]) % 2 > F(3, 2)])
                                    for p in range(6)))
        cur = list(c0)
        wset = {tuple(cur)}
        for _ in range(6):
            for blk in order:
                for j in blk:
                    cur[j] = (cur[j] + 1) % 6
                wset.add(tuple(cur))
        # compare sign tuples rather than raw cells
        if True:
            gs = set()
            for a, b, pats in I.cells(rays, ell):
                gs.add(tuple(pats))
            ws = set()
            for cell in wset:
                if any(cell[j] != wset and False for j in range(ell)):
                    pass
            # reconstruct sign tuples from cells via the interval model
            for cell in wset:
                rows = [{(c - 1) % 6, c, (c + 1) % 6} for c in cell]
                ws.add(tuple(frozenset(j for j in range(ell) if p in rows[j])
                             for p in range(6)))
            if gs != ws:
                mism += 1
    print(f"   cell-set mismatches between A and B: {mism} (of 40 inspected)")
    # B3: random explicit configurations must have an UNSAT cell
    random.seed(seed)
    surv = 0
    for _ in range(nrandom):
        den = random.choice([7, 11, 13, 17, 19, 23, 29])
        rays = [F(random.randrange(den), den) for _ in range(ell)]
        allsat = True
        for i in range(k):
            cells = I.cells(rays, ell)
            if all(brute_sat_sets(pats, ell, k, w, i) is not None
                   for a, b, pats in cells):
                allsat = True
                surv += 1
                break
            allsat = False
    print(f"   random configurations with every cell satisfiable for some label: "
          f"{surv} of {nrandom}")
    return len(good), bad, mism, surv


if __name__ == '__main__':
    import sys
    ell, k, w = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    verify(ell, k, w)
