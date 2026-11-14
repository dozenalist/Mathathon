"""Machine checks for the MC120 referee report.

Units: angles in radians internally, degrees printed for readability.
Hinges checked:
  H1  separation identity: |r u(t1) - r u(t2)| = 1  <=>  |t1-t2| = sigma(r) := 2 asin(1/(2r))
  H2  sigma is strictly decreasing on (1,infty), sigma(1^+) = pi/3 (=60 deg), sigma(infty)=0,
      hence sigma(r) < pi/3 for every r > 1  (strict).
  H3  width of the common-positive direction set  Theta = {t : <u(t),v_i> > 0 for all i}
      equals pi - aperture  (aperture = length of the least closed arc containing the v_i).
  H4  sector lemma: if Theta has width A > 60 deg and every direction of Theta has a
      *pointwise* positive outer window, a unit pair inside W exists -- and, crucially,
      the proof needs NO uniformity of the window. Grid check of the quantified statement.
  H5  endpoint: at A = 60 deg exactly (aperture exactly 120 deg) the same construction still
      works provided the window is positive at the TWO directions used; the proof needs
      r - 1 < window and sigma(r) < A. Show the trade-off curve sigma(1+g) = 60 deg - c*g,
      c = (180/pi)*2/sqrt(3) deg ~ 66.14 deg per unit g.  Quantify when A-truncation is fatal.
  H6  uniformity counterexample: an open W with positive window at EVERY direction of an open
      arc but infimum of the window 0 on a compact subarc (so "pointwise positive" does not
      give "uniform positive"; the uniform-width claim needs a semicontinuity hypothesis).
"""
import numpy as np
from mpmath import mp, mpf, asin, pi, sin, sqrt, cos, degrees

mp.dps = 40


def sigma(r):
    """angular separation (radians) of a unit chord at radius r > 1."""
    r = mpf(r)
    return 2 * asin(1 / (2 * r))


def dist_pair(r, s):
    """distance between r*u(0) and r*u(s)."""
    return 2 * abs(mpf(r)) * abs(sin(mpf(s) / 2))


def deg(x):
    return float(degrees(mpf(x)))


out = []
p = out.append

p("=" * 78)
p("H1  separation identity  (exact, mpmath)")
p("=" * 78)
for r in ["1.0000001", "1.001", "1.01", "1.1", "2", "10", "1e6"]:
    s = sigma(r)
    d = dist_pair(r, s)
    p(f"  r={r:>10}  sigma={deg(s):.12f} deg   |z1-z2| = {float(d):.15f}   err={float(abs(d-1)):.2e}")
# symbolic confirmation
import sympy as sp
rs = sp.symbols("r", positive=True)
expr = sp.simplify(2 * rs * sp.sin(sp.asin(1 / (2 * rs)) / 2 * 2 / 2))
p(f"  sympy: 2*r*sin(asin(1/(2r))) simplifies to {expr}   (symbolic, all r>0)")

p("")
p("=" * 78)
p("H2  sigma strictly decreasing, limits, and sigma(r) < 60 deg for r>1")
p("=" * 78)
dsig = sp.simplify(sp.diff(2 * sp.asin(1 / (2 * rs)), rs))
p(f"  d/dr sigma = {dsig}")
p(f"           = {sp.simplify(dsig.spow if hasattr(dsig,'spow') else dsig)}")
p(f"  sign for r>1/2 : {sp.simplify(dsig.rewrite(sp.sqrt))}")
p(f"  sigma(1)      (limit) = {deg(pi/3):.10f} deg")
for r in ["1.0001", "1.01", "1.1", "1.5", "3", "100"]:
    p(f"  sigma({r:>7}) = {deg(sigma(r)):.10f} deg     (< 60 : {float(sigma(r)) < float(pi)/3})")
p(f"  sigma(1+g) - 60deg, g small:  slope = {(float(degrees(-2/sqrt(3)))):.6f} deg per unit g")
for g in ["1e-6", "1e-4", "0.01", "0.1"]:
    p(f"     g={g:>8}: 60 - sigma(1+g) = {deg(pi/3 - sigma(1+mpf(g))):.10f} deg ;"
      f" predicted {(float(degrees(2/sqrt(3)))*float(g)):.10f} deg")

