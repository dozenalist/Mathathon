"""a = 1/4, patch P = {N <= 19} (73 cells), k = 6.  ONE pipeline: exact forced set, graph, CNF,
cadical decision, and either an edge-checked colouring or a drat-trim-verified DRAT proof."""
from fractions import Fraction as F
import json, subprocess, hashlib, time, os
t0=time.time()
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda: f.read(1<<20), b''): h.update(b)
    return h.hexdigest()

# ---------- exact geometry in Q(sqrt3) ----------
class Q3:
    __slots__=('a','b')
    def __init__(s,a=0,b=0): s.a,s.b=F(a),F(b)
    def __add__(s,o): o=t(o); return Q3(s.a+o.a,s.b+o.b)
    __radd__=__add__
    def __neg__(s): return Q3(-s.a,-s.b)
    def __sub__(s,o): o=t(o); return Q3(s.a-o.a,s.b-o.b)
    def __rsub__(s,o): return t(o)-s
    def __mul__(s,o):
        o=t(o); return Q3(s.a*o.a+3*s.b*o.b,s.a*o.b+s.b*o.a)
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
    def __repr__(s): return f"({s.a})+({s.b})r3"
def t(x): return x if isinstance(x,Q3) else Q3(x)
S3=Q3(0,1); A=F(1,4)
V=lambda u,v:(u[0]+v[0],u[1]+v[1]); W=lambda u,v:(u[0]-v[0],u[1]-v[1])
SC=lambda c,u:(t(c)*u[0],t(c)*u[1]); DT=lambda u,v:u[0]*v[0]+u[1]*v[1]; NN=lambda u:DT(u,u)
def hexverts(a):
    a=t(a); h=F(1,2)
    return [(a*t(c[0]),a*t(c[1])) for c in
            [(S3/F(2),h),(0,1),(-S3/F(2),h),(-S3/F(2),-h),(0,-1),(S3/F(2),-h)]]
def pseg2(p,x,y):
    d=W(y,x); w=W(p,x); dd=NN(d)
    if dd.sign()==0: return NN(w)
    s=DT(w,d)/dd
    if s<=Q3(0): s=Q3(0)
    elif s>=Q3(1): s=Q3(1)
    return NN(W(p,V(x,SC(s,d))))
def centre(p,q):
    s0=t(A)*S3
    return (s0*t(p)+s0*t(q)/2, s0*t(q)*S3/F(2))
def rng2(p,q):
    fig=[V(centre(p,q),z) for z in hexverts(t(2)*A)]
    return min(pseg2((Q3(0),Q3(0)),fig[i],fig[(i+1)%6]) for i in range(6)), max(NN(z) for z in fig)
Norm=lambda p,q:p*p+p*q+q*q
log=[]
def say(s): log.append(s); print(s, flush=True)
# ---------- 1. exact forced set at a = 1/4 ----------
cand=[(p,q) for p in range(-4,5) for q in range(-4,5) if 0<Norm(p,q)<=16]
Fs=sorted([v for v in cand if (lambda r: r[0]<Q3(1) and Q3(1)<r[1])(rng2(*v))])
rings=sorted(set(Norm(*v) for v in Fs))
say(f"[1] exact forced set at a = 1/4: |F| = {len(Fs)}, rings N = {rings}  ({time.time()-t0:.2f}s)")
say(f"    matches the pre-registered analytic derivation {{3,4,7,9}}? {rings==[3,4,7,9]}")
assert rings==[3,4,7,9] and len(Fs)==30
Fa=set(Fs)
# ---------- 2. graph ----------
P=sorted([(p,q) for p in range(-6,7) for q in range(-6,7) if Norm(p,q)<=19], key=lambda v:(Norm(*v),v))
assert len(P)==73
idx={v:i for i,v in enumerate(P)}
E=[(i,j) for i in range(len(P)) for j in range(i+1,len(P))
   if (lambda d: d in Fa or (-d[0],-d[1]) in Fa)((P[j][0]-P[i][0], P[j][1]-P[i][1]))]
