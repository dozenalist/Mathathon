"""Closed form of the two endpoint shifts of Lemma 5.2(3), and the frozen obstruction.

For centres x0 and z = x0 + a with |a| = d, and a unit direction f at z, put
     w = a + f,  r = |w|,  c = r/2.
The two exact unit decompositions of w are s_pm = w/2 +- i (w/r) sqrt(1-c^2),
t_pm = w - s_pm, with |s_pm| = |t_pm| = 1.  Lemma 5.2(3) then gives
     P_z(f) cap P_{x0}(s_pm(f)) = empty    for a.e. f,
whenever s_pm is a local angular diffeomorphism and s_pm is not parallel t_pm.
With a = d real and f = e^{i psi}:
     arg s_pm = arg w +- arccos(r/2),       so the SHIFT is  arg s_pm - psi.
For a CENTRE-INDEPENDENT (frozen) field P the axiom reads
     P(f) cap P(f + shift) = empty   for a.e. f.
"""
import math

def shift(d, psi, sgn):
    """branch sgn=+1 is s_+ = w/2 + i w^ sqrt(1-c^2)."""
    w = complex(d + math.cos(psi), math.sin(psi))
    r = abs(w)
    if r < 1e-14 or r > 2 + 1e-13:
        return None
    argw = math.atan2(w.imag, w.real)
    c = min(r/2, 1.0)
    g = math.acos(c)
    return math.remainder(argw + sgn*g - psi, 2*math.pi)

def deriv(d, psi, sgn, h=1e-7):
    a = shift(d, psi+h, sgn); b = shift(d, psi-h, sgn)
    if a is None or b is None: return None
    return math.remainder(a-b, 2*math.pi)/(2*h)

def shift_interval(d, N=20000):
    lo = hi = None
    for i in range(N):
        psi = -math.pi + 2*math.pi*i/N
        for sgn in (+1,-1):
            s = shift(d,psi,sgn); dv = deriv(d,psi,sgn)
            if s is None or dv is None: continue
            # local-diffeomorphism condition is on arg s = psi + shift, i.e.
            # |d(arg s)/d psi| = |1 + d shift/d psi| must stay away from 0.
            if abs(1 + dv) < 1e-6:
                continue
            if s > 0:
                lo = s if lo is None else min(lo,s)
                hi = s if hi is None else max(hi,s)
    return lo, hi

if __name__ == "__main__":
    print("d      delta_min(+)  M(+)     3*delta_min   M-3*delta_min")
    for d in [0.0,0.1,0.2,0.3,0.4,0.45,0.47,0.4713,0.472,0.475,0.48,0.5,0.55,0.6]:
        lo,hi = shift_interval(d, 4000)
        print(f"{d:6.4f}  {lo:.6f}   {hi:.6f}   {3*lo:.6f}   {hi-3*lo:+.6f}")
