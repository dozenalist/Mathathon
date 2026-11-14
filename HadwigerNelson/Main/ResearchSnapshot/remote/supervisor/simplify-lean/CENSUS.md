# Declaration-level redundancy census, lean/OAI (83 modules, 31,277 lines)

Reproduce: `python3 supervisor/simplify-lean/.scratch/census.py` then `.scratch/dup2.py`
(census.py: 226 ms; dup2.py: 113 s, single-threaded, no Lean).

Extraction: every `theorem`/`lemma` at column 0, statement text split at the first `:=`,
`concl` = last non-blank line of the statement, whitespace-normalised, clustered across files.
2038 declarations parsed (1861 match `^(private |protected |noncomputable )*(theorem|lemma) ` per `rg`).

## Result 1 (negative, useful): the rigidity half has almost no textual redundancy

Restricted to `Analysis/PlaneSpectrum` + `MeasureTheory/CompactFactors` (50 modules, ~15.5k lines),
exactly TWO cross-file duplicate-conclusion clusters exist:

| cluster | declarations | body lines | uses |
|---|---|---|---|
| integer-multiple energy | Energy.lean:323 `conditional_integer_pair_energy` (18), :342 `conditional_integer_triple_energy` (16), AlgebraModels.lean:652 `conditional_integer_multiple_mean_zero` (7) | 41 | 1, 1, 2 |
| `‖∫f‖² ≤ ∫‖f‖²` | Fourier.lean:96 `norm_integral_sq` (15), Kernels.lean:45 `norm_integral_sq` (15) | 30 | 3, 3 |

So mechanical dupe-hunting in this half is capped at ~70 lines. Do not spend a block on it.

### REFUTED (compiled): the pair/triple energy lemmas cannot absorb their local instance

I proposed that `conditional_integer_pair_energy` and `conditional_integer_triple_energy` be
inlined into `RadialEnergy` by expanding `conditional_integer_multiple_mean_zero` over
`Fin.prod_univ_two/three`, and that the line
`have : ErgodicVAdd G Y (μ.map q) := factor_ergodic μ q hq hqcov` in each was dead (unused)
because the conclusion mentions neither `Y` nor `ErgodicVAdd`. **Both claims are wrong as
stated and the second is refuted by the compiler.**

`have : ErgodicVAdd G Y (μ.map q) := …` elaborates to `letI` (the pretty-printer prints it as
`have : T`), so it installs a *local instance* used by instance-implicit arguments in the body.
Evidence (`lean EnergyShort.lean`, pinned 4.34.1, ~7 s, rc 1):

```
EnergyShort.lean:337:2: error: failed to synthesize
  ErgodicVAdd G Y (Measure.map q μ)
```

`EnergyShort.lean` is the tree's `Energy.lean` with that one line deleted. Deleting it breaks
`conditional_integer_pair_energy` at `rw [Family.energy_mean_eq_of_meanNorm_zero …]`.

Inlining is still *possible*, but the instance obligation must then be discharged explicitly at
the call sites: `RadialEnergy:97` and `:395` call these lemmas *without* `have`-ing
`ErgodicVAdd G Y (μ.map q)` themselves, and that file carries no `[ErgodicVAdd G Y (μ.map q)]`
instance variable either, so each call site that relies on the lemma's internal instance
becomes `… (by exact factor_ergodic …)` or a preceding `letI`-style `have`. Net saving after
that is nearer 20 than 34 lines, with two call sites touched. **Downgraded to "not worth a
block"** unless something else in `RadialEnergy` needs the change.

The lesson generalises and should be carried forward: a `have : SomeProperty` whose type is a
type-class *is a local instance*, not a dead paragraph. Before deleting any `have` in this tree,
require a compile of the shortened module — a grep proving the bound-variable name never appears
proves nothing.

The general lemma (`conditional_integer_multiple_mean_zero`, `s : Finset ι`, `n : ι → ℤ`) is
ALREADY fully general; pair/triple are `Fin.prod_univ_two/three` expansions of it, single-use
(RadialEnergy.lean:97, :395). Deleting them means rewriting two call sites with a `simp only`
expansion: est. 34 lines out, ~10 in, two call sites touched in a 500-line module.

## Result 2 (the real candidate): a ~300-line twin pair of contradiction theorems

| | |
|---|---|
| `Analysis/PlaneSpectrum/ConditionalSpectrum.lean:310` | `finite_uniform_precision_contradiction`, 155 proof lines, `happrox : FiniteEncodingApproximationAt μ p q b m γ` (`H : Fin r → Y → Fin m → ℂ`), `hwild` about `differenceLaw (μ.map (q ∘ p))` |
| `MeasureTheory/CompactFactors/ConditionalLimits.lean:385` | `ambient_uniform_precision_contradiction`, 153 proof lines, `happrox : AmbientEncodingAt μ p q b m γ` (`H : Fin r → X → Fin m → ℂ`), `hwild` about `differenceLaw (μ.map q)` |

Same conclusion `False`, same 8 hypotheses except the encoding and the wild law; the proofs are
near-verbatim. Neither is an instance of the other as stated (different ambient spaces and
different wild laws), so the simplification is a common core lemma whose hypotheses are the ones
the 150 lines actually consume, with the two statements as wrappers. This is the largest
declaration-level redundancy in the tree and it sits exactly between the two halves.

## Result 3 (import-direction fact, for the architecture worker)

`Fourier.lean` imports only `Mathlib`; `Kernels.lean` imports `CompactFactors.ConditionalLimits`.
Two `Analysis` modules import `CompactFactors`, three `CompactFactors` modules import
`Analysis`, so the `norm_integral_sq` duplicate cannot be fixed by one import: it needs a
shared low-level module.

## Leads from swarm smwfy8rae/m1 (UNVERIFIED, geometry half, another worker's lane)

`annuli_tendsto` (HoleApproximation:320 / Mesh:77), `angle_preimage_positive`
(FourContinuity:407 / Interfaces:158), `circleSum_one_lipschitz` (PaletteDensity:314 /
FourTransport:9), plus 5 more pairs in m1/clusters.txt. Each is 4-16 body lines.
