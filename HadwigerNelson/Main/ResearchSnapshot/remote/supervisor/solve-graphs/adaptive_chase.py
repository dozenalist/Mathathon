"""Adaptive class-refinement chase (see PREREGISTRATION-adaptive.md).
ONE process, 60 s total, checkpoint per step. No symmetry breaking, no frozen pair list."""
import json, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 57.0
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf
from pysat.solvers import Solver

CHK = os.path.join(HERE, "certs/adaptive_k5.json")
rec = {"prereg": "PREREGISTRATION-adaptive.md", "steps": []}
def save(**kw):
    rec.update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(CHK, "w"), indent=1)
def left(): return DEADLINE - (time.time() - T0)

F = Field([3, 5, 11]); pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n = len(pts); E = [(a, b) for a, b in es]
adj = [set() for _ in range(n)]
for a, b in E: adj[a].add(b); adj[b].add(a)
def mono(c): return sum(1 for u, v in E if c[u] == c[v])

# ---- step 0: load the 18 saved witnesses, verify, reproduce the class structure
# chase_k5.json already accumulates all 18: the 8 ensemble partitions, the (0,39) witness,
# the (0,50) witness and the 8 chase witnesses.  (An earlier loader double-counted and asserted 28.)
W = json.load(open(os.path.join(HERE, "certs/chase_k5.json")))["witnesses"]
assert len(W) == 18, len(W)
assert all(mono(c) == 0 for c in W), "a saved witness fails the edge check"
print(f"[step0] {len(W)} saved witnesses, all verified against {len(E)} edges")

def signatures(Ws):
    return [tuple(c[v] for c in Ws) for v in range(n)]
def survivors(Ws, sig=None):
    if sig is None: sig = signatures(Ws)
    S = set()
    by = {}
    for v, s in enumerate(sig): by.setdefault(s, []).append(v)
    for grp in by.values():
        for a in range(len(grp)):
            for b in range(a + 1, len(grp)):
                i, j = grp[a], grp[b]
                if j not in adj[i]: S.add((i, j))
    return S, by

S, by = survivors(W)
sizes = sorted((len(g) for g in by.values() if len(g) > 1), reverse=True)
print(f"[step0] survivors {len(S)}  nontrivial classes {len(sizes)}  sizes {sizes}")
print(f"[step0] sum C(m,2) = {sum(len(g)*(len(g)-1)//2 for g in by.values())}")
rec.update(baseline=len(S), class_sizes=sizes,
           verified_witnesses=len(W), sum_choose2=sum(len(g)*(len(g)-1)//2 for g in by.values()))
save()
assert sum(len(g)*(len(g)-1)//2 for g in by.values()) == len(S) == 491

# ---- adaptive chase
nv, base_cl = cnf(adj, 5)
use = [0] * n
tested = set()
def vmap(m):
    ms = set(m); return [next(kk for kk in range(5) if (v*5+kk+1) in ms) for v in range(n)]

MAXP = 16
for step in range(1, MAXP + 1):
    if left() < 5: save(stopped="budget"); print("stopped on budget"); break
    S, by = survivors(W)
    if not S: save(stopped="survivors empty"); print("SURVIVORS EMPTY"); break
    cls_of = {}
    for s, grp in by.items():
        for v in grp: cls_of[v] = len(grp)
    cand = [(cls_of[i], -use[i]-use[j], i, j) for (i, j) in S if (i, j) not in tested]
    if not cand:
        save(stopped="all current survivors already tested"); print("all tested"); break
    key = min((-cl, u, i, j) for (cl, u, i, j) in cand)
    _, _, pi, pj = key
    clsz = cls_of[pi]
    before = len(S)
    cl = [list(x) for x in base_cl]
    for kk in range(5):
        cl.append([-(pi*5+kk+1), -(pj*5+kk+1)])          # combinatorial disequality: c(p) != c(q)
    cap = max(2.0, min(8.0, left() - 3))
    sol = Solver(name="cadical153", bootstrap_with=cl)
    tm = threading.Timer(cap, sol.interrupt); tm.start()
    try:
        st = sol.solve_limited(expect_interrupt=True); m = sol.get_model() if st else None
    finally:
        tm.cancel(); sol.delete()
    tested.add((pi, pj)); use[pi] += 1; use[pj] += 1
    st_rec = {"step": step, "pair": [pi, pj], "class_size": clsz, "survivors_before": before}
    if st is None:
        st_rec["verdict"] = "TIMEOUT"; rec["steps"].append(st_rec); save(); print(f"  {step} ({pi},{pj}) TIMEOUT"); break
    if not st:
        cf = os.path.join(HERE, f"certs/adaptive_step{step}_k5.cnf")
        with open(cf, "w") as g:
            g.write(f"p cnf {nv} {len(cl)}\n")
            for x in cl: g.write(" ".join(map(str, x)) + " 0\n")
        st_rec.update(verdict="UNSAT_SOLVER_ONLY", cnf=os.path.basename(cf))
        rec["steps"].append(st_rec); save(); print(f"  {step} ({pi},{pj}) UNSAT (solver-only) -> {cf}"); break
    c = vmap(m); ne = mono(c)
    if ne:
        st_rec.update(verdict="INVALID", mono=ne); rec["steps"].append(st_rec); save(); print(f"  {step} INVALID"); break
    assert c[pi] != c[pj]
    W.append(c)
    S2, _ = survivors(W)
    st_rec.update(verdict="SAT", mono=ne, c= [c[pi], c[pj]], survivors_after=len(S2),
                  removed=before - len(S2))
    rec["steps"].append(st_rec); save(witnesses=W)
    print(f"  {step} ({pi},{pj}) class={clsz} SAT | survivors {before} -> {len(S2)} (removed {before-len(S2)})")

S, by = survivors(W)
sizes = sorted((len(g) for g in by.values() if len(g) > 1), reverse=True)
rec.update(final_survivors=len(S), final_class_sizes=sizes, survivors=sorted(S),
           n_witnesses=len(W), tested_pairs=sorted(tested))
save()
print(f"\n[final] survivors {rec['baseline']} -> {len(S)}; classes now {len(sizes)} {sizes}; {time.time()-T0:.2f}s")
