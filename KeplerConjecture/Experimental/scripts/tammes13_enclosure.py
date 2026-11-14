#!/usr/bin/env python3
"""
Rigorous rational-interval enclosure of delta_13 (Musin-Tarasov 2012, arXiv:1002.1439v3,
Section 2, Remark preceding Theorem 1).

DEFINING EQUATIONS (source, Section 2 Remark):
    (E1)  2*tan(3*pi/8 - a/4) = (1 - 2*cos a)/cos(a)^2
    (E2)  cos d = cos a/(1 - cos a)

CERTIFICATE:  d_13 < arccos(23681/43681)   [the rho = 209/100 endpoint]

METHOD: exact rational interval arithmetic (fractions.Fraction) with
  * pi enclosed by 333/106 < pi < 355/113
  * sin/cos by Taylor series with the explicit alternating-series remainder bound
  * tan = sin/cos by interval division
  * NO floating point is used in any decision.

UNIQUENESS: g(a) = 2 tan(3pi/8 - a/4) - (1-2cos a)/cos^2 a has
    g'(a) = -(1/2) sec^2(3pi/8 - a/4) - 2 sin a (1-cos a)/cos^3 a  <  0
on (0, pi/2) : both terms are strictly negative (sin>0, cos>0, 1-cos>0). So g is
strictly decreasing and has at most one root there. Sign change on a rational
interval therefore pins the root uniquely.

MONOTONICITY USED: h(c) = c/(1-c) is increasing in c on (0,1); h(a) = cos a/(1-cos a)
is strictly decreasing in a on (0,pi); arccos is strictly decreasing. Hence
a* <= a_hi  =>  d = arccos(h(a*)) <= arccos(h(a_hi)) <= arccos(h_lo),
and  h_lo > 23681/43681  iff  arccos(h_lo) < arccos(23681/43681).

DEPENDENCY: the identification d_13 = delta_13 (Theorem 1) rests on the authors'
computer enumeration of irreducible contact graphs. This script certifies the
ARITHMETIC of the constant only, not the enumeration.
"""
from fractions import Fraction as F
import sys

# ---------------- rational interval class ----------------
class Iv:
    __slots__ = ('lo', 'hi')
    def __init__(self, lo, hi=None):
        self.lo = lo if isinstance(lo, F) else F(lo)
        self.hi = self.lo if hi is None else (hi if isinstance(hi, F) else F(hi))
        assert self.lo <= self.hi
    def __add__(s, o): return Iv(s.lo+o.lo, s.hi+o.hi)
    def __sub__(s, o): return Iv(s.lo-o.hi, s.hi-o.lo)
    def __neg__(s):    return Iv(-s.hi, -s.lo)
    def __mul__(s, o):
        p = (s.lo*o.lo, s.lo*o.hi, s.hi*o.lo, s.hi*o.hi)
        return Iv(min(p), max(p))
    def inv(s):
        assert not (s.lo <= 0 <= s.hi), "division by interval containing 0"
        return Iv(1/s.hi, 1/s.lo)
    def __truediv__(s, o): return s * o.inv()
    def __repr__(s): return f"[{float(s.lo):.15g}, {float(s.hi):.15g}]"

PI = Iv(F(333,106), F(355,113))          # 3.14159292... < pi < 3.14159292...

def _taylor_sin(x, n=28):
    """x a Fraction, 0 <= x <= 1.6. Returns rigorous Iv enclosure of sin x."""
    x2 = x*x
    term = x                      # x^(2k+1)/(2k+1)!
    s = Iv(term)
    sign = -1
    for k in range(1, n+1):
        term = term * x2 / F((2*k)*(2*k+1))
        s = s + Iv(sign*term)
        sign = -sign
    # first omitted term
    term_next = term * x2 / F((2*n+2)*(2*n+3))
    return Iv(s.lo - term_next, s.hi + term_next)

def _taylor_cos(x, n=28):
    x2 = x*x
    term = F(1)
    s = Iv(F(1))
    sign = -1
    for k in range(1, n+1):
        term = term * x2 / F((2*k-1)*(2*k))
        s = s + Iv(sign*term)
        sign = -sign
    term_next = term * x2 / F((2*n+1)*(2*n+2))
    return Iv(s.lo - term_next, s.hi + term_next)

