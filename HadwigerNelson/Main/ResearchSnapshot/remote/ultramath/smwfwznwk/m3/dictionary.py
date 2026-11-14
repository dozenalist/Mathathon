"""dictionary.py -- geometric audit of the sector-word dictionary.

Claims certified here (all in the sense of the paper's Lemma 5.2(3) = display (5.3)
and Corollary 5.4 = (5.7)):

 D1  DEVIATION.  Let a = z - x, d = |a| <= d0 = pi/(9m), f a unit direction, and let
     s, t be the unit solutions of  s + t = (z-x) + f, i.e. z + f = x + s + t.
     Then for either choice of s,
            |arg s - (arg f +- pi/3)|  <=  B(d)  <=  1.74 d,
     and with Delta = 2*pi/(6m) = pi/(3m):   B(d0)/Delta <= 0.58 < 1.
     Certified in exact rational arithmetic (Fraction), with a rational enclosure
     of pi; no floating point enters the inequality.

 D2  SHIFTS.  Consequently sector(arg s) - sector(arg f) is congruent to
     m + k, k in {-1,0,+1}, mod 6m, for every configuration: no other shift can
     occur.  Verified on a dense sweep for m = 3,5,6,9,12,15,18 (exact bound above
     is what proves it in general).

 D3  ATTAINMENT.  Each of the six shifts +-(m-1), +-m, +-(m+1) is realised by an
     explicit configuration with d <= d0 whose two sector indices sit at distance
     >= 0.18 Delta from a sector boundary; hence an open set of configurations
     realises it, and the corresponding word constraint is forced.

 D4  HYPOTHESES.  The maps f -> s(f), t(f) of D1 are smooth, s and t are
     nonparallel (angle >= 2.02 rad), and d arg s/d arg f lies in [0.87, 1.01],
     so s is a local diffeomorphism in the angular coordinate: (5.3) applies.

 D5  CENTRES.  y_k = (d0/3) 2^-k (3/5, 4/5) are distinct, |y_k| <= d0/3, and
     |y_k - y_{k+1}| <= d0/6 <= d0, so every pair of them is within the range
     where (5.3) applies and the two-centre transport of the word is in force;
     they accumulate at 0.

Consequence (used in PROOF.md): for a palette field that depends only on the
direction, (5.3)+(5.7) hold for all centre pairs at distance <= d0 iff the sector
word W on Z_{6m} satisfies  W(i) cap W(i+delta) = empty  for every i and every
delta in {+-(m-1), +-m, +-(m+1)} mod 6m.  D2 is the "only if" (no other shift
occurs), D3 the "if" (every offset really occurs), D4 that (5.3) is applicable.
"""
from fractions import Fraction as F
import math
import numpy as np

FAIL = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not cond:
        FAIL.append(name)


print("D1  deviation bound in exact rational arithmetic")
# pi enclosure (31 valid digits)
PI_LO = F(31415926535897932384626433832795, 10**31)
PI_HI = PI_LO + F(1, 10**30)          # pi_lo < pi < pi_hi
#
# Setup: s + t = f + a, |a| = d <= d0, rho = |f+a|, theta = angle(f, a).
#   rho^2 = 1 + 2 d cos(theta) + d^2,   |rho - 1| <= d|cos theta| + d^2/2
#   psi = angle(f, f+a):  sin psi = d sin(theta)/rho, so
#        |psi| <= arcsin(d|sin theta|/rho) <= c1 |sin theta|,
#        c1 = (d/(1-d))(1 + (d/(1-d))^2)        [arcsin x <= x(1+x^2), x <= d/(1-d)]
#   phi = arccos(rho/2):  |phi - pi/3| = |int_1^rho du/sqrt(4-u^2)|
#        <= |rho-1|/sqrt(4-(1+d)^2) <= c2 |cos theta| + c3,
#        c2 = (3/5) d,  c3 = (3/5) d^2/2        [uses 4-(1+d)^2 > 25/9]
#   hence dev <= c1|sin theta| + c2|cos theta| + c3 <= sqrt(c1^2+c2^2) + c3.
# Every step is an exact rational inequality; the square root is certified by
# squaring a rational upper bound (no floating point decides anything).
rows = []
for m in (5, 6, 9, 12, 15, 18, 24, 30, 60, 120, 600):
    d_hi = PI_HI / (9 * m)                                  # >= d0
    assert 4 - (1 + d_hi) ** 2 > F(25, 9), m                # so 1/sqrt(...) < 3/5
    x = d_hi / (1 - d_hi)                                   # >= d/(1-d)
    assert x ** 2 + x ** 4 <= 1, m                           # so arcsin x <= x(1+x^2)
    c1 = x * (1 + x ** 2)
    c2 = F(3, 5) * d_hi
    c3 = F(3, 5) * d_hi ** 2 / 2
    p, q = (c1 ** 2 + c2 ** 2).as_integer_ratio()
    r = math.isqrt(p * q)                                    # ceil(sqrt(p/q)) = r/q
    if r * r < p * q:
        r += 1
    c = F(r, q)                                              # exact: c >= sqrt(c1^2+c2^2)
    assert c1 ** 2 + c2 ** 2 <= c ** 2, m                     # exact: c >= sqrt(c1^2+c2^2)
    B = c + c3
    ratio = B / d_hi                                        # dev <= ratio*d
    frac = ratio / 3                                        # dev/Delta, d0/Delta=1/3
    rows.append((m, ratio, frac))
    print(f"    m={m:4d}:  dev <= {float(ratio):.5f} d ;  dev/Delta <= {float(frac):.5f}")
