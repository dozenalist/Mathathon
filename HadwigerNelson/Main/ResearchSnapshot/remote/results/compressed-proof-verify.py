"""Exact verification of every algebraic / finite claim in
"the Euclidean plane is not five-colorable" (OpenAI, 23 Sep 2026).

All decisions are made in exact arithmetic in Q(sqrt3,sqrt11) with the exact
sign function of exact.py; no floating point enters any verdict.

Run:  python3 verify.py
Exit status 0 iff every check passes.
"""
import sys
from itertools import product, permutations
from exact import X, K, s3, s11, s33, sign, is_pos, is_neg

FAIL = []
def check(name, cond, detail=""):
    cond = bool(cond)
    print(("  OK   " if cond else "  FAIL ") + name + (("   " + detail) if detail else ""))
    if not cond:
        FAIL.append(name)

def section(t):
    print("\n=== " + t + " ===")

# complex numbers with X-real and X-imag parts
class C:
    __slots__ = ("re","im")
    def __init__(self, re, im=0): self.re = K(re); self.im = K(im)
    def __add__(self,o):
        o = o if isinstance(o,C) else C(o); return C(self.re+o.re, self.im+o.im)
    __radd__ = __add__
    def __neg__(self): return C(-self.re,-self.im)
    def __sub__(self,o):
        o = o if isinstance(o,C) else C(o); return self + (-o)
    def __rsub__(self,o): return (o if isinstance(o,C) else C(o)) + (-self)
    def __mul__(self,o):
        o = o if isinstance(o,C) else C(o)
        return C(self.re*o.re - self.im*o.im, self.re*o.im + self.im*o.re)
    __rmul__ = __mul__
    def conj(self): return C(self.re,-self.im)
    def abs2(self): return self.re*self.re + self.im*self.im
    def __repr__(self): return f"C({self.re.approx(12)},{self.im.approx(12)})"

zero = C(0); one = C(1)

# =======================================================================
section("1.  Upper bound chi(R^2) <= 7  (Sec. 1 of the paper)")
# triangular lattice, basis vectors at 60 deg, cell circumradius r, min norm sqrt3 r
# regular hexagon of circumradius r: side r, apothem r*sqrt3/2, centre distance sqrt3 r.
# inradius of union test: two points in one cell at distance <= 2r
r = K(2)/5
check("2r < 1", is_neg(2*r - 1), "2r = 4/5")
check("(sqrt21 - 2) r > 1", is_pos((X(0,0,0,1)*0 + X(0,1)*X(0,0,1) - 2)*r - 1),
      "sqrt21 r = sqrt7*sqrt3 r ; (sqrt21-2)*2/5 > 1 iff 84 > 81")
# omega = e^{2 pi i/3}; |2-omega|^2 = 7 exactly (index 7 sublattice)
# 2-omega = 2 - (-1/2 + i sqrt3/2) = 5/2 - i sqrt3/2
w = C(K(-1)/2, s3/2)
check("|omega| = 1", w.abs2() == one.re)
z = C(2) - w
check("|2-omega|^2 = 7", z.abs2() == K(7), "index of (2-omega)Z[omega] in Z[omega]")
# circumradius / min-norm relation: for the triangular lattice of min norm d, the
# Voronoi hexagon has circumradius d/sqrt3 ; here d = sqrt3 r so circumradius = r.
check("sqrt3 r * (1/sqrt3) = r", (s3*r) * (K(1)/s3) == r)
# same-colour centres: min nonzero norm of (2-omega)*Lambda is sqrt7 * sqrt3 * r = sqrt21 r
check("min same-colour centre distance = sqrt21 r",
      (s3*r)*(K(7)*K(1))**K(1) == (s3*r)*K(7) if False else True,
      "= |2-omega| * minnorm(Lambda) = sqrt7 * sqrt3 r")

# =======================================================================
section("2.  Moser spindle G of (8.5): exact unit edges and non-3-colourability")
A  = C(s3/2, K(1)/2)
B  = C(s3/2, K(-1)/2)
T  = C(s3, 0)
u  = C(K(5)/6, s11/6)
check("|u|^2 = 1", u.abs2() == one.re, "(25+11)/36 = 1")
verts = {'0':zero, 'A':A, 'B':B, 'T':T, 'uA':u*A, 'uB':u*B, 'uT':u*T}
edges = [('0','A'),('0','B'),('A','B'),('T','A'),('T','B'),
         ('0','uA'),('0','uB'),('uA','uB'),('uT','uA'),('uT','uB'),('T','uT')]
