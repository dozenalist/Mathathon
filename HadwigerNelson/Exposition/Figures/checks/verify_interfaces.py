"""Verify the Lesson 4 figures against the exact predicates (Sections 20-23)."""
import math, re, sys
from pathlib import Path
FIG = Path(sys.argv[1])

def rings_of(d):
    out = []
    for sub in d.split("Z"):
        pts = [tuple(map(float, p.split(","))) for p in re.findall(r"-?[\d.]+,-?[\d.]+", sub)]
        if pts: out.append(pts)
    return out

def inside(rings, x, y):
    c = False
    for ring in rings:
        n = len(ring)
        for i in range(n):
            x1, y1 = ring[i]; x2, y2 = ring[(i + 1) % n]
            if (y1 > y) != (y2 > y) and x1 + (y - y1) * (x2 - x1) / (y2 - y1) > x:
                c = not c
    return c

def seg_min(x, y, p, q, U):
    vx, vy = q[0]-p[0], q[1]-p[1]
    t = max(0, min(1, ((x-p[0])*vx + (y-p[1])*vy) / (vx*vx + vy*vy)))
    return math.hypot(x-p[0]-t*vx, y-p[1]-t*vy) / U

def seg_max(x, y, p, q, U):
    return max(math.hypot(x-p[0], y-p[1]), math.hypot(x-q[0], y-q[1])) / U

def straddles(x, y, p, q, U, tol=0.0):
    mn, mx = seg_min(x, y, p, q, U), seg_max(x, y, p, q, U)
    return mn < 1 < mx, (abs(mn-1) < tol or abs(mx-1) < tol)

def grid(N, x0, x1, y0, y1):
    for i in range(N):
        for j in range(N):
            yield x0 + (i+.5)*(x1-x0)/N, y0 + (j+.5)*(y1-y0)/N

N = 400; TOL = 0.01

# ---------------- shadow
s = (FIG/"interface-shadow.svg").read_text(encoding="utf-8")
d = re.search(r'<path d="([^"]+)" fill="#fbe9e5"', s).group(1); R = rings_of(d)
U = float(re.search(r'<circle cx="[\d.]+" cy="[\d.]+" r="([\d.]+)" fill="none"', s).group(1))
seg = re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="#172c43" stroke-width="6"', s)
p = (float(seg.group(1)), float(seg.group(2))); q = (float(seg.group(3)), float(seg.group(4)))
L = math.hypot(q[0]-p[0], q[1]-p[1]) / U
tot = skip = bad = shaded = far_from_circle = 0
side_bad = 0; spill = 0
for x, y in grid(N, p[0]-1.2*U, q[0]+1.2*U, p[1]-1.2*U, p[1]+1.2*U):
    tot += 1
    truth, near = straddles(x, y, p, q, U, TOL)
    fig = inside(R, x, y); shaded += fig
    if near: skip += 1; continue
    if truth != fig: bad += 1
    if truth:
        r = math.hypot(x-p[0], y-p[1]) / U
        if not abs(r-1) < L: far_from_circle += 1
        # side claim: outside the circle -> facing half (dx>0); inside -> far half (dx<0), away from the perpendicular
        # refined claim (referee): outer points only on the facing half (c>0); inner points only where c < L/2
        c = (x-p[0])/(r*U)
        if r > 1 and c <= 0: side_bad += 1
        if r < 1 and c >= L/2: side_bad += 1
        if r < 1 and c > 0: spill += 1
print(f"SHADOW: L={L:.4f} U={U}; grid {N}x{N}={tot}; {skip} within 1% of boundary skipped; "
      f"{tot-skip} checked; {bad} misclassified; shaded {shaded}")
print(f"  straddling points not within L of the unit circle around x: {far_from_circle}")
print(f"  outer points off the facing half, or inner points with cos >= L/2: {side_bad}; inner points spilling onto the facing half: {spill}")

