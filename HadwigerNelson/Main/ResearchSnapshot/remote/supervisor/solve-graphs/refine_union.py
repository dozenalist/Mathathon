"""Adaptive equal-signature refinement at k=5 on G_rep (see REFINE-PREREG.md).
ONE process, <=58 s, checkpoint per step. Frozen initial witness is never modified."""
import json, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 56.0
from pysat.solvers import Solver

OUT = os.path.join(HERE, "certs/refine_union_k5.json")
rec = {"prereg": "REFINE-PREREG.md", "graph": "G_rep: 1048 points, 5487 reported edges",
       "k": 5, "grades": {"edges_exact": "verified", "induced_completeness": "PENDING"},
       "steps": []}
def save(**kw):
    rec.update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(OUT, "w"), indent=1)
def left(): return DEADLINE - (time.time() - T0)

E = [tuple(int(x) for x in l.split()) for l in open(os.path.join(HERE, "certs/union_tau_edges.txt"))
     if not l.startswith("#")]
W0 = [int(l.split()[1]) for l in open(os.path.join(HERE, "certs/union_tau_witness.txt"))
      if not l.startswith("#")]
n = max(max(u, v) for u, v in E) + 1
assert len(W0) == n == 1048, (len(W0), n)
adj = [set() for _ in range(n)]
for u, v in E:
    adj[u].add(v); adj[v].add(u)
def mono(c): return sum(1 for u, v in E if c[u] == c[v])
assert mono(W0) == 0, "frozen initial witness is not proper on the reported edges"
print(f"[0] G_rep n={n} m={len(E)}; frozen witness verified (0 mono)", flush=True)

def same_pairs(c):
    by = {}
    for v, x in enumerate(c): by.setdefault(x, []).append(v)
    S = set()
    for grp in by.values():
        L = len(grp)
        for a in range(L):
            i = grp[a]
            for b in range(a + 1, L):
                j = grp[b]
                if j not in adj[i]: S.add((i, j))
    return S

W = [W0]
S = same_pairs(W0)
rec.update(baseline_survivors=len(S), n_witnesses=1)
save(stage="baseline")
print(f"[0] baseline survivors (one witness): {len(S)}", flush=True)

# CNF: at-least-one + edge constraints
def build_clauses(extra):
    cl = []
    base = 1
    for v in range(n):
        cl.append([base + v * 5 + kk for kk in range(5)])
    for u, v in E:
        for kk in range(5):
            cl.append([-(base + u * 5 + kk), -(base + v * 5 + kk)])
    return cl + extra

use = [0] * n
tested = set()
MAXP = 16
for step in range(1, MAXP + 1):
    if left() < 6:
        rec["stopped"] = "deadline"; save(); print("[stop] deadline", flush=True); break
    if not S:
        rec["stopped"] = "survivors empty"; save(); print("[stop] survivors empty", flush=True); break
    # signatures and classes
    sig = [tuple(c[v] for c in W) for v in range(n)]
    cls = {}
    for v, s in enumerate(sig): cls.setdefault(s, []).append(v)
    csize = {v: len(cls[sig[v]]) for v in range(n)}
    cand = ((-csize[i], use[i] + use[j], i, j) for (i, j) in S if (i, j) not in tested)
    try:
        negcl, us, pi, pj = min(cand)
    except ValueError:
        rec["stopped"] = "no untested survivor"; save(); print("[stop] no untested survivor", flush=True); break
    before = len(S)
    extra = [[-(i * 5 + kk + 1), -(j * 5 + kk + 1)] for i, j in [(pi, pj)] for kk in range(5)]
    cl = build_clauses(extra)
    cap = max(2.0, min(10.0, left() - 4))
    sol = Solver(name="cadical153", bootstrap_with=cl)
    tm = threading.Timer(cap, sol.interrupt); tm.start()
    try:
        st = sol.solve_limited(expect_interrupt=True); m = sol.get_model() if st else None
    finally:
        tm.cancel(); sol.delete()
    tested.add((pi, pj)); use[pi] += 1; use[pj] += 1
    srec = {"step": step, "pair": [pi, pj], "class_size": -negcl, "survivors_before": before}
    if st is None:
        srec["verdict"] = "TIMEOUT"; rec["steps"].append(srec); rec["stopped"] = "solver timeout"; save()
        print(f"  {step} ({pi},{pj}) TIMEOUT", flush=True); break
    if not st:
        cnfp = os.path.join(HERE, f"certs/refine_step{step}_k5.cnf")
        with open(cnfp, "w") as g:
            g.write(f"p cnf {n*5} {len(cl)}\n")
            for x in cl: g.write(" ".join(map(str, x)) + " 0\n")
        srec.update(verdict="UNSAT_CANDIDATE_ONLY", cnf=os.path.basename(cnfp))
        rec["steps"].append(srec); rec["candidate_forced_pair"] = [pi, pj]
        rec["stopped"] = "UNSAT candidate"
        save(); print(f"  {step} ({pi},{pj}) UNSAT -> CANDIDATE ONLY, cnfs saved", flush=True); break
    c = [next(kk for kk in range(5) if (v * 5 + kk + 1) in set(m)) for v in range(n)]
    ne = mono(c)
    if ne:
        srec.update(verdict="INVALID", mono=ne); rec["steps"].append(srec); save()
        print(f"  {step} INVALID {ne}", flush=True); break
    assert c[pi] != c[pj]
    W.append(c); S = S & same_pairs(c)
    srec.update(verdict="SAT", mono=0, survivors_after=len(S), removed=before - len(S),
                c_pair=[c[pi], c[pj]])
    rec["steps"].append(srec); save(witnesses=W, survivors=sorted(S))
    print(f"  {step} ({pi},{pj}) cls={-negcl} SAT | {before} -> {len(S)} (removed {before-len(S)})", flush=True)

rec.update(final_survivors=len(S), n_witnesses=len(W), survivors=sorted(S),
           tested=sorted(tested))
save()
print(f"\n[done] {len(W)} witnesses, survivors {len(S)}, {time.time()-T0:.2f}s", flush=True)
