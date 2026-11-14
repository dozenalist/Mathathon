# Corrected dependency ledger (block 5). Corrections only; no new projects.

## 0. RETRACTIONS AND CORRECTIONS OF BLOCK 4

**R1 (substantive, conclusion reversed).** Block 4 §11 asserted that constant-modulus joint
eigenfunctions with nontrivial unimodular eigenvalue "must be tolerated" by any exclusion argument,
citing `ℤ` on `𝕋²` via `(R_α,R_β)`. **Retracted.** The error: I exhibited an eigenfunction of the
*system itself* and drew a conclusion about the *self-product*. The correct statement is arrow **(A)**
below: a nonconstant eigenfunction of the system with `|χ| = 1` **does** obstruct diagonal ergodicity
of the self-product, via `f(x)\overline{f(y)}`. Consequently "exclude nonconstant eigenfunctions" is a
*necessary* target, not an over-strong one, and Astra's original phrasing was right. The `𝕋²` example is
a *witness for (A)*: the system `(x,y) ↦ (x+α, y+β)` on `𝕋²` is ergodic and its function
`f(x,y) = e^{2πix}` is a nonconstant eigenfunction with eigenvalue `e^{2πiα}`, so by (A) its
self-product is **not** ergodic — the example never showed toleration. (Ergodicity of the system and
ergodicity of its self-product are different assertions; conflating them was the error.)

**R2 (my "missing step" claim in Lemma A).** **Retracted.** Astra's proof needs no repair: since `µ` is
`u`-invariant, `µ{ψ_{uz} = c} = µ{u⁻¹{ψ_z = c}} = µ{ψ_z = c} = 1`, so the constant for `ψ_{uz}` is
`c` *itself*, before any homomorphism argument. Hence `ψ_{rz} = ψ_{sz} = c` a.e. with `r+s = 1`, so
`c = ψ_z = ψ_{rz}ψ_{sz} = c²`, `|c| = 1` gives `c = 1`, then `a_z = 1` and every element of
`span_ℤ(Kz) = E` is annihilated, so `µ = δ_{1_D}`. That is a complete proof. The alternative
(homomorphism) proof I gave is **also correct** and is kept as a variant below, but the claim that
Astra's ordering was deficient is withdrawn.

**R3 (displayed tensor-correlation formula was wrong).** In `U_{u⊗u}G` **both** tensor factors
transform, so the second inner product is *not* `u`-independent. Block 4 §11 wrote
`⟨U_{u⊗u}G,G⟩ = Σ_{z,z'} a_{uz−z'}\overline{⟨f_z,f_{z'}\rangle}`, which is **false**. Correct form
derived below (eq. (T)). The `M3 ⇒` ergodicity proof survives with the corrected formula — I redo it
in full at (B) — but the displayed identity is withdrawn.

**R4 (density).** "(U) with `D` of upper Banach density 1" is not the same as density 1 along the fixed
Følner sequence `Φ_n`, and only the latter is usable in a Følner average. **(U) is withdrawn in the
form given**, and its restatement does not rescue it — see R5.

**R5 ((U) ⇒ M3 WITHHELD).** `|a| ≤ 1 − δ` is a *bound away from 1*, i.e. compactness of the value set;
M3 demands *convergence to the specific point* `a_z\bar a_w`. Boundedness inside a compact disc is
compatible with arbitrary oscillation, so no implication follows. **The arrow (U) ⇒ M3 is withdrawn and
must not be used**; see the mixture test in §5, which shows the underlying implication
(strictness + `K`-invariance ⇒ M3) is outright false.

## 1. Nodes

All on `D = Ê`, `E = F(i)`, `F = ℚ̄∩ℝ`, `K` the unit-modulus algebraic numbers, `µ` a Borel probability,
`a_z = ∫ψ_z dµ`, `U_u f(d) = f(u·d)`.

* **(INV)** `µ` is `K`-invariant. **(ERG)** `µ` is ergodic for the `K`-action. **(WILD)** `µ(C) = 0`.
* **(E1)** Every `f ∈ L²(µ)` with `U_u f = χ(u)f` for all `u ∈ K`, `|χ| = 1`, is constant.
* **(WM)** `µ⊗µ` is ergodic for the diagonal action (equivalently `(D,µ)` is weakly mixing).
* **(M3)** For all `z,w ∈ E`, along the fixed Følner sequence `Φ_n ⊆ K`,
  `avg_{u∈Φ_n} |a_{uz−w} − a_z\overline{a_w}|² → 0`.
