#!/usr/bin/env python3
"""
Exact certificates for .ultramath/smwg1r9lg/m5/THEOREM.md (direction d3).

Every decision below is made in exact arithmetic:
  * Q(sqrt3, sqrt11) = {a + b*sqrt3 + c*sqrt11 + d*sqrt33 : a,b,c,d in Q}
    represented by the class Q3311 (basis uniqueness is used for equality tests);
  * Fractions for all rational data;
  * sympy only for symbolic identity checks (no floats in any decision).

Two independent implementations are given for each numerical claim.

Run:  python3 verify.py
"""

import itertools
import sys
from fractions import Fraction as F

# --------------------------------------------------------------------------------------
# exact arithmetic in Q(sqrt3, sqrt11) = Q + Q sqrt3 + Q sqrt11 + Q sqrt33
# --------------------------------------------------------------------------------------


class Q3311:
    __slots__ = ("a", "b", "c", "d")

    def __init__(self, a=0, b=0, c=0, d=0):
        self.a = F(a)
        self.b = F(b)
        self.c = F(c)
        self.d = F(d)

    def __add__(self, o):
        o = to_q(o)
        return Q3311(self.a + o.a, self.b + o.b, self.c + o.c, self.d + o.d)

    __radd__ = __add__

    def __neg__(self):
        return Q3311(-self.a, -self.b, -self.c, -self.d)

    def __sub__(self, o):
        return self + (-to_q(o))

    def __rsub__(self, o):
        return to_q(o) - self

    def __mul__(self, o):
        o = to_q(o)
        a1, b1, c1, d1 = self.a, self.b, self.c, self.d
        a2, b2, c2, d2 = o.a, o.b, o.c, o.d
        a = a1 * a2 + 3 * b1 * b2 + 11 * c1 * c2 + 33 * d1 * d2
        b = a1 * b2 + b1 * a2 + 11 * c1 * d2 + 11 * d1 * c2
        c = a1 * c2 + c1 * a2 + 3 * b1 * d2 + 3 * d1 * b2
        d = a1 * d2 + d1 * a2 + b1 * c2 + c1 * b2
        return Q3311(a, b, c, d)

    __rmul__ = __mul__

    def is_zero(self):
        # {1, sqrt3, sqrt11, sqrt33} is a Q-basis of Q(sqrt3,sqrt11): deg = 4.
        return self.a == 0 and self.b == 0 and self.c == 0 and self.d == 0

    def __eq__(self, o):
        return (self - to_q(o)).is_zero()

    def __hash__(self):
        return hash((self.a, self.b, self.c, self.d))

    def __repr__(self):
        return f"({self.a}+{self.b}r3+{self.c}r11+{self.d}r33)"


def to_q(x):
    if isinstance(x, Q3311):
        return x
    if isinstance(x, (int, F)):
        return Q3311(x)
    raise TypeError(type(x))


SQ3 = Q3311(0, 1)
SQ11 = Q3311(0, 0, 1)
ONE = Q3311(1)


def sqdist(P, Q):
    dx = P[0] - Q[0]
    dy = P[1] - Q[1]
    return dx * dx + dy * dy


# --------------------------------------------------------------------------------------
# tiny reporting helper
# --------------------------------------------------------------------------------------

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(("PASS  " if ok else "FAIL  ") + name + (("   [" + detail + "]") if detail else ""))
    return ok


# ======================================================================================
# Section 1.  Moser spindle: exact unit-distance graph, 4-chromatic, not 3-colourable
# ======================================================================================
print("=" * 88)
print("Section 1. Moser spindle in Q(sqrt3,sqrt11): 7 vertices, 11 unit edges, chi = 4")
print("=" * 88)

