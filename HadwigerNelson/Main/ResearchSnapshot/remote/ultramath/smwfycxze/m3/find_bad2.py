import math
from fractions import Fraction as F
S3=math.sqrt(3.0)
def centre(m,n): return (S3*(2*m-n)/5.0, 3.0*n/5.0)
HEXV=[(S3/5,1/5),(0.0,2/5),(-S3/5,1/5),(-S3/5,-1/5),(0.0,-2/5),(S3/5,-1/5)]
def hv(m,n):
    c=centre(m,n); return [(c[0]+a,c[1]+b) for a,b in HEXV]
def segd(p,a,b):
    ax,ay=a;bx,by=b;px,py=p;dx,dy=bx-ax,by-ay;den=dx*dx+dy*dy
    t=((px-ax)*dx+(py-ay)*dy)/den
    if t<=0: return math.hypot(px-ax,py-ay)
    if t>=1: return math.hypot(px-bx,py-by)
    return math.hypot(px-ax-t*dx,py-ay-t*dy)
def drange(p,m,n):
    vs=hv(m,n);ins=True
    for i in range(6):
        a,b=vs[i],vs[(i+1)%6]
        if (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])<0: ins=False;break
    dmin=0.0 if ins else min(segd(p,vs[i],vs[(i+1)%6]) for i in range(6))
    dmax=max(math.hypot(p[0]-v[0],p[1]-v[1]) for v in vs)
    return dmin,dmax
def present(p,eps,MR=3):
    out=set()
    for m in range(-MR,MR+1):
        for n in range(-MR,MR+1):
            dmin,dmax=drange(p,m,n)
            if dmin<=1+eps and dmax>=1-eps: out.add((m+2*n)%7)
    return out
def inside(p):
    x,y=p
    for i in range(6):
        a,b=HEXV[i],HEXV[(i+1)%6]
        if (b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])<0: return False
    return True
eps=0.0071
res={}
for a in range(-20,21):
    for b in range(-20,21):
        p=(a/50.0,b/50.0)
        if not inside(p): continue
        k=len(present(p,eps))
        res.setdefault(k,[]).append(p)
for k in sorted(res):
    print("colours present %d : %d points; example %s"%(k,len(res[k]),res[k][0]))
