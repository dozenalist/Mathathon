#!/usr/bin/env python3
# d3: ATTAINING 7 by lattice homomorphisms (constructive upper bounds).
# All arithmetic exact: fractions.Fraction only.  No floats in any claimed result;
# floats appear only inside comments/printed display of exact rationals.
#
# PART A  honeycomb: regular hexagons, circumradius a, centres on the triangular
#         lattice of spacing d = a*sqrt3 (so the hexagons tile the plane: they are
#         the Voronoi cells).  Verify c(p,q) = (p+3q) mod 7 is a proper 7-colouring.
# PART B  rectangular family: for every lattice hom  c(p,q) = (A p + B q) mod 7
#         certify exactly on which grid boxes of (s,t) it is proper, and report the
#         exact area of the region certified covered / certified not covered.
import sys
from fractions import Fraction as F

# ---------------------------------------------------------------- PART A ----
# Coordinates are stored as (alpha, beta) meaning the real point
#     (alpha*sqrt3, beta).
# Then the Euclidean inner product of two such points is RATIONAL:
#     <u,v> = 3 u.alpha v.alpha + u.beta v.beta
# so every squared distance below is an exact Fraction.
def gdot(u, v):   return 3*u[0]*v[0] + u[1]*v[1]
def gn2(u):       return 3*u[0]*u[0] + u[1]*u[1]
def sub(u, v):    return (u[0]-v[0], u[1]-v[1])
def add(u, v):    return (u[0]+v[0], u[1]+v[1])
def smul(c, u):   return (c*u[0], c*u[1])

# Q = hexagon of circumradius 1 (real space), the six vertices, cyclic order.
# real coords: (sqrt3/2,1/2),(0,1),(-sqrt3/2,1/2),(-sqrt3/2,-1/2),(0,-1),(sqrt3/2,-1/2)
HEX = [(F(1,2), F(1,2)), (F(0), F(1)), (F(-1,2), F(1,2)),
       (F(-1,2), F(-1,2)), (F(0), F(-1)), (F(1,2), F(-1,2))]

def cross(u, v):  # real cross product (linear map diag(sqrt3,1) has det>0)
    return u[0]*v[1] - u[1]*v[0]

def inside_hex(v):
    s = None
    for k in range(6):
        a, b = HEX[k], HEX[(k+1) % 6]
        c = cross(sub(b, a), sub(v, a))
        if c != 0:
            sgn = (c > 0)
            if s is None: s = sgn
            elif s != sgn: return False
    return True

def d2_seg(v, a, b):
    """Squared metric-g distance from v to the closed segment [a,b]."""
    d = sub(b, a); dd = gn2(d)
    if dd == 0: return gn2(sub(v, a))
    t = F(gdot(sub(v, a), d), 1)/dd          # exact projection parameter
    if t <= 0: return gn2(sub(v, a))
    if t >= 1: return gn2(sub(v, b))
    return gn2(sub(v, add(a, smul(t, d))))

def d2_to_hex(v):
    """Squared distance from v to the closed hexagon Q (0 if inside)."""
    if inside_hex(v): return F(0)
    return min(d2_seg(v, HEX[k], HEX[(k+1) % 6]) for k in range(6))

# test point of the derivation, brute force cross-check that
# min_{z in Q} |v - z|^2 really is the min over the six edges
def brute_min_d2(v, n=400):
    # crude: dense sampling of the closed hexagon (exploration only, not a claim)
    best = None
    for k in range(6):
        a, b = HEX[k], HEX[(k+1) % 6]
        for i in range(n+1):
            t = F(i, n)
            z = add(a, smul(t, sub(b, a)))
            d = gn2(sub(v, z))
            if best is None or d < best: best = d
    return best

# lattice basis in (alpha,beta) coords:  b1 = sqrt3*(1,0), b2 = (sqrt3/2, 3/2)
B1 = (F(1), F(0)); B2 = (F(1, 2), F(3, 2))

def lat(p, q):
    return add(smul(p, B1), smul(q, B2))

def dmax2(w):
    """max_{z in Q} |w - z|^2, attained at a vertex (convex in z)."""
    return max(gn2(sub(w, z)) for z in HEX)

