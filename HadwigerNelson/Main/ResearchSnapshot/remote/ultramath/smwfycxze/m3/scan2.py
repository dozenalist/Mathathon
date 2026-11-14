import math
S3 = math.sqrt(3.0)
def centre(m,n): return (S3*(2*m-n)/5.0, 3.0*n/5.0)
HEXV = [(S3/5, 1/5), (0.0, 2/5), (-S3/5, 1/5), (-S3/5,-1/5), (0.0,-2/5), (S3/5,-1/5)]
def hverts(m,n):
    c=centre(m,n); return [(c[0]+vx,c[1]+vy) for vx,vy in HEXV]
def segd(p,a,b):
    ax,ay=a; bx,by=b; px,py=p
    dx,dy=bx-ax,by-ay; den=dx*dx+dy*dy
    t=((px-ax)*dx+(py-ay)*dy)/den
    if t<=0: return math.hypot(px-ax,py-ay)
    if t>=1: return math.hypot(px-bx,py-by)
    return math.hypot(px-ax-t*dx, py-ay-t*dy)
def drange(p,m,n):
    vs=hverts(m,n); inside=True
    for i in range(6):
        a,b=vs[i],vs[(i+1)%6]
        if (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])<0: inside=False;break
    dmin = 0.0 if inside else min(segd(p,vs[i],vs[(i+1)%6]) for i in range(6))
    dmax = max(math.hypot(p[0]-v[0],p[1]-v[1]) for v in vs)
    return dmin,dmax
def slacks(p,MR=3):
    out={}
    for m in range(-MR,MR+1):
        for n in range(-MR,MR+1):
            c=(m+2*n)%7
            dmin,dmax=drange(p,m,n)
            s=max(dmin-1.0,1.0-dmax)
            if c not in out or s<out[c]: out[c]=s
    return out
def inside_hex(p):
    x,y=p
    for i in range(6):
        a,b=HEXV[i],HEXV[(i+1)%6]
        if (b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])<0: return False
    return True

N=41; step=0.8/N
best=None; vals=[]
import statistics
for i in range(N+1):
    for j in range(N+1):
        p=(-0.4+i*step,-0.4+j*step)
        if not inside_hex(p): continue
        s=slacks(p); v=sorted(s.values(),reverse=True); vals.append(v[2])
        if best is None or v[2]>best[0]: best=(v[2],p)
print("max over grid of 3rd-largest slack:", best)
vals.sort()
print("median 3rd-largest slack:", vals[len(vals)//2], " min:", vals[0])
for eps in [0.0071, 0.02, 0.0356, 0.05]:
    frac=sum(1 for v in vals if v>eps)/len(vals)
    print("eps=%.4f  fraction of centres with >=3 colours absent: %.3f"%(eps,frac))
