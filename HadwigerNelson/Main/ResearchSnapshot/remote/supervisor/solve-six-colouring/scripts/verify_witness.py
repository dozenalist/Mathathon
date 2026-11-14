"""Independent-arithmetic check of every certified box: for each recorded 7-clique and each
corner/interior sample point of its box, verify all 21 pairwise differences are forced, using
exact Fraction arithmetic on the ORIGINAL dmin/dmax formulas (not the integer scaling)."""
import json, sys
from fractions import Fraction as Fr
def sq(n):
    n = abs(n); return max(0, n-1)**2
def forced(s, t, p, q):
    if p == 0 and q == 0: return False
    return (sq(p)*s*s + sq(q)*t*t <= 1 <= (abs(p)+1)**2*s*s + (abs(q)+1)**2*t*t)
d = json.load(open("out/cover.json"))
bad = 0; checked = 0; boxes_ok = 0
for r in d["certified"]:
    i, j = r["box"]; cl = [tuple(v) for v in r["clique"]]
    assert len(cl) == 7 and len(set(cl)) == 7, r
    for (a, b) in [(i, j), (i+1, j), (i, j+1), (i+1, j+1),
                   (Fr(i)+Fr(3,7), Fr(j)+Fr(2,5)), (Fr(i)+Fr(1,2), Fr(j)+Fr(1,2))]:
        s, t = (Fr(a, 60), Fr(b, 60)) if not isinstance(a, Fr) else (a/60, b/60)
        ok = all(forced(s, t, u[0]-v[0], u[1]-v[1]) for u in cl for v in cl if u != v)
        checked += 1
        if not ok:
            bad += 1
            if bad < 5: print("FAIL", r["box"], (float(s), float(t)))
    else:
        boxes_ok += 1
print(f"certified boxes re-verified: {boxes_ok}/{len(d['certified'])}; point-checks {checked}; failures {bad}")
# the headline structural claim
und = {(r["box"][0], r["box"][1]) for r in d["undecided"]}
print("any undecided box with i>=26:", any(i >= 26 for i, j in und))
print("undecided max i:", max(i for i, j in und))
print("certified with i<=5:", sorted((i, j) for r in d["certified"] for i, j in [r["box"]] if i <= 5))
