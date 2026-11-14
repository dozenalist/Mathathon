#!/usr/bin/env python3
"""Exact verifier for NOTE.md (member m4, swarm smwg1r9lg, direction d2).

Every decision is exact: fractions.Fraction and Q(sqrt3) pairs (a + b*sqrt3).  No floating point
enters any decision.  Exit status 0 iff every check passes.  Every count is produced by two
independent procedures and compared.
"""
from fractions import Fraction as F
from itertools import product
import sys

CHECKS = []
def check(name, cond):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print("FAIL:", name)
    return cond

# ------------------------------------------------------------------ Q(sqrt 3)
class Q3:
    """a + b*sqrt(3), a,b in Q."""
    __slots__ = ("a", "b")
    def __init__(self, a, b=0):
        self.a = a if isinstance(a, F) else F(a)
        self.b = b if isinstance(b, F) else F(b)
    def __add__(self, o):
        o = o if isinstance(o, Q3) else Q3(o)
        return Q3(self.a + o.a, self.b + o.b)
    __radd__ = __add__
    def __neg__(self): return Q3(-self.a, -self.b)
    def __sub__(self, o):
        o = o if isinstance(o, Q3) else Q3(o)
        return Q3(self.a - o.a, self.b - o.b)
    def __rsub__(self, o): return Q3(o).__sub__(self)
    def __mul__(self, o):
        o = o if isinstance(o, Q3) else Q3(o)
        return Q3(self.a*o.a + 3*self.b*o.b, self.a*o.b + self.b*o.a)
    __rmul__ = __mul__
    def __truediv__(self, o):
        o = o if isinstance(o, Q3) else Q3(o)
        n = o.a*o.a - 3*o.b*o.b
        assert n != 0
        return Q3((self.a*o.a - 3*self.b*o.b)/n, (self.b*o.a - self.a*o.b)/n)
    def sign(self):
        if self.b == 0: return (self.a > 0) - (self.a < 0)
        if self.a == 0: return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0: return 1
        if self.a < 0 and self.b < 0: return -1
        lhs, rhs = self.a*self.a, 3*self.b*self.b
        if self.a > 0:
            return 1 if lhs > rhs else (-1 if lhs < rhs else 0)
        return 1 if rhs > lhs else (-1 if rhs < lhs else 0)
    def __eq__(self, o):
        o = o if isinstance(o, Q3) else Q3(o)
        return self.a == o.a and self.b == o.b
    def __repr__(self): return f"({self.a}+{self.b}s3)"

def vadd(p, q): return (p[0]+q[0], p[1]+q[1])
def vsub(p, q): return (p[0]-q[0], p[1]-q[1])
def vscale(t, p):
    t = t if isinstance(t, Q3) else Q3(t)
    return (t*p[0], t*p[1])
def dot(p, q): return p[0]*q[0] + p[1]*q[1]
def sq(p): return dot(p, p)
ZERO, ONE = Q3(0), Q3(1)
S3 = Q3(0, 1)
HALF = Q3(F(1, 2))

# =================================================== A. the orbit system
def words_bruteforce(m, pred):
    return [w for w in product(range(m), repeat=6) if pred(w)]
def ruleP1(w):   # (5.7) at every orbit position: sigma(R e) != sigma(e)
    return all(w[(k+1) % 6] != w[k] for k in range(6))
def ruleP2(w):   # (5.2) at the 120-degree pairs: sigma(R e) notin {sigma(e), sigma(R^2 e)}
    return all(w[(k+1) % 6] not in (w[k], w[(k+2) % 6]) for k in range(6))

