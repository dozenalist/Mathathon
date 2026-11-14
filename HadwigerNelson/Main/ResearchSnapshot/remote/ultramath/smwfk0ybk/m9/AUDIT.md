# d13 — Step 2, statement audit of the measurability removal

Swarm `smwfk0ybk`, member m9. Object: the **statement** of the transfer
(paper Thm 1.3 / Prop 4.2 + Lemma 4.3), not its proofs and not the k = 6 CSP.
Question registered: *is the transfer non-vacuous, and what is the indispensable
step?*

Everything below cites the paper
`attachments/here-are-three-files-ni5n/paper.pdf`; displayed formulas were
re-read against `pdftotext -bbox` word boxes (see §7), not against the plain
extraction.

---

## 0. Findings

1. **Definition 1.2 is not vacuous and not automatic.** It sits *strictly*
   between "measurable" and "measurable and exactly proper" (Lemmas 1.4, 1.5).
   It is satisfiable: the hexagonal 7-colouring is one, and its properness is
   certified in exact arithmetic in `work/hex7.py` (Prop 2.1). It is not
   implied by measurability (Lemma 1.5). So "no weak measurable 5/6-colouring"
   is a meaningful statement and the transfer has content.
2. **The heavy analysis of Step 2 is contained in exactly one statement**,
   the paper's Theorem 2.3 (Haar rigidity of wild character laws). §4's proof
   of Prop 4.2 is otherwise elementary: one Følner average, one spectral
   projection (Lemma 4.1), one sampling/Tonelli step (§3.1). In particular the
   Furstenberg–Zimmer tower is *entirely inside* Theorem 2.3, and Theorem 2.3
   is **colouring-blind**: it is a statement about K-invariant probabilities on
   the character group of the algebraic plane. Auditing §3 further (§10), the
   tower is needed only to produce a factor `Y` over which the relative product
   is ergodic **and** the conditional difference law stays wild — requirement
   (W). Everything else in §3 is elementary and I checked it.
3. **The exact input §4 needs is weaker than Theorem 2.3.** The two cross terms
   in (4.1) vanish automatically (Lemma 3.1), so (4.1) passes to the
   projection iff the *remainder* has zero correlation at algebraic **unit**
   translations. Call that (R). Theorem 2.3 ⟹ (R) ⟹ Prop 4.2, and (R) is
   strictly less than "the spectral measure is a multiple of Haar". (R) is the
   sharpened target for any shortening of Step 2.
4. **Theorem 2.3 is sharp in its arithmetic hypothesis.** With K replaced by
   its torsion subgroup μ_∞ (roots of unity — still divisible, so the paper's
   own divisibility remark no longer suffices) the conclusion is **false**
   (Theorem 6.3); likewise for the unit circle of every number field
   (Remark 6.4). With the full unit circle it survives the whole class of
   "homogeneous" counterexamples (Lemma 6.1: the only K-invariant subgroups of
   E are {0} and E). So no argument can replace the tower's arithmetic input by
   root-of-unity symmetry, divisibility, or the units of a number field.
5. Two natural shortcuts are **dead**, with reasons recorded in §8: the
   "Steinhaus/Falconer ⟹ the notion is unsatisfiable" route (false premise),
   and the p-adic closed-subgroup counterexample to Theorem 2.3 (dies by
   divisibility of E).
6. **Relevance after d1's verdict.** d1 found the tightened interface CSP SAT at
   every `(l, geometry)` at `k = 6` (models with all `|P_i| ≤ 2`), so Step 1
   does not reach `χ ≥ 7` and Step 2 is the live line. This audit certifies that
   the Step 2 statement is not vacuous, that its cost is one named statement,
   and which weakening of that statement (namely (R) / (W)) is the right target.

Nothing here shortens the transfer, and nothing here touches §5–§8. §9 states
exactly what is and is not established, and what the mission still needs.

---

## 1. The notion, exactly

**Definition 1.2 (paper).** `c : R² → {1,…,k}` is Lebesgue measurable with
classes `A_i = c^{-1}({i})`, and for every `R > 0`

  `Σ_i ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0`,

`σ` = normalized arc length on `S¹`.

**Lemma 1.1 (pointwise form).** For a measurable `c`,
Definition 1.2 holds **iff** for a.e. `x ∈ R²`

  `σ{u ∈ S¹ : c(x+u) = c(x)} = 0`.                                     (1.1)

*Proof.* Put `g(x) = σ{u : c(x+u) = c(x)} = Σ_i ∫_{S¹} 1_{A_i}(x)1_{A_i}(x+u)dσ(u)`.
Each summand is jointly measurable in `(x,u)`, so `g` is measurable and
nonnegative (Tonelli), and the condition of Definition 1.2 is
`∫_{B(0,R)} g = 0` for every `R`, i.e. `g = 0` a.e. ∎

