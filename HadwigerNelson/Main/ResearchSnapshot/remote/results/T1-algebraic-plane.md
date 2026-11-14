# T1. The chromatic number of the plane is the chromatic number of the algebraic plane

**Status: proved and machine-verified (Lean 4.34.1, pinned Mathlib d13f23b).**

Let `E = algebraicClosure ℚ ℂ ⊂ ℂ`, regarded as a unit-distance graph: vertices are the
points of `E`, edges are the pairs at Euclidean distance exactly `1`. Write `χ(E)` for its
chromatic number and `χ(ℂ)` for the chromatic number of the plane.

## Theorem T1

`χ(E) = χ(ℂ)`. More precisely, for every positive integer `k` the following are equivalent:

1. `E` has a proper `k`-colouring;
2. `ℂ` has a proper `k`-colouring;
3. `ℂ` has a weak measurable `k`-colouring (paper, Definition 1.2).

Consequently
`6 ≤ χ(E) = χ(ℂ) ≤ 7`,
and, by de Bruijn–Erdős, `χ(ℂ) = sup { χ(F) : F ⊂ E finite }`. In particular a finite
unit-distance graph witnessing `χ(ℂ) ≥ 6` can be chosen with **algebraic coordinates**.

## Proof

`(2) ⇒ (1)` is restriction of a colouring to `E`. `(2) ⇒ (3)` is the fact that a proper
colouring is weak measurable (its set of monochromatic unit pairs is empty).

`(3) ⇒ (2)` is the converse half of the paper's Theorem 1.3: Lemma 4.3 shows that the
full-density-point set of each colour class contains no unit pair, these sets are conull and
disjoint, every finite configuration can be translated into a conull set, and Tychonoff
compactness in `{1,…,k}^ℂ` produces a global proper colouring.

`(1) ⇒ (3)` is the content. It is the paper's Proposition 4.2, and its proof only ever uses
the colouring restricted to `E`: the first line is "restrict the given coloring to `E`", the
compact space `Ω` is a closed set of labelings of `E`, the invariant mean lives on
`E ⋊ K`, the character group is the dual of `E^disc`, and the measurable fields are
produced from the Koopman representation of that system. The values of the colouring off `E`
are never used. Hence the hypothesis of Proposition 4.2 can be weakened from
"`ℂ` is properly `k`-coloured" to "`E` is properly `k`-coloured", with the same conclusion.

The paper states Proposition 4.2 in the weaker form (hypothesis on `ℂ`); the strengthening is
a statement about the lemma's proof, not a new argument.

## Lean formalisation

Three new modules plus two edits:

* `lean/OAI/Geometry/PlaneColoring/Converse.lean` — the finite-configuration lemma
  (`finite_config_proper`), the compactness theorem `exists_properColoring_of_finset`
  (finite characterisation via Tychonoff in `ℂ → Fin k`), and `properColoring_of_weak`
  (weak measurable ⟹ ordinary proper colouring). This direction was **not** in the bundle.
* `lean/OAI/Geometry/PlaneColoring/Transfer.lean` — `proper_iff_weak` (Theorem 1.3 in both
  directions) and `algebraic_colorable_iff` (T1, fully formalised).

The two edits are in `lean/OAI/Geometry/PlaneColoring/BorelTransfer.lean` and
`lean/OAI/Geometry/PlaneColoring/Five.lean`:

* `proper_to_borel_weak_algebraic` : for `c : E → Fin k`, `LabelModel.Proper k c →
  ∃ d : ℂ → Fin k, Measurable d ∧ WeakColoring k d`. The proof body is the original proof
  verbatim; only the binder changed, because `PlaneFiveColor.LabelModel.Space k` was always
  the space of proper labelings of `E`.
* `no_proper_five_coloring_algebraic : ¬ ∃ c : E → Fin 5, LabelModel.Proper 5 c`, with
  `no_proper_five_coloring` recovered from it by restriction.

Verified in this VM with `source scripts/env4341.sh && lean results/lean/Check2.lean`:

```
OAI.EuclideanFiveColor.algebraic_colorable_iff :
  ∀ {k : ℕ} [NeZero k], (∃ c, LabelModel.Proper k c) ↔ ∃ c, ProperColoring k c
OAI.EuclideanFiveColor.proper_iff_weak :
  ∀ {k : ℕ} [NeZero k], (∃ c, ProperColoring k c) ↔ ∃ c, Measurable c ∧ WeakColoring k c
```

and `#print axioms` on the algebraic lower bound, the plane lower bound, the seven-colouring and
the two equivalences all report `[propext, Classical.choice, Quot.sound]`.

## Why it matters

* It is the strongest form of the lower bound that the method yields: a *countable* graph
  already needs six colours.
* It locates the finite witness: its vertices can be taken algebraic, so a certificate can be
  written in exact arithmetic in a number field, as the problem statement demands.
* It isolates exactly what the transfer theorem needs: a proper colouring of the algebraic
  plane, not of the plane.
