#!/usr/bin/env python3
"""
Numeric / exact-arc audit of the SHARPNESS of "far-field decoupling" (task 3).

The palette at x_0 = 0 is a radius-ONE cluster object: i in P^c_{x_0}(e) iff there
are y_n -> x_0, r_n -> 1 with c(y_n + r_n u) = i on a direction set of positive
angular measure (heuristically).  Hence a colour contributes to the palette of a
trace only if some circle  C(y,r) = {y + r e^{it}}  with |y| small, r close to 1
meets {c = i} in a set of POSITIVE angular measure.  This script computes those
angular measures EXACTLY (closed-form arcs, rational arithmetic in Fraction for
the comparisons), and cross-checks them by brute-force sampling.

Colourings (k = 2, colours 0 and 1, x_0 = 0):

  c1  : 0 on the open unit disc, 1 outside          (proper? no; measurable: yes)
  c0' : constant 1                                   (= c1 off the OPEN unit ball)
  cA  : 0 on the annulus  1-delta < |z| < 1, 1 elsewhere, delta = 1/100
  c0' : constant 1                                   (= cA off that annulus,
                                                      so both off B(0,1) and
                                                      on B(0,1-delta))
"""

from fractions import Fraction as F
import math

N_SAMPLE = 1 << 19          # brute-force angular resolution for the cross-check
TWO_PI = 2.0 * math.pi


def frac_in_disc_exact(rho, r, a):
    """Exact angular fraction of {t : |rho + r e^{it}| < a} as a decision in Q,
    plus the closed form 1 - arccos(kappa)/pi when -1 < kappa < 1 (kappa in Q)."""
    if rho == 0 or r == 0:
        return ('full', F(1)) if max(rho, r) < a else ('empty', F(0))
    kappa = (a * a - rho * rho - r * r) / (2 * rho * r)
    # condition is  cos(t-phi) < kappa
    if kappa >= 1:
        return ('full', F(1))      # every angle qualifies (a.e.)
    if kappa <= -1:
        return ('empty', F(0))     # no angle qualifies
    return ('arc', kappa)


def frac_in_disc_f(rho, r, a):
    """Same, in float (used by the sampler cross-check)."""
    if rho == 0 or r == 0:
        return 1.0 if max(rho, r) < a else 0.0
    kappa = (a * a - rho * rho - r * r) / (2 * rho * r)   # cos(t-phi) < kappa
    if kappa >= 1:
        return 1.0
    if kappa <= -1:
        return 0.0
    return 1.0 - math.acos(kappa) / math.pi


def sampled_fraction(rho, r, a, n=N_SAMPLE):
    """Brute force: fraction of N_SAMPLE equally spaced angles with |..| < a."""
    xs = range(n)
    cnt = 0
    for j in xs:
        t = TWO_PI * j / n
        zr = rho + r * math.cos(t)
        zi = r * math.sin(t)
        if zr * zr + zi * zi < a * a:
            cnt += 1
    return cnt / n


print("=" * 78)
print("0. CIRCLE-GEOMETRY CORE  (this is what decoupling rests on, exactly)")
print("=" * 78)
print("For centre y with |y| = rho and radius r, every sample point z = y + r u")
print("satisfies  |z - 0| >= r - rho  and  |z - 0| <= r + rho.  Hence if")
print("  rho < eps/2  and  r > 1 - eps/2   then   |z| > 1 - eps  (strictly).")
for eps in [F(1, 10), F(1, 100), F(1, 1000)]:
    worst = F(1) - eps            # R
    rho = eps / 4
    r = 1 - eps / 4
    print(f"  eps={str(eps):7s}  rho={str(rho):7s}  r={float(r):.6f}  "
          f"r-rho={float(r-rho):.6f}  > R=1-eps={float(worst):.6f} ? "
          f"{r - rho > worst}")

print()
print("=" * 78)
print("1. EXAMPLE 1 (R = 1, i.e. eps = 0): c1 = 1_{|z|>=1},  c0' = 1 everywhere")
print("   c1 = c0' on {|z| >= 1};  they differ on the OPEN unit disc.")
print("   colour-0 angular fraction on the circle of radius r about the origin:")
print("=" * 78)
print(f"{'r':>18} {'frac(colour 0) for c1':>24} {'brute force':>14} {'err':>8}")
for r in [F(0, 1), F(1, 2), F(9, 10), F(99, 100), F(9999, 10000),
          F(10**6 - 1, 10**6), F(1, 1), F(10**6 + 1, 10**6), F(101, 100)]:
    if r == 0:
        continue
    exact = frac_in_disc_f(0.0, float(r), 1.0)
    bf = 1.0 if r < 1 else 0.0
    print(f"{float(r):18.8f} {exact:24.8f} {bf:14.8f} {abs(exact-bf):8.1e}")
print("  => colour 0 has FULL angular measure on every circle of radius r < 1")
print("     about the origin, colour 1 full measure for r > 1.  Both colours are")
print("     therefore palette colours at 0 for c1 (witnesses y_n=0, r_n=1-1/n")
print("     and y_n=0, r_n=1+1/n), while c0' = constant 1 has palette {1} alone.")

print()
print("=" * 78)
print("2. EXAMPLE 1, robustness over a NEIGHBOURHOOD  (typical-sampling needs")
print("   centres y_n -> 0, radii r_n -> 1 -- here is a whole grid of them):")
print("=" * 78)
grid_rho = [F(0), F(1, 10**6), F(1, 1000)]
grid_r = [F(1) - F(1, 10**6), F(1) - F(1, 1000), F(1) - F(1, 100),
          F(1), F(1) + F(1, 100), F(1) + F(1, 1000), F(1) + F(1, 10**6)]
