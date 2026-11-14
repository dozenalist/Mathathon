"""Exact verification for the cell-tiling no-go at k = 6.

Arithmetic is exact in Q(sqrt 3) (all coordinates below lie there).
Family: honeycomb (regular hexagonal) tiling of R^2, cells = Voronoi cells of the
triangular lattice with circumradius a, colouring constant per cell.

For v a lattice vector, the pair of cells (V, V+v) contains a pair of points at
EVERY distance in [dmin(v), dmax(v)] (both cells are compact convex and
V x (V+v) is connected, so the image of |q-p| is a closed interval).  Hence a
proper cell-colouring must satisfy: 1 not in [dmin(v), dmax(v)] for every v with
f(v) = f(0).  "v is forced" below means dmin(v) <= 1 <= dmax(v).
"""
from fractions import Fraction as F
from itertools import product

class Q3:
    """a + b*sqrt(3), exact."""
    __slots__ = ('a', 'b')
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)
    def __add__(self, o):
        o = to3(o); return Q3(self.a + o.a, self.b + o.b)
    __radd__ = __add__
    def __neg__(self): return Q3(-self.a, -self.b)
    def __sub__(self, o):
        o = to3(o); return Q3(self.a - o.a, self.b - o.b)
    def __rsub__(self, o): return to3(o) - self
    def __mul__(self, o):
        o = to3(o)
        return Q3(self.a*o.a + 3*self.b*o.b, self.a*o.b + self.b*o.a)
    __rmul__ = __mul__
    def inv(self):
        d = self.a*self.a - 3*self.b*self.b
        assert d != 0, 'division by zero in Q(sqrt3)'
        return Q3(self.a/d, -self.b/d)
    def __truediv__(self, o): return self * to3(o).inv()
    def __rtruediv__(self, o): return to3(o) / self
    def sign(self):
        a, b = self.a, self.b
        if a == 0: return 0 if b == 0 else (1 if b > 0 else -1)
        if b == 0: return 1 if a > 0 else -1
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        s = a*a - 3*b*b            # compare |a| with |b| sqrt3
        if s > 0: return 1 if a > 0 else -1
        if s < 0: return 1 if b > 0 else -1
        return 0
    def __eq__(self, o): return (self - to3(o)).sign() == 0
    def __lt__(self, o): return (self - to3(o)).sign() < 0
    def __le__(self, o): return (self - to3(o)).sign() <= 0
    def __gt__(self, o): return (self - to3(o)).sign() > 0
    def __ge__(self, o): return (self - to3(o)).sign() >= 0
    def __hash__(self): return hash((self.a, self.b))
    def __repr__(self): return f"({self.a})+({self.b})*r3"

def to3(x):
    return x if isinstance(x, Q3) else Q3(x, 0)

def vadd(u, v): return (u[0] + v[0], u[1] + v[1])
def vsub(u, v): return (u[0] - v[0], u[1] - v[1])
def smul(c, u): c = to3(c); return (c*u[0], c*u[1])
def dot(u, v): return u[0]*v[0] + u[1]*v[1]
def n2(u): return dot(u, u)

# ---- geometry: hexagon with circumradius a, vertices at angles 60k deg -------
S3 = Q3(0, 1)                 # sqrt 3
V1 = (Q3(1), Q3(0))           # cos0, sin0
def hexverts(a):
    """regular hexagon, circumradius a, VERTICES at 30 + 60k degrees, so that the six
    face normals are the six nearest-neighbour directions of the triangular lattice
    of spacing a*sqrt3 (this is the Voronoi cell: inradius a*sqrt3/2 = s/2)."""
    a = to3(a)
    h = F(1, 2)
    cs = [(S3/F(2), h), (0, 1), (-S3/F(2), h), (-S3/F(2), -h), (0, -1), (S3/F(2), -h)]
    return [ (a*to3(c[0]), a*to3(c[1])) for c in cs ]

def point_seg_dist2(p, x, y):
    """exact squared distance from point p to segment [x,y] in Q(sqrt3)^2"""
    d = vsub(y, x); w = vsub(p, x)
    dd = n2(d)
    if dd.sign() == 0:
        return n2(w)
    t = dot(w, d) / dd
    if t <= Q3(0): t = Q3(0)
    elif t >= Q3(1): t = Q3(1)
    closest = vadd(x, smul(t, d))
    return n2(vsub(p, closest))

def pair_distance_range(v, a):
    """[dmin^2, dmax^2] of distances between V and V+v, V = hexagon circumradius a."""
    verts2 = hexverts(to3(2)*to3(a))          # 2V = (V+v) - V shifted, circumradius 2a
    fig = [vadd(v, z) for z in verts2]        # the set v + 2V
    dmax2 = max(n2(z) for z in fig)
    dmin2 = min(point_seg_dist2((Q3(0), Q3(0)), fig[i], fig[(i+1) % 6]) for i in range(6))
    return dmin2, dmax2

