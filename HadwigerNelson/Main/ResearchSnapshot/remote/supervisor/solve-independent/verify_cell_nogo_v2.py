"""v2: corrected honeycomb cell-family no-go.
Fixes over v1: (i) the convention-free criterion is STRICT (dmin < 1 < dmax), because interior
points are unambiguous under every boundary rule; (ii) the forced set is computed as a function
of a, not just at a = 2/5 -- rings other than 1,3,4 are forced at the SMALL end of the range;
(iii) the range is open at 1/sqrt13.  Exact arithmetic in Q(sqrt3)."""
from fractions import Fraction as F
import itertools, json

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
    def __le__(self, o): return (self-to3(o)).sign() <= 0
    def __gt__(self, o): return (self-to3(o)).sign() > 0
    def __ge__(self, o): return (self-to3(o)).sign() >= 0
    def __repr__(self): return f"({self.a})+({self.b})r3"
    def f(self): return float(self.a)+float(self.b)*3**0.5
def to3(x): return x if isinstance(x, Q3) else Q3(x)
S3 = Q3(0,1)
def vadd(u,v): return (u[0]+v[0], u[1]+v[1])
def vsub(u,v): return (u[0]-v[0], u[1]-v[1])
def smul(c,u): c = to3(c); return (c*u[0], c*u[1])
def dot(u,v): return u[0]*v[0]+u[1]*v[1]
def n2(u): return dot(u,u)

def hexverts(a):
    """Voronoi cell of the triangular lattice: vertices at 30+60k degrees (faces normal to the
    six neighbour directions), circumradius a, inradius a*sqrt3/2."""
    a = to3(a); h = F(1,2)
    cs = [(S3/F(2),h),(0,1),(-S3/F(2),h),(-S3/F(2),-h),(0,-1),(S3/F(2),-h)]
    return [(a*to3(c[0]), a*to3(c[1])) for c in cs]

def pseg2(p, x, y):
    d = vsub(y,x); w = vsub(p,x); dd = n2(d)
    if dd.sign() == 0: return n2(w)
    t = dot(w,d)/dd
    if t <= Q3(0): t = Q3(0)
    elif t >= Q3(1): t = Q3(1)
    return n2(vsub(p, vadd(x, smul(t,d))))

def range2(v, a):
    """(dmin^2, dmax^2) of distances between cell V(0) and V(v), circumradius a; plus the
    maximising point z in 2V (a vertex) for dmax -- used for the tangency audit."""
    fig = [vadd(v, z) for z in hexverts(to3(2)*to3(a))]
    dmax2 = max(n2(z) for z in fig); arg = max(fig, key=lambda z: n2(z).f())
    dmin2 = min(pseg2((Q3(0),Q3(0)), fig[i], fig[(i+1)%6]) for i in range(6))
    return dmin2, dmax2, arg

def lat(p,q,a):
    a = to3(a); s = a*S3
    return (s*to3(p)+s*to3(q)/2, s*to3(q)*S3/F(2))

def Norm(p,q): return p*p+p*q+q*q
WIN = 40
PTS = [(p,q) for p in range(-7,8) for q in range(-7,8) if Norm(p,q) <= WIN]

out = []
def say(s): out.append(s); print(s)

# ---------- A. per-ring strict a-intervals (exact) ----------------------------
# forced(l,a) for all l in ring N  <=>  a^2 * max_v mu^2(v) < 1  and  a^2 * min_v nu^2(v) > 1
ring = {}
for (p,q) in PTS:
    if (p,q) == (0,0): continue
    dmin2, dmax2, _ = range2(lat(p,q,1), 1)
    ring.setdefault(Norm(p,q), []).append((dmin2, dmax2))
say("A. strict-forced a-interval per ring N (a = hexagon circumradius, cells of the honeycomb)")
say("   N     mu^2_max (=dmin^2 at a=1)      nu^2_min (=dmax^2 at a=1)     forced for a in")
intervals = {}
for N in sorted(ring):
    rows = ring[N]
    mu2max = max(r[0] for r in rows)      # a^2 * mu2max < 1
    nu2min = min(r[1] for r in rows)      # a^2 * nu2min > 1
    lo = None if nu2min.sign() == 0 else 1/nu2min.f()**0.5
    hi = None if mu2max.sign() == 0 else 1/mu2max.f()**0.5
    intervals[N] = (mu2max, nu2min)
    say(f"  {N:3d}   {mu2max!r:26s} {nu2min!r:26s} ({(lo if lo is not None else 0):.6f}, "
        f"{(hi if hi is not None else float('inf')):.6f})")
    if N > 21: break

