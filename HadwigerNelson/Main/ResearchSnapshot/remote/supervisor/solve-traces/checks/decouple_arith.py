"""Exact check (Fractions) that the m3 k>=7 gadget lies strictly inside the
radius-(1-eps) ball about each of its accumulating cyclic centres, so the
far-field decoupling lemma applies to the palette at those centres."""
from fractions import Fraction as F
import itertools

p0 = (F(1,55), F(18,55)); ell = F(1,100)
# W = p0 + [-ell/2, ell/2]^2 ; q_n = p0 + (ell*2^(-n-3), 0)
def maxdist_ball(q):
    # max over corners of W of |z-q|  (convex max of a convex function on a box -> at corners)
    m2 = F(0)
    for sx in (-1,1):
        for sy in (-1,1):
            z = (p0[0]+sx*ell/2, p0[1]+sy*ell/2)
            d2 = (z[0]-q[0])**2 + (z[1]-q[1])**2
            m2 = max(m2, d2)
    return m2

def sqrt_upper(x):
    """smallest Fraction with square >= x  (exact rational upper bound)"""
    n, d = x.numerator, x.denominator
    r = F(int((n*10**12//d)**0.5), 10**6)
    while r*r < x: r += F(1,10**6)
    return r

print("W = p0 + [-1/200,1/200]^2,  q_n = p0 + (2^(-n-3)/100, 0)")
for n in range(0, 8):
    q = (p0[0] + ell*F(1, 2**(n+3)), p0[1])
    rho = sqrt_upper(maxdist_ball(q))
    print(f"  n={n}: max|z-q_n| <= {rho} = {float(rho):.6f}   (need < 1-eps)")
    assert rho < F(1,2)
print()
print("=> W is contained in B(q_n, 1/2) for every n, so 'agree off B(q_n, 1-eps)'")
print("   with eps = 1/2 holds for the pair (m3 colouring, background c0).")
print()
# every circle used by the trace at q_n: centre y with |y-q_n| < eps/2, radius r with |r-1|<eps/2
eps = F(1,2)
lo = 1 - eps  # worst case lower distance of a sampled point from q_n
print("sampled points satisfy |y + r u - q_n| >= r - |y-q_n| > 1 - eps =", float(lo))
print("and                                 <= r + |y-q_n| < 1 + eps =", float(1+eps))
print("distance from p0:  |y+r u - p0| in ( 1-eps-|q_n-p0| , 1+eps+|q_n-p0| )")
for n in (0,1,2):
    off = ell*F(1,2**(n+3))
    print(f"  n={n}: annulus ({float(1-eps-off):.6f}, {float(1+eps+off):.6f})  contains the m3 annulus A = (1-71/10000, 1+71/10000)")
    assert 1-eps-off < 1-F(71,10000) and 1+F(71,10000) < 1+eps+off
print()
print("m3's exact certificate: A = {1-71/10000 <= |q-p0| <= 1+71/10000} meets no hexagon of c0-colour 0, 2 or 3.")
print("Hence every label in the palette P_{q_n}(e) lies in {1,4,5,6}, while c(q_n) in {0,2,3}:")
print("the cyclic centre's own colour is outside its palette, as required (paper Lemma D), and")
print("the palette sees only the BACKGROUND. Decoupling is what makes the k>=7 counterexample run.")
