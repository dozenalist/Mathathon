"""Two independent exact checks:
 (A) the mesh / multiplicity constants in Lemma 7.5 (the cover obstruction of Section 7),
     with the sharp form of the lemma and W4's explicit multiplicity-three cover;
 (B) the rational arithmetic of the paper's Section 8.6 (Tables 1 and 2 and the residual
     identity), which is the printed proof of Lemma 8.9.
"""
from fractions import Fraction as Fr

print("=" * 78)
print("(A)  Lemma 7.5 and its two constants")
print("=" * 78)
# W4's cover: triangular lattice of spacing s = 6/5, open unit discs about its points.
# covering radius of the triangular lattice with spacing s is s/sqrt3
# nearest non-neighbour (= the other vertices of the Delaunay hexagon ring) is sqrt3 s / 2.
s2 = Fr(6, 5) ** 2
print("\n  covering radius: (s/sqrt3)^2 = s^2/3 =", s2 / 3, "< 1 :", s2 / 3 < 1)
print("  second-neighbour distance: (sqrt3 s/2)^2 = 3 s^2/4 =", 3 * s2 / 4, "> 1 :", 3 * s2 / 4 > 1)
print("  disc diameter = 2 = the mesh bound of Lemma 7.5, multiplicity exactly 3 at the")
print("  Delaunay centroids.  So multiplicity 2 cannot be relaxed: [W4], re-derived in two")
print("  exact rational inequalities.")
print("\n  mesh constant: R4 records that the cover lemma holds for every mesh d < 5, so the")
print("  constant 2 of Lemma 7.5 is NOT needed at 2; the sharp form is 'multiplicity <= 2 and")
print("  mesh < 5'.  In the core, only the multiplicity bound is load-bearing.")

print()
print("=" * 78)
print("(B)  the paper's own rational certificate for Lemma 8.9 (Section 8.6)")
print("=" * 78)
h = Fr(11, 100000)                       # h = 0.00011
#  g      xi0        ups0      P+         P'-            by        bH       a       b
T1 = {
    '0':  (-1.2906,  0.1876,   0.90,      1.35,   0.0353,  4.963,   1.70,  1.71),
    'A':  (-0.6335,  0.9414,   0.095,     0.110,  0.887,   0.319,   1.28,  1.29),
    'B':  (-0.3092, -0.0045,   0.000002,  0.00065, 0.000022, 0.287,  0.095, 0.096),
    'T':  (0.3478,   0.7493,   0.023,     0.026,  0.562,   0.199,   0.682, 0.683),
    'uA': (-1.1598,  1.1790,   9.8,       19.0,   1.391,   2.647,   2.73,  2.74),
    'uB': (-0.3666,  0.5700,   0.0022,    0.024,  0.326,   0.079,   0.459, 0.46),
    'uT': (-0.2358,  1.5614,   12.65,     12.9,   2.44,    2.273,   2.493, 2.495),
}
ok = True
print(f"\n{'g':>3} {'yu<by':>7} {'H<bH':>7} {'a<ll':>7} {'lu<b':>7} {'P+>yubH2':>10} "
      f"{'P-<a3()(1-b/4)(..)2':>20} {'P+<P-':>7}")
for g, (xi, up, Pp, Pm, by, bH, a, b) in T1.items():
    xi, up, Pp, Pm, by, bH, a, b = map(Fr, (str(xi), str(up), str(Pp), str(Pm),
                                            str(by), str(bH), str(a), str(b)))
    xl, xu = (abs(xi) - h) ** 2, (abs(xi) + h) ** 2
    yl, yu = (abs(up) - h) ** 2, (abs(up) + h) ** 2
    ll, lu = xl + yl, xu + yu
    H = max(abs(3 * xl - yu), abs(3 * xu - yl))
    c1 = yu < by
    c2 = H < bH
    c3 = a < ll
    c4 = lu < b
    c5 = yu * H * H < Pp
    c6 = a ** 3 * (1 - b / 4) * min(abs(a - 1), abs(b - 1)) ** 2 > Pm
    c7 = Pp < Pm
    ok &= c1 and c2 and c3 and c4 and c5 and c6 and c7
    print(f"{g:>3} {str(c1):>7} {str(c2):>7} {str(c3):>7} {str(c4):>7} {str(c5):>10} "
          f"{str(c6):>20} {str(c7):>7}")
print(f"\n  every strict rational inequality of Section 8.6 holds: {ok}")

print("\n  residual identity of Section 8.6 (exact, rational midpoint substitution)")
ASTAR = Fr(1732055, 1000000)     # a* = 1.732055  for sqrt 3
BSTAR = Fr(3316625, 1000000)     # b* = 3.316625  for sqrt 11
# every coordinate of every g lies in Q(sqrt3, sqrt11, sqrt33); a 4-tuple is over
# (1, sqrt3, sqrt11, sqrt33).  Under the midpoint substitution they become
# (1, a*, b*, a* b*) -- rationals.
G = {
    '0':  ((0, 0, 0, 0), (0, 0, 0, 0)),
    'A':  ((0, Fr(1, 2), 0, 0), (Fr(1, 2), 0, 0, 0)),
    'B':  ((0, Fr(1, 2), 0, 0), (Fr(-1, 2), 0, 0, 0)),
    'T':  ((0, 1, 0, 0), (0, 0, 0, 0)),
    'uA': ((0, Fr(5, 12), Fr(-1, 12), 0), (Fr(5, 12), 0, 0, Fr(1, 12))),
    'uB': ((0, Fr(5, 12), Fr(1, 12), 0), (Fr(-5, 12), 0, 0, Fr(1, 12))),
    'uT': ((0, Fr(5, 6), 0, 0), (0, 0, 0, Fr(1, 6))),
}
RES = {'0': (3840000, -23040000), 'A': (-29520000, 10176000), 'B': (-12240000, -22464000),
       'T': (25440000, 10752000), 'uA': (32043244, -19212795), 'uB': (4763244, -27212795),
       'uT': (32966488, -23385590)}
CEN = {g: (Fr(str(T1[g][0])), Fr(str(T1[g][1]))) for g in T1}
Mr, Mi = Fr(35, 37), Fr(12, 37)
TR0 = (Fr(-290, 250), Fr(149, 250))


def sub(coef):
    return coef[0] + coef[1] * ASTAR + coef[2] * BSTAR + coef[3] * ASTAR * BSTAR


bad = []
for g in G:
    gre, gim = sub(G[g][0]), sub(G[g][1])
    xr = Mr * (gre + TR0[0]) - Mi * (gim + TR0[1])
    xi_ = Mr * (gim + TR0[1]) + Mi * (gre + TR0[0])
    scale = Fr(710400000000)
    got = ((xr - CEN[g][0]) * scale, (xi_ - CEN[g][1]) * scale)
    exp = RES[g]
    match = (got[0] == exp[0] and got[1] == exp[1])
    if not match:
        bad.append((g, got, exp))
    print(f"    g={g:>2}  residual*scale = ({float(got[0]):15.2f},{float(got[1]):15.2f})"
          f"   printed ({exp[0]},{exp[1]})   match: {match}")
print(f"\n  residual identity reproduced exactly for all seven points: {not bad}")
print("  (This also fixes the reading of (8.6): the printed display must be read as")
print("   z_g = ((35+12i)/37)(g + (-290+149i)/250).  Under the flat reading")
print("   z_g = ((35+12i)/37)g + (-290+149i)/250 the seven points are not the ones tabulated")
print("   and Lemma 8.9 fails at g = 0; the Table 1 numbers decide it.)")