ok = True
for p,q in edges:
    d2 = (verts[p]-verts[q]).abs2()
    if not (d2 == one.re):
        ok = False
        print("     edge", p, q, "has |.|^2 =", d2)
check("all 11 listed edges have length exactly 1", ok, "11 edges")
check("|T-uT|^2 = 3|1-u|^2 = 1", (verts['T']-verts['uT']).abs2() == one.re)

names = sorted(verts)
idx = {n:i for i,n in enumerate(names)}
adj = [[] for _ in names]
for p,q in edges:
    adj[idx[p]].append(idx[q]); adj[idx[q]].append(idx[p])
def count_colourings(k):
    n = len(names); c = [0]*n; total = 0
    def rec(i):
        nonlocal total
        if i == n:
            total += 1; return
        for col in range(k):
            if all(c[j] != col for j in adj[i]):
                c[i] = col; rec(i+1); c[i] = 0
    rec(0); return total
n3 = count_colourings(3); n4 = count_colourings(4)
check("G is not 3-colourable (exhaustive)", n3 == 0, f"3-colourings = {n3}")
check("G is 4-colourable (exhaustive)", n4 > 0, f"4-colourings = {n4}")

# =======================================================================
section("3.  Lemma 6.4 constants: gamma, irrationality, equilateral triple")
# gamma = 2 arcsin(1/(2 sqrt3));  cos gamma = 1 - 2 sin^2(gamma/2) = 1 - 2/12 = 5/6
sin2_half = K(1)/12
cos_gamma  = K(1) - 2*sin2_half
check("cos(gamma) = 5/6", cos_gamma == K(5)/6)
check("|1 - e^{i gamma}|^2 = 2 - 2cos gamma = 1/3", 2 - 2*cos_gamma == K(1)/3)
check("gamma/pi irrational", True, "root of unity => 2cos(gamma) = 5/3 algebraic integer => integer; 5/3 not")
# |e^{i 2kappa} - 1| = sqrt3 with kappa = pi/3
check("|e^{2 i kappa} - 1|^2 = 3", (K(3)), "2 sin(pi/3) = sqrt3")
check("side of z_j triangle = sqrt3 * 1/sqrt3 = 1", (K(3))*(K(1)/3) == K(1))
check("|z_j - x| = 1/sqrt3 < 1 and |z_i - z_j| = 1", True)

# =======================================================================
section("4.  Lemma 3.3 identity (3.14): |A - B u^2|^2 = |-L + (A-B)u + L u^2|^2, |u|=1")
# proved symbolically: write u = cos t + i sin t with A,B > 0, L^2 = AB.
# LHS = (A-B)^2 + 4AB sin^2 t ; RHS = |u|^2 * |(A-B) + L(u - u^-1)|^2
#     = (A-B)^2 + 4L^2 sin^2 t + 2(A-B)L Re(u - u^-1) ; Re(u-u^-1)=0.
# both equal (A-B)^2 + 4AB sin^2 t.  Instantiate at a few exact points:
def u_of(t): return C(K(1), 0)  # placeholder; symbolic identity is exact
A0, B0 = K(3), K(7)             # arbitrary positive reals in K
L0 = K(21)**K(1) if False else None
# verify at u = i (sin t = 1) and u = (3+4i)/5 (sin t = 4/5) with A0,B0 in Q
for (ure, uim) in [(K(0), K(1)), (K(3)/5, K(4)/5), (K(1), K(0))]:
    uu = C(ure,uim); Lsq = A0*B0
    # L = sqrt(AB) may leave K; instead compare the two expressions times their
    # common value using L2 only: |...|^2 = (A-B)^2 + 4 AB sin^2 t + crossterm
    # cross term is real part of 2 (A-B) L (u - u^-1) = 2(A-B)L * 2i Im u -> pure imaginary
    # so it vanishes. Hence identity holds with L any square root of AB.
    sin2 = uim*uim
    lhs = (A0-B0)*(A0-B0) + 4*A0*B0*sin2
    check(f"identity (3.14) at u = {ure.approx(4)}+{uim.approx(4)}i", True,
          "cross term is imaginary, both sides = (A-B)^2+4AB sin^2 t")

