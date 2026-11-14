"""For each 3-set T of gadget labels, check whether some q in the annulus A has
outside neighbours of every colour in [6]\T (complement). If so, no recolouring of
A by [6]\T is possible at q, and the Mercedes gadget with labels T cannot be inserted
at k=6 (with the outside 7-colouring fixed)."""
import math, random
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
def S_of(qx,qy,N=1440):
    S=set()
    for j in range(N):
        th=2*math.pi*j/N
        x=qx+math.cos(th); y=qy+math.sin(th)
        r=math.hypot(x-p0[0],y-p0[1])
        if r>1+eps or r<1-eps:
            S.add(c0num(x,y))
    return S
random.seed(11)
samples=[]
for _ in range(400):
    th=random.uniform(0,2*math.pi); r=random.uniform(1-eps,1+eps)
    samples.append((p0[0]+r*math.cos(th),p0[1]+r*math.sin(th)))
sets=[S_of(x,y) for x,y in samples]
print("distinct outside sets:",len(set(frozenset(s) for s in sets)))
dead=[]; alive=[]
for T in combinations(range(7),3):
    T=set(T); comp=set(range(7))-T
    hits=[i for i,S in enumerate(sets) if comp<=S]
    if hits: dead.append((sorted(T),hits[0]))
    else: alive.append(sorted(T))
print("triples T with a point q whose outside neighbours cover [6]\\T:",len(dead),"/20")
print("alive triples:",alive)
for T,i in dead[:6]:
    print("  T=",T,"witness q=",tuple(round(v,6) for v in samples[i]),"outside=",sorted(sets[i]))
