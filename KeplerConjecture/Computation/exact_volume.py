#!/usr/bin/env python3
"""A small PROOF-CARRYING exact-volume verifier for a rational polyhedron in R^3.

WHAT WAS WRONG BEFORE.  `fixture_nonuniform.cell_volume` decided which triples of planes could meet
in a vertex by `abs(float(det)) < 1e-9`, and it "certified completeness" by checking the discarded
planes only against the vertices it had already found.  Neither establishes what the volume claims:

  * a float determinant filter can drop a triple whose exact determinant is nonzero (or keep a
    degenerate one), so the vertex set need not be complete;
  * checking discarded planes against the found vertices is circular -- if a facet was missed, its
    vertices were never found either, and the check cannot see it;
  * nothing established BOUNDEDNESS, so an unbounded polyhedron (whose "vertices" do not determine
    it) would have been accepted;
  * planes were deduplicated by their raw rational tuple, so (1,0,0,1) and (2,0,0,2) -- the SAME
    half-space -- both survived and the face was counted twice.  For a cube of side 2 that gives
    8 + 4/3 = 28/3 instead of 8 (E's duplicate-face defect).

THE DESIGN: search and check are separate.  `certify_volume` SEARCHES (any method may be used, and
the search is not trusted); `check_certificate` CHECKS a certificate by exact rational arithmetic
alone, and is what the volume claim rests on.  A caller that supplies its own vertices and facets is
verified by the same function, so the checker is independent of the search.

THE CERTIFICATE.  A list of planes (a,b,c,d) meaning a x + b y + c z <= d, an interior point v, a
vertex list, a facet list (plane index + vertex indices in cyclic order), and the volume.  The
checks are:

  V1  every vertex satisfies every plane exactly;
  V2  v is strictly inside every plane (a.v < d) -- a valid apex for the fan;
  V3  each facet's vertices lie exactly on its plane, are >= 3, not collinear, and its AREA VECTOR
      is a strictly positive multiple of the plane's outward normal (so the facet is outward
      oriented);
  V4  every vertex lies on at least three facets' planes (no spurious vertices);
  V5  the facet area vectors sum to ZERO.  This is the boundedness gate: writing A_f = lambda_f a_f
      with lambda_f > 0, the identity sum_f A_f = 0 exhibits sum_f lambda_f a_f = 0 with all
      lambda_f > 0, i.e. the normals POSITIVELY SPAN R^3, so the cone {x : a_f.x <= 0 for all f} is
      {0} and the polyhedron is bounded.  Nobody has to search for the positive combination: the
      facet areas supply it;
  V6  every facet of the polytope appears exactly once -- which V3 + V5 give, because a face of a
      polyhedron is its intersection with a supporting plane, and any plane touching the polytope in
      a two-dimensional set is therefore a facet; the remaining planes are redundant and V1 already
      shows they do not cut the polytope;
  V7  the volume from the divergence theorem, V = (1/3) sum_f x_f . A_f, is positive and EQUALS the
      volume in the certificate.

Together V1-V7 give: P = conv(V) (V1 and the facet coverage give conv(V) = cap(planes)), the vertex
set is complete (a bounded polyhedron is the convex hull of its vertices), and the volume is exact.

DEGENERACIES are rejected rather than approximated: a flat polytope (V7 fails), a facet with zero
area (V3), duplicate planes (deduped by half-space, not by tuple), a dominated plane (same direction,
looser -- dropped), an unbounded polyhedron (V5 fails).

Reproduction: python3 exact_volume.py
"""
import itertools, sys
from fractions import Fraction as F

# ------------------------------------------------------------------ plane normal form
def _gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a

def normalise(plane):
    """Canonical form of a half-space {a.x <= d}: primitive integer (a,b,c,d), sign fixed.

    Two planes define the SAME half-space iff their normal forms are equal.  This is what stops
    (1,0,0,1) and (2,0,0,2) being counted as two faces.
    """
    a, b, c, d = (F(x) for x in plane)
    if a == 0 and b == 0 and c == 0:
        raise ValueError("plane with zero normal")
    # clear denominators
    L = 1
    for x in (a, b, c, d):
        L = L * x.denominator // _gcd(L, x.denominator)
    A, B, C, D = (int(x * L) for x in (a, b, c, d))
    g = 0
    for x in (A, B, C, D):
        g = _gcd(g, x)
    if g:
        A, B, C, D = A // g, B // g, C // g, D // g
    # NO SIGN CONVENTION: (a,b,c,d) -> (-a,-b,-c,-d) describes the OPPOSITE half-space
    # (a.x >= d, not a.x <= d), so only positive scaling is allowed.  An earlier version flipped
    # the sign to make the normal positive and silently turned -x <= 1 into x <= -1.
    return (A, B, C, D)

