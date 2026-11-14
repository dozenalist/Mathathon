"""Palette sizes in the constructed colouring.
For a cell-constant colouring the maximal palette P_x(e) is the set of colours of the
colouring cells whose closure contains x+e (all traces are supported there), so it can be
computed by scanning a small neighbourhood of x+e."""
import math, random
Rr=0.4; d=math.sqrt(3)*Rr; s3=math.sqrt(3)
def c0(x,y):
    qq=complex(x,y); a=qq/d; b=2*a.imag/s3; aa=a.real+b/2
    m0=round(aa); n0=round(b); best=1e9; bm=bn=0
    for dm in(-1,0,1,2):
        for dn in(-1,0,1,2):
            m,n=m0+dm,n0+dn; z=d*(m+n*(-0.5+0.5j*s3)); dd=abs(qq-z)
            if dd<best: best=dd; bm,bn=m,n
    return (bm+2*bn)%7
def palette(px,py,delta=1e-4,n=64):
    s=set()
    for k in range(n):
        a=2*math.pi*k/n
        s.add(c0(px+delta*math.cos(a),py+delta*math.sin(a)))
    s.add(c0(px,py))
    return s
p0=(1/55,18/55); L=0.01
random.seed(7)
mx=0; hist={}
for _ in range(4000):
    x=p0[0]+L*random.uniform(-0.5,0.5); y=p0[1]+L*random.uniform(-0.5,0.5)
    for _ in range(3):
        a=random.uniform(0,2*math.pi)
        P=palette(x+math.cos(a), y+math.sin(a))
        hist[len(P)]=hist.get(len(P),0)+1
        mx=max(mx,len(P))
print("palette size histogram for x in W, unit directions e:",dict(sorted(hist.items())))
print("max |P_x(e)| =",mx,"   (k-3 at k=6 is 3; at k=7 is 4)")
# consistency with the 60-degree exclusion (5.7): P_x(e) cap P_x(Re) = empty
viol=0; tested=0
for _ in range(3000):
    x=p0[0]+L*random.uniform(-0.5,0.5); y=p0[1]+L*random.uniform(-0.5,0.5)
    a=random.uniform(0,2*math.pi)
    P1=palette(x+math.cos(a), y+math.sin(a), delta=1e-5)
    a2=a+math.pi/3
    P2=palette(x+math.cos(a2), y+math.sin(a2), delta=1e-5)
    tested+=1
    if P1&P2: viol+=1
print("(5.7) P_x(e) cap P_x(Re): tested",tested,"violations",viol)
