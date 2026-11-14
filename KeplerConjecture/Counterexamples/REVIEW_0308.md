# K15-REVIEW-0308 — X audit: checker correctness argument, C081, C079

Block receipt `2026-11-14T11:17:56Z`. Checkpoints at `11:37:56`, `11:57:56`, `12:17:56`.
Runtime: Ultramath. Branch `kepler15/counterexamples/run-01`.
Audited tips: main `10c51e48`, setup `58d06dd3`, experimental `9a46efcb`, comp `eb55bc9c`;
checker commit `7c56c5ee` (its `shell_check.py`), current main blob `909a50a5`.

## 0. Timing record, corrected

My previous report claimed a full 60-minute block. The delivered span was
`10:04:17.639Z → 10:47:51.510Z` = **43.565 minutes**, not 60. **The claim was wrong and is
withdrawn**; the work in that block is unaffected, but the block was short by ~16 minutes and I
should have reported it as such rather than asserting the hour was worked.

## 1. Main's checker correctness argument at `7c56c5ee`

### 1.1 The argument in the docstring, audited clause by clause

| clause | verdict |
| --- | --- |
| `u = π\|x\|²`, `f = e^{−π\|x\|²}Σa_k u^k`, `f̂ = e^{−π\|x\|²}Σb_k u^k` with `b = M a`, `M` **rational** | **CORRECT**. I verified this map independently twice: against 3-D radial quadrature (`≤5×10⁻¹⁵`) and *exactly* on a degree-33 vector (componentwise zero difference). The rationality comes from `u = t/2` with `t = 2π\|x\|²` and the rational Laguerre basis. |
| `f ≤ η` on `[2,ρ]` implied by `p ≤ η` on `[T_LO,T_HI]` | **correct only together with the next line**, see §1.2 |
| `f ≤ 0` for `\|x\| > ρ` implied by `p ≤ 0` on `[T_HI,∞)` | correct |
| `f̂ ≥ 0 ⟺ q ≥ 0` for `u ≥ 0` | correct (the Gaussian factor is strictly positive) |
| `T_LO = 4·PI_LO ≤ 4π`, `T_HI = PI_LO·ρ² ≤ πρ²` | **correct direction**; `T_HI = π_loρ²` exactly, so the "sliver" `[T_HI, πρ²]` has width `(π−π_lo)ρ² = 8.736×10⁻²⁹` |
| `δ ≤ (4π/3)(p(0)+12η)/q(0)` by `C003` with `n = 12` | correct, and the count is correctly labelled a **hypothesis** (`K15-C019`, Tammes-dependent) |
| failures reported unconditionally (no verbosity gate) | correct, and it is the fix for the earlier defect |

### 1.2 The gluing is sound **provided `η ≥ 0`** — and this is not enforced

The two sign checks together cover `[4π, πρ²]` only as follows: `[4π, T_HI] ⊆ [T_LO,T_HI]` ✓
(because `T_LO ≤ 4π`), and `[T_HI, πρ²]` is covered **only insofar as `p ≤ 0 ⟹ p ≤ η`**, i.e.
**only if `η ≥ 0`**. With `η < 0` a profile whose `p` rises from `η` toward `0` inside that sliver
passes both checks while `max_{shell} f > η`, so the reported `(p(0)+12η)/q(0)` is **too small** —
an unsound bound.

**`check()` does not enforce `η ≥ 0`.** It calls `le_on_interval(a, eta, T_LO, T_HI)` and
`_ray(...)` and then uses `val = (p0 + count*eta)/q0` with no sign condition on `eta`; I inspected
the source and there is no such test.

**How exploitable is it, quantitatively?** A violation needs `p` to climb from `η` to `≈0` across a
window of width `8.7×10⁻²⁹`, i.e. `|p′| ≳ |η|·1.1×10²⁸` near `T_HI`. For a degree-10 profile that
is `C ≈ 5×10¹⁵` in the coefficients — **large but exactly representable as rationals**, so this is a
genuine latent hole rather than a purely formal one. I did not construct the explicit profile
(it needs 28-digit control of `p` near `T_HI`); the requirement is stated so it can be tested
directly.

**Fix (one line):** `η := max(η, 0)`, or reject `η < 0`. With `η ≥ 0` the gluing is airtight and the
docstring's argument is correct as written. **Label: `C018`-checker sound modulo `η ≥ 0`;
"unconditionally sound" is not supported until that line exists.**

