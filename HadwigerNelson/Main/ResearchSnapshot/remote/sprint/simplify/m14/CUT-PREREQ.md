# Cut prerequisite (m14): the two blocking relocations are done

Patch: `sprint/simplify/m14/cut-prereq-differenceLaw.patch` (363 diff lines; apply with
`patch -p1` from `lean/`). Prepared tree: `sprint/simplify/m14/tree/lean/OAI`.

## What this is for

Findings f33/f36/f37/f38 measured what a successful R1/R11/R16 (a new terminal-factor proof
replacing `UniversalGood` and the approximation property) would let the tree delete: about
3400-3600 lines. The zone could not be deleted because two of its declarations are consumed by the
surviving rigidity proof. This patch moves both out, with namespaces unchanged so every downstream
reference resolves as before.

## Patch contents

| file | before | after | change |
|---|---|---|---|
| `Analysis/PlaneSpectrum/FourierTests.lean` | 295 | 235 | drops the `EuclideanFiveColor.DifferenceFourier` block, imports it instead |
| `Analysis/PlaneSpectrum/DifferenceLaw.lean` | - | 72 | NEW: that block verbatim (`differenceLaw`, `differenceLaw_probability`, `coe_character_div`, `independent_coefficient`, `difference_coefficient`, `difference_coefficient_nonneg`), imports Mathlib only |
| `MeasureTheory/CompactFactors/Approximation.lean` | 496 | 425 | drops `EuclideanFiveColor.DifferenceInvariant` (`differenceLaw`, `invariant`), `KernelSupport.factor_smul_preserving` and `PlaneFiveColor.Spectral.relative_difference_invariant`; imports the new module |
| `MeasureTheory/CompactFactors/DifferenceInvariant.lean` | - | 98 | NEW: those three blocks verbatim; imports `DifferenceLaw` and `RelativeCenters` |
| `Analysis/PlaneSpectrum/Ergodicity.lean` | 415 | 417 | imports both new modules (+2) |

Net now +41 lines: preparation, not a saving. It removes the two dependencies that prevented the
~3400-line zone from being deleted:

* `DifferenceFourier.differenceLaw` is the predicate in the statement of `UniversalGood`
  (ConditionalLimits.lean:669) and of `IsWild (differenceLaw ...)` at Ergodicity.lean:30, :37, :56;
  it was defined in FourierTests, inside the zone.
* `relative_difference_invariant` (formerly Approximation.lean:304) is used at Ergodicity.lean:56
  to conclude that the terminal difference law is wild.

## Verification (pinned toolchain: Lean 4.34.1 + mathlib d13f23b)

Each module was elaborated individually against a build directory holding the pristine oleans of
the base tree plus the oleans of the two new modules, so every other import resolves to the
unmodified development:

```
source scripts/env4341.sh; B=<scratch>/build; export LEAN_PATH="$B:$LEAN_PATH"
cp -r lean/build/lib/OAI $B/     # pristine oleans
lean -o $B/OAI/Analysis/PlaneSpectrum/DifferenceLaw.olean             .../DifferenceLaw.lean       # rc 0
lean -o $B/OAI/MeasureTheory/CompactFactors/DifferenceInvariant.olean .../DifferenceInvariant.lean   # rc 0
lean -o $B/OAI/Analysis/PlaneSpectrum/FourierTests.olean              .../FourierTests.lean        # rc 0
lean -o $B/OAI/MeasureTheory/CompactFactors/Approximation.olean       .../Approximation.lean       # rc 0
lean -o $B/OAI/Analysis/PlaneSpectrum/Ergodicity.olean                .../Ergodicity.lean          # rc 0
```

Not done: a full 83-module rebuild of the patched tree, and the downstream modules
(`BorelTransfer`, `Five`, `Transfer`). The box is saturated by 16 members on 4 cores: single
modules take 5-10 minutes and a 30-module cone build did not finish in 25 minutes. The changes are
import-only downstream, every namespace and statement is unchanged, and there is no import cycle
(`DifferenceLaw` imports Mathlib only; `DifferenceInvariant` imports `DifferenceLaw` and
`RelativeCenters`, neither of which imports `Approximation`).

## What still blocks the zone (f37/f38)

1. `Multipliers.lineFourier` (:250) has one consumer outside the zone: relocate or keep.
2. `Stationary` is mixed: keep the `StationaryMean` section (consumed by Representations.lean:116-127),
   move `exists_terminal_factor` (:126 onward, about 70 lines) into the new terminal-factor module.
3. `InvariantMean` is mixed: keep the core mean API (consumed by StationaryMean); the
   periodization/smoothing half (sections `WeakMean` 491-585, `Periodization` 587-823,
   `OrdinaryIntegral` 824-921, `Smoothing` 923-1072, about 580 lines) is consumed only from
   Multipliers.lean:218-305.
4. Then, once the terminal-factor theorem is replaced, delete `ConditionalLimits` (693),
   `Approximation` (425 after this patch), `ConditionalSpectrum` (494), `PhaseCollision` (530),
   `SmallArcs` (322), `PhaseEncoding` (255) - about 2700 lines, plus the `Stationary` tail and the
   `InvariantMean` half if `Multipliers` goes too.