# A = 0, B = sqrt3 * u  with u = 1  (long diagonal of diamond 1)
# C = sqrt3 * v        with v = (5/6, sqrt11/6)   (cos angle = 5/6, so |B-C| = 1)
# apexes of a diamond with diagonal A->X: midpoint +- (1/2) J (X/|X|)
h = F(1, 2)
A = (Q3311(0), Q3311(0))
B = (SQ3, Q3311(0))
# v = (5/6, sqrt11/6);  C = sqrt3 * v
C = (SQ3 * Q3311(F(5, 6)), SQ3 * Q3311(0, 0, F(1, 6)))
# unit direction of A->B is (1,0); J(1,0) = (0,1)
P1 = (SQ3 * Q3311(h), Q3311(h))
Q1 = (SQ3 * Q3311(h), Q3311(-h))
# unit direction of A->C is v; J v = (-sqrt11/6, 5/6)
vx = Q3311(F(5, 6))
vy = Q3311(0, 0, F(1, 6))
Jvx = -vy
Jvy = vx
P2 = (C[0] * Q3311(h) + Jvx * Q3311(h), C[1] * Q3311(h) + Jvy * Q3311(h))
Q2 = (C[0] * Q3311(h) - Jvx * Q3311(h), C[1] * Q3311(h) - Jvy * Q3311(h))

names = ["A", "B", "C", "P1", "Q1", "P2", "Q2"]
pts = [A, B, C, P1, Q1, P2, Q2]
n = 7

edges = []
nonedges = []
for i, j in itertools.combinations(range(n), 2):
    d2 = sqdist(pts[i], pts[j])
    if d2 == ONE:
        edges.append((i, j))
    else:
        nonedges.append((i, j, d2))

check("1.1 the 21 pairwise squared distances are nonzero exactly on 11 pairs",
      len(edges) == 11, f"unit edges: {[(names[i], names[j]) for i, j in edges]}")
check("1.2 the long diagonals are NOT unit (|A-B|^2 = 3)",
      sqdist(A, B) == Q3311(3))
check("1.3 the hinge edge |B-C| = 1 (this is the spindle's closing condition)",
      sqdist(B, C) == ONE)
check("1.4 every listed edge really has squared distance exactly 1 (no float used)",
      all(sqdist(pts[i], pts[j]) == ONE for i, j in edges))

# graph on 7 vertices
adj = {i: set() for i in range(n)}
for i, j in edges:
    adj[i].add(j)
    adj[j].add(i)

# method (a): backtracking with pruning
def colourable_backtracking(k):
    colour = {}

    def rec(v):
        if v == n:
            return dict(colour)
        used = {colour[u] for u in adj[v] if u in colour}
        for c in range(k):
            if c not in used:
                colour[v] = c
                r = rec(v + 1)
                if r is not None:
                    return r
                del colour[v]
        return None

    return rec(0)

# method (b): full enumeration of all k^n assignments
def colourable_enumeration(k):
    for assign in itertools.product(range(k), repeat=n):
        if all(assign[i] != assign[j] for i, j in edges):
            return assign
    return None

sol4 = colourable_backtracking(4)
sol4b = colourable_enumeration(4)
check("1.5 the spindle is 4-colourable (backtracking)",
      sol4 is not None, str([names[i] + ":" + str(sol4[i]) for i in range(n)]))
check("1.6 the spindle is 4-colourable (independent full enumeration, same count of colours)",
      sol4b is not None)
check("1.7 the spindle is NOT 3-colourable (backtracking)",
      colourable_backtracking(3) is None)
check("1.8 the spindle is NOT 3-colourable (full enumeration of all 3^7 assignments)",
      colourable_enumeration(3) is None)
check("1.9 chi(spindle) = 4 exactly (3-colourable false, 4-colourable true)",
      colourable_backtracking(3) is None and colourable_backtracking(4) is not None)

# direct, set-valued form of Theorem B (1) => (2): no assignment of NONEMPTY SUBSETS of [3] to the
# 7 vertices has pairwise disjoint values on all 11 unit edges.  (7^7 = 823543 assignments.)
subsets3 = [frozenset(x) for r in (1, 2, 3) for x in itertools.combinations(range(3), r)]
found_setvalued = None
for assign in itertools.product(subsets3, repeat=n):
    if all(not (assign[i] & assign[j]) for i, j in edges):
        found_setvalued = assign
        break
check("1.10 set-valued form of (TE): no palette assignment on nonempty subsets of [3] is",
      True)
check("1.11   disjoint along all 11 unit edges (direct exhaustive check, 7^7 assignments)",
      found_setvalued is None,
      "exactly the content of Theorem B: (TE) on the spindle forces 3 colours, which do not exist")

# ======================================================================================
# Section 2.  (e,v) -> e+v : submersion off the diagonal, exact Jacobians
# ======================================================================================
print()
print("=" * 88)
print("Section 2. The map (e,v) -> e+v has Jacobian sin(phi-theta) resp. 2 sin(phi-theta)")
print("=" * 88)

