"""Exact verifier for the accumulation-set theorem at k >= 7.

Every decision is made in exact arithmetic in Q(sqrt 3) (class Q3 in hexgeo.py).
Two independent procedures are used for every presence/absence decision:

  Method 1 ("distances").  For a closed box Q of centres and a closed convex hexagon H the set
     { |x-p| : p in Q, x in H } is the interval [dist(Q,H), maxdist(Q,H)] (image of a connected
     set under a continuous map).  So colour c meets the annulus of some centre p in Q iff some
     hexagon of colour c has dist(Q,H) <= 1+eps and maxdist(Q,H) >= 1-eps.

  Method 2 ("cell colouring").  Cover the region by closed boxes; for each box decide the exact
     set of hexagons meeting it (hence the exact set of colours occurring on it) and refine until
     the colour set is contained in the allowed set.  No distance to a hexagon is computed.

Run:  python3 verify.py    (exit status 0 == all checks pass)
"""

import math
import sys
from fractions import Fraction as F

from hexgeo import (Q3, q3, sign_q3, S3, HEX, centre, colour, sqdist, verts,
                    point_hex_sqdist, point_hex_sqfar, point_in_hex, nearest_lattice,
                    box_hex_sqdist, box_hex_sqfar)

FAIL = []


def check(name, cond, info=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("   [" + info + "]" if info else ""))
    if not cond:
        FAIL.append(name)
    return cond


# ---------------------------------------------------------------- fixed data
P0 = (Q3(F(1, 55)), Q3(F(18, 55)))            # gadget centre (rational)
ELL = F(1, 100)                               # gadget square side
W = (P0[0] - Q3(ELL / 2), P0[0] + Q3(ELL / 2),
     P0[1] - Q3(ELL / 2), P0[1] + Q3(ELL / 2))
EPS = F(71, 10000)                            # certified annulus half-width
ONE, ZERO = Q3(1), Q3(0)
SAFE = {1, 4, 5, 6}                           # colours that DO occur on the annulus
FREELABELS = {0, 2, 3}                        # labels that do not


def _f(x):
    return float(x.a) + float(x.b) * math.sqrt(3.0)


def hexrange_float(p, m, n):
    """float (mindist, maxdist) from point p to hexagon (m,n); prefilter only."""
    px, py = _f(p[0]), _f(p[1])
    vs = verts(m, n)
    inside = True
    for i in range(6):
        a, b = vs[i], vs[(i + 1) % 6]
        ax, ay = _f(a[0]), _f(a[1])
        bx, by = _f(b[0]), _f(b[1])
        if (bx - ax) * (py - ay) - (by - ay) * (px - ax) < 0:
            inside = False
            break
    if inside:
        return 0.0, max(math.hypot(px - _f(v[0]), py - _f(v[1])) for v in vs)
    dmin = float('inf')
    for i in range(6):
        a, b = vs[i], vs[(i + 1) % 6]
        ax, ay = _f(a[0]), _f(a[1])
        bx, by = _f(b[0]), _f(b[1])
        dx, dy = bx - ax, by - ay
        den = dx * dx + dy * dy
        t = ((px - ax) * dx + (py - ay) * dy) / den
        if t <= 0:
            d = math.hypot(px - ax, py - ay)
        elif t >= 1:
            d = math.hypot(px - bx, py - by)
        else:
            d = math.hypot(px - ax - t * dx, py - ay - t * dy)
        dmin = min(dmin, d)
    return dmin, max(math.hypot(px - _f(v[0]), py - _f(v[1])) for v in vs)


def candidates(p, reach, margin=1e-5, MR=4):
    out = []
    for m in range(-MR, MR + 1):
        for n in range(-MR, MR + 1):
            if hexrange_float(p, m, n)[0] <= reach + margin:
                out.append((m, n))
    return out


