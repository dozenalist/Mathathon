# Step 2: what the transfer consumes from the rigidity theorem, and why routes (a), (c), (d) cannot remove it

Member m15, direction **d12** (Step 2, route (c): model-theoretic / Tarski–Seidenberg + selection).
Companion: `check.py` (exact-arithmetic verification of every numerical and algebraic claim below).

Citations are to the extracted paper text; regenerate it with

```
pdftotext -layout attachments/here-are-three-files-ni5n/paper.pdf /tmp/paper.txt
```

and all quoted line numbers below refer to that file (the numbers are also reproduced here verbatim,
so the citation is checkable either way).

---

## 0. Result

The only measurable-versus-arbitrary step in the paper is **Theorem 1.3**:
*proper k-colouring exists ⇔ weak measurable k-colouring exists* (Def. 1.2). For the mission only the
**forward** direction is used, namely

> **Prop. 4.2.** If the plane admits an unrestricted proper k-colouring, then it admits a weak
> measurable k-colouring.

(Lemma 4.3, the converse, enters Theorem 1.1 only as the reverse implication; the deduction of
Theorem 1.1 from Theorem 1.4 uses Prop. 4.2 alone — extracted lines 89–90, verbatim:
"Deduction of Theorem 1.1. A proper five-coloring would give a weak measurable five-coloring by
Theorem 1.3, contrary to Theorem 1.4." So **Step 2's target can be weakened to Prop. 4.2**; the
density-point half of the transfer need not be touched at all.)

Prop. 4.2 consumes the heavy analysis **exactly once**, at the rigidity theorem:

* **Theorem 2.3** (line 299): *every K-invariant probability measure ν on D with ν(C) = 0 is Haar
  measure* (i.e. ν wild ⇒ ν = m_D).
* Its **only** application in the paper outside its own proof is in §4.1, at line 1263 of the
  extraction, verbatim:
  > "The scalar translation spectral measure of bi is K-invariant: covariance gives equality of its
  > Fourier coefficients at z and uz, and Fourier uniqueness gives invariance of the measure. It gives
  > C measure zero, by the spectral-subspace assertion of the lemma. If it is nonzero, normalize it and
  > apply Theorem 2.3. The scalar spectral measure is therefore a multiple of Haar measure, including
  > the zero multiple. It follows that ⟨bi , Tz bi ⟩ = 0 (z ∈ E \ {0})."

  Verifiable: `grep -n "Theorem 2.3" paper.txt` returns exactly lines 134 (preamble), 299 (the
  statement), 1073 ("Proof of Theorem 2.3."), and **1263** (the single use). Everything else in
  Prop. 4.2 — Lemma 4.1's continuous factor, the positivity of p_i, the density of K in S¹, the
  finite-valued approximation and the Fubini sampling — is soft functional analysis; the FZ tower
  modules (14 under `MeasureTheory/CompactFactors` plus 16 of the 19 under `Analysis/PlaneSpectrum`;
  §8 measures them) hang off Theorem 2.3 through its relative-singularity step 1c, not off those.

**Main result (Thm. 1 below): the statement actually consumed at line 1263, the paper's full form
(rigidity: ν = Haar), and the unit-direction-only form that the Lean development actually
instantiates (`residual_fourier` at `z = kCoeff b`, |z| = 1) are *one and the same statement*:

> **(R′)** `ν` wild K-invariant probability ⇒ `ν = m_D`
> ⟺ **(R)** `ν` wild K-invariant probability, `z ∈ E∖{0}` ⇒ `f_ν(z) = 0`
> ⟺ **(R_unit)** `ν` wild K-invariant probability, `u ∈ K` ⇒ `f_ν(u) = 0`  (equivalently `m(1) = 0`).

So

> no weakening of the rigidity hypothesis can replace Theorem 2.3 in this route, and in particular
> **retargeting the closure to unit directions (§8, and direction d7/f19) buys nothing**: (R_unit) is
> not a smaller statement, it is the same one.