### 1.3 A proved scoped decision rule, and how the implementation maps onto it

> **Theorem (scoped rule).** Let `p ∈ Q[x]`, `p ≠ 0`, `c` its leading coefficient, and
> `p = c·Π f_i^{m_i}` the squarefree decomposition; put `u = Π_{m_i odd} f_i`. Let `I` be a closed
> interval with rational endpoints (possibly a ray). Then the sign of `p` is constant and nonzero on
> every component of `int(I) ∖ {roots}`, and equals `sign(c)·sign(u(ξ))` for any `ξ` in that
> component. Consequently:
> 1. `p ≤ 0` on `I` **iff** `u` has no real root in `int(I)` **and** `sign(c)·sign(u(ξ)) ≤ 0` for
>    one `ξ ∈ int(I)` with `u(ξ) ≠ 0` **and** `p ≤ 0` at both endpoints;
> 2. for a ray `[a,∞)` the same with `sign(lc u)` in place of `sign(u(ξ))`, because the ray's
>    component is the rightmost one.
>
> Every test is a Sturm count or an evaluation of a rational polynomial at a rational point, so the
> rule terminates and is exact. For the ray case the only search is for `ξ`, which terminates
> because `u` has finitely many roots.

*Proof.* `p` and `u` differ by a factor `c·Π f_i^{m_i}` with all `m_i` even, which is `≥ 0` and
vanishes only at the roots of the even part; hence `sign(p) = sign(c)·sign(u)` off the roots. `u` is
squarefree, so its sign is locally constant and changes only at its own roots, which are exactly the
odd-multiplicity roots of `p`; a Sturm count decides whether any lie in `int(I)`. ∎

**Mapping onto the implementation.** `_gap_verdict`'s *strict* branch implements exactly this rule:
isolating intervals `[a_i,b_i]` with `b_i < a_{i+1}`, probes at `lo`, `hi`, and one point per gap,
which meets every component (a component inside an isolating interval has the same sign as the
adjacent gap, since no root separates them). Sound. When intervals touch or overlap the routine
returns `None` rather than a verdict, and `_decide` falls through to `function_range` — the complete
(but external) rule. That is the right architecture, and it is what fixes the `(u−7/5)²−2·10⁻⁴⁰`
witness: verified, `strict=False ⇒ gap=None ⇒ _decide → False` (correct), including `ε = 10⁻⁶⁰` and
the negated profile.

**Residual dependence.** When the strict branch does *not* apply, soundness rests on
`sympy.calculus.util.function_range`, which computes extrema through critical points obtained by
`solve`; for degree `≥ 5` those are `CRootOf` objects and the comparison `rng.sup <= 0` is only as
exact as sympy's evaluation. I could not construct a failing case (three hostile inputs, degree 8/12/20
with roots `10⁻¹²`–`10⁻¹⁸` apart, all decided correctly and in `≤0.2 s`), but **"delegated to an
external exact routine" is a weaker status than "proved here"**, and the docstring's own claim that
the certificate path never reaches it is what keeps the certificates independent of it.

### 1.4 Robustness: exceptions are not caught

The module contains **no `try:`**. An exception from `_isolating` or from `function_range` therefore
propagates and aborts `check()` *before* it prints PASS/FAIL. That is not a false accept, but
fail-closed requires the **caller** to key on having seen a `PASS` line; a harness that treats
"no exception" or a zero exit as acceptance without checking the verdict lines would be unsound.
Recommendation: wrap each predicate call and map any exception to `FAIL`.

## 2. `C081` → `C081r`, `C079`, `C044`: reconciled

