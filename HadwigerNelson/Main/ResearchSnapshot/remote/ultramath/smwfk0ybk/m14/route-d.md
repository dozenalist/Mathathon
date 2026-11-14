# Route (d): amenability / quasi-tiling in place of the Furstenberg–Zimmer tower

**Verdict: route (d) is dead, with certificate.** The paper does not use amenability *instead of*
the tower; it uses amenability **five times**, four of them *inside* the proof of the rigidity
theorem that the tower is needed for. "Amenability instead of the tower" is a false dichotomy, and
no general theorem of the shape "amenable group action + proper colouring ⇒ measurable colouring"
holds (§3 barrier). What route (d) does yield is a sharp reduction of the target: the transfer
consumes exactly one instance of the rigidity theorem, (R) in §4, which is strictly weaker than the
paper's Theorem 2.3.

**Extraction caveat (checked, and it matters).** `pdftotext` prints Definition 2.1 as
`F = Q ∩ R, E = F(i), K = {u ∈ E : uū = 1}`. The overline does not survive extraction: the correct
reading is F = **Q̄** ∩ R (the real algebraic numbers), so E = Q̄ and K = the algebraic numbers of
modulus 1. Two independent confirmations inside the paper: (i) L1271 asserts that the algebraic unit
directions are dense in S¹, which is false for E = Q(i) (then K = {±1,±i}); (ii) L281–283 asserts
that u ↦ uⁿ is onto K, which is false for {±1,±i} when n = 3. With F = Q the whole transfer would
collapse, so this is not a cosmetic point.

Paper references are by section/lemma; `L####` are line numbers of
`pdftotext -layout attachments/here-are-three-files-ni5n/paper.pdf`
(produced here as `.scratch/paper.txt`).

---

## 1. Dependency map of the transfer (Theorem 1.3)

Theorem 1.3 (L81) states, for every k: *proper k-colouring of R² exists ⇔ weak measurable
k-colouring exists* (Definition 1.2, L64). Two halves:

| half | paper proof | what it uses |
|---|---|---|
| weak measurable ⇒ proper | Lemma 4.3 (density points, L1315) + finite-graph compactness (L1337–1345) | Fubini, Lebesgue differentiation. **No amenability, no tower, no spectral theory.** Cheap: nothing here is a candidate for a tower-free shortcut. |
| proper ⇒ weak measurable | Proposition 4.2 (L1239) | amenability **and** Furstenberg–Zimmer |

Proposition 4.2 decomposes into five steps (L1239–1310):

1. **Følner step.** Ω = closed set of proper labellings of the unit-distance graph on E, a compact
   metrisable space with a continuous action of the countable group E ⋊ K (E = additive algebraic
   numbers, K = {u ∈ E : uū = 1} = the algebraic numbers of modulus 1, Definition 2.1, L262;
   K contains all roots of unity and also infinite-order elements such as (3+4i)/5, and is dense in
   S¹ via the rational tangent-half-angle map u = (1+it)/(1−it), L1271). E ⋊ K is an extension of
   two abelian groups, hence amenable; Følner averaging of a point mass gives an E ⋊ K-invariant
   Borel probability μ on Ω. → **amenability use #1** (L1245–1248)
2. **Lemma 4.1** (L1168): H_c = {v ∈ L² : lim_{z ∈ E, z→0} ‖T_z v − v‖ = 0} is L² of a factor, its
   orthogonal projection is conditional expectation, and the operators extend to a strongly
   continuous unitary R²-representation preserving the positive cone and 1. → uses the spectral
   theorem for the discrete abelian group E and Bochner's theorem; **no amenability, no tower**.
3. **Decorrelation of the wild part.** p_i = E(f_i | F_c), b_i = f_i − p_i. The scalar spectral
   measure λ_{b_i} is K-invariant (covariance + rotation invariance of μ), gives C measure zero
   (b_i ⊥ H_c = spectral subspace on C), so **Theorem 2.3** (L299) makes it a multiple of Haar
   measure, whence ⟨b_i, T_z b_i⟩ = 0 for every z ∈ E∖{0}. → **the Furstenberg–Zimmer input**
