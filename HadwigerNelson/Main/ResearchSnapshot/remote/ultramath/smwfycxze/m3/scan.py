import math
from fractions import Fraction as F

S3 = math.sqrt(3.0)

def centre(m,n):
    return (S3*(2*m-n)/5.0, 3.0*n/5.0)

HEXV = [(S3/5, 1/5), (0.0, 2/5), (-S3/5, 1/5), (-S3/5,-1/5), (0.0,-2/5), (S3/5,-1/5)]

def hexverts(m,n):
    c = centre(m,n)
    return [(c[0]+vx, c[1]+vy) for vx,vy in HEXV]

def seg_dist(p,a,b):
    ax,ay=a; bx,by=b; px,py=p
    dx,dy = bx-ax, by-ay
    den = dx*dx+dy*dy
    t = ((px-ax)*dx+(py-ay)*dy)/den
    if t<=0: return math.hypot(px-ax,py-ay)
    if t>=1: return math.hypot(px-bx,py-by)
    qx,qy = ax+t*dx, ay+t*dy
    return math.hypot(px-qx,py-qy)

def hex_dist_range(p,m,n):
    """(min dist, max dist) from p to closed hexagon (m,n)."""
    vs = hexverts(m,n)
    # inside?
    inside=True
    for i in range(6):
        a,b = vs[i], vs[(i+1)%6]
        ex,ey = b[0]-a[0], b[1]-a[1]
        cr = ex*(p[1]-a[1]) - ey*(p[0]-a[0])
        if cr < 0: inside=False; break
    if inside: dmin = 0.0
    else: dmin = min(seg_dist(p, vs[i], vs[(i+1)%6]) for i in range(6))
    dmax = max(math.hypot(p[0]-v[0], p[1]-v[1]) for v in vs)
    return dmin, dmax

def colours_in_annulus(p, eps, MR=3):
    lo, hi = 1-eps, 1+eps
    present=set()
    for m in range(-MR,MR+1):
        for n in range(-MR,MR+1):
            dmin,dmax = hex_dist_range(p,m,n)
            if dmin <= hi and dmax >= lo:
                present.add((m+2*n)%7)
    return present

# fundamental domain = Voronoi hexagon; scan
eps = 0.0071
N = 61
counts = {}
good = 0; tot = 0
examples = {}
step = 0.8/N
for i in range(N+1):
    for j in range(N+1):
        x = -0.4 + i*step
        y = -0.4 + j*step
        p = (x,y)
        # inside Voronoi hexagon?
        inside=True
        vs = HEXV
        for k in range(6):
            a,b = vs[k], vs[(k+1)%6]
            ex,ey = b[0]-a[0], b[1]-a[1]
            cr = ex*(y-a[1]) - ey*(x-a[0])
            if cr < 0: inside=False; break
        if not inside: continue
        tot += 1
        pr = colours_in_annulus(p, eps)
        n_missing = 7-len(pr)
        counts[n_missing] = counts.get(n_missing,0)+1
        if n_missing >= 3:
            good += 1
            examples.setdefault(n_missing, (x,y,sorted(pr)))
print("eps =", eps)
print("sampled points in fundamental hexagon:", tot)
print("histogram of #missing colours:", dict(sorted(counts.items())))
print("fraction with >=3 missing (good centres):", good/tot)
for k in sorted(examples): print("  example with",k,"missing:", examples[k])
