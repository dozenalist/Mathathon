"""
Task (2): numerical adversarial check of the far-field decoupling lemma.

Background colouring c0 = the paper's proper seven-colouring (sprint/k6/PHASE-TRANSITION.md):
  r = 2/5 (hexagon circumradius), d = sqrt(3)*r = 2*sqrt(3)/5 (lattice spacing),
  Lambda = d*(Z + Z*w), w = e^{2*pi*i/3};  Voronoi hexagons have circumradius r, inradius sqrt(3)/5.
  colour of the hexagon with centre d*(m + n*w) is (m + 2*n) mod 7.
  (same-colour centres are at distance >= sqrt(21)*r = 1.8330... > 1 + 2r = 1.8, so c0 is proper)

Modified colouring c_rho:  label 7 on the open disk {|z| < rho - 1/100}, c0 elsewhere.
x_0 = 0.  c_rho agrees with c0 off the closed disk of radius rho - 1/100.

Sampling: for a centre y and radius r, the sample function is t |-> colour(y + r*u(t));  we
estimate the angular measure of each colour by N equally spaced angles, i.e. by the exact
rational occupancy counts/N.  This is an *explicit quadrature of the angular measure*: the
estimate for colour i is  (1/N) #{k : colour(y + r u_k) = i}  ->  |{t : ...}| (angular measure).

Error control:
 * counts are exact integers; the quadrature error is O(1/N) in the measure of the boundary
   directions (t where y + r*u(t) lies on a cell boundary), measured below as frac_boundary;
 * each sampled point carries a "certificate margin" margin = dist(2nd nearest centre) -
   dist(nearest centre) > 0, which certifies cell membership independently of float roundoff
   (roundoff on the margin is < 1e-12).
Geometry criterion (exact): the circle of radius r about y misses the open disk of radius R
iff r - |y| >= R.  Checked in exact rational arithmetic below (Fractions).
"""
from fractions import Fraction as F
import math, sys

W = complex(-0.5, math.sqrt(3)/2)      # e^{2 pi i /3}
R_HEX = 0.4                            # circumradius of Voronoi hexagon  (= 2/5)
D = math.sqrt(3)*R_HEX                 # lattice spacing                   (= 2 sqrt3 / 5)

def lattice_coords(z):
    """z = D*(m + n*W)  ->  (m, n) as floats."""
    ze = z / D
    n = 2*ze.imag/math.sqrt(3)
    m = ze.real + n/2
    return m, n

def colour_bg_with_margin(z):
    """colour of z under c0, plus a certified margin (2nd nearest centre dist - nearest)."""
    m0, n0 = lattice_coords(z)
    best = None
    for dm in (-1, 0, 1):
        for dn in (-1, 0, 1):
            m = round(m0) + dm
            n = round(n0) + dn
            c = D*(m + n*W)
            dist = abs(z - c)
            if best is None or dist < best[0]:
                best = (dist, m, n)
    dist1, m, n = best
    second = min(abs(z - D*((m+dm) + (n+dn)*W))
                 for dm in (-2,-1,0,1,2) for dn in (-2,-1,0,1,2)
                 if (dm, dn) != (0, 0))
    return ((m + 2*n) % 7), second - dist1

def make_modified(rho, label=7):
    Rmod = rho - F(1, 100)
    def f(z):
        if abs(z) < float(Rmod):
            return label, float('inf')      # inside an open disk: membership is exact
        c, mg = colour_bg_with_margin(z)
        return c, mg
    return f, Rmod

def sample(col, y, r, N):
    """exact occupancy counts and diagnostics for the circle of radius r about y."""
    counts = [0]*8
    frac_boundary = 0
    min_margin = float('inf')
    min_abs = float('inf'); max_abs = 0.0
    for k in range(N):
        th = 2*math.pi*k/N
        z = y + r*complex(math.cos(th), math.sin(th))
        c, mg = col(z)
        counts[c] += 1
        a = abs(z)
        min_abs = min(min_abs, a); max_abs = max(max_abs, a)
        if mg <= 1e-6:
            frac_boundary += 1
        else:
            min_margin = min(min_margin, mg)
    fr = [c/N for c in counts]
    return fr, frac_boundary/N, min_margin, min_abs, max_abs, counts

def grid_points(delta, radii):
    s = int(round(delta*64))               # grid step = 1/64 (exact in binary floating point)
    offs = sorted({F(a, 64) for a in range(-s, s+1)})
    return [(F(a,64), F(b,64)) for a in range(-s, s+1) for b in range(-s, s+1)], radii

