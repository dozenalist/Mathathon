# Repairing m16's Corollary 3.1

**Direction d7, member m8.** Status: the gap is located exactly, the sharpest true
replacement is proved, the conclusion of the corollary is shown to fail *maximally* at the
palette level, a decided finite computation separates the two palette-level regimes, and the
geometric core of the engine is machine-checked on the pinned toolchain.

Everything below is either proved here or cites a numbered statement of the paper
(`attachments/here-are-three-files-ni5n/paper.pdf`); every finite claim has an exact
certificate and two independent implementations; every no-go names its class and is tested for
vacuity.

---

## 0. Verdict in one paragraph

m16's **Theorem A** (two disjoint non-empty label groups with `|A|+|B| = k-2` cannot alternate
under `R`) is correct, and my independent re-derivation agrees with it. m16's **Corollary 3.1**
(`{e : P_x(e) ⊆ {0,1,2,3}}` is angular *null* at a six-colour four-cycle centre) is **not
established**: the printed proof assumes the set is conull, and conull-ness is all it refutes.
The repair is not cosmetic, and it is not a matter of filling one line: the conclusion is
**false at the palette level in the strongest possible way** (I exhibit a palette field on the
whole direction circle — angular measure `2π`, the maximum — that satisfies the palette bound,
(5.7) and (6.2) for the four-cycle and has two free labels). What survives is an exact
*confined* form of the engine, **Theorem R1** below: the alternation contradicts properness on
a measurable set `E` of directions precisely when the shift-`γ₀` same-state set of `E` is
non-null. Theorem R1 specialises to m16's Theorem A when `E` is the whole circle, so it is not
vacuous; and it is the exact reach of the sum construction, because the geometry of the
construction *forces* the shift to `cos δ = -5/6` (Lemma R3), so no adaptive choice of shift can
widen it. The four-cycle case at `k = 6` therefore remains open, with a new necessary condition
(Corollary R2) that any future argument must respect — and with the palette-level route
provably unable to supply it.

---

## 1. The gap, exactly

Setting: a weak measurable `k`-colouring `c : R^2 -> I` (Definition 1.2), colour classes `A_i`,
`H_i` their closed essential supports, `P_x(e)` the maximal palette in direction `e`
(Definition 5.1), `D_{x,i} = {e : i ∈ P_x(e)}`, `κ = π/3`, `R` = rotation of the direction
circle `S` by `κ`, `σ` = angular Lebesgue measure, `Γ_x` the transition graph (Definition 6.1),
`L = {x : Γ_x contains a cycle}`.

m16's Corollary 3.1 reads, at `k = 6`, for a centre `x` whose `Γ_x` contains the four-cycle
`0-1-2-3-0` with outsiders `X, Y`:

> `{e : P_x(e) ⊆ {0,1,2,3}}` is angular null.

The proof (`engine.md`, §3, verbatim) begins: *"Suppose `P_x(e) ⊆ {0,1,2,3}` a.e."* — i.e. it
assumes the displayed set is **conull**. Under that assumption the argument is correct (with
one mis-citation, §7(a) below): on `E` the palette is a diagonal `{0,2}` or `{1,3}`, (5.7)
forces the two to alternate, and Theorem A with `A = {0,2}`, `B = {1,3}`, `|A|+|B| = 4 = k-2`
contradicts it. What this proves is

    sigma(E) < 2 pi,   not   sigma(E) = 0.

The two statements are not equivalent, and the gap is not closable inside m16's class:
§4 shows `sigma(E) = 2 pi` is achievable by a palette field satisfying every hypothesis the
corollary's proof uses, and §5 shows that the one paper constraint m16 does not use — the
two-centre transport (5.3) — kills *two-valued* fields at the palette level. So m16's
Corollary 3.1 needs both a correction (it is not a corollary of Theorem A) and a genuine new
argument, and the second is not available at the palette level.

Consequence for the prior report: the sentence in `sprint/k6/REPORT.md` §4c is right that the
corollary is unusable, and the corollary is not needed for §7 or for the `k >= 7`
counterexample. It *is* the natural way to make the four-cycle case at `k = 6` follow the
paper's `k = 5` route, so its failure is exactly why that case is open.

---

## 2. The sharpest true replacement: Theorem R1

Throughout, "a.e." is with respect to `σ`, and we use the paper's convention that palettes are
defined up to angular null sets; finitely many null sets are discarded in each application.

### 2.1 The mechanism in general form

