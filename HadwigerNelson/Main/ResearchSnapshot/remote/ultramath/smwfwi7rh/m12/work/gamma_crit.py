"""
Exact gamma-criterion (Lemma 6.4 mechanism, applied with both label roles).

Given two disjoint palette groups  A  (values on direction set E_A) and B (on E_B),
the paper's triangle  z_j - x = e^{i(t+2j*kappa)} (1 - e^{i gamma}),  cos gamma = 5/6,
has  z_j - x = e^{i(t+2j kappa)} + e^{i(t+pi+gamma+2j kappa)}  and pairwise distances
|z_j - z_{j+1}| = sqrt3 * |1-e^{i gamma}| = 1  exactly.
So if  {t, t+120, t+240}  lies in a *closed* sub-arc of E_B  and
      {t+pi+gamma, +120, +240}  in E_A   (or the roles swapped),
then T' = I \\ (A u B) has >= 3 labels.

All angles in degrees.  gamma is bounded rigorously by rational interval arithmetic
(Taylor series of cos with explicit remainder).
"""
from fractions import Fraction as F

# ---- rigorous bounds for gamma = arccos(5/6), in degrees -------------------
def cos_series(x, n=12):
    """cos(x) for Fraction x, with rigorous enclosures (returns (lo,hi))."""
    x = F(x); lo = F(0); hi = F(0); term = F(1)
    for k in range(n+1):
        # term = x^(2k)/(2k)!
        t = term
        if k % 2 == 0: lo += t; hi += t
        else:          lo -= t; hi -= t
        term = term * x * x / ((2*k+1)*(2*k+2))
    # next term has the sign of (-1)^(n+1); bound its size
    rem_lo = -term if (n+1) % 2 == 1 else F(0)
    rem_hi = F(0) if (n+1) % 2 == 1 else term
    if (n+1) % 2 == 1:   # cos is decreasing? use monotone bracket: lo-|term| .. hi+|term|
        return lo - term, hi + term
    else:
        return lo - term, hi + term

def gamma_bounds_deg():
    """return rational (g_lo, g_hi) in degrees with g_lo < gamma_deg < g_hi"""
    # bisection on radian value with rigorous cos enclosure
    lo, hi = F(58,100), F(60,100)          # radians, cos decreasing on [0,pi]
    for _ in range(120):
        mid = (lo+hi)/2
        c_lo, c_hi = cos_series(mid)
        if c_lo > F(5,6):      # cos(mid) > 5/6  => mid < gamma
            lo = mid
        elif c_hi < F(5,6):    # cos(mid) < 5/6  => mid > gamma
            hi = mid
        else:
            break
    # convert to degrees with rational bounds on pi
    PI_LO, PI_HI = F(31415926535897932384626433832795028841971, 10**40), F(3141592653589793238462643383279502884198, 10**39)
    PI_LO = F(314159265358979323846264338327950288419716939937510, 10**50)
    PI_HI = PI_LO + F(1,10**49)
    deg = lambda r, up: r*180/(PI_HI if up else PI_LO)
    return deg(lo, False), deg(hi, True)

G_LO, G_HI = gamma_bounds_deg()
PSI_LO = 180 + G_LO      # psi = 180 + gamma   (degrees)
PSI_HI = 180 + G_HI
print("gamma in degrees: (%.10f, %.10f)" % (float(G_LO), float(G_HI)))
print("psi = pi+gamma  : (%.10f, %.10f)" % (float(PSI_LO)%360, float(PSI_HI)%360))

# ---- interval helpers on the circle of circumference 120 (mod 120) ---------
def norm120(a):  # a Fraction -> [0,120)
    a = F(a) % 120
    return a

def intervals_mod120(arcs):
    """arcs: list of (lo,hi) degree intervals (Fractions). Return union modulo 120."""
    out=[]
    for lo,hi in arcs:
        lo=F(lo); hi=F(hi)
        a=lo%120; length=hi-lo
        while length > 0:
            take=min(F(120)-a, length)
            out.append((a, a+take)); length -= take; a=0
    return merge(out)

def merge(iv):
    iv=sorted(iv); out=[]
    for lo,hi in iv:
        if out and lo <= out[-1][1]:
            out[-1]=(out[-1][0], max(out[-1][1], hi))
        else: out.append((lo,hi))
    return out

def intersect(A,B):
    out=[]
    for a1,a2 in A:
        for b1,b2 in B:
            lo=max(a1,b1); hi=min(a2,b2)
            if hi>lo: out.append((lo,hi))
    return merge(out)

def width(iv): return sum((hi-lo) for lo,hi in iv)

def shift_mod120(iv, s_lo, s_hi):
    """(iv - [s_lo,s_hi]) mod 120 ; returns a superset-safe pair: interval arithmetic.
       We return the union over s in [s_lo,s_hi] of (iv - s) mod 120, as a merged list."""
    out=[]
    for lo,hi in iv:
        a=(lo-s_hi)%120; b=(hi-s_lo)%120
        # (iv - s) for s in [s_lo,s_hi] sweeps [lo-s_hi, hi-s_lo]
        length=(hi-s_lo)-(lo-s_hi)
        if length>=120: return [(F(0),F(120))]
        x=a
        while length>0:
            take=min(F(120)-x, length)
            out.append((x,x+take)); length-=take; x=F(0)
    return merge(out)

def gamma_kill(EA, EB, margin=0):
    """EA,EB: arc lists (degrees, Fractions) of the two disjoint value sets.
       returns (bool, witness interval list, role)"""
    A=intervals_mod120(EA)
    # role 1: t in EA, t+psi in EB
    Bshift = shift_mod120(intervals_mod120(EB), PSI_LO, PSI_HI)
    hit1 = intersect(A, Bshift)
    # role 2: t in EB, t+psi in EA
    Ashift = shift_mod120(A, PSI_LO, PSI_HI)
    hit2 = intersect(intervals_mod120(EB), Ashift)
    return hit1, hit2