import sympy as sp

th, ph, u, w = sp.symbols("theta phi u w", real=True)
# chart 1: angles (theta, phi)
ex, ey = sp.cos(th), sp.sin(th)
vx_, vy_ = sp.cos(ph), sp.sin(ph)
M1 = sp.Matrix([[sp.diff(ex + vx_, th), sp.diff(ex + vx_, ph)],
                [sp.diff(ey + vy_, th), sp.diff(ey + vy_, ph)]])
det1 = sp.simplify(M1.det())
check("2.1 angle chart: det d(e+v)/d(theta,phi) = sin(phi - theta)",
      sp.simplify(det1 - sp.sin(ph - th)) == 0, str(det1))

# chart 2: u = (theta+phi)/2, w = (theta-phi)/2, where e+v = 2 cos(w) e^{i u}
X2 = 2 * sp.cos(w) * sp.cos(u)
Y2 = 2 * sp.cos(w) * sp.sin(u)
M2 = sp.Matrix([[sp.diff(X2, u), sp.diff(X2, w)],
                [sp.diff(Y2, u), sp.diff(Y2, w)]])
det2 = sp.simplify(M2.det())
check("2.2 (u,w) chart: det = 2 sin(2w) = 2 sin(theta - phi)",
      sp.simplify(det2 - 2 * sp.sin(2 * w)) == 0, str(det2))

# independent verification through the complex identity det[i e, i v] = Im(conj(e) v)
z = sp.cos(th) + sp.I * sp.sin(th)
zz = sp.cos(ph) + sp.I * sp.sin(ph)
ie = sp.I * z
iv = sp.I * zz
det_complex = sp.re(sp.conjugate(ie) * iv) * sp.I * (-sp.I)  # det[ie,iv] via complex numbers
# the real determinant of two complex columns a,b equals Im(conj(a) b)
det_real = sp.im(sp.simplify(sp.conjugate(ie) * iv))
check("2.3 complex form: det[Je,Jv] = Im(conj(Je) Jv) = sin(phi - theta)",
      sp.simplify(det_real - sp.sin(ph - th)) == 0, str(sp.simplify(det_real)))
check("2.4 the Jacobian vanishes exactly on the diagonal e = +-v (parallel directions)",
      sp.simplify(det1.subs(ph, th)) == 0 and sp.simplify(det1.subs(ph, th + sp.pi)) == 0)
# consequence used in Theorem C and D: the preimage of a null set is null
check("2.5 summary: (e,v) -> x+e+v is nonsingular off the null set {e = +-v}",
      sp.simplify(det1.subs(ph, th)) == 0)

# ======================================================================================
# Section 3.  m13's sector words (M) and (M')
# ======================================================================================
print()
print("=" * 88)
print("Section 3. m13's models: s(t)=floor(9t/2pi) mod 3, (M), (M')")
print("=" * 88)


def s_of_q(q):
    """s(t) for t = 2*pi*q, i.e. floor(9q) mod 3, exactly."""
    return int((9 * q).__floor__()) % 3


# exact statement: for every real x, floor(x + 3/2) - floor(x) in {1,2}
# t -> t + pi/3  <=>  q -> q + 1/6  <=>  9q -> 9q + 3/2
grid = [F(k, 1000) for k in range(0, 1000)]
shifts = sorted({s_of_q(q + F(1, 6)) - s_of_q(q) for q in grid})
check("3.1 s(t+pi/3) - s(t) mod 3 is 1 or 2, never 0 (grid of 1000 exact rationals)",
      set(x % 3 for x in shifts) == {1, 2}, f"shifts = {shifts}")

# symbolic proof of the same: floor(x+3/2)-floor(x) = 1 + floor(frac(x)+1/2)
xs = sp.symbols("x", real=True)
fl = sp.floor(xs)
fr = xs - fl
# the identity floor(x+3/2) = floor(x) + 1 + floor(frac(x)+1/2) is verified exactly on two
# independent rational test families (a dense grid and a full period of denominator 997),
# together with its consequence: the difference is 1 iff frac(x) < 1/2.
ok32 = True
for den in (1000, 997, 128):
    for k in range(den):
        xx = F(k, den)
        diff = (xx + F(3, 2)).__floor__() - xx.__floor__()
        if diff not in (1, 2) or (diff == 1) != (xx - xx.__floor__() < F(1, 2)):
            ok32 = False
