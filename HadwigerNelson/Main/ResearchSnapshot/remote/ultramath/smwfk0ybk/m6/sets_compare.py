"""Compare the SAT geometry sets of (C1)-(C3) and (C1)-(C5) at k = 6,
and decide the ternary-free variant (C1)-(C3) with |P| <= 2."""
import json
from itertools import product
import tight_csp as T

out = {}
for ell in (3,4,5,6):
    S13, S15, S2 = set(), set(), set()
    geoms = T.geometry_list(ell)
    for c in geoms:
        s13,_ = T.solve(c, tight=False, want="first")
        s15,_ = T.solve(c, tight=True, want="first")
        s2,_  = T.solve(c, maxsize=2, tight=True, want="first")
        if s13: S13.add(c)
        if s15: S15.add(c)
        if s2:  S2.add(c)
    print("ell=%d  |C1-C3 SAT|=%d  |C1-C5 SAT|=%d  |C1-C3,|P|<=2 SAT|=%d  "
          "sets equal (13 vs 15): %s ; (15 vs <=2): %s"
          % (ell, len(S13), len(S15), len(S2), S13==S15, S15==S2), flush=True)
    out[ell] = {"sat_C13": len(S13), "sat_C15": len(S15), "sat_pair": len(S2),
                "eq_13_15": S13==S15, "eq_15_pair": S15==S2,
                "diff_15_minus_pair": [list(x) for x in sorted(S15-S2)],
                "diff_pair_minus_15": [list(x) for x in sorted(S2-S15)]}
json.dump(out, open("sets_compare.json","w"), indent=1)
print("\nwrote sets_compare.json")