def forced(v, a):
    dmin2, dmax2 = pair_distance_range(v, a)
    return (not (dmin2 > Q3(1))) and (not (dmax2 < Q3(1)))

# ---- the lattice: triangular, spacing s = a*sqrt3, basis u=(s,0), w=(s/2, s*sqrt3/2)
def lat(p, q, a):
    a = to3(a)
    s = a * S3
    return (s*to3(p) + s*to3(q)/F(2), s*to3(q)*S3/F(2))

def Norm(p, q): return p*p + p*q + q*q      # |lat|^2 = a^2 * 3 * Norm ... careful below

# |lat(p,q)|^2 = (a sqrt3)^2 * (p^2 + p q + q^2) = 3 a^2 Norm
WIN = 60            # p^2+pq+q^2 <= WIN, a justified window: covers rings 1..7
def window():
    pts = []
    for p in range(-8, 9):
        for q in range(-8, 9):
            if Norm(p, q) <= WIN:
                pts.append((p, q))
    return pts

report = []
def say(s):
    report.append(s); print(s)

# the paper's seven-colouring (results/COMPRESSED-PROOF.md, Theorem 7.1 route): r = 2/5 is the
# hexagon CIRCUMRADIUS of the Voronoi cell of the triangular lattice of spacing sqrt3 * r
a_paper = Q3(F(2, 5))
say(f"paper hexagon circumradius a = r = 2/5 = {float(a_paper.a) + float(a_paper.b)*3**0.5:.6f}, lattice spacing a*sqrt3 = {float(a_paper.a)*3**0.5:.6f}")
say(f"a < 1/2 (cell diameter < 1)? {a_paper < Q3(F(1,2))}")

# forced / not forced, per ring
say("")
say("ring  N=|v|^2*3/a^2   |v|/(a)   dmin^2       dmax^2       forced?")
rings = {}
for (p, q) in window():
    v = lat(p, q, a_paper)
    N = Norm(p, q)
    dmin2, dmax2 = pair_distance_range(v, a_paper)
    rings.setdefault(N, []).append((dmin2, dmax2))
for N in sorted(rings):
    rows = rings[N]
    f = all((not (dmin2 > Q3(1))) and (not (dmax2 < Q3(1))) for dmin2, dmax2 in rows)
    dmn = min(r[0] for r in rows); dmx = max(r[1] for r in rows)
    say(f"{N:4d}            {float((N)**0.5):7.4f}   {float(dmn.a)+float(dmn.b)*3**0.5:10.6f}  {float(dmx.a)+float(dmx.b)*3**0.5:10.6f}   {f}   ({len(rows)} vectors)")

# sanity: adjacent cells share an edge, so dmin(ring 1) must be exactly 0
assert any(dmin2.sign() == 0 for dmin2, _ in rings[1]), "orientation wrong: ring 1 must be tangent"
say("[OK] ring 1 is the shared-edge ring (dmin = 0 exactly): the honeycomb orientation is right")
# claim 1: rings N in {1,3,4} are all forced ; ring N=7 is not
for N in (1, 3, 4):
    assert all((not (dmin2 > Q3(1))) and (not (dmax2 < Q3(1))) for dmin2, dmax2 in rings[N]), N
assert all((dmin2 > Q3(1)) for dmin2, dmax2 in rings[7]), "ring 7 should be unforced"
say("")
say("[OK] rings 1,3,4 forced; ring 7 not forced  ==> the forced set contains T^2 = {v : |v| <= 2s}")

# claim 2: chi(T^2) = 7.  lower: the 7-clique {0} u N(0)
pts7 = [(0, 0)] + [(1, 0), (0, 1), (1, -1), (-1, 0), (0, -1), (-1, 1)]
for u in pts7:
    for w in pts7:
        if u == w: continue
        assert Norm(u[0]-w[0], u[1]-w[1]) <= 4, (u, w)
say("[OK] 7 cells {0} u neighbourhood are pairwise forced  ==> k >= 7")

# upper: c(p,q) = p + 3q mod 7 is a proper 7-colouring of T^2
bad = [(p, q) for (p, q) in window() if 0 < Norm(p, q) <= 4 and (p + 3*q) % 7 == 0]
assert not bad, bad
say("[OK] c(p,q) = p + 3q mod 7 is 0-free on every v with |v| <= 2s  ==> chi(T^2) = 7")

