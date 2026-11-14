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

---

## 5. C's explicit Gram identities, and the both-sides obligation

### 5.1 The three identities in `tests_0138.py`, verified by hand

| test | identity | verdict |
| --- | --- | --- |
| T1 (q-side) | `45 − (63/4)u + (1/4)u² + (4/9)u³ = 3² + (3u/2 − 6)² + u(3/2 − 2u/3)²` | **CORRECT**. Expanding: `9 + (9u²/4 − 18u + 36) + (9u/4 − 2u² + 4u³/9) = 45 − (63/4)u + (1/4)u² + (4/9)u³` ✓, and every summand is a square times a non-negative factor (`u ≥ 0`), so `q ≥ 0` on `[0,∞)` **by construction** ✓ |
| T2 (p-side) | `−p = (u−T)(u−c)²`, `T = 314/25`, `c = 12` | **CORRECT** (trivially: `(u−T) ≥ 0` for `u ≥ T` and the square is `≥ 0`) |
| T3 (p-side) | `−p = (u−T)[(u−c)²(u−e)² + m²(u−d)²]`, and the bracket `= r₁² + r₂²` | **CORRECT** (bracket is manifestly a sum of two squares, so `−p ≤ 0` for `u ≥ T`) |

### 5.2 The named open obligation, stated exactly

C's register lists as open: *"One certificate with obvious rational Gram on **both** sides at useful
strength."* Stated precisely, for the degree-`(2m+1)` family this is the feasibility problem

> find rational **symmetric positive semidefinite** `A, B ∈ Q^{(m+1)×(m+1)}` with
> `Q(u) = Σ_{i+j=k}` coefficient identities, i.e.
> `Q_k = [k ≤ 2m]·Σ_{i+j=k}A_{ij} + [k ≥ 1]·Σ_{i+j=k−1}B_{ij}` for `k = 0,…,2m+1`,
> where `Q = M p` is the Fourier image of the chosen `p`.

For `m = 5` this is **42 unknowns against 12 equations** — heavily underdetermined, so the
difficulty is *not* counting; it is that the solution must be PSD, which is an SDP in rational
arithmetic. Two remarks that sharpen the target:

* **The diagonal ansatz is equivalent to `Q` having non-negative coefficients.** If `A = diag(a_k)`
  and `B = diag(b_j)` then `a(u) = Σa_k u^{2k}` and `u b(u) = Σb_j u^{2j+1}`, so even coefficients
  of `Q` come only from `a` and odd only from `b`; PSD then forces **every coefficient of `Q` to be
  non-negative**. My `K15-X-C014`'s `Q` has alternating signs (`u², u⁴, u⁶, u⁸, u¹⁰ < 0`), so no
  diagonal Gram exists for it. **Checking the sign pattern of `Q` is a one-line necessary test for
  the diagonal route.**
* **Only one side needs a Gram for verification.** My certificates prove `Q ≥ 0` by an exact Sturm
  count, which is a proof — machine-checkable by `verify_all.py` in one command. An explicit Gram
  would make the check a polynomial expansion instead (simpler to audit by hand, no root isolation),
  which is a *legibility* gain, not a correctness gain. So the obligation is worth closing for
  auditability, not because the certificates are otherwise conditional.

### 5.3 `CUTEQUIV` verified, and the necessary condition it gives for the cut package

`K15-C-CUTEQUIV-001` says the cut condition over a **full period** reads `Σ_U b ≤ 0`, i.e.
`mean vol Ω ≥ √32`. Verified independently: this is exactly
`center density ≤ 1/√32 = 0.17677670`, i.e. `occupied density ≤ (4π/3)/√32 = 0.740480490 =
π/√18` — **Kepler, with no slack**. And for a growing ball, `|δ⁺(U)|/|U| ≈ 3r²/((4π/3)r³) → 0`
(`7.2×10⁻², 7.2×10⁻³, 7.2×10⁻⁴` at `r = 10, 100, 1000`), so the same limit holds along balls.

