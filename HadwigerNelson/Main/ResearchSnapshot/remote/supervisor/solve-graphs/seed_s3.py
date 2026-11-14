"""SEED S3 = H union (H + u), u = (1/2, sqrt3/2), |u| = 1. ONE process, <=57 s TOTAL.
Exact int64 bilinear form, all pairs, no floating prefilter. See SEED-S3-PREREG.md."""
import json, os, sys, time, threading
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
T0 = time.time(); DEADLINE = 57.0
import numpy as np
from fractions import Fraction as Fr
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf
from pysat.solvers import Solver

OUT = os.path.join(HERE, "certs/seed_s3.json")
rec = {"seed": "S3 = H union (H+u), u=(1/2, sqrt3/2), |u|=1", "prereg": "SEED-S3-PREREG.md",
       "method": "exact int64 bilinear form over ALL pairs, no floating prefilter"}
def save(**kw):
    rec.update(kw); rec["elapsed"] = round(time.time() - T0, 2)
    json.dump(rec, open(OUT, "w"), indent=1)
def left(): return DEADLINE - (time.time() - T0)

F = Field([3, 5, 11]); basis = F.basis; T = len(basis)
pts0 = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
E0 = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n0 = len(pts0)
i3 = basis.index(3)
ux = tuple([Fr(1, 2)] + [Fr(0)] * (T - 1))          # 1/2
uy = tuple([Fr(0)] * T); uy = list(uy); uy[i3] = Fr(1, 2); uy = tuple(uy)   # sqrt3/2
assert F.is_zero(F.sub(F.add(F.mul(ux, ux), F.mul(uy, uy)), F.rat(1))), "|u| != 1"
print("[1] |u|^2 == 1 exactly (verified in field)", flush=True)

raw = [(p, "A", i) for i, p in enumerate(pts0)]
for i, p in enumerate(pts0):
    raw.append(((F.add(p[0], ux), F.add(p[1], uy)), "B", i))
def lcm(a, b):
    x, y = a, b
    while y: x, y = y, x % y
    return a // x * b
den = 1
for p in pts0:
    for comp in p:
        for c in comp: den = lcm(den, c.denominator)
rec["denominator_lcm"] = den
key = {}; keep = []; prov = []; src = []
for p, tag, i in raw:
    k = (p[0], p[1])
    if k in key: prov[key[k]] += "+" + tag; src[key[k]].append(i)
    else: key[k] = len(keep); keep.append(p); prov.append(tag); src.append([i])
N = len(keep)
overlap = len(raw) - N
print(f"[2] raw {len(raw)} -> {N} distinct; overlap {overlap}; den lcm {den}", flush=True)

X = np.zeros((N, T), dtype=np.int64); Y = np.zeros((N, T), dtype=np.int64)
for i, p in enumerate(keep):
    for j in range(T):
        X[i, j] = p[0][j] * den; Y[i, j] = p[1][j] * den
maxX = int(max(np.abs(X).max(), np.abs(Y).max()))
tab = [[F.table[(p, q)] for q in range(T)] for p in range(T)]
maxk = max(tab[p][q][0] for p in range(T) for q in range(T))
bound = 4 * (T * T) * (maxX * maxX) * maxk       # |D| <= 4 * 64 * maxX^2 * maxk
rec.update(n=N, overlap=overlap, max_abs_scaled_coord=maxX, max_k=maxk,
           overflow_bound_absD=bound, two_pow_62=2**62)
print(f"[3] overflow bound: |D| <= {bound:.3e} < 2^62 = {2**62:.3e} : {bound < 2**62}", flush=True)
assert bound < 2**62, "overflow bound exceeds int64 safety"

SS = den * den
mask = np.ones((N, N), dtype=bool)
maxG = 0
for m in range(T):
    A = np.zeros((T, T), dtype=np.int64)
    for p in range(T):
        for q in range(T):
            k, mm = tab[p][q]
            if mm == m: A[p, q] = k
    G = X @ A @ X.T + Y @ A @ Y.T
    maxG = max(maxG, int(np.abs(G).max()))
    d = np.diag(G).copy()
    D = d[:, None] + d[None, :] - 2 * G
    mask &= (D == (SS if m == 0 else 0))
    del G, D
