#!/usr/bin/env python3
"""
m7 / swarm smwfo9zkl / direction d7.
Exact verification for "The four-cycle stratum of Theorem 6.5 at k = 6".

Exact arithmetic only (fractions.Fraction, integers, sympy).  Run:
    python3 verify.py
A second, independently coded implementation is verify_indep.py; it recomputes
the same numbers by different methods (see section headers).

  A. constants of the Lemma 6.4 mechanism        (sympy, exact)
  B. admissible palettes at a cyclic centre      (enumeration)
  C. state-reduction threshold of section 6.3.1  (enumeration)
  D. which disjoint palette pairs trigger the K_3 mechanism (enumeration)
  E. the k=6 pointwise model at a four-cycle centre (explicit certificate)
  F. an explicit 6-colouring of a strip with four-cycle centres (exact proof by cases)
  G. exact areas of the transition sets at a corner (Gamma_x contains C_4)
"""
from fractions import Fraction as F
from itertools import combinations
import sympy as sp

def hdr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)

# --------------------------------------------------------------- A
hdr("A. Constants of the Lemma 6.4 mechanism (exact)")
gam = 2*sp.asin(1/(2*sp.sqrt(3)))
print("gamma := 2 arcsin(1/(2 sqrt 3))")
print("  cos(gamma)      =", sp.simplify(sp.cos(gam)), "   [paper: 5/6]  ok:",
      sp.simplify(sp.cos(gam)-sp.Rational(5,6))==0)
print("  sin(gamma)      =", sp.simplify(sp.sin(gam)), " = sqrt(11)/6 ?",
      sp.simplify(sp.sin(gam)-sp.sqrt(11)/6)==0)
print("  |1-exp(i gamma)|=", sp.simplify(2*sp.sin(gam/2)), " = 1/sqrt3 ?",
      sp.simplify(2*sp.sin(gam/2)-1/sp.sqrt(3))==0)
print("  triangle side   =", sp.simplify(2*sp.sin(sp.pi/3)*2*sp.sin(gam/2)),
      " = 1 ?", sp.simplify(2*sp.sin(sp.pi/3)*2*sp.sin(gam/2)-1)==0)
print("  gamma/pi irrational: gamma/pi rational => exp(i gamma) a root of unity =>")
print("  2cos(gamma)=5/3 a rational algebraic integer => an integer: contradiction.")
print("  summands nonparallel: angular difference pi+gamma is not a multiple of pi.")

# --------------------------------------------------------------- B
hdr("B. Admissible palettes at a centre whose Gamma_x contains a simple cycle")
def palettes(k, ell):
    edges=[frozenset({i,(i+1)%ell}) for i in range(ell)]
    out=[]
    for sz in range(1,k-2):                       # 1 <= |P| <= k-3
        for P in combinations(range(k), sz):
            P=frozenset(P)
            if any(P<=e for e in edges): continue  # paper (6.2)
            out.append(P)
    return out
for k in (5,6,7):
    for ell in range(3,k+1):
        P=palettes(k,ell)
        from collections import Counter
        sd=dict(sorted(Counter(len(p) for p in P).items()))
        sing=sorted([sorted(p) for p in P if len(p)==1])
        assert set().union(*[p for p in P if len(p)==1]) == set(range(k))-set(range(ell))
        print(f"  k={k} ell={ell}: |P|={len(P):3d}  size distribution {sd}"
              f"  singleton palettes (= outsider singletons) {sing}")

# --------------------------------------------------------------- C
hdr("C. The state-reduction threshold of section 6.3.1")
print("Four-cycle centre, cycle labels 0,1,2,3; state groups {X}, U={0,2}, V={1,3}.")
for k in (5,6,7):
    if k<5: continue
    T={0,1,2,3}; X=min(set(range(k))-T)
    groups={'{X}':frozenset({X}),'U':frozenset({0,2}),'V':frozenset({1,3})}
    P=palettes(k,4); amb=[]
    for Q in P:
        car=[n for n,g in groups.items() if g<=Q]
        if len(car)>=2: amb.append((sorted(Q),car))
    print(f"\n  k={k}: palette bound |P| <= k-3 = {k-3}; a palette carrying two state")
    print(f"         groups needs |P| >= |{{X}} u U| = 3.")
    print(f"         palettes carrying >=2 distinct groups: {len(amb)}")
    for a in amb[:4]: print("            ", a)
    print(f"         => the palette determines the state: {len(amb)==0}"
          f"   (equiv. 3 > k-3, i.e. k <= 5)")

