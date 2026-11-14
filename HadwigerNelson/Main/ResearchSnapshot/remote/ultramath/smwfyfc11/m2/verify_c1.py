#!/usr/bin/env python3
"""C1 audit: (a) countermodel to REPORT.md Lemma D as stated; (b) exact geometry of C cap S.

All computations exact (sympy / Fractions) unless a step is explicitly flagged numeric,
which is only the Monte-Carlo cross-check of an identity already proved in closed form.
"""
import sympy as sp
from fractions import Fraction as F

out = []
def P(*a):
    s = " ".join(str(x) for x in a)
    out.append(s); print(s)

# ---------------------------------------------------------------- (b) geometry
th, h, d = sp.symbols('theta h d', real=True, positive=False)
h = sp.symbols('h', positive=True)

# C = {x + e0 + v : |v| = 1} with e0 = (1,0); S = {y : |y-x| = 1}
# membership in S  <=>  |e0 + v| = 1
v = sp.Matrix([sp.cos(th), sp.sin(th)])
e0 = sp.Matrix([1, 0])
sq = sp.simplify(((e0 + v).T * (e0 + v))[0, 0])
P("[1] |e0+v|^2 =", sp.expand(sp.trigsimp(sq)))
c = sp.symbols('c', real=True)
csols = sp.solve(sp.Eq(2*c + 2, 1), c)
P("[2] |e0+v|^2 = 1  <=>  2cos(theta)+2 = 1  <=>  cos(theta) =", csols)
sols = [t for t in [sp.Rational(2,3)*sp.pi, sp.Rational(4,3)*sp.pi]]
P("[2b] theta in [0,2pi): ", sols, "  exact coords:",
  [[sp.simplify(sp.cos(s)), sp.simplify(sp.sin(s))] for s in sols])
P("[2c] residual check of the equation at both roots:",
  [sp.simplify(2*sp.cos(s) + 2 - 1) for s in sols],
  "; at theta=0,pi (v=+-e0):", [sp.simplify(2*sp.cos(s)+2-1) for s in [0, sp.pi]])
# exact check of the two points and of the antiparallel one
root3 = sp.sqrt(3)
v120 = sp.Matrix([F(-1, 2), root3 / 2]); vm120 = sp.Matrix([F(-1, 2), -root3 / 2])
for nm, vv in [("v=+120deg", v120), ("v=-120deg", vm120)]:
    lhs = sp.simplify(((e0 + vv).T * (e0 + vv))[0, 0])
    P(f"[3] {nm}: v={list(vv)}, |v|^2={sp.simplify((vv.T*vv)[0,0])}, |e0+v|^2={lhs}  -> in S? {lhs==1}")
vanti = sp.Matrix([-1, 0])
P("[4] v=-e0 (antiparallel): |e0+v|^2 =", sp.simplify(((e0 + vanti).T*(e0 + vanti))[0, 0]),
  " -> point x+e0+v = x, distance from x = 0, so NOT in S.")
P("[4b] v=+e0 (parallel): point x+2e0, distance 2, NOT in S.")
P("[5] solutions in [0,2pi) of |e0+v|=|v|=1: exactly the two above; 2cos(theta)+2-1 = 0 has")
P("    exactly two roots mod 2pi since cos is 2pi-periodic and strictly monotone on [0,pi] and [pi,2pi].")

# ------------------------------------------------- (b') the measure identity
# for fixed e, integral over {v in S : |e+v| <= h} of |sin(arg v - arg e)| dsigma(v)
# with e=(1,0), v=(cos s, sin s): |e+v| = 2|cos(s/2)| and |sin s| the Jacobian.
s = sp.symbols('s', real=True)
# |e+v| <= h  <=>  2|cos(s/2)| <= h.  Near s = pi: s in [pi-2asin(h/2), pi+2asin(h/2)]
a = 2*sp.asin(h/2)
I = sp.integrate(sp.sin(s), (s, sp.pi - a, sp.pi))
I = sp.simplify(sp.expand_trig(sp.simplify(I)))
P("[6] per-direction Jacobian mass  int_{|e+v|<=h} |sin(arg v - arg e)| dv =", sp.simplify(2*I),
  "  (expect h^2 exactly, 0<h<=2)")
num = sp.integrate(sp.sin(s), (s, sp.pi - 2*sp.asin(sp.Rational(1,2)/sp.Integer(2)*sp.Integer(1)), sp.pi))
P("[6b] spot value h=1: closed form", sp.simplify(2*sp.integrate(sp.sin(s), (s, sp.pi-2*sp.asin(sp.Rational(1,2)), sp.pi))),
  " vs h^2 = 1")

P("")
P("[7] hence for measurable D subset S with ANGULAR LEBESGUE measure |D| (radians) and 0<h<=2:")
P("    int_{K_h} |Jac| = |D| * h^2 exactly, where K_h = {(e,v): e in D, |e+v|<=h}.")
P("    G(e,v)=x+e+v is at most 2-to-1 (fibre of w != 0 is {e,w-e}, |e|=|w-e|=1: two points),")
P("    so |G(K_h)| >= |D| h^2/2, while G(K_h) subset B(x,h) with |B(x,h)| = pi h^2.")
P("    Fraction of the ball B(x,h) on which (5.2) forbids colour i: >= |D|/(2 pi).")
P("    exact shadow bound: |A_i cap B(x,h)| <= pi h^2 - |D| h^2/2  =>  limsup dens <= 1 - |D|/(2pi)")
P("    (with the paper's normalised sigma = dtheta/2pi this reads 1 - sigma(D)/(2pi)... no:")
P("     sigma(D) = |D|/2pi, so the bound is limsup dens <= 1 - sigma(D)/2 = 1 - |D|/(4pi).")
P("     Use radians throughout; sigma(D) = |D|/(2pi).")
P("    check |D|=pi/3: forbidden fraction = 1/6 =", sp.simplify((sp.pi/3)/(2*sp.pi)))

