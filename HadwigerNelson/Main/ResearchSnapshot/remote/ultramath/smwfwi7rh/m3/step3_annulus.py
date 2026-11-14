"""Step 3: exact shadow/annulus analysis at p_0 = (1/55, 18/55) for the seven-colouring.

For every hexagon whose colour is 0, 2 or 3 we compute exactly
   d_min^2, d_max^2  (squared least/greatest distance from p_0 to the closed hexagon)
and certify  d_min > 1+eps  or  d_max < 1-eps  by comparing squares in Q(sqrt3).
The construction only needs  (1 - eps, 1 + eps)  to meet no hexagon of colour 0,2,3,
where eps = (side of the square)/sqrt2.
"""
from fractions import Fraction as F
import math
from field import Q3
from hexcol import hex_vertices, hex_dist2, hex_maxdist2, z, colour

P0 = (Q3(F(1, 55)), Q3(F(18, 55)))
MAXR = 2.2     # plenty: annulus radius ~1, hexagon circumradius 2/5


def sq(x):
    return x * x


def hexdata(m, n):
    """(d_min^2, d_max^2) of the hexagon of (m,n) measured from P0, exactly."""
    dmin2 = hex_dist2(P0, m, n)
    dmax2 = hex_maxdist2(P0, m, n)
    return dmin2, dmax2


rows = []
for m in range(-12, 13):
    for n in range(-12, 13):
        c = z(m, n)
        d2 = (c[0] - P0[0]) * (c[0] - P0[0]) + (c[1] - P0[1]) * (c[1] - P0[1])
        if d2 > Q3(F(MAXR**2).limit_denominator(10**6)) + Q3(F(1, 100)):
            continue
        dmin2, dmax2 = hexdata(m, n)
        rows.append((colour(m, n), m, n, dmin2, dmax2))

print("hexagons considered:", len(rows))
# exact comparison helper:  d_min > 1+eps  <=>  d_min^2 > (1+eps)^2
def misses(dmin2, dmax2, eps):
    lo = Q3((1 - eps) ** 2)
    hi = Q3((1 + eps) ** 2)
    if dmin2 > hi:
        return 'outside'
    if dmax2 < lo:
        return 'inside'
    return 'MEETS'


# the paper's epsilon
eps0 = 0.0071
print("\n--- paper's eps = %g ---" % eps0)
bad = [(c, m, n) for (c, m, n, a, b) in rows if c in (0, 2, 3) and misses(a, b, eps0) == 'MEETS']
print("hexagons of colour 0,2,3 meeting the annulus:", bad)
for c in (0, 2, 3):
    # slack: how much larger eps can get before this colour touches the annulus
    slacks = []
    for (cc, m, n, a, b) in rows:
        if cc != c:
            continue
        # eps_h = max(d_min-1, 1-d_max), computed numerically for the report
        dmin = math.sqrt(a.float())
        dmax = math.sqrt(b.float())
        slacks.append(max(dmin - 1, 1 - dmax))
    if slacks:
        print(f"  colour {c}: nearest slack (numeric) = {min(slacks):.6f}")

print("\n--- which colours does the annulus meet, and how much can eps grow? ---")
# bisection on eps using exact comparisons
lo, hi = 0.0, 0.5
for _ in range(200):
    mid = (lo + hi) / 2
    ok = all(misses(a, b, mid) != 'MEETS' for (c, m, n, a, b) in rows if c in (0, 2, 3))
    if ok:
        lo = mid
    else:
        hi = mid
print("eps* (exact bisection) = %.12f" % lo)
print("=> maximal square side  ell = sqrt2 * eps* = %.12f" % (math.sqrt(2) * lo))

# sanity: the colours that DO occur in the annulus at eps = 0.0071
occ = sorted({c for (c, m, n, a, b) in rows if misses(a, b, eps0) == 'MEETS'})
print("colours meeting the annulus at eps=0.0071:", occ)
occ2 = sorted({c for (c, m, n, a, b) in rows if misses(a, b, lo * 0.999) == 'MEETS'})
print("colours meeting the annulus at eps=eps*:", occ2)
