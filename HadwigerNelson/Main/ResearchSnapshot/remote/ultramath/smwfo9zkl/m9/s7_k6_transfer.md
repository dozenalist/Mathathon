# §7 at six colours: the transfer theorem, the conversion step, and the cyclic-centre input

Member m9, swarm `smwfo9zkl`. Direction d1: make §7 of the Hadwiger–Nelson five-colour proof
available at six colours, or prove it cannot be.

Notation and numbering are the paper's (`attachments/here-are-three-files-ni5n/paper.pdf`).
`k` is the number of labels, `I = {1,…,k}`, `R` is rotation by `κ = π/3`, `A_i = c^{-1}(i)`,
`a_i = 1_{A_i}`,
`H_i` the closed spatial essential support of `A_i`, `P_x` the maximal palette at centre `x`
(Definition 5.1), `D_ij(B,h)` the transition set of §6.1, `Γ_x` the transition graph
(Definition 6.1), and

```
L = L_k = { x ∈ R² : Γ_x contains a cycle }.
```

Palette bound at `k` labels: `1 ≤ |P_x(e)| ≤ k−3` a.e. (`results/K6-BARRIER.md` §1), so `≤ 3`
at `k = 6`.

## 0. Results

* **Theorem A (not stated in the paper; every `k`, unconditional).** For every `k` and every weak
  measurable `k`-colouring, `L_k` meets every closed square of side ten. In particular `L_k ≠ ∅`.
  *Consequence at `k = 6`: a six-colouring does have a cyclic centre. The nonemptiness that the
  paper's route was said to be missing at `k = 6` is not missing — it is automatic.* §4.
* **Theorem B (§7 transfer at `k = 6`).** If the cyclic locus has finitely many points in one
  closed square of side ten, then Proposition 7.1 holds verbatim at `k = 6` with `ℓ ∈ {3,4,5,6}`.
  §5.
* **Theorem C (the conversion step, answered exactly).** §7 uses no palette-cardinality bound at
  all. The step that turns three labels into a point of the 1-skeleton is *not* a palette→simplex
  map: it is the statement that the **thresholded** label set is a clique in the transition graph
  of a nearby centre, and that a clique in a forest has at most two vertices. Stated and proved as
  Lemma 3.1/3.2 and machine-checked (`card_le_two_of_isClique_of_acyclic`). §3.
* **Theorem D (weakest sufficient statement).** The exact input §7 consumes is
  *(F) one closed square of side ten with finitely many cyclic centres in it and none on its
  boundary*, which is strictly weaker than Theorem 6.5's local finiteness and strictly stronger
  than Theorem A's nonemptiness. §6.
* **Machine-checked:** the §7 geometric engine (`PlanarCover.compact_open_cover_impossible`,
  already generic in the label type, together with the new label-generic
  `graph_map_large_positive_generic`) and the conversion step, at six labels:
  file `k6_s7_engine.lean`, standard axioms only. §9.
* **Honest boundary.** §7 is *not* where six colours fail. With Theorem B in hand the route at
  `k = 6` reduces to §8 with a cycle of length `ℓ ∈ {3,4,5,6}`, and there the paper uses `|P| ≤ 2`
  explicitly (§8.2) and has no argument for `ℓ = 6`. §7.

## 1. The three inputs of §7 and their `k`-dependence

§7 is built from four analytic lemmas (§7.1), one geometric cover lemma (§7.3), two graph lemmas
(§7.4) and the pasting construction (§7.2). I checked each against the literal statements.

**(1.1) Disk averages, paper p. 43.** `p_i^ε(q) = (1/πε²)∫_{B(0,ε)} a_i(q+v) dv`,
`Σ_i p_i^ε ≡ 1` over the `k` labels, `Lip(p_i^ε) ≤ C/ε`, `p_i^ε → a_i` in `L¹_loc` and a.e.
No `k`-dependence; the `k`-sum is used only through `Σ = 1`. In the Lean development this whole
layer is stated for arbitrary `k` (`DiskAverages.lean`: 15 occurrences of `{k : ℕ}`, none of
`Fin 5`).

