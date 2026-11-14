"""
Self-audit of the rational interval primitives used by tammes13_enclosure.py.

Two independent checks:
 (1) SOUNDNESS: every interval returned must CONTAIN the true value, computed
     independently in high-precision floating point (mpmath).  This catches
     wrong-direction monotonicity and swapped endpoints, which are the failure
     modes that still produce plausible-looking numbers.
 (2) SENSITIVITY: a deliberately corrupted primitive (endpoints swapped) must be
     DETECTED by check (1).  If a corruption passes, the audit is worthless.

Status: audit of implementation, not a proof. Run: python3 interval_selfaudit.py
"""
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 60

# import the primitives under test
import importlib.util, sys
spec = importlib.util.spec_from_file_location("enc", "Experimental/scripts/tammes13_enclosure.py")
enc = importlib.util.module_from_spec(spec)
sys.modules["enc"] = enc
spec.loader.exec_module(enc)          # module-level only; main() guarded by __main__

Iv = enc.Iv

def true_cos(x): return mp.cos(mp.mpf(x.numerator)/x.denominator)
def true_sin(x): return mp.sin(mp.mpf(x.numerator)/x.denominator)

def contains(iv, val, tol=mp.mpf('1e-40')):
    lo = mp.mpf(iv.lo.numerator)/iv.lo.denominator
    hi = mp.mpf(iv.hi.numerator)/iv.hi.denominator
    return (lo - tol) <= val <= (hi + tol)

fails = []
def check(name, iv, val):
    if not contains(iv, val):
        fails.append(f"{name}: {iv} does not contain {mp.nstr(val,25)}")

# ---- (1) soundness on a grid of rationals in the ranges actually used ----
xs = [F(k,100) for k in range(101, 160)]          # 1.01 .. 1.59
for x in xs:
    c = enc._taylor_cos(x); s = enc._taylor_sin(x)
    check(f"cos({float(x):.2f})", c, true_cos(x))
    check(f"sin({float(x):.2f})", s, true_sin(x))
print(f"soundness (point) : {len(xs)*2} interval checks, failures = {len(fails)}")

# ---- interval-valued monotone wrappers ----
f2 = 0
for k in range(100, 150):
    lo, hi = F(k,100), F(k+1,100)
    ci = enc.cos_iv(lo,hi); si = enc.sin_iv(lo,hi)
    # cos decreasing: endpoints bracket
    if not (contains(ci, true_cos(lo)) and contains(ci, true_cos(hi))): f2 += 1
    if not (contains(si, true_sin(lo)) and contains(si, true_sin(hi))): f2 += 1
    ti = enc.tan_iv(lo,hi)
    if not (contains(ti, true_sin(lo)/true_cos(lo)) and contains(ti, true_sin(hi)/true_cos(hi))): f2 += 1
print(f"soundness (interval monotone wrappers): endpoint failures = {f2}")
if f2: fails.append(f"{f2} monotone-wrapper endpoint failures")

# ---- (2) sensitivity: corrupt cos_iv by swapping the monotonicity direction ----
def corrupted_cos_iv(lo, hi):
    # Subtle corruption: use cos(hi) for BOTH endpoints.  This is the classic
    # "wrong monotonicity direction" error: the result is a perfectly ordered,
    # plausible interval that is too tight on the left.  A naive ordering assert
    # does NOT catch it; only containment testing does.
    c_lo = enc._taylor_cos(hi)
    return Iv(c_lo.lo, c_lo.hi)

detected = 0
for k in range(100, 150):
    lo, hi = F(k,100), F(k+1,100)
    bad = corrupted_cos_iv(lo,hi)
    if not (contains(bad, true_cos(lo)) and contains(bad, true_cos(hi))):
        detected += 1
print(f"sensitivity: corrupted cos_iv detected in {detected}/50 intervals "
      f"({'OK' if detected>0 else 'AUDIT IS BLIND'})")
if detected == 0: fails.append("audit cannot detect a swapped-endpoint corruption")

# ---- (2b) ordering swap is caught structurally by the Iv constructor ----
try:
    Iv(F(3), F(1))
    print("ordering: constructor did NOT reject lo > hi  (BAD)")
    fails.append("Iv accepts lo > hi")
except AssertionError:
    print("ordering: constructor rejects lo > hi  (structural guard present)")

# ---- (3) pi enclosure ----
pi_lo = mp.mpf(333)/106; pi_hi = mp.mpf(355)/113
print(f"pi: 333/106 = {mp.nstr(pi_lo,20)} < pi = {mp.nstr(mp.pi,20)} < {mp.nstr(pi_hi,20)} : "
      f"{pi_lo < mp.pi < pi_hi}")

print()
if fails:
    print("AUDIT FAILURES:")
    for f in fails: print("  -", f)
    sys.exit(1)
print("AUDIT PASSED: enclosures contain the true values; corruption is detectable.")