# --------------------------------------------------------------- D
hdr("D. The K_3 mechanism and the disjoint-palette pairs that escape it")
print("""Mechanism (RESULT.md, Lemma 3): let G1,G2 be disjoint label groups occurring
in the palette at the directions exp(i(t+2j kappa)) and exp(i(t+pi+gamma+2j kappa))
for j=0,1,2, on a set of t of positive measure.  Then each of the three points
z_j = x + exp(i(t+2j kappa)) + exp(i(t+pi+gamma+2j kappa)) has density one of the
label set T = I \\ (G1 u G2), and the z_j form a unit equilateral triangle.
A proper colouring of that triangle needs 3 distinct labels, so |T| <= 2 is a
contradiction.  Hence  |G1| + |G2| >= k-2  is impossible.
At a centre where the palette map is 2-valued the angle condition is automatic
(2 kappa preserves the value, pi = 3 kappa flips it), so a 2-valued palette map
requires two DISJOINT palettes A,B with |A|+|B| <= k-3.""")
for k in (5,6):
    for ell in range(3,k+1):
        P=palettes(k,ell)
        pairs=[(P[i],P[j]) for i in range(len(P)) for j in range(i+1,len(P))
               if not (P[i]&P[j])]
        low=[(A,B) for A,B in pairs if len(A)+len(B) < k-2]
        print(f"\n  k={k} ell={ell}: disjoint palette pairs {len(pairs):3d};"
              f" escaping (|A|+|B| <= k-3 = {k-3}): {len(low)}")
        if 0 < len(low) <= 14:
            for A,B in low: print("       ",sorted(A),sorted(B)," sum",len(A)+len(B))
        if not low: print("        (none -> NO 2-valued palette map at this stratum)")

# --------------------------------------------------------------- E
hdr("E. The k=6 pointwise model at a four-cycle centre (satisfiability certificate)")
edges=[frozenset({i,(i+1)%4}) for i in range(4)]
I=frozenset(range(6)); X,Y=4,5
A=frozenset({X}); B=frozenset({0,2})
def adm(P): return 1<=len(P)<=3 and not any(P<=e for e in edges)
print("  values:",sorted(A),"(outsider singleton)",sorted(B),"(a diagonal)")
print("  palette bound           :",adm(A) and adm(B))
print("  (6.2) not inside an edge:",not any(A<=e or B<=e for e in edges))
print("  (5.7) A cap B = empty   :",not (A&B))
print("  (5.2) unions != I       :",(A|B)!=I and A!=I and B!=I)
print("  mechanism needs |A|+|B| >= k-2 = 4; here it is",len(A)+len(B),
      "-> silent:",len(A)+len(B)<4)
sec=[0,1,0,1,0,1]
print("  6-sector realisation (R advances the sector by one):")
print("    sectors 0,2,4 ->",sorted(A)," sectors 1,3,5 ->",sorted(B))
print("    P(e) cap P(Re) = empty on every sector:",
      all(not (A if sec[i]==0 else B) & (A if sec[(i+1)%6]==0 else B) for i in range(6)))
print("  => the pointwise system of 6.3.1 at k=6 is SATISFIABLE (and has 2 values)")
print("  => is 2-valued: yes.  Hence no pointwise argument at a four-cycle centre")
print("     at k=6 can exclude 2-valued palette maps.")

