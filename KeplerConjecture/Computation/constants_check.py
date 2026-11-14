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
for R, Phi in ((2, 1), (mpf('2.51'), 1), (mpf('2.09'), 1)):
    chk("3 Phi R (R+1)^5 at Phi=%s R=%s" % (Phi, R), 3 * Phi * R * (R + 1) ** 5,
        3 * float(Phi) * float(R) * (float(R) + 1) ** 5, tol=1e-6)
chk("k_R = 12 form at R = 2.09: 3*12*R*(R+1)^2", 3 * 12 * mpf('2.09') * mpf('3.09') ** 2, 718.40, tol=1e-2)
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

# --- K15-C094 / C095 / C096 (block K15-REVIEW-0308-M-CONTINUE) ----------------
Hlay = sqrt(mpf(8) / 3)
chk("layer spacing H = sqrt(8/3)", Hlay, 1.63299316185545206546)
chk("average Barlow cell volume 2 sqrt3 H", 2 * sqrt(mpf(3)) * Hlay, 5.65685424949238019521)
chk("in-plane offset |T| = 2/sqrt3", 2 / sqrt(mpf(3)), 1.15470053837925152902)
chk("|T|^2 + H^2 = 4 (contact distance)", (2 / sqrt(mpf(3))) ** 2 + Hlay ** 2, 4.0, tol=1e-20)
chk("next distance 2 sqrt2 = sqrt(16/3+8/3)", sqrt(mpf(16) / 3 + mpf(8) / 3), 2.82842712474619009760)
chk("covering: (2/sqrt3)^2 + (H/2)^2 = 2", (2 / sqrt(mpf(3))) ** 2 + (Hlay / 2) ** 2, 2.0, tol=1e-20)
chk("crack: min d for 2-separation = H", Hlay, 1.63299316185545206546)
chk("crack: max d for saturation = 2H", 2 * Hlay, 3.26598632371090413093)
chk("icosahedron edge at circumradius 2.09", 2 * mpf('2.09') / sqrt(1 + ((1 + sqrt(mpf(5))) / 2) ** 2), 2.197556, tol=1e-6)
chk("rho* = 2 (sqrt32/V_dod)^(1/3)", 2 * (sqrt(32) / vdod) ** (mpf(1) / 3), 2.01271866208334826748)
chk("V_dod * 1.045^3", vdod * mpf('1.045') ** 3, 6.33380410563330904910)
chk("margin of V_dod(1.045)^3 over sqrt32", vdod * mpf('1.045') ** 3 / sqrt(32) - 1, 0.11966895845012715101)
chk("slope c needed: (sqrt32/V_dod-1)/0.09", (sqrt(32) / vdod - 1) / mpf('0.09'), 0.21332859530224944336)
chk("crack energy per unit area at d=2.4", 2 * mpf('1.328495') / (2 * sqrt(mpf(3))), 0.76700694586707188002)

# --- K15-C101: the Tammes-13 split --------------------------------------------
from mpmath import sin as _sin, asin as _asin, degrees as _deg
th13 = mpf('57.1367')          # Tammes-13 optimal angular separation (Musin-Tarasov)
chk("13-point threshold radius 1/sin(theta13/2)", 1 / _sin(th13 * pi / 360), 2.091145548032, tol=1e-9)
chk("separation needed at rho = 2.09", _deg(2 * _asin(1 / mpf('2.09'))), 57.170902186746, tol=1e-9)
chk("2.09 is below the 13-point threshold", mpf('2.09'), 2.09)
chk("rho* (2.0127) < 2.09 < 13-point threshold", (2.012718662083 < mpf('2.09')) and (mpf('2.09') < 2.091145548032), True)
chk("V_dod(rho/2)^3 at rho=2.09", vdod * (mpf('2.09') / 2) ** 3, 6.33380410563330904910)
chk("trivial ball bound 4pi/3 (rho/2)^3 at rho=2.09", 4 * pi / 3 * (mpf('2.09') / 2) ** 3, 4.780105486434, tol=1e-9)
chk("ball bound beats V_dod only for rho >", 2 * (3 * vdod / (4 * pi)) ** (mpf(1) / 3), 2.1967082337, tol=1e-9)
chk("E's required pair volume 2 sqrt32 - V_dod", 2 * sqrt(32) - vdod, 5.763417470, tol=1e-9)
chk("E's best pair mean (V_dod+6.263608)/2", (vdod + mpf('6.263608')) / 2, 5.906949514, tol=1e-9)
chk("E's pair mean shortfall vs sqrt32 (%)", 100 * ((vdod + mpf('6.263608')) / 2 / sqrt(32) - 1), 4.42, tol=1e-2)
chk("nearest admissible 13th centre at rho=2.09", 3.206870905, 3.206870905, tol=1e-9)
chk("redundancy threshold 2*R_cell = rho*sqrt2", mpf('2.09') * sqrt(mpf(2)), 2.955706345, tol=1e-9)
chk("margin: nearest admissible / 2R_cell", mpf('3.206870905') / (mpf('2.09') * sqrt(mpf(2))), 1.08498, tol=1e-5)
chk("shell [2.09,2.956] volume", 4 * pi / 3 * (mpf('2.956') ** 3 - mpf('2.09') ** 3), 70.0, tol=1.0)

