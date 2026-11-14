# (N)/(O) after the defect in N-proof.md

Status: **(N)/(O) is not proved by any argument currently on the board.** This note records
(i) the exact defect, (ii) a model that refutes the statement `N-proof.md` actually proves,
(iii) the sharpened statement that survives, (iv) an equivalent reduction that puts the
whole obligation on the fibre measures of the factor, and (v) what is now machine-checked
(`NBricks.lean`).

Recall (m15/AUDIT.md §4): the R1 glue needs `UniversalGood μ p` at the tower supremum, and
for the single map `d = id` that is

> **(O)**  `μR {z : z.1 / z.2 ∈ C} = 0`,  `μR := RelativeProduct.law μ p hp`,

where `p` is the tower supremum (the coarsest factor with ergodic relative product). By
Theorem A' this is equivalent to (H2): `p` is proper. `(N)` was to supply that. It does not.

## 1. The defect, exactly

`N-proof.md` §2 fixes `ε > 0`, takes a finite net `F ⊆ K` of the orbit at scale `ε`,
picks `k'' ∈ K ∖ F` and sets `w := k'' − k'`; then it propagates `φ(wz) < ε` to
`φ(vwz) ≤ L_v ε` for every `v ∈ E` and concludes

> "Hence `μ̂(vwz) ≥ 1 − (L ε)²/2` for every `ε > 0`, so `μ̂(vwz) = 1`."

`w` depends on `ε`: it is produced *after* `ε` from a net that itself depends on `ε`. For
fixed `v` the estimate therefore reads `μ̂(v w_ε z) ≥ 1 − L²ε²/2` with `w_ε → 0`, and
`μ̂(v w_ε z) → μ̂(0) = 1` is a triviality. No `ε → 0` conclusion about a *fixed* argument is
available, and no repair by an ε/3 split helps: the pigeonhole can only ever produce
`w_ε → 0`, because the net property is used at a single scale.

## 2. The statement N-proof.md proves is false

Let `ν := N_ℂ(0, 2I)` on `ℂ` and `μ := j_*ν`. Then

* `μ̂(a) = ∫ exp(i⟨ξ,a⟩) dν(ξ) = exp(−‖a‖²)` for every `a : E`, so `μ` is a probability
  measure with Fourier transform `exp(−‖a‖²)`;
* `μ` is `K`-invariant: `u • j ξ = j(conj(kCoeff u)·ξ)` (`scalar_j`) and `ν` is
  rotation-invariant, so `u_* μ = j_*(rot ν) = μ`;
* **every** `K`-orbit is precompact: `‖char(ky) − char(k'y)‖² = 2 − 2exp(−‖(k−k')y‖²)`, which
  is `≤ 2 − 2exp(−δ²‖y‖²)` whenever `|k − k'| < δ`; `K ⊆ S¹` is totally bounded in the
  Euclidean metric, so a finite Euclidean `δ`-net for `K` is a finite net for the whole
  orbit, at every scale;
* yet `μ = j_*ν` is carried by `j(ℂ) = C`, so `μ(C) = 1 ≠ 0`: the conclusion `μ = δ₁` that
  the §2 argument draws from precompactness is **false** for this `μ`.

(`μ` is not wild, so this does not refute (N) itself. It refutes the implication
`precompact ⟹ μ = δ₁` on which the documented proof rests, and with it every argument of
that shape.)

## 3. What survives, and the reduction

The sharpened statement consistent with the model is