So the notion is precisely: *measurable, and at a.e. point almost every
direction of the unit circle has a different colour* (not: *no* direction —
that is exact properness).

**Lemma 1.2 (null sets).** Definition 1.2 is unchanged by modifying `c` on a
plane-null set. (Paper, after Def 1.2.) *Proof.* If `c' = c` off a null `N`,
the symmetric difference of the two pair sets lies in
`{(x,u) : x ∈ N} ∪ {(x,u) : x+u ∈ N}`, which is `dx dσ(u)`-null by Fubini and
translation invariance of Lebesgue measure for fixed `u`. ∎

**Lemma 1.3 (monotonicity in k).** If a weak measurable k-colouring exists,
then a weak measurable k'-colouring exists for every `k' > k`.
*Proof.* Split one class into two measurable parts: `A = A' ⊔ A''`. For all
`(x,u)`, `1_{A'}(x)1_{A'}(x+u) + 1_{A''}(x)1_{A''}(x+u) ≤ 1_A(x)1_A(x+u)`,
since the right side expands into four nonnegative terms. The sum over classes
therefore does not increase, and stays 0. Iterate. ∎

Consequence used by the mission: "no weak measurable 6-colouring" is at least
as strong as the paper's Theorem 1.4 ("no weak measurable 5-colouring"), so
Step 1's target is a strict strengthening of the published theorem.

**Lemma 1.4 (strictness, upper side).** Definition 1.2 does **not** imply
exact properness. *Proof.* Take the verified 7-colouring of §2, pick a unit
pair `(y, y+u)`, and recolour the single point `y+u` with the colour of `y`.
The change is on a null set, so Lemma 1.2 keeps weak measurability, and the
colour has a monochromatic unit pair. ∎

**Lemma 1.5 (strictness, lower side).** Measurability does **not** imply
Definition 1.2. *Proof.* `k = 2`, `A_1 = {x : 0 ≤ Re x ≤ 1, 0 ≤ Im x < 2}`,
`A_2 = A_1^c`. Both measurable. The set
`{(x,u) : x ∈ A_1, x+u ∈ A_1, |u| = 1}` contains
`{0 ≤ Re x ≤ 1, 0 ≤ Im x ≤ 1} × {u = (cos θ, sin θ) : |θ| ≤ 1/2}`
(for such `x,u`, `Im(x+u) ∈ [-1/2, 3/2] ⊂ [0,2)`), whose `dx dσ(u)`-measure is
`1 · (1/(2π))·1 > 0`. So `Σ_i ∫∫ 1_{A_i}1_{A_i} > 0`. ∎

**Corollary 1.6.** The class of weak measurable k-colourings is strictly
contained in the class of measurable k-colourings and strictly contains the
class of measurable proper k-colourings. In particular the transfer's
conclusion is a genuine relaxation of "measurable and proper", and its
hypothesis class contains colourings with no measurability at all: the
transfer's content is exactly that measurability can be produced from a proper
colouring whose classes are arbitrary, while the *exact* exclusion
`c(x) = c(y) ⇒ |x-y| ≠ 1` may be relaxed to the product-null version.

---

## 2. Non-vacuity, certified: a weak measurable 7-colouring

The paper's upper bound (Hadwiger's hexagonal construction) is not merely a
proper colouring; with a Borel boundary rule it is a *measurable* proper
colouring, hence a weak measurable one by Lemma 1.2/Corollary 1.6. Its
properness rests on three numerical facts, which `work/hex7.py` decides in
exact arithmetic. Since the plain text extraction of the paper drops radicals,
the constants were re-read from word boxes (§7): **the circumradius is `r = 2/5`**
(not `√(2/5)`), the nearest-neighbour distance is `√3 r`, and the two
separations are `2r < 1` and `(√21 - 2) r > 1`.

**Proposition 2.1.** Let `ω = e^{2πi/3}`, `L = Z[ω]`, `α = 2 - ω`,
`d = √3 r` with `r = 2/5`, and `Λ = d·L`. Let `Λ' = α·Λ` and colour
`x ∈ R²` by the class of `Λ'` in `Λ` of the centre of the lexicographically
first closed Voronoi hexagon of `Λ` containing `x`. Then the colouring is
Borel, 7-valued, and no two points at distance exactly 1 have the same colour.

*Certificate* (`work/hex7.py`, all exact):
* (H1) `N(m+nω) = m² - mn + n² ≥ 1` for `(m,n) ≠ (0,0)`: if `n ≠ 0` then
  `4N = (2m-n)² + 3n² ≥ 3` and `N` is an integer; if `n = 0` then `N = m²`.
