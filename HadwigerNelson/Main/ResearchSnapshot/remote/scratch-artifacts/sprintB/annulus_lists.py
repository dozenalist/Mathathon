"""For q in the annulus A (1-eps <= |q-p0| <= 1+eps), compute the set of colours of
points at distance exactly 1 from q that lie OUTSIDE A, in the paper's 7-colouring.
If {1,4,5} is contained in that set for some q, then no recolouring of A by {1,4,5}
can be proper at q (with the outside fixed)."""
import math, random
p0=(1/55,18/55); eps=71/10000
d=math.sqrt(3)*0.4; w=-0.5+0.5j*math.sqrt(3)
def c0num(x,y):
    qq=complex(x,y); a=qq/d; b=2*a.imag/math.sqrt(3); aa=a.real+b/2
    m0=round(aa); n0=round(b)
    best=1e9; bm=bn=0
    for dm in (-1,0,1,2):
        for dn in (-1,0,1,2):
            m,n=m0+dm,n0+dn; z=d*(m+n*w); dd=abs(qq-z)
            if dd<best: best=dd; bm,bn=m,n
    return (bm+2*bn)%7
def outside_colours(qx,qy,N=720):
    S=set()
    for j in range(N):
        th=2*math.pi*j/N
        x=qx+math.cos(th); y=qy+math.sin(th)
        r=math.hypot(x-p0[0],y-p0[1])
        if r>1+eps or r<1-eps:
            S.add(c0num(x,y))
    return S
random.seed(7)
worst=[]; counts={}
for trial in range(200):
    th=random.uniform(0,2*math.pi); r=random.uniform(1-eps,1+eps)
    qx=p0[0]+r*math.cos(th); qy=p0[1]+r*math.sin(th)
    S=outside_colours(qx,qy)
    key=tuple(sorted(S)); counts[key]=counts.get(key,0)+1
    if {1,4,5} <= S: worst.append((qx,qy,S))
print("outside-colour sets observed (colour:count):")
for k,v in sorted(counts.items(),key=lambda kv:-kv[1])[:12]: print("  ",k,v)
print("points q with {1,4,5} all present outside:",len(worst),"/200")
if worst: print("example:",worst[0])
