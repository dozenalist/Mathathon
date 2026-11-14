"""High-precision values of the frozen-field transport radii, with a rigorous bracket.

The quantised criterion flips exactly at the first d where
   M(d) := max_{psi,branch} |delta|      reaches the top of the safe window, or
   m(d) := min_{psi,branch} |delta|      reaches the bottom of it.
For a word whose safe set is {a..b} mod 12 (Delta = 10 deg) the window is
   [a*10 deg, (b+1)*10 deg)   (an integer j is safe iff a <= j mod 12 <= b,
                              and the achievable j's are floor(|delta|/Delta), +1),
so the flip is at  M = (b+1)*Delta  or  m = a*Delta.
"""
from mpmath import mp, mpf, cos, sin, atan2, acos, sqrt, pi as MPI, findroot, fabs
import numpy as np
mp.dps = 30
DELTA = mpf(10)

def extremes(d, N=4000000):
    psi = np.linspace(-np.pi, np.pi, N, endpoint=False)
    d = float(d)
    wr = d + np.cos(psi); wi = np.sin(psi)
    r = np.hypot(wr, wi); argw = np.arctan2(wi, wr)
    g = np.arccos(np.clip(r / 2, -1, 1))
    mx = mn = None; psx = None
    for sgn in (+1, -1):
        dl = argw + sgn * g - psi
        dl = np.mod(dl + np.pi, 2 * np.pi) - np.pi
        a = np.abs(dl)
        if mx is None or a.max() > mx:
            mx = a.max(); psx = psi[int(np.argmax(a))]
        mn = a.min() if mn is None else min(mn, a.min())
    return np.degrees(mx), np.degrees(mn), psx

def dmax_deg(d, psi0):
    """high-precision max over both branches near psi0 (degrees)."""
    def f(p, sgn):
        wr = mpf(d) + cos(p); wi = sin(p)
        r = sqrt(wr * wr + wi * wi)
        return fabs(atan2(wi, wr) + sgn * acos(min(r / 2, 1)) - p) * 180 / MPI
    best = mpf(0)
    for sgn in (+1, -1):
        try:
            p = findroot(lambda p: (lambda wr, wi, r: (
                (atan2(wi, wr) + sgn * acos(min(r / 2, 1)) - p) *
                (sin(p) / sqrt(d * d + 2 * d * cos(p) + 1) * 0 + 1)))(mpf(d) + cos(p), sin(p),
                sqrt((mpf(d) + cos(p)) ** 2 + sin(p) ** 2)), mpf(psi0))
        except Exception:
            p = mpf(psi0)
        v = f(p, sgn)
        best = max(best, v)
    return best

if __name__ == "__main__":
    print("d      M(deg)      m(deg)")
    for d in (0.1, 0.14, 0.14715, 0.15, 0.2, 0.285, 0.28558, 0.286, 0.3):
        M, m, psx = extremes(d)
        print("%.5f  %.6f   %.6f" % (d, M, m))
