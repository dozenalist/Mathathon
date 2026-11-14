"""Two concentric circles: is a 4-chromatic configuration possible?

Graph Gamma(r,s): vertices S_r(x) + S_s(x) (disjoint union), edges
  within r: angular step theta_r,  2 r sin(theta_r/2) = 1
  within s: angular step theta_s
  cross:    alpha - beta = +- phi,  cos phi = (r^2+s^2-1)/(2 r s)
This script builds a finite ball of Gamma(r,s) around a base vertex and asks a
backtracking search for a proper 3-colouring.  A failure would be a finite
4-chromatic configuration on two concentric circles (a genuine counterexample to
"two concentric circles never force four colours"); a success is only evidence.

Pure float numerics with a 1e-9 tolerance: a failure must be re-verified exactly
before it is believed, a success is reported with its colouring.
"""
import math, sys, itertools

TOL = 1e-9

def wrap(a):
    a = a % (2 * math.pi)
    return a

def key(a):
    # quantise angle to a grid of 1e-9 rad
    k = round(wrap(a) / TOL)
    return k

def unkey(k):
    return wrap(k * TOL)

def nbrs_of(which, k, theta_r, theta_s, phi, has_r_edges, has_s_edges, has_cross):
    """neighbours of vertex (which, k); which in {0:circle r, 1:circle s}"""
    out = []
    a = unkey(k)
    if which == 0 and has_r_edges:
        out.append((0, key(a + theta_r)))
        out.append((0, key(a - theta_r)))
    if which == 1 and has_s_edges:
        out.append((1, key(a + theta_s)))
        out.append((1, key(a - theta_s)))
    if has_cross:
        if which == 0:
            out.append((1, key(a - phi)))
            out.append((1, key(a + phi)))
        else:
            out.append((0, key(a - phi)))
            out.append((0, key(a + phi)))
    return out

def build_ball(r, s, depth=5, base=None):
    theta_r = 2 * math.asin(0.5 / r) if r >= 0.5 else None
    theta_s = 2 * math.asin(0.5 / s) if s >= 0.5 else None
    gamma = (r * r + s * s - 1) / (2 * r * s)
    has_cross = abs(gamma) <= 1.0
    phi = math.acos(max(-1.0, min(1.0, gamma))) if has_cross else 0.0
    start = base if base is not None else (0, key(0.0))
    seen = {start: 0}
    frontier = [start]
    for _ in range(depth):
        nxt = []
        for v in frontier:
            for w in nbrs_of(v[0], v[1], theta_r, theta_s, phi, theta_r is not None,
                             theta_s is not None, has_cross):
                if w not in seen:
                    seen[w] = seen[v] + 1
                    nxt.append(w)
        frontier = nxt
    verts = list(seen)
    idx = {v: i for i, v in enumerate(verts)}
    adj = [set() for _ in verts]
    for v in verts:
        for w in nbrs_of(v[0], v[1], theta_r, theta_s, phi, theta_r is not None,
                         theta_s is not None, has_cross):
            if w in idx:
                adj[idx[v]].add(idx[w])
                adj[idx[w]].add(idx[v])
    return verts, adj, dict(theta_r=theta_r, theta_s=theta_s, phi=phi, gamma=gamma,
                            has_cross=has_cross)

def three_colour(adj, limit_nodes=3_000_000):
    """DSATUR backtracking for 3-colourability. Returns colouring or None."""
    n = len(adj)
    col = [-1] * n
    nodes = [0]
    order = []

    def pick():
        best, bestsat, bestdeg = -1, -1, -1
        for v in range(n):
            if col[v] != -1:
                continue
            sat = {col[u] for u in adj[v] if col[u] != -1}
            d = (len(sat), len(adj[v]))
            if d > (bestsat, bestdeg):
                best, bestsat, bestdeg = v, len(sat), len(adj[v])
        return best

    def dfs():
        nodes[0] += 1
        if nodes[0] > limit_nodes:
            raise TimeoutError
        if len(order) == n:
            return True
        v = pick()
        used = {col[u] for u in adj[v] if col[u] != -1}
        for c in range(3):
            if c in used:
                continue
            # colour symmetry: at most one new colour at a time
            if c > 0 and max([col[u] for u in range(n) if col[u] != -1], default=-1) < c - 1:
                continue
            col[v] = c
            order.append(v)
            if dfs():
                return True
            order.pop()
            col[v] = -1
        return False

    try:
        ok = dfs()
    except TimeoutError:
        return "timeout"
    return col if ok else None

def max_clique_bound(adj):
    """cheap: find largest clique by greedy; enough for a K4 test"""
    best = 1
    for v in range(len(adj)):
        clique = [v]
        for u in adj[v]:
            if all(u in adj[w] for w in clique):
                clique.append(u)
        best = max(best, len(clique))
    return best

if __name__ == "__main__":
    pairs = [(1.0, 1 / math.sqrt(2)), (1.0, 0.5), (1.0, 3 / math.sqrt(11)), (1.0, 2.0),
             (0.6, 0.8), (1.0, 1 / (2 * math.sin(math.pi / 5))), (2.0, 1.5),
             (1.0, 1.2), (0.55, 0.95), (1.0, 1 / (2 * math.sin(2 * math.pi / 7)))]
    for (r, s) in pairs:
        for depth in (4, 5):
            verts, adj, info = build_ball(r, s, depth=depth)
            mc = max_clique_bound(adj)
            res = three_colour(adj)
            tag = ("3-COLOURABLE" if isinstance(res, list) else
                   ("TIMEOUT" if res == "timeout" else "NOT 3-COLOURABLE"))
            print(f"r={r:.6f} s={s:.6f} depth={depth} n={len(verts):4d} "
                  f"clique<={mc} phi={info['phi']:.6f} -> {tag}", flush=True)
            if tag == "NOT 3-COLOURABLE":
                print("  *** candidate counterexample, must be re-verified exactly ***")
