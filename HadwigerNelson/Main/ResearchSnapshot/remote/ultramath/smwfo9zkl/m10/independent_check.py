"""
Independent re-derivation with nothing from twocentre.py: plain `math` and plain Python.

Purpose: the two decision procedures in the report share one conflict-graph builder.  A bug in
that builder would corrupt both, so the load-bearing verdicts are re-derived here from the
textbook formulas of the paper, with floats and a different colouring algorithm:

  * Lemma 5.5's sum identity  y + e^{it} = x + e^{i alpha+} + e^{i alpha-},
  * Lemma 6.4's triangle: side exactly 1, circumradius 1/sqrt(3),
  * the Moser spindle has chromatic number 4 (exhaustive 3-colouring search fails),
  * each two-centre probe of the sweep is bipartite (BFS 2-colouring succeeds).
"""
import math, itertools, cmath

# ---------------------------------------------------------------- Lemma 5.5 identity
def lemma55_residual(d, t):
    rho = math.sqrt(1 + d*d + 2*d*math.cos(t))
    Theta = t + math.atan2(-d*math.sin(t), 1 + d*math.cos(t))
    ap = Theta + math.acos(rho/2)
    am = Theta - math.acos(rho/2)
    return abs(cmath.exp(1j*ap) + cmath.exp(1j*am) - (d + cmath.exp(1j*t)))

worst = max(lemma55_residual(d, t)
            for d in (0.1, 0.3, 0.49, 0.7, 0.9)
            for t in [k*0.13 - 3 for k in range(47)])
print('Lemma 5.5 identity: max residual = %.3e' % worst)

# ---------------------------------------------------------------- Lemma 6.4 triangle
gamma = 2*math.asin(1/(2*math.sqrt(3)))
print('cos gamma = %.15f   (5/6 = %.15f)' % (math.cos(gamma), 5/6))
t = math.atan2(4, 3)
z = [cmath.exp(1j*(t + 2*j*2*math.pi/3)) + cmath.exp(1j*(t + math.pi + gamma + 2*j*2*math.pi/3))
     for j in range(3)]
print('Lemma 6.4: |z_j| = %s  side lengths = %s'
      % (['%.12f' % abs(v) for v in z],
         ['%.12f' % abs(z[i]-z[j]) for (i, j) in ((0, 1), (0, 2), (1, 2))]))

# ---------------------------------------------------------------- Moser spindle
r3 = math.sqrt(3)
c, s = 5/6, math.sqrt(11)/6
P = [(0, 0), (r3, 0), (r3/2, 1/2), (r3/2, -1/2)]
Q2 = (r3*c, r3*s)
h = (Q2[0]/2, Q2[1]/2)
perp = (-Q2[1]/(2*r3), Q2[0]/(2*r3))
P += [Q2, (h[0]+perp[0], h[1]+perp[1]), (h[0]-perp[0], h[1]-perp[1])]

def dist2(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

n = len(P)
E = [(i, j) for i in range(n) for j in range(i+1, n) if abs(dist2(P[i], P[j]) - 1) < 1e-12]
print('Moser spindle: 7 points, %d unit edges' % len(E))

def kcolourable(nv, edges, k):
    nbr = [[] for _ in range(nv)]
    for (i, j) in edges:
        nbr[i].append(j); nbr[j].append(i)
    col = [-1]*nv
    def rec(v):
        if v == nv:
            return True
        for c in range(k):
            if all(col[w] != c for w in nbr[v]):
                col[v] = c
                if rec(v+1):
                    return True
                col[v] = -1
        return False
    return rec(0) if rec else None, col

def chromatic(nv, edges, kmax=8):
    for k in range(1, kmax+1):
        ok, col = kcolourable_full(nv, edges, k)
        if ok:
            return k, col
    return None, None

def kcolourable_full(nv, edges, k):
    nbr = [[] for _ in range(nv)]
    for (i, j) in edges:
        nbr[i].append(j); nbr[j].append(i)
    col = [-1]*nv
    order = sorted(range(nv), key=lambda v: -len(nbr[v]))
    def rec(idx):
        if idx == nv:
            return True
        v = order[idx]
        for c in range(k):
            if all(col[w] != c for w in nbr[v]):
                col[v] = c
                if rec(idx+1):
                    return True
                col[v] = -1
        return False
    if rec(0):
        return True, col
    return False, None

chi, col = chromatic(7, E)
print('Moser spindle chromatic number (independent exhaustive search) = %s  colouring %s'
      % (chi, col))

# ---------------------------------------------------------------- two-centre probes: bipartite?
def two_centre_points(d, cost, sint):
    """independent construction of the same probe's pi-image"""
    pts = []
    t = complex(cost, sint)
    for m in range(6):
        f = t*cmath.exp(1j*m*math.pi/3)
        w = d + f
        rho = abs(w)
        kk = math.sqrt(max(0.0, 1 - rho*rho/4))/rho
        for br in (+1, -1):
            a = w/2 + br*1j*w*kk
            for mm in range(6):
                pts.append((d + f*cmath.exp(1j*mm*math.pi/3)))
                pts.append(a*cmath.exp(1j*mm*math.pi/3))
    pts += [d + t*cmath.exp(1j*m*math.pi/3) for m in range(6)]
    return pts

def bipartite(pts):
    n = len(pts)
    nbr = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if abs(abs(pts[i]-pts[j]) - 1) < 1e-9:
                nbr[i].append(j); nbr[j].append(i)
    col = [-1]*n
    for s in range(n):
        if col[s] != -1:
            continue
        col[s] = 0
        stack = [s]
        while stack:
            v = stack.pop()
            for w in nbr[v]:
                if col[w] == -1:
                    col[w] = 1 - col[v]; stack.append(w)
                elif col[w] == col[v]:
                    return False
    return True

bad = []
for d in [a/10 for a in range(1, 10)]:
    for (num, den) in ((3, 4), (5, 12), (8, 15)):
        nn = math.hypot(num, den)
        pts = two_centre_points(d, num/nn, den/nn)
        if not bipartite(pts):
            bad.append((d, (num, den)))
print('two-centre probes that are NOT bipartite:', bad if bad else 'none (27/27 bipartite)')
