"""Independent checker for quotient16_cert.json.  Reads ONLY the certificate, re-derives every
claim from the geometry in Q(sqrt3), and never trusts the producing script's booleans."""
from fractions import Fraction as F
import json, itertools, sys

class Q3:
    __slots__ = ('a','b')
    def __init__(self, a=0, b=0): self.a, self.b = F(a), F(b)
    def __add__(self, o): o = t3(o); return Q3(self.a+o.a, self.b+o.b)
    __radd__ = __add__
    def __neg__(self): return Q3(-self.a, -self.b)
    def __sub__(self, o): o = t3(o); return Q3(self.a-o.a, self.b-o.b)
    def __rsub__(self, o): return t3(o)-self
    def __mul__(self, o):
        o = t3(o); return Q3(self.a*o.a+3*self.b*o.b, self.a*o.b+self.b*o.a)
    __rmul__ = __mul__
    def inv(self):
        d = self.a*self.a-3*self.b*self.b; assert d
        return Q3(self.a/d, -self.b/d)
    def __truediv__(self, o): return self*t3(o).inv()
    def sign(self):
        a, b = self.a, self.b
        if a == 0: return 0 if b == 0 else (1 if b > 0 else -1)
        if b == 0: return 1 if a > 0 else -1
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        s = a*a-3*b*b
        if s > 0: return 1 if a > 0 else -1
        if s < 0: return 1 if b > 0 else -1
        return 0
    def __eq__(self, o): return (self-t3(o)).sign() == 0
    def __lt__(self, o): return (self-t3(o)).sign() < 0
    def __gt__(self, o): return (self-t3(o)).sign() > 0
    def __le__(self, o): return (self-t3(o)).sign() <= 0
    def __ge__(self, o): return (self-t3(o)).sign() >= 0
def t3(x): return x if isinstance(x, Q3) else Q3(x)
S3 = Q3(0,1)
V = lambda u,v:(u[0]+v[0],u[1]+v[1]); W = lambda u,v:(u[0]-v[0],u[1]-v[1])
SC = lambda c,u:(t3(c)*u[0], t3(c)*u[1])
DT = lambda u,v:u[0]*v[0]+u[1]*v[1]
NN = lambda u:DT(u,u)
def hexverts(a):
    a=t3(a); h=F(1,2)
    cs=[(S3/F(2),h),(0,1),(-S3/F(2),h),(-S3/F(2),-h),(0,-1),(S3/F(2),-h)]
    return [(a*t3(c[0]),a*t3(c[1])) for c in cs]
def pseg2(p,x,y):
    d=W(y,x); w=W(p,x); dd=NN(d)
    if dd.sign()==0: return NN(w)
    s=DT(w,d)/dd
    if s<=Q3(0): s=Q3(0)
    elif s>=Q3(1): s=Q3(1)
    return NN(W(p,V(x,SC(s,d))))
A=F(1,5); s=Q3(A)*S3
def centre(p,q): return (s*t3(p)+s*t3(q)/2, s*t3(q)*S3/F(2))
def rng2(p,q):
    fig=[V(centre(p,q),z) for z in hexverts(t3(2)*A)]
    return (min(pseg2((Q3(0),Q3(0)),fig[i],fig[(i+1)%6]) for i in range(6)), max(NN(z) for z in fig))
def one(p): return Q3(1)
def forced(p,q):
    dmn,dmx=rng2(p,q); return (dmn<one(1)) and (dmx>one(1))
def Norm(p,q): return p*p+p*q+q*q

C=json.load(open('quotient16_cert.json'))
fails=[]
def chk(cond,msg):
    if not cond: fails.append(msg)
# 1. verify each claimed forced offset, and that nothing else in the window is forced
FS=set(tuple(v) for v in C["forced_offsets"])
W_=[(p,q) for p in range(-5,6) for q in range(-5,6) if 0<Norm(p,q)<=16]
actual=set(v for v in W_ if forced(*v))
chk(FS==actual, f"forced set mismatch: cert-only {sorted(FS-actual)}, computed-only {sorted(actual-FS)}")
chk(len(FS)==42, f"|F| = {len(FS)} not 42")
# 2. each certified edge witness: in F, correct residue class, cosets distinct
for e in C["quotient"]["edges_with_witness_offset"]:
    (c1,c2)=[tuple(x) for x in e["cosets"]]; v=tuple(e["forced_offset"])
    chk(c1!=c2, "edge with equal cosets")
    chk(v in FS, f"witness {v} not in F")
    chk((v[0]-c1[0]+c2[0])%4==0 and (v[1]-c1[1]+c2[1])%4==0, f"witness {v} wrong residue for {c1},{c2}")
    chk(forced(*v), f"witness {v} fails the strict criterion")
# 3. all 120 pairs present, no duplicates
G=[(p,q) for p in range(4) for q in range(4)]
want=set(frozenset(p) for p in itertools.combinations(G,2))
got=[frozenset(tuple(x) for x in e["cosets"]) for e in C["quotient"]["edges_with_witness_offset"]]
chk(len(got)==120 and len(set(got))==120 and set(got)==want, "edge list is not exactly the 120 pairs")
chk(C["quotient"]["chi"]==16 and C["quotient"]["is_complete"], "certificate does not claim K_16")
chk(sorted(map(tuple,C["connection_set_S"]))==sorted([g for g in G if g!=(0,0)]), "S is not all 15 nonzero residues")
# 4. independent re-derivation of S from F
chk(set((p%4,q%4) for (p,q) in FS)==set(g for g in G if g!=(0,0)), "S != F mod 4")
# 5. the six-colouring statement: every 6-subset of the 16 cosets contains an edge
E=set(frozenset(tuple(x) for x in e["cosets"]) for e in C["quotient"]["edges_with_witness_offset"])
chk(all(any(frozenset(p) in E for p in itertools.combinations(S6,2)) for S6 in itertools.combinations(G,6)),
    "a 6-set of cosets is independent -- quotient would be 6-colourable")
print(f"checks run; failures = {len(fails)}")
for m in fails: print("  FAIL:", m)
print("CERTIFICATE VALID" if not fails else "CERTIFICATE INVALID")
sys.exit(1 if fails else 0)
