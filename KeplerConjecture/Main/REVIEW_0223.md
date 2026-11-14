# Review 0223 — checker repair, constant correction, bridge audit

Block `K15-REVIEW-0223-M`. Receipt `2026-11-14T10:36:27Z`. Reviewed tip
`201974b0677d67bd87d60825fd88011ca9e0d7d1`. This file is the block's account: what
was refuted, what was repaired, what was corrected and what was accepted.

## 1. Third checker defect (`K15-C068`)

`nonneg_on_half_line`, `_ray` and `le_on_interval` accepted
`q(u) = (u − 7/5)² − 2·10⁻⁴⁰`, whose value at `7/5` is `−2·10⁻⁴⁰`. SymPy's two
isolating intervals are `(…, 7/5)` and `(7/5, …)`: they **share a rational
endpoint**, so the "gap between intervals" is empty and the negative dip (width
`9·10⁻²¹`) was never sampled. The previous repair's gap rule was therefore
incomplete, not merely buggy.

**The complete rule now adopted** (correctness argument stated before the code, in
the docstring): the sign is decided from one point per component of the interval
minus the roots; the gap rule is used **only** when the isolating intervals are
separated by non-empty rational gaps, and returns "inconclusive" otherwise; the
inconclusive case is decided by `function_range`, whose algorithm is exactly
"extrema at endpoints and critical points". The certificate path never leaves the
gap branch (certificates have no real roots on the sign regions), so certificate
checking still does not depend on `function_range`; the genuinely independent
oracle remains Computation's `exactcert`.

Regressions: `checker_adversarial.py` is now **29 cases** and includes the three new
witnesses plus `(u−7/5)² + 2·10⁻⁴⁰ ≥ 0` (must pass) and `(u−1/5)² − 2·10⁻⁴⁰` on
`[0,1]` (must fail). Re-verified: all six earlier witnesses still reject, K33b still
`ACCEPT` at `0.779966216777`, fuzz clean.

**Three repairs in three rounds** (`C049`, `C058`, `C068`), each found by an outside
reproduction. The general soundness of the checker remains **suspended** for X; what
can be said is that each repair was followed by re-verification of every earlier
witness and of the certificate.

## 2. `K15-C035` dropped a factor `R` — corrected

X's objection is **right**. The chain is
`Σ_B A ≤ Φ·k_R·((r+R)³ − r³) ≤ Φ·k_R·3R(R+1)²r² ≤ 3ΦR(R+1)⁵r²`, and the constant is
`C₁ = 3ΦR(R+1)⁵`, not `3Φ(R+1)⁵`. At `R = 2.09, Φ = 1` that is **1766.28**, not
845.11. The sharper figures already included `R` and stand: `718.40` (`k_R = 12`,
`K15-C054`) and `1556.53` (`k_R = 26`). `transfer_check.py` and
`constants_check.py` were corrected with the lemma; the fixture still satisfies the
(true, larger) bound.

## 3. Cut-condition quantifiers, infinite extension, proof complexity (`C067`, `C071`)

- Necessity of `Σ_U b ≤ Φ|δ⁺(U)|` is local and needs no compactness.
- Sufficiency in the infinite case uses Hoffman on an exhaustion plus a Tychonoff
  cluster point — and the limit step needs **finite degree**, which `C054` supplies
  at `R ≤ 2.09`. On an unbounded-degree graph the argument fails, so the hypothesis
  is not decoration.
- Proof complexity: the non-effective step is confined to aperiodic packings; for a
  periodic packing the cut condition is a finite min-cut, polynomial. The real cost
  is exact cell volumes, which Hales never needs — so the transfer packaging trades
  hard bookkeeping for uncomputable geometry and is favourable **only** if an
  analytic averaged cell bound exists.

## 4. Next target chosen from worker evidence (`C072`, `D17`)

`(Q)` ("does a saturated packing contain a cell below `√32`?") is **false**
(`K15-C069`): the 13-cluster extends to a saturated packing (`X-C003(iii)`, Zorn) and
its centre cell is the dodecahedron, `5.550291 < √32`. C's exact two-point family
plateaus at `Δ ≈ 1.99` and its higher-degree certificates at `0.77996622`; the
three-point specification is unimplemented with no evidence it pays. The target is
therefore E's **`(H_R)`** in cluster-average form with the explicit `Φ` of `C044`
(`Main/NEXT_PACKAGE.md`). Reversal condition recorded in `D17`.

## 5. Independent fallback: bridge audit (`C070`, `Main/BRIDGE_AUDIT.md`)

CE's Appendix A was read from the retained PDF (Annals 157, 708–709). CE pass to a
**uniformly dense extremal** packing — existence via Groemer — and assert that "only
a negligible fraction of the spheres can intersect the sides"; `K15-C002b` stays with
the given packing and pays `O(S/R) + O(1/S)` with `O(R²S)` boundary centres counted
through disjoint unit balls. Structurally different; neither follows from the other
by rearranging constants. Also recorded: the project's `limsup`-at-a-fixed-centre
density equals CE's uniform upper density for 2-separated packings; Hales' route
needs no bridge; the open items are the uniformity bookkeeping, the `δ = 0` case and
the Zorn saturation step.

## 6. Lean

`CubeDiff.lean` hit the 1 GiB cap after 8.8 s with no theorem checked. Per
instruction, Lean imports are **not** iterated this block: the module stays
`PROPOSED` and `M-LEAN-003` records the resource failure. `Volume.lean` carries only
`Prop`-valued statements.

## 7. Accepted-lemmas account

`Main/ACCEPTED.md` lists every statement the project may rely on, its status, the
closest published source and the difference from it, the open gaps with what closes
each, and an explicit list of what is **not** claimed — in particular no route is
called closed.
