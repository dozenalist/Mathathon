"""Step 6: numerical check of L(c_0) = V at the only scales where it can fail.

A point x is a junction (=point of L) iff every ball about it meets >=3 colours.
Numerically: sample x, and compare the predicate 'ball of radius delta about x meets
>=3 colours' with 'dist(x, V) < delta', for a range of delta.
"""
import numpy as np
from fasthex import colour_arr

rng = np.random.default_rng(3)
R = 2 / 5


def vertex_set(mr, nr):
    vs = []
    for m in range(-mr, mr + 1):
        for n in range(-nr, nr + 1):
            cx, cy = np.sqrt(3) * (2 * m - n) / 5, 3 * n / 5
            for k in range(6):
                a = np.pi / 6 + k * np.pi / 3
                vs.append((cx + R * np.cos(a), cy + R * np.sin(a)))
    return np.array(vs)


V = vertex_set(8, 8)
for delta in [2e-2, 6e-3, 2e-3, 6e-4]:
    n = 4000
    # half the points near vertices, half uniform
    idx = rng.integers(0, len(V), n // 2)
    near = V[idx] + rng.normal(0, 1.5 * delta, (n // 2, 2))
    far = rng.uniform(-2, 2, (n // 2, 2))
    pts = np.vstack([near, far])
    cols = set()
    for a in range(0, 360, 30):
        for rad in (1.0, 0.6):
            cols.add((rad * np.cos(np.radians(a)), rad * np.sin(np.radians(a))))
    cols = list(cols)
    seen = np.zeros(len(pts), dtype=bool)
    for dx, dy in cols:
        c = colour_arr(pts[:, 0] + delta * dx, pts[:, 1] + delta * dy)
        seen |= np.ones(len(pts), bool)
    cnt = np.zeros(len(pts), dtype=int)
    sets = []
    for dx, dy in cols:
        sets.append(colour_arr(pts[:, 0] + delta * dx, pts[:, 1] + delta * dy))
    for i in range(len(pts)):
        cnt[i] = len({s[i] for s in sets})
    d = np.sqrt(((pts[:, None, :] - V[None, :, :]) ** 2).sum(-1)).min(1)
    pred_junction = cnt >= 3
    pred_vertex = d < delta
    mism = np.sum(pred_junction != pred_vertex)
    # mismatches are only expected for points within a factor 2 of delta
    tight = (np.abs(d - delta) > 0.6 * delta) & (cnt == 3) | (np.abs(d - delta) > 0.6 * delta)
    bad = np.sum((pred_junction != pred_vertex) & tight)
    print(f"delta={delta:8.1e}: points {len(pts)}, '#colours>=3' {pred_junction.sum():5d}, "
          f"'dist<delta' {pred_vertex.sum():5d}, mismatches {mism:5d}, "
          f"mismatches away from the boundary band {bad}")
