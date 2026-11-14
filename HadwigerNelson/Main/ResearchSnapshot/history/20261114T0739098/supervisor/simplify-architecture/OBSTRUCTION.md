> **REVISION (block 4) — read Secs.6–8 first.** Astra's review supplied Lemma A (Sec.6), which kills the
> coset branch of Sec.3 outright and corrects three of my statements; Sec.4's option (A) remains the open
> target but in the corrected form M3, and Sec.4's option (B) is withdrawn as insufficient. Secs.1–3 stand
> as the record of the tested route, with the specific corrections marked in Sec.7. Nothing is deleted.

# Self-contained packet: the exact missing hypothesis (M‴) and the first attempted route

Block 3. For review by Astra. All statements below are either [read] from the paper/Lean or
[proved here] (paper-level, complete proofs given, nothing machine-checked in this block). No Lean
run, no search.

## 1. The paper's system, exactly as assumed

`F = ℚ̄ ∩ ℝ`, `E = F(i)` regarded as a **discrete** additive abelian group (countable),
`K = {u ∈ E : u ū = 1}` (multiplicative, countable, divisible: every `u` has an `n`-th root in `K`),
`D = Ê` (compact metrizable character group). Notation: `(ad)(z) = d(az)`, `ψ_z(d) = d(z)`,
`C = j(ℝ²)` where `j(ξ)(z) = exp(i·ξ·z)` (real inner product of coordinates). Facts used: `j` is
continuous and injective; `0 ∈ C`, i.e. the trivial character `1_D ∈ C`; the characters
`{ψ_z}_{z∈E}` are an orthonormal basis of `L²(m_D)`; `a·ψ_z = ψ_{az}`.

Hypotheses of the paper's §3.3 [read, p.17]: `µ` is a Borel probability on `D` that is
**(i)** `K`-invariant, **(ii)** ergodic for the `K`-action, **(iii)** wild: `µ(C) = 0`.
(`µ` is *not* assumed to be Haar; Theorem 2.3, proven in §3, is that wild `⇒ µ = m_D`.)

## 2. The exact statement that the "replace §2.4" simplification needs

Let `R = D ×_Y D` be the relative product over a factor `Y` of `(D,µ)`.

**(M)** The terminal factor `Y_η` of the paper's compact tower (Lemma 3.1) applied to `(D,µ)` is
proper: `Y_η ≠ D`. Equivalently, `id_D` is not `Y_η`-measurable.

**(H2)** The hypothesis of Theorem A′ at that factor: `id_D` is not `Y_η`-measurable.
`(M) ⟺ (H2)`: the factor map of `D` is `id_D`, so `id_D` is `Y`-measurable iff `Y = D`.

**(M‴)** `µ × µ` is ergodic under the diagonal `K`-action on `D × D` — i.e. `(D,µ)` is **weakly
mixing**. Given (M‴) the *trivial* factor suffices: (H1) holds, and `C`-nullity of the conditional
difference law is free (paper Lemma 2.4 = Lean `wild_independent_difference`, machine-checked), so
§2.4, §3.1 and Theorem A′ are all unnecessary. `(M‴) ⇒ (M)`; `(M‴)` is the sharpest sufficient
hypothesis for the simplification, and the one worth testing.

Why this is the whole content: the tower exists exactly to *produce* a factor with an ergodic
relative product, because (M‴) is not known. Nothing below assumes a defect in the paper; the
question is only whether `(M‴)` is cheaper than what §2.4 spends.

## 3. Route tested: point spectrum, and the coset trap

**Lemma 3.1 [proved here].** If `(D,µ)` has a non-constant `f ∈ L²(µ)` with `U_u f = χ(u)f`,
`|χ(u)| = 1` for all `u ∈ K`, then `µ × µ` is **not** ergodic under the diagonal action; hence `(M‴)`
fails.
*Proof.* `F(x,y) = f(x)\overline{f(y)}` is measurable, `|F| = 1`, `F ≠ const` (else `f` is a.e.
constant), and `F(u·x, u·y) = χ(u)f(x)\overline{χ(u)f(y)} = F(x,y)`: a non-constant invariant
function. ∎
So `(M‴)` forces trivial point spectrum. Contrapositive is a *test*, not a proof: to use it one must
exhibit an eigenfunction of `(D,µ)`, and I could not — nor exclude one (§4).

