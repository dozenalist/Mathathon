"""Step 5: transition ratios for the modified colouring c at the predicted cyclic centres.

|h| is scaled to the ball radius: a transition strip of width |h| across an interface of
length ~ delta inside the ball gives |D|/|h| ~ delta, so the three columns should be O(delta).
"""
import numpy as np
from cmod import colour_mod, QN, RHO, P0

rng = np.random.default_rng(11)


def ratios(xc, yc, delta, n=200000):
    tau = delta / 8
    ang = rng.uniform(0, 2 * np.pi, n)
    rad = delta * np.sqrt(rng.uniform(0, 1, n))
    qx, qy = xc + rad * np.cos(ang), yc + rad * np.sin(ang)
    a = colour_mod(qx, qy)
    res = {}
    for (hx, hy) in [(tau, 0.0), (0.0, tau), (tau / np.sqrt(2), tau / np.sqrt(2))]:
        b = colour_mod(qx + hx, qy + hy)
        code = a * 7 + b
        cnt = np.bincount(code, minlength=49).reshape(7, 7)
        M = (cnt + cnt.T).astype(float) * np.pi * delta ** 2 / tau / n
        res[(hx, hy)] = M
    return res, tau


def show(name, xc, yc, delta):
    res, tau = ratios(xc, yc, delta)
    print(f"{name}  at ({xc:.7f},{yc:.7f});  ball {delta:.2e}, |h| {tau:.2e}")
    for (hx, hy), M in res.items():
        pos = [(i, j, M[i, j]) for i in range(7) for j in range(i + 1, 7) if M[i, j] > 0.02 * delta]
        print("    " + (", ".join(f"{i}{j}:{v:.2e}" for i, j, v in pos) if pos else "(no transitions)"))
    print()


show("q_0  Mercedes centre          ", QN[0][0], QN[0][1], 0.3 * RHO[0])
show("ray endpoint of D_0 at 180 deg", QN[0][0] - RHO[0], QN[0][1], 0.3 * RHO[0])
show("general point of W            ", P0[0] - 0.002, P0[1] + 0.001, 4e-4)
show("p_0  accumulation point       ", P0[0], P0[1], 4e-4)
show("hexagon vertex outside W      ", 0.3464, 0.2, 0.05)
