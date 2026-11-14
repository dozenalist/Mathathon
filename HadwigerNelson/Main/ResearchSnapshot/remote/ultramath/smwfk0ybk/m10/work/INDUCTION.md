# The induction lemma at k = 6: the bridge, proved; the two inputs it does not have

Member m10, direction d2 (D3, INDUCTION LEMMA). Everything below is read off the paper
(`attachments/here-are-three-files-ni5n/paper.pdf`, page references are the printed ones),
`results/COMPRESSED-PROOF.md`, and m5/m6's artifacts. Nothing is re-derived from R1–R6.

## 0. Verdict

1. **Theorem A (the bridge) is true and is proved below** in its exact conditional form: a
   weak measurable 6-colouring *that has a cyclic centre carrying a simple label cycle of
   length `ℓ` with the exclusion continua of Proposition 7.1* induces a model of
   `(C1)-(C5)` at the sign matrix of its limiting rays, for almost every direction `e` of
   the orbit, and that sign matrix is one of m5's `6^ℓ` grid instances.
2. **Defect I (a missing input, located exactly).** The italic hypothesis is not available
   at `k = 6` and the paper's proof of it is a `k = 5` proof. So as stated the INDUCTION
   LEMMA — "Proposition 7.1 supplies a point `x`, a simple label cycle of length
   `l ∈ {3,...,6}`" — is not proved at `k = 6`; it is a hypothesis. §4.
3. **Defect II (the conclusion is unreachable anyway).** Even granting Defect I, the
   tightened CSP is satisfiable at `k = 6` for every `ℓ` and every sign matrix, with an
   explicit model (`work/STEP1-VACUITY.md`). So no UNSAT branch exists and `χ ≥ 7` cannot
   follow from `(C1)-(C5)`. §5.
4. **Erratum in the accepted record.** `results/K6-BARRIER.md` §2 says the `k = 6` failure
   of §7 is "multiplicity three / no cover obstruction". It is not: the target-graph
   construction of §7 is label-count blind (the bound "at most two positive coordinates"
   comes from the forest property of `Γ_z`, not from `|P| ≤ 2`). The operative and only
   `k`-dependence in §5–§8 is Theorem 6.5 (local finiteness of cyclic centres). §6.
5. **Which of L1–L5 is reached:** none. The certified increment is an L4-type no-go for the
   state-level (palette-orbit) class at `k = 6`, plus the corrected property list a
   replacement mechanism must have. §7.

---

## 1. The encoding, checked against the paper

`k = 6`, labels `0..5`. Fix a centre `x` and a simple label cycle `i_0,...,i_{ℓ-1}`
(`3 ≤ ℓ ≤ 6`) with continua `K_j` and limiting rays `v_j`. Relabel `i_j ↦ j`, `T = {0..ℓ-1}`,
`U = {ℓ..5}`; this is legitimate because every constraint below is equivariant under a
permutation of the label set (`O_i`, `I_i` are unions of cycle labels and of `U`).

Paper §8, verbatim: *"Let `B ⊂ S` be the finite, antipodally symmetric set of directions
perpendicular to at least one `v_j`. At `e ∉ B`, give edge `j` sign `+` or `−` according as
`e·v_j` is positive or negative. Let `O(e)` be the set of labels remaining after the
endpoints of every positive edge are removed, and let `I(e)` be the set remaining after the
endpoints of every negative edge are removed. Labels outside the cycle belong to both
sets."* Edge `j` joins `j` and `j+1`, so label `j` is an endpoint of edges `j-1` and `j`:

    j ∈ O(e) ⟺ σ_{j-1} = σ_j = −1,     j ∈ I(e) ⟺ σ_{j-1} = σ_j = +1,     U ⊆ O(e) ∩ I(e),

