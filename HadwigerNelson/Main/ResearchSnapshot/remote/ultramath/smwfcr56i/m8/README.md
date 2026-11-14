# PORT of the OAI Hadwiger–Nelson Lean development to Lean 4.33.1 + the VM's Mathlib

Result: **all 83 modules of `lean/OAI` compile** under the toolchain in this VM, and both main
declarations elaborate with only the three standard axioms:

```
'OAI.EuclideanFiveColor.no_proper_five_coloring' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Problem160.properColoring_seven'            depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.Problem160.chromaticNumber_bounds'          depends on axioms: [propext, Classical.choice, Quot.sound]
OAI.EuclideanFiveColor.no_proper_five_coloring : ¬∃ c, OAI.EuclideanFiveColor.ProperColoring 5 c
OAI.Problem160.properColoring_seven : OAI.Problem160.ProperColoring 7
OAI.Problem160.chromaticNumber_bounds : 6 ≤ OAI.Problem160.planeChromaticNumber ∧
  OAI.Problem160.planeChromaticNumber ≤ 7
```

No `sorry`, no `axiom`, no `native_decide`, no `@[implemented_by]`, no `opaque` is introduced
(`grep -rn 'sorry\|native_decide\|implemented_by\|opaque' work2/OAI` is empty).  The bundle targets
Lean 4.34.1; everything below is the port to **Lean 4.33.1** and the Mathlib checked out at
`/opt/mathlib`.  `SNAPSHOT.txt` holds the SHA-256 of the sorted per-file hashes of the pristine
`lean/OAI` snapshot the patch set applies to (83 modules, including the five modules the
coordinator added while this port was running).

## Reproduce

```
cd .ultramath/smwfcr56i/m8
REPO=<project root> ./reproduce.sh            # fresh copy -> apply patches2/all.patch -> build -> audit
```
`reproduce.sh` copies the pristine `lean/OAI`, applies `patches2/all.patch` (`patch -p1`), compiles
every module sequentially with `lean -o` (`port.py`, one process at a time, `LEAN_PATH` = own olean
dir + Mathlib), then elaborates `audit/Axioms.lean`.  Full run: **5 min 10 s** on this VM, 83/83
modules OK.  Incremental re-runs resume from `status2.json` and existing oleans.

Files:
* `patches2/all.patch` — the complete patch set (38 files, 109 hunks), `a/OAI/... b/OAI/...` headers.
* `patches2/CHANGED.txt` — file → number of hunks.
* `patches2/OAI/**.patch` — same, one file per module.
* `status2.json` — per-module result: `ok`, compiler message, seconds.
* `compile_times.txt` — compile time of each touched module.
* `audit/Axioms.lean` — `#print axioms` on the roots and their `#check` statements.
* `port.py` — the sequential driver (`PORT_SRC`, `PORT_LIB`, `PORT_LOG` select the tree).
* `work2/OAI/**` — the patched sources (identical to pristine + `patches2/all.patch`).

## What had to change, by root cause

The bundle was written against a **newer** Mathlib than the one installed here, so most errors are
API drift, not mathematics.  Grouped, with the number of modules touched:

1. **`Measure.map` / `ProbabilityMeasure.map` gained an explicit `AEMeasurable` argument** (13 files).
   `ProbabilityMeasure.map (ν) {f} (hf : AEMeasurable f ν)`, so `μ.map f` became
   `μ.map (f := f) hf`; and `IsProbabilityMeasure (μ.map f)` is no longer found by `inferInstance`.
   Patch: supply the proof, `Measure.isProbabilityMeasure_map hf`.  Where the proof sits *inside a
   definition* (`Centers.frequencyLaw`) this makes the definition carry `[MeasurableMul₂ G]
   [MeasurableInv G]`, and the six `omit [MeasurableMul₂ G] [MeasurableInv G] in` annotations on
   statements that mention `e.center` had to be dropped (see “Statement-level notes”).
2. **Renamed / absent lemmas** (most of the 38 touched files): `ite_eq_left|right` → `if_pos|if_neg`,
   `dite_eq_left|right` → `dif_pos|dif_neg`, `Measurable.of_eval` → `measurable_pi_lambda f`,
   `Finset.prod_le_prod₀` → `Finset.prod_le_prod`, `Isometry.lipschitzWith|antilipschitzWith` →
   `Isometry.lipschitz|antilipschitz`, `MemLp.fun_mul` → `MemLp.mul'` (with
   `hpqr := ENNReal.HolderTriple.instInfty 2`), `Complex.isIntegral_I` → `IsAlgebraic ℚ I` from
   `imaginaryUnit.property`, `eventuallyEmptyOrUniv_iff`/`EventuallyEmptyOrUniv` → two lemmas added
   below.
