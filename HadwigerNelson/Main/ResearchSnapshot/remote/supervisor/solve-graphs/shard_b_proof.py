"""Shard B step 2: self-contained DRAT certificate for the 4-UNSAT of the Heule 553 graph.

The pysat cadical153 binding emits proofs with clause *offsets* (cadical's internal
format); routing them through _proof_bin2text mangles them, and drat-trim rejected the
result.  We therefore use pysat's CaDiCaL195 binding, whose proof is plain DRAT text.
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from udg.exact import Field
from udg.heule import load, load_edges
from udg.graph import cnf
from pysat.solvers import Solver

F = Field([3, 5, 11])
pts = load(os.path.join(HERE, "refs/heule_553.vtx"), F)
es = load_edges(os.path.join(HERE, "refs/heule_553.edge"))
adj = [set() for _ in range(len(pts))]
for a, b in es:
    adj[a].add(b); adj[b].add(a)
nv, cl = cnf(adj, 4)
d = os.path.join(HERE, "certs")
fcnf = os.path.join(d, "heule553_k4.cnf")
with open(fcnf, "w") as f:
    f.write(f"p cnf {nv} {len(cl)}\n")
    for c in cl:
        f.write(" ".join(map(str, c)) + " 0\n")
fdr = os.path.join(d, "heule553_k4.drat")
t0 = time.time()
name = "cadical195"
with Solver(name=name, bootstrap_with=cl, with_proof=True) as s:
    ok = s.solve()
    proof = s.get_proof()
print(f"[{name}] solve:", "SAT" if ok else "UNSAT", "| proof lines:", len(proof), "| first:", proof[0] if proof else None)
assert not ok, "expected UNSAT"
with open(fdr, "w") as g:
    for line in proof:
        g.write(line if isinstance(line, str) else " ".join(map(str, line)) + " 0")
        g.write("\n")
json.dump({"cnf": os.path.basename(fcnf), "nclauses": len(cl), "nvars": nv,
           "drat": os.path.basename(fdr), "drat_lines": len(proof), "solver": name,
           "seconds": round(time.time() - t0, 2), "size_bytes": os.path.getsize(fdr)},
          open(os.path.join(d, "heule553_k4_proof.json"), "w"), indent=1)
print("wrote", fcnf, fdr)
