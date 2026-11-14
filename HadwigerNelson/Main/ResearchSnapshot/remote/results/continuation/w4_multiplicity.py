import math
# W4: explicit multiplicity-3 cover of [-5,5]^2 with Euclidean mesh 2.
# Triangular lattice of spacing s, open disks of radius 1.
s = 1.2
r = 1.0
def centers(mmax=12):
    out=[]
    for m in range(-mmax,mmax+1):
        for n in range(-mmax,mmax+1):
            out.append((s*(m+n/2), s*(math.sqrt(3)/2)*n))
    return out
C = centers()
# 1. covering: every point of the plane is within s/sqrt3 of a lattice point
print("covering radius s/sqrt3 =", s/math.sqrt(3), "< r =", r, ":", s/math.sqrt(3) < r)
# 2. multiplicity: sample the square, count disks containing each point
worst=0; arg=None; hist={}
N=240
for i in range(N+1):
    x=-5+10*i/N
    for j in range(N+1):
        y=-5+10*j/N
        k=sum(1 for (a,b) in C if (x-a)**2+(y-b)**2 < r*r)
        hist[k]=hist.get(k,0)+1
        if k>worst: worst=k; arg=(x,y)
print("sampled multiplicities on [-5,5]^2:", dict(sorted(hist.items())))
print("max multiplicity:", worst, "at", arg)
print("diameter of each disk:", 2*r, "<= 2 :", 2*r <= 2)
# 3. the third nearest lattice point is at distance >= sqrt3 s/2
print("sqrt3*s/2 =", math.sqrt(3)*s/2, "> r =", r, ":", math.sqrt(3)*s/2 > r)
