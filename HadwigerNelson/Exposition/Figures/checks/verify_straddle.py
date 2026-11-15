"""Verify the Lesson 3 straddle figures against the predicates in Sections 16-17."""
import math, re, sys
from pathlib import Path

FIG = Path(sys.argv[1])

# ---------------- Figure A: shaded region vs. Delta(K) = {min<1<max}
s = (FIG / "straddle-band.svg").read_text(encoding="utf-8")
m = re.search(r'<path d="([^"]+)" fill="#fbe9e5" fill-rule="evenodd"', s)
assert m, "band path not found"
rings = []
for sub in m.group(1).split("Z"):
    pts = [tuple(map(float, p.split(","))) for p in re.findall(r"-?[\d.]+,-?[\d.]+", sub)]
    if pts:
        rings.append(pts)
print("band path rings:", len(rings), [len(r) for r in rings])

def inside_evenodd(x, y):
    c = False
    for ring in rings:
        n = len(ring)
        for i in range(n):
            x1, y1 = ring[i]; x2, y2 = ring[(i + 1) % n]
            if (y1 > y) != (y2 > y):
                xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if xi > x:
                    c = not c
    return c

# geometry from the SVG itself: the K segment (stroke-width 6) and the unit from the dashed circle
seg = re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="#172c43" stroke-width="6"', s)
px, py, qx, qy = map(float, seg.groups())
UNIT = float(re.search(r'<circle cx="[\d.]+" cy="[\d.]+" r="([\d.]+)" fill="none"', s).group(1))
Lfig = math.hypot(qx - px, qy - py) / UNIT
print(f"K endpoints ({px},{py})-({qx},{qy}); UNIT={UNIT}; L measured={Lfig:.4f}")

def dist_seg(x, y):
    vx, vy = qx - px, qy - py
    t = max(0, min(1, ((x - px) * vx + (y - py) * vy) / (vx * vx + vy * vy)))
    return math.hypot(x - px - t * vx, y - py - t * vy) / UNIT

def maxd(x, y):  # max over a segment is attained at an endpoint
    return max(math.hypot(x - px, y - py), math.hypot(x - qx, y - qy)) / UNIT

N = 400
x0, x1 = px - 1.15 * UNIT, qx + 1.15 * UNIT
y0, y1 = py - 1.15 * UNIT, py + 1.15 * UNIT
tol = 0.01
tot = bnd = bad = shaded = 0
bads = []
for i in range(N):
    for j in range(N):
        x = x0 + (i + 0.5) * (x1 - x0) / N
        y = y0 + (j + 0.5) * (y1 - y0) / N
        mn, mx = dist_seg(x, y), maxd(x, y)
        truth = mn < 1 < mx
        fig = inside_evenodd(x, y)
        tot += 1; shaded += fig
        if abs(mn - 1) < tol or abs(mx - 1) < tol:
            bnd += 1
            continue
        if truth != fig:
            bad += 1; bads.append((x, y, mn, mx, fig))
print(f"Figure A grid {N}x{N}: {tot} samples, {bnd} within 1% of boundary (skipped), "
      f"{tot-bnd} checked, {bad} misclassified; shaded={shaded}")
print("  first misclassified:", bads[:5])
# strict boundary check: misclassifications at any tolerance
strict = sum(1 for i in range(N) for j in range(N)
             if ((lambda x, y: (dist_seg(x, y) < 1 < maxd(x, y)) != inside_evenodd(x, y))
                 (x0 + (i + .5) * (x1 - x0) / N, y0 + (j + .5) * (y1 - y0) / N)))
print(f"  with no tolerance at all: {strict} of {tot} disagree (polygon approximation only)")

# label placements in figure A
for lab in ["within 1 of all of K", "Δ(K)"]:
    for mm in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*>' + re.escape(lab) + "<", s):
        x, y = float(mm.group(1)), float(mm.group(2)) - 7
        print(f"  label '{lab}' at ({x:.0f},{y:.0f}): min={dist_seg(x,y):.3f} max={maxd(x,y):.3f} "
              f"in Delta={dist_seg(x,y) < 1 < maxd(x,y)} shaded={inside_evenodd(x,y)}")

# ---------------- Figure B: contact distances
s = (FIG / "straddle-contact.svg").read_text(encoding="utf-8")
U = 360.0
z = re.search(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="7" fill="#172c43"', s)
zx, zy = map(float, z.groups())
lines = [tuple(map(float, l)) for l in re.findall(
    r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)"', s)]
K = [l for l in lines if l[1] == l[3]][0]
print(f"\nFigure B: z=({zx},{zy}); K from x={K[0]} to {K[2]} at y={K[1]}")
dK0 = math.hypot(K[0] - zx, K[1] - zy) / U; dK1 = math.hypot(K[2] - zx, K[3] - zy) / U
print(f"  K end distances: near {dK0:.4f} (<1: {dK0<1}), far {dK1:.4f} (>1: {dK1>1})")
for l in lines:
    if (l[0], l[1]) == (zx, zy):
        d = math.hypot(l[2] - zx, l[3] - zy) / U
        onK = abs(l[3] - K[1]) < 1e-6 and K[0] <= l[2] <= K[2]
        print(f"  ruler to ({l[2]:.1f},{l[3]:.1f}): length {d:.4f}, endpoint on K: {onK}")
# dashed arc crosses K exactly at the contact?
arc = re.search(r'<polyline points="([^"]+)"', s).group(1)
apts = [tuple(map(float, p.split(","))) for p in arc.split()]
rad = [math.hypot(x - zx, y - zy) / U for x, y in apts]
print(f"  dashed arc radius range {min(rad):.5f}..{max(rad):.5f}; y-range {min(p[1] for p in apts):.1f}..{max(p[1] for p in apts):.1f}")
for lab in ["dashed: unit circle of z"]:
    mm = re.search(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*>' + re.escape(lab), s)
    print(f"  label '{lab}' at ({mm.group(1)},{mm.group(2)})")

# ---------------- Figure C: gap distances
s = (FIG / "straddle-gap.svg").read_text(encoding="utf-8")
U = 240.0
dots = [tuple(map(float, d)) for d in re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="8"', s)]
(ax, ay), (bx, by) = dots
mc = re.search(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="10"', s)
mx_, my_ = map(float, mc.groups())
print(f"\nFigure C: z=first point ({ax},{ay}); second ({bx},{by})")
print(f"  distance z->z = 0, z->second = {math.hypot(bx-ax, by-ay)/U:.4f}, z->missing contact = {math.hypot(mx_-ax, my_-ay)/U:.4f}")
arc = re.search(r'<polyline points="([^"]+)"', s).group(1)
apts = [tuple(map(float, p.split(","))) for p in arc.split()]
rad = [math.hypot(x - ax, y - ay) / U for x, y in apts]
print(f"  dashed arc radius range {min(rad):.5f}..{max(rad):.5f}; passes through midpoint: "
      f"{min(math.hypot(x-mx_, y-my_) for x, y in apts):.2f}px")