**Trap (recorded because it is seductive and wrong) [proved here].** The natural candidate
`ψ_z(x)\overline{ψ_z(y)}` is **not** diagonal-invariant: `(u·ψ_z)(x)\overline{(u·ψ_z)(y)} =
ψ_{uz}(x)\overline{ψ_{uz}(y)}`. The reason is structural: `π(x,y) = xy^{-1}` is *equivariant*
(`π(u·(x,y)) = u·π(x,y)`), not invariant, so the "difference character" is a function on the
quotient by the diagonal, not an invariant of the diagonal action. Any argument that extracts
`|µ̂(z)| ∈ {0,1}` from an invariant "difference character" is invalid.

**Lemma 3.2 [proved here].** For `z ≠ 0` and any probability `µ`, `|µ̂(z)| = 1` iff `ψ_z` is `µ`-a.e.
constant, iff `µ` is carried by a **coset of the annihilator** `H_z = {d : d(z) = 1}` (a proper
closed, hence `m_D`-null, subgroup).
*Proof.* Cauchy–Schwarz equality case for `|∫ψ_z dµ| = 1 = ∫|ψ_z| dµ`; then `µ(d(z) = ξ) = 1`, i.e.
`µ(aH_z) = 1` for the coset `a` with `a(z) = ξ`. ∎

**Consequence — the failure point of this route [proved here].** Lemma 3.2 shows `|µ̂(z)| = 1` is a
*support* condition, not an eigenfunction; and wildness plus ergodicity do **not** exclude it by any
argument I have: inside a coset `aH_z`, the wild set is `C ∩ aH_z = {j(ξ) : ξ·z = (value fixed by a)}`,
a one-real-parameter family (an affine line in the `ξ`-plane), so a `K`-invariant ergodic `µ` carried
by `aH_z` can still satisfy `µ(C) = 0` as far as this computation shows. Ergodicity constrains only
the induced action of `K` on the coset space `D/H_z ≅ 𝕋`. **So the point-spectrum/support route does
not reach `(M‴)`.** The route dies at exactly this point, and not at a missing estimate.

## 4. What is therefore still open, stated sharply

Either of the following settles the simplification; neither is in the literature I checked nor in
the repository:

* **(A)** Prove `(M‴)`: for `K`-invariant ergodic `µ` on `D` with `µ(C) = 0`, `µ × µ` is ergodic.
  The point-spectrum route is closed (§3); the remaining content is the mean-square decay
  `Avgu∈Φ |µ̂(uz−z)|² → 0` for all `z`, i.e. Fourier decay along `K`-orbits — which is what the
  paper's §3 obtains as its byproduct. A proof of (A) *by a route independent of §2.4* would delete
  §2.4+§3.1 outright; a proof that reuses §3 is circular and gives nothing.
* **(B)** Prove `(M)` directly for the paper's own tower: exhibit the first stage `Y_1` of the tower
  for `(D,µ)` and show it is proper. (A generic skew shift reaching the top — my block-2
  Counterexample 2 — says nothing about `(D,µ)`; it only refutes the general propagation `P3`.)

If neither is available, the honest ledger entry is: *Theorem A′ is a correct, machine-checked
theorem whose hypothesis (H2) coincides with the paper's own open bookkeeping step; therefore it
does **not** shorten the paper's proof, and the projected paper-level saving of §2.4 is
conditional on (A) or (B), not established.*

## 5. Corollaries of this block already banked

* **(M‴)** is strictly stronger than (M): (A) implies the trivial factor works, no tower needed.
* The Lean consumer `ergodic_wild_fourier` (`Analysis/PlaneSpectrum/Ergodicity.lean:52`) carries
  `[ErgodicVAdd Rot (D×D) (RelativeProduct.law µ q hq)]` as an *instance* for the factor `q` it
  obtains from `exists_terminal_factor`; under (A) that instance is trivial to discharge at the
  constant factor, which is precisely the deliverable to aim at.
* Block 2's negative results stand and are unaffected: `(2.6)`-compactness is not transitive
  (skew shift), and the paper's tower can terminate at the top in a generic system. Neither refutes
  the paper's specialised `(D,µ)` system, and neither is used as if it did.

## 6. Lemma A [Astra; verified here] — the coset branch is dead

For **any** `K`-invariant probability `µ` on `D` (ergodicity not needed) and `z ≠ 0`: `|a_z| = 1`
implies `a_z = 1` and `µ = δ_{1_D}`. Hence a wild `µ` has `|a_z| < 1` for every `z ≠ 0`.

Ingredients, each verified: `span_ℤ K = E` (`t = n(u+v)` with `u = t/2n + i√(1−(t/2n)²) ∈ K` for real
algebraic `t`, `|t| ≤ 2n`); Cauchy–Schwarz equality gives `ψ_z ≡ c`; `K`-countability gives one conull
set for all `ψ_{uz}`; the constants assemble into a homomorphism `c : E → 𝕋`, so `µ = δ_{d_0}`; then
`K`-invariance makes `d_0` kill `(K−1)E`, and `(r−1)+(s−1) = −1` for `r = (1+i√3)/2`, `s = r̄` together
with `E = span_ℤ K` forces `d_0 ≡ 1`. Full proof: `AUDIT.md` §9.