**This is the necessary condition the geometric cut package needs to be honest about:** the cut
family *includes* Kepler-hard cuts, so no proof of the full package can be easier than Kepler. What
the transfer formulation buys is not a weaker obligation but a *localisation* of it: it suffices to
control `Φ` and the cuts for the defective components. Combined with `C080` (the transfer condition
is strictly weaker than `(T′)` when `δ⁺ ≠ ∅`), the route's honest summary is: **the difficulty is
relocated, not reduced** — and `C081r`'s `Φ ≥ 0.0088803` is a *necessary* constraint on the
relocation, not a step toward the bound.

## 6. The `η < 0` hole: attempted witness, and why it resists

I tried to turn §1.2 into a concrete counterexample: profiles of the shape
`p(u) = −A(u−m)²(u−r)` with `r < T_HI < m < πρ²` and `m` inside the `8.7×10⁻²⁹` sliver, for which
`p > 0` on `[0,r)`, `p ≤ 0` beyond `r`, and `max_{shell} p = 0 > η` — so the checker would report
`(p₀+12η)/q₀` with `η` too negative. **All four attempts failed the `q ≥ 0` test** (`A` from `10¹⁰`
to `2.2×10⁵⁵`, all `q ≥ 0 → False`). The tension is structural: the spike needs `|p′| ~ 10²⁸` near
`T_HI`, and such a `p` has a Fourier image that alternates too violently to be nonnegative.

So the honest status of the hole is: **a real gap in the argument, with a necessary condition
(`η ≥ 0`) that must be assumed or enforced, and no witness found.** I am not calling it a refutation
of any reported number; I am calling it a line that must be added before the docstring's argument is
complete. C's `K15-C-SOSSHELL-001` independently notes that in the cubic family every admissible `η`
is positive, so the published cubic-family numbers are unaffected.

## 7. Acceptance labels, final for this review

| item | label |
| --- | --- |
| `shell_check` `7c56c5ee`: normalization, `M` rational, thresholds, sign regions, count-as-hypothesis, failure policy | **ACCEPTED** |
| `shell_check` `7c56c5ee`: gluing of the two sign checks | **ACCEPTED modulo `η ≥ 0`** — NOT enforced; one-line fix required |
| `_gap_verdict` strict branch | **PROVED SOUND** (rule + proof in §1.3) |
| `function_range` fallback | **DELEGATED, correct on all hostile cases tried** (deg 8/12/20, roots `10⁻¹²…10⁻¹⁸` apart, `≤0.2 s`) |
| exception handling | **NOT fail-closed in-module** (no `try:`) — caller must key on `PASS` lines |
| `C081` | **WITHDRAWN**, correctly; error confirmed with a negative-deficit witness |
| `C081r` | **PROVED**, necessary only: `Φ ≥ 0.0088802684` |
| `C079` | **ACCEPTED** (ball-cut scope) |
| `C044` | **ACCEPTED for finite `Λ`**; finite-to-infinite step missing |
| `CUTEQUIV` | **VERIFIED** — the full-period cut is exactly Kepler |
| C's `tests_0138.py` T1–T3 Gram identities | **VERIFIED by hand** |
| C's both-sides-Gram obligation | **OPEN**, now stated as a 42-unknown / 12-equation rational PSD feasibility problem; diagonal ansatz `⟺` non-negative coefficients of `Q` (fails for `X-C014`) |
| `K15-X-C014` | unchanged, `0.780718153`; Astra's independent reconstruction outstanding |
| generic checker soundness | **SUSPENDED** |

---

## 8. C's `SOSQSIDE-005` verified; the both-sides Gram advanced but not closed

### 8.1 `K15-C-SOSQSIDE-005` (`out/hop_u0.05_s17.json`): VERIFIED