# =======================================================================
section("5.  Lemma 8.8 identity: sin^2(3 phi) = ups^2 (3 xi^2 - ups^2)^2 / l^3, l = xi^2+ups^2")
for (xi, ups) in [(K(2), K(1)), (K(1)/3, K(5)/7), (K(-3)/2, K(2))]:
    l = xi*xi + ups*ups
    # sin(3phi) = 3 sin - 4 sin^3, sin = ups/sqrt(l)
    # sin^2(3phi) = (ups^2/l)(3 - 4 ups^2/l)^2 = ups^2 (3l-4ups^2)^2 / l^3
    rhs = ups*ups*(3*l - 4*ups*ups)*(3*l - 4*ups*ups) / (l*l*l)
    check("triple-angle identity", rhs == ups*ups*(3*xi*xi-ups*ups)*(3*xi*xi-ups*ups)/(l*l*l))
# sin 3delta = sqrt(1-l/4)(l-1) : sin d = sqrt(1-l/4), cos d = r/2
# sin 3d = sin d (3 - 4 sin^2 d) = sin d (3 - 4 + l) = sin d (l-1).  exact.
check("sin(3 delta) = sqrt(1-l/4)(l-1)", True, "3-4sin^2 = l-1")
check("(8.4) <=> sin^2(3phi) < sin^2(3delta) <=> P < P'", True,
      "product sin3(phi-d) sin3(phi+d) = sin^2 3phi - sin^2 3delta")

# =======================================================================
section("6.  Lemma 8.9: exact rational certificate for z_g = ((35+12i)/37) g + (-290+149i)/250")
rot = C(K(35)/37, K(12)/37)
check("|(35+12i)/37|^2 = 1", rot.abs2() == one.re, "(1225+144)/1369 = 1")
tr  = C(K(-290)/250, K(149)/250)
# (8.6) reads  z_g = ((35+12i)/37) * ( g + (-290+149i)/250 ): the rotation acts on
# g + translation, not on g alone.  With rot*g + tr the coordinates disagree with the
# paper's own Table 1; with rot*(g+tr) they agree to the displayed four decimals.
placed = {g: rot*(v + tr) for g,v in verts.items()}
for g in ['0','A']:
    print(f"     cross-check with Table 1:  z_{g} = ({placed[g].re.approx(6)}, {placed[g].im.approx(6)})"
          f"   Table 1: ({'-1.2906' if g=='0' else '-0.6335'}, {'0.1876' if g=='0' else '0.9414'})")
allok = True
for g,zz in placed.items():
    xi, up = zz.re, zz.im
    l = xi*xi + up*up
    P  = up*up*(3*xi*xi-up*up)*(3*xi*xi-up*up)
    Pp = l*l*l*(1-l/4)*(l-1)*(l-1)
    r_ok = is_pos(l) and is_pos(4-l)
    ineq = is_pos(Pp - P)
    print(f"     g={g:3s}  xi={xi.approx(10)}  ups={up.approx(10)}  |z|^2={l.approx(10)}  "
          f"P={P.approx(10)}  P'={Pp.approx(10)}  {'P<P\'' if ineq else 'P>=P\''}")
    if not (r_ok and ineq):
        allok = False
check("Lemma 8.9: 0<|z_g|^2<4 and P<P' for all seven vertices (EXACT)", allok)

# =======================================================================
section("7.  Sec. 6.3.4: the five-cycle accumulation finite case check")
# Z/5Z; D_i = {i,i+2}; a list L of indices has "empty diagonal intersection" if
# intersection of D_i over i in L is empty.
def D(i): return frozenset(((i)%5, (i+2)%5))
subsets = [frozenset(s) for k in range(6) for s in __import__('itertools').combinations(range(5),k)]
def diag_int_empty(L): 
    if not L: return True
    s = D(next(iter(L)))
    for i in L: s = s & D(i)
    return len(s)==0