def run(rho, delta, N, nrad):
    fn, Rmod = make_modified(rho)
    c0 = lambda z: colour_bg_with_margin(z)
    radii = [F(64 - j, 64) for j in range(-nrad, nrad+1)]   # r = 1 - j/64, |j| <= nrad
    pts = [F(a, 64) for a in range(-int(round(delta*64)), int(round(delta*64))+1)]
    centres = [(a, b) for a in pts for b in pts]
    out = {}
    for name, col in (("background c0", c0), ("modified c_rho", fn)):
        rows = []
        for (a, b) in centres:
            y = complex(float(a), float(b))
            ay2 = a*a + b*b                    # exact |y|^2
            for r in radii:
                fr, fb, mm, amin, amax, cnt = sample(col, y, r, N)
                # exact criterion  r - |y| >= Rmod   <=>  (r - Rmod)^2 >= |y|^2  (both sides >= 0)
                safe = (r - Rmod) >= 0 and (r - Rmod)**2 >= ay2
                rows.append((a, b, r, fr, fb, mm, amin, amax, safe))
        out[name] = rows
    return out, Rmod

def report(rho, delta, N=2048, nrad=6, thr=1e-3):
    res, Rmod = run(rho, delta, N, nrad)
    print(f"=== rho = {rho}   (recoloured disk of radius {float(Rmod):.4f} carries label 7) ===")
    print(f"    x_0 = 0, grid: |y| <= {delta} with y on (1/64)Z^2, radii r = 1 - j/64, |j| <= {nrad}, N = {N} angles")
    for name, rows in res.items():
        safe = [row for row in rows if row[8]]
        unsafe = [row for row in rows if not row[8]]
        pal = set()
        for row in rows:
            for i in range(8):
                if sum(1 for x in rows if x[3][i] > thr) > 0:
                    pal.add(i)
        # palette estimate as delta -> 0: colours with occupancy > thr on EVERY grid circle
        pal_all = {i for i in range(8) if all(row[3][i] > thr for row in rows)}
        print(f"  [{name}]")
        print(f"    circles with r - |y| >= {float(Rmod):.6f} (exact criterion, Fractions): {len(safe)} of {len(rows)}")
        if safe:
            m7 = max(row[3][7] for row in safe)
            print(f"      max fraction of label 7 on those circles: {m7:.6f}   "
                  f"(counts all zero: {all(row[5-1] is not None for row in safe) and m7 == 0.0})")
            print(f"      min over those circles of (2nd-nearest-centre margin): "
                  f"{min(row[5] for row in safe):.3e};  max fraction of directions on a cell boundary: "
                  f"{max(row[4] for row in safe):.3e}")
            print(f"      observed min/max |z| on the outermost such circle: "
                  f"{min(row[6] for row in safe):.6f} / {max(row[7] for row in safe):.6f}")
        if unsafe:
            print(f"      max fraction of label 7 on the {len(unsafe)} circles that do meet the disk: "
                  f"{max(row[3][7] for row in unsafe):.6f}")
        print(f"    colours with occupancy > {thr} on some grid circle (estimate made coarser by the grid): {sorted(pal)}")
        print(f"    colours with occupancy > {thr} on *every* grid circle (limit estimate): {sorted(pal_all)}")
        print(f"    occupancy of the 7 background labels on the circle y=0, r=1: "
              f"{[round(x,4) for x in [row for row in rows if row[0]==0 and row[1]==0 and row[2]==1][0][3]]}")
    return res

def margin_study(rho, N=2048):
    """max fraction of the modified label over the grid |y|<=delta, |r-1|<=delta, as delta -> 0."""
    fn, Rmod = make_modified(rho)
    print(f"=== margin study, rho = {rho}: max occupancy of label 7 over |y| <= d, |r-1| <= d ===")
    for d64 in (8, 4, 2, 1):
        d = F(d64, 64)
        mx = 0.0; mx_safe = 0.0; arg = None
        for a in range(-d64, d64+1):
            for b in range(-d64, d64+1):
                y = complex(a/64, b/64); ay2 = F(a*a+b*b, 64*64)
                for j in range(-d64, d64+1):
                    r = F(64 - j, 64)
                    fr, fb, mm, amin, amax, cnt = sample(fn, y, r, N)
                    safe = (r - Rmod) >= 0 and (r - Rmod)**2 >= ay2
                    if safe: mx_safe = max(mx_safe, fr[7])
                    if fr[7] > mx:
                        mx = fr[7]; arg = (str(r), (a/64, b/64), safe)
        print(f"  d = {float(d):.4f}: max occupancy label 7 = {mx:.6f} at {arg}; "
              f"max over circles with r-|y| >= R (exactly): {mx_safe:.6f}")

if __name__ == "__main__":
    report(F(85,100), F(1,16), N=2048, nrad=6)
    report(F(130,100), F(1,16), N=2048, nrad=6)
    margin_study(F(85,100), N=1024)
