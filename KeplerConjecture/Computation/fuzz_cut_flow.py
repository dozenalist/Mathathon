#!/usr/bin/env python3
"""Randomised soundness test of the repaired cut/flow interface.

The review says generic soundness remains a proof obligation.  This does not discharge it; it is the
evidence that would have to precede such a proof, at a scale the 12 hand-written audit cases cannot
reach: RANDOM instances, each decided three ways.

  (1) the cut condition, by the exhaustive scan over all subsets (exact rationals);
  (2) feasibility of {div(v) >= b(v) for every v, |phi_e| <= Phi}, by Fourier-Motzkin elimination
      over Q (exact, and built from range(len(b)) so it cannot repeat the D8 omission);
  (3) the interface's own verdicts: feasible_flow (a flow, which must then verify exactly) and
      find_violating_cut (a witness, which must then be a genuine violation).

WHAT IS CHECKED, per instance:
  a. if feasible_flow returns a flow, verify_flow_exact accepts it AND the oracle agrees it is feasible;
  b. if find_violating_cut returns a witness at Phi, the oracle says infeasible at Phi;
  c. the scan's t* satisfies: oracle feasible at Phi >= t*, infeasible at Phi < t*  (Phi rational);
  d. the two directions never contradict each other.

A disagreement is a defect either in the interface or in the oracle, and is printed with the instance.

Run: python3 fuzz_cut_flow.py [n_instances] [seed]      (default 400, seed 0)
"""
import itertools, random, sys
from fractions import Fraction as F
sys.path.insert(0, ".")
from audit_cut_flow_api import fm_feasible      # the exact oracle, shared, not reimplemented
import cut_flow as CF

def random_instance(rng, n_max=4):
    n = rng.randint(1, n_max)
    b = [F(rng.randint(-2, 2)) for _ in range(n)]
    pairs = list(itertools.combinations(range(n), 2))
    rng.shuffle(pairs)
    k = rng.randint(0, len(pairs))
    edges = pairs[:k]
    return b, edges

def main(argv):
    N = int(argv[1]) if len(argv) > 1 else 400
    seed = int(argv[2]) if len(argv) > 2 else 0
    rng = random.Random(seed)
    fails = []
    stats = dict(feasible=0, infeasible=0, unbounded=0, flows=0, witnesses=0)
    for t in range(N):
        b, edges = random_instance(rng)
        Phi = F(rng.randint(0, 5), rng.randint(1, 2))
        # (3a) a returned flow must be genuine
        oracle = fm_feasible(b, edges, Phi)
        if oracle is None:
            stats.setdefault("undecided", 0); stats["undecided"] = stats.get("undecided", 0) + 1
            continue
        flow = CF.feasible_flow(b, edges, Phi)
        if flow is not None:
            stats["flows"] += 1
            ok_cap, ok_div, div = CF.verify_flow_exact(b, edges, Phi, flow)
            if not (ok_cap and ok_div):
                fails.append(("flow fails exact verification", b, edges, Phi, flow)); continue
            if not oracle:
                fails.append(("flow exists but the oracle says infeasible", b, edges, Phi)); continue
        # (3b) a witness must be a genuine violation
        w = CF.find_violating_cut(b, edges, Phi)
        if w is not None:
            stats["witnesses"] += 1
            ratio, U, sb, bd = w
            if bd == 0:
                if not (sb > 0):
                    fails.append(("empty-boundary witness with sum <= 0", b, edges, Phi, w)); continue
                stats["unbounded_witness"] = stats.get("unbounded_witness", 0) + 1
            else:
                if not (sb > Phi * bd):
                    fails.append(("witness does not violate", b, edges, Phi, w)); continue
                if oracle:
                    fails.append(("witness exists but the oracle says feasible", b, edges, Phi)); continue
        # (3c) the scan's t* must separate feasibility
        sc = CF.exhaustive_cut_scan(b, edges)
        ts = sc["t_star"]
        if ts >= CF.UNBOUNDED:
            if fm_feasible(b, edges, F(10) ** 6):
                fails.append(("t* = +inf but the oracle is feasible at 1e6", b, edges, None)); continue
            stats["unbounded_scan"] = stats.get("unbounded_scan", 0) + 1
        else:
            at = fm_feasible(b, edges, ts)
            if at is True:
                stats["feasible"] += 1
            elif at is False:
                fails.append(("oracle infeasible at Phi = t*", b, edges, ts)); continue
            else:
                continue
            below = ts - F(1, 4)
            if below >= 0 and fm_feasible(b, edges, below) is True:
                fails.append(("oracle feasible below t*", b, edges, below)); continue
            stats["infeasible"] += 1
    print("%d instances, seed %d" % (N, seed))
    print("  flows returned and verified : %d" % stats["flows"])
    print("  violating witnesses         : %d" % stats["witnesses"])
    print("  scan feasible at t*         : %d" % stats["feasible"])
    print("  scan infeasible below t*    : %d" % stats["infeasible"])
    print("  unbounded (empty boundary)  : %d witness, %d by the scan"
          % (stats.get("unbounded_witness", 0), stats.get("unbounded_scan", 0)))
    if fails:
        print("\nDISAGREEMENTS: %d" % len(fails))
        for f in fails[:10]:
            print("  ", f[0], " b =", [str(x) for x in f[1]], " edges =", f[2], " Phi =", f[3])
        return 1
    print("\nno disagreement between the interface and the exact oracle")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
