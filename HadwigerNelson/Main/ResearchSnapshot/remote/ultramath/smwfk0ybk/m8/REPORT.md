# Step 2, route (e): measured shrinkage of the Lean dependency closure of the transfer

**Direction d6 of swarm `smwfk0ybk` (member m8).** Question asked by the standing brief:
*shrink the Lean dependency closure of the transfer theorem while keeping the same statement,
measuring lines before and after; if it is already minimal, make one named step's dependence explicit.*

Target `T` := `OAI.EuclideanFiveColor.proper_iff_weak` (paper Theorem 1.3, both directions),
in `lean/OAI/Geometry/PlaneColoring/Transfer.lean`.

## 1. Result (all numbers machine-measured in this VM, Lean 4.34.1 + pinned mathlib)

| object | modules | lines |
|---|---|---|
| import closure of `Transfer.lean` inside `lean/OAI` | 49 | 21813 |
| modules *required* by the proof term of `T` (transitive use) | 36 (+`Transfer.lean`, 37 l.) | 17037 |
| **extracted transfer-only development (this directory, verified)** | **41** | **16478** (24.5 % smaller) |
| forward direction only (Prop 4.2, `proper_to_borel_weak`) | 32 | 15974 |
| backward direction only (`properColoring_of_weak`: density points + compactness) | 4 | 1060 |
| whole development for comparison | 83 | 31277 |

Per family (original -> extracted, lines):

| family | modules | lines | retained |
|---|---|---|---|
| `MeasureTheory.CompactFactors` (the Furstenberg–Zimmer tower) | 14 | 7728 -> 7493 | **97.0 %** |
| `Analysis.PlaneSpectrum` (spectral projection, Haar rigidity, selections) | 19 | 8466 -> 7647 | **90.3 %** |
| `Geometry.PlaneColoring` (palettes, traces, transitions, geometry) | 16 | 5619 -> 1338 | 23.8 % |

Verification (`bash .ultramath/smwfk0ybk/m8/verify.sh`): all **41/41** modules elaborate with
`LEAN_PATH` containing *only* the extracted build directory and the toolchain/mathlib (the shared
`lean/build/lib` is removed, so nothing is silently taken from the original development), and

```
@OAI.EuclideanFiveColor.proper_iff_weak : ∀ {k : ℕ} [NeZero k],
  (∃ c, OAI.EuclideanFiveColor.ProperColoring k c) ↔ ∃ c, Measurable c ∧ OAI.EuclideanFiveColor.WeakColoring k c
'OAI.EuclideanFiveColor.proper_iff_weak' depends on axioms: [propext, Classical.choice, Quot.sound]
```

identical (type string and axiom list) to the same two commands run against `lean/OAI`.

## 1b. The same measurement for the paper's Theorem 1.1 (whole development)

To locate the transfer inside the paper's proof, the same tooling was run with target
`OAI.EuclideanFiveColor.no_proper_five_coloring : ¬ ∃ c : ℂ → Fin 5, ProperColoring 5 c`
(paper Theorem 1.1; `Five.lean`).

| object | modules | lines |
|---|---|---|
| closure of `Five.lean` | 70 | 30351 |
| extracted, verified (`work/min5`) | 70 | 29691 (2.2 % smaller) |
| declarations reachable from Theorem 1.1 | | 2490 of 2571 |
| the transfer's segment inside that closure | 47 | 21690 (**71.5 % of the lines**) |

`bash .ultramath/smwfk0ybk/m8/verify.sh` builds 70/70 modules and reports, from the extracted
tree and from `lean/OAI`, the same statement `¬∃ c, ProperColoring 5 c` and the same axioms
`[propext, Classical.choice, Quot.sound]`.

Two conclusions. (i) The paper's development as formalised is *tight*: only 81 of 2571
declarations (2.2 % of the lines) are unreachable from Theorem 1.1, so no material
formalisation-side reduction of the whole proof exists. (ii) The measurability-removal step is the
dominant cost of that proof: 21690 of 30351 lines (71.5 %). Any genuine shortening of Step 2 must
therefore *remove mathematics from Prop 4.2*, and route (e) tells us it cannot be done by pruning.

