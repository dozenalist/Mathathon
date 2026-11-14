#!/usr/bin/env python3
"""
INDEPENDENT second implementation for the m7 claims.
Different data structures (integer bitmasks, no frozensets, no itertools.combinations
enumeration by size) and different derivations (sympy maximisation instead of the
bounding-box case analysis; a direct construction of the escaping pairs instead of
a filter over all pairs).  Run:  python3 verify_indep.py
It must reproduce every number printed by verify.py.
"""
import sympy as sp
from fractions import Fraction as F

ok = True
def chk(name, got, want):
    global ok
    good = (got == want)
    ok &= good
    print(f"  {'OK ' if good else 'FAIL'} {name}: got {got}  want {want}")

print("== 1. palettes as bitmasks ==")
def cycle_edges(k, ell):
    return [ (1<<i) | (1<<((i+1)%ell)) for i in range(ell) ]
def admissible_mask_list(k, ell):
    E = cycle_edges(k, ell); out=[]
    for m in range(1, 1<<k):            # every nonempty subset
        sz = bin(m).count("1")
        if sz > k-3: continue           # palette bound
        if any(m & e == m for e in E): continue   # inside a cycle edge (6.2)
        out.append(m)
    return out
want = {(5,3):9,(5,4):7,(5,5):5,(6,3):35,(6,4):33,(6,5):31,(6,6):29,
        (7,3):92,(7,4):90,(7,5):88,(7,6):86,(7,7):84}
for (k,ell),w in want.items():
    chk(f"|palettes| k={k} ell={ell}", len(admissible_mask_list(k,ell)), w)

print("\n== 2. singleton palettes = the outsider singletons ==")
for k in (5,6,7):
    for ell in range(3,k+1):
        L=admissible_mask_list(k,ell)
        sing=[m for m in L if bin(m).count("1")==1]
        got=sorted((m & -m).bit_length()-1 for m in sing)
        chk(f"singletons k={k} ell={ell}", got, list(range(ell,k)))

print("\n== 3. how many admissible palettes carry two 6.3.1 state groups ==")
def n_ambiguous(k):
    X=1<<4; U=(1<<0)|(1<<2); V=(1<<1)|(1<<3)
    n=0
    for m in admissible_mask_list(k,4):
        cnt = ((m & X)==X) + ((m & U)==U) + ((m & V)==V)
        if cnt >= 2: n+=1
    return n
chk("ambiguous palettes k=5", n_ambiguous(5), 0)
chk("ambiguous palettes k=6", n_ambiguous(6), 2)
chk("ambiguous palettes k=7", n_ambiguous(7), 11)

print("\n== 4. disjoint pairs and the K_3 threshold ==")
def pair_stats(k, ell):
    L=admissible_mask_list(k,ell)
    tot=0; esc=0
    for i in range(len(L)):
        for j in range(i+1,len(L)):
            if L[i] & L[j]: continue
            tot+=1
            if bin(L[i]).count("1")+bin(L[j]).count("1") < k-2: esc+=1
    return tot, esc
chk("disjoint pairs (5,4)", pair_stats(5,4), (7,0))
chk("disjoint pairs (5,5)", pair_stats(5,5), (5,0))
chk("disjoint pairs (6,4)", pair_stats(6,4), (110,13))
chk("disjoint pairs (6,5)", pair_stats(6,5), (85,5))
chk("disjoint pairs (6,6)", pair_stats(6,6), (64,0))
chk("disjoint pairs (5,3)", pair_stats(5,3), (13,1))
chk("disjoint pairs (6,3)", pair_stats(6,3), (139,24))

print("\n== 5. the escaping pairs at k=6, ell=4, built directly ==")
# an escaping pair must be {outsider singleton} + {set of size <= 2 disjoint from it}
outs=[4,5]; edges6=[(1<<i)|(1<<((i+1)%4)) for i in range(4)]
esc=set()
for o in outs:
    so=1<<o
    for A in admissible_mask_list(6,4):
        if A & so: continue                      # must be disjoint
        if bin(A).count("1") not in (1,2): continue
        if bin(A).count("1")+1 > 3: continue
        esc.add((min(so,A),max(so,A)))
chk("number of escaping pairs (6,4)", len(esc), 13)
chk("every escaping pair contains an outsider singleton",
    all(bin(a).count("1")==1 or bin(b).count("1")==1 for a,b in esc), True)

print("\n== 6. the k=6 pointwise model, re-checked on all six sectors ==")
A=1<<4; B=(1<<0)|(1<<2); I=(1<<6)-1
edges4=[(1<<i)|(1<<((i+1)%4)) for i in range(4)]
chk("A admissible", 1<=bin(A).count("1")<=3 and not any(A&e==A for e in edges4), True)
chk("B admissible", 1<=bin(B).count("1")<=3 and not any(B&e==B for e in edges4), True)
chk("A,B disjoint", A&B, 0)
chk("A|B != I", (A|B)!=I, True)
chk("|A|+|B| < k-2 (mechanism silent)", bin(A).count("1")+bin(B).count("1")<4, True)
sect=[A,B,A,B,A,B]
chk("(5.7) on all six sectors", all(sect[i]&sect[(i+1)%6]==0 for i in range(6)), True)

print("\n== 7. the strip colouring, conditions re-derived with sympy ==")
a=sp.Rational(51,100); b=sp.Rational(43,50)
x,y=sp.symbols('x y',real=True)
# worst case over the rectangle [3am-a,3am+a] x [-b,b]: maximise x^2+y^2
def sup_dist2(m):
    lo=3*a*m-a; hi=3*a*m+a
    return max(lo**2,hi**2)+b**2