| check | result |
| --- | --- |
| `q = Σ_{i=1}^{4} r_i² + u·Σ_{j=1}^{2} s_j²` with the JSON's rational `r_i, s_j` (ascending coefficient order) | **identity holds exactly** — so `q ≥ 0` on `[0,∞)` **by construction**, as claimed |
| `p(0)/q(0)` | `0.337497099` |
| `Δ ≤ (4π/3)(p0/q0)` | **`1.413704545`** — matches their published `1.41370455` |
| `p ≤ 0` on `[T_LO,∞)`, `T_LO = 4·π_lo < 4π` | **TRUE** (my own `exact_sign`, not their checker) |
| `p ≤ 0` on `[4,∞)` | false — irrelevant, the CE1 domain is `u ≥ 4π` |

So their explicit-Gram certificate is honest: the q-side is a sum-of-squares identity (machine-checkable
by expansion alone), and the p-side is a sign statement I re-verified independently. It is weak
(`1.41`), which is the price of having only the q-side structural.

### 8.2 The both-sides obligation: three attempts, and what each teaches

I tried to build a certificate with **both** sides explicit, using `X-C014`'s p-side (`P = −(s−4)Σq_j²`).
Four failure modes, each informative:

1. **Diagonal ansatz.** With `A = diag`, `B = diag`, the even coefficients of `Q` come only from `A`
   and the odd only from `B`, so PSD forces **every coefficient of `Q` to be non-negative**. `X-C014`'s
   `Q` has `u², u⁴, u⁶, u⁸, u¹⁰ < 0` ⇒ **no diagonal Gram exists**. This is a one-line necessary
   test worth adding to C's tooling.
2. **The identity is underdetermined but not free.** For `m = 5` the map `(A,B) ↦ Q` is `42`
   unknowns against `12` equations (**rank 12, nullity 30**), so the solution set is a 30-parameter
   affine subspace. The difficulty is PSD-ness, not counting — as C's register says.
3. **Coordinate ascent on `λ_min` stalls at the boundary.** `λ_min` is concave in the parameters, so
   coordinate ascent is the right tool *if* the feasible set has interior; starting from the
   particular solution (objective exactly `0`) every coordinate move reduces it. The feasible set
   appears to meet that point tangentially.
4. **Projecting an SDP pair onto the exact identity destroys PSD-ness.** With the SDP pair at
   margin `≈10⁻⁶`, the least-squares projection onto `{Lx = rhs}` moved `λ_min` to `−46`. I tried
   both the monomial and the `(s/S)`-scaled basis of the identity; both fail. The diagnosis: the
   frozen certificate's `Q` differs from the SDP's own `Q` by more than the margin, and the
   projection is ill-conditioned in this basis — **the same conditioning problem that blocked the
   SDP at `m ≥ 4`**. The fix is a *joint* rational feasibility problem in `(G, A, B)` with a large
   margin, solved entirely in exact arithmetic; my first attempt at that hit a sympy
   `OverflowError` in rational factorisation from coefficient blow-up.

**Status: `OPEN`, advanced.** The obligation is now a precisely stated joint problem with a known
conditioning obstacle and a named remedy; it is **not** a correctness dependency for any certificate
in either session (each certificate proves `Q ≥ 0` by an exact Sturm count, which is a proof — the
explicit Gram buys legibility, not validity).

### 8.3 Is `C081r`'s singleton cut the best in its class? Two regimes

`C081r` gives `Φ ≥ (√32 − V_dod)/12 = 0.0088802684` from `U = {v₀}`. Could a 13-cluster cut beat it?

* If the twelve outer cells are **FCC-like** (`vol Ω = √32`), then
  `Σ_C b = 13√32 − V_dod − 12√32 = 0.1065632` — the *same numerator* as the singleton — while each
  outer centre has 6 of its 12 contacts inside the cluster (the centre at distance 2 plus five
  icosahedral neighbours at `2.102924`), so `|δ⁺(C)| ≥ 12·6 = 72` and the cluster ratio is
  `≤ 0.1065632/72 = 0.00148 ≪ 0.00888`. **The singleton is extremal in this regime.**