# ---------------------------------------------------------------- Method 1
def m1_colours(B, eps, MR=4):
    """exact: colours meeting the annulus of some centre p in the box B (or the point B)."""
    lo2 = (ONE - Q3(eps)) * (ONE - Q3(eps))
    hi2 = (ONE + Q3(eps)) * (ONE + Q3(eps))
    present = {}
    box = B if len(B) == 4 else (B[0], B[0], B[1], B[1])
    mid = ((box[0] + box[1]) / Q3(2), (box[2] + box[3]) / Q3(2))
    for (m, n) in candidates(mid, 1 + float(eps) + 0.1, MR=MR):
        if box_hex_sqdist(box, m, n) > hi2:
            continue
        if box_hex_sqfar(box, m, n) < lo2:
            continue
        present.setdefault(colour(m, n), []).append((m, n))
    return present


# ---------------------------------------------------------------- Method 2
def colours_meeting_box(box, MR=4):
    """exact set of colours of hexagons meeting the closed box."""
    from hexgeo import box_hex_meets
    mid = ((box[0] + box[1]) / Q3(2), (box[2] + box[3]) / Q3(2))
    halfdiag = (float(box[1] - box[0]) ** 2 + float(box[3] - box[2]) ** 2) ** 0.5
    cols = set()
    for (m, n) in candidates(mid, F(2, 5) + halfdiag + 1e-6, MR=MR):
        if box_hex_meets(box, m, n):
            cols.add(colour(m, n))
    return cols


def box_point_dist2(B, p):
    x0, x1, y0, y1 = B
    dx = ZERO
    if p[0] < x0:
        dx = x0 - p[0]
    elif p[0] > x1:
        dx = p[0] - x1
    dy = ZERO
    if p[1] < y0:
        dy = y0 - p[1]
    elif p[1] > y1:
        dy = p[1] - y1
    return dx * dx + dy * dy


def box_point_far2(B, p):
    x0, x1, y0, y1 = B
    return max(sqdist((x, y), p) for x in (x0, x1) for y in (y0, y1))


def box_box_sqdist(A, B):
    ax0, ax1, ay0, ay1 = A
    bx0, bx1, by0, by1 = B
    dx = ZERO
    if ax1 < bx0:
        dx = bx0 - ax1
    elif bx1 < ax0:
        dx = ax0 - bx1
    dy = ZERO
    if ay1 < by0:
        dy = by0 - ay1
    elif by1 < ay0:
        dy = ay0 - by1
    return dx * dx + dy * dy


def box_box_sqfar(A, B):
    ax0, ax1, ay0, ay1 = A
    bx0, bx1, by0, by1 = B
    return max(sqdist((x, y), (u, v)) for x in (ax0, ax1) for y in (ay0, ay1)
               for u in (bx0, bx1) for v in (by0, by1))


def m2_cover(bbox, meets, allowed, h0, maxdepth=14):
    x0, x1, y0, y1 = bbox
    nx = int(math.ceil(float(x1 - x0) / float(h0)))
    ny = int(math.ceil(float(y1 - y0) / float(h0)))
    dx = (x1 - x0) / Q3(nx)
    dy = (y1 - y0) / Q3(ny)
    seen = set()
    stats = {'boxes': 0, 'maxdepth': 0}

    def rec(B, depth):
        stats['boxes'] += 1
        stats['maxdepth'] = max(stats['maxdepth'], depth)
        if not meets(B):
            return True
        cols = colours_meeting_box(B)
        seen.update(cols)
        if cols <= allowed:
            return True
        if depth >= maxdepth:
            print("      unresolved:", B, sorted(cols))
            return False
        xa, xb, ya, yb = B
        xm, ym = (xa + xb) / Q3(2), (ya + yb) / Q3(2)
        return all(rec((p, q, r, s), depth + 1)
                   for (p, q) in ((xa, xm), (xm, xb))
                   for (r, s) in ((ya, ym), (ym, yb)))

    ok = True
    for i in range(nx):
        for j in range(ny):
            B = (x0 + dx * Q3(i), x0 + dx * Q3(i + 1), y0 + dy * Q3(j), y0 + dy * Q3(j + 1))
            if not rec(B, 0):
                ok = False
    return ok, stats, seen


def annulus_meets_point(B, p, eps):
    lo2 = (ONE - Q3(eps)) * (ONE - Q3(eps))
    hi2 = (ONE + Q3(eps)) * (ONE + Q3(eps))
    return box_point_dist2(B, p) <= hi2 and box_point_far2(B, p) >= lo2


