"""Exact criterion + certified K_7 cover for cell-constant colourings of lattice rectangle tilings.
L = s Z x t Z, 0<s,t, s^2+t^2<1;  cells R(i,j) = [is-s/2,is+s/2] x [jt-t/2,jt+t/2].
For v = (p s, q t):   dmin^2 = max(0,|p|-1)^2 s^2 + max(0,|q|-1)^2 t^2,
                      dmax^2 = (|p|+1)^2 s^2 + (|q|+1)^2 t^2.
R x (R+v) is connected and distance is continuous, so the distance set is the closed interval
[dmin,dmax], both ends attained.  Hence cells R(0,0),R(v) contain a pair at distance exactly 1
iff dmin <= 1 <= dmax; call v FORCED.  A cell colouring is proper iff no colour class contains a
forced difference, so a proper k-colouring exists iff Cay(Z^2, F) is k-colourable, F = forced set;
6 pairwise-forced offsets give a 7-clique hence no proper 6-colouring.
Truncation is exact: forced needs dmin <= 1 and dmin >= |v|-sqrt(s^2+t^2), so |v| <= 1+sqrt(s^2+t^2).
All arithmetic exact integers with common denominator H=60 (M=H^2).
"""
from fractions import Fraction as Fr

H = 60
M = H * H

def sq(n):
    n = abs(n)
    return max(0, n - 1) ** 2

def forced_at_int(i, j, p, q):
    if p == 0 and q == 0: return False
    return (sq(p) * i * i + sq(q) * j * j <= M
            <= (abs(p) + 1) ** 2 * i * i + (abs(q) + 1) ** 2 * j * j)

def forced_at_frac(s, t, p, q):
    if p == 0 and q == 0: return False
    return (sq(p) * s * s + sq(q) * t * t <= 1
            <= (abs(p) + 1) ** 2 * s * s + (abs(q) + 1) ** 2 * t * t)

def window(i, j):
    i = max(i, 1); j = max(j, 1)
    # dmin^2 = sq(p) i^2 <= M  <=>  (|p|-1) <= sqrt(M)/i = H/i  <=>  |p| <= 1 + H//i
    return 1 + H // i + 1, 1 + H // j + 1

def forced_set_point(i, j):
    P, Q = window(i, j)
    return {(p, q) for p in range(-P, P + 1) for q in range(-Q, Q + 1) if forced_at_int(i, j, p, q)}

def guaranteed_box(i, j):
    """forced for EVERY (s,t) in (i/60,(i+1)/60] x (j/60,(j+1)/60]:
       dmin^2(s,t) <= dmin^2(upper) <= 1 and dmax^2(s,t) >= dmax^2(lower) >= 1 (both increasing)."""
    i1, j1 = i + 1, j + 1
    P, Q = window(i1, j1)
    out = set()
    for p in range(-P, P + 1):
        for q in range(-Q, Q + 1):
            if p == 0 and q == 0: continue
            if sq(p) * i1 * i1 + sq(q) * j1 * j1 > M: continue
            if (abs(p) + 1) ** 2 * i * i + (abs(q) + 1) ** 2 * j * j < M: continue
            out.add((p, q))
    return out

def clique_with_origin(G, target=7, budget=400000):
    verts = sorted(G, key=lambda v: (abs(v[0]) + abs(v[1]), v))
    best, nodes = [], [0]
    def adj(u, v): return (v[0] - u[0], v[1] - u[1]) in G
    def bk(cur, cand):
        if nodes[0] > budget: return True
        nodes[0] += 1
        if len(cur) == target - 1:
            best.extend(cur); return True
        if len(cur) + len(cand) < target - 1: return False
        for k, v in enumerate(cand):
            bk(cur + [v], [w for w in cand[k + 1:] if adj(v, w)])
            if best or nodes[0] > budget: return True
        return False
    bk([], verts)
    return [(0, 0)] + best if len(best) == target - 1 else None

def selftest(verbose=True):
    bad = 0
    for (i, j) in [(7, 9), (13, 40), (30, 30), (55, 58), (3, 2), (59, 59), (4, 51)]:
        G = forced_set_point(i, j)
        s, t = Fr(i, H), Fr(j, H)
        P, Q = window(i, j)
        ref = {(p, q) for p in range(-P, P + 1) for q in range(-Q, Q + 1) if forced_at_frac(s, t, p, q)}
        if G != ref:
            bad += 1
            if verbose: print("MISMATCH point", (i, j), len(G), len(ref))
        for (p, q) in guaranteed_box(i, j):
            for (a, b) in [(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)]:
                if a == 0 or b == 0: continue
                if not forced_at_int(a, b, p, q):
                    bad += 1
                    if verbose: print("BOX MISMATCH", (i, j), (p, q), (a, b))
    if verbose: print("selftest mismatches:", bad)
    return bad == 0

if __name__ == "__main__":
    print("selftest passed:", selftest())