* (H2) `α·1 = 2 - ω → (2,-1)`, `α·ω = 1 + 3ω → (1,3)`, determinant
  `2·3 - (-1)·1 = 7`, so `[L : αL] = 7`; the class map is
  `(m,n) ↦ m + 2n mod 7`, verified to vanish on both generators and to take
  exactly 7 values.
* (H3) `N(α) = 4 - 2(ω+ω̄) + 1 = 7` using `ω + ω̄ = -1`. Hence
  `min{|λ| : 0 ≠ λ ∈ αL} = √7 · min{|μ| : 0 ≠ μ ∈ L} = √7` in lattice units.
* (H4) the Voronoi hexagon of `L` has circumradius `1/√3` in lattice units:
  the six deep holes `(2,1)/3, (-1,1)/3, (-1,-2)/3, (-2,-1)/3, (1,-1)/3, (1,2)/3`
  all satisfy `N = 1/3`, so in plane units the circumradius is
  `d/√3 = r`, and the diameter is `2r = 4/5 < 1`.
* (H5) two points of `Λ` of the same colour are `≥ √7 d = (2/5)√21` apart.
  Subtracting the two circumradii,
  `(√21 - 2)·(2/5) > 1 ⟺ √21 > 9/2 ⟺ 21 > 81/4 ⟺ 336/25 > 81/25`,
  which is what the script decides (both sides of `√21·(2r) > 1 + 2r`
  squared, `2r = 4/5`).

Hence two same-coloured points either lie in one hexagon (`|x-y| ≤ 2r < 1`) or
in distinct same-coloured hexagons (`|x-y| ≥ (√21-2)r > 1`). The colouring is
Borel because each colour class is a finite union of closed convex cells with a
Borel tie-break on boundaries. ∎

With Lemma 1.2 this is a weak measurable 7-colouring, and with Lemma 1.3,
weak measurable k-colourings exist for every `k ≥ 7`. Together with the
paper's Theorem 1.4 (none for `k ≤ 5`) this pins the threshold at 6 or 7 —
i.e. Definition 1.2 discriminates exactly at the value the mission needs.

---

## 3. Dependency audit of Proposition 4.2

Prop 4.2 (proper ⟹ weak measurable) is used by §1 as a *black box* and by the
mission as the contrapositive: no weak measurable 6-colouring ⟹ no proper
6-colouring ⟹ `χ(R²) ≥ 7`. Its proof has exactly four inputs.

**3.1 The four inputs.**

| # | input | where used | weight |
|---|---|---|---|
| I1 | amenability of the countable group of plane isometries preserving `E` | Følner average of a point mass gives an invariant Borel `µ` on `Ω` = proper labelings of `E` | classical |
| I2 | Lemma 4.1: `H_c = {v : lim_{E∋z→0} ‖T_z v - v‖ = 0}` is `L²` of a factor, projection = conditional expectation, positivity, extension of `T_x` to `R²` strongly continuously, rotation invariance | `p^i = E(f^i | F_c)`, `b^i = f^i - p^i`, extension of (4.2) from algebraic to all unit `u` | abelian spectral theorem + Bochner |
| I3 | **Theorem 2.3** (Haar rigidity): every K-invariant probability on `D` with `ν(C) = 0` is Haar | `λ_{b^i} = c·m_D` ⟹ `⟨b^i, T_z b^i⟩ = 0` for `z ≠ 0` | **Furstenberg–Zimmer tower, §§2–3** |
| I4 | measurable sampling + Tonelli | jointly measurable field `H_i(x,ω)`, one good sample, least positive index | elementary |

I1–I2 and I4 are self-contained given the classical theorems they cite; the
19 Lean modules live over I3.

*Small observation on I1.* The label indicators are rotation-fixed for **every**
labelling, and the `K`-invariance of `λ_{b^i}` follows from covariance and
`V_u f^i = f^i` alone. So the averaging needs amenability of `E` only; `K`'s
amenability is used to make `µ` isometry-invariant, which no step of §4
appears to consume. (Recorded as an observation, not used below.)

**3.2 The exact input, weakened.** (4.1) says `∫ f^i T_u f^i dµ = 0` for
`u ∈ K` (it holds pointwise for every proper labelling). The proof must pass
it to `p^i`.

**Lemma 3.1 (cross terms vanish for free).** `⟨p^i, T_u b^i⟩ = ⟨T_{-u} p^i, b^i⟩ = 0`
and `⟨b^i, T_u p^i⟩ = 0`, for **every** `u ∈ E`, because `H_c` is translation
invariant and `b^i ⊥ H_c`.

