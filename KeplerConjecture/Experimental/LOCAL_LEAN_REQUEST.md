# Local request — Lean formalisation of the block-partition lemma

```text
request_id   = K15-EXP-004
status       = REQUESTED
owner        = i-ve-attached-thomas-4iws (E)
reviewer     = X (statement), Main (scope)
claim_id     = K15-E032 (R2' partition), K15-E001 Step 2/3 (shell count)
source_commit= see final report of the 2026-11-14 full-hour block
branch       = kepler15/experimental/run-01
dependencies = Lean v4.35.0, Mathlib v4.35.0 (pinned by the project)
resources    = 1 core, 8 GB, 20 min cap
```

## Why this lemma

It is the only stable, self-contained combinatorial statement produced so far. It does not
depend on the Tammes enclosure, on the dodecahedral theorem, or on any numerical input, so it
can be kernel-checked independently of the analytic route — which is exactly what a Lean
target should be at this stage.

## Statement to formalise

In a metric space `E` (use `EuclideanSpace ℝ (Fin 3)`), let `Λ : Finset E` be `2`-separated
(pairwise distances `≥ 2`). Fix `τ = 418/100` and `ρ = 209/100`. Define on `Λ` the relation
`u ~ v ↔ u ≠ v ∧ dist u v ≤ τ`, let `C` range over its connected components, and set
`N(C) = {s ∈ Λ : ∃ v ∈ C, dist s v ≤ ρ}`, `Block(C) = C ∪ N(C)`.

```lean
theorem blocks_pairwiseDisjoint
    (Λ : Finset (EuclideanSpace ℝ (Fin 3)))
    (hsep : ∀ u ∈ Λ, ∀ v ∈ Λ, u ≠ v → 2 ≤ dist u v) :
    ∀ C₁ C₂ : Set _, C₁ ≠ C₂ →
      Disjoint (block Λ C₁) (block Λ C₂)

theorem blocks_cover (Λ : Finset _) :
    Λ ⊆ ⋃ C ∈ components Λ, block Λ C

theorem block_diam_le (hC : C ∈ components Λ) :
    ∀ u ∈ block Λ C, ∀ v ∈ block Λ C, dist u v ≤ diam C + 418/100
```

The mathematical content is the one line proved in `GEOMETRIC_PARTITION.md` §K15-E032: if
`s ∈ N(C₁) ∩ N(C₂)` then `dist v₁ v₂ ≤ 2ρ = τ`, so `v₁ ~ v₂` and `C₁ = C₂`. The third
statement needs `diam C` as a hypothesis or a bounded-component assumption.

## Success criteria

```text
command   = lake build KeplerConjecture.Experimental.Blocks
expect    = exit 0, no `sorry`, and
            #print axioms blocks_pairwiseDisjoint  ->  [propext, Classical.choice, Quot.sound]
output    = build log + axiom output returned by Astra
```

## Current state

`PROPOSED`. No Lean source has been written, and I am not writing it speculatively: the
statement should be frozen by X first, since the `Block`/`components` definitions have to
match `GEOMETRIC_PARTITION.md` exactly and Mathlib's `Finset` component API may not
correspond to the graph-theoretic components intended. If X confirms the statement, the file
is a short formalisation.

## What this does not do

It does not touch the open inequalities `(T'-R2')`, does not formalise any numerical bound,
and gives no evidence about the density `π/√18`. It is infrastructure only.