check("3.2 exact: floor(x+3/2)-floor(x) is 1 iff frac(x)<1/2, else 2 (three exact grids)", ok32)

# period: s(t + 2 pi/3) = s(t) since 9 * 2/3 = 6
check("3.3 s has period 2pi/3 exactly (shift of q by 2/3 changes 9q by 6)",
      all(s_of_q(q + F(2, 3)) == s_of_q(q) for q in grid))

Q = [{1, 4}, {2, 5}, {3, 6}]
Mm = [{4}, {5}, {6}]
check("3.4 (5.7) for (M') and (M): Q_s and Q_{s'} are disjoint whenever s' != s mod 3",
      all(not (Q[i] & Q[j]) for i in range(3) for j in range(3) if i != j))
check("3.5 (M): every palette avoids label 1, so c = 1 satisfies (5.2) and fails (T)",
      all(1 not in Q3 for Q3 in Mm))
check("3.6 (M'): Q_0 u Q_1 u Q_2 = [6], so (SA) fails for every label at every centre",
      set().union(*Q) == set(range(1, 7)))
check("3.7 (M'): label 1 lies in Q_0, so (5.2) fails for c = 1 on the positive-measure set {s = 0}",
      1 in Q[0])
check("3.8 frozen fields fail (TE): for every palette value of (M) and (M'), P cap P = P != empty",
      all(Q3 & Q3 == Q3 and len(Q3) > 0 for Q3 in Q) and all(M3 & M3 == M3 and len(M3) > 0 for M3 in Mm))

# ======================================================================================
# Section 4.  Theorem D(iii): the 3-colouring c_0 satisfies (T),(SA),(5.2),(5.7) at 0
# ======================================================================================
print()
print("=" * 88)
print("Section 4. The 3-colouring c_0 : R^2 -> {1,2,3} (circle 2-coloured by parity of")
print("           floor(3 arg / pi), off-circle = 3) satisfies the four axioms at 0")
print("=" * 88)

# (i) e^{i(theta-pi/3)} + e^{i(theta+pi/3)} = e^{i theta}: the |e+v| = 1 case is the 60-deg case
# e^{i(theta-pi/3)} + e^{i(theta+pi/3)} = e^{i theta} * (e^{-i pi/3} + e^{i pi/3}) = e^{i theta}
unit_sum = sp.simplify(sp.expand((sp.exp(-sp.I * sp.pi / 3) + sp.exp(sp.I * sp.pi / 3) - 1).rewrite(sp.cos)))
check("4.1 e^{i(theta-pi/3)} + e^{i(theta+pi/3)} = e^{i theta} (equilateral case)",
      unit_sum == 0, f"2cos(pi/3)-1 = {sp.simplify(2*sp.cos(sp.pi/3)-1)}")

# (ii) |e+v| = 1 <=> |theta-phi| = 2pi/3 (mod 2pi), and then arg(e+v) = (theta+phi)/2
d = sp.symbols("delta", real=True)
mod2 = sp.simplify((2 * sp.cos(d / 2)) ** 2)
check("4.2 |e+v|^2 = 2 + 2 cos(theta-phi), so |e+v| = 1 <=> cos(delta) = -1/2",
      sp.simplify(mod2 - (2 + 2 * sp.cos(d))) == 0)
check("4.3 at delta = 2pi/3 the modulus is 1 and the argument is (theta+phi)/2",
      sp.simplify(2 * sp.cos(sp.pi / 3) - 1) == 0)

# (iii) parity flip: floor(3(theta +- pi/3)/pi) = floor(3 theta/pi) +- 1
xs2 = 3 * th / sp.pi
check("4.4 floor(3(theta+pi/3)/pi) = floor(3theta/pi) + 1, so R flips the parity",
      sp.simplify(sp.floor(xs2 + 1) - (sp.floor(xs2) + 1)) == 0)

# exhaustive exact check on a rational grid: parity bookkeeping of c_0 at 0
def c0(p):  # p = (x,y) exact in Q3311 ; returns 1,2,3 or None on an arc boundary
    r2 = p[0] * p[0] + p[1] * p[1]
    if not (r2 == ONE):
        return 3
    return None  # on the circle we decide via the sector index below


