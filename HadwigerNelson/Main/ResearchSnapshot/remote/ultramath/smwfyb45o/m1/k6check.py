from fractions import Fraction as F
from tri_tiling import U, D, shifted, poly_pair
# the 6 triangles of the tiling that contain the lattice vertex 0
cells = [(0,(0,0)), (1,(-1,0)), (0,(-1,0)), (1,(0,-1)), (0,(0,-1)), (1,(-1,-1))]
lo, hi = F(0), None
print("pair : dmin^2, dmax^2 (lattice units), forced iff 1/dmax^2 <= l^2 <= 1/dmin^2")
for i in range(6):
    for j in range(i+1,6):
        (t1,v1),(t2,v2) = cells[i], cells[j]
        P = U if t1==0 else D
        Q = U if t2==0 else D
        w = (v1[0]-v2[0], v1[1]-v2[1])
        dmn,dmx = poly_pair(P, shifted(Q,(F(w[0]),F(w[1]))))
        assert dmn == 0, (i,j,dmn)
        lo = max(lo, 1/dmx)
        print(" %d%d  dmin2=%s dmax2=%s   l^2 >= %s" % (i,j,dmn,dmx,1/dmx))
print("K_6 valid for all l^2 >= %s (=1/3 iff 3l^2>=1), decimal %s" % (lo, float(lo)))
