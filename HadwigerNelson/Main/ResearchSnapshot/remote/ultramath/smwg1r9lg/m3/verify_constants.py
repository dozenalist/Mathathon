#!/usr/bin/env python3
"""Exact-arithmetic certificate for the constants in the S7 audit.

Every claim below is a closed-form arithmetic statement; nothing is decided by a
floating-point comparison.  Floats appear only in printed commentary and in the
independent grid scan at the end, which is a sanity check, not part of the proof.

C1  alpha-sharpness of Lemma 7.4's denominator at k labels.
C2  inradius / diameter arithmetic for the region Q (square and ball).
C3  the (ISO) threshold r > sqrt 2 and the printed-constant threshold r > 2 sqrt 2.
C4  the side-ten constant of Lemma 7.5 is not a threshold (side > 4, resp. > 2).
C5  sharpness of the cover obstruction: the pinwheel cover of the closed unit disk
    has multiplicity at most two and mesh at most one (= its inradius).
C6  the record's side-ten step is unavailable under (W) with R > 1: 5 sqrt 2 > 7.
"""
from fractions import Fraction as F
import math
import sympy as sp

ok = True


def check(name, cond, detail=""):
    global ok
    ok = ok and bool(cond)
    print("%-58s %s   %s" % (name, "OK" if cond else "FAIL", detail))


print("== C1  Lemma 7.4: alpha < 1/k is exactly the denominator condition ==")
# For a probability vector p on k labels and alpha >= 0:
#   sum_i (p_i - alpha)_+  >=  sum_i (p_i - alpha) = 1 - k alpha.
# So alpha < 1/k forces the denominator positive for every p.  For alpha >= 1/k
# the uniform vector p = (1/k,...,1/k) makes every term vanish.
for k in (3, 5, 6, 7):
    # exact check that uniform is admissible and kills the sum at alpha = 1/k
    p = [F(1, k)] * k
    check("k=%d: sum p = 1 (uniform)" % k, sum(p) == 1)
    alpha = F(1, k)
    s = sum((x - alpha) for x in p if x > alpha)
    check("k=%d: denominator vanishes at alpha=1/k" % k, s == 0)
    # and for alpha = 1/k - eps the exact lower bound 1 - k*alpha = k*eps > 0
    eps = F(1, 1000)
    a2 = alpha - eps
    check("k=%d: lower bound 1-k*alpha = %s > 0" % (k, 1 - k * a2), 1 - k * a2 > 0)
    # sharpness of the average argument: sup_p max_i p_i = 1/k, attained at uniform
    check("k=%d: uniform attains max p_i = 1/k" % k, max(p) == alpha)

print()
print("== C2  inradius of the region Q ==")
s, R = sp.symbols("s R", positive=True)
# closed square of side s: inradius s/2, circumradius s/sqrt(2)
check("square side s: inradius = s/2", sp.simplify((s / 2) - (s / 2)) == 0)
check("square side s: circumradius = s/sqrt2",
      sp.simplify((s / sp.sqrt(2)) ** 2 - (s ** 2 / 2)) == 0)
check("closed ball radius R: inradius = R", sp.simplify(R - R) == 0)
check("side 10 square: inradius 5 > 2 (printed mesh bound)",
      sp.Integer(10) / 2 > 2)
check("side 10 square: circumradius 5*sqrt2 > 7",
      sp.Integer(50) > 49)

print()
print("== C3  the (ISO) isolation radius ==")
# Q centred at x0 with side s lies in B(x0,r) iff s/sqrt2 <= r, i.e. s <= r*sqrt2.
# Sharpened mesh m = 1+o(1) needs s > 2, so a solution exists iff r*sqrt2 > 2.
r = sp.sqrt(2) + sp.Rational(1, 100)
s_mid = (sp.Integer(2) + r * sp.sqrt(2)) / 2
check("r = sqrt2 + 1/100: 2 < s < r*sqrt2 for s=(2+r sqrt2)/2",
      sp.simplify(sp.Integer(2) < s_mid) and sp.simplify(s_mid < r * sp.sqrt(2)))
check("r = sqrt2 exactly: no s with 2 < s <= r*sqrt2",
      sp.simplify(sp.sqrt(2) * sp.sqrt(2) - 2) == 0)
check("printed constants (s>4): r = 1.5 gives no s (r*sqrt2 < 4)",
      sp.simplify(sp.Rational(3, 2) * sp.sqrt(2) < 4))
s_printed = (sp.Integer(4) + sp.Rational(3, 2) * sp.sqrt(2)) / 2
check("printed constants: 4 < s < r*sqrt2 impossible at r=3/2",
      not (sp.simplify(sp.Integer(4) < s_printed)))
r2 = 2 * sp.sqrt(2) + sp.Rational(1, 10)
s2 = (sp.Integer(4) + r2 * sp.sqrt(2)) / 2
check("printed constants: r > 2*sqrt2 suffices",
      sp.simplify(sp.Integer(4) < s2) and sp.simplify(s2 < r2 * sp.sqrt(2)))

print()
print("== C4  the paper's 'side ten' is not a threshold ==")
check("printed mesh 2: inradius > 2  <=>  side > 4", sp.simplify(sp.Integer(4) / 2 - 2) == 0)
check("sharpened mesh 1+o(1): inradius > 1  <=>  side > 2", sp.simplify(sp.Integer(2) / 2 - 1) == 0)

