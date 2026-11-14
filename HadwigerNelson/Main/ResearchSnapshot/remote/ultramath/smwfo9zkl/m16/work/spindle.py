"""Self-contained verification of the standard 7-vertex 4-chromatic unit-distance graph
(the Moser spindle) and of whether it can sit on 3 concentric circles.

Spindle: two copies of the unit 'diamond' K4-e (5 unit edges, the two non-adjacent
vertices at distance sqrt3) sharing a vertex a, with the two opposite long-diagonal
ends d, g at distance 1.  Vertices: a,d,g (spine) plus b,c (the diamond on a,d) and
e,f (the diamond on a,g); 11 unit edges.  Classical fact: chromatic number 4.
"""
import sympy as sp
s3 = sp.sqrt(3); s11 = sp.sqrt(11)
a = sp.Matrix([0,0])
d = sp.Matrix([s11/2, sp.Rational(1,2)])
g = sp.Matrix([s11/2, -sp.Rational(1,2)])

def apexes(P, Q):
    """the two points at distance 1 from both P and Q (requires |PQ| = sqrt3)"""
    M = (P+Q)/2
    v = (Q-P)
    n = sp.Matrix([-v[1], v[0]]) / sp.sqrt(v.dot(v))
    h = sp.Rational(1,2)          # sqrt(1 - (sqrt3/2)^2)
    return M + h*n, M - h*n

b, c = apexes(a, d)
e, f = apexes(a, g)
V = {0:a, 1:b, 2:c, 3:d, 4:e, 5:f, 6:g}
E = [(0,1),(0,2),(1,2),(1,3),(2,3),   # diamond on a,d : a-b,a-c,b-c,b-d,c-d
     (0,4),(0,5),(4,5),(4,6),(5,6),   # diamond on a,g
     (3,6)]                            # spine edge d-g
print("vertex coordinates (exact):")
for k,v in V.items(): print("  ", k, sp.simplify(v.T))
bad = 0
for (i,j) in E:
    L2 = sp.simplify((V[i]-V[j]).dot(V[i]-V[j]))
    if L2 != 1: bad += 1; print("  NOT unit:", (i,j), L2)
print("edges:", len(E), " all unit:", bad == 0)
print("non-edges:")
for i in range(7):
    for j in range(i+1,7):
        if (i,j) not in E:
            L2 = sp.simplify((V[i]-V[j]).dot(V[i]-V[j]))
            print(f"   {i}-{j}: d^2 = {sp.nsimplify(L2)} = {float(L2):.6f}")

def chi(n, E):
    import itertools
    E = set(E)
    for cc in range(1, n+1):
        for col in itertools.product(range(cc), repeat=n):
            if all(col[i]!=col[j] for (i,j) in E): return cc, col
print("\nchromatic number (exhaustive):", chi(7, E)[0])

# can the 7 vertices be placed with at most 3 distinct distances from some centre x?
import numpy as np
P = np.array([[float(sp.N(v[0])), float(sp.N(v[1]))] for v in V.values()])
def ndist(x, tol=1e-7):
    r = np.sqrt(((P - x)**2).sum(axis=1))
    r = np.sort(r)
    k = 1
    for i in range(1,7):
        if r[i]-r[i-1] > tol: k += 1
    return k, r
best = (99, None, None)
for gx in np.linspace(-1.5, 2.5, 401):
    for gy in np.linspace(-1.5, 1.5, 401):
        k, r = ndist(np.array([gx,gy]))
        if k < best[0]: best = (k, (gx,gy), r)
print("\ngrid search over centres x: minimum number of distinct vertex-distances =", best[0], "at x ~", best[1])
print("   radii there:", np.round(best[2], 6))
# local refinement around the best point
from scipy.optimize import minimize
def obj(x):
    r = np.sqrt(((P - x)**2).sum(axis=1)); r = np.sort(r)
    return sum((r[i+1]-r[i])**2 for i in range(6))
res = minimize(obj, np.array(best[1]), method="Nelder-Mead",
               options={"xatol":1e-12,"fatol":1e-18,"maxiter":20000})
k, r = ndist(res.x, tol=1e-6)
print("after Nelder-Mead refinement: x =", np.round(res.x,9), " #distinct radii =", k)
print("   radii:", np.round(r, 8))
print("   pairwise gaps:", np.round(np.diff(r), 9))