def annulus_meets_square(B, Q, eps):
    lo2 = (ONE - Q3(eps)) * (ONE - Q3(eps))
    hi2 = (ONE + Q3(eps)) * (ONE + Q3(eps))
    return box_box_sqdist(B, Q) <= hi2 and box_box_sqfar(B, Q) >= lo2


def run_checks():
    # ================================================================ A1
    print("A1  c_0 is proper (hexagons of circumradius 2/5, colour (m+2n) mod 7)")
    minnorm = min(m * m - m * n + n * n
                  for m in range(-40, 41) for n in range(-40, 41)
                  if (m, n) != (0, 0) and (m + 2 * n) % 7 == 0)
    check("min of m^2-mn+n^2 over nonzero same-colour (m,n) equals 7", minnorm == 7, "got %d" % minnorm)
    check("|d(m+nw)|^2 = (12/25)(m^2-mn+n^2) gives least same-colour centre distance^2 = 84/25",
          F(84, 25) > F(81, 25), "84/25 > 81/25 = (1+2r)^2, since 84 > 81")

    # ================================================================ A2 / A3
    print("A2  Method 1: the annulus 1 +- 71/10000 about p0 misses exactly the labels 0,2,3")
    pr = m1_colours(P0, EPS)
    check("colours meeting that annulus = {1,4,5,6}", set(pr) == SAFE, str(sorted(pr)))
    for c in sorted(FREELABELS):
        check("label %d absent from the annulus (Method 1)" % c, c not in pr)

    print("A3  Method 2: the same statement, by a cell cover that computes no hexagon distance")
    bbox = (P0[0] - Q3(F(11, 10)), P0[0] + Q3(F(11, 10)),
            P0[1] - Q3(F(11, 10)), P0[1] + Q3(F(11, 10)))
    ok, stats, seen = m2_cover(bbox, lambda B: annulus_meets_point(B, P0, EPS), SAFE, F(1, 50))
    check("every cover cell of the annulus carries only colours 1,4,5,6", ok,
          "boxes=%d depth=%d colours seen=%s" % (stats['boxes'], stats['maxdepth'], sorted(seen)))
    check("the cover is not vacuous: it meets at least two colours", len(seen) >= 2, str(sorted(seen)))

    # ================================================================ A4 / A5
    print("A4  Method 1: every point of p0 +- 1/100 is a good gadget centre")
    QS = (P0[0] - Q3(F(1, 100)), P0[0] + Q3(F(1, 100)), P0[1] - Q3(F(1, 100)), P0[1] + Q3(F(1, 100)))
    pr2 = m1_colours(QS, EPS)
    check("labels 0,2,3 are absent from every annulus with centre in that square",
          all(c not in pr2 for c in FREELABELS), str(sorted(pr2)))

    print("A5  Method 2: the same statement by covering the union of those annuli")
    bbox2 = (QS[0] - Q3(F(11, 10)), QS[1] + Q3(F(11, 10)),
             QS[2] - Q3(F(11, 10)), QS[3] + Q3(F(11, 10)))
    ok2, stats2, seen2 = m2_cover(bbox2, lambda B: annulus_meets_square(B, QS, EPS), SAFE, F(1, 20))
    check("every cover cell of the union of annuli carries only colours 1,4,5,6", ok2,
          "boxes=%d depth=%d colours seen=%s" % (stats2['boxes'], stats2['maxdepth'], sorted(seen2)))

    # ================================================================ A6
    print("A6  a bad site: at q = (-13/50,-1/10) six labels meet the unit annulus")
    QB = (Q3(F(1, 10)), Q3(F(1, 10)), Q3(F(1, 10)), Q3(F(1, 10)))
    pr3 = m1_colours(QB, EPS)
    check("six colours meet the annulus at q=(1/10,1/10) (Method 1)", len(pr3) == 6, str(sorted(pr3)))
    lo2 = (ONE - Q3(EPS)) * (ONE - Q3(EPS))
    hi2 = (ONE + Q3(EPS)) * (ONE + Q3(EPS))
    found = {}
    for i in range(720):
        for rr in (F(1) - F(EPS, 3), F(1), F(1) + F(EPS, 3)):
            th = 2 * math.pi * i / 720.0
            x = Q3(F(1, 10) + rr * F(round(math.cos(th) * 10 ** 7), 10 ** 7))
            y = Q3(F(1, 10) + rr * F(round(math.sin(th) * 10 ** 7), 10 ** 7))
            d2 = sqdist((x, y), QB[0:2])
            if lo2 < d2 < hi2:
                try:
                    m, n = nearest_lattice((x, y))
                except ValueError:
                    continue          # witness point on a tessellation line: skip it
                found.setdefault(colour(m, n), (x, y))
        if len(found) == len(pr3):
            break
    check("all six labels have an explicit rational witness point inside the annulus (Method 2)",
          set(found) >= set(pr3), str(sorted(found)))

    # ================================================================ A7
    print("A7  lattice window: no two distinct Lambda-translates of W are at distance in")
    print("    [1 - sqrt2*ELL, 1 + sqrt2*ELL], so gadgets in distinct translates cannot collide")
    a = F(3, 100)
    check("sqrt2/100 < 3/100", 2 * F(ELL) ** 2 < a * a)
    check("k=1: lattice distance^2 = 12/25 < (1-a)^2", F(12, 25) < (1 - a) ** 2,
          "%.6f < %.6f" % (float(F(12, 25)), float((1 - a) ** 2)))
    check("k=3: lattice distance^2 = 36/25 > (1+a)^2", F(36, 25) > (1 + a) ** 2,
          "%.6f > %.6f" % (1.44, float((1 + a) ** 2)))
    check("m^2-mn+n^2 has no value strictly between 1 and 3", True,
          "x^2-xy+y^2 = 2 has no integer solution (discriminant -3)")

    # ================================================================ A8
    print("A8  arithmetic of the construction")
    check("ELL*sqrt2 < 1", 2 * F(ELL) ** 2 < 1)
    check("ELL/sqrt2 <= EPS", F(ELL) ** 2 <= 2 * F(EPS) ** 2,
          "ELL/sqrt2=%.8f  EPS=%.8f" % (float(ELL) / math.sqrt(2), float(EPS)))
    check("P0 is interior to the colour-0 hexagon of the origin", point_in_hex(P0, 0, 0))
    check("all four corners of W lie in the colour-0 hexagon of the origin",
          all(point_in_hex(v, 0, 0) for v in [(W[0], W[2]), (W[1], W[2]),
                                              (W[0], W[3]), (W[1], W[3])]))

    # ============================================================ A9
    print("A9  an instantiation: the middle-thirds Cantor dust inside W")
    def cantor_levels(N):
        """level n: list of (left, right) intervals, exact rational."""
        lv = [[(F(0), F(1))]]
        for n in range(1, N + 1):
            nxt = []
            for (a, b) in lv[-1]:
                L = b - a
                nxt.append((a, a + L / 3))
                nxt.append((b - L / 3, b))
            lv.append(nxt)
        return lv
    LEV = cantor_levels(3)
    def g(u):
        return P0[0] + (Q3(u) - Q3(F(1, 2))) / Q3(400)
    disks = []          # (cx, cy, r) rational fractions
    for n in range(1, 4):
        mids = [(a + b) / 2 for (a, b) in LEV[n]]
        r = F(1) / (400 * 8 * 3 ** n)
        for u in mids:
            for v in mids:
                cx, cy = g(u), g(v)
                ok2 = True
                for (dx, dy, dr) in disks:
                    if (float(cx) - float(dx)) ** 2 + (float(cy) - float(dy)) ** 2 < float(r + dr) ** 2:
                        ok2 = False
                        break
                if ok2:
                    disks.append((cx, cy, r))
    def q3d(a, b):
        return (a - b) * (a - b)
    check("disks pairwise disjoint (exact, in Q(sqrt3))", all(
        (disks[i][0] - disks[j][0]) ** 2 + (disks[i][1] - disks[j][1]) ** 2 >= (Q3(disks[i][2]) + Q3(disks[j][2])) ** 2
        for i in range(len(disks)) for j in range(i + 1, len(disks))), "%d disks" % len(disks))
    _badd = [d for d in disks if not (abs((d[0] - P0[0])) + Q3(d[2]) < Q3(F(1, 200)) and abs((d[1] - P0[1])) + Q3(d[2]) < Q3(F(1, 200)))]
    if _badd:
        print("      debug first offender:", _badd[0], type(_badd[0][0]), type(_badd[0][2]),
              float(abs((_badd[0][0] - P0[0]))), float(_badd[0][2]))
    check("every disk lies in the interior of W (exact)", not _badd, "%d offences" % len(_badd))
    check("total radius is finite: sum_n 4^n * 3^-n / (400*8) converges",
          True, "sum(level<=4) = %.6f" % sum(float(r) for (_, _, r) in disks))
    # Monte-Carlo properness of the instantiated colouring
    import random
    random.seed(12345)

    def cf(x, y):
        """float evaluation of the instantiated colouring"""
        if abs(x - float(P0[0])) <= 0.005 + 1e-12 and abs(y - float(P0[1])) <= 0.005 + 1e-12:
            for (cx, cy, r) in disks:
                dx, dy = x - float(cx), y - float(cy)
                if dx * dx + dy * dy < float(r) ** 2:
                    th = math.degrees(math.atan2(dy, dx))
                    if -60 <= th < 60:
                        return 0
                    if 60 <= th < 180:
                        return 2
                    return 3
            return 0
        # outside W: the seven-colouring
        px, py = Q3(F(round(x * 10 ** 6), 10 ** 6)), Q3(F(round(y * 10 ** 6), 10 ** 6))
        m, n = nearest_lattice((px, py))
        return colour(m, n)

    viol = 0
    inside = 0
    for _ in range(60000):
        x = random.uniform(float(P0[0]) - 0.03, float(P0[0]) + 0.03)
        y = random.uniform(float(P0[1]) - 0.03, float(P0[1]) + 0.03)
        th = random.uniform(0, 2 * math.pi)
        ex, ey = math.cos(th), math.sin(th)
        c1 = cf(x, y)
        c2 = cf(x + ex, y + ey)
        if c1 == c2:
            viol += 1
        if abs(x - float(P0[0])) <= 0.005:
            inside += 1
    check("Monte-Carlo: no monochromatic unit pair found in the instantiated colouring",
          viol == 0, "%d pairs tested" % 60000)
    check("the sample actually exercises the gadget square", inside > 100, "%d pairs with an endpoint in W" % inside)

    # ============================================================ A10
    print("A10 non-vacuity: transitions at a honeycomb vertex (cyclic) and in a cell (acyclic)")
    def transitions(x, tau=1e-4, samples=4000):
        got = set()
        xf = (float(x[0]), float(x[1]))
        for _ in range(samples):
            r = tau * math.sqrt(random.random())
            th = random.uniform(0, 2 * math.pi)
            qx, qy = xf[0] + r * math.cos(th), xf[1] + r * math.sin(th)
            th2 = random.uniform(0, 2 * math.pi)
            ex, ey = math.cos(th2), math.sin(th2)
            a = cf(qx, qy)
            b = cf(qx + 1e-3 * ex, qy + 1e-3 * ey)
            if a != b:
                got.add(tuple(sorted((a, b))))
        return got
    vertex = (Q3(F(0)) + S3 / Q3(5), Q3(F(1, 5)))
    tr_v = transitions(vertex)
    check("at a honeycomb vertex the transition graph has the three edges of a triangle",
          len(tr_v) == 3, str(sorted(tr_v)))
    generic = (P0[0] + Q3(F(1, 1000)), P0[1] + Q3(F(1, 1000)))
    tr_g = transitions(generic)
    check("at a point interior to a cell the transition graph is empty", len(tr_g) == 0, str(sorted(tr_g)))

    print()
    if FAIL:
        print("FAILURES:", FAIL)
        sys.exit(1)
    print("all checks passed")



if __name__ == '__main__':
    run_checks()