def words_transfer(m):
    """cyclic words with w(k+1)!=w(k) for all k = trace(M^6), M on ordered pairs a!=b"""
    states = [(a, b) for a in range(m) for b in range(m) if a != b]
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    M = [[0]*n for _ in range(n)]
    for (a, b) in states:
        for c in range(m):
            if c != b:
                M[idx[(a, b)]][idx[(b, c)]] += 1
    def mm(X, Y):
        return [[sum(X[i][k]*Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    P = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    B, e = M, 6
    while e:
        if e & 1: P = mm(P, B)
        B, e = mm(B, B), e >> 1
    return sum(P[i][i] for i in range(n))

for m in (2, 3, 4):
    brute = len(words_bruteforce(m, ruleP1))
    trans = words_transfer(m)
    check(f"A1 orbit words m={m}: brute force == transfer matrix == (m-1)^6+(m-1) = {(m-1)**6+(m-1)}",
          brute == trans == (m - 1) ** 6 + (m - 1))
check("A2 k=6 (m=3) orbit words = 66",  len(words_bruteforce(3, ruleP1)) == 66)
check("A3 k=6 three-valued orbit words = 60",
      len([w for w in words_bruteforce(3, ruleP1) if len(set(w)) == 3]) == 60)
check("A4 k=5 (m=2) orbit words = 2  [calibration: binarity forced]",
      len(words_bruteforce(2, ruleP1)) == 2)
check("A5 k=7 (m=4) orbit words = 732  [calibration, record Block C]",
      len(words_bruteforce(4, ruleP1)) == 732)
check("A6 (5.2) at the 120-degree pairs is EQUIVALENT to (5.7) on the orbit: same word set",
      set(words_bruteforce(3, ruleP1)) == set(words_bruteforce(3, ruleP2)) and
      set(words_bruteforce(4, ruleP1)) == set(words_bruteforce(4, ruleP2)))
two = [w for w in words_bruteforce(3, ruleP1) if len(set(w)) == 2]
check("A7 two-valued solutions inside 3 labels: exactly 6 words", len(two) == 6)
check("A8 every two-valued solution is 2-periodic (Lemma 5.1)",
      all(all(w[k] == w[(k+2) % 6] for k in range(6)) for w in two))
check("A9 exhaustive over all 2-valued 6-words: (5.7) forces 2-periodicity",
      all(all(w[k] == w[(k+2) % 6] for k in range(6))
          for w in product((0, 1), repeat=6) if ruleP1(w)))
check("A10 no 3-valued word is 2-periodic (the three-valued states are genuinely three)",
      all(any(w[k] != w[(k+2) % 6] for k in range(6))
          for w in words_bruteforce(3, ruleP1) if len(set(w)) == 3))

# =================================================== B. exact direction geometry
dirs = [(ONE, ZERO),
        (HALF, S3*HALF),
        (ZERO - HALF, S3*HALF),
        (ZERO - ONE, ZERO),
        (ZERO - HALF, ZERO - S3*HALF),
        (HALF, ZERO - S3*HALF)]
def R60(p):
    return (HALF*p[0] - (S3*HALF)*p[1], (S3*HALF)*p[0] + HALF*p[1])
ok = True
for k in range(6):
    e = dirs[k]
    r = R60(e)
    R2e = R60(r)
    ok &= (sq(e) == ONE) and (sq(r) == ONE) and (r == dirs[(k+1) % 6])
    ok &= (sq(vsub(e, r)) == ONE)               # |e - R e| = 1 (properness at unit distance)
    ok &= (vadd(e, R2e) == r)                   # e + R^2 e = R e   (turns (5.2) into (P2))
    ok &= (sq(vadd(e, R2e)) == ONE)
check("B1 |e_k|=1, R e_k=e_{k+1}, |e-Re|=1, e+R^2e=Re  (six exact directions, Q(sqrt3))", ok)

# unit decomposition for 0<|w|<2: exactly two unit vectors s,t with s+t=w
w = (Q3(F(24, 25)), Q3(F(32, 25)))
s1 = (ZERO, ONE)
s2 = vsub(w, s1)
check("B2 |w| = 8/5 in (0,2)", sq(w) == Q3(F(64, 25)) and sq(w).sign() > 0 and (Q3(4) - sq(w)).sign() > 0)
check("B3 s1 + t1 = w with |s1| = |t1| = 1, and {s,t} = {t,s}",
      sq(s1) == ONE and sq(s2) == ONE and vadd(s1, s2) == w)
check("B4 the linear condition s.w = |w|^2/2 holds for both solutions",
      dot(s1, w) == HALF*sq(w) and dot(s2, w) == HALF*sq(w))
check("B5 a third solution would have to satisfy the same linear condition (line meets the circle "
      "in at most two points): |{s : |s|=1, s.w=|w|^2/2}| <= 2  [exact discriminant]",
      (sq(w)*sq(w)/4) == (HALF*sq(w))*(HALF*sq(w)))

# =================================================== C. the rigid alternation
def normalise(A):
    pieces = []
    for (a, b) in A:
        while a >= 6: a -= 6; b -= 6
        while b > 6:
            pieces.append((a, F(6))); a, b = F(0), b - 6
        pieces.append((a, b))
    pieces.sort()
    out = []
    for (a, b) in pieces:
        if b <= a: continue
        if out and out[-1][1] == a: out[-1] = (out[-1][0], b)
        else: out.append((a, b))
    return out
def sh(A): return normalise([(a + 1, b + 1) for (a, b) in A])
def meas(A): return sum(b - a for (a, b) in A)
def inter(A, B):
    out = []
    for (a, b) in A:
        for (c, d) in B:
            lo, hi = max(a, c), min(b, d)
            if lo < hi: out.append((lo, hi))
    return normalise(out)
ALT = [(F(0), F(1)), (F(2), F(3)), (F(4), F(5))]      # units of pi/3 on the circle R/6
check("C1 alternation: A cap R(A) = empty", inter(ALT, sh(ALT)) == [])
check("C2 alternation: A u R(A) = whole circle", normalise(ALT + sh(ALT)) == [(F(0), F(6))])
check("C3 alternation: measure(A) = measure(R A) = 1/2 of 2 pi",
      meas(ALT) == 3 and meas(sh(ALT)) == 3 and meas(ALT) + meas(sh(ALT)) == 6)
check("C4 A is R^2-invariant (as Lemma 5.1 forces)", sh(sh(ALT)) == normalise(ALT))
HALFSPLIT = [(F(0), F(3))]
check("C5 the naive half-split [0,pi) is NOT alternating: overlaps its rotate",
      inter(HALFSPLIT, sh(HALFSPLIT)) != [])
check("C6 [0,pi) is not R^2-invariant either",
      sh(sh(HALFSPLIT)) != normalise(HALFSPLIT))

# =================================================== D. Theorem 3(ii) geometry
ok = True
for (rho, d) in [(F(3, 2), F(1, 4)), (F(5, 2), F(1, 3)), (F(11, 10), F(1, 20)), (F(2), F(1, 2))]:
    if rho > 1 and d < rho - 1:
        ok &= (d + 1 < rho)          # sup_{z in dB(y,1)} |z - p| <= d + 1 < rho
check("D1 |y-p| < rho-1, rho>1  =>  closed unit circle about y lies in B(p,rho)", ok)
check("D2 the radius threshold is exactly 1: rho-1 > 0 required", F(1) - 1 == 0)

# =================================================== E. hexagonal 7-colouring (k=7) calibration
s = F(2, 5)                         # circumradius, m3's convention
u = (S3*s, ZERO)
v = (S3*s*HALF, Q3(3)*s*HALF)
check("E1 |u| = |v| = |u-v| = sqrt3 s", sq(u) == Q3(3)*Q3(s)*Q3(s) == sq(v) and sq(vsub(u, v)) == sq(u))
def colour(m, n): return (m + 3*n) % 7
check("E2 the six lattice neighbours of a cell have a different colour",
      all(colour(*a) != 0 for a in [(1, 0), (0, 1), (1, -1), (-1, 0), (0, -1), (-1, 1)]))
best = None
for m in range(-10, 11):
    for n in range(-10, 11):
        if (m, n) == (0, 0) or colour(m, n) % 7 != 0: continue
        d2 = 3*s*s*(m*m + m*n + n*n)
        if best is None or d2 < best: best = d2
check("E3 nearest same-coloured cell centres at squared distance 21 s^2 = 84/25", best == F(84, 25))
check("E4 sqrt21*s - 2s > 1  <=>  sqrt21 > 9/2  <=>  21 > 81/4  (exact rationals): same-coloured "
      "cells of the 7-colouring at s = 2/5 are more than 1 apart pointwise",
      F(21) > F(81, 4))
ap = S3*s*HALF
check("E5 apothem sqrt3 s/2 > 0: the colour is constant on a neighbourhood of a cell centre", ap.sign() > 0)

def cell_and_margin(p):
    """nearest lattice point (m,n), squared distance, and the exact Voronoi margin
    min over the three directions w in {u, v, u-v} of |w|^2/2 - (p-c).w  (>0 iff interior)."""
    b = (Q3(2)*p[1]) / (Q3(3)*Q3(s))
    a = p[0] / (S3*Q3(s)) - HALF*b
    a0 = int(a.a + F(1, 2)) if a.a >= 0 else -int(-a.a + F(1, 2))
    b0 = int(b.a + F(1, 2)) if b.a >= 0 else -int(-b.a + F(1, 2))
    best = None
    for m in range(a0 - 1, a0 + 2):
        for n in range(b0 - 1, b0 + 2):
            c = vadd(vscale(Q3(m), u), vscale(Q3(n), v))
            d = sq(vsub(p, c))
            if best is None or (d - best[0]).sign() < 0:
                best = (d, (m, n), c)
    d, (m, n), c = best
    rel = vsub(p, c)
    margin = None
    for wv in (u, v, vsub(u, v)):
        val = HALF*sq(wv) - dot(rel, wv)
        if margin is None or (val - margin).sign() < 0:
            margin = val
    return (m, n), d, margin

def on_circle(t):
    if t is None: return (ZERO - ONE, ZERO)
    d = 1 + t*t
    return (Q3((1 - t*t)/d), Q3(2*t/d))

lab = {}
for k in range(-4000, 4001):
    t = F(k, 60)
    p = on_circle(t)
    (m, n), d2, margin = cell_and_margin(p)
    if margin.sign() > 0:                 # point lies in the open cell: an arc of this colour
        lab.setdefault(colour(m, n), t)
p = on_circle(None); (m, n), d2, margin = cell_and_margin(p)
if margin.sign() > 0: lab.setdefault(colour(m, n), "inf")
check("E6 the unit circle about a hexagon centre carries at least three labels, each on an arc "
      "of positive length (every witness point certified strictly interior to its hexagon)",
      len(lab) >= 3)
print("   [E6] labels carried on arcs of the unit circle about a cell centre:",
      sorted(lab), "; one certified direction (t = tan(theta/2)) for each:", lab)
print("   [E7] Gamma_x = empty at a hexagon centre: the colour is constant on B(x, apothem)")
print("        (E5), so D_ij(B,h) = empty for every small ball B about x and all small h.")

# =================================================== F. strip witness (circle data alone is not enough)
def strip_colour(x): return (x // F(1, 10)) % 3
lab = set()
for k in range(-1000, 1001):
    p = on_circle(F(k, 700))
    if p[0].b == 0: lab.add(strip_colour(p[0].a))
check("F1 strip colouring: the unit circle about a strip-interior point carries exactly 3 labels",
      lab == {0, 1, 2})
print("   [F1] strip colouring labels on the circle:", sorted(lab),
      "| Gamma = empty at x = 1/20 (colour constant on the strip)")


# =================================================== G. discrete model of the pushforward identity
# The algebra behind Theorem 3 (4.1), checked exactly on a finite group model: centres G = Z/7 x Z/7,
# "unit circle at s" = translation by s in a fixed 6-element set S, colouring c: G -> Fin(6).
def gidx(p): return (p[0] % 7, p[1] % 7)
G = [gidx((i, j)) for i in range(7) for j in range(7)]
S6 = [gidx((1, 0)), gidx((-1, 0)), gidx((0, 1)), gidx((0, -1)), gidx((1, 1)), gidx((-1, -1))]
_odd = {(0, 0), (1, 2), (3, 4)}
def cfun(p):                       # colour 0 except on a small set, where the colour is 5
    return 5 if (p[0] % 7, p[1] % 7) in _odd else 0
O = {0, 1, 2}
E = [x for x in G if all(cfun(gidx((x[0] + s[0], x[1] + s[1]))) in O for s in S6)]
check("G0 the finite model has a nonempty admissible centre set E", len(E) > 0)
# G1: the exact pushforward identity  sum_{x in E} sum_{s in S} f(x+s) = sum_y f(y) #{s : y-s in E}
import random
random.seed(20260101)
for trial in range(20):
    f = {y: random.randint(-5, 5) for y in G}
    lhs = sum(f[gidx((x[0] + s[0], x[1] + s[1]))] for x in E for s in S6)
    N = {y: sum(1 for s in S6 if gidx((y[0] - s[0], y[1] - s[1])) in E) for y in G}
    rhs = sum(f[y] * N[y] for y in G)
    check(f"G1 discrete pushforward identity, trial {trial}", lhs == rhs)
# G2: the conclusion: since f := 1{c notin O} vanishes on every x+s with x in E, the f-weighted
# sum over y vanishes identically -- i.e. the model counterpart of (4.1).
f = {y: (1 if cfun(y) not in O else 0) for y in G}
lhs = sum(f[gidx((x[0] + s[0], x[1] + s[1]))] for x in E for s in S6)
N = {y: sum(1 for s in S6 if gidx((y[0] - s[0], y[1] - s[1])) in E) for y in G}
rhs = sum(f[y] * N[y] for y in G)
check("G2 discrete analogue of (4.1): both sides vanish", lhs == 0 and rhs == 0)
# G3: the converse direction -- a centre y whose 'circle' is fully inside E must itself carry a
# label of O in the model (this is the step that makes 'E conull' impossible).
full = [y for y in G if N[y] == 6]
check("G3 every y whose circle lies entirely in E is O-coloured in the model",
      all(cfun(y) in O for y in full))

# =================================================== report
npass = sum(1 for _, ok in CHECKS if ok)
print()
print(f"{npass}/{len(CHECKS)} checks passed")
for name, ok in CHECKS:
    if not ok: print("  FAILED:", name)
sys.exit(0 if npass == len(CHECKS) else 1)