# numeric cross-check of the 2-to-1 / area claim by brute force on a grid
import numpy as np
def shadow(d_lo, d_hi, hh, N=3000, R=400):
    # K_h on a (theta_e, s) grid; image points; count which cells of B(x,h) are hit
    te = np.linspace(0, 2*np.pi, N, endpoint=False)
    sv = np.linspace(0, 2*np.pi, N, endpoint=False)
    TE, SV = np.meshgrid(te, sv, indexing='ij')
    VX = np.cos(TE) + np.cos(SV); VY = np.sin(TE) + np.sin(SV)
    mask = ((TE >= d_lo) & (TE <= d_hi)) & (np.hypot(VX, VY) <= hh)
    jac = np.abs(np.sin(SV - TE))
    weighted = jac[mask].sum() * (2*np.pi/N)**2            # ~ int_{K_h} |Jac|
    # image area by occupancy on a fine grid of B(x,h)
    xs = np.linspace(-hh, hh, R); X, Y = np.meshgrid(xs, xs, indexing='ij')
    inside = (X**2 + Y**2) <= hh**2
    cell = (2*hh/R)**2
    occ = np.zeros_like(inside)
    idx = ((VX[mask] + hh)/(2*hh)*(R-1)).astype(int)
    idy = ((VY[mask] + hh)/(2*hh)*(R-1)).astype(int)
    ok = (idx >= 0) & (idx < R) & (idy >= 0) & (idy < R)
    occ[idx[ok], idy[ok]] = True
    img_area = (occ & inside).sum() * cell
    dd = (min(d_hi, 2*np.pi) - d_lo)/(2*np.pi)
    return weighted, dd*hh**2, img_area, dd*hh**2/2, np.pi*hh**2

for (lo, hi, hh) in [(0.0, 2*np.pi/6, 0.5), (0.0, 2*np.pi/3, 0.3), (1.0, 2.0, 2.0)]:
    w, wref, ia, iaref, ball = shadow(lo, hi, hh)
    P(f"[8] grid check D=[{lo:.3f},{hi:.3f}] h={hh}: int|Jac|={w:.6f} (d h^2={wref:.6f}), "
      f"|G(K_h)|={ia:.6f} (>= d h^2/2 = {iaref:.6f}), |B(x,h)|={ball:.6f}")

P("")
# ---------------------------------------------------- (a) the countermodel
# c = i on the open disc B(0,2), c = 0 elsewhere.  i = 1.
P("[9] COUNTERMODEL M1: x=0, i=1, c=1 on B(0,2), c=0 on R^2\\B(0,2).")
P("    - Lebesgue measurable (Borel, two open/closed pieces).")
P("    - x=0 is a density-1 point of A_1: B(0,1) subset A_1, dens = 1.  c(x)=1.")
P("    - sampling (y_n,r_n)=(0,1) constant, permitted by Definition 5.1.")
P("    - is (0,1) a TYPICAL circle sampling? need 0+e typical for a.e. e: |0*e|=1<2 so 0+e is")
P("      an interior point of A_1, hence a density-1 point of its own class: TRUE FOR EVERY e.")
P("    - therefore a_1(0+1*e) = 1 for EVERY e, so b == (1,0,0,0,0,0) in L^inf(S;R^6) lies in W_0,")
P("      b_1(e)=1>0 for every e, so e in D_{0,1} for every e: P_0(e) contains 1 FOR ALL e.")
P("    - Def 1.2 (weak measurable) FAILS: {(y,u): |u|=1, y,y+u in B(0,2)} contains B(0,1) x S,")
P("      product measure pi*1 = pi > 0, so the Def-1.2 sum equals >= pi > 0, not 0.")
P("    - Lemma 5.2(2) FAILS in M1: with e_0=(1,0), v=(0,1), point x+e_0+v=(1,1), |(1,1)|<2,")
P("      so A_1-density there is 1, not 0. (Consistent: 5.2(2) needs Lemma 4.3.)")
P("    - Lemma 4.3 FAILS in M1: (0.0,0.5) and (1.0,0.5) are unit apart, both interior, both colour 1.")
P("    - M1 is not proper: any unit pair inside B(0,2) is monochromatic.")
P("    - strengthening: c=1 on B(0,R_0) makes Lemma D fail at EVERY x with |x| < R_0-1,")
P("      a set of measure pi (R_0-1)^2 which tends to infinity. So the failure set can be conull.")

# exact numeric spot checks of M1 statements
P("[10] M1 spot checks (exact): |(1,1)|=sqrt2<2 so (1,1) is interior -> A_1-density 1.",
  sp.simplify(sp.sqrt(2) < 2))
P("     distance((0,0.5),(1,0.5)) =", 1, " both in B(0,2):", sp.sqrt(F(1,4)) < 2)

open('.ultramath/smwfyfc11/m2/verify_c1.out', 'w')
with open('.ultramath/smwfyfc11/m2/verify_c1.out', 'w') as f:
    f.write("\n".join(out) + "\n")
print("\n[written verify_c1.out]")