*Proof.* `p^i ∈ H_c`; `H_c` is `T`-invariant (Lemma 4.1), so `T_{-u}p^i ∈ H_c ⟂ b^i`. ∎

**Corollary 3.2.** In the setting of Prop 4.2, for every `u ∈ K`,
`∫ p^i T_u p^i dµ = - ∫ b^i T_u b^i dµ`.

So the whole analytic burden is the vanishing of the **remainder's**
autocorrelation at algebraic **units**:

  **(R)** Let a standard probability space carry a pmp `E`-action with
  `K`-covariance `V_u T_z V_u^{-1} = T_{uz}`. Let `v ∈ L²` be rotation-fixed
  with spectral measure `λ_v(C) = 0`. Then `⟨v, T_u v⟩ = 0` for every `u ∈ K`.

**Proposition 3.3.** Theorem 2.3 ⟹ (R) ⟹ Prop 4.2. Moreover (R) is strictly
weaker than the conclusion of Theorem 2.3: 2.3 identifies the whole measure
`λ_v` as a multiple of Haar and hence gives vanishing at *every* nonzero
translation and for *every* spectral measure; (R) asks only for the value of
one autocorrelation, only at radius 1 (algebraically: only at the units).

*Proof of the first arrow.* `V_u v = v` and covariance give, for all `z`,
`⟨v,T_{uz}v⟩ = ⟨V_uv, V_uT_zv⟩ = ⟨v, T_zv⟩`, so `λ_v` is K-invariant; with
`λ_v(C) = 0` Theorem 2.3 gives `λ_v = c·m_D`, and
`⟨v,T_uv⟩ = ∫ψ_u dc·m_D = c·0` for `u ≠ 0` (Haar Fourier coefficients vanish
off 0). The second arrow is Corollary 3.2 plus the density of algebraic units
in `S¹` with strong continuity (Lemma 4.1). ∎

**Consequence for Step 2.** Any shorter proof of the transfer that keeps §4's
skeleton must prove (R) — not the full rigidity. (R) is the named target; the
tower is one route to it and is *not* used anywhere else in §4.

---

## 4. Sharpness of the named step

Theorem 2.3 is not a formal consequence of "K-invariant + wild". §6 exhibits an
explicit counterexample once `K` is replaced by the roots of unity — a change
that preserves divisibility, so the paper's own remark that `K` is divisible
(the mechanism of Lemma 2.4) does not suffice. Conversely Lemma 6.1 shows that
with the full algebraic unit circle the *homogeneous* class of candidates
(Haar measures of closed subgroups) is empty. Both are short and exact; they
delimit what a tower-free replacement may use.

---

## 5. The reference group structure (used in §6)

`F = Q̄ ∩ R` (real algebraic numbers), `E = F(i) = Q̄`, `K = {u ∈ Q̄ : |u| = 1}`
(algebraic unit circle), `D = Hom(E, T)` compact, `C = j(R²)` the ordinary
continuous characters, `K` acting by `(ud)(z) = d(uz)`.

Facts: `E` is **divisible** (a `Q`-vector space of countable dimension);
`K` is divisible and its torsion subgroup is exactly μ_∞ (so `K/μ_∞` is a
`Q`-vector space, containing the classes of units of infinite order);
`C ≅ R²` as a Borel subgroup; `C` is not closed in `D`.

---

## 6. Sharpness results

**Lemma 6.1 (the only K-invariant subgroups of E are {0} and E).**

*Step 1.* Every `λ ∈ Q̄` with `|λ| ≤ 2` is a sum of two elements of `K`.
Indeed the circles `|z| = 1` and `|z - λ| = 1` meet (their centre distance is
`|λ| ≤ 2`); an intersection point `z` satisfies `z z̄ = 1` and
`λ z̄ + λ̄ z = |λ|²`, so `z` solves the quadratic `λ̄ z² - |λ|² z + λ = 0` over
`Q̄`; and `Q̄` is algebraically closed. Then `z ∈ K` and `λ - z ∈ K`.

*Step 2.* Let `L ≤ E` be K-invariant and `0 ≠ w ∈ L`. For any `λ ∈ Q̄`,
write `λ = λ₁ + … + λ_n` with `|λᵢ| ≤ 2` (take `n = ⌈|λ|/2⌉`, all `λᵢ = λ/n`).
Then `λᵢ w = (u + u') w = uw + u'w ∈ L` by Step 1 and K-invariance, so
`λ w ∈ L`, and `L ⊇ Q̄·w = E`. ∎

