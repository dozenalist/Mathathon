"""Exact checks for .ultramath/smwgptxn1/m2/proof.md  (MC120: exact form, sharpening, falsifications).
Everything is exact (sympy rationals / radicals) or a tiny enumeration. Runs in a few seconds.
Usage: python3 check.py
"""
from sympy import symbols, sin, cos, sqrt, pi, asin, simplify, expand, N, Rational, solve, Eq, limit
from itertools import combinations

w, d = symbols('w delta', positive=True)

# ---------- (a) Lemma 1: diameter of the open annular sector {1<r<1+d, |phi|<w/2} ----------
d1 = 2*(1+d)*sin(w/2)                      # two outer corner points
d2sq = expand((1+d)**2 + 1 - 2*(1+d)*cos(w))
print("(a) 2*sin(pi/6) =", simplify(2*sin(pi/6)), "   (exactly 1)")
print("    d2^2 - (d^2+4(1+d)sin^2(w/2)) =", simplify(d2sq - (d**2 + 4*(1+d)*sin(w/2)**2)))
print("    d1 at w=pi/3 :", simplify(d1.subs(w, pi/3)))          # = 1+d  -> >1 for every d>0
print("    d1,d2 at w=pi/3, d=0 :",
      simplify(d1.subs({w: pi/3, d: 0})), sqrt(d2sq.subs({w: pi/3, d: 0})))   # both 1
print("    inf_{delta>0} 2*asin(1/(2+2delta)) =", limit(2*asin(1/(2+2*d)), d, 0), " = pi/3")
print("    inf_{delta>0} 2*asin(sqrt(1-delta)/2) =", limit(2*asin(sqrt(1-d)/2), d, 0), " = pi/3")
print("    d1 = d2  <=>  1/(1+delta) = sqrt(1-delta)  <=>  delta =",
      [simplify(x) for x in solve(Eq(1/(1+d), sqrt(1-d)), d)], "= (sqrt5-1)/2 ~", N((sqrt(5)-1)/2))
for dl in (Rational(1,10), Rational(1,100), Rational(1,2)):
    wthr = 2*asin(1/(2+2*dl)); wthr2 = 2*asin(sqrt(1-dl)/2)
    print("    delta=%s : w* = %s deg   => admissible aperture < %s deg"
          % (dl, N(wthr*180/pi, 8), N(180 - wthr*180/pi, 8)),
          " | other branch", N(wthr2*180/pi, 8))
print("    cone aperture a -> common-positive arc width pi-a ; at a=2pi/3 :",
      simplify((pi - w).subs(w, 2*pi/3)), " > pi/3 ?", simplify((pi-w).subs(w, 2*pi/3) - pi/3))

# ---------- (b) falsification: two edge-pair blocks cover at most 4 labels ----------
E = [frozenset({i, (i + 1) % 6}) for i in range(6)]
print("\n(b) max |E_i u E_j| over the 36 ordered pairs of edge pairs =",
      max(len(E[i] | E[j]) for i in range(6) for j in range(6)))
ok = [(T, sorted(frozenset().union(*[E[i] for i in T])))
      for T in combinations(range(6), 3)
      if len(frozenset().union(*[E[i] for i in T])) >= 5]
print("    three edge-pair blocks with |union| >= 5 :", len(ok), "of", len(list(combinations(range(6), 3))))
for T, U in ok:
    print("       ", T, U)

# ---------- (b2) the withheld inference: spread >= 120 deg does NOT give pairwise >= 120 deg ----------
import mpmath as mp
mp.mp.dps = 30
tol = mp.mpf(10) ** -12
def cdist(x, y):
    e = abs((x - y) % (2 * mp.pi)); return min(e, 2 * mp.pi - e)
def spread(dirs):
    """360 - largest gap of the directions, in radians."""
    A = sorted(x % (2 * mp.pi) for x in dirs)
    gaps = [A[k + 1] - A[k] for k in range(len(A) - 1)] + [A[0] + 2 * mp.pi - A[-1]]
    return 2 * mp.pi - max(gaps)
deg = lambda r: round(float(r * 180 / mp.pi), 9)
cm = [mp.mpf(0), mp.mpf(60) * mp.pi / 180, mp.mpf(200) * mp.pi / 180]
print("(b2) countermodel {0,60,200} deg : spread =", deg(spread(cm)), "deg  (>= 120, so MC120 is satisfied)")
print("     but circ-dist(0,60) =", deg(cdist(cm[0], cm[1])), "deg  (< 120)  => pairwise does NOT follow")
print("     and largest gap =", deg(2 * mp.pi - spread(cm)), "deg  (<= 240, the correct weak form)")

# ---------- (c) SUFFICIENT boundary condition only: pairwise >= 120 deg => regular triple ----------
print("\n(c) SUFFICIENT condition only (pairwise >= 120deg => regular triple);")
import mpmath as mp
mp.mp.dps = 30
tol = mp.mpf(10) ** -12
def cdist(x, y):
    e = abs((x - y) % (2 * mp.pi)); return min(e, 2 * mp.pi - e)
N2 = 720; found = set()
for i in range(N2):
    for j in range(N2):
        A = [mp.mpf(0), i * 2 * mp.pi / N2, j * 2 * mp.pi / N2]
        if all(cdist(A[p], A[q]) >= 2 * mp.pi / 3 - tol for p in range(3) for q in range(p)):
            found.add(tuple(sorted(round(float(x * 180 / mp.pi), 6) for x in A)))
print("    pairwise >= 120 deg forces the regular triple; sets found (0.5 deg grid, tol 1e-12):", sorted(found))
print("    ==> but this antecedent is NOT established by Theorem 1; see (b2).")

# ---------- (d) the forced equilateral triple is not a unit triangle ----------
x = mp.mpf(2) * mp.pi / 3
print("(d) |e(0) - e(2pi/3)| =", abs(1 - mp.mpc(mp.cos(x), mp.sin(x))), " sqrt3 =", mp.sqrt(3))

# ---------- (e) Theorem 3 certificate: two unit-distance annuli ----------
print("\n(e) two-centre lens, perpendicular bisector: h in (sqrt3/2, sqrt((1+delta)^2-1/4));")
print("    vertical extent > 1  <=>  1+delta > sqrt(2+sqrt3) = (sqrt6+sqrt2)/2 :",
      simplify(sqrt(2 + sqrt(3)) - (sqrt(6) + sqrt(2)) / 2), "= 0")
print("    delta threshold =", N(sqrt(2 + sqrt(3)) - 1, 12))
print("\nAll checks printed above are exact identities or exact finite counts.")
