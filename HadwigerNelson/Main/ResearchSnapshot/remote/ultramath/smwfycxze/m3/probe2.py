from hexgeo import *
from fractions import Fraction as F

p0 = (Q3(F(1,55)), Q3(F(18,55)))
EPS = Q3(F(71,10000))

def absent_ok(Q, c, eps, MR=3):
    """True iff colour c is ABSENT from the closed annulus 1+-eps around EVERY point of Q.
    Q is a closed axis-parallel square given as (x0,x1,y0,y1) with Q3 coords.
    Uses: distance set from Q to hexagon H is the interval [dist(Q,H), maxdist(Q,H)] (both convex)."""
    lo = Q3(1)-eps; hi = Q3(1)+eps
    lo2 = lo*lo; hi2 = hi*hi
    x0,x1,y0,y1 = Q
    corners = [(x0,y0),(x1,y0),(x0,y1),(x1,y1)]
    for m in range(-MR, MR+1):
        for n in range(-MR, MR+1):
            if colour(m,n) != c: continue
            vs = verts(m,n)
            # min over p in Q, x in H of |x-p| = dist(Q,H): min over segment-pairs; simpler:
            # min over corners of dist(corner,H) is an upper bound; for exactness use convexity:
            # dist(Q,H) = min over x in H of dist(x,Q). Compute as min over H-edges of dist(edge,Q).
            dmin2 = min(seg_seg_sqdist(Q, vs[i], vs[(i+1)%6]) for i in range(6))
            if dmin2 > hi2:   # hexagon entirely beyond the outer circle for all p in Q
                continue
            dmax2 = max(sqdist(p, v) for p in corners for v in vs)
            if dmax2 < lo2:   # hexagon entirely inside the inner circle for all p in Q
                continue
            return False
    return True

def seg_seg_sqdist(Q, a, b):
    """exact squared distance between segment ab and square Q (both convex closed)."""
    x0,x1,y0,y1 = Q
    Qc = [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
    # min over Q-edges vs ab: minimum of two segment-segment distances (or containment)
    if point_in_segbox_min(a) or point_in_segbox_min(b):
        pass
    qd = [seg_sqdist(p, a, b) for p in Qc]
    hd = [seg_sqdist(a, Qc[i], Qc[(i+1)%4]) for i in range(4)]
    hd += [seg_sqdist(b, Qc[i], Qc[(i+1)%4]) for i in range(4)]
    # also interior overlap / crossing cases: if segments intersect, distance 0
    for i in range(4):
        if segs_intersect(a,b,Qc[i],Qc[(i+1)%4]):
            return Q3(0)
    return min(min(qd), min(hd))

def point_in_segbox_min(p):
    return False

def segs_intersect(a,b,c,d):
    def cr(o,p,q):
        return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
    d1 = sign_q3(cr(c,d,a)); d2 = sign_q3(cr(c,d,b))
    d3 = sign_q3(cr(a,b,c)); d4 = sign_q3(cr(a,b,d))
    if d1*d2 < 0 and d3*d4 < 0: return True
    return False

# (i) open good square around p0: find maximal rational half width
for hw in [F(1,200),F(1,100),F(1,50),F(1,25),F(1,10),F(1,5)]:
    Q = (p0[0]-Q3(hw), p0[0]+Q3(hw), p0[1]-Q3(hw), p0[1]+Q3(hw))
    absent = [c for c in range(7) if absent_ok(Q, c, EPS)]
    print("halfwidth", hw, "absent colours on whole square:", absent)
