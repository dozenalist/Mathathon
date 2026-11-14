# Top-level statement audit: what we would actually certify (block 13)

Analysis only. No build. The encoding-core edits are **not** in the claim path below, and I do not
report the claim as locally verified: the root build and axiom prints are still outstanding.
Grades: [R] read from source at the cited line, [C] computed/derived here.

## 1. [R] The three public roots, verbatim

**(a) Hadwiger–Nelson lower bound, complex-plane vocabulary** — `Geometry/PlaneColoring/Five.lean:133`

```lean
theorem no_proper_five_coloring : ¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c
```

with `ProperColoring` from `Geometry/PlaneColoring/Coloring.lean:7`:

```lean
def ProperColoring (k : ℕ) (c : ℂ → Fin k) : Prop :=
  ∀ x y : ℂ, ‖x - y‖ = 1 → c x ≠ c y
```

**(b) Same claim in the bundle's own vocabulary** — `Geometry/PlaneColoring/Chromatic.lean:113`

```lean
theorem not_properColoring_five : ¬ ProperColoring 5          -- Problem160.ProperColoring
```
with `Problem160.ProperColoring` (`Geometry/PlaneColoring/Basic.lean:26`, `Plane := EuclideanSpace ℝ (Fin 2)`, line 11):

```lean
def ProperColoring (k : ℕ) : Prop :=
  ∃ c : Plane → Fin k, ∀ x y : Plane, dist x y = 1 → c x ≠ c y
```

**(c) The displayed inequality** — `Chromatic.lean:136`

```lean
theorem chromaticNumber_bounds : 6 ≤ planeChromaticNumber ∧ planeChromaticNumber ≤ 7
```
with `planeChromaticNumber : ℕ := sInf {k : ℕ | ProperColoring k}` (`Basic.lean:40`).

`(a)` and `(b)` are **proven** equivalent, not assumed: `Problem160.planeProperColoring_iff :
ProperColoring k ↔ ∃ d : ℂ → Fin k, EuclideanFiveColor.ProperColoring k d` (`Chromatic.lean:92`),
via `toPlane`/`ofPlane` (`Chromatic.lean:29,32`) and `dist_ofPlane`.

## 2. [R] The proof path, and where each hypothesis lives

`no_proper_five_coloring` is a one-step reduction (`Five.lean:133-137`):

```lean
rintro ⟨c,hc⟩
exact no_proper_five_coloring_algebraic ⟨fun x => c x, fun x y h => hc x y h⟩
```

* `no_proper_five_coloring_algebraic : ¬ ∃ c : E → Fin 5, LabelModel.Proper 5 c` (`Five.lean:126`),
  where `E := algebraicClosure ℚ ℂ` (`Analysis/PlaneSpectrum/Basic.lean:9`) and
  `LabelModel.Proper k ω := ∀ x y : E, ‖(x:ℂ)-(y:ℂ)‖ = 1 → ω x ≠ ω y`
  (`Analysis/PlaneSpectrum/Representations.lean:55`).
* The passage `ℂ → E` is a **restriction**, and it is definitionally transparent: the coercion is
  applied outside the subtraction, so the term `hc x y h` is passed unchanged. Nothing is transported
  back; the algebraic plane is used only to *obtain* the contradiction.
* Next: `proper_to_borel_weak_algebraic {k} [NeZero k] {c : E → Fin k} (hc : LabelModel.Proper k c) :
  ∃ d : ℂ → Fin k, Measurable d ∧ WeakColoring k d` (`BorelTransfer.lean:439`).
* Then: `no_measurable_weak_five_coloring {c : ℂ → Fin 5} (hc : Measurable c) (hw : WeakColoring 5 c) : False`
  (`Five.lean:105`), with `WeakColoring k c := AEMeasurable c volume ∧ ∀ᵐ p ∂(volume.prod angularMeasure),
  c p.1 ≠ c (p.1 + direction p.2)` (`Coloring.lean:27`).

## 3. [C] What the CLAIM assumes, versus what only the PROOF assumes

