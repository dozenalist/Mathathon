"""Exact unit-distance graphs, exact validation, and certified colourability decisions."""
from fractions import Fraction
from itertools import combinations
import json

from .exact import Field


class PointSet:
    """Points with coordinates in a Field.  Coordinate = (x_expr, y_expr) where an
    expr is a dict {basis_value: Fraction} (see exact.Field.sqrt / rat)."""

    def __init__(self, radicands):
        self.F = Field(radicands)
        self.pts = []
        self.names = []

    def P(self, name, xexpr=None, yexpr=None, xy=None):
        F = self.F
        if xy is not None:
            xexpr, yexpr = xy
        x = F.rat(0) if xexpr is None else _mk(F, xexpr)
        y = F.rat(0) if yexpr is None else _mk(F, yexpr)
        self.pts.append((x, y))
        self.names.append(name)
        return len(self.pts) - 1

    def canonical(self):
        """Merge coincident points (exact), keeping first occurrence names."""
        F = self.F
        keep, names, dup = [], [], 0
        for i, pt in enumerate(self.pts):
            hit = None
            for j in keep:
                if F.eq(self.pts[j][0], pt[0]) and F.eq(self.pts[j][1], pt[1]):
                    hit = j
                    break
            if hit is None:
                keep.append(i)
                names.append(self.names[i])
            else:
                dup += 1
                names[keep.index(hit)] += "=" + self.names[i]
        out = PointSet(F.rs)
        out.pts = [self.pts[i] for i in keep]
        out.names = names
        return out, dup

    def copy(self):
        ps = PointSet(self.F.rs)
        ps.pts = list(self.pts)
        ps.names = list(self.names)
        return ps

    def sqdist(self, i, j):
        F = self.F
        dx = F.sub(self.pts[i][0], self.pts[j][0])
        dy = F.sub(self.pts[i][1], self.pts[j][1])
        return F.add(F.mul(dx, dx), F.mul(dy, dy))

    def unit_graph(self):
        n = len(self.pts)
        adj = [set() for _ in range(n)]
        nonedges = []
        for i, j in combinations(range(n), 2):
            d2 = self.sqdist(i, j)
            if self.F.is_zero(self.F.sub(d2, self.F.one)):
                adj[i].add(j)
                adj[j].add(i)
            else:
                nonedges.append((i, j))
        return adj, nonedges


def _mk(F, expr):
    out = list(F.zero)
    for b, c in expr.items():
        out[F.idx[int(b)]] += Fraction(c)
    return tuple(out)


def numeric_check(pts, F, adj, tol_hit=1e-25, tol_miss=1e-25, dps=60):
    """Independent high-precision evaluation: every edge must have |d^2-1| < tol_hit,
    every non-edge must have |d^2-1| > tol_miss.  Guards against field-arithmetic bugs."""
    import mpmath as mp
    mp.mp.dps = dps
    rs = F.rs

    def ev(x):
        s = mp.mpf(0)
        for c, b in zip(x, F.basis):
            if not c:
                continue
            k, sq = _sf(b)
            s += mp.mpf(c.numerator) / mp.mpf(c.denominator) * mp.mpf(k) * mp.sqrt(sq)
        return s

    xy = [(ev(x), ev(y)) for x, y in pts]
    worst_hit = mp.mpf(0)
    best_miss = mp.mpf(1)
    n = len(xy)
    for i, j in combinations(range(n), 2):
        d2 = (xy[i][0] - xy[j][0]) ** 2 + (xy[i][1] - xy[j][1]) ** 2
        dev = abs(d2 - 1)
        if j in adj[i]:
            worst_hit = max(worst_hit, dev)
        else:
            best_miss = min(best_miss, dev)
    return worst_hit, best_miss


def _sf(n):
    from .exact import squarefree_split
    return squarefree_split(n)