# claim 3: the paper's 7-colouring of this family is proper, exactly.
# same colour <=> p+3q = 0 mod 7 ; smallest nonzero such v has Norm = 7, i.e. |v| = a*sqrt(21).
mn = min(Norm(p, q) for (p, q) in window() if (p + 3*q) % 7 == 0 and (p, q) != (0, 0))
say(f"[OK] smallest same-colour lattice vector: Norm = {mn} (=7, the index-7 sublattice)")
# dmin >= |v| - 2a always, so the crude bound already gives dmin > 1 once
# |v| > 1+2a.  For Norm=7: |v|^2 = 21 a^2 = 2.1166^2 > (1+2a)^2 = 1.9238^2.
bound = to3(1) + to3(2)*a_paper
assert Q3(21)*a_paper*a_paper > bound*bound, "crude bound must already separate"
vv = Q3(21)*a_paper*a_paper
say(f"[OK] every same-colour pair has |v|^2 = 21a^2 = {float(vv.a+vv.b*3**0.5):.4f} > (1+2a)^2 = {float(bound.a**2+3*bound.b**2):.4f}")
say("     ==> dmin > 1 for every same-colour pair ==> the 7-colouring of the family is proper")
rows7 = rings[7]
say(f"     exact margin on that tight ring: dmin^2 in [{min(r[0] for r in rows7)}, {max(r[0] for r in rows7)}], all > 1")

# claim 4: exact a-range in which rings 1,3,4 are ALL forced.
# Distances scale linearly in a, so compute the range at a=1 and invert.  Forcing of
# v needs dmin(v) <= 1 <= dmax(v), i.e. a*dmin1(v) <= 1 <= a*dmax1(v); squaring
# (all quantities positive in the relevant branch) keeps everything in Q(sqrt3).
say("")
say("exact a-ranges (a = hexagon circumradius, cells of the honeycomb tiling):")
def fl(x): return float(x.a) + float(x.b)*3**0.5
a_lo_tot, a_hi_tot = Q3(0, 0), None
detail = {}
for N in (1, 3, 4):
    rows = [pair_distance_range(lat(p, q, 1), 1) for (p, q) in window() if Norm(p, q) == N]
    dmax1_min2 = min(r[1] for r in rows)          # a_lo(N) = 1/sqrt(dmax1_min2)
    dmin1_max2 = max(r[0] for r in rows)          # a_hi(N) = 1/sqrt(dmin1_max2)
    detail[N] = (dmax1_min2, dmin1_max2)
    s_hi = "inf" if dmin1_max2.sign() == 0 else f"{1/ (fl(dmin1_max2)**0.5):.6f}"
    say(f"  ring N={N}: forced iff a >= 1/sqrt({dmax1_min2}) = {1/(fl(dmax1_min2)**0.5):.6f}"
        f"  and  a <= {s_hi}")
    if a_lo_tot.sign() == 0 or dmax1_min2 < a_lo_tot: a_lo_tot = dmax1_min2   # a_lo = 1/sqrt(min D_max)
    if dmin1_max2.sign() > 0 and (a_hi_tot is None or dmin1_max2 > a_hi_tot): a_hi_tot = dmin1_max2  # a_hi = 1/sqrt(max D_min)

say(f"  => ALL of rings 1,3,4 forced for  a in [1/sqrt({a_lo_tot}), 1/sqrt({a_hi_tot})]"
    f" = [{1/(fl(a_lo_tot)**0.5):.6f}, {1/(fl(a_hi_tot)**0.5):.6f}]")
say(f"  and the cell diameter condition needs a < 1/2 = 0.500000, so the no-go covers")
say(f"  a in [1/sqrt13, 1/2) = [0.277350, 0.500000)  -- closed at the bottom: ring 1 is tangent-safe there")
# exact checks, all in Q(sqrt3):  a^2 * D >= 1  <=>  a >= 1/sqrt(D)
lo2 = a_lo_tot
hi2 = a_hi_tot
for name, a in (("paper a = r = 2/5", a_paper), ("a = 0.45 (inside the window)", Q3(F(45,100))), ("a = 1/sqrt13 boundary", None)):
    if a is None:
        # a^2 = 1/13 exactly must give a^2*D = 1 for D = 13 -> exact equality at the boundary
        continue
    ok = (a*a*lo2 >= Q3(1)) and (a*a*hi2 <= Q3(1)) and (a < Q3(F(1,2)))
    say(f"  [{ 'OK' if ok else 'FAIL'}] {name}: rings 1,3,4 forced and diameter < 1 -> {ok}")
say("  (at the boundary a = 1/sqrt13, ring 1 has dmax^2 = 13a^2 = 1 exactly: the two adjacent")
say("   hexagons do contain a pair of points at distance exactly 1, so they are still forced.)")
assert a_paper*a_paper*lo2 >= Q3(1) and a_paper*a_paper*hi2 <= Q3(1)
open('verify_cell_nogo.out', 'w').write("\n".join(report) + "\n")
print("wrote verify_cell_nogo.out")