| ingredient | in the claim? | where |
|---|---|---|
| vertex domain | **yes** — all of `ℂ` (equivalently all of `EuclideanSpace ℝ (Fin 2)`) | `Coloring.lean:7`, `Basic.lean:26` |
| edge predicate | **yes** — distance *exactly* `1`: `‖x - y‖ = 1` / `dist x y = 1` | same |
| colour set | **yes** — `Fin 5`, i.e. exactly five labelled colours; `Fin k` in the general form | same |
| totality of the colouring | **yes** — a total function `ℂ → Fin 5`, no partial or a.e. reading | same |
| measurability | **no** | enters only at `BorelTransfer.lean:439` → `Five.lean:105` |
| algebraic plane `E` | **no** — the contradiction is transferred back; the claim quantifies over `ℂ` | `Five.lean:133` |
| `[NeZero k]` | **no** | instantiated at `k = 5` in the proof |
| angular measure / rotations / Fourier side | **no** | interior of the argument |
| conditional expectations, compact factors | **no** | interior; reached via `Approximation` |
| `Classical.choice`, `propext`, `Quot.sound` | **no** as hypotheses — they are *axioms used by the proof* | `open scoped Classical`, `noncomputable section` at `Five.lean:3-7` |

So the root statement is a **plain combinatorial claim about the unit-distance graph of the plane**,
with no regularity, no measurability and no conditional or tower hypotheses. Everything analytic sits
strictly inside the proof. This is the property that makes the result a Hadwiger–Nelson bound rather
than a bound on measurable colourings.

## 4. [C] Mismatch check against unrestricted Hadwiger–Nelson: none found

| requirement | in the development | verdict |
|---|---|---|
| vertex set is the full real plane | `ℂ` (root a) and `EuclideanSpace ℝ (Fin 2)` (root b), isometric via `toPlane`/`ofPlane` | ok |
| edges at Euclidean distance exactly 1 | `‖x - y‖ = 1` on `ℂ`; `dist x y = 1` on `EuclideanSpace ℝ (Fin 2)` | ok |
| colouring total, arbitrary (no regularity) | `∃ c : ℂ → Fin 5, …` | ok |
| conclusion is χ ≥ 6 | `¬ ∃ c, ProperColoring 5 c`, plus `not_properColoring_of_le` for all `k ≤ 5` | ok |
| upper bound χ ≤ 7 | `properColoring_seven`, `planeChromaticNumber_le_seven` | ok |
| both as one statement about χ | `chromaticNumber_bounds : 6 ≤ planeChromaticNumber ∧ … ≤ 7` | ok |

Two things a referee should still be told, neither a mismatch:

1. `planeChromaticNumber` is `sInf` on `ℕ`. `sInf ∅ = 0`, so the numeric value depends on the set
   being inhabited; `6 ≤ …` uses `properColoring_seven` for exactly that. This is a proof obligation,
   discharged — not a hidden hypothesis.
2. `Fin 0` is empty, so `ProperColoring 0` is false; monotonicity `properColoring_mono` covers `k ≤ 5`
   including `0`. Consistent, no special case needed.

## 5. [C] The claim does not depend on the encoding-core edits

`no_proper_five_coloring` lives in `Five` (build order 72), which *is* reverse-dependent on the edited
pair through `Approximation → ConditionalSpectrum` (block 11). So the **proof** route is touched, but
the **statement** is not: the statement mentions no encoding predicate, no `IsWild`, no conditional
kernel. A statement-level regression is therefore only possible through the `def → abbrev` change if
some name in the statement had unfolded differently — which is exactly what `SignatureEquivalence.lean`
and `SignatureCheckFresh.lean` test, and neither the statement of (a), (b) nor (c) mentions those
definitions at all.

## 6. Status discipline

Not claimed: that `no_proper_five_coloring` or `chromaticNumber_bounds` has been re-verified locally.
The checks that would license that claim are (i) the 82-module build completing, (ii) `AxiomRoots.lean`
printing a subset of `{propext, Classical.choice, Quot.sound}` for `no_proper_five_coloring`, and
(iii) the signature packets passing. None of the three has been done in this block.