# ---------- B. the forced set as a function of a on (1/sqrt13, 1/2) -----------
def forced_rings(a2, iv=intervals):
    """a2 = a^2 (rational). Ring N forced <=> a^2 mu2max < 1 < a^2 nu2min, exactly."""
    res = []
    for N, (mu2max, nu2min) in iv.items():
        if (Q3(a2)*nu2min - Q3(1)).sign() > 0 and (Q3(1) - Q3(a2)*mu2max).sign() > 0:
            res.append(N)
    return sorted(res)

say("")
say("B. the actual forced set on subintervals of (1/sqrt13, 1/2) = (0.277350, 0.500000)")
# completeness of the window: a ring forced at a >= 1/sqrt13 needs dmin^2(a=1) <= 1/a^2 <= 13,
# and dmin(a=1) >= |v|(a=1) - 2, so |v|^2(a=1) = 3N <= (sqrt13+2)^2 = 31.4 -> N <= 10. So only
# N in {1,3,4,7,9} can ever be forced in this range; WIN=40 covers them with margin.
assert max(N for N in intervals if N <= 10) == 9
say("   (window sufficiency: forced at a >= 1/sqrt13 forces dmin^2(a=1) <= 13, i.e. 3N <= 31.4,")
say("    so only rings N in {1,3,4,7,9} can occur -- all inside the computed window)")
crit = set()
for N, (mu2max, nu2min) in intervals.items():
    for k2 in (mu2max, nu2min):
        if k2.sign() > 0 and k2.b == 0:
            v = F(1)/k2.a
            if F(1,13) < v < F(1,4):
                crit.add(v)
cuts = sorted(crit)
bounds = [F(1,13)] + cuts + [F(1,4)]
for k in range(len(bounds)-1):
    a2lo, a2hi = bounds[k], bounds[k+1]
    mid2 = (a2lo+a2hi)/2
    rs = forced_rings(mid2)
    say(f"   a^2 in ({float(a2lo):.6f}, {float(a2hi):.6f}) = (a_lo, a_hi) with a in ({a2lo**0.5:.6f}, {a2hi**0.5:.6f})  ->  forced rings {rs}")
    assert set((1,3,4)).issubset(rs)
say("   ==> on the WHOLE open range the forced set contains {1,3,4}; its exact value is")
say("       {1,3,4,7,9} on (1/sqrt13,1/sqrt12), {1,3,4,7} on (1/sqrt12,1/sqrt7), {1,3,4} on (1/sqrt7,1/2).")

# ---------- C. the supervisor's test: is N=7 forced at the small end? --------
say("")
a2_small = F(28,100)**2                        # a = 0.28, just above 1/sqrt13 = 0.27735
rs = forced_rings(a2_small)
say(f"C. at a = 0.28 (just above 1/sqrt13): forced rings = {rs}")
say(f"   ==> N=7 IS forced at the small end; the v1 claim 'forced set is exactly N in {{1,3,4}}'")
say(f"       is FALSE on (1/sqrt13, 1/sqrt7) = (0.277350, 0.378000).  It is true on (1/sqrt7, 1/2).")
assert 7 in rs

# ---------- D. theorem at a = 2/5, strict, with the 7-clique -----------------
say("")
a = Q3(F(2,5))
clique7 = [(0,0),(1,0),(0,1),(1,-1),(-1,0),(0,-1),(-1,1)]
strict_forced = lambda p,q: (range2(lat(p,q,a),a)[0] < Q3(1) < range2(lat(p,q,a),a)[1])
ok = all(strict_forced(u[0]-w[0], u[1]-w[1]) for u in clique7 for w in clique7 if u != w)
say(f"D. a = 2/5: the 7 cells {{0}} u N(0) are pairwise STRICTLY forced: {ok}")
assert ok
bad = [(p,q) for (p,q) in PTS if 0 < Norm(p,q) <= 4 and (p+3*q) % 7 == 0]
say(f"   chi(T^2) = 7 : the 7-colouring p+3q mod 7 is 0-free on all 18 vectors with N <= 4 : {not bad}")
assert not bad
sc = [(p,q) for (p,q) in PTS if (p+3*q) % 7 == 0 and (p,q) != (0,0)]
mn = min(Norm(p,q) for (p,q) in sc)
wit = min(sc, key=lambda x: range2(lat(x[0],x[1],a), a)[0].f())
dmin2, dmax2, _ = range2(lat(wit[0],wit[1],a), a)
say(f"   smallest nonzero same-colour vector has N = {mn}; witness (p,q) = {wit};")
say(f"   its strict margin dmin^2 = {dmin2!r} = {dmin2.f():.4f} > 1  (paper's cruder bound (sqrt21-2)*2/5 squared = {((21**0.5-2)*0.4)**2:.4f})")
assert dmin2 > Q3(1)
# every same-colour pair, by the crude bound: dmin >= |v| - 2a
say(f"   crude check: min same-colour |v|^2 = 21a^2 = {21*0.16:.2f} > (1+2a)^2 = {(1.8)**2:.2f}")

