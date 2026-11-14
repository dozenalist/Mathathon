# m3 (direction d11, "consolidation") — measured compression and tower-interface account

All numbers below are exact, produced by the scripts in `work/` against
`lean/OAI` (read-only).  Nothing in `lean/OAI` was modified; the patched tree is
`tree/OAI`.

## 1. Compressed tree: 31277 -> 29671 lines (-1606)

`tree/OAI` is a copy of `lean/OAI` after two deletion-only transformations.
15 of 83 modules are untouched; the per-module table is `work/per_module.txt`,
the full diff is `work/compress.diff` (apply with `patch -p1` inside a directory
holding `OAI/`), and every deleted declaration is listed in
`work/removed_list.txt` (117 rows, with file, name, kind, lines).

### 1a. Redundant `open` commands: -657 lines (`work/redundant_open.py`)

There are 971 `open`/`open scoped` lines in the tree. 657 of them open only
names that are *already open at that point in the same scope stack* (or are
folded into an earlier `open` of the same kind with no name-resolving line in
between).  Deleting such a command leaves the set of opened names in force at
every later token unchanged, so every declaration elaborates to the same term:
the transformation is visibly semantics preserving, without a build.  `open ... in`,
`renaming` and `hiding` are left alone (1 occurrence of `open ... in` exists).

### 1b. Unreferenced declarations: -949 lines, 117 declarations (`work/remove_dead.py`)

A declaration is deleted only if all of the following hold.

* Its last name component occurs in the *whole tree text* no more often than the
  number of declarations carrying that component — i.e. it is never mentioned by
  any proof, type, `variable` line, attribute list or doc string. (References in
  Lean are identifier tokens, so this scan is exhaustive; the tree contains no
  `exact?`/`apply?`/`library_search`/`simp?`, and `aesop`/`simp` only search
  *attribute*-tagged lemmas, which are never deleted here.)
* It carries no attribute at all (so no `@[simp]`, `@[to_additive]`, …).
* It is not an `instance`, `structure`, `class` or `inductive` (implicit use).
* It is not one of the named headline results, and its name is not cited in
  `README.md` or any `results/*.md`.
* It lives in the `Five.lean` import closure (the 70 modules that carry the
  headline proof). The 13 modules that exist only to state the secondary results
  (`Seven`, `Chromatic`, `NullSetRobust`, `Converse`, `Transfer`, `Metric`,
  `Lattice`, `Covering`, `Assembly`, `MeasurableAssembly`, `MeasurableProper`,
  `ConnectedUnitFree`, `Basic`) keep every lemma and definition; only their
  unreferenced `theorem`s were considered, and those are listed separately in
  `work/removed_list.txt` so they can be vetoed individually. Note that
  `exists_measurable_proper_seven`, `weakMeasurableColoring_seven` and
  `diam_le_one_connectedComponentIn_of_properColoring` are among them: if the
  coordinator wants those statements kept, restoring them costs 45 lines.
* Names containing `.` (namespace-qualified declarations such as
  `DensityOne.compl`) are never touched: they are also reachable by dot
  notation, which a token scan cannot resolve.

The scan is iterated to a fixpoint (a dead lemma can make another one dead); 7
rounds were needed. Largest removals: `ConditionalLimits` 111,
`PhaseCollision` 67, `InvariantMean` 63, `Functions` 63, `RelativeProducts` 58,
`RelativeCenters` 56, `FourContinuity` 55, `BoundaryTrace` 53.

## 2. Verification status (blocked by machine load, not by the patch)

A single 34-line module from the patched tree compiles clean
(`OAI/Geometry/PlaneColoring/Coloring.lean`, olean written), but it took 15
minutes wall for 5.7 s user + 113 s sys: with ~16 concurrent `lean` processes
(pooled load average 17-23 on 4 cores) every process re-reads Mathlib's 6.4 GB
of oleans and waits on I/O. A trivial `import Mathlib` file does not finish in
280 s. A full 83-module build is therefore out of reach at the moment.

Exact commands (once the box is quiet):

```bash
cd .ultramath/smwfoekgk/m3
export TMPDIR=$PWD/.scratch
LEAN_PATH=$PWD/tree:$LEAN_PATH python3 work/build.py tree build ../../../lean/build/lib
LEAN_PATH=$PWD/build:$PWD/tree:$LEAN_PATH lean .scratch/CheckAll.lean   # #print axioms
```

