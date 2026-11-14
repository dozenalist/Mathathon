"""
Exact certification that the direction sum set E_A + E_B of two palette values
contains the unit equilateral triangle  T_t = {(t,0),(t+1,0),(t+1/2,sqrt3/2)}.

Membership test (exact characterisation):
   w in E_A + E_B  (E_A,E_B subsets of the unit circle)
   iff |w| <= 2 and one of the (at most two) decompositions
        w = e^{i th} + e^{i ph},   |e^{i th}-e^{i ph}| = |w| ,
   has  th in E_A, ph in E_B  (or th in E_B, ph in E_A).
   Explicit: r=|w|, beta=arccos(r/2); th = arg w +- beta ; ph = arg(w - e^{i th}).
"""
import numpy as np
from mpmath import mp, mpf, mpc, exp, sqrt, cos, sin, pi, acos, arg, fabs
mp.dps = 50

def in_arcs(x, arcs):
    """x in degrees (mpf). arcs: list of (lo,hi) in exact degrees (mpf). Returns (bool, margin_deg)."""
    y = x % 360
    best = mpf(-1)
    for lo,hi in arcs:
        lo=mpf(lo); hi=mpf(hi)
        if lo < y < hi:
            m = min(y-lo, hi-y)
            best = max(best, m)
    return best

def decompose(w):
    """w: mpc. returns list of (th_deg, ph_deg) for the two decompositions (mpf degrees)."""
    r = fabs(w)
    if r > 2:
        return []
    if r < mpf('1e-40'):
        return []
    beta = acos(r/2)
    a = arg(w)
    out=[]
    for s in (+1,-1):
        th = a + s*beta
        ph = arg(w - exp(mpc(0,1)*th))
        out.append((th*180/pi, ph*180/pi))
    return out

def margins(w_re, w_im, arcsA, arcsB, swapped=True):
    """best margin (degrees) over decompositions and label assignment"""
    w = mpc(mpf(w_re), mpf(w_im))
    best = (-1, None)
    for (th,ph) in decompose(w):
        mA = in_arcs(th, arcsA); mB = in_arcs(ph, arcsB)
        if mA>0 and mB>0:
            m = min(mA,mB)
            if m > best[0]: best = (m, ('AB', float(th), float(ph), float(mA), float(mB)))
        if swapped:
            mA2 = in_arcs(th, arcsB); mB2 = in_arcs(ph, arcsA)
            if mA2>0 and mB2>0:
                m = min(mA2,mB2)
                if m > best[0]: best = (m, ('BA', float(th), float(ph), float(mA2), float(mB2)))
    return best

def triangle_margins(t, arcsA, arcsB):
    """T_t unit triangle; return list of per-vertex best margins"""
    t = mpf(t)
    s3 = sqrt(3)/2
    V = [(t, mpf(0)), (t+1, mpf(0)), (t+mpf(1)/2, s3)]
    return [margins(a,b,arcsA,arcsB) for (a,b) in V]

if __name__=="__main__":
    import sys
    sys.path.insert(0,'work')
    from models import words, dirset
    W=words()
    trials = {
      "block_l6": ([(0,40),(120,160),(240,280)], [(40,80),(160,200),(280,320)]),
      "block_l3": ([(0,40),(120,160),(240,280)], [(40,80),(160,200),(280,320)]),
      "block_l4": ([(0,40),(120,160),(240,280)], [(40,80),(160,200),(280,320)]),
      "block_l5": ([(0,40),(120,160),(240,280)], [(40,80),(160,200),(280,320)]),
      "free_l6_35_24": ([(0,20),(120,140),(240,260)], [(40,70),(160,190),(280,310)]),
      "free_l6_25_14": ([(20,40),(140,160),(260,280)], [(70,100),(190,220),(310,340)]),
    }
    for key,(A,B) in trials.items():
        print("="*70); print(key)
        best=None
        for tnum in range(-200,201):
            t = mpf(tnum)/100
            ms = triangle_margins(t, [(mpf(a),mpf(b)) for a,b in A], [(mpf(a),mpf(b)) for a,b in B])
            if all(m[0]>0 for m in ms):
                score=min(m[0] for m in ms)
                if best is None or score>best[0]: best=(score,t,ms)
        if best:
            print("  best rational t =",best[1], "min margin deg = %.3f"%best[0])
            for m in best[2]: print("   ",m[1])
        else:
            print("  no rational t on the 1/100 grid works")
