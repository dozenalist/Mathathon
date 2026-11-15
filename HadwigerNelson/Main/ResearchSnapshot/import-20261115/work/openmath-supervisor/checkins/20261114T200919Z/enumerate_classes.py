#!/usr/bin/env python3
"""Enumerate-and-decide skeleton over the 7776 finite classes of the continuous
six-direction input of the licensed relaxation R.

Class space:  [tau] in (Z/6)^6 / <(1,1,1,1,1,1)>, representative tau_0 = 0
              (see core.tau_of / core.canon; REPORT.md Sec.1).
Per class the decision is: does there exist P_0..P_5, each a nonempty set of size
<= 2 hitting R+(t+60j) and R-(t+60j), with P_j disjoint P_{j+1} for all j cyclic?
That is exactly R restricted to 2-witness palettes, which is EQUIVALENT to R
(both directions, REPORT.md Sec.2).

Memory: O(1) beyond the candidate alphabet (<= 21 sets per phase).
Use --limit for a slice, --all for the whole class space, --orbits to walk
<label-cycle, reflection> orbit representatives (730 instead of 7776).

NOT run in full here: see MANIFEST.md for the scheduled run.
"""
import argparse, json, sys, time
from itertools import product
from core import (C, E, PAT, cands, canon, Rsets_from_tau, solve_dp, solve_half,
                  count_solutions)

CLASSES = [(0,) + r for r in product(range(6), repeat=5)]


def Lift(tau):
    return canon(tuple(tau[(k - 1) % 6] for k in range(6)))


def Refl(tau):
    # plane reflection theta -> -theta: beta_k = -alpha_{5-k}, phase t -> -t.
    # On classes this is computed from the faithful model alpha_i = 60*tau_i at t=15.
    from fractions import Fraction as F
    from core import tau_of
    a = [60 * x for x in tau]
    b = [-a[(5 - k) % 6] for k in range(6)]
    tt, d = tau_of(b, F(-15))
    assert not d
    return canon(tt)


def orbit_reps():
    seen = set()
    out = []
    for c in CLASSES:
        if c in seen:
            continue
        stack = [c]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.append(Lift(x))
            stack.append(Refl(x))
        out.append(c)
    return out


def decide(tau):
    table = [cands(*R) for R in Rsets_from_tau(tau)]
    if any(len(t) == 0 for t in table):
        return dict(tau=list(tau), table=[[sorted(x) for x in t] for t in table],
                    sat=False, reason="a phase has no hitting set of size <=2",
                    sizes=[len(t) for t in table], nsol=0)
    sat, w = solve_dp(table)
    sat2, _ = solve_half(table)          # cross-check, different algorithm
    if sat != sat2:
        raise SystemExit(f"solver disagreement on {tau}")
    return dict(tau=list(tau), sizes=[len(t) for t in table], sat=sat,
                nsol=count_solutions(table) if sat else 0,
                table=None if sat else [[sorted(x) for x in t] for t in table],
                witness=None if not sat else [sorted(x) for x in w])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--orbits", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    cls = CLASSES if a.all else (orbit_reps() if a.orbits else CLASSES)
    if a.limit:
        cls = cls[:a.limit]
    t0 = time.time()
    n_sat = n_unsat = 0
    f = open(a.out, "w") if a.out else None
    for c in cls:
        rec = decide(c)
        n_sat += rec["sat"]
        n_unsat += not rec["sat"]
        if f:
            f.write(json.dumps(rec) + "\n")
        else:
            print(f"tau={c} sizes={rec['sizes']} SAT={rec['sat']} #sols={rec['nsol']}"
                  + ("" if rec["sat"] else "  UNSAT-table-exhausted"))
    if f:
        f.close()
    print(f"# decided {len(cls)} classes: SAT={n_sat} UNSAT={n_unsat} "
          f"in {time.time()-t0:.3f}s")


if __name__ == "__main__":
    main()