3. **Changed lemma shapes** (11 modules): `eLpNorm_congr_norm_ae` no longer takes the measurability
   arguments; `eLpNorm_one_eq_lintegral_enorm` is stated with implicit `f`; `Measure.map_smul` takes
   `(c) (μ) (f)`; `Measure.fst_map_prodMk` takes `Measurable Y`; `condDistrib_comp` takes `(X) (hY)
   (hf)`; `condDistrib_self` takes `Y`; `compProd_map_condDistrib` takes only `hY`
   (`(μ.map X) ⊗ₘ condDistrib Y X μ = μ.map fun a ↦ (X a, Y a)`); `summable_norm_of_tsum_eLpNorm_ne_top`
   now asks for `∀ n, AEStronglyMeasurable (g n) μ` first; `StarAlgebra.isMulCommutative_adjoin`
   takes `R` explicitly and has two goals instead of three.
4. **Two genuinely new proofs** (no statement changed):
   * `OAI/Geometry/PlaneColoring/ContinuumLimits.lean`, `nonemptyCompacts_mem_limit`:
     `NonemptyCompacts.lipschitz_infDist` does not exist in this Mathlib, so the proof that
     `x n ∈ K n → x`, `K n → L` in `NonemptyCompacts X` forces `y ∈ L` is redone from
     `NonemptyCompacts.isClosed_inter_nonempty_of_isClosed` applied to closed balls:
     `∀ ε>0, (L ∩ closedBall y ε).Nonempty`, then `Metric.mem_closure_iff` and `L` closed.
   * `OAI/Analysis/PlaneSpectrum/SpectralMeasure.lean`, `algebra_commRing`: the `CommRing` on
     `algebra U` is built with `StarSubalgebra.commRingTopologicalClosure _ (fun x y => mul_comm x y)`
     instead of `let := adjoin_comm U; inferInstance`.
5. **Three auxiliary lemmas added** (all proved, all used):
   * `EuclideanFiveColor.Amenable.ae_or_ae_not_of_eventuallyConst` (`Amenability.lean`, and a copy in
     `RelativeCenters.lean` which does not import `Amenability`): in this Mathlib
     `Filter.EventuallyConst f l` is `(map f l).Subsingleton` (“some `l`-set has subsingleton image”),
     so `EventuallyConst s (ae μ)` for a set `s` gives `(∀ᵐ x, x ∈ s) ∨ (∀ᵐ x, x ∉ s)` only via the
     basis characterisation; the proof does that.
   * `EuclideanFiveColor.KernelCompact.eventuallyConst_set_iff` (`Kernels.lean`): the reverse
     direction, so `EventuallyConst s (ae μ) ↔ (ae s) ∨ (ae ¬s)`; replaces
     `eventuallyEmptyOrUniv_iff` at its three use sites (`Kernels`, `Energy`, `Ergodicity`).

## Statement-level notes (complete list)

* `OAI/MeasureTheory/CompactFactors/Centers.lean` (**8** declarations) and
  `OAI/MeasureTheory/CompactFactors/RelativeCenters.lean` (**1** declaration): the
  `omit [MeasurableMul₂ G] [MeasurableInv G] in` prefix removed (`center_mem_coset`,
  `quotient_center`, `center_mem_ordinary_iff`, `centerMap_mem_ordinary_iff`, …); the propositions
  proved are unchanged, but as `frequencyLaw` now carries those two instance arguments (item 1), a
  statement that mentions `e.center` cannot omit them.  No hypothesis of any paper-facing statement
  was added or removed; every one of these lemmas is used only inside the development, where both
  instances are in scope.
* `OAI/MeasureTheory/CompactFactors/Separability.lean`, `covariance_mean_zero`: the statement is
  written as `(letI : IsProbabilityMeasure (μ.map q) := …; Family.meanNorm (μ.map q) M …) = 0`,
  because `Family.meanNorm` needs that instance and `hq` is not a typeclass argument.  The
  proposition is definitionally the original one; the `letI` is erased by `iota`/`zeta` reduction.
* Everything else is proof-level: no statement, hypothesis or definition body changed, apart from
  `Centers.frequencyLaw`, which keeps its type and its defining equation but carries two extra
  instance arguments.

## Compile table (each touched module, local toolchain)

See `compile_times.txt` and `status2.json` for the machine-readable form; slowest touched modules:
`SpectralMeasure` 10.3 s, `RadialEnergy` 8.9 s, `Functions`/`Centers`/`Factors` ≈ 5 s; median 3 s.
Whole 83-module development: ≈ 5 min sequential.
