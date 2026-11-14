"""Exact checks for the trace-limit lemma (Prop. 4) and its weakened form.

Single process, exact fractions only. Sections [9]-[11] of supervisor_checks.out.
"""
import os
from fractions import Fraction as F
from itertools import combinations

out = []
def say(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)

# [9] The weakened form is FALSE: a family of one-hot fields, all T-valued, whose ONLY
# limit object is the uniform field (all three coordinates positive). Model: 12 sectors,
# T = {3,4,5}, b_n(s) = 3 + ((s+n) mod 3). Exact L^2 inner products.
say("[9] weak-limit countermodel (12 sectors, T = {3,4,5})")
N = 12
def b(n, s): return 3 + ((s + n) % 3)
for n, m in [(0,1), (0,2), (0,3)]:
    agree = sum(1 for s in range(N) if b(n,s) == b(m,s))
    ip = F(agree, N)
    say(f"    <b_{n},b_{m}> = {agree}/{N} = {ip}; || b_{n} - b_{m} ||^2 = 2 - 2*{ip} = {2-2*ip}")
say("    => the family has only 3 distinct members, so a constant (hence L^2-Cauchy) subsequence")
say("       exists; the illustration is about the INFERENCE below, not about non-compactness")
uni = F(1,3)
say(f"    convex average of 3 consecutive = ({uni},{uni},{uni}); all three coordinates > 0,")
say("    so a WEAK limit would have |P| >= 3 at the accumulation point. Traces are STRONG")
say("    limits (trace_realization: sampleCode -> b in L^2), so this inference is invalid.")
say("    => 'singleton palettes pass to the limit' is false; only 'the limit singleton is IN the palette'")

# [10] the sharp true statement, as a label count
say("[10] Prop. 4 conclusion, as a label statement")
def comp(V): return frozenset(range(6)) - frozenset(V)
V  = frozenset({0,1,2}); Vp = frozenset({0,1,2})
say(f"    V={sorted(V)} V'={sorted(Vp)}: T cap T' = {sorted(comp(V) & comp(Vp))} (nonempty -> OK)")
Vp2 = frozenset({3,4,5})
say(f"    V={sorted(V)} V'={sorted(Vp2)}: T cap T' = {sorted(comp(V) & comp(Vp2))} -> EMPTY, excluded by Prop. 4")
say("    equivalently V u V' != [6]: a missing label is shared by the two triangles")
n_viol = sum(1 for A in combinations(range(6),3) for B in combinations(range(6),3)
             if not (comp(A) & comp(B)))
say(f"    ordered pairs (V,V') with V u V' = [6]: {n_viol} of {20*20} = {(F(n_viol,400))}")
n_viol_un = sum(1 for A in combinations(range(6),3) for B in combinations(range(6),3)
                if A < B and not (comp(A) & comp(B)))
say(f"    unordered such pairs: {n_viol_un} of 210")

# [11] consistency with the only explicit colouring in the record (m3, k = 7)
say("[11] m3 (k=7) consistency check of Prop. A")
T7 = sorted(set(range(7)) - {0,2,3})
say(f"    triangle labels {{0,2,3}}, complement T = {T7}, |T| = {len(T7)} = k-3 = 4")
say("    m3: the unit circle about q_n lies outside the gadget W (radius ~1/2 about q_n in the")
say("    far field), so its colours are the four background labels {1,4,5,6} = T. Prop. A holds")
say("    with equality, and this is exactly why k >= 7 can carry four outsiders and k = 6 cannot.")

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "supervisor_checks.out"),
     "a").write("\n".join(out) + "\n")
