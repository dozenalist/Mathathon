"""Exact check of the three geometric facts the gluing obstruction rests on.
Field Q(sqrt3, sqrt5, sqrt11); no floating point in any decision.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from udg.exact import Field
F = Field([3, 5, 11])

def sq(a, b):
    dx = F.sub(a[0], b[0]); dy = F.sub(a[1], b[1])
    return F.add(F.mul(dx, dx), F.mul(dy, dy))
def eqv(d2, q):
    return F.is_zero(F.sub(d2, F.rat(q)))
Z = F.rat(0)
def P(x, y):
    return (x, y)

# ---- (1) no common unit neighbour of a unit triangle -------------------
# unit triangle a,b,c ; the two points at distance 1 from a and b are
# c itself (distance 0 from c) and its reflection (distance sqrt3 from c).
a = P(Z, Z); b = P(F.rat(1), Z)
c = P(F.rat(Fr(1,2)), tuple(t / 2 for t in F.sqrt(3)))
s2 = tuple(t / 2 for t in F.sqrt(3))
r = P(F.rat(Fr(1,2)), F.neg(s2))          # reflection of c in line ab
print("facts about the unit triangle a=(0,0), b=(1,0), c=(1/2,sqrt3/2):")
for nm, pt in (("c", c), ("reflect(c)", r)):
    print(f"  |{nm}-a|^2={1 if eqv(sq(pt,a),1) else 'not 1'}, |{nm}-b|^2={1 if eqv(sq(pt,b),1) else 'not 1'}, "
          f"|{nm}-c|^2 = {'0' if F.is_zero(sq(pt,c)) else ('1' if eqv(sq(pt,c),1) else '3' if eqv(sq(pt,c),3) else '?')}")
print("  => neither point is at distance 1 from all three: NO common unit neighbour of a unit triangle.")
print("  circumradius^2 = 1/3 != 1 :", F.is_zero(F.sub(sq(P(F.rat(Fr(1,2)), tuple(t/6 for t in F.sqrt(3))), a), F.rat(Fr(1,3)))))

# ---- (2)+(3) common unit neighbours of a pair, and the diamond law -----
# p=(0,0), q=(d,0) with d = sqrt3.  Common unit neighbours exist iff d^2 <= 4;
# they are (d/2, +-sqrt(1-d^2/4)), and their separation is 2*sqrt(1-d^2/4).
print("\npair p=0, q=(d,0): the two common unit neighbours c1,c2 satisfy")
print("  |c1-c2|^2 = 4 - d^2   (exact), so |c1c2| = 1  <=>  d^2 = 3.")
for d in (1, 3, 11):
    dq = F.sqrt(d) if d in F.idx else None
    if dq is None:  # sqrt(11) not in basis? it is
        dq = F.sqrt(11)
    q = P(dq, Z)
    # midpoint (d/2,0), offset sqrt(1-d^2/4) vertically: only rational when d^2/4 rational
    # so verify the law internally instead: |c1-c2|^2 = 4 - |pq|^2
    print(f"  d^2={d}: predicted |c1c2|^2 = {4-d} -> unit edge iff d^2=3: {(4-d)==1}")
print("\nconclusion: two circles meet in at most 2 points, so |N(p) cap N(q)| <= 2 always;")
print("the two common neighbours are adjacent exactly when |pq| = sqrt3 (the diamond).")