* **(LEMA)** For `z ≠ 0`: `|a_z| = 1 ⇒ µ = δ_{1_D}`; hence under (WILD), `|a_z| < 1`.
* **(APP)** `[ErgodicVAdd Rot (D×D) (RelativeProduct.law µ q hq)]` holds at the *constant* factor `q`,
  so paper Lemma 2.4 (`wild_independent_difference`, machine-checked) gives the `C`-null conditional
  difference law, and §2.4, §3.1, Theorem A′ become unnecessary.

## 2. Arrow (A) [proved here]: (ERG) + (E1-failure) ⇒ ¬(WM). Complete proof

Let `f` be nonconstant with `U_u f = χ(u)f`, `|χ(u)| = 1`.
(i) `|U_u f| = |f|`, so `|f|` is invariant; by (ERG) `|f| = c` a.e. for a constant `c ≥ 0`; `f ≠ 0`
gives `c > 0`.
(ii) `Φ(x,y) := f(x)\overline{f(y)}` satisfies `Φ(u·x,u·y) = χ(u)f(x)\overline{χ(u)f(y)} = Φ(x,y)`:
invariant.
(iii) `Φ` is nonconstant: if `Φ = k` a.e. then `f(x)\overline{f(y)} = k` for a.e. `(x,y)`; choose `y` in
a conull set with `f(y) ≠ 0`, then `f(x) = k/\overline{f(y)}` for a.e. `x`, so `f` is constant a.e. —
contradiction.
(iv) A nonconstant invariant function defeats ergodicity of the diagonal action. ∎
**Consequence (the correction to block 4):** eigenfunction exclusion is *necessary* for (WM).
**Scope note, honest:** the converse `(E1) ⇒ (WM)` is **not available**: no proof here and no
counterexample constructed here. The ledger therefore records (E1) as necessary, not sufficient, and no
claim is made in either direction beyond (A).

## 3. Arrow (B) [proved here]: (M3) ⇒ (WM). Complete proof, with the corrected formula

Take `F ∈ L²(µ⊗µ)` invariant with `∫F = 0`, `‖F‖ = 1`, and a finite character polynomial
`G = Σ_{(z,w)∈Σ} c_{z,w}ψ_z⊗\overline{ψ_w}` with `‖F−G‖ ≤ η` and `∫G = 0` (characters span densely by
Stone–Weierstrass; no Haar orthogonality is used).
(a) `U_u` unitary ⇒ `‖U_{u⊗u}G − G‖ ≤ 2η` for every `u`.
(b) Write `G = Σ_z ψ_z⊗f_z`, `f_z = Σ_w c_{z,w}\overline{ψ_w}`. **Both** factors transform, so
```
⟨U_{u⊗u}G,G⟩ = Σ_{z,z'} a_{uz−z'}·⟨U_u f_z, f_{z'}⟩        (T)
```
with `⟨U_uf_z,f_{z'}⟩ = Σ_{w,w'} c_{z,w}\bar c_{z',w'}\overline{a_{w−u⁻¹w'}}` — genuinely
`u`-dependent, which is the correction R3. Using `K`-invariance (`a_{uz−z'} = a_{z−u⁻¹z'}`),
```
⟨U_{u⊗u}G,G⟩ = Σ_{z,w,z',w'} c_{z,w}\bar c_{z',w'} a_{z−u⁻¹z'}\overline{a_{w−u⁻¹w'}}.      (T′)
```
At `u = 1` this is `Σ c\bar c a_{z−z'}\overline{a_{w−w'}} = ‖G‖²`.
(c) By (M3) each factor in (T′) converges to its constant in **mean square** — `a_{z−u⁻¹z'} →
a_z\bar a_{z'}` (this includes the diagonal case `z = z'`, where the limit is `|a_z|²`) — and both are
bounded by `1`; a product of a mean-square-convergent bounded sequence with a bounded sequence converges
in mean. Finitely many pairs, so no uniformity in frequency is needed:
`avg_u ⟨U_{u⊗u}G,G⟩ → Σ c_{z,w}\bar c_{z',w'}(a_z\bar a_{z'})(\overline{a_w\bar a_{w'}}) = |Σ c_{z,w}a_z\bar a_w|² = |∫G|² = 0`.
(d) Hence `avg_u ‖U_{u⊗u}G − G‖² → 2‖G‖² − 2·0 ≥ 2(1−η)²`, contradicting (a)'s `≤ 4η²` when
`η < 1/3`. ∎
**Used:** density of characters, (M3), unitarity. **Not used:** (LEMA), (WILD), (ERG), any tower, Haar.

