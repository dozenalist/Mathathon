"""Continued adaptive k=5 separation on the verified induced graph. ONE process, <=57 s.
See REFINE2-PREREG.md."""
import json, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 56.0
from pysat.solvers import Solver

OUT = os.path.join(HERE, "certs/refine2_k5.json")
rec = {"prereg": "REFINE2-PREREG.md", "k": 5,
       "graph": "verified induced unit-distance graph, 1048 points, 5487 edges",
       "grade": "induced completeness VERIFIED (independent check, all 548628 pairs)", "steps": []}
def save(**kw):
    rec.update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(OUT, "w"), indent=1)
def left(): return DEADLINE - (time.time() - T0)

E = [tuple(int(x) for x in l.split()) for l in open("certs/union_tau_edges.txt") if not l.startswith("#")]
n = 1048
adj = [set() for _ in range(n)]
for u, v in E:
    adj[u].add(v); adj[v].add(u)
prev = json.load(open("certs/refine_union_k5.json"))
W = prev["witnesses"]                      # 17 witnesses
assert len(W) == 17

def mono(c): return sum(1 for u, v in E if c[u] == c[v])
bad = [t for t, c in enumerate(W) if mono(c)]
if bad:
    save(stage="ABORT", why=f"witness {bad} not proper on the reported edges")
    raise SystemExit(0)
print(f"[0] {len(W)} witnesses verified against all {len(E)} edges; n={n}", flush=True)

# provenance of each point (A-only / B-only / A+B) -- needed for the reconciliation
prov = [None] * n
for line in open("certs/union_tau_points.txt"):
    if line.startswith("#"): continue
    f = line.split()
    prov[int(f[0])] = f[1]
print(f"[0] provenance loaded; A-only {prov.count('A')}, B-only {prov.count('B')}, overlap {prov.count('A+B')}", flush=True)

# ---- classes, maintained incrementally (O(n) per witness) --------------------
cls = [0] * n
ncls = 1
for c in W:
    nxt = {}; newid = 0; remap = {}
    for key in range(ncls): pass
    m = {}
    for v in range(n):
        k = (cls[v], c[v])
        if k not in m: m[k] = len(m)
        remap[v] = m[k]
    cls = [remap[v] for v in range(n)]; ncls = len(m)

def survivors_and_classes(cls, ncls):
    grp = {}
    for v in range(n): grp.setdefault(cls[v], []).append(v)
    S = set()
    for g in grp.values():
        L = len(g)
        for a in range(L):
            i = g[a]
            for b in range(a + 1, L):
                j = g[b]
                if j not in adj[i]: S.add((i, j))
    return S, grp

S, grp = survivors_and_classes(cls, ncls)
print(f"[0] baseline survivors recomputed: {len(S)} (recorded {prev['final_survivors']})", flush=True)
# ---- reconciliation 112 vs 177 ---------------------------------------------
both_idx = [p for p in S if p[0] < 553 and p[1] < 553]
both_aonly = [p for p in S if prov[p[0]] == "A" and prov[p[1]] == "A"]
print(f"[0] survivors with BOTH INDICES < 553: {len(both_idx)}  (local count 177)", flush=True)
print(f"[0] survivors with BOTH ENDPOINTS A-only: {len(both_aonly)}  (my earlier 112)", flush=True)
touch_overlap = [p for p in both_idx if prov[p[0]] != "A" or prov[p[1]] != "A"]
print(f"[0] of the {len(both_idx)}: {len(touch_overlap)} have an endpoint in the 58-point overlap", flush=True)
rec.update(baseline_survivors=len(S), both_index_lt553=len(both_idx), both_aonly=len(both_aonly),
           both_idx_touching_overlap=len(touch_overlap))
save(stage="baseline")

# ---- CNF pieces -------------------------------------------------------------
def clauses(extra):
    cl = [[v * 5 + kk + 1 for kk in range(5)] for v in range(n)]
    for u, v in E:
        for kk in range(5):
            cl.append([-(u * 5 + kk + 1), -(v * 5 + kk + 1)])
    return cl + extra

