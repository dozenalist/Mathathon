"""H union (H + tau), H = frozen Heule553, tau = (3/2, sqrt3/2).  ONE process, <=60 s total.

Exact field Q(sqrt3,sqrt5,sqrt11) throughout.  Floats are used ONLY to nominate candidate
pairs (a generous band around distance 1); every edge decision is an exact field identity.
Correctness of the prefilter is checked against all 2722 known H-edges.
"""
import json, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 58.0
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import cKDTree
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf
from pysat.solvers import Solver

OUT = os.path.join(HERE, "certs/union_tau.json")
rec = {"construction": "H union (H + tau)", "tau": "(3/2, sqrt3/2)", "field": "Q(sqrt3,sqrt5,sqrt11)"}
def save(**kw):
    rec.update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(OUT, "w"), indent=1)
def left(): return DEADLINE - (time.time() - T0)
def stage(msg, **kw):
    save(**kw); print(f"[{time.time()-T0:6.2f}s] {msg}", flush=True)

F = Field([3, 5, 11])
pts0 = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
E0 = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n0 = len(pts0)
basis = F.basis
w = np.array([np.sqrt(float(b)) for b in basis])          # float value of each basis element
def to_float(pt):
    return np.array([sum(float(c) * w[i] for i, c in enumerate(comp)) for comp in pt])
P0 = np.array([to_float(p) for p in pts0])
stage(f"loaded H: {n0} points, {len(E0)} edges", stage="load", n0=n0, m0=len(E0))

# sanity of the float pipeline against the known unit edges of H
err = max(abs(float(np.sum((P0[a]-P0[b])**2)) - 1.0) for a, b in E0)
assert err < 1e-9, err
BAND = 1e-6
stage(f"float sanity: max |d^2-1| over the 2722 known unit edges = {err:.2e} (band {BAND:g})",
      float_max_err_known_unit_edges=err, band=BAND)

# ---- build H + tau, exact dedup ---------------------------------------------
xt = [Fr(3, 2)] + [Fr(0)]*(len(basis)-1)                  # 3/2
yt = [Fr(0)]*(len(basis)); yt[basis.index(3)] = Fr(1, 2)  # sqrt3/2
xt, yt = tuple(xt), tuple(yt)
tau = (xt, yt)
assert F.is_zero(F.sub(F.add(F.mul(xt, xt), F.mul(yt, yt)), F.rat(3))), "|tau|^2 != 3"

pts = list(pts0) + [(F.add(p[0], xt), F.add(p[1], yt)) for p in pts0]
index = {}
keep = []
for i, p in enumerate(pts):
    key = (p[0], p[1])
    if key in index:
        continue
    index[key] = len(keep); keep.append(p)
n = len(keep)
rec["pre_dedup"] = len(pts); rec["n_after_dedup"] = n
rec["overlap_size"] = len(pts) - n
stage(f"built union: {len(pts)} points -> {n} after exact dedup (overlap {len(pts)-n})",
      stage="build", pre_dedup=len(pts))

# per-point provenance: is it an image of H (A) and/or of H+tau (B)?
lab = [set() for _ in range(n)]
for i in range(len(pts)):
    lab[index[(pts[i][0], pts[i][1])]].add("A" if i < n0 else "B")
A_only = [v for v in range(n) if lab[v] == {"A"}]
B_only = [v for v in range(n) if lab[v] == {"B"}]
bothv = [v for v in range(n) if lab[v] == {"A", "B"}]
stage(f"provenance: A-only {len(A_only)}, B-only {len(B_only)}, shared {len(bothv)}", stage="prov")

# ---- candidate edges by prefilter, then EXACT decision ----------------------
Pf = np.array([to_float(p) for p in keep])
tree = cKDTree(Pf)
cand = sorted(tree.query_pairs(r=1.0 + BAND))
stage(f"prefilter nominated {len(cand)} pairs within the band", stage="prefilter", candidates=len(cand))

def sqd(i, j):
    dx = F.sub(keep[i][0], keep[j][0]); dy = F.sub(keep[i][1], keep[j][1])
    return F.add(F.mul(dx, dx), F.mul(dy, dy))
