# Section 7 at six colours: the full transfer from "the cyclic locus is finite near one point"

**Direction d9** (member m12, swarm smwfo9zkl). Question: which property of the cyclic locus
`L = {x : Γ_x contains a cycle}` does §7 of the paper actually consume? Answer proved below:
**far less than local finiteness.** §7 runs verbatim at every `k ≥ 3`, in particular at
`k = 6`, as soon as `L` meets *one* ball of radius `> 1` in finitely many points. Nothing in
§7 uses a palette bound: the passage of the thresholded disk averages (7.4) into the
1-skeleton of the simplex is produced by the *forest* structure of `Γ_z` off `L`, not by
`|P_x(e)| ≤ k−3`, so the "3-palette to 1-skeleton gap" does not exist as a step of §7.

Two unconditional theorems at `k = 6` come out of the same audit:

* `L` is closed (Theorem A);
* `L` is `1`-dense: `dist(y, L) ≤ 1` for **every** `y ∈ R²` (Theorem D). So no weak measurable
  six-colouring has all transition graphs acyclic: the "empty cyclic locus" alternative is
  impossible, and every point of the plane has a cyclic centre within distance `1`.

The conditional part is sharp: **if `L ∩ B(y,R)` is finite for some `R > 1`, then the whole of
§7 goes through at `k = 6`, producing a cycle of common exclusion continua of length
`ℓ ∈ {3,4,5,6}`** (Theorem B′). The hypothesis is strictly weaker than local finiteness and
strictly weaker than "one isolated cyclic centre with a gap", and §6 states the resulting
dichotomy: either that finiteness holds and §7 runs, or `L` is infinite in every ball of radius
`> 1`, in which case the printed §7 gives nothing.

Contents: §0 results · §1 setting · §2 Theorems A and D · §3 the audit (with the answer to the
"3-palette" question) · §4 Theorem B′ · §5 sharpness and vacuity · §6 the dichotomy at `k = 6`
· §7 files and commands.

Everything is checked against the paper at two independent extractions (`pdftotext -layout`
and `mutool draw -F txt`); the passages relied on are quoted verbatim in §1.3.

---

## 0. Results

Throughout `k ≥ 3`, `I = {1,…,k}`, `c : R² → I` is a **weak measurable `k`-colouring** (paper,
Definition 1.2), `Γ_x` is the transition graph of paper Definition 6.1, and
`L = {x ∈ R² : Γ_x contains a cycle}`.

> **Theorem A (every `k`).** `L` is closed. More precisely, with `𝒞_ℓ` the finite set of simple
> `ℓ`-cycles of the complete graph on `I`, `L = ⋃_{ℓ=3}^{k} L_ℓ` where
> `L_ℓ = ⋃_{C ∈ 𝒞_ℓ} ⋂_{ij ∈ C} E_{ij}` is closed and `E_{ij} = {x : ij ∈ Γ_x}`.

> **Theorem D (every `k`; unconditional at `k = 6`).** `dist(y, L) ≤ 1` for every `y ∈ R²`. In
> particular `L ≠ ∅`, and every closed ball of radius `> 1` contains a cyclic centre.

> **Theorem B′ (transfer of §7 with weakened input, every `k ≥ 3`).** Suppose there are `y ∈ R²`
> and `R > 1` with `L ∩ B(y,R)` finite. Then the conclusion of Proposition 7.1 holds at `k`:
> there are an integer `ℓ` with `3 ≤ ℓ ≤ k`, distinct labels `i_0,…,i_{ℓ−1} ∈ I`, a point
> `x ∈ B(y,R)` and a radius `ρ > 0` such that for each `j` mod `ℓ` there are a compact connected
> set `K_j ⊂ B(x,ρ)`, a direction `v_j ∈ S¹` and a sequence `q_{j,t} ∈ K_j ∖ {x}` with
>   1. `x ∈ K_j` and `K_j ∩ ∂B(x,ρ) ≠ ∅`;
>   2. `q_{j,t} → x` and `(q_{j,t} − x)/|q_{j,t} − x| → v_j`;
>   3. `H_{i_j} ∩ ∆(K_j) = H_{i_{j+1}} ∩ ∆(K_j) = ∅`, where `∆(K) = {z : min_{q∈K}|z−q| < 1 <
>      max_{q∈K}|z−q|}` and `H_i` is the closed spatial essential support of the colour class
>      `A_i`.
> At `k = 6` this is a cycle of common exclusion continua of length `ℓ ∈ {3,4,5,6}`, with the
> sliver data `K_j`, `x`, `ρ`, `v_j`, `i_j`. The proof is the paper's §7 line by line; the only
> changes are (i) the region is a closed disk and the cover obstruction is stated for any
> compact convex region of inradius `> m` (Lemma 5.1 below, a strict generalisation of paper
> Lemma 7.5 with the sharp constant `side > 2·mesh`), and (ii) `L₀ = L ∩ Q′` is a finite set of
> arbitrary cardinality instead of being enumerated by a pigeonhole over one point.

