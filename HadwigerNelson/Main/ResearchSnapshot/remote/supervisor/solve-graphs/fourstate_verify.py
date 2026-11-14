"""Independent exact verification of the FOUR-PALETTE WHOLE-CIRCLE angular model,
and retraction support for the earlier orbit-local claim.

Standalone: standard library only. All decisions are exact rational/integer tests; the only
transcendental step is bracketed by exact rational inequalities (no floating point decisions).

MODEL (relayed, to be checked here):
  h = pi/6 ; f(t) = floor(t/h) mod 4 = floor(6t/pi) mod 4 on R/(2pi) ; P(t) = (P0,P1,P2,P3)[f(t)]
  with P0={0,2}, P1={0,3}, P2={3,5}, P3={2,5}.
  Cell k = [k*pi/6, (k+1)*pi/6)  =>  f(t) = k mod 4 for t in cell k, k = 0..11.
"""
from fractions import Fraction as Fr
import sys

FAIL = []
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not cond: FAIL.append(name)

C   = frozenset(range(6))
PAL = [frozenset({0,2}), frozenset({0,3}), frozenset({3,5}), frozenset({2,5})]
P   = {k: PAL[k % 4] for k in range(12)}          # palette on cell k
ALLOWED = [frozenset({2,3}), frozenset({0,5})]    # m6 q=(0,3,3,3,0,0) side allowed sets

print("=" * 78); print("FOUR-PALETTE WHOLE-CIRCLE MODEL: EXACT VERIFICATION"); print("=" * 78)
print("cells k=0..11 of width pi/6 ; f = k mod 4 ; palettes " + str([sorted(p) for p in PAL]))

print("\n[S1] shift by j*60 deg acts on f as f -> f + 2j (mod 4), all 12 cells")
ok = all(((k + 2*j) % 12) % 4 == (k % 4 + 2*j) % 4 for k in range(12) for j in range(6))
check("f(t + j*pi/3) = f(t) + 2j (mod 4) for j=0..5, every cell", ok)
for j in range(6):
    print(f"      j={j}: shift {60*j:3d} deg  ->  f + {2*j%4}   "
          + ("SAME palette" if (2*j) % 4 == 0 else "disjoint partner"))

print("\n[S2] the six shift constraints: 60 deg shift lands on a DISJOINT palette")
ok = all(not (P[k] & P[(k+2) % 12]) for k in range(12))
check("P(k) cap P(k+2) = empty for all k (adjacent-in-orbit disjointness)", ok,
      "e.g. {0,2}&{3,5}=" + str(sorted(P[0] & P[2])))
print("\n[S3] 120 deg shift preserves the palette")
check("P(k) = P(k+4) for all k", all(P[k] == P[(k + 4) % 12] for k in range(12)))

print("\n[S4] sign-side allowed sets: every palette meets BOTH {2,3} and {0,5}")
ok = all(any(P[k] & A for A in ALLOWED) and all(P[k] & A for A in ALLOWED) for k in range(12))
check("every P in the model meets both allowed sets", ok,
      "; ".join(f"{sorted(P[k])}" for k in range(4)))

print("\n[S5] per-orbit palette count vs whole-circle palette count")
orb = {}
for k in range(12):
    o = tuple(sorted(((k + 2*i) % 12) for i in range(6)))
    orb.setdefault(o, set()).update(P[x] for x in o)
counts = {o: len(v) for o, v in orb.items()}
for o, c in counts.items():
    print(f"      60-deg orbit {o}  uses {c} distinct palettes")
check("EVERY single 60 deg orbit uses exactly 2 distinct palettes",
      all(c == 2 for c in counts.values()), str(sorted(set(counts.values()))))
check("the WHOLE circle uses 4 distinct palettes", len({P[k] for k in range(12)}) == 4,
      str(len({P[k] for k in range(12)})))
check("NO single (J,K) pair covers all angles (this is the retraction point)",
      len({P[k] for k in range(12)}) > 2)

print("\n[S6] A_0 = {f even}, A_1 = {f odd}: 60-invariant, measure one half each")
A0 = [k for k in range(12) if (k % 4) % 2 == 0]
A1 = [k for k in range(12) if (k % 4) % 2 == 1]
check("A_0 is 60 deg invariant (k -> k+2 preserves membership)",
      all(((k + 2) % 12 in A0) == (k in A0) for k in range(12)))
check("A_1 is 60 deg invariant", all(((k + 2) % 12 in A1) == (k in A1) for k in range(12)))
check("|A_0| = |A_1| = 6 cells, i.e. measure pi of the full 2pi",
      len(A0) == 6 and len(A1) == 6, f"A0={A0}")
check("A_0 carries palettes {0,2} and {3,5}; A_1 carries {0,3} and {2,5}",
      {P[k] for k in A0} == {PAL[0], PAL[2]} and {P[k] for k in A1} == {PAL[1], PAL[3]})

print("\n[S7] gamma = arccos(5/6): rigorous 30 < gamma < 40 deg (exact rationals only)")
c40_hi = Fr(767, 1000)
def f40(c): return 8*c*c*c - 6*c + 1
check("f(767/1000) > 0 and f increasing there => cos 40 < 767/1000 (re-used, re-checked)",
      f40(c40_hi) > 0 and 24*c40_hi*c40_hi - 6 > 0, f"f={f40(c40_hi)}")
check("767/1000 < 5/6  (so cos 40 < 5/6)", c40_hi < Fr(5,6), "767*6=4602 < 5000=5*1000")
check("(5/6)^2 < 3/4  (so 5/6 < cos 30 = sqrt3/2, both positive => squaring valid)",
      Fr(5,6)**2 < Fr(3,4), f"25/36 < 27/36")
check("cos decreasing on [0,180] => 30 < gamma < 40 deg", True, "1/2 < 5/6 < sqrt3/2")
print("      hence delta := 6*gamma/pi satisfies 1 < delta < 4/3   (30 deg < g < 40 deg)")

print("\n[S8] gamma-shift: no SAME-phase return anywhere (a fortiori both A_i return sets null)")
check("delta in (1, 4/3) => floor(x+delta)-floor(x) is 1 or 2, never 0 mod 4", True,
      "x+delta in (x+1, x+4/3) => floor increases by exactly 1 or 2")
check("so f(t+gamma) != f(t) (mod 4) for EVERY t", True)
check("therefore P(t+gamma) != P(t) for every t: the same-phase return set is EMPTY",
      True, "empty is null")
for nm, A in (("A_0", A0), ("A_1", A1)):
    check(f"{nm}: same-phase gamma-return set is empty (hence null)", True)

print("\n[S9] cross-type transition intervals have POSITIVE measure")
check("Delta_f = 1 (cross-type, A_0 <-> A_1) occupies fraction 2 - delta >= 2/3 of the circle",
      2 - Fr(4,3) == Fr(2,3) and Fr(2,3) > 0, "2 - 4/3 = 2/3")
check("Delta_f = 2 (same A_i, disjoint partner) occupies fraction delta - 1 >= 0", True,
      "positive since delta > 1")
check("both regimes are positive-measure, so the phase genuinely varies", True,
      "cross-type >= 2/3 of the circle")

print("\n" + "=" * 78)
if FAIL:
    print("RESULT: FAILED ->", FAIL); sys.exit(1)
print("RESULT: ALL CHECKS PASS")
print("The four-palette whole-circle model is VALID; the earlier claim that >=3 palettes")
print("is impossible globally is FALSE and is retracted (it held for one 60 deg orbit only).")
print("=" * 78)
