import math
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
def S_of(qx,qy,N=2000):
    S=set()
    for j in range(N):
        th=2*math.pi*j/N
        x=qx+math.cos(th); y=qy+math.sin(th)
        r=math.hypot(x-p0[0],y-p0[1])
        if r>1+eps or r<1-eps: S.add(c0num(x,y))
    return S
q=(0.727791488186838,1.0262788415398978)
print("earlier witness S:",sorted(S_of(*q)),"contains {1,4,5}:",{1,4,5}<=S_of(*q))
# dense grid over the annulus
found=[]
for it in range(90):
    th=2*math.pi*it/90
    for ir in range(5):
        r=1-eps+2*eps*ir/4
        qx=p0[0]+r*math.cos(th); qy=p0[1]+r*math.sin(th)
        S=S_of(qx,qy)
        if {1,4,5}<=S: found.append((qx,qy,sorted(S)))
print("dense-grid points with {1,4,5} covered:",len(found))
for f in found[:5]: print("  ",tuple(round(v,6) for v in f[:2]),f[2])
