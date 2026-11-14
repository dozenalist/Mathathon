"""
Exact/series checks for two computational cores of the paper that are used by the
lower bound.

 (1) Section 8.5: the trigonometric identities behind the polynomial region (8.4).
 (2) Section 5.3 (Lemma 5.5): the first-order expansions of the circle maps alpha_+
     and alpha_-, and of F = alpha_+ o alpha_-^{-1} - 2*kappa, which drive the
     separation of binary centres.  Verified as formal series in d.

Run:  python3 work/paper_identities.py
"""
import sympy as sp

t, d = sp.symbols('t d', real=True)
I = sp.I

print("=== (1) Section 8.5: identities behind the region (8.4) ===")
xi, up = sp.symbols('xi ups', real=True)
r2 = xi**2 + up**2
phi = sp.atan2(up, xi)
# sin(3 phi) = ups (3 xi^2 - ups^2) / r^3   and  sin^2(3 phi) = ups^2 (3xi^2-ups^2)^2 / r^6
lhs = sp.simplify(sp.expand(sp.sin(3*phi) - up*(3*xi**2 - up**2)/r2**sp.Rational(3, 2)))
# do it trigonometrically instead of with atan2: substitute xi = r cos, ups = r sin
r, th = sp.symbols('r theta', real=True, positive=False)
sub = {xi: r*sp.cos(th), up: r*sp.sin(th)}
expr = sp.simplify(sp.expand(sp.sin(3*th) - (r*sp.sin(th))*(3*(r*sp.cos(th))**2 - (r*sp.sin(th))**2)/r**3))
print("  sin(3 phi) = ups(3 xi^2 - ups^2)/l^{3/2} :",
      sp.simplify(sp.expand(sp.expand(expr).rewrite(sp.sin))) == 0)
resid = sp.simplify(sp.expand_trig(sp.expand(sp.sin(3*th)**2 - (r*sp.sin(th))**2*(3*(r*sp.cos(th))**2 - (r*sp.sin(th))**2)**2/r**6)))
print("  sin^2(3 phi) - ups^2(3xi^2-ups^2)^2/l^3 =", resid, "  (zero identity)")
# sin(3 delta) = sqrt(1 - l/4) (l - 1) with cos(delta) = r/2
delta = sp.symbols('delta', positive=True)
print("  sin(3 delta) - sin(delta)(4cos^2 delta - 1) :",
      sp.simplify(sp.expand(sp.sin(3*delta) - sp.sin(delta)*(4*sp.cos(delta)**2 - 1))))
print("  so sin(3 delta) = sqrt(1-l/4)(l-1) when cos delta = r/2 (l = r^2):",
      sp.simplify(sp.expand((4*(r/2)**2 - 1) - (r**2 - 1))) == 0,
      "  and sin(delta)^2 = 1 - l/4:", sp.simplify(sp.expand(sp.sin(sp.acos(r/2))**2 - (1 - r**2/4))) == 0)
# the product identity: sin3(phi-delta) sin3(phi+delta) = sin^2(3phi) - sin^2(3 delta)
p, q = sp.symbols('p q', real=True)
print("  sin3(phi-d)sin3(phi+d) - [sin^2(3phi)-sin^2(3d)] :",
      sp.simplify(sp.expand(sp.sin(3*(p - q))*sp.sin(3*(p + q)) - (sp.sin(3*p)**2 - sp.sin(3*q)**2))))
print("  => (8.4) says exactly that this product is NEGATIVE, i.e. the two unit directions")
print("     phi-delta and phi+delta lie in sectors with opposite outsider values.")

print()
print("=== (2) Lemma 5.5: first-order expansions in d ===")
# Theta_d(t) = t + Im log(1 + d e^{-it})
Theta = t + sp.im(sp.series(sp.log(1 + d*sp.exp(-I*t)), d, 0, 2).removeO())
print("  Theta_d(t) - t = ", sp.simplify(sp.expand(Theta - t)))
# |d + e^{it}| = sqrt(1 + 2 d cos t + d^2)
rho = sp.sqrt(1 + 2*d*sp.cos(t) + d**2)
kap = sp.pi/3
alpha_p = Theta + sp.acos(rho/2)
alpha_m = Theta - sp.acos(rho/2)
sp_ap = sp.series(alpha_p, d, 0, 2).removeO()
sp_am = sp.series(alpha_m, d, 0, 2).removeO()
target_p = t + kap - d*sp.sin(t) - d/sp.sqrt(3)*sp.cos(t)
target_m = t - kap - d*sp.sin(t) + d/sp.sqrt(3)*sp.cos(t)
print("  alpha_+ - [t + kappa - d sin t - (d/sqrt3) cos t] =", sp.simplify(sp.expand(sp_ap - target_p)))
print("  alpha_- - [t - kappa - d sin t + (d/sqrt3) cos t] =", sp.simplify(sp.expand(sp_am - target_m)))
# F = alpha_+ o alpha_-^{-1} - 2 kappa : invert alpha_- to first order and compose
# alpha_-(s) = s - k - d sin s + (d/sqrt3) cos s  =>  s = alpha_-(s) + k + d sin s - (d/sqrt3) cos s
# to first order in d: s = u + k + d sin(u+k) - (d/sqrt3) cos(u+k) with u = alpha_-(s)
u = sp.symbols('u', real=True)
sinv = u + kap + d*sp.sin(u + kap) - d/sp.sqrt(3)*sp.cos(u + kap)
comp = (sp_ap.subs(t, sinv))
comp = sp.series(comp, d, 0, 2).removeO()
F = sp.simplify(sp.expand(comp - 2*kap))
target_F = u + 2*d/sp.sqrt(3)*sp.sin(u - sp.pi/6)
print("  F(u) - [u + (2d/sqrt3) sin(u - pi/6)] =", sp.simplify(sp.expand(F - target_F)))
print("  equivalent form  -2d/sqrt3 cos(t+kappa):",
      sp.simplify(sp.expand(-2*d/sp.sqrt(3)*sp.cos(t + kap) - 2*d/sp.sqrt(3)*sp.sin(t - sp.pi/6))) == 0)
print()
print("  max over j=0..5 of sin(t - j pi/3) >= sqrt(3)/2 for every t (scan of 2001 values of t):")
worst = min(max(sp.N(sp.sin(tt - j*sp.pi/3)) for j in range(6)) for tt in
            [i*sp.pi/1000 for i in range(2001)])
print("    min over the scan of max_j sin(t - j pi/3) =", worst, " >= sqrt3/2 =", sp.N(sp.sqrt(3)/2))
print("    (proof: the six arguments are equally spaced by pi/3, so one of them lies within pi/6 of pi/2,")
print("     and sin(pi/2 - pi/6) = cos(pi/6) = sqrt3/2.)")