This also corrects an accepted finding: d7/f9–f19 (m14) states that (R_unit) is "a strictly smaller
*statement*" than the paper's `m ≡ 0`. It is not — see Cor. 1.1 and Prop. 2.3. (m5's d5/f25
parenthetical "z=1 equivalent to all z" is right; what follows is its proof at statement level, and it
extends it: the equivalence holds for *all* wild K-invariant measures, not only the class arising in
Prop. 4.2.)

Consequently the Lean dependency closure of the transfer cannot drop the CompactFactors modules by
weakening the rigidity input (relevant to route (e)); the only lever is a *different proof* of
Theorem 2.3 itself, or a transfer-free route (see §7).

I then falsify my own route (c): §4 shows what Tarski–Seidenberg can and cannot see (§4 is the only
place a first-order/definable argument could enter, and it provably cannot reach Lebesgue measure),
and §5 shows that the "measurable selection" half of route (c) is *impossible*, not merely unproved:
there is no measurable transversal of R²/E. §6 shows amenability alone is insufficient, which
constrains route (d).

---

## 1. The setting, exactly as in the paper

Definition 2.1 (extracted lines 262–272):

* `F = Q̄ ∩ R`, `E = F(i)` — the countable algebraic plane, an additive discrete group, dense in C;
* `K = {u ∈ E : u ū = 1}` — the algebraic unit circle, a countable **divisible** abelian group;
* `D = Ê_disc` — the compact metrisable character group of E; `ψ_z(d) = d(z)` for z ∈ E;
* `C = j(R²)`, `j(ξ)(z) = exp(i ξ·z)` — the subgroup of ordinary continuous characters.
* For a ∈ E: `(a d)(z) = d(a z)`; the action of K on D is by multiplication of arguments, and on the
  frequency side by orthogonal maps (line 288–291).

Definition 2.2 and Theorem 2.3 (lines 292–301): ν is **wild** if ν(C) = 0; Fourier coefficients
`f_ν(z) = ∫_D ψ_z dν`; Theorem 2.3: every K-invariant Borel probability ν with ν(C) = 0 equals m_D
(normalized Haar). The paper then says explicitly (lines 304–305, verbatim):

> "The Fourier coefficients of Haar probability vanish at every nonzero z ∈ E. This is the conclusion
> needed in Section 4:"

Definition 1.2 of a weak measurable colouring (lines 64–70): a Lebesgue measurable
`c : R² → {1,…,k}` such that for every R > 0, `Σ_i ∫_{B(0,R)}∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0`.

Lemma 4.1 (lines 1168–1200): `H_c = {v ∈ L² : lim_{z→0, z∈E} ‖T_z v − v‖ = 0}` is `L²(F_c)` for a
factor `F_c`, is the spectral subspace on `C`, and the operators extend to a strongly continuous
unitary representation `T_x` of the *full* plane R², preserving the positive cone and 1; rotations
preserve `H_c`.

Prop. 4.2 (lines 1239–1312): from a proper k-colouring of E,
1. `Ω = {proper k-labellings of E}` is closed in the compact `{1,…,k}^E` (nonempty); the countable
   amenable group `E ⋊ K` acts continuously; Følner averages give an invariant probability µ.
2. `f_i` = indicator that the origin has label i; properness gives
   **(4.1)** `∫_Ω f_i T_u f_i dµ = 0` for every u ∈ K (u a unit vector of E, hence |0 − u| = 1).
3. `p_i = E(f_i | F_c)`, `b_i = f_i − p_i`; `0 ≤ p_i ≤ 1`, `Σ_i p_i = 1`; both are rotation-fixed.
4. The **scalar translation spectral measure λ_i** of `b_i` is K-invariant and `λ_i(C) = 0`.
   Theorem 2.3 applied to `λ_i/λ_i(D)` gives
   **(⋆)** `⟨b_i, T_z b_i⟩ = ∫_D ψ_z dλ_i = 0` for all z ∈ E∖{0}.