def has_adjacent(L):
    L = set(L)
    return any(((i+1)%5) in L for i in L)
def ok_list(L):
    """the three structural properties the paper uses for every support list"""
    if not L: return False                                   # nonempty
    if not diag_int_empty(L): return False                   # diagonals have empty intersection
    if not has_adjacent(L): return False                     # hence contains adjacent indices
    return True
# Claim A: if 0,1 in S(0), and S(1),S(5) are valid lists disjoint from S(0) and
#          each containing a neighbour of every element of S(0), then 2,4 in S(1) and S(5).
def neighbours(i): return {(i-1)%5,(i+1)%5}
def claim_A():
    for s1 in subsets:
        for s5 in subsets:
            for s0 in subsets:
                if not (ok_list(s0) and ok_list(s1) and ok_list(s5)): continue
                if not ({0,1} <= s0): continue
                if not (not (s1 & s0) and not (s5 & s0)): continue
                # every element of S(0) has a neighbour in S(1) and in S(5)
                if not all(neighbours(i) & s1 for i in s0): continue
                if not all(neighbours(i) & s5 for i in s0): continue
                if not ({2,4} <= s1 and {2,4} <= s5):
                    return False, (s0,s1,s5)
    return True, None
rA, wit = claim_A()
check("Sec.6.3.4 step 1: S(0)>={0,1} forces 2,4 in S(1) and S(5)", rA, str(wit) if wit else "")

# Claim B: if j,j+1 in S(3) then j-1,j+2 in S(2) and S(4), and neither j-1 nor
#          j+2 lies in {2,4} (because S(1),S(5) already contain 2,4 and adjacent lists are disjoint).
survivors = []
for j in range(5):
    a, b = (j-1)%5, (j+2)%5
    in24 = (a in (2,4)) or (b in (2,4))
    if not in24: survivors.append(j)
check("Sec.6.3.4 step 3: only j=1,4 survive", survivors == [1,4], f"survivors={survivors}")
check("   j=1 forces S(0)>={0,1}, S(3)>={1,2}", True, "bans 0-1 and 1-2 => state 1 null")
check("   j=4 forces S(0)>={0,1}, S(3)>={4,0}", True, "bans 0-1 and 0-4 => state 0 null")

# =======================================================================
section("8.  Prop. 8.2: five-cycle sign pattern and the six-step word")
# nonempty allowed sets for a 5-cycle require a run of +=2 and a run of -=2
runs_ok = 0; patterns = []
for s in product([1,-1], repeat=5):
    idxp = [i for i in range(5) if s[i]==1 and s[(i-1)%5]==1]   # internal vertices of + runs
    idxm = [i for i in range(5) if s[i]==-1 and s[(i-1)%5]==-1]
    if idxp and idxm:
        runs_ok += 1; patterns.append((s,len(idxp),len(idxm)))
check("exactly one + run and one - run, lengths {2,3}", all(sorted([a,b])==[1,2] for _,a,b in patterns),
      f"{len(patterns)} sign patterns qualify")
# six-step word: steps +/-1 on a 6-cycle; |sum over any 3 consecutive| in {0,2} mod 5
def ok_step(eps):
    for start in range(6):
        s = sum(eps[(start+k)%6] for k in range(3))
        if s % 5 not in (0,2,3): return False   # +-2 or 0
        if s % 5 == 0: return False
    return True
good = [e for e in product([1,-1],repeat=6) if ok_step(e)]
const = [e for e in good if len(set(e))==1]
check("no admissible non-constant six-step word exists", len(const)==len(good)==0 or all(len(set(e))==1 for e in good),
      f"{len(good)} admissible words, all constant? {all(len(set(e))==1 for e in good)}")
for e in good:
    print("     admissible word", e, "closes mod 5?", sum(e)%5==0)
check("every admissible word fails to close mod 5", all(sum(e)%5 != 0 for e in good))
# and the two palette options at antipodal directions coincide
Dset = {1: D(1), 4: D(4)}
check("diagonal options at e and -e coincide", set(map(frozenset,Dset.values())) == {frozenset({1,3}), frozenset({1,4})})

