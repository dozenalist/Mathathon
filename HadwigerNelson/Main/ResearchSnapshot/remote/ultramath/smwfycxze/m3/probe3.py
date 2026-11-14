from hexgeo import *
from fractions import Fraction as F
import math

def f3(q): return float(q.a) + float(q.b)*math.sqrt(3.0)

p0 = (Q3(F(1,55)), Q3(F(18,55)))

# slack_c(p) = min over hexagons of colour c of max(d_min - 1, 1 - d_max)
def slacks(p, MR=3):
    out = {}
    for m in range(-MR,MR+1):
        for n in range(-MR,MR+1):
            c = colour(m,n)
            dmin = math.sqrt(f3(point_hex_sqdist(p,m,n)))
            dmax = math.sqrt(f3(point_hex_sqfar(p,m,n)))
            s = max(dmin-1.0, 1.0-dmax)
            if c not in out or s < out[c]:
                out[c] = s
    return out

s = slacks(p0)
print("slacks at p0 (positive = colour absent from annulus of that half-width):")
for c in sorted(s): print("  colour",c,"slack %.9f"%s[c])
vals = sorted(s.values(), reverse=True)
print("sorted slacks:", ["%.9f"%v for v in vals])
print("3rd largest =", "%.9f"%vals[2], "-> max eps for 3 absent =", "%.9f"%vals[2])
print("max square side ell = eps*sqrt2 =", "%.9f"%(vals[2]*math.sqrt(2)))
print("4th largest =", "%.9f"%vals[3], "-> max eps for 4 absent")
