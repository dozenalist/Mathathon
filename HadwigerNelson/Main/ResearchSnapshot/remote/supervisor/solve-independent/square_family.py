"""Square-cell family (cells = Voronoi cells of c*Z^2, colour constant per cell): exact check
that the forced set already contains a 7-clique at c = 3/5, so the family needs >= 7 colours there.
A clique of size m in the forced set forces at least m colours by the cell lemma."""
from fractions import Fraction as F

def ranges(p, q, c):
    dx = max(F(0), abs(p)*c - c); dy = max(F(0), abs(q)*c - c)
    return dx*dx + dy*dy, c*c*((abs(p)+1)**2 + (abs(q)+1)**2)

def forced(p, q, c):
    """STRICT criterion (v2): a partition needs dmin < 1 < dmax, equality endpoints are
    boundary-only and their colour is decided by the boundary rule, not by the cell."""
    dmin2, dmax2 = ranges(p, q, c)
    return dmin2 < 1 < dmax2

c = F(3, 5)
clique = [(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2)]
print(f"c = 3/5 = 0.6 ; cell diameter c*sqrt2 = {float(c)*2**0.5:.4f} < 1 : {float(c)*2**0.5 < 1}")
ok = True
for i, u in enumerate(clique):
    for w in clique[i+1:]:
        d = (u[0]-w[0], u[1]-w[1])
        f = forced(d[0], d[1], c)
        ok &= f
        print(f"  pair {u}-{w}: dmin^2={ranges(d[0],d[1],c)[0]}  dmax^2={ranges(d[0],d[1],c)[1]}  forced={f}")
print("\nALL 21 pairs forced:", ok, "==> square-cell colourings at c = 3/5 need >= 7 colours")
