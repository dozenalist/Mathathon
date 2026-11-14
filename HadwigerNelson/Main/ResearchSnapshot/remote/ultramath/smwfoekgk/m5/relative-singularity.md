# Theorem A, formalised (member m5, direction d2 = R4)

## Statement proved in Lean

`work/C.lean`, check with

```
source scripts/env4341.sh
cd .ultramath/smwfoekgk/m5/work
LEAN_PATH="$PWD:$LEAN_PATH" lean Chk.lean        # ~12 min, prints the axioms
```

```
OAI.PlaneFiveColor.Spectral.RelativeSingularity.relative_singularity_of_ergodic
  {X Y} [MeasurableSpace X] [MeasurableSpace Y] [StandardBorelSpace X] [Nonempty X]
        [StandardBorelSpace Y] [Nonempty Y] [MulAction K X]
  (μ : Measure X) [IsProbabilityMeasure μ] (q : X → Y) (hq : Measurable q)
  (d : X → D) (hd : Measurable d)
  (hde : ∀ k x, d (k • x) = k • d x)                       -- d is K-equivariant
  [ErgodicVAdd Rot (X × X) (RelativeProduct.law μ q hq)]    -- (H1)
  (hdiag : ¬ ∀ᵐ z ∂(RelativeProduct.law μ q hq), d z.1 = d z.2)   -- (H2) sharp form
  : DifferenceFourier.differenceLaw (μ.map q) (condDistrib d q μ) C = 0
```
Axioms: `[propext, Classical.choice, Quot.sound]`. No `sorry`, no `native_decide`, no `opaque`.

**Note on hypotheses.** The theorem is *stronger* than the paper's Lemma 2.7 replacement
in two ways, and both matter for reuse:

* it does **not** need `IsWild (μ.map d)`.  `UniversalGood` carries that hypothesis anyway,
  so this is free; but it shows wildness plays no role in relative singularity at an
  ergodic relative product.
* (H1) is *literally* the instance the tree uses at the only consumer of `UniversalGood`
  (`Analysis/PlaneSpectrum/Ergodicity.lean:37`, `ergodic_wild_fourier`), so the theorem
  plugs in there with no restatement.

**(H2) is stated in the sharp finite form actually consumed**, `d` is not a.e. constant on
the relative product, not as "`d` is not `q`-measurable".  The `r = 0` branch of the proof
is exactly the implication  (*) `d =ᵐ g ∘ q` for measurable `g` ⟹ a.e. `d z.1 = d z.2`,
together with a measurable selection of the Dirac fibres of `condDistrib id q μ`.  The
easy direction of (*) is what the application supplies; the converse is the remaining
formalisation gap (see "Remaining gap").  The paper's printed Lemma 2.7 is false without
this hypothesis (at `Y = X`, `δ_0` has `C`-mass 1), so some form of (H2) is unavoidable.

## What is machine-checked, module by module

| file | lines | content |
|---|---|---|
| `work/A.lean` | 111 | `gram_obstruction`, `no_four_points` (four equidistant points need `finrank ≥ 3`) — ported unchanged from `.ultramath/smwfk0ybk/m11/work/Core.lean` where they were verified |
| `work/B.lean` | 131 | `exists_four_pairwise` (four conditionally independent samples with all six pairs in a conull `T`), `measure_eq_zero_or_univ_of_ae_invariant` (the 0/1 law for an a.e.-invariant measurable set) |
| `work/C.lean` | 399 | `C_eq_range`, `image_closedBall_measurable`, `image_closedBall_zero`, `C_eq_iUnion`, `kCoeff_norm`, `scalar_div`, `differenceLaw_eq_law`, `relative_singularity_of_ergodic` |
| `work/D.lean` | 71 | `differenceLaw_id_C_eq_zero_of_ergodic` (Theorem A at `d = id`, the exact C-nullity that `ergodic_wild_fourier` needs) and `differenceLaw_C_eq_one_of_diag` (sharpness: (H2) is not removable) |

