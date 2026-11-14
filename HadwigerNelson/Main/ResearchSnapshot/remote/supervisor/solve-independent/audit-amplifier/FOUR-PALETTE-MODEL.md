# Astra's four-palette whole-circle field: audit, the exact global/partial distinction, and a refuted multi-state analogue

Source-only audit. **No computation, no Lean.** Read-only: `States.lean` (RealState :92, two_state_impossible
:243, Angles via `Coloring.lean:16`), `BinaryPalettes.lean` (BinaryCenter :9, binary_alternation :11,
binary_pair_distinct :28, binary_centers_separated :123, ae_not_binary_circle :182), and
`supervisor/solve-geometry/ANNULUS-LOCAL-GLOBAL-AUDIT.md` §1 for the source object table. Astra's field and
the side-allowed sets are relayed data; `m11`'s half-circle bound is external.

> # RETRACTIONS (later block, `AC-AUDIT.md` §0) — five of my claims here are wrong
>
> **R1.** `BinaryCenter` means the palette **hits** the pair (contains `i` or `j` at a.e. direction), **not**
> that the palette is contained in the pair. My "contained" reading is withdrawn.
> **R2.** The four-state field **does** hit `{0,5}` a.e. (`{0,2}`, `{0,3}` contain 0; `{3,5}`, `{2,5}`
> contain 5), so `BinaryCenter c hc x 0 5` holds and my "no BinaryCenter pair exists … inapplicable" claim is
> **false** and withdrawn.
> **R3.** `B2` means each palette has card ≤ 2, which the field satisfies; it does not mean all palettes lie in
> one 2-set. Conflation withdrawn, and with it the "no 2-set contains all four palettes" test.
> **R4.** §2's Proposition ("no `Bool` coarsening satisfies both `RealState` premises") is **false**:
> `s = [f ∈ {0,1}]` gives `RealState` with `J = {0}` and `K = {5}` and does flip at 60°. The premise that
> actually fails is **`hcard`**: `univ \ ({0}∪{5})` has cardinality 4 > 2. In general every `RealState` level
> set here admits at most one label, so `|J ∪ K| ≤ 2` always. The binding premise is `hcard`, not `RealState`.
> **R5.** §3's "the candidate (MS) is REFUTED by the field" is withdrawn: the field omits the
> state-determination hypothesis, so it is not a counterexample to `(MS)`. All broad no-go sentences in this
> file ("no purely state-theoretic generalisation can close the gap", "every licensed relation is inapplicable
> or slack") are frozen and withdrawn as statements.

## 0. Retractions of my own claims from the previous block

* **R1.** I wrote that "finite `m6` is not the restriction of ANY whole-circle trace field". **Withdrawn.**
  What §2 of `F6-SIX-CYCLE.md` proves is strictly weaker: *no naive extension with the fixed pair
  `J = {0,2}`, `K = {3,5}` and an a.e. 60° flip exists* under the full source hypotheses. It says nothing
  about whole-circle fields with **more** palettes, and Astra's four-palette field is such a field.
* **R2.** My proposed 6-word `({0,2}, {3,5}, {1,4}, {3,5}, {0,2}, {3,5})` is **not a licensed model** and is
  withdrawn. For fixed `m6` `q = (0,3,3,3,0,0)` the side-allowed label sets are `{2,3}` and `{0,5}`, and the
  palette `{1,4}` meets **neither**: `{1,4} ∩ {2,3} = ∅`. So the licensing condition kills it, and my
  "minimal surviving obstacle" was not surviving at all.
* **R3.** Consequent scope correction: `F6-SIX-CYCLE.md`'s Theorem (two-palette 6-cycles impossible) stands,
  but its corollary "every genuine 6-cycle must use ≥ 3 palettes" is **weaker than I implied** — it does not
  follow that a ≥ 3-palette 6-cycle survives, and in fact Astra's 4-palette field shows such a thing **is**
  realisable. The correct statement is only: *the two-palette case is closed, and the ≥ 3-palette case is
  where the live question sits.*

## 1. Astra's field, audited line by line [relayed, checked by hand here]

`h = π/6`; `f(t) = ⌊t/h⌋ mod 4 = ⌊6t/π⌋ mod 4` on `ℝ/(2π)`; `P(t) = ({0,2}, {0,3}, {3,5}, {2,5})[f(t)]`.

| claim | check | verdict |
|---|---|---|
| 12 sectors of `π/6`; `f` cycles `0,1,2,3` three times round | arithmetic on `2π/h = 12` | ✓ |
| 60° shift = `2h` moves `f` by `2 mod 4`, hence to the **disjoint** partner | `{0,2}↔{3,5}`: disjoint ✓; `{0,3}↔{2,5}`: disjoint ✓ | ✓ |
| 120° shift = `4h` preserves `P` | `4 ≡ 0 mod 4` | ✓ |
| every single 60°-orbit uses exactly **2** palettes, the whole circle **4** | orbit `{t, t+π/3}` = `{P_f, P_{f+2}}` | ✓ |
| `A_0 = {f even}`, `A_1 = {f odd}`: each 60°-invariant, measure `½` | `f ↦ f+2` preserves parity; 6 of 12 sectors | ✓ |
| every `P` meets both side-allowed sets `{2,3}` and `{0,5}` | `{0,2}∩{2,3}={2}`, `∩{0,5}={0}`; `{0,3}∩{2,3}={3}`; `{3,5}∩{2,3}={3}`, `∩{0,5}={5}`; `{2,5}∩{2,3}={2}`, `∩{0,5}={5}` | ✓ all four |
| `γ = arccos(5/6) ∈ (π/6, π/3)` | `arccos(5/6) ≈ 33.56°`, and `30° < 33.56° < 60°` | ✓ |
| `f(t+γ) − f(t) ∈ {1,2} mod 4` | `γ/h ≈ 1.1186 ∈ (1,2)` | ✓ |
| same `A_i` returns have **opposite** Boolean phase | same parity ⇒ difference even ⇒ `= 2` (not `0`) ⇒ `P ↦` disjoint partner | ✓ |
| both same-phase `γ`-return sets are **null** | same phase ⇒ difference `0 mod 4`, impossible since difference ∈ `{1,2}` ⇒ the sets are **empty** | ✓ (empty, hence null) |

So the field is internally consistent and licensed by the combinatorial premises. **It is an angular model
only**: it is a function of the direction at one centre, not a colouring `ℂ → Fin 6`, so it is not an input
to any lemma in the tree and it does **not** refute `WeakColoring 6` — exactly Astra's own reading.

## 2. The exact global/partial two-state distinction [proof]

`two_state_impossible` (`States.lean:243`) requires **one** measurable `s : Angles → Bool` defined on the
**whole** circle, with

    RealState hc x {s = false} J   and   RealState hc x {s = true} K ,

i.e. the *entire* level set `{s = false}` must be a.e. inside `liftPalette x i` for every `i ∈ J`.

**Proposition.** No `Bool` coarsening of Astra's field satisfies both `RealState` premises, for any `J`, `K`.

*Proof.* A `Bool` on the circle that is a function of `f` must be either constant or `f mod 2` (up to
relabelling). If `s = f mod 2 =: A_0/A_1`, then `{s = false} = A_0` carries palettes `{0,2}` and `{3,5}`
alternately, each on half of `A_0`; so `A_0 ⊆ liftPalette x 0` fails on the half where the palette is
`{3,5}`, and `A_0 ⊆ liftPalette x 2` fails there too, while `A_0 ⊆ liftPalette x 3` fails on the other half.
The intersection `liftPalette x 0 ∩ liftPalette x 3` is null (a direction has one palette, and `{0,2}` and
`{3,5}` are disjoint), so no nonempty `J` works. A constant `s` fails even sooner. ∎

**The distinction, stated once.** The field is *orbitwise* two-state (2 palettes on each 60°-orbit) and
*globally* four-state. `two_state_impossible` quantifies over a **globally** two-valued `s`; the
`RealState` hypothesis is what forbids the orbitwise/global mismatch. So the correct inference is:

> orbitwise two states ⇏ one global pair of `RealState` sets,

and **Astra's field is precisely the counterexample to that inference**. It does not contradict
`two_state_impossible` — it shows the lemma's hypothesis is not automatic.

**The partial-set failure, in the tree's own vocabulary.** Astra's localised argument runs on a *partial*
set `A` (one `A_i`, measure `½`) and yields: no same-phase `γ`-return on `A`. That conclusion is
satisfied by the field (the same-phase return set is empty). What fails is the step from the partial set to
the whole circle: `states_densityOne` and `state_densityZero` (`States.lean:96,109`) are the machinery that
converts a `RealState` into a density statement, and they need the whole level set, not half of it.

## 3. ONE candidate multi-state analogue (proposed, then refuted)

**State family.** `r ∈ ℕ`, `r ≥ 2`; a measurable partition `A : Fin r → Set ℝ` of `Angles`; finsets
`J : Fin r → Finset (Fin k)` with `RealState hc x (A l) (J l)` for all `l`; a **rotation law**
`σ : Fin r → Fin r` with `t ∈ A l ⟹ t + π/3 ∈ A (σ l)` a.e. and `Disjoint (J l) (J (σ l))`; and the
generalised count bound `(univ \ ⋃_l J l).card ≤ 2`.

**Triangle-return constraint (the new ingredient).** For `γ` with `cos γ = 5/6` and `π/6 < γ < π/3`, there
is `σ_γ : Fin r → Fin r` with

    ∀ᵐ t, ∀ l, t ∈ A l → t + γ ∈ A (σ_γ l)          (γ is STATE-DETERMINED)

plus `σ_γ ≠ id` and `σ_γ ∘ σ = σ ∘ σ_γ` (the triangle shift commutes with the 60° shift).

**(MS) candidate.** Under those hypotheses with `r` finite, `False`.

**The candidate is REFUTED by Astra's field**, and this is the block's sharpest result. Take
`r = 4`, `A_l = {f = l}` (each of measure `¼`, on which the palette is the **single** set `J_l = P_l`, so
`RealState` holds for each `l`), `σ = (+2 mod 4)`, `J_l ∩ J_{l+2} = ∅` ✓, and
`⋃_l J_l = {0,2,3,5}` with complement `{1,4}`, so the count bound holds **at equality**. Every hypothesis
of (MS) except state-determination is satisfied. And `γ` is **not** state-determined: `f(t+γ) − f(t) ∈ {1,2}`
*depends on `t`*, so `t ∈ A_l` can give `t+γ ∈ A_{l+1}` or `∈ A_{l+2}`. Hence (MS) with the
state-determination hypothesis is not violated by the field — the field simply does not satisfy that
hypothesis, and (MS) gives no contradiction. Worse for the candidate: if (MS) is weakened to conclude that
state-determination *must* hold, the field is a counterexample to that conclusion.

> **So no purely state-theoretic generalisation of `two_state_impossible` can close the gap.** The
> four-palette field is a legitimate whole-circle object satisfying the state family, the rotation law and
> the count bound, and it evades every state-level constraint by making the triangle shift
> state-*indeterminate*. That indeterminacy is not a defect to be repaired but the actual content: it is
> what Astra calls the need for **stronger cross-type constraints from actual source production**.

## 4. Does the geometry worker's licensed relation apply? [source-checked]

Both candidate licensed relations fail to touch the model, which I checked rather than assumed:

* **`binary_centers_separated` (`BinaryPalettes.lean:123`)** needs `BinaryCenter x i j` at two distinct
  centres, where `BinaryCenter x i j := ∀ᵐ t, t ∈ paletteSet x i ∨ t ∈ paletteSet x j` (`:9`) means the
  palette is a.e. **contained in the fixed pair `{i,j}`**. Astra's four palettes are `{0,2}, {0,3}, {3,5},
  {2,5}`, and **no 2-set contains all four** (`{0,2}` omits `3,5`; `{3,5}` omits `0,2`; `{0,3}` omits `2,5`;
  `{2,5}` omits `0,3`; any other pair omits more). Hence **no `BinaryCenter` pair exists at any centre of
  this field**, and the separation theorem is inapplicable — not contradicted, inapplicable.
* **`m11`'s half-circle bound** `σ{e : T ⊆ P_x(e)} ≤ ½` is **satisfied with room**: each palette occupies
  3 of 12 sectors, so for `T` equal to one of the four palettes the measure is `¼ ≤ ½`, and for any other
  2-set it is `0`. The bound is external to the tree and I have not re-derived it; it is quoted from the
  record.
* `binary_alternation` (`:11`) and `binary_transport_invariant` (`:76`) are conditional on `BinaryCenter`,
  so they too are silent.

**Conclusion of the test:** every currently licensed relation is either inapplicable (needs `BinaryCenter`)
or satisfied with slack (`m11`). The field therefore survives the whole licensed layer, which is exactly
consistent with Astra's statement that the global step needs source production rather than combinatorics.

## 5. Scope ledger

* **[proof]** §2: no `Bool` coarsening of the field satisfies both `RealState` premises; the orbitwise/global
  mismatch is the precise reason `two_state_impossible` is not instantiable.
* **[proof]** §3: `r = 4` with `A_l = {f = l}` realises the state family with `RealState`, the rotation law
  `+2`, disjoint partners, and the count bound at equality; `γ` is not state-determined.
* **[refuted]** the (MS) candidate of §3 in both its forms (as a `False`-conclusion and as a
  state-determination conclusion).
* **[inapplicable]** `binary_centers_separated`, `binary_alternation`, `binary_transport_invariant`;
  **[satisfied with slack]** `m11`'s bound.
* **Not claimed:** any numerical bound; `WeakColoring 6` refuted (it is not — the field is angular only);
  any verdict on `F6`, `L6`, or cycle lengths other than 6; any claim that a finite orbit model being
  UNSAT would be a global result.
