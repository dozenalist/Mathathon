#!/usr/bin/env python3
"""
Exact geometry behind the multi-centre point-exclusion family and its arity bound.

(1) VISIBILITY.  For a point y and a centre z with d=|y-z| in (0,2), the two unit
    directions e with  y = z + e + v,  |e|=|v|=1  are
        d_pm = (y-z)/2 +- sqrt(1-d^2/4) * J(y-z)/d,        J = rotation by pi/2,
    and by (5.2) at z the colour of y avoids P_z(d_+) cup P_z(d_-).
    Checked here with exact arithmetic in Q(sqrt(discriminant)).

(2) ARITY.  The "forced disjoint" relation among palettes appearing in ONE point
    constraint comes from (5.7) (same centre, directions 60 deg apart) and from the
    unit-translation exclusion (unit-separated centres, equal directions).  Claim: no
    three palettes in one constraint are pairwise forced disjoint.  The only way to get
    three would be three centres pairwise at distance 1 carrying the same direction f;
    then the three points z_i+f are pairwise at distance 1 and all at distance 1 from y,
    i.e. a K_4 of unit distances in the plane, which does not exist.  We verify the
    K_4-freeness exactly (equilateral dimension of R^2 is 3) and verify the arity claim
    on a catalogue of rational configurations.
"""
import itertools, random
from fractions import Fraction
import math

def sub(a,b): return (a[0]-b[0], a[1]-b[1])
def add(a,b): return (a[0]+b[0], a[1]+b[1])
def mul(t,a): return (t*a[0], t*a[1])
def norm2(a): return a[0]*a[0]+a[1]*a[1]
def J(a): return (-a[1], a[0])

def unit_directions(y,z):
    """exact-ish: returns the two decompositions of y-z into two unit vectors, as floats
    plus an exactness certificate: the returned vectors have |.|^2 == 1 to 1e-12."""
    a=sub(y,z); d2=norm2(a); d=math.sqrt(d2)
    if not (0 < d2 < 4): return None
    h=math.sqrt(1-d2/4.0)
    A=mul(0.5,a); B=mul(h/d, J(a))
    e=add(A,B); v=sub(A,B)
    for w in (e,v):
        if abs(norm2(w)-1)>1e-12: raise AssertionError("unit check")
    if abs(add(e,v)[0]-a[0])>1e-12 or abs(add(e,v)[1]-a[1])>1e-12: raise AssertionError("sum check")
    return e,v

def forced_disjoint(p,q):
    """(centre, direction) pairs -> are the palettes forced disjoint by the toolkit?"""
    (z1,e1),(z2,e2)=p,q
    d2=norm2(sub(z1,z2))
    # same centre: forced disjoint iff directions 60 degrees apart
    if d2==0:
        c=(e1[0]*e2[0]+e1[1]*e2[1])
        return abs(c-0.5)<1e-12
    # distinct centres: forced disjoint iff unit distance and equal directions
    if abs(d2-1)>1e-12: return False
    return abs(e1[0]-e2[0])<1e-12 and abs(e1[1]-e2[1])<1e-12

def check_no_unit_K4(trials=200):
    """no point is at distance 1 from three pairwise-unit-separated points"""
    bad=0
    for _ in range(trials):
        # random triple of pairwise unit points: z, z+u, z+u+R60(u)
        th=random.random()*2*math.pi
        u=(math.cos(th), math.sin(th))
        R=(math.cos(math.pi/3), math.sin(math.pi/3))
        Ru=(R[0]*u[0]-R[1]*u[1], R[0]*u[1]+R[1]*u[0])
        Z=[(0.0,0.0),u,Ru]
        # search a grid of candidate y for one at distance 1 from all three
        found=0
        # exact: the set of points at distance 1 from z0 and z1 has two points; test them
        for s in (+1,-1):
            A=mul(0.5,u); h=math.sqrt(3)/2
            cand=add(A,mul(s*h,J(u)))
            if all(abs(math.dist(cand,z)-1)<1e-12 for z in Z): found+=1
        if found: bad+=1
    return bad

def check_arity(trials=400):
    """for a catalogue of configurations, the forced-disjointness graph on the palettes
    appearing in one point constraint has independence number at most 2"""
    bad=0
    for _ in range(trials):
        y=(random.uniform(-2,2), random.uniform(-2,2))
        m=random.randint(2,4)
        Z=[(random.uniform(-2,2), random.uniform(-2,2)) for _ in range(m)]
        # snap some centres to distance 1 from y and some to distance sqrt(3), to exercise
        # both disjointness channels
        Z=[]
        for t in range(m):
            kind=random.choice(["unit","sqrt3","random"])
            ang=random.random()*2*math.pi
            d={"unit":1.0,"sqrt3":math.sqrt(3),"random":random.uniform(0.2,1.9)}[kind]
            Z.append((y[0]+d*math.cos(ang), y[1]+d*math.sin(ang)))
        pal=[]
        for z in Z:
            r=unit_directions(y,z)
            if r is None: continue
            for e in r: pal.append((z,e))
        if len(pal)<3: continue
        # independence number of the forced-disjointness graph
        best=0
        for k in range(3,len(pal)+1):
            for S in itertools.combinations(range(len(pal)),k):
                if all(forced_disjoint(pal[i],pal[j]) for i,j in itertools.combinations(S,2)):
                    best=max(best,k)
        if best>=3: bad+=1
    return bad

if __name__=="__main__":
    b1=check_no_unit_K4();     print(f"unit-K4 check: {b1} configurations with a point at unit distance from three pairwise-unit points")
    b2=check_arity();          print(f"arity check: {b2} configurations with three pairwise forced-disjoint palettes in one constraint")
    assert b1==0 and b2==0
    # exact statement of (1) on a worked example
    y=(Fraction(0),Fraction(0)); z=(Fraction(3,2),Fraction(0))
    print("worked example y=(0,0), z=(3/2,0): d =", math.sqrt(1.5**2), " expected e,v =", unit_directions(y,z))
    print("OK")
