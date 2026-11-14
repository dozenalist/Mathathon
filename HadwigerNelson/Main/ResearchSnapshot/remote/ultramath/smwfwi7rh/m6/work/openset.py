"""The (5.2) constraint in its rigorous open-set form, for the survivors.

(5.2) holds for a.e. pair (u,v) in S x S.  Applied to a product of two arcs it gives
c(x+u+v) notin P_x(u) cup P_x(v) for a.e. (u,v) in the product.  Since every palette
avoids the centre's colour i, every union has at most k-1 elements, so the only case in
which this forbids anything is

    P_x(u) cup P_x(v) = [k] \\ {i},

in which case the whole sum region has colour i.  If in addition the sum region meets the
circle of radius one about x, that gives two density-one points of colour i at distance
one, contradicting Lemma 4.3.

For two arcs of directions D, D' (angles pi*q), the achievable separations q' - q are the
interval (a' - b, b' - a); the sum has modulus one exactly when the separation is
+-2/3 in these units.  So (D,D') is "unit-capable" iff that interval meets +-2/3.

Hence a palette field constant on the cells is admissible for the full rigorous §8 layer
iff there is an assignment Q of an admissible palette to each cell such that

    Q(D) cup Q(D') != [k] \\ {i}      for every unit-capable pair (D, D').
"""

from fractions import Fraction as F
from itertools import combinations
import s8
import rigorous
import strips
import walk


def unit_capable(a, b, a2, b2):
    """Does some pair (q,q') in D x D' give |e^{i pi q} + e^{i pi q'}| = 1?"""
    lo = a2 - b
    hi = b2 - a
    t = F(2, 3)
    # the separation q' - q ranges over (lo, hi) mod 2; check +-2/3 modulo 2
    for target in (t % 2, (-t) % 2):
        # does an element congruent to target mod 2 lie in (lo,hi)?
        k = 0
        while target + 2 * k <= hi + 2:
            v = target + 2 * k
            if lo < v < hi:
                return True
            if v > hi:
                break
            k += 1
        k = -1
        while target + 2 * k > lo - 2:
            v = target + 2 * k
            if lo < v < hi:
                return True
            k -= 1
    return False


def cells_of(rays, ell):
    out = []
    for (a, b, S, O, I, w) in strips.arcs(rays, ell):
        out.append(dict(a=a, b=b, S=S, O=O, I=I))
    return out


def assignment_exists(cs, ell, k, w2, i):
    n = len(cs)
    full = set(range(k)) - {i}
    doms = []
    for c in cs:
        d = []
        for size in range(1, w2 + 1):
            for P in combinations(range(k), size):
                P = frozenset(P)
                if i in P or not (P & c['O']) or not (P & c['I']):
                    continue
                if any(P <= frozenset({j, (j + 1) % ell}) for j in range(ell)):
                    continue
                d.append(P)
        doms.append(d)
    dang = [[False] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x != y:
                dang[x][y] = unit_capable(cs[x]['a'], cs[x]['b'], cs[y]['a'], cs[y]['b'])
    chosen = {}
    order = sorted(range(n), key=lambda t: len(doms[t]))

    def ok(t, P):
        for u, Q in chosen.items():
            if dang[t][u] and (P | Q) == full:
                return False
        return True

    def rec(t):
        if t == n:
            return True
        c = order[t]
        for P in doms[c]:
            if ok(c, P):
                chosen[c] = P
                if rec(t + 1):
                    return True
                del chosen[c]
        return False

    return rec(0)


def main(ell=6, k=6, w2=3):
    sat, good = rigorous.walk(ell, k, w2, True, verbose=False)
    print(f"ell={ell} k={k}: {len(good)} rigorous survivors")
    bad = 0
    nullcells = 0
    for (i, c0, order) in good:
        rays = strips.rays_of(tuple((c + 1) % 6 for c in c0), tuple(reversed(order)), ell)
        cs = cells_of(rays, ell)
        if assignment_exists(cs, ell, k, w2, i):
            continue
        bad += 1
        if bad <= 3:
            print("   no assignment for survivor", i, c0, order)
    print(f"   survivors with no admissible assignment for the open-set (5.2): {bad}")
    return good, bad


if __name__ == '__main__':
    main()