one = F.one
edges = []; rejected = 0
for (i, j) in cand:
    if F.is_zero(F.sub(sqd(i, j), one)):
        edges.append((i, j))
    else:
        rejected += 1
stage(f"exact decision: {len(edges)} unit edges, {rejected} candidate pairs rejected", stage="edges")

adj = [set() for _ in range(n)]
for a, b in edges:
    adj[a].add(b); adj[b].add(a)
Eset = set(edges)
# every known H edge must be recovered  (prefilter completeness check)
imap = {index[(pts0[v][0], pts0[v][1])]: v for v in range(n0)}
missed = [e for e in E0 if tuple(sorted((imap[e[0]], imap[e[1]]))) not in Eset]
stage(f"prefilter completeness: known H edges missed = {len(missed)}", stage="completeness", missed=len(missed))
assert not missed

# classify: new edges = in the union but in neither copy's internal edge set
EB = set()
for (a, b) in E0:
    ka = (F.add(pts0[a][0], xt), F.add(pts0[a][1], yt)); kb = (F.add(pts0[b][0], xt), F.add(pts0[b][1], yt))
    EB.add(tuple(sorted((index[ka], index[kb]))))
EA = {tuple(sorted((imap[a], imap[b]))) for a, b in E0}
new_edges = [e for e in edges if e not in EA and e not in EB]
rec.update(n=n, m=len(edges), new_edges=len(new_edges), EA=len(EA), EB=len(EB))
stage(f"edges: internal A {len(EA)}, internal B {len(EB)}, NEW cross edges {len(new_edges)}",
      stage="classify")

# is the overlap a clique?
overlap_is_clique = all(b in adj[a] for a, b in
                        ((bothv[i], bothv[j]) for i in range(len(bothv)) for j in range(i+1, len(bothv))))
rec["overlap_is_clique"] = overlap_is_clique
rec["theoremA_hypothesis_holds"] = (len(new_edges) == 0 and overlap_is_clique)
stage(f"overlap clique? {overlap_is_clique}; Theorem A applies (clique-sum)? {rec['theoremA_hypothesis_holds']}",
      stage="theoremA")

# ---- 5-colourability -------------------------------------------------------
save(edges=edges, adj_degrees=None)          # checkpoint the construction before any solver call
nv, cl = cnf(adj, 5)
cap = max(3.0, min(32.0, left() - 8))
sol = Solver(name="cadical153", bootstrap_with=cl)
tm = threading.Timer(cap, sol.interrupt); tm.start()
try:
    st = sol.solve_limited(expect_interrupt=True); model = sol.get_model() if st else None
finally:
    tm.cancel(); sol.delete()

if st is None:
    rec["verdict"] = "TIMEOUT_INCONCLUSIVE"
    stage("solver TIMEOUT -> inconclusive", stage="solver"); sys.exit(0)
if st:
    c5 = [next(kk for kk in range(5) if (v*5+kk+1) in set(model)) for v in range(n)]
    bad = sum(1 for a, b in edges if c5[a] == c5[b])
    rec.update(verdict="SAT_5COLOURABLE", witness=c5, monochromatic_edges=bad)
    stage(f"5-colouring found; independent re-check: {bad} monochromatic of {len(edges)} edges",
          stage="solver")
    # verify H's restriction independently
    hbad = sum(1 for a, b in E0 if c5[imap[a]] == c5[imap[b]])
    rec["h_restriction_monochromatic"] = hbad
    stage(f"restriction to H: {hbad} monochromatic (must be 0)", stage="verify_H")
else:
    cnfp = os.path.join(HERE, "certs/union_tau_k5.cnf")
    with open(cnfp, "w") as g:
        g.write(f"p cnf {nv} {len(cl)}\n")
        for x in cl:
            g.write(" ".join(map(str, x)) + " 0\n")
    rec.update(verdict="UNSAT_CANDIDATE_ONLY", cnf=os.path.basename(cnfp),
               note="candidate only: needs exact geometry re-check plus an independently validated proof certificate")
    stage("5-UNSAT returned -> CANDIDATE ONLY, saved CNF", stage="solver")
save()
print(f"[done] {time.time()-T0:.2f}s -> {OUT}")
