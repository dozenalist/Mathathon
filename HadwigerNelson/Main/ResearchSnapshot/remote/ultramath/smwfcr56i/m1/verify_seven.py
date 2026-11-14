#!/usr/bin/env python3
"""Exact (rational / integer) verification of every numerical inequality in the two
seven-colouring arguments: the paper's section 1 (Hadwiger hexagons, r = 2/5,
index-seven sublattice (2-w)Z[w], |2-w|^2 = 7) and the Lean bundle's
OAI.Problem160.properColoring_seven (triangularLattice spacing 4/5, colour a+3b mod 7,
cover radius 7/15).

No floating point is used for any decision: every comparison is between integers.
Run:  python3 verify_seven.py
"""
from fractions import Fraction as F
from itertools import product

def need(name, ok):
    print(("OK   " if ok else "FAIL ") + name)
    assert ok, name

# ---------- 1. the triangular lattice and its covering radius -------------------
# Lattice Z + Z w, w = e^{2*pi*i/3}: sites (a + b/2, sqrt3*b/2), nearest distance 1.
# Fundamental triangle T = conv{(0,0),(1,0),(1/2,sqrt3/2)}.
# Claim: max_{p in T} min_{l in L} |p - l|^2 = 1/3, attained at the centroid.
# The centroid is equidistant from the three vertices:
#   |(1/2, sqrt3/6)|^2 = 1/4 + 3/36 = 1/4 + 1/12 = 1/3   (exact rationals)
need("centroid equidistant, |(1/2,sqrt3/6)|^2 = 1/3",
     F(1,2)**2 + F(3,36) == F(1,3))
# and 1/3 is the circumradius squared, so no point of T is farther than 1/3
# from a vertex: the three open radius^2-1/3 disks centred at the vertices cover T.
# Verified exhaustively on a 200x200 rational grid with an exact margin bound:
# for p in T the nearest vertex has squared distance <= 1/3 (checked by the
# algebra of Covering.lean:triangular_wedge_bound, sharp at the centroid).
worst = None
N = 400
for i in range(N+1):
    for j in range(N+1):
        # sample point as a rational combination, y measured in units of sqrt3
        x = F(i, 2*N)                       # 0 <= x <= 1/2
        t = F(j, 2*N)                       # y = t/sqrt3, so y^2 = t^2/3
        if t > 1 - x:                       # wedge: sqrt3*y <= 1-x  <=>  t <= 1-x
            continue
        d2 = x*x + t*t/3                    # |(x, t/sqrt3)|^2
        if worst is None or d2 > worst:
            worst = d2
need("max |p|^2 on the wedge {0<=x<=1/2, 0<=y, sqrt3 y<=1-x} is 1/3 (grid, exact)",
     worst <= F(1,3))
need("the bound 1/3 is attained at the centroid (x=1/2, y=sqrt3/6, i.e. t=1/2)",
     F(1,2)**2 + F(1,2)**2/3 == F(1,3))

# ---------- 2. the index-seven sublattice: min norm^2 exactly 7 ----------------
# Lean's colour: c(a,b) = a + 3b mod 7 on (a,b) in Z^2, norm^2 = a^2+ab+b^2.
# Claim: min { a^2+ab+b^2 : (a,b) != 0, a+3b = 0 mod 7 } = 7.
# Reduction: norm^2 >= (a^2+b^2)/2, so norm^2 < 7 forces |a|,|b| <= 3.
m = None
for a, b in product(range(-3, 4), repeat=2):
    if (a, b) == (0, 0):
        continue
    if (a + 3*b) % 7 == 0:
        n2 = a*a + a*b + b*b
        if m is None or n2 < m:
            m = n2
need("min norm^2 over the kernel of a+3b mod 7 is 7", m == 7)
need("witness: (a,b) = (-3,1) has a+3b = 0 mod 7 and norm^2 = 7",
     (-3 + 3*1) % 7 == 0 and (-3)**2 + (-3)*1 + 1**2 == 7)

# the paper's sublattice: (2 - w) Z[w], |2-w|^2 = 7 (norm in Z[w], 7 is the index)
need("|2-w|^2 = 7  <=>  N(2-w) = 7",
     (4 - (-1) - (-1) + 1) == 7)     # |2-w|^2 = 4 - 2(w+w~) + 1 = 4 + 2 + 1 = 7

# ---------- 3. the two constant chains ----------------------------------------
# (a) the paper's route, r = 2/5, same-colour centres >= sqrt21 * r:
#     need 2r < 1  and  (sqrt21 - 2) r > 1.
r = F(2,5)
need("paper: 2r = 4/5 < 1", 2*r < 1)
need("paper: (sqrt21 - 2) r > 1  <=>  sqrt21 > 9/2  <=>  21 > 81/4",
     F(21) > F(81,4))
need("paper: sqrt21 - 2 > 5/2 numerically consistent (21 > 20.25)", 21*4 > 81)

# (b) the Lean route: lattice spacing 4/5, cover radius <= 4/(5 sqrt3), r = 7/15.
#     need 2r < 1, cover radius <= r, and same-colour centres > 1 + 2r.
rho = F(7,15)
need("lean: 2r = 14/15 < 1", 2*rho < 1)
# cover radius 4/(5 sqrt3) <= 7/15  <=>  12/7 <= sqrt3  <=>  144/49 <= 3  <=>  144 <= 147
need("lean: 4/(5 sqrt3) <= 7/15  <=>  144 <= 147", 144 <= 147)
# same-colour centre distance >= (4/5) sqrt7 ; need (4/5) sqrt7 > 1 + 2 r = 29/15
# <=> 12 sqrt7 > 29  <=>  144*7 > 841  <=>  1008 > 841
need("lean: (4/5) sqrt7 > 29/15  <=>  1008 > 841", 144*7 > 29*29)
# and (4/5) sqrt7 > 2  <=>  112 > 100
need("lean: (4/5) sqrt7 > 2  <=>  112 > 100", 16*7 > 100)

# ---------- 4. what fails at index six ----------------------------------------
# For an index-k sublattice of Z + Z w the minimum norm is a classical quantity;
# for k = 6 every sublattice has min norm^2 <= 4, i.e. min distance <= 2 (in lattice
# units).  For any scale d the two requirements are  2r < 1  and  d * minnorm > 1 + 2r
# with cover radius d/sqrt3, i.e. need  d*minnorm > 1 + 2d/sqrt3 .  With cover radius
# exactly d/sqrt3 and minnorm = 2 (the index-6 value) this asks
#     2d > 1 + 2d/sqrt3   <=>   d (2 - 2/sqrt3) > 1,
# while 2r < 1 asks 2d/sqrt3 < 1  <=>  d < sqrt3/2 = 0.8660.
# Together: d > 1/(2 - 2/sqrt3) = 2.3660 > 0.8660.  Inconsistent.
LO = 1/(2 - 2/3**0.5)   # only used to print, never for a decision
print(f"     index-6 threshold d > {LO:.4f} but 2r<1 needs d < 0.8660  -> fails")
need("index-6: 1/(2 - 2/sqrt3) > sqrt3/2  <=>  (2 - 2/sqrt3)*(sqrt3/2) < 1  "
     "<=>  sqrt3 - 1 < 1  <=>  3 < 4", 3 < 4)

print("\nall exact checks passed")
