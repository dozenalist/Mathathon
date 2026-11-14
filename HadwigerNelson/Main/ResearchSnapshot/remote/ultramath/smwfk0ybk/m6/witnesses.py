"""Extract and verify one model for every satisfiable (ell, ray geometry) at k = 6,
with all constraints (C1)-(C5), and write witnesses.json.

Every model is re-verified by check_model (which recomputes O_i, I_i from the
cell vector and checks C1,C2,C3,C4,C5 from scratch).
"""
import json
import tight_csp as T

out = {"k": 6, "note": "(C1)-(C5); cells are the ray cells c_j, c_0 = 0; "
                      "palettes are given as sorted label lists",
       "cases": []}
counts = {}
for ell in (3, 4, 5, 6):
    sat = 0
    for c in T.geometry_list(ell):
        ok, sols = T.solve(c, tight=True, want="first")
        if not ok:
            continue
        P = sols[0]
        err = T.check_model(c, P, tight=True)
        assert err is None, (c, err)
        # also require a pair-model to exist (the structural fact)
        ok2, sols2 = T.solve(c, maxsize=2, tight=True, want="first")
        assert ok2 and T.check_model(c, sols2[0], tight=True) is None
        sat += 1
        out["cases"].append({"ell": ell, "cells": list(c),
                             "palettes": T.as_sets(P),
                             "palettes_pair_model": T.as_sets(sols2[0])})
    counts[ell] = sat
out["counts"] = counts
json.dump(out, open("witnesses.json", "w"))
print("ell -> satisfiable geometries:", counts, " total", sum(counts.values()))
print("wrote witnesses.json (%d cases, all re-verified)" % len(out["cases"]))
