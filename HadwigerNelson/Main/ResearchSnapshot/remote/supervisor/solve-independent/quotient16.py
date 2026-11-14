"""SIX-colourability of ONE periodic quotient at a = 1/5: the period lattice 4Z^2 (index 16).
Everything exact in Q(sqrt3).  One process.  Produces a self-contained certificate.
Graph: vertices = cosets of 4Z^2 in Z^2 (16 of them, labelled by (p mod 4, q mod 4));
an edge between two distinct cosets iff some forced offset v lies in their difference class,
i.e. iff some pair of cells in those cosets can be at distance exactly 1 in their interiors."""
from fractions import Fraction as F
import json, itertools

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
    def invariant(self): return self.a*self.a - 3*self.b*self.b
    def inv(self):
        d = self.invariant(); assert d != 0
        return Q3(self.a/d, -self.b/d)
    def __truediv__(self, o): return self*to3(o).inv()
    def sign(self):
        a, b = self.a, self.b
        if a == 0: return 0 if b == 0 else (1 if b > 0 else -1)
        if b == 0: return 1 if a > 0 else -1
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        s = self.invariant()
        if s > 0: return 1 if a > 0 else -1
        if s < 0: return 1 if b > 0 else -1
        return 0
    def __eq__(self, o): return (self-to3(o)).sign() == 0
    def __lt__(self, o): return (self-to3(o)).sign() < 0
    def __gt__(self, o): return (self-to3(o)).sign() > 0
    def __le__(self, o): return (self-to3(o)).sign() <= 0
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
A = F(1,5)
def centre(p,q):
    s = to3(A)*S3
    return (s*to3(p)+s*to3(q)/2, s*to3(q)*S3/F(2))
def pair_range2(p,q):
    """exact (dmin^2, dmax^2) between cell (0,0) and cell (p,q)."""
    fig = [vadd(centre(p,q), z) for z in hexverts(to3(2)*A)]
    dmax2 = max(n2(z) for z in fig)
    dmin2 = min(pseg2((Q3(0),Q3(0)), fig[i], fig[(i+1)%6]) for i in range(6))
    return dmin2, dmax2
def Norm(p,q): return p*p+p*q+q*q
def forced(p,q):
    dmin2, dmax2 = pair_range2(p,q)
    return (dmin2 < Q3(1)) and (dmax2 > Q3(1))

rec = []
def say(s): rec.append(s); print(s)

say("=== a = 1/5, period 4Z^2 (index 16), 42 forced offsets, exact Q(sqrt3) ===")
say("")

# ---- 1. rigorous window: forced => |v| in (1-2a, 1+2a) = (0.6, 1.4) => 3 < N < 16.333 ----
say("[1] window bound (proof, no search truncation)")
say("    dmin >= |v| - 2a and dmax <= |v| + 2a with a = 1/5, and |v|^2 = 3a^2 N = 0.12 N:")
say("    dmin < 1 <= |v|+2a  =>  |v| > 0.6  =>  N > 3")
say("    dmax > 1 <= dmin-2a  =>  |v| < 1.4  =>  N < 16.3333")
say("    so F is contained in the vectors with N in {4,7,9,12,13,16}: a finite, explicit set.")
CAND = [(p,q) for p in range(-5,6) for q in range(-5,6) if 0 < Norm(p,q) <= 16]
Fset = [(p,q) for (p,q) in CAND if forced(p,q)]
Fset.sort()
byN = {}
for (p,q) in Fset: byN.setdefault(Norm(p,q), []).append((p,q))
say(f"    computed: |F| = {len(Fset)} ; by ring {[(N, len(v)) for N, v in sorted(byN.items())]}")
assert len(Fset) == 42
assert set(byN) == {4,7,9,12,13}
say("    [OK] matches the saved artifact forced_a1_5.out: |F| = 42, N in {4,7,9,12,13}, ring 16 empty")

# ---- 2. no self-loops: 4Z^2 meets F in nothing ----
say("")
say("[2] self-loops: a cycle at one vertex would kill the quotient outright")
NL = [ (p,q) for p in range(-8,9) for q in range(-8,9) if p%4==0 and q%4==0 and 0<Norm(p,q)<=64]
say(f"    multiples of 4 in the window: N values {sorted(set(Norm(p,q) for (p,q) in NL))}")
assert all(not forced(p,q) for (p,q) in NL)
say("    [OK] 4Z^2 meets F in nothing (all such norms are multiples of 16, and ring 16 is unforced)")

