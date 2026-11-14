"""One induced subgraph of Cay(Z^2, F) at a = 1/5: P = {v : N(v) <= 19}, 6-colouring decision.
Exact Q(sqrt3) for the forced set (re-verified), then exact combinatorics on G[P]."""
from fractions import Fraction as F
import sys, itertools, json, time
t0 = time.time()

# ---------- exact forced offsets (Q(sqrt3)) : re-verification, not assumption ----------
class Q3:
    __slots__=('a','b')
    def __init__(s,a=0,b=0): s.a,s.b=F(a),F(b)
    def __add__(s,o): o=t(o); return Q3(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return Q3(-s.a,-s.b)
    def __sub__(s,o): o=t(o); return Q3(s.a-o.a,s.b-o.b)
    def __rsub__(s,o): return t(o)-s
    def __mul__(s,o):
        o=t(o); return Q3(s.a*o.a+3*s.b*o.b, s.a*o.b+s.b*o.a)
    __rmul__=__mul__
    def inv(s):
        d=s.a*s.a-3*s.b*s.b; assert d
        return Q3(s.a/d,-s.b/d)
    def __truediv__(s,o): return s*t(o).inv()
    def sign(s):
        a,b=s.a,s.b
        if a==0: return 0 if b==0 else (1 if b>0 else -1)
        if b==0: return 1 if a>0 else -1
        if a>0 and b>0: return 1
        if a<0 and b<0: return -1
        sq=a*a-3*b*b
        return (1 if a>0 else -1) if sq>0 else ((1 if b>0 else -1) if sq<0 else 0)
    def __eq__(s,o): return (s-t(o)).sign()==0
    def __lt__(s,o): return (s-t(o)).sign()<0
    def __gt__(s,o): return (s-t(o)).sign()>0
    def __le__(s,o): return (s-t(o)).sign()<=0
    def __ge__(s,o): return (s-t(o)).sign()>=0
def t(x): return x if isinstance(x,Q3) else Q3(x)
S3=Q3(0,1); A=F(1,5)
def hexverts(a):
    a=t(a); h=F(1,2)
    cs=[(S3/F(2),h),(0,1),(-S3/F(2),h),(-S3/F(2),-h),(0,-1),(S3/F(2),-h)]
    return [(a*t(c[0]),a*t(c[1])) for c in cs]
V=lambda u,v:(u[0]+v[0],u[1]+v[1]); W=lambda u,v:(u[0]-v[0],u[1]-v[1])
SC=lambda c,u:(t(c)*u[0],t(c)*u[1]); DT=lambda u,v:u[0]*v[0]+u[1]*v[1]; NN=lambda u:DT(u,u)
def pseg2(p,x,y):
    d=W(y,x); w=W(p,x); dd=NN(d)
    if dd.sign()==0: return NN(w)
    s=DT(w,d)/dd
    if s<=Q3(0): s=Q3(0)
    elif s>=Q3(1): s=Q3(1)
    return NN(W(p,V(x,SC(s,d))))
s0=Q3(A)*S3
def centre(p,q): return (s0*t(p)+s0*t(q)/2, s0*t(q)*S3/F(2))
def forced(p,q):
    fig=[V(centre(p,q),z) for z in hexverts(t(2)*A)]
    dmn=min(pseg2((Q3(0),Q3(0)),fig[i],fig[(i+1)%6]) for i in range(6))
    dmx=max(NN(z) for z in fig)
    return (dmn<Q3(1)) and (dmx>Q3(1))
Norm=lambda p,q:p*p+p*q+q*q
Fset=sorted((p,q) for p in range(-5,6) for q in range(-5,6)
            if 0<Norm(p,q)<=16 and forced(p,q))
assert len(Fset)==42 and set(Norm(*v) for v in Fset)=={4,7,9,12,13}
Fsset=set(Fset)
rec=[]
def say(s): rec.append(s); print(s)
say(f"[0] forced set re-verified exactly: |F| = {len(Fset)}, rings {sorted(set(Norm(*v) for v in Fset))}  ({time.time()-t0:.1f}s)")

# ---------- the patch ----------
P=sorted(((p,q) for p in range(-6,7) for q in range(-6,7) if Norm(p,q)<=19),
         key=lambda v:(Norm(*v),v))
say(f"[1] patch P = {{v : N(v) <= 19}} : |P| = {len(P)} <= 81  : {len(P)==73}")
assert len(P)==73
idx={v:i for i,v in enumerate(P)}
E=set()
for i,u in enumerate(P):
    for j in range(i+1,len(P)):
        w=(P[j][0]-u[0],P[j][1]-u[1])
        if w in Fsset or (-w[0],-w[1]) in Fsset: E.add((i,j))
n=len(P); m=len(E)
deg=[0]*n
for (i,j) in E: deg[i]+=1; deg[j]+=1
say(f"[2] G[P]: {n} vertices, {m} edges, degrees min {min(deg)} max {max(deg)} mean {2*m/n:.1f}  ({time.time()-t0:.1f}s)")
adj=[set() for _ in range(n)]
for (i,j) in E: adj[i].add(j); adj[j].add(i)

# ---------- max clique (exact, branch and bound) ----------
best=[set()]
def expand(R, Cand):
    if not Cand:
        if len(R)>len(best[0]): best[0]=set(R)
        return
    if len(R)+len(Cand)<=len(best[0]): return
    for v in sorted(Cand, key=lambda x:-deg[x]):
        if len(R)+len(Cand)<=len(best[0]): return
        expand(R|{v}, Cand & adj[v])
        Cand = Cand - {v}
expand(set(), set(range(n)))
CL=sorted(best[0])
say(f"[3] max clique of G[P]: size {len(CL)}  witness cells {[P[i] for i in CL]}")
say(f"     -> chi(G[P]) >= {len(CL)}")

# ---------- DSATUR colouring (upper bound) ----------
def dsatur(k, order_hint=None):
    col=[-1]*n
    def pick():
        bestv, bestkey = -1, None
        for v in range(n):
            if col[v]!=-1: continue
            nb={col[u] for u in adj[v] if col[u]!=-1}
            key=(len(nb), len(nb & adj[v] & {u for u in range(n) if col[u]==-1} if False else nb), deg[v])
            sat=len(nb)
            key=(sat, sum(1 for u in adj[v] if col[u]!=-1))
            if bestkey is None or key>bestkey: bestkey, bestv = key, v
        return bestv
    cnt=[0]
    def rec_(left):
        if left==0: return True
        v=pick()
        used={col[u] for u in adj[v] if col[u]!=-1}
        for c in range(k):
            if c in used: continue
            if c>max(col)+1 and False: continue
            col[v]=c
            if rec_(left-1): return True
            col[v]=-1
        return False
    if rec_(n): return col
    return None
# greedy first for a quick upper bound
def greedy(order):
    col=[-1]*n
    for v in order:
        used={col[u] for u in adj[v] if col[u]!=-1}
        c=0
        while c in used: c+=1
        col[v]=c
    return col
g=greedy(sorted(range(n), key=lambda v:-deg[v]))
GU=max(g)+1
say(f"[4] greedy (degree order) gives chi(G[P]) <= {GU}")

# ---------- exact k-colourability with python-sat, with symmetry breaking ----------
from pysat.solvers import Cadical153
def cnf_kcolor(k):
    cnf=[]
    def var(v,c): return v*k+c+1
    for v in range(n):
        cnf.append([var(v,c) for c in range(k)])
        for c in range(k):
            for c2 in range(c+1,k): cnf.append([-var(v,c),-var(v,c2)])
    for (i,j) in E:
        for c in range(k): cnf.append([-var(i,c),-var(j,c)])
    # symmetry breaking: colours are used in order of first appearance (sequential encoding, weak form)
    # (safe: only fixes colour NAMES per vertex-order prefix)
    for v in range(1,n):
        for c in range(1,k):
            # if v takes colour c then some earlier vertex takes colour c-1
            cnf.append([-var(v,c)]+[var(u,c-1) for u in range(v)])
    cnf.append([var(0,0)])
    return cnf, var
results={}
for k in range(len(CL), GU+1):
    cnf, var = cnf_kcolor(k)
    with Cadical153(bootstrap_with=cnf) as s:
        sat = s.solve()
        model = s.get_model() if sat else None
    results[k]=sat
    say(f"[5] k={k}: {'SAT' if sat else 'UNSAT'}   ({time.time()-t0:.1f}s)")
    if sat:
        col=[0]*n
        for v in range(n):
            for c in range(k):
                if model[var(v,c)-1]>0: col[v]=c
        # verify edge by edge
        bad=[(i,j) for (i,j) in E if col[i]==col[j]]
        say(f"     model verified edge-by-edge: {len(bad)} monochromatic edges out of {m}")
        assert not bad
        CHI=k; COLOURING=col
        break
say(f"[6] chi(G[P]) = {CHI}  (lower bound {len(CL)} from the clique, upper bound {CHI})")
from collections import Counter
say(f"     colour class sizes: {sorted(Counter(COLOURING).values(), reverse=True)}")
say(f"     6-colourable: {CHI<=6}")
json.dump({"patch":"N(p,q) <= 19","n":n,"m":m,"edges_indexed":sorted([list(e) for e in E]),
           "cells":P,"clique_size":len(CL),"clique_cells":[P[i] for i in CL],
           "chi":CHI,"colouring":COLOURING,
           "sat_by_k":{str(k):v for k,v in results.items()}}, open('patch19_cert.json','w'))
open('patch19.out','w').write("\n".join(rec)+"\n")
print(f"\nwrote patch19_cert.json, patch19.out  (total {time.time()-t0:.1f}s)")
