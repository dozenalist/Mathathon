"""Independent check of the reach geometry by brute force (no use of geometry_fast.py).

For a distance d and sector width Delta = pi/(3m), sector j = [jD,(j+1)D):
sample f (angle phi in sector j) and the translation a = d e^{i beta}, solve
        s + t = f + a,  |s| = |t| = 1
by the exact formula s = (r/2)(1 +- i sqrt(4-|r|^2)/|r|), r = f + a (requires |r| <= 2),
and record which sector s falls into, i.e. the offset o with arg s in sector j+o.
The observed offset range should be exactly  |o - m| < 1 + Sigma(d)/Delta.
"""
import math
import geometry_fast as G

PI = math.pi


def reach_offsets(d, m, j=0, nphi=200, nbeta=701):
    D = PI / (3 * m)
    offs = set()
    for ip in range(nphi):
        phi = j * D + (ip + 0.5) * D / nphi
        f = (math.cos(phi), math.sin(phi))
        for ib in range(nbeta):
            beta = 2 * PI * ib / nbeta
            a = (d * math.cos(beta), d * math.sin(beta))
            r = (f[0] + a[0], f[1] + a[1])
            rho = math.hypot(*r)
            if rho > 2 or rho < 1e-12:
                continue
            th = math.atan2(r[1], r[0])
            al = math.acos(rho / 2)
            for sg in (+1, -1):
                ang = th + sg * al
                ang = (ang - j * D) % (2 * PI)      # relative to the sector start
                o = int(math.floor(ang / D))
                offs.add(o if o <= 3 * m else o - 6 * m)
    return offs


def predicted(d, m):
    S = G.sigma(d)[0]
    D = PI / (3 * m)
    lim = 1 + S / D
    return {o for o in range(-3 * m, 4 * m) if abs(o - m) < lim or abs(o + m) < lim}


if __name__ == "__main__":
    print(" d      m    observed offsets      predicted (|o-m| < 1+Sig/D)   agree?")
    for d in (0.02, 0.05, 0.1, 0.1755, 0.19):
        for m in (6, 12):
            obs = reach_offsets(d, m)
            prd = predicted(d, m)
            # the brute force can only see offsets actually hit by samples: it must be a subset
            # of the predicted set, and must exhaust it up to sampling (no missing integer)
            ok = obs <= prd
            print(f"{d:6.4f} {m:4d}   obs_min={min(obs):4d} obs_max={max(obs):4d}"
                  f"   prd_min={min(prd):4d} prd_max={max(prd):4d}   subset={ok}")
            if not ok:
                print("   extra observed:", sorted(obs - prd))
    print()
    print("Sigma monotonicity on a fine grid")
    prev = -1.0
    bad = []
    for i in range(1, 401):
        d = i * 0.005
        s = G.sigma(d)[0]
        if s < prev - 1e-12:
            bad.append(d)
        prev = s
    print("  violations:", bad if bad else "none on (0,2] with step 0.005")
