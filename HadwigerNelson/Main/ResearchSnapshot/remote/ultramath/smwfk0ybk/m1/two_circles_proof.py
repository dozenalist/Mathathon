"""Two concentric circles never force four colours (generic radii): exact check of the
coordinate model behind the proof.

Model.  x in R^2, r, s > 1/2, r != s, and |gamma| <= 1 with
    gamma = (r^2+s^2-1)/(2 r s),   phi = arccos gamma,
    theta_r = 2 arcsin(1/(2r)),    theta_s = 2 arcsin(1/(2s)).
An angle on circle r is written a*theta_r + b*theta_s + 2c*phi, on circle s
a*theta_r + b*theta_s + (2c+1)*phi (integers a,b,c), because every cross edge
changes the circle and shifts the angle by +-phi, so returning to a circle needs
an even number of cross steps.

Edges in these coordinates (all of them):
  r-edge: (r,a,b,c) - (r,a+-1,b,c)
  s-edge: (s,a,b,c) - (s,a,b+-1,c)
  cross : (r,a,b,c) - (s,a,b,c)   and   (r,a,b,c) - (s,a,b,c-1)

Claimed 3-colouring (colours 0,1 on circle r; 1,2 on circle s):
  chi(r,a,b,c) = (a+b) mod 2,      chi(s,a,b,c) = ((a+b) mod 2) + 1.
Every edge has two different colours -- an exact integer identity, checked below.

Well-definedness: the coordinate map must be injective on the ball; it is a
function of the angle, so two coordinate sets with equal angle must get equal
colour.  That holds exactly when every integer relation
    m*theta_r + n*theta_s + 2k*phi == 0 (mod 2pi)
has m+n even (the *parity condition*); the script checks injectivity numerically
for concrete (r,s) and the parity condition exactly is checked by d17.md.
"""
import math
from itertools import product

def colour(circle, a, b, c):
    if circle == 0:
        return (a + b) % 2
    return ((a + b) % 2) + 1

def ball(depth):
    """BFS in integer coordinates from (circle r, 0,0,0)."""
    start = (0, 0, 0, 0)          # (circle, a, b, c)
    seen = {start: 0}
    frontier, out = [start], [(start, 0)]
    for _ in range(depth):
        nxt = []
        for v in frontier:
            cir, a, b, c = v
            if cir == 0:
                nb = [(0, a + 1, b, c), (0, a - 1, b, c),
                      (1, a, b, c), (1, a, b, c - 1)]
            else:
                nb = [(1, a, b + 1, c), (1, a, b - 1, c),
                      (0, a, b, c), (0, a, b, c + 1)]
            for w in nb:
                if w not in seen:
                    seen[w] = seen[v] + 1
                    nxt.append(w)
        frontier = nxt
    return list(seen)

def check_colouring(depth=6):
    verts = ball(depth)
    bad = 0
    edges = 0
    for v in verts:
        cir, a, b, c = v
        if cir == 0:
            nb = [(0, a + 1, b, c), (0, a - 1, b, c), (1, a, b, c), (1, a, b, c - 1)]
        else:
            nb = [(1, a, b + 1, c), (1, a, b - 1, c), (0, a, b, c), (0, a, b, c + 1)]
        for w in nb:
            if w in set(verts):
                edges += 1
                if colour(*v) == colour(*w):
                    bad += 1
                    if bad < 4:
                        print("  bad edge", v, w, colour(*v))
    return len(verts), edges // 2, bad

def angles(r, s, verts):
    tr = 2 * math.asin(0.5 / r)
    ts = 2 * math.asin(0.5 / s)
    gam = (r * r + s * s - 1) / (2 * r * s)
    ph = math.acos(max(-1.0, min(1.0, gam)))
    out = []
    for (cir, a, b, c) in verts:
        ang = a * tr + b * ts + (2 * c + 1) * ph
        out.append((cir, ang % (2 * math.pi)))
    return out, ph

def welldefined_on_ball(r, s, verts, tol=1e-7):
    """Distinct coordinate vertices may share an angle (integer relations exist).
    The colouring is a function of the angle iff every such collision carries equal
    colours: that is exactly the parity condition.  Returns (collisions, violations,
    smallest positive gap)."""
    pts, ph = angles(r, s, verts)
    coll = 0
    viol = 0
    worst = 1e9
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            if pts[i][0] != pts[j][0]:
                continue
            d = abs(pts[i][1] - pts[j][1])
            d = min(d, 2 * math.pi - d)
            if d <= tol:
                coll += 1
                if colour(*verts[i]) != colour(*verts[j]):
                    viol += 1
            else:
                worst = min(worst, d)
    return coll, viol, worst

if __name__ == "__main__":
    for depth in (4, 6, 8):
        n, e, bad = check_colouring(depth)
        print(f"coordinate ball depth={depth}: vertices={n} edges={e} bad edges={bad}")
    print()
    for (r, s) in [(1.0, 1 / math.sqrt(2)), (1.0, 3 / math.sqrt(11)), (0.6, 0.8),
                   (1.0, 1.2), (2.0, 1.5), (1.0, 1 / (2 * math.sin(math.pi / 5)))]:
        verts = ball(6)
        worst = injective_on_ball(r, s, verts, tol=1e-7)
        print(f"r={r:.6f} s={s:.6f}: smallest angular gap between distinct coordinate "
              f"vertices on one circle = {worst:.3e}  -> "
              f"{'injective' if worst > 1e-7 else 'COLLISION'}")
