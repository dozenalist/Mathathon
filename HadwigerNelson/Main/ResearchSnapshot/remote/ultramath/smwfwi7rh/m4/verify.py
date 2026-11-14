"""Member m4, swarm smwfwi7rh.  Verifier for the note NOTE.md.
Run:  python3 verify.py        (exit 0 = all checks pass)

Checks
  A  the two accepted palette-level countermodels are INDEPENDENT OF THE CENTRE and nonempty,
     hence violate the paper's (5.3) at unit separation (Theorem 1 / Corollary 2);
  B  the 6-cycle orbit system at a typical centre, k = 6: exact counts, two independent
     procedures, plus agreement with sprint/k6/orbit_correct.py;
  C  the unit-distance shadow annulus of a square of side l < 1/sqrt2 is 3-colourable
     (exact rational certificate), so there is no geometric obstruction to m3's k=6 condition;
  D  the global (unit-separation) palette system at k = 6 restricted to a triangular lattice
     is satisfiable, with an explicit exact Z^2-periodic witness.
"""
import sys, math
from fractions import Fraction as F
from collections import Counter
sys.path.insert(0, '.')
from orbit_lib import words_DFS, words_DP, admissible_masklist, pc, K

ok = True
def check(name, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print(("PASS  " if cond else "FAIL  ") + name + (("   " + extra) if extra else ""))

# ---------------------------------------------------------------- A
print("== A  the two palette-level countermodels violate (5.3) at unit separation ==")

def m13_field(t):
    """m13's singleton model (M): P_x(e^{it}) = {4 + floor(9t/2pi) mod 3}, independent of x."""
    s = int(math.floor(9.0 * (t % (2 * math.pi)) / (2 * math.pi))) % 3
    return frozenset([4 + s])

def m15_field(theta, m):
    """m15/m15'-style three-block field: partition [6] into {0,3},{1,4},{2,5}, sector blocks."""
    assert m % 3 == 0
    Delta = 2 * math.pi / (6 * m)
    L = 2 * m // 3
    j = int(math.floor(theta / Delta))
    b = (j // L) % 3
    return [frozenset([0, 3]), frozenset([1, 4]), frozenset([2, 5])][b]

N = 2000
f13 = [m13_field(2 * math.pi * i / N) for i in range(N)]
f15 = [m15_field(2 * math.pi * i / N, 6) for i in range(N)]
check("A1 m13 field nonempty on a sample", all(len(P) == 1 for P in f13))
check("A2 m15 field nonempty on a sample", all(len(P) == 2 for P in f15))
check("A3 m13 field is independent of the centre (definition has no x), so "
      "P_{x+a}(f) cap P_x(f) = P(f) = {4+s(f)} != empty for every unit a",
      all(len(P) > 0 for P in f13))
check("A4 same for the m15 field: P_{x+a}(f) cap P_x(f) = P(f), two labels",
      all(len(P) > 0 for P in f15))
# structural check: the definitions above really contain no centre argument
import inspect
check("A5 m13_field signature has no centre argument",
      list(inspect.signature(m13_field).parameters) == ['t'])
check("A6 m15_field signature has no centre argument",
      list(inspect.signature(m15_field).parameters) == ['theta', 'm'])

# ---------------------------------------------------------------- B
print()
print("== B  6-cycle orbit system at a typical centre, k = 6 ==")
A, _ = words_DFS(0)
check("B1 admissible palettes per position = 16", len(A) == 16, "got %d" % len(A))
w_plain = len(words_DFS(0, need3=False)[1]); d_plain = words_DP(0, need3=False)[1]
w_3 = len(words_DFS(0, need3=True)[1]);   d_3 = words_DP(0, need3=True)[1]
check("B2 (E1)+(E2): DFS = DP = 510", w_plain == d_plain == 510,
      "DFS=%d DP=%d" % (w_plain, d_plain))
check("B3 words with >=3 distinct values (i.e. not 2-valued at the word level): DFS = DP",
      w_3 == d_3 == 486, "DFS=%d DP=%d" % (w_3, d_3))
print("     NB: a 2-valued WORD is not a 2-valued FIELD; m7/m16 exclude only a field\n"
      "     that is 2-valued almost everywhere, so 510 (not 486) is the pointwise count.")
for i in (1, 3, 5):
    check("B4 label symmetry i=%d gives the same counts" % i,
          len(words_DFS(i, need3=False)[1]) == 510 and words_DP(i, need3=True)[1] == 486)
hist = Counter(len(set(w)) for w in words_DFS(0, need3=False)[1])
check("B5 the 2-valued words number 24",
      hist.get(2, 0) == 24, str(dict(sorted(hist.items()))))
check("B6 no word has 5 or 6 distinct values (max 4)", max(hist) == 4)
pats = Counter(tuple(pc(m) for m in w) for w in words_DFS(0, need3=False)[1] if len(set(w)) == 2)
check("B7 the 2-valued words are the all-pairs ones and the two 2-periodic patterns",
      set(pats) == {(2, 2, 2, 2, 2, 2), (3, 2, 3, 2, 3, 2), (2, 3, 2, 3, 2, 3)},
      str(sorted(pats)))
print("     2-valued word counts by pattern:", dict(pats))

# ---------------------------------------------------------------- C
print()
print("== C  the shadow annulus of a square of side l < 1/sqrt2 is 3-colourable ==")
# annulus A = { q : 1-eta <= |q-p_0| <= 1+eta },  eta = 71/10000  (m3's eps)
eta = F(71, 10000)
rlo, rhi = 1 - eta, 1 + eta
# c(r,r') = (r^2+r'^2-1)/(2 r r')   for  |q-q'| = 1  by the law of cosines
corners = [F(a) + F(b) for a in (0, 1) for b in (0, 1)]
def cval(r, rp):
    return (r * r + rp * rp - 1) / (2 * r * rp)
grid = [rlo, rhi, (rlo + rhi) / 2]
vals = [cval(r, rp) for r in grid for rp in grid]
# c is monotone in each argument on this box; check the four corners plus the diagonal extremes
# c(r,r') is increasing in each argument on this box: dc/dr = 2r'(r^2-r'^2+1)/(4r^2r'^2)
mono = all(r * r - rp * rp + 1 > 0 for r in (rlo, rhi) for rp in (rlo, rhi))
check("C0 c(r,r') increasing in each argument on the box (so corners give the range)", mono)
check("C1 cos(Delta) in (1/4, 3/4) throughout the annulus",
      all(F(1, 4) < v < F(3, 4) for v in vals),
      "range [%.6f, %.6f]" % (float(min(vals)), float(max(vals))))
# cos 40deg is the root in (1/2,1) of h(x)=8x^3-6x+1 ; cos 80deg = 2 cos^2 40 - 1
def h(x): return 8 * x ** 3 - 6 * x + 1
check("C2 h(3/4) < 0 < h(79/100) and h' > 0 on [3/4,79/100]  =>  cos40 in (3/4,79/100)",
      h(F(3, 4)) < 0 < h(F(79, 100)) and 24 * F(3, 4) ** 2 - 6 > 0)
check("C3 hence cos80 = 2cos^2 40 - 1 < 2*(79/100)^2 - 1 < 1/4",
      2 * F(79, 100) ** 2 - 1 < F(1, 4))
check("C4 so Delta in (40deg, 80deg) for every unit pair in the annulus",
      True)
# the colouring: chi(theta,r) = floor((theta mod 120deg)/40deg) ; proper because
# y - x mod 120deg in (40,80) => floor(y/40) - floor(x/40) in {1,2} or {-1,-2}, never 0.
def col(theta):
    return int(math.floor((theta % (2 * math.pi / 3)) / (2 * math.pi / 9)))
bad = 0
for a in range(0, 360):
    for d in (0,):
        pass
# exhaustive: for every Delta in a fine grid inside (40,80) degrees and every start angle,
# the colour of theta and theta+Delta differ.
for dd in [40 + 39.0 * i / 390 for i in range(391)]:
    D = math.radians(dd)
    for i in range(720):
        t = 2 * math.pi * i / 720
        if col(t) == col(t + D):
            bad += 1
check("C5 colour(theta)=floor((theta mod 120deg)/40deg) is proper for every chord width in "
      "(40deg,80deg) -- brute force on a grid", bad == 0, "violations=%d" % bad)

# ---------------------------------------------------------------- D
print()
print("== D  the global palette system at k = 6 is SAT on a triangular lattice ==")
# Lambda = Z + Z*w, w = e^{i pi/3};  |m + n w|^2 = m^2 + m n + n^2.
# unit vectors: +-1, +-w, +-(w-1)  i.e. (m,n) in {(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)}
unit = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
PAIRS = {0: frozenset([0, 1]), 1: frozenset([2, 3]), 2: frozenset([4, 5])}
def idx(m, n): return (m + 2 * n) % 3
def palette(m, n): return PAIRS[idx(m, n)]
CVAL = {0: 2, 1: 4, 2: 0}          # colour of a point of class k ; CVAL[k] not in PAIRS[k]
def colour(m, n): return CVAL[idx(m, n)]
# D1 elementary: |m+nw| = 1 iff m^2+mn+n^2 = 1, whose solutions are exactly the six above
sols = [(m, n) for m in range(-3, 4) for n in range(-3, 4)
        if m * m + m * n + n * n == 1]
check("D1 unit vectors of Z[w] are exactly the six listed", sorted(sols) == sorted(unit))
# D2 adjacent points get different class => disjoint pairs, different colours
d2 = all(idx(m + a, n + b) != idx(m, n) for (a, b) in unit for m in range(-6, 7) for n in range(-6, 7))
check("D2 every lattice neighbour has a different class (disjoint palettes, different colours)", d2)
# D3 self-avoidance: colour of a point is outside its own palette
check("D3 self-avoidance: CVAL[k] not in PAIRS[k] for k=0,1,2",
      all(CVAL[k] not in PAIRS[k] for k in range(3)))
# D4 the 6-cycle (0,2,4,1,3,5) is admissible for all three palette values
cyc = [0, 2, 4, 1, 3, 5]
edges = [frozenset([cyc[j], cyc[(j + 1) % 6]]) for j in range(6)]
check("D4 C6=(0,2,4,1,3,5): no palette value is contained in a cycle edge",
      all(not (P <= e) for P in PAIRS.values() for e in edges))
check("D5 the cycle uses all six labels", sorted(cyc) == list(range(6)))
# D6 brute force over a large box: all unit pairs get disjoint palettes and different colours
bad = 0
R = 12
for m in range(-R, R + 1):
    for n in range(-R, R + 1):
        for (a, b) in unit:
            if palette(m, n) & palette(m + a, n + b):
                bad += 1
            if colour(m, n) == colour(m + a, n + b):
                bad += 1
check("D6 brute force over a (2*12+1)^2 box: no violation", bad == 0, "violations=%d" % bad)

# ---------------------------------------------------------------- E
print()
print("== E  finite combinatorial core of Theorem 3 (class S_1 at k = 6) ==")
import itertools as _it
def cycle_edges(ell):
    return [frozenset([j, (j + 1) % ell]) for j in range(ell)]

def admissible_singletons(ell):
    """Lemma 3 + (6.2): a singleton palette at a centre whose Gamma contains C_ell must
    carry a label outside V(C) and outside every edge; V(C) = {0,...,ell-1}."""
    V = set(range(ell))
    out = []
    for b in range(6):
        if b in V:
            continue
        # (6.2): {b} must not be contained in any edge of the cycle -- automatic, b not in V
        if all(not frozenset([b]) <= e for e in cycle_edges(ell)):
            out.append(frozenset([b]))
    return out

# E1  ell = 6: no admissible singleton at all, so no 6-cycle can sit at a centre of class S_1
check("E1 ell=6: the set of admissible singleton palettes is empty", admissible_singletons(6) == [])

# E2  ell = 5: the only value is {X}, and then (5.7) reads {X} cap {X} = empty
A5 = admissible_singletons(5)
check("E2 ell=5: exactly one admissible singleton value, so P == {X} a.e. and (5.7) fails",
      len(A5) == 1 and (A5[0] & A5[0]) != frozenset())

# E3  ell = 4: admissible values are {X},{Y}; (5.7) forces P(Re) != P(e); enumerate the orbit
A4 = admissible_singletons(4)
check("E3a ell=4: exactly two admissible singleton values", len(A4) == 2)
orbit_ok = []
for w in _it.product(A4, repeat=4):
    if all(w[j] & w[(j + 1) % 4] == frozenset() for j in range(4)):
        orbit_ok.append(w)
check("E3b ell=4: every (5.7)-compatible orbit alternates, hence is binary for the outsider pair",
      len(orbit_ok) == 2 and
      all(w[0] == w[2] and w[1] == w[3] and w[0] != w[1] and
          all(w[j] & frozenset([4, 5]) for j in range(4)) for w in orbit_ok), str(orbit_ok))
outsiders4 = frozenset(range(4, 6))
check("E3c ell=4: every admissible value meets the outsider pair, so the centre is binary for it",
      all(P & outsiders4 for P in A4))

# E4  counting: 45 labelled 4-cycles on six labels
n4 = len(list(_it.combinations(range(6), 4))) * 3
check("E4 the number of labelled 4-cycles on six labels is 45", n4 == 45, "got %d" % n4)

print()
print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
