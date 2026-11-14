"""Exact geometry of the two unit decompositions of Lemma 5.2(3).

For centres x0 and z = x0 + a with |a| = d in (0,2) and a unit direction f at z:
    w = a + f,  |w| = r,  c = r/2  (<=1 by |a| <= 2 ... note r <= 2 needs d <= 1 or f not antiparallel)
    s_pm(f) = w/2 +- i*(w/r)*sqrt(1-c^2),  t_pm = w - s_pm,  |s|=|t|=1.
Lemma 5.2(3) then gives  P_z(f) cap P_{x0}(s_pm(f)) = empty  a.e.
The *shift* is  arg(s_pm / f).
"""
import cmath, math

def shifts(d, psi):
    """a = d (real), f = exp(i psi).  Returns list of (branch, s, t, shift)."""
    a = complex(d, 0.0)
    f = cmath.exp(1j*psi)
    w = a + f
    r = abs(w)
    if r < 1e-15:
        return []
    c = r/2.0
    if c > 1 + 1e-12:
        return []           # no unit decomposition (|w| > 2)
    c = min(c, 1.0)
    h = math.sqrt(max(0.0, 1.0 - c*c))
    what = w/r
    out = []
    for sgn in (+1, -1):
        s = w/2.0 + sgn*1j*what*h
        t = w - s
        out.append((sgn, s, t, math.atan2(s.imag, s.real) - math.atan2(f.imag, f.real)))
    return out

def wrap(x):
    x = math.remainder(x, 2*math.pi)
    return x

if __name__ == "__main__":
    for d in [0.0, 0.05, 0.1, 0.2, 0.4, 0.5, 0.6, 0.732, 0.8, 0.9, 1.0, 1.2, 1.5, 1.9]:
        vals = []
        for pos in range(0, 2001):
            psi = -math.pi + 2*math.pi*pos/2000
            for sgn, s, t, sh in shifts(d, psi):
                vals.append((sgn, wrap(sh)))
        sp = [v for sgn, v in vals if sgn > 0]
        sm = [v for sgn, v in vals if sgn < 0]
        print(f"d={d:5.3f}  shift+ in [{min(sp):+.4f},{max(sp):+.4f}]  shift- in [{min(sm):+.4f},{max(sm):+.4f}]   (pi/3={math.pi/3:.4f})")