**Corollary 6.2.** There is no closed subgroup `H ⊆ D` with `H ≠ {0}` and
`H ≠ D` that is K-invariant and has `H ∩ C` `Haar_H`-null. *Proof.* Write
`H = L^⊥` with `L = H^⊥`, a closed subgroup of the discrete group `E`.
`H` is K-invariant iff `L = uL` for all `u ∈ K` (as `(uH)^⊥ = u^{-1}L`), and
`H ≠ {0} ⟺ L ≠ E`, `H ≠ D ⟺ L ≠ {0}`. By Lemma 6.1 a K-invariant `L` is `{0}`
or `E`, so `H` is `D` or `{0}`; and `H = {0}` is not wild, since
`δ_0(C) = 1`. ∎
So the class "homogeneous wild K-invariant measures" is empty and cannot
threaten Theorem 2.3.

**Theorem 6.3 (root-of-unity rigidity fails).** Let `μ_∞ ⊂ E` be the group of
roots of unity and let it act on `D` by the same formula. Let
`L = span_Z(μ_∞) = {z₁ + … + z_n : zᵢ ∈ μ_∞}` and `H = L^⊥ = {d : d(ℓ) = 1 ∀ℓ ∈ L}`.
Then

1. `L ⊊ E`, since every element of `L` is an algebraic integer while `1/3` is
   not. Hence `H ≠ {0}` (else `L = L^{⊥⊥} = {0}^⊥ = E`) and `H ≠ D` (as
   `L ≠ {0}`, `1 ∈ L`).
2. `H` is closed and `μ_∞`-invariant: `(ud)(ℓ) = d(uℓ) = 1` for `u, ℓ` roots of
   unity.
3. `ν := Haar_H` satisfies `ν(C) = 0`. Indeed
   `C ∩ H = {j(ξ) : ⟨ξ, ζ⟩ ∈ 2πZ ∀ ζ ∈ μ_∞}`; using `ζ = 1, i, e^{iπ/3}` gives
   `ξ₁ ∈ 2πZ`, `ξ₂ ∈ 2πZ`, `ξ₁ + √3 ξ₂ ∈ 4πZ`, hence `ξ₂ = 0` and `ξ₁ ∈ 4πZ`:
   a countable set, so `Haar_H`-null (H is infinite).
4. `ν ≠ m_D`.

So the analogue of Theorem 2.3 with `K` replaced by `μ_∞` is **false**, even
though `μ_∞` is divisible and `ν` satisfies the conclusion of Lemma 2.4.
∎

**Remark 6.4 (the same failure for every number field).** Let `N₀ ⊂ F` be a
number field, `N = N₀(i)`, and `G_N = K ∩ N = {u ∈ N : |u| = 1}`. Then `G_N` is
finitely generated (its elements are integral, and Dirichlet's unit theorem
applies), so for `0 ≠ z ∈ E` the additive group `L = span_Z(G_N·z)` is finitely
generated, hence `L ⊊ E` (a finitely generated group is not a `Q`-vector space
of infinite dimension). With `H = L^⊥`, the same three steps as in Theorem 6.3
give: `H` is a nontrivial proper closed `G_N`-invariant subgroup, and
`C ∩ H = {j(ξ) : ⟨ξ, uz⟩ ∈ 2πZ ∀u ∈ G_N}` is countable because `G_N ∋ 1, i`
and `z, iz` are `R`-independent. So `Haar_H` is wild and `G_N`-invariant and not
`Haar_D`: the analogue of Theorem 2.3 fails for the unit circle of **every**
number field, not only for the roots of unity. Only the full infinite-degree
unit circle of `Q̄` supports the rigidity (Lemma 6.1, Corollary 6.2). ∎

**Lemma 6.5 (support rigidity).** Let `λ` be a K-invariant Borel probability on
`D` with `λ(ann(1)) = 1`, where `ann(1) = {d : d(1) = 1}`. Then `λ = δ_0`, so
`λ(C) = 1` and `λ` is not wild.

*Proof.* For `u ∈ K` let `Φ_u(d) = d(u·)`; `Φ_u` is a homeomorphism of `D` and
preserves `λ`. One checks `ann(⟨u⟩) = {d : d(u) = 1} = Φ_{u^{-1}}(ann(1))`:
`Φ_{u^{-1}}(e)(u) = e(u^{-1}u) = e(1) = 1`, and conversely
`e(z) := d(uz)` gives `Φ_{u^{-1}}(e)(z) = d(uu^{-1}z) = d(z)`. Hence
`λ(ann(⟨u⟩)) = λ(ann(1)) = 1` for every `u ∈ K`, and `K` is countable, so
`λ(⋂_{u∈K} ann(⟨u⟩)) = 1`. The intersection is `ann(L)` for `L` the additive
subgroup of `E` generated by `K`; by Lemma 6.1 Step 1, `L = E`; and
`ann(E) = {0}`. So `λ({0}) = 1`. Since the trivial character is `j(0) ∈ C`,
`λ(C) = 1`. ∎

