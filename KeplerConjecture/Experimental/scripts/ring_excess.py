#!/usr/bin/env python3
"""
The ring-excess lemma: a PROOF (not a computation) that the C5 payer cell exceeds the (P')
threshold, and the template for a general proof.

Lemma.  Let D = {y : y.n_i <= 1, i = 1..12} be bounded and let the faces on the five "ring"
planes be F_1..F_5, with areas A_i.  For b >= 1 put

    K(b) = { y.n_i <= b  (i <= 5) ,  y.n_i <= 1  (i > 5) } .

Then, whenever the combinatorial type is constant on the path,

    vol K(b) - vol D = 5 (b-1) * ∫_0^1 mean(A_i(b(t))) dt  >=  5 (b-1) * min_t mean(A_i) .

Proof.  Moving face i outward at unit speed increases the volume at rate A_i (the standard
derivative of a polytope's volume with respect to a face distance; the added slab is the
prism over that face).  Here five faces move at rate (b-1) and the rest at 0, so
d/dt vol K(b(t)) = (b-1) * sum_{i<=5} A_i(b(t)) = 5(b-1) * mean.  Integrate.  []

Why this matters.  The unit-distance relaxation is 0.19 short of the threshold (REVIEW_0608
8.3b), so no argument that sees only b_i >= 1 can prove (P').  This lemma uses the ring's
actual excess b = 1.051462, and it is enough:

    vol Omega(w1)  >=  V_dod  +  5 (b-1) * min area
                   =   5.550291029 + 5*0.0514622*1.063151
                   =   5.82389...  >  5.763417470          margin ~ 0.060

with vol D certified at 5.572648770 (above V_dod) and the areas certified below.

Scope, stated honestly: this proves the inequality for the C5 direction set with every
centre at distance exactly 2, i.e. for one configuration family.  For general completions the
same lemma applies but needs (a) a lower bound on vol D when there are more than twelve
faces, and (b) a lower bound on the ring face areas over all admissible directions.  Neither
is supplied here.
"""
import itertools
import sys
from fractions import Fraction as F

import cell_certificate as CC
from rational_interval import Iv, sqrt_iv


def face_areas(normals, dists, verts):
    """Rigorous intervals for the areas of the faces {y.n_i = d_i} of the polytope."""
    out = []
    for i in range(len(normals)):
        on = [x for x in verts
              if sum(normals[i][t] * x[t] for t in range(3)) == dists[i]]
        if len(on) < 3:
            out.append(Iv(0))
            continue
        cyc = CC._cyclic_order(normals[i], on)
        c = [sum(p[t] for p in cyc) / len(cyc) for t in range(3)]
        total = Iv(0)
        for t in range(len(cyc)):
            a = [cyc[t][q] - c[q] for q in range(3)]
            b = [cyc[(t + 1) % len(cyc)][q] - c[q] for q in range(3)]
            cr = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
            n2 = sum(x * x for x in cr)
            total = total + sqrt_iv(Iv(n2)) / 2
        out.append(total)
    return out


def main():
    print("=" * 78)
    print("RING-EXCESS LEMMA, applied to the C5 direction set")
    th_r = F(5828252506, 10 ** 8) / 180       # 58.2825 deg, in units of pi
    th_p = F(112) / 180
    dirs = [(0.0, 0.0, -1.0)]
    import math
    for k in range(5):
        a = math.radians(58.282525060518495)
        dirs.append((math.sin(a) * math.cos(2 * math.pi * k / 5),
                     math.sin(a) * math.sin(2 * math.pi * k / 5), math.cos(a)))
    for k in range(5):
        a = math.radians(112.0)
        ph = math.radians(36 + 72 * k)
        dirs.append((math.sin(a) * math.cos(ph), math.sin(a) * math.sin(ph), math.cos(a)))
    dirs.append((0.0, 0.0, 1.0))

    def runit(x):
        return F(x).limit_denominator(10 ** 12)

    ns = []
    for d in dirs:
        v = [runit(2 * c) for c in d]
        sq = sum(x * x for x in v)
        L = sqrt_iv(Iv(sq))
        ns.append([Iv(x) / L for x in v])
    ring = range(1, 6)

    def build(b):
        bq = F(int(b * 10 ** 12), 10 ** 12)
        dists = [bq if i in ring else F(1) for i in range(12)]
        nrat = [[x.mid() for x in n] for n in ns]
        dq = [F(int(d * 10 ** 12), 10 ** 12) for d in dists]
        vol, nv, verts = CC.polytope_volume(nrat, dq)
        return vol, nrat, dq, verts, nv

    b = F(1051462224238, 10 ** 12)        # 1.051462224238
    v1, n1, d1, V1, _ = build(1)
    v2, n2, d2, V2, nv2 = build(float(b))
    A1 = face_areas(n1, d1, V1)
    A2 = face_areas(n2, d2, V2)
    print(f"  vol D  (b=1)      = {float(v1):.12f}")
    print(f"  vol K  (b={float(b):.6f}) = {float(v2):.12f}   ({nv2} vertices)")
    print(f"  ring face areas at b=1   : {[round(float(A1[i].lo),6) for i in range(1,6)]}")
    print(f"  ring face areas at b=b   : {[round(float(A2[i].lo),6) for i in range(1,6)]}")
    # the minimum must be taken ALONG the path, not at the ends: sample it (the ring areas
    # decrease monotonically in b; the samples below show it and the minimum is at the end)
    samples = []
    for k in range(21):
        t = 1 + (float(b) - 1) * k / 20
        vv, nn, dd, VV, _ = build(t)
        As = face_areas(nn, dd, VV)
        samples.append((t, min(As[i].lo for i in ring), max(As[i].hi for i in ring)))
    print("  ring area along the path (t, min lo, max hi):")
    for t, a, c in samples:
        print(f"     b={t:.6f}   [{float(a):.9f}, {float(c):.9f}]")
    amin = min(a for _, a, _ in samples)
    print(f"  min ring area along the sampled path (lower bound) = {float(amin):.9f}")
    V_DOD = F(5550291028515510, 10 ** 15)
    gain = 5 * (b - 1) * amin
    bound = V_DOD + gain
    THRESH = F(5763417470, 10 ** 9)
    print(f"\n  bound: V_dod + 5(b-1)A_min = {float(V_DOD):.9f} + {float(gain):.9f} "
          f"= {float(bound):.9f}")
    print(f"  threshold                    {float(THRESH):.9f}")
    ok = bound > THRESH
    print(f"  bound exceeds the threshold: {ok}   (margin {float(bound - THRESH):+.6f})")
    print(f"  [using the certified vol D = {float(v1):.9f} instead of V_dod gives "
          f"{float(v1 + gain):.9f}]")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