> **Theorem C (strictness, sharpness, vacuity).**
> **(a)** Theorem B′'s hypothesis is strictly weaker than local finiteness of `L` (example in
> §5.1) and strictly weaker than "some `x ∈ L` has `dist(x, L∖{x}) > 1`" (§5.4): finitely many
> cyclic centres at distance `0.1` from each other satisfy it and fail the isolation hypothesis.
> **(b)** The constant `R > 1` is the sharp constant of the printed architecture: the derived
> component-cover mesh bound is `1 + o(1)`, so a region of inradius `> 1` is required and
> nothing `≤ 1` can be obtained from the argument (§5.2).
> **(c)** The multiplicity-two hypothesis of the cover obstruction is essential, and the
> argument is not vacuous: for every `m > 0` there is an explicit relatively open cover of the
> plane with multiplicity exactly `3` and mesh `≤ m`, with exact coordinates in `Q(√3)` and a
> verifier; and at `k = 5` with `L` locally finite Theorem B′ reproduces the paper's true
> Proposition 7.1 verbatim, so no hypothesis is overreaching (§5.3, §5.5).

**Status at `k = 6`, stated exactly.**

*Unconditional*: `L` is closed and `L = L_3 ∪ L_4 ∪ L_5 ∪ L_6` with each `L_ℓ` closed; `L` is
`1`-dense, so `L ≠ ∅` and every ball of radius `> 1` meets `L`; §7 contains no palette input
and has exactly two `k`-dependencies, `α < 1/6` and `ℓ ≤ 6`; the sharpness and vacuity
statements of Theorem C.

*Conditional on `L` being finite near one ball of radius `> 1`*: the full conclusion of
Proposition 7.1 at `k = 6` (Theorem B′). §6 shows that this is the exact form of the remaining
gap for the printed architecture: either it holds (and §7 runs), or `L` is infinite in every
ball of radius `> 1` (and §7 as printed gives nothing).

---

## 1. Setting and notation

### 1.1 Paper objects used

* Definition 1.2 (weak measurable `k`-colouring): measurable `c : R² → {1,…,k}` with
  `Σ_i ∫_{B(0,R)} ∫_{S¹} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0` for every `R > 0`.
* Theorem 1.3: a proper `k`-colouring of the plane exists iff a weak measurable `k`-colouring
  does — for every `k`, in particular at `k = 6`. So the theorems below apply to six-colourings
  after one application of Theorem 1.3.
* §5: `S¹` with normalised arc measure `σ`; `R` = rotation by `κ = π/3`, `J` = rotation by
  `π/2`; colour classes `A_i`, indicators `a_i`, closed spatial essential supports
  `H_i = {q : |A_i ∩ B(q,r)| > 0 for every r > 0}`.
* Definition 6.1 and (6.1): `D_{ij}(B,h) = {q ∈ B : (c(q), c(q+h)) ∈ {(i,j),(j,i)}}` and
  `ij ∈ Γ_x` iff for every ball `B ∋ x` of positive finite radius,
  `lim sup_{h→0, h≠0} |D_{ij}(B,h)|/|h| > 0`.
* (7.1): `∆(K) = {z : min_{q∈K}|z−q| < 1 < max_{q∈K}|z−q|}` for nonempty compact `K`.
* (7.2)–(7.4), Lemmas 7.2–7.8, Proposition 7.1 of §7; quoted where used.

### 1.2 What §7 does not need

Nothing in §7 uses the circle palette `P_x` of Definition 5.1, the palette bound (5.12), the
transfer relations (5.2)/(5.3), (5.7), the rotation `R`, or the number `5`. §3 verifies this
line by line. This is the mechanism behind item (i) of the "Corrections" note in
`results/K6-BARRIER.md`.

### 1.3 The paper's own constants, verified at two extractions

`pdftotext -layout` and `mutool draw -F txt` agree on all of the following.

* §7.2: "Fix `0 < α < 1/5`, and define `q_i^ε(z) = (p_i^ε(z) − α)_+ / Σ_{k∈I}(p_k^ε(z) − α)_+`.
  The denominator is positive because the five probabilities sum to one."
* §7.2: "Choose a closed square `Q` of side ten with `∂Q ∩ L = ∅`. Such a square is obtained by
  a small translation: local finiteness leaves only finitely many points to avoid near the
  boundary of all squares in that translation family. Choose a larger closed square `Q′`
  containing `Q` in its interior, and write `L₀ = L ∩ Q′`, a finite set by Theorem 6.5."
* Lemma 7.4: total final radii "at most `|L₀|δ + m_{δ,ε} + η`".
* Lemma 7.5: "A closed square of side ten has no relatively open cover of multiplicity at most
  two and mesh at most two".
* Lemma 7.6: "They form a cover of `Q` of multiplicity at most two, since every point of `G`
  has at most two positive coordinates. We claim that the mesh of this component cover is at
  most `1 + o(1)`."
* Lemma 7.6, proof of the mesh claim: "there are a fixed constant `c > 0`, a fixed label `i`,
  and paths in `U_{n,i}` joining points at distance greater than `1 + c`."; and at the end:
  "This argument also rules out the possibility of having no core disks in `Q`."
