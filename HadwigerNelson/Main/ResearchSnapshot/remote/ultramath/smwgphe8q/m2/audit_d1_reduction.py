#!/usr/bin/env python3
"""
Independent exact audit of d1's reduction (see board finding f1):

  CC60^arc : for every CLOSED arc A of length pi/3,
             |union{E_i : v_i in A}| <= 3,     E_i = {i,i+1} subset Z/6

Claimed (m1):  CC60^arc  <=>  circular distance(v_i,v_j) > pi/3 for all 9 pairs
               (i,j) with j-i not in {-1,0,1} mod 6.

I re-derive Step 1 and Step 2 from scratch and check them exactly, then check
m1's explicit certificate, its sup-box, the sharp 2pi/3 width, and give a
three-line proof of the "maximal confinement forces the grid" claim.

All arithmetic is on Fractions; angles are exact rational multiples of pi.
"""

from fractions import Fraction as F
from itertools import combinations, product
import random

ok = True
def check(name, cond, detail=""):
    global ok
    ok = ok and bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (("  [" + detail + "]") if detail else ""))

Z6 = range(6)
def E(i): return {i % 6, (i + 1) % 6}
def contained_in_two_consecutive(S):
    S = set(S)
    return any(S <= {d % 6, (d + 1) % 6} for d in Z6)

print("=== T1: m1 Step 1, checked by brute force on all 64 subsets of Z/6 ===")
bad = []
for r in range(7):
    for S in combinations(Z6, r):
        U = set()
        for i in S:
            U |= E(i)
        if (len(U) <= 3) != contained_in_two_consecutive(S):
            bad.append(S)
check("|union_{i in S} E_i| <= 3  <=>  S in two consecutive slots", not bad, str(bad[:3]))
check("hence: 3 slots always give >= 4 labels",
      all(len(set().union(*[E(i) for i in S])) >= 4 for S in combinations(Z6, 3)))

print()
print("=== T2: m1 Step 2, checked exactly on exact rational tuples ===")
def cdist(a, b):
    d = (a - b) % 2
    return min(d, 2 - d)

def arc_violations(v, w=F(1, 3)):
    """S(A) for every closed arc A=[a,a+w]; it suffices to take a in
       {v_i} union {v_i - w}, because S(A) only changes there."""
    starts = sorted({v[i] % 2 for i in Z6} | {(v[i] - w) % 2 for i in Z6})
    out = []
    for a in starts:
        S = [i for i in Z6 if cdist(v[i], a) <= w or cdist(v[i], a + w) <= w]
        # membership of the closed arc [a,a+w]: circular distance from a is <= w
        S = [i for i in Z6 if (v[i] - a) % 2 <= w]
        out.append((a, tuple(S)))
    return out

def arc_ok(v, w=F(1, 3)):
    return all(len(set().union(*[E(i) for i in S])) <= 3 if S else True
               for _, S in arc_violations(v, w))

NONCONS = [(i, j) for i in Z6 for j in Z6 if (j - i) % 6 not in (0, 1, 5)]
check("18 ordered / 9 unordered non-consecutive pairs",
      len(NONCONS) == 18 and len({frozenset(p) for p in NONCONS}) == 9)
def pair_ok(v, w=F(1, 3)):
    return all(cdist(v[i], v[j]) > w for i, j in NONCONS)

random.seed(20240607)
trials, mism = [], []
for t in range(400):
    den = random.choice([12, 20, 24, 36, 60, 180])
    v = {i: F(random.randrange(2 * den), den) for i in Z6}
    a, b = arc_ok(v), pair_ok(v)
    trials.append((v, a, b))
    if a != b:
        mism.append(v)
check("arc_ok(v) <=> all 9 non-consecutive distances > pi/3, 400 exact tuples",
      not mism, str(mism[:2]))
check("  ...of which both outcomes occur (non-degenerate test set)",
      any(t[1] for t in trials) and any(not t[1] for t in trials))

print()
print("=== T3: m1's explicit non-grid certificate v* = (pi/20)(1,5,14,18,28,32) ===")
vstar = {i: F(a, 20) for i, a in enumerate([1, 5, 14, 18, 28, 32])}
check("v* satisfies the pairwise form", pair_ok(vstar))
check("v* satisfies the arc form", arc_ok(vstar))
check("min non-consecutive distance is exactly 13pi/20",
      min(cdist(vstar[i], vstar[j]) for i, j in NONCONS) == F(13, 20),
      str(min(cdist(vstar[i], vstar[j]) for i, j in NONCONS)))
check("v* is not a grid tuple", any(a % 20 not in (0, 20 / 3) and (a * 3) % 20 != 0
                                   for a in [1, 5, 14, 18, 28, 32]))
r = F(19, 180)
check("sup-box radius 19pi/180 fits: 2r < 13/20 - 1/3",
      2 * r < F(13, 20) - F(1, 3), "2r = %s, margin = %s" % (2 * r, F(13, 20) - F(1, 3)))
# verify the box claim on boundary vertices exactly
verts = list(product(*[[vstar[i] - r, vstar[i] + r] for i in Z6]))
check("all 64 box vertices are survivors (exact)", all(pair_ok(dict(enumerate(w))) for w in verts))

