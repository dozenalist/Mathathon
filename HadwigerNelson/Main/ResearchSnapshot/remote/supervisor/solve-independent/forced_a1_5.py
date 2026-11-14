"""a = 1/5 honeycomb: exact forced offsets, endpoint exceptions, and the periodic (coset) bound."""
from fractions import Fraction as F

class Q3:
    __slots__ = ('a','b')
    def __init__(self, a=0, b=0): self.a, self.b = F(a), F(b)
    def __add__(self, o): o = to3(o); return Q3(self.a+o.a, self.b+o.b)
    __radd__ = __add__
    def __neg__(self): return Q3(-self.a, -self.b)
    def __sub__(self, o): o = to3(o); return Q3(self.a-o.a, self.b-o.b)
    def __rsub__(self, o): return to3(o)-self
    def __mul__(self, o):
        o = to3(o); return Q3(self.a*o.a+3*self.b*o.b, self.a*o.b+self.b*o.a)
    __rmul__ = __mul__
    def inv(self):
        d = self.a*self.a-3*self.b*self.b; assert d != 0
        return Q3(self.a/d, -self.b/d)
    def __truediv__(self, o): return self*to3(o).inv()
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
    def __eq__(self, o): return (self-to3(o)).sign() == 0
    def __lt__(self, o): return (self-to3(o)).sign() < 0
    def __gt__(self, o): return (self-to3(o)).sign() > 0
    def __le__(self, o): return (self-to3(o)).sign() <= 0
    def __ge__(self, o): return (self-to3(o)).sign() >= 0
    __hash__ = None
    def __repr__(self): return f"({self.a})+({self.b})r3"
def to3(x): return x if isinstance(x, Q3) else Q3(x)
S3 = Q3(0,1)
def vadd(u,v): return (u[0]+v[0], u[1]+v[1])
def vsub(u,v): return (u[0]-v[0], u[1]-v[1])
def smul(c,u): c = to3(c); return (c*u[0], c*u[1])
def dot(u,v): return u[0]*v[0]+u[1]*v[1]
def n2(u): return dot(u,u)
def hexverts(a):
    a = to3(a); h = F(1,2)
    cs = [(S3/F(2),h),(0,1),(-S3/F(2),h),(-S3/F(2),-h),(0,-1),(S3/F(2),-h)]
    return [(a*to3(c[0]), a*to3(c[1])) for c in cs]
def pseg2(p,x,y):
    d = vsub(y,x); w = vsub(p,x); dd = n2(d)
    if dd.sign() == 0: return n2(w)
    t = dot(w,d)/dd
    if t <= Q3(0): t = Q3(0)
    elif t >= Q3(1): t = Q3(1)
    return n2(vsub(p, vadd(x, smul(t,d))))
def range2(p, q, a):
    a = to3(a); s = a*S3
    v = (s*to3(p)+s*to3(q)/2, s*to3(q)*S3/F(2))
    fig = [vadd(v, z) for z in hexverts(to3(2)*a)]
    dmax2 = max(n2(z) for z in fig)
    dmin2 = min(pseg2((Q3(0),Q3(0)), fig[i], fig[(i+1)%6]) for i in range(6))
    return dmin2, dmax2
def Norm(p,q): return p*p+p*q+q*q
WIN = 24
PTS = [(p,q) for p in range(-9,10) for q in range(-9,10) if 0 < Norm(p,q) <= WIN]

def forced_set(a):
    Fs = set(); data = {}
    for (p,q) in PTS:
        dmin2, dmax2 = range2(p,q,a)
        f = (dmin2 < Q3(1)) and (dmax2 > Q3(1))
        data[(p,q)] = (dmin2, dmax2, f)
        if f: Fs.add((p,q))
    return Fs, data

out = []
def say(s): out.append(s); print(s)

a = Q3(F(1,5)); D = F(2,5)
say(f"a = 1/5 : hexagon circumradius 0.2, cell diameter D = 0.4, lattice spacing a*sqrt3 = {0.2*3**0.5:.6f}")
Fs, data = forced_set(a)
say("")
say("ring  N   |v|     forced/total   note")
rings = {}
for (p,q), (dmin2, dmax2, f) in data.items():
    rings.setdefault(Norm(p,q), []).append((p,q,dmin2,dmax2,f))
for N in sorted(rings):
    rs = rings[N]; nf = sum(1 for r in rs if r[4])
    note = ""
    if 0 < nf < len(rs):
        note = "PARTIAL -> forced: " + str([r[:2] for r in rs if r[4]])
    say(f"  {N:3d}  {0.2*(3*N)**0.5:6.4f}   {nf:2d}/{len(rs):2d}   {note}")
say("")
say(f"|F| = {len(Fs)} forced offsets out of {len(PTS)} vectors with N <= {WIN}; N range of F: "
    f"[{min(Norm(*v) for v in Fs)}, {max(Norm(*v) for v in Fs)}]")