5. Both cross terms in (4.1) vanish, so `∫_Ω p_i T_u p_i dµ = 0` for every u ∈ K; K is dense in S¹
   (rational tangent half-angle, line 1270); strong continuity gives it for all `u ∈ S¹`; unitarity
   and the group law give
   **(4.2)** `⟨T_x p_i, T_{x+u} p_i⟩ = ∫_Ω (T_x p_i)(T_{x+u} p_i) dµ = 0` for every x ∈ R², u ∈ S¹.
6. Measurable sample: finite-valued approximations of `x ↦ T_x p_i` with summable squared errors,
   a countable exhaustion of the plane, a subsequence per a.e. x, clamping to [0,1], then Tonelli and
   one sample ω chosen off countably many null sets; the least index with positive field is the
   colouring.

The whole weight of Part I sits in step 4. Steps 1–3, 5, 6 are soft.

---

## 2. Theorem 1: the three forms of the rigidity input are one statement

Write, for a finite Borel measure ν on D, `f_ν(z) = ∫_D ψ_z dν` (z ∈ E). Note `ψ_0 ≡ 1`, so
`f_ν(0) = ν(D)`.

**(R′)** (= Theorem 2.3) *For every K-invariant Borel probability ν on D with ν(C) = 0: ν = m_D.*

**(R)** *For every K-invariant Borel probability ν on D with ν(C) = 0 and every z ∈ E∖{0}:
`f_ν(z) = 0`.*

**(R_unit)** *For every K-invariant Borel probability ν on D with ν(C) = 0 and every u ∈ K:
`f_ν(u) = 0`.* (Since K-invariance gives `f_ν(u) = f_ν(1)` for every u ∈ K, this is the single scalar
statement `m(1) = 0`.)

**Theorem 1.** (R′) ⟺ (R) ⟺ (R_unit): all three are the same statement about wild K-invariant
probabilities.

*Proof.* (R′) ⇒ (R): reduces to ν = m_D, and Haar coefficients vanish at every nonzero z (paper,
line 304; also a direct computation).

(R) ⇒ (R_unit): immediate.

**(R_unit) ⇒ (R).** Let ν be wild and K-invariant and let a ∈ E∖{0}. Multiplication by a is an
automorphism of the additive group E, so `φ_a : D → D`, `(φ_a d)(z) = d(a z)`, is a continuous
automorphism of D. Put `ν_a := (φ_a)_* ν`. Two facts:

* **ν_a is wild.** `φ_a(C) = C`: for a continuous character `d = j(ξ)`,
  `(φ_a d)(z) = exp(i ξ·(a z)) = exp(i (M_aᵀ ξ)·z) = j(M_aᵀ ξ)(z)`, where `M_a` is the real-linear
  map `z ↦ a z`; `M_aᵀ` is invertible, so `φ_a(C) = C` and `ν_a(C) = ν(C) = 0`.
* **ν_a is K-invariant.** For `u ∈ K` the maps `ψ_u` (`(ψ_u d)(z) = d(u z)`) and `φ_a` commute,
  because E is commutative: `(ψ_u φ_a d)(z) = d(a u z) = d(u a z) = (φ_a ψ_u d)(z)`. Since ν is
  `ψ_u`-invariant and `φ_a` is a bijection, ν_a is `ψ_u`-invariant.

So (R_unit) applies to ν_a, giving `0 = f_{ν_a}(1) = ∫ d(1) dν_a(d) = ∫ (φ_a e)(1) dν(e)
= ∫ e(a) dν(e) = f_ν(a)`. As a ∈ E∖{0} was arbitrary, (R) holds.

(R) ⇒ (R′): by (R), `f_ν(z) = 0` for z ≠ 0 and `f_ν(0) = ν(D) = 1 = f_{m_D}(0)`, so `f_ν = f_{m_D}`.
The continuous characters of the compact group D are exactly `{ψ_z : z ∈ E}` (the dual of D is the
discrete group E) and they generate a Stone–Weierstrass-dense subalgebra of `C(D)`; equality of all
Fourier coefficients therefore gives `ν = m_D`. (The same "Fourier uniqueness" the paper invokes at
line 1190 and line 1260.) ∎

**Corollary 1.1.** (R_unit) is *not* a smaller statement than (R) or (R′): they are equivalent. Hence

