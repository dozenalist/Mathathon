"""Shrink the patch to a minimal 6-UNSAT induced core (certificate minimisation, same patch).
Any induced subgraph of G[P] is an induced subgraph of Cay(Z^2,F), so a core refutes the family."""
import json, time
from pysat.solvers import Cadical153
t0=time.time()
C=json.load(open('patch19_cert.json'))
cells=C["cells"]; E=[tuple(e) for e in C["edges_indexed"]]
def ncolors_unsat(keep, K):
    """is G[keep] K-UNSAT?"""
    pos={v:i for i,v in enumerate(keep)}
    cnf=[]
    for i in range(len(keep)):
        cnf.append([i*K+c+1 for c in range(K)])
        for c in range(K):
            for c2 in range(c+1,K): cnf.append([-(i*K+c+1),-(i*K+c2+1)])
    for (a,b) in E:
        if a in pos and b in pos:
            for c in range(K): cnf.append([-(pos[a]*K+c+1),-(pos[b]*K+c+1)])
    with Cadical153(bootstrap_with=cnf) as s: return not s.solve()
K=6
keep=list(range(len(cells)))
assert ncolors_unsat(keep,K), "the full patch must be 6-UNSAT"
print(f"full patch ({len(keep)} cells) is 6-UNSAT  ({time.time()-t0:.1f}s)")
changed=True; rnd=0
while changed:
    changed=False; rnd+=1
    for v in list(keep):
        trial=[x for x in keep if x!=v]
        if trial and ncolors_unsat(trial,K):
            keep=trial; changed=True
    print(f"  round {rnd}: core size {len(keep)}   ({time.time()-t0:.1f}s)")
core=sorted(keep)
sub=[cells[i] for i in core]
# chi of the core
def chi_of(keep):
    for k in range(2,12):
        pos={v:i for i,v in enumerate(keep)}
        cnf=[]
        for i in range(len(keep)):
            cnf.append([i*k+c+1 for c in range(k)])
            for c in range(k):
                for c2 in range(c+1,k): cnf.append([-(i*k+c+1),-(i*k+c2+1)])
        for (a,b) in E:
            if a in pos and b in pos:
                for c in range(k): cnf.append([-(pos[a]*k+c+1),-(pos[b]*k+c+1)])
        with Cadical153(bootstrap_with=cnf) as s:
            if s.solve(): return k
    return None
chi_core=chi_of(core)
edges=[(a,b) for (a,b) in E if a in set(core) and b in set(core)]
pos={v:i for i,v in enumerate(core)}
core_edges=[[pos[a],pos[b]] for (a,b) in edges]
print(f"CORE: {len(core)} cells, {len(core_edges)} edges, chi = {chi_core}")
print(f"cells: {sub}")
json.dump({"K":K,"n_cells":len(core),"cells":sub,"edges_indexed":core_edges,"chi":chi_core,
           "note":"induced subgraph of the patch P = {N<=19}; subset of Cay(Z^2,F) at a = 1/5"},
          open('core_cert.json','w'))
print(f"saved core_cert.json ({time.time()-t0:.1f}s)")