## 4. Graded arrows

| arrow | grade |
|---|---|
| (ERG) + ¬(E1) ⇒ ¬(WM)  — (A) | **[proved here]**, complete, §2 |
| (M3) ⇒ (WM) — (B) | **[proved here]**, complete, §3 |
| (WM) ⇒ (M3) | **[classical/imported]** — the matrix-coefficient criterion for weak mixing; not re-proved here. With (B) this gives `(M3) ⇔ (WM)` |
| (WM) + (WILD) ⇒ (APP) | **[proved here at paper level]**, from machine-checked `wild_independent_difference` (= Lemma 2.4) at the constant factor |
| (LEMA): (INV) ∧ `|a_z| = 1` ⇒ `µ = δ_{1_D}`; (WILD) ⇒ `|a_z| < 1` | **[Astra], verified here**; Astra's own ordering suffices (R2) |
| (LEMA) ⇒ (E1) | **NO** — (LEMA) excludes only *characters* as eigenfunctions; general `f ∈ L²(µ)` is untouched |
| (E1) ⇒ (WM) | **NO** — no proof, no counterexample constructed; not asserted |
| (LEMA) ⇒ (M3) | **NO** — false already with `K`-invariance + wildness + non-ergodicity, §5 |
| (U) ⇒ (M3) | **WITHDRAWN** (R5); additionally (U) as stated was mis-stated (R4) |
| (M3) ⇒ (M) = H2 | **NO** — `(M3) ⇒ (APP)` makes (M) unnecessary at the *constant* factor, but H2 is about the *terminal* factor; the two are not equivalent |

## 5. Mixture test: strictness + invariance + wildness does NOT give (M3)

Concrete system: `K' = ℤ²` acting on `X = 𝕋²` by `(m,n)·(x,y) = (x+mα, y+nβ)`, `1,α,β` `ℚ`-independent.
Its invariant measures include `Leb` and `δ_0`. Take `µ_λ = λ·Leb + (1−λ)δ_0`, `0 < λ < 1`.
* `µ_λ` is invariant. It is **not ergodic** (the two components are mutually singular invariant sets).
* Pointwise strictness holds: for `(m,n) ≠ (0,0)`,
  `a_{(m,n)} = λ·0 + (1−λ)·1 = 1−λ < 1`, and `a_0 = 1`; so the analogue of (LEMA)'s conclusion holds.
* (M3) **fails**, by an explicit positive limit: with `z = w = (1,0)`,
  `a_{uz−w} = 1−λ` for every `u ≠ (1,0)` and `= 1` at `u = (1,0)`, so
  `avg_u |a_{uz−w} − a_z\bar a_w|² → |(1−λ) − (1−λ)²|² = λ²(1−λ)² > 0`.
* Where the hypotheses are violated: **ergodicity** fails (the mixture of two mutually singular ergodic
  measures is not extreme). In the paper's setting the degenerate component `δ_0` is exactly what
  **(WILD)** forbids — `δ_{1_D}(C) = 1` — so the paper's wildness hypothesis is precisely what blocks
  this mixture. That is why the test separates the *logic* of the implication and is **not** a
  counterexample to (M3) for the paper's `µ`.

**Conclusion banked:** any derivation of (M3) from pointwise strictness must use **ergodicity** in an
essential way; strictness plus invariance plus the wild condition cannot suffice. This is the precise
sense in which (U) and (LEMA)-strictness are the wrong currency.

## 6. Where the ledger stands

`(M3) ⇔ (WM)` [one arrow imported], `(WM) ⇒ (APP)` [paper level, Lemma 2.4 machine-checked],
`¬(E1) ⇒ ¬(WM)` [proved]. What is missing for the simplification is a proof of (WM) for the paper's
`µ`, and the only analytic criterion in hand is (M3), whose gap is: **convergence, not boundedness, of
`a` along `K`-orbits of frequencies, uniformly over the finitely many frequency pairs of an
approximant** — with ergodicity necessarily entering (the mixture test). (LEMA) supplies neither.
**No positivity project, no finite-search project, and no escalation this block; Astra's use count stays
at 1.**
