#!/usr/bin/env python3
"""Re-verify a stored exact-volume certificate by a formula that uses neither the interior point
nor the area vectors.

`exact_volume.check_certificate` proves the certificate's own obligations (V1-V8), but V5 and V7
both use the area-vector formula and V7/V8 both use the interior point `v`.  This checker uses

        V = (1/6) * sum over the faceted triangles of  det(a, b, c) ,   outward oriented,

the signed-tetrahedron formula for a closed oriented surface.  It is origin independent, needs no
apex, and no area vectors: only the vertex coordinates and the cyclic order of each facet.

It also checks that the facets close (sum of the oriented triangle cross products is zero), so a
certificate with a missing facet is rejected here too.

Usage: python3 verify_certificate_independent.py [certificate.json]
Default: out/certificate_dense_shell_centre.json
"""
import json, os, sys
from fractions import Fraction as F

_HERE = os.path.dirname(os.path.abspath(__file__))

def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1])
            - u[1] * (v[0] * w[2] - v[2] * w[0])
            + u[2] * (v[0] * w[1] - v[1] * w[0]))

def verify(path):
    blob = json.load(open(path))
    cert = blob.get("certificate", blob)
    allp = [tuple(F(x) for x in p) for p in cert["planes"]]
    planes = [tuple(F(x) for x in p) for p in cert.get("candidate_planes", cert["planes"])]
    verts = [tuple(F(x) for x in P) for P in cert["vertices"]]
    facets = cert["facets"]
    vol = F(cert["volume"])

    # (0) FACET UNIQUENESS and CONSTRAINT SATISFACTION -- the two things Astra's witnesses attack.
    #     Without them this checker shares the blind spots it is supposed to expose: a doubled facet
    #     list also doubles the signed-tetrahedron sum, so the two formulas would "agree" at 2V.
    if len({f["plane"] for f in facets}) != len(facets):
        raise SystemExit("FAIL: two facets share a plane index")
    for pt in verts:
        for (a, b, c, d) in allp:
            if a * pt[0] + b * pt[1] + c * pt[2] > d:
                raise SystemExit("FAIL: a vertex violates a constraint")
    #     and the normals must span R^3, or closure does not bound the polyhedron (a prism closes)
    for i in range(len(facets)):
        for j in range(i + 1, len(facets)):
            for k in range(j + 1, len(facets)):
                u, w, z = (planes[facets[t]["plane"]][:3] for t in (i, j, k))
                if det3(u, w, z) != 0:
                    break
            else:
                continue
            break
        else:
            continue
        break
    else:
        raise SystemExit("FAIL: the facet normals span fewer than 3 dimensions")

    # (1) every facet's vertices lie on its plane and are outward ordered -- checked by the sign of
    #     the triangle orientation against the plane normal, which needs no area vector
    total_det = F(0)
    closure = [F(0), F(0), F(0)]
    for f in facets:
        a, b, c, d = planes[f["plane"]]
        poly = [verts[t] for t in f["verts"]]
        for i in range(1, len(poly) - 1):
            p0, p1, p2 = poly[0], poly[i], poly[i + 1]
            for P_ in (p0, p1, p2):
                if a * P_[0] + b * P_[1] + c * P_[2] != d:
                    raise SystemExit("FAIL: a facet vertex is not on its plane")
            total_det += det3(p0, p1, p2)
            u = [p1[t] - p0[t] for t in range(3)]
            w = [p2[t] - p0[t] for t in range(3)]
            cr = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
            # outward orientation: the triangle's normal must point along the plane's normal
            if cr[0] * a + cr[1] * b + cr[2] * c <= 0:
                raise SystemExit("FAIL: a triangle is inward oriented")
            for t in range(3):
                closure[t] += cr[t] / 2
    v_signed = total_det / 6
    print("  signed-tetrahedron volume : %s" % v_signed)
    print("  certificate's volume      : %s" % vol)
    if v_signed != vol:
        raise SystemExit("FAIL: the two formulas disagree")
    print("  PASS: the origin-independent formula reproduces the certified volume")
    if tuple(closure) != (F(0), F(0), F(0)):
        raise SystemExit("FAIL: the triangles do not close")
    print("  PASS: the oriented triangles close (sum of cross products is zero)")
    return 0

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "out", "certificate_dense_shell_centre.json")
    print("independent re-check of", path)
    sys.exit(verify(path))
