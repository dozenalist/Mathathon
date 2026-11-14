#!/usr/bin/env python3
"""Checks for S7-INPUT.md (swarm smwfo9zkl, member m12, direction d9).

A. Section 5.3 exact: multiplicity-3 open covers of every mesh exist, so the
   multiplicity-two hypothesis of the cover obstruction (Lemma 5.1) is essential.
   All lattice arithmetic is exact: the triangular lattice with spacing d is
   identified with Z + Z*omega, omega = exp(i*pi/3).  A lattice point (a,b) is
   d*(a + b/2, b*sqrt(3)/2), and the SQUARED distance between (a,b) and (c,e),
   divided by d^2, is the integer  (a-c)^2 + (a-c)(b-e) + (b-e)^2.
   No floating point is used for the three structural claims.

B. Lemma 6.1 by exhaustive enumeration of all 2^15 graphs on six vertices,
   with two independent acyclicity tests (union-find and DFS back edge).

C. The k=6 cycle count needed for the pigeonhole in Step 6, two ways.

D. Numerical check of the Brouwer mechanism of Lemma 5.1: a multiplicity-two
   cover with mesh above the inradius exists and its partition-of-unity image
   misses the central point; the multiplicity-three cover of A has mesh below
   the inradius and its image reaches the central point.
"""

from fractions import Fraction as F
import itertools
import math
import sys

FAIL = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (("  [" + detail + "]") if detail else ""))
    if not ok:
        FAIL.append(name)

# ---------------------------------------------------------------- A: covers
# Squared distance / d^2 between lattice points (a,b), (c,e); exact integer.
def n2(p, q):
    da, db = p[0] - q[0], p[1] - q[1]
    return da * da + da * db + db * db

def lattice_points(R):
    """All (a,b) with |d*(a+b*omega)| <= R*d, i.e. a^2+ab+b^2 <= R^2 (R integer)."""
    out = []
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            if a * a + a * b + b * b <= R * R:
                out.append((a, b))
    return out

def part_A():
    print("\n== A. multiplicity-three covers with mesh <= m for every m ==")
    # claim 1: covering radius d/sqrt(3) < 4d/5  (exact: 1/3 < 16/25)
    check("A1 covering radius d/sqrt(3) < 4d/5", F(1, 3) < F(16, 25),
          "1/3 < 16/25")
    # claim 2: no four lattice points have all pairwise distances < 8d/5.
    #   the norm form a^2+ab+b^2 takes values {0,1,3,4,7,9,...};  (8/5)^2 = 64/25 = 2.56,
    #   so a pair at distance < 8d/5 has norm 0 or 1, i.e. distance 0 or d.
    R = 4
    pts = lattice_points(R)
    bad = 0
    for quad in itertools.combinations(pts, 4):
        if all(n2(p, q) * 25 < 64 for p, q in itertools.combinations(quad, 2)):
            bad += 1
    check("A2 no 4 lattice points with all pairwise distances < 8d/5", bad == 0,
          "exhaustive over %d points, %d violations" % (len(pts), bad))
    tri = [(0, 0), (1, 0), (0, 1)]
    check("A2-control 3 points with pairwise distances < 8d/5 do exist",
          all(n2(p, q) * 25 < 64 for p, q in itertools.combinations(tri, 2)))
    # claim 3: the circumcentre of an elementary triangle is at distance
    #   d/sqrt(3) < r = 4d/5 from its three vertices: exactly A1.
    check("A3 elementary triangle gives multiplicity >= 3 at its circumcentre",
          F(1, 3) < F(16, 25))
    # numerical scan: count lattice points within radius 4d/5 of z, fine grid
    counts = {}
    N = 240
    for i in range(N):
        for j in range(N):
            x, y = i / N, j / N
            cnt = 0
            for a in range(-2, 3):
                for b in range(-2, 3):
                    px = a + b / 2.0
                    py = b * math.sqrt(3) / 2.0
                    if (x - px) ** 2 + (y - py) ** 2 < (4 / 5) ** 2:
                        cnt += 1
            counts[cnt] = counts.get(cnt, 0) + 1
    check("A4 scanned multiplicity is exactly 3 (counts on a 240x240 grid)",
          sorted(counts) == [1, 2, 3], "multiplicities seen: %s" % (sorted(counts),))
    for m in [F(1, 10), F(1, 3), F(3, 2), F(7)]:
        d = 5 * m / 8
        r = 4 * d / 5
        check("A5 mesh 2r <= m for m=%s" % m, 2 * r <= m, "2r=%s" % (2 * r,))

