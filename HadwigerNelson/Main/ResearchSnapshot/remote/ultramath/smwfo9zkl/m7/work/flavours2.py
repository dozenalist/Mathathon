"""2-periodic sector palette systems at a four-cycle centre, k=6: a type is an ordered pair
(P,Q) of disjoint admissible palettes (P on the even sectors, Q on the odd ones).  Then
(5.7) holds, (5.2) holds, and the K_3 mechanism is silent iff |P|+|Q| <= k-3 whenever P,Q are
disjoint -- i.e. iff P cap Q = empty forces one of them to be a singleton.  Compatibility of
two types (the (5.3) constraint at distance 1) is componentwise disjointness."""
from itertools import combinations
k=6; edges=[frozenset({i,(i+1)%4}) for i in range(4)]
adm=[]
for sz in range(1,k-2):
    for p in combinations(range(k),sz):
        p=frozenset(p)
        if not any(p<=e for e in edges): adm.append(p)
adm.sort(key=lambda s:(len(s),sorted(s)))
print("admissible palettes at a four-cycle centre, k=6:", len(adm))
types=[]
for P in adm:
    for Q in adm:
        if P & Q: continue
        if len(P)+len(Q) > k-3: continue      # mechanism must be silent
        types.append((P,Q))
print("2-periodic types (P even, Q odd):", len(types))
def compat(a,b):
    return not (a[0]&b[0]) and not (a[1]&b[1])
def hom(n, pairs):
    order=sorted(range(n), key=lambda c:-sum(1 for p in pairs if c in p))
    asg={}
    def rec(t):
        if t==n: return True
        c=order[t]
        for ty in types:
            if all(compat(ty, asg[d]) for (p,q) in pairs
                   for d in ((q,) if p==c else (p,) if q==c else ()) if d in asg):
                asg[c]=ty
                if rec(t+1): return True
                del asg[c]
        return False
    return (rec(0), dict(asg))
moser=[(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(3,5),(4,5),(4,6),(5,6),(0,6)]   # chi = 4
tests=[("K_3 of centres",3,[(0,1),(1,2),(0,2)]),
       ("4-cycle of centres",4,[(0,1),(1,2),(2,3),(3,0)]),
       ("5-cycle of centres",5,[(0,1),(1,2),(2,3),(3,4),(4,0)]),
       ("Moser spindle (7 vertices, chi=4)",7,moser)]
for name,n,prs in tests:
    sat,asg=hom(n,prs)
    print(f"\n{name}: {'SAT' if sat else 'UNSAT'} within the 2-periodic class")
    if sat:
        for c in sorted(asg): print("   centre",c,": even",sorted(asg[c][0])," odd",sorted(asg[c][1]))