## 2. What was actually cut, and what could not be

* **Import-level pruning is impossible.** For all 83 modules, every `import OAI.…` line is used by
  some declaration of the importing file: 0 of 98 OAI import edges are dead
  (`work/graph.py` over `work/edges.log`). So the 21813-line closure is genuinely imported, and the
  only lever is declaration-level surgery.
* **Declaration-level reachability** (`work/Reach.lean`, `work/Reach2.lean`; `ImportGraph`'s
  `Name.transitivelyRequiredModules` / `transitivelyUsedConstants`): `T` uses 2038 of the 3192
  constants of the development. 13 modules of the closure (4776 lines) contain **no** constant
  reachable from `T`; 8 of them end up with no declaration at all and are deleted, the other 5 keep
  a handful of attributed/private declarations, which are retained only because `simp`/`aesop` sets
  are consulted implicitly (deliberate over-retention — the extraction errs towards keeping).
* **Extraction** (`work/extract.py`): comment/string-aware item splitter; a declaration is kept iff
  (a) it is transitively used by the proof term of `T`, or (b) it carries an attribute — `simp`/
  `aesop` lemma sets are consulted implicitly and an unused-looking `@[simp]` lemma can be
  load-bearing (this cost me three rebuild rounds: `embed_mul`, `realPart_apply`, …) — or (c) it is
  `private`/anonymous, plus a fixpoint over identifiers occurring in retained declarations and in
  control items (`variable`, `attribute`, `open`, …). Docstrings and `omit … in` prefixes travel with
  their declaration. The 8 modules left with no declaration are replaced by their import expansion
  (so transitive name availability is preserved) and deleted; the import block of every remaining
  file is rewritten accordingly.
* Result for `T`: 4871 lines of declarations removed, 8 modules deleted, 14 net lines of imports
  added; 49 modules / 21813 lines -> 41 / 16478.

## 3. Findings relevant to Step 2

1. **The brief's "19 of the 78 modules" does not match the dependency structure.** Machine-measured,
   the transfer depends on 49 of the 83 modules (21813 of 31277 lines), of which 14 are *all* the
   `CompactFactors` modules and 19 of the 20 `PlaneSpectrum` modules. Whatever the 19 counted, the
   measurable part of the development is the whole analysis segment, not a fifth of it.
2. **Route (e) is now exhausted: the Furstenberg–Zimmer/spectral machinery is not formalisation
   bloat.** After deleting every declaration unreachable from `T`, the compact-factor tower keeps
   97.0 % of its lines and the spectral part 90.3 %, while the palette/trace geometry keeps 23.8 %.
   There is no dead module or dead sub-development in the analysis segment to remove: a shorter
   proof of the transfer must *replace mathematics*, not prune code. In the dependency sense this is
   sharp — every retained declaration is either in the proof term of `T` or is an attributed/private
   declaration kept because `simp`/`aesop` sets are consulted implicitly; nothing in the analysis
   segment survives for any other reason.
3. **The cost is concentrated in one implication.** `properColoring_of_weak` (weak measurable =>
   proper, which the bundle did not have) is 4 modules / 1060 lines; the forward direction
   (Prop 4.2) is 32 modules / 15974 lines, i.e. 73 % of the closure. Any Step-2 progress must attack
   Prop 4.2; the converse is already cheap.
4. **Remark, outside this direction (route (a) is circular).** The palette machinery is developed
   under `hc : Measurable c` throughout (`Palettes.tracePositive_measurable` derives measurability of
   `{t | 0 < traceValue … t}` from `Lp.stronglyMeasurable`). The palette at `(x,e)` is a *ray-slice*
   object, and for a non-measurable colouring the slices `t ↦ 1_{A_j}(x + t e)` need not be
   measurable, so (5.3) cannot be derived from an arbitrary proper colouring. The palette
   equivalence of the previous run therefore does not replace the transfer.
