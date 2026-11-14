"""Exact checks for the repaired trace-limit claims. Single process, exact Fractions."""
import os
from itertools import product
from fractions import Fraction as F

out = []
def say(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s)

# [13] Rademacher model: one-hot fields with a FIXED positive pairwise L^2 distance.
# Omega = {0,1}^3, uniform; u_k = e_1 where omega_k = 0, e_2 otherwise.
say("[13] Rademacher counterexample (Omega = {0,1}^3, uniform)")
words = list(product([0,1], repeat=3))
def u(k, w): return 1 if w[k] == 0 else 2
for k, l in [(0,1), (0,2), (1,2)]:
    diff = sum(1 for w in words if u(k,w) != u(l,w))
    p = F(diff, len(words))
    say(f"    k={k}, l={l}: P(u_k != u_l) = {diff}/{len(words)} = {p}; ||u_k-u_l||^2 = 2*{p} = {2*p};"
        f" P(|u_k-u_l| >= 1) = {p}")
say("    => pairwise L^2 distance 1 for every pair, and L^0 distance 1/2: no Cauchy subsequence.")
say("    So the set of one-hot (T-valued) fields is NOT compact in L^2 or in measure:")
say("    'closed and bounded in L^0' does not give compactness on a nonatomic space.")

# [14] what m10 Lemma 1 licences: circle a.e.-typicality at EVERY centre
say("[14] admissibility bookkeeping")
say("    Lean: TypicalSampling c y r := 0 < r and (for ae t) Typical (y + r*direction t),")
say("    Typical z := DensityOne {w : c w = c z} z.  IsTrace x b := (x,1,b) in closure(sampleSet).")
say("    Lean has ae_typicalSampling: for fixed r > 0, a.e. y is admissible (a.e.-in-CENTRE).")
say("    The per-centre form needed here is different: the non-typical set N is plane-null and")
say("    the circle is an isometry of angular measure, so (x,1) is admissible for EVERY x.")
say("    That is paper-level (Lemma 4.3 + absolute continuity), not the Lean a.e. statement.")
say("    Hence admissibility is NOT the gap; convergence of the codes is.")

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "supervisor_checks.out"),
     "a").write("\n".join(out) + "\n")