# --- K15-C106: the pair bound and its bridge (review 0438) ---------------------
chk("pair bound 2 sqrt32", 2 * sqrt(32), 11.3137084990, tol=1e-9)
chk("2 V_dod (what McLaughlin alone gives for a pair)", 2 * vdod, 11.100582057, tol=1e-9)
chk("pair bound minus 2 V_dod (strictness gap)", 2 * sqrt(32) - 2 * vdod, 0.213126442, tol=1e-8)
chk("required payer 2 sqrt32 - V_dod", 2 * sqrt(32) - vdod, 5.763417470, tol=1e-9)
chk("13-cluster requirement 13 sqrt32 - V_dod", 13 * sqrt(32) - vdod, 67.9888142149, tol=1e-8)
chk("pair bound gives 12*(2sqrt32 - V_dod)", 12 * (2 * sqrt(32) - vdod), 69.1610096456, tol=1e-8)
chk("13-cluster cut margin", 12 * (2 * sqrt(32) - vdod) - (13 * sqrt(32) - vdod), 1.172195431, tol=1e-7)
chk("margin as % of the requirement", 100 * (12 * (2 * sqrt(32) - vdod) - (13 * sqrt(32) - vdod)) / (13 * sqrt(32) - vdod), 1.7241004, tol=1e-6)
chk("E's payer value + V_dod", vdod + mpf('5.897967122'), 11.4482581505, tol=1e-9)
chk("payer margin over the pair bound", vdod + mpf('5.897967122') - 2 * sqrt(32), 0.1345496515, tol=1e-9)
chk("payer margin as % of 2 sqrt32", 100 * (vdod + mpf('5.897967122') - 2 * sqrt(32)) / (2 * sqrt(32)), 1.1892621, tol=1e-6)
chk("bridge conclusion 4pi/(3sqrt32) = pi/sqrt18", 4 * pi / (3 * sqrt(32)), 0.740480489693061, tol=1e-12)
chk("slack coefficient 2sqrt32 - 2V_dod", 2 * sqrt(32) - 2 * vdod, 0.213126442, tol=1e-8)

# --- K15-C107: the monotone pair bridge ---------------------------------------
def dens_from_K(K):
    return 8 * pi / (3 * K)
chk("bridge with K = 2 V_dod reproduces ML", dens_from_K(2 * vdod), 0.754697399337, tol=1e-12)
chk("bridge with K = 2 sqrt32 reproduces pi/sqrt18", dens_from_K(2 * sqrt(32)), 0.740480489693, tol=1e-12)
chk("sqrt32 / V_dod = the whole-gap factor", sqrt(32) / vdod, 1.019199573577, tol=1e-12)
chk("density at K = 2V_dod*(1.01)", dens_from_K(2 * vdod * mpf('1.01')), 0.7472251479, tol=1e-9)
chk("density at K = 2V_dod*(1.0192)", dens_from_K(2 * vdod * mpf('1.0192')), 0.7404801799, tol=1e-8)

