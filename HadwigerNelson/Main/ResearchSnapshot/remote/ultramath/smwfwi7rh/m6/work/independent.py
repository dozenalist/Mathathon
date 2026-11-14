"""Independent check: build explicit exact ray configurations, compute the orbit
cells and the allowed sets straight from the circle geometry, and decide the
palette system by brute force over six-tuples of palettes.

No use is made of the row-interval abstraction or of the transfer/CSP code in
decision.py; the only shared ingredient is s8.sgn_cos, the sign of cos(pi*x).
"""

from fractions import Fraction as F
from itertools import combinations, product
import random
import s8


def sign_cos(x):
    y = x % 2
    if y == F(1, 2) or y == F(3, 2):
        return 0
    return -1 if F(1, 2) < y < F(3, 2) else 1


def cells(rays, ell):
    """Cell decomposition of the direction circle with the sign pattern on each."""
    crit = set()
    for r in rays:
        for p in range(6):
            for s in (F(1, 2), F(-1, 2)):
                crit.add((r - F(p, 3) + s) % 2)
    crit = sorted(crit)
    out = []
    for a, b in zip(crit, crit[1:] + [crit[0] + 2]):
        mid = (a + b) / 2
        pats = []
        bad = False
        for p in range(6):
            S = set()
            for j, r in enumerate(rays):
                sg = sign_cos(mid + F(p, 3) - r)
                if sg == 0:
                    bad = True
                elif sg > 0:
                    S.add(j)
            pats.append(frozenset(S))
        if bad:
            raise RuntimeError('degenerate cell')
        out.append((a, b, tuple(pats)))
    return out


def allowed(S, ell, k):
    pos, neg = set(), set()
    for j in range(ell):
        if j in S:
            pos |= {j, (j + 1) % ell}
        else:
            neg |= {j, (j + 1) % ell}
    return frozenset(range(k)) - pos, frozenset(range(k)) - neg


def brute_sat(pats, ell, k, w, sa):
    """Is there a six-tuple of palettes satisfying every constraint?"""
    ois = [allowed(S, ell, k) for S in pats]
    for O, I in ois:
        if not O or not I:
            return None                       # already impossible by Lemma 8.1
    doms = []
    for (O, I) in ois:
        d = []
        for size in range(1, w + 1):
            for P in combinations(range(k), size):
                P = frozenset(P)
                if not (P & O) or not (P & I):
                    continue
                if sa is not None and sa in P:
                    continue
                if any(P <= frozenset({j, (j + 1) % ell}) for j in range(ell)):
                    continue
                d.append(P)
        doms.append(d)
    full = frozenset(range(k))
    for tup in product(*doms):
        ok = True
        for p in range(6):
            for q in range(p + 1, 6):
                d = (q - p) % 6
                if d in (0, 3):
                    continue
                if tup[p] | tup[q] == full:
                    ok = False
                    break
                if d in (1, 5) and (tup[p] & tup[q]):
                    ok = False
                    break
                if sa is not None and d in (2, 4) and tup[p] | tup[q] == full - {sa}:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return tup
    return None


def config_ok(rays, ell, k, w, sa):
    """Does every cell of this configuration admit a palette tuple?"""
    for a, b, pats in cells(rays, ell):
        if brute_sat(pats, ell, k, w, sa) is None:
            return False, (a, b, pats)
    return True, None


def random_sweep(ell, k, w, trials=400, seed=5):
    random.seed(seed)
    surviving = []
    for _ in range(trials):
        den = random.choice([7, 11, 13, 17, 19, 23])
        rays = [F(random.randrange(den), den) for _ in range(ell)]
        for sa in range(k):
            ok, wit = config_ok(rays, ell, k, w, sa)
            if ok:
                surviving.append((rays, sa))
    return surviving


if __name__ == '__main__':
    import sys
    ell, k, w = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    trials = int(sys.argv[4]) if len(sys.argv) > 4 else 400
    sv = random_sweep(ell, k, w, trials)
    print(f"ell={ell} k={k}: random configurations all of whose cells are satisfiable "
          f"for some avoided label: {len(sv)} of {trials} x {k}")
    for r, sa in sv[:3]:
        print("   ", [str(x) for x in r], "label", sa)
