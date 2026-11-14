from hexgeo import *
from fractions import Fraction as F
import math, itertools

EPS = Q3(F(71,10000))
lo2 = (Q3(1)-EPS)*(Q3(1)-EPS); hi2 = (Q3(1)+EPS)*(Q3(1)+EPS)

def present_f(p, eps, MR=3):
    out=set()
    for m in range(-MR,MR+1):
        for n in range(-MR,MR+1):
            if point_hex_sqdist(p,m,n) <= hi2 and point_hex_sqfar(p,m,n) >= lo2:
                out.add(colour(m,n))
    return out

cands = []
for a in range(-16,17):
    for b in range(-16,17):
        p = (Q3(F(a,40)), Q3(F(b,40)))
        # inside the Voronoi hexagon of the origin?
        vs = HEX
        inside=True
        for k in range(6):
            A,B = vs[k], vs[(k+1)%6]
            e = (B[0]-A[0], B[1]-A[1])
            cr = e[0]*(p[1]-A[1]) - e[1]*(p[0]-A[0])
            if sign_q3(cr) < 0: inside=False;break
        if not inside: continue
        pr = present_f(p, EPS)
        cands.append((len(pr), p, sorted(pr)))
cands.sort(key=lambda t: -t[0])
print("points with the most colours present:")
seen=set()
for k,p,pr in cands[:12]:
    print("  colours present %d"%k, p, pr)
print("max present:", cands[0][0])
print("min present:", cands[-1][0])