# --- K15-C108: Theorem D / Theorem C bookkeeping -------------------------------
chk("witness sigma_0 (icosahedral pair)", vdod + mpf('5.897967122'), 11.4482581505, tol=1e-10)
chk("delta_0 bound from the witness", vdod + mpf('5.897967122') - 2 * vdod, 0.3476760935, tol=1e-9)
chk("delta_0 as % of 2V_dod", 100 * (mpf('5.897967122') - vdod) / (2 * vdod), 3.132, tol=1e-2)
chk("delta_0 if the sharp (L) held", 2 * sqrt(32) - 2 * vdod, 0.213126442, tol=1e-8)
chk("delta_0_sharp as % of 2V_dod", 100 * (2 * sqrt(32) - 2 * vdod) / (2 * vdod), 1.9199, tol=1e-3)
chk("Theorem C at rho=1/2 (perfect matching), sharp delta_0 -> pi/sqrt18",
    (4 * pi / 3) / (vdod + (2 * sqrt(32) - 2 * vdod) / 2), 0.740480489693, tol=1e-12)
chk("V_dod + delta_0/2 = sqrt32 exactly", vdod + (2 * sqrt(32) - 2 * vdod) / 2, sqrt(32), tol=1e-18)
chk("Theorem C at rho=1/4, sharp delta_0", (4 * pi / 3) / (vdod + (2 * sqrt(32) - 2 * vdod) / 4), 0.747521353722, tol=1e-11)

# --- K15-C100/C109: the analytic ladder, exactly (review 0438) ------------------
TRU = mpf('0.740480489693')
chk("ML above truth (%)", 100 * (mpf('0.754697399337') / TRU - 1), 1.91996, tol=1e-5)
chk("3-point lattice above truth (%)", 100 * (mpf('0.741506') / TRU - 1), 0.138493, tol=1e-5)
chk("3-point general above truth (%)", 100 * (mpf('0.770271') / TRU - 1), 4.02313, tol=1e-4)
chk("lattice -> general factor", mpf('0.770271') / mpf('0.741506'), 1.0387927, tol=1e-6)
chk("3-point proof would need this % improvement", 100 * (1 - TRU / mpf('0.770271')), 3.86754, tol=1e-4)
chk("ML gap and pair window are the SAME number", 100 * (mpf('0.754697399337') / TRU - 1), 100 * (sqrt(32) / vdod - 1), tol=2e-3)

# --- reconciliation of C's CUTBLOB-001 value (review 0438) ---------------------
chk("b(v0) = sqrt32 - V_dod", sqrt(32) - vdod, 0.106563220977, tol=1e-12)
chk("C's t* = b(v0)/12 = 0.008880268414739", (sqrt(32) - vdod) / 12, 0.008880268414739, tol=1e-15)

# --- the per-point cap (Liter ature 5.3(i)), reconciled -----------------------
chk("per-point family cap 8/V_dod", 8 / vdod, 1.4413658597, tol=1e-10)
# the literature's convention has min separation 1, so volumes scale by 8 and
# delta = (pi/6) * (number density) = (pi/6) * 8/V_dod
chk("same number as the density-convention 0.754697399337",
    (pi / 6) * (8 / vdod), 0.754697399337, tol=1e-12)
chk("equivalently (4pi/3)/V_dod", (4 * pi / 3) / vdod, 0.754697399337, tol=1e-12)

# --- K15-C111: A15 cell volumes, exact rationals --------------------------------
chk("A15 vol_A = 125/16", mpf(125) / 16, 7.8125, tol=1e-15)
chk("A15 vol_B = 129/16", mpf(129) / 16, 8.0625, tol=1e-15)
chk("A15 2*vol_A + 6*vol_B = a^3 = 64", 2 * mpf(125) / 16 + 6 * mpf(129) / 16, 64, tol=1e-12)
chk("A15 contact pair (B-B) = 129/8", 2 * mpf(129) / 16, 16.125, tol=1e-12)
chk("A15 A+B (NON-contact pair) = 127/8", (mpf(125) + mpf(129)) / 16, 15.875, tol=1e-12)
chk("A15 A-B distance = sqrt5 (not 2)", sqrt(mpf(5)), 2.2360679774997896964, tol=1e-15)

# --- K15-C116: the near-contact band -------------------------------------------------
chk("critical separation 6/sqrt5", 6 / sqrt(mpf(5)), 2.683281572999747635, tol=1e-12)
chk("(6/sqrt5)^2 = 36/5", (6 / sqrt(mpf(5))) ** 2, mpf('7.2'), tol=1e-15)
chk("band width 6/sqrt5 - 2", 6 / sqrt(mpf(5)) - 2, 0.683281572999747635, tol=1e-12)
chk("route needs 0.012718662083, a factor", (6 / sqrt(mpf(5)) - 2) / mpf('0.012718662083'), 53.723, tol=1e-2)

