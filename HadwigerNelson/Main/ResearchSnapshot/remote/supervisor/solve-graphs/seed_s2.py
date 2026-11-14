"""SEED S2 = H union R90(H).  ONE process, <=58 s TOTAL incl. all validation.
Exact int64 bilinear form -> complete induced edge set, NO floating prefilter."""
import json, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 58.0
import numpy as np
from fractions import Fraction as Fr
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf
from pysat.solvers import Solver

OUT = os.path.join(HERE, "certs/seed_s2.json")
rec = {"seed": "S2 = H union R90(H), R90(x,y)=(-y,x)", "prereg": "SEED-S2-PREREG.md",
       "method": "exact int64 bilinear form, all pairs, no floating prefilter"}
def save(**kw):
    rec.update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(OUT, "w"), indent=1)
def left(): return DEADLINE - (time.time() - T0)

F = Field([3, 5, 11]); basis = F.basis
pts0 = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
E0 = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n0 = len(pts0)

# ---- build S2 with provenance ------------------------------------------------
raw = [(p, "A", i) for i, p in enumerate(pts0)]
for i, p in enumerate(pts0):                       # R90(x,y) = (-y, x)
    raw.append(((F.neg(p[1]), p[0]), "B", i))
den = 1
for p in pts0:
    for comp in p:
        for c in comp:
            den = den * c.denominator // np.gcd(den, c.denominator) if False else den
# lcm without numpy on Fractions
def lcm(a, b): 
    x, y = a, b
    while y: x, y = y, x % y
    return a // x * b
den = 1
for p in pts0:
    for comp in p:
        for c in comp: den = lcm(den, c.denominator)
rec["denominator_lcm"] = den
key2idx = {}; keep = []; prov = []; src = []
for p, tag, i in raw:
    k = (p[0], p[1])
    if k in key2idx:
        prov[key2idx[k]] += "|" + tag
    else:
        key2idx[k] = len(keep); keep.append(p); prov.append(tag); src.append(i)
N = len(keep)
print(f"[1] raw {len(raw)} -> {N} distinct points, denominator lcm {den}", flush=True)
rec.update(n= N, pre_dedup=len(raw), overlap=len(raw) - N)
save(stage="built")

# ---- integer coordinates ----------------------------------------------------
T = len(basis)
X = np.zeros((N, T), dtype=np.int64); Y = np.zeros((N, T), dtype=np.int64)
for i, p in enumerate(keep):
    for j in range(T):
        X[i, j] = p[0][j] * den; Y[i, j] = p[1][j] * den
# multiplication table: basis[p]*basis[q] = k * basis[m]
tab = [[F.table[(p, q)] for q in range(T)] for p in range(T)]

# ---- exact bilinear Gram per basis component -> all-pairs d^2 ---------------
SS = den * den
edge_mask = np.ones((N, N), dtype=bool)   # AND across basis components
maxmag = 0
for m in range(T):
    A = np.zeros((T, T), dtype=np.int64)
    for p in range(T):
        for q in range(T):
            k, mm = tab[p][q]
            if mm == m: A[p, q] = k
    G = X @ A @ X.T + Y @ A @ Y.T
    maxmag = max(maxmag, int(np.abs(G).max()))
    d = np.diag(G).copy()
    D = d[:, None] + d[None, :] - 2 * G
    edge_mask &= (D == (SS if m == 0 else 0))
    del G, D
