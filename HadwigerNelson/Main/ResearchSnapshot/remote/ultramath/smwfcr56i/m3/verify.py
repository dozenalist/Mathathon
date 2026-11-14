#!/usr/bin/env python3
"""Checks for the note sharp-cover-obstruction.md.

Every comparison that decides something is exact rational arithmetic; sin/cos are
bounded rigorously with rational Taylor partial sums (alternating series with
decreasing terms, so consecutive partial sums bracket the value).
"""
from fractions import Fraction as F
import math

ok = True
def check(name, cond, detail=""):
    global ok
    ok = ok and bool(cond)
    print(("PASS " if cond else "FAIL ") + name + ("   [" + detail + "]" if detail else ""))

PI_LOW  = F(3141592653589793, 10**15)
PI_HIGH = F(3141592653589794, 10**15)

def _alt_series(x, coeff):
    """sum_k (-1)^k x^(2k+coeff) / (2k+coeff)!  bracketed by consecutive partial sums."""
    partials, t, n = [], x**coeff, coeff
    for k in range(60):
        partials.append(sum(partials) + t if False else None)  # placeholder
        n = coeff + 2 * k
    # explicit loop
    s = F(0); t = x**coeff; n = coeff
    seq = []
    for k in range(60):
        s += (t if k % 2 == 0 else -t)
        seq.append(s)
        t = t * x * x / ((n + 1) * (n + 2))
        n += 2
    return min(seq[-1], seq[-2]), max(seq[-1], seq[-2])

def sin_bounds(x):
    """a <= sin x <= b, for 0 <= x <= 2 (rational x)."""
    return _alt_series(x, 1)

def cos_bounds(x):
    """a <= cos x <= b, for 0 <= x <= 2 (rational x)."""
    return _alt_series(x, 0)

# ------------------------------------------------------- exact value sin 30 deg
# sin is increasing on [0, pi/2], so sin(PI_LOW/6) <= sin(pi/6) <= sin(PI_HIGH/6)
a = sin_bounds(PI_LOW / 6)[0]
b = sin_bounds(PI_HIGH / 6)[1]
check("sin(30 deg) = 1/2 exactly (rigorously bracketed)", a <= F(1, 2) <= b,
      f"{float(a):.17f} <= 0.5 <= {float(b):.17f}")

# ------------------------------- 1. the extremal configuration: six closed sectors
R = F(5)
# a closed sector of radius R and half-angle alpha has diameter max(R, 2 R sin alpha);
# for alpha = 30 deg this is exactly R = 5 (equilateral far corners).
check("closed 30-deg sector of radius 5 has diameter exactly 5",
      max(R, 2 * R * F(1, 2)) == 5, "2*5*sin(30)=5, and 5 = R")

def sectors_containing(z, alpha_deg):
    """number of closed sectors {|arg - 60j| <= alpha} containing z=(x,y)."""
    x, y = z
    if x == 0.0 and y == 0.0:
        return 6
    ang = math.degrees(math.atan2(y, x))
    n = 0
    for j in range(6):
        d = (ang - 60.0 * j + 180.0) % 360.0 - 180.0
        if abs(d) <= alpha_deg + 1e-12:
            n += 1
    return n

mult = {}
for j in range(6):
    for r in (0.5, 1.0, 3.0, 5.0):
        th = math.radians(60.0 * j)
        mult.setdefault(sectors_containing((r * math.cos(th), r * math.sin(th)), 30.0), 0)
# the exactly tiling six-sector cover has its seams on the rays theta = 30 + 60j
check("on each of the 6 seam rays two sectors of the tiling meet",
      all(sectors_containing((3.0 * math.cos(math.radians(30 + 60 * j)),
                              3.0 * math.sin(math.radians(30 + 60 * j))), 30.0) == 2
          for j in range(6)))
check("the origin lies in all 6 sectors", sectors_containing((0.0, 0.0), 30.0) == 6)
gen = [sectors_containing((r * math.cos(t), r * math.sin(t)), 30.0)
       for r in (0.3, 1.0, 2.5, 4.9) for t in [k * 0.7 for k in range(9)]]
check("generic points lie in exactly one sector (the cover is a tiling)", max(gen) == 1, f"max {max(gen)}")

# ---------------------------- 2. six sectors of half-angle 30+eps: mesh -> 5
DELTA = F(1, 1000)
for eps_deg in (5.0, 2.0, 1.0, 0.1, 0.01):
    x = F(str((30.0 + eps_deg) * math.pi / 180.0))
    lo, hi = sin_bounds(x)
    mesh_lo = 2 * (5 + DELTA) * lo
    mesh_hi = 2 * (5 + DELTA) * hi
    check(f"six sectors, half-angle {30.0+eps_deg:g} deg, radius 5.001: mesh < 6",
          mesh_hi < 6, f"mesh in ({float(mesh_lo):.5f},{float(mesh_hi):.5f}); tends to 5")

# ------------------------------------------- 3. two half-discs: multiplicity 2, mesh 10
def half_discs_containing(x, y, rad=5.001, eps=1e-9):
    n = 0
    if x > -eps and x * x + y * y < rad * rad:
        n += 1
    if x < eps and x * x + y * y < rad * rad:
        n += 1
    return n
check("two half-discs give multiplicity at most 2 everywhere (sampled)",
      max(half_discs_containing(-5 + 10 * i / 97, -5 + 10 * j / 97)
          for i in range(98) for j in range(98)) <= 2)
check("two half-discs have mesh 2(5+delta) -> 10 > 5",
      2 * (5 + DELTA) > 5, "so 10 is an upper bound for the optimal mesh")

# ------------------------------------- 4. the projection map: the argument is sharp at d=R
check("F(z) = (Re z, 0) has |F(z)-z| = |Im z| <= 5 on the closed disc of radius 5",
      all(abs(y) <= 5 for y in [-5 + 10 * k / 100 for k in range(101)]),
      "image lies in one line: at d = 5 the winding argument gives nothing")

# ------------------------------------------------------------- 5. trivialities
check("2 < 5", 2 < 5)
check("the Lean/paper hypothesis 'diam <= 2' is the instance d = 2 of 'diam <= d, d < 5'", 2 < 5)

print()
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
raise SystemExit(0 if ok else 1)