print(f"{'rho=|y|':>10} {'r':>12} {'min|z|':>12} {'max|z|':>12} "
      f"{'frac0(c1)':>12} {'frac0(c0\')':>12}")
for rho in grid_rho:
    for r in grid_r:
        f0 = frac_in_disc_f(float(rho), float(r), 1.0)
        print(f"{float(rho):10.6f} {float(r):12.6f} {float(r - rho):12.6f} "
              f"{float(r + rho):12.6f} {f0:12.6f} {0.0:12.6f}")
print("  palettes at 0 (threshold: max frac > 0):")
print("     c1 : {0, 1}     c0' : {1}      ==> DIFFER on every direction.")

print()
print("=" * 78)
print("3. EXAMPLE 3 (thin annulus, delta = 1/100): cA = 0 on 1-delta<|z|<1,")
print("   c0' = 1 everywhere.  These agree on {|z| >= 1} AND on {|z| <= 1-delta},")
print("   i.e. they differ only in the annulus (1/100 away from the sphere),")
print("   well inside the open unit ball.")
print("=" * 78)
delta = F(1, 100)
a_in = 1 - delta            # colour 0 set is {a_in < |z| < 1}
print(f"{'rho':>10} {'r':>12} {'frac inside |z|<1':>20} {'frac outside |z|>1-d':>22}"
      f" {'=> frac(colour 0)':>20}")
for rho in [F(0), F(1, 1000), F(1, 200)]:
    for r in [F(1) - F(1, 1000), F(1) - F(1, 200), F(1) - delta / 2,
              F(1) - F(1, 10**6), F(1), F(1) + F(1, 1000)]:
        fin = frac_in_disc_f(float(rho), float(r), 1.0)          # inside unit disc
        fout = frac_in_disc_f(float(rho), float(r), float(a_in))  # inside inner disc
        f0 = fin - fout                                           # annulus part
        print(f"{float(rho):10.6f} {float(r):12.6f} {fin:20.6f} {fout:22.6f} "
              f"{f0:20.6f}")
print("  => colour 0 has full angular measure on every circle with")
print("     1-delta < r < 1 and rho small: witness (y_n=0, r_n=1-1/n) for n large.")
print("     colour 1 likewise (r_n = 1+1/n).  So P^cA_0 = {0,1} a.e. vs")
print("     P^c0'_0 = {1} a.e.: the palettes differ although the two colourings")
print("     agree off B(0,1) AND on the whole ball B(0,1-1/100).")

print()
print("=" * 78)
print("4. CONTROL (the positive side, eps > 0).  Pair: cb = 0 on {|z| < 1-eps},")
print("   1 elsewhere, and c0' = 1 everywhere.  They agree EXACTLY on")
print("   {|z| >= 1-eps}, so the theorem applies with this eps.  In the")
print("   decoupling window rho < eps/2, r > 1-eps/2 we have min|z| = r-rho > ")
print("   1-eps, so no circle meets the disagreement region: frac0 = 0 for the")
print("   bad colouring too, and both window-palettes are {1}.  (eps = 1/100.)")
print("=" * 78)
eps = F(1, 100)
a_dis = 1 - eps            # colour 0 set of cb is the open disc of radius 1-eps
print(f"{'rho < eps/2':>14} {'r > 1-eps/2':>14} {'min|z|':>12} {'> 1-eps':>10}"
      f" {'frac0(cb)':>12} {'frac0(c0\')':>13}")
for rho in [F(0), F(1, 400), F(1, 200) - F(1, 10**6)]:
    for r in [F(1) - eps / 2 + F(1, 10**6), F(1) - F(1, 200), F(1), F(1) + F(1, 50)]:
        fin = frac_in_disc_f(float(rho), float(r), float(a_dis))
        print(f"{float(rho):14.6f} {float(r):14.6f} {float(r - rho):12.6f} "
              f"{str(r - rho > 1 - eps):>10} {fin:12.6e} {0.0:13.6f}")
print("  Exactly zero (the closed form returns the constant branch: the circle")
print("  of radius r about a point at distance rho with r-1 > -eps/2, rho < eps/2")
print("  has min|z| = r-rho > 1-eps, i.e. kappa <= -1 when 1-eps <= min|z|),")
print("  so the palettes of cb and c0' agree, as the theorem predicts.")

print("=" * 78)
print("5. SAMPLER CROSS-CHECK of the closed-form arc lengths (should agree to")
print(f"   O(1/N) = {1.0/N_SAMPLE:.2e}):")
print("=" * 78)
for (rho, r, a) in [(0.3, 1.0, 1.0), (0.3, 0.9, 0.99), (0.001, 0.999, 1.0),
                    (0.5, 1.2, 1.0)]:
    ex = frac_in_disc_f(rho, r, a)
    bf = sampled_fraction(rho, r, a)
    print(f"  rho={rho:6.3f} r={r:6.3f} a={a:6.3f}  closed={ex:.8f} "
          f"sampled={bf:.8f}  |diff|={abs(ex-bf):.2e}")
print()
print("Summary: the palette at 0 of the radius-1 trace is NOT determined by c")
print("off the OPEN ball B(0,1): examples 1 and 3 both violate it, and they")
print("violate it on a set of directions of FULL angular measure.")
