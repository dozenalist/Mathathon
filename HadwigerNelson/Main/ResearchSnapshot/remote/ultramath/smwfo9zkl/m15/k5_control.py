"""k = 5 control table: resolution thresholds for the same constraint system.

k=5, ell=3 : UNSAT at every resolution tested (hand proof: Lemma 3).
k=5, ell=4 : UNSAT at m=3, SAT from m=6.
k=5, ell=5 : UNSAT at m <= 9, SAT from m=10.

The last two show that only the triangle case is decided by the palette
constraints at k=5: the paper's 4-cycle and 5-cycle local-finiteness proofs use
strictly more than (P0)-(P4).
"""
import sys
from sector_csp_general import solve

EXPECT = {3: {2: False, 3: False, 4: False, 6: False, 9: False, 12: False,
              18: False, 30: False, 60: False},
          4: {3: False, 6: True, 12: True, 24: True},
          5: {3: False, 6: False, 9: False, 10: True, 11: True, 12: True,
              24: True}}

if __name__ == "__main__":
    bad = 0
    for ell, tab in EXPECT.items():
        for m, want in sorted(tab.items()):
            sat, sig, info = solve(5, ell, m)
            ok = (sat == want)
            bad += not ok
            print("  k=5 ell=%d m=%2d n=%3d |V|=%d  SAT=%-5s (expected %-5s) %s"
                  % (ell, m, info["n"], info["nv"], sat, want,
                     "OK" if ok else "MISMATCH"))
    print("mismatches:", bad)
    sys.exit(0 if bad == 0 else 1)
