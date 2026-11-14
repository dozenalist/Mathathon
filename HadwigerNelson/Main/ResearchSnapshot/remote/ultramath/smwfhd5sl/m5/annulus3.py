"""A three-valued strip with no unit pair that is nowhere essentially constant.

This refutes the only natural repair at k = 6 of the step that carries Section 8.4-8.6
at k = 5 (paper Lemma 8.6, local constancy of the outsider state, whose proof uses that
the strip is coloured by a *pair* {X,Y}: the five-vertex path of (8.3) alternates).

Object.  w = 1/20 and  A = { z : 19/20 < |z| < 21/20 }.  Put, for z != 0,
             f(z) = floor( 9 * arg(z) / (2 pi) )  mod 3,     arg(z) in [0, 2 pi).
So A is cut into nine half-open sectors of angle 2 pi/9, coloured 0,1,2,0,1,2,0,1,2.

Claim 1.  f(z) = f(z') and |z - z'| = 1 have no solution with z, z' in A.
Claim 2.  f is not essentially constant on any angular neighbourhood of any point of A.
          (In fact on any arc of angle > 2 pi/9 it takes two values on sets of positive
          measure.)

Proof of Claim 1 (exact, all steps rational).  Write r = |z|, r' = |z'| and let
Delta in [0, pi] be the angle between them.  The law of cosines gives
      cos Delta = g(r,r') = (r^2 + r'^2 - 1) / (2 r r').
Step 1.  On [19/20, 21/20]^2 the function g has no interior critical point: grad g = 0
forces r^2 = r'^2 - 1, i.e. r = sqrt(r'^2-1); but r' <= 21/20 gives r'^2 - 1 <= 41/400,
so r <= sqrt(41/400) < 19/20.  Hence the range of g is the range on the boundary, and a
one-variable check on each of the four edges gives
      161/361  <=  cos Delta  <=  241/441.                                  (S1)
Step 2.  If f(z) = f(z') then the sector indices are congruent modulo 3, so the signed
difference of arguments lies within 2 pi/9 of a multiple of 2 pi/3; for the unsigned
Delta in [0,pi] this says
      Delta in (0, 2 pi/9)  or  Delta in (4 pi/9, 8 pi/9).                  (S2)
Step 3.  cos is strictly decreasing on [0,pi], so (S1) gives
      Delta in [arccos(241/441), arccos(161/361)].
Now
      cos(2 pi/9) > 11/20 > 241/441      (so Delta > 2 pi/9), and
      cos(4 pi/9) < 7/25 < 161/361       (so Delta < 4 pi/9),
which contradicts (S2).  QED

The three numerical facts, each exactly:
 (a) 8 c^3 - 6 c + 1 = 0 for c = cos(2 pi/9), from cos 3x = 4c^3 - 3c and cos(2 pi/3)
     = -1/2.  p(x) = 8x^3 - 6x + 1 satisfies p(11/20) = -969/1000 < 0 < p(4/5) = 37/125
     and p' = 24x^2 - 6 > 0 on [11/20, 4/5], so p has exactly one root there; the three
     roots are cos(2 pi/9) > cos(4 pi/9) > cos(8 pi/9) because 2 pi/9 < 4 pi/9 < 8 pi/9
     <= pi and cos is strictly decreasing on [0, pi]; the largest root is the one in
     (11/20, 4/5).  Hence 11/20 < cos(2 pi/9) < 4/5.
 (b) cos(4 pi/9) = 2 cos^2(2 pi/9) - 1 < 2*(4/5)^2 - 1 = 7/25.
 (c) 241/441 < 11/20 and 7/25 < 161/361.

Run: python3 annulus3.py    (prints the rational certificate and a numerical sweep)
"""

from fractions import Fraction as F

W = F(1, 20)
RLO, RHI = 1 - W, 1 + W          # 19/20, 21/20


def g(r, rp):
    return (r * r + rp * rp - 1) / (2 * r * rp)


def boundary_analysis():
    """Exact range of g on the closed square [RLO,RHI]^2, by edges."""
    vals = {}
    for a in (RLO, RHI):
        for b in (RLO, RHI):
            vals[(a, b)] = g(a, b)
    return vals


