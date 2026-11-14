# Realised line measurement (m1)

Units: physical lines of `.lean` files (trailing newline not counted), as in the sprint's
31277-line baseline count.

| tree | modules | lines |
|---|---|---|
| `lean/OAI` (baseline) | 83 | 31277 |
| `sprint/simplify/stage/lean/OAI` (staged) | 85 | 31318 |
| `tree/OAI` (staged, scaffolding-compacted) | 85 | 31144 |
| `tree/OAI` + 5 audit modules | 90 | 31956 |

## Per-module compaction (staged -> compacted); modules not listed are unchanged

| module | staged | compacted | delta |
|---|---|---|---|
| `MeasureTheory/CompactFactors/Factors.lean` | 586 | 567 | -19 |
| `MeasureTheory/CompactFactors/Functions.lean` | 884 | 865 | -19 |
| `MeasureTheory/CompactFactors/AlgebraModels.lean` | 664 | 647 | -17 |
| `MeasureTheory/CompactFactors/Approximation.lean` | 425 | 409 | -16 |
| `MeasureTheory/CompactFactors/ConditionalLimits.lean` | 701 | 685 | -16 |
| `MeasureTheory/CompactFactors/Kernels.lean` | 774 | 758 | -16 |
| `MeasureTheory/CompactFactors/RelativeCenters.lean` | 598 | 585 | -13 |
| `MeasureTheory/CompactFactors/Centers.lean` | 703 | 691 | -12 |
| `Analysis/PlaneSpectrum/ConditionalSpectrum.lean` | 497 | 486 | -11 |
| `Analysis/PlaneSpectrum/SmallArcs.lean` | 322 | 312 | -10 |
| `Analysis/PlaneSpectrum/PhaseCollision.lean` | 537 | 531 | -6 |
| `MeasureTheory/CompactFactors/ConditionalSelection.lean` | 442 | 436 | -6 |
| `MeasureTheory/CompactFactors/Separability.lean` | 573 | 567 | -6 |
| `Analysis/PlaneSpectrum/PhaseEncoding.lean` | 255 | 252 | -3 |
| `MeasureTheory/CompactFactors/DifferenceInvariant.lean` | 98 | 96 | -2 |
| `Analysis/PlaneSpectrum/DifferenceLaw.lean` | 72 | 71 | -1 |
| `Analysis/PlaneSpectrum/FourierTests.lean` | 235 | 234 | -1 |

Total removed by the compactor: **174** lines over 17 modules (rule 1: 170 scope-active duplicate `open`/`open scoped` lines; rule 2: 4 excess blank lines).

Net against the 31277-line baseline, 85 original modules: **-133** lines.

Net against the 31318-line staged tree, 85 original modules: **-174**.

New audit modules (not part of the development's dependency closure; additive only):

| module | lines |
|---|---|
| `Analysis/PlaneSpectrum/TerminalGlue.lean` | 84 |
| `MeasureTheory/CompactFactors/OrbitBridge.lean` | 157 |
| `MeasureTheory/CompactFactors/TowerAudit.lean` | 323 |
| `MeasureTheory/CompactFactors/TowerCorrect.lean` | 153 |
| `MeasureTheory/CompactFactors/WeakMixingTerminal.lean` | 95 |
