# LOCAL build/validation packet — common encoding core

Purpose: everything a reviewer on the isolated Windows Lean queue needs to re-derive the result
without consulting any summary. Companion: `REVIEW-encoding-core.md` (findings, citations).
**No item in this packet has been built here.** Grade: [C] computed, [R] read, [U] uncompiled.

## 1. Pinned manifest (verified on this VM, not quoted)

| item | value | how checked |
|---|---|---|
| Lean | 4.34.1, commit `5045d0056413266e57c625dcd7c365b10e377c52`, `x86_64-unknown-linux-gnu`, Release | `source scripts/env4341.sh && lean --version` |
| Mathlib | `d13f23b723b8a846827a245b89c10fc7d3f11612` | `git -C .scratch/mathlib4 rev-parse HEAD` |
| binary path | `.scratch/toolchain/bin/lean` (prepended by `scripts/env4341.sh`) | that script |
| `LEAN_PATH` root | `lean/build/lib` + pinned mathlib `.lake/build/lib/lean` + packages | `scripts/env4341.sh` |

Both pins match the values stated in the brief exactly. The brief's "minimal cache" corresponds to
this VM's `.scratch/toolchain` + `.scratch/mathlib4` pair; the Windows serial queue needs its own
warm mathlib, since a cold `import Mathlib` is ~20 s of disk read and the 14-module closure below
reaches Mathlib transitively through all of them.

## 2. Import roots and root-closed dependency list (14 modules, 7,533 lines)

Roots: `OAI.Analysis.PlaneSpectrum.ConditionalSpectrum` and
`OAI.MeasureTheory.CompactFactors.ConditionalLimits`. Closure computed by BFS over `^import`
lines of all 83 modules (script in §6). Order below is a **topological order, dependencies first**,
i.e. the per-module compile order; sha256 is of the sha256-of-file at the time of the review.

| # | module | path | lines | sha256 |
|---|--------|------|-------|--------|
| 1 | `OAI.Analysis.PlaneSpectrum.Basic` | `lean/OAI/Analysis/PlaneSpectrum/Basic.lean` | 735 | `6db8eef0290bb1962405e338d049d19a1a77ff9e58a50251ca0aa6835c2b3d16` |
| 2 | `OAI.Analysis.PlaneSpectrum.Characters` | `lean/OAI/Analysis/PlaneSpectrum/Characters.lean` | 560 | `3879bd9d07340af833a1350db7add3ab03d856af920410ce7bb9c24dc17d5f07` |
| 3 | `OAI.Analysis.PlaneSpectrum.InvariantMean` | `lean/OAI/Analysis/PlaneSpectrum/InvariantMean.lean` | 1078 | `33798cddc6dc5be9c3f2c963d393da2b4b5274f45f0f255dcb9b36c565f4b84b` |
| 4 | `OAI.Analysis.PlaneSpectrum.Multipliers` | `lean/OAI/Analysis/PlaneSpectrum/Multipliers.lean` | 314 | `6bc285bc0da10d8ed7875b03f8ca49a6d2c8fa19a4597b1bb09b01018bf8c092` |
| 5 | `OAI.Analysis.PlaneSpectrum.FourierTests` | `lean/OAI/Analysis/PlaneSpectrum/FourierTests.lean` | 295 | `f3625fb3399e28a5db3f531b7d2ac602988a8656fb28e6dd0747167a4be1393c` |
| 6 | `OAI.Analysis.PlaneSpectrum.SmallArcs` | `lean/OAI/Analysis/PlaneSpectrum/SmallArcs.lean` | 322 | `9c317fcfa15cf19a00aef927007704e78cf33269bb82d45065cb8a95160fe690` |
| 7 | `OAI.Analysis.PlaneSpectrum.PhaseEncoding` | `lean/OAI/Analysis/PlaneSpectrum/PhaseEncoding.lean` | 255 | `e941182ef95925e8472e94f79b1cc8adce7ee289f626d87f06d6d8092270ec54` |
| 8 | `OAI.Analysis.PlaneSpectrum.PhaseCollision` | `lean/OAI/Analysis/PlaneSpectrum/PhaseCollision.lean` | 537 | `10d6acf8d99c8209f225e9b35d1cbb4e4ab0738840b481bf7f72739534bb2627` |
| 9 | `OAI.MeasureTheory.CompactFactors.ConditionalSelection` | `lean/OAI/MeasureTheory/CompactFactors/ConditionalSelection.lean` | 442 | `2f19feac00b8ec75d265e04707bdda09aecb6bfb44965d34646f568743ca8e66` |
| 10 | `OAI.Analysis.PlaneSpectrum.ConditionalSpectrum` | `lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean` | 497 | `6602b9d8f20bbdfd447f2f3fcfa523f2c33d09c247e3d2983be7503df9f2dc9b` |
| 11 | `OAI.MeasureTheory.CompactFactors.Centers` | `lean/OAI/MeasureTheory/CompactFactors/Centers.lean` | 703 | `de094ea004737839cae2ce4829db40c78a2f1da8031459188ad5c271a7d98634` |
| 12 | `OAI.MeasureTheory.CompactFactors.RelativeCenters` | `lean/OAI/MeasureTheory/CompactFactors/RelativeCenters.lean` | 598 | `cae5e5e4cca54436788e66ea37b0a8818ef1156d8ccbbcb443bf7884169f7577` |
| 13 | `OAI.MeasureTheory.CompactFactors.Approximation` | `lean/OAI/MeasureTheory/CompactFactors/Approximation.lean` | 496 | `f6adcc691c345ddbe4fad40746f2e0da11be96b961c528f49af01e9ea8e5c30d` |
| 14 | `OAI.MeasureTheory.CompactFactors.ConditionalLimits` | `lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean` | 701 | `ca74ba1033fead55133670218739a36b4c75173d9b04d765affd19da9d215cc0` |
Note the order-cost of the merge: with the core placed in `ConditionalSpectrum` (position 10), a
change there invalidates positions 11–14 (Centers → RelativeCenters → Approximation →
ConditionalLimits), 2,338 lines. A change confined to the ambient wrapper invalidates only
position 14.