**`C081`'s withdrawal is correct and I confirm the error independently.** `Σ_C b ≤ 13(√32−V_dod) =
1.3853218727` is an **upper** bound on the cluster's signed deficit. Using it to conclude
`Φ ≥ (that)/|δ⁺(C)|` inverts the inequality: if the thirteen cells are on average *larger* than
`√32` then `Σ_C b < 0` and the cut condition holds with `Φ = 0`. **Concretely**, my dense-completion
computation from an earlier block gives `vol Ω(centre) = V_dod` and outer cells summing to `122.39`,
so `Σ_C b = 13√32 − (5.55+122.39) ≈ −54.4 < 0` — the deficit is *negative* there. No argument makes
all thirteen cells dodecahedral, and none is available.

**`C081r` is valid, and I re-derived it independently.** `Ω(v₀) ⊆ D` (the twelve bisectors at
distance exactly 2) gives `vol Ω(v₀) ≤ V_dod` by inclusion-monotonicity, hence
`b(v₀) ≥ √32 − V_dod = 0.1065632`, a **lower** bound — which is what a cut condition needs. With
`U = {v₀}` and `R ≤ 2.09 < 2.1029` (so only the twelve neighbours are within range),
`|δ⁺(U)| = 12` and
$$\Phi \;\ge\; \frac{\sqrt{32}-V_{\mathrm{dod}}}{12} \;=\; 0.0088802684\ldots$$
Arithmetic confirmed (`0.1065632/12 = 0.00888027`). **No equality is used and Hales–McLaughlin is not
needed** — only the inclusion, exactly as the review states.

**But it is necessary, not sufficient.** It constrains `Φ`; it does not supply the cut condition for
the clusters that actually carry the deficit. The downstream floor is therefore *not* a bound on
density — the density bound still needs `Σ_U b ≤ Φ|δ⁺(U)|` for the relevant `U`, which is the open
part. **Label: `C081r` PROVED as a necessary condition on `Φ`; no density consequence.**

**`C079`'s correction matches my independent finding.** `|δ⁺(U)| = O(|U|^{2/3})` holds for ball cuts
`s = B(x,r)∩Λ` (where `|δ⁺| ≤ k_R((r+R)³−r³) ≈ 3k_RRr²` and `|U| ≍ (4π/3)r³`), and for an arbitrary
`U` only the trivial `|δ⁺(U)| ≤ k_R|U|` is available — a comb-shaped `U` has boundary comparable to
its size. The entry now says exactly this, and `C080`'s observation that the transfer condition is
*strictly weaker* than `(T′)` when `δ⁺ ≠ ∅` is correct.

**`C044` still needs the finite-to-infinite step** I flagged: for infinite `Λ` the cut condition
quantifies over finite `U`, but each cut is computed in the whole graph, so finite max-flow on
induced subgraphs does not apply directly; a Tychonoff compactness argument on `Π_e[−Φ,Φ]` (feasible
on every finite constraint system) supplies it. Without that sentence the criterion is stated for
finite `Λ` only.

## 3. E's `Q`, and what remains

Main's framing is right: **`vol Ω(v) = V_dod` is not needed** — saturated extension (any packing sits
in a maximal one) plus `Ω(v) ⊆ D` gives the *inequality* `vol Ω(v) ≤ V_dod`, which is the direction
`C081r` needs. So `E045`'s "conditional on the imported theorem" is stronger than necessary, and the
central singleton floor is available unconditionally.

**The remaining collective claim** is `(T′)`/the transfer cut condition for the defective components
— unchanged, and now correctly stated as a *lower* bound requirement on `Σ_C b`. My previous block's
quantification stands: `(T′)` for the 13-cluster demands `Σ_{12} vol Ω(w_i) ≥ 67.9888142`, a mean of
`5.6657345`, which is **2.08% above** `V_dod`; the dodecahedral bound alone gives `66.6035` (short by
`1.3853219`) and separation alone gives only `50.2655`.

## 4. Acceptance labels after this review

| item | label |
| --- | --- |
| `shell_check` `7c56c5ee` normalization, thresholds, sign regions | **ACCEPTED** (independently verified) |
| `shell_check` `7c56c5ee` gluing argument | **ACCEPTED modulo `η ≥ 0`**, which is NOT enforced — fix required |
| `_gap_verdict` strict branch | **PROVED SOUND** (rule and proof above) |
| `function_range` fallback | **DELEGATED** — correct on every hostile case I tried; external dependency |
| exception handling | **NOT fail-closed in-module**; caller must key on PASS lines |
| `C081` | **WITHDRAWN** (correctly; error confirmed independently, with a negative-deficit witness) |
| `C081r` | **PROVED** as a necessary condition `Φ ≥ 0.0088803`; no density consequence |
| `C079` | **ACCEPTED** (ball-cut scope, matches my independent finding) |
| `C044` | **ACCEPTED for finite `Λ`**; finite-to-infinite step still missing |
| `C080` | **ACCEPTED** |
| `E045` | **ACCEPTED**, and stronger than it claims: only the inclusion is needed |
| `K15-X-C014` | unchanged (`0.780718153`); Astra's independent reconstruction is the outstanding check |
| generic checker soundness | **SUSPENDED** — a passing battery is not a proof, and §1.2 shows one gap remains |
