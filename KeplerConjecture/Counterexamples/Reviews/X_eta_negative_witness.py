#!/usr/bin/env python3
"""MINIMAL UNSOUNDNESS WITNESS for Main's shell_check at 7c56c5ee (blob 909a50a).

The profile is C's OWN committed one (out/shell_propose.json, n=27, rho=41/20), so nothing is
invented.  Fed with a NEGATIVE shell allowance eta, every check PASSES and the reported density
bound is 1.5%, contradicting Kepler (0.7405).

Root cause: K15-C003's price is n*max(M,0), so for M < 0 the correct bound is the eta = 0 one.
The formula (p(0)+n*eta)/q(0) is therefore valid ONLY for eta >= 0; `check()` does not enforce it.
This is why the eta >= 0 requirement is not a technicality about gluing the two sign regions --
it is the validity condition of the bound itself.
"""
import json, sys
import sympy as sp
from fractions import Fraction as F
sys.path.insert(0, '.')
spec = __import__('importlib.util').util.spec_from_file_location("sc", "shell_check_7c56c5ee.py")
sc = __import__('importlib.util').util.module_from_spec(spec); spec.loader.exec_module(sc)

d = json.load(open('C_shell_propose.json'))
row = [r for r in d['rows'] if r['count'] == 27][0]
a = [F(sp.Rational(x).p, sp.Rational(x).q) for x in row['verdict']['a_monomial']]

print("profile: C's out/shell_propose.json, n=27, rho=41/20 (committed, not invented)")
print("\n(1) eta = 0 (C's published setting):")
r0 = sc.check(a, rho=F(41,20), eta=F(0))
print("\n(2) eta = -7611431/500000000  (= -0.015222862, the max of p on the shell):")
r1 = sc.check(a, rho=F(41,20), eta=F(-7611431, 500000000))
print("\nEXPECTED: (1) PASS with 0.78037 (correct, and what C published).")
print("          (2) must FAIL -- a density bound of 1.5% is impossible since Kepler is 74%.")
print("          Observed: both PASS. The second is the unsoundness witness.")