## 3. Expected public theorem signatures [U]

Unchanged from today, byte-identical (checked, §4):

```lean
OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction :
  (μ : Measure X) [IsProbabilityMeasure μ] → (p : X → Y) → (q : Y → W) → (b : X → D) →
  Measurable p → Measurable q → Measurable b → (m : ℕ) → 0 < m → (g : Y → Fin m → D) →
  (∀ᵐ y ∂μ.map p, condDistrib b p μ y = (m : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (g y i)) →
  IsWild (differenceLaw (μ.map (q ∘ p)) (condDistrib b (q ∘ p) μ)) →
  (ρ c : ℝ) → (N : ℕ) → 0 < ρ → 0 < c → 0 < N → harc → happrox → False

OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction : — same shape with
  (q : X → W), IsWild (differenceLaw (μ.map q) (condDistrib b q μ)), AmbientEncodingAt
```

New items, expected but **not** in the tree yet:

```lean
OAI.PlaneFiveColor.Spectral.EncodingApproximationAt (μ) [IsProbabilityMeasure μ] (p : X → Y)
  (P : X → W) {Z : Type*} (S : X → Z) (b : X → D) (m : ℕ) (γ : ℝ) : Prop
OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction   -- same hypotheses at (P, S)
```

Naming caveat for integration: the delivered preview uses `FiniteEncodingApproximationAt'` /
`AmbientEncodingAt'` with primes purely to coexist with the imported originals; at integration the
aliases must take the **unprimed public names**, and `abbrev AmbientEncodingAt` must stay in
`ConditionalLimits.lean` (its current home, downstream of the core), not move into
`ConditionalSpectrum.lean`. A home move is not a statement change but belongs in the delta record.

## 4. Statement delta [C]

Extracted `theorem … :` text from source and from `Wrappers.lean`, whitespace-normalised, compared:
**identical for both roots**. Delta = ∅. The only diff the script produced was its own trailing
`:= by` strip. Script: §6.

## 5. Axiom-check commands [U]

Run after the full 83-module build is rc 0. In this repo's environment:

```bash
source scripts/env4341.sh
cat > supervisor/simplify-lean/lean/CheckCore.lean <<'EOF'
import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits
#print axioms OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction
#print axioms OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction
#print axioms OAI.PlaneFiveColor.Spectral.uniform_precision_contradiction
#check @OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction
#check @OAI.PlaneFiveColor.Spectral.ambient_uniform_precision_contradiction
EOF
lean supervisor/simplify-lean/lean/CheckCore.lean
```

Required output: all three lines `depends on axioms: [propext, Classical.choice, Quot.sound]`.
Any `sorryAx`, or a fourth axiom, fails the check regardless of compilation. The two `#check` lines
must show `Measure Circle` at the same position as the pre-change `#check` — the instance-identity
test of REVIEW F5.

## 6. Reproducing the checks in this packet

```bash
cd <repo>
python3 supervisor/simplify-lean/.scratch/check_scope.py   # §2 closure, import direction, missing ids (0.3 s)
python3 supervisor/simplify-lean/.scratch/closure_order.py # §2 sha256 + topological order (0.3 s)
```
Both are stdlib-only, deterministic, write nothing, and each runs well under the 60 s cap.

## 7. What this packet does NOT establish

* That the merged core or either wrapper **compiles**. Nothing was built (instruction: no Lean/lake
  builds this block). Every Lean statement above is [U].
* That the transplant body is semantically the right one at `S := id` — only that the statement text
  matches and that `Iff.rfl` is the correct certificate to demand.
* That `abbrev` conversion leaves all 83 modules compiling. This needs the full-tree build, not the
  14-module closure, because alias transparency reaches downstream declarations.
