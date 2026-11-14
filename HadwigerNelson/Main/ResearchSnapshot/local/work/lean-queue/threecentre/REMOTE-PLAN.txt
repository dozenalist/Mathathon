# Three-centre fixed-state exclusion — module, manifest, and Interfaces call-replacement audit (block 21)

Source/verification block. **No Lean run** (no cloud build permitted). Grades: **[C] computed from
source**, **[M] paper argument checked here**, **[P] proposed, uncompiled**, **[S] reported**.

## 1. What was produced

`supervisor/simplify-lean/threecentre/FixedStateThreeCentres.lean` — 193 lines, one theorem,
sha256 `af45ff16cfe059ce3534a8c3362ec941211ea0cc15e6d30503e558371364135b`.

It imports exactly two modules — `OAI.Geometry.PlaneColoring.FiveSupport` and
`OAI.Geometry.PlaneColoring.BoundaryTrace` — and calls **none** of `strict_state_sequence_local_false`
(States:547), `strict_state_sequence_false` (States:683), `strict_state_no_unit_support` (States:704)
or any of their descendants. Verified by scanning the proof text for those three names: zero hits.

No `sorry`, no `admit`, no placeholder constant. The scan in §6 excludes comments and confirms this.

## 2. [M] Independent check of the A2 paper argument

Checked line by line against the sources; the argument is correct, and one point deserves recording
because it is where a three-centre proof could silently fail:

* **Angles are fixed before exceptional sets.** `y := x + direction b`, `z := x + direction d` give
  `‖z − y‖ = 1`, so `direction_exists` (WeakColoring:145) produces `alpha` with
  `direction alpha = z − y` *once*, before any `∀ᵐ`. The third palettes-disjointness statement is then
  `palette_neighbor_disjoint` at centre `y` with parameter `alpha`, i.e.
  `Disjoint (palette (y + direction alpha)) (palette y)`, and `y + direction alpha = z`. If `alpha`
  were chosen inside the a.e. argument the exceptional set would depend on the angle and the
  intersection of five conull sets would not be legitimate. It is not.
* **The trace inputs.** `state_support_avoiding_trace` (BoundaryTrace:24) applied to `hB` at `b` and at
  `d` gives traces at `y` and at `z` vanishing on `K`; `avoiding_trace_palette` (BoundaryTrace:53)
  then gives `¬ palette y t ⊆ K` and `¬ palette z t ⊆ K` for a.e. angular `t`.
* **The positive-measure point.** `hA.2 : ∀ i ∈ J, A ≤ᵐ[volume] liftPalette x i` gives, after a finite
  intersection over the Fintype `Fin k` (made vacuous outside `J` so no `Finset`-indexed a.e. API is
  needed), a conull set on which `t ∈ A → J ⊆ palette x t`. Combined with `0 < volume A` this yields a
  single `t ∈ A` satisfying all six statements; the existence step is done with `ae_iff` plus
  `measure_mono`, not with any support API.
* **The finite label fact.** From `¬ palette y t ⊆ K` take `j` with `j ∈ palette y t`, `j ∉ K`.
  `Disjoint (palette y t) (palette x t)` and `J ⊆ palette x t` give `j ∉ J`; then `j ∉ J ∪ K`, so
  `j = X`. Symmetrically `X ∈ palette z t`. Contradiction with `Disjoint (palette y t) (palette z t)`.
  No cardinality bound on the palette is used and `J, K` need not be disjoint — matching the note that
  this is the general-label form of the forcing step inside `five_support_step_ban`.

One hypothesis I checked for slack: **positivity of `volume B` is not needed and not used.** Only
`0 < volume A` (the `J`-side) appears. The contract is therefore exactly the original one.

## 3. [C] Interfaces call-replacement audit — the statement is a drop-in

`interfaceStateSupport_no_unit` (Interfaces:266) ends with the single call

```lean
  exact strict_state_no_unit_support hc hw hl (four_state_represents_of_group hc hg r)
    (four_state_represents_of_group hc hg s)
    (angle_state_preimage_positive (interfaceStateSet_measurable hc x r)
      (four_state_diagonal_positive_of_group hc hw hg r hr)) hb hd
```

