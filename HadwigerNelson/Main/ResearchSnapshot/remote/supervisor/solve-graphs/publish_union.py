"""Independent re-check of the refinement result + self-contained bundle. No solver."""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0,'.')
from udg.exact import Field
from udg.heule import load, load_edges
F=Field([3,5,11]); basis=F.basis
pts0=load('refs/heule_553.vtx',F); E0=load_edges('refs/heule_553.edge')
xt=tuple([Fr(3,2)]+[Fr(0)]*7); yt=[Fr(0)]*8; yt[basis.index(3)]=Fr(1,2); yt=tuple(yt)
# rebuild with provenance
keys={}; keep=[]; prov=[]
def add(pt,tag,src):
    k=(pt[0],pt[1])
    if k in keys:
        prov[keys[k]].add(tag); return
    keys[k]=len(keep); keep.append(pt); prov.append({tag}); srcs.append(src)
srcs=[]
for i,p in enumerate(pts0): add(p,'A',i)
for i,p in enumerate(pts0): add((F.add(p[0],xt),F.add(p[1],yt)),'B',i)
n=len(keep); print("points",n,"overlap",sum(1 for s in prov if len(s)==2))
E=[tuple(int(x) for x in l.split()) for l in open('certs/union_tau_edges.txt') if not l.startswith('#')]
rec=json.load(open('certs/refine_union_k5.json')); W=rec['witnesses']
print("witnesses",len(W))
bad=0
for t,c in enumerate(W):
    m=sum(1 for u,v in E if c[u]==c[v])
    if m: print("  witness",t,"mono",m); bad+=1
print("  all witnesses proper on all",len(E),"edges:",bad==0)
adj=[set() for _ in range(n)]
for u,v in E: adj[u].add(v); adj[v].add(u)
def same_pairs(c):
    by={}
    for v,x in enumerate(c): by.setdefault(x,[]).append(v)
    S=set()
    for grp in by.values():
        for a in range(len(grp)):
            for b in range(a+1,len(grp)):
                i,j=grp[a],grp[b]
                if j not in adj[i]: S.add((i,j))
    return S
S=same_pairs(W[0])
for c in W[1:]: S&=same_pairs(c)
print("  survivors recomputed:",len(S),"recorded:",rec['final_survivors'],"match:",len(S)==rec['final_survivors'])
print("  survivor list match:",sorted(S)==[tuple(x) for x in rec['survivors']])
# any survivor internal to the H copy? (restriction-map fact: those are known non-forced in H)
hin=[(i,j) for (i,j) in S if i<n and j<n and prov[i]=={'A'} and prov[j]=={'A'}]
print("  survivors with BOTH endpoints A-only:",len(hin))
# self-contained bundle
with open('certs/union_tau_points.txt','w') as g:
    g.write("# index provenance source_in_heule553 x_coeffs(8, basis 1,3,5,11,15,33,55,165) y_coeffs(8)\n")
    for i,p in enumerate(keep):
        pr="+".join(sorted(prov[i]))
        xc=",".join(str(c) for c in p[0]); yc=",".join(str(c) for c in p[1])
        g.write(f"{i} {pr} {srcs[i]} {xc} {yc}\n")
print("wrote certs/union_tau_points.txt")