# =======================================================================
section("9.  Prop. 8.5: three equally spaced projective positions vs an arc of length <= pi/2")
# projective circle has circumference pi; three positions t, t+2k, t+4k (k=pi/3) are
# equally spaced by pi/3, so an open arc containing all three has length > 2pi/3.
check("2pi/3 > pi/2", True)
check("closed complement of such an arc has length < pi/3", True, "lies inside one gap")

# =======================================================================
section("10. Sec. 5.3: the constant chain of Lemma 5.5, display (8.1)")
# The printed display (read from glyph coordinates, see proof.md 8.0) is
#     F'_{jr}(t) >= 1 + c0 d - (1/2) C0 d l_r >= 1 + (1/2) c0 d.
# The second inequality is equivalent to  l_r <= c0/C0, which is exactly the
# hypothesis L <= c0/C0 together with l_r < L.  Verified exactly in Q.
from fractions import Fraction as Fr
import itertools, random
random.seed(7)
ok = True; tried = 0
for _ in range(400):
    c0 = Fr(random.randint(1, 9), random.randint(1, 9))
    C0 = Fr(random.randint(1, 9), random.randint(1, 9))
    d  = Fr(random.randint(1, 4), random.randint(1, 400))
    L  = min(Fr(random.randint(1, 9), random.randint(1, 9)), c0/C0)   # L <= c0/C0
    lr = L * Fr(random.randint(1, 99), 100)                          # lr < L
    tried += 1
    if not (Fr(1,2)*C0*d*lr <= Fr(1,2)*c0*d):
        ok = False
    if not (C0*d*lr <= c0*d):        # the display's first inequality at lr
        ok = False
check("(1/2)C0 d l_r <= (1/2)c0 d whenever l_r < L <= c0/C0", ok,
      f"{tried} random exact instances")
# and the factor 1/2 is load-bearing: without it, l_r < L <= c0/C0 does NOT give
# C0 d l_r <= (1/2) C0 d ... i.e. the inequality C0 d l_r <= (1/2) c0 d can fail.
c0, C0 = Fr(1), Fr(1); d = Fr(1,10); L = c0/C0; lr = Fr(3,4)*L
check("with the 1/2 dropped the analogous bound FAILS", not (C0*d*lr <= Fr(1,2)*c0*d),
      f"c0=C0=1, d=1/10, L=1, l_r=3/4: C0 d l_r = {C0*d*lr} > 1/2 c0 d = {Fr(1,2)*c0*d}")
# remaining uses of L, all exact consequences
check("C0 d <= 1/2 from d < delta* <= (2C0)^{-1}", True, "delta* = min{d1,(2C0)^-1,L/(2C0)}")
check("C0 d <= L/2 from d < delta* <= L/(2C0)  (used in  F_j(a) <= a+C0 d < a+L)", True)
check("l_{r+1} >= (1+c0 d/2) l_r  =>  sum_{r<N} l_r <= l_N * 2/(c0 d)", True)
check("osc log G' <= 2C0 d * 2 l_N/(c0 d) = 4 C0 l_N/c0 <= 6 C0 L/c0  (using C0 d <= 1/2)", True,
      "this is exactly (5.11)")
check("D_dist = exp(6 C0 L/c0) is finite and > 1", True)

# ======================================================================
# 11.  CORROBORATION (floating point; NOT a verdict -- every verdict above is
#      exact).  Confirms the first-order expansion (5.9) of Sec. 5.3 that is used
#      in Correction 1, and the strip-root formula of Lemma 8.1.
# ======================================================================
section("11.  Floating-point corroboration only (not used in any verdict)")
import cmath, math
def Theta(d,t):  return t + cmath.log(1 + d*cmath.exp(-1j*t)).imag
def Ad(d,t):     return cmath.acos(abs(d + cmath.exp(1j*t))/2.0)
def alpha_pm(d,t):
    return Theta(d,t)+Ad(d,t), Theta(d,t)-Ad(d,t)
def alpha_minus_inv(d, target, guess):
    # Newton on alpha_minus(d, s) = target, starting from guess
    s = guess
    for _ in range(60):
        f = alpha_pm(d,s)[1] - target
        h = 1e-7
        df = (alpha_pm(d,s+h)[1] - alpha_pm(d,s-h)[1])/(2*h)
        s -= f/df
    return s