The new theorem's binder list is identical in kind, order and implicitness to the original
(`{k} {c}` implicit, `(hc) (hw)` explicit, `{x} {J K} {X}`, `(hlabels)`, `{A B}`, `(hA) (hB)`, `(hp)`,
`{b d}`, `(hb) (hd)`, conclusion `‖direction (b:Angles) - direction (d:Angles)‖ ≠ 1`). Therefore the
replacement is **one identifier**: `strict_state_no_unit_support` → `fixed_state_no_unit_three_centres`,
with every argument unchanged.

Everything else in that proof — `angle_support_lift`, `four_state_represents_of_group`,
`four_state_diagonal_positive_of_group`, `angle_state_preimage_positive`, the choice of the opposite
nonzero `r`, the complement computation `i ∉ fourGroup r ∪ fourGroup s ↔ i = 4` — is untouched, because
none of it changes.

**Not claimed:** that this makes `strict_state_no_unit_support` deletable. The original declaration
stays in `States.lean`; only this one call is redirected, and only after the new theorem is accepted.

## 4. [P] Manifest

| item | path | sha256 |
|---|---|---|
| new module | `supervisor/simplify-lean/threecentre/FixedStateThreeCentres.lean` | `af45ff16cfe059ce3534a8c3362ec941211ea0cc15e6d30503e558371364135b` |
| import 1 | `lean/OAI/Geometry/PlaneColoring/FiveSupport.lean` | `6d54703f840a1b4d20b81f5f206b18d79a1fbacde9a481990049b3c41b9c4813` |
| import 2 | `lean/OAI/Geometry/PlaneColoring/BoundaryTrace.lean` | `c3c0c75a0fb2e2184e8ff39562faac2c38e3d372864ddeca9eb942fa0f2a692f` |
| transitive (unchanged) | `lean/OAI/Geometry/PlaneColoring/States.lean` | `941fcbdcd90fb50426d4588d62ea10f9bdc882d455f546f2095ead91a0439340` |
| consumer to patch later | `lean/OAI/Geometry/PlaneColoring/Interfaces.lean` | `47dd83f5591742eeabe2aab290f5a855115f0397c12f22b824e5c8047cd1e99e` |

Toolchain: Lean 4.34.1 commit `5045d0056413266e57c625dcd7c365b10e377c52`, Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`. Build command for the parent's local queue:

```bash
source scripts/env4341.sh
lean supervisor/simplify-lean/threecentre/FixedStateThreeCentres.lean
```

`#print axioms fixed_state_no_unit_three_centres` is the last line before `end`. Expected
`[propext, Classical.choice, Quot.sound]`; any `sorryAx` means a hole survived.

## 5. [P] What a first local run may need

The proof is complete — every goal is discharged — but it is **uncompiled**, and a subset of Mathlib
names was written from the tree's own usage rather than checked against the pinned build. The places
most likely to need a name-level fix, in order:

1. `ae_iff.mp hae` for turning `∀ᵐ t, p t` into `volume {t | ¬ p t} = 0`;
2. `Finset.not_subset.mp` and `Finset.disjoint_left.mp` (expected present, but they are the two
   Finset API calls that carry the finite label fact);
3. `ae_all_iff.mpr` over `Fin k` (the tree uses the same idiom in `state_support_avoiding_trace`);
4. `angleMk_quasiMeasurePreserving.ae` argument order (used identically in `state_support_avoiding_trace`,
   so this one is low risk).

None of these is a mathematical gap: each is a lemma-name or argument-shape question whose failure
produces a compile error pointing at one line.

## 6. [C] Hole scan

Strip block and line comments from the module, then count: `sorry` 0, `admit` 0, `BLOCKER` 0,
`sorryAx` 0. The only occurrence of the word "sorry" in the file is inside the header comment that
says there is none.

## 7. Scope discipline

* This is a **fixed-state** theorem. It says nothing about weakly mixing colourings, about global
  colourings beyond `WeakColoring k c`, or about the plane at large. It lives in the **local/angular**
  model (palettes at a centre, Haar measure on `Angles`), and no conclusion about the global weak
  colouring should be read off it.
* The **moving-centre** extension (A2's closed-carrier argument, aimed at the `FourContinuity` consumer)
  is explicitly **not** attempted here. It is staged after this fixed proof is accepted, and it needs
  the packet `a2-closed-carrier-proof.txt`, which I have not seen; nothing in this block should be read
  as validating it.
* The manuscript's Lemma 6.7 numbering remains unresolved. `step_ban` (`five_support_step_ban`) is
  retained and used; no global `States` deletion is claimed.
