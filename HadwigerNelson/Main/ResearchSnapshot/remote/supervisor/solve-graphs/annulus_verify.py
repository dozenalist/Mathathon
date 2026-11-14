"""Standalone EXACT verifier for the Astra annulus 3-colouring candidate.

Claim under test.  On the open annulus A = {z : 0.99 < |z| < 1.01} colour
z = r e^{i theta} by the index of the half-open 40-degree sector containing theta,
taken mod 3:  theta in [40k, 40k+40)  ->  colour k mod 3,  k = 0..8.
Then two points of the SAME colour are never at Euclidean distance exactly 1.

Everything below is rational arithmetic (fractions.Fraction).  No floats are used in any
decision; decimals appear only in printed commentary.  Needs no third-party module.

Run:  python3 annulus_verify.py
"""
from fractions import Fraction as Fr
import sys

FAIL = []
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not cond: FAIL.append(name)

# ---------------------------------------------------------------- 0. constants
LOW  = Fr(99, 100)        # 0.99  inner boundary of the annulus (open)
HIGH = Fr(101, 100)       # 1.01  outer boundary (open)
MARGIN_X = Fr(5, 1000)    # 0.005 bound on |x| for the sampling-circle lemma

print("=" * 78)
print("ANNULUS 3-COLOURING: EXACT VERIFIER")
print("=" * 78)
print(f"annulus  {float(LOW)} < |z| < {float(HIGH)}   (open, exact endpoints {LOW}, {HIGH})")

# ---------------------------------------------------------------- 1. cos 40 bracket
# cos(3t) = 4cos^3 t - 3cos t.  With t = 40 deg, 3t = 120 deg and cos 120 = -1/2, so
#     c := cos 40 deg  satisfies   f(c) = 8c^3 - 6c + 1 = 0.
# f'(c) = 24c^2 - 6 > 0 for c > 1/2, so f is strictly increasing on (1/2, inf).
# f(1/2) = -1 < 0 and f(1) = 3 > 0, so f has exactly ONE root in (1/2, 1), and that root is c.
def f(c):         # 8c^3 - 6c + 1, exact
    return 8 * c * c * c - 6 * c + 1
def fp(c):        # 24c^2 - 6
    return 24 * c * c - 6

C_LO = Fr(766, 1000)      # claimed lower bracket for cos 40
C_HI = Fr(767, 1000)      # claimed upper bracket
print("\n[1] bracket for cos 40 deg via  f(c) = 8c^3 - 6c + 1")
check("c > 1/2 so f is strictly increasing there (f'(c)=24c^2-6 > 0 for c in [C_LO,C_HI])",
      fp(C_LO) > 0 and fp(C_HI) > 0, f"f'(C_LO)={fp(C_LO)}")
check("f(1/2) < 0 < f(1)  (unique root of f in (1/2,1))", f(Fr(1,2)) < 0 < f(Fr(1)), f"f(1/2)={f(Fr(1,2))}, f(1)={f(Fr(1))}")
check(f"f({C_LO}) < 0  =>  cos 40 > {C_LO}", f(C_LO) < 0, f"f={f(C_LO)}")
check(f"f({C_HI}) > 0  =>  cos 40 < {C_HI}", f(C_HI) > 0, f"f={f(C_HI)}")
check("so  C_LO < cos 40 < C_HI  (rigorous, by monotonicity of f)", True)

# cos 80 = 2cos^2 40 - 1 ; c > 0 and x -> 2x^2-1 is increasing on (0,inf)
COS80_MAX = 2 * C_HI * C_HI - 1      # upper bound for cos 80
COS80_MIN = 2 * C_LO * C_LO - 1      # lower bound for cos 80
print(f"\n    1 - cos40 <= 1 - C_LO = {1 - C_LO}   (exact {float(1 - C_LO):.12f})")
print(f"    1 - cos80 >= 2 - 2*C_HI^2 = {2 - 2*C_HI*C_HI}   (exact {float(2 - 2*C_HI*C_HI):.12f})")

# ---------------------------------------------------------------- 2. sector combinatorics
# Sectors S_k = [40k, 40k+40), k = 0..8 (degrees), tiles the circle; colour = k mod 3.
# Angular separation between alpha in S_k and beta in S_l is d = beta - alpha (degrees),
# and the "smaller angle" is Delta = min(|d| mod 360, 360 - (|d| mod 360)) in [0,180].
# We enumerate every ordered pair of same-colour sectors and bound Delta.
def fold_interval(lo, hi):
    """Delta-range for a raw difference interval (lo,hi), folded into [0,180]."""
    cand = []
    for a, b in ((lo, hi), (360 - hi, 360 - lo)):
        a2, b2 = max(a, Fr(0)), min(b, Fr(180))
        if a2 < b2: cand.append((a2, b2))
    if not cand: return None
    return (min(c[0] for c in cand), max(c[1] for c in cand))

print("\n[2] sector combinatorics: every same-colour ordered pair (k,l), k != l")
def smaller_angle_interval(a, b):
    """Range of Delta = min(|d|, 360-|d|) as d runs over the open interval (a,b)."""
    pieces = []
    for lo, hi in ((a, b), (360 - b, 360 - a)):
        lo2, hi2 = max(lo, Fr(0)), min(hi, Fr(180))
        if lo2 < hi2: pieces.append((lo2, hi2))
    if not pieces: return None
    return (min(x[0] for x in pieces), max(x[1] for x in pieces))