**Corollary 6.6.** If `λ` is wild and K-invariant then `∫ d(1) dλ(d) ≠ 1`.
*(The integral equals 1 only if `d(1) = 1` `λ`-a.e.)* This is only the boundary
case of (R): the general statement `∫d(1)dλ = 0` is not obtained this way — see
§8.4.

**Reading.** Theorem 2.3 needs the *infinite-order* algebraic units — Step 1 of
Lemma 6.1, where `λ/n`-scaling and the algebraic closedness of `Q̄` replace the
root of unity `1/3 ∉ span_Z(μ_∞)`. Any replacement of the tower must use that
same arithmetic input; symmetry alone (invariance under roots of unity, or
divisibility) will not give (R).

---

## 7. Formula check (radicals)

`pdftotext -layout` loses radicals. Using `pdftotext -bbox` on page 2, the
words `'r'`, `'='`, `'2/5.'` sit in one line at `x = 396.1, 406.3, 420.8`, with
no radical glyph between them (the only `√` on that line is at `x = 200.5`,
immediately before `'3r.'`), and on page 3 the `√` at `x = 177.2` precedes
`'21r'` at `x = 186.8`. So the four constants are `r = 2/5`, nearest-neighbour
distance `√3 r`, separations `2r < 1` and `(√21-2) r > 1` — the values used in
Proposition 2.1. (Reproduce with
`pdftotext -bbox -f 3 -l 3 …/paper.pdf -`.)

---

## 8. Dead ends, with reasons

**8.1 "A measurable unit-distance-free set is null, so Definition 1.2 is
unsatisfiable."** False premise. The *open* ball `B(0, 1/2)` is measurable, has
positive measure and contains no pair at distance exactly 1 (its diameter is
`1`, not attained). Steinhaus gives `A - A ⊇` a neighbourhood of 0 for
positive-measure `A`, which produces pairs at *small* distances, not at
distance 1. Consequently there is no Falconer/Steinhaus vacuity argument
against Definition 1.2, and §2's certificate is not redundant.

**8.2 The p-adic closed subgroup as a counterexample to Theorem 2.3.** Let
`|·|_p` be a p-adic absolute value on `E` and
`D_p = {d ∈ D : d is |·|_p-continuous}`, a closed subgroup of `D`, invariant
under all of `K` (multiplication by `u ∈ E` is `|·|_p`-continuous). One would
like `Haar_{D_p}` as a wild non-Haar measure. It fails: `D_p = {0}`. For
`z ∈ E` and `d ∈ D_p`, `p^n z → 0` in `|·|_p`, so
`d(z)^{p^n} = d(p^n z) → 1`; and `t^{p^n} → 1` in `T` forces `t = 1` (if
`p^nθ = 2πk_n + ε_n` with `ε_n → 0` then `ε_{n+1} = pε_n` eventually, so
`ε_N = 0` for large `N` and `θ ∈ 2πZ/p^N` for all `N`, hence `θ = 0`). Since
`E` is divisible, `p^n z → 0` for *every* `z`, so `d ≡ 1`. Hence
`Haar_{D_p} = δ_0` and `δ_0(C) = 1`: not wild. The divisibility of `E` is what
kills every such attempt, and it is also the reason Theorem 6.3 needs a
*torsion* invariance group rather than a topological one.

**8.3 "Rotations of the plane are enough; the algebraic unit circle is just a
convenience."** Dead by Theorem 6.3 and Remark 6.4.

**8.4 A direct proof of (R) from marginal laws.** Attempted, and it fails at one
identifiable point. Idea: `φ(1) = ∫d(1)dλ(d) = E[X]` with `X = d(1)`; by
K-invariance the law of `d(w)` is the same for every `w ∈ K`, so every marginal
`law(ψ_w)`, `w ∈ K`, equals `ν = law(X)`. If one could show `ν = ν^{*n}` for
some `n ≥ 2` one would get `ν̂ ∈ {0,1}`, hence `ν = Haar_G` for a closed subgroup
`G ≤ T` (Fourier uniqueness), hence `E[X] ∈ {0}` unless `G = {1}`, and the
`G = {1}` case is excluded by Lemma 6.5 — which would prove (R).

The step that fails: `ψ_{u+w} = ψ_uψ_w`, and when `u, w, u+w` are all units one
is tempted to conclude `ν = ν^{*2}` from `1 + ω = e^{iπ/3} ∈ K`. That is invalid
because `ψ_u` and `ψ_w` are functions of the *same* `d`: their product's law is
not the convolution of their laws. Divisibility of `K` does not repair this,
since the multiplicative power `u^n` and the additive multiple `nu` are
different elements of `E` (`|u^n| = 1`, `|nu| = n`), so no genuine power
relation between `φ`-values at units is available. A proof of (R) must use
positive-definiteness or the tower, not marginal laws alone. What survives is
Lemma 6.5 / Corollary 6.6, the boundary case `E[X] = 1`.

