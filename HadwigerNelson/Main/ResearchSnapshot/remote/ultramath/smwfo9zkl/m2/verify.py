"""Exact verification for d13 (member m2, swarm smwfo9zkl).

Three independent finite checks.
E1  The k=6 core of Theorem B (two-centre palette bound):
    no two disjoint 3-subsets of [6] leave a nonempty label free.
    General k: the bound |P_x(e)|+|P_y(e)| <= k-1 is trivial for k<=5,
    genuine exactly at k=6, and vacuous (unsatisfiable premise) for k>=7.
E2  Theorem A (palette systems are colourings) on a non-trivial
    unit-distance graph: the Moser spindle (chi = 4), exact coordinates.
    k=3 must be UNSAT for sets of any size, k=4 SAT; every solution's
    minimum-map must be a proper colouring.
E3  Vacuity check for Theorem B: the single-centre constraints at k=6
    (sixty-degree exclusion + no exhausted union) DO admit a model with a
    ternary palette, so Theorem B is genuinely a two-centre statement.
"""
import itertools, json
from fractions import Fraction as F
import sympy as sp

# ---------------------------------------------------------------- E1
def e1():
    """Counting core of Theorem B.  For general k the palette bound is
    1 <= |P| <= k-3.  Count unordered pairs {A,B} of palettes with |A|=|B|=k-3
    that are disjoint, and of those how many have A u B = [k] (which is what
    makes the equilateral completion have no free label)."""
    out = {}
    for k in range(4, 9):
        b = k - 3
        sets = [frozenset(c) for c in itertools.combinations(range(1, k + 1), b)]
        full = frozenset(range(1, k + 1))
        disj = fill = 0
        for A, B in itertools.combinations(sets, 2):
            if not (A & B):
                disj += 1
                fill += (A | B == full)
        # also: for any disjoint pair not filling [k], a nonempty free label exists
        spare_ok = all(any(True for C in sets for l in C if l not in (A | B))
                       for A, B in itertools.combinations(sets, 2) if not (A & B))
        out[k] = dict(bound=b, disjoint_pairs=disj, pairs_filling_all_labels=fill,
                      every_other_pair_has_free_label=spare_ok)
    return out

# ---------------------------------------------------------------- geometry
s3, s11 = sp.sqrt(3), sp.sqrt(11)
def moser_spindle():
    """7 vertices, exact coordinates in Q(sqrt3, sqrt11); returns (pts, edges)."""
    o = sp.Matrix([0, 0])
    # diamond 1: hinge o, r1,s1 at unit distance from o and each other, tip q1
    r1 = sp.Matrix([1, 0]); s1 = sp.Matrix([sp.Rational(1, 2), s3 / 2])
    q1 = r1 + s1                                     # (3/2, sqrt3/2), |q1|^2 = 3
    c, s = sp.Rational(5, 6), s11 / 6                # cos,sin of the tip angle
    d = sp.Matrix([(5 * s3 - s11) / 12, (5 + sp.sqrt(33)) / 12])   # unit direction
    q2 = s3 * d
    # r2,s2: equilateral apexes on segment o q2
    m = q2 / 2
    perp = sp.Matrix([-q2[1], q2[0]]) / sp.sqrt(3)   # unit perpendicular
    r2 = m + perp / 2; s2 = m - perp / 2
    pts = [o, r1, s1, q1, r2, s2, q2]
    edges = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d2 = sp.simplify((pts[i] - pts[j]).dot(pts[i] - pts[j]))
            if sp.simplify(d2 - 1) == 0:
                edges.append((i, j))
    return pts, edges

# ---------------------------------------------------------------- CSP
def csp_solve(n, edges, k, maxsize=None, all_solutions=False, limit=None):
    """Palette CSP: each vertex gets a nonempty subset of [k] of size <= maxsize,
    palettes disjoint across every edge.  Backtracking with forward checking."""
    vals = [frozenset(c) for r in range(1, (maxsize or k) + 1)
            for c in itertools.combinations(range(1, k + 1), r)]
    nbr = {v: [w for (a, b) in edges for (v, w) in ((a, b), (b, a)) if v == a or v == b] for v in range(n)}
    nbr = {v: sorted({w for (a, b) in edges if a == v for w in [b]} | {a for (a, b) in edges if b == v for w in [a]})
           for v in range(n)}
    sols = []
    dom = {v: list(vals) for v in range(n)}
    def bt(assign):
        if limit and len(sols) >= limit:
            return
        if len(assign) == n:
            sols.append(dict(assign)); return
        v = min((u for u in range(n) if u not in assign), key=lambda u: len(dom[u]))
        for A in dom[v]:
            newdom = {}
            ok = True
            for w in nbr[v]:
                if w in assign:
                    continue
                d = [B for B in dom[w] if not (A & B)]
                if not d:
                    ok = False; break
                newdom[w] = d
            if not ok:
                continue
            saved = {w: dom[w] for w in newdom}
            dom.update(newdom); assign[v] = A
            bt(assign)
            del assign[v]
            dom.update(saved)
            if not all_solutions and sols:
                return
        return
    bt({})
    return sols

