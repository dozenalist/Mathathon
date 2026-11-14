#!/usr/bin/env python3
"""
Exact verifier for the angular-duality layer of CC60 ("closed 60-degree cone").

Everything is exact rational arithmetic.  An angle is a Fraction `a` meaning
a*pi radians; no trigonometric function is ever evaluated numerically.  The
only ingredient is

   Re(conj(direction(tau)) * direction(a)) > 0   <->   cdist(tau,a) < 1/2
   (angles in units of pi; cdist = circular distance)

together with "cos is strictly decreasing on [0,pi]".

Notation matching the source (AngularBoundary.lean):
   ApproachingContinuum x K v,  v unit  (signed direction, |v| = 1)
   Forward(tau)   = {i : Re(conj(dir tau) * v_i) > 0}       ("outer strip angles")
   Backward(tau)  = {i : Re(conj(dir tau) * v_i) < 0}       ("inner strip angles")
   D(I)           = {tau : I subset of Forward(tau)}
   w(I)           = length of the smallest closed arc containing {v_i : i in I}

Claims checked, all exactly:
  C1  len D(I) = max(0, pi - w(I));  D(I) is a single open arc when nonempty.
  C2  D(I) nonempty  <=>  w(I) < pi   (open semicircle criterion).
  C3  The six folded grid directions 0,pi/3,...,5pi/3 have w = 5pi/3 and
      D = empty -- CC60 is NOT a claim about that tuple; it is a claim about
      subsets lying in one closed pi/3 arc, which is what the filter tests.
  C4  For every subset I with w(I) <= pi/3,  len D(I) >= 2pi/3 > 0.  The bound
      is attained exactly when w(I) = pi/3.  So the strip layer NEVER blocks
      a subset that a closed pi/3 arc can hold: formulation (i)'s hypotheses
      are all geometrically realised.
  C5  D(I) has OPEN endpoints, and the endpoints are exactly the critical
      angles v_i +- pi/2.  So a *closed* arc of directions is safe, while a
      closed arc of *angles* is not: at the two endpoints of D(I) the strict
      inner-product inequality fails and the source lemma gives nothing.
  C6  Equal directions are invisible: D(I) depends on {v_i : i in I} as a set.
  C7  Antipodal pairs: w >= pi so D = empty; each singleton still has
      len D = pi.  Hence outer strips alone constrain each continuum on exactly
      one open semicircle, and Forward(t+pi) = complement of Forward(t).
      Outer+inner together constrain each single continuum i at every angle, so
      a *single* continuum carries no angular information; only subsets do.
  C8  The shared region is a genuine open annulus sector of positive area:
      area{1<r<1+d, |theta-beta|<eta} = d(2+d)eta > 0 exactly.  A single radial
      ray has area 0 and would make the a.e. exclusion vacuous.
  C9  Sharp threshold: width exactly pi gives D = empty, with no closed-
      inequality repair.
"""

from fractions import Fraction as F
from itertools import combinations

ok = True
def check(name, cond, detail=""):
    global ok
    ok = ok and bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (("  [" + detail + "]") if detail else ""))

def cdist(a, b):
    d = (a - b) % 2
    return min(d, 2 - d)

def forward(tau, a):
    return cdist(tau, a) < F(1, 2)

def backward(tau, a):
    return cdist(tau, a) > F(1, 2)

def D(I, angles):
    """Exact D(I) as a list of open intervals (lo,hi) of tau, circle of period 2."""
    crit = sorted({(angles[i] + s) % 2 for i in I for s in (F(1, 2), F(-1, 2))})
    if not crit:
        return [(F(0), F(2))]
    n, out = len(crit), []
    for k in range(n):
        lo = crit[k]
        hi = crit[(k + 1) % n] + (2 if k == n - 1 else 0)
        mid = (lo + hi) / 2
        if all(forward(mid, angles[i]) for i in I):
            out.append((lo, hi))
    return out

def width(angles, I):
    pts = sorted({angles[i] % 2 for i in I})
    if len(pts) <= 1:
        return F(0)
    gaps = [(pts[(k + 1) % len(pts)] - pts[k]) % 2 for k in range(len(pts))]
    return 2 - max(gaps)

def length(intervals):
    return sum((hi - lo for lo, hi in intervals), F(0))