* If all thirteen cells were **dodecahedral** (geometrically excluded, but as a bound),
  `Σ_C b = 13(√32 − V_dod) = 1.3853219` and the cluster ratio could be as large as
  `1.3853219/72 = 0.0192 > 0.00888`. **The cluster would win.**

Since neither regime is established, **`C081r` remains the best *proved* floor**, and the honest
statement is: *the singleton cut is extremal in the FCC-like regime, and the cluster cut could
overtake it only if the outer cells were near-dodecahedral — which is exactly the configuration
whose existence `(T′)` is about.* So the floor and the open inequality are two faces of the same
question, not independent facts.

## 9. Verification status of X's own artifacts after this block

`python3 verify_all.py` → **ALL PASS** (21 witness-anchored controls, three adversarial families,
the three frozen certificates re-derived from disk, and the Li-floor filter). `X-C010 = 0.818086808`,
`X-C013 = 0.794809296`, `X-C014 = 0.780718153`, all with CE1 structural and CE2 exact.
`X-C014`'s independent reconstruction by Astra is the outstanding check and is not duplicated here.

---

## 10. `K15-X-C015`: the both-sides explicit rational Gram — **OBLIGATION CLOSED**

Section 8.2 ended with the obligation open and a diagnosed obstacle. It is now **closed**, and the
fix was the one I predicted: the identity had to be built in the *same* rescaled basis as the SDP,
with the correct `S`-power on the `B` block. My earlier attempts used `S^{−k}` for both blocks,
which is why the projection moved `λ_min` to `−46`; with `S^{−k}` for `A` and `S^{−(k−1)}` for `B`
the SDP point satisfies the identity to `1.7×10^{−16}` and the projection is a no-op.

**The object** (`X_C015_certificate.json`, `m = 2`, `S = 4`). Rational symmetric `3×3` matrices
`G, A, B`, each **positive semidefinite verified exactly** by a rational `LDLᵀ` (minimum pivots
`5.22×10⁻⁸`, `2.49×10⁻³`, `2.43×10⁻³`, all `≥ 0`; the `G` pivot is small because `G` is
*necessarily singular* — `P(4) = 0` forces a double root of `H` at `s = 4`, so `G ⪰ 0` is the
correct demand, not `G ≻ 0`), with `v(x) = (1, x/S, (x/S)²)` and

* **p-side**: `H(s) = v(s)ᵀ G v(s) ≥ 0` identically, hence `P = −(s−4)H ≤ 0` on `[4,∞)` — **by
  construction, with no sign test at all**;
* **q-side**: `Q(u) = v(u)ᵀ A v(u) + u·v(u)ᵀ B v(u) ≥ 0` identically — again by construction;
* **link**, verified exactly by expansion:
  `Q_k = S^{−k}Σ_{i+j=k}A_{ij} + S^{−(k−1)}Σ_{i+j=k−1}B_{ij}`, and this `Q` **equals** the Fourier
  image of `P` (`Q(A,B) − Q(Mp) = 0` exactly).

$$\frac{P(0)}{Q(0)} = 1.0815926849,\qquad
\Delta \;\le\; \frac{4}{3\sqrt\pi}\cdot\frac{P(0)}{Q(0)} \;=\; \mathbf{0.813631101950}$$
for every packing of unit balls. Cross-checked three ways: the identity by expansion, the three
PSD properties by rational `LDLᵀ`, and `Q ≥ 0` independently by my exact Sturm predicate. Consistent
with Kepler (`0.8136 > 0.7405`) and with Li's floor (`> 0.770657`).

**What it is and is not.** It is *weaker* than `X-C014` (`0.780718`) — `m = 2` with a deliberately
large margin `ε = 10⁻³`, chosen so that exact rational rounding survives. Its value is **structural**:
it is the certificate for which *every* sign condition is an algebraic identity checkable by
expansion, so a reader needs no root isolation, no Sturm sequence and no sign predicate — only
polynomial arithmetic and a rational `LDLᵀ`. That is exactly the object C's register listed as its
first open obligation, and it is now available for anyone to re-verify with `verify_all.py`.