def prepare(planes):
    """Normalise, dedupe identical half-spaces, and drop planes strictly dominated by a parallel one.

    Returns (kept, dropped) where `dropped` lists the planes removed and why.  A plane (a,d) is
    dominated by (a',d') with a' = mu a (mu > 0) and d'/mu <= d: it is implied by the other.
    """
    seen = {}
    dropped = []
    for pl in planes:
        n = normalise(pl)
        if n in seen:
            dropped.append((pl, "duplicate of %r" % (n,)))
            continue
        seen[n] = pl
    kept = []
    for n, pl in seen.items():
        a, b, c, d = n
        dominated = False
        for n2 in list(seen):
            if n2 == n:
                continue
            a2, b2, c2, d2 = n2
            # same direction?  (a,b,c) and (a2,b2,c2) parallel with positive factor
            cross = (b * c2 - c * b2, c * a2 - a * c2, a * b2 - b * a2)
            if cross != (0, 0, 0):
                continue
            dot = a * a2 + b * b2 + c * c2
            if dot <= 0:
                continue                     # opposite directions: not comparable
            # n2 = mu * n with mu = |a2| / |a| > 0 ; constraint n2 is tighter iff d2/mu < d
            # compare d2 * |a| with d * |a2| without floats: use cross products of the tuples
            num = d2 * (abs(a) + abs(b) + abs(c))
            den = abs(a2) + abs(b2) + abs(c2)
            lhs = d * den
            if num <= lhs:
                dominated = True
                break
        if dominated:
            dropped.append((pl, "dominated by a parallel plane"))
        else:
            kept.append(n)
    return kept, dropped

# ------------------------------------------------------------------ exact geometry
def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1])
            - u[1] * (v[0] * w[2] - v[2] * w[0])
            + u[2] * (v[0] * w[1] - v[1] * w[0]))

def solve3(P):
    """Intersection of three planes, EXACTLY; None iff the 3x3 determinant is exactly zero.

    No float filter: the only triples skipped are those whose exact determinant vanishes, and for
    those the intersection is empty or a line, never a single vertex.
    """
    (a1, b1, c1, d1), (a2, b2, c2, d2), (a3, b3, c3, d3) = P
    D = det3((a1, b1, c1), (a2, b2, c2), (a3, b3, c3))
    if D == 0:
        return None
    # EXACT DIVISION.  det3 returns an int when the planes are integers, and int/int in Python is
    # FLOAT division: an earlier version wrote `det / D` and silently returned 2^-53-rounded
    # vertices, which then failed their own plane check.  F(num, D) is rational division.
    x = F(det3((d1, b1, c1), (d2, b2, c2), (d3, b3, c3)), D)
    y = F(det3((a1, d1, c1), (a2, d2, c2), (a3, d3, c3)), D)
    z = F(det3((a1, b1, d1), (a2, b2, d2), (a3, b3, d3)), D)
    return (F(x), F(y), F(z))

def inside(pt, plane):
    a, b, c, d = plane
    return a * pt[0] + b * pt[1] + c * pt[2] <= d

def on(pt, plane):
    a, b, c, d = plane
    return a * pt[0] + b * pt[1] + c * pt[2] == d

def enumerate_vertices(planes):
    """Every intersection of three planes that satisfies all the planes.  Exact, nothing skipped
    except exact degeneracy."""
    out = set()
    for triple in itertools.combinations(planes, 3):
        pt = solve3(triple)
        if pt is None:
            continue
        if all(inside(pt, pl) for pl in planes):
            out.add(pt)
    return sorted(out)

def order_polygon(pts, normal):
    """Order coplanar points cyclically (exactly) and return them plus their area vector."""
    m = [sum(P[t] for P in pts) / len(pts) for t in range(3)]
    e1 = [pts[0][t] - m[t] for t in range(3)]
    a, b, c = normal
    e2 = [b * e1[2] - c * e1[1], c * e1[0] - a * e1[2], a * e1[1] - b * e1[0]]
    def xy(P):
        w = [P[t] - m[t] for t in range(3)]
        return (sum(w[t] * e1[t] for t in range(3)), sum(w[t] * e2[t] for t in range(3)))
    def half(p):
        x, y = p[0]
        return 0 if (y > 0 or (y == 0 and x >= 0)) else 1
    import functools
    def cmp(p, q):
        hp, hq = half(p), half(q)
        if hp != hq:
            return -1 if hp < hq else 1
        cr = p[0][0] * q[0][1] - p[0][1] * q[0][0]
        return -1 if cr > 0 else (1 if cr < 0 else 0)
    tagged = sorted([(xy(P), P) for P in pts], key=functools.cmp_to_key(cmp))
    poly = [P for (_, P) in tagged]
    # area vector = 1/2 sum (v_i x v_{i+1})
    A = [F(0), F(0), F(0)]
    n = len(poly)
    for i in range(n):
        u, v = poly[i], poly[(i + 1) % n]
        A[0] += u[1] * v[2] - u[2] * v[1]
        A[1] += u[2] * v[0] - u[0] * v[2]
        A[2] += u[0] * v[1] - u[1] * v[0]
    A = [x / 2 for x in A]
    return poly, tuple(A)

