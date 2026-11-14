# Astra joint-pair lemma: independent audit, dependency ledger, and verdict (block 19)

Source-only. No build, no cloud operation, no compute beyond reading source and counting names.
**Verdict up front: the lemma is mathematically correct and its application to `five_support_no_sixty`
is valid — but it does NOT remove `strict_state_no_unit_support` from the development, because a second
consumer exists whose 23 transitive descendants include `no_proper_five_coloring`.** Details in §3.

Grades: **[M] mathematics verified by hand here**, **[C] computed from source**, **[S] reported**, **[P] proposed**.

## 1. The candidate, restated in the development's own vocabulary

For `f : ℝ → ι` finite-valued measurable, `d : ℝ`, the development already has the generic carrier
(`FiveSupport.lean:38`):

```lean
def stateSupport (f : ℝ → ι) (i : ι) : Set ℝ := (volume.restrict {t | f t = i}).support
```

with `variable {ι : Type*} [Fintype ι] [MeasurableSpace ι] [MeasurableSingletonClass ι]`. The joint-pair
set is `jointPair f d i j := {t | f t = i ∧ f (t + d) = j}`. The claim is

> if for all `i j` with `stateSupport f i ∩ stateSupport f j` nonempty we have `volume (jointPair f d i j) = 0`,
> then `Disjoint (stateSupport f i) ((· + d) ⁻¹' stateSupport f i)`.

This is exactly `five_support_no_sixty` (`FiveSupport.lean:138`) at `ι = Fin 5`, `f = fiveState c hc x`,
`d = sixty`.

## 2. [M] The proof, checked step by step

1. **`{f = i} = ⋃_j Q_ij`.** `Q_ij ⊆ {f = i}` is immediate; conversely if `f t = i` then `f (t+d) = j`
   for exactly one `j`, so `t ∈ Q_ij`. Finite union. ✔
2. **Disjointness.** For `j ≠ j'`, `Q_ij ∩ Q_ij' = ∅` because a point of both would give
   `f (t+d) = j = j'`. ✔ (Used for the restrict additivity.)
3. **`S_i = ⋃_j supp(volume ↾ Q_ij)`.** From (1), (2) and
   `μ ↾ (⨆_j A_j) = ∑_j μ ↾ A_j` for a finite disjoint family, then
   `supp(∑_j μ_j) = ⋃_j supp μ_j`. The second identity holds for measures because
   `(∑ μ_j)(U) = ∑ μ_j(U)` and a finite sum of `ℝ≥0∞` is positive iff some term is; the `U`-family is
   directed by `⊇`, so one `j` works throughout. ✔ (This is the only place finiteness of `ι` is used,
   and it is used essentially.)
4. **Picking `j`.** `a ∈ S_i = ⋃_j supp(volume ↾ Q_ij)`, a finite union, so some `j` has
   `a ∈ supp(volume ↾ Q_ij)`. ✔
5. **Translation step.** `a ∈ supp(μ ↾ Q)`, i.e. every neighbourhood `U` of `a` has `volume(Q ∩ U) > 0`.
   The map `t ↦ t + d` is a homeomorphism preserving `volume`; so `(t ↦ t+d) '' (Q ∩ U)` has the same
   positive measure and contains `(a+d)` in its closure-translate. Since `(t↦t+d) '' Q ⊆ {f = j}`,
   `volume({f = j} ∩ (U + d)) > 0` for every neighbourhood of `a + d`, i.e. `a + d ∈ S_j`. ✔
   *This is the only analytic step*, and it needs only the Haar property of Lebesgue measure on `ℝ`
   and openness of translation — no measurability of the image is required because the argument runs
   on measures of sets, and `volume` is complete.
6. **Contradiction.** If also `a + d ∈ S_i` then `S_i ∩ S_j ∋ a + d`, so the hypothesis gives
   `volume(Q_ij) = 0`; then `volume ↾ Q_ij` is the zero measure, its support is empty, contradicting
   `a ∈ supp(volume ↾ Q_ij)`. ✔

**Conclusion: the lemma is true as stated.** No gap found. Two remarks that a referee should see:
`d = 0` is not excluded but is harmless (`Q_ii = {f = i}`, and the hypothesis then forces `S_i = ∅`);
and `I` finite is essential — for infinite `I` the support-union identity fails (a countable union of
null sets can carry full measure), so the finite hypothesis is not a convenience.

## 3. [C] Dependency ledger — the reason this is not a removal

`strict_state_no_unit_support` (`States.lean:704`) has exactly **two** direct users:

| user | site |
|---|---|
| `five_support_no_sixty` | `FiveSupport.lean:138` |
| `interfaceStateSupport_no_unit` | `Interfaces.lean:266` |

