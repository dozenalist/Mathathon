# Candidate: deduplicate `norm_integral_sq`, preserving BOTH public names

**Status: candidate. Uncompiled. No build, no cloud compute, no edit to shared originals or to the
frozen R4 candidate.** Everything here lives under `dedup-norm-integral-sq/`.

## 1. Correction of my earlier arithmetic

My previous block claimed `−17` for "delete 18, add import, add open". That was wrong by the redundant
blank line I silently counted: 18 − 1 − 1 = **−16**, as the supervisor says. The present candidate is a
different design (alias instead of deletion), so its number is different again — measured, not
estimated: **−12**.

## 2. The two locations and the identity

| | location | content |
|---|---|---|
| copy A (kept, proof-bearing) | `Analysis/PlaneSpectrum/Fourier.lean:96–113` | 18 lines, `EuclideanFiveColor.ProbabilityL2.norm_integral_sq` |
| copy B (proof replaced by wrapper) | `MeasureTheory/CompactFactors/Kernels.lean:45–62` | 18 lines, `EuclideanFiveColor.KernelCompact.norm_integral_sq` |

The two 18-line texts are **identical byte for byte** (measured: `texts identical: True`), including
hypotheses `(hf : Integrable f μ)`, `(hf₂ : Integrable (fun x => ‖f x‖^2) μ)` and conclusion
`‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ`. So the substitution is a *renaming of the proof object*, not a
re-derivation: no hypothesis can move, at any call site, in either direction.

## 3. What the candidate changes (exactly two hunks, one file)

```diff
--- a/lean/OAI/MeasureTheory/CompactFactors/Kernels.lean
+++ b/lean/OAI/MeasureTheory/CompactFactors/Kernels.lean
@@ -1,4 +1,5 @@
 import OAI.MeasureTheory.CompactFactors.ConditionalLimits
+import OAI.Analysis.PlaneSpectrum.Fourier
 ...
@@ -45,21 +46,8 @@
 lemma norm_integral_sq (μ : Measure X) [IsProbabilityMeasure μ]
     (f : X → ℂ) (hf : Integrable f μ)
     (hf₂ : Integrable (fun x => ‖f x‖^2) μ) :
-    ‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ := by
-  … 14 lines of proof …
+    ‖∫ x, f x ∂μ‖^2 ≤ ∫ x, ‖f x‖^2 ∂μ :=
+  EuclideanFiveColor.ProbabilityL2.norm_integral_sq μ f hf hf₂
```

The statement lines are reused **verbatim** from the original (only `:= by` becomes `:=`), so the
public statement of `KernelCompact.norm_integral_sq` is unchanged to the character. The name stays, so
this is **not** an API break: the three consumers are untouched.

### Measured line arithmetic

| step | lines |
|---|---|
| duplicate block `Kernels.lean:45–62` | −18 |
| wrapper (statement 4 lines with `:=`, body 1 line) | +5 |
| added import | +1 |
| **file length** 774 → 762 | **−12** |

For comparison, the *pure deletion* variant (drop the name entirely, rename the three call sites) is
−16 as you state, and it does break the public name `EuclideanFiveColor.KernelCompact.norm_integral_sq`.
Alias preservation costs 4 lines and buys zero API change; I recommend the alias.

## 4. Import DAG and affected closure

New edge (the only structural change):

```
Kernels  ──new──▶  Analysis.PlaneSpectrum.Fourier  (163 lines, imports Mathlib ONLY)
   │                        └── no OAI imports at all: closure(Fourier) = ∅
   └──▶ MeasureTheory.CompactFactors.ConditionalLimits ──▶ … (14 modules)
```

* **No cycle is possible**: a cycle would need a path `Fourier → … → Kernels`, and `Fourier` has no OAI
  imports. This is why the fix is one edge, and it refutes CENSUS's "cannot be fixed by one import".
* **Closure of `Kernels`** (measured): 15 OAI modules, unchanged in *count* — `Fourier` was already in
  it. So the OAI import closure does **not grow**.
* **Mathlib weight: zero added.** `Fourier` imports the umbrella `Mathlib`, and five modules already in
  `closure(Kernels)` import it (`SmallArcs`, `InvariantMean`, `Centers`, `Basic`, `PhaseEncoding`).