**(1.2) Lemma 7.2 (unit-pair inequality), paper p. 44, `k`-free.**
For `|q−z| = 1` and every label `i`: `p_i^ε(q) + p_i^ε(z) ≤ 1`. Proof: for a.e. translation
`h ∈ B(0,ε)` both `q+h`, `z+h` are typical, and two typical points at unit distance have
different colours (Lemma 4.3, which is stated and proved for every `k`). The second half:
`q_n → q`, `ε_n → 0`, `lim inf_n p_i^{ε_n}(q_n) > 0 ⟹ q ∈ H_i`.
Machine-checked for arbitrary `k`: `diskAverage_unit_pair` (DiskAverages.lean), and the (7.7)
support-exclusion mechanism it feeds, `diskAverage_support_exclusion` (ContinuumLimits.lean), whose
label type is `Fin k` with `k` a variable.

**(1.3) Lemma 7.3 (a missing edge has small overlap), paper p. 44, `k`-free.**
If `ij ∉ Γ_x` there is a ball `B ∋ x` such that for all `B'' ⊂ B' ⊂ B`,
`∫_{B'} p_i^ε p_j^ε = o(ε)`, and the set `{q ∈ B'' : p_i^ε(q) > α, p_j^ε(q) > α}` is covered by
finitely many open disks of total radius `→ 0`. Proof uses only the negation of (6.1) and the
Fourier decay (6.3) of the normalised circle measure. No `k`.

**(1.4) The threshold (7.4), paper p. 44 — first `k`-dependence, harmless.**
`q_i^ε(z) = (p_i^ε(z) − α)_+ / Σ_l (p_l^ε(z) − α)_+`, with `0 < α < 1/5` in the paper;
`q_i^ε(z) > 0 ⟺ p_i^ε(z) > α`. The paper's justification "the denominator is positive because
the five probabilities sum to one" is the estimate `Σ_l (p_l^ε − α)_+ ≥ 1 − kα`, so the correct
condition at `k` labels is

  **`0 < α < 1/k`; at `k = 6`, `α < 1/6`.**

(Lean, `k = 5`: `thresholdTotal_pos` proves exactly `1 − 5α ≤ thresholdTotal`.) Nothing else
changes.

**(1.5) The target graph `G`, paper p. 44 — no `k`-dependence.**
`G` is the one-skeleton of the simplex of probability vectors on `I`, i.e. `{q : |supp q| ≤ 2}`.
A point of it has at most two positive barycentric coordinates for every `k`. See §3.

**(1.6) The square `Q` and `L₀`, paper p. 44 — second `k`-dependence, the substantive one.**
The paper chooses a closed square `Q` of side ten with `∂Q ∩ L = ∅` and sets
`L₀ = L ∩ Q'` (finite by Theorem 6.5). Finiteness of `L₀` is used for: the radius budget
`Σ_{x∈L₀} δ → 0`; "no final disk contains two distinct points of `L₀`"; and the final choice of a
subsequence with a fixed core point `x` and radius `ρ` containing no other point of `L₀`. At
`k = 6` Theorem 6.5 is not available, so this is exactly the missing input. §5, §6.

**(1.7) Lemma 7.4 (small holes and tree fillings), paper pp. 44–46 — no `k`-dependence given
(1.6).** The only label-count quantities are: the number of non-edges of `Γ_z`, which is
`C(k,2) < ∞` (at `k = 6`, 15 instead of 10 — a finite number of non-edges is all that is used),
and the conclusion "at most two positive coordinates". The tree filling uses that the positive
coordinates form a clique in a forest, hence span at most one edge, hence the connected boundary
image lies in a single finite tree, which is contractible.

