"""Geometric reconstruction of the orbit cells from explicit rational ray directions,
and validation of the row model used by implementations A and B.

For ray j at direction r_j (units of pi, i.e. direction angle pi*r_j) and base
direction q (also in units of pi), the sign of edge j at orbit position p is

    sigma_j(p) = sign cos(pi*(q + p/3 - r_j)),

and (8.1)'s allowed sets are read off from S_p = {j : sigma_j(p) = +1}.

A configuration is (weak order of the slack residues r_j mod 1/3, starting cell).
The construction below realises any such pair by exact rational rays:

    r_j = (2 - t_j) mod 2,      t_j = (6 - c0[j])/3 + eta_j,
    eta_j = eps * (B - b_j),    eps = 1/(100 B (ell+1)),

with b_j the block index of ray j.  Then r_j mod 1/3 is decreasing in b_j, so
the slip order is block 0, 1, ..., B-1, and at q = 0+ the pattern is c0.
"""
from fractions import Fraction as F
import implA


def sgn(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def sign_at(q, r, p):
    x = (q + F(p, 3) - r) % 2
    c = 1 if x == 0 else None
    # cos(pi x) > 0  iff  x mod 2 in [0,1/2) or (3/2,2)
    if x == F(1, 2) or x == F(3, 2):
        return 0
    return 1 if (x < F(1, 2) or x > F(3, 2)) else -1


def pattern_at(q, rays, ell):
    S = []
    for p in range(6):
        sp = set()
        for j in range(ell):
            s = sign_at(q, rays[j], p)
            if s == 0:
                return None
            if s > 0:
                sp.add(j)
        S.append(frozenset(sp))
    return tuple(S)


def build_rays(order, c0, ell):
    B = len(order)
    block = {}
    for b, blk in enumerate(order):
        for j in blk:
            block[j] = b
    rays = []
    for j in range(ell):
        eta = F(1, 6) - F(block[j], 1) * F(1, 3 * B) - F(1, 9 * B)
        t = F(6 - c0[j], 3) + eta
        rays.append((2 - t) % 2)
    return tuple(rays)


def critical(rays, ell):
    out = set()
    for j in range(ell):
        for p in range(6):
            for s in (F(1, 2), F(-1, 2)):
                out.add((rays[j] - F(p, 3) + s) % 2)
    return sorted(out)


def cells(rays, ell):
    crit = critical(rays, ell)
    out = []
    for a, b in zip(crit, crit[1:] + [crit[0] + 2]):
        mid = (a + b) / 2
        pat = pattern_at(mid % 2, rays, ell)
        assert pat is not None, (a, b, rays)
        out.append((a, b, pat))
    return out


def walk_from_geometry(order, c0, ell):
    """Cells starting at q = 0+, in increasing q, over one full turn."""
    rays = build_rays(order, c0, ell)
    T = implA.intervals()
    start = pattern_at(F(1, 1000), rays, ell)
    want0 = tuple(frozenset(j for j in range(ell) if p in T[c0[j]]) for p in range(6))
    assert start == want0, (start, want0, rays)
    crit = critical(rays, ell)
    crit = [c for c in crit if c > F(1, 1000)]
    seq = []
    for a, b in zip(crit, crit[1:]):
        mid = (a + b) / 2
        seq.append(pattern_at(mid, rays, ell))
    # first cell of the listing is the one containing 1/1000
    seq = [start] + seq
    return rays, seq


def check_walk(order, c0, ell):
    """Does the geometric cell sequence equal the row-model walk of (c0, order)?"""
    rays, seq = walk_from_geometry(order, c0, ell)
    T = implA.intervals()
    cur = list(c0)
    model = [tuple(frozenset(j for j in range(ell) if p in T[cur[j]]) for p in range(6))]
    for _ in range(6):
        for blk in order:
            for j in blk:
                cur[j] = (cur[j] - 1) % 6
            model.append(tuple(frozenset(j for j in range(ell) if p in T[cur[j]])
                               for p in range(6)))
    # drop the closing repeat
    model = model[:-1]
    if len(model) != len(seq):
        return False, (rays, len(model), len(seq))
    return model == seq, rays


if __name__ == '__main__':
    import sys, random
    random.seed(7)
    tot = bad = 0
    for ell in (3, 4):
        orders = implA.weak_orders(ell)
        for order in orders:
            for c0 in [(0,) * ell, tuple(range(ell)), (5,) * ell, tuple((3 * j) % 6 for j in range(ell))]:
                ok, info = check_walk(order, c0, ell)
                tot += 1
                if not ok:
                    bad += 1
                    print("MISMATCH", ell, order, c0, info)
    for ell in (5, 6):
        orders = implA.weak_orders(ell)
        for _ in range(300):
            order = random.choice(orders)
            c0 = tuple(random.randrange(6) for _ in range(ell))
            ok, info = check_walk(order, c0, ell)
            tot += 1
            if not ok:
                bad += 1
                print("MISMATCH", ell, order, c0, info)
    print(f"geometric row-model checks: {tot} configurations, {bad} mismatches")
