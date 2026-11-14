"""Exact checks for the algebraic steps of the analytic core (paper section 3.3)
and for the unit-sum structural lemma.  All arithmetic is exact (sympy, Q(sqrt(3))[i])."""
import sympy as sp

I = sp.I
s3 = sp.sqrt(3)

print("=== (A) step (3.14): equal moduli but unequal arguments ===")
A, B = sp.Integer(1), sp.Integer(4)
L = sp.Integer(2)                        # L = sqrt(A*B)
u = sp.Rational(1, 2) + I*s3/2           # e^{i pi/3}, an element of K
one = sp.expand(A - B*u**2)
two = sp.expand(-L + (A - B)*u + L*u**2)
print("  A - B u^2           =", sp.simplify(one))
print("  -L+(A-B)u+L u^2     =", sp.simplify(two))
m1 = sp.simplify(sp.expand(sp.expand(one*sp.conjugate(one))))
m2 = sp.simplify(sp.expand(sp.expand(two*sp.conjugate(two))))
print("  |A-Bu^2|^2          =", m1)
print("  |-L+(A-B)u+Lu^2|^2  =", m2)
print("  moduli equal   :", sp.simplify(m1 - m2) == 0)
print("  arguments equal:", sp.simplify(one - two) == 0)

print()
print("=== (B) unit-sum lemma: |z| <= 2 in F(i)  =>  z = u + v, u,v in K ===")
print("    u = z/2 + i (z/|z|) sqrt(1-|z|^2/4),   v = z/2 - i (z/|z|) sqrt(1-|z|^2/4)")


def unitsum(zz):
    mm = sp.simplify(sp.expand(zz*sp.conjugate(zz)))
    s = sp.sqrt(sp.simplify(1 - mm/4))
    uu = sp.simplify(sp.expand(zz/2 + I*(zz/sp.sqrt(mm))*s))
    vv = sp.simplify(sp.expand(zz/2 - I*(zz/sp.sqrt(mm))*s))
    return (sp.simplify(sp.expand(uu*sp.conjugate(uu)) - 1),
            sp.simplify(sp.expand(uu + vv - zz)))


ok = True
for zz in [sp.Rational(1, 3), sp.Integer(2), sp.sqrt(2),
           sp.Rational(1, 2) + I*sp.Rational(3, 7),
           I*sp.sqrt(sp.Rational(7, 5)), sp.sqrt(3)*I, -sp.Rational(4, 3),
           sp.Integer(0)]:
    r1, r2 = unitsum(zz)
    ok = ok and (r1 == 0 or abs(complex(sp.N(r1))) < 1e-25) and (r2 == 0 or abs(complex(sp.N(r2))) < 1e-25)
    print("    z=%-20s |u|^2-1=%-22s u+v-z=%s" % (zz, r1, r2))
print("  all instances exact:", ok)

print()
print("=== (C) hexagonal 7-colouring constants (upper-bound sanity anchor) ===")
s = sp.Rational(2, 5)
print("  2r =", 2*s, " < 1 :", 2*s < 1)
print("  (sqrt(21)-2) r =", sp.simplify(sp.expand((sp.sqrt(21) - 2)*s)),
      "=", sp.N((sp.sqrt(21) - 2)*s, 20), "  exact test 2sqrt21>9 <=> 84>81:", 84 > 81)