# ---- 3. connection set S = F mod 4 ----
S = sorted(set((p%4, q%4) for (p,q) in Fset))
say("")
say(f"[3] connection set S = F mod 4 : |S| = {len(S)} distinct residues")
say(f"    S = {S}")
G = [(p,q) for p in range(4) for q in range(4)]
NONZERO = [g for g in G if g != (0,0)]
say(f"    |(Z/4)^2 minus 0| = {len(NONZERO)}")
say(f"    S == all nonzero residues?  {set(S) == set(NONZERO)}")
say(f"    multiplicity: how many of the 42 offsets hit each residue: "
    f"{ {r: sum(1 for (p,q) in Fset if (p%4,q%4)==r) for r in S} }")
assert set(S) == set(NONZERO)
say("    ==> the quotient graph is COMPLETE on 16 vertices (K_16)")

# ---- 4. INDEPENDENT adjacency verification (does not use the F list at all) ----
say("")
say("[4] independent adjacency check: for each of the 120 unordered pairs of distinct cosets,")
say("    search the whole coset difference class for a vector that satisfies the strict")
say("    criterion directly (exact, no reference to the list F).")
edges = {}
missing = []
for c1, c2 in itertools.combinations(G, 2):
    d = (c1[0]-c2[0], c1[1]-c2[1])
    wit = None
    for w in itertools.product(range(-2,3), repeat=2):
        v = (d[0]+4*w[0], d[1]+4*w[1])
        if v == (0,0) or Norm(*v) > 16: continue
        if forced(v[0], v[1]): wit = v; break
    if wit is None: missing.append((c1,c2))
    else: edges[(c1,c2)] = wit
say(f"    pairs tested: {120} ; pairs WITHOUT a forced representative: {len(missing)}")
assert not missing
say("    [OK] every pair of distinct cosets is adjacent: the graph is K_16, verified independently")
# cross-check: the witnesses found are members of F and have the right residue
bad = [ (c1,c2,v) for (c1,c2),v in edges.items()
        if v not in Fset or (v[0]-c1[0]+c2[0]) % 4 != 0 or (v[1]-c1[1]+c2[1]) % 4 != 0 ]
say(f"    witness cross-checks (in F, correct residue class): failures = {len(bad)}")
assert not bad

# ---- 5. the decision ----
say("")
say("[5] decision for this period")
say("    K_16 needs 16 distinct colours, so the quotient admits NO 6-colouring.")
say("    Equivalently: any 6-colouring would put two of the 16 cosets in one colour class,")
say("    and that pair is adjacent, so their cells contain points at distance exactly 1.")
# bounded DSATUR/backtracking confirmation, symmetry breaking colour(0,0)=0
adj = {c: set() for c in G}
for (c1,c2) in edges: adj[c1].add(c2); adj[c2].add(c1)
order = sorted(G, key=lambda c: -len(adj[c]))
best = [0]
def dsat(colour, used):
    if len(colour) == len(G):
        best[0] = max(best[0], used); return True
    # DSATUR pick
    uncol = [c for c in G if c not in colour]
    nb = {c: len({colour[x] for x in adj[c] if x in colour}) for c in uncol}
    deg = {c: sum(1 for x in adj[c] if x in colour) for c in uncol}
    v = max(uncol, key=lambda c: (nb[c], deg[c], -c[0], -c[1]))
    for col in range(used + 1):          # symmetry breaking: no new colour beyond used+1
        if all(colour[x] != col for x in adj[v] if x in colour):
            colour[v] = col
            if dsat(colour, max(used, col+1)): return True
            del colour[v]
    return False
colour = {(0,0): 0}
ok16 = dsat(colour, 1)
say(f"    DSATUR with symmetry breaking, unlimited colours: 16-colourable = {ok16}, "
    f"colours found = {len(set(colour.values()))}")