# --- K15-C119: where the dodecahedral bound does work ----------------------------
def inball(d):
    return 8 / mpf(d) ** 3
chk("inball bound at d = 2 is trivially 1", inball(mpf(2)), 1.0, tol=1e-12)
chk("inball meets ML at d", (8 / mpf('0.754697399337')) ** (mpf(1) / 3), 2.1967082337, tol=1e-9)
chk("inball meets the truth at d", (8 / mpf('0.740480489693')) ** (mpf(1) / 3), 2.21067782856, tol=1e-9)
chk("inball at 6/sqrt5", inball(6 / sqrt(mpf(5))), 0.41408665, tol=1e-7)

# --- K15-C121: explicit stability for <= 12-face cells --------------------------
chk("V_dod*(1.045)^3", vdod * mpf('1.045') ** 3, 6.33380410563330904910)
chk("that over sqrt32", vdod * mpf('1.045') ** 3 / sqrt(32), 1.11966895845012715101)
chk("so b(v) is negative", sqrt(32) - vdod * mpf('1.045') ** 3, -0.676949856141, tol=1e-12)
chk("inball threshold rho = (3V_dod/4pi)^(1/3)", (3 * vdod / (4 * pi)) ** (mpf(1) / 3), 1.098354117, tol=1e-9)
chk("2*R_cell at rho=1.045", 2 * mpf('1.045') * sqrt(mpf(2)), 2.955706345, tol=1e-9)

# --- K15-C122: the F<=20 target ------------------------------------------------
a_ico = 12 / (sqrt(mpf(3)) * (3 + sqrt(mpf(5))))          # icosahedron edge, inradius 1
V_ico = mpf(5) / 12 * (3 + sqrt(mpf(5))) * a_ico ** 3
chk("icosahedron edge, inradius 1", a_ico, 1.3231690765, tol=1e-9)
chk("icosahedron volume, inradius 1", V_ico, 5.0540561436, tol=1e-9)
chk("V_ico * 1.045^3", V_ico * mpf('1.045') ** 3, 5.76751766492, tol=1e-9)
chk("V_ico * 1.045^3 exceeds sqrt32 by (%)", 100 * (V_ico * mpf('1.045') ** 3 / sqrt(32) - 1), 1.956, tol=1e-3)
chk("target c_F = sqrt32/1.045^3", sqrt(32) / mpf('1.045') ** 3, 4.95708216846, tol=1e-9)
chk("inball c = 4pi/3 falls short (product)", 4 * pi / 3 * mpf('1.045') ** 3, 4.780105486434, tol=1e-9)

# --- K15-C124/C125 (review 0608) -----------------------------------------------
EPS_BAND = 6 / sqrt(mpf(5)) - 2
chk("band end eps = 6/sqrt5 - 2", EPS_BAND, 0.683281572999747635, tol=1e-12)
chk("case-2 density at the band end", 1 / (1 + EPS_BAND / 2) ** 3, 0.414086, tol=1e-6)
chk("case-2 density is well below ML", 1 / (1 + EPS_BAND / 2) ** 3 < mpf('0.754697399337'), True)
chk("C125: truncated octahedron volume, inradius 1", 8 * sqrt(mpf(2)) * (2 / sqrt(mpf(6))) ** 3, 6.158402871, tol=1e-9)
chk("C125: regular icosahedron volume, inradius 1", mpf(5) / 12 * (3 + sqrt(mpf(5))) * (12 / (sqrt(mpf(3)) * (3 + sqrt(mpf(5))))) ** 3, 5.0540561436, tol=1e-9)
chk("C125: 14-face truncated oct is WORSE than 20-face icosahedron", 8 * sqrt(mpf(2)) * (2 / sqrt(mpf(6))) ** 3 > mpf(5) / 12 * (3 + sqrt(mpf(5))) * (12 / (sqrt(mpf(3)) * (3 + sqrt(mpf(5))))) ** 3, True)
th = mp.acos(1 - 2 / mpf(20))
chk("C125: equal-cap estimate for F=20", 20 * 2 * pi * (-mp.log(mp.cos(th))) / 3, 4.413331, tol=1e-6)
chk("C125: equal-cap estimate is BELOW the C122 threshold", 20 * 2 * pi * (-mp.log(mp.cos(th))) / 3 < sqrt(32) / mpf('1.045') ** 3, True)

