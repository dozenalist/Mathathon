"""Step B: the one solver experiment. For each of the 8 pre-registered survivor pairs (list
frozen in certs/prereg_chase_pairs.json BEFORE this ran), require the new witness to split that
pair; verify all 2722 edges; recompute the survivor intersection against ALL witnesses so far.
One process, <=55 s, checkpoint after each pair. No sweep, no subprocess.
"""
import json, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 55.0
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf
from pysat.solvers import Solver

CHK = os.path.join(HERE, "certs/chase_k5.json")
rec = {"prereg": "certs/prereg_chase_pairs.json", "steps": []}
def save(**kw):
    rec.update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(CHK, "w"), indent=1)
def left(): return DEADLINE - (time.time() - T0)

F = Field([3, 5, 11]); pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n = len(pts); E = [(a, b) for a, b in es]
adj = [set() for _ in range(n)]
for a, b in E: adj[a].add(b); adj[b].add(a)

def bad_edges(c):
    return sum(1 for u, v in E if c[u] == c[v])

def same_pairs(c):
    byc = {}
    for v, x in enumerate(c): byc.setdefault(x, []).append(v)
    S = set()
    for grp in byc.values():
        for a in range(len(grp)):
            for b in range(a + 1, len(grp)):
                i, j = grp[a], grp[b]
                if j not in adj[i]: S.add((i, j))
    return S

# --- rebuild baseline from the 10 saved witnesses -------------------------
ens = json.load(open(os.path.join(HERE, "certs/ensemble_k5.json")))
dis = json.load(open(os.path.join(HERE, "certs/experiment_diseq.json")))
W = [w["canonical"] for w in ens["witnesses"]] + [ens["tested_witness"], dis["colouring_Gpq"]]
assert all(bad_edges(c) == 0 for c in W), "a saved witness is invalid"
S = same_pairs(W[0])
for c in W[1:]: S &= same_pairs(c)
base = len(S)
print(f"[baseline] verifed {len(W)} witnesses, survivors {base}")
save(baseline=base, n_witnesses_used=len(W))

prereg = json.load(open(os.path.join(HERE, "certs/prereg_chase_pairs.json")))
nv, base_cl = cnf(adj, 5)
base_cl = [list(x) for x in base_cl]
base_cl.append([1])                                        # c(0)=0  (symmetry breaking)
for v in range(1, n):
    for t in range(1, 5):
        base_cl.append([-(v * 5 + t + 1)] + [u * 5 + (t - 1) + 1 for u in range(v)])

def vmap(model):
    ms = set(model)
    return [next(kk for kk in range(5) if (v * 5 + kk + 1) in ms) for v in range(n)]

unsat = []
for row in prereg["selected"]:
    t, pi, pj = row["t"], row["i"], row["j"]
    if left() < 6:
        save(stopped=f"budget: reached pair {t}"); break
    cl = [list(x) for x in base_cl]
    for kk in range(5):                                    # split: c(p) != c(q)
        cl.append([-(pi * 5 + kk + 1), -(pj * 5 + kk + 1)])
    cap = max(2.0, min(9.0, left() - 4))
    sol = Solver(name="cadical153", bootstrap_with=cl)
    tm = threading.Timer(cap, sol.interrupt); tm.start()
    try:
        st = sol.solve_limited(expect_interrupt=True); m = sol.get_model() if st else None
    finally:
        tm.cancel(); sol.delete()
    step = {"t": t, "pair": [pi, pj], "verdict": None, "seconds": round(time.time() - T0, 2)}
    if st is None:
        step["verdict"] = "TIMEOUT"; rec["steps"].append(step); save(); print(f"  #{t} ({pi},{pj}) TIMEOUT"); break
    if not st:
        # ---- UNSAT: the pair is forced equal at k=5. Save CNF; NOT certified yet.
        step["verdict"] = "UNSAT_UNCERTIFIED"
        cnfp = os.path.join(HERE, f"certs/chase_pair{t}_k5.cnf")
        with open(cnfp, "w") as g:
            g.write(f"p cnf {nv} {len(cl)}\n")
            for c in cl: g.write(" ".join(map(str, c)) + " 0\n")
        step["cnf"] = os.path.basename(cnfp)
        unsat.append(step); rec["steps"].append(step); save(); print(f"  #{t} ({pi},{pj}) UNSAT (uncertified) -> {cnfp}")
        continue
    c = vmap(m)
    ne = bad_edges(c)
    step["monochromatic_edges"] = ne
    step["verified"] = (ne == 0)
    if ne != 0:
        step["verdict"] = "INVALID"; rec["steps"].append(step); save(); print(f"  #{t} INVALID"); break
    step["verdict"] = "SAT"
    step["c_p"], step["c_q"] = c[pi], c[pj]
    step["pair_split"] = bool(c[pi] != c[pj])
    assert c[pi] != c[pj], "witness failed to split the designated pair"
    W.append(c); S &= same_pairs(c)
    step["survivors_after"] = len(S)
    step["eliminated_this_step"] = base - len(S) if len(rec["steps"]) == 0 else prev - len(S)
    prev = len(S)
    rec["steps"].append(step); save(witnesses=W)
    print(f"  #{t} ({pi},{pj}) SAT  verified 0/{len(E)} mono edges | c=({c[pi]},{c[pj]}) | survivors {len(S)} (elim {step['eliminated_this_step']})")

final = len(S) if rec["steps"] else base
rec.update(final_survivors=final, survivors_eliminated=base - final,
           unsat_pairs=[u["pair"] for u in unsat], survivors=sorted(S))
save()
print(f"\n[final] baseline {base} -> survivors {final} (eliminated {base-final}) in {time.time()-T0:.2f}s")
print(f"[final] UNSAT pairs reported (UNCERTIFIED): {[u['pair'] for u in unsat]}")