# --------------------------------------------------------------- F
hdr("F. An explicit proper measurable 6-colouring of a strip with four-cycle centres")
a=F(51,100); b=F(43,50); W=2*b
print(f"  cells [ia,(i+1)a) x [jb,(j+1)b), i in Z, j in {{0,1}}; colour (i mod 3, j)")
print(f"  a = {a}, b = {b}, strip width W = 2b = {W} = {float(W):.6f}")
print("  Same-colour pairs: x-diff in [3am-a,3am+a], y-diff in (-b,b).  By cases:")
print("   (the intervals are centred at 3am with half-width a, so they leave gaps:)")
print(f"    m = 0 : sup distance^2 = a^2+b^2      = {a*a+b*b}  < 1   : {a*a+b*b<1}")
print(f"    m = 1 : inf |x-diff| = 2a             = {2*a}   > 1   : {2*a>1}")
print(f"   |m|>=2 : inf |x-diff| >= 5a           = {5*a}   > 1   : {5*a>1}")
print("  => no two same-coloured points are at distance exactly 1: the colouring is proper.")
print("  Redundant exact scan over 81x81 periods (interval bounding boxes):")
def gap(lo1,hi1,lo2,hi2):
    if hi1<lo2: return lo2-hi1
    if hi2<lo1: return lo1-hi2
    return F(0)
def far(lo1,hi1,lo2,hi2):
    return max(abs(lo1-hi2),abs(hi1-lo2))
bad=0; R=40
for i in range(-R,R):
    for j in (0,1):
        for di in range(-R,R):
            for dj in (0,1):
                if (i%3,j)==(di%3,dj) and (i,j)!=(di,dj):
                    dxlo=gap(i*a,(i+1)*a,di*a,(di+1)*a); dxhi=far(i*a,(i+1)*a,di*a,(di+1)*a)
                    dylo=gap(j*b,(j+1)*b,dj*b,(dj+1)*b); dyhi=far(j*b,(j+1)*b,dj*b,(dj+1)*b)
                    if dxlo*dxlo+dylo*dylo<=1<=dxhi*dxhi+dyhi*dyhi: bad+=1
print(f"    same-colour cell pairs whose bounding box straddles the unit circle: {bad}")
print("  At a corner x=(ia,b) the four incident cells have colours")
cols=sorted({((di)%3,(dj)%2) for di in (-1,0) for dj in (-1,0)})
print("   ",cols," (4 distinct)")
print("  At a corner x=(ia,b) the four incident cells have four distinct colours, so")
print("  the four interfaces through x carry the four edges of a 4-cycle (section G).")

# --------------------------------------------------------------- G
hdr("G. Exact transition areas at a corner: the four edges of Gamma_x")
print("""  At the corner x=(ia,b), put B = B(x,rho) with 0<rho<=min(a,b).
  For h = (-t,0) with 0<t<<rho, the set {q : c(q)=(i,0), c(q+h)=(i-1,0)}
  inside B is  [ia,ia+t) x [b-rho,b)  up to null sets, of area t*min(rho,b).
  Hence  area(D_(i,0),(i-1,0)(B,h)) / |h| = min(rho,b) > 0  for every such h,
  so the limsup in Definition 6.1 is positive: that edge is present.
  The same computation in the other three quadrants gives the edges
      ((i-1)%3,0)-((i,0)),   ((i,0),((i,1))),   (((i,1)),((i-1)%3,1)),
      (((i-1)%3,1),((i-1)%3,0)),
  i.e. exactly a 4-cycle on the four colours.  Non-adjacent colour pairs have
  transition sets empty for all sufficiently small h (they meet only at x).
  Off the corners Gamma_x is empty (cell interior) or a single edge (interface).""")
print(f"  min(rho,b) for rho=b is {min(a,b)} = {float(min(a,b)):.6f} > 0.")
print("  Hence L = {(ia,b) : i in Z}: nonempty, locally finite.")
print("""
  LIMIT.  A palette at x is built from traces on circles of radius ~1 about x,
  so it needs the colouring on an annulus about x, hence on a set of width >= 2.
  The construction has W = 2b = 1.72 < sqrt(3) < 2.  For the rectangular family
  (p columns x q rows, p*q = 6, colour (i mod p, j mod q)) the four cases are:
    p=1 q=6 and p=2 q=3 : the x-difference intervals [p*a*m-a, p*a*m+a] have
      half-width a and consecutive centres at distance p*a; for p=1,2 they
      overlap or touch, so 1 lies in one of them for EVERY (a,b) and the
      colouring is improper.  No safe parameters exist.
    p=6 q=1 : W = b < sqrt(1-a^2) subject to 5a > 1, so W < 0.98.
    p=3 q=2 : m=1 gives [2a,4a]; safety requires 2a > 1 (then every |m|>=1 is
      safe) or 4a < 1 together with 16a^2+b^2 < 1 (then W < 6/5).  The first
      branch gives W = 2b < 2*sqrt(1-a^2) < sqrt(3), approached as a -> 1/2.
  So the family caps at sqrt(3) = 1.732 < 2: this route cannot reach a unit circle.
  More strongly: if EVERY strip were 6-colourable then every finite unit-distance
  graph would be 6-colourable (it fits in a strip of its own diameter), so by
  de Bruijn-Erdos chi(R^2) <= 6.  Deciding strip 6-colourability in general is
  therefore equivalent to chi(R^2) <= 6: the counterexample route at k=6 is not
  independent of the original problem.""")
