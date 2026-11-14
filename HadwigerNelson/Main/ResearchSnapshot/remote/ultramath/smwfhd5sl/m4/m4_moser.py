"""Exact verification of the Moser-spindle certificate used in Section 8.5 of the paper,
and of the placement certificate (Lemma 8.9 / Table 1 / Table 2).

Everything is exact: coordinates of the placed points lie in the Q-algebra
A = Q(s, t) with s = sqrt(3), t = sqrt(11), basis (1, s, t, s t).  Polynomials are
evaluated in that algebra and compared through rigorous rational interval bounds
on s and t.
"""
from fractions import Fraction as F
import itertools

# ---------------------------------------------------------------- exact algebra
# element = (a, b, c, d) meaning a + b*s + c*t + d*s*t,  s^2 = 3, t^2 = 11
ZERO = (F(0), F(0), F(0), F(0))
ONE = (F(1), F(0), F(0), F(0))


def mk(a=0, b=0, c=0, d=0):
    return (F(a), F(b), F(c), F(d))


def add(x, y):
    return tuple(p + q for p, q in zip(x, y))


def sub(x, y):
    return tuple(p - q for p, q in zip(x, y))


def neg(x):
    return tuple(-p for p in x)


def mul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    # (a + b s + c t + d st)(e + f s + g t + h st)
    # s^2 = 3, t^2 = 11, st*st = 33, s*st = 3 t, t*st = 11 s
    r0 = a * e + 3 * b * f + 11 * c * g + 33 * d * h
    r1 = a * f + b * e + 11 * c * h + 11 * d * g
    r2 = a * g + 3 * b * h + c * e + 3 * d * f
    r3 = a * h + b * g + c * f + d * e
    return (r0, r1, r2, r3)


def smul(x, q):
    return tuple(q * p for p in x)


def algeq(x, y):
    return all(p == q for p, q in zip(x, y))


# rigorous rational bounds for s and t (both directions), 10 digits
S_LO, S_HI = F(17320508075, 10**10), F(17320508076, 10**10)
T_LO, T_HI = F(33166247903, 10**10), F(33166247904, 10**10)


def bounds(x):
    """rigorous [lo,hi] rational interval containing the real value of x."""
    a, b, c, d = x
    lo = hi = a
    for coef, (plo, phi) in ((b, (S_LO, S_HI)), (c, (T_LO, T_HI)), (d, (S_LO * T_LO, S_HI * T_HI))):
        if coef >= 0:
            lo += coef * plo
            hi += coef * phi
        else:
            lo += coef * phi
            hi += coef * plo
    return lo, hi


def lt(x, y):
    """certified strict inequality x < y."""
    lo, hi = bounds(sub(x, y))
    if hi < 0:
        return True
    if lo >= 0:
        return False
    raise ValueError("undecided: tighten the rational bounds")


# ------------------------------------------------------- the Moser-Soifer graph
s = mk(0, 1)      # sqrt 3
t = mk(0, 0, 1)   # sqrt 11
I = mk(0, 0, 0, 0)

U_RE = mk(F(5, 6))
U_IM = mk(0, 0, F(1, 6))     # u = (5 + i sqrt11)/6


def cpair(re, im):
    return (re, im)


def cmul(z, w):
    return (sub(mul(z[0], w[0]), mul(z[1], w[1])), add(mul(z[0], w[1]), mul(z[1], w[0])))


U = cpair(U_RE, U_IM)

G = {
    '0': cpair(ZERO, ZERO),
    'A': cpair(smul(s, F(1, 2)), smul(ONE, F(1, 2))),
    'B': cpair(smul(s, F(1, 2)), smul(ONE, F(-1, 2))),
    'T': cpair(s, ZERO),
}
G['uA'] = cmul(U, G['A'])
G['uB'] = cmul(U, G['B'])
G['uT'] = cmul(U, G['T'])


def cmul(z, w):
    return (sub(mul(z[0], w[0]), mul(z[1], w[1])), add(mul(z[0], w[1]), mul(z[1], w[0])))


U = cpair(U_RE, U_IM)
G['uA'] = cmul(U, G['A'])
G['uB'] = cmul(U, G['B'])
G['uT'] = cmul(U, G['T'])

names = sorted(G)
EDGES = [('0', 'A'), ('0', 'B'), ('A', 'B'), ('T', 'A'), ('T', 'B'),
         ('0', 'uA'), ('0', 'uB'), ('uA', 'uB'),
         ('uT', 'uA'), ('uT', 'uB'), ('T', 'uT')]


def dist2(z, w):
    dr = sub(z[0], w[0])
    di = sub(z[1], w[1])
    return add(mul(dr, dr), mul(di, di))


print("=== Moser spindle, exact ===")
for a, b in EDGES:
    d2 = dist2(G[a], G[b])
    assert algeq(d2, ONE), (a, b, d2)
print(f"{len(EDGES)} edges, all |z_a - z_b|^2 = 1 exactly (in Q(sqrt3,sqrt11))")

adj = {v: set() for v in names}
for a, b in EDGES:
    adj[a].add(b)
    adj[b].add(a)

# exhaustive 3-colourability test
sols = 0
for col in itertools.product(range(3), repeat=len(names)):
    c = dict(zip(names, col))
    if all(c[a] != c[b] for a, b in EDGES):
        sols += 1
print(f"proper 3-colourings of the 7-vertex graph: {sols}  (3^7 = {3**7} tested)")