assert all(0.2*(3*Norm(*v))**0.5 < 1.4 for v in Fs)
tang = sorted([(p,q) for (p,q),(d2,x2,f) in data.items() if Norm(p,q) <= 16 and x2 == Q3(1)])
near = sorted([(p,q) for (p,q),(d2,x2,f) in data.items() if Norm(p,q) <= 16 and d2 == Q3(1)])
say(f"ENDPOINT EXCEPTIONS (dmax^2 == 1 exactly, tangency, not forced): {tang}")
say(f"ENDPOINT EXCEPTIONS (dmin^2 == 1 exactly): {near}")

def sublattice_basis(d):
    """ALL sublattices of Z^2 of index d, upper Hermite normal form: basis (a,b),(0,c),
       a*c = d, 0 <= b < c.  (The lower form (a,0),(b,c) is NOT complete: it misses e.g.
       the index-7 lattice <(1,3),(0,7)> of the paper's 7-colouring.)"""
    res = []
    for a_ in range(1, d+1):
        if d % a_: continue
        c_ = d // a_
        for b_ in range(c_):
            res.append((a_, b_, c_))
    return res
def in_lattice(p, q, bas):
    a_, b_, c_ = bas
    if p % a_: return False
    m = p // a_
    return (q - m*b_) % c_ == 0
NMAX = 17
say("")
say("Periodic/coset test: a colouring periodic with period Lambda_p must have F and Lambda_p disjoint")
say("(cells in one coset share a colour).  Enumerating all sublattices of index d:")
dmin_idx = None; witness = None
for d in range(2, 26):
    ok = [bas for bas in sublattice_basis(d)
          if all(not (in_lattice(p,q,bas) and (p,q) in Fs)
                 for p in range(-5,6) for q in range(-5,6) if 0 < Norm(p,q) <= NMAX)]
    say(f"  index {d:2d}: {len(ok):2d} avoiding   {('e.g. HNF ' + str(ok[0])) if ok else ''}")
    if ok and dmin_idx is None:
        dmin_idx, witness = d, ok[0]
say("")
say(f"MINIMUM avoiding index at a = 1/5: {dmin_idx}   (witness HNF basis {witness})")
a_, b_, c_ = witness
vecs = set()
for m in range(-6,7):
    for n in range(-6,7):
        if m == 0 and n == 0: continue
        p = m*a_ + n*b_; q = n*c_
        if Norm(p,q) <= 60: vecs.add(Norm(p,q))
say(f"  witness sublattice has no vector with N in {sorted(set(Norm(*v) for v in Fs))} ; its N values <= 60: {sorted(vecs)}")
assert not any(in_lattice(p,q,witness) for (p,q) in Fs)
say("  [OK] coset colouring on this sublattice is proper on cell INTERIORS (not yet on the 1-skeleton)")
say("")
say("Corrected derivation (proof, not search).  The Eisenstein norm N is multiplicative and")
say("N(k*lambda) = k^2 N(lambda), so a sublattice containing lambda contains 2*lambda, 3*lambda, ...")
say("Avoidance therefore needs N(lambda) and 4N(lambda) and 9N(lambda) all outside F_N.")
say("At a = 1/5, F_N = {4,7,9,12,13}: n = 1 gives 4 in F_N, n = 3 gives 12 in F_N, and")
say("n in {4,7,9,12,13} are themselves forbidden, so N(lambda) >= 16 for every nonzero lambda.")
say("Packing bound: covolume >= (sqrt3/2)*min|lambda|^2, and index = covolume/((sqrt3/2)*3a^2)")
say("  = min|lambda|^2/(3a^2) = min N  ->  index >= 16.")
say("Attained by 4*T = 4Z x 4Z (index 16), whose norms are all multiples of 16: 0 forced offsets.")
say("")
say("(The earlier heuristic '|lambda| > 1+D forces index >= ceil((1+D)^2/(3a^2)) = 17' was WRONG:")
say("ring 16 has |lambda| = 1.3856 < 1+D = 1.4 and is unforced, because dmin >= 1 there (the two")
say("cells are far apart in a direction where the hexagon is thin).  The bound is 16, not 17.)")
a2 = Q3(F(2,5)); F2, _ = forced_set(a2)
d2min = None
for d in range(2, 12):
    if any(all(not (in_lattice(p,q,bas) and (p,q) in F2)
               for p in range(-5,6) for q in range(-5,6) if 0 < Norm(p,q) <= NMAX)
           for bas in sublattice_basis(d)):
        d2min = d; break
say("")
say(f"CONTROL a = 2/5 (paper's 7-colouring): minimum avoiding index = {d2min}; bound ceil((1.8)^2/(3*0.16))")
say(f"  = {(1.8)**2/0.48:.4f} -> >= 7.  Bound SHARP there, so the 7-colouring is the minimal-index")
say("  periodic colouring at a = 2/5.")
open('forced_a1_5.out','w').write("\n".join(out)+"\n")
print("wrote forced_a1_5.out")