* **Reverse closure** (modules that must rebuild whenever `Kernels` or now `Fourier` changes): **17** —
  `Energy, Ergodicity, RadialEnergy, Representations, SpectralMeasure, BorelTransfer, Chromatic, Five,
  NullSetRobust, Transfer, AlgebraModels, BoundedFunctions, Factors, Functions, RelativeProducts,
  Separability, Stationary`. That is the real cost: `Fourier` acquires 17 dependents it did not have.

Full lists: `affected.json`.

## 5. Files, hashes

| artefact | sha256 |
|---|---|
| original `Kernels.lean` (774 lines) | `8665ae62def8d70befc2929f9ae787f15b68e5c007a95c3257c011823059fe89` |
| candidate `Kernels.lean` (762 lines) | `050bb27408fa871c3026bf0529b18283c299c5f89c3a09db3c131f5b71eac623` |
| `Fourier.lean` (unchanged, 163 lines) | `315079396f8612ab5dea11fe22913e20a73e780862fba140148dd57ad4655a05` |
| `0001-kernels-norm-integral-sq.patch` | `680879c3b05869ca6203995cfdab169bcb1a53518d2101970c6982c5012561a9` |

## 6. Smoke checks

`SmokeNames.lean` checks: both names exist (`#check`); they have the **same type**; and `#print axioms`
on both names and on the three consumers' enclosing lemmas (`fiberMean_l2_bound`,
`conditional_norm_l2_le`, `compact_descend`), expecting `[propext, Classical.choice, Quot.sound]`.

**Correction (this block).** An earlier version of the smoke file asserted
`KernelCompact.norm_integral_sq μ f hf hf₂ = ProbabilityL2.norm_integral_sq μ f hf hf₂` **by `rfl`** and
called that a certificate of "the same proof object". **Withdrawn**: by proof irrelevance, any two
proofs of the same proposition are definitionally equal, so that `rfl` holds for every pair of proofs of
this statement and witnesses nothing about implementation identity. What is actually true is a
*source-level* fact: the wrapper's body is the term `…ProbabilityL2.norm_integral_sq μ f hf hf₂`. The
checkable content is therefore type identity plus the source reading — there is no `rfl`-level
implementation-identity certificate, and the file no longer pretends to one.

## 7. Recommendation: **defer** — a real but small win, not worth a build cycle now

For:

* It removes a *duplicated proof*, which is a fidelity risk (two 18-line scripts that must agree
  forever; if one is ever repaired the other silently stays wrong). That is the genuine mathematical
  argument, and it is why I would keep this on the list.
* It costs zero new hypotheses, zero Mathlib weight, zero OAI closure growth, and zero API change.
* The exposure is one import edge and two hunks in one file.

Against, and why I come out negative for this sprint:

* `−12` out of ~31 000 lines is 0.04 %. On the frozen R4 scale (`−126`) this is a rounding error.
* It gives `Fourier` seventeen dependents it did not have, for a lemma that is *already* stated and
  proved correctly on both sides. Coupling bought to save twelve lines.
* The 82-module audit is currently mid-flight; inserting a new edge now perturbs the affected closure
  and the rebuild order exactly when a stable revision is the thing of value.

**Verdict:** positive-as-cleanup, negative-as-a-sprint-item. Do it when `Kernels.lean` is next opened
for another reason, or when a fidelity audit of duplicated lemmas is run anyway; do not spend a build
cycle on it now, and do not bundle it with R4.

## 8. Falsifiers (what would make the candidate wrong)

1. `EuclideanFiveColor.ProbabilityL2.norm_integral_sq` not resolving from inside
   `namespace OAI.EuclideanFiveColor.KernelCompact` — expected to resolve by namespace-prefix trimming;
   if not, the body needs `OAI.`-qualification (no semantic change).
2. The `rfl` in `SmokeNames.lean` failing, which would mean the wrapper is not literally the same proof
   object (it should be, by construction).
3. A consumer of `KernelCompact.norm_integral_sq` that `grep -rn` missed because it is reached through
   `export`/`open` rather than by name.
4. `Fourier` turning out not to be a leaf (measured: `closure(Fourier) = ∅`, `import Mathlib` only).
