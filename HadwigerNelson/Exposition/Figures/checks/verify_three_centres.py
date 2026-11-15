"""Verify the Lesson 5 and Lesson 6 figures and the Lesson 5 counting claim.
Usage: python verify_three_centres.py <Figures dir>
Checks: (1) three-centre-triangle.svg side lengths and support-arc geometry;
(2) the counting step of Section 29 by exhaustive search over all palette triples;
(3) proof-casefan.svg arrow structure (one arrow into step 5, exactly three branches, three into the contradiction)."""
import itertools, math, re, sys
from collections import Counter
from pathlib import Path

FIG = Path(sys.argv[1])

# (1) triangle
s = (FIG / "three-centre-triangle.svg").read_text(encoding="utf-8")
U = 300.0
x, y, z = [tuple(map(float, d)) for d in re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="[78]"', s)]
dist = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1]) / U
ang = lambda p: math.degrees(math.atan2(-(p[1] - x[1]), p[0] - x[0]))
print("TRIANGLE |xy|=%.6f |xz|=%.6f |yz|=%.6f" % (dist(x, y), dist(x, z), dist(y, z)))
print("  direction of y %.4f deg, of z %.4f deg" % (ang(y), ang(z)))
for pl in re.findall(r'<polyline points="([^"]+)" fill="none" stroke="#235f9d" stroke-width="9"', s):
    pts = [tuple(map(float, p.split(","))) for p in pl.split()]
    a = [ang(p) for p in pts]; r = [dist(p, x) for p in pts]
    print("  support arc %.2f..%.2f deg, radius %.5f..%.5f" % (min(a), max(a), min(r), max(r)))

# (2) counting step
subsets = [frozenset(c) for n in range(6) for c in itertools.combinations(range(5), n)]
def count(J, K):
    sols = []
    for P in subsets:
        if not J <= P: continue
        for Q in subsets:
            if P & Q or Q <= K: continue
            for R in subsets:
                if P & R or Q & R or R <= K: continue
                sols.append((sorted(P), sorted(Q), sorted(R)))
    return sols
for J, K in [({0, 1}, {2, 3}), ({0, 1}, {2}), ({0, 1, 2}, {2, 3})]:
    sols = count(frozenset(J), frozenset(K))
    print(f"COUNT J={sorted(J)} K={sorted(K)}: {len(sols)} triples satisfy all conditions" + (f"; e.g. {sols[0]}" if sols else ""))

# (3) case fan
s = (FIG / "proof-casefan.svg").read_text(encoding="utf-8")
print("CASEFAN arrows:", dict(Counter(re.findall(r'data-id="([^"]+)"', s))))
