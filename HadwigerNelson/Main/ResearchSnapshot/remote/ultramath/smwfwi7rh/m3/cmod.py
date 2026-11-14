"""The k>=7 colouring c: c_0 outside W, label 0 on W minus the disks, Mercedes sectors on D_n."""
import numpy as np
from fractions import Fraction as F
from fasthex import colour_arr

P0 = (1 / 55, 18 / 55)
ELL = 1 / 100
QN = [(P0[0] + ELL * 2 ** (-n - 3), P0[1]) for n in range(40)]
RHO = [ELL * 2 ** (-n - 14) for n in range(40)]


def inW(x, y, ell=ELL):
    return (np.abs(np.asarray(x) - P0[0]) <= ell / 2) & (np.abs(np.asarray(y) - P0[1]) <= ell / 2)


def sector_colour(dx, dy):
    """Mercedes: label 0 on (-60,60) deg, 2 on (60,180), 3 on (180,300)."""
    ang = np.degrees(np.arctan2(dy, dx)) % 360.0
    out = np.where((ang > 60) & (ang <= 180), 2, np.where((ang > 180) & (ang <= 300), 3, 0))
    return out


def colour_mod(x, y):
    x = np.atleast_1d(np.asarray(x, float))
    y = np.atleast_1d(np.asarray(y, float))
    out = colour_arr(x, y)
    inside = inW(x, y)
    if not np.any(inside):
        return out
    out = np.where(inside, 0, out)
    for q, rho in zip(QN, RHO):
        d = np.hypot(x - q[0], y - q[1])
        ind = d <= rho
        if np.any(ind):
            out = np.where(ind, sector_colour(x - q[0], y - q[1]), out)
    return out
