"""Independent high-precision check of the two extreme shifts.

Second, independent procedure: closed form with mpmath at 40 digits plus a local
ternary search on each branch, rather than the coarse scan of frozen.py.
    shift_+-(psi) = atan2(sin psi, d + cos psi) +- arccos(r/2) - psi,   r = |d + e^{i psi}|.
"""
import mpmath as mp
mp.mp.dps = 40

def sh(d, psi, sgn):
    d = mp.mpf(d); psi = mp.mpf(psi)
    w = d + mp.e**(1j*psi)
    r = abs(w)
    if r <= 0 or r > 2: return None
    argw = mp.arg(w)
    g = mp.acos(r/2)
    v = argw + sgn*g - psi
    v = v - 2*mp.pi*mp.floor(v/(2*mp.pi) + mp.mpf(1)/2)
    return v

def extrema(d, sgn=+1):
    lo = hi = None
    N = 720
    vals = []
    for i in range(N):
        psi = -mp.pi + 2*mp.pi*i/N
        v = sh(d, psi, sgn)
        if v is None: continue
        vals.append((psi, v))
    vals = [t for t in vals if t[1] > 0]
    if not vals: return None
    imin = min(range(len(vals)), key=lambda i: vals[i][1])
    imax = max(range(len(vals)), key=lambda i: vals[i][1])
    def refine(idx):
        a = vals[(idx-1) % len(vals)][0]; b = vals[(idx+1) % len(vals)][0]
        f = lambda t: sh(d, t, sgn)
        if a > b: a, b = b, a
        best = (vals[idx][0], vals[idx][1])
        for _ in range(200):
            m1 = a + (b-a)/3; m2 = b - (b-a)/3
            f1, f2 = f(m1), f(m2)
            if f1 is None or f2 is None: break
            if idx == imin:
                if f1 < f2: b = m2
                else:       a = m1
            else:
                if f1 > f2: b = m2
                else:       a = m1
        t = (a+b)/2
        return (t, f(t))
    return refine(imin), refine(imax)

for d in ["0.175","0.3044","0.305","0.46","0.4609","0.47","0.5","1"]:
    r = extrema(d)
    if r is None: print(d, "none"); continue
    (tmin,vmin),(tmax,vmax) = r
    print(f"d={d:8s}  delta_min={mp.nstr(vmin,12):>16s} at psi={mp.nstr(tmin,10):>14s}"
          f"   M={mp.nstr(vmax,12):>16s} at psi={mp.nstr(tmax,10):>14s}"
          f"   M-2dmin={mp.nstr(vmax-2*vmin,8)}")