def main():
    print(f"annulus: {float(RLO):.6f} < |z| < {float(RHI):.6f}, "
          f"w = {W}")

    # ---- Step 1: g has no interior critical point
    # grad g = 0  <=>  r^2 = r'^2 - 1 and r'^2 = r^2 - 1, impossible.
    # (indeed r^2 = r'^2 - 1 => r' >= 1 and r = sqrt(r'^2-1) <= sqrt(RHI^2-1) < RLO)
    rmax_sq = RHI * RHI - 1
    assert rmax_sq < RLO * RLO, "interior critical point not excluded"
    print(f"no interior critical point: max r over r^2=r'^2-1 is "
          f"{float(rmax_sq) ** 0.5:.6f} < {float(RLO):.6f}")

    # ---- Step 1 (cont.): the four edges, monotone in the second variable
    corners = boundary_analysis()
    gmin = min(corners.values())
    gmax = max(corners.values())
    # one-variable checks: on each edge the map is monotone, so corners suffice;
    # verify monotonicity exactly by sign of the derivative numerator on the edge
    # edge r = a:  d/dr' g = (r'^2 + 1 - a^2) / (2 a r'^2)  > 0  since a^2 <= RHI^2 < 1 + RLO^2
    assert RHI * RHI < 1 + RLO * RLO
    print("edge r'=const derivative numerator r^2 + 1 - r'^2 > 0 on the square: "
          f"{float(RLO*RLO + 1 - RHI*RHI):.6f} > 0")
    print(f"range of cos Delta: [{gmin} , {gmax}] = "
          f"[{float(gmin):.6f}, {float(gmax):.6f}]")
    assert gmin == F(161, 361) and gmax == F(241, 441)

    # ---- Step 3: the two bounds
    assert gmax < F(11, 20) < 1, "need cos(2pi/9) > 11/20 > gmax"
    assert F(7, 25) < gmin, "need cos(4pi/9) < 7/25 < gmin"
    print(f"241/441 = {float(gmax):.6f} < 11/20 = 0.55 < cos(2pi/9)  =>  Delta > 2pi/9")
    print(f"161/361 = {float(gmin):.6f} > 7/25 = 0.28  > cos(4pi/9)  =>  Delta < 4pi/9")

    # ---- the polynomial certificate for cos(2pi/9)
    def p(x):
        return 8 * x ** 3 - 6 * x + 1
    assert p(F(11, 20)) == F(-969, 1000)
    assert p(F(4, 5)) == F(37, 125)
    print(f"p(11/20) = {p(F(11,20))} < 0 < p(4/5) = {p(F(4,5))}, "
          f"p' = 24x^2-6 > 0 on [11/20,4/5] (24*(11/20)^2-6 = "
          f"{float(24*F(11,20)**2-6):.4f} > 0)")
    print("=> 11/20 < cos(2pi/9) < 4/5,  cos(4pi/9) < 7/25")

    # ---- numerical sweep: sample unit-distance pairs and test the colours
    import math, random
    random.seed(7)
    tested = 0
    same = 0
    worst = 9.0
    def col(th):
        return int(9 * ((th % (2 * math.pi)) / (2 * math.pi))) % 3
    for _ in range(400000):
        r = random.uniform(float(RLO), float(RHI))
        rp = random.uniform(float(RLO), float(RHI))
        cs = (r * r + rp * rp - 1) / (2 * r * rp)
        if abs(cs) > 1:
            continue
        d = math.acos(cs)
        t = random.uniform(0, 2 * math.pi)
        z = (r * math.cos(t), r * math.sin(t))
        zp = (rp * math.cos(t + d), rp * math.sin(t + d))
        assert abs(math.hypot(z[0] - zp[0], z[1] - zp[1]) - 1) < 1e-12
        tested += 1
        if col(t) == col(t + d):
            same += 1
        worst = min(worst, abs(d - 2 * math.pi / 9), abs(d - 4 * math.pi / 9),
                    abs(d - 8 * math.pi / 9))
    print(f"numerical sweep: {tested} unit-distance pairs inside the annulus; "
          f"monochromatic pairs = {same}; closest angular separation to a forbidden "
          f"value = {worst:.4f}")
    assert same == 0
    print("certificate complete")


if __name__ == "__main__":
    main()
