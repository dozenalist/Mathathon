# Independent audit: the Astra joint-pair support candidate and its fiveState application

Block 19. Source reading and mathematical analysis only; no builds, no computation. Grades: **[S]** source
read, **[S+]** source read and the conclusion follows at the quoted line, **[P-v]** I verified the
mathematical claim myself (complete proof below), **[P-x]** refuted by explicit counterexample, **[C]**
my reading. The block timestamp is in `STATUS.json` (`updated_utc`, from the clock).

## 0. Verdicts

| item | verdict |
|---|---|
| the general joint-pair support theorem, **positive support** reading | **TRUE**, complete proof in §1; all four checkpoints pass (§2) |
| the same statement with **ordinary closures** instead of positive supports | **FALSE** — explicit counterexample in §2(c) |
| measurability / finite-value requirements | as Astra states them, no extra hypothesis needed (§2(a),(b)) |
| source compatibility of `S_i` with the Lean | **exact**: `stateSupport f i = (volume.restrict {t | f t = i}).support` (`FiveSupport.lean:39`), `Measure.support` = positive support |
| the fiveState application | **sound**, and its two a.e. inputs already exist (`fiveState_adj`, `five_support_step_ban`) — §4 |
| does `States:704` (`strict_state_no_unit_support`) disappear? | **No.** It is transitively reached by retained input through **two** routes; the candidate closes one of them — §5 |
| naming | **not** a Lemma 6.7 deletion; the manuscript Lemma 6.7 is the support-contact step ban, a different statement — §6 |
| `shiftedAEfacts` | **no such declaration exists** in `lean/` or in any supervisor file I can read — §3 |

## 1. The theorem and its proof (my own, complete)

**Setting.** `α` a topological space with Borel measure `μ`; `T : α → α` continuous and
**measure-preserving** (`μ (T ⁻¹' A) = μ A` for Borel `A` — no injectivity needed); `ι` a **finite** type;
`f : α → ι` **total and measurable**. Put
```
S i  := (μ.restrict {x | f x = i}).support            -- positive support: x ∈ S i ↔ ∀ U ∋ x open, μ (U ∩ {f=i}) ≠ 0
Q i j := {x | f x = i ∧ f (T x) = j}
```
**Hypothesis.** `∀ i j, S i ∩ S j ≠ ∅ → μ (Q i j) = 0`.
**Claim.** `∀ i, Disjoint (S i) (T ⁻¹' S i)`, i.e. `x ∈ S i → T x ∉ S i`.

**Proof.**

1. *(Disintegration of the level set.)* For each `i`, `{f = i} = ⋃_j Q i j`, a **finite disjoint** union,
   because `f` is total with values in the finite type `ι`. Hence
   `μ.restrict {f=i} = ∑_j μ.restrict (Q i j)` (finite additivity of restriction to a disjoint measurable
   union).
2. *(Support of a finite sum.)* `supp (∑_j ν_j) = ⋃_j supp ν_j` for a **finite** family of measures: if
   `x ∉ supp ν_j` for all `j`, choose open `U_j ∋ x` with `ν_j U_j = 0` and let `U = ⋂_j U_j` (finite,
   open, `∋ x`); then `(∑_j ν_j) U ≤ ∑_j ν_j U_j = 0`. Combining with 1:
   $$S_i=\bigcup_j \operatorname{supp}\bigl(\mu\restriction Q_{ij}\bigr).$$
3. *(Existence of the partner.)* If `a ∈ S i`, then by 2 there is `j` with `a ∈ supp (μ|Q i j)`. In
   particular `μ (Q i j) > 0` (take `U = univ`), so `Q i j ≠ ∅` in measure.