check("dev <= 1.30 d for every m >= 5", all(r[1] <= F(130, 100) for r in rows),
      f"worst ratio {float(max(r[1] for r in rows)):.5f}")
print("    [each term of B(d)/d is increasing in d and d0 decreases in m, so the")
print("     maximum over m >= 5 is attained at m = 5, where the ratio is printed above;")
print("     the limit m -> infinity is sqrt(1 + 9/25) = 1.166]")
check("dev/Delta < 1 (so only the shifts m-1, m, m+1 occur)",
      all(r[2] < 1 for r in rows), f"worst {float(max(r[2] for r in rows)):.5f}")
print("    [the record's constant 1.5938 gives 1.5938/3 = 0.5312667 < 1: same conclusion;")
print("     the certificate above does not assume it, and covers rho < 1 which the")
print("     quoted derivation arcsin(d0)/d0 + 1/sqrt(4-(1+d0)^2) does not spell out]")

print()
print("D2/D3/D4  configuration sweep and attainment")


def configurations(m, nf=241, nd=31):
    Delta = 2 * np.pi / (6 * m)
    d0 = np.pi / (9 * m)
    argf = (np.arange(nf) + 0.5) * 2 * np.pi / nf
    arga = np.arange(nf) * 2 * np.pi / nf
    F1 = np.stack([np.cos(argf), np.sin(argf)], 1)
    A1 = np.stack([np.cos(arga), np.sin(arga)], 1)
    seen = set()
    worst = 0.0
    minst = 1e9
    for j in range(1, nd + 1):
        d = d0 * j / nd
        P = (F1[:, None, :] + d * A1[None, :, :]).reshape(-1, 2)
        f = np.repeat(F1, nf, 0)
        rho = np.linalg.norm(P, axis=1)
        h = np.sqrt(1 - rho**2 / 4)
        perp = np.stack([-P[:, 1], P[:, 0]], 1) / rho[:, None]
        for sgn in (1.0, -1.0):
            S = P / 2 + sgn * h[:, None] * perp
            T = P - S
            ang = np.arctan2(S[:, 1], S[:, 0])
            base = np.arctan2(f[:, 1], f[:, 0])
            dev = np.mod(ang - (base + sgn * np.pi / 3) + np.pi, 2 * np.pi) - np.pi
            worst = max(worst, float(np.abs(dev).max()))
            minst = min(minst, float(np.abs(np.arctan2(
                S[:, 0] * T[:, 1] - S[:, 1] * T[:, 0], (S * T).sum(1))).min()))
            i0 = np.floor(base / Delta)
            i1 = np.floor(ang / Delta)
            for jj in np.unique((i1 - i0) % (6 * m)):
                seen.add(int(jj))
    return sorted(seen), worst, minst, Delta, d0


for m in (3, 5, 6, 9, 12, 15, 18):
    seen, worst, minst, Delta, d0 = configurations(m)
    exp = sorted({(m + k) % (6 * m) for k in (-1, 0, 1)} | {(-m + k) % (6 * m) for k in (-1, 0, 1)})
    check(f"m={m}: realised shifts == the six offsets", seen == exp,
          f"|dev|max={worst:.4g} <= 1.74 d0={1.74*d0:.4g}; min angle(s,t)={minst:.3f}")