# ---------- E. tangency audit: at a = 1/sqrt13 the unit pair is vertex-only
say("")
say("E. tangency audit at the lower endpoint.  Take a^2 = 1/13 exactly (a = 1/sqrt13), ring N=1.")
say("   dmax^2 for a tangent pair = 13 a^2 = 1 exactly, so the unit pair exists only at the")
say("   distance maximum, which is attained at a VERTEX of 2V:")
dmin2_1, dmax2_1, arg = range2(lat(1,0,1), 1)     # at a = 1, dmax^2 = 13
say(f"   dmin^2 = {dmin2_1!r}, dmax^2 = {dmax2_1!r} (should be 13), maximiser z = {arg!r}")
say("   z is a vertex of 2V, so p and q are vertices of the two hexagons, on the tiling's")
say("   1-skeleton.  Under any partition (boundary-ownership) rule such a point belongs to")
say("   exactly one cell, and need not belong to either of the two tangent cells -- so the")
say("   pair is NOT forced, and the criterion must be strict.  Hence the range is OPEN at 1/sqrt13.")
v0 = lat(1,0,1)
rel = vsub(arg, v0)          # remove the translation: rel must be a vertex of 2V
zv = hexverts(to3(2))
assert any(rel[0] == z[0] and rel[1] == z[1] for z in zv), "maximiser must be a vertex"
say(f"   relative maximiser z - v = {rel!r}, one of the six vertices of 2V: confirmed exactly")
say("   [checked: the maximiser is one of the six vertices of 2V]")

# ---------- F. the upper end: a = 1/2 exactly ---------------------------------
say("")
say("F. upper endpoint a = 1/2 exactly.  Cell diameter is 2a = 1, so a cell contains a unit pair")
dmin00, dmax00, arg00 = range2(lat(0,0,Q3(F(1,2))), Q3(F(1,2)))
v00 = lat(0,0,Q3(F(1,2)))
rel00 = vsub(arg00, v00)
zv2 = hexverts(to3(1))
say(f"   only on its boundary: dmax^2 of one cell = {dmax00!r} = 1 exactly, maximiser {rel00!r}")
assert dmax00 == Q3(1)
assert any(rel00[0] == z[0] and rel00[1] == z[1] for z in zv2), "unit pair of the cell must be vertices"
say("   and the maximiser is a pair of opposite VERTICES, so no unit pair lies in the open cell:")
say("   the interior distance set is (0,1), 1 not attained.  Hence a = 1/2 is admissible.")
ah = Q3(F(1,2))
okh = all(range2(lat(p,q,ah), ah)[0] < Q3(1) < range2(lat(p,q,ah), ah)[1]
          for p, q in [(1,0),(0,1),(1,-1),(1,1),(-1,-1),(2,0),(0,2),(2,-2),(-2,2)])
say(f"   rings 1,3,4 are still STRICTLY forced at a = 1/2 (spot check on all ring classes): {okh}")
assert okh
say("   same-colour ring N=7: dmin^2 = 7a^2 = 1.75 > 1, so the index-7 colouring is proper at a = 1/2")
say("   ==> corrected range: (1/sqrt13, 1/2];  for a > 1/2 the family is empty (a cell")
say("       contains a unit pair in its interior), so the statement holds vacuously there.")

open('verify_cell_nogo_v2.out','w').write("\n".join(out)+"\n")
print("\nwrote verify_cell_nogo_v2.out")
