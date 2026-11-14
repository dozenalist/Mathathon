import math, json
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
# five candidate witnesses from the dense grid + one explicit
cands=[(-0.888877,0.731122),(1.005643,0.431059),(0.260104,1.297568),
       (0.732414,1.016999),(1.011082,0.327273),
       (0.727791488186838,1.0262788415398978)]
Ss=[S_of(*q) for q in cands]
for q,S in zip(cands,Ss): print("q",tuple(round(v,6) for v in q),"S",sorted(S))
ans={}
for T in combinations(range(7),3):
    comp=set(range(7))-set(T)
    for q,S in zip(cands,Ss):
        if comp<=S: ans[T]=(q,sorted(S)); break
print("triples covered by the six witnesses:",len(ans),"/35")
missing=[T for T in combinations(range(7),3) if T not in ans]
print("missing:",missing)
json.dump({str(list(k)):{"q":list(v[0]),"S":v[1]} for k,v in ans.items()}, open(".scratch/gadget6_witnesses.json","w"))