> **(N')** If some (equivalently every) `K`-orbit in `L²(μ)` is precompact, then `μ(C) = 1`.

Since `IsWild` demands `μ(C) = 0`, (N') implies (N). Two of its three steps are elementary:

1. **(F1)** `ν(a) := μ̂(a)` satisfies `ν(k a) = ν(a)` for `k ∈ K`. [machine-checked]
2. **(F2)** `‖char(a+b) d − 1‖ ≤ ‖char a d − 1‖ + ‖char b d − 1‖`, hence `φ` is subadditive
   and `|ν(a) − ν(b)| ≤ φ(a − b)` by positive definiteness. [machine-checked]
3. If `ν` is continuous at `0` for the **Euclidean** topology of `ℂ`, then `ν` is Euclidean
   continuous everywhere (step 2), and since `K ⊆ S¹` is Euclidean dense and `|ka| = |a|`,
   `ν` is **radial**: `ν(a) = ρ(‖a‖)`.
4. `ρ(‖·‖)` is then positive definite on `ℂ` (a continuous p.d. function on the dense
   subgroup `E` extends), so it is `ν̂₀` for a rotation-invariant probability `ν₀` on `ℂ`;
   Fourier coefficients separate measures on `D` (trigonometric polynomials are dense), so
   `μ = j_*ν₀`, hence `μ(C) = 1`.

**So (N') is equivalent to:** total boundedness of `(K, d₁)`, `d₁(k,k') := φ(k − k')`,
forces `ν` to be Euclidean continuous. Equivalently, in completion language: the closure
`G` of the `K`-action in `U(L²(μ))` is a compact group, and one must show the inclusion
`K ↪ S¹` extends to `G → S¹`. Nothing in `IsWild` or in precompactness currently gives that:
`K` is dense in both `S¹` and `G`, both compact, and two compactifications of the same
countable divisible group need not be comparable. A counterexample to (N) is exactly a
`K`-invariant positive-definite `ν` with `(K, d₁)` totally bounded, `ν` *not* Euclidean
continuous, and `μ(C) = 0`.

## 4. A second, cheaper equivalent form of (O): fibre measures

`μR = ∫_Y (κ_y ⊗ κ_y) dν(y)` where `κ_y = condDistrib id p μ` is the fibre measure of the
factor `p` over `y`, and

`μR {z : z.1 / z.2 ∈ C} = ∫_Y (κ_y ⊗ κ_y){ratio ∈ C} dν(y)`,

with `(κ ⊗ κ){ratio ∈ C} = ∫ κ(x C) dκ(x)`. Hence

> **(†)**  for `ν`-a.e. `y`: `κ_y(x C) = 0` for `κ_y`-a.e. `x`  ⟹  (O).

This is a genuine reduction: it needs nothing about the Koopman spectrum, nothing about
`C`-nullness of a joining, and it is *statement-level* arithmetic with the existing lemma
`wild_independent_difference` (`Basic.lean:326`), which is (†) at the point factor, i.e.
`(μ ⊗ μ){ratio ∈ C} = 0` — the tree already knows the base case.

Also worth recording: (†) is **downward closed** (a mixture of measures each satisfying (†)
satisfies (†)), holds at the point factor, and *fails at the top factor* (there `κ_y = δ_y`
and `ratio ≡ 1 ∈ C`). So (†) is a fineness condition, exactly like `UniversalGood`, and no
monotonicity of `(†)` in the factor can move it up the tower. That is the precise sense in
which "(O) is not a formal consequence of IsWild": `IsWild` is a statement about the coarse
end of the tower, and (O) about the fine end.

## 4b. Two simplifications found after the first draft

**(i) `ν` is automatically radial — no continuity needed.** For `a, b ∈ E` with
`‖a‖ = ‖b‖ ≠ 0` we have `b/a ∈ E` and `‖b/a‖ = 1`, so `b/a ∈ K` by definition of `K`, and
`ν(b) = ν((b/a)·a) = ν(a)` by (F1). So `ν(a) = ρ(‖a‖)` *always*, and the whole of (N')
reduces to

> total boundedness of the orbit ⟹ `ρ` is continuous at `0`,

because `ρ ∘ ‖·‖` continuous at `0` extends to a continuous p.d. function on `ℂ`, hence is
`ν̂₀` for a rotation-invariant `ν₀` on `ℂ`, hence `μ = j_*ν₀` hence `μ(C) = 1`. Conversely
continuity at `0` plainly implies total boundedness (a finite Euclidean net for `K ⊆ S¹`
is a finite net for the orbit). **So (N') ⟺ "total boundedness forces `ρ` continuous at
`0`"**, one step shorter than §3 and with radiality free.

**(ii) The hypothesis in radial form.** Put `Λ_ε := {a : Re ν(a) > 1 − ε²/2}`, so
`Λ_ε = {a : ‖a‖ ∈ S_ε}`. Then: `Λ_ε − Λ_ε ⊆ Λ_{2ε+ε²/2}` (positive definiteness), `K` is
covered by finitely many translates `k_i + Λ_ε` (total boundedness), and `⟨K⟩ = E`
(additively, by (F3)) forces `⟨Λ_ε⟩ = E` for every `ε`: the *divisibility* of `E` upgrades
finite index to equality. So the hypothesis becomes a pure statement about the radial
profile: **for every `ε > 0` the sphere-radii `S_ε` are such that finitely many translates
of the radial set `{a : ‖a‖ ∈ S_ε}` cover `K`** — equivalently `Λ_ε` generates `E`. What is
missing is only the passage from "`Λ_ε` generates `E`" to "`Λ_ε` contains a Euclidean ball
around `0`", and that passage is where the length obstruction of §1 reappears: the
generating expression for `y` has length `L_ε(y) → ∞` as `ε → 0`. A counterexample to (N')
must therefore be a radial p.d. `ρ` with `Λ_ε` generating `E` for every `ε` and `ρ`
discontinuous at `0`; whether such a `ρ` can satisfy `μ(C) = 0` is exactly the open point.

## 4c. Two attacks that do not close, recorded so they are not repeated

**(a) The equivariant-fibre theorem only excludes non-identity cosets.**
`fixed_of_positive_fiber` (`Basic.lean:189`) applied to the `K`-equivariant map
`π : D × D → D/C`, `π(x₁,x₂) = [x₁/x₂]` (well defined: `k • (d₁/d₂) = (k • d₁)/(k • d₂)`,
and `C` is `K`-invariant), with `μR` in place of `μ`, gives: if `μR{π = q} > 0` then `q` is
`K`-fixed, and the only `K`-fixed coset is `C` itself (`minusOne ∈ K` plus
`coset_fixed_minusOne`). That is: **every non-identity coset is `μR`-null** — hence also
`μR{x₁/x₂ ∈ d₀ C} = 0` for every `d₀ ∉ C`. The one coset the theorem cannot exclude is
exactly `C = j(ℂ)`, i.e. (O). (The same argument with `π = [·]` on `D` is the proof of
`wild_coset_null`, and the reason it finishes there is the wildness hypothesis `μ(C) = 0`.)
So (O) is precisely "the *identity*-coset case of the wildness statement, for the relative
product"; there is no equivariance argument that reaches it, because the whole point of
`IsWild` is that the identity coset is null.

**(b) A "hole" in the radial profile at `0` is compatible with total boundedness.**
In the radial form of §4b, a lack of continuity at `0` means `S_ε` misses an interval
`(0,δ)`, hence every `k ∈ K ∖ F` must be at Euclidean distance `≥ δ` from *every* net point
`k_i ∈ F` (a chord in `(0,δ)` would be a good chord). This is satisfiable: `F = {1,−1}`
works whenever `S_ε ⊇ [0,√2]`, because `‖k−1‖² + ‖k+1‖² = 4`, so for every `k` at least one
of the two chords is `≤ √2`. Positive definiteness then forces `ν ≈ 1` on the `√2`-ball
around `0` (via `|ν(a) − ν(0)| ≤ √(2 − 2Re ν(a))`), i.e. such an example is `≈ δ₁` and has
`μ(C) ≈ 1`, so it is not a counterexample to (N') — but it shows that total boundedness
alone neither implies nor forbids continuity at `0`: the only remaining input is wildness
`μ(C) = 0` itself.

## 5. Machine-checked (`NBricks.lean` and `F3.lean`, verified with `lean` under `scripts/env4341.sh`)

* `norm_char_add_sub_one_le`, `norm_char_sum_sub_one_le` — (F2), pointwise and finitary.
* `char_kCoeff_mul_eq_char_smul`, `integral_char_kCoeff_mul` — (F1).
* `one_mem_C` (`1 = j 0 ∈ C`), `wild_ne_dirac_of_mem_C` — (O)-side triviality used by the
  `r = 0` branch of Theorem A.
* `F3.lean`: `exists_list_sum_kCoeff : ∀ z : E, ∃ l : List K, z = (l.map kCoeff).sum` —
  **(F3)**, that `K` additively generates `E`, in the general form. The tree has only the
  real two-term case (`ConditionalSpectrum.lean:116`). Supporting lemmas: `iK`,
  `kCoeff_iK`, `kCoeff_iK_mul`, `map_map_kCoeff_mul_iK`, `list_sum_map_mul_left`,
  `exists_list_sum_kCoeff_ofF` (the real case, by scaling `real_algebraic_sum_two_rotations`).

## 6. Consequence for the sprint

`TowerMax.lean`'s own docstring concedes that `hgood` (= properness of the supremum) is the
one obligation maximality cannot supply. With the `N-proof.md` route invalid, R1's 4112
declaration lines are **not** currently realisable without a new hypothesis, and the
acceptance criterion (a) is out of reach until one of the following is supplied:

* a proof of (N') / of the `G → S¹` extension of §3, or
* a proof of (†) at the tower supremum (§4), or
* any other proof of a.e. non-`C`-ness of `z ↦ z.1/z.2` over the supremum.

Acceptance criterion (b) is available now: the measured prize is unchanged (4112 declaration
lines by the m10 harness certificate), but the restructure cannot be certified, so the honest
figure is the baseline plus the neutral preparation cost.

## 7. Independent check of a second structural defect (corroborates m1's d12)

`TowerMax.Tower.step` takes `H` measurable with `‖H‖ ≤ 2` and only asks `H` to be *not*
already a function of `p`. There is **no compactness hypothesis on `H`** (compare
`CompactTower.strict_compact_successor`, which produces an `H` whose orbit is totally
bounded). Hence every bounded measurable function can be adjoined in one step, and since
`L²(μ)` is separable, countably many steps (the `join` constructor absorbs limits) reach
the top factor `id`. So the "tower supremum" of `TowerMax.exists_ergodic_factor` is the
*top* factor, its relative product is the diagonal — which is ergodic, so
`exists_ergodic_factor` is true but content-free — and `hgood` at that point is False, not
merely unproven: `UniversalGood` fails at the top because the relative law there is `δ₁`
and `1 ∈ C` (`one_mem_C`). So `exists_terminal_factor_of_tower_good` is vacuous as stated,
independently of §1–§4.

A repair must add the compactness hypothesis to `Tower.step` (the tree's
`CompactFunctions.Compact` / `compactSigma`, or "`H`'s `K`-orbit is totally bounded mod
`L²(p)`"), and then the sup is the *maximal compact extension* and `hgood` at the sup is
exactly properness — i.e. (N') again. Both defects therefore land on the same obligation.