---

## 9. What is and is not established

* Established: Definition 1.2 lies strictly between measurability and
  measurable properness (Lemma 1.4, 1.5), is monotone in `k` (Lemma 1.3), is
  satisfiable at `k = 7` with an exact certificate (Prop 2.1). Therefore the
  mission's Step 1 target ("no weak measurable 6-colouring") is not vacuous,
  and Step 2 is not the vacuous part of the paper.
* Established: §4's non-elementary content is exactly Theorem 2.3, which is
  colouring-blind, and §4 actually needs only (R) (Prop 3.3, Corollary 3.2).
  This is the "dependency made explicit" part of the Step 2 acceptance
  criterion.
* Established: the rigidity's arithmetic hypothesis cannot be weakened to
  divisibility, to root-of-unity symmetry, or to the unit circle of a number
  field (Theorem 6.3, Remark 6.4), while its homogeneous counterexample class is
  empty (Lemma 6.1, Corollary 6.2).
* Established (§10): the FZ tower inside Theorem 2.3 is needed only for
  requirement (W) — a factor with ergodic relative product *and* wild
  conditional difference law. Steps (f)–(k) of §10 are elementary and were
  checked; Lemma 3.4 and Lemma 3.5 are correct as stated; the only imprecision
  found is in the sign bookkeeping of (3.19) ("taking real parts of (3.17)"
  must be "multiply (3.17) by `v`, then take real parts"), which is repaired by
  one line and is not a gap.
* **Not** established: any shorter proof of Theorem 2.3, of (W) or of (R);
  §5–§8 untouched; Lemma 2.7's induction body and Lemma 3.1's fiberwise
  construction read but not verified. No terminal outcome L1–L5 is reached by
  this audit alone: it certifies the integrity of the Step 2 statement,
  localises its cost to one statement and one requirement, and does not lower
  it.

---

## 10. Audit of §2–§3: where the tower actually enters

Theorem 2.3 is proved in §§2–3. I read the whole chain and checked every step whose
content is elementary or arithmetic. Result: **no defect found**, and the tower's
role is much narrower than "19 Lean modules": it is used for exactly one thing.

**10.1 The chain.** With `µ` K-invariant and wild on `D`:

| step | statement | input |
|---|---|---|
| (a) | reduce to ergodic `µ` by the ergodic decomposition for the K-action on `D`; `C` is K-invariant Borel and null, so a.e. ergodic component is wild, and a mixture of Haar is Haar | standard |
| (b) | Lemma 3.1: a countable tower of factors `Y_α` of `(D,µ)` with the approximation property (2.6) at each successor and with `D ×_{Y_η} D` ergodic | **FZ compact-extension construction** |
| (c) | Lemma 2.7: the conditional difference law `ν_Y` of two conditionally independent samples over any `Y` in that tower satisfies `ν_Y(C) = 0` | **tower + (2.6)**, transfinite induction seeded by Lemma 2.4 |
| (d) | Lemma 3.2: relative multiple-average convergence (3.2) over `Y`, using ergodicity of `D ×_Y D` | relative weak mixing |
| (e) | `m(z) := ‖E(ψ_z|Y)‖²₂ = ∫ψ_z dν_Y` is radial, `0 ≤ m ≤ 1`, `m(0)=1`; Lemma 2.5 gives the line-average identity (2.4) for `m` | (c) + Lemma 2.5 |
| (f) | Lemma 3.3: `m(A)m(B) ≤ m(|A−B|)` and `Avg_{u∈Φ_N} m(2r|Re u|) → m(r)²` | (d); divisibility of `K` (surjectivity of `u ↦ u^{±2}`) |
| (g) | Lemma 3.4: arbitrarily large `S ⊂ K ∩ N` with every `d₀ = [N:Q]` elements a Q-basis | elementary |
| (h) | Lemma 3.5: `w(z) ≤ 4MH` for integer combinations under a cap | (f) |
| (i) | syndetic set `A₀`, good selections, the identity `2rD₀ Re v = Σ a_k 2r Re(kv)`, `p_k = 2r|Re(kv)|` | (f),(g),(h) |
| (j) | `m(s) ≥ e^{-4M₀H} > 0` on `F ∩ (0, 2rc₀)`, contradicting (2.4) | (e),(i) |
| (k) | `m(z) = 0` for `z ≠ 0`; then `∫ψ_z dµ = ∫g_z dν = 0`; Fourier uniqueness gives `µ = m_D` | (j) |