n=len(P); adj=[set() for _ in range(n)]
for (i,j) in E: adj[i].add(j); adj[j].add(i)
deg=[len(adj[i]) for i in range(n)]
say(f"[2] G[P]: {n} cells, {len(E)} edges, degree {min(deg)}..{max(deg)} (centre {deg[idx[(0,0)]]}, |F| = 30)")
# max clique
best=[set()]
def expand(R,C):
    if not C:
        if len(R)>len(best[0]): best[0]=set(R)
        return
    if len(R)+len(C)<=len(best[0]): return
    for v in sorted(C,key=lambda x:-deg[x]):
        if len(R)+len(C)<=len(best[0]): return
        expand(R|{v}, C&adj[v]); C=C-{v}
expand(set(), set(range(n)))
say(f"[3] max clique = {len(best[0])}  witness {[P[i] for i in sorted(best[0])]}")
# ---------- 3. CNF ----------
K=6
def var(v,c): return v*K+c+1
cnf=[]
for v in range(n):
    cnf.append([var(v,c) for c in range(K)])
    for c in range(K):
        for c2 in range(c+1,K): cnf.append([-var(v,c),-var(v,c2)])
for (i,j) in E:
    for c in range(K): cnf.append([-var(i,c),-var(j,c)])
with open('p25.cnf','w') as f:
    f.write(f"p cnf {n*K} {len(cnf)}\n")
    for cl in cnf: f.write(" ".join(map(str,cl))+" 0\n")
say(f"[4] CNF: {n*K} vars, {len(cnf)} clauses -> p25.cnf   ({time.time()-t0:.2f}s)")
# ---------- 4. cadical decision ----------
CAD="/opt/lean/bin/cadical"
r=subprocess.run([CAD,"--no-binary","-q","p25.cnf","p25.drat"],capture_output=True,text=True,timeout=40)
say(f"[5] cadical exit={r.returncode} (10=SAT, 20=UNSAT)  ({time.time()-t0:.2f}s)")
say(f"    stdout tail: {r.stdout.strip().splitlines()[-2:] if r.stdout.strip() else '(quiet)'}")
result = "SAT" if r.returncode==10 else ("UNSAT" if r.returncode==20 else f"UNKNOWN({r.returncode})")
say(f"    -> {result}")
out={"a":"1/4","patch":"N <= 19","n":n,"edges":len(E),"K":K,
     "forced_rings":rings,"forced_offsets":[list(v) for v in Fs],
     "max_clique":len(best[0]),"result":result,
     "sha256":{"cnf":sha('p25.cnf')}}
if result=="SAT":
    # need the model: re-run cadical without -q to get the v-lines
    r2=subprocess.run([CAD,"p25.cnf"],capture_output=True,text=True,timeout=40)
    model=[]
    for line in r2.stdout.splitlines():
        if line.startswith("v"):
            model += [int(x) for x in line[1:].split() if x not in('0',)]
    col=[None]*n
    for lit in model:
        v,c=divmod(abs(lit)-1,K)
        if lit>0 and c<K: col[v]=c
    bad=[(i,j) for (i,j) in E if col[i]==col[j]]
    say(f"[6] SAT: colouring extracted; MONOCHROMATIC EDGES = {len(bad)} of {len(E)}")
    assert not bad
    from collections import Counter
    say(f"    colour classes: {sorted(Counter(col).values(),reverse=True)}")
    out["colouring"]=col
else:
    say(f"[6] UNSAT: proof p25.drat = {os.path.getsize('p25.drat')} bytes; verifying with drat-trim")
    d=subprocess.run(['./tools/drat-trim','p25.cnf','p25.drat'],capture_output=True,text=True,timeout=40)
    tail=[l for l in d.stdout.splitlines() if l.strip()][-4:]
    for l in tail: say("    drat-trim| "+l)
    out["drat_verified"]= "s VERIFIED" in d.stdout
    out["drat_tail"]=tail
    out["sha256"]["drat"]=sha('p25.drat')
    out["sha256"]["drat_trim"]=sha('tools/drat-trim')
    say(f"    VERIFIED? {out['drat_verified']}")
out["elapsed_s"]=round(time.time()-t0,2)
json.dump(out,open('a_quarter_cert.json','w'),indent=1)
open('a_quarter.out','w').write("\n".join(log)+"\n")
say(f"[7] total wall clock {time.time()-t0:.2f}s")