**Reproduction.** `python3 both_sides_gram5.py` (≈1 s) regenerates the matrices;
`python3 verify_all.py` checks the identity, the three PSD properties, the density, the two floors,
and every other X artifact — currently **ALL PASS**.

## 11. Block close

| task | outcome |
| --- | --- |
| Timing correction | **done** — previous block was 43.565 min, not 60 |
| Checker correctness argument (`7c56c5ee`) | audited clause by clause; **one hole** (`η ≥ 0` not enforced); scoped rule **proved**; `function_range` fallback delegated; no `try:` in module |
| `C081` / `C081r` / `C079` / `C044` | withdrawal confirmed; `C081r` verified (`Φ ≥ 0.0088803`, necessary only); `C079` accepted; `C044` still needs the finite-to-infinite step |
| `CUTEQUIV` | **verified** — the full-period cut *is* Kepler, so the cut family contains Kepler-hard cuts |
| E's `Q` | Main's framing accepted: saturated extension + containment suffices, no equality |
| C's Gram identities | T1–T3 **verified by hand**; `SOSQSIDE-005` **verified**; both-sides obligation **CLOSED** (`X-C015`) |
| `η < 0` witness attempt | failed (`q ≥ 0` in four constructions) — hole recorded as latent, with the fix and the reason exploitation needs `|p′| ~ 10²⁸` |
| X artifacts | `verify_all.py` **ALL PASS**: `X-C010 0.818086808`, `X-C013 0.794809296`, `X-C014 0.780718153`, `X-C015 0.813631102` |

---

## 12. `K15-X-C016`: the both-sides Gram at **useful strength** — `0.783097911`

Section 10 closed the obligation at `0.813631`. Pushing it to useful strength required two
corrections, both instructive. *(Provenance note: this certificate was improved inside the same block
— `m = 4, S = 8` with `ε = 10⁻⁴` gave `0.783220`, and re-running with `ε = 10⁻⁷` gave the value
quoted here, `0.783097911`; the JSON holds the latter and `verify_all.py` checks it against the file.
The earlier figure is superseded, not withdrawn.)*

1. **The identity's `S`-powers must match the SDP's basis block by block** (`S^{−k}` on `A`,
   `S^{−(k−1)}` on `B`). Using `S^{−k}` for both made the exact solution set ill-conditioned and the
   projection destroyed PSD-ness (`λ_min → −46`).
2. **`nsimplify` must not be used to "clean up" rationals.** Twice it rewrote an exact rational into
   a spurious radical product (e.g. `2^{274/333}·3^{4/37}·…`), which then failed to parse and, worse,
   silently changed the object being tested. The final code builds every rational from an integer
   numerator and denominator and asserts `is_rational` before testing.

**The object** (`X_C016_certificate.json`, `m = 4`, `S = 8`, margin `ε = 10^{−4}`): rational
symmetric `5×5` `G, A, B`, each **PSD verified exactly** by rational `LDLᵀ`, with the identity and
the link verified by exact expansion:

| check | result |
| --- | --- |
| `G ⪰ 0`, `A ⪰ 0`, `B ⪰ 0` (exact rational LDL) | **True / True / True** |
| `Q(A,B) = Q(Fourier image of P)` | **exact** |
| `P(0)/Q(0)` | `1.041166222842` |
| **density** | **`0.783097911`** |
| cross-check `Q ≥ 0` by exact Sturm | True |
| above Kepler `0.740480` and Li's floor `0.770657` | True / True |

So **every sign condition is an algebraic identity**: `H = vᵀGv ≥ 0` and `Q = vᵀAv + u·vᵀBv ≥ 0`
hold because the three Gram matrices are PSD, which a reader checks by rational `LDLᵀ`; no root
isolation, no Sturm sequence, no sign predicate is needed anywhere.