4. Cross terms vanish because p_i ∈ H_c, b_i ⊥ H_c and H_c is translation invariant; with (4.1)
   (properness: ∫ f_i T_u f_i dμ = 0 for u ∈ K, since every u ∈ K has |u| = 1) this gives
   ∫ p_i T_u p_i dμ = 0 for u ∈ K, extended to all u ∈ S¹ by strong continuity (`dense`: algebraic
   unit directions = K are dense in S¹, L1271). This is (4.2).
5. **Sampling.** Jointly measurable fields H_i(x,ω) representing T_x p_i, plane-null exceptional
   set, one sample ω, c(x) = least i with H_i(x,ω) > 0. → uses separability + Tonelli only.

**Theorem 2.3** (K-invariant + wild ⇒ Haar) is proved in §3, and amenability is used there again:

| step | content | amenability |
|---|---|---|
| §2.2 (L345–347) | invariant mean m on the bounded functions on F/Z; the "line integral" I of (2.3) | **use #2** |
| Lemma 2.5 (L373) | wild ν ⇒ I(φ(t) f̂_ν(at)) = 0 for all a ≠ 0, φ ∈ C_c(R) | uses #2 |
| Lemma 2.7 (L479) | wildness survives the passage to relative (conditional) difference laws up any tower with property (2.6) | — (this is the tower) |
| Lemma 3.1 (L726) | compact tower: exists factor Y with X ×_Y X ergodic, built level by level | **the FZ structure theorem** |
| Lemma 3.2 (L819), §3.2 | conditional multiple averages along Følner sequences in K | **use #3** |
| Lemma 3.3 (L958), (3.13) | radial difference inequality w(|A−B|) ≤ w(A)+w(B) and Avgu∈Φ_N m(2r|Re u|) → m(r)² | **use #4** |
| Lemma 3.4 (L1011) | general position in a number field: arbitrarily large S ⊂ K ∩ N with every d₀ elements a Q-basis | — |
| Lemma 3.5 (L1043) | addition under a cap: integer combinations of lengths cost ≤ 4MH | — |
| §3.5 (L1073–1150) | syndetic set A₀ = {u : w(2r|Re u|) ≤ H}, good selections, lower bound m ≥ e^{−4M₀H} on (0, 2rc₀), contradiction with (2.4) | **use #5** (Følner sequences in the syndeticity step, L1078–1079) |

**Conclusion for the audit.** Every piece of "amenable averaging" that route (d) proposes is
already present, and the tower is what converts an averaged statement into a pointwise one:
Lemma 2.5 gives the vanishing of a *mean* of a Fourier coefficient along a line, Lemma 2.7 upgrades
it to the conditional difference law over the terminal factor, and Lemmas 3.3–3.5 turn it into a
pointwise statement. Removing the tower removes the factor over which the averaging is taken.

---

## 2. The exact step route (d) would have to supply

Let (Ω, μ) be the Følner system of step 1, a pmp action of the amenable group E ⋊ K, and let

  (∗)  "an invariant probability on proper labellings of a countable graph + amenability of the
        acting group  ⇒  a measurable proper colouring exists"

be the missing implication. Route (d) (Kieffer / Ornstein–Weiss quasi-tiling, amenability used
directly on the orbit closure) is exactly the claim that (∗) is available. **It is not:** §3 gives
a counterexample, in which the whole Følner construction of step 1 applies verbatim and the
conclusion fails. So route (d) cannot replace Theorem 2.3; the tower's job is not something
amenability can be substituted for.

Note also why the paper's own mechanism cannot be blamed on the group: E is a *fixed* countable
discrete structure and the plane's structure enters only through Lemma 4.1, which manufactures the
strongly continuous R²-action on a factor. That is the (spectral, tower-free) part; the tower enters
only through Theorem 2.3, i.e. through rigidity of measures on the compact character group D.

### 2.1 Where the average is taken (why "quasi-tiling" points at the wrong space)

The identity that does the work is (4.2): ∫_Ω (T_x p_i)(T_{x+u} p_i) dμ = 0 **for every** x ∈ R² and
every unit u. It is an inner product in L²(Ω), obtained from ⟨p_i, T_u p_i⟩ = 0 at u ∈ K plus
unitarity and the group law; nothing is averaged over the plane, and no approximation occurs. The
weak colouring is then read off one sample ω, c(x) = least i with H_i(x,ω) > 0, and (4.2) is what
makes it proper up to a null set. So the averaging takes place in the *label-space* variable ω, on
the orbit closure Ω, not in the space variable x.

