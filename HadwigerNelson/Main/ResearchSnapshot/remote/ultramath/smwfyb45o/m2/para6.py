"""Exact (Fraction) forced-set / clique / 6-colouring engine for parallelogram tilings.

Tiling: P = [0,1)*a + [0,1)*b, a,b rational, lattice L = Z a + Z b, cells P + v, v in L.
All cell offsets are indexed: cell (i,j) = P + i a + j b.

PROPERNESS.  For an offset v, { |v - d| : d in P - P } =: [dmin(v), dmax(v)] is exactly the
set of distances realised between P and P+v.  (P-P is convex, so the image under a continuous
map is an interval; P-P = { s a + t b : |s|,|t| <= 1 }.)  Two cells of the same colour must
never realise distance 1, so a same-colour offset v is LEGAL iff 1 not in [dmin(v), dmax(v)].
v is FORCED iff dmin(v) <= 1 <= dmax(v)  (closed: tangency counts).

  dmax(v)^2 = max over vertices w of P-P of |v - w|^2        (norm is convex -> max at vertex)
  dmin(v)^2 = 0 if v in P-P, else min over the 4 edges e of dist(v,e)^2

All quantities are exact rationals (Fractions); distances are only ever compared with 1 via
their exact squares, so no square roots and no floating point appear anywhere.

TRUNCATION (proved, not assumed).  dmin(v) >= |v| - R where R = max(|a+b|,|a-b|), because
every d in P-P has |d| <= R.  Hence forced => |v| <= 1 + R.  With diam(P) < 1 we have
R <= |a|+|b| < 2, so |v| < 3: only finitely many lattice points can be forced.
The script enumerates all lattice points with |v| < 3 exactly (integer arithmetic after
clearing denominators) and asserts that every point it discards has |v| >= 3.
"""
from fractions import Fraction as Fr
from itertools import product
import sys

# ---------- exact plane geometry ----------
def sub(u, v): return (u[0] - v[0], u[1] - v[1])
def add(u, v): return (u[0] + v[0], u[1] + v[1])
def smul(c, u): return (c * u[0], c * u[1])
def dot(u, v): return u[0] * v[0] + u[1] * v[1]
def cross(u, v): return u[0] * v[1] - u[1] * v[0]
def n2(u): return dot(u, u)

def le_1_plus_sqrtR2(Q, R2):
    """Exact test: is  Q <= (1 + sqrt(R2))^2 = 1 + R2 + 2 sqrt(R2) ?  (Q,R2 exact rationals >= 0)"""
    t = Q - 1 - R2
    if t <= 0:
        return True
    return t * t <= 4 * R2

def dist2_seg(p, q1, q2):
    """squared distance from point p to the closed segment [q1,q2]; exact."""
    d = sub(q2, q1)
    dd = dot(d, d)
    if dd == 0:
        return n2(sub(p, q1))
    t = dot(sub(p, q1), d) / dd
    if t < 0: t = Fr(0)
    if t > 1: t = Fr(1)
    return n2(sub(p, add(q1, smul(t, d))))

def in_convex_closed(p, poly):
    """p in closed convex polygon `poly` (vertices in cyclic order); exact."""
    pos = neg = False
    m = len(poly)
    for i in range(m):
        c = cross(sub(poly[(i + 1) % m], poly[i]), sub(p, poly[i]))
        if c > 0: pos = True
        elif c < 0: neg = True
    return not (pos and neg)