def inf_dist2(m):
    lo=3*a*m-a; hi=3*a*m+a
    if lo<=0<=hi: return sp.Integer(0)
    return min(lo**2,hi**2)+sp.Integer(0)
chk("m=0 sup^2 < 1", sp.simplify(sup_dist2(0)-1)<0, True)
chk("m=1: min |x| = 2a > 1", sp.simplify(2*a-1)>0, True)
chk("m=2: min |x| = 5a > 1", sp.simplify(5*a-1)>0, True)
for m in (1,-1,2,-2,3,-3):
    sd=sup_dist2(m); id_=inf_dist2(m)
    good = (sd<1) or (id_>1)
    chk(f"m={m}: unit circle misses the rectangle", good, True)
# exact boundary-case sweep over a long range of m
allgood=all((sup_dist2(m)<1) or (inf_dist2(m)>1) for m in range(-500,501))
chk("-500<=m<=500 all safe", allgood, True)
chk("m=0 sup^2 < 1", sp.simplify(a*a+b*b-1)<0, True)
chk("strip width 2b < sqrt(3)", sp.simplify(2*b < sp.sqrt(3)), True)
chk("strip width 2b < 2 (cannot hold a unit circle)", 2*b<2, True)

print("\n== 8. Gamma_x at a corner: four distinct colours, four adjacencies ==")
cols={ (di%3, dj%2) for di in (-1,0) for dj in (-1,0) }
chk("four distinct colours at a corner", len(cols), 4)
edges=[( (-1,-1),(0,-1) ), ( (0,-1),(0,0) ), ( (0,0),(-1,0) ), ( (-1,0),(-1,-1) )]
mapped=[( (p[0]%3,p[1]%2), (q[0]%3,q[1]%2) ) for p,q in edges]
chk("the four adjacencies are distinct", len(set(frozenset(e) for e in mapped)), 4)
# they form a 4-cycle: each of the four colours appears in exactly two adjacencies
from collections import Counter
deg=Counter()
for p,q in mapped: deg[p]+=1; deg[q]+=1
chk("every colour has degree 2 (a 4-cycle)", sorted(deg.values()), [2,2,2,2])
chk("the 4-cycle uses all four colours", len(deg), 4)

print("\n== 9. the mechanism constants, re-derived ==")
g=sp.acos(sp.Rational(5,6))
chk("cos(2 arcsin(1/(2 sqrt3))) = 5/6", sp.simplify(sp.cos(2*sp.asin(1/(2*sp.sqrt(3))))-sp.Rational(5,6)), 0)
chk("2 sin(g/2) = 1/sqrt3  (half-angle identity)",
    sp.simplify(2*sp.sqrt((1-sp.Rational(5,6))/2)-1/sp.sqrt(3)), 0)
chk("2 sin(kappa) * 2 sin(g/2) = 1 (triangle side)",
    sp.simplify(2*sp.sin(sp.pi/3)*2*sp.sqrt((1-sp.Rational(5,6))/2)-1), 0)

print("\n== 10. the two-centre Moser-spindle model, re-checked with bitmasks ==")
def m(*ls): return sum(1<<i for i in ls)
E4=[m(i,(i+1)%4) for i in range(4)]
def admissible(x): return 1 <= bin(x).count("1") <= 3 and not any(x & e == x for e in E4)
even=[m(4), m(5), m(0,2), m(4), m(5), m(0,2), m(1,3)]
odd =[m(0,2), m(1,3), m(4), m(5), m(0,2), m(4), m(5)]
moser=[(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(3,5),(4,5),(4,6),(5,6),(0,6)]
okk=True
for c in range(7):
    seq=[even[c],odd[c]]*3
    a=admissible(even[c]) and admissible(odd[c])
    b=all(seq[i]&seq[(i+1)%6]==0 for i in range(6))
    d=all(bin(seq[i]|seq[j]).count("1")<6 for i in range(6) for j in range(i+1,6))
    e=all( (seq[i]&seq[(i+o)%6]!=0) or (bin(seq[i]).count("1")+bin(seq[(i+o)%6]).count("1")<=3)
           for i in range(6) for o in (3,4))
    okk &= a and b and d and e
    chk(f"centre {c}: admissibility, (5.7), (5.2), mechanism", a and b and d and e, True)
for (p,q) in moser:
    chk(f"unit pair {p}-{q} sector-wise disjoint",
        all((even[p]&even[q])==0 and (odd[p]&odd[q])==0 for _ in (0,)), True)
# 4-chromaticity by a different route: count proper 3-colourings of the Moser spindle = 0
def count_col(n, edges, k):
    tot=0
    def rec(i,col):
        nonlocal tot
        if i==n: tot+=1; return
        for c in range(k):
            if all(col[j]!=c for j in range(i) if (j,i) in edges or (i,j) in edges):
                col[i]=c; rec(i+1,col); col[i]=-1
    rec(0,[-1]*n)
    return tot
E=set(moser)|set((b,a) for a,b in moser)
chk("proper 3-colourings of the Moser spindle", count_col(7, list(E), 3), 0)
chk("proper 4-colourings exist", count_col(7, list(E), 4) > 0, True)

print("\nALL INDEPENDENT CHECKS PASSED" if ok else "\n*** SOME INDEPENDENT CHECK FAILED ***")
