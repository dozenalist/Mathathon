# Final review: corrected encoding-core integration (block 10)

Reviewed object: `supervisor/simplify-lean/snapshots/integ-48aa378f6f6db82b/` — a hash-frozen
copy of the architect's corrected revision, taken at 2026-11-14T09:24Z. Hashes confirmed against
the values supplied by the supervisor:

| file | sha256 | verdict |
|---|---|---|
| `OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean` | `48aa378f6f6db82bfeb0e65920ec2606507364541e72bf77ab969c6c87895dd1` | **matches** |
| `OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean` | `58707f0495837a89b58d5ac7d131ee855220c74cba28851474489b7a8cdd9e0d` | **matches** |

Analysis and source review only. No build, no cloud operation. Grades: [C] computed from the
frozen text, [R] read, [U] uncompiled.

## 1. [C] The repair touched exactly ONE file, and only by moving a block

`ConditionalLimits.lean`'s hash is **identical** to the version frozen in block 9
(`integ-d123de9bc689a01c`) — so the ambient side did not change at all. Diffing the block-9 and
block-10 frozen `ConditionalSpectrum.lean` gives `288a289,320` and `459,490d490`: a single 32-line
block, moved verbatim, in one direction. Nothing was edited, retyped, or reordered internally.

**Source-change flag:** the four declarations `abbrev FiniteEncodingApproximationAt`,
`def FiniteEncodingApproximation`, `lemma two_array_norm_bound`, `lemma simultaneous_test_budget`
moved from after the core theorem to before it. Relative to the *original* tree, the resulting order

```
FiniteEncodingApproximationAt → FiniteEncodingApproximation → two_array_norm_bound
  → simultaneous_test_budget → [new] uniform_precision_contradiction → finite_uniform_precision_contradiction
```

is exactly the original order of the four with the new theorem appended after them — i.e. PLAN §3's
anchor, and the original relative order is preserved. No declaration changed text.

## 2. [C] Declaration order: zero forward references remain

Re-ran the audit on the corrected file (`snapshots/integ-48aa378f6f6db82b/`):

| declaration | line |
|---|---|
| `def EncodingApproximationAt` | 273 |
| `abbrev FiniteEncodingApproximationAt` | 291 |
| `def FiniteEncodingApproximation` | 295 |
| `lemma two_array_norm_bound` | 299 |
| `lemma simultaneous_test_budget` | 305 |
| `theorem uniform_precision_contradiction` | 325 |
| `theorem finite_uniform_precision_contradiction` | 494 |
| `theorem finite_uniform_successor_contradiction` | 512 |

All **14** same-file identifiers the core body uses are declared before it; the latest is
`simultaneous_test_budget` at 305. **Forward references: NONE.** The block-9 defect is closed, and
closed by the minimal edit.

## 3. [R] Interface and abstraction fidelity

* **The interface is unchanged** from the version reviewed in block 8 — the diff contains no edit
  inside `EncodingApproximationAt`, the core theorem's statement, or its 151-line body. So block 8's
  findings carry over intact: the abstraction needs **no `Measurable S`** (because
  `FiniteModule.common_fiber_contradiction`, `ConditionalSelection.lean:259–271`, requires
  measurability only of `Hp`/`Hm` and takes `Integrable` of `Ap`/`Am` from `happrox`); `harc`'s
  `Measure Circle` has no competing instance (Mathlib declares none for `Circle`); `hwild` remains a
  hypothesis at `P`.
* **`S := p` / `S := id`**: the aliases are `EncodingApproximationAt μ p (fun x => q (p x)) p b m γ`
  and `EncodingApproximationAt μ p q id b m γ`; `H i (id x) ≡ H i x` is beta/delta on a reducible
  `id`. UNCOMPILED, and this is the one place a build can still surprise.
* **Namespace**: `namespace PlaneFiveColor.Spectral` opens at 172, its `section` closes at 256, so the
  inserted block at 273 is at namespace level with the `variable {X Y W : Type*}` block at 263 in
  scope — the same environment as the original `def`. Nothing new is `private`; required, since
  `ConditionalLimits.lean` uses `EncodingApproximationAt` and `uniform_precision_contradiction`
  across a module boundary.
* **Assumptions**: `omit [StandardBorelSpace Y] [Nonempty Y]` retained on the core; no instance and
  no import added in either file.
* **Custom axioms / sorry**: `rg` over both corrected files for `sorry`, `admit`, `^axiom`,
  `native_decide`, `@[implemented_by]`, `opaque`, `unsafe` → **no match**.

## 4. Corrected testing language (replaces my block-9 wording)

My block-9 note said a 14-module build "proves the definitions parse". That was wrong and is
withdrawn. The accurate statements are:

* A **14-module build proves typechecking** of the two edited modules and of every module they
  transitively import, at their actual types. It is a real check of the interface, the bodies, and
  `abbrev` transparency *within* that closure — not a parse check.
* A **full build checks downstream elaboration**: that every module which imports the edited ones
  still elaborates against the changed declaration kinds. It does **not** by itself establish
  "identical meanings"; statement identity is a separate, textual/`#check` matter (block 8 §F2), and
  the only semantic guarantee is the wrappers' unchanged statements plus definitional equality of the
  aliases.
* Consequently the value of the full build is *bounded by the actual reverse dependency set*, which
  is measured next — not by the module count.

## 5. [C] Reverse dependencies: 19 of 83, not 69

Computed from `MANIFEST-full.json` (no new scan of shared sources). The claim that all 69 modules
outside the smoke closure are affected is **not established and is false**:

| quantity | value |
|---|---|
| modules reverse-depending on the edited pair | **19** |
| modules depending on neither edit | **62** |

Only **two** modules import an edited module directly:

* `OAI.MeasureTheory.CompactFactors.Approximation` imports `ConditionalSpectrum` (build order 20)
* `OAI.MeasureTheory.CompactFactors.Kernels` imports `ConditionalLimits` (build order 22)

The full 19, in build order:
`Approximation`(20), `Kernels`(22), `BoundedFunctions`(23), `RelativeProducts`(24), `Separability`(25),
`AlgebraModels`(26), `Functions`(27), `Factors`(28), `Stationary`(29), `Representations`(30),
`Energy`(31), `RadialEnergy`(34), `SpectralMeasure`(35), `Ergodicity`(36), `BorelTransfer`(56),
`Five`(72), `Chromatic`(79), `NullSetRobust`(82), `Transfer`(83).

### Exact fully qualified consumers (replacing "Approximation.lean:414")

| consumer FQN | declaration site | consumes |
|---|---|---|
| `OAI.PlaneFiveColor.Spectral.finite_uniform_successor_contradiction` | `ConditionalSpectrum.lean:512` | root 1, same module |
| `OAI.PlaneFiveColor.Spectral.relative_singularity_successor` | `Approximation.lean:384` (call at 413–414) | root 1, cross-module, positional |
| `OAI.PlaneFiveColor.Spectral.relative_singularity_approximation` | `ConditionalLimits.lean:463` (call at 501) | root 2, same module |

### Which headline roots the edit can reach

* `OAI.EuclideanFiveColor.no_proper_five_coloring` (`Five.lean:133`) — **inside** the blast radius
  (`Five` → … → `Approximation` → `ConditionalSpectrum`). Must be re-checked.
* `OAI.Problem160.properColoring_seven` / `weakMeasurableColoring_seven` (`Seven.lean:36`, `:60`) —
  **outside** it: `Seven` is not among the 19. The χ ≤ 7 half is therefore provably untouched by
  this edit, which is worth stating positively rather than as caution.

## 6. Axiom policy (corrected)

Acceptance is **subset**, not equality: a root using only `propext`, or `[propext, Quot.sound]`, is
fine. `sorryAx` anywhere fails the claim (it means the transplanted body was not substituted); any
name outside `{propext, Classical.choice, Quot.sound}` fails (custom axiom).

## 7. Deliverables

* `supervisor/simplify-lean/lean/AxiomRoots.lean` — the axiom-root file: imports exactly the five
  modules declaring the nine roots, prints `#print axioms` for the three edited-surface theorems, the
  three named consumers, and the three headline roots, plus three `#check`s for `abbrev` arity.
* `supervisor/simplify-lean/axiom_gate.py` — the gate. Parses `depends on axioms:` lines including
  Lean's wrapped multi-line form, accepts any subset of the three, fails on `sorryAx` or a
  non-standard name, exits 2 if a root is missing (i.e. the file did not elaborate). Verified on a
  synthetic sample: a 2-element set PASSes, a wrapped 3-element set PASSes, missing roots give
  `GATE: FAIL` with rc 2.
* `supervisor/simplify-lean/MANIFEST-full.json` — full 83-module manifest (block 9, unchanged).
* `supervisor/simplify-lean/.scratch/revdeps.json` — the 19/62 partition with the two direct importers.

## 8. Limitations

* Nothing compiled here. Every Lean-level claim is textual.
* I reviewed the frozen copies, not the `.patch` files; a patch regenerated after 09:24Z would not be
  covered, which is why the hashes above are the object of record.
* The 19-module reverse closure is a statement about *import edges*, not about semantic influence: a
  module can import without using, and no module outside the 19 can be affected.
* "Definitional equality of the aliases" is the one claim a build must still confirm; the gate file
  checks the axioms, not the defeq.