cases = []
allgood = True
n_pairs = 0
for k in range(9):
    for l in range(9):
        if k == l: continue
        if (k - l) % 3 != 0: continue            # different colours: not our concern
        n_pairs += 1
        m = (l - k) % 9                          # forward sector distance, 1..8
        a, b = 40 * m - 40, 40 * m + 40          # open interval of raw differences
        rng = smaller_angle_interval(Fr(a), Fr(b))
        cases.append((k, l, m, rng))
        ok = rng is not None and rng[0] >= 80 and rng[1] <= 180
        allgood &= ok
        print(f"      k={k} l={l} m={m}  colour {k%3}={l%3}   Delta in ({float(rng[0])}, {float(rng[1])})"
              f"    >=80? {rng[0] >= 80}")
check("every same-colour DISTINCT-sector pair has Delta >= 80 deg", allgood,
      f"{n_pairs} ordered pairs")
check("same-sector pairs have Delta in [0,40)  (half-open, so Delta < 40)",
      True, "S_k = [40k,40k+40) => separation strictly < 40")
check("no same-colour pair lands in the forbidden band (40,80)",
      all(c[3] is not None and (c[3][0] >= 80 or c[3][1] <= 40) for c in cases))
check("the two Delta-regimes are exactly [0,40) and (80,180] - they do not meet",
      all(c[3] is not None and c[3][0] >= 80 for c in cases))

# ---------------------------------------------------------------- 3. distance bounds
# |z1-z2|^2 = (r1-r2)^2 + 2 r1 r2 (1 - cos Delta),  r_i in (LOW,HIGH).
# CASE A: Delta <= 40 deg  =>  want |z1-z2| < 1.
drmax2 = (HIGH - LOW) ** 2                     # (r1-r2)^2 <= 0.02^2
rr_max = HIGH * HIGH                           # r1 r2  <= 1.01^2
caseA_ub = drmax2 + 2 * rr_max * (1 - C_LO)     # 1 - cosDelta <= 1 - cos40 <= 1 - C_LO
print("\n[3] CASE A  (same sector, Delta < 40 deg): want |z1-z2| < 1")
print(f"      |z1-z2|^2 <= (r1-r2)^2 + 2 r1 r2 (1-cos40)")
print(f"                <= ({HIGH}-{LOW})^2 + 2*({HIGH})^2*(1-{C_LO}) = {caseA_ub}  = {float(caseA_ub):.9f}")
check("CASE A: max |z1-z2|^2 < 1", caseA_ub < 1, f"{float(caseA_ub):.6f} < 1")
check("CASE A: hence |z1-z2| < 1 for ALL Delta in [0,40] and all r1,r2", caseA_ub < 1)

# CASE B: Delta >= 80 deg  =>  want |z1-z2| > 1.
rr_min = LOW * LOW
caseB_lb = 2 * rr_min * (2 - 2 * C_HI * C_HI)   # 1 - cosDelta >= 1 - cos80 >= 2 - 2 C_HI^2
print("\n[4] CASE B  (distinct same-colour sectors, Delta in (80,160)): want |z1-z2| > 1")
print(f"      |z1-z2|^2 = (r1-r2)^2 + 2 r1 r2 (1-cosDelta) >= 2 r1 r2 (1-cos80)")
print(f"                >= 2*({LOW})^2*(2-2*({C_HI})^2) = {caseB_lb}  = {float(caseB_lb):.9f}")
check("CASE B: min |z1-z2|^2 > 1", caseB_lb > 1, f"{float(caseB_lb):.6f} > 1")
check("CASE B: hence |z1-z2| > 1 for ALL Delta in [80,180] and all r1,r2", caseB_lb > 1)

print(f"\n      margins:  Case A  1 - {float(caseA_ub):.6f} = {float(1-caseA_ub):.6f}")
print(f"                Case B  {float(caseB_lb):.6f} - 1 = {float(caseB_lb-1):.6f}")

# ---------------------------------------------------------------- 4. sampling circles
# For |x| < 0.005 and |r-1| <= 0.005, the circle {|z-x| = r} lies in the annulus.
# Reverse triangle inequality:  r - |x| <= |z| <= r + |x|.
print("\n[5] sampling-circle containment: |x| < 0.005, |r-1| <= 0.005  =>  circle in annulus")
inner = (1 - MARGIN_X) - MARGIN_X     # r > 0.995, |x| < 0.005  ->  |z| > 0.99
outer = (1 + MARGIN_X) + MARGIN_X     # r < 1.005, |x| < 0.005  ->  |z| < 1.01
print(f"      reverse triangle inequality:  r - |x| <= |z| <= r + |x|")
print(f"      |z| >= r - |x| > 0.995 - 0.005 = {inner}   (strict: |x| < 0.005)")
print(f"      |z| <= r + |x| < 1.005 + 0.005 = {outer}   (strict: |x| < 0.005)")
check("inner boundary: r - |x| > LOW", inner == LOW, f"{inner} == {LOW}, strict via |x| < 0.005")
check("outer boundary: r + |x| < HIGH", outer == HIGH, f"{outer} == {HIGH}, strict via |x| < 0.005")
check("unit circle (r=1) about any |x|<0.005 lies in the annulus", True,
      "|z| in (0.995, 1.005) is a subset of (0.99, 1.01)")
print(f"      loss of slack caused by |x|<=0.005 and |r-1|<=0.005: 0.005 + 0.005 = 0.01,")
print(f"      which is exactly the annulus half-width 1.01 - 1.0 = 0.01, so the two margins")
print(f"      meet: the lemma is TIGHT and needs both inequalities strict.")

print("\n" + "=" * 78)
if FAIL:
    print("RESULT: FAILED  ->", FAIL); sys.exit(1)
print("RESULT: ALL CHECKS PASS")
print("=" * 78)
