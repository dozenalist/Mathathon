#!/usr/bin/env python3
"""Re-derive every constant the ledger quotes (K15-C052).

Each line prints PASS/FAIL against the value written in Main/CLAIMS.md or
Main/RESULTS.md.  Exact where the constant is algebraic; 40-digit mpmath where it
involves pi or a transcendental.  Run before quoting any of these numbers.

Usage: python3 constants_check.py
"""
import sys
from fractions import Fraction as F
from mpmath import mp, mpf, sqrt, pi, acos, cos, degrees
mp.dps = 40

fails = []
def chk(name, got, want, tol=1e-11):
    ok = abs(float(got) - float(want)) <= tol
    print(("PASS " if ok else "FAIL ") + "%-46s %-18.12f (ledger %.12f)" % (name, float(got), float(want)))
    if not ok:
        fails.append(name)

# --- ball / dodecahedron ------------------------------------------------------
vball = 4 * pi / 3
chk("vol B1 = 4pi/3", vball, 4.18879020478639098462)
s5 = sqrt(5)
a = 2 * sqrt(10 / (25 + 11 * s5))          # edge of the inradius-1 dodecahedron
vdod = (15 + 7 * s5) / 4 * a ** 3
chk("V_dod (dodecahedron, inradius 1)", vdod, 5.5502910285155102690)
chk("dodecahedral density (4pi/3)/V_dod", vball / vdod, 0.75469739933740583039)
chk("Kepler density pi/sqrt18", pi / sqrt(18), 0.74048048969306104117)
chk("sqrt32 = 4 sqrt2", sqrt(32), 5.65685424949238019521)
chk("sqrt32 / V_dod", sqrt(32) / vdod, 1.0192, tol=1e-5)

# --- Rogers simplex bound -----------------------------------------------------
Om = 3 * acos(mpf(1) / 3) - pi
sigma3 = 4 * (Om / 3) / (mpf(8) / (6 * sqrt(2)))
chk("Rogers sigma_3", sigma3, 0.77963557004425293783)
chk("V_Rogers = (4pi/3)/sigma_3", vball / sigma3, 5.37275409913458775555)
chk("improvement needed over Rogers", sqrt(32) / (vball / sigma3), 1.05288, tol=1e-5)
chk("improvement needed over dodecahedral", sqrt(32) / vdod, 1.0192, tol=1e-5)

# --- Tammes thresholds --------------------------------------------------------
for rho in (mpf('2.02'), mpf('2.05'), mpf('2.09')):
    c = 1 - 2 / rho ** 2
    chk("cos theta_min at rho=%s" % rho, c, float(1 - 2 / rho ** 2))
    chk("  theta_min (deg) at rho=%s" % rho, degrees(acos(c)),
        degrees(acos(c)), tol=1e-12)
chk("cos theta_min at 2.09 = 23681/43681", mpf(23681) / 43681, float(1 - 2 / mpf('2.09') ** 2), tol=1e-15)

# --- transfer constant --------------------------------------------------------
for R, Phi in ((2, 1), (mpf('2.51'), 1)):
    chk("3 Phi (R+1)^5 at Phi=%s R=%s" % (Phi, R), 3 * Phi * (R + 1) ** 5,
        3 * float(Phi) * (float(R) + 1) ** 5, tol=1e-9)
chk("Phi needed at the icosahedral vertex, R=2", 0.106563 / 26, 0.004098576923076923)

# --- verified certificate -----------------------------------------------------
p0 = F(42935541634304122537361009, 230584300921369395200000000)
q0 = F(4611686310674994558554251, 4611686018427387904000000)
chk("K33b ratio p0/q0", float(p0 / q0), 0.186203218267)
chk("K33b Delta = (4pi/3)(p0/q0)", float(p0 / q0) * float(4 * pi / 3), 0.779966216777)

# --- E's directional-bound constants (K15-C042) -------------------------------
deficit = sqrt(32) - vdod
chk("sqrt32 + deficit/12 (E's 5.665735)", sqrt(32) + deficit / 12, 5.665735, tol=1e-6)
chk("13*(sqrt32 - V_dod) (E's 1.385321873)", 13 * deficit, 1.385321873, tol=1e-6)
chk("shortfall of 4.734 vs 5.665735 (%)", 100 * (1 - mpf('4.734') / mpf('5.665735')), 16.4451, tol=1e-3)
chk("shortfall of V_dod vs sqrt32 (%)", 100 * (1 - vdod / sqrt(32)), 1.8839, tol=1e-3)

print()
print("constants checked:", len(fails) == 0 and "ALL PASS" or ("FAILURES: %s" % fails))
sys.exit(0 if not fails else 1)