def csp_solve_sympy(n, edges, k, maxsize=None):
    """Independent second decision procedure: CNF + sympy's DPLL."""
    from sympy.logic.inference import satisfiable
    from sympy import symbols
    vals = [frozenset(c) for r in range(1, (maxsize or k) + 1)
            for c in itertools.combinations(range(1, k + 1), r)]
    sx = {}
    for v in range(n):
        for A in vals:
            sx[(v, A)] = symbols(f"p{v}_{'_'.join(map(str, sorted(A)))}")
    clauses = []
    for v in range(n):
        clauses.append([sx[(v, A)] for A in vals])                      # at least one
        for A, B in itertools.combinations(vals, 2):                    # at most one
            clauses.append([~sx[(v, A)], ~sx[(v, B)]])
    for (a, b) in edges:                                                # disjointness
        for A in vals:
            for B in vals:
                if A & B:
                    clauses.append([~sx[(a, A)], ~sx[(b, B)]])
    f = True
    for cl in clauses:
        g = False
        for lit in cl:
            g = lit if g is False else (g | lit)
        f = g if f is True else (f & g)
    return satisfiable(f)

def is_proper(col, edges):
    return all(col[a] != col[b] for a, b in edges)

def min_map(sol):
    return {v: min(A) for v, A in sol.items()}

# ---------------------------------------------------------------- E3
def e3():
    """Single-centre k=6 model: A_0..A_5 nonempty subsets of [6], |A_j|<=3,
    A_j cap A_{j+1}=empty, A_j cup A_l != [6] for l-j in {1,2,4,5}."""
    full = set(range(1, 7))
    vals = [frozenset(c) for r in range(1, 4) for c in itertools.combinations(range(1, 7), r)]
    bad = {1, 2, 4, 5}
    sols = []
    def ok(seq, j, A):
        for i, B in enumerate(seq):
            d = (j - i) % 6
            if d in bad and (A | B) == full:
                return False
            if d in (1, 5) and (A & B):
                return False
        return True
    def bt(seq):
        j = len(seq)
        if j == 6:
            if (seq[0] & seq[5]) or (seq[0] | seq[5]) == full:   # close the cycle
                return
            sols.append(tuple(seq)); return
        for A in vals:
            if j == 0 and len(A) != 3:
                continue
            if ok(seq, j, A):
                seq.append(A); bt(seq); seq.pop()
            if len(sols) > 3: return
    bt([])
    return [tuple(sorted(A) for A in s) for s in sols[:3]]

if __name__ == "__main__":
    res = {}
    res["E1"] = e1()
    pts, edges = moser_spindle()
    res["graph"] = dict(n=len(pts), m=len(edges), edges=edges)
    res["E2"] = {}
    for k, ms in [(2, None), (3, None), (4, None), (4, 1), (6, 3), (6, 2)]:
        key = f"k{k}_max{ms}"
        sols = csp_solve(len(pts), edges, k, maxsize=ms, all_solutions=False, limit=1)
        res["E2"][key] = dict(sat=bool(sols), witness=None if not sols else
                              {v: sorted(A) for v, A in sols[0].items()})
    # all solutions at k=4 and k=6max3 -> check min-selection on every one
    for k, ms in [(4, 1), (6, 2)]:
        sols = csp_solve(len(pts), edges, k, maxsize=ms, all_solutions=True, limit=20000)
        res["E2"][f"k{k}_max{ms}_allsol"] = dict(count=len(sols),
            min_map_proper=all(is_proper(min_map(s), edges) for s in sols),
            min_maps=len({tuple(sorted(min_map(s).items())) for s in sols}))
    # independent procedure
    for k, ms in [(3, None), (4, None)]:
        v = csp_solve_sympy(len(pts), edges, k, maxsize=ms)
        res["E2"][f"sympy_k{k}_max{ms}"] = dict(sat=bool(v))
    res["E3"] = e3()
    print(json.dumps(res, indent=1, default=str))