**(1.8) Lemma 7.5 (cover obstruction on a square), paper p. 46 — no `k`-dependence, and
machine-checked in a label-general form.** A closed square of side ten has no relatively open
cover of multiplicity at most two and mesh at most two. The paper's proof is Brouwer plus
`|F(z)−z| ≤ mesh`. In the Lean development the corresponding statement is
`PlanarCover.compact_open_cover_impossible`, whose index type `ι` is an arbitrary type — the
label set never appears. My `graph_map_small_mesh_impossible_generic` composes it with the
graph-space fact for an arbitrary finite label type.

**(1.9) Lemma 7.6 (non-null core loops), paper p. 47 — no `k`-dependence.** Uses only the
component cover of `{g_{n,i} > 0}`, its multiplicity (at most two positive coordinates), and the
mesh bound from Lemma 7.2. Note the paper's own closing remark: *"This argument also rules out
the possibility of having no core disks in `Q`."* That remark is the whole content of Theorem A.

**(1.10) Lemmas 7.7, 7.8, and the proof of Proposition 7.1, paper pp. 47–50 — no `k`-dependence
except the cycle length.** Lemma 7.7 is graph theory on an arbitrary finite connected simple
graph; Lemma 7.8 is planar topology. The one place `k` enters is

  *"There are only finitely many simple cycles in the complete graph on five vertices. Pass to a
  subsequence with one chosen cycle, of length `ℓ ∈ {3,4,5}`"* (paper p. 49),

so at `k` labels `ℓ ∈ {3,…,k}`, and at `k = 6`, **`ℓ ∈ {3,4,5,6}`**. Finiteness is all that is
used, so nothing else changes.

**Summary of the audit.** §7 depends on `k` in exactly three places: (i) the numerical threshold
`α < 1/k` (1.4); (ii) the *number* of non-edges, `C(k,2) < ∞` (1.7); (iii) the cycle length bound
`ℓ ≤ k` (1.10). It has exactly one substantive dependence, the finiteness of `L₀` (1.6), and
**no dependence on the palette-cardinality bound `|P_x(e)| ≤ k−3`.**

## 2. Where the palette bound *is* used (and so where six colours really fail)

For contrast, and to make the audit non-vacuous, the printed uses of `|P| ≤ 2` are:

* §5.4 / Proposition 5.6 itself (`k−3 = 2` at `k = 5`).
* Theorem 6.5, triangle case: "a nonempty subset of the three triangle labels of size at most two
  lies in some triangle edge". At `k = 6` a palette of size 3 can avoid all three edges.
* Theorem 6.5, four- and five-cycle cases: "a palette not containing `X` has size at most two, …
  leaving precisely the two diagonals".
* §8.2, five-cycle exclusion: *"The palette size bound (5.12) and (8.1) imply that almost every
  palette is a pair"* — false at `k = 6`, where the bound is 3.
* §8.4/§8.5, triangle interface: the outsider set `P_x(e) ∩ (I∖T)` is a singleton, i.e.
  `|P| ≤ 1 + 3 = 4`; at `k = 6` it can be a 2-element set (`results/K6-BARRIER.md` §3).

None of these is in §7. The three failures at `k = 6` are therefore all *outside* §7: local
finiteness (§6), and the §8 exclusions.

## 3. The conversion step, exactly

The question posed for this direction was: *a 3-palette gives three positive barycentric
coordinates, while a point of the 1-skeleton has at most two; say exactly which step converts a
3-palette to a point of the 1-skeleton, or prove that no such step exists.*

**Answer: no step converts a palette. The palette is never converted, because §7 does not use
palettes.** The vector `q^ε(z)` is not the palette of anything: it is a normalised threshold
average of the *disk averages at the single point `z`*, and the alternatives offered by a
3-palette are irrelevant. The step that produces the 1-skeleton point is the following.

**Lemma 3.1 (clique in a forest).** Let `G` be a simple graph on `I` that is acyclic (a forest),
i.e. containing no cycle. Let `S ⊆ I` be such that every two distinct `i,j ∈ S` are joined by an
edge of `G`. Then `|S| ≤ 2`.