* Proof of Proposition 7.1: "Since `L₀ ∩ Q` is finite, pass to a subsequence with a fixed
  `x ∈ L₀ ∩ int(Q)` whose core boundary loop is non-null at every index. Choose `ρ > 0` so
  small that `B(x,ρ) ⊂ int(Q)` and contains no other point of `L₀`." and "There are only
  finitely many simple cycles in the complete graph on five vertices. Pass to a subsequence
  with one chosen cycle, of length `ℓ ∈ {3,4,5}`."

---

## 2. Theorems A and D

> **Lemma 2.1.** For every `k ≥ 3` and every pair `ij`, the edge-presence locus
> `E_{ij} = {x : ij ∈ Γ_x}` is closed in `R²`.

*Proof.* Let `x_n ∈ E_{ij}` with `x_n → x`, and let `B ∋ x` be a ball of positive finite radius.
For all large `n`, `ρ_n := dist(x_n, R² ∖ B) > 0` and `B(x_n, ρ_n) ⊂ B`, hence
`D_{ij}(B(x_n,ρ_n), h) ⊂ D_{ij}(B,h)` for every `h`, so by monotonicity of `D_{ij}` in its ball
argument
`lim sup_{h→0} |D_{ij}(B,h)|/|h| ≥ lim sup_{h→0} |D_{ij}(B(x_n,ρ_n),h)|/|h| > 0`
because `x_n ∈ E_{ij}`. As `B` was arbitrary, `x ∈ E_{ij}`. ∎

> **Theorem A.** `L` is closed, and `L = ⋃_{ℓ=3}^{k} L_ℓ` with `L_ℓ` closed.

*Proof.* A graph contains a cycle iff it contains one whose vertices are distinct. A simple
cycle on `I` has length `ℓ` with `3 ≤ ℓ ≤ k`, and `Γ_x` contains it iff `x` lies in the
intersection of the closed loci `E_{ij}` of its edges. There are finitely many simple cycles on
`I`, so `L` is a finite union of finite intersections of closed sets. ∎

This is the paper's argument for `k = 5`; it uses no palette information and transfers.

> **Theorem D.** For every `k ≥ 3` and every weak measurable `k`-colouring, every closed ball of
> radius `> 1` meets `L`; equivalently `dist(y, L) ≤ 1` for every `y ∈ R²`.

*Proof.* Suppose `L ∩ B̄(y,r) = ∅` for some `r > 1`. Pick `1 < r₀ < r₁ < r` and set
`Q := B̄(y, r₀)`, `Q′ := B̄(y, r₁)`; then `Q` is compact convex with inradius `r₀ > 1` and
`L ∩ Q′ = ∅`. Run paper §7.1–§7.4 with this `Q`, `Q′` and `L₀ = L ∩ Q′ = ∅`:

* Lemma 7.4 applies with **no core disks** (`L₀` is empty): there are `ε_n ↓ 0` and finite
  families `H_n` of marked open disks with total radii `→ 0` such that `q^{ε_n}` is `G`-valued
  on `Q ∖ ⋃_{B ∈ H_n} B`, and there is a continuous `g_n : Q → G` equal to `q^{ε_n}` off the
  holes, obtained by filling the marked disks through trees (every `Γ_z`, `z ∈ Q′`, is a
  forest, since `L ∩ Q′ = ∅`).
* The first paragraph of Lemma 7.6 then gives a contradiction: the component cover
  `U_{n,i} = {z ∈ Q : (g_n(z))_i > 0}` has multiplicity at most two (a point of the
  1-skeleton has at most two positive barycentric coordinates) and mesh `≤ 1 + o(1) ≤ m` for
  any fixed `m ∈ (1, r₀)` and large `n`, contradicting Lemma 5.1 applied to `Q` (inradius
  `r₀ > m`).

So no ball of radius `> 1` can be disjoint from `L`, and `dist(y,L) ≤ 1` follows by taking
`r ↓ 1`. ∎

