"""The block's single experiment (see PREREGISTRATION-ensemble.md). One process, 58 s cap."""
import sys, os, time, json, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 58.0
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf
from pysat.solvers import Solver

CHK = os.path.join(HERE, "certs/ensemble_k5.json")
rec = {"prereg": "PREREGISTRATION-ensemble.md", "witnesses": [], "stages": {}}
def save(**kw):
    rec["stages"].update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(CHK, "w"), indent=1)
def left(): return DEADLINE - (time.time() - T0)

F = Field([3, 5, 11])
pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n = len(pts); E = [(a, b) for a, b in es]
adj = [set() for _ in range(n)]
for a, b in E:
    adj[a].add(b); adj[b].add(a)
rec.update(n=n, m=len(E), nonadjacent_pairs=149906)
save(stage="load", t=round(time.time() - T0, 2))

def only_edges(c):
    """independent check: no monochromatic edge, using the .edge list directly."""
    for u, v in E:
        if c[u] == c[v]:
            return False, (u, v)
    return True, None

def canonical(c, k=5):
    remap, out = {}, []
    for x in c:
        if x not in remap: remap[x] = len(remap)
        out.append(remap[x])
    assert len(remap) == k, f"used {len(remap)} colours"
    return out

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

nv, base = cnf(adj, 5)
clauses = [list(x) for x in base]
# first-occurrence symmetry breaking: each PARTITION gets exactly one admissible assignment,
# so blocking an assignment blocks the partition (block-1 on partition blocking).
clauses.append([1])                                   # vertex 0 has colour 0
for v in range(1, n):
    for t in range(1, 5):
        clauses.append([-(v * 5 + t + 1)] + [u * 5 + (t - 1) + 1 for u in range(v)])
parts = []           # canonical vectors
pair_sets = []
MAXW = 8
for w in range(MAXW):
    cap = max(2.0, min(12.0, left() - 8))
    sol = Solver(name="cadical153", bootstrap_with=clauses)
    tm = threading.Timer(cap, sol.interrupt); tm.start()
    try:
        st = sol.solve_limited(expect_interrupt=True); model = sol.get_model() if st else None
    finally:
        tm.cancel(); sol.delete()
    if st is None:
        save(stage="ensemble", stopped=f"TIMEOUT at witness {w}"); break
    if not st:
        save(stage="ensemble", stopped=f"UNSAT: only {w} partitions exist"); break
    ms = set(model)
    c = [next(kk for kk in range(5) if (v * 5 + kk + 1) in ms) for v in range(n)]
    ok, bad = only_edges(c)
    if not ok:
        save(stage="ensemble", stopped=f"INVALID witness {w} edge {bad}"); break
    cc = canonical(c)
    if cc in parts:
        save(stage="ensemble", stopped=f"DUPLICATE partition at {w} (canonicalisation failed)"); break
    parts.append(cc); pair_sets.append(same_pairs(cc))
    rec["witnesses"].append({"index": w, "canonical": cc, "verified_edges": len(E),
                             "same_colour_nonadjacent": len(pair_sets[-1])})
    clauses.append([-(v * 5 + cc[v] + 1) for v in range(n)])   # block THIS partition exactly
    save(stage="ensemble_witness", w=w, n_same=len(pair_sets[-1]), t=round(time.time() - T0, 2))

rec["n_distinct_partitions"] = len(parts)
print(f"[ensemble] distinct verified partitions: {len(parts)}  t={time.time()-T0:.2f}s")
for i, S in enumerate(pair_sets):
    print(f"  witness {i}: verified {len(E)} edges, {len(S)} same-colour non-adjacent pairs")

surv = set(pair_sets[0])
for S in pair_sets[1:]:
    surv &= S
rec["survivors"] = sorted(surv); rec["n_survivors"] = len(surv)
print(f"[intersection] survivors after {len(pair_sets)} witnesses: {len(surv)}")

# eliminated list: pair -> first witness index separating it
elim = {}
first = pair_sets[0]
for pr in first:
    if pr in surv: continue
    for idx in range(1, len(pair_sets)):
        if pr not in pair_sets[idx]:
            elim[pr] = idx; break
with open(os.path.join(HERE, "certs/ensemble_eliminated.txt"), "w") as g:
    g.write("# i j witness_index_that_separates\n")
    for (i, j), k in sorted(elim.items()):
        g.write(f"{i} {j} {k}\n")
print(f"[eliminated] {len(elim)} pairs eliminated, saved to certs/ensemble_eliminated.txt")

verdict = None
EXCLUDED = {(0, 39)}
if surv:
    best = None
    for (i, j) in surv:
        if (i, j) in EXCLUDED or (j, i) in EXCLUDED:
            continue
        key = (-len(adj[i] & adj[j]), i, j)
        if best is None or key < best[0]: best = (key, i, j)
    if best is None:
        rec["tested_pair_verdict"] = "only survivor was the excluded pair (0,39)"
        save(stage="done", verdict="NO_TESTABLE_SURVIVOR", t=round(time.time() - T0, 2))
        print("[test] only survivor is the excluded pair; nothing tested"); raise SystemExit(0)
    _, pi, pj = best
    rec["tested_pair"] = [pi, pj]
    adj2 = [set(x) for x in adj]; adj2[pi].add(pj); adj2[pj].add(pi)
    nv2, cl2 = cnf(adj2, 5)
    cap = max(2.0, min(20.0, left() - 3))
    sol = Solver(name="cadical153", bootstrap_with=cl2)
    tm = threading.Timer(cap, sol.interrupt); tm.start()
    try:
        st2 = sol.solve_limited(expect_interrupt=True); m2 = sol.get_model() if st2 else None
    finally:
        tm.cancel(); sol.delete()
    if st2 is None:
        verdict = "TIMEOUT"
    elif st2:
        ms2 = set(m2)
        c2 = [next(kk for kk in range(5) if (v * 5 + kk + 1) in ms2) for v in range(n)]
        ok2, bad2 = only_edges(c2)
        verdict = "SAT" if ok2 else "INVALID"
        rec.update(tested_pair_verdict=verdict, tested_witness=c2,
                   c_p=c2[pi], c_q=c2[pj], differ=bool(c2[pi] != c2[pj]))
    else:
        verdict = "UNSAT_NO_CERT"
    rec["tested_pair_verdict"] = verdict
    print(f"[test] pair ({pi},{pj}) verdict {verdict}")
else:
    verdict = "NO_SURVIVORS"
    rec["tested_pair_verdict"] = "not needed (zero survivors)"
rec["verdict"] = verdict
save(stage="done", verdict=verdict, t=round(time.time() - T0, 2))
print(f"[done] verdict={verdict} total {time.time()-T0:.2f}s")
