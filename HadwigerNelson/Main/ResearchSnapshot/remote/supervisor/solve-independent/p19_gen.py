import json, time
t0=time.time()
C=json.load(open('patch19_cert.json'))
n=C["n"]; E=[tuple(e) for e in C["edges_indexed"]]; K=6
def var(v,c): return v*K+c+1
cnf=[]
for v in range(n):
    cnf.append([var(v,c) for c in range(K)])
    for c in range(K):
        for c2 in range(c+1,K): cnf.append([-var(v,c),-var(v,c2)])
for (i,j) in E:
    for c in range(K): cnf.append([-var(i,c),-var(j,c)])
from pysat.solvers import Glucose3
with Glucose3(bootstrap_with=cnf, with_proof=True) as g:
    sat=g.solve(); proof=g.get_proof()
print("SAT:", sat, "| proof lines:", len(proof), "| types:", set(type(c).__name__ for c in proof))
print("first 3:", proof[:3])
print("last 3:", proof[-3:])
print("empty clauses at:", [i for i,c in enumerate(proof) if c==[]][:5])
print("clause lengths: min",min(len(c) for c in proof),"max",max(len(c) for c in proof))
json.dump({"K":K,"clauses":cnf,"proof":proof}, open('patch19_drup.json','w'))
print(f"saved ({time.time()-t0:.1f}s)")