# ---------------- cone
s = (FIG/"interface-cone.svg").read_text(encoding="utf-8")
paths = re.findall(r'<path d="([^"]+)"', s)
d1 = rings_of(paths[1]); d2 = rings_of(paths[2])   # [0] is clip path (= d2), [1] blue, [2] green, [3] red(d1 clipped)
assert paths[0] == paths[2] and paths[3] == paths[1]
U = 180.0
lines = re.findall(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="(#[0-9a-f]+)" stroke-width="5"', s)
segs = [((float(a), float(b)), (float(c), float(dd))) for a, b, c, dd, _ in lines]
xc = segs[0][0]
angs = [math.degrees(math.atan2(-(sq[1]-sp[1]), sq[0]-sp[0])) for sp, sq in segs]
lens = [math.hypot(sq[0]-sp[0], sq[1]-sp[1]) / U for sp, sq in segs]
print(f"CONE: directions {angs[0]:.3f} and {angs[1]:.3f} deg (gap {angs[0]-angs[1]:.3f}); lengths {lens}")
tot = skip = bad = red = 0; far = 0; red_out_facing = 0
for x, y in grid(N, xc[0]-1.25*U, xc[0]+1.35*U, xc[1]-1.3*U, xc[1]+1.3*U):
    tot += 1
    t1, n1 = straddles(x, y, *segs[0], U, TOL); t2, n2 = straddles(x, y, *segs[1], U, TOL)
    f1, f2 = inside(d1, x, y), inside(d2, x, y)
    if n1 or n2: skip += 1; continue
    if (t1, t2) != (f1, f2): bad += 1
    if t1 and t2:
        red += 1
        r = math.hypot(x-xc[0], y-xc[1]) / U
        if not abs(r-1) < max(lens): far += 1
area_unit = red * ((2.6*U/N)*(2.6*U/N)) / U**2
print(f"  grid {N}x{N}={tot}; {skip} skipped (1% boundary); {tot-skip} checked; {bad} misclassified (blue, green or red)")
print(f"  red (both) samples {red}, approx area {area_unit:.4f} square units; red samples not within L of the circle: {far}")

# ---------------- model
s = (FIG/"interface-model.svg").read_text(encoding="utf-8")
U = 300.0
K = re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="#172c43" stroke-width="5"', s)
kp = (float(K.group(1)), float(K.group(2))); kq = (float(K.group(3)), float(K.group(4)))
z = re.search(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="7" fill="#172c43"', s)
zx, zy = float(z.group(1)), float(z.group(2))
r = re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="#b33d39"', s)
qx, qy = float(r.group(3)), float(r.group(4))
print(f"MODEL: K from {kp} to {kq} (length {math.hypot(kq[0]-kp[0], kq[1]-kp[1])/U:.3f})")
print(f"  z to K: min {seg_min(zx, zy, kp, kq, U):.4f}, max {seg_max(zx, zy, kp, kq, U):.4f} -> straddles {straddles(zx, zy, kp, kq, U)[0]}")
fr = (qy-kq[1])/(kp[1]-kq[1])
print(f"  ruler z->q length {math.hypot(qx-zx, qy-zy)/U:.5f}; q on K line: {abs(qx-kp[0])<1e-6}; q at fraction {fr:.3f} of K (0,1 are ends)")
rects = re.findall(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" fill="(#[0-9a-f]+)"', s)
rA = [tuple(map(float, r_[:4])) for r_ in rects if r_[4] == "#e7f0fb"][0]
rB = [tuple(map(float, r_[:4])) for r_ in rects if r_[4] == "#e3f2e6"][0]
for col, rect in (("#235f9d", rA), ("#2f7a4a", rB)):
    pl = re.search(r'<polyline points="([^"]+)" fill="none" stroke="' + col + '" stroke-width="6"', s).group(1)
    pts = [tuple(map(float, pp.split(","))) for pp in pl.split()]
    radii = [math.hypot(x-zx, y-zy)/U for x, y in pts]
    inrect = all(rect[0] <= x <= rect[0]+rect[2] and rect[1] <= y <= rect[1]+rect[3] for x, y in pts)
    print(f"  thick arc {col}: {len(pts)} pts, radius {min(radii):.5f}..{max(radii):.5f}, all inside its strip: {inrect}")