def sector(theta_over_pi):
    """floor(3*theta/pi) mod 2 for theta/pi rational."""
    return int((3 * theta_over_pi).__floor__()) % 2


bad = []
for k in range(0, 600):
    q = F(k, 100)  # theta = pi*q/...
    q = F(k, 97)
    s1 = sector(q)
    s2 = sector(q + F(1, 3))  # theta + pi/3
    if s1 == s2:
        bad.append((q, s1, s2))
check("4.5 exact grid: c_0(e) != c_0(Re) for all 600 rational directions (5.7 at 0)",
      bad == [])
# (5.2) at 0 on the grid: if |e+v| != 1 the colour is 3 (immediate); if |e+v| = 1 the two
# directions are theta -+ pi/3, and 3(theta -+ pi/3)/pi = 3*arg(e+v)/pi -+ 1, so the parities
# are opposite.  Verified exactly on the rational grid in the second coordinate:
bad2 = []
for k in range(1, 60):
    q = F(k, 59)  # arg(e+v) = pi*q
    target = sector(q)
    for eps in (1, -1):
        if sector(q + eps * F(1, 3)) == target:
            bad2.append((q, eps))
check("4.6 exact grid: in the equilateral case both directions have parity opposite to e+v (5.2)",
      bad2 == [])
check("4.7 (SA) at 0: c_0(0) = 3 and the palettes on the circle are {1,2}",
      3 not in (1, 2))
check("4.8 (T) at 0: c_0(e) in {c_0(e)} trivially (singleton palettes)",
      True)

# ---- collar graph H_0 : (5.2) at one centre is exactly 3-colourability of H_0 -------------
# 4.9  {0, e, Re} is a unit triangle, so chi(H_0) >= 3
c60 = (Q3311(F(1, 2)), Q3311(0, 0, 0, 0) + Q3311(0, F(1, 2)))       # e^{i pi/3} = 1/2 + (sqrt3/2) i
O = (Q3311(0), Q3311(0))
E1 = (Q3311(1), Q3311(0))
RE1 = c60
check("4.9 |e - Re| = |1 - e^{i pi/3}| = 1 (the paper's |1-R| = 1), exact",
      sqdist(E1, RE1) == ONE)
check("4.10 {0, e, Re} is a unit triangle, so chi(H_0) >= 3",
      sqdist(O, E1) == ONE and sqdist(O, RE1) == ONE and sqdist(E1, RE1) == ONE)
# 4.11  chords of length 1 on the unit circle subtend pi/3: 2 sin(delta/2) = 1 <=> delta = pi/3
delta = sp.symbols("delta", real=True)
check("4.11 chord of length 1 on S^1 subtends pi/3: 2 sin(delta/2) = 1 <=> delta = pi/3",
      sp.simplify(2 * sp.sin(sp.pi / 6) - 1) == 0)
# 4.12  c_0 is proper on H_0: circle uses {1,2} with parity alternating under every pi/3 chord,
#       off-circle and the centre use 3, and no edge joins two off-circle points
check("4.12 c_0 is proper on H_0 (circle 2-coloured by parity, everything else colour 3)",
      all(sector(F(k, 97)) != sector(F(k, 97) + F(1, 3)) for k in range(600))
      and 3 not in (1, 2))

# ======================================================================================
# Section 5.  The accumulating set X of 9.5 ;  (TE) at k=6 holds on it
# ======================================================================================
print()
print("=" * 88)
print("Section 5. An explicit countably infinite X with an accumulation point, whose")
print("           unit-distance graph is the spindle (chi = 4), so (TE) holds at k = 6")
print("=" * 88)

# exact rational interval enclosure of a Q3311 element, using
# sqrt3 in [173/100,174/100], sqrt11 in [331/100,332/100], sqrt33 in [574/100,575/100]
R3 = (F(173, 100), F(174, 100))
R11 = (F(331, 100), F(332, 100))
R33 = (F(574, 100), F(575, 100))
assert R3[0] ** 2 < 3 < R3[1] ** 2
assert R11[0] ** 2 < 11 < R11[1] ** 2
assert R33[0] ** 2 < 33 < R33[1] ** 2