**Consequence for this packet:** the counterexample sought in §3/§4 cannot exist. A `µ` carried by a
coset of `ann(z)` with `µ(C) = 0` would have `|a_z| = 1`, hence `µ = δ_{1_D}`, hence `µ(C) = 1`.
The branch is closed, and no search was continued.

## 7. Superseded statements (exact list)

| block-3 statement | status |
|---|---|
| "`µ` on a coset of `ann(z)` with `µ(C)=0` is not excluded; the point-spectrum route dies at a one-parameter family of lines" | **refuted** by Lemma A. Route closed, not merely stalled |
| "ergodicity constrains only the induced action of `K` on `D/H_z ≅ 𝕋`" | **withdrawn**: `u·ann(z) = ann(uz)`, so `H_z` is not `K`-stable and no quotient action exists |
| "`C ∩ (a·ann(z))` is an affine line" | **corrected**: countably many parallel affine lines (`ξ·(Re z, Im z) = θ_0 + 2πk`) |
| next step "(M‴) via `Avg_u |µ̂(uz−z)|² → 0`" | **withdrawn**: this is the uncentered quantity; it tends to `|a_z|⁴`, and equals 1 at `z = 0` |
| next step option (B) "compute the first tower stage and decide properness" | **insufficient**: stages increase, so first-stage properness does not give terminal properness |
| `(M‴)` treated as a hypothesis distinct from diagonal ergodicity | **corrected**: `(M‴) = M3` = weak mixing = diagonal ergodicity of `µ⊗µ` |

## 8. The corrected target, and the one uniformity gap that remains

**(M3)** [Astra; checked here]: for all `z, w ∈ E`, `avg_{u∈Φ_n}|a_{uz−w} − a_z\overline{a_w}|² → 0`
along a fixed finite Følner sequence in `K`, no uniformity over frequencies; with `h_z = ψ_z − a_z`,
`⟨U_u h_z, h_w⟩ = a_{uz−w} − a_z\bar a_w` because `a_{uz} = a_z`. Trivial for `z = 0` or `w = 0`.

**[proved here] M3 ⇒ `µ⊗µ` ergodic**, by finite-character approximation alone (Stone–Weierstrass
density, M3 at finitely many pairs, no Haar, no tower): see `AUDIT.md` §11 for the computation.
So `M3 = (M‴)` and the analytic criterion is *sufficient*; the remaining work is proving M3.

**The obstruction, stated exactly.** Suppose `F` is a nonconstant invariant function and
`G = Σ_z ψ_z⊗f_z` a finite character approximant. Then
`‖U_{u⊗u}G − G‖² = 2‖G‖² − 2Re Σ_{z,z'} a_{z−u^{-1}z'}⟨f_{z'},f_z⟩`, and invariance forces the real part
`≥ ‖G‖² − 2η²` **for every `u`**. A contradiction needs a *uniform* deficit

> **(U)** for every finite `Z` and `δ_0 > 0`, there are `δ > 0` and `D ⊆ K` of upper Banach density 1
> with `|a_{z−u^{-1}z'}| ≤ 1 − δ` for all `u ∈ D`, `z ≠ z' ∈ Z`.

Lemma A gives only `|a_{z−u^{-1}z'}| < 1` for each fixed `u` — a statement about *values* of `a` at
frequencies — while (U) is a statement about *limits of `a` along `K`-orbits of frequencies*, uniformly
over an unbounded range of frequencies. At the pair `z = u^{-1}z'` the coefficient is exactly `a_0 = 1`,
so no strictness exists there at all. `(U) ⇒ M3` strictly, so a proof of (U) would be stronger than the
paper's own §3: this is a correct reduction, not a shortcut, and the uniformity gap — not any defect in
Lemma A — is the surviving obstacle.

**Correct scope of the eigenfunction target** [proved here, witness in `AUDIT.md` §11]: constant-modulus
joint eigenfunctions with a nontrivial unimodular eigenvalue do *not* obstruct diagonal ergodicity
(`ℤ` acting on `𝕋²` by `(R_α,R_β)`, `1,α,β` `ℚ`-independent: ergodic, yet `ψ_1⊗ψ_1` has eigenvalue
`e^{2πi(α+β)}`). The target must be restricted to nonconstant *invariant* functions — equivalently
nonconstant eigenfunctions of non-constant modulus, or of eigenvalue `1`.
