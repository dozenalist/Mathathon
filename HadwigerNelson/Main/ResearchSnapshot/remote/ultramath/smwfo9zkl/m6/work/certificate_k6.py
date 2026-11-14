#!/usr/bin/env python3
"""
Exact certificate for the k = 6, ell = 6 strip-layer model.

All data is rational.  Unit vectors at multiples of pi/3 are stored as a pair
(cx, sy) meaning the actual vector (cx, sy*sqrt(3)/2); the dot product of two
such vectors is cx1*cx2 + (3/4)*sy1*sy2, rational, so every sign decision below
is exact.

Centre x = (0,0).  Test direction e = (1,0).  Limiting directions of the six
exclusion continua of Proposition 7.1:
     v_0 = v_1 = v_2 = e^{i pi/3},      v_3 = v_4 = v_5 = e^{i 4 pi/3}.
Palettes at the six R-orbit directions (R = rotation by pi/3):
     P(R^j e) = {1,4} for j even,  {2,5} for j odd.

The script recomputes the sign matrix, the strip sets O_j, I_j, and checks every
constraint of the strip model (S0-S4), printing the certificate.  Every claim
here is an exact equality or inequality between rationals.
"""
from fractions import Fraction as F

# ---- exact unit vectors at multiples of pi/3 : (cx, sy) means (cx, sy*sqrt3/2)
COS = [F(1), F(1, 2), F(-1, 2), F(-1), F(-1, 2), F(1, 2)]
SIN = [F(0), F(1), F(1), F(0), F(-1), F(-1)]

def dot(u, v):
    return u[0] * v[0] + F(3, 4) * u[1] * v[1]      # exact in Q

def sgn(q):
    return (q > 0) - (q < 0)

k, ell = 6, 6
E = [(COS[j], SIN[j]) for j in range(6)]            # R^j e, j = 0..5
V = [(F(1, 2), F(1))] * 3 + [(F(-1, 2), F(-1))] * 3  # v_0..v_5
assert len(V) == ell

# ---- sign matrix, exact
sigma = [[sgn(dot(E[j], V[i])) for j in range(6)] for i in range(ell)]
print("sign matrix sigma[i][j] (edge i at direction R^j e), +1/-1:")
for i, row in enumerate(sigma):
    print("   edge %d ->" % i, row)
assert all(s != 0 for row in sigma for s in row), "direction perpendicular to some v_i"

# ---- the + positions of each edge must be a run of three consecutive positions
for i, row in enumerate(sigma):
    plus = [j for j in range(6) if row[j] > 0]
    assert len(plus) == 3 and (plus[1] - plus[0]) % 6 == 1 and (plus[2] - plus[1]) % 6 == 1, \
        f"edge {i}: + positions {plus} are not three consecutive positions"
print("\nevery edge is positive on exactly three consecutive positions  [checked]")

# ---- strip sets
def strips(sig):
    out = []
    for j in range(6):
        pos = set(); neg = set()
        for i in range(ell):
            ends = {i, (i + 1) % ell}
            if sig[i][j] > 0:
                pos |= ends
            else:
                neg |= ends
        out.append((set(range(k)) - pos, set(range(k)) - neg))
    return out

AI = strips(sigma)
print("\n O_j / I_j (labels not endpoints of positive / negative edges):")
for j, (O, I) in enumerate(AI):
    print(f"   j={j}: O={sorted(O)} I={sorted(I)}")

# ---- the palette word
word = [[1, 4] if j % 2 == 0 else [2, 5] for j in range(6)]
print("\npalette word P(R^j e):", word)

# ---- verification
ok = True
for j, (O, I) in enumerate(AI):
    P = set(word[j])
    if not O or not I:
        print(f"  FAIL S0 at j={j}"); ok = False
    if not 1 <= len(P) <= k - 3:
        print(f"  FAIL S1 at j={j}: |P|={len(P)} > k-3={k-3}"); ok = False
    if not P & O:
        print(f"  FAIL S2/O at j={j}"); ok = False
    if not P & I:
        print(f"  FAIL S2/I at j={j}"); ok = False
for j in range(6):
    if set(word[j]) & set(word[(j + 1) % 6]):
        print(f"  FAIL S3 between j={j} and j={(j+1)%6}"); ok = False
for j in range(6):
    for a in range(ell):
        if set(word[j]) <= {a, (a + 1) % ell}:
            print(f"  FAIL S4 at j={j}: palette inside cycle edge {a}"); ok = False

print("\nS0 (strips nonempty), S1 (1<=|P|<=k-3), S2 (8.1), S3 (Cor 5.4), S4 (Lemma 6.2):",
      "ALL HOLD" if ok else "VIOLATED")
print("""
Reading of the certificate: at a cyclic centre x of a hypothetical weak
measurable 6-colouring, with a six-cycle of exclusion continua whose limiting
directions are v_i = e^{i pi/3} for i<3 and e^{i 4 pi/3} for i>=3, the palette
assignment P(R^j e) = {1,4} (j even), {2,5} (j odd) satisfies every restriction
that Section 8.1 (Lemma 8.1), Corollary 5.4 and Lemma 6.2 impose at the six
R-orbit directions.  Hence no contradiction can be extracted from those
restrictions alone, in particular not the contradiction of Proposition 8.2.
""")
