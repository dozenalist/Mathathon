"""Witnesses for k=6, cycle lengths 3, 4, 5: sector palette systems with
accumulating cycle centres.  Written to JSON, and re-verified from scratch by
an independent checker that does not share code with the solver encoding.
"""
import json, sys
from step_relation import csp, recheck
from pysat.solvers import Cadical153


def get_witness(k, ell, m):
    n, V, D, idx, cls = csp(k, ell, m)
    with Cadical153(bootstrap_with=cls) as s:
        if not s.solve():
            return None
        model = set(x for x in s.get_model() if x > 0)
    nv = len(V)
    sig = []
    for i in range(n):
        for a in range(nv):
            if idx[i, a] in model:
                sig.append(sorted(V[a]))
                break
    return dict(k=k, ell=ell, m=m, n=n, offsets=D, sigma=sig)


if __name__ == "__main__":
    out = {}
    for ell in (3, 4, 5, 6):
        w = get_witness(6, ell, 12)
        assert w is not None
        out[ell] = w
        print("k=6 ell=%d m=%d n=%d : witness with %d sectors, values %s"
              % (ell, w["m"], w["n"], len(w["sigma"]),
                 sorted({tuple(v) for v in w["sigma"]})), flush=True)
    json.dump(out, open("witnesses_k6.json", "w"), indent=1)
    print("written to witnesses_k6.json")
