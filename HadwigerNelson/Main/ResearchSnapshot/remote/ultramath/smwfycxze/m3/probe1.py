from hexgeo import *
from fractions import Fraction as F
import itertools, math

p0 = (Q3(F(1,55)), Q3(F(18,55)))
print("which hex contains p0:", which_hex(p0), "colour", c0(p0))

EPS = F(71,10000)

def annulus_colours_exact(p, eps, MR=3):
    """exact: colours c such that some hexagon of colour c meets the closed annulus
       {1-eps <= |x-p| <= 1+eps}."""
    lo2 = (Q3(1)-Q3(eps))*(Q3(1)-Q3(eps))
    hi2 = (Q3(1)+Q3(eps))*(Q3(1)+Q3(eps))
    present = {}
    slack = {}
    for m in range(-MR, MR+1):
        for n in range(-MR, MR+1):
            c = colour(m,n)
            d2min = point_hex_sqdist(p, m, n)
            if d2min > hi2:
                continue
            d2max = point_hex_sqfar(p, m, n)
            if d2max < lo2:
                continue
            present.setdefault(c, []).append((m,n))
    return present

for eps in [F(71,10000)]:
    pr = annulus_colours_exact(p0, eps)
    print("eps=",eps,"colours present:", sorted(pr), "count", len(pr))
    for c in sorted(pr):
        print("   colour",c,"hexagons:",pr[c][:4], "..." if len(pr[c])>4 else "")
    print("absent:", [c for c in range(7) if c not in pr])