rec["measured_max_abs_G"] = maxG
assert maxG < 2**62
u_, v_ = np.nonzero(np.triu(mask, 1))
E = sorted(zip(u_.tolist(), v_.tolist()))
print(f"[4] all {N*(N-1)//2} pairs exact -> {len(E)} induced edges ({time.time()-T0:.2f}s)", flush=True)
rec.update(m=len(E), pairs_checked=N*(N-1)//2)
save(stage="edges", edges=E)

def sqd(i, j):
    dx = F.sub(keep[i][0], keep[j][0]); dy = F.sub(keep[i][1], keep[j][1])
    return F.add(F.mul(dx, dx), F.mul(dy, dy))
badf = [e for e in E if not F.is_zero(F.sub(sqd(*e), F.one))]
print(f"[5] Field re-check of all {len(E)} edges: {len(badf)} failures", flush=True)
rec["field_recheck_failures"] = len(badf); assert not badf, badf[:5]

imap = {i: key[(pts0[i][0], pts0[i][1])] for i in range(n0)}
Hset = {tuple(sorted((imap[a], imap[b]))) for a, b in E0}
claimed = set(E)
miss = [e for e in Hset if e not in claimed]
Hidx = {imap[i] for i in range(n0)}
extraH = [(i, j) for (i, j) in E if i in Hidx and j in Hidx and (i, j) not in Hset]
print(f"[5] frozen H-edges missed {len(miss)}, extra inside H {len(extraH)}", flush=True)
rec["H_edges_missed"] = len(miss); rec["H_extra_edges"] = len(extraH)
assert not miss and not extraH

# ---- provenance classification: genuine A<->B only (no shared points counted) ----
def cls(i):
    p = prov[i]
    return "AB" if "+" in p else p
cat = {"AA": 0, "BB": 0, "cross": 0, "touch_overlap": 0}
cross_edges = []
for (i, j) in E:
    a, b = cls(i), cls(j)
    if a == "A" and b == "A": cat["AA"] += 1
    elif a == "B" and b == "B": cat["BB"] += 1
    elif (a == "A" and b == "B") or (a == "B" and b == "A"):
        cat["cross"] += 1; cross_edges.append((i, j))
    else: cat["touch_overlap"] += 1
print(f"[6] categories {cat} (sum {sum(cat.values())} = |E| {len(E)})", flush=True)
# intended-interaction identity: (w, w+u) is a unit edge for every non-coinciding w
prop_ok = 0; prop_missing = []
for w in range(n0):
    a = imap[w]; b = key[(F.add(pts0[w][0], ux), F.add(pts0[w][1], uy))]
    if a == b: continue
    pr = tuple(sorted((a, b)))
    if pr in claimed: prop_ok += 1
    else: prop_missing.append(pr)
print(f"[6] intended pairs (w,w+u): {prop_ok} present, {len(prop_missing)} missing; bound was >= {n0-overlap}", flush=True)
rec.update(categories=cat, genuine_cross_edges=cat["cross"], intended_pairs_present=prop_ok,
           intended_pairs_missing=len(prop_missing), overlap_mapping=[(imap[w],
           key[(F.add(pts0[w][0], ux), F.add(pts0[w][1], uy))]) for w in range(n0)
           if imap[w] == key[(F.add(pts0[w][0], ux), F.add(pts0[w][1], uy))]])
save(stage="validated")

if cat["cross"] == 0:
    rec["verdict"] = "STRUCTURALLY INERT (0 genuine cross edges) - stopped, no solver run"
    save(stage="gate"); print("[gate] INERT: 0 genuine cross edges; stopping without solving", flush=True)
else:
    adj = [set() for _ in range(N)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    nv, cl = cnf(adj, 5)
    cap = max(3.0, min(22.0, left() - 5))
    sol = Solver(name="cadical153", bootstrap_with=cl)
    tm = threading.Timer(cap, sol.interrupt); tm.start()
    try: st = sol.solve_limited(expect_interrupt=True); model = sol.get_model() if st else None
    finally: tm.cancel(); sol.delete()
    if st is None:
        rec["verdict"] = "TIMEOUT_INCONCLUSIVE (structure recorded)"
    elif st:
        c = [next(kk for kk in range(5) if (x * 5 + kk + 1) in set(model)) for x in range(N)]
        bad = sum(1 for a, b in E if c[a] == c[b])
        rec.update(verdict="SAT_5COLOURABLE", witness=c, monochromatic=bad)
        print(f"[7] 5-colouring found; all-edge check monochromatic = {bad}", flush=True)
    else:
        p = os.path.join(HERE, "certs/seed_s3_k5.cnf")
        with open(p, "w") as g:
            g.write(f"p cnf {nv} {len(cl)}\n")
            for x in cl: g.write(" ".join(map(str, x)) + " 0\n")
        rec.update(verdict="UNSAT_CANDIDATE_ONLY", cnf=os.path.basename(p))
        print("[7] UNSAT -> CANDIDATE ONLY, CNF saved", flush=True)

with open(os.path.join(HERE, "certs/seed_s3_points.txt"), "w") as g:
    g.write("# idx provenance sources x_coeffs y_coeffs (basis 1,3,5,11,15,33,55,165)\n")
    for i, p in enumerate(keep):
        g.write(f"{i} {prov[i]} {','.join(map(str,src[i]))} " + ",".join(str(x) for x in p[0]) +
                " " + ",".join(str(x) for x in p[1]) + "\n")
with open(os.path.join(HERE, "certs/seed_s3_edges.txt"), "w") as g:
    g.write("# u v\n")
    for a, b in E: g.write(f"{a} {b}\n")
if rec.get("witness"):
    with open(os.path.join(HERE, "certs/seed_s3_witness.txt"), "w") as g:
        g.write("# vertex colour\n")
        for i, x in enumerate(rec["witness"]): g.write(f"{i} {x}\n")
save(stage="done")
print(f"[done] {time.time()-T0:.2f}s -> {OUT}", flush=True)
