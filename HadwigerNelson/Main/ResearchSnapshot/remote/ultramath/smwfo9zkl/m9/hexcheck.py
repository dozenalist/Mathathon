import numpy as np, math
# Isbell hexagonal 7-colouring: Voronoi cells of the triangular lattice with spacing L, coloured by i+3j mod 7.
s = 0.40                      # hexagon side
L = math.sqrt(3)*s            # lattice (centre) spacing
e1 = np.array([L,0.0]); e2 = np.array([L*0.5, L*math.sqrt(3)/2])
def cell(x):
    # nearest lattice point, axial coords via lattice reduction
    # solve x = a e1 + b e2
    b = x[1]/(L*math.sqrt(3)/2); a = x[0]/L - b/2
    best=None
    ia,ib = round(a), round(b)
    for da in (-1,0,1):
        for db in (-1,0,1):
            aa,bb = ia+da, ib+db
            c = aa*e1+bb*e2
            d = np.hypot(*(x-c))
            if best is None or d<best[0]-1e-15: best=(d,aa,bb)
    return best[1],best[2]
def colour(x):
    a,b = cell(x); return (a+3*b)%7
def colarr(P):
    b = P[:,1]/(L*math.sqrt(3)/2); a = P[:,0]/L - b/2
    ia = np.round(a).astype(int); ib = np.round(b).astype(int)
    best = np.full(len(P), np.inf); A=np.zeros(len(P),int); B=np.zeros(len(P),int)
    for da in (-1,0,1):
        for db in (-1,0,1):
            aa=ia+da; bb=ib+db
            cx = aa*L+bb*L*0.5; cy = bb*L*math.sqrt(3)/2
            d = np.hypot(P[:,0]-cx,P[:,1]-cy)
            m = d<best
            best=np.where(m,d,best); A=np.where(m,aa,A); B=np.where(m,bb,B)
    return (A+3*B)%7

# --- 1. properness: no same-colour pair at distance 1 ---
rng=np.random.default_rng(0)
P = rng.uniform(0,20,(4000,2))
bad=0
for ang in np.linspace(0,2*math.pi,60,endpoint=False):
    Q = P + np.array([math.cos(ang),math.sin(ang)])
    same = colarr(P)==colarr(Q)
    bad += int(same.sum())
print("same-colour unit pairs found (should be 0):",bad)

# --- 2. transition graph at selected centres ---
def Gamma(x, r=0.12, hs=(2e-3,1e-3,5e-4,2.5e-4)):
    g = np.linspace(-r,r,161)
    X,Y = np.meshgrid(x[0]+g, x[1]+g)
    Q = np.stack([X.ravel(),Y.ravel()],axis=1)
    Q = Q[np.hypot(Q[:,0]-x[0],Q[:,1]-x[1])<=r]
    cq = colarr(Q)
    area = math.pi*r*r
    out={}
    for h in hs:
        for ang in np.linspace(0,math.pi,8,endpoint=False):
            d = h*np.array([math.cos(ang),math.sin(ang)])
            cp = colarr(Q+d)
            for i in range(7):
                for j in range(i+1,7):
                    m = ((cq==i)&(cp==j))|((cq==j)&(cp==i))
                    val = m.sum()/len(Q)*area/h
                    out[(i,j)]=max(out.get((i,j),0.0),val)
    return {k:v for k,v in out.items() if v>0.02}

# candidate centres
tri = (e1+e2)/3.0            # circumcentre of the elementary triangle 0,e1,e2 -> triple point
edge = (e1)/2.0              # midpoint of the segment joining two adjacent centres -> on a cell edge
ctr  = np.array([0.0,0.0])   # a cell centre
for name,x in [("triple point",tri),("edge point",edge),("cell centre",ctr)]:
    G = Gamma(x)
    print(f"{name} {np.round(x,4)}: colours near = {sorted(set(colarr(np.array([x+0.01*np.array([math.cos(t),math.sin(t)]) for t in np.linspace(0,2*math.pi,16,endpoint=False)]))))}")
    print("   edges of Gamma_x (i,j,limsup D/|h|):", sorted(G.items(), key=lambda kv:-kv[1])[:8])
    # triangle?
    E=set(G)
    tri3 = any((min(a,b),max(a,b)) in E and (min(a,c),max(a,c)) in E and (min(b,c),max(b,c)) in E
               for a in range(7) for b in range(a+1,7) for c in range(b+1,7))
    print("   contains a triangle:",tri3)