CHI = len(set(colour.values()))
def six_check():
    """exhaustive 6-colouring attempt, symmetry broken: colour(0,0)=0"""
    col = {(0,0): 0}
    def rec_(v_list):
        if len(col) == len(v_list): return True
        v = v_list[len(col)]
        for c in range(6):
            if all(col.get(x) != c for x in adj[v]): 
                col[v] = c
                if rec_(v_list): return True
                del col[v]
        return False
    return rec_(order)
six = six_check()
say(f"    exhaustive 6-colouring attempt (symmetry broken): SAT = {six}")
assert not six and CHI == 16
say("    [OK] UNSAT at 6 colours.  Lower bound is a clique: 16 pairwise adjacent cosets.")
say("")
say("    chi(quotient) = 16 exactly (K_16).")

# ---- 6. scope ----
say("")
say("[6] scope of this UNSAT")
say("    * It excludes colourings constant on the cosets of 4Z^2 only, i.e. colourings with")
say("      period lattice containing 4Z^2.  It is NOT a statement about non-periodic colourings.")
say("      It is stronger than needed for the interiors: it fails before any boundary question,")
say("      so no ownership rule and no ring-3 tangency pair is involved.")
say("    * Combined with the previous block's theorem (index >= 16 at a = 1/5) and its complete")
say("      sublattice enumeration: index 16 has exactly ONE avoiding sublattice, 4Z^2 (31 upper-HNF")
say("      forms at index 16, 1 avoids F); indices 17 and 18 have NONE.  So every periodic proper")
say("      colouring at a = 1/5 has index >= 19.")
# re-verify the index-16/17/18 counts in-process
def hnfs(d):
    out = []
    for a_ in range(1, d+1):
        if d % a_: continue
        c_ = d//a_
        for b_ in range(c_): out.append((a_, b_, c_))
    return out
def in_lat(p, q, bas):
    a_, b_, c_ = bas
    if p % a_: return False
    return (q - (p//a_)*b_) % c_ == 0
def avoids(bas):
    return all(not (in_lat(p,q,bas) and forced(p,q))
               for p in range(-6,7) for q in range(-6,7) if 0 < Norm(p,q) <= 16)
for d in (16, 17, 18, 19):
    av = [b for b in hnfs(d) if avoids(b)]
    say(f"    index {d}: {len(hnfs(d))} sublattices, {len(av)} avoiding F  {av[:3]}")
say("")
say("CONCLUSION: the index-16 quotient (period 4Z^2) needs 16 colours; six colours are impossible")
say("there.  Nothing here bounds chi(R^2), and no other period was swept.")

cert = {
 "parameter": {"name": "a = 1/5", "a": "1/5", "cell": "regular hexagon, circumradius a, Voronoi cell of the triangular lattice of spacing a*sqrt3",
               "field": "Q(sqrt3), exact rational arithmetic, no floating point"},
 "criterion": "forced(p,q) iff dmin^2 < 1 < dmax^2 between cell (0,0) and cell (p,q) [strict, interior points]",
 "window_proof": "forced implies 3 < N <= 16 with N = p^2+pq+q^2, so the search over N <= 16 is complete",
 "forced_offsets": Fset,
 "forced_offsets_by_ring": {str(k): v for k, v in sorted(byN.items())},
 "period_lattice": {"lattice": "4Z x 4Z", "index": 16, "HNF": [4,0,4]},
 "self_loops": "none: 4Z^2 meets F in nothing",
 "connection_set_S": S,
 "quotient": {"vertices": 16, "edges": 120, "is_complete": True, "chi": 16,
              "edges_with_witness_offset": [{"cosets": [list(c1), list(c2)], "forced_offset": list(v)}
                                            for (c1,c2), v in sorted(edges.items())]},
 "decision": "UNSAT for 6 colours: the quotient is K_16",
 "scope": "period 4Z^2 only; not a whole-plane statement; boundary rules and tangency pairs not needed",
 "six_colouring_search": {"method": "DSATUR + exhaustive backtracking, symmetry broken by colour(0,0)=0", "result": "UNSAT"},
 "sublattice_counts": {str(d): {"total": len(hnfs(d)), "avoiding": len([b for b in hnfs(d) if avoids(b)])} for d in (16,17,18,19)}
}
open('quotient16_cert.json','w').write(json.dumps(cert, indent=1) + "\n")
open('quotient16.out','w').write("\n".join(rec) + "\n")
print("\nwrote quotient16_cert.json and quotient16.out")
