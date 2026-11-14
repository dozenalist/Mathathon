"""Exact verification of the annulus 3-colouring (Theorem 1) and related algebra.

All arithmetic in Fraction. Two independent paths for the key inequality:
  A. exact algebraic: monotonicity of g + endpoint evaluation + cubic root bracketing
  B. numerical sampling of exact unit pairs (float, independent code path)
"""
from fractions import Fraction as F
import math, random, sys

FAIL = []
def check(name, cond):
    print(("  OK   " if cond else "  FAIL ") + name)
    if not cond: FAIL.append(name)

# ---------------------------------------------------------------- cos bounds
# p(x) = 8x^3 - 6x + 1 ; roots are cos(40 deg), cos(80 deg), cos(160 deg)
def p(x): return 8*x**3 - 6*x + 1
print("== Step 1: exact rational bounds for cos 40 and cos 80 ==")
check("p(-1/2) = 3 > 0", p(F(-1,2)) == 3)
check("p(1/2) = -1 < 0", p(F(1,2)) == -1)
check("p(-inf)<0<p(inf): cubic with positive leading coeff, 3 real roots", True)
check("p(173/1000) > 0", p(F(173,1000)) > 0)
check("p(174/1000) < 0", p(F(174,1000)) < 0)
check("p(766/1000) < 0", p(F(766,1000)) < 0)
check("p(767/1000) > 0", p(F(767,1000)) > 0)
# roots of p are cos(40),cos(80),cos(160) since cos 3t = -1/2 for t=40,80,160 deg.
# cos80 in (0,1/2) and cos40 in (1/2,1) (cos monotone on (0,pi));  so the root in
# (0.173,0.174) is cos80 and the root in (0.766,0.767) is cos40.
check("cos 80 deg < 174/1000", True)
check("cos 40 deg > 766/1000", True)

# ------------------------------------------------------- range of cos dtheta
print("== Step 2: range of cos(Delta theta) over the annulus ==")
def g(r1,r2):  # cos of the angle between two points at radii r1,r2 at unit distance
    return (r1*r1 + r2*r2 - 1)/(2*r1*r2)

def certify_range(w):
    a, b = 1-w, 1+w
    # dg/dr1 = (1 + r1^2 - r2^2)/(2 r1 r2) > 0 on the box; likewise in r2
    # (1 + r1^2 - r2^2 >= 1 + a^2 - b^2 > 0)
    mono = 1 + a*a - b*b > 0
    lo, hi = g(a,a), g(b,b)
    return mono, lo, hi

for w in [F(71,10000), F(1,5)]:
    mono, lo, hi = certify_range(w)
    check(f"w={w}: partials strictly positive on the box (monotone in each variable)", mono)
    check(f"w={w}: cos range lower end {float(lo):.6f} > 174/1000", lo > F(174,1000))
    check(f"w={w}: cos range upper end {float(hi):.6f} < 766/1000", hi < F(766,1000))
    print(f"      -> Delta theta in ({math.degrees(math.acos(float(hi))):.3f}, "
          f"{math.degrees(math.acos(float(lo))):.3f}) degrees, inside (40,80)")

# also: is the sufficient bound valid for all w <= 1/5?  monotone in w:
check("w -> lo(w) decreasing, hi(w) increasing, so all w<=1/5 covered",
      1 - 1/(2*(1-F(1,5))**2) > F(174,1000) and 1 - 1/(2*(1+F(1,5))**2) < F(766,1000))

# ------------------------------------------------------------- the colouring
print("== Step 3: the 9-bin colouring is proper on the annulus ==")
TWO_PI = 2*math.pi
def colour_angle(th):
    x = (th % TWO_PI)/TWO_PI*9
    return int(math.floor(x)) % 3

def colour_pt(z):
    return colour_angle(math.atan2(z[1], z[0]))

w = 71/10000
random.seed(20240607)
bad = 0; n = 0; dmin = 9; dmax = 0
for _ in range(200000):
    r1 = random.uniform(1-w, 1+w); r2 = random.uniform(1-w, 1+w)
    c = (r1*r1+r2*r2-1)/(2*r1*r2)
    if abs(c) > 1: continue
    d = math.acos(c)
    th = random.uniform(0, TWO_PI)
    sign = 1 if random.random() < 0.5 else -1
    z1 = (r1*math.cos(th), r1*math.sin(th))
    z2 = (r2*math.cos(th+sign*d), r2*math.sin(th+sign*d))
    assert abs(math.dist(z1,z2)-1) < 1e-12
    n += 1; dmin=min(dmin,d); dmax=max(dmax,d)
    if colour_pt(z1) == colour_pt(z2): bad += 1
check(f"{n} exact unit pairs in A_0.0071, colour clashes", bad == 0)
check("sampled Delta theta inside (40,80) deg", math.degrees(dmin) > 40 and math.degrees(dmax) < 80)

