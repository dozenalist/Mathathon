"""Independent audit of supervisor/solve-six-colouring (read-only use of its data).
Checks: (1) the box list and its coverage; (2) the recorded 7-clique witnesses with EXACT
arithmetic under BOTH the closed-cell criterion (dmin<=1<=dmax) and the strict criterion
(dmin<1<dmax) that an actual partition needs."""
from fractions import Fraction as F
import json, sys

H = 60
def sq(m): return max(0, abs(m)-1)**2
def dmin2(p, q, s, t): return sq(p)*s*s + sq(q)*t*t
def dmax2(p, q, s, t): return (abs(p)+1)**2 * s*s + (abs(q)+1)**2 * t*t

# ---- 1. box list and coverage -------------------------------------------------
boxes = [(i, j) for i in range(1, 60) for j in range(i, 60) if i*i + j*j < 3600]
print(f"box list {{(i,j): 1<=i<=j<=59, i^2+j^2<3600}} has {len(boxes)} boxes "
      f"(worker claims 1401): {len(boxes)==1401}")
smin = min((F(i,H), F(j,H)) for i, j in boxes)
print(f"smallest covered s on the grid: {float(min(b[0] for b in boxes)/H):.6f} = 1/60")
# the union of the half-open boxes is exactly {(s,t) : 1/60 < s <= t, s^2+t^2 < 1}
probe = [(F(1,120), F(1,2)), (F(1,60), F(1,2)), (F(1,200), F(99,100))]
for (s, t) in probe:
    covered = any(F(i,H) < s <= F(i+1,H) and F(j,H) < t <= F(j+1,H) and i <= j for (i, j) in boxes)
    print(f"  (s,t)=({float(s):.5f},{float(t):.4f}) valid? {s*s+t*t < 1 and s <= t} ; covered by the 1401 boxes? {covered}")

# ---- 2. witnesses ------------------------------------------------------------
data = json.load(open('../solve-six-colouring/out/cover.json'))
cert = data["certified"]
print(f"\nrecorded certified boxes: {len(cert)} (worker claims 681): {len(cert)==681}")
print(f"recorded undecided count: {data.get('undecided_count', 'n/a')}; keys: {list(data.keys())[:8]}")

bad_close = bad_strict = 0
wall_close = wall_strict = 0
worst = None
for entry in cert:
    i, j = entry["box"]; cl = entry["clique"]
    # box is (i/H,(i+1)/H] x (j/H,(j+1)/H]; monotone bounds:
    #   dmin2 <= dmin2 at upper corner, dmax2 >= dmax2 at lower corner
    lo = (F(i,H), F(j,H)); hi = (F(i+1,H), F(j+1,H))
    for a in range(len(cl)):
        for b in range(a+1, len(cl)):
            p = cl[a][0]-cl[b][0]; q = cl[a][1]-cl[b][1]
            if p == 0 and q == 0:
                bad_close += 1; continue
            dmin_hi = dmin2(p, q, *hi)        # upper bound for dmin2 on the box
            dmax_lo = dmax2(p, q, *lo)        # lower bound for dmax2 on the box
            if not dmin_hi <= 1 <= dmax_lo: bad_close += 1
            # strict version, valid on the OPEN box: dmin2 < 1 (strict unless the value is 0)
            # and dmax2 > 1 (dmax2 is strictly increasing in s,t: both coefficients >= 1)
            # open-box version: dmin2 non-decreasing in (s,t) so dmin2 <= dmin_hi <= 1 on the box,
            # and it is < 1 strictly inside unless the value is constant 0; dmax2 is STRICTLY
            # increasing (both coefficients (|p|+1)^2 >= 1 > 0), so dmax2 > dmax_lo >= 1 inside.
            ok_strict = (dmin_hi <= 1) and (dmax_lo >= 1) and not (dmin_hi == 1 and sq(p)+sq(q) == 0)
            if not ok_strict:
                bad_strict += 1
                if worst is None: worst = (i, j, p, q, dmin_hi, dmax_lo)
            # does the pair need the equality endpoint at the upper corner?
            if dmin_hi == 1 or dmax_lo == 1: wall_strict += 1
print(f"\nwitness pairs checked: {7*6//2*len(cert)}")
print("  region covered: s > 1/60 only (no box has i = 0); s = 1/60 itself is in no box;")
print(f"  closed-cell criterion (<=,>=) failures: {bad_close}")
print(f"  failures of the open-box (strict-inside) criterion: {bad_strict}")
print(f"  pairs whose forcedness uses an EQUALITY at the closed upper corner (not strict there): {wall_strict}")
if worst: print("  first strict failure:", worst)
