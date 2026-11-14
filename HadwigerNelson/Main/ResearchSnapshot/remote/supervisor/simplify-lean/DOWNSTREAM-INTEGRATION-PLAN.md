# Minimal downstream integration plan for the general contact-ban / shift theorem (block 20)

Source-only. No build, no patch offered (the parent holds the compiling implementation; duplicating it
is excluded). Grades: **[C] computed from source**, **[M] mathematics checked here**, **[P] proposed**,
**[S] reported by the parent**.

## 1. Correction to my previous block, recorded first

`jointpair/JointPairSupport.lean` is **SUPERSEDED** and must not be queued. Its three blockers —
restrict of a finite disjoint union, support of a finite measure sum, translate of a support point —
were all reconstructing machinery the development already has. Two facts I missed:

* `FiveSupport.lean:55` `stateSupport_shift_relation` already performs the whole
  support-extraction plus translation step, for an *arbitrary* relation `R : ι → ι → Prop`;
* `fiveSupport c hc x i` is definitionally `stateSupport (fun t : ℝ => fiveState c hc x (t : Angles)) i`,
  so the generic lemma applies to the five-colour case with no transport.

The parent's route is the right one and my file is retained only as a record of the wrong plan.
**Nothing of mine is to be built.**

## 2. [M] Source audit of the compact derivation — it works, and there are no finite-union API blockers

Target: `five_support_no_sixty`, i.e. from `a ∈ S i` conclude `a + sixty ∉ S i`, where
`S i := fiveSupport c hc x i` and `f t := fiveState c hc x (t : Angles)`.

**Step A — the a.e. disjointness hypothesis.** For each pair `(i, j) : Fin 5 × Fin 5`:

```
hpair i j : ∀ᵐ t ∂volume, (S i ∩ S j).Nonempty → ¬ (f t = i ∧ f (t + sixty) = j)
```

proved by `by_cases fiveAdj i j`:

* `¬ fiveAdj i j`: `fiveState_adj` gives `∀ᵐ t ∂angularMeasure, fiveAdj (f t) (f (t + sixty))`; pull
  back along `angleMk_quasiMeasurePreserving.ae` — the *same* idiom the file already uses at
  `five_support_next` (lines 124–127, `simpa only [Function.comp_def, AddCircle.coe_add]`).
* `fiveAdj i j`: from `h : (S i ∩ S j).Nonempty` obtain a witness `a`, and `five_support_step_ban`
  (`FiveSupport.lean:91`) at `hi`, `hj`, `hij` gives
  `∀ᵐ t ∂angularMeasure, ¬ (f t = i ∧ f (t + sixty) = j)` and the symmetric one; pull back as above.
* if `(S i ∩ S j).Nonempty` is false the clause is vacuous, no a.e. input needed.

Then `ae_all_iff.mpr` over the finite product type turns the `5 × 5` family into one a.e. statement, and
at a good `t` the failure of `Disjoint (S (f t)) (S (f (t + sixty)))` would exhibit a pair with
`S i ∩ S j ≠ ∅` inside the corresponding `Q_ij` — excluded.

**Step B — one application.** `stateSupport_shift_relation hf (R := fun i j => Disjoint (S i) (S j))
(d := sixty) hR hi` yields `∃ j, Disjoint (S i) (S j) ∧ a + sixty ∈ S j`. Both `R` and `d` must be
passed explicitly — `stateSupport_shift_relation` takes them as implicit binders, which is exactly the
"first failure only needed explicit `R`, `d` arguments" the parent reports. **[S]** consistent.

**Step C — close.** If `a + sixty ∈ S i`, then it lies in both `S i` and `S j` with `Disjoint (S i) (S j)`
— contradiction. One line.

**API audit result: no finite-union blockers.** What the derivation consumes is
`ae_all_iff` over a `Fintype`, the two existing a.e. pull-backs, `by_cases` on a decidable relation, and
`Set.disjoint_left`. It uses **no** `Measure.restrict_iUnion`, **no** `support_sum`, and **no** explicit
support-of-translate lemma: all three live inside `stateSupport_shift_relation`, which is already proved
in the file. My earlier B1/B2/B3 were therefore not merely expensive, they were unnecessary.

Size estimate: the parent's 58-line V1+V2 is consistent with this shape (≈20 lines for `hpair`, ≈8 for
the `ae_all` assembly, ≈10 for the case split, ≈10 for Steps B–C, plus binders). I do not reproduce it.

## 3. [C] Minimal downstream integration plan

### 3.1 The statement that must not change

```lean
lemma five_support_no_sixty (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) {a : ℝ} {i : Fin 5}
    (hi : a∈fiveSupport c hc x i) : a+sixty∉fiveSupport c hc x i
```

`FiveSupport.lean:138–139`. Binders, implicitness and `c hc` being section variables from
`variable (c : ℂ → Fin 5) (hc : Measurable c)` at line 84. **No change of any kind** — only the proof
term is replaced.

### 3.2 Insertion location for the general helper [C]

Inside `FiveSupport.lean`, between `five_support_prev` (ends at line 137) and
`five_support_no_sixty` (starts at line 138). Constraints that fix that spot and no other:

* it needs `fiveState_adj` (`Accumulation`, imported at line 1) and `five_support_step_ban`
  (line 91) — both already above;
* it needs `stateSupport_shift_relation` (line 55) — above;
* it must be **before** line 138 because `five_support_no_sixty`'s new proof calls it, and Lean 4 has
  no forward references;
* placing it after line 138 would force `five_contact_next`/`prev` to move, which is unnecessary churn.

So: **insert immediately before the `lemma five_support_no_sixty` header**, i.e. immediately after the
`five_support_prev` proof block ends.

### 3.3 Affected five-cycle declarations — the compatibility test set [C]

`five_support_no_sixty` has exactly five call sites, in **three** declarations:

| declaration | site | call lines |
|---|---|---|
| `five_contact_next` | `FiveSupport.lean:175` | 179, 180 |
| `five_contact_prev` | `FiveSupport.lean:185` | 190, 193 |
| `five_opposite_contacts_false` | `FiveSupport.lean:199` | 216 |

**Zero of them need editing.** Because the statement is byte-identical, every call keeps its
positional arguments and implicit inference; these three are the *test set* that shows consumer
compatibility, not edit sites. Anything beyond compiling this file is out of scope for the patch.

Verification recipe for the integrator, no cloud build:
1. `FiveSupport.lean` compiles (this alone re-elaborates 179/180/190/193/216);
2. `Accumulation`, `CyclicCore`, `Interfaces`, `FullApproximation`, `Five` still compile — they are the
   reverse-dependent modules, unchanged by the edit.

## 4. [C]/[M] Can a reusable contact-ban interface serve the Interfaces second user?

`strict_state_no_unit_support` has two direct users. The second is
`interfaceStateSupport_no_unit` (`Interfaces.lean:266`), concluding
`‖direction t − direction u‖ ≠ 1` for two points `t`, `u` of the **same** angular support
`interfaceStateSupport hc x s := (angularMeasure.restrict {t | fourState … t = s}).support`
(`Interfaces.lean:258`).

Three obstacles, and only one of them is the one I expected:

1. **Carrier.** Not an obstacle. `interfaceStateSupport` lives on `Angles` with Haar measure, but
   `angle_support_lift` (`Interfaces.lean:166`) already transports a point of the angular support to a
   real `b` with `((b : Angles) = t)` and `b ∈ (volume.restrict ((↑)⁻¹' A)).support`, and
   `interfaceStateSupport_no_unit` already uses exactly that. So a statement living over `ℝ`/`volume`
   would be usable here.
2. **Quantification.** This *is* the obstacle. The Interfaces conclusion ranges over **arbitrary pairs**
   of support points — every direction, not one shift. `fiveState_adj` and `five_support_step_ban` give
   nullity only for the fixed shift `sixty`; `stateSupport_shift_relation` is likewise stated for a
   single `d`. To reach the Interfaces statement you need the ban for the direction actually realised
   by `b − d`, which is an arbitrary real.
3. **Circularity.** A parameterised interface
   `(∀ d, ban at d) → ∀ d, S i ∩ (· + d)⁻¹' S i = ∅` is not circular *as a statement* — but
   **discharging** its hypothesis for arbitrary `d` is precisely what `strict_state_no_unit_support`
   currently supplies. So the interface would relocate the obligation, not remove it.

**Verdict: not reusable for the second user without new input.** For the five-colour consumer the ban
is available because `step_ban` and `fiveState_adj` are sixty-specific by construction; for the
Interfaces consumer no such per-direction ban exists in the tree. Anyone attempting it should first
find a *direction-uniform* nullity statement, and I have not found one.

**Naming discipline.** Nothing here is a "Lemma 6.7 deletion". `step_ban`
(`five_support_step_ban`) is retained and used; `strict_state_no_unit_support` **stays** in `States.lean`
because the Interfaces chain depends on it — 24 transitive users including `no_proper_five_coloring`.
The manuscript's Lemma 6.7 numbering remains unresolved and is not to be cited either way.

## 5. What I am deliberately not delivering

* **No patch.** The parent's private V1+V2 source compiles locally; a second implementation would
  duplicate it and could diverge. My contribution is the plan above: statement, anchor, test set, and
  the API audit establishing that no new measure-theory lemma is needed.
* **No generic module.** The superseded file is marked and left in place.
* **No claim of a States deletion**, and no claim that line count settles conceptual value: the consumer
  is unchanged, so the gain is in the proof's *shape* (one general lemma + two existing bans instead of
  a bespoke two-palette argument at this site), not in lines removed.

## 6. Status of claims

| claim | grade |
|---|---|
| compact derivation is sound and needs no new measure API | [M] + [C] |
| insertion point is between line 137 and 138 | [C] |
| exactly three consumer declarations, zero edits | [C] |
| Interfaces second user not reachable by this route | [M] + [C] |
| parent's 58-line V1+V2 compiles locally | [S], not verified here |
| Astra theorem accepted at paper level, local annulus/finite-witness scope | [S] |
| any accepted Lean result | **none yet** |