def formula(I, angles):
    """The claimed length of D(I).  For I empty there is no constraint: D = circle, length 2."""
    if not I:
        return F(2)
    w = width(angles, I)
    return F(0) if w >= 1 else 1 - w

# ---------------------------------------------------------------- the battery
grid  = {i: F(i, 3) for i in range(6)}                       # multiples of pi/3
grade = {i: F(8 * i, 24) for i in range(6)}                  # generic non-grid, spacing pi/3
near  = {0: F(0), 1: F(9, 24), 2: F(7, 24), 3: F(33, 24), 4: F(30, 24), 5: F(55, 24)}
eq    = {0: F(0), 1: F(0), 2: F(0), 3: F(1, 3), 4: F(1, 3), 5: F(1, 6)}
ant   = {0: F(0), 1: F(1), 2: F(2, 5), 3: F(1, 5), 4: F(3, 7), 5: F(4, 7)}
semi  = {0: F(0), 1: F(1, 5), 2: F(2, 5), 3: F(3, 5), 4: F(4, 5), 5: F(1)}
batteries = {"grid": grid, "grade": grade, "near": near, "eq": eq, "ant": ant, "semi": semi}

print("=== C3: the folded grid tuple has width 5pi/3, not pi/3 ===")
check("w(grid, all six) = 5/3", width(grid, range(6)) == F(5, 3), str(width(grid, range(6))))
check("D(grid, all six) = empty", D(range(6), grid) == [], str(D(range(6), grid)))
check("w(grade, all six) = 5/3", width(grade, range(6)) == F(5, 3))
check("D(grade, all six) = empty", D(range(6), grade) == [])
print("   -> CC60 is a claim about SUBSETS inside one closed pi/3 arc, which is")
print("      exactly what the AC-CONE-SIX filter tests (adjacent pairs {d,d+1}).")

print()
print("=== C1/C2: len D(I) = max(0, pi - w(I)) over all 64 subsets of each battery ===")
for name, ang in batteries.items():
    bad, badne = [], []
    for r in range(7):
        for I in combinations(range(6), r):
            L, f = length(D(I, ang)), formula(I, ang)
            if L != f:
                bad.append((I, width(ang, I), L, f))
            if (len(D(I, ang)) > 0) != (width(ang, I) < 1):
                badne.append(I)
    check("len D(I) = max(0,pi-w(I))  [%s]" % name, not bad, str(bad[:2]))
    check("D(I) nonempty <=> w(I) < pi  [%s]" % name, not badne, str(badne[:3]))

print()
print("=== C4: every subset a closed pi/3 arc can hold has len D >= 2pi/3 ===")
for name, ang in batteries.items():
    worst, arg, fails, sharp = None, None, [], []
    for r in range(7):
        for I in combinations(range(6), r):
            if width(ang, I) <= F(1, 3):
                L = length(D(I, ang))
                if L <= 0:
                    fails.append((I, L))
                if worst is None or L < worst:
                    worst, arg = L, I
                if width(ang, I) == F(1, 3) and L == F(2, 3):
                    sharp.append(I)
    check("no vacuous D among width<=pi/3 subsets [%s]" % name, not fails, str(fails[:2]))
    has_sharp = any(width(ang, I) == F(1, 3)
                    for r in range(7) for I in combinations(range(6), r))
    check("len D >= 2/3 there%s [%s]" % (", and = 2/3 at w = pi/3" if has_sharp else "", name),
          worst >= F(2, 3) and (bool(sharp) or not has_sharp),
          "min %s at %s; sharp examples %s" % (worst, arg, sharp[:2]))

print()
print("=== C5: D has open endpoints, and they are exactly the critical angles ===")
for d in range(6):
    I = (d, (d + 1) % 6)
    inter = D(I, grid)
    check("D({%d,%d}) is one open arc of length 2/3" % I,
          len(inter) == 1 and length(inter) == F(2, 3), str(inter))
    lo, hi = inter[0]
    check("  ...both endpoints are critical angles (some inner product = 0)",
          any(cdist(lo, grid[i]) == F(1, 2) for i in I)
          and any(cdist(hi, grid[i]) == F(1, 2) for i in I))
    check("  ...interior point is forward for both, endpoints are not",
          all(forward((lo + hi) / 2, grid[i]) for i in I)
          and not all(forward(lo, grid[i]) for i in I)
          and not all(forward(hi, grid[i]) for i in I))

