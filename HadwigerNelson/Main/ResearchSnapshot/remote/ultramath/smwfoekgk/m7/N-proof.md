# Proof of (N): a wild measure is never a compact extension of the point

This closes the hole identified as f4/f41 (the side condition (N) that R1/R3/R6 need and that
neither the paper nor the tree supplies). The argument is elementary — Fourier coefficients,
total boundedness, `|eval z| = 1` — and needs **no ergodicity** and **no Theorem A**. All
constants below are from `lean/OAI/Analysis/PlaneSpectrum/Basic.lean`.

## 0. The objects

* `E := algebraicClosure ℚ ℂ` (Basic.lean:8), `DiscreteE := Multiplicative E` with the discrete
  topology, `D := PontryaginDual DiscreteE` (compact abelian group, Basic.lean:48-53).
* `K := {u : Circle | IsAlgebraic ℚ (u:ℂ)}` (Basic.lean:11-16): **all unit-modulus algebraic
  numbers**. `kCoeff : K → E` (`kCoeff u = ⟨u.val, ·⟩`, Basic.lean:224), multiplicative,
  `kCoeff 1 = 1`, `kCoeff u ≠ 0`.
* `j : ℂ → D`, `j ξ z = Circle.exp (inner ℝ ξ (embed z))` (Basic.lean:76-80), `j 0 = 1`
  (`j_zero`), `j (ξ+η) = j ξ · j η` (`j_add`), `jHom : Multiplicative ℂ →* D` with
  `map_one' := j_zero` (Basic.lean:94-98), `C := jHom.range` (Basic.lean:100).
  **Hence `(1 : D) ∈ C`.**
* The `K`-action on `D` (Basic.lean:234-237): `u • d := scalar (kCoeff u) d` where
  `scalar a d` is characterised by `scalar a (scalar b d) = scalar (a*b) d` (`scalar_mul`) and
  `scalar (a+b) d = scalar a d * scalar b d` (`scalar_add`) — i.e. `scalar a d` is the character
  `z ↦ d (a·z)` and `(u • d)(z) = d(kCoeff u · z)`.
* `eval z := scalar z` viewed as a circle-valued function on `D`; `eval 0 = 1`,
  `eval (a+b) = eval a · eval b`, `|eval z| = 1`. (In the tree: `scalar`.)
* `IsWild μ` (Basic.lean:300-303) = `(∀ u : K, MeasurePreserving (u • ·) μ μ) ∧ μ (C : Set D) = 0`.

Throughout, `μ` is a probability measure on `D` with `IsWild μ`. Write
`μ̂(w) := ∫ d, (eval w d : ℂ) ∂μ` and `φ(w) := ‖eval w − 1‖_{L²(μ)}`, so
`φ(w)^2 = 2 − 2 Re μ̂(w)` and `φ(0) = 0`.

## 1. Three elementary facts

**(F1) K-invariance of μ̂, hence of φ.** For `u : K`,
`∫ d, (eval w (u • d)) ∂μ = ∫ d, (eval w d) ∂μ` by `MeasurePreserving` of `d ↦ u • d`; and
`eval w (u • d) = d(kCoeff u · w) = eval (kCoeff u · w) d`. Hence `μ̂(kw) = μ̂(w)` and
`φ(kw) = φ(w)` for `k = kCoeff u`, `u : K`. (Identify `K` with its image in `E`; `kCoeff` is
injective.)

**(F2) Translation formula and triangle inequality.** `eval a − eval b = eval b · (eval (a−b) − 1)`
and `|eval b| = 1`, so `‖eval a − eval b‖₂ = φ(a − b)`. Also
`|eval(u₁+u₂) − 1| ≤ |eval u₁ − 1| + |eval u₂ − 1|` pointwise (since `|eval u₂| = 1`), hence
`φ(u₁+u₂) ≤ φ(u₁) + φ(u₂)`.

**(F3) Every algebraic number is a finite sum of unit-modulus algebraic numbers.** Let `u ∈ E`,
`u ≠ 0`, `N ∈ ℕ` with `|u|/N ≤ 1`. Then `cos θ := |u|/(2N) ∈ [−1,1] ∩ E` and
`sin θ := √(1 − cos²θ) ∈ E`, so `k₁ := e^{iθ} = cos θ + i sin θ ∈ E` with `|k₁| = 1`, i.e.
`k₁ ∈ K`; likewise `k₂ := k₁⁻¹ = e^{−iθ} ∈ K`; and `u/|u| ∈ K` because
`|u/|u|| = 1` and `u/|u| ∈ E` (`|u|^2 = u·conj u ∈ E`). Then
`u = N · (u/N) = N · (u/|u|) · (|u|/N) = N·(u/|u|)·(k₁ + k₂)`, a sum of the `2N` elements
`(u/|u|)k₁, (u/|u|)k₂` of `K`, each repeated `N` times. (`0 = k + (−k)`.)

## 2. The theorem