*Proof.* Three distinct pairwise adjacent vertices span a triangle, which is a cycle (a
`3`-cycle); acyclic graphs have no cycles. ∎
Machine-checked: `card_le_two_of_isClique_of_acyclic` (and the `Fin 6` instance
`k6_card_le_two_of_isClique_of_acyclic`).

**Lemma 3.2 (the conversion step).** Let `0 < α < 1/k`, `ε > 0`, and let `z_* ∈ R²` have `Γ_{z_*}`
a forest. Suppose `z ∈ R²` is such that for every non-edge `{i,j}` of `Γ_{z_*}`,
`¬(p_i^ε(z) > α ∧ p_j^ε(z) > α)`. Then

  `S_ε(z) := { i ∈ I : p_i^ε(z) > α }` is a clique of `Γ_{z_*}` and `|S_ε(z)| ≤ 2`,

equivalently `q^ε(z)` is a point of the 1-skeleton `G` of the simplex.

*Proof.* By hypothesis no pair of elements of `S_ε(z)` is a non-edge of `Γ_{z_*}`, i.e. every pair
is an edge (distinct elements being distinct labels). Apply Lemma 3.1. ∎

So the passage "three labels above threshold" → "point of the 1-skeleton" runs through
**acyclicity of one single transition graph `Γ_{z_*}` at a nearby centre**, never through
`|P_x(e)| ≤ 2`. Three labels can all exceed `α` at `z` only if `Γ_{z_*}` contains a triangle —
that is, only if `z_*` is close to the cyclic locus. This is the precise sense in which

  **§7 is available at `k` labels if and only if the core disks can be placed finitely**,

i.e. if and only if cyclic centres can be avoided everywhere except in a finite set — which is
(1.6) and nothing else.

**Remark 3.3 (no palette-level replacement exists).** A tempting alternative at `k = 6` would be
to short-circuit the acyclicity hypothesis with an explicit continuous map of the simplex to its
1-skeleton, e.g. "keep the two largest coordinates". That cannot work, and this is provable:

  *Let `c` be a weak measurable `k`-colouring. For every `ε > 0`, every `α ∈ (0,1/k)` and every
  closed square `Q` of side ten there is **no** continuous `g : Q → G` (`G` the 1-skeleton of
  `Δ^{k−1}`) with `g_i(q) > 0 ⟹ p_i^ε(q) > α` for all `i` and `q`.*

Indeed such a `g` is a continuous graph-valued map of the disk, so it has a positive-coordinate
component of diameter `> 2` (machine-checked: `graph_map_large_positive_generic`, any finite label
type); then Step 5 of the proof of Theorem A (with no holes, hence `E_n = ∅`) produces `α|A_i∩U| = 0`
for a point `a ∈ H_i`, a contradiction. So the graph-valued map of §7 cannot be manufactured from
the thresholded vector alone: the excision of cyclic centres is essential, and only the acyclicity
of `Γ_{z_*}` certifies it. (Consistently, for `k ≥ 4` no retraction of `Δ^{k−1}` onto its
1-skeleton exists: `H₁` of that graph is `ℤ^{(k−1)(k−2)/2}` while `H₁(Δ^{k−1}) = 0`.) Note this
no-go does not over-kill: it is a statement about maps compatible with one fixed colouring's disk
averages, and it is exactly what forces §7 to excise `L`.

## 4. Theorem A: cyclic centres exist at every `k`, unconditionally

**Theorem A.** Let `k ≥ 1` and let `c` be a weak measurable `k`-colouring (§4 of the paper). Then
`L_k = {x : Γ_x contains a cycle}` meets every closed square of side ten.

*Proof.* Suppose `Q` is a closed square of side ten with `L_k ∩ Q = ∅`. Then `Γ_z` is a forest for
every `z ∈ Q`. Run the §7 construction with the core set empty. Choose `α ∈ (0,1/k)`.

