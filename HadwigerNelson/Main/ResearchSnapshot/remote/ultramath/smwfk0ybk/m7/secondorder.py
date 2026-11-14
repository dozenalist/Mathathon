"""The SECOND-ORDER consequence of the paper's transfer lemma (5.2): a one-centre
constraint in x that is strictly stronger than m6's pair exclusion (C4).

(5.2): for sigma x sigma-a.e. (e,v),  c(x+e+v) not in P_x(e) u P_x(v).

Fix the R-orbit f_i = R^i f (i = 0..5) at x and, for ordered pairs (i,j) with
j - i != 3 (mod 6), put

    p_ij := x + f_i + f_j,        L_ij := Fin k \\ (P_i u P_j).

Then for a.e. f, simultaneously over the finitely many pairs,
    (a) c(p_ij) in L_ij                                  [(5.2)]
    (b) c(p_ij) != c(p_kl) whenever |p_ij - p_kl| = 1     [properness].
The term j = i+3 is excluded: then f_i + f_j = 0, so p_ij = x and the instance
has v = -e, which is measure zero and therefore NOT supplied by (5.2).

With w = e^(i pi/3), d = j - i and angles in units of pi/6,
    1 + w^d = 2cos(d pi/6) e^(i d pi/6),   f_i + f_j = 2cos(d pi/6) w^(2i+d),
so every p is of the form  s * e^(i m pi/6)  with s, m real, s in {2, +-sqrt3, +-1},
and for two such points
    |p - q|^2 = s^2 + t^2 - 2 s t cos((m - m') pi/6)   in  Q(sqrt 3).
All tests below are exact in Q(sqrt3) (a pair of Fractions); no floating point.

So a palette assignment at x is admissible only if this finite graph is properly
list-colourable.  Tested below on the parity field of the one-centre no-go and on
m5's and m6's own k = 6 orbits.
"""
from fractions import Fraction as F

# element of Q(sqrt3) as (a,b) meaning a + b*sqrt3
def add(x, y): return (x[0] + y[0], x[1] + y[1])
def sub(x, y): return (x[0] - y[0], x[1] - y[1])
def mul(x, y): return (x[0]*y[0] + 3*x[1]*y[1], x[0]*y[1] + x[1]*y[0])
ZERO, ONE = (F(0), F(0)), (F(1), F(0))

COS6 = [(F(1), F(0)), (F(0), F(1, 2)), (F(1, 2), F(0)), (F(0), F(0)),
        (F(-1, 2), F(0)), (F(0), F(-1, 2)), (F(-1), F(0)), (F(0), F(-1, 2)),
        (F(-1, 2), F(0)), (F(0), F(0)), (F(1, 2), F(0)), (F(0), F(1, 2))]
# 2 cos(d pi/6), d = 0..5
MOD = [(F(2), F(0)), (F(0), F(1)), (F(1), F(0)), (F(0), F(0)),
       (F(-1), F(0)), (F(0), F(-1))]


def pt(i, j):
    """x-normalised key of p_ij = c_d * w^(2i+d): (modulus, angle index in pi/6)."""
    d = (j - i) % 6
    assert d != 3
    s = MOD[d]
    m = (2 * i + d) % 12
    if s[0] < 0 or (s[0] == 0 and s[1] < 0):
        s = (-s[0], -s[1])
        m = (m + 6) % 12
    return (s, m)


def d2(p, q):
    """|p - q|^2 in Q(sqrt3)."""
    s, m = p
    t, n = q
    return sub(add(mul(s, s), mul(t, t)), mul((F(2), F(0)), mul(mul(s, t), COS6[(m - n) % 12])))


def build(orbit, k):
    full = (1 << k) - 1
    pts = {}
    for i in range(6):
        for j in range(6):
            if (j - i) % 6 == 3:
                continue
            key = pt(i, j)
            allowed = full & ~(orbit[i] | orbit[j])
            pts[key] = allowed if key not in pts else (pts[key] & allowed)
    keys = sorted(pts, key=lambda p: (p[1], p[0]))
    adj = {p: set() for p in keys}
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            if d2(keys[a], keys[b]) == ONE:
                adj[keys[a]].add(keys[b])
                adj[keys[b]].add(keys[a])
    return keys, adj, pts


def list_colour(keys, adj, L, k):
    def rec(un, assign):
        if not un:
            return dict(assign)
        best = None
        for v in un:
            av = [c for c in range(k) if (L[v] >> c) & 1
                  and all(assign.get(u) != c for u in adj[v] if u in assign)]
            if best is None or len(av) < len(best[1]):
                best = (v, av)
                if not av:
                    return None
        v, av = best
        for c in av:
            assign[v] = c
            r = rec(un - {v}, assign)
            if r is not None:
                return r
            del assign[v]
        return None
    return rec(set(keys), {})


def report(name, orbit, k=6):
    keys, adj, L = build(orbit, k)
    sol = list_colour(keys, adj, L, k)
    edges = sum(len(adj[v]) for v in keys) // 2
    sizes = sorted(bin(L[v]).count("1") for v in keys)
    print(f"{name}\n    {len(keys)} points, {edges} unit edges, list sizes "
          f"{sizes[0]}..{sizes[-1]}, list-colourable: {'YES' if sol else 'NO'}")
    return sol


if __name__ == "__main__":
    k = 6
    bl = lambda *xs: tuple(sum(1 << l for l in x) for x in xs)
    report("parity field l=3: {3},{4},{3},{4},{3},{4}",
           bl((3,), (4,), (3,), (4,), (3,), (4,)))
    report("parity field l=4: {4},{5},{4},{5},{4},{5}",
           bl((4,), (5,), (4,), (5,), (4,), (5,)))
    report("m5 k=6 l=5 witness: {5},{1,4},{5},{1,4},{5},{1,4}",
           bl((5,), (1, 4), (5,), (1, 4), (5,), (1, 4)))
    report("m5 k=6 l=6 witness: {1,4},{2,5},{1,4},{2,5},{1,4},{2,5}",
           bl((1, 4), (2, 5), (1, 4), (2, 5), (1, 4), (2, 5)))
    report("m6 sharp orbit: {1,2,3},{5,6},{1,2,4},{5,6},{1,3,4},{5,6}",
           bl((1, 2, 3), (5, 6), (1, 2, 4), (5, 6), (1, 3, 4), (5, 6)))
    report("all singletons {1},{2},{1},{2},{1},{2}", bl((1,), (2,), (1,), (2,), (1,), (2,)))
    report("all triples A,Ac alternating: {1,2,3},{4,5,6},...  [violates (C4)]",
           bl((1, 2, 3), (4, 5, 6), (1, 2, 3), (4, 5, 6), (1, 2, 3), (4, 5, 6)))
