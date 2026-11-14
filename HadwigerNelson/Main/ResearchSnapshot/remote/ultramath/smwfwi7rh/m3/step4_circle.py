"""Step 4: how many colours does the unit circle about a point meet, for the seven-colouring?

A gadget of the m3 type needs a region whose unit shadow avoids three labels; the unit
circle about the accumulation point is always inside the shadow, so the gadget needs a
point whose unit circle misses three labels.  Here we compute that count for c_0.
"""
import numpy as np
from fasthex import colour_arr

rng = np.random.default_rng(7)
N = 3000


def circle_colours(xc, yc, n=N):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return set(np.unique(colour_arr(xc + np.cos(t), yc + np.sin(t))).tolist())


print("unit-circle colour counts for the seven-colouring")
cases = {
    "hexagon centre (lattice point)": (0.0, 0.0),
    "hexagon vertex (in L)": (0.3464, 0.2),
    "generic cell point": (0.05, 0.02),
    "p_0 = (1/55,18/55)": (1 / 55, 18 / 55),
    "midpoint of an edge": (0.1732, 0.3),
}
for k, (x, y) in cases.items():
    s = circle_colours(x, y)
    print(f"  {k:34s}: {sorted(s)}  ({len(s)} colours)")

# minimum over many random points
mn = 7
arg = None
for _ in range(400):
    x, y = rng.uniform(0, 1.4, 2)
    s = circle_colours(x, y, 1200)
    if len(s) < mn:
        mn, arg = len(s), (x, y, sorted(s))
print("\nminimum count over 400 random centres:", mn, "at", arg)

# does a non-cyclic point (cell interior / edge) ever see <= 3 colours?
mn2 = 7
for _ in range(300):
    x, y = rng.uniform(0, 2.8, 2)
    s = circle_colours(x, y, 1200)
    mn2 = min(mn2, len(s))
print("minimum count over 300 more random centres in a larger box:", mn2)