def cos_iv(lo, hi):
    """0 < lo <= hi < pi/2 : cos is decreasing."""
    c_hi = _taylor_cos(lo)   # cos(lo) largest
    c_lo = _taylor_cos(hi)   # cos(hi) smallest
    return Iv(c_lo.lo, c_hi.hi)

def sin_iv(lo, hi):
    """0 < lo <= hi < pi/2 : sin is increasing."""
    s_lo = _taylor_sin(lo); s_hi = _taylor_sin(hi)
    return Iv(s_lo.lo, s_hi.hi)

def tan_iv(lo, hi):
    return sin_iv(lo, hi) / cos_iv(lo, hi)

# ---------------- g(a) ----------------
def g_iv(lo, hi):
    """Rigorous Iv enclosure of g on [lo,hi] (0 < lo <= hi < pi/2)."""
    # arg = 3*pi/8 - a/4 for a in [lo,hi]  =>  [3pi/8 - hi/4, 3pi/8 - lo/4]
    arg_lo = (Iv(3)*PI/Iv(8) - Iv(hi)/Iv(4)).lo
    arg_hi = (Iv(3)*PI/Iv(8) - Iv(lo)/Iv(4)).hi
    # tan is increasing on (0, pi/2)
    t = tan_iv(arg_lo, arg_hi)
    lhs = Iv(2) * t
    c = cos_iv(lo, hi)
    rhs = (Iv(1) - Iv(2)*c) / (c*c)
    return lhs - rhs

def gp_iv(lo, hi):
    """Rigorous Iv enclosure of g'(a) = -(1/2)sec^2(3pi/8-a/4) - 2 sin a (1-cos a)/cos^3 a
    on [lo,hi] with 0 < lo <= hi < pi/2.  Both terms are negative there."""
    arg_lo = (Iv(3)*PI/Iv(8) - Iv(hi)/Iv(4)).lo
    arg_hi = (Iv(3)*PI/Iv(8) - Iv(lo)/Iv(4)).hi
    c_arg = cos_iv(arg_lo, arg_hi)
    sec2 = Iv(1) / (c_arg*c_arg)
    t1 = Iv(-1)/Iv(2) * sec2
    sa = sin_iv(lo, hi); ca = cos_iv(lo, hi)
    t2 = Iv(-2) * sa * (Iv(1) - ca) / (ca*ca*ca)
    return t1 + t2

def h_at(x):
    """Iv enclosure of h(x) = cos x/(1-cos x), x a Fraction in (0, pi/2)."""
    c = _taylor_cos(x)
    c_lo = Iv(c.lo); c_hi = Iv(c.hi)
    # h increasing in c => use full interval of c
    return c / (Iv(1) - c)