> **Theorem R1\* (no unit triangle in the forced set).**
> Let `k >= 4`, `c` a weak measurable `k`-colouring, `x ∈ R^2`, and let `A, B ⊆ I` be disjoint
> non-empty with `|A| + |B| >= k-2`; put `C = I \ (A ∪ B)`, so `|C| <= 2`. For `j = 1,2,3`
> let `e_j, v_j ∈ S` be unit directions, each pair `(e_j, v_j)` non-parallel, such that
> `e_j` is an angular density-one point of `D_{x,i}` for every `i ∈ A`, and `v_j` is an
> angular density-one point of `D_{x,i}` for every `i ∈ B`. Then the three points
>
>     z_j = x + e^{i e_j} + e^{i v_j}
>
> are **not** pairwise at unit distance.

*Proof.* Fix `j`. By Lemma 5.2(2) applied with first direction `e_j` and second direction `v_j`
(legitimate: `e_j` is a density-one point of `D_{x,i}` for `i ∈ A`, and `v_j` is non-parallel to
`e_j`), the spatial density of `A_i` at `z_j` is zero for every `i ∈ A`. Applying the same
assertion with the two directions exchanged gives density zero of `A_i` at `z_j` for every
`i ∈ B`. Since `sum_{i∈I} 1_{A_i} = 1` a.e. (Definition 1.2), the union `U = union_{i∈C} A_i`
has spatial density one at each `z_j`.

Suppose now that `z_0, z_1, z_2` are pairwise at unit distance. Choose `r > 0` with
`|U ∩ B(z_j,r)| > (3/4) π r^2` for `j = 0,1,2`. For each `j` the set
`{v ∈ B(0,r) : z_j + v ∉ U}` has measure `< (1/4) π r^2`, so the union over `j = 0,1,2` has
measure `< (3/4) π r^2 < π r^2`; hence some `v` satisfies `z_j + v ∈ U` for all three `j`.
Discarding the (finitely many) null sets `(non-typical set) - z_j` and
`(A_i ∩ (A_i - (z_j - z_{j'})))` for `i ∈ C`, `j ≠ j'`, which are null by Lemma 4.3, we may
additionally suppose that all three points `w_j = z_j + v` are density points of their own
colour classes. Their colours lie in `C`; by Lemma 4.3 any two density points of colour classes
at distance one have different colours; the three `w_j` are pairwise at distance one; so `C`
has at least three elements, contradicting `|C| <= 2`. `square`

(For `|C| <= 1` the last step is immediate. No hypothesis on the palette size is used, which is
why the theorem is `k`-uniform.)

### 2.2 The confined alternation theorem

`E ⊆ S` is the set of directions on which the two-state structure is known; `A_0 ⊆ E` is the
set of directions carrying state `A`.

> **Theorem R1 (confined alternation).** Let `k >= 4`, `c` a weak measurable `k`-colouring,
> `x ∈ R^2`, `A, B ⊆ I` disjoint non-empty with `|A| + |B| >= k-2`, `C = I \ (A ∪ B)`. Let
> `E ⊆ S` and `A_0 ⊆ E` be measurable and suppose
>
>  (H1) `A ⊆ P_x(e)` for a.e. `e ∈ A_0`, and `B ⊆ P_x(e)` for a.e. `e ∈ E \ A_0`;
>  (H2) `1_{A_0}(t+κ) = 1 - 1_{A_0}(t)` for a.e. `t ∈ E ∩ (E - κ)`.
>
> Put `γ₀ = 2 arcsin(1/(2 sqrt 3))` (so `cos γ₀ = 5/6`, `sin γ₀ = sqrt 11 / 6`) and
>
>     G = { t ∈ A_0 : t + 2κ ∈ A_0, t + 4κ ∈ A_0,
>                     t + π + γ₀ + 2jκ ∈ E \ A_0 for j = 0,1,2 }.
>
> Then `σ(G) = 0`.

*Proof.* Suppose `σ(G) > 0`. The sets `A_0`, `E \ A_0`, `D_{x,i}` are measurable, and for each
fixed `i ∈ A ∪ B` and each fixed shift `s` the set `{t : t + s ∉ D_{x,i}}` is a null set when
`D_{x,i}` is replaced by its density-one subset; so, discarding finitely many null sets, we may
choose `t ∈ G` such that all six directions

     e_j = t + 2jκ,      v_j = t + π + γ₀ + 2jκ      (j = 0,1,2)