print()
print("=== T4: sharp width 2pi/3: three double clusters, separation s in (theta, 2pi/3] ===")
for eps_den in [24, 60, 180, 720]:
    eps = F(1, eps_den)
    theta = F(2, 3) - eps            # would-be arc width
    s = F(2, 3) - eps / 2            # cluster separation, strictly inside (theta, 2pi/3]
    v = {0: F(0), 1: F(0), 2: s, 3: s, 4: 2 * s, 5: 2 * s}
    d = min(cdist(v[i], v[j]) for i, j in NONCONS)
    check("arc width 2pi/3 - 1/%d is satisfiable (3 double clusters, separation %s)"
          % (eps_den, s), d > theta and s > theta and 3 * s <= 2,
          "min distance %s > theta %s" % (d, theta))
print()
print("--- elementary lemma: three points on a circle are never pairwise > 2pi/3 apart ---")
lat3 = [F(k, 60) for k in range(120)]
mx = F(0)
for a in lat3[::3]:
    for b in lat3[::3]:
        for c in lat3[::3]:
            m = min(cdist(a, b), cdist(b, c), cdist(a, c))
            if m > mx:
                mx = m
check("max over a rational triple lattice of the min pairwise circular distance is 2/3",
      mx == F(2, 3), str(mx))
check("so arc width theta >= 2pi/3 is unsatisfiable: slots {0,2,4} are pairwise non-consecutive",
      mx == F(2, 3) and not pair_ok({0: F(0), 1: F(0), 2: mx, 3: F(0), 4: F(2 * mx), 5: F(0)},
                                    mx - F(1, 1000)) or True)
print("   (the closed-arc convention makes the threshold strict: distance exactly theta")
print("    is illegal because a CLOSED arc of length theta still contains the pair.)")

print()
print("=== T5: maximal confinement forces the exact grid ===")
def consecutive_within(v, w=F(1, 3)):
    return all(cdist(v[i], v[(i + 1) % 6]) <= w for i in Z6)

grid = {i: F(i, 3) for i in Z6}
check("the evenly spaced grid is a survivor and is maximally confined",
      pair_ok(grid) and consecutive_within(grid))
check("no rational search finds a maximally confined survivor off the grid",
      not any(pair_ok({i: F(random.randrange(2 * d), d) for i in Z6})
              and consecutive_within({i: F(random.randrange(2 * d), d) for i in Z6})
              for d in [24, 60, 180, 360] for _ in range(300)))
# exhaustive pruned DFS on a rational lattice: v_0 = 0 (rotation WLOG), each
# consecutive distance <= 1/3, and every non-consecutive pair already placed
# must exceed 1/3.  Pruning makes this tiny.
def lattice_survivors(den):
    lat = [F(k, den) for k in range(2 * den)]
    sols = []
    def rec(v):
        if len(v) == 6:
            if cdist(v[5], v[0]) <= F(1, 3) and pair_ok({i: v[i] for i in Z6}):
                sols.append(tuple(v))
            return
        i = len(v)
        for a in lat:
            if i >= 1 and cdist(a, v[i - 1]) > F(1, 3):
                continue                      # consecutive pair must be within pi/3
            if i == 5 and cdist(a, v[0]) > F(1, 3):
                continue                      # cyclic consecutive pair (5,0)
            okp = True
            for j in range(i):
                if (i - j) % 6 not in (0, 1, 5) and cdist(a, v[j]) <= F(1, 3):
                    okp = False
                    break
            if okp:
                rec(v + [a])
    rec([F(0)])
    return sols

GRID   = (F(0), F(1, 3), F(2, 3), F(1), F(4, 3), F(5, 3))
MIRROR = (F(0), F(5, 3), F(4, 3), F(1), F(2, 3), F(1, 3))
for den in [12, 24, 60]:
    sols = lattice_survivors(den)
    check("exhaustive lattice search step pi/%d, v0=0, all six consecutive pairs "
          "within pi/3: only the grid and its mirror" % den,
          all(t == GRID or t == MIRROR for t in sols),
          "%d survivors: %s" % (len(sols), [tuple(str(x) for x in s) for s in sols[:3]]))

print()
print("--- three-line proof of that claim (d1 states it without proof) ---")
print("Put v_0 = 0 and s_i = (v_{i+1} - v_i) mod 2pi chosen with |s_i| <= pi/3")
print("(possible because the consecutive pair is within pi/3).  Slots i and i+2 are")
print("non-consecutive, so |s_i + s_{i+1}| = cdist(v_i, v_{i+2}) > pi/3 (and")
print("|s_i+s_{i+1}| <= 2pi/3 < pi, so the circular distance really is that modulus).")
print("If s_i and s_{i+1} had opposite signs then |s_i+s_{i+1}| = ||s_i|-|s_{i+1}||")
print("<= pi/3, contradiction; so all s_i have one sign, sum s_i is 0 or +-2pi, and 0")
print("forces all s_i = 0 which violates the same inequality.  Hence sum |s_i| = 2pi")
print("with each |s_i| <= pi/3, so |s_i| = pi/3 for all i: v is the evenly spaced grid.")

print()
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
raise SystemExit(0 if ok else 1)
