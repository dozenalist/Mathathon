# m1 measurements and verdicts (swarm smwfoekgk)

Baseline: 83 modules, 31277 lines, at `lean/OAI`.  Every number below is from scanning that tree.

## 1. The tree is mechanically tight (the main planning fact)

| lever | ceiling | note |
|---|---|---|
| dead declarations (module level) | ~0 | fan-in <= 1 for 75 of 83 modules; the five headline roots' closure is 82/83 modules, 31204/31277 lines |
| duplicated proof bodies | 34 lines (7 groups) | byte-identical normalised bodies over 2573 declarations |
| duplicated statements | 43 lines (7 groups) | `differenceLaw` is defined identically three times: FourierTests:235, RelativeCenters:235, Approximation:112 |
| inter-declaration scaffolding | 1178 lines | header/open/namespace/blank/comment lines |
| declarations of <= 3 lines | 1379 lines | upper bound if every short declaration were removable; many are legitimate API |
| blocks >= 12 lines, >= 70% tactic-led | 1250 lines | upper bound for automation collapse of long leaf blocks |

Line split: 7708 statement lines, 22766 proof lines, ~1178 glue.

Two clusters measured at declaration granularity with qualified-name resolution:
* `MeasureTheory/CompactFactors` (7742 lines): 7290 transitively required from its 138 externally
  visible roots; 452 unreachable. Tight.  (An earlier scan matching bare identifiers only reported
  7019 free; retracted as board finding f31.)
* `Geometry/PlaneColoring/{Accumulation,GraphRealization,GraphPatches,GraphCuts}` (1522 lines):
  14 lines internally unreachable (`graphRealization_nonneg`, `graphSpace_compact`,
  `fiberCrosses_symm`). Tight.

Conclusion: no mechanical route, and no union of mechanical routes, reaches the 1500-line target on
these ceilings. The target requires an architectural replacement.

## 2. The one architectural prize and the gate in front of it

Prize (m8, d8, cross-checked here): replacing `relative_singularity_approximation` by Theorem A and
restructuring `exists_terminal_factor` frees 6088 lines (19.5%): 10 modules deleted whole (Centers
703, Factors 586, Characters 560, ConditionalSpectrum 497, SmallArcs 322, Multipliers 314,
FourierTests 295, ConditionalSelection 442, PhaseCollision 537, PhaseEncoding 255 = 4511) and 4
truncated (RelativeCenters, Approximation, ConditionalLimits, Stationary: 1577 saved, 419 residue).

Sub-prize reachable without the center machinery: 1114 lines (SmallArcs 322 + PhaseCollision 537 +
PhaseEncoding 255).  Measured: `relative_singularity_successor` (Approximation.lean:384-416, 33
lines) does NOT call `relative_singularity_approximation`; it calls `exact_finite_center_reduction`,
`UniformEnumeration.constant_uniform_lists`, `finite_uniform_successor_contradiction` and
`finite_encoding_approximation_of_compact`.  Only the chain join goes through the approximation lemma.

Gate.  The terminal factor has exactly one consumer, `Ergodicity.lean:54`, which instantiates
`UniversalGood` at `d = id` and needs precisely `IsWild (differenceLaw (mu.map q) (condDistrib id q
mu))`, i.e. C-nullness of the relative difference law *of the identity* over q.  Theorem A supplies
that from "id is not q-measurable", i.e. from q being a PROPER factor.  Compact-extension maximality
gives no properness: if X is compact over the trivial factor the tower top is X, and at q = X the
required conclusion is false, because `condDistrib id id mu = dirac` (Mathlib `condDistrib_self`), so
the law is `delta_1` and `1 ∈ C` since `C = jHom.range` and `jHom 1 = j 0`.  Equivalently
`UniversalGood mu id` is refutable for every `IsWild mu`.  The dev's own predicate has properness for
free: goodness is downward closed, `good(bot)` holds (`relative_singularity_base`), `good(X)` fails.
That is why maximality is over goodness, and why preserving goodness across a limit step is exactly
the approximation property.

## 3. Verdicts I can certify

* R6 (fixed point): dead as a distinct route, blocked as an architecture.  Its greatest fixed point is
  the join of all compact extensions, i.e. R1, and every variant lands on the gate above.  The device
  it would replace is 87 lines (SeparableZorn 50 + CodedMax 37), so it is neutral anyway.
* Factor-representation recast (Factors/Separability): dead, at most 72 lines (48 representation
  sites; 58 + 14 lines unreachable).
* Accumulation/graph cluster: dead, 14 lines.
* (H2) is necessary and is not implied by any hypothesis in the tree; any R1/R6-style replacement must
  add "the chosen factor is proper" as a lemma.