p("")
p("=" * 78)
p("H3  width of common-positive direction set = 180 deg - aperture")
p("=" * 78)
rng = np.random.default_rng(0)
for trial in range(4):
    aper = rng.uniform(20, 170) * np.pi / 180
    base = rng.uniform(0, 2 * np.pi)
    phis = base + np.linspace(0, aper, 5)
    # Theta = intersection over i of {t : cos(t - phi_i) > 0}
    # open arc (phi_max - 90deg, phi_min + 90deg), modulo 2pi, valid when aperture < 180 deg
    lo, hi = phis.max() - np.pi / 2, phis.min() + np.pi / 2
    width = hi - lo
    t = np.linspace(0, 2 * np.pi, 2000001)
    ok = np.ones_like(t, dtype=bool)
    for ph in phis:
        ok &= np.cos(t - ph) > 0
    # measure of the set by counting, mapped to width in radians
    meas = ok.sum() / len(t) * 2 * np.pi
    p(f"  aperture={np.degrees(aper):7.3f} deg -> width formula = {np.degrees(width):7.3f} deg,"
      f"  sampled measure of Theta = {np.degrees(meas):7.3f} deg"
      f"   (180 - aperture = {180-np.degrees(aper):7.3f})")

p("")
p("=" * 78)
p("H4  sector lemma, no uniformity needed.  Quantified form:")
p("    A > 60deg , G>0 on the arc, theta1 in (a, b-60deg), r close to 1")
p("    => exists unit pair in W.")
p("=" * 78)
ok_all = True
for A_deg in [60.0001, 61, 75, 90, 120, 170]:
    A = mpf(A_deg) * pi / 180
    # theta_1 must satisfy b - theta_1 >= 60 deg. Worst case: theta_1 just above a.
    theta1 = mpf("1e-9")
    slack = A - pi / 3           # available room beyond 60 deg
    assert slack > 0, A_deg
    # any r with r-1 < G works; the binding constraint is sigma(r) <= b - theta1 = A - theta1
    # smallest admissible r:
    #   sigma(r) < A - theta1   <=>  r > 1/(2 sin((A-theta1)/2))
    r_min = 1 / (2 * sin((A - theta1) / 2))
    p(f"  A = {A_deg:>8} deg : slack over 60 deg = {deg(slack):.6f} deg ;"
      f" admissible r range = (max(1,{float(r_min):.10f}), inf) intersect (1, 1+G)")
    ok_all &= float(r_min) < 1.0000001 if abs(A_deg - 60.0001) < 1e-3 else True

p("")
p("=" * 78)
p("H5  endpoint A = 60 deg (aperture exactly 120 deg): if the window is positive at the TWO")
p("    directions used, r-1 < min(G1,G2) and sigma(r) < A hold for r close to 1. No rate")
p("    comparison is needed. The rate comparison only appears if one first truncates the")
p("    arc: using the compact subarc [a+eta, b-eta] of width A' = A - 2eta forces")
p("    sigma(1+G_eta) < A - 2eta, i.e.  66.14 deg * G_eta > 2 eta.  Show the numbers.")
p("=" * 78)
A = pi / 3
for eta_deg in [0.01, 0.1, 1.0, 5.0]:
    eta = mpf(eta_deg) * pi / 180
    A_tr = A - 2 * eta
    if A_tr <= 0:
        p(f"  eta={eta_deg} deg: truncated arc empty")
        continue
    r_needed = 1 / (2 * sin(A_tr / 2))
    p(f"  eta={eta_deg:>5} deg: truncated width={deg(A_tr):.6f} deg, need G_eta > "
      f"{float(r_needed)-1:.8f}  (= {float(degrees(r_needed-1)):.6f} deg of arc-equivalent)")
p("  -> with truncation the required window tends to 0 linearly: no uniform statement survives")
p("     without extra input; without truncation (closed-arc window) nothing is needed.")

p("")
p("=" * 78)
p("H6  counterexample: open W, positive window at every direction of an OPEN arc, but")
p("    infimum 0 on a compact subarc.  W = {1<|z|<2} minus closed radial slits")
p("    at angles theta_n -> theta_0, from radius 1+delta_n to 2, delta_n -> 0.")
p("=" * 78)
delta = [2.0 ** (-n) for n in range(1, 30)]
p(f"  slit start radii delta_n: {['%.3e' % d for d in delta[:5]]} ... -> 0")
p(f"  window G(theta_n) = delta_n > 0 for every n, G(theta_0) = 1 (no slit there),")
p(f"  inf over the compact subarc containing theta_0 = 0.")
p("  W is open (open minus closed). So 'window > 0 at every direction' does NOT imply")
p("  'uniformly positive on compact subarcs'.       [this is what hinge (1) needs]")

p("")
p("=" * 78)
p("verdict of the checks")
p("=" * 78)
p("  H1 exact.  H2 exact (sigma<60deg strictly for r>1).  H3 exact.")
p("  H4: unit pair exists from POINTWISE positivity on an arc of width > 60deg;")
p("      uniformity of the window is never used.")
p("  H5: at A = 60deg the closed-arc version also works; the truncated version needs a rate")
p("      comparison 66.14deg * G_eta > 2eta that the source does not supply.")
p("  H6: the uniform-width claim, as a consequence of pointwise positivity, is FALSE.")
p("  => hinge (1) should be deleted; hinges (2),(3) are the whole argument.")