Transitive users of `strict_state_no_unit_support`: **24 declarations**, including
`five_support_no_sixty`, `interfaceStateSupport_margin`, `four_interface_word_data`,
`no_four_interfaces`, `no_four_commonInterface`, `commonInterface_graph_acyclic`,
`five_sequence_no_accumulation`, `cyclicCore_compact_finite`, `fullApprox_exists`,
`no_measurable_weak_five_coloring`, `no_proper_five_coloring_algebraic` and **`no_proper_five_coloring`**
itself (the top-level root).

So rerouting `five_support_no_sixty` through the joint-pair lemma removes **one of the two** uses. The
other — `interfaceStateSupport_no_unit` — is load-bearing for the main theorem, and nothing in the
Astra route touches it. The dependency survives; the topology section still needs
`strict_state_no_unit_support`.

**Line accounting.** The new generic module is ~117 lines of plan (probably 60–90 real lines). The
replacement proof of `five_support_no_sixty` needs the premise of the joint-pair lemma, which is two
case splits (`fiveState_adj` for non-adjacent pairs, `five_support_step_ban` for adjacent ones with the
support intersection supplied by `hi`/`hj` of the contact point) plus the application — realistically
40–60 lines. What it deletes is ~4 lines at `FiveSupport.lean:139-144`. **Net ≈ +100 to +150 lines, and
no theorem removed.**

## 4. What the replacement proof of `five_support_no_sixty` would look like [P]

```lean
lemma five_support_no_sixty (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i : Fin 5}
    (hi : a ∈ fiveSupport c hc x i) : a + sixty ∉ fiveSupport c hc x i := by
  -- f := fun t : ℝ => fiveState c hc x (t : Angles), d := sixty
  -- premise: for each pair, either the states are non-adjacent (fiveState_adj ⇒ Q null)
  -- or they are adjacent and the supports meet at the witness, giving step_ban ⇒ Q null
  ...
```

The two premise cases:
* `¬ fiveAdj i j`: `fiveState_adj` gives `∀ᵐ t ∂angularMeasure, fiveAdj (f t) (f (t + sixty))`; pull back
  along `angleMk_quasiMeasurePreserving` (this is exactly what `five_support_next` already does with
  `simpa only [Function.comp_def, AddCircle.coe_add]`), so a.e. `t` is outside `Q_ij` when `¬ fiveAdj i j`.
* `fiveAdj i j` with a contact witness `a ∈ S_i ∩ S_j`: `five_support_step_ban` (`FiveSupport.lean:91`)
  gives `∀ᵐ t ∂angularMeasure, ¬ (f t = i ∧ f (t + sixty) = j)`, again pulled back.

Retained: `fiveState_adj`, `five_support_step_ban`, `angleMk_quasiMeasurePreserving`.
Dropped locally: `five_adj_four`, `stateSupport_nonempty_measure`, `strict_state_no_unit_support`,
`direction_sixty_unit_real` at that one site.

## 5. Verdict

* **Mathematics: correct.** The Astra argument is sound and the finite-`I` hypothesis is essential. [M]
* **Application: valid.** It would prove `five_support_no_sixty` from `fiveState_adj` + `step_ban`. [M]
* **Simplification: none for the development.** `strict_state_no_unit_support` stays, because
  `interfaceStateSupport_no_unit` and its 23 descendants depend on it. **This must not be described as a
  Lemma 6.7 deletion** — the manuscript naming is unresolved, and on the present evidence no deletion
  occurs at all. [C]
* **Lean module delivered as a plan, not a proof.** Three named blockers (restrict of a finite disjoint
  union; support of a finite sum; translate of a support point), each with candidate Mathlib names, and a
  caveat that the closing proof's rewrites are likewise unchecked. No admission tactic is used. [P]

## 6. Blockers, stated exactly

| # | claim needed | why it is open |
|---|---|---|
| B1 | `volume.restrict (⋃_j Q_ij) = ∑_j volume.restrict (Q_ij)` | candidate `Measure.restrict_iUnion_finset` / `restrict_iUnion` with `PairwiseDisjoint`; exact name unverified against the pinned toolchain |
| B2 | `support (∑_j μ_j) = ⋃_j support μ_j` | candidate `Measure.support_sum`; else `Finset.induction` from `support_add`/`support_zero` |
| B3 | `a ∈ supp(μ ↾ A) → a + d ∈ supp(μ ↾ ((·+d) '' A))` | needs the Haar property (`map_add_right_eq_self` for volume) phrased at `nhds`; no Mathlib name checked |

None of the three is mathematically doubtful; all three are library-shape questions, which is why the
file is a plan rather than a near-miss.

## 7. Toolchain note

The development is pinned at Lean **4.34.1** (commit `5045d0056413266e57c625dcd7c365b10e377c52`) with
Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, which is what any first check should use. A 4.35
submission would need a separate compatibility pass — `Measure.restrict_iUnion*` and `support_sum`
have historically been renamed between releases, so B1/B2 are exactly the steps most likely to need
adjustment. No toolchain change is proposed.
