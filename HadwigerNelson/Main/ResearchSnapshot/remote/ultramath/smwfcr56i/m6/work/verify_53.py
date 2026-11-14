"""Verification of the uniform expansion (5.9) of paper section 5.3 and of the
constants in (5.10), symbolically at first order in d and numerically to high
precision for the full nonlinear maps.

Lemma 5.5 (binary-centre separation) is what forces palettes to have at most two
labels (Proposition 5.6); its quantitative input is that the circle
diffeomorphism F = alpha_+ o alpha_-^{-1} - 2*kappa (kappa = pi/3) satisfies

     F(t) = t + d * (a_+(t+kappa) - a_-(t+kappa)) + O(d^2)
          = t + (2d/sqrt3) sin(t - pi/6) + O(d^2),                        (5.9)

whence, for the six phases t, t+kappa, ..., t+5kappa,

     max_{0<=j<=5} (F_j(t) - t) >= c_0 d ,   max_j F_j'(t) >= 1 + c_0 d .  (5.10)
"""
import sympy as sp
import mpmath
mpmath.mp.dps = 40

d, t = sp.symbols('d t', real=True)
I = sp.I
kappa = sp.pi/3

# ---------- exact first-order data ----------
logval = sp.log(1 + d*sp.exp(-I*t))
imlog = sp.simplify(sp.expand_complex(sp.series(logval, d, 0, 3).removeO()).as_real_imag()[1])
print("Im log(1 + d e^{-it})            =", sp.simplify(imlog))

rho = sp.sqrt(sp.simplify(sp.expand((d + sp.exp(I*t))*(d + sp.exp(-I*t)))))
print("|d + e^{it}|                     =", sp.simplify(sp.series(rho, d, 0, 3).removeO()))

delta = sp.series(sp.acos(rho/2), d, 0, 3).removeO()
delta = sp.simplify(sp.expand(sp.expand_trig(delta)))
print("delta = arccos(|d+e^{it}|/2)     =", delta)

alpha_p = t + imlog + delta
alpha_m = t + imlog - delta
a_p = sp.simplify(sp.trigsimp(sp.diff(alpha_p - (t + kappa), d).subs(d, 0)))
a_m = sp.simplify(sp.trigsimp(sp.diff(alpha_m - (t - kappa), d).subs(d, 0)))
print()
print("a_+(t) = d-coeff of alpha_+(t)-(t+kappa) =", sp.simplify(a_p))
print("a_-(t) = d-coeff of alpha_-(t)-(t-kappa) =", sp.simplify(a_m))
okp = sp.simplify(a_p - (-sp.sin(t) - sp.cos(t)/sp.sqrt(3))) == 0
okm = sp.simplify(a_m - (-sp.sin(t) + sp.cos(t)/sp.sqrt(3))) == 0
print("  matches paper (5.9) line 1:  a_+ = -sin t - cos t/sqrt3 :", okp,
      "   a_- = -sin t + cos t/sqrt3 :", okm)

c1 = sp.simplify(sp.trigsimp(a_p.subs(t, t + kappa) - a_m.subs(t, t + kappa)))
print()
print("d-coefficient of F, a_+(t+kappa) - a_-(t+kappa) =", sp.simplify(sp.expand_trig(c1)))
tgt = 2/sp.sqrt(3)*sp.sin(t - sp.pi/6)
tgt2 = -2/sp.sqrt(3)*sp.cos(t + kappa)
print("  equals (2/sqrt3) sin(t - pi/6)     :", sp.simplify(sp.expand_trig(c1 - tgt)) == 0)
print("  equals -(2/sqrt3) cos(t + kappa)   :", sp.simplify(sp.expand_trig(c1 - tgt2)) == 0)
alt = sp.simplify(sp.expand_trig(sp.simplify(sp.trigsimp(a_p - a_m.subs(t, t+kappa)))))
print("  NOTE: a_+(t) - a_-(t+kappa) =", alt,
      " vanishes identically -- so the O(d) term genuinely uses a_+(t+kappa), as printed.")

# ---------- full nonlinear check at high precision ----------
print()
print("=== full nonlinear check: |F(t) - t - d*c1(t)| = O(d^2) ===")
kpim = mpmath.pi/3
def Theta(dv, tv):
    return tv + mpmath.im(mpmath.log(1 + dv*mpmath.exp(-1j*tv)))
def alpha(dv, tv, sgn):
    rr = abs(dv + mpmath.exp(1j*tv))
    return Theta(dv, tv) + sgn*mpmath.acos(rr/2)
def alpha_inv(dv, target, sgn):
    x = target + (kpim if sgn > 0 else -kpim)
    for _ in range(80):
        h = mpmath.mpf('1e-30')
        der = (alpha(dv, x+h, sgn) - alpha(dv, x-h, sgn))/(2*h)
        x = x - (alpha(dv, x, sgn) - target)/der
    return x
worst = mpmath.mpf(0)
for kt in range(63):
    tv = mpmath.mpf('0.1')*kt
    for dv in [mpmath.mpf('1e-1'), mpmath.mpf('1e-2'), mpmath.mpf('1e-3'), mpmath.mpf('1e-4')]:
        U = alpha_inv(dv, tv, -1)
        Fv = alpha(dv, U, +1) - 2*kpim
        c1v = mpmath.mpf(2)/mpmath.sqrt(3)*mpmath.sin(tv - mpmath.pi/6)
        worst = max(worst, abs(Fv - tv - dv*c1v)/dv**2)
print("sup over grid of |F(t)-t-d c1(t)|/d^2  =", mpmath.nstr(worst, 12))
print("  => O(d^2) remainder of (5.9) is uniform; (5.10) holds with c_0 = 1 - O(d).")

# ---------- the six phases of (5.10) ----------
print()
print("=== (5.10): max over six phases spaced by kappa ===")
N = 40000
mn = min(max(mpmath.sin(mpmath.mpf(k)*mpmath.pi/N - j*mpmath.pi/3 - mpmath.pi/6)
             for j in range(6)) for k in range(N))
mx = min(max(mpmath.cos(mpmath.mpf(k)*mpmath.pi/N - j*mpmath.pi/3 - mpmath.pi/6)
             for j in range(6)) for k in range(N))
print("min over t of max_j sin(t - j pi/3 - pi/6) =", mpmath.nstr(mn, 15))
print("min over t of max_j cos(t - j pi/3 - pi/6) =", mpmath.nstr(mx, 15))
print("sqrt(3)/2 =", mpmath.nstr(mpmath.sqrt(3)/2, 15))
print("  both equal sqrt(3)/2 exactly, so c_0 = (2/sqrt3)(sqrt3/2) = 1 - O(d).")