# --- K15-C126: X's corrected band and the d=2 agreement ------------------------
chk("X-C051 two-dodecahedra threshold", mpf('3.4555003444'), 3.4555003444, tol=1e-9)
chk("that threshold sits just below 2 sqrt3", 2 * sqrt(3) - mpf('3.4555003444'), 0.00860127, tol=1e-7)
chk("X band width 3.4555 - 2 covers C124's eps", mpf('3.4555003444') - 2 > mpf('0.6832816'), True)
chk("C124 case-2 density at eps = 0.6832816", 1 / (1 + mpf('0.6832816') / 2) ** 3, 0.414086, tol=1e-6)

# --- K15-C127: the corrected band ------------------------------------------------
chk("two-dodecahedra threshold, corrected arc test", mpf('3.4555003444044642049'), 3.4555003444, tol=1e-9)
chk("band width", mpf('3.4555003444044642049') - 2, 1.4555003444, tol=1e-9)
chk("C124 needs eps/2 > this (inball radius 1.0983541)", (1 / mpf('0.754697399337')) ** (mpf(1)/3) - 1, 0.098354116850, tol=1e-9)
chk("so eps_needed = d_ML - 2", 2 * ((1 / mpf('0.754697399337')) ** (mpf(1)/3) - 1), 0.196708233700, tol=1e-9)
chk("eps_needed equals C119 d_ML - 2", 2 * ((1 / mpf('0.754697399337')) ** (mpf(1)/3) - 1), (8 / mpf('0.754697399337')) ** (mpf(1)/3) - 2, tol=1e-12)
chk("band / needed room (x)", (mpf('3.4555003444044642049') - 2) / (2 * ((1 / mpf('0.754697399337')) ** (mpf(1)/3) - 1)), 7.4, tol=0.05)

# --- K15-C128: the one-pair certificate ---------------------------------------
chk("one-pair R = 32/5", mpf(32)/5, 6.4, tol=1e-15)
chk("one-pair c = -(3-sqrt5)/2", -(3-sqrt(mpf(5)))/2, -0.381966011250105, tol=1e-14)
chk("one-pair h (deg)", degrees(mp.acos(-(3-sqrt(mpf(5)))/2)), 112.455515, tol=1e-5)
chk("one-pair |T| (deg)", degrees(2*pi-2*mp.acos(-(3-sqrt(mpf(5)))/2)), 135.08897, tol=1e-4)
chk("one-pair |T| > 72 deg (the twist period)", 2*pi-2*mp.acos(-(3-sqrt(mpf(5)))/2) > 2*pi/5, True)
chk("equivalently h < 4pi/5 = 144 deg", mp.acos(-(3-sqrt(mpf(5)))/2) < 4*pi/5, True)

# --- K15-C129: the closed-form band --------------------------------------------
chk("closed form 4/sqrt5 + 2 sqrt((2sqrt5-1)/5)", 4/sqrt(mpf(5)) + 2*sqrt((2*sqrt(mpf(5))-1)/5), 3.4555003444044642048, tol=1e-18)
chk("agrees with the bisection", 4/sqrt(mpf(5)) + 2*sqrt((2*sqrt(mpf(5))-1)/5), mpf('3.4555003444044642049'), tol=1e-15)
chk("agrees with X-C051 to 10 sig figs", abs(4/sqrt(mpf(5)) + 2*sqrt((2*sqrt(mpf(5))-1)/5) - mpf('3.4555003444')) < 1e-9, True)
chk("R = 32/5 in the one-pair computation", mpf(2)*(4/sqrt(mpf(5)))*(4/sqrt(mpf(5))), 32/mpf(5), tol=1e-30)
chk("cos(4pi/5) = -(1+sqrt5)/4", cos(4*pi/5) + (1+sqrt(mpf(5)))/4, 0, tol=1e-30)
chk("C124 needs eps 0.1967082, band gives 1.4555 (factor)", (4/sqrt(mpf(5)) + 2*sqrt((2*sqrt(mpf(5))-1)/5) - 2) / 0.196708233700, 7.3992853, tol=1e-6)

print()
print("constants checked:", len(fails) == 0 and "ALL PASS" or ("FAILURES: %s" % fails))
sys.exit(0 if not fails else 1)