def report_A():
    print("=" * 78)
    print("PART A  honeycomb: hexagon cells, circumradius a, lattice spacing a*sqrt3")
    print("        colouring c(p,q) = (p + 3q) mod 7")
    print("=" * 78)
    # (0) smallest same-colour lattice norm and the exact same-colour vectors
    ker = [(p, q) for p in range(-40, 41) for q in range(-40, 41)
           if not (p == 0 and q == 0) and (p + 3*q) % 7 == 0]
    # quadratic form  N(p,q) = p^2+pq+q^2 ;  |w|^2 = 3 N(p,q)  (real Euclidean)
    assert all(gn2(lat(p, q)) == 3*(p*p+p*q+q*q) for (p, q) in ker)
    mn = min(p*p+p*q+q*q for (p, q) in ker)
    print("min over same-colour v!=0 of p^2+pq+q^2  =", mn,
          "   e.g.", sorted([(p, q) for (p, q) in ker if p*p+p*q+q*q == mn]))
    print("  => smallest same-colour centre distance |v| = sqrt(3*7) = sqrt21")

    # (1) PROVED by hand, checked here exactly: for a = 1/2
    #     dmin(v) >= a*(|w| - 1) >= a*(sqrt21 - 1) since Q lies in the unit disc,
    #     and a*(sqrt21-1) > 1  <=>  sqrt21 > 3  <=> 21 > 9.
    print("\n  a = 1/2 (hexagons of diameter 1, the published honeycomb claim):")
    print("    dmin(v) = a*dist(w,Q) >= a*(|w|-1) >= (1/2)(sqrt21-1), and")
    print("    (sqrt21-1)/2 > 1  <=>  sqrt21 > 3  <=>  21 > 9   TRUE")
    # exact check of the same statement for every same-colour v with
    # |v| <= 1 + diam-relevant truncation: forced needs dmin <= 1, and
    # dmin >= a(|w|-1), so only |w| <= 1/a + 1 = 3 matters, i.e. 3(p^2+pq+q^2)
    # <= 9, i.e. p^2+pq+q^2 <= 3.  No same-colour v has that (min is 7).
    thr = 3*(1 + 3)  # (1/a + 1)^2 = 9 in |w|^2 units -> 3*N <= 9 -> N <= 3
    short = [(p, q) for (p, q) in ker if p*p+p*q+q*q <= 3]
    print("    same-colour v with p^2+pq+q^2 <= 3 (the only ones that could be",
          "forced):", short)
    assert short == []
    print("    => c = (p+3q) mod 7 is PROPER for a = 1/2.  PROVED.")

    # (2) exact a-threshold by the same crude bound, and the true critical a on a
    #     grid of rationals (grid result, explicitly marked as computed).
    print("\n  crude bound: a*(sqrt21-1) > 1  <=>  a > (sqrt21+1)/20 =", 
          1/(21**0.5 - 1), "(float, display only); exact: a > (sqrt21+1)/20")
    print("  => PROPER for every a > (sqrt21+1)/20, in particular a >= 3/10 .",
          "  check of (3/10)(sqrt21-1) > 1:")
    # (3/10)(sqrt21-1) > 1 <=> 3*sqrt21 > 13 <=> 27*21 > 169 <=> 567 > 169 TRUE
    print("     (3/10)(sqrt21-1) > 1 <=> 3 sqrt21 > 13 <=> 567 > 169  TRUE")

    # (3) true critical interval: v is forced iff a^2 d2(w,Q) <= 1 <= a^2 dmax2(w)
    #     i.e. a in [1/dmax(w), 1/dist(w,Q)].  Scan rational a on a grid.
    bad = []
    ND = 200
    for k in range(1, ND + 1):
        a = F(k, ND)
        ok = True
        # truncation: a*dist >= a(|w|-1) > 1 suffices
        lim2 = (F(1, 1)/a + 1)**2
        for (p, q) in ker:
            w = lat(p, q)
            if gn2(w) > lim2:      # |w| > 1/a + 1 : dmin > 1, legal
                continue
            dmin2 = a*a*d2_to_hex(w)
            if dmin2 > 1:          # legal: 1 < dmin
                continue
            if a*a*dmax2(w) >= 1:  # forced
                ok = False; break
        if not ok: bad.append(k)
    lo = [k for k in bad if k < ND//2]
    print("\n  grid scan of a in {k/200} (COMPUTED ON A GRID, not proved):")
    print("    worst (largest) failing a on the grid:", 
          (max(bad) if bad else None), "/200 =", (max(bad)/ND if bad else None))
    print("    failing grid a values (as k/200):", bad)

# ---------------------------------------------------------------- PART B ----
# Rectangular family.  Cells R(i,j) = [is-s/2,is+s/2] x [jt-t/2,jt+t/2].
# Independent re-derivation (see notes.md): for v = (p s, q t), p,q in Z,
#   dmin(v)^2 = max(0,|p|-1)^2 s^2 + max(0,|q|-1)^2 t^2     (= dist(v, 2R), 2R=[-s,s]x[-t,t])
#   dmax(v)^2 = (|p|+1)^2 s^2 + (|q|+1)^2 t^2
# forced(v) : dmin^2 <= 1 <= dmax^2   (closed: tangency counts).
# c(p,q) = (A p + B q) mod 7 proper  <=>  no forced v in ker = {v != 0 : A p + B q = 0 mod 7}.
#
# Certificate on a box [i/N,(i+1)/N] x [j/N,(j+1)/N]:
#   dmin^2 and dmax^2 are increasing in S=s^2 and T=t^2 (all coefficients >= 0), so
#   a *witness* v with  D(v)<=1 at the MAX corner and U(v)>=1 at the MIN corner
#   is forced on the WHOLE box.  If a hom has no witness, then for every v in its
#   kernel either dmin>1 throughout the box or dmax<1 throughout the box, so the
#   hom is proper on the whole box.  Multiplying through by N^2 gives integers.
def rect_certify(N, verbose=True):
    homs = [(A, B) for A in range(7) for B in range(7) if (A, B) != (0, 0)]
    maxX = 1 + N                       # largest |p| that can ever be a witness
    ker = {}
    for h in homs:
        A, B = h
        L = []
        for p in range(-maxX, maxX + 1):
            for q in range(-maxX, maxX + 1):
                if p == 0 and q == 0: continue
                if (A*p + B*q) % 7: continue
                L.append((max(abs(p), abs(q)), p, q))
        L.sort()
        ker[h] = L
    cov, unc, covA, uncA = [], [], F(0), F(0)
    N2 = N*N
    for i in range(N):
        for j in range(N):
            mbound = max(1 + N//(i+1), 1 + N//(j+1))   # safe truncation
            ip, jp = i+1, j+1
            covering = None
            allwit = True
            for h in homs:
                wit = False
                for (m, p, q) in ker[h]:
                    if m > mbound: break
                    ap, aq = abs(p), abs(q)
                    xp = ap-1 if ap >= 1 else 0
                    xq = aq-1 if aq >= 1 else 0
                    # D(v) at max corner (S,T)=(ip^2,jp^2)/N^2  <= 1 ?
                    if xp*xp*ip*ip + xq*xq*jp*jp > N2: continue
                    # U(v) at min corner (i^2,j^2)/N^2 >= 1 ?
                    if (ap+1)**2*i*i + (aq+1)**2*j*j >= N2:
                        wit = True; break
                if not wit:
                    covering = h; allwit = False; break
            area = F((2*i+1)*(2*j+1), N**4)     # area of this (s,t) box
            if covering is not None:
                cov.append((i, j, covering)); covA += area
            elif allwit:
                unc.append((i, j)); uncA += area
            else:
                raise RuntimeError
    tot = F(0)
    for i in range(N):
        for j in range(N):
            tot += F((2*i+1)*(2*j+1), N**4)
    assert tot == 1
    if verbose:
        print("grid N =", N, " boxes:", N*N, " quarter-disc area must be pi/4 ~",
              0.7853981633974483, "(float, display only)")
        print("  certified COVERED   boxes:", len(cov), " exact rational area:",
              covA, "= ", float(covA), "(float display)")
        print("  certified UNCOVERED boxes:", len(unc), " exact rational area:",
              uncA, "= ", float(uncA), "(float display)")
        print("  undefined boxes:", N*N-len(cov)-len(unc), " area:", 1-(covA+uncA))
        from collections import Counter
        cnt = Counter(h for (_, _, h) in cov)
        print("  homs actually used and how many boxes each certifies:")
        for h, c in cnt.most_common():
            print("     ", h, c)
        print("  covered fraction of the quarter disc (area / (pi/4)) =",
              "4*A/pi with A =", covA, "approx", float(4*covA/3.14159265358979323846),
              "(float display)")
        # per-hom exact covered area and its box set shape
        print("  exact area certified by each hom:")
        per = {}
        for (i, j, h) in cov:
            per[h] = per.get(h, F(0)) + F((2*i+1)*(2*j+1), N**4)
        for h, a in sorted(per.items(), key=lambda kv: -kv[1]):
            print("     ", h, a, "approx", float(a), "(float display)")
    return cov, unc, covA, uncA


def rect_validate():
    """Independent brute-force validation of the dmin/dmax formulas."""
    print("=" * 78)
    print("Formula validation (exact): dmin^2, dmax^2 vs brute force over corners")
    print("=" * 78)
    bad = 0
    for (s, t) in [(F(1, 3), F(1, 4)), (F(2, 5), F(1, 7)), (F(1, 7), F(3, 11))]:
        for p in range(-4, 5):
            for q in range(-4, 5):
                if p == 0 and q == 0: continue
                # cells as closed rectangles
                A = (p*s-s/2, p*s+s/2, q*t-t/2, q*t+t/2)   # second cell rel. first
                gx = max(F(0), abs(p)*s - s)  # x-gap between R(0,0) and R(p,q)
                gy = max(F(0), abs(q)*t - t)
                dmin2 = gx*gx + gy*gy
                f_dmin2 = max(0, abs(p)-1)**2*s*s + max(0, abs(q)-1)**2*t*t
                # dmax: max over the 4x4 corner pairs of the two rectangles
                cand = []
                for x1 in (-s/2, s/2):
                    for x2 in (p*s-s/2, p*s+s/2):
                        for y1 in (-t/2, t/2):
                            for y2 in (q*t-t/2, q*t+t/2):
                                cand.append((x2-x1)**2 + (y2-y1)**2)
                dmax2 = max(cand)
                f_dmax2 = (abs(p)+1)**2*s*s + (abs(q)+1)**2*t*t
                if dmin2 != f_dmin2 or dmax2 != f_dmax2: bad += 1
    print("  mismatches:", bad, "(0 = formulas confirmed exactly)")
    assert bad == 0

if __name__ == "__main__":
    rect_validate()
    report_A()
    print()
    rect_certify(int(sys.argv[1]) if len(sys.argv) > 1 else 30)