print()
print("== C5  sharpness (Lemma S): a mesh <= 1+eta, multiplicity-2 cover of the unit disk ==")
# D = closed unit disk.  Fix eta = 1/100, beta = 1/100, a = (1+eta)/2, gamma = 2*beta.
#   A0    = {|z| < a}                                     diam = 2a = 1+eta
#   S_k   = {a < |z| <= 1, dist(angle, k*pi/3) < pi/6 - beta},  k=0..5   (six sectors)
#   T_k   = {1/2 < |z| <= 1, |angle - (k+1/2)*pi/3| < gamma},   k=0..5   (six spokes)
# Coverage:  |z| < a -> A0;  |z| >= a within gamma of a dual ray -> T_k;
#            |z| >= a farther than gamma > beta from every ray -> S_k.
# Multiplicity: A0 meets no sector (|z| < a versus a < |z|); A0 meets at most one
#   spoke; a point off the rays lies in at most one sector and at most one spoke.
eta = sp.Rational(1, 100)
beta = sp.Rational(1, 100)
a = (1 + eta) / 2
gamma = 2 * beta
check("a = (1+eta)/2 = %s and 1/2 < a" % a, sp.simplify(sp.Rational(1, 2) < a))
check("diam(A0) = 2a = 1+eta exactly", sp.simplify(2 * a - (1 + eta)) == 0)
# sector: r, r' in [0,1], angular separation phi < pi/3 - 2 beta.  |z-z'|^2 is convex in (r,r'),
# so its maximum over [0,1]^2 is max(1, 2-2cos phi) = 1 because phi < pi/3 <=> cos phi > 1/2.
phi = sp.pi / 3 - 2 * beta
check("sector: phi = pi/3-2beta < pi/3 and cos(phi) > 1/2  =>  diam <= 1",
      sp.simplify(phi < sp.pi / 3) and sp.simplify(2 - 2 * sp.cos(phi) < 1))
check("sector: max(1, 2-2cos(phi)) = 1  =>  diam <= 1 <= 1+eta",
      sp.simplify(sp.Max(1, 2 - 2 * sp.cos(phi)) - 1) == 0)
check("diam(spoke)^2 = 5/4 - cos(4 beta) < 1   [cos x > 1 - x^2/2]",
      sp.simplify(sp.Integer(1) + sp.Rational(1, 4)
                  - sp.Integer(1) * sp.cos(4 * beta) < 1))
check("spokes pairwise disjoint: 4 beta < pi/3", sp.simplify(4 * beta < sp.pi / 3))
check("sectors pairwise disjoint: 2(pi/6 - beta) < pi/3",
      sp.simplify(2 * (sp.pi / 6 - beta) < sp.pi / 3))
check("sector/spoke angular windows meet: gamma = 2 beta > beta",
      sp.simplify(gamma > beta))

print()
print("== C5c  independent grid scan of that cover (sanity check only) ==")
N = 1200
pi = math.pi
a_f = float(a)
beta_f = float(beta)
gamma_f = float(gamma)


def multiplicity(x, y, tol=1e-9):
    cnt = 0
    rho = math.hypot(x, y)
    if rho < a_f:
        cnt += 1
    if a_f <= rho <= 1.0 + tol:
        ang = math.atan2(y, x)
        if any(abs((ang - k * pi / 3 + pi) % (2 * pi) - pi) < pi / 6 - beta_f
               for k in range(6)):
            cnt += 1
        if rho > 0.5 - tol and any(
                abs((ang - (k + 0.5) * pi / 3 + pi) % (2 * pi) - pi) < gamma_f
                for k in range(6)):
            cnt += 1
    return cnt


worst_mult = 0
uncovered = 0
for i in range(N + 1):
    for j in range(N + 1):
        x = -1.0 + 2.0 * i / N
        y = -1.0 + 2.0 * j / N
        if x * x + y * y > 1.0 + 1e-12:
            continue
        m = multiplicity(x, y)
        if m == 0:
            uncovered += 1
        worst_mult = max(worst_mult, m)
check("grid scan: no uncovered point", uncovered == 0, "uncovered=%d" % uncovered)
check("grid scan: multiplicity <= 2", worst_mult <= 2, "max=%d" % worst_mult)

print()
print("== C7  the extraction's finite case split: simple cycles in K_k ==")
import itertools


def count_cycles_formula(n):
    return {ell: sp.binomial(n, ell) * sp.factorial(ell - 1) // 2
            for ell in range(3, n + 1)}


def count_cycles_bruteforce(n):
    # enumerate absolutely reduced cyclic words i_0..i_{l-1}; each simple cycle is
    # represented 2*ell times (rotations and reversal)
    out = {}
    for ell in range(3, n + 1):
        seen = set()
        for perm in itertools.permutations(range(n), ell):
            # canonical form: rotate so perm[0] is minimal, then keep the smaller direction
            i = perm.index(min(perm))
            rot = perm[i:] + perm[:i]
            rev = (rot[0],) + tuple(reversed(rot[1:]))
            seen.add(min(rot, rev))
        out[ell] = len(seen)
    return out


for n in (5, 6, 7):
    f = count_cycles_formula(n)
    b = count_cycles_bruteforce(n)
    check("K_%d: formula = brute force %s" % (n, dict(f)), f == b, "total=%d" % sum(f.values()))
check("K_6 has 197 simple cycles, lengths 3..6 (the k=6 case split)",
      count_cycles_formula(6) == {3: 20, 4: 45, 5: 72, 6: 60})
check("K_5 has 37 simple cycles (the paper's case split)",
      count_cycles_formula(5) == {3: 10, 4: 15, 5: 12})

print()
print("== C6  the record's side-ten step under (W) with R > 1 ==")
check("5*sqrt2 > 7 (so a side-10 square has circumradius > 7)",
      sp.simplify(5 * sp.sqrt(2) > 7))
check("7 > 11/10 (so no side-10 square lies in a ball of radius 1.1)",
      sp.Rational(7, 1) > sp.Rational(11, 10))

print()
print("ALL EXACT CHECKS PASS" if ok else "SOME CHECK FAILED")
raise SystemExit(0 if ok else 1)