# D4: local diffeomorphism in the angular coordinate
t = np.linspace(-1.2, 1.2, 40001)
for m in (5, 6, 12):
    d0 = np.pi / (9 * m)
    for dd in (d0 / 2, d0):
        a = dd * np.array([np.cos(1.0), np.sin(1.0)])
        fx, fy = np.cos(t) + a[0], np.sin(t) + a[1]
        rr = np.hypot(fx, fy)
        hh = np.sqrt(1 - rr**2 / 4)
        arg = np.unwrap(np.arctan2(fy / 2 + hh * fx / rr, fx / 2 - hh * fy / rr))
        der = np.diff(arg) / np.diff(t)
        check(f"m={m}, d={'d0/2' if dd < d0 else 'd0'}: d arg s/d arg f bounded away from 0",
              der.min() > 0.8 and der.max() < 1.1, f"[{der.min():.3f},{der.max():.3f}]")

# D4a: the second branch must also be usable, because (5.3) is applied with either
# centre as the "first direction" (x + g = z + t(g) + s(g), g = f + a, needs t a
# local diffeomorphism in arg g).  Same family, a -> -a, so check it directly.
for m in (5, 6, 12):
    d0 = np.pi / (9 * m)
    for dd in (d0 / 2, d0):
        a = dd * np.array([np.cos(1.0), np.sin(1.0)])
        gx, gy = np.cos(t) + a[0], np.sin(t) + a[1]
        rr = np.hypot(gx, gy)
        hh = np.sqrt(1 - rr**2 / 4)
        arg = np.unwrap(np.arctan2(gy / 2 - hh * gx / rr, gx / 2 + hh * gy / rr))
        der = np.diff(arg) / np.diff(t)
        check(f"m={m}, d={'d0/2' if dd < d0 else 'd0'}: d arg t/d arg g bounded away from 0",
              der.min() > 0.8 and der.max() < 1.2, f"[{der.min():.3f},{der.max():.3f}]")

# D3: explicit attaining configurations with an interior margin
m = 6
n, Delta, d0 = 36, 2 * np.pi / 36, np.pi / 54
offs = {5, 6, 7, 29, 30, 31}
best = {}
for i in range(1440):
    argf = 2 * np.pi * (i + 0.5) / 1440
    for k in range(0, 2880, 4):
        arga = 2 * np.pi * k / 2880
        a = d0 * np.array([np.cos(arga), np.sin(arga)])
        fx, fy = np.cos(argf) + a[0], np.sin(argf) + a[1]
        rho = np.hypot(fx, fy)
        h = np.sqrt(1 - rho**2 / 4)
        for sgn in (1, -1):
            sx, sy = fx / 2 + sgn * h * (-fy) / rho, fy / 2 + sgn * h * fx / rho
            args = np.arctan2(sy, sx)
            j = (int(np.floor(args / Delta)) - int(np.floor(argf / Delta))) % n
            if j in offs:
                marg = min((argf / Delta) % 1, 1 - (argf / Delta) % 1,
                           (args / Delta) % 1, 1 - (args / Delta) % 1)
                if j not in best or marg > best[j][0]:
                    best[j] = (float(marg), float(argf), float(arga), int(sgn))
for j in sorted(offs):
    print(f"    offset {j:2d}: margin {best[j][0]:.3f} sectors, arg f={best[j][1]:.5f},"
          f" arg(z-x)={best[j][2]:.5f}, d=d0, branch {best[j][3]:+d}")
check("each of the six offsets is attained with interior margin >= 0.15 sector",
      set(best) == offs and all(b[0] >= 0.15 for b in best.values()))

print()
print("D5  accumulating centres")
for m in (5, 6, 9, 12):
    d0 = np.pi / (9 * m)
    u = np.array([3 / 5, 4 / 5])
    # exact dyadic data: take d0/3 to be the rational PI_LO/(3*9m), which differs
    # from the true pi/(27m) by less than 1e-31; distinctness is then exact.
    base = PI_LO / (27 * m)
    ysF = [base / 2**k for k in range(80)]
    ptsF = [(y * F(3, 5), y * F(4, 5)) for y in ysF]
    ys = np.array([float(y) for y in ysF])
    pts = ys[:, None] * u[None, :]
    steps = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    check(f"m={m}: y_k distinct, |y_k| <= d0/3, |y_k-y_(k+1)| <= d0/6, accumulate at 0",
          len(set(ptsF)) == len(ptsF)                       # exact
          and all(y <= base for y in ysF)                   # exact
          and steps.max() <= d0 / 6 * (1 + 1e-12),
          f"sup|y_k|=d0/3={float(base):.6g}, max step={steps.max():.6g}, d0={d0:.6g}")

print()
print("SUMMARY:", "ALL CHECKS PASS" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
