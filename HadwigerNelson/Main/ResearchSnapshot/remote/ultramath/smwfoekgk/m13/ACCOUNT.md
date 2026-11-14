# Sprint A: certified achievability account (m13)

All numbers below were produced from the tree at `lean/OAI` by the tools in this
directory (`imp.py`, `decls.py`, `use.py`, `bom.py`, `marginal.py`, `direct.py`,
`clust.py`) and by `rg`/`wc`. No number here is an estimate unless it says so.
Nobody's claim is repeated here unless I recomputed it.

## 1. The shape of the tree

| block | modules | lines |
|---|---|---|
| `Analysis/PlaneSpectrum` (spectral / rigidity half) | 18 | 8,466 |
| `Geometry/PlaneColoring` (transfer + endgame) | 51 | 15,083 |
| `MeasureTheory/CompactFactors` (tower / factor half) | 19 | 7,728 |
| total | 83 | 31,277 |

* Closure of the headline `Geometry/PlaneColoring/Five.lean`: **70 modules,
  30,351 lines**. The 13 modules outside it (926 lines: `Chromatic`,
  `Seven`, `Converse`, `Covering`, `NullSetRobust`, `ConnectedUnitFree`,
  `MeasurableProper`, `MeasurableAssembly`, `Metric`, `Lattice`, `Basic`,
  `Assembly`, `Transfer`) are the asset's other headline theorems, not dead weight.
* **65 of 83 modules have exactly one direct importer**, covering 25,053 lines.
  The tree is a chain, not a lattice (`direct.py`).
* Declaration census (`decls.py`): **2,573 declarations, 30,016 lines inside
  declarations**, median 6 lines, mean 11.7. Distribution:
  * 125 declarations ≥ 40 lines carry 7,576 lines,
  * 48 ≥ 60 lines carry 3,913,
  * 17 ≥ 80 lines carry 1,842,
  * 7 ≥ 100 lines carry 934.
  The largest ten: 171 `ConditionalLimits:385 ambient_uniform_precision_contradiction`,
  169 `ConditionalSpectrum:310 finite_uniform_precision_contradiction`,
  155 `Moser:285 seven_point_certificate`, 118 `ConditionalSelection:259`,
  117 `PhaseCollision:142`, 104 and 100 in `Functions`, 99 `Approximation:185`,
  99 `Separability:268`, 96 `HoleApproximation:115`.

## 2. The only concentrated deletable block in the tree

`MeasureTheory/CompactFactors` and `Analysis/PlaneSpectrum` form a linear chain
with single importers (`direct.py`):

```
Kernels -> ConditionalLimits -> Approximation -> ConditionalSpectrum ->
   {ConditionalSelection -> PhaseCollision -> PhaseEncoding, SmallArcs, FourierTests}
Approximation -> RelativeCenters -> Centers;  RelativeCenters -> Basic
```

**Approximation-specific mass** (each of these modules has no importer outside the
set): `Approximation` 496, `ConditionalSpectrum` 497, `ConditionalSelection` 442,
`PhaseCollision` 537, `PhaseEncoding` 255, `SmallArcs` 322, `FourierTests` 295 =
**2,844 lines in 7 modules** (`bom.py`). Note 5 of the tree's 10 largest proofs
sit in exactly these modules (171, 169, 118, 117, 99 = 674 lines of proof).

Not freed with them: `Centers` 703 + `RelativeCenters` 598 (compact-factor
centres; an R1-shaped route keeps compactness), `ConditionalLimits` 701 (mixed:
UniversalGood plus compact machinery), `Basic` 735 (rigidity 1a, shared even
though its only direct importer is `RelativeCenters`).

**Trap for every reachability argument** (`marginal.py`): deleting module
`Approximation` makes **13 modules / 6,832 lines** unreachable from `Five.lean`
— but nine of those (InvariantMean 1078, Basic 735, Characters 560, Centers 703,
RelativeCenters 598, Multipliers 314, ...) are the rigidity proof's own
dependencies, reached only *through* the approximation chain. Reachability must
be recomputed after re-pointing imports or it overstates the saving by ~4k lines.

## 3. The two halves meet at two modules

`rg -n "^import OAI.Analysis" Geometry/PlaneColoring/*.lean` returns exactly:

* `BorelTransfer.lean` (447) imports `PlaneSpectrum/Ergodicity.lean` — the only
  consumption of the whole 16.2k-line spectral half by the endgame;
* `Transitions.lean` (142) imports `PlaneSpectrum/CircleOperator.lean`.

So the "conversion" block — rigidity result to colouring contradiction — is
`BorelTransfer` 447 + `WeakColoring` 168 + `Transitions` 142 = **757 lines**.

## 4. Verdicts on routes I registered and killed (each with its certificate)

| route | verdict | certificate |
|---|---|---|
| d12 conversion/endgame compression | dead | conversion block is 757 lines (§3), under the 1500 threshold |
| d25 hypothesis-cluster bundling | dead | full factor cluster appears in **14 declarations / 99 signature lines**, kernel cluster 4 / 38, centred-kernel 3 / 26 (`clust.py`); the 156 `hqcov` and 141 `hq :` occurrences are single-hypothesis uses inside proofs |
| d28 circle-operator decay | dead | `Transitions` consumes the **rate** `‖colorError h‖²/‖h‖ → 0` (`circle_smoothing_L2`), not `o(1)`; the rate comes from the Bessel-type bound `circleSymbol_sq_bound` / `oscillatory_integral_bound` in `CircleDecay` (233 lines). Riemann–Lebesgue cannot replace a rate. My premise that `PC/Compactness` belonged to this package was also wrong: it is the weak-* trace machinery imported by `CircleOperator`. |
| d29 generic transport unification, Steps 9–11 | dead | the k=4 layer carries a velocity/gap theory (`transportVelocity`, `sumTransport_*`, `four_gap_*`, `strict_increment_limit`, 304 lines) with **zero** counterpart in `FiveSupport`, `BoundaryTrace`, `Sectors`, `Exclusion`, `Moser`; k=5 is finite contact combinatorics (112 lines), k=3 is support/limit (242). No aligned generic transport exists; the shared residue is a few support/trace lemmas. |
| d32 ergodic decomposition from the Fourier basis | dead | the decomposition's decisive step `ergodic_of_test_limits` concludes `μ.restrict s = μ.real s • μ` by `ext_of_generate_finite` over the π-system of `testSet`s. Characters cannot do this: the `z = 0` coefficient is `μ.real s` on both sides, and for `z ≠ 0` the coefficients of the restricted measure are exactly the unknowns; the characters are not orthogonal in `L²(μ)` for arbitrary `μ`. |
| d33 K/Rot duplication collapse | dead | `Rot` + `kCoeff` + `rotMul` + `mulRot` occur 118 times in 4 files (`RadialEnergy` 65, `Representations` 36, `Ergodicity` 12, `Energy` 5); the pure glue (`instance : Countable Rot`, `smul_ergodic_of_rot`, the two coercions) is under 120 lines. |
| d12's Steps 5–11 reading | dead | 337 declarations, 4,156 lines, median 8; no proof over 155 except `Moser`; and `results/K6-BARRIER.md` records that each of the three cycle exclusions fails exactly at k = 6, so the three arguments cannot be unified into one. |

## 5. One positive result for the (H2) side condition (posted as f24)

`D^K = {1} ⊆ C`, so no point mass is wild:

* `d` is K-fixed iff `d((k-1)z) = 1` for all `k ∈ K`, `z ∈ E`;
* `-1 ∈ K` (`|-1| = 1`), so `(K-1)E ⊇ (-1-1)E = 2E = E` (E is a ℚ-vector space);
* hence `d(2z) = 1` for all `z`, so `d = 1 = j 0 ∈ C`.

Consequence: `IsWild (δ_d)` forces `d = 1` and then `δ_d(C) = 1`, so the
one-point system never refutes (N). Companion: for `z ≠ 0` every nonzero
K-orbit in `E` is infinite (`u z = z, u ≠ 1 ⟹ z = 0` in the field `E`), which is
the lemma a finite-dimensional-invariant-subspace proof of (N) needs.

## 6. What this says about the sprint