are angular density-one points of `D_{x,i}` for every `i ∈ A` (at the `e_j`) respectively every
`i ∈ B` (at the `v_j`). By construction `e_j ∈ A_0` (so `A ⊆ P_x(e_j)` by (H1)) and
`v_j ∈ E \ A_0` (so `B ⊆ P_x(v_j)`). Also `v_j - e_j ≡ π + γ₀ (mod 2π)`, and `sin γ₀ = sqrt 11/6
≠ 0`, so `e_j` and `v_j` are non-parallel. Theorem R1\* now forbids the three points

     z_j = x + e^{i e_j} + e^{i v_j}
         = x + e^{i(t + 2jκ)} (1 - e^{i γ₀})  =  x + λ ω^j ,
     λ = 1 - e^{iγ₀},   ω = e^{2 i κ} = e^{2πi/3},

from being pairwise at unit distance. But `|λ|^2 = 1/3` and `|1 - ω|^2 = 3`, so
`|z_j - z_{j'}| = |λ| |ω^j - ω^{j'}| = (1/sqrt 3)(sqrt 3) = 1` for `j ≠ j'`. Contradiction.
Hence `σ(G) = 0`. `square`

The arithmetic is exact in `Q(sqrt 3, sqrt 11)` (`verify_geom.py`, checks G1–G3, two
independent implementations) and machine-checked (`lean/repair31.lean`,
`dist_z01`, `dist_z12`, `dist_z02`).

### 2.3 R1 specialises to m16's Theorem A (non-vacuity)

