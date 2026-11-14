# Relative singularity from a single factor: a four-step replacement for Lemma 2.7 of the paper

Member m11, direction d11 (Step 2, route (b): "replace the Furstenberg–Zimmer tower by a single
compact factor or by a maximal compact extension, and prove directly the relative product property").

**Result.** The paper's Lemma 2.7 (Relative singularity) is used exactly once in the whole proof of
Theorem 1.3, namely in §3.3, at the *terminal* factor of the compact tower of Lemma 3.1. At that
factor the relative product `X ×_Y X` is ergodic (Lemma 3.1(3)). It is therefore enough to prove:

> **Theorem A.** Let `K` be a countable group acting by measure-preserving automorphisms on a
> compact abelian group `D`, let `C ⊆ D` be a Borel subgroup isomorphic to `ℝ²` via a group
> isomorphism `j : ℝ² → C` such that every `k ∈ K` maps `C` to `C` and the induced map on
> `j`-parameters is orthogonal. Let `X` be an ergodic probability-preserving `K`-system, `Y` an
> invariant factor, `R = X ×_Y X` with the diagonal action, and `d : X → D` a Borel equivariant map
> whose law is *wild*, `d_*μ(C) = 0`. If
> **(H1)** `R` is ergodic, and
> **(H2)** `d` is not `Y`-measurable (does not agree a.e. with `f ∘ π_Y`),
> then the relative difference law `ν_Y` of `d(x)/d(x')` for conditionally independent `x, x'`
> over `Y` satisfies `ν_Y(C) = 0`.

This replaces the transfinite induction with phase collisions (§2.4, ≈ 4½ pages: from the statement
of Lemma 2.7 to the end of §2.4) by four lines of measure theory, and it makes the approximation
property (2.6) of the tower — the only place where the compactness of the extensions is used —
dispensable altogether. Informally: **the tower is needed to *produce* a factor over which the
relative product is ergodic; it is not needed to prove that the relative difference law is wild
there.** The wildness at such a factor follows from ergodicity of the relative product plus
non-measurability of `d`, with no compactness at all.

The two finite inputs of step 4 are machine-checked (stock toolchain, Lean 4.33.1 + `/opt/mathlib`):

```
lean .ultramath/smwfk0ybk/m11/work/Core.lean
```

`SwarmM11.gram_obstruction`, `SwarmM11.no_four_points`, `SwarmM11.no_measure_fixed_difference_norm`,
all depending only on `[propext, Classical.choice, Quot.sound]`.

---

## 1. The four-step proof

Notation as in the paper: `D` is the Pontryagin dual of the discrete additive group `E`, `C ⊂ D` is
the subgroup of ordinary continuous characters, `j : ℝ² → C` the additive-to-multiplicative
parametrisation (`j_add`), and `K` acts on `D` by `(k d)(z) = d(kz)`, a group automorphism, with
`kC = C` and `j⁻¹(k · j(ξ)) = O_k ξ` for an orthogonal `O_k` (paper §2.1, p. 6: "an element of `K`
acts on these parameters by an orthogonal map"). Write `μ` for the law on `X`, `ν` for the law of
`π_Y`, `κ_y` for the disintegration of `μ` over `Y`, and
`μ_R = ∫ κ_y ⊗ κ_y dν(y)` for the law of the relative product. `d(x)/d(x')` is the group difference
in `D`. Recall `ν_Y = (μ_R).map (x,x') ↦ d(x)/d(x')`, so `ν_Y(C) = μ_R(F)` with
`F = {(x,x') : d(x)/d(x') ∈ C}`.

**Step 1 (the dichotomy).** `F` is Borel (`d` Borel, `C` Borel — paper p. 6) and invariant under
the diagonal action: for `k ∈ K`,
`d(kx)/d(kx') = k(d(x))/k(d(x')) = k(d(x)/d(x'))`, using that `k` is an automorphism of `D`, and
`kC = C`, so `(kx,kx') ∈ F ⟺ (x,x') ∈ F`. By (H1), `μ_R(F) ∈ {0,1}`.

Assume from now on `μ_R(F) = 1`; we derive a contradiction. (Conclusion: `μ_R(F) = 0`, i.e.
`ν_Y(C) = 0`.)

**Step 2 (the radial function is constant).** On `F` define `ρ(x,x') = |j⁻¹(d(x)/d(x'))|`, and
`ρ = 0` off `F`. Then `ρ` is Borel, `[0,∞)`-valued, and on `F`
`ρ(kx,kx') = |j⁻¹(k(d(x)/d(x')))| = |O_k j⁻¹(d(x)/d(x'))| = ρ(x,x')`,
because `O_k` is orthogonal. Since `F` is conull and invariant, `ρ·1_F` is invariant, so by (H1)
there is `r ∈ [0,∞)` with `ρ = r` `μ_R`-a.e. (In particular `r` is finite.)

**Step 3 (case `r = 0`).** Then `d(x) = d(x')` for `μ_R`-a.e. pair. By the disintegration, for
`ν`-a.e. `y` the law `κ_y` is carried by a single point under `d`: the barycentre
`f(y) = ∫ d dκ_y` (Borel, `D` compact metrisable) satisfies `d = f ∘ π_Y` a.e. So `d` is
`Y`-measurable, contradicting (H2). Hence `r > 0`.

**Step 4 (case `r > 0`, the contradiction).** For `ν`-a.e. `y`, both `κ_y ⊗ κ_y(F) = 1` and
`ρ = r` `κ_y ⊗ κ_y`-a.e. Fix such a `y` (it exists: `ν` is a probability). Take four
`κ_y`-independent samples `x_1, …, x_4`. For each of the six pairs, `d(x_i)/d(x_j) ∈ C` and
`|j⁻¹(d(x_i)/d(x_j))| = r` with probability one, so all six hold simultaneously. Put
`u_i = j⁻¹(d(x_i)/d(x_1))` for `i = 2,3,4` (well defined since `d(x_i)/d(x_1) ∈ C`). Then
`|u_i| = r` and `u_i - u_j = j⁻¹(d(x_i)/d(x_j))` (additivity of `j`, `j_add`), so `|u_i - u_j| = r`.
Hence `0, u_2, u_3, u_4` are four points of `ℝ²` that are pairwise at distance `r > 0`: impossible.
Equivalently, and this is the machine-checked form: the pushed-forward law
`λ = (κ_y).map (x ↦ j⁻¹(d(x)/d(x_0)))` (any base point `x_0` in the fibre) is a probability measure
on `ℝ²` with `(λ ⊗ λ){‖p₁ - p₂‖ = r} = 1`, and no such measure exists
(`no_measure_fixed_difference_norm`). ∎

The only two facts about `(D, C, K, j)` used are: `C` is a subgroup on which `j` is an isomorphism
of abstract groups, and `K` acts on it by orthogonal maps in the `j`-parameters. Both are proved in
the paper (§2.1) and formalised in `lean/OAI/Analysis/PlaneSpectrum/Basic.lean`
(`j_add`, `kCoeff`/`eval_scalar`, `scalar_mem_C`).

## 2. Interface with the paper: why this is enough for the transfer

* Lemma 2.7 is invoked in the paper exactly once: §3.3, "Apply Lemma 3.1 to the system `(D, µ)`, and
  let `Y` be its terminal factor. Lemma 2.7, applied to the identity map of `D`, says that the
  conditional difference law `ν_Y` over this factor is wild." (`paper.txt` lines 941–945.)
* Everything after that point uses only: `Y` is a factor with `X ×_Y X` ergodic (Lemma 3.2's
  hypothesis, and Lemma 3.3's proof via mean ergodicity on `Y`), plus `P = E(·|Y)`, `g_z = Pψ_z`,
  `m(z) = ‖g_z‖²`, and the wildness `f_{ν_Y} = m` of (3.11) together with Lemma 2.5. No later step
  refers to a tower, to (2.6), or to any intermediate factor.
* Consequently Theorem A applied with `X = D`, `d = id`, `Y = Y_η` gives exactly what §3.3 uses,
  **provided `Y_η ⊊ X`** (equivalently: the identity map is not `Y_η`-measurable).
* With Theorem A in place, the only remaining use of the tower is the *existence* statement of
  Lemma 3.1(3) — "there is a factor over which the relative product is ergodic". The approximation
  property (2.6) is used nowhere else in the paper (it appears only in the definition of the tower
  and in the statement and proof of Lemma 2.7), so it can be deleted from Lemma 3.1 without
  affecting anything else.

## 3. The hypotheses are sharp, and the compactness hypothesis is not

**(H2) cannot be dropped** (so the "single factor" statement needs non-measurability, not
compactness). Let `X = D`, `μ` an ergodic `K`-invariant probability with `μ(C) = 0` (e.g. an ergodic
component of Haar measure; `C` is Haar-null because it is a countable union of compact sets with
empty interior), `d = id : X → D` (wild), and take the top factor `Y = X`. Then `R = X ×_X X ≅ X`
is ergodic, `d` is `Y`-measurable, and the relative difference law is `δ_1`, whose `C`-mass is `1`
(`1 ∈ C`). So the conclusion fails. This also shows that the paper's Lemma 2.7 must be read with
`Y` a *proper* factor: at `Y = X` its conclusion is false for every wild `d`. The paper's §3.3 needs
precisely `Y_η ⊊ X`, so nothing is lost; the Lean development enforces it implicitly, because its
`UniversalGood μ p` quantifies over *all* equivariant wild `d`, so in the application (where
`X = D` and `d = id` is available) it would fail at a generating `p`.

**(H1) cannot be dropped** (relative-product ergodicity is the right hypothesis, and "wild marginal
plus `d` not `Y`-measurable" alone is not enough). Let `X = D` with Haar measure `μ`, `d = id`, and
let `Y = D/C` be the coset factor, `p(x) = xC`. Then `d` is wild and not `Y`-measurable, but
differences of two conditionally independent samples over `Y` lie in `C`, so `ν_Y(C) = 1`. Here `R`
is not ergodic: for any `s > 0` the function `(x,x') ↦ 1{|j⁻¹(x/x')| = s}` is well defined on `R`
(because `x/x' ∈ C`), invariant under the diagonal action (orthogonality), and non-constant. This is
exactly the "positive-mass cosets" configuration analysed in the proof of the paper's Lemma 2.7, and
it shows that (H1) is what the terminal factor supplies.

**The compactness hypothesis (2.6) is not needed for the singularity step.** By Theorem A, for the
terminal factor it is irrelevant: no compactness of any extension, no phase lists, no matching
distance, no `m²`-collision estimate. What (2.6) does supply in the paper is a route to *produce* the
terminal factor (Lemma 3.1); the existence of a factor with ergodic relative product can equally be
obtained by maximality among such factors, which is how the Lean development does it
(`CodedMax.exists_maximal` over `UniversalGood`, `Stationary.lean`).

**Lean-level confirmation of the interface.** The two hypotheses that
`Analysis/PlaneSpectrum/Ergodicity.lean` carries at the point where §3.3's argument starts are
exactly
`[ErgodicVAdd Rot (D×D) (RelativeProduct.law μ q hq)]` (relative-product ergodicity) and
`hw : IsWild (DifferenceFourier.differenceLaw (μ.map q) (condDistrib id q μ))` (relative singularity
for `d = id`). Theorem A is precisely a proof of the second from the first plus non-measurability of
the identity, so it is a drop-in replacement in the formal development as well.

## 4. Machine-checked core

`work/Core.lean` (self-contained: `import Mathlib`, ≈7 s, checked with `lean` on the stock
toolchain):

| declaration | statement |
|---|---|
| `SwarmM11.gram_obstruction` | three vectors with Gram matrix `(r²/2)(1+J)`, `r > 0`, are linearly independent, so `finrank ≥ 3` |
| `SwarmM11.no_four_points` | four points of a real inner product space with `finrank ≤ 2` are not pairwise at the same positive distance |
| `SwarmM11.no_measure_fixed_difference_norm` | a probability measure `λ` on `ℝ²` with `(λ ⊗ λ){‖p₁-p₂‖ = r} = 1`, `r > 0`, does not exist |

The third is exactly Step 4 after the disintegration; the second is its geometric content (Gram
determinant argument); the first is the linear algebra. Axioms: `[propext, Classical.choice,
Quot.sound]`.

What a full Lean formalisation of Theorem A would still need (all present in the repository, none of
it the FZ machinery): `RelativeProduct.law`/`condDistrib` (`MeasureTheory/CompactFactors/`), the
ergodicity instance for the relative product, `measurableSet_C`, and the Fubini step over the
disintegration producing `κ_y ⊗ κ_y`-a.e. statements from `μ_R`-a.e. ones. The theorem to add is

```lean
theorem relative_singularity_of_ergodic
    (μ : Measure X) [IsProbabilityMeasure μ] [ErgodicSMul K X μ]
    (p : X → Y) (hp : Measurable p) (hpe : ∀ k, ∀ᵐ x ∂μ, p (k • x) = k • p x)
    (hmix : ErgodicSMul K (X × X) (RelativeProduct.law μ p hp))
    (d : X → D) (hd : Measurable d) (hde : ∀ k, ∀ᵐ x ∂μ, d (k • x) = k • d x)
    (hwild : IsWild (μ.map d))
    (hnot : ∀ f : Y → D, Measurable f → ¬ (d =ᵐ[μ] f ∘ p)) :
    EuclideanFiveColor.DifferenceFourier.differenceLaw (μ.map p) (condDistrib d p μ) C = 0
```

which is a drop-in strengthening (different hypotheses, same conclusion) of what
`PlaneSpectrum/Ergodicity.lean` extracts from `exists_terminal_factor`.

## 5. Size of the saving

* Paper: Lemma 2.7's proof plus the (2.6) approximation property occupy ≈ 4½ pages of §2.4
  (pp. 9–14) out of the 17 pages of §2–§3, and they are the only part of the rigidity proof that
  needs the compact-tower induction.
* Lean (measured by import graph over `lean/OAI`, 83 modules, 31 277 lines): the cluster
  `PlaneSpectrum/ConditionalSpectrum.lean` (497), `SmallArcs.lean` (322),
  `CompactFactors/ConditionalSelection.lean` (442), `PlaneSpectrum/PhaseCollision.lean` (537),
  `PlaneSpectrum/PhaseEncoding.lean` (255) is a closed chain hanging off a single module
  (`CompactFactors/Approximation.lean`, home of `relative_singularity_successor`); nothing else
  imports any of it. With `relative_singularity_{base,successor,approximation}` and `UniversalGood`
  replaced by Theorem A, those 2 053 lines plus most of `CompactFactors/ConditionalLimits.lean`
  (701) become unnecessary, on top of the removal of (2.6) from `Factors.lean`.

## 6. Honest limits

* Theorem A is not a strengthening of Lemma 2.7: it is false at the top factor (see §3), and it
  says nothing about intermediate factors of a tower. It is exactly the statement §3.3 needs.
* The existence of a factor with ergodic relative product is *not* made cheaper by any of this: the
  Hilbert–Schmidt / finite-rank argument of Lemma 3.1 survives (in Lean,
  `CompactFactors/Factors.lean`, `Kernels.lean`, ...). What is shown is that the *singularity*
  induction on top of it is unnecessary.
* Only the finite core is machine-checked here. The Fubini/disintegration step and the
  measurability of `(x,x') ↦ d(x)/d(x')` are carried out on paper above.
* Properness of the terminal factor is required by the paper's own §3.3 as well: at `Y = X` one has
  `P = id`, `m ≡ 1`, and the section's conclusion "`m` vanishes off 0" is false. It is also implied
  by Lemma 2.7 itself, since at `Y = X` that lemma would assert `0 ∉ C`. So Theorem A's explicit
  non-measurability hypothesis loses no case; it only names a hypothesis the paper uses implicitly.
* Cross-check of the interface claim, by grep of the extracted text: `(2.6)` occurs only in its own
  definition, in the proof of Lemma 2.7 (lines 572, 577 of `pdftotext -layout` output) and in the
  construction of Lemma 3.1 (lines 725, 730, 735, 789); `Lemma 2.7` is cited only at line 943
  (§3.3). Nothing else in §1–§4 uses either.

## 7. How the paper would read (replacement text, no other change)

1. **§2.4.** Delete the definition of a tower (2.6) and Lemma 2.7 with its proof. Insert Theorem A
   above (statement + the four steps) as the new "relative singularity" lemma. Lemma 2.4, Lemma 2.5,
   Lemma 2.6 are untouched.
2. **§3.1.** Lemma 3.1 keeps its parts (1) trivial start and generated joins, (2) each successor is a
   *strict* extension, (3) the terminal factor has ergodic relative product. The approximation
   property (2.6) and the paragraph proving it ("The finite expansion of the rotated polynomial
   proves (2.6)") are deleted; the stopping rule and the separability argument that makes the
   ordinal countable are unchanged.
3. **§3.3.** Unchanged except for the citation: "Lemma 2.7, applied to the identity map of `D`"
   becomes "Theorem A applied with `d = id`", with the hypothesis `Y_η ⊊ X` made explicit; it holds
   because otherwise `P = id`, `m ≡ 1`, and the section's conclusion fails.
4. **Everything from §3.2 onwards** (Lemma 3.2, Lemma 3.3, §3.4, the number-field argument, the
   ergodic decomposition) is unchanged: `grep` of the extracted text shows that "tower" occurs only
   in §2.4, §3.1 and the citation at line 943, and that (2.6) occurs only in its own definition, in
   Lemma 2.7's proof and in Lemma 3.1's construction.