# ---------------------------------------------------- B: forests have no K3
def acyclic_unionfind(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False          # closing an edge inside a component: cycle
        parent[ru] = rv
    return True

def acyclic_dfs(n, edges):
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    state = [0] * n               # 0 white, 1 grey, 2 black
    for s in range(n):
        if state[s]:
            continue
        stack = [(s, -1)]
        while stack:
            u, par = stack.pop()
            if state[u] == 0:
                state[u] = 1
                stack.append((u, par))
                for w in adj[u]:
                    if w == par:
                        continue
                    if state[w] == 1:
                        return False   # back edge
                    if state[w] == 0:
                        stack.append((w, u))
            else:
                state[u] = 2
    return True

def has_triangle(n, edges):
    E = set(edges)
    for a, b, c in itertools.combinations(range(n), 3):
        if (a, b) in E and (b, c) in E and (a, c) in E:
            return True
    return False

def part_B():
    print("\n== B. Lemma 6.1: cliques in a forest have at most two vertices ==")
    n = 6
    pairs = list(itertools.combinations(range(n), 2))
    n_forest = n_tri = n_disagree = bad = 0
    for mask in range(1 << len(pairs)):
        edges = [pairs[k] for k in range(len(pairs)) if mask >> k & 1]
        ac1 = acyclic_unionfind(n, edges)
        ac2 = acyclic_dfs(n, edges)
        if ac1 != ac2:
            n_disagree += 1
        tri = has_triangle(n, edges)
        n_forest += ac1
        n_tri += tri
        if (ac1 and tri) or (tri and ac1):
            bad += 1
        if tri and not ac2:
            pass                       # consistent
    check("B1 the two acyclicity tests agree on all 2^15 graphs", n_disagree == 0,
          "%d disagreements" % n_disagree)
    check("B2 every acyclic graph on 6 vertices is triangle-free", bad == 0,
          "%d forests, %d graphs with a triangle, of %d graphs"
          % (n_forest, n_tri, 1 << len(pairs)))
    check("B3 the control triangle is detected",
          has_triangle(6, [(0, 1), (1, 2), (0, 2)])
          and not has_triangle(6, [(0, 1), (1, 2)])
          and not has_triangle(6, [(0, 1), (1, 2), (2, 3)]),
          "K3 yes, path no, 4-cycle no")

# ------------------------------------------------- C: cycle counts for k=6
def simple_cycles_bruteforce(n):
    out = {}
    for L in range(3, n + 1):
        seen = set()
        for perm in itertools.permutations(range(n), L):
            k = perm.index(min(perm))
            rot = perm[k:] + perm[:k]
            rev = (rot[0],) + tuple(reversed(rot[1:]))
            seen.add(min(rot, rev))
        out[L] = len(seen)
    return out

def simple_cycles_formula(n):
    return {L: math.comb(n, L) * math.factorial(L - 1) // 2 for L in range(3, n + 1)}

def part_C():
    print("\n== C. simple cycles in the complete graph on 6 vertices ==")
    bf = simple_cycles_bruteforce(6)
    fo = simple_cycles_formula(6)
    check("C1 brute force and closed formula agree", bf == fo, "%s vs %s" % (bf, fo))
    check("C2 20 + 45 + 72 + 60 = 197 cycles total", sum(bf.values()) == 197,
          "sum=%d" % sum(bf.values()))
    check("C3 the four lengths 3,4,5,6 all occur", sorted(bf) == [3, 4, 5, 6])

# --------------------------------------- D: the Brouwer mechanism of Lemma 5.1
def pou_image(grid, centres, radius):
    out = []
    for z in grid:
        ws, U = 0.0, [0.0, 0.0]
        for c in centres:
            d = math.hypot(z[0] - c[0], z[1] - c[1])
            w = max(0.0, radius - d)
            if w > 0:
                ws += w
                U[0] += w * c[0]
                U[1] += w * c[1]
        if ws > 0:
            out.append((U[0] / ws, U[1] / ws))
    return out

def part_D():
    print("\n== D. numerical Brouwer mechanism of Lemma 5.1 ==")
    R_Q, m = 2.2, 1.5
    N = 200
    grid = [(R_Q * (2 * i / N - 1), R_Q * (2 * j / N - 1))
            for i in range(N + 1) for j in range(N + 1)]
    grid = [z for z in grid if math.hypot(*z) <= R_Q]

    # (i) a genuine multiplicity-two cover of Q: U_1 = Q cap {y > -eps},
    #     U_2 = Q cap {y < eps}, mesh = diam U_a = 2 R_Q > inradius, so Lemma 5.1
    #     does not apply.  Subordinate partition of unity: phi_a = dist(.,Q\U_a)
    #     normalised, i.e. phi_1 = (y+eps)/2eps, phi_2 = (eps-y)/2eps.  The image
    #     of F lies on the segment [z_1,z_2], which here misses the centre.
    eps = 0.2
    z1, z2 = (-R_Q, R_Q), (-R_Q, -R_Q)
    def F2(z):
        w1 = max(0.0, z[1] + eps)
        w2 = max(0.0, eps - z[1])
        s = w1 + w2
        return ((w1 * z1[0] + w2 * z2[0]) / s, (w1 * z1[1] + w2 * z2[1]) / s)
    img2 = [F2(z) for z in grid]
    mind = min(math.hypot(*f) for f in img2)
    check("D1 multiplicity-two cover, mesh 2R > inradius: image misses the centre",
          mind > 0.5, "min |F| = %.4g (R=%.1f)" % (mind, R_Q))

    # (ii) the multiplicity-three cover of A: mesh 1 <= m, inradius 2.2 > m.
    #      The partition-of-unity image is dense in the inner disk of radius m,
    #      i.e. the central region is filled -- no contradiction, as predicted
    #      by the sharpness of the multiplicity-two hypothesis.
    d, r = 0.625, 0.5
    centres3 = []
    k = int(R_Q / d) + 2
    for a in range(-k, k + 1):
        for b in range(-k, k + 1):
            cx, cy = d * (a + b / 2.0), d * (b * math.sqrt(3) / 2.0)
            if math.hypot(cx, cy) <= R_Q + r:
                centres3.append((cx, cy))
    img = pou_image(grid, centres3, radius=r)
    targets = [(0.3 * i, 0.3 * j) for i in range(-5, 6) for j in range(-5, 6)
               if math.hypot(0.3 * i, 0.3 * j) <= m - 0.1]
    worst = max(min(math.hypot(t[0] - f[0], t[1] - f[1]) for f in img) for t in targets)
    check("D2 multiplicity-three cover, mesh <= m: image fills the inner disk",
          worst < 0.06, "worst distance from an inner point to F(Q) = %.4g" % worst)
    mx = 0
    for z in grid[::7]:
        cnt = sum(1 for c in centres3 if math.hypot(z[0] - c[0], z[1] - c[1]) < r)
        mx = max(mx, cnt)
    check("D3 that cover has multiplicity exactly 3 on the sampled grid", mx == 3,
          "max multiplicity %d" % mx)

if __name__ == "__main__":
    part_A()
    part_B()
    part_C()
    part_D()
    print("\n%d checks failed" % len(FAIL))
    if FAIL:
        for f in FAIL:
            print("  failed:", f)
        sys.exit(1)
    print("all checks passed")