class Para:
    """Exact distance interval [dmin,dmax] between P and P+v for P = [0,1]a+[0,1]b."""
    def __init__(self, a, b, check_diam=True):
        self.a = (Fr(a[0]), Fr(a[1]))
        self.b = (Fr(b[0]), Fr(b[1]))
        if cross(self.a, self.b) == 0:
            raise ValueError("a,b must be a basis")
        # P - P = { s a + t b : |s|,|t| <= 1 }, vertices in cyclic order:
        self.mm = [add(self.a, self.b), sub(self.a, self.b),
                   smul(-1, add(self.a, self.b)), sub(self.b, self.a)]
        self.R2 = max(n2(v) for v in self.mm)          # max |d|^2 over d in P-P
        self.diam2 = max(n2(self.a), n2(self.b),
                         n2(add(self.a, self.b)), n2(sub(self.a, self.b)))
        if check_diam:
            assert self.diam2 < 1, "need diam(P) < 1"

    def dmin2(self, v):
        if in_convex_closed(v, self.mm):
            return Fr(0)
        return min(dist2_seg(v, self.mm[i], self.mm[(i + 1) % 4]) for i in range(4))

    def dmax2(self, v):
        return max(n2(sub(v, w)) for w in self.mm)

    def offset(self, p, q):
        return add(smul(Fr(p), self.a), smul(Fr(q), self.b))

    def forced(self, p, q):
        v = self.offset(p, q)
        return self.dmin2(v) <= 1 <= self.dmax2(v)

    def lattice_pts_inside(self, r2):
        """all (p,q) with |p a + q b|^2 < r2, exactly; every other (p,q) is provably outside."""
        den = 1
        for c in (self.a[0], self.a[1], self.b[0], self.b[1]):
            den = den * c.denominator // __import__('math').gcd(den, c.denominator)
        A = (int(self.a[0] * den), int(self.a[1] * den))
        B = (int(self.b[0] * den), int(self.b[1] * den))
        det = cross(A, B)
        # v = (pA+qB)/den ; p = (v1 B2 - v2 B1)/det  (in integer units)
        # |v_int| < sqrt(r2)*den  =>  |p| <= sqrt(r2)*den*(|B1|+|B2|)/|det|
        import math
        s = math.isqrt(int(r2.numerator * den * den // r2.denominator)) + 1
        P = (s * (abs(B[0]) + abs(B[1]))) // abs(det) + 2
        Q = (s * (abs(A[0]) + abs(A[1]))) // abs(det) + 2
        out = []
        lim = r2 * den * den          # |v_int|^2 < lim  (lim is an integer-ish Fraction)
        for p in range(-P, P + 1):
            for q in range(-Q, Q + 1):
                w = (p * A[0] + q * B[0], p * A[1] + q * B[1])
                if n2(w) < lim:
                    out.append((p, q))
        return out

    def forced_set(self):
        """exact forced set in index coordinates, with the truncation certificate."""
        cand = self.lattice_pts_inside(Fr(9))          # |v| < 3
        F = frozenset((p, q) for (p, q) in cand if self.forced(p, q))
        # certificate 1: all discards really are at distance >= 3
        for (p, q) in self.lattice_pts_inside(Fr(9 * 4)):  # scan a much bigger window
            if (p, q) not in cand:
                assert n2(self.offset(p, q)) >= 9, "truncation radius too small"
                break
        # certificate 2: the analytic bound dmin >= |v| - R,  R = sqrt(R2)
        for (p, q) in F:
            assert (p, q) != (0, 0)
            assert le_1_plus_sqrtR2(n2(self.offset(p, q)), self.R2), "analytic bound violated"
        assert all((-p, -q) in F for (p, q) in F), "forced set must be symmetric"
        return F

# ---------- clique ----------
def max_clique(verts, adj):
    best = []
    def bk(R, P):
        nonlocal best
        if len(R) + len(P) <= len(best):
            return
        if not P:
            if len(R) > len(best):
                best = list(R)
            return
        # pivot
        piv = max(P, key=lambda u: len(adj[u] & P))
        for v in list(P - adj[piv]):
            bk(R + [v], P & adj[v])
            P = P - {v}
    bk([], set(verts))
    return best

def graph(F):
    V = set(F) | {(0, 0)}
    adj = {u: {v for v in V if v != u and (v[0] - u[0], v[1] - u[1]) in F} for u in V}
    return V, adj

# ---------- linear 6-colourings ----------
def linear_mod6(F, m=6):
    """c(i,j) = A i + B j mod m; proper iff no forced index-vector dies."""
    sols = [(A, B) for A in range(m) for B in range(m)
            if all((A * p + B * q) % m for (p, q) in F)]
    return sols

def proper_check_linear(F, m, A, B):
    return all((A * p + B * q) % m != 0 for (p, q) in F)

# ---------- exact 6-colouring of a finite torus (for cases linear fails) ----------
def torus_colour(F, n, m=6, node_limit=400000):
    """Is there c: (Z/n)^2 -> Z/m with c(x)!=c(x+v) for all forced v?  Exact DFS.
    Returns a colouring (as dict) or None/'limit'."""
    cells = [(i, j) for i in range(n) for j in range(n)]
    idx = {c: k for k, c in enumerate(cells)}
    nb = {c: [] for c in cells}
    for c in cells:
        for (p, q) in F:
            nb[c].append(idx[((c[0] + p) % n, (c[1] + q) % n)])
    col = [-1] * len(cells)
    nodes = [0]
    order = sorted(range(len(cells)), key=lambda k: -len(nb[cells[k]]))
    def dfs(t):
        nodes[0] += 1
        if nodes[0] > node_limit: raise TimeoutError
        if t == len(order): return True
        k = order[t]; c = cells[k]
        used = {col[d] for d in nb[c] if col[d] >= 0}
        for x in range(m):
            if x not in used:
                col[k] = x
                if dfs(t + 1): return True
                col[k] = -1
        return False
    try:
        ok = dfs(0)
    except TimeoutError:
        return 'limit'
    return {cells[k]: col[k] for k in range(len(cells))} if ok else None

# ---------- report on one parallelogram ----------
def report(a, b, verbose=True, torus=(4, 5)):
    para = Para(a, b)
    F = para.forced_set()
    V, adj = graph(F)
    Cl = max_clique(sorted(V), adj)
    sols = linear_mod6(F)
    tor = None
    if not sols and torus:
        for n in torus:
            tor = torus_colour(F, n)
            if tor not in (None, 'limit'):
                tor = ('found', n)
                break
            if tor == 'limit':
                break
    if verbose:
        print(f"a={a} b={b}  diam^2={float(para.diam2):.4f} |F|={len(F)} "
              f"omega={len(Cl)} lin6={len(sols)} torus6={tor}")
        print(f"   forced (p,q): {sorted(F)}")
        print(f"   max clique: {sorted(Cl)}")
    return dict(a=a, b=b, para=para, F=F, omega=len(Cl), clique=Cl, lin=sols, torus=tor)

if __name__ == '__main__':
    tests = [
        ((Fr(1, 3), 0), (0, Fr(1, 3))),          # square, tiny
        ((Fr(2, 5), 0), (0, Fr(2, 5))),
        ((Fr(1, 2), 0), (0, Fr(1, 2))),
        ((Fr(1, 2), 0), (0, Fr(3, 5))),
        ((Fr(3, 5), 0), (0, Fr(3, 5))),
        ((Fr(1, 2), 0), (Fr(1, 4), Fr(2, 5))),   # slanted
        ((Fr(1, 3), 0), (Fr(1, 4), Fr(1, 3))),   # slanted, small
    ]
    for a, b in tests:
        report(a, b)
        print()
