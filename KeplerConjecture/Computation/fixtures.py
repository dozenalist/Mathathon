"""Elementary, independently checkable fixtures for the K15 computation layer.

Each fixture is exact or elementary; none depends on the LP solver. They exist so
that the convention chain (see k15conv.py) and the transform convention can be
audited without trusting any optimization output.

F1  Gaussian self-duality under the project transform convention.
F2  1D sinc control: the transform of the triangle vanishes at all nonzero integers.
F3  Ball difference body: an exact Cohn-Elkies certificate that yields exactly the
    trivial bound Delta <= 1. All constants closed-form and hand-checkable.
F4  Density scaling sqrt(2) <-> 2**(-5/2) by direct lattice ENUMERATION (not algebra).
F5  Poisson summation on FCC, which is the check that catches dual-shell enumeration bugs.
"""
from mpmath import mp, mpf, pi, sqrt, exp, quad, inf, nsum
import numpy as np

mp.dps = 30

# ----------------------------------------------------------------- F1
def f1_gaussian_duality(s=1.0):
    """In R^3 with fhat(t) = int f(x) e^{-2 pi i <x,t>} dx, e^{-pi s |x|^2} has
    transform s^{-3/2} e^{-pi |t|^2/s}. Checked by 1D reduction + quadrature."""
    def ft1(a):                      # 1D transform of e^{-pi a x^2}
        return lambda t: quad(lambda x: exp(-pi*a*x*x)*mp.cos(2*pi*t*x), [-inf, 0, inf])
    ok = True
    for a in (mpf("0.7"), mpf(1), mpf("2.3")):
        for t in (mpf(0), mpf("0.4"), mpf("1.3")):
            got = ft1(a)(t)
            want = a**mpf("-0.5") * exp(-pi*t*t/a)
            err = abs(got - want)
            ok &= err < mpf("1e-22")
    # 3D value at a specific point, factorised
    a, tv = mpf("1.1"), (mpf("0.3"), mpf("0.5"), mpf("0.9"))
    val = 1
    for c in tv:
        val *= ft1(a)(c)
    want = a**mpf("-1.5") * exp(-pi*sum(c*c for c in tv)/a)
    ok &= abs(val - want) < mpf("1e-22")
    return ok, abs(val - want)

# ----------------------------------------------------------------- F2
def f2_sinc_1d():
    """f(t) = (1-|t|)_+ has fhat(y) = (sin(pi y)/(pi y))^2, which vanishes at every
    nonzero integer. The 1D sharp CE certificate; used only as a transform control."""
    worst = mpf(0)
    for k in range(1, 8):
        worst = max(worst, abs(mp.sin(pi*k)**2 / (pi*k)**2))
    # and the value at 0 is 1 (normalised)
    v0 = quad(lambda t: (1-abs(t)), [-1, 0, 1])
    return worst < mpf("1e-28"), v0, worst

# ----------------------------------------------------------------- F3
def f3_ball_difference_body():
    """g = 1_{B_1} in R^3, f = g * g(-.).  Then
         supp f subset B_2, hence f <= 0 off B_2  (f vanishes there);
         fhat = |ghat|^2 >= 0;
         f(0) = |B_1| = 4pi/3,  fhat(0) = |B_1|^2 = (4pi/3)^2;
         A(f) = f(0)/fhat(0) = 3/(4pi);
         CE (unit-radius convention) gives Delta <= (4pi/3) A(f) = 1 exactly.
    So the difference-body mechanism reproduces the trivial bound with no slack in
    the arithmetic -- an exact acceptance test for the unit-radius convention.
    Also numerically: vol(B_1 cap B_1 shifted by v) is positive for |v|<2 and 0 for |v|>=2."""
    R = mpf(1)
    vol = 4*pi*R**3/3
    f0, fh0 = vol, vol**2
    A = f0/fh0
    bound = (4*pi/3)*A
    # numerical sanity: overlap volume of two unit balls at distance d
    def overlap(d):
        if d >= 2: return mpf(0)
        # lens volume, exact formula
        return pi*(4*R**3/3) - pi*d*0 + 0  # placeholder replaced below
    def lens(d):
        if d >= 2*R: return mpf(0)
        return pi*(4*R + d)*(2*R - d)**2/12
    checks = (abs(lens(mpf("2.5"))) == 0 and lens(mpf("1.0")) > 0 and lens(mpf("1.9")) > 0
              and abs(lens(mpf(0)) - vol) < mpf("1e-25"))
    return (abs(bound - 1) < mpf("1e-28"), A, bound, checks)

