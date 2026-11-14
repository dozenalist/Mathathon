from fractions import Fraction as F
from tri_tiling import U, D, shifted, poly_pair
# 7 cells certified at l^2=1/5: (type, offset)
cl = [(0,(0,0)),(0,(-3,0)),(0,(-3,2)),(0,(-1,-1)),(1,(-3,1)),(1,(-2,2)),(1,(0,1))]
lo, hi = F(0), None
for i in range(len(cl)):
    for j in range(i+1,len(cl)):
        (t1,v1),(t2,v2) = cl[i], cl[j]
        P = U if t1==0 else D
        Q = U if t2==0 else D
        w = (v1[0]-v2[0], v1[1]-v2[1])
        dmn,dmx = poly_pair(P, shifted(Q,(F(w[0]),F(w[1]))))
        # forced iff dmn*l^2 <= 1 <= dmx*l^2  <=> l^2 <= 1/dmn (if dmn>0) and l^2 >= 1/dmx
        if dmx>0: lo = max(lo, 1/dmx)
        if dmn>0:
            hi = 1/dmn if hi is None else min(hi, 1/dmn)
print("clique cells:", cl)
print("no proper 6-colouring for all l^2 in [%s, %s]" % (lo, hi))
print("decimal:", float(lo), float(hi))
# also the l^2=1/9 witness
cl2 = [(0,(0,0)),(0,(-4,0)),(0,(-4,2)),(0,(-2,-2)),(0,(-2,0)),(0,(-2,2)),(0,(0,-2))]
lo2, hi2 = F(0), None
for i in range(len(cl2)):
    for j in range(i+1,len(cl2)):
        w = (cl2[i][1][0]-cl2[j][1][0], cl2[i][1][1]-cl2[j][1][1])
        dmn,dmx = poly_pair(U, shifted(U,(F(w[0]),F(w[1]))))
        if dmx>0: lo2 = max(lo2, 1/dmx)
        if dmn>0: hi2 = 1/dmn if hi2 is None else min(hi2, 1/dmn)
print("all-U clique:", cl2, "-> no 6-colouring for l^2 in [%s, %s]" % (lo2, hi2), float(lo2), float(hi2))
