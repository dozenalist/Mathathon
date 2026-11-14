"""The shift set of Lemma 5.2(3) at centre separation d.

For centres x0 and z=x0+a, |a|=d, and unit direction f at z, the two exact unit
decompositions of w=a+f give s_pm with  s_pm + t_pm = a+f.  Lemma 5.2(3) gives
   P_z(f) cap P_{x0}(s_pm(f)) = empty   a.e.,
provided s_pm is a local angular diffeomorphism and s_pm not parallel t_pm.
Write shift = arg(s_pm) - arg(f).  A centre-independent (frozen) palette field P
satisfies this iff  P(f) cap P(f+shift) = empty  for a.e. f.
"""
import cmath, math

def branches(d, psi, h=1e-7):
    a = complex(d, 0.0); f = cmath.exp(1j*psi); w = a+f; r = abs(w)
    if r < 1e-13 or r > 2+1e-13:
        return []
    c = min(r/2.0, 1.0); q = math.sqrt(max(0.0, 1-c*c)); what = w/r
    out = []
    for sgn in (1, -1):
        s = w/2 + sgn*1j*what*q; t = w-s
        def argsh(ps):
            ww = a+cmath.exp(1j*ps)
            if abs(ww) < 1e-13 or abs(ww) > 2+1e-13:
                return None
            cc = min(abs(ww)/2, 1.0); qq = math.sqrt(max(0.0, 1-cc*cc))
            ss = ww/2 + sgn*1j*(ww/abs(ww))*qq
            return math.atan2(ss.imag, ss.real)
        ap, am = argsh(psi+h), argsh(psi-h)
        der = None if (ap is None or am is None) else math.remainder(ap-am, 2*math.pi)/(2*h)
        par = abs(s.imag*t.real - s.real*t.imag)
        out.append(dict(sgn=sgn, s=s, t=t,
                        shift=math.remainder(math.atan2(s.imag, s.real)-psi, 2*math.pi),
                        deriv=der, sxt=par))
    return out

def admissible(d, psi, deriv_tol=1e-4, par_tol=1e-6):
    res = []
    for b in branches(d, psi):
        if b['sxt'] < par_tol:
            continue
        if b['deriv'] is None or abs(b['deriv']) < deriv_tol:
            continue
        res.append(b)
    return res

def shift_interval(d, N=2000):
    vals = []
    for i in range(N):
        psi = -math.pi + 2*math.pi*i/N
        for b in admissible(d, psi):
            vals.append(b['shift'])
    pos = [v for v in vals if v > 0]; neg = [v for v in vals if v < 0]
    return (min(pos) if pos else None, max(pos) if pos else None,
            min(neg) if neg else None, max(neg) if neg else None)

if __name__ == "__main__":
    print(" d      min+      max+      min-      max-     |  3*min+ vs max+")
    for d in [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.55, 0.6, 0.65, 0.7, 0.732, 0.8, 0.9, 1.0]:
        lo, hi, nlo, nhi = shift_interval(d)
        if lo is None:
            print(f"d={d:.3f}  no admissible branches"); continue
        print(f"d={d:5.3f}  {lo:.5f}  {hi:.5f}  {nlo:.5f}  {nhi:.5f}   | {3*lo:.5f} vs {hi:.5f}  ratio_ok={3*lo<=hi}")
