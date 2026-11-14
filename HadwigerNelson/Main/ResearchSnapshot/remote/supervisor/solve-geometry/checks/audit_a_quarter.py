"""Independent audit of supervisor/solve-independent/{A-QUARTER.md,p25.cnf,p25.drat}.
Reconstructs F(1/4), the 73-cell patch, the edge set, decodes p25.cnf and compares."""
import json, os, math, sys
from fractions import Fraction as F

Z=(F(0),F(0)); ONE=(F(1),F(0)); TWO=(F(2),F(0)); O=((Z),(Z))
def qadd(x,y): return (x[0]+y[0],x[1]+y[1])
def qsub(x,y): return (x[0]-y[0],x[1]-y[1])
def qmul(x,y): return (x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def qdiv(x,y):
    d=y[0]*y[0]-3*y[1]*y[1]; return ((x[0]*y[0]-3*x[1]*y[1])/d,(x[1]*y[0]-x[0]*y[1])/d)
def sign(x):
    u,w=x
    if w==0: return (u>0)-(u<0)
    if u>0: return 1 if (w>0 or u*u>3*w*w) else -1
    if w>0: return 1 if 3*w*w>u*u else -1
    return -1
def qlt(x,y): return sign(qsub(x,y))<0
def psub(a,b): return (qsub(a[0],b[0]),qsub(a[1],b[1]))
def padd(a,b): return (qadd(a[0],b[0]),qadd(a[1],b[1]))
def smul(s,a): return (qmul(s,a[0]),qmul(s,a[1]))
def nrm2(p): return qadd(qmul(p[0],p[0]),qmul(p[1],p[1]))
H=[((F(0),F(1,2)),(F(1,2),F(0))),((Z),(F(1),F(0))),((F(0),-F(1,2)),(F(1,2),F(0))),
   ((F(0),-F(1,2)),(-F(1,2),F(0))),((Z),(-F(1),F(0))),((F(0),F(1,2)),(-F(1,2),F(0)))]
H2=[smul(TWO,v) for v in H]
def off(p,q): return ((F(0),F(p)+F(q,2)),(F(3,2)*q,Z[1]))
def musq(p,q):   # dmin^2 at a=1
    v=off(p,q); V=[padd(v,w) for w in H2]; best=None
    for i in range(6):
        x,y=V[i],V[(i+1)%6]; d=psub(y,x); w=psub(O,x); dd=nrm2(d)
        if sign(dd)==0: cand=nrm2(w)
        else:
            t=qdiv(qadd(qmul(w[0],d[0]),qmul(w[1],d[1])),dd)
            if qlt(t,Z): t=Z
            if qlt(ONE,t): t=ONE
            cand=nrm2(psub(w,smul(t,d)))
        if best is None or qlt(cand,best): best=cand
    return best
def qmaxs(xs):
    m=xs[0]
    for x in xs[1:]:
        if qlt(m,x): m=x
    return m
def nusq(p,q):   # dmax^2 at a=1  (max over the six vertices of 2H+v)
    v=off(p,q); return qmaxs([nrm2(padd(v,w)) for w in H2])
Norm=lambda p,q:p*p+p*q+q*q
BALL=[(p,q) for p in range(-5,6) for q in range(-5,6) if 0<Norm(p,q)<=16]

out=[]
def say(*a):
    s=" ".join(str(x) for x in a); out.append(s); print(s)

# ---- 1. F(1/4): mu(v) < 4 < nu(v) with mu,nu the a=1 extrema  <=> mu^2<16<nu^2
A=F(1,4); FORCED4=[]
for (p,q) in BALL:
    mu=musq(p,q); nu=nusq(p,q)
    if mu[1]==0 and nu[1]==0 and mu[0]<16 and nu[0]>16: FORCED4.append((p,q))
rings=sorted({Norm(*v) for v in FORCED4})
say(f"[16] F(1/4) recovered from the a=1 exact extrema: {len(FORCED4)} offsets, rings {rings}")

# ---- 2. patch
P=sorted([(p,q) for p in range(-6,7) for q in range(-6,7) if Norm(p,q)<=19], key=lambda v:(Norm(*v),v))  # producer's order (a_quarter.py:75)
idx={v:i for i,v in enumerate(P)}
say(f"     patch {{N <= 19}}: {len(P)} cells")

# ---- 3. edges
FS=set(FORCED4); E=set()
for u in P:
    for v in P:
        if u!=v:
            d=(v[0]-u[0], v[1]-u[1])
            if d in FS: E.add((idx[u],idx[v]))
deg=[0]*len(P)
for (i,j) in E: deg[i]+=1; deg[j]+=1
c0=idx[(0,0)]
say(f"     G[P]: {len(E)} directed-edge count -> {len(E)//2} undirected edges;"
    f" degrees {min(deg)}..{max(deg)}, centre degree {deg[c0]}")

# ---- 4. decode p25.cnf
src=os.path.join("..","..","supervisor","solve-independent","p25.cnf")
lines=[l.split() for l in open(src) if l.strip() and not l.startswith('p') and not l.startswith('c')]
cls=[[int(t) for t in l[:-1]] for l in lines]
say(f"     p25.cnf: {len(cls)} clauses parsed")
alo=[c for c in cls if len(c)==6]
var2cell={}
for c in alo:
    key=tuple(sorted(c))
    var2cell[c[0]]=key
cellof={}   # variable -> cell index
for v0,key in var2cell.items():
    for k in key: cellof[k]=(v0-1)//6
edges_file=set(); amo_same=0; amo_cross=0; atleast=0
for c in cls:
    if len(c)==6: atleast+=1; continue
    if len(c)==2:
        a,b=c[0],c[1]
        if abs(a-b)<=5 and (a-1)//6==(b-1)//6: amo_same+=1
        else:
            ca,cb=cellof[abs(a)],cellof[abs(b)]
            if ca==cb: amo_same+=1
            else: amo_cross+=1; edges_file.add((min(ca,cb),max(ca,cb)))
say(f"     clause types: at-least-one {atleast}, same-cell pairs {amo_same}, cross-cell pairs {amo_cross}")
say(f"     decoded edge pairs: {len(edges_file)}; expected {len(E)//2};"
    f" sets equal: {edges_file=={(min(i,j),max(i,j)) for (i,j) in E}}")
say(f"     clause count identity 73 + 73*15 + 6*{len(edges_file)} = "
    f"{73+73*15+6*len(edges_file)} (file: {len(cls)})")

# ---- 5. interval
mu2=[musq(*v)[0] for v in FORCED4]; nu2=[nusq(*v)[0] for v in FORCED4]
say(f"     at a=1 over F(1/4): max mu^2 = {max(mu2)}, min nu^2 = {min(nu2)}"
    f"  -> interval (1/sqrt{min(nu2)}, 1/sqrt{max(mu2)}) = "
    f"({math.sqrt(1/min(nu2)):.9f}, {math.sqrt(1/max(mu2)):.9f})")
say(f"     a=1/4 inside: {max(mu2)<16 and 16<min(nu2)};"
    f" endpoints excluded by tangency: 1/{min(nu2)} exact={min(nu2)**0.5==5},"
    f" 1/sqrt{max(mu2)} exact={max(mu2)==12}")
say(f"     (accepted interval (1/sqrt28,1/sqrt19) = (0.188982,0.229416) overlaps the new one on"
    f" (1/5,1/sqrt19): non-empty since 1/5 < 1/sqrt19 (5>sqrt19: {25>19}))")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","supervisor_checks.out"),"a").write("\n".join(out)+"\n")

# ---- 6. exact clause-set comparison (producer order recovered from a_quarter.py:75)
say("[17] exact CNF regeneration in the producer's vertex order")
def clauses_for(order, Fset):
    idx={v:i for i,v in enumerate(order)}; out=[]
    for v in order:
        i=idx[v]; out.append(tuple(6*i+c+1 for c in range(6)))
        for c1 in range(6):
            for c2 in range(c1+1,6): out.append(tuple(sorted((-6*i-c1-1,-6*i-c2-1))))
    for v in order:
        for w in order:
            if v!=w and (w[0]-v[0],w[1]-v[1]) in Fset:
                ia,ib=idx[v],idx[w]
                if ia<ib:
                    for c in range(6): out.append(tuple(sorted((-6*ia-c-1,-6*ib-c-1))))
    return out
regen=clauses_for(P,FS)
fileset=[tuple(sorted(c)) for c in cls]
say(f"     regenerated {len(regen)} clauses; file {len(fileset)};"
    f" equal as multisets: {sorted(regen)==sorted(fileset)}")
dups=[x for x in set(regen) if regen.count(x)!=fileset.count(x)]
say(f"     clauses differing in multiplicity: {len(dups)} {dups[:3]}")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","supervisor_checks.out"),"a").write("\n".join(out)+"\n")

# ---- 6. exact clause-set comparison (producer order recovered from a_quarter.py:75)
say("[17] exact CNF regeneration in the producer's vertex order")
def clauses_for(order, Fset):
    idx={v:i for i,v in enumerate(order)}; out=[]
    for v in order:
        i=idx[v]; out.append(tuple(6*i+c+1 for c in range(6)))
        for c1 in range(6):
            for c2 in range(c1+1,6): out.append(tuple(sorted((-6*i-c1-1,-6*i-c2-1))))
    for v in order:
        for w in order:
            if v!=w and (w[0]-v[0],w[1]-v[1]) in Fset:
                ia,ib=idx[v],idx[w]
                if ia<ib:
                    for c in range(6): out.append(tuple(sorted((-6*ia-c-1,-6*ib-c-1))))
    return out
regen=clauses_for(P,FS)
fileset=[tuple(sorted(c)) for c in cls]
say(f"     regenerated {len(regen)} clauses; file {len(fileset)};"
    f" equal as multisets: {sorted(regen)==sorted(fileset)}")
dups=[x for x in set(regen) if regen.count(x)!=fileset.count(x)]
say(f"     clauses differing in multiplicity: {len(dups)} {dups[:3]}")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","supervisor_checks.out"),"a").write("\n".join(out)+"\n")

# ---- 6. ordering-independent graph identity via 1-WL refinement, then clause-set equality
say("[17] graph identity, ordering-independent")
Eset={(min(i,j),max(i,j)) for (i,j) in E}
def wl(n, adj):
    col=[len(adj[i]) for i in range(n)]           # initial: degree
    hist=[]
    for _ in range(n):
        sig=[(col[i], tuple(sorted(col[j] for j in adj[i]))) for i in range(n)]
        uniq={s:k for k,s in enumerate(sorted(set(sig)))}
        new=[uniq[s] for s in sig]
        if new==col: break
        col=new; hist.append(len(set(col)))
    return col
adj_mine=[set() for _ in range(len(P))]
for (i,j) in Eset: adj_mine[i].add(j); adj_mine[j].add(i)
adj_file=[set() for _ in range(len(P))]
for (i,j) in edges_file: adj_file[i].add(j); adj_file[j].add(i)
cm=wl(len(P),adj_mine); cf=wl(len(P),adj_file)
same=len(set(cm))==len(set(cf))==len(P) and sorted(cm)==sorted(cf)
say(f"     WL refinement: mine {len(set(cm))} classes, file {len(set(cf))} classes,"
    f" both discrete: {len(set(cm))==len(P) and len(set(cf))==len(P)}, signatures equal: {same}")
perm=None
if same:
    inv={c:i for i,c in enumerate(cm)}
    perm={i:inv[c] for i,c in enumerate(cf)}      # file index -> my index
    ok=all((min(perm[i],perm[j]),max(perm[i],perm[j])) in Eset for (i,j) in edges_file)
    say(f"     bijection from WL colours is an isomorphism: {ok}; mapping sample {list(perm.items())[:4]}")
# clause-set equality under the permutation
def clauses_for(order, Fset):
    idx={v:i for i,v in enumerate(order)}; out=[]
    for v in order:
        i=idx[v]; out.append(tuple(6*i+c+1 for c in range(6)))
        for c1 in range(6):
            for c2 in range(c1+1,6): out.append(tuple(sorted((-6*i-c1-1,-6*i-c2-1))))
    for a in order:
        for b in order:
            if a!=b and (b[0]-a[0],b[1]-a[1]) in Fset:
                ia,ib=idx[a],idx[b]
                for c in range(6): out.append(tuple(sorted((-6*ia-c-1,-6*ib-c-1))))
    return out
if perm:
    order_file=[None]*len(P)
    for fi,mi in perm.items(): order_file[fi]=P[mi]
    regen=set(clauses_for(order_file,Fset))
    say(f"     regenerated clause set size {len(regen)}; file clause set size {len({tuple(sorted(c)) for c in cls})};"
        f" equal: {regen=={tuple(sorted(c)) for c in cls}}")
