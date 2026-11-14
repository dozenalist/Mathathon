# Next proposal (separate from the R4 deliverable): one duplicated proof obligation

**Analysis only.** Nothing implemented, nothing built, no saving claimed. The R4 frozen deliverable
(`encoding-core/integration/`, Spectrum `d26d5690…`, Limits `24f89dd3…`) is untouched by this file and
must not be modified while the 82-module queue runs.

## 1. The candidate: `norm_integral_sq`, duplicated byte for byte

| | location | lines |
|---|---|---|
| copy A | `lean/OAI/Analysis/PlaneSpectrum/Fourier.lean:96–113` (in `namespace EuclideanFiveColor.ProbabilityL2`) | 18 |
| copy B | `lean/OAI/MeasureTheory/CompactFactors/Kernels.lean:45–62` (in `namespace EuclideanFiveColor.KernelCompact`) | 18 |

Measured: the two texts are **identical byte for byte** (`texts identical: True`, 18 lines each). Not
merely the same conclusion — the same statement, the same tactic script, the same variable names. The
only difference is the enclosing namespace and the section's unused type variable (`Ω` resp. `Y`).

Frozen input hashes (read-only, unchanged):
`Fourier.lean` `315079396f8612ab5dea…`, `Kernels.lean` `8665ae62def8d70befc2…`,
`BoundedFunctions.lean` `e7acbec9b3d2d8c91a91…`, `Functions.lean` `53ed391142b8388df9ad…`.

## 2. The common logical statement

```lean
lemma norm_integral_sq (μ : Measure X) [IsProbabilityMeasure μ]
    (f : X → ℂ) (hf : Integrable f μ)
    (hf₂ : Integrable (fun x => ‖f x‖^2) μ) :
    ‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ
```

In words: **averaging contracts `L²`**. The proof is the variance decomposition
`0 ≤ ∫ (‖f‖ − a)²` with `a = ∫ ‖f‖`, combined with the triangle inequality `‖∫f‖ ≤ ∫‖f‖`. It is pure
Hilbert-space geometry: it says that the conditional-expectation operator, being an orthogonal
projection of `L²(μ)`, has operator norm at most one, written in the integral form the tower actually
consumes.

## 3. Hypothesis comparison: identity, not implication

| | copy A (kept) | copy B (deleted) | after extraction at B's call sites |
|---|---|---|---|
| `μ`, `[IsProbabilityMeasure μ]` | yes | yes | same term supplied |
| `f : X → ℂ` | yes | yes | same |
| `hf : Integrable f μ` | yes | yes | same |
| `hf₂ : Integrable (fun x => ‖f x‖^2) μ` | yes | yes | same |
| conclusion | `‖∫f‖² ≤ ∫‖f‖²` | identical | identical |

Because the statements are *identical* rather than inter-derivable, no call site needs any new
hypothesis, and no hypothesis can be silently strengthened: deleting B and calling A is a
renaming, not a re-derivation. This is the strongest possible form of "no strengthening of
assumptions" and the reason this candidate is preferred to anything in the wildness/weak-mixing
direction.

**All three uses of copy B** (measured by `grep -rn`):

| site | form |
|---|---|
| `Kernels.lean:101` | bare `apply norm_integral_sq` (same file, same namespace) |
| `BoundedFunctions.lean:211` | `exact KernelCompact.norm_integral_sq _ f (integrable _ …) …` |
| `Functions.lean:875` | `exact KernelCompact.norm_integral_sq (κ z) E (hEi z) (hE₂i z)` |

Copy A's own use (`Fourier.lean:131`) is unaffected. Both cross-module sites already import
`Kernels`, hence would see `Fourier` after one added edge (below), and both are applications, so the
*term* keeps its type exactly.

## 4. Why this is extractable at all — the cycle question, measured

The recorded reason for not merging these two (`sprint/simplify-lean/CENSUS.md`, result 1) was that
"the `norm_integral_sq` duplicate cannot be fixed by one import: it needs a shared low-level module".
**That conclusion is refuted by measurement:**

* `Fourier.lean` imports **`Mathlib` only** — its OAI import closure is **empty** (`|closure| = 0`).
* `Kernels.lean` imports `ConditionalLimits`; its closure is 14 modules and **does not contain
  `Fourier`**; conversely `closure(Fourier)` does not contain `Kernels`. The two are invisible to each
  other today.

