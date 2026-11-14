# Clause (D) of bridge (B): what is provable, and the exact gap

Source/analysis only. No build, no cloud compute, no agent launched. Clock: 2026-11-14 15:2x UTC
(`date -u` read at the start of the block).

## 0. Two corrections first

**C1 (applicability of the block-16 countermodels).** The two models in `FIVE-CYCLE-INTERFACE.md` §9 are
models of the **abstract data** `(S : ℝ → Finset (Fin 5), θ : ℝ → Fin 5)` only. They are **not**
instances of the actual objects: `Angles = AddCircle (2*Real.pi)` (`Coloring.lean:16`) so a state
function must be 2π-periodic, which my `θ t = (g t + ⌊t/60⌋) mod 5` is not (it gains +6 ≡ +1 per full
turn), and the second model's closed-interval supports overlap at the endpoints, so its "single state at
0" premise fails. **Applicability retracted**; what survives is only the quantifier observation that
"(O″) is a ∀∃ over support sets" and "(SB) is a ∀¬ over θ-values", which is what incomparability needed.

**C2 (my block-16 §10.3 claim about (D) was wrong).** I wrote that "(D) is not
`palette_neighbor_disjoint` … nothing else in the tree supplies (D)". The first half stands, the second
is false: `PaletteTransport.lean:450` has

```lean
lemma palette_sixty_disjoint (hw : WeakColoring k c) (x : ℂ) :
    ∀ᵐ f ∂angularMeasure, Disjoint (palette c hc x f) (palette c hc x (f+(sixty : Angles)))
```
with `sixty : ℝ := Real.pi/3` (`PaletteTransport.lean:390`) and `angularMeasure =
AddCircle.haarAddCircle` (`Coloring.lean:17`). That is exactly the **one centre, two angles 60° apart**
statement I said was missing — at the *palette* level. And `Accumulation.lean:392` `fiveState_adj`
already upgrades it to the **level-set** level. So (D)'s palette and level-set forms are in the tree;
what is missing is one specific upgrade. This file pins it.

## 1. The objects, cited

| name | definition | source |
|---|---|---|
| `Angles` | `AddCircle (2*Real.pi)` | `Coloring.lean:16` |
| `angularMeasure` | `AddCircle.haarAddCircle` (Haar probability) | `Coloring.lean:17` |
| `sixty` | `Real.pi/3` | `PaletteTransport.lean:390` |
| `fiveDiag i` | `{i, i+2}` | `Exclusion.lean:8` |
| `fiveAdj i j` | `i+1 = j ∨ j+1 = i` | `Exclusion.lean:9` |
| `FiveCenter x` | `∀ i : Fin 5, TransitionEdge c i (i+1) x` | `Accumulation.lean:358` |
| `fiveState x t` | `fiveCanonical (palette c hc x t)` | `Accumulation.lean:364` |
| `fiveRealState x i` | `{t : ℝ | fiveState x (t : Angles) = i}` | `FiveSupport.lean:82` |
| `fiveSupport x i` | `(volume.restrict (fiveRealState x i)).support` | `FiveSupport.lean:83` |
| `TransitionEdge i j x` | `i ≠ j ∧ ∀ R > 0, 0 < limsup (transitionRatio x R) (𝓝[≠] 0)` | `Transitions.lean:23` |
| `transitionSet i j x R h` | `{q | q ∈ ball x R ∧ ((c q = i ∧ c(q+h) = j) ∨ (c q = j ∧ c(q+h) = i))}` | `Transitions.lean:9` |
| `transitionRatio i j x R h` | `volume (transitionSet …) / ofReal ‖h‖` | `Transitions.lean:21` |

**(D), the clause to decide.** For a five-cycle centre `x` and a weak 5-colouring `c`, for a.e.
`a : ℝ`: `Disjoint {i | a ∈ fiveSupport x i} {i | a + 60 ∈ fiveSupport x i}`.

Equivalently, with `A_i := fiveRealState x i` (a Borel subset of `ℝ`): no `i` has both `a` and `a+60`
in the closed support of `vol.restrict A_i`.

## 2. Line-by-line: everything the tree gives, with premises supplied

**Step 1** [premise: `hw : WeakColoring 5 c`, `hx : FiveCenter c x`]
`fiveState_diag` (`Accumulation.lean:379`): `∀ᵐ t ∂angularMeasure, palette c hc x t = fiveDiag (fiveState x t)`.

**Step 2** [premise: `palette_sixty_disjoint hw x`, `PaletteTransport.lean:450`]
`∀ᵐ t ∂angularMeasure, Disjoint (palette x t) (palette x (t+sixty))`.

**Step 3** [1 + 2 + `five_diag_disjoint` (`Exclusion.lean:20`, `by decide`)]
`∀ᵐ t ∂angularMeasure, fiveAdj (fiveState x t) (fiveState x (t+sixty))`. This is exactly
`fiveState_adj` (`Accumulation.lean:392`); its proof is the three lines quoted above, so no new premise.

**Step 4** [3 + `fiveAdj` def, `Exclusion.lean:9`]
`fiveAdj i i` is `i+1 = i ∨ i+1 = i`, false in `Fin 5`. Hence **`∀ᵐ t ∂angularMeasure, fiveState x t ≠
fiveState x (t+sixty)`** — the states at 60° separation are a.e. *distinct*.

**Step 5** [4, transported to `ℝ` by `angleMk_quasiMeasurePreserving`]
For each `i`: `vol ({t : ℝ | fiveState x (t:Angles) = i} ∩ (({t | fiveState x (t:Angles) = i}) - sixty)) = 0`.
In the notation above: `vol (A_i ∩ (A_i - 60)) = 0` for every `i`.