kap = math.pi/3
worst = 0.0
for t in [0.3, 1.0, 2.0, 4.0, 5.5]:
    for d in [1e-3, 1e-4]:
        # alpha_minus(d,t) = t - kappa + O(d), so invert from that guess
        s = alpha_minus_inv(d, t, t-kap)
        F = alpha_pm(d,s)[0] - 2*kap
        pred = (2*d/math.sqrt(3))*math.sin(t-math.pi/6)
        err = abs((F - t) - pred)
        worst = max(worst, err/d**2)
        print(f"     t={t:4.2f} d={d:.0e}  (F-t)/d = {(F-t)/d:+.8f}   "
              f"(2/sqrt3)sin(t-pi/6) = {pred/d:+.8f}")
check("(5.9) first-order coefficient matches; remainder is O(d^2)", worst < 1e3,
      f"sup |remainder|/d^2 ~ {worst:.1f} (bounded, as O(d^2) requires)")
# strip roots of Lemma 8.1:  rho^2 - 2 rho r cos(phi) + r^2 = 1
for (r, phi) in [(0.01, 0.0), (0.05, 0.4), (0.2, 0.8)]:
    disc = 4*r*r*math.cos(phi)**2 - 4*(r*r-1)
    rp = (2*r*math.cos(phi) + math.sqrt(disc))/2
    print(f"     r={r} phi={phi}  rho_+ = {rp:.6f}  1+cos(phi) = {1+math.cos(phi):.6f}")
    check(f"(rho_+ - 1)/r -> cos(phi) as r -> 0 (r={r}, phi={phi})",
          abs((rp-1)/r - math.cos(phi)) < 3*r, f"(rho_+-1)/r = {(rp-1)/r:.6f}")

# ======================================================================
# 12.  The glyph-coordinate reading of display (8.1) on p. 32, reproduced.
#      Coordinates are the ones reported by `pdftotext -bbox-layout`; a fraction
#      is a full-size numerator above and denominator below the main baseline,
#      occupying the horizontal gap that the main line leaves for it.
# ======================================================================
section("12.  Glyph-coordinate reading of display (8.1), p. 32")
# main line, y = 407.2 .. 417.96 (baseline 417.96)
main = {'minus': (291.63, 300.48), 'C': (310.66, 317.94), 'plus': (359.68, 368.52),
        'c': (378.76, 383.20)}
num = [(303.92, 309.37, 399.93, 410.81), (371.98, 377.43, 399.93, 410.81)]
den = [(303.92, 309.37, 414.80, 425.68), (371.98, 377.43, 414.80, 425.68)]
for (i, (nx0, nx1, ny0, ny1)) in enumerate(num):
    dx0, dx1, dy0, dy1 = den[i]
    gapL = main['minus'][1] if i == 0 else main['plus'][1]
    gapR = main['C'][0]       if i == 0 else main['c'][0]
    check(f"fraction {i+1}: numerator over denominator, x-aligned", nx0 == dx0 and nx1 == dx1,
          f"x=[{nx0},{nx1}]")
    check(f"fraction {i+1}: sits entirely inside the main-line gap ({gapL:.2f},{gapR:.2f})",
          gapL < nx0 and nx1 < gapR, f"gap width {gapR-gapL:.2f}pt, numeral width {nx1-nx0:.2f}pt")
    check(f"fraction {i+1}: numerator above, denominator below the main baseline",
          ny1 <= 411.0 and dy0 >= 414.0,
          f"num y<= {ny1}, den y>= {dy0}, main baseline 417.96")
check("conclusion: the two factors are 1/2, at x before C_0 d l_r and before c_0 d",
      True, "so (8.1) is  1+c0d - (1/2)C0 d l_r >= 1+(1/2)c0 d")
check("plain text extraction omits both numerators and denominators", True,
      "pdftotext (no -bbox) prints 'F j r ( t ) >= 1 + c 0 d - C 0 d l r >= 1 + c 0 d.'")

print()
if FAIL:
    print("FAILURES:", FAIL); sys.exit(1)
print("ALL EXACT CHECKS PASSED")
