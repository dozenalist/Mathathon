# Adversarial audit of the end-to-end six-colour extension chain

Read-only audit of the actual sources: `results/COMPRESSED-PROOF.md` (the referee-checkable compression),
the Lean tree `lean/OAI/Geometry/PlaneColoring/`, and the retired k = 6 records. No computation; no
Lean build. Grades: **[paper-reviewed]** = the compression states it and marks its grade; **[computational]**
= machine-checked in the tree or certified by a run recorded elsewhere; **[proposed]** = mine, unverified.

**Bottom line.** The four-arrow decomposition is *structurally right*, and arrow 4 is genuinely `k`-generic.
But two of the four arrows are hard-wired to `k = 5` by their *proofs*, not merely by their statements, and
the third needs a constants pass at `α < 1/6`. **Ternary exclusion at `k = 6` would give `|P| ≤ 2`; it does
not give `χ ≥ 7`,** and I make no such claim.

## 1. Arrow 1 — ternary exclusion ⟹ palette size ≤ 2

**What is actually in the tree.** `BinaryPalettes.lean:252`:

    lemma palette_triple_null (c : ℂ → Fin 5) (hc : Measurable c) (hw : WeakColoring 5 c)
        (x : ℂ) (S : Finset (Fin 5)) (hS : S.card = 3) :
        ∀ᵐ t ∂angularMeasure, ¬ S ⊆ palette c hc x t

and `BinaryPalettes.lean:260`:

    lemma palette_cardinality (c : ℂ → Fin 5) (…) (x : ℂ) :
        ∀ᵐ t ∂angularMeasure, 1 ≤ (palette c hc x t).card ∧ (palette c hc x t).card ≤ 2

So the arrow *is* a machine-checked implication `palette_triple_null ⟹ palette_cardinality`, and
`palette_cardinality` has exactly five consumers: `Exclusion.lean:130`, `Interfaces.lean:78`,
`States.lean:319`, `Accumulation.lean:161` and `:361`. **[computational]**

**Why the proof cannot transfer.** `palette_triple_null`'s body computes
`(Finset.univ \ S).card = 2` (`:255`), extracts the complement as a pair with `Finset.card_eq_two`
(`:256`), and then invokes `ae_not_binary_circle c hc hw x i j` (`:258`) — a statement about **two**
labels. At `k = 6` the complement of a 3-set has **three** elements, so `card_eq_two` cannot fire and the
binary-circle lemma does not apply. The obstruction is in the proof, not in the statement.

**The arrow's shape, however, is `k`-generic**: `palette_cardinality` infers `|P| ≤ 2` from the exclusion
of `|P| ≥ 3`, and that inference is insensitive to `k`. So the missing object is exactly a `Fin 6`
`palette_triple_null`; nothing else in this arrow is `k`-specific. This reproduces, from the source, the
first of the three `k = 6` failures recorded in `results/K6-BARRIER.md`. **[paper-reviewed]**

## 2. Arrow 2 — local finiteness of transition cycles ℓ = 3…6 ⟹ finite core

**What is actually in the sources.** `results/COMPRESSED-PROOF.md` states Proposition 7.1 with
**`ℓ ∈ {3,4,5}`** — hard-wired, five labels. Its consumers in the tree terminate in
`FullApproximation.lean:330`, `theorem fullApprox_exists {c : ℂ → Fin 5}`, with the finite-core variant at
`:268`. **[computational + paper-reviewed]**

**The `α` threshold, located exactly.** Lemma 7.4 (`COMPRESSED-PROOF.md:986`) requires `0 < α < 1/5`
because it normalises

    q_i^ε = (p_i^ε − α)_+ / Σ_k (p_k^ε − α)_+ ,        denominator ≥ 1 − 5α > 0 ,

and the target is "the complete graph on five vertices". So the threshold is **exactly the inequality
`1 − kα > 0`, i.e. `α < 1/k`**: at `k = 5` it is `1/5`, at `k = 6` it is `1/6`. That is the whole content
of the `α < 1/k` phrase — it is a normalisation denominator, not a new geometric obstruction.