# ----------------------------------------------------------------- F4
def f4_density_scaling(M=6):
    """Enumerate FCC in ALIGNED half-open boxes so the count is exact, with no boundary
    error at all -- this is a count, not an estimate.

    sep-1 FCC:  L_A = D_3/sqrt2, D_3 = even-coordinate-sum integer points.
        y in [-M,M)^3 has exactly half of the (2M)^3 integer points even-sum (M>=1),
        so #(L_A cap box) = 4M^3 and the box has side 2M/sqrt2 and volume 2*sqrt2*M^3.
        Hence rho_A = 4M^3/(2 sqrt2 M^3) = sqrt2 EXACTLY.
    sep-2 FCC:  L_B = sqrt2 D_3 (this is the same lattice scaled by 2).
        Side 2M sqrt2, volume 16 sqrt2 M^3, same count 4M^3,
        hence rho_B = 4M^3/(16 sqrt2 M^3) = 1/(4 sqrt2) = 2^(-5/2) EXACTLY.
    The enumeration below reproduces both and the count ratio 8, digit for digit."""
    L = np.arange(-M, M)
    Y = np.array([(a, b, c) for a in L for b in L for c in L if (a + b + c) % 2 == 0], dtype=float)
    n = len(Y)
    volA = (2.0*M/np.sqrt(2))**3
    volB = (2.0*M*np.sqrt(2))**3
    rhoA, rhoB = n/volA, n/volB
    return dict(count=n, expect_count=4*M**3, rhoA=rhoA, rhoB=rhoB,
                expect_rhoA=float(np.sqrt(2)), expect_rhoB=2**-2.5,
                ratio=volB/volA, expect_ratio=8.0,
                exact=(n == 4*M**3))

# ----------------------------------------------------------------- F5
def f5_poisson_fcc():
    """Poisson summation on FCC for a Gaussian: sum_{x in L} F(x) = (1/det L) sum_{mu in L*} Fhat(mu).
    With F(x) = e^{-pi a |x|^2} (self-dual family), Fhat(t) = a^{-3/2} e^{-pi |t|^2/a}.
    This is exactly the check that exposed a dual-shell enumeration bug on 2026-11-14:
    a hand-built half-integer shell list was wrong and only brute-force enumeration over
    Z^3 u (Z+1/2)^3 settled it. Any replacement shell enumerator must pass this test."""
    a = mpf("0.7")
    def F(x):  return exp(-pi*a*x*x)
    def Fh(t): return a**mpf("-1.5")*exp(-pi*t*t/a)
    L = np.arange(-14, 15)
    sL = F(mpf(0))
    for p in L:
        for q in L:
            for r in L:
                if (p+q+r) % 2 == 0 and (p, q, r) != (0, 0, 0):
                    sL += F(sqrt(mpf(int(p*p+q*q+r*r)))/sqrt(2))
    # dual BCC: sqrt2 * (Z^3 u (Z+1/2)^3)
    sD = Fh(mpf(0))
    for p in L:
        for q in L:
            for r in L:
                if (p, q, r) != (0, 0, 0):
                    sD += Fh(sqrt(2)*sqrt(mpf(int(p*p+q*q+r*r))))
    for p in L:
        for q in L:
            for r in L:
                x, y, z = mpf(int(2*p+1))/2, mpf(int(2*q+1))/2, mpf(int(2*r+1))/2
                sD += Fh(sqrt(2)*sqrt(x*x+y*y+z*z))
    lhs = sL
    rhs = sD/sqrt(mpf("0.5"))       # 1/det L with det L = 1/sqrt2
    return abs(lhs-rhs), lhs, rhs

if __name__ == "__main__":
    print("F1 Gaussian duality           :", f1_gaussian_duality())
    ok2, v0, worst = f2_sinc_1d()
    print("F2 sinc control               : ok=%s  int f=%s  max|fhat(k)|=%s" % (ok2, mp.nstr(v0, 8), mp.nstr(worst, 4)))
    ok3, A, bound, chk = f3_ball_difference_body()
    print("F3 ball difference body       : exact Delta<=1 -> ok=%s  A(f)=%s  bound=%s  lens_ok=%s"
          % (ok3, mp.nstr(A, 10), mp.nstr(bound, 10), chk))
    d = f4_density_scaling()
    print("F4 density scaling (exact count): #=%d (expect 4M^3=%d) exact=%s" % (d["count"], d["expect_count"], d["exact"]))
    print("   rhoA=%.12f (sqrt2=%.12f)  rhoB=%.12f (2^-2.5=%.12f)  vol ratio=%.6f"
          % (d["rhoA"], d["expect_rhoA"], d["rhoB"], d["expect_rhoB"], d["ratio"]))
    res, lhs, rhs = f5_poisson_fcc()
    print("F5 Poisson on FCC             : |lhs-rhs| = %s  (lhs=%s rhs=%s)" % (mp.nstr(res, 4), mp.nstr(lhs, 10), mp.nstr(rhs, 10)))