* no weakening of the rigidity hypothesis can replace Theorem 2.3 in this route, so the Furstenberg–
  Zimmer tower cannot be removed from the transfer by weakening what is proved about wild measures;
* **retargeting the Lean closure to unit directions buys nothing.** The only instance used at
  `BorelTransfer.lean:61` is `residual_fourier` at `z = kCoeff b` with `|z| = 1`, and this is the
  suggestion of d7/f19 for route (e); by Theorem 1 the unit instance is *the same statement*, so
  `residual_fourier_unit` can only reduce the target's syntax, never its logical strength, and no
  part of Theorem 2.3's proof can be dropped on that account.

**Correction to an accepted finding.** d7/f9–f19 (m14) asserts that (R_unit) is "a strictly smaller
*statement*" than the paper's `m ≡ 0`, and proposes the retarget. That assertion is false:
Theorem 1 above is a proof of the equivalence over the whole class of wild K-invariant probabilities.
(m5's d5/f25 parenthetical "z = 1 equivalent to all z" is correct; Theorem 1 proves it for the whole
class rather than only for the spectral measures arising in Prop. 4.2, so no restriction of the class
can be exploited either.) What survives from d7 is the correct and separate point that the paper's
*proof* of `m(1) = 0` still runs the whole number-field apparatus — a shorter proof is not excluded,
but it cannot come from a weaker statement.

**Remark 1.2 (scope).** Theorem 1 is a statement-level equivalence. At the *instance* level,
Prop. 4.2 applies Theorem 2.3 only to the measures λ_i that actually arise as scalar spectral measures
of the label residuals b_i; a hypothetical structure theorem about that subclass is not excluded here.
§3 checks that the structure the transfer *does* extract gives no leverage.

**Prop. 2.3 (machine check of the two algebraic facts).** The facts used in (R_unit) ⇒ (R) — that
`ψ_u` and `φ_a` commute, and that `f_{(φ_a)_*ν}(1) = f_ν(a)` — are verified exhaustively in a finite
model of the character group (`check.py` section (F)): `A = F_8` (as a 3-dimensional F_2-vector space,
with field multiplication, so E is modelled by a commutative ring), `K = A∖{0}`, all a ∈ A∖{0}, all
K-invariant ν, all characters. `φ_a(C) = C` is not modelled (no topology in the finite model), but it
is the one-line frequency computation displayed in the proof.

---

## 3. Proposition 2: the other hypotheses of Prop. 4.2 give no leverage

Besides "λ_i is wild and K-invariant", Prop. 4.2 has three structural inputs. They are:

* **(a) unit correlation** (4.1): `⟨f_i, T_u f_i⟩ = 0` for u ∈ K;
* **(b) positivity**: `p_i = E(f_i | F_c) ≥ 0`, and `T_u p_i ≥ 0`;
* **(c) label sum**: `Σ_i f_i = 1`, hence `Σ_i p_i = 1` and `Σ_i b_i = 0`.

**Lemma 2.1 (derived constraint).** For every u ∈ K,
`f_{λ_i}(u) = ⟨b_i, T_u b_i⟩ = −⟨p_i, T_u p_i⟩ ∈ ℝ and ≤ 0`.

*Proof.* `0 = ⟨f_i,T_u f_i⟩ = ⟨p_i,T_u p_i⟩ + ⟨b_i,T_u b_i⟩`, the cross terms vanishing because `H_c`
is translation-invariant (`T_u p_i ∈ H_c`, `b_i ⊥ H_c`). `p_i ≥ 0` and `T_u p_i = (ω ↦ p_i(T_{-u}ω)) ≥ 0`,
so `⟨p_i, T_u p_i⟩ = ∫ p_i · T_u p_i dµ ≥ 0` and is real. Hence `⟨b_i,T_u b_i⟩` is real and ≤ 0. ∎

**Proposition 2.2 (Haar satisfies every extracted constraint).** Let `m_i = ‖b_i‖² ≥ 0` and suppose
each `λ_i = m_i · m_D`. Then

