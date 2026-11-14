"""The paper's two-angle decomposition maps, and a bound on their deviation.

Paper (Lemma 5.5 proof, p.30): for y = x + d (d > 0 real, |x-y| = d < 1/2) and t real,

    Theta_d(t) = t + Im log(1 + d e^{-it}),
    alpha_pm(t) = Theta_d(t) +/- arccos(|d + e^{it}|/2),

is a smooth degree-one lift with, for every t,

    d + e^{it} = e^{i alpha_+(t)} + e^{i alpha_-(t)}.                             (2ang)

Part 1  (2ang) verified numerically;  Part 2  the deviation
    DEV(d) = sup_t max_pm |alpha_pm(t) - (t +/- pi/3)|
is tabulated and compared with the rigorous bound C d, C = 4, of no-go.md Prop 3.1.  The
key constants of that proof are recomputed here; a second, independent path evaluates
alpha_pm on a grid with mpmath.iv interval arithmetic (rigorous enclosures).

Note: the deviation bound is a statement about ONE pair of centres, i.e. a single d; it is
uniform in t and in the direction of the displacement (rotation equivariance, checked in
model_check.py).
"""
import numpy as np
import mpmath as mp
from mpmath import iv

KAPPA = np.pi / 3.0


# ---------------------------------------------------------------- float64 path
def alpha_pm_float(d, t):
    z = 1.0 + d * np.exp(-1j * t)
    Theta = t + np.angle(z)
    rho = abs(d + np.exp(1j * t))
    a = np.arccos(rho / 2.0)
    return Theta + a, Theta - a


def residual_float(d, t):
    ap, am = alpha_pm_float(d, t)
    return abs((d + np.exp(1j * t)) - (np.exp(1j * ap) + np.exp(1j * am)))


def dev_float(d, t):
    ap, am = alpha_pm_float(d, t)
    return max(abs(ap - (t + KAPPA)), abs(am - (t - KAPPA)))


# ------------------------------------------------------- interval (rigorous) path
def iv_acos(y):
    """arccos on [0,1] as an interval enclosure (mpmath.iv has no acos)."""
    return iv.atan2(iv.sqrt(1 - y * y), y)


def alpha_pm_iv(d, t):
    d = iv.mpf(d)
    t = iv.mpf(t) if not isinstance(t, iv.mpf) else t
    ct, st = iv.cos(t), iv.sin(t)
    Theta = t + iv.atan2(-d * st, 1 + d * ct)      # t + arg(1 + d e^{-it})
    rho = iv.sqrt(d * d + 2 * d * ct + 1)          # |d + e^{it}|
    a = iv_acos(rho / 2)
    return Theta + a, Theta - a


def dev_iv(d, t):
    ap, am = alpha_pm_iv(d, t)
    return max(abs(ap - (iv.mpf(t) + iv.mpf(mp.pi) / 3)),
               abs(am - (iv.mpf(t) - iv.mpf(mp.pi) / 3)))


def main():
    print("=== (2ang) identity residual, float64 (formula sanity check) ===")
    worst = 0.0
    for d in [0.001, 0.01, 0.05, 0.1, 0.25, 0.49]:
        ts = np.linspace(-np.pi, np.pi, 20001, endpoint=False)
        r = max(residual_float(d, t) for t in ts)
        worst = max(worst, r)
        print(f"  d={d:<6}  sup residual = {r:.3e}")
    print(f"  worst: {worst:.3e}  (float64 rounding only)")

    print("\n=== deviation sup_t max_pm |alpha_pm - (t +/- kappa)|  (float64, fine grid) ===")
    ts = np.linspace(-np.pi, np.pi, 60001, endpoint=False)
    worst_ratio = 0.0
    for d in [1e-4, 1e-3, 1e-2, 0.02, 0.03, 0.05, 0.0873, 0.1, 0.2, 0.3, 0.4, 0.49]:
        m = max(dev_float(d, t) for t in ts)
        ratio = m / d
        worst_ratio = max(worst_ratio, ratio)
        print(f"  d={d:<8}  sup dev = {m:.6e}   sup dev/d = {ratio:.6f}")
    print(f"  worst sup(dev/d) = {worst_ratio:.6f}   (bound of Prop 3.1: 4)")

    print("\n=== independent path: mpmath.iv enclosures of dev at a coarse grid ===")
    for d in [0.01, 0.05, 0.49]:
        best = (0.0, 0.0)
        for j in range(400):
            t = -mp.pi + 2 * mp.pi * j / 400
            v = dev_iv(d, t)
            u = float(v.b)                   # rigorous upper bound of the deviation
            if u > best[0]:
                best = (u, float(t))
        print(f"  d={d:<6}  max over grid of the certified upper bound = {best[0]:.6e} "
              f"at t={best[1]:.6f};  dev/d <= {best[0]/d:.6f}")

    print("\n=== the three constants of the analytic proof (Prop 3.1) ===")
    M = 0.0
    for rho in np.linspace(0.5, 1.5, 400001):
        if abs(rho - 1) > 1e-9:
            M = max(M, abs(np.arccos(rho / 2) - KAPPA) / abs(rho - 1))
    print(f"  (iii) sup_{{rho in [1/2,3/2]}} |arccos(rho/2)-kappa|/|rho-1| = {M:.6f}   (used: 0.8)")
    worst2 = 0.0
    worst1 = 0.0
    for d in np.linspace(1e-6, 0.5, 2001):
        ts2 = np.linspace(-np.pi, np.pi, 2001, endpoint=False)
        for t in ts2:
            rho = abs(d + np.exp(1j * t))
            worst2 = max(worst2, abs(rho - 1) / d)
            worst1 = max(worst1, abs(np.angle(1 + d * np.exp(-1j * t))) / d)
    print(f"  (ii)  sup |rho-1|/d            = {worst2:.6f}   (used: 2)")
    print(f"  (i)   sup |arg(1+d e^-it)|/d   = {worst1:.6f}   (used: 2)")
    print(f"\n  => sup dev/d <= (i) + M*(ii) = {worst1:.4f} + {M:.4f}*{worst2:.4f} = "
          f"{worst1 + M * worst2:.4f}  <= 4   OK")


if __name__ == "__main__":
    main()
