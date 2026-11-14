"""Chromatic number of the unit-distance graph of the thin annulus
A = {1-eps <= |z-p0| <= 1+eps}, eps=71/10000, around p0=(1/55,18/55).
Discretize angles and radii; edges if distance is within tol of 1.
Decide k-colourability for k=2,3,4 with CaDiCaL.
"""
import numpy as np, subprocess, tempfile, os
from itertools import combinations
eps=71/10000
p0=np.array([1/55,18/55])
Nth=720; Nr=5
radii=np.linspace(1-eps,1+eps,Nr)
pts=[]
for r in radii:
    for j in range(Nth):
        th=2*np.pi*j/Nth
        pts.append(p0+r*np.array([np.cos(th),np.sin(th)]))
pts=np.array(pts); n=len(pts)
print("vertices",n)
# pairwise distances
D=np.linalg.norm(pts[:,None,:]-pts[None,:,:],axis=2)
tol=1e-4
adj=(np.abs(D-1.0)<tol)
np.fill_diagonal(adj,False)
print("edges",adj.sum()//2,"max degree",adj.sum(axis=1).max())
def colorable(k):
    clauses=[]
    def var(i,c): return i*k+c+1
    for i in range(n):
        clauses.append([var(i,c) for c in range(k)])
        for a,b in combinations(range(k),2): clauses.append([-var(i,a),-var(i,b)])
    ii,jj=np.nonzero(np.triu(adj,1))
    for i,j in zip(ii,jj):
        for c in range(k):
            clauses.append([-var(i,c),-var(j,c)])
    with tempfile.NamedTemporaryFile('w',suffix='.cnf',delete=False) as f:
        f.write(f"p cnf {n*k} {len(clauses)}\n")
        for c in clauses: f.write(" ".join(map(str,c))+" 0\n")
        path=f.name
    r=subprocess.run(['/opt/lean/bin/cadical','-q',path],capture_output=True,text=True,timeout=600)
    os.unlink(path)
    return ('s SATISFIABLE' in r.stdout), r.stdout
for k in (2,3,4):
    sat,_=colorable(k)
    print(f"k={k}: {'SAT' if sat else 'UNSAT'}")
    if sat: break
