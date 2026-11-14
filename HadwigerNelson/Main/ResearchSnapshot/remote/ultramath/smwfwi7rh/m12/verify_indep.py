#!/usr/bin/env python3
"""
verify_indep.py -- SECOND, INDEPENDENT verification of the elimination table.

Different from verify.py in every step:
  * gamma is obtained from  gamma = 2 arcsin(1/(2 sqrt 3))  by the arcsin power
    series in rational interval arithmetic (verify.py bisects cos gamma = 5/6);
  * the palette fields are re-derived from their published descriptions as
    *functions of the angle* and the criterion is decided by scanning t over the
    circle and testing the six membership conditions pointwise (verify.py works
    with exact interval-set algebra and never samples);
  * the witness check evaluates the palette at both endpoints of the gamma
    enclosure, which makes the conclusion independent of the enclosure's width.

Run:  python3 verify_indep.py
"""
from fractions import Fraction as F
import itertools

# --------------------------------------------------- 1. gamma, arcsin series --
def sqrt_bounds(x, iters=400):
    x = F(x); lo = F(int(x)) if int(x) > 0 else F(1, 10**6)
    while lo*lo > x: lo /= 2
    hi = lo + 1
    while hi*hi < x: hi *= 2
    for _ in range(iters):
        m = (lo+hi)/2
        if m*m < x: lo = m
        else: hi = m
    return lo, hi

PI_LO = F(31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679, 10**100)
PI_HI = PI_LO + F(1, 10**98)

def asin_bounds(t_lo, t_hi, n=60):
    """arcsin on [t_lo,t_hi] in [0,1/2]; all series coefficients positive"""
    lo = F(0); hi = F(0)
    for m in range(n+1):
        c = F(1)
        for k in range(m): c = c * F(2*k+1, 2*k+2)
        c = c/(2*m+1)
        lo += c * t_lo**(2*m+1); hi += c * t_hi**(2*m+1)
    c = F(1)
    for k in range(n+1): c = c * F(2*k+1, 2*k+2)
    hi += c/(2*(n+1)+1) * t_hi**(2*(n+1)+1)
    return lo, hi

s3lo, s3hi = sqrt_bounds(3)
t_lo, t_hi = F(1)/(2*s3hi), F(1)/(2*s3lo)
a_lo, a_hi = asin_bounds(t_lo, t_hi)
G_LO = 2*a_lo*180/PI_HI
G_HI = 2*a_hi*180/PI_LO
PSI_LO, PSI_HI = 180+G_LO, 180+G_HI
print("gamma in degrees  (%.15f, %.15f)" % (float(G_LO), float(G_HI)))
print("psi = 180+gamma   (%.15f, %.15f)   width %.2e" % (float(PSI_LO), float(PSI_HI), float(PSI_HI-PSI_LO)))

# ------------------------------------------------ 2. palette fields (exactly) --
BLOCK_TABLES = {
 "m15 uniform blocks, ell=3": [frozenset({0,3}), frozenset({1,4}), frozenset({2,5})],
 "m15 uniform blocks, ell=4": [frozenset({0,2}), frozenset({1,4}), frozenset({3,5})],
 "m15 uniform blocks, ell=5": [frozenset({0,2}), frozenset({1,3}), frozenset({4,5})],
 "m15 uniform blocks, ell=6": [frozenset({0,3}), frozenset({1,4}), frozenset({2,5})],
 "FREE-LABEL, ell=3":         [frozenset({3}),    frozenset({4}),    frozenset({5})],
 "FREE-LABEL, ell=4":         [frozenset({0,2}),  frozenset({1,3}),  frozenset({4})],
 "FREE-LABEL, ell=5":         [frozenset({0,2}),  frozenset({1,3}),  frozenset({5})],
}
FREE_L6 = [[(3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
           [(3,5),(3,5),(2,5),(2,5),(2,4,5),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)],
           [(3,5),(3,5),(2,5),(2,5),(2,4),(2,4),(2,4),(1,4),(1,4),(1,3),(1,3),(1,3)]]

def make_palette_fn(name):
    if name in BLOCK_TABLES:
        tab = BLOCK_TABLES[name]
        def f(ang):
            sect = int(F(ang) % 360 // 10)        # 10-degree sectors
            return tab[(sect // 4) % 3]           # 40-degree blocks, period 120
        return f
    if name == "FREE-LABEL, ell=6":
        w = [frozenset(t) for r in FREE_L6 for t in r]
        def f(ang):
            sect = int(F(ang) % 360 // 10)
            return w[sect % 36]
        return f
    if name == "m13 singleton triangle":
        def f(ang):
            return frozenset({4 + int(F(9)*(F(ang) % 360)/360) % 3})
        return f
    raise KeyError(name)

def values_of(fn):
    return sorted({fn(F(k,2)) for k in range(720)}, key=lambda s:(len(s),sorted(s)))

def witness(fn, A, B, step=1):   # step in units of 1/4 degree
    """scan t; require t,t+120,t+240 all in A-orbit and t+psi+120j in B (or the reverse)"""
    for role in ('A->B','B->A'):
        first, second = (A,B) if role=='A->B' else (B,A)
        for k in range(0, 1440//step):
            t = F(k*step,4)
            if fn(t)!=first or fn(t+120)!=first or fn(t+240)!=first: continue
            ok = True
            for j in (0,1,2):
                # palette at t+psi+120j must be `second` for BOTH endpoints of the psi enclosure
                if fn(t+PSI_LO+120*j)!=second or fn(t+PSI_HI+120*j)!=second:
                    ok=False; break
            if ok: return role, t
    return None

def main():
    print()
    print("%-28s %-4s %-10s %s" % ("model","vals","periodic","status"))
    killed=[]
    for name in list(BLOCK_TABLES)+["FREE-LABEL, ell=6","m13 singleton triangle"]:
        fn = make_palette_fn(name)
        vals = values_of(fn)
        per = all(fn(F(k,4))==fn(F(k,4)+120) for k in range(1440))
        kills=[]
        for A,B in itertools.combinations(vals,2):
            if A & B: continue
            w = witness(fn,A,B)
            if w and 6-len(A|B) < 3: kills.append((sorted(A),sorted(B),w))
        status = "ELIMINATED" if kills else "survives"
        if kills: killed.append(name)
        print("%-28s %-4d %-10s %s" % (name, len(vals), per, status))
        for A,B,w in kills[:2]:
            print("      A=%-9s B=%-9s role %s  t = %.4f deg  T' = %d" % (A,B,w[0],float(w[1]),6-len(set(A)|set(B))))
    print()
    print("eliminated %d of %d ; survivors %s" % (len(killed), 9, [m for m in list(BLOCK_TABLES)+["FREE-LABEL, ell=6","m13 singleton triangle"] if m not in killed]))

    print()
    print("arc-sum disc bound (strictly stronger than the gamma criterion):")
    d = PI_LO/3; val = d*sqrt_bounds(3)[0] - d*d; inv3 = 1/sqrt_bounds(3)[1]
    print("  delta*sigma - delta^2 = %.6f  >=  1/sqrt3 = %.6f : %s" % (float(val), float(inv3), val>=inv3))

if __name__=="__main__":
    main()