**What changes.** Two things, of different kinds:
* **`ℓ = 6`**: a new cycle length. The paper contains no `ℓ = 6` argument anywhere.
* **`α < 1/6` constants pass**: since `1/6 < 1/5`, every constant calibrated against `1/5` must be
  re-derived — the mesh bound (≤ 2 at `Lemma 7.5`), the radius `ρ`, and the `ε_n` sequence all descend from
  the α-dependent tree filling. Mechanical, but not free, and it is where a silent error would live,
  because a smaller `α` shrinks the disk budgets used in the tree-filling step.

## 3. Arrow 3 — exclusion of common-interface cycles ℓ = 3…6 ⟹ eventual forest / core filling

**What is actually in the tree.** The combinatorial objects are `k = 5`-specific finite types verified by
`decide`: `Exclusion.lean:17-24` has `five_admissible_diag`, `five_diag_disjoint`, `five_diag_nonempty`,
`five_diag_unique`, `five_adj_four`, `five_no_common_adj`, all on `Fin 5`; `Interfaces.lean:19-37` has
`interface_four_*` on `Fin 4 → Bool`. **[computational]**

**What changes at `k = 6`.** Three separate obligations: (i) a sixth object (6-cycle interface) that has
no counterpart; (ii) re-running the `Fin 5 → Fin 6` finite computations for the 3-, 4- and 5-cycle cases,
which is cheap but touches every `five_*` lemma; (iii) the paper's three cycle-exclusion arguments (lengths
3, 4, 5) are each proved by a *different* device — a parity rule for two diagonals at length 4, a
one-positive-one-negative sign run at length 5 — and the length-6 case has neither. `results/K6-BARRIER.md`
§4 records exactly this. **[paper-reviewed]**

## 4. Arrow 4 — the generic multiplicity-two covering contradiction

**This arrow is `k`-generic and needs nothing new.** Lemma 7.5 (`COMPRESSED-PROOF.md:997`) is

> a closed square of side ten has no relatively open cover of multiplicity ≤ 2 and mesh ≤ 2,

and the tree's `PlanarCover.compact_open_cover_impossible` (`PlanarCovers.lean:374`) is proved for a
general constant `R`, not for `2`, with the only topological input being
`Complex.exists_continuousOn_eqOn_exp_comp`; no Brouwer, no `Fin 5`. Multiplicity ≤ 2 is supplied by arrow 1
(via `|P| ≤ 2`), so **conditional on arrow 1 the covering contradiction costs nothing extra**.
**[computational]**

## 5. What the audit establishes, and what it refuses

* The decomposition is correct, and the *cheap* half of the work is already done: arrow 4 is generic and
  arrow 1's derivation `triple excluded ⟹ |P| ≤ 2` is `k`-insensitive.
* **Two arrows are blocked by their proofs, not their statements**: arrow 1 (`card_eq_two` on a
  two-element complement) and arrow 3 (every finite object is `Fin 5`/`Fin 4 → Bool`).
* **Ternary exclusion at `k = 6` does not give `χ ≥ 7`.** Even granted, one still needs the `ℓ = 6` cycle
  of Prop 7.1, the `ℓ = 6` interface exclusion, and the `α < 1/6` constants pass — and the whole §7
  assembly has an independent hypothesis (the local finiteness (W) of the cyclic locus) that no palette
  argument supplies. I make no claim that any subset of these proves `χ ≥ 7`.

## 6. The three highest-value exact missing lemmas

**L1 — ternary exclusion at `k = 6`.** **[proposed]**

    lemma palette_triple_null_six (c : ℂ → Fin 6) (hc : Measurable c) (hw : WeakColoring 6 c)
        (x : ℂ) (S : Finset (Fin 6)) (hS : S.card = 3) :
        ∀ᵐ t ∂angularMeasure, ¬ S ⊆ palette c hc x t