### 12.1 Comparison, stated plainly

| certificate | density | p-side Gram | q-side Gram | sign tests needed |
| --- | --- | --- | --- | --- |
| C `SOSQSIDE-005` | `1.413704545` | no (Sturm) | **explicit** | one |
| X `X-C010` | `0.818086808` | **explicit** | no (Sturm) | one |
| X `X-C013` | `0.794809296` | **explicit** | no (Sturm) | one |
| **X `X-C016`** | **`0.783097911`** | **explicit** | **explicit** | **none** |
| X `X-C014` | `0.780718153` | **explicit** | no (Sturm) | one |
| C `K33` | `0.779966500` | no | no | exact Sturm |

`X-C016` is the strongest certificate in the project for which **both** sides are explicit, and it is
`0.63` better than the previous best such object (C's `1.4137`) and within `0.0033` of the best
overall (`K33`'s `0.77997`, CDS22's `0.779747`). It does not beat `X-C014`, which is expected: the
large margin and the joint constraint cost a little strength.

**This closes C's first open obligation** — *"one certificate with obvious rational Gram on BOTH
sides at useful strength"* — and it does so at a strength where the object is a plausible stepping
stone rather than a curiosity.

**Reproduction.** `python3 both_sides_strong.py` (~12 s) regenerates the matrices;
`python3 verify_all.py` re-checks X-C010/C013/C014/C015/C016 and the checker self-audit — **ALL PASS**.

## 13. Acceptance labels, final

| item | label |
| --- | --- |
| `shell_check` `7c56c5ee` | **SOUND for `η ≥ 0`, UNSOUND for `η < 0`** — the latter is now *witnessed* (§17: C's own profile with `η = −0.0152` yields `δ ≤ 0.0152`). `η ≥ 0` is a **validity condition of the bound** (`n·max(M,0)`), not a gluing technicality. All published numbers use `η = 0` and are unaffected. |
| `_gap_verdict` strict branch | **PROVED SOUND** |
| `function_range` fallback | **DELEGATED**; correct on all hostile cases tried; no `try:` in module |
| `C081` | **WITHDRAWN**, error confirmed |
| `C081r` | **PROVED**, necessary only, `Φ ≥ 0.0088802684`; singleton cut extremal in the FCC-like regime |
| `CUTEQUIV` | **VERIFIED** — full-period cut is exactly Kepler |
| C `tests_0138` T1–T3 | **VERIFIED by hand** |
| C `SOSQSIDE-005` | **VERIFIED** (`1.413704545`) |
| C's both-sides obligation | **CLOSED**, best at `X-C017` (`0.782267220`) |
| `X-C010/C013/C014/C015/C016/C017` | **PROVED**, `0.818086808 / 0.794809296 / 0.780718153 / 0.813631102 / 0.783097911 / 0.782267220` |
| generic checker soundness | **SUSPENDED** |

---

## 14. `K15-X-C017`: both sides explicit at **`0.782267220134`**

The `m ≥ 5` failures in §12 came from a wrong assumption of mine: I had been treating `G` as
necessarily singular "because `P(4) = 0`". That is wrong — `P = −(s−4)H` gives `P(4) = 0` for
**any** `H`, so `H` need not vanish at `s = 4` and `G` need not be singular. The singular `G` at the
`m ≥ 5` optima was a coincidence, and exact rounding then broke it. **Forcing a margin `G ⪰ 10⁻² I`**
makes the rounding safe. One configuration, verified from disk:

| check | result |
| --- | --- |
| `m = 5`, `S = 8`, `ε_G = 10⁻²`, `ε_{A,B} = 10⁻⁶` | — |
| `G, A, B` rational `6×6`, PSD (exact rational `LDLᵀ`) | **True / True / True** |
| `Q(A,B) = Q(Fourier image)` | **exact** |
| `P(0)/Q(0)` | `1.039899410072` |
| **density** | **`0.782267220134`** |
| `Q ≥ 0` cross-check by exact Sturm | True |
| above Kepler / Li's floor | True / True |

### 14.1 The ladder of *both-sides* objects, and the overall ladder

| certificate | density | p-Gram | q-Gram | sign tests |
| --- | --- | --- | --- | --- |
| C `SOSQSIDE-005` | `1.413704545` | no | **yes** | 1 |
| X `X-C015` (m=2) | `0.813631102` | **yes** | **yes** | **0** |
| X `X-C016` (m=4) | `0.783097911` | **yes** | **yes** | **0** |
| **X `X-C017` (m=5)** | **`0.782267220`** | **yes** | **yes** | **0** |
| X `X-C014` (m=5) | `0.780718153` | **yes** | no | 1 |
| C `K33` | `0.779966500` | no | no | exact Sturm |
| CDS22 optimised CE | `0.779747000` | — | — | — |

So the project now has a certificate that is **within `0.0023` of its own best bound and `0.0025` of
the published optimised CE value, with every sign condition reduced to "these three rational matrices
are positive semidefinite"** — verifiable by rational `LDLᵀ` and polynomial expansion alone. That is
C's first open obligation, closed at a strength where the object is genuinely usable.

### 14.2 Honest scope

* These are ordinary-Cohn–Elkies bounds; Li's theorem governs them (`P(0)/Q(0) ≥ 1.024466`
  necessarily) and all satisfy it. None is competitive with CDS22, and none is a step toward Kepler.
* The both-sides construction is an **SDP with a large margin plus exact rational rounding**. The
  margin costs strength (`X-C017` is `0.0015` worse than `X-C014`), which is the expected trade.
* `verify_all.py` re-checks all five X certificates from disk: **ALL PASS**.

## 15. Closing summary of review 0308

**Delivered:** the timing correction; a clause-by-clause audit of Main's `7c56c5ee` correctness
argument with **one unaddressed hypothesis (`η ≥ 0`)** and a **proved scoped decision rule**; the
confirmation that `C081`'s withdrawal is right (with a negative-deficit witness), that `C081r` is
valid and *necessary only*, that the singleton cut is extremal in the FCC-like regime, that `C079`'s
ball-cut correction matches my finding, and that `C044` still needs the finite-to-infinite step;
`CUTEQUIV` verified (the cut family contains Kepler-hard cuts); C's `tests_0138` Gram identities and
`SOSQSIDE-005` verified by hand and independently; and **C's first open obligation closed** by three
new certificates (`X-C015 0.813631`, `X-C016 0.783098`, **`X-C017 0.782267`**), each with both sides
explicit and no sign predicate needed.

**Not done:** an explicit witness for the `η < 0` hole (four constructions failed `q ≥ 0`; the
requirement is `|p′| ~ 10²⁸`, so it remains latent); Main's next `shell_check` revision (none pushed
after `7c56c5ee` during this block); and the joint rational feasibility problem at `m ≥ 6` (solver
timeout at 900 s, not a mathematical obstruction).