> **Corollary R1a (m16's Theorem A).** Let `A, B` be disjoint non-empty with `|A| + |B| = k-2`
> and suppose `A_0 ⊆ S` is measurable with `A ⊆ P_x(e)` a.e. on `A_0`, `B ⊆ P_x(e)` a.e. on
> `S \ A_0`, and `1_{A_0}(t+κ) = 1 - 1_{A_0}(t)` a.e. on `S`. Then this is impossible.

*Proof.* Take `E = S` in R1. Then (H2) makes `A_0` `2κ`-periodic and `κ`-flipping, hence
`σ(A_0) = π`, and

     G = {t ∈ A_0 : 1_{A_0}(t+π+γ₀) = 0} = A_0 ∩ Y_{γ₀},   Y_{γ₀} = {t : 1_{A_0}(t+γ₀) = 1_{A_0}(t)},

because `1_{A_0}(t+π+γ₀) = 1 - 1_{A_0}(t+γ₀)` and `t + 2jκ` preserves the state. If
`σ(A_0 ∩ Y_{γ₀}) = 0`, then `A_0` flips under `γ₀` a.e. Pass to the quotient circle
`S/<2κ>` of length `2κ` (`A_0` is `2κ`-periodic): it carries a measurable set `A'` of measure
`κ = (2κ)/2` which is almost disjoint from its rotation by `γ₀ ∈ (0, 2κ)`; two half-measure
subsets of a circle with null intersection are complementary, so `A'` flips under `γ₀`, hence is
invariant under `2γ₀`. Since `γ₀/κ = 3γ₀/π` is irrational — `γ₀/π` is irrational because
`2 cos γ₀ = 5/3` is rational and not an integer (Niven) — the rotation by `2γ₀` is ergodic, so
`A'` is null or conull modulo `2κ`, contradicting measure `(2κ)/2`. Hence
`σ(A_0 ∩ Y_{γ₀}) > 0`, and R1 contradicts it. `square`

So R1 is a strict generalisation of Theorem A: same conclusion, hypotheses on a measurable set
`E` instead of on all of `S`. (m16's own Step 1 is the ergodicity input; I have replaced their
"flip under `γ` forces invariance under `2γ`" by the same argument on the quotient, which is
where the `2κ`-periodicity is used.)

### 2.4 What R1 gives for the four-cycle at `k = 6` (Corollary 3.1 repaired)

> **Corollary R2.** `k = 6`, `x` a centre with `0-1-2-3-0 ⊆ Γ_x`, `T = {0,1,2,3}`,
> `A = {0,2}`, `B = {1,3}`. Put
> `E = {e : P_x(e) ⊆ T}`, `A_0 = {e : P_x(e) = A}`, `B_0 = {e : P_x(e) = B}`,
> `E' = A_0 ∪ B_0`. Then
>
>  (a) `E ∩ R^{-1}E ⊆ E'`: every direction of `E` that carries a **triple** palette has `Re ∉ E`;
>  (b) `(E', A_0)` satisfies (H1) trivially and (H2) by (5.7), so Theorem R1 applies: the
>      good set `G = {t ∈ A_0 : t+2κ, t+4κ ∈ A_0, t+π+γ₀+2jκ ∈ B_0 for j = 0,1,2}` is
>      angular null.
>
> In particular (and this is all): if `σ(E') > 0` then for a.e. `t` in the good set the
> alternation fails — the orbit of `t + γ₀` leaves `E'`, or the state at `t + γ₀` differs from
> that at `t`. `σ(E) = 0` is **not** obtained.

*Proof.* On `E` the palette is non-empty and has size `<= 3`; singletons of `T` and adjacent
pairs are excluded by (6.2) (each label of the four-cycle lies on a cycle edge, so `{i} ⊆ {i,j}`
and `{i,j}` are forbidden). Let `e ∈ E` and suppose `P_x(e) = D` is a triple; then
`D ⊆ T`, so `T \ D` is a singleton. By (5.7), `P_x(Re) ∩ D = ∅`; if also `Re ∈ E`, then
`P_x(Re) ⊆ T \ D`, a singleton, contradicting (6.2). Hence (a). For (b): on `A_0` the palette
equals `A ⊇ A`, and on `E' \ A_0 = B_0` it equals `B`; and for a.e. `t ∈ E' ∩ (E' - κ)` both
palettes `P_x(t)`, `P_x(t+κ)` are `A` or `B`, so by (5.7) they are disjoint, hence different,
i.e. `1_{A_0}(t+κ) = 1 - 1_{A_0}(t)`. Apply Theorem R1 with `(E, A_0) := (E', A_0)`. `square`

Two remarks on the statement.

* The passage from `E` to `E'` is not cosmetic: on the part of `E` whose `R`-image leaves `E`
  — a set of measure `σ(E) - σ(E ∩ R^{-1}E)` — nothing is known, and it is exactly there that a
  triple palette could sit. This is the precise sense in which "the correct conclusion is not
  null": R1 controls only the `R`-self-consistent part of `E`.
* **This is the whole of what survives of Corollary 3.1.** It does not say `σ(E) = 0`. §4 shows
  that `σ(E) = 2π` is attainable by a palette field satisfying exactly the palette hypotheses
  used in (a), so the missing step cannot be palette-level.

---

## 3. Why the confinement cannot be removed: the shift is forced

The natural repair strategy for Cor 3.1 is to *choose* the shift adaptively: "good shifts are
abundant" (m16's Lemma 5.1), so one might hope to find, for the given state function on `E`, a
shift `δ` with a positive-measure same-state set and still get a unit triangle. That is
impossible, and the reason is a rigidity in the geometry, which also explains why the paper's
construction has the shape it has.

> **Lemma R3 (rigidity of the shift).** Let `v ∈ S^1 ⊆ C` and `λ = 1 + v`.
>  (i) `|λ|^2 = 2 + 2 Re v`; hence `|λ| = 1/sqrt 3` iff `Re v = -5/6`, i.e. iff
>      `v = e^{±i(π - γ₀)}`. So among all shifts `δ = arg v`, exactly two make
>      `|1 + e^{iδ}| = 1/sqrt 3` — those with `cos δ = -5/6`.
>  (ii) Three pairwise unit-distance points form an equilateral triangle and have circumradius
>      exactly `1/sqrt 3`. Consequently a set of the shape `{c + e^{iv} : v ∈ Y}` (one fixed
>      endpoint, `Y ⊆ S`) — a subset of a circle of radius `1` — never contains three pairwise
>      unit-distance points, whatever `Y` is.

*Proof.* (i) is `normSq (1+v) = normSq v + 2 Re v + 1` and `normSq v = 1`
(Lean: `normSq_one_add`, `rigidity`; exact algebra: `verify_geom.py` G4). (ii) For an equilateral
triangle of side `1`, the centroid is the circumcentre and the circumradius is `1/sqrt 3`
(`verify_geom.py` G5; the identity is `|z_0 - (z_0+z_1+z_2)/3|^2 = (1/9)|w_1+w_2|^2 = 3/9` when
`|w_1| = |w_2| = |w_1-w_2| = 1`). Since `1/sqrt 3 ≠ 1`, such a triangle is not inscribed in a
circle of radius `1`. `square`

Reading. In the engine the three forced points are built from *one* parameter `t` and *one*
shift, `z_j = x + e^{i(t+2jκ)}(1 + e^{iδ})`, and they are automatically pairwise unit only when
`cos δ = -5/6` (Lemma R3(i)) — which, by the alternation structure, is exactly the pair of shifts
`δ = π ± γ₀`, i.e. exactly the same-state set of the fixed shift `γ₀`. There is no other single
shift. And the alternative "one fixed endpoint, three free directions" is excluded by Lemma
R3(ii). So the sum construction has precisely the reach stated in Theorem R1, and *no argument of
this type* can conclude `σ(E) = 0` from `σ(E) > 0`. A repair of Corollary 3.1 must therefore be
a genuinely different mechanism, not a sharpening of the engine.

Remark (the general configuration). Three sums with *independent* pairs `(e_j, v_j)` are not
covered by Lemma R3, and they are exactly what m16's §5.5 calls (Q). §4 shows that at the palette
level such configurations exist in abundance (`E = S`), so measure theory alone cannot exclude
them; whether a proper colouring can realise them is the open four-cycle problem itself.

---

## 4. Corollary 3.1's conclusion fails maximally at the palette level

> **Theorem R4 (maximal palette-level falsity).** There is a measurable set-valued map
> `P : S -> {subsets of [6]}` with
>
>  (P1) `|P(e)| = 2` for every `e`;
>  (P2) `P(e) ∩ P(e') = ∅` whenever `e' = R e` — the sixty-degree exclusion (5.7);
>  (P3) `P(e) ∉ {{i,j} : {i,j} an edge of C_ell}` for `ell = 4, 5, 6` — the edge exclusion (6.2);
>  (P4) `4, 5 ∉ P(e)` for every `e` — non-proper self-avoidance with two free labels;
>
> and `{e : P(e) ⊆ {0,1,2,3}} = S`, i.e. angular measure `2π`, the maximum possible.

*Construction.* Resolution `n = 36` sectors of width `Δ = 2π/36`; sector `i` is
`[iΔ, (i+1)Δ)`. Put `P(e) = {0,2}` if `floor(i/6)` is even and `{1,3}` if it is odd, i.e. six
blocks of `κ = 60°` alternating between the two diagonals of the four-cycle `0-1-2-3`.
(Equivalently `P` is the unique `2κ`-periodic palettes-`{0,2}`/`{1,3}` alternation with period
`2κ`.) `square`

Verification: `verify_sector.py` §3, two independent implementations, certificate
`CERT-sector-decision.json`; all four properties hold (`A=True, ED=True` for `ell = 4,5,6,
FL=True, 57=True`), and the failing `(sector, offset)` pairs of the transport are listed
(24 of 216). The construction is the direct analogue of m16's own remark (§4c of
`sprint/k6/REPORT.md`), which produces `σ(E) = 2π/3` from the three-block partition
`{0,2},{1,4},{3,5}`; the alternation above pushes it to the maximum `2π`.