*Step 1 (local graph-valuedness).* For `z ∈ Q` and each non-edge `{i,j}` of the forest `Γ_z`,
Lemma 7.3 gives `s_z > 0` such that the simultaneous violation set
`{q ∈ B(z,s_z) : p_i^ε(q) > α, p_j^ε(q) > α}` admits finite open disk covers of total radius
`m_{z,ε} → 0` (`ε ↓ 0`). There are finitely many non-edges, so one radius works for all of them.
The balls `B(z,s_z)`, `z ∈ Q`, cover the compact set `Q`; take a finite subcover and its Lebesgue
number `λ > 0`, and mark all disks from the finitely many covers. The total marked radius
`m_ε → 0`.

*Step 2.* At `q ∈ Q` outside all marked disks, let `B(z,s_z) ∋ q` be a member of the subcover.
Every non-edge of `Γ_z` is non-violated at `q`, so by Lemma 3.2 `|{i : p_i^ε(q) > α}| ≤ 2` because
`Γ_z` is a forest. Hence `q^ε` maps `Q` minus the marked disks into the 1-skeleton `G`.

*Step 3 (pasting).* Each marked disk that meets `Q` has diameter `< λ`, so its closed disk lies in
one member `B(z,s_z)` of the subcover; `q^ε` maps its boundary into the realisation of the forest
`Γ_z ∩ {edges spanned by a 2-point clique}`, whose image is connected, hence lies in one finite
tree of `Γ_z`, which is contractible. Extend continuously over the disk with values in that tree,
and restrict to `Q` if the disk crosses `∂Q`. The disks have pairwise disjoint closures and the
family is finite (merge overlaps as in the paper's Lemma 7.4), so pasting gives a continuous

  `g : Q → G` with `g = q^ε` off the holes, and `g_i(q) > 0 ⟹ p_i^ε(q) > α` for `q` off the holes.

*Step 4 (multiplicity two).* `g` takes values in `G`, so at most two coordinates of `g(q)` are
positive; hence the family of connected components of the relatively open sets
`U_i = {q ∈ Q : g_i(q) > 0}`, `i ∈ I`, is a relatively open cover of `Q` of multiplicity at most
two. (Every `g(q)` has a positive coordinate because `Σ_i g_i ≡ 1`.)

*Step 5 (mesh).* If a component of `U_i` contains `a,b` at distance `> 1 + c`, then (as the paper
proves, replacing points in holes by boundary points and using that `g = q^ε` there)
`p_i^ε(a_n) > α` and `p_i^ε(b_n) > α` with `|a_n − b_n| ≥ 1 + c − o(1)`. Passing to limits,
Lemma 7.2 gives `a ∈ H_i` with `|a − b| > 1`. For `z` in a small ball `U` about `a` and all large
`n`, `|z − a_n| < 1 < |z − b_n|`, so the path in the component meets the circle of radius one
about `z` in a point `w` with `p_i^ε(w) > α`; then Lemma 7.2 gives `p_i^ε(z) ≤ 1 − α` for every
`z ∈ U ∖ E_n`, where `|E_n| → 0` is the union of the `(1±r)`-annuli of the holes (paper (7.6)).
On `A_i ∩ U` we have `a_i = 1`, so `α|A_i ∩ U| ≤ ‖a_i − p_i^ε‖_{L¹(U)} + α|E_n ∩ U| → 0`,
contradicting `a ∈ H_i`. Hence for large `ε` the mesh is at most two.

*Step 6.* Lemma 7.5 says a closed square of side ten has no relatively open cover of multiplicity
at most two and mesh at most two. Contradiction. ∎

**Corollary A'.** Every weak measurable `k`-colouring has a cyclic centre, `L_k ≠ ∅`, and every
point of the plane is within distance `5√2` of one.

**Corollary A'' (six colours).** Let `k = 6`. If the plane has an unrestricted proper
6-colouring, then by Proposition 4.2 (proved there for every positive integer `k`) it has a weak
measurable 6-colouring, and hence a cyclic centre: `L_6 ≠ ∅`.

**Consistency (no over-kill).**
* At `k = 5` Theorem A says that the closed locally finite set `L` of Theorem 6.5 meets every
  side-ten square — true and weaker than Theorem 6.5.
* The argument is independent of the palette bound, so it cannot be an "accident of `k = 5`".
* `k = 7`: in Isbell's hexagonal 7-colouring (hexagons of side `s ∈ (0.387, 0.5)` in the
  triangular lattice of spacing `√3·s`, coloured by `i + 3j mod 7`, which is proper because the
  minimal non-zero kernel vector has length `√7·√3·s > 1 + 2s`), at a triple point `z` three
  distinct colours meet, and for each pair the transition set contains a strip of width `|h|` and
  length comparable to `s` inside any ball about `z`; hence each of the three pairs is an edge of
  `Γ_z` and `Γ_z` contains a triangle. So `L` contains the triple-point lattice (a honeycomb of
  nearest-neighbour distance `s = 0.4 < 10`), and meets every side-ten square: Theorem A holds in
  a case known to exist.