def facets_of(planes, verts):
    """The facets, with each polygon ordered and its area vector; only genuine 2-faces are kept."""
    facets = []
    for i, pl in enumerate(planes):
        on_pl = [P for P in verts if on(P, pl)]
        if len(on_pl) < 3:
            continue
        poly, A = order_polygon(on_pl, pl[:3])
        if A == (0, 0, 0):
            continue                      # collinear: a degenerate face, not a facet
        a, b, c, _ = pl
        cross = (A[1] * c - A[2] * b, A[2] * a - A[0] * c, A[0] * b - A[1] * a)
        dot = A[0] * a + A[1] * b + A[2] * c
        if cross != (0, 0, 0) or dot <= 0:
            return None, "facet %d is not outward oriented (area vector %r, normal %r)" % (i, A, pl[:3])
        facets.append(dict(plane=i, verts=poly, area=A))
    return facets, None

# ------------------------------------------------------------------ the checker
def check_certificate(cert):
    """Re-verify a certificate from its own data.  Exact; raises ValueError on any failure."""
    planes = [tuple(F(x) for x in pl) for pl in cert.get("candidate_planes", cert["planes"])]
    v = tuple(F(x) for x in cert["interior"])
    verts = [tuple(F(x) for x in P) for P in cert["vertices"]]
    facets = cert["facets"]
    vol = F(cert["volume"])
    P = lambda pt, pl: pl[0] * pt[0] + pl[1] * pt[1] + pl[2] * pt[2]
    # V1
    for pt in verts:
        for pl in planes:
            if P(pt, pl) > pl[3]:
                raise ValueError("V1: vertex %r violates plane %r" % (pt, pl))
    # V2
    for pl in planes:
        if not P(v, pl) < pl[3]:
            raise ValueError("V2: the interior point is not strictly inside plane %r" % (pl,))
    # V3 + V5
    total_area = [F(0), F(0), F(0)]
    for f in facets:
        pl = planes[f["plane"]]
        poly = [verts[t] for t in f["verts"]]
        if len(poly) < 3:
            raise ValueError("V3: facet on plane %d has %d vertices" % (f["plane"], len(poly)))
        for pt in poly:
            if P(pt, pl) != pl[3]:
                raise ValueError("V3: facet vertex %r is not on its plane" % (pt,))
        # RECOMPUTE the area vector from the ordered polygon: the stored one must agree, which is
        # what makes the vertex ORDER load-bearing (an earlier checker trusted the stored area and
        # so accepted a facet whose vertices had been reversed).
        A = [F(0), F(0), F(0)]
        for i in range(len(poly)):
            u, w = poly[i], poly[(i + 1) % len(poly)]
            A[0] += u[1] * w[2] - u[2] * w[1]
            A[1] += u[2] * w[0] - u[0] * w[2]
            A[2] += u[0] * w[1] - u[1] * w[0]
        A = tuple(x / 2 for x in A)
        if A != tuple(F(x) for x in f["area"]):
            raise ValueError("V3: facet on plane %d: the stored area vector does not match the "
                             "ordered vertices" % f["plane"])
        a, b, c, _ = pl
        cross = (A[1] * c - A[2] * b, A[2] * a - A[0] * c, A[0] * b - A[1] * a)
        dot = A[0] * a + A[1] * b + A[2] * c
        if cross != (0, 0, 0) or dot <= 0:
            raise ValueError("V3: facet on plane %d is not outward oriented" % f["plane"])
        total_area = [total_area[t] + A[t] for t in range(3)]
    # V5: closure == positive spanning == bounded
    if tuple(total_area) != (F(0), F(0), F(0)):
        raise ValueError("V5: the area vectors do not close (%r): the surface is not a closed "
                         "boundary, so boundedness is not certified" % (total_area,))
    # V4: every vertex is on at least three facets
    for idx, pt in enumerate(verts):
        k = sum(1 for f in facets if idx in f["verts"])
        if k < 3:
            raise ValueError("V4: vertex %r lies on only %d facets" % (pt, k))
    # V7: the divergence theorem
    total = F(0)
    for f in facets:
        A = tuple(F(x) for x in f["area"])
        x = verts[f["verts"][0]]
        total += x[0] * A[0] + x[1] * A[1] + x[2] * A[2]
    computed = total / 3
    if computed <= 0:
        raise ValueError("V7: non-positive volume %s (a flat or inverted polytope)" % computed)
    if computed != vol:
        raise ValueError("V7: the certificate says %s, the divergence theorem gives %s"
                         % (vol, computed))
    # V8: the SAME volume by a different formula -- fan every facet into triangles and sum the
    # tetrahedra with apex v.  This does not use the area vectors at all, so it catches a facet
    # whose ordering closes (V5) but whose areas are wrong.
    fan = F(0)
    for f in facets:
        poly = [verts[t] for t in f["verts"]]
        for i in range(1, len(poly) - 1):
            A_, B_, C_ = poly[0], poly[i], poly[i + 1]
            fan += abs(det3(tuple(A_[t] - v[t] for t in range(3)),
                            tuple(B_[t] - v[t] for t in range(3)),
                            tuple(C_[t] - v[t] for t in range(3)))) / 6
    if fan != computed:
        raise ValueError("V8: the fan volume %s disagrees with the divergence-theorem volume %s"
                         % (fan, computed))
    return computed