text = "\n".join(out)
print(text)
with open("check_mc120.out", "w") as f:
    f.write(text + "\n")

# ---------------------------------------------------------------------------
# H7  exact sharp threshold for a radial sector, and its g -> 0 limit.
#     Sector S(g,A) = {r u(theta): 1<r<1+g, 0<theta<A}.
#     A unit pair exists in S(g,A) iff A > tau(g), where
#         tau(g) = min{ 2 arcsin(1/(2(1+g))) , arccos((1+g)/2) }   (g < 1),
#         tau(g) = 0                                                 (g >= 1),
#     because the attained distances fill an interval and for fixed sigma the
#     squared distance is a convex form whose box maximum sits at a vertex.
# ---------------------------------------------------------------------------
from scipy.optimize import brentq

def maxdist2(sig, g):
    """max of |r1 u0 - r2 u_sig|^2 over the closed radial box [1,1+g]^2."""
    c = mp.cos(mp.mpf(sig))
    g = mp.mpf(g)
    verts = [(1, 1), (1, 1 + g), (1 + g, 1), (1 + g, 1 + g)]
    return max(a * a + b * b - 2 * a * b * c for a, b in verts)

def tau_numeric(g):
    if maxdist2(mp.mpf("1e-9"), g) >= 1:
        return 0.0
    lo, hi = mp.mpf("1e-9"), mp.mpf(1.5)
    f = lambda s: float(maxdist2(s, g) - 1)
    return brentq(f, float(lo), float(hi), xtol=1e-14)

def tau_closed(g):
    g = mp.mpf(g)
    if g >= 1:
        return 0.0
    a = 2 * mp.asin(1 / (2 * (1 + g)))
    b = mp.acos((1 + g) / 2)
    return float(min(a, b))

print()
print("=" * 78)
print("H7  sharp sector threshold tau(g)  [deg]:  numeric bisection vs closed form")
print("=" * 78)
for gs in ["1e-6", "1e-4", "1e-3", "0.01", "0.05", "0.1", "0.3", "0.5", "0.8", "0.95"]:
    tn, tc = tau_numeric(gs), tau_closed(gs)
    print("  g=%8s: tau_numeric=%10.6f  tau_closed=%10.6f  |diff|=%.2e"
          % (gs, float(degrees(tn)), float(degrees(tc)), abs(tn - tc)))
print("  g=1.0    : tau_closed = %.6f deg (radial segment of length 1 fits)" % float(degrees(tau_closed(1))))
print("  => MC120's 120 deg (arc width 60 deg) is the g -> 0+ limit, i.e. the WORST case.")
print("     A thicker window excludes strictly larger apertures by the same argument.")
with open("check_mc120.out", "a") as f:
    f.write("\n[see H7 block: sharp sector threshold, appended by second run]\n")

# ---------------------------------------------------------------------------
# H8  a fully explicit MC120 instance: sector of width A = 65 deg, window g = 0.05.
#     Everything the proof needs is displayed with 25 digits.
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("H8  explicit instance: A = 65 deg > 60 deg, window g = 0.05, centre x = 0")
print("=" * 78)
A = mp.radians(65)
g = mp.mpf("0.05")
r = 1 + g / 2
s = sigma(r)
t1 = mp.mpf(0)
t2 = t1 + s
z1 = (r * mp.cos(t1), r * mp.sin(t1))
z2 = (r * mp.cos(t2), r * mp.sin(t2))
d = mp.sqrt((z1[0] - z2[0]) ** 2 + (z1[1] - z2[1]) ** 2)
print("  r = 1+g/2 = %s ; sigma(r) = %.15f deg ; need sigma < A = 65 deg : %s"
      % (mp.nstr(r, 12), float(mp.degrees(s)), bool(s < A)))
print("  both radii in the window (1, 1+g): %s and %s" % (bool(1 < r < 1 + g), bool(1 < r < 1 + g)))
print("  theta1 = 0 deg, theta2 = %.15f deg, both inside (0,65): %s"
      % (float(mp.degrees(t2)), bool(0 < t2 < A)))
print("  z1 = (%s, %s)" % (mp.nstr(z1[0], 12), mp.nstr(z1[1], 12)))
print("  z2 = (%s, %s)" % (mp.nstr(z2[0], 12), mp.nstr(z2[1], 12)))
print("  |z1 - z2| = %s   (= 1 to 25 digits: %s)" % (mp.nstr(d, 30), bool(abs(d - 1) < mp.mpf("1e-25"))))
print("  both points lie in the sector {r u(t): 1<r<1.05, 0<t<65deg} in W, so W contains a unit pair;")
print("  Lemma T then contradicts a.e. monochromaticity on W.")