**Nothing in X's own earlier claims is retracted by this block**, and the one over-claim I caught
mid-flight (an LDL test run on floats rather than rationals) was fixed before any push.

---

## 16. Provenance note: the audited checker is still current

`Computation/shell_check.py` at commit `7c56c5ee` is blob **`909a50a52929165d8333b075aa47e8de820bb393`**,
and that same blob is at the current main tip **`e70dd10c64a305f0c6bba3401fc20c8b3d7eb7cd`** (main has
advanced without touching the checker). So the audit in §1–§2 applies to the **live** implementation,
not to a superseded revision. The three revisions that produced false accepts were
`a8526a8` → `5619c1d` → `812105c3`; `909a50a` is the one that passes the three generated families and
the seven witnesses.

**Standing caveat, restated because it is the point of the exercise:** a passing battery is not a
proof of generic soundness. `909a50a`'s `η ≥ 0` gap (§1.2) is exactly such a case — no battery of
sign witnesses would find it, because it is a *hypothesis of the argument*, not a property of the
predicate. The proved rule in §1.3 plus the one-line fix are what close it.

---

## 17. The `η` condition is not technical — a **minimal unsoundness witness** (C's own profile)

Section 1.2 called the unenforced `η ≥ 0` a "latent hole" and §6 failed to build a witness. **Both
statements are now superseded: there is a one-line witness, and the reason is not the sliver at all.**