1. `f_{λ_i}(z) = 0` for every z ≠ 0, so (⋆) holds — the benign case;
2. `f_{λ_i}(u) = 0` for every u ∈ K∖{0}, so Lemma 2.1 holds with equality (the `u = 0` case is not in K);
3. `⟨b_i, b_j⟩ = ⟨f_i,f_j⟩ − ⟨p_i,p_j⟩ = −∫ p_i p_j ≤ 0` for i ≠ j, and `Σ_i b_i = 0` gives
   `Σ_{i<j} ∫ p_i p_j = ½ Σ_i m_i`;
4. `Σ_i p_i = 1` gives `Σ_i ‖p_i‖² = 1 − Σ_i m_i`; with 3. this is `Σ_i ‖p_i‖² + 2Σ_{i<j}⟨p_i,p_j⟩ = 1`
   and `Σ_i m_i ≤ 1`. No contradiction.

Consequently the constraints (a),(b),(c) — the only information about λ_i beyond wildness and
K-invariance that the transfer extracts — are simultaneously satisfiable in the *Haar* case, i.e. they
do not cut the class of admissible measures down in a way that could substitute for rigidity. Together
with Theorem 1 this says: the rigidity input is used at exactly the strength at which it is stated.

(Numerical verification of items 3–4 for symbolic m_i: `check.py` section (D).)

---

## 4. Theorem 3: what Tarski–Seidenberg can see, and why route (c) cannot reach Prop. 4.2

Route (c) proposes to avoid the spectral machinery by Tarski–Seidenberg plus a selection theorem. The
following theorem delimits the first half exactly.

**Theorem 3 (χ is a first-order constant).** Let `R'` be any real closed field, and let `Γ_{R'}` be the
unit-distance graph on `R'²`. Then `χ(Γ_{R'}) = χ(Γ_R)`.

*Proof.* By de Bruijn–Erdős, `χ(Γ_{R'}) = sup{χ(G) : G a finite subgraph of Γ_{R'}}` (the value ∞ if
the sup is unbounded). A finite subgraph of `Γ_{R'}` is the unit-distance pattern of a finite tuple of
points of `R'²`. For a finite graph `G` on `{1,…,n}`, "G is the unit-distance pattern of some n-tuple"
is the sentence

```
σ_G  ≡  ∃ x_1 … x_n  ( ⋀_{(i,j) ∈ E(G)} |x_i − x_j|² = 1  ∧  ⋀_{(i,j) ∉ E(G), i<j} |x_i − x_j|² ≠ 1 )
```

in the language of ordered fields, with **no parameters**. The theory RCF is complete, so `σ_G` holds in
`R'` iff it holds in `R`. Hence the set of realisable finite unit-distance graphs, and therefore the
supremum of their chromatic numbers, is the same for `R` and `R'`. ∎

**Consequence for route (c).** Every step of a Tarski–Seidenberg argument is valid in every real closed
field, so its conclusion is invariant under passing to an arbitrary real closed field — in particular it
holds over a **non-Archimedean** real closed field, where there is no Lebesgue measure at all. But
Prop. 4.2's conclusion is Definition 1.2, an identity of Lebesgue integrals on R². Lebesgue measure, the
σ-algebra of measurable sets, and the space `D` of *all* characters of the discrete group E (a compact
metrisable group of cardinality 𝔠, since E is countable; not a definable object) are outside the
real-closed-field language.
So:

* Tarski–Seidenberg can at most transport χ between real closed fields (Theorem 3 shows it does so
  perfectly), and that transfer is *already* available as R1;
* it has no access to `D`, to K-invariant measures on `D`, or to Lebesgue measure, so it cannot supply
  step 4 of Prop. 4.2, whose entire content is a statement about K-invariant measures on `D`.