print("\nEND of exact checks.")

# --------------------------------------------------------------- H
hdr("H. The two-centre constraint at k=6: a Moser-spindle configuration of four-cycle centres")
print("""Class: sector palette systems.  At each centre the palette map is constant on the six
sectors [j*kappa,(j+1)*kappa) of its R-orbit, values from the 33 admissible palettes.
Constraints at every centre: palette bound; (6.2) for the four cycle edges; (5.7)
(consecutive sectors disjoint); (5.2) (no two values with union I); and the K_3 mechanism
at the sector offsets 3 and 4 (a pair there that is disjoint must have |A|+|B| <= k-3).
Between two centres at distance exactly 1: the palettes at the same sector are disjoint
((5.3) with s = f, i.e. P_y(f) cap P_x(f) = empty).
The class is a SUBCLASS of all palette systems, so a model here is a model of the
constraint level itself.""")
admH=[frozenset(p) for sz in range(1,4) for p in combinations(range(6),sz)
      if not any(frozenset(p)<=e for e in [frozenset({i,(i+1)%4}) for i in range(4)])]
def disj(a,b): return not (a&b)
def ok_centre(seq):
    if any(not disj(seq[i],seq[(i+1)%6]) for i in range(6)): return False
    if any(len(seq[i]|seq[j])==6 for i in range(6) for j in range(i+1,6)): return False
    for i in range(6):
        for off in (3,4):
            a,b=seq[i],seq[(i+off)%6]
            if disj(a,b) and len(a)+len(b)>3: return False
    return True
F=frozenset
model={
 0:[F({4}),F({0,2}),F({4}),F({0,2}),F({4}),F({0,2})],
 1:[F({4}),F({0,2}),F({4}),F({0,2}),F({4}),F({0,2})],
}
# the 2-periodic flavours used (P on even sectors, Q on odd)
flav={0:(F({4}),F({0,2})), 1:(F({5}),F({1,3})), 2:(F({0,2}),F({4})),
      3:(F({4}),F({5})),     4:(F({5}),F({0,2})), 5:(F({0,2}),F({4})),
      6:(F({1,3}),F({5}))}
moser=[(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(3,5),(4,5),(4,6),(5,6),(0,6)]
seqs={c:(f[0],f[1])*3 for c,f in flav.items()}
print("\n  centre : even-sector palette   odd-sector palette")
for c in sorted(flav):
    print(f"    {c}    : {sorted(flav[c][0])}                    {sorted(flav[c][1])}")
allok=True
for c in sorted(seqs):
    good=ok_centre(seqs[c])
    allok&=good
    print(f"  centre {c}: admissible, (6.2), (5.7), (5.2), mechanism : {good}")
pairok=all(disj(flav[p][i],flav[q][i]) for (p,q) in moser for i in (0,1))
print("  all 11 Moser-spindle unit pairs have sector-wise disjoint palettes:", pairok)
print("  Moser spindle is 4-chromatic (verified by brute force over all 3-colourings):",
      not any(all(col[a]!=col[b] for a,b in moser)
              for col in __import__("itertools").product(range(3),repeat=7)))
print("  => the pointwise system TOGETHER WITH the distance-1 two-centre exclusion is")
print("     satisfiable at k=6 on a 4-chromatic unit-distance configuration of 7 four-cycle")
print("     centres.  Hence no argument from these constraints can give the k=6 four-cycle case.")