**10.2 What I verified by hand.**

* (f) first identity: this is right — the projection of
  `ψ_{-L+(A-B)u+Lu²}` is approximated by `g_{-L}U_ug_{A-B}U_u²g_L`, whose `L²` norm
  is `≤ ‖g_{A-B}‖₂` because the outer factors have sup-norm `≤ 1` (`‖g_z‖_∞ ≤ 1`
  since `|ψ_z| = 1`). The two sides of the algebraic identity
  `|A-Bu²|² = (A-B)² + 4AB(Im u)² = |-L+(A-B)u+Lu²|²` with `L = √(AB)` are exact.
* (f) second identity: `ru + rū = 2r Re u`; the average reduces to
  `∫|g_r|²U_u^{-2}|g_r|²dν` and mean ergodicity along the Følner image of `u ↦ u^{-2}`
  gives `m(r)²`; this needs `K` divisible (squaring onto) — one of two places where
  divisibility is used, the other being Lemma 2.4's finite-orbit argument.
* (g) is correct as stated: `u(t) = (1+it)/(1-it)`, and if a nonzero Q-linear
  functional `ℓ` killed every `u(t)` then the formal expansion
  `u(ha) = 1 + 2iha - 2h²a² + …` gives `ℓ(1) = ℓ(ia) = ℓ(a²) = 0` for all `a ∈ N₀`,
  and `4a = (a+1)² - (a-1)²` shows squares span `N₀`, so `ℓ` vanishes on
  `N₀ + iN₀ = N`. The "finitely many proper subspaces cannot cover" step is the
  standard product-of-numerators argument over the infinite field `Q`.
* (h) is correct: keep residues in `[0,p)`; a signed input costs `≤ 2H`
  (`w(p-b) ≤ w(p)+w(b)`), and adding two residues costs `≤ 4H` by three uses of
  the difference inequality, in both the `a+b < p` and `a+b > p` cases.
* (i) the one place where the text is too terse: "taking real parts of (3.17)"
  is not enough, one must multiply `D₀·1 = Σ a_k k` by `v` and then take real
  parts. That gives `2rD₀ Re v = Σ a_k·2r Re(kv)` exactly, and each
  `2r Re(kv) = ±p_k`; the overall sign of `Re v` is absorbed by negating all
  `a_k`, which does not change `Σ|a_k| ≤ M₀`. With that reading (3.19) is exact.
  This is a bookkeeping imprecision, not a gap.
* (i) also uses `1, i ∈ span_Q T` for (3.18): correct, `T` is a Q-basis of
  `N = N₀(i)`. Vanishing of `max_k |Re(kv)|` would give `Re v = Re(iv) = 0`,
  impossible on `|v| = 1`.
* (j) needs `t + i√(1-t²) ∈ K` for `t ∈ F ∩ [-1,1]`: correct, `√(1-t²) ∈ F`
  because `F` is a real closed field.

**10.3 The irreducible core.** By 10.1 the Furstenberg–Zimmer machinery is needed
for (b)+(c)+(d) and for nothing else, and (b)+(c) exist to satisfy *two*
requirements that pull in opposite directions:

  **(W)** find a K-factor `Y` of `(D,µ)` such that (i) `D ×_Y D` is ergodic
  (needed for relative mixing, step (d)) **and** (ii) the conditional difference
  law `ν_Y` is wild (needed for the line average, step (e)).

At the trivial factor, (ii) holds (Lemma 2.4) and (i) fails; at the terminal
factor, (i) holds by construction and (ii) is Lemma 2.7, whose proof is the
transfinite induction through the compact extensions. So **any** proof of
Theorem 2.3 must supply (W) or bypass it. That is the finest localisation this
audit can certify, and it is the concrete thing to attack for Step 2: not "the
tower" but "wildness survives the passage to a relatively ergodic factor".

**10.4 What is not checked.** Lemma 2.7's induction body (the positive-mass coset
/ centre construction of §2.4) and Lemma 3.1's fiberwise finite-rank construction
are the two genuinely FZ-internal arguments; I read them but do not claim to have
verified them, and no step of mine depends on them. Lemma 3.2 is standard relative
mixing given ergodicity of the relative product.

---

## 11. Exact check

```
cd .ultramath/smwfk0ybk/m9 && python3 work/hex7.py
```
prints the six exact checks of Proposition 2.1 and `all exact checks passed`.
Lemmas 1.1–1.5, 6.1, 6.5, Corollaries 1.6, 3.2, 6.2, 6.6, Theorem 6.3,
Remark 6.4, Propositions 2.1, 3.3 and §8, §10 are proved above; only Prop 2.1 uses
computation, and that computation is the exact-arithmetic script.