with `σ_j = sign(e·v_j)`. This is exactly m5's `allowed_sets` (`interface_csp.py`), so
m5's encoder and the paper agree, including which of `O`,`I` gets the negative edges
(paper Prop 8.2: *"A label belongs to `I(e)` exactly when its two incident signs are
positive, and to `O(e)` exactly when both are negative"*).

**Sign-cell completeness (m5's `6^ℓ` covers every ray geometry).** Write
`t_j = (θ_j − θ_e)/(π/3)` with `θ` the argument of the direction. Then
`σ_j^{(i)} = sign cos((t_j − i)π/3)`. `cos(πy/3)` vanishes iff `y ∈ Z + 1.5 mod 6`, and
`{i + 1.5 mod 6 : i ∈ Z/6} = Z + 0.5 mod 6`; so the whole vector `(σ_j^{(i)})_i` is constant
on each cell `t_j ∈ (c_j + 1/2, c_j + 3/2)` and equals its value at the grid point
`t_j = c_j + 1 ∈ Z`. Conversely every grid point is such a cell interior. Hence the `6^ℓ`
integer cell vectors enumerate exactly the sign matrices of all ray geometries with no
`e_i ⊥ v_j`, and those are the only ones we need (see Theorem A).
Check: `python3 work/signcells.py` → 20000 random real ray configurations, 0 mismatches,
plus a within-cell invariance test.

Note the exceptional set matters: `B` is finite, so a direction `e` whose whole `R`-orbit
avoids `B` exists, and for such `e` the induced instance is a grid instance.

---

## 2. Theorem A (the bridge)

**Theorem A.** Let `c : ℂ → Fin 6` be a weak measurable 6-colouring (paper Def. 1.2) and
suppose

(H1) there are `x ∈ ℂ`, distinct labels `i_0,...,i_{ℓ-1}` (`3 ≤ ℓ ≤ 6`), `ρ > 0`, compact
connected `K_j ⊆ B(x,ρ)` with `x ∈ K_j`, `K_j ∩ ∂B(x,ρ) ≠ ∅`, unit vectors `v_j`, and
`q_{j,n} ∈ K_j \ {x}` with `(q_{j,n}−x)/|q_{j,n}−x| → v_j`, such that both endpoint
supports are excluded: `H_{i_j} ∩ Δ(K_j) = H_{i_{j+1}} ∩ Δ(K_j) = ∅` for every `j`
(this is the conclusion of paper Prop. 7.1).

Then there is a conull set `G ⊆ S` (depending on `x` and on the data of (H1)) such that for
every `e ∈ G`, with `P_i := P_x(R^i e)` (`i ∈ Z/6`) and with `σ, O_i, I_i` computed from the
rays `v_j` at `f = R^i e`:

    (C1) 1 ≤ |P_i| ≤ 3
    (C2) P_i ∩ O_i ≠ ∅ and P_i ∩ I_i ≠ ∅
    (C3) P_i ∩ P_{i+1} = ∅          (indices mod 6)
    (C4) no two of P_0,...,P_5 are complementary 3-sets
    (C5) #{i : |P_i| = 3} ≤ 3

and the sign matrix `(σ_j^{(i)})_{i,j}` is one of the `6^ℓ` grid instances of §1.

*Proof.* Define the following subsets of `S` (`σ`-null sets, each from the named input):

* `N₁` = `{e : 1 ≤ |P_x(e)| ≤ 3 fails}`. Null: upper bound is R5 (general-`k` palette bound,
  `results/K6-BARRIER.md` §1, machine-checked at `k=5` as Prop. 5.6); lower bound is
  Definition 5.1's nonemptiness ("It also gives nonemptiness of `P_x(e)` almost everywhere").
* `B` = the finite set above (`|B| ≤ 2ℓ`). Null? no: finite, so we simply avoid it.
* `F` = `{f ∈ S : (8.1) fails at f}`. Null: Lemma 8.1 states (8.1) *for almost every*
  `f ∈ S \ B`.
* `N₃` = `{f : P_x(f) ∩ P_x(Rf) ≠ ∅}`. Null: Corollary 5.4, display (5.7), for a.e. `f`.
* `N₄` = `∪_{j,m ∈ Z/6} ∪_{|A|=3} (R^{-j}B_A ∩ R^{-m}B_{A^c})` where `B_A = {e : P_x(e)=A}`.
  Null: for fixed `j,m,A`, `σ(R^{-j}B_A ∩ R^{-m}B_{A^c}) ≤ min(σ(B_A), σ(B_{A^c})) = 0` by
  m6's Theorem 1 (`A ∪ A^c = Fin 6`, so not both are palette-positive); the union is over
  `6·6·20/2 = 360` pairs.
* `N₅` = `{e : #{i : |P_x(R^i e)| = 3} ≥ 4}`. Null: m6's Theorem 2.

Let
`G = (∩_{i∈Z/6} R^{-i}(N₁ ∪ F ∪ N₃)) \ (N₄ ∪ N₅ ∪ ∪_{i} R^{-i}B)`.
A finite union/intersection of null sets is null and `∪_i R^{-i}B` is finite, so `G` is
conull, hence nonempty and in fact of full measure.

Fix `e ∈ G`. Then for each `i`: `R^i e ∉ N₁` gives (C1); `R^i e ∉ F ∪ B` and (8.1) give
(C2); `R^i e ∉ N₃` gives `P_x(R^i e) ∩ P_x(R^{i+1}e) = ∅`, which is (C3); `e ∉ N₄` gives
(C4); `e ∉ N₅` gives (C5). Finally `R^i e ∉ B` for all `i` says no `e_i` is perpendicular
to any `v_j`, so §1's cell argument puts the sign matrix in the `6^ℓ` grid. ∎

**Remark on the `a.e.` bookkeeping.** The mission's one-line formulation ("m6's Theorem 1
supplies (C4)") needs the extra step above: Theorem 1 is a statement about *measures of
level sets*, `σ({P=A}) > 0`, not about a single direction. A colouring may have
`P_x(e_0) = A` and `P_x(e_2) = A^c` simultaneously at one direction, as long as both level
sets are null. What is true is the `360`-fold finite-union statement `N₄`; since the CSP is
evaluated at a *generic* `e`, that is exactly enough. The same remark applies to (C5)
(m6's Theorem 2 is `a.e.` in `e`, so it is (C5) verbatim), to (C3) (six rotations of one
null set) and to (C2) (the orbit must avoid the *finite* set `B`, not just a null set).

**Corollary A′.** If the system `(C1)-(C5)` were unsatisfiable for every `ℓ ∈ {3,...,6}` and
every sign matrix, then (H1) would be false for every weak measurable 6-colouring. That is
the only form in which the CSP decision bears on `χ`. By §5 the hypothesis of A′ is false.

---

## 3. What Theorem A does *not* need

The proof uses no separation lemma, no cover lemma, no §6 material, no §7 material beyond
(H1), no measurability of `P_x` in `x`, and no count of labels beyond `k = 6`. In
particular Theorem A is insensitive to the `k`-dependence that kills §7, which is the point
of isolating (H1) as a hypothesis.

---

## 4. Defect I: (H1) is not available at `k = 6`

Prop. 7.1 is stated *"For the weak measurable five-coloring under consideration, there exist
an integer `ℓ ∈ {3,4,5}` ..."* — a `k = 5` statement. Three separate gaps at `k = 6`:

**(a) `ℓ = 6` is outside the paper.** The paper's cycle lengths are `3,4,5`; there is no
six-cycle case and no argument excluding it. `results/K6-BARRIER.md` §4 says the same.

**(b) The proof is `k = 5`-specific at Theorem 6.5.** The project's own dependency tree
(`results/COMPRESSED-PROOF.md`, the `Prop 7.1` node) lists `Prop 5.6 (palettes have size
<= 2)` and `Thm 6.5 (L is closed and locally finite)` as inputs of Prop. 7.1, and `Thm 6.5`
in turn consumes `Lemma 5.5 (triangles)` and `Prop 5.6`. Here is where the count enters, for
the triangle case, verbatim:

> *"For a triangle, (6.2) for its three edges and Proposition 5.6 force `P_x(e)` to
> intersect the pair of outside labels almost everywhere. Indeed, a nonempty subset of the
> three triangle labels of size at most two lies in some triangle edge, which is
> forbidden. By (5.7) the intersection with the outside pair is unique almost everywhere and
> alternates under `R`. Thus every such `x` is binary for that fixed pair. Lemma 5.5 proves
> local finiteness of the triangle locus."*

The two inferences are (i) `P ∩ (outside) ≠ ∅` a.e., then (ii) `|P ∩ (outside)| = 1` a.e.,
then alternation, then Lemma 5.5. `Prop. 5.6` is `|P_x(e)| ≤ 2`, i.e. `|P| ≤ k−3` only at
`k = 5`; R5 at `k = 6` gives `|P| ≤ 3`, and with `T = {a,b,c}` and outside `Y = {d,e,f}`
the graph condition (6.2) (`P ⊄ {i,j}` for `ij ∈ Γ_x`, all three edges) is satisfied by

* `P = {a,b,c}` — (i) fails: `|P ∩ Y| = 0`;
* `P = {a,d,e}` — (ii) fails: `|P ∩ Y| = 2`, so (5.7) does not force a singleton and there
  is no alternating selection, hence no binary centre;
* `P = {a,b,d}` — (ii) fails the same way (and `{a,d}` is not an edge, `{b,d}` is not);

by contrast the `k = 5` palette types are `P ⊆ T` with `|P| ≤ 2` (excluded by (6.2)) or
`|P ∩ Y| ≤ 1` with `|Y| = 2`. So the two displayed inferences both fail at `k = 6`, and
Lemma 5.5 — the only separation input — has no hypothesis.

**(c) §7 then needs finiteness of `L`.** `§7.2`: *"Choose a closed square `Q` of side ten with
`∂Q ∩ L = ∅`. Such a square is obtained by a small translation: local finiteness leaves only
finitely many points to avoid"*; `Lemma 7.4`: *"write `L₀ = L ∩ Q′`, a finite set by Theorem
6.5"*, and the core disks are `B(x,δ)`, `x ∈ L₀`, with `M_δ = Q′ \ ∪_{x∈L₀} B(x,δ)` and
*"every `Γ_z`, `z ∈ M_δ`, is a forest"*. With `L` not known locally finite, `L₀` is not
known finite and the whole construction of Prop. 7.1 stops.

So the INDUCTION LEMMA as stated in the brief is **conditional on a `k = 6` theorem that neither
the paper nor the project contains**: "a weak measurable 6-colouring has a cyclic centre
carrying a simple label cycle of length `3 ≤ ℓ ≤ 6` with the exclusion continua of (H1)". The
machine-checked layer of `lean/OAI` is `k = 5`-specific at exactly this point
(`no_five_exclusion_continua`, `no_triangle_commonInterface`, `no_four_commonInterface` are
all `WeakColoring 5` / `ℂ → Fin 5`). I state this as a defect in the record, not as a
proof that no such theorem is true: `results/K6-BARRIER.md` §4 asserts the `3 ≤ ℓ ≤ k` form
while the same file's §1–§2 say the `k = 5` palette bound is what §6–§7 consume.

### 4.1 The exact repair target (for whoever takes the `k = 6` cyclic-centre theorem)

For a triangle cycle `T = {a,b,c}` at `k = 6` with outside triple `Y = {d,e,f}`:

**(iii) is empty.** With `ell = 3` the three signs contain no `++` pair and `−−` pair
simultaneously, so `T ∩ O_i` and `T ∩ I_i` are never both nonempty (checked over all 216
geometries x 6 positions, `work/ternary_models.py` (A)); hence `P ⊆ T` never satisfies
`(C2)`, and the full-triangle palette `P = T` never occurs. In particular the pattern
`T, {d,e}, T, {d,e}, T, {d,e}` is a model at **0** of 216 geometries, not at all of them as
one would guess from (6.2) alone.

**What survives is `|P ∩ Y| ∈ {1,2,3}`**, and each value occurs (216/216 geometries admit a
palette of each kind, (B)/(C)):
(i) `|P ∩ Y| = 1` — the paper's binary-centre route works;
(ii) `|P ∩ Y| = 2` — no alternating selection from a triple, binary-centre lemma unavailable;
(iii') `|P ∩ Y| = 3` — forces `P = Y` exactly, so the palette avoids every cycle label. `Y`
itself is admissible at *every* position of *every* geometry, so `(8.1) + (C1)` do not
exclude this state.

So the repair must exclude `|P ∩ Y| ≥ 2` on a positive-measure set of directions at a centre
where the triangle is present. Two further remarks:

* The `k = 5` proof's step "`P ∩ Y` is a singleton almost everywhere" is derived from (5.7):
  if `P(e) ⊇ Y` then `P(Re) ∩ Y = ∅`, so `P(Re) ⊆ T` with `|P| ≤ 2`, which lies in an edge
  and violates (6.2). At `k = 6` the same argument only gives `|P(Re)| ≤ 3` and stops (and
  by the first item `P(Re) = T` is impossible), so it yields the weaker true statement
  **`|P(e) ∩ Y| = 2 ⇒ |P(Re) ∩ Y| = 1`** — a genuine extra constraint, which is however
  vacuous on every binary model and therefore cannot help (see (P1) below).
* `(iii')` is not refutable by any circle-only argument: by (5.2) and Fubini, `P_x(e) = Y` on
  a positive-measure set forces the circle `x + e` to be coloured a.e. by `T`, i.e. to be
  properly 3-coloured, a genuine phenomenon (`χ(S_r) = 3` exactly for `θ/2π = p/q` with `q`
  odd, m1's `d7-SPHERE-CAP.md`). Excluding it must use the joint structure of two centres.

The four-cycle case has the same defect (`§6.3.1`: *"A palette not containing `X` has size at
most two"*).

**Erratum (K6-BARRIER §3).** That file states *"the general bound is `1 ≤ |A(e)| ≤ k − 4`"*
for a length-three interface with `A(e) = P_x(e) ∩ (I ∖ T)`. At `k = 6`, `ell = 3` the bound
fails: `P_x(e) = Y = {d,e,f}` satisfies `1 ≤ |P| ≤ k−3` and meets `O_i` and `I_i` at every
position of every geometry, so `|A(e)| = 3 > k−4 = 2`. (At `k = 5` the analogous data
`P = Y` gives `|A| = 2 > 1`; the bound needs the extra hypothesis `P ∩ T ≠ ∅`, which `(8.1)`
does not supply.) The file's conclusion — that the `k = 6` triangle state is not binary —
stands (items (ii) and (iii')); only the stated bound is wrong.

---

## 5. Defect II: the UNSAT branch does not exist

See `work/STEP1-VACUITY.md`. Summary: at `k = 6` every model of `(C1)-(C3)` can be shrunk
coordinatewise to one with `|P_i| ≤ 2`, and such a model satisfies `(C4)` and `(C5)`
automatically. So the tightened decision table *is* m5's table: `36/36`, `216/216`,
`225/1296`, `177/7776` (SAT/geometries) at `ℓ = 3,4,5,6`. Verified exhaustively by an
independent encoder. Consequently Corollary A′ cannot fire.

---

## 6. Erratum: where §7 really fails at `k = 6`

`results/K6-BARRIER.md` §2 argues: three labels in a palette ⇒ the thresholded vector
(7.4) has three positive coordinates ⇒ the component cover has multiplicity three ⇒
Lemma 7.5 (multiplicity at most two) does not apply. **The middle step is false.** The paper
bounds the number of positive coordinates of (7.4) by a *graph* argument, not by the palette
bound: at a point of `M_δ` outside the marked disks, the positive coordinates form a clique
in the forest `Γ_z` (else that pair is a nonedge of `Γ_z` and Lemma 7.3 puts the point inside
a marked disk), and a clique in a forest has at most two vertices. This is uniform in the
number of labels: with the target `G` taken as the one-skeleton of the `k`-simplex, the map
`g_n : Q → G` exists for every `k`, hole-filling works because a forest is contractible, and
the component cover `U_{n,i} = {z : (g_n(z))_i > 0}` has multiplicity `≤ 2` for every `k`.
Hence the existence of multiplicity-3 relatively open covers at every mesh (m3's COVER NO-GO)
does not make Lemma 7.5 inapplicable, and one does not need "a replacement for Lemma 7.5
handling multiplicity three" (K6-BARRIER §5, item 2).

What is `k`-dependent in §5–§8 is: (i) `|P| ≤ k−3` (R5) and (ii) Theorem 6.5, whose triangle
case above uses `|P| ≤ 2`. Only (ii) blocks Prop. 7.1.

Two consequences for the record, both stated as corrections rather than as agreement:

* `results/K6-BARRIER.md` §2 ("with three positive labels at a palette the thresholded vector
  has three positive coordinates") and §5 item 2 ("a replacement for Lemma 7.5 handling
  multiplicity three") are superseded: the thresholded vector has at most two positive
  coordinates at every `k`.
* `m3`'s L4 table row `LB5` reads *"the cover datum produced by paper §7 at multiplicity
  `k − 3 ≥ 3`"*. The premise is wrong: the `§7` component cover has multiplicity `≤ 2` at
  every `k`, so `m3`'s Theorem C (`Cov(3,d)` for every `d > 0`) — a true statement about
  labelled covers — is not an obstruction to `§7` at `k = 6`. What `m3` does establish is
  the label-blindness of the cover lemma (R4), which is compatible with `§7` going through
  at `k = 6`.
* The correct `k = 6` obstruction in `§5–§8` is therefore exactly one statement:
  **`L = {x : Γ_x contains a cycle}` is locally finite at `k = 6`** (Theorem 6.5 with the
  palette bound `k − 3 = 3`), or any substitute that supplies (H1). This is `(P5)` below.

---

## 7. Which of L1–L5 is reached, and the replacement list

**None of L1–L5.** I did not prove `χ ≥ 7` (and §5 shows this route cannot), did not exhibit
a 6-colouring, and did not complete L4's full statement (m5+m3+m4 hold the cover-and-palette
no-go for the six-step relaxation).

The certified increment is an L4-shaped no-go *with its property list*, for the strictest
class anyone has proposed:

> **Theorem B (see STEP1-VACUITY.md).** At `k = 6`, for every `ℓ ∈ {3,...,6}` and every sign
> matrix, if `(C1)-(C3)` is satisfiable then so is `(C1)-(C5)`; the tightened table is m5's.

Hence the tightening round is vacuous, and the necessary conditions on any further `(C6)`
are:

* **(P1) `(C6)` must be false on every *singleton* model.** At `ℓ ∈ {3,4}` and `k = 6`,
  `|U| = 6−ℓ ≥ 2` and `U ⊆ O_i ∩ I_i` for every geometry, so `P_i = {p_i}` with
  `p_i ∈ U`, `p_i ≠ p_{i+1}` is a model for every geometry — in particular
  `{p}{q}{p}{q}{p}{q}` with `p ≠ q` in `U`. Any `(C6)` satisfied by it leaves the `ℓ = 3`
  and `ℓ = 4` rows SAT for every geometry, and then `χ ≥ 7` cannot follow.
* **(P2) `(C6)` therefore cannot be a function of palette sizes and set relations alone**
  (`(C4)`,`(C5)` and their descendants are). It must be false for palette data realizable
  with two labels.
* **(P3) `(C6)` must be plane-level**: at least one second centre, i.e. the strip/trace data
  of Lemma 8.1 (the *strip* restrictions, not just `(8.1)`) or m8's translation structure.
  This is forced, not stylistic — the two horns of a dichotomy: every constraint on the six
  palettes that survives the shrink of Theorem B (`STEP1-VACUITY.md` §1, e.g. anything true
  of all binary models) is vacuous at `k = 6`; and the *full* a.e. palette system is
  equivalent to the original problem (m8's A.E. COLLAPSE). So a finite truncation is empty
  and the infinite one is the question.
* **(P4) `(C6)` must be true at `k = 7`** (`χ ≤ 7` is a theorem) and must keep m5's
  calibration (`k = 4` UNSAT at `ℓ = 3,4`; `k = 5`, `ℓ = 5` UNSAT), or it is not a successor
  of the palette mechanism.
* **(P5) Any complete route must first supply the `k = 6` form of Theorem 6.5** (or of
  (H1)): a cyclic centre with a simple label cycle. Without it no CSP decision can be
  invoked at all, SAT or UNSAT. This is the first missing lemma, and by §6 it is *not* a
  cover-theoretic statement: it is a statement about which labels can share a palette at a
  centre whose transition graph contains a triangle, a square or a six-cycle. §4.1 lists the
  two palette types that the paper's argument cannot handle.

---

## 8. Checks

    cd .ultramath/smwfk0ybk/m10
    python3 work/signcells.py        # §1: 6^ell grid completeness, 20k random configs
    python3 work/vacuity.py          # §5: (C4),(C5) hold on every m5 witness; encoder calibration
    python3 work/tightened_table.py  # §5: the exhaustive tightened table at k=6 (0.8 s)
    (Lean check of the shrink lemma: work/Shrink.lean, `lean work/Shrink.lean`)