assert maxmag < 2**62, maxmag
rec["gram_max_magnitude"] = maxmag
u, v = np.nonzero(np.triu(edge_mask, 1))
E = sorted(zip(u.tolist(), v.tolist()))
print(f"[2] exact all-pairs done: {N*(N-1)//2} pairs -> {len(E)} edges  ({time.time()-T0:.2f}s)", flush=True)
rec.update(m=len(E), pairs_checked=N*(N-1)//2)
save(stage="edges", edges=E)

# ---- validation 1: every edge re-verified by the independent Field path -----
def sqd(i, j):
    dx = F.sub(keep[i][0], keep[j][0]); dy = F.sub(keep[i][1], keep[j][1])
    return F.add(F.mul(dx, dx), F.mul(dy, dy))
badf = [e for e in E if not F.is_zero(F.sub(sqd(*e), F.one))]
print(f"[3] independent Field re-check of all {len(E)} edges: {len(badf)} failures", flush=True)
rec["field_recheck_failures"] = len(badf)
assert not badf, badf[:5]

# ---- validation 2: the 2722 frozen H-edges reproduced exactly ---------------
imap = {}
for i, p in enumerate(pts0):
    imap[i] = key2idx[(p[0], p[1])]
claimed = set(E)
miss = [e for e in E0 if tuple(sorted((imap[e[0]], imap[e[1]]))) not in claimed]
Hset = {tuple(sorted((imap[a], imap[b]))) for a, b in E0}
Hidx = {imap[i] for i in range(n0)}
extra_in_H = [(i, j) for (i, j) in E if i in Hidx and j in Hidx and (i, j) not in Hset]
print(f"[3] frozen H-edges missed: {len(miss)}; extra edges inside H: {len(extra_in_H)}", flush=True)
rec["H_edges_missed"] = len(miss); rec["H_extra_edges"] = len(extra_in_H)
assert not miss and not extra_in_H

# ---- counts -----------------------------------------------------------------
new_edges = [(i, j) for (i, j) in E
             if not ((prov[i].startswith("A") and prov[j].startswith("A")) or
                     (prov[i].startswith("B") and prov[j].startswith("B")))]
rec["new_edges"] = len(new_edges)
print(f"[4] edges {len(E)} = H-side {len(Hset)} + R90-side + NEW {len(new_edges)}", flush=True)
save(stage="validated")

# ---- 5-colouring ------------------------------------------------------------
adj = [set() for _ in range(N)]
for a, b in E:
    adj[a].add(b); adj[b].add(a)
nv, cl = cnf(adj, 5)
cap = max(3.0, min(25.0, left() - 6))
sol = Solver(name="cadical153", bootstrap_with=cl)
tm = threading.Timer(cap, sol.interrupt); tm.start()
try:
    st = sol.solve_limited(expect_interrupt=True); model = sol.get_model() if st else None
finally:
    tm.cancel(); sol.delete()
if st is None:
    rec["verdict"] = "TIMEOUT_INCONCLUSIVE"; save(stage="solver")
    print("[5] solver timeout -> inconclusive", flush=True)
elif st:
    c = [next(kk for kk in range(5) if (x * 5 + kk + 1) in set(model)) for x in range(N)]
    bad = sum(1 for a, b in E if c[a] == c[b])
    rec.update(verdict="SAT_5COLOURABLE", witness=c, monochromatic=bad)
    save(stage="solver")
    print(f"[5] 5-colouring found; edge-check monochromatic = {bad}", flush=True)
else:
    cnfp = os.path.join(HERE, "certs/seed_s2_k5.cnf")
    with open(cnfp, "w") as g:
        g.write(f"p cnf {nv} {len(cl)}\n")
        for x in cl: g.write(" ".join(map(str, x)) + " 0\n")
    rec.update(verdict="UNSAT_CANDIDATE_ONLY", cnf=os.path.basename(cnfp))
    save(stage="solver"); print("[5] UNSAT -> CANDIDATE ONLY, CNF saved", flush=True)

# ---- persist points / edges -------------------------------------------------
with open(os.path.join(HERE, "certs/seed_s2_points.txt"), "w") as g:
    g.write("# idx provenance src_in_H x_coeffs y_coeffs (basis 1,3,5,11,15,33,55,165)\n")
    for i, p in enumerate(keep):
        g.write(f"{i} {prov[i]} {src[i]} " + ",".join(str(x) for x in p[0]) + " " +
                ",".join(str(x) for x in p[1]) + "\n")
with open(os.path.join(HERE, "certs/seed_s2_edges.txt"), "w") as g:
    g.write("# u v (exact induced unit edges of S2)\n")
    for a, b in E: g.write(f"{a} {b}\n")
if rec.get("witness"):
    with open(os.path.join(HERE, "certs/seed_s2_witness.txt"), "w") as g:
        g.write("# vertex colour (proper 5-colouring)\n")
        for i, x in enumerate(rec["witness"]): g.write(f"{i} {x}\n")
save(stage="done")
print(f"[done] {time.time()-T0:.2f}s -> {OUT}", flush=True)