**R1's conclusion is not palette-level either.** In the same model the good set of Corollary R2
is large, not null: with `A_0 = {P = {0,2}}` (three blocks of length `κ`, measure `π`) and
`B_0 = {P = {1,3}}`, `A_0` is `2κ`-periodic, so `t ∈ G` iff `t ∈ A_0` and `t + γ₀ ∈ A_0`, i.e.
iff `t mod 2κ < κ - γ₀` (as `0 < γ₀ < κ`); hence

    σ(G) = 3 (κ - γ₀) = π - 3 γ₀ ≈ 1.3845 > 0.

So the confined statement of Theorem R1 is *also* violated by the extremal palette field: it is
a properness-level constraint, not a palette-level one. (Indeed R1 fails on this model for the
right reason: `|A|+|B| = 2 < k-2` is not the issue — the model has no colouring.)

**What this does and does not show.**

* It shows that Corollary 3.1's *conclusion* has no proof from the palette axioms used in its
  proof: `(P1)+(P2)+(P3)` hold with `σ(E) = 2π`. Hence the gap in §1 is not a small one, and no
  sharpening of the palette bookkeeping will close it.
* It also shows why the field cannot be a colouring's palette: with `|A| + |B| = 4 = k-2` and
  global alternation, Theorem R1/Corollary R1a (equivalently m16's Theorem A) forbids it for
  every proper `6`-colouring. So the model is *the* extremal object that properness kills, and
  the whole distance between Corollary 3.1 and the truth is properness.
* Finally, the model fails the paper's two-centre transport (5.3): the transport displacement of
  m15's geometric lemma is `m + k` sectors with `k ∈ {-1,0,1}` and the model has 24 failing
  `(sector, offset)` pairs. §5 shows this is not an accident: transport *always* kills two-valued
  sector fields.

---

## 5. Decided finite computation: two-valued sector fields are impossible with (5.7)+(5.3)

A *sector field* at resolution `n = 6m` is a word `V : Z/n -> P([6])`, sector `i` carrying the
palette on `[iΔ,(i+1)Δ)`, `Δ = 2π/n`; rotation by `κ = π/3` is the sector shift `i -> i+m`. The
palette constraints at `k = 6` are

    A   1 <= |V(i)| <= 3                                  (palette bound; Prop. 5.6 + complement-of-4)
    ED  V(i) not a subset of an edge of C_ell              ((6.2))
    FL  f not in V(i) for all i                            (free label f)
    57  V(i) cap V(i+m) = empty                            ((5.7))
    TR  V(i) cap V(i +- m + k) = empty, k in {-1,0,1}      ((5.3), m15's exact displacement bound)

(`TR` is the sector form of the two-centre transport: m15's geometric lemma gives
`|arg s_\pm - (arg f \pm π/3)| <= 1.5938 d`, and with `d <= d_0 = π/(9m)` the displacement is at
most `1.5938 · d_0 / Δ = 1.5938/3 < 1` sector, `Δ = π/(3m)`; both signs of the `π/3` offset
occur, so the offsets are `+-m + k`, `k ∈ {-1,0,1}`.)

> **Lemma R5 (finite).** Let `n = 6m`, `m >= 1`, and let `V : Z/n -> {P, Q}` be a **two-valued**
> sector field, i.e. the palette takes at most two values. If `57` and `TR` hold, then `V` is
> constant — so in particular `57` fails for non-empty values. Hence **no two-valued
> translation-invariant sector field satisfies (5.7) and (5.3) at any resolution.**

*Proof.* `57` gives `V(i+m) ≠ V(i)`, so with two values `V(i+m)` is the other value. `TR` with
`k = 1` gives `V(i+m+1) ≠ V(i)`, i.e. `V(i+m+1)` is the other value as well, hence
`V(i+m+1) = V(i+m)`; `TR` with `k = -1` gives `V(i+m-1) = V(i+m)`. Writing `j = i+m` (an
arbitrary residue, since `i` is arbitrary) gives `V(j+1) = V(j)` and `V(j-1) = V(j)` for all
`j`, i.e. `V` is constant, contradicting `57`. `square`

*Machine-checked*: `lean/repair31.lean`, theorem `Repair31.no_two_valued_sector_field`, for all
`n, m` at once (`ZMod n`-valued two-valued field, axioms `[propext, Quot.sound]`).

*Exhaustive decision, two independent implementations* (`verify_sector.py` §1: word-list
enumeration with `frozenset` values; bit-mask/rotation arithmetic): for every
`ell ∈ {3,4,5,6}`, free label `f ∈ {0,4,5}` and `m ∈ {2,...,8}`,

| constraint set | number of two-valued sector fields |
|---|---|
| `A + ED + FL + 57` | up to `26112` (non-empty for every `(ell, f, m)`) |
| `A + ED + FL + 57 + TR` | **0** |

The two implementations agree on every entry.

*Vacuity (the computation is not vacuous — `TR` is satisfiable).* The same checker accepts, with
`TR` on:

| model | values | `ell` | free label | `A / ED / FL / 57 / TR` |
|---|---|---|---|---|
| FREE-LABEL three-block, `n=36`, `L=4` | `{3},{4},{5}` | 3 | 0 | all true |
| FREE-LABEL three-block, `n=36`, `L=4` | `{0,2},{1,3},{4}` | 4 | 5 | all true |
| FREE-LABEL three-block, `n=36`, `L=4` | `{0,2},{1,3},{5}` | 5 | 4 | all true |
| FREE-LABEL six-value word, `n=36` | 6 distinct values | 6 | 0 | all true |
| m15 uniform no-go, `n=36`, `L=4` | `{0,2},{1,4},{3,5}` | 4 | — | all true |

**Consequences.**

1. *The "2-periodic free-label word" is killed at the palette level too, but by the transport,
   not by properness.* At `n = 36`, `ell = 6`, free label `0` there are `768` two-valued
   `57`-satisfying words with palette sizes `(2,2)` and `768` with sizes `(2,3)` — the latter
   contain the `(3,2,3,2,3,2)` pattern of `sprint/k6/REPORT.md` §6. All of them satisfy
   `A + ED + FL + 57`, and all of them fail `TR`. So at the palette level the coordinate
   distinction is: `(5.7)+(6.2)` does **not** kill the two-periodic word; `(5.3)` does. The
   statement "the 2-periodic word is killed by m16/m7" is correct only in the colouring class
   (where Theorem R1/Corollary R1a applies because the total size `>= k-2`), not in the palette
   class in which the free-label models live. This matters for the coordinator's lead (ii) and
   for any exact SAT search over free-label sector fields: **the search must impose `TR`, and
   with `TR` the two-valued stratum is empty**, so every free-label witness at `ell = 6` needs
   `>= 3` values (matching the six-value witness of `FREE-LABEL.md`).
2. *R4 is genuinely palette-level-only.* The two properties separate cleanly: `(P1)+(5.7)+
   (6.2)` admits two-valued alternations with `σ(E) = 2π`; adding `(5.3)` kills all of them.
   So the palette-level failure of Corollary 3.1 is *maximal* (R4) and *tight* (R5): the
   palette axioms determine exactly where the two-valued stratum dies.

---

## 6. What the four-cycle case at `k = 6` now needs

State of the art after this report (unchanged by it in principle, sharpened in practice):

1. `σ(E) = 0` (`E = {e : P_x(e) ⊆ {0,1,2,3}}`) would give "the palette contains an outsider for
   a.e. direction" at a six-colour four-cycle centre, the exact analogue of the paper's
   `k = 5` triangle conclusion, and would let the paper's §6.3 route continue.
2. `σ(E) = 0` is **not** implied by the palette axioms: R4 attains `σ(E) = 2π`.
3. The engine gives only Corollary R2: the `γ₀`-good set on the `R`-self-consistent part `E'` of
   `E` is null. This is a new necessary condition on the palette field of any proper
   `6`-colouring with a four-cycle centre, and it must be respected by any proposed model.
4. The engine cannot be improved to `σ(E) = 0` by any argument of its own type (Lemma R3:
   the shift is forced), and m16's alternative route (a longer unit-distance configuration) is
   exactly its open problem (Q), for which the single-shift ceiling is proved (their Theorem E).
5. Therefore a resolution of the four-cycle case at `k = 6` needs an argument in the regime
   `0 < σ(E) < 2π` that uses properness *directly* on a set of direction pairs, not through a
   two-state alternation. The one structural asset not yet used: for `e ∈ A_0` and `v ∈ B_0`
   with independent angles, (5.2) forces `c(x + e^{ie} + e^{iv}) ∈ C = {4,5}`; by the density
   argument of Lemma 5.2(2) the whole sumset `{e^{ie} + e^{iv}}` (a set with non-empty interior
   whenever both state sets have positive measure, by the Steinhaus/density argument) is then
   forced into the two labels `{4,5}`, so the unit-distance graph induced on that sumset must be
   bipartite. What is missing is a lower bound on *how large* that sumset is; the interior can be
   arbitrarily small when `σ(E)` is small, which is precisely why R4's extremal model escapes.

This is stated as the precise residual target, not as a proof.

---

## 7. Audit notes on m16

(a) **Corollary 3.1: conull vs null** — §1. The corollary's proof establishes
`σ(E) < 2π` only. Additionally the phrase *"A triple `D` has complement inside `{0,1,2,3}` a
single label, excluded by (6.2)"* mis-cites (6.2): a triple `D ⊆ T` is not a subset of an edge,
so (6.2) does not exclude it. The correct argument is the sentence that follows it: (5.7) forces
the partner palette `P_x(Re) ⊆ T \ D`, a singleton, which (6.2) does exclude. With that repair
the derivation of `P_x ∈ {{0,2},{1,3}}` a.e. on `E ∩ R^{-1}E` is correct (see Corollary R2(a):
the part of `E` whose `R`-image leaves `E` is not covered).

(b) **Theorem A is correct** and I re-derived it independently (§2.3). Its constants are right:
`γ₀ = 2 arcsin(1/(2 sqrt 3))`, `cos γ₀ = 5/6`, `sin γ₀ = sqrt 11/6`, `|1 - e^{iγ₀}| = 1/sqrt 3`,
`|1 - e^{2iκ}| = sqrt 3`, so the three `z_j` are pairwise at distance exactly `1`
(`verify_geom.py` G1–G3; machine-checked in Lean). The only step in m16's proof I would write
differently is the null-set handling at the end (their "uniform common translation … with
positive probability" is correct; the version in §2.1 discards finitely many null sets
explicitly).

(c) **`sprint/k6/REPORT.md` §4c is right** that the corollary is unusable; and my R4 strengthens
their counterexample's measure from `2π/3` to `2π`.

(d) **The "2-periodic word is killed by m16/m7" claim** needs the quantifier made explicit; see
§5, consequence 1. In the colouring class it is true (total size `5 >= k-2 = 4`, Corollary R1a);
in the palette class of the free-label models it is false for `(5.7)+(6.2)` and true only with
the transport `(5.3)` (Lemma R5).

(e) m16's Theorem E ("a unit-distance graph on one circle is 3-colourable") is correct as
stated; my Lemma R3(ii) is the sharp companion at the three-point level (radius must be exactly
`1/sqrt 3`), which is what forces the shift.

---

## 8. Machine-checked core (Lean 4.34.1, pinned Mathlib `d13f23b`)

File: `lean/repair31.lean`. Command, from the repository root:

```bash
source scripts/env4341.sh && (cd .ultramath/smwfwi7rh/m8/lean && lean repair31.lean)
```

Theorems (all with `#print axioms` output recorded below):

| name | statement |
|---|---|
| `dist_z01`, `dist_z12`, `dist_z02` | the three forced points `z_j = λ ω^j`, `λ = 1 - e^{iγ₀}`, `ω = e^{2πi/3}`, are pairwise at distance exactly `1`, with `Re e^{iγ₀} = 5/6`, `Im e^{iγ₀} = sqrt 11/6` |
| `no_proper_two_colouring` | no `f : C -> Fin 2` separates every unit-distance pair: the engine's last step (paper's Lemma 6.4 / m16's Theorem A / Theorem R1\*), with the paper's explicit constants |
| `rigidity` | `normSq v = 1 -> normSq (1+v) = 1/3 -> v.re = -5/6`: the shift of the engine is forced (Lemma R3(i)) |
| `no_two_valued_sector_field` | for all `n, m`, no two-valued `V : ZMod n -> Bool` satisfies `V(i+m) = !V(i)` together with the transport `V(i+m+1) = !V(i)` and `V(i+m-1) = !V(i)` (`k = ±1`; the proof uses `k = +1` only) (Lemma R5) |

Axiom audit (output of the run):

```
'Repair31.no_proper_two_colouring' depends on axioms: [propext, Classical.choice, Quot.sound]
'Repair31.rigidity' depends on axioms: [propext, Classical.choice, Quot.sound]
'Repair31.no_two_valued_sector_field' depends on axioms: [propext, Quot.sound]
```

What is *not* formalised: the paper's Lemma 5.2/Lemma 4.3 measure theory (it is cited, exactly
as the paper and m16 cite it) and the sets `E, A_0, G` of R1. The Lean file checks the two
places where the paper's numerical constants enter and the one place where a finite
combinatorial obstruction is claimed.

---

## 9. Files, commands, reproduction

All paths relative to the repository root; everything is inside `.ultramath/smwfwi7rh/m8/`.

| file | content | command |
|---|---|---|
| `REPORT.md` | this document | — |
| `verify_geom.py` | exact `Q(sqrt 3, sqrt 11)` arithmetic: constants G1–G6 of Lemma R3, two independent implementations (custom exact field + sympy) | `python3 .ultramath/smwfwi7rh/m8/verify_geom.py` |
| `verify_sector.py` | sector-field decisions of §4, §5: two-valued UNSAT with `TR` / SAT without, vacuity models, R4 countermodel | `python3 .ultramath/smwfwi7rh/m8/verify_sector.py` |
| `CERT-sector-decision.json` | certificate written by `verify_sector.py` (sha256 in its output line) | as above |
| `lean/repair31.lean` | machine-checked core of §8 | `source scripts/env4341.sh && (cd .ultramath/smwfwi7rh/m8/lean && lean repair31.lean)` |
| `lean/CERT-lean.txt` | the output of that exact command (no errors, no warnings, axiom audit) | as above |

Runtimes: `verify_geom.py` < 1 s; `verify_sector.py` ≈ 2.5 min (exhaustive over
`m <= 8`, 12 `(ell, free)` combinations); `lean repair31.lean` 1–8 min depending on the page
cache (mostly Mathlib import).

---

## 10. What is not claimed

* `σ(E) = 0` at a six-colour four-cycle centre is **not** proved; §4 shows it cannot come from
  the palette axioms, §6 states the exact residual target.
* Local finiteness at `k = 6`, `(W)`, and `chi(R^2)` are untouched.
* Theorem R1 is a theorem about the paper's weak measurable colourings; it says nothing about
  abstract palette fields, which is exactly why §4 exists.
* No claim is made that Lemma R5's two-valued obstruction is *sufficient*: three-valued fields
  satisfying `(5.7)+(5.3)` exist (§5, vacuity table), so only the two-valued stratum is dead.