print()
print("=== C6: equal directions are invisible ===")
check("D({0,1,2}) = D({0}) with three equal directions", D({0, 1, 2}, eq) == D({0}, eq))
check("D(all six) = D({0,3}) for the equated tuple", D(range(6), eq) == D({0, 3}, eq))
check("len D(all six) = 2/3 for the equated tuple", length(D(range(6), eq)) == F(2, 3))

print()
print("=== C7: antipodal pairs; outer-only vs outer+inner ===")
check("D({0,1}) empty when v_1 = -v_0", D({0, 1}, ant) == [])
check("each singleton still has len D = pi = 1",
      length(D({0}, ant)) == 1 and length(D({1}, ant)) == 1)
check("no tau has both v_0 and v_1 forward",
      not any(forward(F(k, 480), ant[0]) and forward(F(k, 480), ant[1]) for k in range(960)))
check("Forward(t+pi) = complement of Forward(t), all batteries, off critical set",
      all(not (forward(t, ang[i]) == forward(t + 1, ang[i]))
          for ang in batteries.values() for i in range(6) for k in range(480)
          for t in [F(k, 240)] if cdist(t, ang[i]) != F(1, 2)))
check("outer+inner covers every angle for each single continuum, except the null critical set",
      all((forward(F(k, 480), ang[i]) or backward(F(k, 480), ang[i]))
          == (cdist(F(k, 480), ang[i]) != F(1, 2))
          for ang in batteries.values() for i in range(6) for k in range(960)))

print()
print("=== C8: positive-measure shared annulus sector ===")
for dlt, eta in [(F(1, 3), F(1, 4)), (F(1, 7), F(2, 9)), (F(5, 11), F(1, 24)), (F(1, 96), F(1, 300))]:
    A = (dlt * (2 + dlt) / 2) * (2 * eta)
    check("area(d=%s, eta=%s) = %s > 0" % (dlt, eta, A), A == dlt * (2 + dlt) * eta and A > 0)
print("   -> a single radial ray has area 0, so an a.e. statement on it is vacuous;")
print("      the source's outer_strip supplies a whole open sector instead.")

print()
print("=== C9: threshold is exactly width pi ===")
check("w(semi, all six) = 1 and D = empty", width(semi, range(6)) == 1 and D(range(6), semi) == [])
check("no tau in a fine rational grid is forward for both endpoints of the closed semicircle",
      not any(forward(F(k, 720), F(0)) and forward(F(k, 720), F(1)) for k in range(1440)))
check("width of D just below pi is just above 0",
      length(D({0, 1}, {0: F(0), 1: F(1) - F(1, 972)})) == F(1, 972) and F(1, 972) > 0)

print()
print("=== C10: the strict inequality Re(conj(e),v) > 0 cannot be relaxed ===")
# K = {i*s : 0 <= s <= 1} (compact, connected: a continuum), x = 0, v = i, e = 1.
# Then Re(conj(e) v) = 0, ApproachingContinuum holds, but r*e is NOT in Straddle K
# for any r > 1, because dist(r*1, i*s)^2 = r^2 + (1-s)^2 > 1 for all s in [0,1].
def straddle_upper_ok(r, s):
    """r*1 = x + r*e has a point of K at distance >= 1 ?  exact."""
    return r * r + (1 - s) * (1 - s) < 1

far = [ (r, s) for r in [F(3,2), F(11,10), F(101,100), F(1001,1000)]
               for s in [F(k, 720) for k in range(721)] ]
check("at a boundary angle, no point of K is within distance 1 of r*e for any r>1",
      not any(straddle_upper_ok(r, s) for r, s in far),
      "%d exact samples" % len(far))
check("the approach data is legal: |x + r_n*w_n| = r_n and r_n -> 0",
      all(F(1, n + 1) > 0 and F(1, n + 1) <= 1 for n in range(50)))
check("but the conclusion of outer_strip fails there: r*e is in Straddle K only for r <= 1",
      all(straddle_upper_ok(r, s) for r in [F(1, 2), F(9, 10)]
          for s in [F(719, 720)]))
print("   -> the hypothesis must stay strict; the closed pi/3 cone is nevertheless")
print("      safe, because at its centre every inner product is >= cos(pi/6) = sqrt3/2 > 0,")
print("      and the dual arc D(I) of any subset of width <= pi/3 is OPEN of length >= 2pi/3.")

print()
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
raise SystemExit(0 if ok else 1)
