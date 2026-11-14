"""Step 2: numerical confirmation that Gamma_x is the interface graph of the tiling."""
import numpy as np
from fasthex import colour_arr

rng = np.random.default_rng(20260514)
R = 2 / 5


def ratios(xc, yc, delta=0.05, tau=1e-3, n=400000):
    ang = rng.uniform(0, 2 * np.pi, n)
    rad = delta * np.sqrt(rng.uniform(0, 1, n))
    qx, qy = xc + rad * np.cos(ang), yc + rad * np.sin(ang)
    a = colour_arr(qx, qy)
    out = {}
    for (hx, hy) in [(tau, 0.0), (0.0, tau), (tau / np.sqrt(2), tau / np.sqrt(2))]:
        b = colour_arr(qx + hx, qy + hy)
        code = a * 7 + b
        cnt = np.bincount(code, minlength=49).reshape(7, 7)
        M = (cnt + cnt.T).astype(float) * np.pi * delta ** 2 / tau / n
        out[(hx, hy)] = M
    return out


def show(name, xc, yc):
    print(f"{name} at ({xc:.4f},{yc:.4f})")
    for (hx, hy), M in ratios(xc, yc).items():
        pos = [(i, j, M[i, j]) for i in range(7) for j in range(i + 1, 7) if M[i, j] > 1e-4]
        print(f"   h=({hx:.1e},{hy:.1e}): " +
              ", ".join(f"{i}{j}:{v:.4f}" for i, j, v in pos) if pos else "   (none)")
    print()


v0 = (R * np.cos(np.pi / 6), R * np.sin(np.pi / 6))
v1 = (R * np.cos(np.pi / 2), R * np.sin(np.pi / 2))
show("VERTEX (hexagons of colour 0,1,3)", v0[0], v0[1])
show("EDGE MIDPOINT", (v0[0] + v1[0]) / 2, (v0[1] + v1[1]) / 2)
show("CELL INTERIOR", 0.05, 0.02)
