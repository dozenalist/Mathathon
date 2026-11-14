"""Independent verification of the union result. No solver. Fresh code path."""
import json, sys
from fractions import Fraction as Fr
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0,'.')
from udg.exact import Field
from udg.heule import load, load_edges

F=Field([3,5,11]); basis=F.basis
pts0=load('refs/heule_553.vtx',F); E0=load_edges('refs/heule_553.edge')
xt=tuple([Fr(3,2)]+[Fr(0)]*7); yt=[Fr(0)]*8; yt[basis.index(3)]=Fr(1,2); yt=tuple(yt)
pts=list(pts0)+[(F.add(p[0],xt),F.add(p[1],yt)) for p in pts0]
idx={}; keep=[]
for p in pts:
    k=(p[0],p[1])
    if k not in idx: idx[k]=len(keep); keep.append(p)
print("points:",len(pts),"-> dedup",len(keep),"overlap",len(pts)-len(keep))
def sqd(i,j):
    dx=F.sub(keep[i][0],keep[j][0]); dy=F.sub(keep[i][1],keep[j][1])
    return F.add(F.mul(dx,dx),F.mul(dy,dy))
rec=json.load(open('certs/union_tau.json'))
E=[tuple(e) for e in rec['edges']]
print("recorded edges:",len(E))
bad=[e for e in E if not F.is_zero(F.sub(sqd(*e),F.one))]
print("edges NOT exactly unit:",len(bad))
# witness
c=rec['witness']; n=len(keep)
mono=sum(1 for a,b in E if c[a]==c[b])
print("witness length",len(c),"colours",sorted(set(c)),"monochromatic",mono)
# restriction to H  (H is the A-copy)
imap={idx[(pts0[v][0],pts0[v][1])]:v for v in range(len(pts0))}
print("H-restriction monochromatic:",sum(1 for a,b in E0 if c[imap[a]]==c[imap[b]]))
# danger zone: rejected candidates closest to distance 1 must be exactly non-unit
w=np.array([np.sqrt(float(b)) for b in basis])
Pf=np.array([[sum(float(cc)*w[i] for i,cc in enumerate(comp)) for comp in p] for p in keep])
cand=sorted(cKDTree(Pf).query_pairs(r=1.0+1e-6))
Eset={tuple(e) for e in E}
rej=[(i,j) for (i,j) in cand if (i,j) not in Eset]
rej.sort(key=lambda ij: abs(float(np.sum((Pf[ij[0]]-Pf[ij[1]])**2))-1.0))
worst=rej[:400]
badrej=[(i,j) for (i,j) in worst if F.is_zero(F.sub(sqd(i,j),F.one))]
print(f"danger zone: {len(worst)} rejected candidates closest to 1, exact-unit among them: {len(badrej)}")
gaps=[abs(float(np.sum((Pf[i]-Pf[j])**2))-1.0) for (i,j) in worst]
print(f"  smallest |d^2-1| among rejected: {min(gaps):.3e}  (band was 1e-6)")
print("VERIFIED:", len(bad)==0 and mono==0 and len(badrej)==0)