## 5. Theorem B: §7 at six colours

**Theorem B.** Let `k = 6`, let `c` be a weak measurable 6-colouring, and assume

  **(F)** there are closed squares `Q ⊂ int Q'` of side ten (for `Q`) with `∂Q ∩ L = ∅` and
  `L ∩ Q'` finite.

Then there exist `ℓ ∈ {3,4,5,6}`, distinct labels `i_0,…,i_{ℓ−1} ∈ I`, `x ∈ R²`, `ρ > 0`, and for
each `j` a compact connected `K_j ⊂ B(x,ρ)`, a direction `v_j ∈ S` and points
`q_{j,n} ∈ K_j ∖ {x}` with `q_{j,n} → x`, `(q_{j,n}−x)/|q_{j,n}−x| → v_j`, such that

  `x ∈ K_j`, `K_j ∩ ∂B(x,ρ) ≠ ∅`, and `H_{i_j} ∩ Δ(K_j) = H_{i_{j+1}} ∩ Δ(K_j) = ∅`.

*Proof.* This is the paper's proof of Proposition 7.1 (pp. 42–50) with three substitutions and
otherwise verbatim: `α ∈ (0,1/6)` (1.4); the finite set `L₀ = L ∩ Q'` supplied by (F) instead of
by Theorem 6.5 (1.6); the cycle length bound `ℓ ∈ {3,…,6}` (1.10). The finite number of non-edges
`C(6,2) = 15` replaces 10 (1.7). Every other input — Lemmas 7.2, 7.3, 7.5, 7.6, 7.7, 7.8 — is
label-blind by §1, and the multiplicity-two step is Lemma 3.1/3.2. ∎

Combined with Theorem A: **at `k = 6`, (F) `⟹` a cycle of exclusion continua of length 3, 4, 5 or
6.** So the printed route to `χ(R²) ≥ 7` at six colours needs, in §7, only (F) — not
nonemptiness, not the palette bound, not any new geometry.

## 6. Theorem D: the weakest sufficient statement, and what (F) is not

Theorem B's hypothesis (F) is what the construction literally consumes; §1 identifies the four
places. It is worth recording its strength:

* **(LF) `L` locally finite** (Theorem 6.5 at `k = 5`) `⟹ (F)`: choose `Q`, `Q'` and a small
  translation with `∂Q ∩ L = ∅`. So (F) is *strictly weaker* than local finiteness — it asks only
  that one square contain finitely many cyclic centres.
* **(F) `⟹ L ≠ ∅`** (Theorem A gives a point of `L` in every side-ten square, so the finite set
  `L₀` is nonempty). So the paper's dichotomy "nonempty or locally finite" collapses: nonemptiness
  is automatic, and (F) is the only question.