5. **Where the remaining Step-2 effort belongs.** Since (i) 71.5 % of the lines of the five-colour
   theorem belong to the transfer, (ii) 97 % of the compact-factor and 90 % of the spectral lines
   survive extraction, and (iii) the whole development has only 2.2 % dead code, the only route to a
   shorter Step 2 is a *mathematically* different proof of Prop 4.2. Route (e) is closed: it can
   save at most 24.5 % of the transfer's own closure and 2.2 % of the paper's theorem.
6. **The named hinges (dependency made explicit).** Counting, inside the extracted transfer tree,
   the declarations whose source mentions a constant of each module (`work/hinges.py`,
   `work/names.log`), the analysis segment is reached through very few consumer declarations:

   | module (retained lines) | distinct consuming declarations outside it |
   |---|---|
   | `PlaneSpectrum.RadialEnergy` (471) | **1**: `Ergodicity.projectedMass_vanish` |
   | `PlaneSpectrum.PhaseCollision` (469) | **1**: `ConditionalSelection.common_fiber_contradiction` |
   | `PlaneSpectrum.NumberFields` (523) | 2, both in `Selections` |
   | `CompactFactors.ConditionalLimits` (602) | 3 (`Factors.bounded_approximation`, `Kernels.bounded_rectangles`, `Stationary.exists_terminal_factor`) |
   | `PlaneSpectrum.SmallArcs` (321) | 4 |
   | `PlaneSpectrum.Selections` (431) | 4 |

   Read as a dependency statement (syntactic references in the extracted tree, a superset of what the
   proof terms need): killing `RadialEnergy` or `PhaseCollision` would require re-deriving exactly one
   lemma each — those two lemmas are the only hinges on which 945 lines of the transfer hang. This is
   the sharpest place to look for a mathematical replacement; it is not a claim that such a
   replacement exists.

## 4. Honest limitations

* The reduction is **formalisation-side**, exactly in the sense of route (e): it removes declarations
  not reachable from `T`. It does not shorten any individual proof, and it is not a shorter
  mathematical proof of Theorem 1.3.
* Soundness of the removal is established by elaboration plus the axiom certificate, not by a
  metatheorem about "unused declarations". The conservative attribute rule means the extraction is
  *under*-aggressive, not over-aggressive.
* Only `T` and its ingredients are preserved. `no_proper_five_coloring`, `algebraic_colorable_iff`,
  `proper_to_borel_weak_algebraic`-as-target and everything else in `lean/OAI` are **not** in the
  extracted tree; `algebraic_colorable_iff` is dropped.
* No claim of *mathematical* indispensability: finding 2 says each analysis module is required by
  *this* proof, which does not exclude a different, shorter proof of the same statement.

## 5. Files

| path (relative to this directory) | contents |
|---|---|
| `work/min/OAI/**` | the extracted 41-module transfer development (deliverable object (a)) |
| `work/min5/OAI/**` | the extracted 70-module development for Theorem 1.1 (deliverable object (b)) |
| `work/transfer-extraction.patch` | the full diff against `lean/OAI` (153 KB), for review/proposal |
| `work/table.tsv` | per-module original vs extracted line counts (transfer) |
| `work/extract.py` | the extractor (item splitter + retention rules); `run(root, target, outdir, usedjson)` |
| `work/build.py`, `work/build5.py` | topological builders, `lean -o`, shared OAI build dir removed from `LEAN_PATH` |
| `work/EdgesAll.lean`, `work/edges.log` | per-constant used-constant edges of all 83 modules |
| `work/Reach.lean`, `work/Reach2.lean`, `work/Reach3.lean`, `work/Reach2five.lean` | required-module analyses for `proper_iff_weak`, `proper_to_borel_weak`, `properColoring_of_weak`, `no_proper_five_coloring` |
| `work/reach.log`, `work/used.log`, `work/used5.log`, `work/reach3.log` | their outputs |
| `work/graph.py`, `work/closure.py`, `work/imports.json`, `work/use.json` | import graph, closure, dead-import test |
| `work/Check.lean`, `work/Check5.lean` | statement + `#print axioms` checks used by `verify.sh` |
| `verify.sh` | one command that rebuilds and re-checks both extractions |

No shared file was modified: `lean/`, `results/`, `scripts/` are untouched; the patch is a
proposal.