> **(N)** Let `μ` be a probability measure on `D` with `IsWild μ`. Then for every `z ∈ E`,
> `z ≠ 0`, the `K`-orbit of `eval z` in `L²(μ)` is **not** precompact.
>
> Consequently `A := {f ∈ L²(μ) : the K-orbit of f is precompact}` is a proper closed subspace
> of `L²(μ)`, so the maximal compact extension `Y*` of the point factor (defined by
> `L²(Y*) =` the largest factor-subspace contained in `A`) is a **proper** factor, and therefore
> `id : D → D` is not `Y*`-measurable — which is exactly hypothesis (H2) of Theorem A at `Y*`.

*Proof.* Suppose `z ≠ 0` and the orbit `{eval(k^{-1}z) : k ∈ K}` is precompact. Fix `ε > 0`.
By total boundedness there is a **finite** `F ⊆ K` with
`∀ k ∈ K, ∃ k' ∈ F : φ((k − k')z) < ε`. (Take a finite `ε`-net of the orbit inside the orbit,
using (F2) for the last step.) Since `K` is infinite, choose `k'' ∈ K ∖ F`; then
`w := k'' − k' ≠ 0` for the `k' ∈ F` supplied by the net property, and `φ(w z) < ε`.

By (F1), `φ(k w z) < ε` for **every** `k ∈ K`. Let `v ∈ E`. By (F3), `v = Σ_{i≤L} k_i` with
`k_i ∈ K`, so by (F2)
`φ(v w z) = φ(Σ_i k_i w z) ≤ Σ_i φ(k_i w z) ≤ L ε`.
Hence `π̂(v w z) ≥ 1 − (Lε)²/2` for every `ε > 0`, so `μ̂(v w z) = 1`.

Now `w z ≠ 0`, so as `v` runs over `E`, `v w z` runs over all of `E` (multiplication by the
nonzero algebraic number `wz` is a bijection of the field `E`). Therefore `μ̂(y) = 1` for every
`y ∈ E`. Since `|eval y| = 1`, `μ̂(y) = 1 = ∫ Re(eval y)` forces `eval y = 1` `μ`-a.e.; as the
characters separate points of `D`, `d = 1` `μ`-a.e., i.e. `μ = δ_1`. But `1 ∈ C` (§0), so
`μ(C) = 1`, contradicting `IsWild μ`. ∎

## 3. Why `A` is proper and `Y*` is a proper factor

`A` is a closed subspace of `L²(μ)` (a limit of vectors with precompact orbit has precompact
orbit), contains `1`, is closed under conjugation, and is invariant under the `K`-action. `(N)`
says `eval z ∉ A` for `z ≠ 0` while `eval z ∈ L²(μ)`, so `A ⊊ L²(μ)`.

For the factor structure: `A ∩ L^∞(μ)` is a `*`-subalgebra of `L^∞(μ)` closed under bounded
monotone limits (the `L²`-closure of `A` gives monotone closure because bounded monotone
convergence holds in `L²`), hence `A ∩ L^∞ = L^∞(Y*)` for a factor `Y*`; and it is a module over
itself (`kh`, `kf` both ranging over precompact families forces `(kh)(kf)` to range over a
precompact family), so `L²(Y*) ⊆ A`. Every `Y` with `L²(Y) ⊆ A` satisfies
`L^∞(Y) ⊆ A ∩ L^∞ = L^∞(Y*)`, hence `L²(Y) ⊆ L²(Y*)`: **`Y*` is the maximum of that class**, no
Zorn needed. Finally `L²(Y*) ⊆ A ⊊ L²(μ)` gives `Y* ≠ X`; since `σ(id) = Borel(D)` is the full
`σ`-algebra and `σ(Y*) ⊊ σ(id)`, `id` is not `Y*`-measurable. ∎

## 4. What this buys, and what is still owed

With (N), the R1/R3/R6 programme is unblocked, because the two things f4 listed as missing are
now supplied: (H2) at the maximal compact extension is §2, and it is the *only* extra input
Theorem A needs at `Y*`, whose relative square is ergodic by maximality plus transitivity of
compactness. The remaining obligations are the two structural ones, both elementary and both
measured in `COSTS.md` §5 and finding f30:

* the standard compact-extension predicate (orbit totally bounded modulo `L²(base)`), because
  the tree's `Compact`/`Scalar` predicate is not closed under composition;
* join-closure along `ChainJoin.code` (from `ChainJoin.approximation` +
  `LimitDensity.generated_factor_approximation`, ~100 lines) and transitivity (~40 lines).

Nothing in §2 uses ergodicity of `μ`; it uses only `K`-invariance, `μ(D) = 1`, `μ(C) = 0`, and
`K` = all unit-modulus algebraic numbers (in particular (F3), which fails for any proper
subgroup of `K`, so the argument is sharp: it is exactly the `K ⊆ ⅅ` structure of Basic.lean:11
that makes it work).