The paper records the "no core disks" case in one sentence ("This argument also rules out the
possibility of having no core disks in `Q`") inside the `k = 5` proof; Theorem D is the
explicit `k`-independent statement, with the quantitative radius `1`.

---

## 3. The audit: every step of §7 against `k`

| Step | Statement used | `k`-dependence | Verdict |
|---|---|---|---|
| (7.2), Lemma 7.2 | `p_i^ε(q) + p_i^ε(z) ≤ 1` for `|q−z| = 1`; support detection | none (only properness of a.e. unit pairs, i.e. Definition 1.2) | transfers |
| Lemma 7.3 | for a missing edge `ij ∉ Γ_x`, `∫_{B'} p_i^ε p_j^ε = o(ε)`; violations covered by disks of total radius `→ 0` | none (uses (6.1) and the Fourier decay of `σ̂`; `a_i ∈ L^∞`) | transfers |
| (7.4) | `q_i^ε = (p_i^ε − α)_+ / Σ(p − α)_+` | **`α < 1/k`**: positivity of the denominator uses `Σ_i p_i^ε = 1` over `k` labels, so some `p_i^ε ≥ 1/k` | paper's `α < 1/5` becomes `α < 1/6`; nothing else |
| Lemma 7.4, first part | off `L`, `Γ_z` is a forest; the positive coordinates of (7.4) form a clique in it, "therefore number at most two" | none: a forest has clique number `2` for every `k` (Mathlib `SimpleGraph.IsAcyclic.cliqueFree`; `lean/S7Audit.lean`) | **transfers; this is the passage into `G`** |
| Lemma 7.4, second part | one core disk per point of `L₀`; total radii `|L₀|δ + m + η → 0` | none beyond `|L₀| < ∞`, which is `B′`'s hypothesis | transfers |
| Lemma 7.5 | no relatively open cover of a closed square of side ten with multiplicity `≤ 2` and mesh `≤ 2` | none (plane topology) | transfers, and generalises (Lemma 5.1) |
| Lemma 7.6, multiplicity | the component cover has multiplicity `≤ 2` "since every point of `G` has at most two positive coordinates" | none: `G` is the 1-skeleton of the simplex on `k` vertices; a point of a 1-skeleton has `≤ 2` positive barycentric coordinates for every `k` | transfers |
| Lemma 7.6, mesh | mesh `≤ 1 + o(1)` | none (the constant `1` is the forbidden distance) | transfers |
| Lemmas 7.7, 7.8 | reduced circuits, midpoint detection, connected preimage crosses the annulus | none (finite-graph topology) | transfers |
| Proposition 7.1 | pick one core disk with a non-null loop; annulus around it | needs `L₀` finite (for the pigeonhole over finitely many core disks and for a positive gap), not `L` locally finite | transfers under `B′`; `ℓ ∈ {3,…,k}` |

**Two and only two `k`-dependencies in the whole of §7**: the threshold `α < 1/k` and the
range `3 ≤ ℓ ≤ k`. Neither involves palettes.

**Answer to the sprint's Step 2 question** ("say exactly which step converts a 3-palette to a
point of the 1-skeleton, or prove that no such step exists"). There is no such step, and no
3-palette is ever converted. The route is:

1. `z ∉ L` ⟹ `Γ_z` is a forest (Definition 6.1 and the definition of `L`);
2. Lemma 7.3: if `i,j` both exceed the threshold `α` at `z` and `z` is outside the marked
   disks, then `ij ∈ Γ_z`;
3. hence outside `L` and the marked disks the set `{i : q_i^ε(z) > 0}` is a clique in the
   forest `Γ_z`; it has at most two elements, and a two-element clique is an edge of `Γ_z`;
4. therefore `q^ε(z)` lies in the 1-skeleton `G`.

The palette `P_x(e)` never appears. A palette of size three at a centre `x` is irrelevant to
§7 *as such*; what matters is only that `Γ_z` be acyclic off a set that §7 can cover by disks
of total radius tending to zero. That set is `L`, and the only quantitative requirement on it
is Theorem B′'s hypothesis.

---

## 4. Theorem B′: §7 from finiteness near one region

We assume: `y ∈ R²`, `R > 1`, `L ∩ B(y,R)` is finite. Choose `r₁, r₀, m, ε` with
`1 < m < r₀ < r₁ < R` and `ε := m − 1 > 0`; put `Q′ := B̄(y, r₁)` and
`Q := B̄(y′, r₀)`, where `y′` is chosen with `|y′ − y| < r₁ − r₀` and such that
`∂Q ∩ L₀ = ∅` — possible because `L₀ := L ∩ Q′` is finite and a small generic translate `y′`
avoids the finitely many circles on which some point of `L₀` lies on `∂Q`. Then
`Q ⊂ int Q′ ⊂ Q′ ⊂ B(y,R)`, `L₀` is **finite**, `x ∈ int Q` for every `x ∈ L₀ ∩ Q` (as
`∂Q ∩ L₀ = ∅`), and the inradius of `Q` is `r₀ > m`. All references are to paper §7; changes
are flagged **[changed]**.

### Step 1. Disk averages (paper §7.1, Lemma 7.2)

For `ε > 0`, `p_i^ε(q) = (1/πε²)∫_{B(0,ε)} a_i(q+v) dv` are continuous probability
coordinates with `Lip(p_i^ε) ≤ C/ε` and `p_i^ε → a_i` in `L¹_loc` and a.e. Lemma 7.2 holds
verbatim: `p_i^ε(q) + p_i^ε(z) ≤ 1` for `|q − z| = 1`, and `q_n → q`, `ε_n → 0`,
`lim inf p_i^{ε_n}(q_n) > 0` imply `q ∈ H_i`. (Only Definition 1.2 and Lemma 4.3 are used.)

### Step 2. Threshold (paper (7.4)) — the first `k`-dependence

Fix `α` with `0 < α < 1/k` (at `k = 6`, `α < 1/6`; the paper's `α < 1/5` is the case `k = 5`).
Let `q_i^ε(z) = (p_i^ε(z) − α)_+ / Σ_j (p_j^ε(z) − α)_+`; the denominator is positive because
some `p_j^ε ≥ 1/k > α`. Then `q^ε` is continuous into the simplex on `I`, and
`q_i^ε(z) > 0 ⟺ p_i^ε(z) > α`. **No other constant in §7 depends on `k`.**

### Step 3. Holes and tree fillings (paper Lemma 7.4)

> **Lemma 4.1.** There are `ε_n ↓ 0` and finite families `H_n` of open disks with pairwise
> disjoint closures and total radii tending to zero such that, for all large `n`,
> 1. for each `x ∈ L₀` exactly one disk `B_{n,x} ∈ H_n` is designated its core disk, contains
>    `x` in its interior, and satisfies `B_{n,x} ⊂ int Q` if `x ∈ Q` and `B_{n,x} ∩ Q = ∅`
>    otherwise; different points have different core disks;
> 2. `q^{ε_n}` takes values in `G` on `Q ∖ ⋃_{B∈H_n} B`;
> 3. there is a continuous `g_n : Q ∖ ⋃_{x ∈ L₀ ∩ Q} B_{n,x} → G` equal to `q^{ε_n}` off
>    `⋃_{B∈H_n} B`.

*Proof.* Exactly paper Lemma 7.4, whose proof uses only: `Γ_z` is a forest for `z ∈ M_δ`
(compactness of the finite set `L₀` and `M_δ := Q′ ∖ ⋃_{x∈L₀} B(x,δ)`), Lemma 7.3 for the
finitely many nonedges, the finite subcover by balls `B(z,s_z)`, the tree-filling of non-core
disks, the merging of disks with intersecting closures, and the total-radii bound
`|L₀|δ + m_{δ,ε} + η`. Since `|L₀| < ∞`, taking `δ_n ↓ 0` and then `ε_n`, `η_n` small gives
total radii `→ 0`. Positions: a disk of radius `r` containing `x` lies in `B(x,2r)`, and the
positive distances from the finitely many points of `L₀` to `∂Q` give item 1. ∎

**[changed]** Nothing; this step already works with any finite `L₀`. In the paper `L₀` is finite
by Theorem 6.5; here it is finite by hypothesis.

### Step 4. The cover obstruction (paper Lemma 7.5) for a convex region

> **Lemma 5.1.** Let `Q ⊂ R²` be compact and convex with nonempty interior and inradius `> m`
> (it contains a closed disk of radius `m`). Then `Q` has no relatively open cover of
> multiplicity at most two and mesh at most `m`.

*Proof.* Compactness gives a finite subcover `U_1,…,U_N` with the same bounds; `U_a ≠ Q` since
`diam U_a ≤ mesh ≤ m < inradius(Q) = diam Q / 2`. Choose `z_a ∈ U_a` and a continuous partition
of unity `φ_a` with `φ_a > 0` only on `U_a`; set `F(z) = Σ_a φ_a(z) z_a`. Convexity gives
`F(Q) ⊂ Q`; at most two weights are positive, so `F(Q)` lies in the finite union of the
segments `[z_a,z_b]` and points `z_a`; and `|F(z) − z| ≤ Σ_a φ_a(z)|z_a − z| ≤ m`. Pick `y`
with `dist(y,∂Q) > m`. Then `z ↦ y + z − F(z)` maps `Q` into `B̄(y,m) ⊂ int Q ⊂ Q`, so
Brouwer's fixed point theorem (paper's reference [14], Theorem 1.9) gives `z` with `F(z) = y`.
Hence `{y : dist(y,∂Q) > m} ⊂ F(Q)`, a set with nonempty interior — impossible for a finite
union of segments. ∎

Paper Lemma 7.5 is the case `Q` = closed square of side ten (inradius `5 > 2`), `m = 2`.
Lemma 5.1 is strictly stronger: it gives that square case in the sharp form `side > 2m`, and it
allows a disk of radius `r₀` with `m = (1 + r₀)/2`, which is what Step 5 needs.

### Step 5. A non-null core loop (paper Lemma 7.6)

> **Lemma 6.1.** In a finite forest every clique has at most two vertices; a two-element clique
> is an edge. (Machine-checked, `lean/S7Audit.lean`.)

> **Lemma 6.2.** For all sufficiently large `n` some core disk `B_{n,x}` with `x ∈ L₀ ∩ Q` has
> a boundary loop whose `g_n`-image is not null-homotopic in `G`.

*Proof.* Otherwise, along a subsequence, all core boundary loops are null-homotopic; extending
each over its disk and pasting gives a continuous `ĝ_n : Q → G` equal to `q^{ε_n}` off the
holes. For `i ∈ I` let `U_{n,i}` be the components of `{z ∈ Q : (ĝ_n(z))_i > 0}`; `Q` and its
relatively open subsets are locally path connected, so these components are open, path
connected, and cover `Q`. Multiplicity is at most two, since a point of the 1-skeleton `G` of
the simplex on `I` has at most two positive barycentric coordinates — for every `k` (Lemma
6.1 with the clique being the support). Mesh is at most `1 + o(1)`: the paper's argument shows
that, for every fixed `c > 0`, paths joining points at distance `> 1 + c` give points
`a_n, b_n` with `p_i^{ε_n} > α`, `|a_n − b_n| ≥ 1 + c − o(1)`, limits `a,b` with `|a−b| > 1`,
`a ∈ H_i`, and then `α|A_i ∩ U| ≤ ‖p_i^{ε_n} − a_i‖_{L¹(U)} + α|E_n ∩ U| → 0` in a ball
`U ∋ a`, contradicting `a ∈ H_i`. (Only the forbidden distance `1` enters.) For large `n` the
mesh is at most `m`, while `Q` has inradius `r₀ > m`: Lemma 5.1 contradicts the existence of
the cover. ∎

### Step 6. The annulus and the limit continua (paper Lemma 7.8 and the proof of Proposition 7.1)

There are finitely many core disks (`|L₀| < ∞`). By Lemma 6.2 and a pigeonhole along a
subsequence, fix a core disk index — equivalently, since there are finitely many points of
`L₀ ∩ Q` and each core disk contains one, fix `x ∈ L₀ ∩ Q` such that **`B_{n,x}` has a
non-null boundary loop for all large `n`**. Let
`γ := dist(x, L₀ ∖ {x}) > 0` (positive since `L₀` is finite) and choose `ρ` with
`0 < ρ < min(γ/2, dist(x, ∂Q))` and `ρ > 2·diam B_{n,x}` for all large `n`; this is possible
because the diameters tend to zero. Then `B(x,ρ) ⊂ int Q` and, for large `n`, no core disk
other than `B_{n,x}` meets `B(x,ρ)` (a core disk at `x′ ∈ L₀`, `x′ ≠ x`, has diameter `< γ/2`
and centre `x′`). **[changed]** No global isolation of `x` in `L` is needed: only the finiteness
of `L₀` (which gives `γ > 0`), the vanishing of the core diameters, and the choice
`∂Q ∩ L₀ = ∅` made in Step 0.

So `g_n` is defined on the closed annulus `A_n = B(x,ρ) ∖ B_{n,x}`, and its inner boundary loop
is non-null. It therefore has a nonempty cyclically reduced circuit `W_n`; by Lemma 7.7
(midpoint detection) `W_n` contains a simple cycle, and every loop freely homotopic to a
nonzero power of `W_n` meets the midpoint `m_j` of each of its edges. There are finitely many
simple cycles on `I`; pass to a subsequence carrying one simple cycle of length `ℓ`,
`3 ≤ ℓ ≤ k`, with labels `i_0,…,i_{ℓ−1}` in cyclic order. **[changed]** `ℓ ∈ {3,4,5}` becomes
`ℓ ∈ {3,…,k}`.

For each `j`, Lemma 7.8 gives a compact connected component
`K_{n,j} ⊂ g_n^{-1}({m_j}) ∩ A_n` meeting both boundary circles of `A_n`. Pass to Hausdorff
limits `K_{n,j} → K_j ⊂ B̄(x,ρ)`. As in the paper: `K_j` is compact connected; `x ∈ K_j`
(contact points of `∂B_{n,x}`, which lie within `2·diam B_{n,x}` of `x`); `K_j` meets
`∂B(x,ρ)`; the support exclusion `H_{i_j} ∩ ∆(K_j) = H_{i_{j+1}} ∩ ∆(K_j) = ∅` holds (the value
`m_j` has two endpoint coordinates `1/2`, so `p_i^{ε_n} > α` on `K_{n,j}`; (7.2) gives
`p_i^{ε_n} ≤ 1 − α` at unit-distance points; `‖p_i^{ε_n} − a_i‖_{L¹(U)} → 0` and `|E_n| → 0`
finish); and `{|q − x| : q ∈ K_j} = [0,ρ]` by connectedness, so points of `K_j` at radii `ρ/t`
give the limiting directions `v_j`. ∎

**Theorem B′** is Step 1 + Lemma 4.1 + Lemma 6.2 + Step 6, with the point `x` and radius `ρ`
supplied by Step 6.

### Consequences

* **Corollary (isolated cyclic centre).** If some `x ∈ L` has `dist(x, L∖{x}) > 1`, then
  Theorem B′ applies with `R := dist(x, L∖{x})`; this is the case in which the conclusion can
  be taken at the cyclic centre itself.
* **Corollary (local finiteness ⟹ §7).** If `L` is locally finite (in particular under paper
  Theorem 6.5 at `k = 5`), then `L ∩ B(y,R)` is finite for every `y, R`, and Theorem B′ gives
  Proposition 7.1 for every `k`, reproducing the paper's statement at `k = 5`.
* **Corollary (Theorem D).** Running Step 5 with `L₀ = ∅` (no core disks at all) contradicts
  Lemma 5.1; hence `L ∩ B(y,R) ≠ ∅` for every `R > 1`.

---

## 5. Sharpness and vacuity tests

### 5.1 Theorem B′'s hypothesis is strictly weaker than local finiteness

Local finiteness of `L` gives `L ∩ B(y,R)` finite for every `y` and `R`, hence Theorem B′'s
hypothesis; so Theorem 6.5 (at `k = 5`, or at any `k` for which it is proved) implies the
hypothesis.

The converse fails, as a statement about closed sets:
`L = {0} ∪ ⋃_{n ≥ 1} {10n + 1/t : t ≥ 1}` is closed, `L ∩ B(0,2) = {0}` is finite (so B′'s
hypothesis holds with `y = 0`, `R = 2`), and `L` accumulates at each `10n`, so `L` is not
locally finite. Thus B′'s hypothesis is a strict weakening of local finiteness.

*Scope, stated exactly:* this is a statement about the hypothesis the printed proof consumes,
not an example of a colouring. Theorem B′ says: if a `k`-colouring's locus is finite near one
ball of radius `> 1`, then Proposition 7.1 holds for that colouring. Theorem 6.5 is one way of
producing such a ball; it is not the only one, and its extra strength is unused.

### 5.2 The constant `R > 1` is sharp for this architecture

Steps 4 and 5 need a compact convex region `Q` with `inradius(Q) > m`, where `m` is at least
the derived component-cover mesh. That mesh bound is `1 + o(1)`, and the `1` is exactly the
forbidden unit distance: the contradiction is produced by two connected points at distance
`> 1`. Hence `inradius(Q) > 1 + c` for some fixed `c > 0`, and `Q` has to fit inside the ball
of radius `R` on which `L` is finite; this is where `R > 1` comes from. No smaller constant can
be extracted from the printed argument, because the mesh bound cannot be lowered below the
forbidden distance.

### 5.3 The multiplicity-two hypothesis of Lemma 5.1 is essential

For every `m > 0` there is a relatively open cover of the plane with multiplicity exactly `3`
and mesh at most `m`, with coordinates in `Q(√3)` and an exact verifier. Let `d = 5m/8`,
`r = 4d/5 = m/2`, `ω = e^{iπ/3}`, and take all open disks of radius `r` about the triangular
lattice `Λ_d = d(Z + Zω)`.

1. **Cover:** the covering radius of `Λ_d` is `d/√3`, the circumradius of the elementary
   equilateral triangle, and `d/√3 < 4d/5` because `1/3 < 16/25`.
2. **Multiplicity ≤ 3:** if four lattice points lay within distance `r` of one point `z`, their
   pairwise distances would be `< 2r = 8d/5 < d√3`. But the lattice norms are
   `d√(a²+ab+b²) ∈ {0, d, d√3, 2d, …}`, so the lattice points at distance `< d√3` from a fixed
   `λ` are only `λ` and its six nearest neighbours, and at most three of these seven have all
   pairwise distances `< d√3` (two neighbours at angle `120°` are at distance `d√3`).
3. **Multiplicity ≥ 3:** the circumcentre of an elementary triangle is at distance
   `d/√3 < r` from its three vertices.

So Lemma 5.1's conclusion fails with `3` in place of `2` at every mesh: the paper's
multiplicity-two hypothesis is not removable, and the *forest* structure (Lemma 4.1) — hence
the finiteness of `L` near the region — is the load-bearing input of §7. Verified exactly in
`checks/verify.py` (Section A), including an exhaustive search for four-point clusters of
`Λ_d` with diameter `< 8d/5`.

### 5.4 Theorem B′ is strictly weaker than the isolation hypothesis of §4's first corollary

Take `L = {0} ∪ {1/10} ∪ ⋃_{n ≥ 1} {10n + 1/t : t ≥ 1}`. This is closed,
`L ∩ B(0,2) = {0, 1/10}` is finite, so B′'s hypothesis holds; but `dist(0, L∖{0}) = 1/10` and
`dist(1/10, L∖{1/10}) = 1/10`, and every other point is a limit or has an even smaller gap, so
**no** point of `L` has `dist(x, L∖{x}) > 1`: the isolation hypothesis fails. Hence B′'s
hypothesis is strictly weaker than "some cyclic centre is isolated with gap `> 1`", which is in
turn strictly weaker than local finiteness.

Two further weakenings that do **not** suffice for the printed architecture:

* **Nonemptiness of `L`.** By Theorem D it is true, but it gives no finiteness, so it does not
  reach B′'s hypothesis.
* **Countability of `L`.** Let `L = Z² + ({0} ∪ {1/t : t ≥ 1})`, a closed countable set. Every
  ball of radius `> 1` contains a point of `Z²` and hence infinitely many points of `L`, so
  B′'s hypothesis fails for this `L`: a proof that `L` is countable (or closed and countable)
  would not suffice for the printed architecture.

### 5.5 Vacuity test

The argument must not kill a case known to exist. Two checks:

* At `k = 5` with `L` locally finite, Theorem B′ reproduces the paper's Proposition 7.1
  verbatim (the `α < 1/5`, `ℓ ∈ {3,4,5}` instance), which is a true statement used by the
  paper. So the hypotheses of Theorem B′ are consistent with the `k = 5` theory.
* By §5.3 the cover lemma does not apply to multiplicity-three covers, so Theorem B′ does not
  accidentally prove a false statement about them; the forest argument is doing real work.
  Theorem D's constant `1` is the same mesh constant, so it is not an arbitrary choice.

---

## 6. The dichotomy at `k = 6`

By Theorem D, `L ≠ ∅` for every weak measurable six-colouring. By Theorem A, `L` is closed and
`L = L_3 ∪ L_4 ∪ L_5 ∪ L_6` with each `L_ℓ` closed. Then exactly one of the following holds.

* **(F) There are `y ∈ R²` and `R > 1` with `L ∩ B(y,R)` finite.** Then Theorem B′ gives a
  simple label cycle `i_0,…,i_{ℓ−1}` with `ℓ ∈ {3,4,5,6}`, a point `x`, a radius `ρ > 0`, and
  one compact connected exclusion continuum `K_j` per edge with both endpoint supports excluded
  from `∆(K_j)`. This is exactly the input of §8; the remaining task is the exclusion of the
  four cycle lengths at `k = 6` (the `ℓ = 6` case has no `k = 5` analogue).
* **(I) For every `y ∈ R²` and every `R > 1`, `L ∩ B(y,R)` is infinite.** Then the printed §7
  gives nothing: every region of inradius `> 1` contains infinitely many cyclic centres, so the
  disk removal of Lemma 7.4 cannot be performed with holes of total radius tending to zero, and
  the pigeonhole of Step 6 has no positive gap to work with. This is the exact obstruction to
  the printed architecture at `k = 6`.

The dichotomy is exhaustive and exclusive and holds for every weak measurable six-colouring.
What it means for the remaining work:

1. **The target is finiteness on one ball, not a locus-wide statement.** Proving local
   finiteness of `L` everywhere is sufficient but far stronger than necessary. It suffices to
   exhibit one `y` and one `R > 1` with `L ∩ B(y,R)` finite.
2. **A per-cycle analysis can halt early.** Since `L` is the finite union of the closed `L_ℓ`,
   the hypothesis (F) follows if, near some point, the ℓ-cycle loci are finite for all four
   lengths; one does not need accumulation excluded globally, and one does not need the ℓ-locus
   to be discrete everywhere.
3. **Nonemptiness is not the issue.** Theorem D settles it: `L` is `1`-dense. So the missing
   prerequisite in the paper's route at `k = 6` is not "is there a cyclic centre" but "is the
   cyclic locus finite somewhere at scale `> 1`".
4. **The palette bound is irrelevant to this step.** `|P_x(e)| ≤ 3` is used in §5 and §6 (and
   in §8's palette analysis), not in §7; the passage into the 1-skeleton is Lemma 7.3 plus
   acyclicity of `Γ_z` off `L`.

---

## 7. Files and how to check them

* `S7-INPUT.md` — this document: Theorems A and D (§2), the audit (§3), Theorem B′ (§4),
  sharpness and vacuity (§5), the dichotomy (§6).
* `checks/verify.py` — exact and numerical checks; run `python3 checks/verify.py`.
  * **A.** §5.3: the multiplicity-3 cover of mesh `≤ m` for several `m`, exact in `Q(√3)`: the
    covering radius `d/√3 < 4d/5`, an exhaustive check that no four lattice points have all
    pairwise distances `< 8d/5`, and the three-point circumcentre; plus a numerical scan of the
    covering multiplicity on a `240×240` grid (multiplicities observed: exactly `1`, `2`, `3`).
  * **B.** Lemma 6.1 by exhaustive enumeration of all `2^15` graphs on six vertices, with two
    independent acyclicity tests (union–find, and DFS back edge) and the check "acyclic ⟹ no
    triangle": `2932` forests, `26979` graphs with a triangle, no overlap; control cases show
    that the tests fire on `K_3` and do not fire on a path or a 4-cycle.
  * **C.** The `k = 6` cycle count `Σ_{ℓ=3}^6 C(6,ℓ)(ℓ−1)!/2 = 20 + 45 + 72 + 60 = 197` by two
    independent procedures (brute-force enumeration of cyclic vertex sequences modulo rotation
    and reflection, and the closed formula), needed for the pigeonhole in Step 6.
  * **D.** A numerical check of the Brouwer mechanism behind Lemma 5.1 on a disk of radius
    `2.2` with `m = 1.5`: for a multiplicity-two cover whose mesh exceeds the inradius the
    partition-of-unity image misses the centre (`min |F| = 2.2`), while for the
    multiplicity-three cover of §5.3 with mesh `1 ≤ m` the image fills the inner disk of radius
    `m` (worst distance `0.022`).
  Expected output: every line begins with `PASS`, and the last line is `all checks passed`.
* `lean/S7Audit.lean` — machine-checked on the pinned toolchain (Lean 4.33.1 with the stock
  `/opt/mathlib`, empty `LEAN_PATH` requirements beyond the preset):
  * Lemma 6.1 in the form used: if `G.IsAcyclic` and `C` is a finite clique of `G`, then
    `C.card ≤ 2` (via `SimpleGraph.IsAcyclic.cliqueFree`);
  * the threshold `α < 1/k` of Step 2: if `p : Fin k → ℝ`, `0 ≤ p i`, `Σ p = 1` and
    `α < (k:ℝ)⁻¹`, then some `p i > α`, with the `k = 6` instance (`α < 1/6`) as a corollary;
  * non-vacuity examples for both statements.
  Check with `lean lean/S7Audit.lean` (exit status `0`, no diagnostics; on a loaded machine the
  Mathlib import alone can take several minutes).
