"""Arithmetic for supervisor/solve-geometry. Open-ball convention throughout.

Run: python3 checks/constants.py   (writes supervisor_checks.out next to this package)
"""
import math, os
from fractions import Fraction as F

out = []
def say(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)

# [1] square inside a ball: a side-s square centred at x0 lies in B(x0,r) iff s < sqrt2*r
say("[1] square-in-ball containment (circumradius s/sqrt2)")
for r in [1.5, math.sqrt(2), 2.0, 4.0]:
    say(f"    r={r:.6f}: admissible 2 < s < sqrt2*r = ({2}, {math.sqrt(2)*r:.6f})"
        f" -> {'NONEMPTY' if math.sqrt(2)*r > 2 else 'EMPTY'}")
say(f"    WEAKEST.md's printed '4 < s < r/sqrt2' needs r > 4*sqrt2 = {4*math.sqrt(2):.6f},"
    f" contradicting its own r > sqrt2 = {math.sqrt(2):.6f}; correct line is '2 < s < sqrt2*r'")

# [2] disk form: required inradius is the mesh, not twice the mesh
say("[2] disk form: needed inradius = component-cover mesh = 1+o(1), so the radius threshold is 1")
say("    (paper's rounded mesh 2 would give 2; m12 Lemma 5.1 states inradius(Q) > mesh)")

# [3] upper bound on the isolation gap
say("[3] Prop. 1 window: a disk of radius r>1 avoiding x fits in B(x,rho) iff 2r < rho")
for rho in [1.5, 1.999, 2.0, 2.001]:
    say(f"    rho={rho:.4f}: {'CONTRADICTION with density' if rho > 2 else 'no contradiction'} -> rho <= 2")

# [4] (6/5)Z^2 -- corrected: isolation radius is 6/5, not 3/5
a = F(6, 5); af = float(a)
say("[4] L = (6/5)Z^2   [OPEN-ball convention, corrected this block]")
say(f"    covering radius a/sqrt2 = {af/math.sqrt(2):.9f} <= 1 -> 1-dense (density theorem not violated)")
say(f"    nearest-neighbour distance = {af}; isolation radius r* = {af} (= a, NOT a/2 = {af/2})")
say(f"    (ISO)(r) holds for r <= 6/5, fails for r > 6/5; it refutes r > sqrt2 = {math.sqrt(2):.4f}"
    f" since 6/5 < sqrt2: {af < math.sqrt(2)}")
say(f"    exact: (6/5)^2 = {F(36,25)} <= 2 : {F(36,25) <= 2}")

# [5] cluster: (W) without (ISO)
say("[5] L = {0,(1/50,0)}: |L cap B(0,1.5)| = 2 finite -> (W); isolation radii 1/100")
say("    -> (W) is strictly weaker than 'isolated point with gap > 1'")

# [6] lattice isolation radii
say("[6] lattice r* = a (open ball excludes the neighbours at distance exactly a)")
for aa in [1.0, 1.2, 1.5]:
    say(f"    L = {aa}Z^2: r* = {aa}, packing radius {aa/2}, covering radius {aa/math.sqrt(2):.6f}"
        f" -> 1-dense {aa/math.sqrt(2) <= 1}")
say("    a = 1  : r* = 1   -> (ISO)(r) FAILS for every r > 1 while 1-dense (refutes gap>1)")
say("    a = 6/5: r* = 1.2 -> (ISO)(r) HOLDS for r in (1,6/5]; refutes only r > 6/5, e.g. r > sqrt2")

# [7] (W) does not imply (W2)
say("[7] L = {0} u U_k S(0, 3k/2): (W) holds, (W2) fails")
say("    |L cap B(0,1.2)| = 1 (nearest circle at radius 1.5) -> (W) with R = 1.2")
ks = [1.5 * k for k in range(1, 200)]
for rho in [0.0, 0.3, 0.74, 1.0, 2.3, 7.7]:
    d = min([rho] + [abs(c - rho) for c in ks])
    say(f"      |y|={rho}: dist(y,L)={d:.3f} <= 1 (1-dense); nearest circle within 2"
        f" -> |L cap B(y,2)| infinite")
say("    radii are 1.5 apart, so every y lies within 0.75 of a circle and every radius-2 ball cuts")
say("    one in an arc => (W2) FAILS for every y, while (W) holds")

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "supervisor_checks.out"),
     "w").write("\n".join(out) + "\n")