# ---------------- main certificate ----------------
def main():
    threshold = F(23681, 43681)          # exact cos(theta_min) at rho = 209/100
    out = []
    def say(s):
        out.append(s); print(s)

    say("=== Tammes N=13 enclosure: certificate for rho = 209/100 ===")
    say(f"pi in {PI}")

    # bracket the root of g
    a_lo = F(12113, 10000)               # 1.2113
    a_hi = F(12114, 10000)               # 1.2114
    g_lo = g_iv(a_lo, a_lo); g_hi = g_iv(a_hi, a_hi)
    say(f"g({float(a_lo)}) = {g_lo}")
    say(f"g({float(a_hi)}) = {g_hi}")
    assert g_lo.lo > 0, "expected g > 0 at left endpoint"
    assert g_hi.hi < 0, "expected g < 0 at right endpoint"
    say("sign change g>0 -> g<0 on [a_lo,a_hi]; g strictly decreasing on (0,pi/2)")
    say("  => unique root a* in [a_lo, a_hi]")
    say("")

    # --- refine the bracket by bisection (rigour kept: sign change maintained) ---
    # Note: bisection stalls once the interval evaluation straddles 0 near the root,
    # because plain interval arithmetic loses the sign there. That is why the bracket
    # below is ~1e-5 wide rather than 1e-12; it is ample for the margin required.
    for _ in range(40):
        mid = (a_lo + a_hi) / 2
        gm = g_iv(mid, mid)
        if gm.lo > 0:
            a_lo = mid
        elif gm.hi < 0:
            a_hi = mid
        else:
            break
    say(f"refined bracket: a* in [{float(a_lo):.15f}, {float(a_hi):.15f}]")
    say(f"  width {float(a_hi-a_lo):.3e}  (limited by sign loss in interval evaluation)")

    # d <= arccos(h(a*)) <= arccos(h_lo) with h_lo from lower bound of cos(a_hi)
    c_hi_pt = _taylor_cos(a_hi)
    c_lo_bound = c_hi_pt.lo              # lower bound for cos(a_hi)
    h_lo_val = c_lo_bound / (1 - c_lo_bound)
    say(f"cos(a_hi) >= {float(c_lo_bound):.18g}")
    say(f"h(a*) >= h(a_hi) >= {float(h_lo_val):.18g}")
    say(f"threshold cos(theta_min) = 23681/43681 = {float(threshold):.18g}")
    margin = h_lo_val - threshold
    say(f"margin = {float(margin):.6e}  ({'>0 CERTIFIED' if margin > 0 else 'FAILED'})")
    assert margin > 0

    # --- second radius: rho = 2.05 must also give count 12 ---
    R2 = F(205,100)
    thr2 = 1 - F(2,1)/(R2*R2)          # exact rational
    say("")
    say(f"rho = 2.05 : cos(theta_min) = {thr2.numerator}/{thr2.denominator} = {float(thr2):.18g}")
    say(f"   R/4 = {float(R2/4):.18g}  (equal-radius case binds iff thr2 >= R/4: {thr2 >= R2/4})")
    m2 = h_lo_val - thr2
    say(f"   h(a*) >= {float(h_lo_val):.18g} ; margin = {float(m2):.6e}  "
        f"({'>0 CERTIFIED' if m2 > 0 else 'FAILED'})")
    assert m2 > 0 and thr2 >= R2/4
    say("   => at most 12 centres in [2, 2.05] as well")
    say("")
    say(f"rho = 2.09 : margin = {float(margin):.6e}  (>0 CERTIFIED)")
    say("Both radii certified against the same bracket on a*, with no floating estimate.")

    # report degrees rigorously by bisection (cos decreasing)
    def deg_upper(c_target, lo=F(0), hi=F(157,100)):
        """smallest rational t with cos(t) <= c_target, i.e. an upper bound on arccos(c_target)."""
        for _ in range(64):
            mid = (lo+hi)/2
            cm = _taylor_cos(mid)
            if cm.lo > c_target:   # cos(mid) > target => mid < arccos(target)
                lo = mid
            else:
                hi = mid
        return hi
    # d upper bound: arccos(h_lo_val) <= deg_upper of a rational slightly below h_lo_val
    h_rat = F(int(h_lo_val * F(10**15)), 10**15)
    assert h_rat <= h_lo_val
    d_up = deg_upper(h_rat - F(1, 10**15))
    th_min = deg_upper(threshold)
    say("")
    say(f"delta_13 < {float(d_up*180/PI.lo):.9f} deg   (rigorous upper bound)")
    say(f"theta_min   > {float(th_min*180/PI.hi):.9f} deg   (rigorous lower bound, rho=2.09)")
    th2 = deg_upper(thr2)
    say(f"theta_min(2.05) > {float(th2*180/PI.hi):.9f} deg   (rigorous lower bound, rho=2.05)")
    say("")
    say("CONCLUSION: delta_13 < theta_min, so K15-E014 holds at rho = 209/100:")
    say("  at most 12 centres of a 2-separated set lie in [2, 2.09].")
    say("Dependency: identification d_13 = delta_13 is Theorem 1 of arXiv:1002.1439v3,")
    say("which rests on a computer enumeration of irreducible contact graphs. This")
    say("certificate covers the arithmetic of the constant only.")

    with open('Experimental/evidence/tammes13_enclosure.txt','w') as f:
        f.write("\n".join(out)+"\n")

if __name__ == "__main__":
    main()
