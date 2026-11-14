# Cost account for R2 / R5 / R6 (and the R1 defect they inherit)

Member m7, direction d7. All line counts are `wc -l` on `lean/OAI/**` at commit state of
2026-11-14 (83 modules, 31277 raw lines; 31113 excluding the 13 modules unreachable from the
headline `Geometry.PlaneColoring.Five`).

## 1. The prize: what deleting the approximation route actually buys

`MeasureTheory.CompactFactors.Approximation` is imported only by
`ConditionalLimits` (→`Kernels`→`Functions`→`Factors`→`Stationary`→…). Removing it from the
import graph makes 13 modules / **6832 lines** unreachable from `Five.lean`
(`python3 .scratch/graph.py` in the repo). But most of those 13 are load-bearing for *survivors*,
so the naive number is an overestimate. Per-module verdict:

| module | lines | verdict |
|---|---|---|
| Analysis/PlaneSpectrum/Basic | 735 | **KEEP**: declares `K, D, C, IsWild, eval, scalar, kCoeff, measurableSet_C`; used by Ergodicity, RadialEnergy, SpectralMeasure, Representations, BorelTransfer, NumberFields, Energy… Only its *import route* is via `Approximation`; repair with one `import` line. |
| Analysis/PlaneSpectrum/InvariantMean | 1078 | **KEEP**: `mean`, `mean_add/smul/shift/const`, `PlaneFiveColor.InvariantMean.mean` used by `Stationary.lean` itself and `Amenability`, `Energy`. |
| Analysis/PlaneSpectrum/Characters | 560 | DELETE: only importer chain Multipliers→FourierTests→ConditionalSpectrum; `Characters.coeff` has no external use (the `coeff` in `ConditionalLimits` is a bound variable). |
| Analysis/PlaneSpectrum/Multipliers | 314 | DELETE |
| Analysis/PlaneSpectrum/FourierTests | 295 | DELETE |
| Analysis/PlaneSpectrum/SmallArcs | 322 | DELETE (`exists_small_arc_constants` used only by the two approximation theorems) |
| Analysis/PlaneSpectrum/ConditionalSpectrum | 497 | DELETE (imported only by `Approximation`) |
| Analysis/PlaneSpectrum/PhaseCollision | 537 | DELETE |
| Analysis/PlaneSpectrum/PhaseEncoding | 255 | DELETE |
| MeasureTheory/CompactFactors/Centers | 703 | DELETE (imported only by `RelativeCenters`; the `center`/`kernel`/`coordinate` hits in Geometry are name collisions — no Geometry module imports `Centers`) |
| MeasureTheory/CompactFactors/RelativeCenters | 598 | DELETE (`exact_finite_center_reduction` used only by `ConditionalLimits`' approximation block) |
| MeasureTheory/CompactFactors/ConditionalSelection | 442 | **377 DELETE, 65 KEEP**: lines 181–245 `ConditionalFiber.{ae_fiber_of_ae, ae_in_own_fiber, integral_fiber, integrable_fiber_integral}` are used by `Functions.lean:850,872,876` and `Kernels.lean:636,730,760` and must be relocated. Everything else in the file (GoodFiber 23–125, Approximation 128–178, FiniteModule 247–370 = the `PhaseEncoding` consumer, FiniteBins 373–438) dies with the block. |
| MeasureTheory/CompactFactors/Approximation | 496 | DELETE, except `KernelSupport.factor_smul_preserving` and `relative_difference_invariant` (~30 lines) which `Ergodicity.lean` uses → relocate. |

Plus, inside `ConditionalLimits.lean` (701 lines, survives for `LimitDensity`):

| block | lines | verdict |
|---|---|---|
| 40–177 `LimitDensity` (`bounded_vector_approximation`, `generated_factor_approximation`) | 138 | **KEEP**: consumed by `ChainJoin.approximation` (`Factors.lean`), which every chain-join argument needs, including a compactness-based one. |
| 179–325 `bounded_phase_encoding`, `finite_encoding_at_of_approximation`, `relative_singularity_limit` | 147 | DELETE — **already dead**: `relative_singularity_limit` has zero consumers in the 83 modules (only its own declaration; it was pre-written for the transfinite route). |
| 327–345 `ConditionalBase` | 19 | DELETE (feeds `relative_singularity_base`) |
| 347–552 `relative_singularity_base`, `AmbientEncodingAt`, `ambient_uniform_precision_contradiction` | 206 | DELETE |
| 553–568 `scalar_identity` | 16 | DELETE |
| 570–700 `ambient_encoding_of_at`, `relative_singularity_approximation`, `UniversalGood`, `universalGood_of_factor` | 131 | DELETE |

**Total prize: 377+65 relocated is 377 net from ConditionalSelection; the deletable mass is
560+314+295+322+497+537+255+703+598+377+496+519 = 5473 lines. Net after relocating ~150 lines of
surviving lemmas: ≈ 5.3k lines, i.e. 17% of the tree — 3.5× the 1500 target.** This is the number
any terminal-factor reroute should be measured against; it is also why mechanical trimming (R7)
and the `open`/duplicate-header work (d18) cannot get there.

## 2. R1/R6 cost: dominated by ONE missing lemma, plus one defect

Both routes end at the same place: produce a factor `p` with
(a) `ErgodicVAdd Rot (D×D) (RelativeProduct.law μ p hp)` and (b) `GoodId μ p`
(`GoodId` = the relative difference law of the *identity* is C-null). Everything else in
`Stationary.lean` is then dead. See `TerminalGlue.lean` in this directory: the same statement as
`ergodic_wild_fourier` follows from (a)+(b) alone (`ergodic_wild_fourier_of_goodId`), so the
`∀ wild d` in `UniversalGood` is spurious at the terminal factor.

Getting (a) by maximality over "compact extensions of the point" needs, in Lean:

1. **join-closure** — cheap, *and already implicit in the tree*: `FactorLp.space` of
   `ChainJoin.code q` is the increasing union of the `FactorLp.space μ (q n)`, and
   `ChainJoin.approximation` + `LimitDensity.generated_factor_approximation` already give the
   approximation of any join-measurable bounded `H` by stage-`j` functions. For the *precompact
   orbit* formulation of compactness that is exactly total boundedness of the orbit, so the
   countable join of compact-over-point factors is compact over the point. Cost ≈ 60–120 lines,
   no new machinery.
2. **transitivity** ("compact over a compact-over-point factor ⇒ compact over the point") —
   *this* is the whole route, ~20 lines of Hilbert-space argument in the standard formulation
   (project onto `L²(Y)`; `k·f ≈ f_i + E_Y(k·f) - E_Y(f_i)`, and the `E_Y(f_i)` have their own
   finite ε-net by compactness of `Y` over the point).
   **Defect: it does not go through for the predicate the tree actually uses.**
   `EuclideanFiveColor.CompactApproximation.Scalar` / `CompactFunctions.Compact`
   (`Approximation.lean:154`, `Functions.lean`) only says
   `H(k·x) ≈ Σ_i a_i(k, q x)·Hf_i(x)` with **arbitrary** bounded measurable `Hf_i`. That is
   strictly weaker than relative compactness modulo `L²(q)`: projecting
   `Σ a_i(q)·Hf_i` onto `L²(q)^⊥` is norm-non-increasing but does **not** stay small, so
   `Hf_i` cannot be replaced by `E_q(Hf_i)`. Hence `Compact` is not transitive, and R1/R6 must
   first introduce the standard predicate (orbit totally bounded modulo `L²(q)`), prove the
   successor step in *that* predicate (the kernel computation of `compact_applyKernel`,
   `Factors.lean:141`, is reusable verbatim: it approximates the kernel by a finite-rank sum of
   `q`-measurable coefficient functions), and then transitivity. Realistic cost 300–500 lines to
   delete 5.3k.
3. **(H2) at the top — a defect no route on the board currently accounts for.**
   Theorem A needs "identity is not `p`-measurable". Maximality does **not** give it: if the
   maximal compact extension `Y*` determined the point (i.e. `X` is almost periodic over the
   point), the relative square over `Y*` would be the diagonal, *ergodic*, so maximality is not
   violated — and then `GoodId` is **false**, because the relative difference law is `δ_1` and
   `1 ∈ C`. So R1/R6 need a third obligation: `¬ ∃ g, Measurable g ∧ id =ᵐ[μ] g ∘ p`
   (equivalently: `μ` is not almost periodic over the point). Under the current architecture this
   comes for free: `UniversalGood` at the top factor *is* `GoodId` for `d = id`. Any reroute that
   replaces `UniversalGood` must prove it separately.

## 3. Verdicts

* **R6 (fixed point) ≡ R1.** `CodedMax.exists_maximal` (`Factors.lean:…`) is already
  predicate-generic: `exists_terminal_factor` calls
  `CodedMax.exists_maximal (K := K) μ (UniversalGood μ) hbase hjoin`. Swapping the predicate
  for `CompactOverPoint` needs exactly obligations 1–3 above; no Zorn, no ordinals, no fixed-point
  operator. The "explicit fixed point" idea buys nothing extra because the maximality principle is
  already countable/separable and costs <100 lines.
* **R5 (countable reduction) is a strict sub-step of R1.** L² separability gives a countable dense
  subset of the compact part; each element generates a factor via `OrbitFactor.extend`
  (`Factors.lean:120`), and the join of the resulting ℕ-sequence is `ChainJoin.code`. So "the
  maximal compact factor is the join of a countable explicit family" is *true and cheap* in this
  tree — but it only removes the maximality wrapper (`CodedMax` ≈ 60 lines, `ChainJoin` ≈ 120), and
  it does **not** remove obligation 2 or 3. Measured saving of R5 *as a route*: ≈ 0 lines of the
  5.3k prize; it is a lemma, not an architecture.
* **R2 (transfinite) is dominated and strictly more expensive than R6.** Termination by
  "no strictly increasing ω₁-chain of closed subspaces in a separable Hilbert space" is correct
  (pairwise-orthogonal unit vectors), but it needs countable-ordinal recursion plus a cardinality
  lemma for orthonormal families, and it still needs obligations 2 and 3 (transitivity of
  compactness is what makes each successor a compact extension of the *point*, and (H2) at the top
  is unaffected by how the tower is indexed). ℕ-recursion alone is *not* enough: the join of the
  ℕ-tower can be non-ergodic again, so a ℕ-indexed tower has no termination proof without the
  ω₁ argument. Meanwhile the paper's tower already only needs `relative_singularity_limit`
  (`ConditionalLimits.lean:269`) at limit stages — a theorem that is **written, 57 lines, and has
  zero consumers** — so R2's *only* missing piece is the well-founded recursion; but see §2 defect
  3: R2 with `UniversalGood` propagation still pays the whole approximation chain, and R2 with
  compactness pays §2.2 + §2.3. Net: R2 ≈ R6 + (ordinal machinery ≥ 400 lines) ⇒ dominated.

## 4. Machine-checked interface: `TerminalGlue.lean`

`TerminalGlue.lean` (in this directory) compiles under the pinned 4.34.1 toolchain; the three
main theorems report axioms `[propext, Classical.choice, Quot.sound]`:

```
source scripts/env4341.sh && lean .ultramath/smwfoekgk/m7/TerminalGlue.lean
```

What it establishes:

| declaration | content |
|---|---|
| `GoodId μ p` | `differenceLaw (μ.map p) (condDistrib id p μ) C = 0` — relative singularity for the identity map only |
| `goodId_const` | `GoodId` holds at the point factor (one line from `relative_singularity_base`) |
| `goodId_of_universalGood` | `UniversalGood ⇒ GoodId` |
| `ergodic_wild_fourier_of_goodId` | `GoodId μ p` + `[ErgodicVAdd Rot (D×D) (law μ p hp)]` ⇒ `∫ eval z dμ = 0` for `z ≠ 0`, **with no wildness hypothesis on μ** |
| `TerminalObligation μ` | `∃ p hp, Measurable p ∧ equivariant p ∧ GoodId μ p ∧ ErgodicVAdd Rot (D×D) (law μ p hp)` |
| `ergodic_wild_fourier_of_terminalObligation` | `TerminalObligation μ ⇒ ∫ eval z dμ = 0` |
| `terminalObligation_of_exists_terminal_factor` | the existing tree discharges `TerminalObligation`, so the interface is non-vacuous |

Consequence: the two approximation sites in `Stationary.lean` are only used to *certify* the
terminal factor, never to construct it, and what they certify is a strictly weaker statement than
`UniversalGood`. Any reroute that produces `TerminalObligation` by other means deletes §1's 5.3k
lines.

## 5. Why `(N)` is the crux, and what it reduces to

If the maximal compact extension `Y*` determines the point (`id` is `Y*`-measurable) then the
relative square over `Y*` is the diagonal, hence ergodic, and `GoodId μ Y*` is *false* (the
relative law is `δ_1`, `1 ∈ C`). So maximality is compatible with maximal failure, and every
R1-shaped route needs the side condition

> (N) a wild ergodic `μ` is not a compact extension of the point.

(N) is not free. Reducing it: `Y* = X` iff `L²(μ)` is spanned by vectors with precompact
`K`-orbit; the characters `eval z` (`z ≠ 0`) are in `L²(μ)`, and `k·eval z = eval(k⁻¹z)`, so
compactness over the point is equivalent to

> for every `ε > 0` there are `k_1,… ,k_m ∈ K` with `∀k ∈ K ∃i: Re μ̂((k-k_i)z) > 1-ε`

i.e. **total boundedness of the orbit `Kz` in the pseudometric `ρ(w,w')² = 2 - 2 Re μ̂(w-w')`**.
Because `μ` is `K`-invariant, `μ̂(kw) = μ̂(w)`, so the level sets `{w : Re μ̂(w) > 1-ε}` are
`K`-invariant; and since `|eval w| = 1`, they are approximately closed under addition. So (N)
says the level sets of `μ̂` are *not* close to syndetic. Any proof of (N) is therefore a decay
statement about `μ̂` — i.e. morally a fragment of the target theorem — which is why it is the
part of the reroute that cannot be assumed and must be attacked directly.

## 6. (N) is discharged — see `N-proof.md`

`N-proof.md` in this directory proves the side condition (N) that finding f4 identified as the
hole in every R1/R3/R6 plan:

> If `μ` is a probability on `D` with `IsWild μ`, then for every `z ∈ E`, `z ≠ 0`, the `K`-orbit
> of `eval z` in `L²(μ)` is not precompact. Hence `L²(Y*) ⊆ A ⊊ L²(μ)` and `id` is not
> `Y*`-measurable, which is exactly (H2) for Theorem A at the maximal compact extension.

The engine is three lines: `μ` is `K`-invariant so `μ̂(kw) = μ̂(w)`; `|eval w| = 1` makes
`w ↦ ‖eval w − 1‖` subadditive; and because `K` is **all** unit-modulus algebraic numbers
(Basic.lean:11), every algebraic number is a finite sum of elements of `K`, so total boundedness
of one orbit forces `μ̂ ≡ 1`, i.e. `μ = δ_1`, contradicting `μ(C) = 0` since `1 ∈ C`
(`jHom.map_one' = j_zero`). No ergodicity, no Theorem A, no mixing.

With this, the full R1 architecture is: `A` proper (§2) → `Y*` = maximum of
`{Y : L²(Y) ⊆ A}` with no Zorn (§3) → relative square over `Y*` ergodic by maximality +
transitivity of compactness → Theorem A at `Y*` using (H2) → `TerminalObligation` →
`ergodic_wild_fourier` → the headline theorem, with §1's 5.3k lines deleted and the two
structural obligations of finding f30 (standard predicate, ~200-300 lines) as the only new code.
