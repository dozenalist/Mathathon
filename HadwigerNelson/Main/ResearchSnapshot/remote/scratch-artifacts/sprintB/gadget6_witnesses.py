import math
from itertools import combinations
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
def S_of(qx,qy,N=3000):
    S=set()
    for j in range(N):
        th=2*math.pi*j/N
        x=qx+math.cos(th); y=qy+math.sin(th)
        r=math.hypot(x-p0[0],y-p0[1])
        if r>1+eps or r<1-eps: S.add(c0num(x,y))
    return S
# dense grid
pts=[]
for it in range(180):
    th=2*math.pi*it/180
    for ir in range(7):
        r=1-eps+2*eps*ir/6
        pts.append((p0[0]+r*math.cos(th),p0[1]+r*math.sin(th)))
sets=[S_of(x,y) for x,y in pts]
ans={}
for T in combinations(range(7),3):
    comp=set(range(7))-set(T)
    for i,S in enumerate(sets):
        if comp<=S:
            ans[T]=(pts[i],sorted(S)); break
print("triples with a witness:",len(ans),"/20")
for T in sorted(ans): print("  T=",list(T),"q=",tuple(round(v,6) for v in ans[T][0]),"S=",ans[T][1])