A quasi-tiling or Kieffer-type argument is an average in x (or along Følner sets of the acting
group), and it cannot produce an exact identity of this form: for a class A ⊆ R² and a mollified
density p_ε = 1_A ∗ ρ_ε, p_ε(x)p_ε(x+u) > 0 holds on the open set (A + B(0,ε)) ∩ (A − u + B(0,ε))
whenever that set is nonempty, so the correlation integral is strictly positive as soon as u lies in
clos(A − A) + B(0,2ε) — a condition that has nothing to do with unit-distance properness of A. An
x-side argument therefore has to be repaired by estimates, and the target here is an equality, not
an inequality. (The paper's own 7-colouring is no counterexample: its classes are hexagonal cells
with 2r < 1 and √21 r − 2r > 1 (L95–104), so its *indicator* field does satisfy the identity
exactly — which shows that the x-side is not where the difficulty is; the difficulty is purely on
the ω-side, and there amenability is already used to the full.)

---

## 3. Barrier theorem: amenability of the acting group is not enough

**Theorem.** Let X = {0,1}^ℤ with μ = Bernoulli(1/2)^ℤ, S the shift, and G the graph on X with
edges x — Sx. Then

  (i)  χ(G) = 2;
  (ii) there is **no** μ-measurable proper 2-colouring of G;
  (iii) the Følner construction of Proposition 4.2 step 1 applies verbatim: the compact space
       Ω = {c ∈ {1,2}^X : c(Sx) ≠ c(x) ∀x} is nonempty and closed, S acts on it continuously, and
       averaging a point mass over a Følner sequence of ℤ gives an S-invariant Borel probability.

*Proof.* (i) The shift is free a.e. (the action is by coordinate permutations, and a.e. x has
trivial stabiliser), so a.e. component of G is the orbit {x + n : n ∈ ℤ} ≅ ℤ; the line with edges
n — n+1 is bipartite. Choosing a bipartition class in each component gives a proper 2-colouring
(uses choice; no regularity).

(ii) Suppose c : X → {1,2} is μ-measurable and proper, and put h = (−1)^c ∈ L²(μ), ‖h‖ = 1. Then
h(Sx) = −h(x) μ-a.e. The characters χ_S(x) = ∏_{s∈S} (−1)^{x_s}, S ⊆ ℤ finite, form an orthonormal
basis of L²(μ); with the convention (Sx)_n = x_{n+1} one has χ_S(Sx) = χ_{S+1}(x). Writing
h = Σ_S c_S χ_S, the identity h∘S = −h reads c_{S+1} = −c_S for every finite S. The map S ↦ S+1 has infinite orbits on finite subsets of ℤ
(no nonempty finite S satisfies S + k = S for k ≠ 0), so on each orbit |c_S| is a positive constant
and Σ_S |c_S|² = ∞ unless all c_S = 0. Hence h = 0, contradicting ‖h‖ = 1. ∎

(iii) is immediate: restrict any proper 2-colouring from (i) to Ω, which is closed by definition of
the product topology.

*Why the L² bound cannot be replaced by a finite check* (`barrier_check.py`, exact arithmetic):
on the finite cycle ℤ/n the equation h(x+1) = −h(x) is solvable exactly for even n, with a
1-dimensional solution space (so every finite quotient admits a solution); solving the truncated
system c_{S+1} = −c_S inside a window [−N,N] leaves one free parameter per boundary orbit, the free
dimension 3, 11, 42, 163 for N = 1,2,3,4, and the truncated solution generated by the orbit of the
empty set has squared L² norm exactly N+1. The obstruction is the L² summability, i.e. the
infinite volume — which is exactly the regime in which the paper's rigidity theorem lives.

**Consequence.** A proof of Theorem 1.3 that used only amenability + Følner averaging + Fubini would
also prove "for this pmp action of the amenable group ℤ the 2-colourable graph G has a measurable
2-colouring", which is false. Hence the rigidity input (Theorem 2.3, or its consumed instance (R) in
§4) is indispensable *for this proof strategy*, and route (d) supplies nothing that shortens it.

