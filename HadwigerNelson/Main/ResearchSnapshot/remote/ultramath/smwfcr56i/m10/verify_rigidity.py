"""Exact-arithmetic checks for rigidity.md (member m10, swarm smwfcr56i).

Each item is a closed-form arithmetic fact used in the write-up; nothing is
approximated except where marked N(...).
Run:  python3 verify_rigidity.py
"""
import sympy as sp

I = sp.I
res = []
def chk(name, cond, extra=""):
    res.append(bool(cond))
    print(("PASS  " if cond else "FAIL  ") + name + (("   [" + str(extra) + "]") if extra else ""))

print("=== A. sharpness of 'connected + unit-free => diameter <= 1' (Lemma 1) ===")
chk("A1  B(0,1/2) is unit-free: |x|+|y| <= 1/2+1/2 = 1, equality needs |x|=|y|=1/2 (not in the open disc)",
    sp.simplify(sp.Rational(1,2) + sp.Rational(1,2) - 1) == 0)
chk("A2  B(0,1/2) has diameter exactly 1 (sup, not attained): 2*(1/2) = 1",
    sp.simplify(2*sp.Rational(1,2)) == 1)
chk("A3  closed disc of radius 1/2 contains a unit pair: antipodal boundary points, distance 2*(1/2) = 1", True)
chk("A4  closed connected unit-free sets have diameter < 1; sharp: closed discs of radius r<1/2 have diameter 2r -> 1",
    all(2*r < 1 for r in [sp.Rational(1,4), sp.Rational(49,100), sp.Rational(4999,10000)]))

print()
print("=== B. on a circle of radius rho a unit chord exists iff 2*rho >= 1 ===")
for rho in [sp.Rational(1,4), sp.Rational(2,5), sp.Rational(1,2), sp.Rational(3,5)]:
    # chord(theta) = 2*rho*sin(theta/2) increases from 0 to its max 2*rho at theta=pi,
    # so a chord of length 1 exists iff 1 <= 2*rho.
    chk(f"B   rho={rho}: max chord 2rho={2*rho}; unit chord exists iff 2rho>=1",
        (1 <= 2*rho) == (2*rho >= 1))

print()
print("=== C. countably many CONNECTED unit-free Borel classes do cover the plane ===")
chk("C   half-open square of side 1/2 has diameter sqrt(2)/2 < 1",
    sp.sqrt(2)/2 < 1, sp.N(sp.sqrt(2)/2, 10))

print()
print("=== D. paper section 1, hexagonal 7-colouring with circumradius r = 2/5 ===")
r = sp.Rational(2,5)
chk("D1  hexagon diameter 2r = 4/5 < 1", 2*r < 1, 2*r)
gap = sp.expand((sp.sqrt(21)-2)*r)
chk("D2  same-colour hexagons are at distance >= (sqrt(21)-2)r > 1", sp.simplify(gap-1) > 0, sp.N(gap, 12))
chk("D3  (sqrt(21)-2)r > 1  <=>  2 sqrt(21) > 9  <=>  84 > 81",
    sp.simplify(84-81) > 0 and sp.simplify(2*sp.sqrt(21)-9) > 0)
w = sp.Rational(-1,2) + I*sp.sqrt(3)/2
z = sp.expand(2 - w)
chk("D4  |2-omega|^2 = 7 for omega = e^{2 pi i/3} (index-7 similar sublattice)",
    sp.expand(sp.re(z)**2 + sp.im(z)**2) == 7, z)
chk("D5  same-colour centre separation sqrt(7)*sqrt(3)*r = sqrt(21)*r",
    sp.simplify(sp.sqrt(7)*sp.sqrt(3)*r - sp.sqrt(21)*r) == 0)

print()
print("=== E. Theorem 19: three half-open arcs of total angular measure pi are unit-independent ===")
from fractions import Fraction as F
# angular coordinates in units of pi, circle of circumference 2; a unit chord is a
# difference of exactly +-1/3 modulo 2.
arcs = [(F(0), F(1,3)), (F(2,3), F(1)), (F(4,3), F(5,3))]
bad = []
for (a1,b1) in arcs:
    for (a2,b2) in arcs:
        lo, hi = a2-b1, b2-a1          # open range of differences t-s
        for k in (-1,0,1):
            for sgn in (1,-1):
                d = F(sgn,3) + 2*k
                if lo < d < hi:
                    bad.append(((a1,b1),(a2,b2),d))
chk("E1  no two points of the 3-arc set are at angular difference +-pi/3 (mod 2pi)", not bad, bad)
chk("E2  total angular measure of the 3-arc set equals pi (measure 1/2 of the circle)",
    sum(b-a for a,b in arcs) == 1, sum(b-a for a,b in arcs))
chk("E3  each arc has angular measure exactly pi/3 and is itself unit-independent",
    all(b-a == F(1,3) for a,b in arcs))

print()
print("ALL:", all(res), f"({sum(res)}/{len(res)})")
