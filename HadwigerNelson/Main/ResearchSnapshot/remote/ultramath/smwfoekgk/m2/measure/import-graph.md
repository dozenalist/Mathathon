# Certified import-graph measurement of lean/OAI (83 modules, 31277 lines)

Method: parse `import OAI.*` from source; transitive closure. Counts are physical
lines per file (`wc -l`), not logical lines.

## Totals
- 83 modules, 31277 lines.
- Import closure of the headline `OAI.Geometry.PlaneColoring.Five`:
  **70 modules, 30351 lines**. Everything else (13 modules, 926 lines) is outside.

## d15 verdict: the "other headline theorems" hold no savings
Marginal mass = closure(theorem's module) minus closure(Five.lean):

| target | own module | closure | marginal beyond Five closure |
|---|---|---|---|
| `properColoring_seven` (Seven.lean) | 68 | 8 mods / 518 | 8 mods / **518** |
| `proper_iff_weak` (Transfer.lean) | 37 | 49 / 21813 | 2 mods / **123** (Converse 86, Transfer 37) |
| `chromaticNumber_bounds` (Chromatic.lean) | 145 | 79 / 31014 | 9 mods / **663** (incl. the 518 above) |
| `not_proper_five_coloring_compl_null` (NullSetRobust.lean) | 67 | 72 / 30504 | 2 mods / **153** |

Union of all four marginals: `Chromatic`'s 663 + `NullSetRobust`'s extra 67 = **~816 lines**,
and the three theorems themselves are 3-10 line corollaries of machinery that already exists
(`proper_to_borel_weak`, `no_measurable_weak_five_coloring`, Moser's theorem). Seven's 518 lines
are an independent small development (Covering/Metric/Lattice/Assembly/MeasurableAssembly/
MeasurableProper) for the 7-colouring; it is not shared with the headline.

**Consequence (the useful part for the swarm):** at most ~816 lines can ever come from outside
the Five closure, and those 816 are mostly the 7-colour construction, which is a kept result.
So *every* line of the required >=1500 reduction must come from inside the 70-module Five
closure. No trimming of "other theorems" can substitute for the factor/spectral work.

## Where the mass inside the Five closure is
- `Geometry/PlaneColoring`: 50 modules, 15083 lines (geometric/colouring side)
- `Analysis/PlaneSpectrum`: 19 modules, 8466 lines (spectral side)
- `MeasureTheory/CompactFactors`: 14 modules, 7728 lines (factor/tower side)

Private-subtree measure (modules x such that every import path from x to Five.lean passes
through the named module):

| hub | private modules | private lines |
|---|---|---|
| `CompactFactors.Approximation` | 13 | **6832** |
| `CompactFactors.ConditionalLimits` | 14 | 7533 |
| `CompactFactors.Stationary` | 3 | 1671 |
| `PlaneSpectrum.PhaseCollision` | 2 | 792 |

The approximation hub dominates ~6.8k lines of the tree: the prize is real and concentrated
exactly where the swarm is working. `PhaseCollision` + `PhaseEncoding` (792) is the tightest
core of it.

## Duplicated definitions seen while measuring
`differenceLaw` is defined three times independently: `CompactFactors/Approximation.lean:112`,
`CompactFactors/RelativeCenters.lean:235`, `Analysis/PlaneSpectrum/FourierTests.lean:235`.
That is a real (if small) consolidation target for whoever owns de-duplication.