Hence adding the single edge `Kernels → Fourier` **cannot create a cycle**: a cycle would need a path
`Fourier → … → Kernels`, and `Fourier` has no OAI imports at all. One import edge suffices.

What survives of the CENSUS objection is a *layering* worry, not a cycle: `Kernels` lives in the
measure-theory half and `Fourier` in the plane-spectrum half. But (i) `Fourier`'s `ProbabilityL2`
content is generic `L²` geometry with nothing plane-specific in it, and (ii) the tree already has
build edges from `CompactFactors` into `Analysis`, so the direction is precedented. The principled
alternative is variant 2 below.

## 5. Expected net line change (textual, uncompiled)

**Variant 1 — delete copy B, keep copy A, one import edge** (recommended):

```
  -18   Kernels.lean:45–62 (statement + proof), plus the now-redundant blank  = -19
   +1   import OAI.Analysis.PlaneSpectrum.Fourier                        in Kernels.lean
   +1   open EuclideanFiveColor.ProbabilityL2                            in Kernels.lean
    0   BoundedFunctions.lean:211, Functions.lean:875: KernelCompact. → ProbabilityL2. (in place)
-----
  -17   net
```

**Variant 2 — new leaf module `OAI.Analysis.NormIntegralSq` (imports `Mathlib` only), both sides import it:**

```
  -18 -18   both copies
   +24      new file (header, namespace, opens, the one lemma)
    +2      two import lines
-----
  -10   net, one more module in the tree (82 → 83), halves stay decoupled
```

Variant 1 is smaller and touches two files; variant 2 is smaller *conceptually* but adds a module and
loses lines. I recommend variant 1 now, and record variant 2 as the answer if the two halves are ever
separated.

## 6. Why the extraction clarifies the mathematics (not just the count)

The whole compact-extension apparatus — `KernelCompact`'s fibre means, `BoundedFunctions`, and the
`At`/`Compact` module machinery in `Functions.lean` — consumes exactly **one** analytic inequality:
averaging contracts `L²`. Today a referee meets that computation twice, in two namespaces, has to check
that the two 15-line scripts agree, and is left with the impression that "Fourier" and "kernels"
contribute two different inputs. After the merge, the tower's analytic input is a single named fact in
the leaf module, and the dependency edge `CompactFactors → PlaneSpectrum.Fourier` documents the true
statement of affairs: the compact-factor tower is `L²`-theoretic (orthogonal projection + contraction),
not transform-theoretic. That is the exposition point of deduplicating it — the line count is almost
incidental.

## 7. Rejected candidate, recorded

`sprint/simplify-lean/CENSUS.md`'s other cluster is **not** a duplication and is rejected:
`conditional_integer_pair_energy` (`Energy.lean:323–340`, 18 lines) and
`conditional_integer_triple_energy` (`Energy.lean:342–357`, 16 lines) are *not* copies of each other —
they have different conclusions (a product of two conditional energies vs a three-way identity with
conditional insertions) — and **both already call** the general
`conditional_integer_multiple_mean_zero` (`AlgebraModels.lean:652`) and already carry its `hdiv`
hypothesis. They are thin, single-use wrappers differing only in the `Fin.prod_univ_two` vs
`Fin.prod_univ_three` expansion and in the final energy identity applied. Merging them would push those
expansions into the call sites (`RadialEnergy.lean:97`, `:395`), buying roughly −24 lines at the cost of
two distinct statements becoming one opaque one. Genuine factoring is already done there; nothing to
extract.

## 8. Status, limits, falsifiers

* Not implemented: no patch, no new module, no build. `-17` (or `-10`) is a **textual estimate**.
* The two source files are shared originals and were read only; hashes above are their current values.
* Would be falsified by: (a) `Fourier` turning out not to be a leaf (measured: closure empty, so no);
  (b) a use of `KernelCompact.norm_integral_sq` that `grep -rn` missed because it is reached through
  `open`/`export` rather than by name; (c) `apply norm_integral_sq` at `Kernels.lean:101` resolving to
  something else once `open` widens the namespace; (d) the added import forcing a rebuild that
  perturbs the 82-module order beyond this closure.
* Compared with any wildness or weak-mixing proposal, this candidate's virtue is that its "no new
  assumption" claim is an *identity* of statements, checkable in two lines of source, not an argument.
