"""Exact adversarial review of submitted sign-predicate repairs.

Run with an immutable Main shell_check.py and X exact_sign.py as arguments.
PASS below means the reported bug is reproduced or a repair passes a named
fixture, never a proof that an arbitrary implementation is sound.
"""
import importlib.util
import sys
import sympy as sp

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out

M = module('main_repair', sys.argv[1])
X = module('x_repair', sys.argv[2])
u = sp.Symbol('u')

def cs(p):
    return list(reversed(sp.Poly(p, u).all_coeffs()))

print('Original Main witnesses (must now be False):')
for label, got in [
    ('interval endpoint roots', M.le_on_interval([0, 1, -1], 0, 0, 1)),
    ('nonnegative half-line endpoint root', M.nonneg_on_half_line([0, -1, 1])),
    ('nonpositive ray endpoint root', M._ray([0, 1, -1], 0))]:
    print(label, got)
    assert got is False or got == False

print('Additional Main witnesses (all false inequalities):')
cases = [
    ('interval squared roots at all three probes',
     (u*(u-sp.Rational(1,2))*(u-1))**2,
     lambda p: M.le_on_interval(cs(p), 0, 0, 1), sp.Rational(1,4)),
    ('half-line negative square at all four probes',
     -(u*(u-1)*(u-sp.Rational(1,2))*(u-2))**2,
     lambda p: M.nonneg_on_half_line(cs(p)), sp.Rational(1,4)),
    ('ray positive square at all three probes',
     (u*(u-1)*(u-2))**2,
     lambda p: M._ray(cs(p), 0), sp.Rational(1,2)),
]
for label, p, predicate, point in cases:
    value = sp.expand(p).subs(u, point)
    got = predicate(p)
    print(label, 'accepted=', got, 'exact witness=', value, 'at', point)
    assert got == True, 'Submitted repair changed: independently review rather than reuse this disposition'
    assert value != 0

print('X repaired predicate: irrational simple/double roots and endpoints')
for p, a, want, expect in [
    ((u*u-2)*(u*u-3), 0, 1, False),
    ((u*u-2)**2, 0, 1, True),
    (-(u*u-2)**2, 0, -1, True),
    (u*(u-1), 0, 1, False),
    ((u-1)**2, 1, 1, True),
    (-(u-1)**2, 1, -1, True)]:
    got = X.sign_on_half_line(p, a, want, var=u)
    print(str(p), a, want, got, 'expected', expect)
    assert got == expect
print('REPRODUCED: Main repair still has three false accepts; X named controls pass.')