# ---------------------------------------------------------------- colourability
def exhaustive_count(adj, k, cap=None):
    """Exact count of proper k-colourings of the labelled graph (adj as sets).
    Returns (count, first colouring or None).  Complete: no cap by default."""
    n = len(adj)
    order = sorted(range(n), key=lambda v: -len(adj[v]))
    col = [-1] * n
    count = 0
    first = [None]

    def rec(pos):
        nonlocal count
        if pos == n:
            count += 1
            if first[0] is None:
                first[0] = list(col)
            return
        v = order[pos]
        used = {col[u] for u in adj[v] if col[u] >= 0}
        for c in range(k):
            if c in used:
                continue
            col[v] = c
            rec(pos + 1)
            col[v] = -1
            if cap is not None and count > cap:
                return
        return

    rec(0)
    # first[0] is already indexed by vertex id (col[v] is set inside the recursion)
    return count, first[0]


def verify_colouring(adj, col, k):
    if any(c is None or c < 0 or c >= k for c in col):
        return False, "colour out of range / uncoloured"
    for v, S in enumerate(adj):
        for u in S:
            if u > v and col[u] == col[v]:
                return False, f"monochromatic edge {v}-{u}"
    return True, "ok"


def cnf(adj, k):
    """CNF for k-colourability: var (v,c) = v*k+c+1. Returns (nvars, clauses)."""
    n = len(adj)
    cl = [[v * k + c + 1 for c in range(k)] for v in range(n)]
    for v, S in enumerate(adj):
        for u in S:
            if u > v:
                for c in range(k):
                    cl.append([-(v * k + c + 1), -(u * k + c + 1)])
    return n * k, cl


def sat_decision(adj, k, solvers=("cadical153", "minisat22"), time_limit=None):
    """Decision by CDCL.  Returns dict with per-solver verdicts and a model."""
    from pysat.formula import CNF
    from pysat.solvers import Solver
    nv, cl = cnf(adj, k)
    f = CNF()
    for c in cl:
        f.append(c)
    res = {"nvars": nv, "nclauses": len(cl), "verdicts": {}, "model": None}
    n = len(adj)
    for s in solvers:
        kw = {"bootstrap_with": f.clauses}
        if time_limit:
            kw["time_limit"] = time_limit
        with Solver(name=s, **kw) as sol:
            ok = sol.solve()
            res["verdicts"][s] = "SAT" if ok else "UNSAT"
            if ok and res["model"] is None:
                m = set(sol.get_model())
                res["model"] = [next(c for c in range(k) if (v * k + c + 1) in m) for v in range(n)]
    return res


def clique_number_bound(adj):
    """Exact maximum clique size (graphs here are small); a unit-distance graph must be K_4-free."""
    n = len(adj)
    best = 0
    for r in range(1, n + 1):
        found = False
        for S in combinations(range(n), r):
            if all(b in adj[a] for a, b in combinations(S, 2)):
                found = True
                break
        if found:
            best = r
        else:
            break
    return best


def degrees(adj):
    return sorted(len(a) for a in adj)


def validate(ps, adj, nonedges, name, log):
    """Full validation record for one exact unit-distance graph."""
    n = len(ps.pts)
    wh, bm = numeric_check(ps.pts, ps.F, adj)
    deg = degrees(adj)
    omega = clique_number_bound(adj)
    # all points distinct
    distinct = all(not ps.F.is_zero(ps.F.sub(ps.pts[i][0], ps.pts[j][0])) or
                   not ps.F.is_zero(ps.F.sub(ps.pts[i][1], ps.pts[j][1]))
                   for i, j in combinations(range(n), 2))
    rec = {
        "name": name, "n": n, "m": sum(deg) // 2, "field": ps.F.rs,
        "max_num_dev_on_edges": float(wh), "min_num_dev_off_edges": float(bm),
        "all_points_distinct": distinct, "clique_number": omega,
        "min_degree": deg[0], "max_degree": deg[-1],
        "is_unit_distance_graph": bool(float(wh) < 1e-25 and distinct),
        "k4_free": omega <= 3,
    }
    log(f"  [{name}] n={rec['n']} m={rec['m']} field=Q(sqrt{ps.F.rs}) "
        f"maxdev(edges)={rec['max_num_dev_on_edges']:.2e} "
        f"min|d2-1|(nonedges)={rec['min_num_dev_off_edges']:.3f} "
        f"omega={omega} distinct={distinct}")
    return rec
