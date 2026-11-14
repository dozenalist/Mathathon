from hexgeo import *
from fractions import Fraction as F
p0 = (Q3(F(1,55)), Q3(F(18,55)))
print("nearest_lattice(p0):", nearest_lattice(p0), "-> colour", colour(*nearest_lattice(p0)))
# sanity: a point in a known hexagon
q = (Q3(F(-1,2)), Q3(F(1,3)))
print("nearest_lattice(q):", nearest_lattice(q), "colour", colour(*nearest_lattice(q)))
# method 2 smoke test: colours on a small box around p0 (should be just 0)
box = (Q3(F(1,55))-Q3(F(1,1000)), Q3(F(1,55))+Q3(F(1,1000)), Q3(F(18,55))-Q3(F(1,1000)), Q3(F(18,55))+Q3(F(1,1000)))
hits = [(m,n,colour(m,n)) for m in range(-3,4) for n in range(-3,4) if box_hex_sqdist(box,m,n)==Q3(0)]
print("hexagons meeting the tiny box around p0:", hits)
