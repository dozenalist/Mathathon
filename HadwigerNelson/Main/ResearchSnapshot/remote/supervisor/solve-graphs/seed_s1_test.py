"""Seed S1 test -- PREPARED FOR THE NEXT BLOCK, NOT RUN IN THIS BLOCK.
Geometry owns the sole compute slot this block; this file must not be executed yet.

Spec: SEED-S1.md.  One process, hard 60 s cap covering generation, validation, all solver
calls and witness/certificate checks.  Deterministic; stops at the first failed stage.

    python3 seed_s1_test.py            # to be run next block, once the slot is free

Stages (stop at first failure):
  0  build M, translate by tau=(3/2, sqrt3/2), dedup, all-induced unit edges
  1  exact validation + cross-edge count + clique number (K4 => arithmetic bug)
  2  does Theorem A's hypothesis hold? (it requires ZERO cross edges)
  3  5-colourability by CDCL; SAT => verify colouring on ALL edges;
     UNSAT => save CNF, attempt DRAT, check with tools/drat-trim, report SOLVER-ONLY if unchecked
  4  (only if 3 is SAT+verified) report palette structure WITHOUT any forcing claim
"""
import json, os, sys, time, threading

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
T0 = time.time()
DEADLINE = 58.0

from udg.exact import Field
from udg.graph import cnf, clique_number_bound
from udg import build as B
from pysat.solvers import Solver

OUT = os.path.join(HERE, "certs/seed_s1.json")
rec = {"spec": "SEED-S1.md", "stage": "start"}
def save(**kw):
    rec.update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(OUT, "w"), indent=1)
def left():
    return DEADLINE - (time.time() - T0)

F = Field([3, 11])                      # the spindle's own field, basis {1, sqrt3, sqrt11, sqrt33}

# ---------------------------------------------------------------- stage 0
ps, info = B.moser()                    # 7 vertices, 11 edges, chi = 4, exact in Q(sqrt3,sqrt11)
base = ps.copy()
n0 = len(base.pts)
assert n0 == 7, n0

# tau = (3/2, sqrt3/2);  |tau|^2 = 9/4 + 3/4 = 3 exactly, so |tau| = sqrt3.
# sqrt3 is the diamond's characteristic tip separation (Theorem C), so this translate is aimed
# at creating NEW diamonds between the copies rather than an incidental disjoint union.
x_t = tuple(c / 2 for c in F.rat(3))
y_t = tuple(c / 2 for c in F.sqrt(3))

def shift(pt):
    return (F.add(pt[0], x_t), F.add(pt[1], y_t))

for k in range(n0):
    base.pts.append(shift(base.pts[k]))
    base.names.append(f"{base.names[k]}+tau")

merged, dups = base.canonical()          # exact-coordinate dedup; coincidences recorded
rec["stage0"] = {"n_before_dedup": len(base.pts), "n_after_dedup": len(merged.pts),
                 "coincidences": dups, "tau": "3/2, sqrt3/2", "tau_sq_norm": 3}
save(stage="stage0_built")
print(f"[0] points {len(base.pts)} -> {len(merged.pts)} after dedup ({dups} coincidences)")

# ---------------------------------------------------------------- stage 1
adj, nonedges = merged.unit_graph()
n = len(merged.pts)
m = sum(len(a) for a in adj) // 2
cross = [(i, j) for i in range(n) for j in adj[i]
         if i < j and (merged.names[i].endswith("+tau") != merged.names[j].endswith("+tau"))]
omega = clique_number_bound(adj)
distinct = len({(tuple(x), tuple(y)) for x, y in merged.pts}) == n
rec["stage1"] = {"n": n, "m": m, "cross_edges": len(cross), "omega": omega,
                 "all_distinct": distinct}
save(stage="stage1_validated")
print(f"[1] n={n} m={m} cross_edges={len(cross)} omega={omega} distinct={distinct}")
if not distinct:
    save(stage="ABORT", why="coincident points survived dedup"); raise SystemExit(0)
if omega >= 4:
    save(stage="ABORT", why="clique number >= 4: impossible in the plane, arithmetic bug")
    raise SystemExit(0)

# ---------------------------------------------------------------- stage 2
rec["stage2_theoremA_hypothesis_holds"] = (len(cross) == 0)
save(stage="stage2")
print(f"[2] Theorem A hypothesis would need zero cross edges; measured {len(cross)}"
      f" -> {'clique-sum, uninteresting by Theorem A' if not cross else 'NOT a clique-sum'}")

# ---------------------------------------------------------------- stage 3
nv, cl = cnf(adj, 5)
sol = Solver(name="cadical153", bootstrap_with=cl)
tm = threading.Timer(max(2.0, min(20.0, left() - 30)), sol.interrupt); tm.start()
try:
    st = sol.solve_limited(expect_interrupt=True); model = sol.get_model() if st else None
finally:
    tm.cancel(); sol.delete()

def verify(c, edges):
    return sum(1 for u, v in edges if c[u] == c[v])

edges = [(i, j) for i in range(n) for j in adj[i] if i < j]
if st is None:
    rec["stage3"] = {"verdict": "TIMEOUT"}; save(); print("[3] TIMEOUT -> inconclusive")
elif st:
    c = [next(kk for kk in range(5) if (v * 5 + kk + 1) in set(model)) for v in range(n)]
    bad = verify(c, edges)
    rec["stage3"] = {"verdict": "SAT", "monochromatic_edges": bad, "colouring": c,
                     "verified": bad == 0}
    save(); print(f"[3] SAT, verified={bad == 0} (monochromatic {bad} of {len(edges)})")
    if bad:
        raise SystemExit(0)
else:
    # ---- 5-UNSAT: a separate candidate, never certified here
    cnfp = os.path.join(HERE, "certs/seed_s1_k5.cnf")
    with open(cnfp, "w") as g:
        g.write(f"p cnf {nv} {len(cl)}\n")
        for x in cl:
            g.write(" ".join(map(str, x)) + " 0\n")
    rec["stage3"] = {"verdict": "UNSAT_SOLVER_ONLY", "cnf": os.path.basename(cnfp),
                     "note": "chi >= 6 from this seed would be extraordinary; treat as a red flag "
                             "requiring a drat-trim checked proof before any interpretation"}
    save(); print("[3] UNSAT (solver-only) ->", cnfp)
    raise SystemExit(0)

# ---------------------------------------------------------------- stage 4
# Palette structure around the sqrt3 pair inherited from the spindle.  Report only:
# no forcing claim, because per SEED-S1.md a 5-forcing statement needs its own
# pre-registration and a separating-witness certificate.
rec["stage4"] = {"note": "palette measurement only; no forcing claim; needs its own prereg"}
save(stage="done")
print(f"[4] done in {time.time() - T0:.2f}s; results in {OUT}")