use = [0] * n; tested = set(); MAXP = 200
for step in range(1, MAXP + 1):
    if left() < 3.0:
        rec["stopped"] = "deadline"; save(); print(f"[stop] deadline at step {step}", flush=True); break
    if not S:
        rec["stopped"] = "NO SURVIVORS"; save(); print("[stop] NO SURVIVORS", flush=True); break
    csize = {}
    for g in grp.values():
        for v in g: csize[v] = len(g)
    pick = None
    for (i, j) in S:
        if (i, j) in tested: continue
        key = (-csize[i], use[i] + use[j], i, j)
        if pick is None or key < pick[0]: pick = (key, i, j)
    if pick is None:
        rec["stopped"] = "all current survivors tested"; save(); print("[stop] all tested", flush=True); break
    _, pi, pj = pick
    before = len(S)
    extra = [[-(pi * 5 + kk + 1), -(pj * 5 + kk + 1)] for kk in range(5)]
    cl = clauses(extra)
    cap = max(1.5, min(8.0, left() - 2.0))
    sol = Solver(name="cadical153", bootstrap_with=cl)
    tm = threading.Timer(cap, sol.interrupt); tm.start()
    try:
        st = sol.solve_limited(expect_interrupt=True); m = sol.get_model() if st else None
    finally:
        tm.cancel(); sol.delete()
    tested.add((pi, pj)); use[pi] += 1; use[pj] += 1
    sr = {"step": step, "pair": [pi, pj], "class_size": -pick[0][0], "before": before}
    if st is None:
        sr["verdict"] = "TIMEOUT"; rec["steps"].append(sr); rec["stopped"] = "solver timeout"
        save(); print(f"  {step} ({pi},{pj}) TIMEOUT", flush=True); break
    if not st:
        cnfp = os.path.join(HERE, f"certs/refine2_step{step}_k5.cnf")
        with open(cnfp, "w") as g:
            g.write(f"p cnf {n*5} {len(cl)}\n")
            for x in cl: g.write(" ".join(map(str, x)) + " 0\n")
        sr.update(verdict="UNSAT_CANDIDATE_ONLY", cnf=os.path.basename(cnfp))
        rec["steps"].append(sr); rec["candidate_forced_pair"] = [pi, pj]
        rec["stopped"] = "UNSAT candidate"; save()
        print(f"  {step} ({pi},{pj}) UNSAT -> CANDIDATE ONLY", flush=True); break
    c = [next(kk for kk in range(5) if (v * 5 + kk + 1) in set(m)) for v in range(n)]
    ne = mono(c)
    if ne:
        sr.update(verdict="INVALID", mono=ne); rec["steps"].append(sr); save()
        print(f"  {step} INVALID {ne}", flush=True); break
    assert c[pi] != c[pj]
    W.append(c)
    # incremental refinement of classes
    m2 = {}
    for v in range(n):
        k = (cls[v], c[v])
        if k not in m2: m2[k] = len(m2)
    cls = [m2[(cls[v], c[v])] for v in range(n)]
    S, grp = survivors_and_classes(cls, len(m2))
    sr.update(verdict="SAT", mono=0, after=len(S), removed=before - len(S), c_pair=[c[pi], c[pj]])
    rec["steps"].append(sr); save()
    print(f"  {step} ({pi},{pj}) cls={sr['class_size']} SAT | {before} -> {len(S)} (removed {before-len(S)})", flush=True)

# ---- persist everything -----------------------------------------------------
with open("certs/refine2_witnesses.txt", "w") as g:
    g.write("# one proper 5-colouring per line, 1048 entries, space separated\n")
    for c in W: g.write(" ".join(map(str, c)) + "\n")
with open("certs/refine2_survivors.txt", "w") as g:
    g.write("# i j   exact survivor list\n")
    for (i, j) in sorted(S): g.write(f"{i} {j}\n")
rec.update(final_survivors=len(S), n_witnesses=len(W), n_targets=len(rec["steps"]),
           survivors=sorted(S), tested=sorted(tested))
save()
print(f"\n[done] witnesses {len(W)}, targets {len(rec['steps'])}, survivors {len(S)}, {time.time()-T0:.2f}s", flush=True)
