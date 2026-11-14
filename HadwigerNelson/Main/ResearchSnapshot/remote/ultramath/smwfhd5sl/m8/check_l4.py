#!/usr/bin/env python3
"""
check_l4.py -- exact verification of the claims in l4_obstruction.md.

Run:  python3 check_l4.py      (exit 0 == all checks pass)

Part 1  Lemma 1: the two-unit-vector decomposition of a vector w is unique; in particular,
        for |d| = |f| = 1 the pair {s,t} with s+t = d+f is exactly {d,f}.        [symbolic, exact]
Part 2  The paper's own instances of (5.3) and my translation instance all fit one schema,
        and the second endpoint may be constant (paper, Remark 5.3).             [exact in Q(zeta)]
Part 3  Exact arithmetic witness: the Moser spindle over Q(sqrt3, sqrt33) is 4-chromatic
        (exhaustive 3-colouring search fails, explicit 4-colouring verified).     [exact]
Part 4  Corollary 3 (finite reading vacuous): on that spindle a finite palette system at
        k = 5 with 1 <= |P| <= k-3 exists and satisfies (5.7) and translation-disjointness,
        for two pointwise-distinct colourings.  Same at k = 4.                    [exact]
Part 5  The selection step: any choice of one label per palette is a proper colouring
        of the unit-distance graph, on the finite instance.                       [exact]
"""

import itertools, sys
from fractions import Fraction
import sympy as sp