**Step 6 — THE GAP.** One wants: `supp(A_i) ∩ (supp(A_i) - 60) = ∅`.
Step 5 gives only that `A_i` and its 60-shift meet in a **null** set. That does **not** imply their
*closed supports* are disjoint, and the inference is not a technicality:

> **Witness that Step 5 ⇏ Step 6** (measure-theoretic, on `ℝ` with Lebesgue measure — an abstract model
> of the inference, **not** a colouring, and claiming nothing about (D)): let
> `A := ⋃_{k∈ℤ} ⋃_{n≥1} (60k + (0, ε_n))` with `Σ ε_n < 60`. Then `A ∩ (A - 60) = ∅`, so Step 5's
> conclusion holds with room to spare, while `0 ∈ supp A` and `60 ∈ supp A` (both are accumulation
> points of the union), so `supp A ∩ (supp A - 60) ∋ 0 ≠ ∅`. The mechanism is exactly thin
> accumulation: `A_i` may creep towards `a` and towards `a+60` through sets of vanishing measure. ∎

Nothing in the tree forbids this creep: `fiveSupport` is defined through `Measure.support`
(`FiveSupport.lean:83`), a purely *topological* closure condition on the restricted measure. It carries
no lower density bound at any scale, and no lemma in the 82-module tree states one.

**Why the promising tools do not close the gap.** `hx` speaks about *position* space:
`TransitionEdge c i (i+1) x` is `0 < limsup_h volume(transitionSet … x R h)/‖h‖` (`Transitions.lean:21-23`),
a positive-density statement for pairs `(q, q+h)` inside a **ball around `x`**, i.e. about the colouring
in a neighbourhood of `x`. `A_i` lives in *angle* space: the directions from `x` along which state `i`
is the palette representative. `transition_abundance` (`Transitions.lean:25`) extracts a scale `a > 0`
and a filter `h → 0` with `a‖h‖ < volume.real (transitionSet …)`; `transitionEdge_closed`
(`Accumulation.lean:197`) is about *closedness in `x`*; `missing_edge_lim` (`Accumulation.lean:214`)
converts a *missing* edge into a limit. None of the three converts angular thin accumulation into a
density statement, and none mentions `fiveSupport` at all.

## 3. The smallest missing lemma

> **(M) — level-set/support upgrade at the 60° step.**
> ```lean
> lemma five_support_sixty_disjoint (hw : WeakColoring 5 c) {x : ℂ} (hx : FiveCenter c x) :
>     ∀ᵐ a : ℝ ∂volume, Disjoint {i : Fin 5 | a ∈ fiveSupport c hc x i}
>       {i : Fin 5 | a + (sixty : ℝ) ∈ fiveSupport c hc x i}
> ```

This *is* (D). It is not a restatement of anything in the tree: its premises would be Steps 1–5, and
its conclusion is Step 6, which Step 5 does not give. The tree's nearest neighbours are:

* `fiveState_adj` — the level-set form (Step 3), strictly weaker by the witness above;
* `palette_sixty_disjoint` — the palette form, weaker still;
* `five_support_step_ban` — a *transition* ban for adjacent pairs present in `S a`; it consumes `S a`
  memberships rather than producing them, so it cannot supply (D);
* `transition_abundance` / `transitionEdge_closed` / `missing_edge_lim` — position-space density and
  closedness, no angular density content.

**Is (M) plausible?** Yes: the closed walk constraint agrees with it. Since `fiveState x (t+sixty)` is
adjacent to `fiveState x t` a.e. (Step 3) and the angle is periodic with `6·60° = 360°`, the six states
at `t, t+60, …, t+300` form a closed walk of 6 steps with increments `±1` on the 5-cycle; the increments
must sum to `0 ∈ ℤ/5` with six even terms, forcing three `+1` and three `−1` and forbidding a repeat at
step 1 (which is exactly `≠` at 60°, Step 4). Revisits are forced at distance ≥ 2 steps (120°). So (M)
is consistent with the combinatorics; what it adds is that the *supports* — not just the level sets —
inherit that separation.

## 4. Verdict

* **(D) is not proved here, and not refuted.** Steps 1–5 are a complete, premise-cited derivation of the
  level-set form; Step 6 is exactly the missing inference, and it is missing for a structural reason
  (closure of a restricted measure says nothing about density), witnessed by an explicit
  measure-theoretic model.
* **(M) is the smallest precise missing lemma**, it respects every base assumption (`hw`, `hx` only, no
  second `FiveCenter`, no bridge hypothesis), and it is stated in the tree's own vocabulary.
* **Bridge (B) is therefore still blocked at (D)**, as well as at (V) (the missing centre construction
  of §10.3). (B) must not be assumed anywhere.

## 5. Grades

| item | grade |
|---|---|
| C1: the §9 models are abstract-only; applicability retracted | [verified here] |
| C2: `palette_sixty_disjoint` exists and gives the one-centre two-angle form | [read] `PaletteTransport.lean:450` |
| Steps 1–5 with premises | [read + argued] each premise cited to a line; the deduction Step 4 uses only `fiveAdj`'s definition |
| Step 5 ⇏ Step 6, with witness | [proved here] on `ℝ` — an abstract model of the inference only |
| (M) is not in the tree; (D) unproved | [argued here] from the inspected declarations |
| plausibility of (M) via the closed 6-step walk | [argued here], arithmetic `3·(+1) + 3·(−1) = 0` |