* **(F) is *not* implied by Theorem A.** A closed set meeting every side-ten square may be
  infinite in every square (e.g. a dense set, or `Z²` scaled down), so Theorem A alone does not
  give §7.

Why (F) and not something weaker? In the paper's Lemma 7.4 the core disks are excised and then
refilled; with infinitely many core boundaries accumulating in `Q` the pasted map need not be
continuous at accumulation points, and the radius budget `Σ_{x∈L₀} δ` is no longer finite. I know
of no variant of §7 that survives an infinite accumulating core: *within this method* finiteness
in one square is used essentially. This is a statement about the method, not a proof that no other
method works, and I record it as such.

## 7. What §7 does not settle

Theorem B feeds §8 with `ℓ ∈ {3,4,5,6}` at `k = 6`. §8 is where the `k = 6` route now stops:

1. **`ℓ = 6` is a new case.** The paper's §8 excludes `ℓ = 3,4,5` only.
2. **§8.2 uses the palette bound.** For the five-cycle it needs "almost every palette is a pair";
   at `k = 6` a palette may have three labels, so the state count changes from two diagonals to
   the admissible 2- and 3-subsets.
3. **§8.4/§8.5 use `|P ∩ (I∖T)| = 1`** at a triangle interface; at `k = 6` it can be 2
   (`results/K6-BARRIER.md` §3).

So the answer to the sprint question is: **§7 *is* available at six colours, up to the finiteness
of the core in one square; the `k = 6` obstruction has moved to §8.** Two consequences worth
recording:

* Theorem A makes Step 1 of the sprint's plan explicit: the cyclic locus at `k = 6` is nonempty
  and thick at scale ten, so any two-centre CSP built on top of §7 has an input. What is missing
  for that is (F).
* A proof of (F) needs only one cycle case at one point, not all of them: by Theorem A the locus
  is nonempty, so if the triangle locus (say) were known to be locally finite and to contain an
  isolated point, (F) would follow by translating a square of side ten onto it.

## 8. Vacuity tests

The rules for this sprint ask that every no-go be tested against a case known to exist. There are
three things to test.

**(8.1) Theorem A does not over-kill.** It must hold in a colouring known to exist. Isbell's
hexagonal 7-colouring (hexagons of side `s = 0.4`, spacing `L = √3·s ≈ 0.6928`, colour
`i + 3j mod 7`; proper because the minimal non-zero kernel vector has length `√7·L ≈ 1.833 > 1+2s
= 1.8`) satisfies it. Numerically (`hexcheck.py`, exact colouring, 240 000 sampled unit pairs):

* no same-colour unit pair was found (consistent with properness);
* at a triple point `x = (e₁+e₂)/3` the colours `0,1,3` meet and all three pairs are transition
  edges: `limsup D/|h| ≈ 0.73, 0.126, 0.122`, so `Γ_x` contains a triangle and `x ∈ L`;
* on a cell edge (`x = e₁/2`) `Γ_x` is a single edge; at a cell centre `Γ_x` is empty.

So `L` contains the triple-point lattice, which is `≈ 0.4`-dense and therefore meets every side-ten
square. Theorem A is consistent, and its conclusion "`L` is thick at scale ten" is exactly what
happens in the one colouring of the plane we can write down.

**(8.2) Hypothesis (F) of Theorem B is non-vacuous, and does not by itself prove anything.**
In the same colouring `L` is the (locally finite) triple-point lattice, so (F) holds at `k = 7`.
Hence (F) is satisfiable in a case where a colouring exists, so (F) alone cannot yield
`χ(R²) ≥ 7`: as recorded in §7, the `k = 6` content has to come from §8. This is the sharp sense in
which Theorem B is a transfer theorem and not a proof.

**(8.3) Remark 3.3's no-go does not over-kill.** It forbids continuous graph-valued maps
compatible with a *fixed* colouring's disk averages, which is a class that provably contains no
member; it says nothing about colourings, so it cannot delete a known case.

## 9. Machine-checked files and how to check them