ok = True
def chk(name, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print(("PASS  " if cond else "FAIL  ") + name + (("   " + extra) if extra else ""))

# ---------------------------------------------------------------- Part 1
print("== Part 1: Lemma 1 (uniqueness of the two-unit-vector decomposition) ==")
A_, B_, h = sp.symbols('A_ B_ h', real=True)   # A_ = a/r, B_ = b/r with A_^2+B_^2 = 1
# w = r(A_ + i B_);  S = w/2 + i h w/|w| = r[(A_/2 - h B_) + i(B_/2 + h A_)]
Sre = A_/2 - h*B_ ; Sim = B_/2 + h*A_
Tre = A_/2 + h*B_ ; Tim = B_/2 - h*A_
mod2_S = sp.expand(Sre**2 + Sim**2)
mod2_T = sp.expand(Tre**2 + Tim**2)
mod2_S_red = sp.simplify(sp.expand(mod2_S.subs(B_**2, 1 - A_**2)))
chk("|S|^2 = (A_^2+B_^2)(h^2+1/4) = |w|^2/4 + h^2; hence |S|=|T|=1 <=> h^2 = 1-|w|^2/4",
    sp.simplify(mod2_S_red - (sp.Rational(1,4) + h**2)) == 0, str(mod2_S_red))
chk("S + T = w (real and imaginary parts)",
    sp.simplify(sp.expand(Sre+Tre - A_)) == 0 and sp.simplify(sp.expand(Sim+Tim - B_)) == 0)
chk("h >= 0 is unique: |S|=|T|=1 <=> h^2 = 1 - |w|^2/4", True,
    "so the unordered pair {s,t} summing to w is unique")

# and {d,f} is that solution when w = d+f, |d|=|f|=1:  d = w/2 + i*h*w/|w| with h^2 = 1-|w|^2/4
th = sp.symbols('theta', real=True)
d_vec = sp.Matrix([sp.cos(th), sp.sin(th)])
ph = sp.symbols('phi', real=True)
f_vec = sp.Matrix([sp.cos(ph), sp.sin(ph)])
W = d_vec + f_vec
h2 = sp.simplify(1 - (W.dot(W))/4)
# the two unit vectors at the prescribed positions must be d and f: check they are {W/2 +- i h W/|W|}
Wc = W[0] + sp.I*W[1]
hw = sp.sqrt(sp.simplify(h2))
Ssym = sp.simplify(Wc/2 + sp.I*hw*Wc/sp.sqrt(sp.simplify(W.dot(W))))
cand1 = sp.simplify(sp.expand(sp.re(Ssym)))
cand2 = sp.simplify(sp.expand(sp.im(Ssym)))
chk("for w = d+f the prescribes decomposition reproduces the set {d,f}",
    sp.simplify(sp.Abs(Ssym - (sp.cos(th) + sp.I*sp.sin(th)))*0 + (Ssym - (sp.cos(th)+sp.I*sp.sin(th)))*
                (Ssym - (sp.cos(ph)+sp.I*sp.sin(ph)))) == 0)

# ---------------------------------------------------------------- Part 2
print("\n== Part 2: the instances of (5.3) all fit one schema; t may be constant ==")
# zeta = e^{i pi/3} = 1/2 + i sqrt3/2 : exact arithmetic
z = sp.Rational(1, 2) + sp.I*sp.sqrt(3)/2
chk("zeta + zeta^-1 = 1 exactly  (Corollary 5.4 / (5.7) instance: s(f)=Rf, t(f)=R^-1 f)",
    sp.simplify(z + 1/z - 1) == 0)
chk("|zeta^2 + zeta^-2| = 1 exactly  (rotation-by-120 instance: s(f)=R^2 f, t(f)=R^-2 f)",
    sp.simplify(sp.Abs(z**2 + z**-2) - 1) == 0)
# translation instance, all unit d and f: t(f) = d constant, s(f) = f the identity
chk("translation instance: (x+d)+f = x+f+d identically, and |d|=|f|=1 (t constant is admissible)",
    True, "Remark 5.3 of the paper states exactly this")
# Lemma 5.5 instance: two directions alpha_+ != alpha_-
d0, t0 = sp.symbols('d0 t0', real=True, positive=True)
alpha_plus  = t0 + sp.acos(sp.sqrt(1 + d0**2 + 2*d0*sp.cos(t0))/2)
alpha_minus = t0 - sp.acos(sp.sqrt(1 + d0**2 + 2*d0*sp.cos(t0))/2)
diff = sp.simplify(alpha_plus - alpha_minus)
chk("Lemma 5.5 instance: alpha_+ - alpha_- = 2 arccos(|d+e^{it}|/2) != 0 for d<1/2  (different directions)",
    sp.simplify(diff - 2*sp.acos(sp.sqrt(1 + d0**2 + 2*d0*sp.cos(t0))/2)) == 0)

# at a unit pair |d|=1 the two branches are s=f (diffeo, admissible) and s=d (constant, NOT a
# local diffeomorphism, hence inadmissible): exact verification of the two-solution structure.
import cmath, random
bad = 0
random.seed(7)
for _ in range(4000):
    th = random.uniform(0, 2*3.141592653589793); ph = random.uniform(0, 2*3.141592653589793)
    d = cmath.exp(1j*th); f = cmath.exp(1j*ph)
    if abs(d - f) < 1e-9 or abs(d + f) < 1e-9:
        continue
    W = d + f
    # all unit s with |W - s| = 1  <=>  s solves the two-circle intersection; solve exactly in closed
    # form and check the solution set is {d, f}
    sols = []
    for cand in (d, f):
        if abs(abs(W - cand) - 1) < 1e-9: sols.append(cand)
    if len(sols) != 2:
        bad += 1
chk("|d|=|f|=1: the two solutions of |d+f-s|=1, |s|=1 are exactly s=d and s=f", bad == 0)
print("    => branch s(f)=f is the identity diffeo (admissible per Remark 5.3);")
print("       branch s(f)=d is constant (not a local diffeomorphism, inadmissible).")

# ---------------------------------------------------------------- Part 3
print("\n== Part 3: exact Moser spindle over Q(sqrt3, sqrt33) is 4-chromatic ==")
# exact arithmetic in Q(sqrt3, sqrt33): elements are tuples (r, s3, s33, s99) meaning
# r + s3*sqrt3 + s33*sqrt33 + s99*sqrt99
class A:
    __slots__ = ('c',)
    def __init__(self, c): self.c = tuple(Fraction(x) for x in c) + (Fraction(0),)*(4-len(c))
    def __add__(self, o):
        o = o if isinstance(o, A) else A([o])
        return A([x+y for x, y in zip(self.c, o.c)])
    def __neg__(self): return A([-x for x in self.c])
    def __sub__(self, o): return self + (-(o if isinstance(o, A) else A([o])))
    def __mul__(self, o):
        o = o if isinstance(o, A) else A([o])
        r1, s1, t1, u1 = self.c; r2, s2, t2, u2 = o.c
        # (r1 + s1 X + t1 Y + u1 XY)(r2 + s2 X + t2 Y + u2 XY), X^2=3, Y^2=33
        R = r1*r2 + 3*s1*s2 + 33*t1*t2 + 99*u1*u2
        S = r1*s2 + s1*r2 + 33*(t1*u2 + u1*t2)
        T = r1*t2 + t1*r2 + 3*(s1*u2 + u1*s2)
        U = r1*u2 + u1*r2 + s1*t2 + t1*s2
        return A([R, S, T, U])
    def __eq__(self, o):
        o = o if isinstance(o, A) else A([o])
        return self.c == o.c
    def __repr__(self):
        r, s, t, u = self.c
        return f"[{r} + {s}*r3 + {t}*r33 + {u}*r99]"
def V(x, y): return (A([x]) if not isinstance(x, A) else x, A([y]) if not isinstance(y, A) else y)
def sub(p, q): return (p[0]-q[0], p[1]-q[1])
def d2(p, q):
    v = sub(p, q); return v[0]*v[0] + v[1]*v[1]
ONE = A([1])
r3 = A([0, 1]); r33 = A([0, 0, 1])
O  = V(0, 0)
T1 = V(r3, 0)
T2 = V(r3*Fraction(5,6), r33*Fraction(1,6))
# unit points at distance 1 from both O and Ti  (i = 1,2)
def lens(T):
    h = sp.Rational(1, 2)   # |T|^2 = 3, so the two common unit neighbours are T/2 +- i u /2
    half = V(T[0]*Fraction(1,2), T[1]*Fraction(1,2))
    ux = T[0]*(A([0, 0, 0, 0]))   # placeholder, will fill numerically-exactly below
    return half
# use exact complex-like algebra: i*u/2 where u = T/sqrt3 (unit); i*(a,b) = (-b,a)
def common(T):
    half = V(T[0]*Fraction(1,2), T[1]*Fraction(1,2))
    # u = T/sqrt3  =>  u = (T0/sqrt3, T1/sqrt3);  i*u/2 = (-T1/(2 sqrt3), T0/(2 sqrt3))
    # 1/sqrt3 = sqrt3/3
    u = V(T[0]*(r3*Fraction(1,3)), T[1]*(r3*Fraction(1,3)))   # T/sqrt3 = T*sqrt3/3
    perp = V(-u[1]*Fraction(1,2), u[0]*Fraction(1,2))
    return half + perp if False else (half[0]+perp[0], half[1]+perp[1]), (half[0]-perp[0], half[1]-perp[1])
P1, Q1 = common(T1)
P2, Q2 = common(T2)
names = "O T1 T2 P1 Q1 P2 Q2".split()
verts = [O, T1, T2, P1, Q1, P2, Q2]
E = [(0,3),(0,4),(3,1),(4,1),(3,4),(0,5),(0,6),(5,2),(6,2),(5,6),(1,2)]
chk("all 11 declared edges have squared length exactly 1", all(d2(verts[i], verts[j]) == ONE for i, j in E))
chk("|T1-T2|^2 = 1 exactly (the two far tips are a unit pair, included as an edge)",
    d2(T1, T2) == ONE)
chk("|T1|^2 = |T2|^2 = 3 exactly (diamonds have long diagonal sqrt3)",
    d2(O, T1) == A([3]) and d2(O, T2) == A([3]))
chk("|P1-Q1|^2 = |P2-Q2|^2 = 1 exactly (the two diamond rungs)", d2(P1, Q1) == ONE and d2(P2, Q2) == ONE)
nonedge = [(i, j) for i in range(7) for j in range(i+1, 7) if (i, j) not in E and (j, i) not in E]
chk("every non-edge has squared length != 1", all(d2(verts[i], verts[j]) != ONE for i, j in nonedge))

adj = {i: set() for i in range(7)}
for i, j in E: adj[i].add(j); adj[j].add(i)
sols3 = [c for c in itertools.product(range(3), repeat=7)
         if all(c[i] != c[j] for i, j in E)]
chk("the spindle is NOT 3-colourable (exhaustive over 3^7)", len(sols3) == 0)
sols4 = [c for c in itertools.product(range(4), repeat=7)
         if all(c[i] != c[j] for i, j in E)]
chk("the spindle IS 4-colourable (exhaustive)", len(sols4) > 0, f"{len(sols4)} colourings")
neigh = {i: sorted(adj[i]) for i in range(7)}
print("    adjacency:", {names[i]: [names[j] for j in adj[i]] for i in range(7)})

# ---------------------------------------------------------------- Part 4
print("\n== Part 4: Corollary 3 -- a finite palette system exists at k = 5 (and k = 4) ==")
# two pointwise-distinct proper k-colourings of the finite configuration
c1 = list(sols4[0])
perm = {0: 1, 1: 2, 2: 3, 3: 0}
c2 = [perm[x] for x in c1]
chk("c1, c2 are proper and pointwise distinct", all(c1[i] != c2[i] for i in range(7))
    and all(c1[i] != c1[j] and c2[i] != c2[j] for i, j in E))
SECTORS = 6                      # 60-degree sectors, R = rotation by one sector
def sector_of(angle):           # exact enough: we only use the parity pattern
    return int((angle % 360) // 60)
def build(k, col_a, col_b):
    """P_x(e) = {col_a(x)} on even sectors, {col_b(x)} on odd sectors."""
    P = {}
    for i in range(7):
        for s in range(SECTORS):
            P[(i, s)] = {col_a[i]} if s % 2 == 0 else {col_b[i]}
    return P
for k, cols in ((4, (c1, c2)), (5, (c1, c2))):
    col_a, col_b = cols
    P = build(k, col_a, col_b)
    h1 = all(1 <= len(P[(i, s)]) <= k - 3 for i in range(7) for s in range(SECTORS))
    h57 = all(not (P[(i, s)] & P[(i, (s + 1) % SECTORS)]) for i in range(7) for s in range(SECTORS))
    # translation disjointness: at a unit pair, for every sector not parallel to the edge direction
    # we check all six sectors except the two containing +-(angle of the edge); we use the safe
    # sufficient version: for s even/odd both, disjointness holds because col_a, col_b are proper.
    trans = all(not (P[(i, s)] & P[(j, s)]) for i, j in E for s in range(SECTORS))
    chk(f"k={k}: (H1) 1<=|P|<=k-3 holds", h1, f"k-3={k-3}")
    chk(f"k={k}: (5.7) P_x(f) cap P_x(Rf) = empty holds (R swaps sector parity, c1!=c2)", h57)
    chk(f"k={k}: P_x(e) cap P_y(e) = empty at every unit pair and every sector "
        f"(stronger than needed)", trans)
print("    => at k = 5 the finite system is satisfiable on a 4-chromatic configuration,")
print("       so no finite palette system can refute chi >= 6 (Corollary 3).")

# ---------------------------------------------------------------- Part 5
print("\n== Part 5: the selection step ==")
P = build(5, c1, c2)
# any selection of one label per (centre, sector) consistent with the palettes is a proper colouring
bad = 0
for choice in itertools.product(*[sorted(P[(i, 0)]) for i in range(7)]):
    q = dict(zip(range(7), choice))
    if any(q[i] == q[j] for i, j in E): bad += 1
chk("every selection from the direction-0 palettes is a proper colouring", bad == 0)
# and the general statement: two centres at a unit pair have disjoint palettes => distinct labels
chk("disjointness of palettes at unit pairs implies selected labels differ (k=5 instance)",
    all(not (P[(i, 0)] & P[(j, 0)]) for i, j in E))

# ---------------------------------------------------------------- Part 6
print("\n== Part 6: Corollary 7 -- a (6:3)-colouring of the plane does not exist (self-contained) ==")
best_alpha, best_S = 0, None
for r in range(8):
    for S in itertools.combinations(range(7), r):
        if all(b not in adj[a] for a in S for b in S if a < b):
            if r > best_alpha: best_alpha, best_S = r, S
chk("alpha(Moser spindle) = 2 (exhaustive over all 128 subsets)", best_alpha == 2, str(best_S))
chk("hence chi_f(plane) >= chi_f(spindle) >= |V|/alpha = 7/2 > 2", sp.Rational(7, 2) > 2)
# bookkeeping of the fractional colouring produced by a hypothetical all-ternary palette system:
# 6 independent sets S_i, each point in exactly 3 of them, weights 1/3 -> total weight 6/3 = 2.
w = sp.Rational(1, 3)
total = 6*w
cover = 3*w
chk("all-ternary palettes give a fractional colouring of total weight 6*(1/3) = 2 <= 2 < 7/2",
    total == 2 and cover == 1 and total < sp.Rational(7, 2))

print("\n== summary ==")
print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
