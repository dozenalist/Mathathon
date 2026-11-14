#!/usr/bin/env python3
"""
verify.py -- checks for proof.md (swarm smwg019eu, member m2, direction d5).

Every numerical decision is made in interval arithmetic (mpmath.iv = MPFI: each operation
returns an interval containing the exact result).  Truncated series are truncated far
beyond the stated tolerance and the truncation is charged to the tolerance column.

Run:  python3 verify.py       (exit status 0 iff every check passes)

  A  algebraic constants used in the document
  B  the benchmark table of Section 4, each row from its defining quantity
  C  the Poisson summation mechanism of Lemma 1.3, explicit cases
  D  the elementary local-count table, Corollary 2.3
  E  Proposition 3.3 and the local-constant obstruction 3.2(i)
"""
from mpmath import iv
import sys
from sympy import Rational, floor

iv.dps = 60
PASS, FAIL = [], []

def I(x):
    return iv.mpf(str(x))

def show(t, nd=18):
    return f"[{iv.nstr(t.a, nd)}, {iv.nstr(t.b, nd)}]"

def check(name, t, claimed, tol, note=""):
    lo, hi = I(claimed) - I(tol), I(claimed) + I(tol)
    ok = (t.a >= lo.b) and (t.b <= hi.a)
    (PASS if ok else FAIL).append(name)
    print(f"{'PASS' if ok else 'FAIL'}  {name:<38} {show(t):<44} claim {claimed} +- {tol}")
    if note:
        print(f"      {note}")
    return ok

def check_gt(name, big, small, note=""):
    ok = big.a > small.b
    (PASS if ok else FAIL).append(name)
    print(f"{'PASS' if ok else 'FAIL'}  {name:<38} {show(big)} > {show(small)}")
    if note:
        print(f"      {note}")
    return ok

VOLB1 = I(4) * iv.pi / I(3)

print("=" * 104)
print("A. algebraic constants used in proof.md")
print("=" * 104)
pi_over_sqrt18 = iv.pi / iv.sqrt(I(18))
check("A1 delta_truth = pi/sqrt18", pi_over_sqrt18, "0.740480489693", "5e-13")
check("A2 c_truth = 1/(4 sqrt2)", I(1) / (I(4) * iv.sqrt(I(2))), "0.176776695", "5e-10")
check("A2' c = 3delta/(4pi) on the truth", I(3) * pi_over_sqrt18 / (I(4) * iv.pi),
      "0.176776695", "5e-10", "normalisation consistency, Section 0.2")
s5 = iv.sqrt(I(5))
a_edge = I(2) / iv.sqrt((I(25) + I(11) * s5) / I(10))
V_dodec = (I(15) + I(7) * s5) / I(4) * a_edge ** 3
V_dodec2 = I(2) * (I(15) + I(7) * s5) * (I(10) / (I(25) + I(11) * s5)) ** (I(3) / I(2))
check("A3 V_dodec(inradius 1), edge form", V_dodec, "5.550291028515", "5e-12")
check("A3' V_dodec, radical closed form", V_dodec2, "5.550291028515", "5e-12")
four_sqrt2 = I(4) * iv.sqrt(I(2))
check("A4 4 sqrt 2 (Gauss covolume)", four_sqrt2, "5.656854249492", "5e-12")
check("A4' vol(B_1) = 4 pi/3", VOLB1, "4.188790204786", "5e-12")

print()
print("=" * 104)
print("B. benchmark table (Section 4): delta <-> c, each row from its defining quantity")
print("=" * 104)
check("B1 delta truth = pi/sqrt18", pi_over_sqrt18, "0.740480489693", "5e-13")
check("B1 c truth = 3delta/(4pi)", I(3) * pi_over_sqrt18 / (I(4) * iv.pi), "0.176776695", "5e-10")
c_HM, delta_HM = I(1) / V_dodec, VOLB1 / V_dodec
check("B2 Hales-McLaughlin c = 1/V0", c_HM, "0.180170732", "5e-10")
check("B2 Hales-McLaughlin delta = 4pi/(3V0)", delta_HM, "0.754697399337", "5e-13")
check("B2' consistency c = 3delta/(4pi)", I(3) * delta_HM / (I(4) * iv.pi), "0.180170732", "5e-10")
delta_CDS = I("0.770270440")
check("B3 CDS c = 3delta/(4pi)", I(3) * delta_CDS / (I(4) * iv.pi), "0.183888522", "5e-9")
V_Muder = I("5.41848")
c_M, d_M = I(1) / V_Muder, VOLB1 / V_Muder
check("B4 Muder c = 1/V0", c_M, "0.1845536", "5e-7",
      "NOTE: the task statement prints 0.184553; V0 = 5.41848 implies 0.1845536")
check("B4 Muder delta = 4pi/(3V0)", d_M, "0.7730563", "5e-7",
      "NOTE: the task statement prints 0.773055; V0 = 5.41848 implies 0.77305632")
