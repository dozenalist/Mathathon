#!/usr/bin/env python3
"""Did Main's eta >= 0 guard actually close the REVIEW_0308 section 17 witness?  Check it.

The witness: C's own committed profile (`C_shell_propose.json`, row n = 27, rho = 41/20) fed to
`shell_check.check` with eta = -7611431/500000000 (the maximum of p on the shell).  On
`7c56c5ee` (blob 909a50a) every check passes and the reported bound is a 1.5% density, which
contradicts Kepler; the cause is that K15-C003's price is n*max(M,0), so for M < 0 the licensed
statement is the plain two-point bound.

`5caa1c9` (main tip) adds `if eta < 0: return None`.  This script checks three things at once:
the old code still exhibits the fault, the new code rejects it, and the eta = 0 control is
numerically unchanged (so the guard did not disturb the published numbers).

Run: python3 Reviews/verify_eta_closed.py     (exit 0 iff the witness is closed and the control holds)
"""
import contextlib, importlib.util, io, json, os, sys
import sympy as sp
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('.py',''), os.path.join(HERE, name))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

old = load("shell_check_7c56c5ee.py")      # blob 909a50a, the version reviewed at 0308
new = load("shell_check_5caa1c9.py")       # blob 5caa1c9, main tip at 9d6414d

d = json.load(open(os.path.join(HERE, 'C_shell_propose.json')))
row = [r for r in d['rows'] if r['count'] == 27][0]
a = [F(sp.Rational(x).p, sp.Rational(x).q) for x in row['verdict']['a_monomial']]
ETA = F(-7611431, 500000000)

def dens(r):
    if r is None: return None
    return float(r[-1]) if isinstance(r, tuple) else float(r)

with contextlib.redirect_stdout(io.StringIO()):
    r_old = old.check(a, rho=F(41,20), eta=ETA, verbose=False)
    r_new = new.check(a, rho=F(41,20), eta=ETA, verbose=False)
    r0    = new.check(a, rho=F(41,20), eta=F(0), verbose=False)
    r0old = old.check(a, rho=F(41,20), eta=F(0), verbose=False)

d_old, d_new, d_ctrl, d_ctrl_old = dens(r_old), dens(r_new), dens(r0), dens(r0old)
print("eta = %s = %.9f, C's row n = 27, rho = 41/20" % (ETA, float(ETA)))
print("  blob 909a50a : %s" % ("None" if d_old is None else "density %.9f   <- the witness" % d_old))
print("  blob 5caa1c9 : %s" % ("None          <- rejected" if d_new is None else "density %.9f" % d_new))
print("  eta = 0 control (new): %.9f   (C published 0.78037032)" % d_ctrl)
ok = (d_old is not None and d_old < 0.02) and (d_new is None) and abs(d_ctrl - d_ctrl_old) < 1e-12
print("\nVERDICT: %s" % ("witness CLOSED, control unchanged" if ok else "NOT CLOSED / control moved"))
sys.exit(0 if ok else 1)
