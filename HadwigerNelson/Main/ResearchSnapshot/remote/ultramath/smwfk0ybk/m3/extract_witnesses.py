"""Extract and verify a tightened-CSP witness for EVERY satisfiable (l, geometry) at k = 6.

Each witness is re-checked against the paper's LITERAL definition of the slivers
(O(e) = labels left after removing the endpoints of every positive edge, I(e) likewise
for the negative edges; labels outside the cycle belong to both), independently of
m5's encoding, and against every clause of (C1)-(C5).
"""
import json
from itertools import product
from csp_vacuity import sig_matrix, admissible, solve
from paper_defs import paper_slivers

K = 6


def check(cells, pal, l):
    """independent verification of one witness; returns list of failures"""
    sig = sig_matrix(l, cells)
    fails = []
    labels = set(range(K))
    for i in range(6):
        P = set(pal[i])
        O, I = paper_slivers(l, K, sig[i])
        if not (1 <= len(P) <= K - 3):
            fails.append(f"(C1) at {i}")
        if not (P & O):
            fails.append(f"(C2-O) at {i}")
        if not (P & I):
            fails.append(f"(C2-I) at {i}")
    for i in range(6):
        if set(pal[i]) & set(pal[(i + 1) % 6]):
            fails.append(f"(C3) at {i}")
    for i in range(6):
        for j in range(i + 1, 6):
            if set(pal[i]) | set(pal[j]) == labels:
                fails.append(f"(C4) at ({i},{j})")
    if sum(1 for i in range(6) if len(set(pal[i])) == 3) > 3:
        fails.append("(C5)")
    return fails


def main():
    out = {"k": K, "instances": {}, "unsat": {}}
    total_sat = 0
    for l in range(3, K + 1):
        wits = []
        unsat = 0
        for tail in product(range(6), repeat=l - 1):
            c = (0,) + tail
            adm = admissible(l, K, sig_matrix(l, c), K - 3)
            model = solve(adm, True) if all(adm) else None
            if model is None:
                unsat += 1
                continue
            f = check(c, model, l)
            if f:
                raise SystemExit(f"WITNESS FAILED {l} {c}: {f}")
            wits.append({"cells": list(c), "palettes": model,
                         "sizes": [len(p) for p in model]})
        out["instances"][str(l)] = {"satisfiable": len(wits), "unsatisfiable": unsat,
                                    "all_witnesses_binary": all(max(w["sizes"]) <= 2 for w in wits),
                                    "witnesses": wits}
        out["unsat"][str(l)] = unsat
        total_sat += len(wits)
        print(f"l={l}: {len(wits)} satisfiable with a verified witness, {unsat} unsatisfiable; "
              f"all witnesses have palette sizes <= 2: "
              f"{all(max(w['sizes']) <= 2 for w in wits)}", flush=True)
    out["total_satisfiable"] = total_sat
    out["total_instances"] = sum(6 ** (l - 1) for l in range(3, K + 1))
    json.dump(out, open("witnesses_k6.json", "w"), indent=1)
    print(f"total: {total_sat}/{out['total_instances']} instances satisfiable, "
          f"every witness verified against the paper's literal sliver definition")


if __name__ == "__main__":
    main()