delta_CE = I("0.779746762")
c_CE = I(3) * delta_CE / (I(4) * iv.pi)
check("B5 CE c = 3delta/(4pi)", c_CE, "0.186150827", "5e-9")
check("B6 Rogers c = 3delta/(4pi)", I(3) * I("0.779636") / (I(4) * iv.pi), "0.186124", "5e-6")
check_gt("B7 delta_HM < delta_CDS", delta_CDS, delta_HM)
check_gt("B7' delta_CDS < delta_Muder", d_M, delta_CDS)
check_gt("B7'' delta_Muder < delta_CE", delta_CE, d_M)

print()
print("=" * 104)
print("C. Poisson mechanism of Lemma 1.3, explicit cases;  f(x) = exp(-pi|x|^2), so fhat = f")
print("=" * 104)
# C1: L = 2Z^3, V = 8, k = 1, v = 0.  (PS): sum_L f = (1/V) sum_{L*} fhat.
s_even = I(1)
for k in range(1, 16):
    s_even += I(2) * iv.exp(-I(4) * iv.pi * I(k) ** 2)     # truncation < 1e-1000
S_lat = s_even ** 3
s_dual = I(0)
for j in range(-25, 26):
    s_dual += iv.exp(-iv.pi * (I(j) / I(2)) ** 2)          # truncation < 1e-230
dual_sum = s_dual ** 3 / I(8)
check("C1 (PS) sum_L f = (1/V) sum_L* fhat", S_lat - dual_sum, "0", "1e-50",
      "Lemma 1.3(i), k = 1, v = 0; series truncation errors < 1e-230")
check_gt("C2 sum_L f >= fhat(0)/V", S_lat, I(1) / I(8), "Lemma 1.3(ii), k = 1")
# C3: an admissible k = 2 periodic packing: L = 4Z^3 (V = 64), v_1 = 0, v_2 = (2,2,2).
# min distance = min(4, 2 sqrt 3) = 3.464 >= 2  (nearest images of (2,2,2) are at 2 sqrt 3).
s4 = I(1)
for k in range(1, 6):
    s4 += I(2) * iv.exp(-iv.pi * (I(4) * I(k)) ** 2)
S_all = s4 ** 3
Sw = I(0)
for i in range(-3, 4):
    for j in range(-3, 4):
        for k in range(-3, 4):
            d2 = (I(4) * I(i) + I(2)) ** 2 + (I(4) * I(j) + I(2)) ** 2 + (I(4) * I(k) + I(2)) ** 2
            Sw += iv.exp(-iv.pi * d2)
S2 = S_all + I(2) * Sw
check_gt("C3 k=2: S(f) >= k^2 fhat(0)/V", S2, I(4) / I(64),
         "Lemma 1.3(ii): k^2 fhat(0)/V = 4/64 = 0.0625")
check_gt("C4 k=2: S(f) <= k f(0)", I(2), S2, "Lemma 1.3(iii): k f(0) = 2")

print()
print("=" * 104)
print("D. elementary local counts, Corollary 2.3: n(delta) = floor((3+delta)^3) - 1")
print("=" * 104)
for d in ["0.001", "0.01", "0.036", "0.0366", "0.04", "0.07", "0.1", "0.2", "0.5", "1.0"]:
    n = int(floor((Rational(3) + Rational(d)) ** 3)) - 1     # exact integer arithmetic
    check(f"D n(delta={d})", I(n), str(n), "0", "exact")
def cbrt(x):
    return iv.exp(iv.log(x) / I(3))
t26, t27, t28 = cbrt(I(28)) - I(3), cbrt(I(29)) - I(3), cbrt(I(30)) - I(3)
print(f"      thresholds (Corollary 2.3): n = 26 for 0 < delta < 28^(1/3)-3 = {iv.nstr(t26.a, 12)}")
print(f"                                  n = 27 up to 29^(1/3)-3 = {iv.nstr(t27.a, 12)}")
print(f"                                  n = 28 up to 30^(1/3)-3 = {iv.nstr(t28.a, 12)}")
check("D threshold 28^(1/3)-3", t26, "0.0365889719", "1e-9")
check("D threshold 29^(1/3)-3", t27, "0.0723168257", "1e-9")

print()
print("=" * 104)
print("E. Proposition 3.3 and the local-constant obstruction 3.2(i)")
print("=" * 104)
inv_CE = I(1) / c_CE
check("E1 fhat(0)/f(0) at the CE optimum", inv_CE, "5.3719879", "5e-6")
check("E2 (4sqrt2)/(CE ratio)", four_sqrt2 / inv_CE, "1.0530281", "5e-6",
      "any refutation of the truncation identity must beat the two-point optimum by this")
local_const = I(1) / VOLB1
check("E3 1/vol(B_1) = 3/(4pi)", local_const, "0.238732414638", "5e-12")
check("E4 (1/volB1)*(4sqrt2)", local_const * four_sqrt2, "1.350474", "5e-6",
      "the factor by which every local/Lipschitz argument misses (3.2)")
check_gt("E5 local constant exceeds 1/V", local_const, I(1) / four_sqrt2)
for w in ["1e-1", "1e-2", "1e-3", "1e-4"]:
    print(f"      shell example 3.2(ii): w = {w:<7} ratio = {iv.nstr((I(12)/(I(8)*iv.pi*I(w))).a, 10)}")

print()
print("=" * 104)
print(f"SUMMARY: {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    for f in FAIL:
        print("   FAILED:", f)
    sys.exit(1)
print("ALL CHECKS PASSED")