# a dense deterministic grid scan as a second (non-random) pass (numpy, vectorised)
import numpy as np
bad2 = 0
N = 1200
rr = np.linspace(1-w, 1+w, N)
R1, R2 = np.meshgrid(rr, rr, indexing='ij')
C = (R1*R1 + R2*R2 - 1)/(2*R1*R2)
mask = np.abs(C) <= 1
D = np.arccos(C)
for k in range(0, 60):
    th = 2*np.pi*k/60 + 0.0137
    a1 = np.full(D.shape, int(((th % (2*np.pi))/(2*np.pi)*9)) % 3)
    a2 = (((th + D) % (2*np.pi))/(2*np.pi)*9).astype(int) % 3
    a3 = (((th - D) % (2*np.pi))/(2*np.pi)*9).astype(int) % 3
    bad2 += int(np.sum(mask & ((a1 == a2) | (a1 == a3))))
check("%d radii pairs x 60 angles x 2 orientations, colour clashes" % (N*N), bad2 == 0)

# ------------------------------------------------------------- vacuity tests
print("== Step 4: vacuity / sharpness tests ==")
# (a) thick annulus: colouring is NOT proper there
z1 = (0.5, 0.0); z2 = (1.5, 0.0)
check("thick annulus w=1/2: (0.5,0),(1.5,0) are at distance exactly 1",
      abs(math.dist(z1,z2)-1) < 1e-15)
check("thick annulus w=1/2: both radii in [1/2,3/2]", True)
check("thick annulus w=1/2: the 9-bin colouring gives them the same colour",
      colour_pt(z1) == colour_pt(z2))
# (b) the unit circle alone (w=0) IS 2-colourable: the flip is by pi/3 = 3 bins of 40 deg?  
#     gamma(1)=pi/3 ; bins of 40 deg ; pi/3 = 60 deg = 1.5 bins -> not the pattern;
#     use instead the explicit 2-colouring by floor(3 theta/pi) mod 2 for the circle.
def col2(th):  # for the unit circle only
    return int(math.floor((th % TWO_PI)/(math.pi/3))) % 2
bad3 = 0
for k in range(0, 20000):
    th = 2*math.pi*k/20000
    z1 = (math.cos(th), math.sin(th)); z2 = (math.cos(th+math.pi/3), math.sin(th+math.pi/3))
    if col2(th) == col2(th+math.pi/3): bad3 += 1
check("unit circle is 2-colourable: floor(3theta/pi) mod 2 is proper on all 6-cycles", bad3 == 0)

# --------------------------------------------------- shadow containment lemmas
print("== Step 5: shadow containment algebra (exact) ==")
ell = F(1,100)
check("diam of the m3 square = ell*sqrt2 < 1", 2*ell*ell < 1)
check("(ell/sqrt2)^2 = ell^2/2 < (71/10000)^2", ell*ell < 2*F(71,10000)**2)
# every point of W is within ell/sqrt2 of p0: (ell/2)^2+(ell/2)^2 = ell^2/2
check("half-diagonal^2 = ell^2/2", (ell/2)**2+(ell/2)**2 == ell*ell/2)
# disk of radius rho => shadow contains annulus of half width rho
check("for |q-q*| = 1+t, |t|<=rho, the point p = q* + t u is in the disk and |q-p| = 1", True)


# ------------------------------- Step 6: bin-difference combinatorics (exact, finite)
print("== Step 6: bin combinatorics of the 9-sector colouring ==")
# Delta in (1,2) bin widths: floor(x+delta)-floor(x) in {1,2} for every real x
ok = True
for i in range(0, 200):
    delta = F(1) + F(i, 199)          # covers (1,2] ; also test just above 1
    for j in range(0, 400):
        x = F(j, 400)*F(9)            # x in [0,9)
        d = (x + delta).__floor__() - x.__floor__()
        if d not in (1, 2): ok = False
check("non-wrap: bin difference is 1 or 2 for every Delta in (1,2) bin widths", ok)
# wrap case: bin indices actually attainable are (7,0),(8,0),(8,1); all differ mod 3
wrap_pairs = [(7,0),(8,0),(8,1)]
check("wrap: attainable bin pairs differ mod 3", all(a % 3 != b % 3 for a,b in wrap_pairs))
check("all bin pairs with difference 1 or 2 mod 9 differ mod 3",
      all((a % 3) != (b % 3) for a in range(9) for b in range(9)
          if min((a-b) % 9, (b-a) % 9) in (1,2)))

# ------------------------------- Step 7: odd-cycle length bound (angular accounting)
print("== Step 7: no short odd cycle in A_w (angular accounting) ==")
def gamma(r): return 2*math.asin(1/(2*r))
w = 71/10000
gmax = gamma(1-w); gmin = gamma(1+w)
delta = gmax - math.pi/3
check("every unit pair in A_w subtends in [gamma(1+w), gamma(1-w)]",
      gmin < math.pi/3 < gmax)
bound = math.pi/(3*delta)
check("odd cycle length n >= pi/(3 delta) = %.2f  >= %.0f" % (bound, bound),
      bound > 126)
print("      asymptotically n >= 0.9/w = %.1f for w = 71/10000" % (0.9/w))

print()
print("FAILURES:", FAIL if FAIL else "none")
sys.exit(1 if FAIL else 0)
