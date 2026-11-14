"""Independent verification (separate code path, same exact arithmetic) plus 6-colouring search.

(1) CROSS-CHECK of the polygon geometry against the closed-form rectangle formula quoted in
    the problem statement: for a=(s,0), b=(0,t),
        dmin^2 = max(0,|p|-1)^2 s^2 + max(0,|q|-1)^2 t^2
        dmax^2 = (|p|+1)^2 s^2 + (|q|+1)^2 t^2
    My Para.dmin2/dmax2 use polygon vertex/edge geometry and never use this formula, so
    agreement on a large sample of exact rationals is a genuine check of the geometry code.

(2) CERTIFICATE: check that a given list of index points is a clique of the forced graph, by
    printing every pairwise difference with its exact [dmin^2, dmax^2].

(3) 6-COLOURING SEARCH: exact DFS for periodic colourings c: (Z/n)^2 -> Z/6 with
    c(x) != c(x+v) for every forced v.  A hit is a genuine full-plane 6-colouring of that
    tiling (it is periodic, and every constraint is checked for every cell class).
"""
from fractions import Fraction as Fr
from itertools import product
from para6 import Para, n2, sub, smul, add, graph, max_clique, linear_mod6  # noqa
import para6, sys, random

def rectangle_formula(s, t, p, q):
    dmin2 = max(0, abs(p) - 1) ** 2 * s * s + max(0, abs(q) - 1) ** 2 * t * t
    dmax2 = (abs(p) + 1) ** 2 * s * s + (abs(q) + 1) ** 2 * t * t
    return dmin2, dmax2

def cross_check(trials=200, rng=range(-6, 7)):
    random.seed(7)
    for _ in range(trials):
        s = Fr(random.randint(1, 40), random.randint(1, 40))
        t = Fr(random.randint(1, 40), random.randint(1, 40))
        para = Para((s, Fr(0)), (Fr(0), t), check_diam=False)
        for p in rng:
            for q in rng:
                v = para.offset(p, q)
                a1, a2 = para.dmin2(v), para.dmax2(v)
                b1, b2 = rectangle_formula(s, t, p, q)
                assert a1 == b1, (s, t, p, q, a1, b1)
                assert a2 == b2, (s, t, p, q, a2, b2)
    print("cross-check OK: polygon geometry == closed-form rectangle formula "
          f"on {trials} random rational (s,t) x 169 offsets each")

def check_clique(a, b, pts):
    para = Para(a, b)
    print(f"-- clique certificate for a={a} b={b}, diam^2={para.diam2} --")
    ok = True
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            p = pts[j][0] - pts[i][0]; q = pts[j][1] - pts[i][1]
            v = para.offset(p, q)
            d1, d2 = para.dmin2(v), para.dmax2(v)
            f = (d1 <= 1 <= d2)
            ok &= f
            print(f"   {pts[i]} - {pts[j]}  v={p}a+{q}b  dmin^2={d1}  dmax^2={d2}  "
                  f"1 in [dmin,dmax]: {f}")
    print(f"   => {len(pts)} points pairwise forced: K_{len(pts)} {'CERTIFIED' if ok else 'FAILED'}")
    return ok

# (3) periodic 6-colouring search
def periodic6(a, b, F, n, m=6, node_limit=3_000_000):
    cells = [(i, j) for i in range(n) for j in range(n)]
    idx = {c: k for k, c in enumerate(cells)}
    nb = [[idx[((i + p) % n, (j + q) % n)] for (p, q) in F] for (i, j) in cells]
    nb = [sorted(set(x)) for x in nb]
    for k, (i, j) in enumerate(cells):
        if k in nb[k]:
            return None                      # a forced vector is 0 mod n -> impossible
    col = [-1] * len(cells)
    nodes = [0]
    order = sorted(range(len(cells)), key=lambda k: -len(nb[k]))
    def dfs(t):
        nodes[0] += 1
        if nodes[0] > node_limit:
            raise TimeoutError
        if t == len(order):
            return True
        k = order[t]
        used = {col[d] for d in nb[k] if col[d] >= 0}
        for x in range(m):
            if x not in used:
                col[k] = x
                if dfs(t + 1):
                    return True
                col[k] = -1
        return False
    try:
        okc = dfs(0)
    except TimeoutError:
        return 'limit'
    if not okc:
        return None
    return {(i, j): col[idx[(i, j)]] for (i, j) in cells}, nodes[0]

def verify_periodic6(a, b, colouring, n, m=6):
    """Full exact verification: for every forced v and every cell class x, colours differ."""
    para = Para(a, b)
    F = para.forced_set()
    for v in F:
        for (i, j), c in colouring.items():
            d = colouring[((i + v[0]) % n, (j + v[1]) % n)]
            assert d != c, ("CLASH", v, (i, j))
    return True

if __name__ == '__main__':
    cross_check()
    print()
    check_clique((Fr(2, 5), Fr(0)), (Fr(0), Fr(2, 5)),
                 [(0, 0), (1, -1), (1, 1), (2, -2), (2, 0), (3, -1), (3, 1)])
    print()
    print("=== full clique certificates for a list of rational parallelograms ===")
    FAM = [((Fr(2, 5), Fr(0)), (Fr(0), Fr(2, 5))),          # 0.4 x 0.4 square
           ((Fr(2, 5), Fr(0)), (Fr(0), Fr(1, 2))),          # rectangle
           ((Fr(1, 3), Fr(0)), (Fr(1, 6), Fr(1, 3))),       # slanted
           ((Fr(1, 3), Fr(1, 3)), (Fr(1, 3), Fr(-1, 3))),   # 60-degree rhombus
           ((Fr(1, 4), Fr(0)), (Fr(1, 2), Fr(1, 4))),       # slanted
           ]
    certified = []
    for a, b in FAM:
        para = Para(a, b)
        F = para.forced_set()
        V, adj = graph(F)
        Cl = max_clique(sorted(V), adj)
        if len(Cl) >= 7:
            if check_clique(a, b, sorted(Cl)):
                certified.append((a, b, len(Cl)))
        print()
    print("CERTIFIED no-6-colouring:", certified)
    print()
    print("=== periodic 6-colouring search for the low-omega cases ===")
    for a, b in [((Fr(1, 5), Fr(0)), (Fr(0), Fr(1, 5))),
                 ((Fr(1, 4), Fr(0)), (Fr(0), Fr(1, 4))),
                 ((Fr(2, 7), Fr(0)), (Fr(0), Fr(2, 7))),
                 ((Fr(3, 10), Fr(0)), (Fr(1, 5), Fr(1, 4))),
                 ((Fr(3, 10), Fr(0)), (Fr(0), Fr(3, 10))),
                 ((Fr(1, 3), Fr(0)), (Fr(0), Fr(1, 3)))]:
        para = Para(a, b)
        F = para.forced_set()
        V, adj = graph(F)
        w = len(max_clique(sorted(V), adj))
        res = []
        for n in (4, 5, 6, 7, 8):
            r = periodic6(a, b, F, n)
            if r in (None, 'limit'):
                res.append((n, r))
            else:
                col, nodes = r
                assert verify_periodic6(a, b, col, n)
                res.append((n, 'FOUND'))
                print("   !!! 6-COLOURING FOUND:", a, b, "period", n, "nodes", nodes)
                print("   pattern (row j, col i):",
                      [[col[(i, j)] for i in range(n)] for j in range(n)])
                break
        print(f"a={a} b={b} omega={w} search={res}")

