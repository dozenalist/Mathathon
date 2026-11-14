"""The single bounded computation of the block (see EXPERIMENT-disequality.md).
One process, 58 s internal deadline, checkpointed JSON after every stage.
"""
import sys, os, time, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 58.0
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf, verify_colouring
from pysat.solvers import Solver
import threading

def solve_capped(clauses, cap):
    """SAT solve with a hard wall cap.  This pysat build has no time_limit kwarg,
    so a watchdog thread interrupts the solver; None means interrupted (TIMEOUT)."""
    sol = Solver(name="cadical153", bootstrap_with=clauses)
    timer = threading.Timer(max(1.0, cap), sol.interrupt)
    timer.start()
    try:
        v = sol.solve_limited(expect_interrupt=True)
        m = sol.get_model() if v else None
    finally:
        timer.cancel(); sol.delete()
    return v, m

CHK = os.path.join(HERE, "certs/experiment_diseq.json")
rec = {"preregistration": "EXPERIMENT-disequality.md", "stages": {}}
def save(**kw):
    rec["stages"].update(kw); rec["elapsed"] = round(time.time()-T0, 2)
    json.dump(rec, open(CHK, "w"), indent=1)
def left():
    return DEADLINE - (time.time()-T0)

F = Field([3, 5, 11])
pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n = len(pts); adj = [set() for _ in range(n)]
for a, b in es:
    adj[a].add(b); adj[b].add(a)
rec.update(n=n, m=len(es), nonadjacent_pairs=149906)
save(stage="load", t=round(time.time()-T0, 2))

# ---- step 1: one 5-colouring of G -------------------------------------
nv, cl = cnf(adj, 5)
ok, model = solve_capped(cl, max(5, min(28, left()-25)))
if ok is None or not ok:
    save(stage="colour5", verdict="TIMEOUT_OR_FAIL", t=round(time.time()-T0, 2))
    print("colouring stage did not return SAT within budget -> INCONCLUSIVE"); print(json.dumps(rec["stages"])); raise SystemExit(0)
c = [None]*n
for v in range(n):
    for kk in range(5):
        if (v*5+kk+1) in set(model):
            c[v] = kk; break
save(stage="colour5", verdict="SAT", t=round(time.time()-T0, 2))

# ---- step 2: independent verification of the colouring ----------------
okc, msg = verify_colouring(adj, c, 5)
rec["colouring_G"] = c; rec["colouring_G_verified"] = bool(okc)
save(stage="verify_colour5", verified=bool(okc), msg=msg, t=round(time.time()-T0, 2))
if not okc:
    print("INVALID_WITNESS:", msg); raise SystemExit(0)

# ---- step 3: candidates = non-adjacent pairs already equal ------------
eq_pairs = 0
best = None
for i in range(n):
    for j in range(i+1, n):
        if j in adj[i] or c[i] != c[j]:
            continue
        eq_pairs += 1
        cn = len(adj[i] & adj[j])
        key = (-cn, i, j)
        if best is None or key < best[0]:
            best = (key, i, j, cn)
_, pi, pj, cn = best
print(f"[select] equal-colour non-adjacent pairs: {eq_pairs} of 149906")
print(f"[select] chosen pair ({pi},{pj}) common neighbours={cn} colours=({c[pi]},{c[pj]})")

def sd(i, j):
    dx = F.sub(pts[i][0], pts[j][0]); dy = F.sub(pts[i][1], pts[j][1])
    return F.add(F.mul(dx, dx), F.mul(dy, dy))
d2 = sd(pi, pj)
isunit = F.is_zero(F.sub(d2, F.one))
rec["pair"] = {"i": pi, "j": pj, "coords_i": [str(x) for x in pts[pi]], "coords_j": [str(x) for x in pts[pj]],
               "d2_basis_coeffs": [str(x) for x in d2], "d2_is_1": bool(isunit),
               "common_neighbours": cn, "colours_in_witness": [c[pi], c[pj]]}
save(stage="select", equal_colour_pairs=eq_pairs, pair=rec["pair"], t=round(time.time()-T0, 2))

# ---- step 4: decide G + pq at k = 5 ----------------------------------
adj2 = [set(x) for x in adj]; adj2[pi].add(pj); adj2[pj].add(pi)
nv2, cl2 = cnf(adj2, 5)
tl = max(4, min(30, left()-6))
v2, m2 = solve_capped(cl2, tl)
if v2 is None:
    rec["verdict"] = "TIMEOUT"; save(stage="decide_GPlusPQ", verdict="TIMEOUT", time_limit=tl, t=round(time.time()-T0, 2))
elif v2:
    c2 = [None]*n
    ms = set(m2)
    for v in range(n):
        for kk in range(5):
            if (v*5+kk+1) in ms:
                c2[v] = kk; break
    ok2, msg2 = verify_colouring(adj2, c2, 5)
    rec["verdict"] = "SAT"; rec["colouring_Gpq"] = c2; rec["colouring_Gpq_verified"] = bool(ok2)
    rec["c_p_neq_c_q"] = bool(c2[pi] != c2[pj])
    save(stage="decide_GPlusPQ", verdict="SAT", verified=bool(ok2), msg=msg2, t=round(time.time()-T0, 2))
    print(f"[decide] SAT; independent check of the G+pq colouring: {ok2} ({msg}); c(p)!=c(q): {c2[pi]!=c2[pj]}")
else:
    rec["verdict"] = "UNSAT_NO_CERT"
    save(stage="decide_GPlusPQ", verdict="UNSAT", certificate=None,
         note="solver-reported only; no DRAT certificate attempted inside the 60 s budget", t=round(time.time()-T0, 2))
    print("[decide] UNSAT (solver-reported only, no certificate)")
print(json.dumps({k: rec[k] for k in ("verdict","elapsed") if k in rec}, indent=1))