**Scope of the barrier (stated so it cannot be over-read).** It does not show that the transfer is
unprovable by other means, and it does not impugn the paper: the paper's setting is not a pmp action
on a probability space, and the transfer of the barrier is a statement about *every* measurable
colouring of a random environment, whereas the paper needs one colouring of the fixed countable E.
What it shows is that "amenability of the acting group" cannot be the mechanism, so the quasi-tiling
literature (Kieffer, Ornstein–Weiss) has no entry point here: those theorems need an
almost-invariant object to tile, and a single arbitrary colouring of ℝ² provides none.

---

## 4. Refinement (R): the exact rigidity instance the transfer consumes

**Claim.** Proposition 4.2 uses Theorem 2.3 only through

  **(R)**  for every finite K-invariant Borel measure λ on D with λ(C) = 0 and every u ∈ K,
           λ̂(u) = ∫_D ψ_u dλ = 0.

*Verification.* In the proof of Proposition 4.2 the only occurrence of the decay statement
"⟨b_i, T_z b_i⟩ = 0 (z ∈ E∖{0})" is at z = u ∈ K: the cross terms ∫p_i T_u b_i and ∫b_i T_u p_i
vanish by orthogonality of H_c and its complement and translation invariance of H_c (no decay
needed), and the remaining term is ∫b_i T_u b_i with |u| = 1, u ∈ K. Then ∫p_i T_u p_i = 0 for
u ∈ K follows, and the passage to all of S¹ is by strong continuity of x ↦ T_x p_i, using that the
algebraic unit directions (= K, via the rational tangent-half-angle parametrization of L1271) are dense in S¹. No *vanishing* statement is
used anywhere in §4 at an algebraic point of modulus ≠ 1: Lemma 4.1 uses Fourier coefficients at all
z ∈ E only to identify the support of a spectral measure, which is not a decay assertion.

In §3's notation (L941–957: g_z = E(ψ_z|Y), m(z) = ‖g_z‖² = f̂_{ν_Y}(z), radial because equal moduli
differ by an element of K) the instance (R) is exactly

  **m(1) = 0**,  i.e. vanishing of the radial function at radius 1 only,

whereas the paper proves m(r) = 0 for every positive r ∈ F and then reads off λ = Haar.

*Consequences, stated with their limits.*

1. Theorem 2.3 is strictly stronger than what Theorem 1.3 consumes. (R) is the right target for any
   shorter proof or cheaper formalisation of the transfer, and it is what a Lean dependency
   reduction should aim at.
2. (R) is **not** automatically a shorter *proof*. If m(1) > 0 the paper's argument runs with r = 1
   and the radii 2r|Re u| = 2|Re u|; the syndetic cover A₀ ⊂ K of §3.5 and Lemma 3.4 are then
   invoked with the number field N₀ generated by the coordinates of the finitely many q_j, so
   N₀ ≠ ℚ in general and Lemmas 3.4–3.5 do not become vacuous when r = 1. So (R) is a smaller
   *statement*, not yet a smaller *proof*. That, precisely, is the open target left by route (d).
3. A sanity check that removes the cheapest would-be counterexamples to Theorem 2.3:

   **Lemma.** The only K-fixed point of D is 0 ∈ C.
   *Proof.* d(uz) = d(z) for all u ∈ K, z ∈ E. With u = −1: d(−z) = d(z), while d(−z) = d(z)^{−1}
   for an additive character, so d(z) ∈ {±1} for all z, i.e. d ∈ Hom(E, ℤ/2). E = (algebraic
   numbers, +) is divisible, so E = 2E and Hom(E, ℤ/2) = 0; hence d = 1, i.e. d = 0 ∈ C. ∎
   Consequently a point mass δ_d is K-invariant and wild only if d ∉ C is K-fixed, which is
   impossible: every K-invariant wild λ is atomless at K-fixed points, and the naive δ_d
   counterexample to Theorem 2.3 does not exist. (It does not exclude atoms with infinite K-orbit.)

---

## 5. Note relevant to route (b) (single compact factor): the tower cannot be truncated to one level