What route (c) would actually need is `χ(Γ_R) ≤ k ⇒ a **definable** (semi-algebraic) proper
k-colouring exists`, since a definable colouring is Lebesgue measurable. That implies Prop. 4.2, so it
is at least as strong as the forward half of Theorem 1.3, and no proof of it is known. It holds at k = 7: the hexagonal Hadwiger
7-colouring is given by semi-algebraic data (Voronoi cells of a triangular lattice, coloured by
cosets of the index-seven sublattice `(2−ω)Λ`, with `|2−ω|² = 7`) — see check (C) in `check.py`,
which verifies exactly that equal-coloured Voronoi cells are separated by *more than 1*
(`√(42/5) > 2√(2/5) + 1`, exact form `841 > 160`), hence that the colouring is proper: no unit pair
lies in two cells of the same colour. So route (c) can at best produce a *definable* colouring; it cannot
produce the transfer's implication without the further, unproved implication `χ ≤ k ⇒ definable
k-colouring`, and no part of Tarski–Seidenberg supplies that (Theorem 3 shows the first-order method
is exactly χ-invariance).

**Credit and relation to d5/f25.** d5 (m5) asserts "Tarski-Seidenberg is fully consumed at R1" as a
one-line verdict on route (c); Theorem 3 above is the proof of that verdict, and it also states the
ceiling exactly: Tarski–Seidenberg gives *invariance of χ across real closed fields*, which is more
than R1 says and is all the first-order method can ever give.

**Status of route (c): falsified as a route to Prop. 4.2.** The first half (Tarski–Seidenberg) cannot
reach the rigidity input (§4); the second half (selection) is *impossible*, not merely unproved (§5).

---

## 5. Proposition 4: there is no measurable selection, so the plane field cannot be obtained by transport

**Proposition 4.** Let `E ⊂ R²` be the countable dense subgroup of Definition 2.1. There is no
Lebesgue measurable set `A ⊆ R²` meeting every coset of E in exactly one point.

*Proof.* Suppose A is measurable and meets each coset of E at most once. Then `A − A` contains no
nonzero element of E: if `a, a' ∈ A` and `a − a' = z ∈ E∖{0}`, then a and a' lie in the same coset.
If A had positive measure, Steinhaus's theorem would make `A − A` contain a neighbourhood of 0, hence
a nonzero element of E (E is dense) — contradiction. So A is null. If A met *every* coset, then
`R² = ⋃_{z∈E} (A + z)` would be a **countable** union of null sets (E is countable), hence null — a
contradiction. ∎

**Credit and relation to d5/f25.** d5 (m5) lists "prove indispensability via the selection
obstruction" as the route-(a) plan; Proposition 4 is that obstruction, and it is a theorem, not a
failure of an attempt: no measurable transversal exists at all.

**Consequence.** The naive selection route to Prop. 4.2 is

> for each x ∈ R², measurably choose an algebraic offset `z(x) ∈ E` (equivalently a point of `x + E`),
> and read off the E-colouring.

Any such measurable choice `x ↦ x − z(x)` restricted to a set containing one point per coset is a
partial transversal, forbidden by Proposition 4; so no measurable family of offsets exists. This is
exactly the hole that Lemma 4.1 fills in the paper, and it fills it *without* a transversal: the
operators `T_x` for x ∈ R² are defined as strong limits `T_{z_n} v → T_x v` for `z_n ∈ E`, `z_n → x`,
which converges because `v ∈ H_c` (the definition is independent of the approximating sequence; the
Lean counterpart is `orbitExtension` / `orbitExtension_continuous` in
`lean/OAI/Geometry/PlaneColoring/BorelTransfer.lean`, built on `dense_E`). Since Proposition 4 rules
out the selection alternative, **the uniform-continuity extension on the continuous factor is
indispensable in its role**: any proof of Prop. 4.2 must either produce the plane field this way or
give a different construction of a jointly measurable field with (4.2). "Measurable selection" and
Lusin–Novikov cannot be that construction, because the quotient `R²/E` admits no measurable section at
all (it is not even smooth: the cosets are dense).

---

## 6. Remark 5: amenability alone is not enough (superseded, but independent, for route (d))

**Status.** d7/f8 (m14, accepted) already kills route (d) with a *finite*-k certificate: the
two-sided Bernoulli shift on `{0,1}^ℤ` with graph `x ~ Sx` has χ = 2 and no measurable proper
2-colouring, and the Følner construction of Prop. 4.2 applies to it verbatim. That is strictly
stronger than the remark below (which is a `k = ℵ₀` statement) and I do not claim it. The remark is
kept only because its mechanism is different — it shows that the failure is already present for a
**Cayley graph of an abelian amenable group with a countable Borel generating set**, so nothing in the
statement "the unit-distance graph is a Cayley graph of an amenable group" can be the source of the
transfer.

**Proposition 5.** Let `G = (R,+)` and `S = Q∖{0}`; the Cayley graph `Γ_S` (x ~ y iff x − y ∈ Q∖{0})
satisfies `χ(Γ_S) = ℵ₀ < χ_meas(Γ_S)`.

*Proof.* Each coset of Q is a countable clique, so `ℵ₀ ≤ χ ≤ ℵ₀`. Conversely every measurable set A
meeting each Q-coset at most once is null (the Steinhaus argument of Proposition 4), so a measurable
colouring with countably many colours would express R as a countable union of null sets. ∎

**Consequence.** The two accepted Step-2 barriers together (d7/f8 for k = 2, Prop. 5 for k = ℵ₀)
say: the transfer is not an amenability phenomenon and cannot be obtained from amenability plus
compactness. The paper's transfer must use arithmetic specific to `K ⊂ E` — divisibility of K (step
1a) and the number-field argument (step 1e) — which is exactly what Theorem 2.3 does.

## 7. What is left for Step 2, and what Step 2 is now worth

**State of the four candidate routes after this direction and the accepted Step-2 directions:**

| route | verdict | certificate |
|---|---|---|
| (a) palette equivalence | circular | d5/f25: a *jointly measurable* palette field yields the weak colouring with no spectral theory, but Definition 5.1 builds the field from circle averages of Borel classes, so the field presupposes the measurability that Theorem 2.3 supplies. |
| (b) one compact factor | dead | d7/f10: the skew product `T(x,y) = (x+α, y+x)` is a compact (isometric) extension of its Kronecker factor whose relative square is not ergodic, and property (2.6) forces any admissible `Y` to be Kronecker, so no single level can serve as `Y` in Lemma 2.7. |
| (c) Tarski–Seidenberg + selection | dead | §4 (Tarski–Seidenberg's reach is exactly RCF-invariance of χ, so it cannot see Lebesgue measure or D) and §5 (no measurable transversal of R²/E: the selection half is impossible, not unproved). |
| (d) amenability / quasi-tiling | dead | d7/f8 (Bernoulli shift, k = 2) and §6 (Q-coset Cayley graph, k = ℵ₀). |
| (e) shrink the Lean closure | no interface move | Theorem 1 (§2): the rigidity input is one statement in three equivalent forms, so retargeting to `|z| = 1` is not a weakening; §8 measures that the transfer proper adds only 2 modules / 492 lines to a 15 482-line rigidity closure. |

So the only remaining lever inside the paper's route is **a different proof of Theorem 2.3** (equivalently
of `m(1) = 0`, by Theorem 1). Everything else in Prop. 4.2 is soft: Lemma 4.1, the density of K in S¹
(`check.py` section (B)), the finite-valued approximation, the Fubini sampling — none of them carries
any CompactFactors module.

**What Step 2 is now worth, given the Step-1 decision.** Step 1 is closed negatively (d1/f2, d1/f27:
the tightened interface CSP is SAT at every length, and the tightening is provably inert for all
k ≥ 5). Step 2 was only ever the bridge that turns "no weak measurable k-colouring" into "no
k-colouring"; with the k = 6 geometric obstruction not available, the bridge has no load to carry at
k = 6. Hence:

* Step 2's residual value is (i) formalisational — 15 482 lines of rigidity for one scalar statement —
  and (ii) conditional: any future lower bound at k = 6 on the palette side would need Prop. 4.2
  again, and by Theorem 1 it would need Theorem 2.3 at full strength.
* Nothing in this direction gives χ ≥ 7, and nothing in it can: it is a Step-2 analysis.

For completeness: only the forward direction (Prop. 4.2) is needed to deduce χ ≥ 7 from "no weak
measurable 6-colouring"; the converse (Lemma 4.3) is used only for the reverse implication of
Theorem 1.3 and can be dropped from any Step-2 target. Its Lean closure is 2 modules / 210 lines, so
it is also the cheap half.

---

## 8. Measured dependency (data for route (e)), and a fact-check of the module counts

`depclosure.py` (companion script) parses the `import OAI.…` lines of `lean/OAI` and computes
transitive closures with line counts. Measured on the tree as it stands:

```
lean/OAI                            : 83 modules, 31277 lines
Analysis/PlaneSpectrum              : 19 modules,  8466 lines
MeasureTheory/CompactFactors        : 14 modules,  7728 lines
closure of PlaneSpectrum.Ergodicity : 30 modules, 15482 lines  (14 CompactFactors, 16 PlaneSpectrum)
closure of PlaneColoring.BorelTransfer : 32 modules, 15974 lines
closure of BorelTransfer minus closure of Ergodicity : 2 modules, 492 lines
closure of PlaneColoring.WeakColoring : 2 modules, 210 lines (no CompactFactors, no PlaneSpectrum)
```

Three consequences, all quantitative:

1. **Prop. 4.2's own contribution to the closure is 2 modules, 492 lines.** Everything else is the
   rigidity theorem's closure. So route (e) can shrink at most ~500 lines of the forward transfer
   without touching the rigidity input — the 15 482-line block is the rigidity theorem, and by
   Theorem 1 it cannot be weakened away.
2. **The Lean statement of the rigidity input is already the sharp form (R).** The paper states
   Theorem 2.3 as "ν is Haar"; Lean states the vanishing form, which by Theorem 1 is the same
   statement — so the formalisation is already minimal and cannot be improved by restating:
   * `OAI/Analysis/PlaneSpectrum/Basic.lean:300` — `IsWild ν` = K-invariance of ν plus `ν C = 0`
     (matches Definition 2.2);
   * `OAI/Analysis/PlaneSpectrum/Ergodicity.lean:335` —
     `wild_fourier (μ) [IsProbabilityMeasure μ] (hw : IsWild μ) (z : E) (hz : z ≠ 0) :
     ∫ d, (eval z d : ℂ) ∂μ = 0`, i.e. **(R) verbatim**;
   * `Ergodicity.lean:364` — `finite_wild_fourier`, the finite-measure (unnormalised) form, which is
     what is actually applied;
   * `Ergodicity.lean:403` — `residual_fourier`, the orthogonality of the residual `b = f − p` to all
     nonzero algebraic translations, derived from `finite_wild_fourier`;
   * `OAI/Geometry/PlaneColoring/BorelTransfer.lean:59` — `projected_unit_correlation`, which is
     `residual_fourier` plus the soft `projection_coefficient` identity;
   * `BorelTransfer.lean:439/448/451` — `proper_to_borel_weak_algebraic`, `proper_to_borel_weak`,
     `proper_to_weak`.
   So the formalisation already uses the tightest available form: Theorem 1 says nothing weaker could
   have been stated, and by the same token no statement-level weakening can shorten this chain.
3. **The converse (Lemma 4.3) is separate and free**: `WeakColoring`'s closure is 2 modules,
   210 lines, with no rigidity content. Combined with §0, this says the Step-2 target decomposes into
   an expensive forward half whose cost is *entirely* Theorem 2.3, and a cheap reverse half that the
   mission does not need.

**Fact-check of the counts quoted in the brief.** The brief says "the Furstenberg–Zimmer tower, the
compact factors, the conditional expectations and 19 of the 78 Lean modules"; `results/SPINE.md` says
`MeasureTheory/CompactFactors/* (19 modules), PlaneSpectrum/* (18)`. Measured: 83 modules, of which
**14** are under `MeasureTheory/CompactFactors` and **19** under `Analysis/PlaneSpectrum` (SPINE's
"18"). So the number 19 is the size of `PlaneSpectrum`, not of `CompactFactors`; the two together are
30 modules. This matters for route (e)'s bookkeeping but not for any mathematical claim.
