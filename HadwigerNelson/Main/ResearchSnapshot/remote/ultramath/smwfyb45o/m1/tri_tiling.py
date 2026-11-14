#!/usr/bin/env python3
"""Equilateral-triangle-cell lattice tiling: exact forced-set / clique computation.

Cells: U = conv(0,e1,e2), D = conv(e1,e2,e1+e2) with e1=(1,0), e2=(1/2,sqrt3/2),
both scaled by the side l>0.  All arithmetic is in the lattice basis (x1,x2)
with the exact rational form <x,y> = x1y1+(x1y2+x2y1)/2+x2y2, |x|^2=x1^2+x1x2+x2^2,
so squared distances are (rational)*l^2.  No floating point in any decision.
"""
from fractions import Fraction as F
import sys, time

def ip(a, b):
    return a[0]*b[0] + (a[0]*b[1] + a[1]*b[0])/2 + a[1]*b[1]

def n2(a):
    return a[0]*a[0] + a[0]*a[1] + a[1]*a[1]

def seg_dist2(p, a, b):
    ab = (b[0]-a[0], b[1]-a[1])
    L = n2(ab)
    if L == 0:
        return n2((p[0]-a[0], p[1]-a[1]))
    t = ip((p[0]-a[0], p[1]-a[1]), ab) / L
    if t < 0: t = F(0)
    if t > 1: t = F(1)
    q = (a[0] + t*ab[0], a[1] + t*ab[1])
    return n2((p[0]-q[0], p[1]-q[1]))

def poly_pair(P, Q):
    dmax2 = max(n2((p[0]-q[0], p[1]-q[1])) for p in P for q in Q)
    dmin2 = None
    for p in P:
        for i in range(len(Q)):
            d = seg_dist2(p, Q[i], Q[(i+1) % len(Q)])
            if dmin2 is None or d < dmin2: dmin2 = d
    for q in Q:
        for i in range(len(P)):
            d = seg_dist2(q, P[i], P[(i+1) % len(P)])
            if dmin2 is None or d < dmin2: dmin2 = d
    return dmin2, dmax2

U = [(F(0),F(0)), (F(1),F(0)), (F(0),F(1))]
D = [(F(1),F(0)), (F(0),F(1)), (F(1),F(1))]

def shifted(P, v):
    return [(p[0]+v[0], p[1]+v[1]) for p in P]

def forced_sets(l2):
    one = F(1)
    R = 3
    while F(R*R) * l2 < one:
        R *= 2
    R = R + 3
    FUU, FUD = set(), set()
    for i in range(-R, R+1):
        for j in range(-R, R+1):
            v = (F(i), F(j))
            if (i, j) != (0, 0):
                dmn, dmx = poly_pair(U, shifted(U, v))
                if dmn*l2 <= one <= dmx*l2:
                    FUU.add((i, j))
            dmn, dmx = poly_pair(U, shifted(D, v))
            if dmn*l2 <= one <= dmx*l2:
                FUD.add((i, j))
    return FUU, FUD

def max_clique_cells(FUU, FUD):
    verts = [(0, 0, 0)]
    for w in sorted(FUU):
        if w != (0, 0):
            verts.append((0, int(w[0]), int(w[1])))
    for w in sorted(FUD):
        verts.append((1, int(w[0]), int(w[1])))
    verts = list(dict.fromkeys(verts))
    n = len(verts)
    def conflict(a, b):
        if a == b: return False
        wa = (a[1]-b[1], a[2]-b[2])
        if a[0] == b[0]:
            return wa in FUU and wa != (0, 0)
        return wa in FUD or (-wa[0], -wa[1]) in FUD
    adj = [[False]*n for _ in range(n)]
    for a in range(n):
        for b in range(a+1, n):
            if conflict(verts[a], verts[b]):
                adj[a][b] = adj[b][a] = True
    best = [0, []]
    def rec(chosen, cands):
        if len(chosen) > best[0]:
            best[0] = len(chosen); best[1] = list(chosen)
        cl = list(cands)
        for idx, v in enumerate(cl):
            if len(chosen) + len(cl) - idx <= best[0]:
                return
            rec(chosen + [v], [u for u in cl[idx+1:] if adj[v][u]])
    anchor = verts.index((0, 0, 0))
    rec([anchor], [i for i in range(n) if adj[anchor][i]])
    return best[0], [verts[i] for i in best[1]]

if __name__ == "__main__":
    print("typed forced graph, max clique (>=7 ==> NO proper 6-colouring)")
    for num, den in [(1,100),(1,40),(1,25),(1,16),(1,12),(1,9),(1,8),(3,20),(1,6),(1,5),(1,4),(3,10),(1,3),(2,5),(1,2),(3,5),(2,3),(3,4),(9,10)]:
        l2 = F(num, den)
        t0 = time.time()
        FUU, FUD = forced_sets(l2)
        om, cl = max_clique_cells(FUU, FUD)
        print("l^2=%d/%d l=%.4f |F_UU|=%d |F_UD|=%d omega=%d clique=%s [%.1fs]" % (num, den, float(l2)**0.5, len(FUU), len(FUD), om, cl, time.time()-t0))
        sys.stdout.flush()
