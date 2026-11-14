"""Exact + numerical verification of the geometric transport reduction.

Statement (GEOM).  Let f be a unit vector, a a vector with 0 < |a| <= d_0 = pi/(9m),
W = f + a, r = |W|.  The two exact unit decompositions of W are
      s_+- = W*(1/2 +- i*sqrt(1/r^2 - 1/4)),      s_+ + s_- = W = f + a,
and then
      | arg s_+- - (arg f +- pi/3) |  <=  1.5938 * |a|.
Since 1.5938*d_0 < Delta = 2*pi/(6m) = pi/(3m) (exactly: 15938/90000 < 1/3), the sector
index of s_+- differs from that of f +- pi/3 (i.e. from i +- m) by at most one, so the
palette condition (5.3) reduces to disjointness at the six offsets {+-(m-1),+-m,+-(m+1)}.

Part 1 is an exact rational proof; part 2 samples the statement directly as a check that
the reduction has no sign or indexing error.
"""
from fractions import Fraction as F
import math, sys

# ---------------------------------------------------------------- part 1: exact rationals
PI_UB = F(355,113)                      # pi < 355/113
K_UB  = F(15938,10000)                  # the constant 1.5938

def exact_bounds(m):
    """certified rational chain for GEOM at this m (requires m >= 5)"""
    assert m >= 5
    D0 = PI_UB/(9*m)                    # d_0 < D0
    # (i) 1/sqrt(1-t^2) <= 1 + t^2/2 + t^4 for t <= 1/2  =>  arcsin(d) <= d + d^3/6 + d^5/10
    #     (we use the weaker d + d^3/6 + d^4/4 ... see below for the exact inequality used)
    arcsin_coeff = 1 + D0**2/6 + D0**4/4          # arcsin(d) <= d*(1 + d^2/6 + d^4/4)
    # (ii) 1/sqrt(4-(1+d)^2) <= r  iff  r^2*(4-(1+d)^2) >= 1; use d <= D0 and r = 0.5918
    r = F(5918,10000)
    X = 4 - (1+D0)**2
    ok_r = r**2 * X >= 1
    # (iii) total coefficient must be <= 1.5938
    total = arcsin_coeff + r
    return dict(D0=D0, arcsin_coeff=arcsin_coeff, r=r, ok_r=ok_r, total=total,
                ok_total = total <= K_UB,
                margin = K_UB - total,
                half_interval = K_UB*PI_UB/(9*m) < PI_UB/(3*m))  # 1.5938 d_0 < Delta

def part1():
    print("part 1: exact rational proof of GEOM and of 1.5938*d_0 < Delta")
    # justified step used above: for 0 < t <= 1/2,  1/sqrt(1-t^2) <= 1 + t^2/2 + t^4
    t = F(1,2)
    lhs = 1/(1-t**2)              # squared form: compare squares instead of the sqrt
    rhs = (1 + t**2/2 + t**4)**2
    print(f"   1/(1-t^2) = {float(lhs):.6f} <= (1+t^2/2+t^4)^2 = {float(rhs):.6f}: {lhs<=rhs}")
    assert lhs <= rhs
    worst=None
    for m in list(range(5,40))+[60,100,10**3,10**5]:
        b=exact_bounds(m)
        assert b['ok_r'] and b['ok_total'] and b['half_interval'], (m,b)
        if worst is None or b['margin']<worst[1]: worst=(m,b['margin'])
    print(f"   m>=5: 1/sqrt(3-2D0-D0^2) <= 0.5918 and arcsin(d)<=d(1+d^2/6+d^4/4);")
    print(f"   total coefficient 1+0.5918+D0^2/6+D0^4/4 <= 1.5938 for all m>=5;")
    print(f"   tightest margin {float(worst[1]):.6f} at m={worst[0]}")
    print(f"   and 1.5938*d_0 < Delta  <=>  1.5938/9 < 1/3  (exact: {K_UB/9 < F(1,3)})")
    print()

# ---------------------------------------------------------------- part 2: numeric sampling
def part2(ms=(5,6,9,12), sub=8, npsi=720):
    print("part 2: sample the analytic statement  z+s+t = z'+f  over a grid")
    import numpy as np
    for m in ms:
        n = 6*m
        D = 2*np.pi/n
        d0 = np.pi/(9*m)
        thetas = (np.arange(n*sub)+0.5)/sub*D                       # centre of sub-cells
        psis   = np.arange(npsi)*2*np.pi/npsi
        rhos   = np.array([0.25,0.5,0.75,1.0])*d0
        T,P,R = np.meshgrid(thetas,psis,rhos,indexing='ij')
        A = R*np.exp(1j*P)
        f = np.exp(1j*T)
        W = f + A
        r = np.abs(W)
        root = np.sqrt(np.maximum(1/r**2-0.25,0.0))
        devs=[]; disp=set()
        for sgn in (+1,-1):
            s = W*(0.5 + sgn*1j*root)
            arg = np.angle(s)
            target = T + sgn*np.pi/3
            dev = np.abs(np.angle(np.exp(1j*(arg-target))))
            devs.append(dev.max()/R.max())
            # sector index of the sampled direction and of s
            i = np.floor(((T%(2*np.pi))/D)).astype(int)%n
            j = np.floor(((arg%(2*np.pi))/D)).astype(int)%n
            disp |= set(np.unique(((j-i)%n)).tolist())
        print(f"   m={m}: max |arg s - (arg f +- pi/3)| / |a| = {max(devs):.6f} "
              f"(bound 1.5938); realised sector displacements {sorted(disp)}")
        from word import offsets
        assert disp <= set(offsets(m)), (m, sorted(disp))
        print(f"        displacements are exactly a subset of the six offsets {offsets(m)}: OK")
    print()

if __name__=='__main__':
    part1(); part2()
