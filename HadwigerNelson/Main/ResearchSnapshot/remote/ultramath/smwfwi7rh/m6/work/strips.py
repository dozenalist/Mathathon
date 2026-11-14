"""Reconstruct explicit ray configurations from a surviving cell and check the
monochromatic-strip obstruction.

A configuration is (weak cyclic order of the residues arg v_j mod pi/3, and the
row assignment at q = 0).  The row of ray j at q = 0 is the cyclic 3-interval
{m-1,m,m+1} with m = cell[j], and that happens exactly when 3*arg(v_j)/pi lies in
(m-1/2, m+1/2).  So write arg(v_j)/pi = (m_j + f_j)/3 with f_j in (-1/2,1/2); the
residue class of arg(v_j) mod 1/3 is f_j/3 and the slip order is the order of the
f_j.

Monochromatic-strip obstruction (MS).  Lemma 8.1 gives, on an arc of S \\ B on which
O is a singleton {c}, an open strip just outside radius one using only colour c.
Two points of that strip at equal radius r < 1 are at distance one exactly when
their angular separation is 2 arcsin(1/(2r)) -> pi/3 as r -> 1.  Since the strip has
a positive radial width, an arc of angular width > pi/3 makes the strip contain two
same-coloured points at distance one, contradicting properness.  The same holds for
I and the inner strip.
"""

from fractions import Fraction as F
import s8
import walk
import decision

PI3 = None


def rays_of(choice, order, ell):
    """Explicit angles arg(v_j)/pi in [0,2) realising this cell and slip order."""
    blocks = {}
    for bi, block in enumerate(order):
        for j in block:
            blocks[j] = bi
    nb = len(order)
    # f_j strictly increasing across blocks, inside (-1/2, 1/2)
    f = {}
    for j in range(ell):
        bi = blocks[j]
        f[j] = F(-1, 2) + F(2 * bi + 1, 2 * (nb + 1))
    rays = [F(choice[j]) + f[j] for j in range(ell)]
    return [(r / 3) % 2 for r in rays]


def arcs(rays, ell):
    """Components of the circle minus the critical set, with (O,I) on each."""
    crit = set()
    for r in rays:
        for p in range(6):
            for s in (F(1, 2), F(-1, 2)):
                crit.add((r - F(p, 3) + s) % 2)
    crit = sorted(crit)
    out = []
    for a, b in zip(crit, crit[1:] + [crit[0] + 2]):
        mid = (a + b) / 2
        S = frozenset(j for j in range(ell) if s8.sgn_cos(mid - rays[j]) > 0)
        O, I = s8.allowed_sets(S, ell, 6)
        out.append((a, b, S, O, I, (b - a)))
    return out


def check(ell=6, k=6, w2=3):
    sr, good = walk.main(ell, k, w2, True, verbose=False)
    print(f"ell={ell} k={k}: {len(good)} surviving configurations")
    viol = []
    clean = []
    for (i, c0, order) in good:
        # the configuration whose geometric cell set IS the surviving cell set
        rays = rays_of(tuple((c + 1) % 6 for c in c0), tuple(reversed(order)), ell)
        for (a, b, S, O, I, w) in arcs(rays, ell):
            for name, A in (('O', O), ('I', I)):
                if len(A) == 1 and w > F(1, 3):
                    viol.append((i, c0, order, name, tuple(sorted(A)), w))
        clean.append((i, c0, order))
    print("  configurations with a monochromatic strip of width > pi/3:", len(viol))
    print("  configurations with no such strip:", len(clean))
    import collections
    pat = collections.Counter()
    for (i, c0, order) in clean:
        pat[tuple(sorted(tuple(sorted(b)) for b in order))] += 1
    for kk, v in sorted(pat.items(), key=lambda kv: -kv[1]):
        print("   surviving slip blocks", kk, v)
    # describe the geometry of the clean ones
    if clean:
        i, c0, order = clean[0]
        rays = rays_of(c0, order, ell)
        print("   example angles/pi:", [str(r) for r in rays])
        for (a, b, S, O, I, w) in arcs(rays, ell):
            print("     arc", float(a), float(b), "width", float(w), "S", sorted(S),
                  "O", sorted(O), "I", sorted(I))
    return viol, clean


if __name__ == '__main__':
    check()