Nothing in the endgame (Steps 5–11, ~13.5k lines) can yield 1,500 lines: the
block is flat (median declaration 6–8 lines, largest proof 155), its two heavy
sub-blocks were taken by d17 (Step 8, 2,223 lines) and d19 (palette pipeline,
2,947 lines), and the three cycle exclusions are provably not unifiable
(k = 6 barrier). The conversion layer is 757 lines. **The only concentrated
deletable mass in the tree is the 2,844-line approximation chain** (§2), and the
only route that reaches the target without it is the measured static dead-weight
ceiling of d1 (1,771 lines) plus d14 plus d26, composed by d22.

Every route's *attrition* against elaboration is still unattested: the 1,771-line
figure is a source-level count, and 7,576 of the tree's lines live in the 125
declarations of ≥ 40 lines, so any deletion set that touches a long proof costs
more than its line count suggests.
## 7. Direct measurement of the fallback (deletion) route — posted as f32

`safe_del3.py` tokenises every module once, splits qualified names at dots, drops
declarations carrying an attribute, and keeps a theorem/lemma only if its name
occurs **nowhere** in the tree outside its own declaration block (so intra-file
uses, `simp`-set membership, quoted names and qualified uses all keep it).
Spot-checked by hand: `sampling_weak_compact` (Compactness:130),
`collision_from_close_encodings` (PhaseCollision:396) and
`finite_continuum_subsequence` (ContinuumLimits:163) each occur exactly once in
the whole tree, so they are genuinely dead.

* **134 declarations, 1,128 lines are directly unreferenced.**
* Of those, required roots must stay: `not_proper_five_coloring_compl_null`
  (48, NullSetRobust), `ConnectedUnitFree` (29), and any other unreferenced
  headline theorem in the root modules. Directly deletable core: **~1,040 lines**.
* d1's 1,771 is reachability-based and additionally counts declarations used only
  by other dead declarations: sound in principle, but exactly the part where
  elaboration attrition bites, because those names do appear in proof text.

Consequence: against 1,500, the conservative margin is ~460 short before any
attrition, so the sprint needs d1 + d14 + d26 all to land and be composed.

## 8. Automation route, measured tree-wide (posted as f34, corrected by f35)

Classification of every body line of every declaration (blanks and comment lines
excluded; 28,385 lines over 2,573 declarations):

| band | lines | share |
|---|---|---|
| heavy automation (`nlinarith`, `linarith`, `ring`, `field_simp`, `positivity`, `omega`, `polyrith`, `interval_cases`, `gcongr`) | 1,421 | 5% |
| `simp`/`rw`/`simpa`/`exact`/`refine`/`apply` | 6,365 | 22% |
| structural (`obtain`, `cases`, `have`, `constructor`, bullets, `calc`) | 20,599 | 72% |

Declaration-size buckets: 1,629 declarations under 10 body lines (6,213 lines),
830 of 10–39 lines (15,210), 114 of 40+ (6,962). The mass is in the 10–39 band,
so a sample restricted to the largest proofs (my first attempt, f34) understates
the route by a factor of four: the monsters are 7% automation, the tree is 27%.

Verdict for d14: the rewriteable population is 7,786 lines; a third better gives
~2,100, a fifth gives ~1,270. So d14 is a genuine contributor with a band of
several hundred to ~1,500 lines, and it must land for the union to clear 1,500.

## 9. Bottom line

* One route clears 1,500 on its own: the 2,844-line approximation chain (§2),
  gated on (N), join-closure and transitivity of the compact predicate.
* Otherwise the sprint needs the union: d1's deletion (1,040 conservative /
  1,771 reachability), d14's automation (300–1,500), d26's mean unification,
  composed by d22 — with attrition against elaboration as the only unmeasured
  risk, and 7,576 lines sitting in 125 long declarations where a deletion costs
  more than its line count suggests.
* The endgame cannot supply the difference: flat (median 6–8 lines per
  declaration), its two heavy sub-blocks held by d17/d19, its three cycle
  exclusions provably non-unifiable (k = 6 barrier), and its conversion layer
  only 757 lines.

Tools, all in this directory: `imp.py` (import closure), `decls.py` (declaration
census), `use.py` (per-declaration consumers), `bom.py` (approximation-chain
bill), `marginal.py` (module-marginal reachability and its funnel artifact),
`direct.py` (single-importer chain), `clust.py` (hypothesis clusters),
`safe_del.py`/`safe_del2.py`/`safe_del3.py` (deletion counts, with the
qualified-name bug and its fix documented in the file names).