# every *other* pair is at a non-unit distance, and more precisely none of them is a unit pair
nonedges = [(a, b) for a, b in itertools.combinations(names, 2) if (a, b) not in EDGES and (b, a) not in EDGES]
print(f"non-edges: {len(nonedges)}")
for a, b in nonedges:
    d2 = dist2(G[a], G[b])
    assert not algeq(d2, ONE)

# paper's orientation check: 0 and T are forced to be equal in any proper 3-colouring
# (two triangles sharing AB); their rotated copies force 0 and uT equal; T-uT is a unit edge.
print("forced: any proper 3-colouring of {0,A,B,T,uA,uB,uT} has c(0)=c(T) and c(0)=c(uT), but |T-uT|=1")

# ------------------------------------------------------------- placement (8.6)
#  z_g = ((35+12i)/37) g + (-290+149i)/250
print()
print("=== placement certificate (8.6), exact ===")
print("|35+12i|^2 =", 35**2 + 12**2, " 37^2 =", 37**2)

# The printed (8.6) is  z_g = ((35+12i)/37) ( g + (-290+149i)/250 ):  the rotation
# multiplies the WHOLE bracket.  (pdftotext silently drops the outer parentheses; the
# numeric check against the paper's own Table 1 below is what fixes the reading.)
MUL = (mk(F(35, 37)), mk(F(12, 37)))       # exact rotation, |MUL| = 1
TR0 = (mk(F(-290, 250)), mk(F(149, 250)))  # inner translation
TR = cmul(MUL, TR0)                        # effective translation


def place(z):
    return (add(cmul(MUL, z)[0], TR[0]), add(cmul(MUL, z)[1], TR[1]))


P = {g: place(z) for g, z in G.items()}

# 8.5: unit edges are preserved by a rotation+translation  (check exactly)
for a, b in EDGES:
    assert algeq(dist2(P[a], P[b]), ONE)
print(f"placed graph: {len(EDGES)} unit edges still exactly unit")


def pol_less(z):
    """exact test of  (8.4):  ups^2 (3 xi^2 - ups^2)^2  <  l^3 (1 - l/4)(l-1)^2,  l = xi^2+ups^2"""
    xi, up = z
    x2 = mul(xi, xi)
    y2 = mul(up, up)
    l = add(x2, y2)
    lhs = mul(y2, mul(sub(smul(x2, 3), y2), sub(smul(x2, 3), y2)))
    four = mk(4)
    one = mk(1)
    rhs = mul(mul(mul(l, l), l), mul(sub(one, smul(l, F(1, 4))), mul(sub(l, one), sub(l, one))))
    return lhs, rhs, l


rows = []
print(f"{'g':>3} {'xi':>16} {'ups':>16} {'l':>18} {'verdict'}")
for g in names:
    lhs, rhs, l = pol_less(P[g])
    ok_pos = lt(ZERO, l) and lt(l, mk(4))
    ok_neq1 = lt(ONE, l) if lt(ONE, l) else lt(l, ONE)
    ok = lt(lhs, rhs)
    lo_l, hi_l = bounds(l)
    rows.append((g, lo_l, hi_l, ok, ok_pos))
    print(f"{g:>3} {float(bounds(P[g][0])[0]):16.6f} {float(bounds(P[g][1])[0]):16.6f} "
          f"({float(lo_l):.6f},{float(hi_l):.6f})  P<P': {ok}   0<l<4: {ok_pos}  l!=1: {ok_neq1}")
    assert ok and ok_pos and ok_neq1, g
print("Lemma 8.9 verified exactly for all seven placed points.")

# ------------------------------------------- the paper's Table 1 / Table 2 check
print()
print("=== check of the paper's decimal table (Table 1) ===")
print(f"{'g':>3} {'xi0(pap)':>10} {'xi0(ours)':>11} {'ups0(pap)':>10} {'ups0(ours)':>11} "
      f"{'|dx|':>9} {'|dy|':>9} {'P+':>10} {'P-prime':>10} {'h=1.1e-4 ok?':>13}")
tab = {
    '0': (-1.2906, 0.1876, 0.90, 1.35),
    'A': (-0.6335, 0.9414, 0.095, 0.110),
    'B': (-0.3092, -0.0045, 0.000002, 0.00065),
    'T': (0.3478, 0.7493, 0.023, 0.026),
    'uA': (-1.1598, 1.1790, 9.8, 19.0),
    'uB': (-0.3666, 0.5700, 0.0022, 0.024),
    'uT': (-0.2358, 1.5614, 12.65, 12.9),
}
h = F(11, 100000)
worst = F(0)
for g in names:
    xi0, up0, Pp, Pm = tab[g]
    xlo, xhi = bounds(P[g][0])
    ylo, yhi = bounds(P[g][1])
    xm = (F(xlo) + F(xhi)) / 2
    ym = (F(ylo) + F(yhi)) / 2
    dx = abs(xm - F(xi0))
    dy = abs(ym - F(up0))
    worst = max(worst, dx, dy)
    print(f"{g:>3} {xi0:10.4f} {float(xm):11.6f} {up0:10.4f} {float(ym):11.6f} "
          f"{float(dx):9.6f} {float(dy):9.6f} {Pp:10.4g} {Pm:10.4g} "
          f"{'yes' if max(dx, dy) < h else 'NO':>13}")
print(f"worst deviation from the paper's rounded centres: {float(worst):.6f}   (claimed h = 0.00011)")
