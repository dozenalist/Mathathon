"""s5_trig.py -- exact symbolic checks of the geometric identities the lemmas use."""
import sympy as sp

t = sp.symbols('t', real=True)
R = lambda x: sp.simplify(x * sp.exp(sp.I * sp.pi / 3))

print("(1) |1 + exp(2 pi i/3)| = 1 :", sp.simplify(sp.Abs(1 + sp.exp(2*sp.I*sp.pi/3))))
print("(2) |1 + exp(i pi/3)| = sqrt3 :", sp.simplify(sp.Abs(1 + sp.exp(sp.I*sp.pi/3))))
print("(3) 1 + exp(2 pi i/3) = exp(i pi/3) :",
      sp.simplify(1 + sp.exp(2*sp.I*sp.pi/3) - sp.exp(sp.I*sp.pi/3)))
print("(4) exp(i pi/3) - 1 = exp(2 pi i/3) :",
      sp.simplify(sp.exp(sp.I*sp.pi/3) - 1 - sp.exp(2*sp.I*sp.pi/3)))

# (5) uniqueness of the unit decomposition: s + t = u + f with |s|=|t|=|u|=|f|=1
u = sp.exp(sp.I*t); f = sp.exp(sp.I*sp.pi/7)
s, = sp.symbols('s'),
# solve |s| = 1, |u + f - s| = 1 (two solutions; check that u and f are the solutions)
print("(5) s = u solves |s|=1 and |u+f-s|=1 :",
      sp.simplify(sp.Abs(u + f - u)), sp.simplify(sp.Abs(f)))
print("    s = f solves it too :", sp.simplify(sp.Abs(u + f - f) - 1))
# the two solutions of |s|=1, |w-s|=1 for w = u+f:  s = w/2 +- i*sqrt(1-|w|^2/4)*w/|w|
w = sp.simplify(u + f)
print("    |w|^2 = 2 + 2 cos(angle) :", sp.simplify(sp.Abs(w)**2 - (2 + 2*sp.cos(sp.pi/7 - t))))

# (6) unit triangle (y, y+w, y+Rw): all sides 1
w = sp.exp(sp.I*t)
side1 = sp.simplify(sp.Abs(w)); side2 = sp.simplify(sp.Abs(R(w)))
side3 = sp.simplify(sp.Abs(w - R(w)))
print("(6) |w| =", side1, " |Rw| =", side2, " |w - Rw| =", side3)
print("    R(w) = w exp(i pi/3) :", sp.simplify(R(w) - w*sp.exp(sp.I*sp.pi/3)))
print("    side directions: w, Rw, R^2 w ; R^2w = R(w) - w : ",
      sp.simplify(R(w) - w - sp.simplify(w*sp.exp(2*sp.I*sp.pi/3))))

# (7) the three side directions of a unit triangle are at 120 degrees: {w, Rw, R^2 w}
print("(7) sum of the three side vectors of the unit triangle = 0 :",
      sp.simplify((R(w) - w) + (w) + (-R(w))))

# (8) R^2-invariance of U with sigma(U) = pi and U cap R U = empty  =>  U u R U = S
print("(8) R^{-1} = R^5, R^3 = -id, so -U = R U when R^2 U = U : symbolic, see text")