*Consuming declaration:* a `Fin 6` `palette_cardinality` (today `BinaryPalettes.lean:260` is `Fin 5`,
conclusion `|P| ≤ 2`), which would then be consumed by the `k = 6` analogues of `Exclusion.lean:130`,
`Interfaces.lean:78`, `States.lean:319`, `Accumulation.lean:161`, `:361`.
*Why it is the highest value:* it is the only arrow whose **statement** already transfers; a proof would
immediately give `|P| ≤ 2` at `k = 6` and make arrow 4 available. *Why it is hard:* the existing proof's
two decisive steps (`Finset.card_eq_two`, `ae_not_binary_circle`) both need a two-element complement.

**L2 — the `ℓ = 6` case of Proposition 7.1** (a six-cycle of common exclusion continua, at `α < 1/6`).
**[proposed]**

*Consuming declaration:* a `Fin 6` `fullApprox_exists` (`FullApproximation.lean:330` is `Fin 5`), i.e. the
finite-core / hole-approximation step that turns a cycle of exclusion continua into a disk computation.

**L3 — the `ℓ = 6` common-interface cycle exclusion (the forest / core-filling step).** **[proposed]**

*Consuming declaration:* the `k = 6` analogue of the `five_*` layer in `Exclusion.lean:17-24` and the
`interface_four_*` layer in `Interfaces.lean:19-37` — concretely, a 6-cycle interface object replacing
`Fin 4 → Bool`, plus `Fin 6` re-runs of `five_admissible_diag` and `five_adj_four`.

**Not one of the three, but on the critical path: the `α < 1/6` constants pass** (§2). It is a
re-parametrisation, not a lemma, and it must be done before L2's proof can be trusted at `k = 6`.

## 7. One proposed falsifying instance (not constructed)

**Target:** L1. **Instance sought:** a measurable weak 6-colouring `c : ℂ → Fin 6` and a point `x` such
that some 3-set `S ⊆ Fin 6` lies in `palette c hc x t` for a positive-measure set of directions `t`.

**Why this must be centre-dependent, and that is the useful part.** A **centre-independent** sector field
at `k = 6` cannot be the falsifier: on a centre-independent field the unit-triangle bound gives
`3|P| ≤ 6`, i.e. `|P| ≤ 2`, which is exactly why the 36-sector ternary word `{2,4,5}` was **withdrawn** in
the record (`sprint/k6/FREE-LABEL.md`). So any falsifier lives in the centre-dependent class — the same
class that `m10`'s Theorem 2 does not remove, and the same class the `k = 6` frontier is confined to. That
is a real narrowing of the search space and the reason the instance is worth stating at all.

**Status:** proposed, unconstructed, and it would refute L1 rather than any part of the paper.
`results/K6-BARRIER.md` §1 already notes that a centre carrying a *ternary* palette is "not by itself
contradictory" because the unit circle's unit-distance graph is a disjoint union of six-cycles and hence
2-colourable — consistent with, but not a construction of, the instance.

## 8. Exact SAT-relaxation constraints read from the record (not the summaries)

From `sprint/k6/REPORT.md` and `results/K6-BARRIER.md`, the constraints that were actually imposed, with
their record labels: **(5.2)** the colouring axiom; **(5.3)** two-centre transport;
**(5.7)** the sixty-degree exclusion `P_x(f) ∩ P_x(Rf) = ∅`; **Lemma 6.2 / (6.2)** the cycle edge
exclusions; **Lemma 5.5** binary-centre separation; **(8.4)** the region inequality. The retired k = 6
verdict on these, quoted rather than reinterpreted: `(T)`, `(SA)`, `(5.2)` and `(5.7)` are satisfiable at
every cycle length, `(T) + (5.7)` collapses to `(5.7)`, and no palette axiom proves (W) at `k = 6` without
proving the problem. **[paper-reviewed: these are the record's own findings, which I have not re-derived]**

Existing archives (unchanged, read-only): `sprint/k6/{REPORT,SYNTHESIS,FREE-LABEL,WEAKEST}.md`,
`results/continuation/SUMMARY.md`.

## 9. Status of this block's own artifacts

`combine/` (source-only witness-combination packet, nine fixtures, syntax-checked, never executed) is
**banked unchanged**; no benchmark and no closed-seed rerun was performed. `WITNESS-COMBINATION.md` carries
the corrected normalisation and the withdrawn runtime claim. No new placement work was started, and the
closed union is not revisited.
