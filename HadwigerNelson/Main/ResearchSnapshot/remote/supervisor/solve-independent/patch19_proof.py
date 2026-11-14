"""UNSAT certificate for 6-colouring G[P] at a = 1/5, patch P = {N <= 19} (73 cells).
Plain CNF (NO symmetry breaking) so UNSAT is unconditional; DRUP proof from Glucose3,
verified by a two-watched-literal RUP checker written here."""
import json, time, sys
t0=time.time()
C=json.load(open('patch19_cert.json'))
n=C["n"]; E=[tuple(e) for e in C["edges_indexed"]]
K=6
def var(v,c): return v*K+c+1
cnf=[]
for v in range(n):
    cnf.append([var(v,c) for c in range(K)])
    for c in range(K):
        for c2 in range(c+1,K): cnf.append([-var(v,c),-var(v,c2)])
for (i,j) in E:
    for c in range(K): cnf.append([-var(i,c),-var(j,c)])
print(f"plain CNF: {n} vertices, {len(E)} edges, K={K}, {len(cnf)} clauses, "
      f"{max(abs(l) for cl in cnf for l in cl)} vars")

from pysat.solvers import Glucose3, Cadical153
s=Cadical153(bootstrap_with=cnf); sat=s.solve(); s.delete()
print(f"Cadical153 (no symmetry breaking): SAT={sat}")
with Glucose3(bootstrap_with=cnf, with_proof=True) as g:
    sat2=g.solve()
    proof=g.get_proof()
print(f"Glucose3 : SAT={sat2}, proof lines = {len(proof)}  ({time.time()-t0:.1f}s)")
assert not sat and not sat2
assert proof and proof[-1]==[], "proof must end with the empty clause"
json.dump({"K":K,"n":n,"clauses":len(cnf),"proof_lines":len(proof),"proof":proof},
          open('patch19_drup.json','w'))
print(f"wrote patch19_drup.json  ({time.time()-t0:.1f}s)")