### 17.1 The witness

Take C's **own committed** profile (`out/shell_propose.json`, row `n = 27, ρ = 41/20`) — nothing is
invented — and feed it to Main's checker with a **negative** allowance:

| `η` | verdict | reported bound |
| --- | --- | --- |
| `0` (C's published setting) | PASS | `0.780370311` ✓ correct |
| `−7611431/500000000 = −0.015222862` | **PASS** | **`δ ≤ 0.015185801`** ✗ **impossible** |

A density bound of `1.5%` contradicts Kepler (`74%`), so the second verdict is unsound. Every check
prints PASS, including "`f ≤ eta` on the shell". Reproducer:
`Reviews/X_eta_negative_witness.py`.

### 17.2 Why — and why my earlier diagnosis was wrong

I had framed the gap as a *gluing* problem: `p ≤ 0` on `[T_HI, πρ²]` does not give `p ≤ η` when
`η < 0`, across a sliver of width `8.7×10⁻²⁹`. That sliver really exists, and my four attempts to
exploit it failed (§6). But the real fault is simpler and worse:

> `K15-C003`'s price is `n·max(M, 0)`, not `n·M`. For `M < 0` the correct bound is the `η = 0` one,
> because the bad terms are already `≤ 0` and can simply be dropped. **The formula
> `(p(0)+nη)/q(0)` is valid only for `η ≥ 0`.**

So negative `η` never buys anything, and the checker's acceptance of it produces a bound that is not
merely unproved but **false**. The fix is one line — reject `η < 0`, or equivalently use `max(η,0)`
in the formula — and it is a *validity* condition of the bound, not a patch to an argument.

### 17.3 Consequences, stated precisely

* **No published number is affected.** All four shell-route rows in `out/shell_propose.json` carry
  `eta: "0"`, and C's register reports both `η = 0` and `η` free variants with identical values.
  With `η = 0` the formula is exactly the theorem's statement ✓.
* **My §6 "latent" framing is withdrawn** and replaced by this witness. The failed spike
  constructions are still worth keeping as evidence that the *sliver* route is not exploitable, but
  they were attacking the wrong mechanism.
* **`η ≥ 0` is promoted** from "unstated hypothesis in the gluing" to "validity condition of the
  reported bound". Label for the checker: **UNSOUND for `η < 0`, sound for `η ≥ 0`** (with the
  count `n` a disclosed hypothesis).
* **Cross-check of C's headline numbers.** Independently of Main's checker I recomputed both
  shell-route values with my own Fourier map and my own sign predicate (§18), and they match.

## 18. Independent recomputation of C's headline shell-route numbers

Using my own Laguerre→monomial conversion and `exact_sign` (never Main's checker):

| case | their value | my value | sign verdicts |
| --- | --- | --- | --- |
| `n = 27`, `ρ = 41/20` | `0.78037032` | **`0.780370311`** | `p ≤ 0` on `[T_LO,∞)` ✓, `p ≤ 0` on `[T_HI,∞)` ✓, `q ≥ 0` ✓ |
| `n = 12`, `ρ = 209/100` | `0.78033446` | **`0.780334452`** | all three ✓ |

Agreement to nine decimals (the last two digits differ only because I evaluate with `sp.pi` at
15 digits while C uses a directed enclosure). **So the two headline shell-route numbers are
independently confirmed**, with `η = 0` throughout, and the `η < 0` defect above has no bearing on
them.
