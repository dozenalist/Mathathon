"""Calibration of the k = 6 decision procedure against the paper's own theorems.

The same code, with the label count k set to 4, 5, 6 and the two global
constraints switched off, must reproduce m5's table (which at (5,5) is a
strengthening of the paper's Proposition 8.2 and at k = 4 the paper-level
Theorem 2 of INTERFACE-NOGO.md).  This is what makes the encoding non-vacuous:
it refutes the five-cycle at k = 5 exactly as the published proof does.
"""
import tight_csp as T

def run(k, ells, tight):
    T.K = k; T.FULL = (1 << k) - 1
    out = {}
    for ell in ells:
        geoms = T.geometry_list(ell)
        sat = 0
        for c in geoms:
            if c[0] != 0:            # geometry_list normalises c_0 = 0
                continue
            s, _ = T.solve(c, maxsize=k - 3, tight=tight, want="first")
            sat += 1 if s else 0
        out[ell] = (sat, len(T.geometry_list(ell)))
    T.K = 6; T.FULL = (1 << 6) - 1
    return out

print("k = 4 (paper: state level is complete, every length UNSAT)")
for ell, (s, n) in run(4, (3, 4), False).items():
    print("   ell=%d  SAT=%d / %d" % (ell, s, n))
print("k = 5 (paper: l = 5 UNSAT = Prop 8.2; l = 3,4 partially SAT)")
for ell, (s, n) in run(5, (3, 4, 5), False).items():
    print("   ell=%d  SAT=%d / %d" % (ell, s, n))
print("k = 6, (C1)-(C3) only [m5 table: 36, 216, 225, 177]")
for ell, (s, n) in run(6, (3, 4, 5, 6), False).items():
    print("   ell=%d  SAT=%d / %d" % (ell, s, n))
print("k = 6, tightened (C1)-(C5)")
for ell, (s, n) in run(6, (3, 4, 5, 6), True).items():
    print("   ell=%d  SAT=%d / %d" % (ell, s, n))
