"""Shard B (declared in REPORT.md section 6): positive control at the 5-chromatic level.

Take Heule's published 553-vertex 5-chromatic unit-distance graph (arXiv:1805.12181,
data: github.com/marijnheule/CNP-SAT), re-parse its exact coordinates into our own field
Q(sqrt3,sqrt5,sqrt11) without Singular, and decide 4-colourability with our pipeline.

Declared scope: one benchmark (n = 553, m = 2722), k = 4.  Outputs a certificate record.
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf, sat_decision, clique_number_bound

OUT = os.path.join(HERE, "certs")
F = Field([3, 5, 11])
t0 = time.time()
pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
n = len(pts)
print(f"[load] {n} vertices, {len(es)} edges, field Q(sqrt3,sqrt5,sqrt11) ({len(F.basis)} basis elements)")


def sd(a, b):
    dx = F.sub(a[0], b[0]); dy = F.sub(a[1], b[1])
    return F.add(F.mul(dx, dx), F.mul(dy, dy))


# 1. every published edge is exactly unit distance
bad = [i for i, (a, b) in enumerate(es) if not F.is_zero(F.sub(sd(pts[a], pts[b]), F.one))]
print(f"[validate] published edges at distance != 1: {len(bad)}")
assert not bad

# 2. all vertices distinct
assert len({(tuple(x), tuple(y)) for x, y in pts}) == n, "duplicate vertices"

# 3. completeness: no pair at unit distance that is not a published edge
eset = {tuple(sorted(e)) for e in es}
hidden = 0
for i in range(n):
    for j in range(i + 1, n):
        if (i, j) in eset:
            continue
        if F.is_zero(F.sub(sd(pts[i], pts[j]), F.one)):
            hidden += 1
print(f"[completeness] unit-distance pairs missing from the .edge file: {hidden}")

adj = [set() for _ in range(n)]
for a, b in es:
    adj[a].add(b); adj[b].add(a)
print(f"[graph] degrees min={min(map(len,adj))} max={max(map(len,adj))}, "
      f"clique number={clique_number_bound(adj) if n < 200 else 'skipped(n>200)'}")

# 4. 4-colourability decision by CDCL on our own CNF
nv, cl = cnf(adj, 4)
print(f"[sat] k=4 CNF: {nv} vars, {len(cl)} clauses")
res = sat_decision(adj, 4)
print(f"[sat] verdicts: {res['verdicts']}")

rec = {"benchmark": "Heule 553-vertex 5-chromatic unit-distance graph",
       "source": "arXiv:1805.12181 / github.com/marijnheule/CNP-SAT (vtx/553.vtx, edge/553.edge)",
       "field": "Q(sqrt3,sqrt5,sqrt11)", "n": n, "m": len(es),
       "edges_not_unit": len(bad), "duplicate_vertices": 0,
       "unit_pairs_missing_from_edge_file": hidden,
       "cnf_vars": nv, "cnf_clauses": len(cl),
       "verdicts": res["verdicts"], "model": res["model"],
       "seconds": round(time.time() - t0, 2)}
json.dump(rec, open(os.path.join(OUT, "heule553_4col.json"), "w"), indent=1)
print(f"[done] wrote {OUT}/heule553_4col.json in {rec['seconds']}s")