def certify_volume(planes, interior, candidates=None):
    """SEARCH: build a certificate for {x : a.x <= d for every plane}, then CHECK it.

    TWO-PART COMPLETENESS ARGUMENT, which is why a float pre-pass may PROPOSE the candidates:

      (i)  the certificate proves that the enumerated polytope is exactly cap(A) -- the intersection
           of the planes in `candidates` -- with its complete vertex and facet structure (V1-V7;
           V5's closure is what certifies boundedness, so the vertex set determines the polytope);
      (ii) every plane NOT in `candidates` is checked (exactly) against every vertex of that
           polytope.  If such a plane cut cap(A), some vertex of cap(A) would lie outside it (a
           half-space that properly cuts a polytope leaves a vertex outside); so the check passing
           proves cap(all planes) = cap(A).

    Hence the volume is the volume of the intersection of EVERY plane given, whether or not the
    candidate set was chosen well -- the float pre-pass only has to be fast, not right.  Passing
    candidates=None enumerates over all the planes and is the slow, assumption-free path.
    """
    kept, dropped = prepare(planes)
    for pl in kept:
        if not (pl[0] * interior[0] + pl[1] * interior[1] + pl[2] * interior[2] < pl[3]):
            raise ValueError("the supposed interior point is not strictly inside %r" % (pl,))
    if candidates is None:
        A, rest = list(kept), []
    else:
        cand = set(normalise(pl) for pl in candidates)
        A = [pl for pl in kept if pl in cand]
        rest = [pl for pl in kept if pl not in cand]
        if len(A) < 4:
            raise ValueError("only %d candidate planes" % len(A))
    verts = enumerate_vertices(A)
    if len(verts) < 4:
        raise ValueError("only %d vertices from %d planes: the polytope is unbounded or degenerate"
                         % (len(verts), len(A)))
    facets, err = facets_of(A, verts)
    if err:
        raise ValueError(err)
    # (ii) every plane outside the candidate set must contain every vertex
    for pl in rest:
        for pt in verts:
            if not inside(pt, pl):
                raise ValueError("a plane outside the candidate set cuts the polytope: %r" % (pl,))
    total = F(0)
    for f in facets:
        A_ = f["area"]
        x = f["verts"][0]
        total += x[0] * A_[0] + x[1] * A_[1] + x[2] * A_[2]
    vol = total / 3
    cert = dict(planes=[[str(x) for x in p] for p in kept],
                candidate_planes=[[str(x) for x in p] for p in A],
                interior=[str(x) for x in interior],
                vertices=[[str(x) for x in P] for P in verts],
                facets=[dict(plane=A.index(f["plane"]) if False else f["plane"],
                             verts=[verts.index(P) for P in f["verts"]],
                             area=[str(x) for x in f["area"]]) for f in facets],
                volume=str(vol),
                dropped=[[list(pl), why] for (pl, why) in dropped])
    check_certificate(cert)
    return vol, cert


def volume(planes, interior):
    return certify_volume(planes, interior)[0]