`k6_s7_engine.lean` (this directory), checked with the pinned toolchain:

```
cd "$REPO" && source scripts/env4341.sh
cd .ultramath/smwfo9zkl/m9
lean -o k6_s7_engine.olean k6_s7_engine.lean
LEAN_PATH="$LEAN_PATH:." lean check_engine.lean     # prints the axioms
```

Contents (all standard axioms `[propext, Classical.choice, Quot.sound]`, no `sorryAx`):

| name | what it says |
|---|---|
| `graphRealization_positive_two` | at a point of the graph realization of **any** simple graph, three positive coordinates force two indices to be equal (at most two positive coordinates) |
| `card_le_two_of_isClique_of_acyclic` | Lemma 3.1: a clique in an acyclic graph has at most two vertices — the conversion step |
| `graph_map_small_mesh_impossible_generic` | for **any** finite `V`, a continuous map `F` of the closed radius-5 disk into `GraphSpace (⊤ : SimpleGraph V)` whose every positive-coordinate preconnected set has diameter `≤ 2` is impossible: its positive-coordinate component cover has multiplicity `≤ 2` and mesh `≤ 2`, contradicting `PlanarCover.compact_open_cover_impossible` (Lemma 7.5, whose index type is arbitrary) |
| `graph_map_large_positive_generic` | the same statement positively, for any finite `V` |
| `k6_graph_map_large_positive`, `k6_card_le_two_of_isClique_of_acyclic` | the `V = Fin 6` instances |
| `K6.thresholdTotal_pos` | (7.4) at six labels: the denominator is positive whenever `α < 1/6` (the paper's `α < 1/5` estimate is `1 − 5α ≤ Σ`; at six labels it is `1 − 6α ≤ Σ`) |
| `K6.thresholdMap_pos`, `K6.thresholdMap_sum` | `q^ε_i(q) > 0 ⟺ p_i^ε(q) > α`, and `Σ_i q^ε_i ≡ 1`, at six labels |
| `K6.threshold_support_card_le_two` | the six-label conversion step end to end: if every above-threshold pair is an edge of an acyclic graph on `Fin 6`, the thresholded support has at most two labels |

The file imports only `OAI.Geometry.PlaneColoring.PlanarCovers` (the cover obstruction and the disk
averages) and `OAI.Geometry.PlaneColoring.GraphRealization` (the graph space), so it rechecks
without the §4 transfer machinery.

That is: **§7's geometric engine is machine-checked at six labels.** The remaining content of
Theorems A and B is analytic (§7.1's four lemmas), and their label-genericity is recorded
above and confirmed by the Lean development's own `k`-generic statements
(`diskAverage_unit_pair`, `diskAverage_support_exclusion`, `continuum_limit_support_exclusion` are
all stated for `{k : ℕ}`).

## 10. References into the paper

* p. 33 Proposition 5.6 (palette bound `|P| ≤ 2` at `k = 5`, used in §5, §6, §8 — not in §7).
* p. 34 Definition 6.1 and (6.1) (transition graph), Lemma 6.2 and (6.3).
* p. 37 Theorem 6.5 (local finiteness), triangle case p. 37–38, four-cycle pp. 38–40,
  five-cycle pp. 40–42.
* p. 42 (7.1) straddling region, Proposition 7.1; p. 43 disk averages; p. 44 Lemma 7.2,
  Lemma 7.3, (7.3), (7.4); pp. 44–46 Lemma 7.4; p. 46 (7.6), Lemma 7.5; p. 47 Lemma 7.6,
  (7.7); pp. 47–48 Lemma 7.7; p. 49 Lemma 7.8; pp. 49–50 proof of Proposition 7.1.
* p. 25 Lemma 4.3 (density-point properness, every `k`); p. 24 Proposition 4.2 (every `k`).
* p. 51 §8.1 Lemma 8.1; p. 51 §8.2 five-cycle exclusion (uses (5.12)); pp. 52–54 §8.3–8.5.