(For the pinned 4.34.1 toolchain: `source scripts/env4341.sh`, then the same
two commands with `tree` first on `LEAN_PATH`.)

## 3. Where the lines actually are (for the tower routes)

* The `Five.lean` closure is **70 of 83 modules, 30351 of 31277 lines**; almost
  every module has exactly one consumer, so the tree is a chain and
  module-level deletion yields at most 926 lines (the 13 outside modules).
* The tower block `Stationary` + `Approximation` + `ConditionalLimits` +
  `RelativeCenters` is **1996 lines** and exports only **five** declarations to
  the rest of the tree: `exists_terminal_factor` (used once, `Ergodicity.lean:54`),
  `relative_difference_invariant` (also `Ergodicity`), `invariant` (Energy,
  Ergodicity, Kernels, Separability), and `StationaryMean.inner` / `.integral`
  — the last two are *not* tower material: `StationaryMean` (~125 lines of the
  201-line file) is the invariant-measure construction used by `Representations`,
  `Energy`, `SpectralMeasure`, `RadialEnergy` and must be moved out, not deleted.
* Enlarging the cluster to the 16 modules reachable only through the tower
  (`InvariantMean`, `Characters`, `Multipliers`, `FourierTests`,  plus
  `PhaseEncoding`, `PhaseCollision`, `SmallArcs`, `ConditionalSpectrum`,
  `ConditionalSelection`, `RelativeCenters`, `Approximation`,
  `ConditionalLimits`, `Centers`, `Factors`, `Functions`, `Stationary`) gives
  **8469 lines exporting 31 declarations**; of those, the ones used by modules
  outside the cluster are only: `eval`, `eval_add`, `eval_neg`,
  `measurable_eval_coe`, `lineFourier_eq` (21 lines, `ConditionalSpectrum`),
  `invariant` + `relative_difference_invariant` (56 lines, `Approximation`),
  `lineFourier` + `weight` (`Multipliers`), `exists_small_wild_parameter`
  (`FourierTests`), `[Countable` (`Factors`), `ae_fiber_of_ae` + `ae_in_own_fiber`
  (`ConditionalSelection`, used by `Kernels`), and the `InvariantMean` cube API
  used by `Energy`. So a replacement that supplies `exists_terminal_factor` and
  keeps ~150 lines of these leaves **roughly 6000 of the 8469 lines deletable**.
  Full list: `work/iface_tower.txt`.

## 4. Two facts that constrain the tower routes

* **The trivial factor can never be used.** `relative_singularity_base`
  (`ConditionalLimits.lean:352`, 8 lines) already proves `UniversalGood` for the
  constant factor: `IsWild ν -> (ν ⊗ ν){d/d' ∈ C} = 0`. But Theorem A needs an
  ergodic relative product, and over the constant factor that is `μ ⊗ μ` under
  the diagonal K-action; `D` is an abelian Pontryagin dual, so
  `(k d)/(k d') = d/d'` — the difference is a non-constant invariant. Hence
  `X ×_pt X` is never ergodic and no bottom-factor shortcut exists.
* **R1's successor step is already in the tree.** `CompactTower.strict_compact_successor`
  (`Factors.lean:206`) needs only `¬ ErgodicSMul K (X × X) (law μ q)` and returns
  `H` (bounded, measurable, not `q`-measurable) such that *every* bounded
  measurable `F` on `Y × OrbitSpace K` is `Compact` over `extend q H` — i.e. the
  successor is a compact extension of `q`. The join-closure machinery is also
  present (`compact_union`, `compact_iUnion` for countable unions,
  `compactSigma_le`, `compact_descend`, `compact_base`, `compact_shift` in
  `Functions.lean`/`Factors.lean`). What R1 still lacks is (i) the maximality
  argument over the class of compact extensions of the trivial factor, phrased so
  that a chain's join is again in the class, and (ii) the one (H2) fact
  `id` is not measurable for the top factor — equivalently the join of all
  compact extensions of the trivial factor is a *proper* factor of `D`. That
  single statement is the exact (H2) supply, and it is where R1 can fail.