Build, in this order (each imports the previous one's `.olean`):

```
source scripts/env4341.sh
cd .ultramath/smwfoekgk/m5/work
lean -o A.olean A.lean                                   # 18 s
LEAN_PATH="$PWD:$LEAN_PATH" lean -o B.olean B.lean       # 60 s
LEAN_PATH="$PWD:$LEAN_PATH" lean -o C.olean C.lean       # 2-9 min, disk dependent
LEAN_PATH="$PWD:$LEAN_PATH" lean -o D.olean D.lean       # 15 s with warm cache
LEAN_PATH="$PWD:$LEAN_PATH" lean Chk2.lean               # prints all seven axioms
```

All seven checked theorems depend only on `[propext, Classical.choice, Quot.sound]`.
Toolchain: pinned Lean 4.34.1 + `.scratch/mathlib4` (d13f23b) with `lean/build/lib` on
`LEAN_PATH` (the OAI oleans are 4.34.1-built).  Not re-checked under the stock 4.33.1
toolchain, because that would require rebuilding all 83 OAI modules against `/opt/mathlib`;
nothing in these four files is version-sensitive except through OAI itself.

## The proof, in the form in which it was formalised

Notation: `ν = μ.map q`, `κ = condDistrib id q μ`, `μR = RelativeProduct.law μ q hq`
`= (κ.prod κ) ∘ₘ ν` (`law_eq_mixture`), `ratio z = d z.1 / d z.2`,
`A t = {z | ratio z ∈ j '' closedBall 0 t}`.

1. **Bridge.** `differenceLaw ν (condDistrib d q μ) = μR.map ratio`.  (Needs
   `condDistrib d q μ =ᵐ[ν] (condDistrib id q μ).map d`, i.e. `condDistrib_comp`, plus
   `Measure.map_prod_map`.  This is the only place the two developments interact.)
2. **Radial family.** Each `A t` is measurable, monotone in `t`, and `A t ⊆ (g +ᵥ ·)⁻¹ A t`
   for `g : Rot`: equvariance of `d` gives `ratio (g +ᵥ z) = scalar (kCoeff (rotMul g)) (ratio z)`,
   and `scalar a (j ξ) = j (conj a * ξ)` with `‖conj (kCoeff k)‖ = 1` preserves the modulus.
   Measure invariance gives a.e. invariance, so by (H1) each `μR (A t) ∈ {0,1}`.
3. **Threshold.** Let `Tset = {t ≥ 0 | μR (A t) = 1}`, `r = sInf Tset`.  `Tset` is nonempty
   because `⋃ n A n = ratio ⁻¹' C` and `μR` of that set is the quantity under consideration.
   Then `μR (A t) = 1` for `t > r`, `= 0` for `0 ≤ t < r`, and (using
   `⋂ m A (r + 1/(m+1)) = A r`) also `μR (A r) = 1`.
4. **`r = 0`.**  `A 0 = {z | d z.1 = d z.2}`, so (H2) is violated. **This is the only use
   of (H2).**
5. **`r > 0`.**  With `U m = A (r − r/(m+1))`, the set `A r \ ⋃ m U m` is conull and equals
   `ratio ⁻¹' SphD` where `SphD = j '' closedBall 0 r \ ⋃ m j '' closedBall 0 (r − r/(m+1))`,
   and `w ∈ SphD ↔ ∃ ξ, j ξ = w ∧ ‖ξ‖ = r`.  Hence for `ν`-a.e. `y`,
   `(κ y ⊗ κ y) (ratio ⁻¹' SphD) = 1`; pushing by `d` (using
   `Measure.map_prod_map`) gives a probability `λ` on `D` with
   `λ ⊗ λ {(p,q) | p/q ∈ SphD} = 1`.  `exists_four_pairwise` produces `a b c' e` with all
   six ratios in `SphD`, say `j ξ_{ab} = a/b` etc., `‖ξ_{·}‖ = r`.  Then
   `j (ξ_ab + ξ_bc') = (a/b)(b/c') = a/c' = j ξ_ac'` forces `ξ_ac' = ξ_ab + ξ_bc'`, and
   likewise for the other two pairs, so `0, ξ_ab, ξ_ac', ξ_ad` are four points of `ℂ` at
   pairwise distance `r > 0`, contradicting `no_four_points` (`finrank ℝ ℂ = 2`).
6. Therefore `μR (ratio ⁻¹' C) = 0`, i.e. `differenceLaw ν (condDistrib d q μ) C = 0`.

Two simplifications relative to the swarm's earlier plan, both now checked:

* no Gram matrix is needed — but `no_four_points` is already available, so the four-sample
  version costs nothing extra: the four pair-marginals of `λ^⊗4` are all `λ ⊗ λ`, and a
  union bound over the six pair events gives the four good points.
* no measurable-selection theorem and no kernel-integral measurability is needed anywhere in
  the `r > 0` branch: the modulus is handled by the *sets* `j '' closedBall 0 t` (compact
  images, hence measurable) instead of by a radial *function*.

## Remaining gap (precisely)

To replace the hypothesis `hdiag` by "`d` is not `q`-measurable" one has to prove

  `(∀ᵐ z ∂μR, d z.1 = d z.2) → ∃ g : Y → D, Measurable g ∧ d =ᵐ[μ] g ∘ q`.

Route (all ingredients exist in the tree/library):
(a) `μR {z | d z.1 = d z.2} = ∫⁻ y, (κ y ⊗ κ y) {d z.1 = d z.2} ∂ν`, so for `ν`-a.e. `y`
    the inner measure is 1 (`lintegral_eq_zero_iff` on the complement);
(b) `Measure.prod_apply`: for `κ_y`-a.e. `x`, `κ_y {x' | d x' = d x} = 1`;
(c) from (b) and `IsProbabilityMeasure (κ y)`, all "good" `x` carry the same `d`-value, so
    `κ_y` is carried by a single `d`-fibre;
(d) a measurable selection: `Ψ : D → OrbitSpace DiscreteE`, `Ψ w = (w z)_{z : DiscreteE}` is
    continuous and injective, so `Ψ_measurableEmbedding.measurable_invFun` (the device the
    tree already uses in `FactorCode.decode`) selects the point from the measurable family
    `y ↦ (κ y (C_n))_n`; comparing with `Ψ ∘ d` finishes.

Steps (a)-(c) are ~60 lines, (d) ~60 lines.  They were **not** written; everything else is
complete and compiling.  Until they are, the honest statement of the deliverable is:
"Theorem A with (H2) in the sharp finite form", which is exactly what the `r = 0` branch
consumes and is *weaker* than (H2)-as-non-measurability only in that one direction.

## Consequences for the other routes

* (H1) in the tree is `ErgodicVAdd Rot (D × D) (RelativeProduct.law μ q hq)`, so R4 delivers
  `UniversalGood μ q` as soon as that instance and `hdiag` are available — no compactness, no
  approximation property (2.6), no phase-collision induction.
* R1 still has to certify that the maximal compact extension is *proper*: if it is `X`
  itself then `hdiag` fails, and the tree's own `ergodic_wild_fourier` argument does not go
  through.  See the board finding f22.

## Measured budget (acceptance criterion (c))

Import graph of `lean/OAI`: 83 modules, 31277 lines.

* the whole direct home of the approximation property (2.6) and of `UniversalGood` is
  `CompactFactors/Approximation.lean` (496) + `CompactFactors/ConditionalLimits.lean` (701)
  = **1197 lines**.  A fully successful R4 therefore deletes at most ~1197 lines — *below*
  the 1500-line target.  R4 removes an obstruction; it does not by itself produce 2000 lines.
* the rest has to come from the tower.  The `CompactFactors` subtree is 14 modules,
  **7728 lines**: Amenability 411, BoundedFunctions 223, Functions 884, Kernels 774,
  Factors 586, Centers 703, RelativeCenters 598, RelativeProducts 472, Separability 573,
  AlgebraModels 664, ConditionalSelection 442, Approximation 496, ConditionalLimits 701,
  Stationary 201.  11 modules outside the subtree (3548 lines) import it, but for the main
  theorem only through `Ergodicity`/`RadialEnergy`.
* no single `CompactFactors` module is an exclusive dependency of another: deleting one
  costs exactly its own line count.  Deletions are additive and independent, so partial
  success is measurable — useful for the R9 harness.
* R1/R2 must still construct, without a tower, a factor strictly finer than the trivial one
  whose relative product is ergodic.  Theorem A makes the *wildness* half free; the
  *existence* half is now the entire budget.  The candidate target is
  Kernels + Factors + Centers + RelativeCenters + RelativeProducts + Separability +
  AlgebraModels = 4407 lines, with Functions + Amenability + BoundedFunctions (1518) kept as
  reusable L²/amenability plumbing.