Route (b) proposes replacing the tower of Lemma 3.1 by a single compact factor. Two independent
obstructions, the first a counterexample:

1. The classical skew product T(x,y) = (x+α, y+x) on 𝕋² with α ∉ ℚ / ℤ. Its Kronecker factor Z_k is
   the x-circle (an eigenfunction Σ a_{mn} e^{2πi(mx+ny)} satisfies (m+n,n) = (m,n), so n = 0), and
   T is an isometric-over-the-base extension of Z_k, i.e. a compact extension. But the relative
   product X ×_{Z_k} X is **not** ergodic: (x,y,y') ↦ y − y' is invariant, since (y+x) − (y'+x) =
   y − y'. So a single compact factor does not achieve the ergodicity that Lemma 3.1's terminal
   factor provides, and hence does not replace Y in Lemma 2.7.
2. Property (2.6) blocks the truncation outright. If a tower had a single nontrivial level Y over
   the trivial factor, (2.6) with W = trivial reads: for every bounded H on Y and every ε > 0 there
   are H_1,…,H_q on Y and *constants* b_r^k with ‖U_kH − Σ b_r^k H_r‖ < ε. The orbit of H is then
   contained in a fixed finite-dimensional space up to ε, uniformly in k; hence Y is an isometric
   (Kronecker) factor, and by (1) may still have non-ergodic relative product. The transfinite tower
   is therefore not a presentation artefact of the paper: the induction in Lemma 2.7 runs along
   levels that genuinely cannot be merged.

---

## 6. Falsification tests and status

| test | result |
|---|---|
| Is amenability used anywhere as an alternative to the tower, i.e. is there a step provable by amenability alone that the paper proves by FZ? | No: the five amenability uses are the Følner measure (L1245), the mean on F/ℤ (L345), and three Følner-sequence arguments *inside* Theorem 2.3 (L801, L958, L1078). Direction (d) has no entry point. |
| Does "invariant measure on proper labellings + amenable group ⇒ measurable colouring" hold? | Refuted: §3 barrier, χ(G) = 2, no measurable 2-colouring, Følner construction applies verbatim. |
| Is Theorem 2.3 needed in full by Theorem 1.3? | No: only (R) at u ∈ K, i.e. m(1) = 0 (§4). |
| Is there a K-fixed wild point mass, i.e. a cheap counterexample to Theorem 2.3? | No (§4.3). |
| Can the tower be one level? | No (§5): skew product counterexample + (2.6) forces isometry at a single level. |

**Status: direction (d) dead, with the above certificate. Named indispensable step: Theorem 2.3,
consumed only in the form (R).**

## Files
- `route-d.md` (this file)
- `barrier_check.py` — exact-arithmetic checks for §3; run `python3 barrier_check.py` (0.1 s).

---

## 7. Status of Step 2 after this direction

Consequences for the two remaining routes, with the dependency explicit.

- **Route (b) (single compact factor / maximal compact extension): blocked** by §5. The tower is
  not a presentation artefact: one level forces an isometric factor by (2.6), and the relative
  product over the Kronecker factor can fail to be ergodic (skew product).
- **Route (e) (Lean closure): retargeted.** The single consumer of the rigidity chain is
  `OAI/Geometry/PlaneColoring/BorelTransfer.lean:61`, at `z = kCoeff b` with `b : K`, i.e. at a
  unit direction. The chain is
  `residual_fourier` (`Analysis/PlaneSpectrum/Ergodicity.lean:403`) ← `finite_wild_fourier` (:364)
  ← `wild_fourier` (:335) ← `ergodic_wild_fourier` (:52) ← `OAI/MeasureTheory/CompactFactors/*`
  + `RadialEnergy` + `ConditionalSpectrum`. So the closure reduction should be attempted against
  the |z| = 1 instance (R), not against the paper's Theorem 2.3. Caveat: (R) is a smaller statement
  but not automatically a smaller proof (§4.2), so the reduction must be measured, not assumed.
- **Route (c) (definability): untouched here.** Nothing in this direction bears on it.
- **What would change the verdict on route (d):** a proof of (R) that uses only amenability, or an
  argument showing the barrier of §3 cannot be transported to the paper's non-pmp setting. Neither
  is in hand; the barrier's scope paragraph is deliberately narrow.