4. *(The translate is in the partner's support.)* I claim `T a ∈ S j`. Suppose not: there is an open
   `U ∋ T a` with `μ (U ∩ {f = j}) = 0`. Set `V := T ⁻¹' U`, a neighbourhood of `a` by continuity. Then
   `V ∩ Q i j ⊆ T ⁻¹' (U ∩ {f = j})`, so
   `μ (V ∩ Q i j) ≤ μ (T ⁻¹' (U ∩ {f=j})) = μ (U ∩ {f=j}) = 0`
   by measure preservation — contradicting `a ∈ supp (μ|Q i j)`.
5. *(Contradiction from a contact.)* If also `T a ∈ S i`, then `S i ∩ S j ≠ ∅`, so the hypothesis gives
   `μ (Q i j) = 0`, contradicting step 3. Hence `T a ∉ S i`. ∎

**Notes.** No a.e. statement and no exceptional set occurs anywhere: the theorem is about supports and exact
null sets. `T` need not be injective or invertible; only `μ ∘ T⁻¹ = μ` and continuity are used. Finiteness of
`ι` is used **twice** (the union in step 1 and the intersection in step 2).

## 2. The four checkpoints

**(a) Measurability.** `f` measurable ⟹ each `Q i j` is measurable: `{f = i}` measurable, and
`{x | f (T x) = j} = T ⁻¹' {f = j}` measurable since `T` is continuous hence Borel-measurable. Without this,
`μ (Q i j)` need not be defined and `μ.restrict (Q i j)` is not the measure being discussed. ✓
*Astra's hypothesis "measurable f" is exactly right and sufficient; nothing about `f`'s regularity beyond
measurability is used.*

**(b) Finite unions of restricted measures.** The identity `μ|{f=i} = ∑_j μ|Q i j` needs (i) the level set to
be the *disjoint* union of the `Q i j` — which uses that `f` is **total** into `ι` — and (ii) finite
additivity of restriction. The support identity `supp (∑ ν_j) = ⋃ supp ν_j` needs finiteness in the
intersection step. Both hold. ✓ (For infinite `ι` the second identity can fail without local finiteness —
so "finite-valued" is not decoration.)

**(c) RETRACTED (block 20).** The counterexample below is **wrong** and must not be used.
`Q₀₀ = {t : f t = 0 ∧ f (t+1) = 0}` is `ℝ∖ℚ`, which has **full** Lebesgue measure, not measure zero
(under `d = 1`, irrational ↦ irrational, and the irrationals have full measure). So the premise instance
`S₀ ∩ S₀ ≠ ∅ ⟹ μ(Q₀₀) = 0` **fails**, and the example is not a model of the hypothesis at all. The correct
reading of that `f`: positive supports are `S₀ = ℝ` (the irrationals are conull) and `S₁ = ∅` (the rationals
are null, so `μ|ℚ = 0` and its support is empty) — exactly as the referee says.
**Consequence:** the closure reading of the theorem is **neither refuted nor established by me**. The proof of
§1 genuinely uses positive supports at step 2 (`closure (⋃_j Q_ij)` is in general strictly larger than
`⋃_j closure(Q_ij)`), but I have no countermodel to the closure version, so it must be reported as *open*, not
as false. This does not affect the application: the Lean's `stateSupport`/`fiveSupport` are positive supports.

~~**(c) Positive support versus ordinary closure — decisive, and the closure version is FALSE.**~~
Take `α = ℝ`, `μ` Lebesgue, `f = 1_ℚ` (values in `Bool`), `T t = t + 1`. Then
`Q₀₀ = ℝ∖ℚ`, `Q₀₁ = ∅`, `Q₁₀ = ∅`, `Q₁₁ = ℚ` — **all four null**.
* With **closures**: `closure (ℝ∖ℚ) = closure (ℚ) = ℝ`, so every premise instance has nonempty contact and a
  null `Q`; the premise holds, but the conclusion would assert
  `ℝ ∩ (ℝ - 1) = ℝ = ∅` — **false**.
* With **positive supports**: `ν := μ|ℚ` is the zero measure, so `supp ν = ∅`, and likewise
  `supp (μ|ℝ∖ℚ) = ∅`; then `S₀ = S₁ = ∅`, the premise is vacuous and the conclusion holds.
~~So the theorem is a statement about *positive* supports, and any formalisation that silently reads the
supports as closures is refuted by this example.~~ — **retracted**, see the banner above.

**(d) Translation/measure preservation.** Step 4 uses only `μ (T ⁻¹' A) = μ A` (measure preservation) and
continuity of `T` (to pull a neighbourhood back). It does **not** need `T` to be a bijection, an isometry, or
`f` to be continuous. In the Lean applications `T` is `t ↦ t + d`, and
`measurePreserving_add_right` supplies exactly this. ✓

## 3. Source compatibility

| Astra | Lean | status |
|---|---|---|
| `S_i = supp (volume|{f=i})` | `def stateSupport (f : ℝ → ι) (i) : Set ℝ := (volume.restrict {t | f t = i}).support` (`FiveSupport.lean:39`); `fiveSupport` (`:84`) is the same on the angle circle | **[S+] exact match**; Mathlib's `Measure.support` is the positive support |
| `f` measurable, finite-valued | `fiveState_measurable`, `five_realState_measurable` (`:85`) | **[S]** |
| `T(t) = t+d` measure-preserving | `measurePreserving_add_right (volume : Measure ℝ) d`, and on the circle `measurePreserving_add_right angularMeasure (sixty : Angles)` (used at `Accumulation.lean:393`) | **[S]** |
| "shiftedAEfacts" | **no declaration of that name exists** in `lean/` or in the supervisor records; the existing relatives are `ae_mem_stateSupport` (`:40`), `ae_state_support` (`:44`), `stateSupport_cover` (`:49`), `stateSupport_shift_relation` (`:55`), `stateSupport_nonempty_measure` (`:71`) | **[S] name not found — do not cite it** |
| step 4 (translate lands in the partner support) | `stateSupport_shift_relation` is a *different but related* statement: it moves `a ∈ stateSupport f i` to `a + d ∈ stateSupport f j` under an a.e. relation `R (f t) (f (t+d))` | **[S] not the same lemma**: Astra's step 4 needs no a.e. hypothesis, but starts from `supp (μ|Q i j)` |
| the disintegration `supp (μ|{f=i}) = ⋃_j supp (μ|Q i j)` | **nothing in the tree** — this is the genuinely new lemma | **[S] identified as the one missing piece** |

So the honest inventory is: *one* new lemma (the disintegration, step 1+2), everything else already exists.

## 4. Application to `fiveState`

Instantiate §1 with `α = Angles`, `μ = angularMeasure`, `T t = t + sixty`, `ι = Fin 5`,
`f = fiveState c hc x`. Then `Q i j = {t | fiveState t = i ∧ fiveState (t+sixty) = j}` and `S i = fiveSupport c hc x i`.

The premise `S i ∩ S j ≠ ∅ → μ (Q i j) = 0` has to be supplied for all pairs:

* **non-adjacent `i, j`**: `fiveState_adj` (`Accumulation.lean:390-391`) gives
  `∀ᵐ t ∂angularMeasure, fiveAdj (fiveState t) (fiveState (t+sixty))`, so a non-adjacent pair occurs only on a
  null set: `μ (Q i j) = 0` **unconditionally** ✓ **[S+]**;
* **adjacent `i, j` with `S i ∩ S j ≠ ∅`**: `five_support_step_ban` (`FiveSupport.lean:90-96`), whose
  conclusion is `∀ᵐ t, ¬(state t = i ∧ state (t+sixty) = j) ∧ ¬(state t = j ∧ state (t+sixty) = i)` — exactly
  `μ (Q i j) = 0` and `μ (Q j i) = 0` ✓ **[S+]**.

Conclusion: `∀ a, a ∈ fiveSupport c hc x i → a + sixty ∉ fiveSupport c hc x i`, which is
**`five_support_no_sixty`** (`FiveSupport.lean:138-147`) with a different proof. So the candidate does what it
claims *if* the disintegration lemma of §3 is added. **Not yet formalised; this is a [C]/proposed route, not a
verified one.**

## 5. Is `States:704` reached transitively? Yes — and it does **not** disappear

`strict_state_no_unit_support` is `States.lean:704`. Its consumers, exhaustively (`grep -rn`):

1. `FiveSupport.lean:144`, inside `five_support_no_sixty` (`:138`);
2. `Interfaces.lean:277`, inside an interface-support lemma about `interfaceStateSupport`.

`five_support_no_sixty` is then used at `FiveSupport.lean:179, 180, 190, 193, 216` (inside `five_contact_next`
`:`175` and the two further lemmas there). `FiveSupport`, `States` and `AngularBoundary` are all in the
**70-module `OAI` cone of `Five.lean`** (computed). So:

* **retained input does reach `States:704`** — transitively, through `five_support_no_sixty` and through
  `Interfaces.lean:277`;
* the Astra candidate replaces only route 1. Route 2 (`Interfaces.lean:277`) is untouched by anything in this
  proposal, so the lemma `strict_state_no_unit_support` **cannot be deleted** and the `strict_state_sequence_false`
  machinery (§ around `States.lean:640-714`) stays needed unless `Interfaces.lean:277` is also re-derived;
* what genuinely disappears is **one dependency edge**: `five_support_no_sixty` would no longer need
  `States:704`. That is a real reduction in coupling, and it is all that should be claimed.

## 6. Naming

This is **not** a Lemma 6.7 deletion, and it must not be called one. The manuscript's Lemma 6.7 is the *support
contact bans an angular step* statement (paper l. 2139) — about a contact `{i, i+1} ⊆ S(a)` banning the steps
`i ↔ i+1` a.e. `five_support_step_ban` is its formal counterpart and is **retained** by this candidate, which
uses it as an input. The candidate's own statement is the *no-sixty-contact* statement for a single support,
which is `five_support_no_sixty`. The manuscript naming of that statement is unresolved; the audited facts
support "`five_support_no_sixty` re-proved without `States:704`", nothing more.

## 7. What is missing to complete it

One lemma, statable now, in the shape of §1–§2:

```
lemma support_restrict_level_eq_iUnion (μ : Measure α) [SFinite μ] {ι : Type*} [Fintype ι]
    {f : α → ι} (hf : Measurable f) {T : α → α} (hT : Measurable T) (i : ι) :
    (μ.restrict {x | f x = i}).support = ⋃ j, (μ.restrict {x | f x = i ∧ f (T x) = j}).support
```
— then §1 steps 3–5 are three lines each with `stateSupport_shift_relation`-style arguments replaced by the
measure-preservation computation of step 4. No further machinery, no exceptional sets, no a.e. hypothesis.

**Risk to flag.** In the Lean the measure on `Angles` is `angularMeasure`, and the shift `+ sixty` is
measure-preserving (`measurePreserving_add_right angularMeasure sixty`), so §1 applies verbatim; but the
statement `fiveSupport` uses `volume.restrict` on `ℝ` pulled back through `angleMk`, so the identification
"`fiveSupport` = support of the pushed measure" is one bookkeeping lemma that I have **not** checked. That is
the second (smaller) obligation.


## 8. Block 20 additions

### 8.1 Corrected dependency wording

Earlier I wrote that `States:704` "is reached transitively by retained input". That conflated two things and
must be stated precisely:

* the **new retained input** of the Astra route — `fiveState_adj` (`Accumulation.lean:390`) and
  `five_support_step_ban` (`FiveSupport.lean:90`) — does **not** depend on `States:704`. I checked both
  proofs' dependency lists: `five_support_step_ban` uses `five_support_trace`, `traceValue`,
  `avoiding_trace_palette`, `palette_neighbor_disjoint`, `fiveState_diag`, `five_forced_label`; none of them
  invokes `strict_state_no_unit_support`. So the new route is **not circular**;
* `States:704` persists in the development because of a **different consumer**, `Interfaces.lean:277`, which
  is outside the new route. That is the correct phrasing: *not reached through the retained step_ban*, but
  retained elsewhere.

### 8.2 The second interface consumer: `interfaceStateSupport_no_unit` (`Interfaces.lean:266-277`)

Statement (read verbatim):
```
lemma interfaceStateSupport_no_unit (hw : WeakColoring 5 c) {x : ℂ}
    (hg : ∀ᵐt∂angularMeasure, fourGroup (fourState c hc x t) ⊆ palette c hc x t)
    {s : Fin 3} (hs : s≠0) {t u : Angles}
    (ht : t ∈ interfaceStateSupport hc x s) (hu : u ∈ interfaceStateSupport hc x s) :
    ‖direction t - direction u‖ ≠ 1
```
with `interfaceStateSet x s = {t | fourState c hc x t = s}` and
`interfaceStateSupport x s = (angularMeasure.restrict (interfaceStateSet x s)).support` — again a **positive**
support, and `fourState` is `Fin 3`-valued and measurable (`States.lean:325-327`).

**Shape match.** On the unit circle, `‖direction t - direction u‖ = 1` exactly when the angular difference is
`±sixty` (`direction_sixty_unit` gives one direction; the tree also carries the chord computation at
`Interfaces.lean:236-241`). So the interface conclusion **is** "no shift by `±sixty` within
`interfaceStateSupport x s`" — precisely the conclusion shape of the joint-pair theorem with `d = sixty` and
`d = -sixty`. That is a genuine structural compatibility, not a name resemblance.

**Conditional route.** If (P1) the nulls for `fourState`'s shift-pairs are available — for all `i j : Fin 3`,
`interfaceStateSupport i ∩ interfaceStateSupport j ≠ ∅ → angularMeasure {t : fourState t = i ∧ fourState (t+sixty) = j} = 0` —
then §1 gives the interface conclusion at once.

**Is (P1) available?** Partly, and at a different level: `four_support_no_sixty`
(`FourTransport.lean:218-223`) already proves the *same-shaped* statement for `fourSupport` (the support of
`volume.restrict` on the **real line**), and its proof does **not** use `States:704` — it uses
`four_support_sequence_no_unit` (`FourContinuity.lean:441`) and `direction_sixty_unit_real`. So the
sixty-ban at the `fourState` level is already available by a route independent of `States:704`.

**Missing premises, precisely.** Two bookkeeping facts, neither of which is `States:704` or an equivalent:

1. **converse chord lemma**: `‖direction t - direction u‖ = 1 → u = t + sixty ∨ u = t - sixty` (as elements of
   `Angles`). The tree has the forward evaluation `direction_sixty_unit` and the trigonometric computation at
   `Interfaces.lean:236-241`; I did not find the converse as a named lemma.
2. **support correspondence**: `interfaceStateSupport hc x s` (support of `angularMeasure.restrict {fourState = s}`
   on `Angles`) versus `fourSupport c hc x s` (support of `volume.restrict (fourRealState … s)` on `ℝ`), under
   the quasi-measure-preserving `angleMk`/`angle_support_lift`. This is the same bookkeeping obligation already
   flagged in §7.

So the answer to the new target is: **yes, the second consumer is shape-compatible with a contact-ban/shift
theorem, and the required sixty-ban already exists at the `fourSupport` level without `States:704`; what is
missing is the chord converse plus the angle-lift support correspondence** — a conditional theorem, not an
obstruction. No module count was used in reaching this.

**What this does not show.** It does not yet delete `States:704`, it does not re-derive
`strict_state_sequence_false`, and it does not touch Lemma 6.7/`five_support_step_ban`, which stays retained.