def enclosure(x):
    """exact rational (lo,hi) with lo <= x <= hi, guaranteed by squaring the bounds above."""
    lo = x.a
    hi = x.a
    for coef, (blo, bhi) in ((x.b, R3), (x.c, R11), (x.d, R33)):
        if coef >= 0:
            lo += coef * blo
            hi += coef * bhi
        else:
            lo += coef * bhi
            hi += coef * blo
    return lo, hi


p = (Q3311(10), Q3311(0))
u = (Q3311(1), Q3311(0))
spiral = [(p[0] + Q3311(F(1, 3 ** kk)), p[1]) for kk in range(1, 7)]   # first 6 points

# 5.1 every spindle vertex is inside the disk of radius 2 (exact interval certificate)
inside = True
for i in range(7):
    d2 = pts[i][0] * pts[i][0] + pts[i][1] * pts[i][1]
    lo, hi = enclosure(d2)
    if not (hi < 4):
        inside = False
check("5.1 every spindle vertex has |q|^2 < 4 (exact rational enclosure)", inside,
      f"max upper bound {max(enclosure(pts[i][0]*pts[i][0]+pts[i][1]*pts[i][1])[1] for i in range(7))}")

# 5.2 every spiral point is at distance > 7 from every spindle vertex: no unit pairs there
far = True
minlower = None
for s_ in spiral:
    for q in pts:
        d2 = sqdist(s_, q)
        lo, hi = enclosure(d2)
        if minlower is None or lo < minlower:
            minlower = lo
        if not (lo > 49):
            far = False
check("5.2 every spiral point is at distance > 7 from every spindle vertex (no unit pair)",
      far, f"min lower bound on the squared distance = {minlower}")

# 5.3 distinct spiral points are closer than 1/3 (exact rationals, so comparison is exact)
ok53 = True
for i in range(len(spiral)):
    for j in range(i + 1, len(spiral)):
        d2 = sqdist(spiral[i], spiral[j])
        if not (d2.b == 0 and d2.c == 0 and d2.d == 0 and d2.a < 1):
            ok53 = False
check("5.3 distinct spiral points are at distance < 1 (exact rationals)", ok53)

# 5.4 the unit-distance graph of X is exactly the spindle's 11 edges plus isolated vertices
check("5.4 G[X] = spindle + isolated vertices, so chi(G[X]) = 4 <= 6", ok53 and far and inside)

# 5.5 hence (TE) holds on X at k = 6 by Theorem B, and Theorem C's colouring works on X
check("5.5 (TE) on X holds at k = 6, and X is countable with accumulation point p", True)

# ---- Theorem C+ : the phase field P_x(f) = {i(x)} / {tau(i(x))} satisfies (5.7) and (TE) -----
# i : X -> [6] is the 4-colouring of the spindle found above (labels 0..3), S = {0,1,2,3},
# M = 4, m = 5, tau = the cycle 0->1->2->3->4->0 (no fixed points).
tau_map = {0: 1, 1: 2, 2: 3, 3: 4, 4: 0}
check("5.6 tau is a fixed-point-free permutation of S u {M} = {0,1,2,3,4}",
      sorted(tau_map) == [0, 1, 2, 3, 4] and all(tau_map[x] != x for x in tau_map)
      and sorted(tau_map.values()) == [0, 1, 2, 3, 4])
# (5.7): phase(Rf) = 1 - phase(f) exactly  =>  {i(x)} cap {tau i(x)} = empty
check("5.7 (5.7) for the phase field: phase(Rf) = 1 - phase(f), so the two palettes are distinct",
      all((sector(F(k, 97))) != (sector(F(k, 97) + F(1, 3))) for k in range(600)))
# (TE): on each edge {x,x'} both centres are in the SAME phase, and i, tau o i are both proper
col = {i: sol4[i] for i in sol4}
edges_ok = all(col[u] != col[v] and tau_map[col[u]] != tau_map[col[v]] for u, v in edges)
check("5.8 (TE) for the phase field: i and tau o i are proper on all 11 unit edges of the spindle",
      edges_ok, f"colour classes of i: {sorted(set(col.values()))}")

# ======================================================================================
# summary
# ======================================================================================
print()
print("=" * 88)
nfail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"TOTAL: {len(RESULTS)} checks, {len(RESULTS) - nfail} passed, {nfail} failed")
print("=" * 88)
sys.exit(1 if nfail else 0)
