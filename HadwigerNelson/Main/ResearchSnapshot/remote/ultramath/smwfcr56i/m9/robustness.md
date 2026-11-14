# Durability of the lower bound `chi(R^2) >= 6`

*Sharpen of paper Theorem 1.1 — direction d12, member m9. Machine-checked: `Robust.lean`,
log in `lean-log.txt`, axioms in §8.*

## 0. Results

The paper's lower bound is a **finite-witness** phenomenon, and is therefore insensitive to
deleting from the plane any set in a large class. Writing `chi(S)` for the chromatic number of
the unit-distance graph on `S ⊆ R^2`:

> **Theorem C.** Let `k ≥ 1` and let `Z ⊆ R^2` be Lebesgue-null, or meagre, or of cardinality
> `< c = 2^{aleph_0}`, or of finite outer Lebesgue measure, or contained in a closed half-plane.
> Then `R^2 ∖ Z` is `k`-colourable **iff** `R^2` is. Consequently
>
>   `chi(R^2 ∖ Z) = chi(R^2)`  for every such `Z`.

With the paper's Theorem 1.1 and the hexagonal 7-colouring:

> **Corollary D.** For every `Z` in the five classes, `chi(R^2 ∖ Z) ∈ {6,7}`.
> In particular **the plane minus a point**, minus a countable set (e.g. `Q^2`), minus a line,
> minus a closed half-plane, minus any bounded set, minus any null set, minus any meagre set
> **is not 5-colourable**.

> **Corollary E (necessary condition on a 5-colourable set).** If `chi(S) ≤ 5` for `S ⊆ R^2`,
> then `S^c` is non-null, non-meagre, of cardinality `c`, of infinite outer measure, and not
> contained in any closed half-plane. A 5-colourable subset of the plane must have a complement
> that is large in all four measure/category/cardinality senses and not contained in any closed half-plane.

> **Corollary F (localisation).** There is `R_0 > 0` such that for every `R ≥ R_0`, every ball
> `B` of radius `R` and every `Z` in the five classes, `chi(B ∖ Z) ≥ 6`. In particular
> `chi(B) ≥ 6` for every such ball: the plane's lower bound is realised inside a bounded region.

Two guards against misreading:

* This is *not* the paper's null-set invariance of Definition 1.2, which concerns modifying a
  colouring on a null set (a null set of unit *pairs*). Theorem C deletes *vertices* and
  concerns unrestricted colourings; it uses no measurability.
* The result is one-sided in the right way: deleting vertices can only lower `chi`, and it does
  — deleting a co-bounded set brings `chi` down to `1` (§6). So Theorem C is the strongest
  statement of its shape: for the five classes it gives two-sided equality `chi(R^2∖Z) = chi(R^2)`.

## 1. Notation

Identify `R^2` with `C`; `|z| = ‖z‖`. For `S ⊆ C`, `G(S)` is the graph with vertex set `S` and
edge set `{{x,y} : |x−y| = 1}`; `chi(S) = chi(G(S))`. A `k`-colouring of `S` is a map
`c : S → {1,…,k}` with `c(x) ≠ c(y)` whenever `|x−y| = 1`. `vol` is planar Lebesgue measure,
`|Z|` its value on a measurable `Z` and `|Z|_e` the outer measure. `c := |C| = 2^{aleph_0}`.
"Null" means `vol`-null; "meagre" means of the first Baire category.

## 2. The translate lemma

Fix a finite set `W ⊆ C` and `Z ⊆ C`. The **bad translations** are

  `T_Z(W) := { t ∈ C : (W + t) ∩ Z ≠ ∅ } = ⋃_{w ∈ W} (Z − w)`,  `Z − w := {z − w : z ∈ Z}`.

> **Lemma A.** If `Z` satisfies (a) `|Z| = 0`, or (b) `Z` meagre, or (c) `|Z| < c`, or
> (d) `|Z|_e < ∞`, or (e) `Z ⊆ H` for a closed half-plane `H`, then `T_Z(W) ≠ C`; i.e. some
> translate `W + t` is disjoint from `Z`.

*Proof.* (a) Each `Z − w` is null (translations preserve measure), and `T_Z(W)` is a finite
union of them, hence null; `|C| = ∞`, so `T_Z(W) ≠ C`.
(b) Each `Z − w` is meagre (translations are homeomorphisms), so `T_Z(W)` is meagre; a complete
metric space is not meagre (Baire), so `T_Z(W) ≠ C`.
(c) `|Z − w| = |Z| < c` for each `w ∈ W`. A finite union of sets of cardinality `< c` has
cardinality `< c`: if `|Z|` is finite this is clear, and if `|Z|` is infinite then
`|W|·|Z| = |Z| < c`; and `|C| = c`. Hence `T_Z(W) ≠ C`.
(d) Outer measure is translation invariant and subadditive:
`|T_Z(W)|_e ≤ ∑_{w∈W} |Z − w|_e = |W| · |Z|_e < ∞ < |C|_e`. Hence `T_Z(W) ≠ C`.
(e) Write `H = {x : <x,n> ≤ β}` with `n ≠ 0`, and let `m := min_{w∈W} <w,n>` (finite `W`).
For `w ∈ W`, `H − w = {t : <t,n> ≤ β − <w,n>} ⊆ {t : <t,n> ≤ β − m}`; hence
`T_Z(W) ⊆ {t : <t,n> ≤ β − m}`, a proper subset of `C`. ∎

> **Lemma A′ (refinement).** Let `A ⊆ C`. If `A ⊄ T_Z(W)` then there is `t ∈ A` with
> `(W + t) ∩ Z = ∅`. In the instances of Lemma A: for `Z` null, `A ⊄ T_Z(W)` holds whenever
> `|A|_e > 0`; for `Z` meagre, whenever `A` is non-meagre; for `|Z|_e < ∞`, whenever
> `|A|_e > |W| · |Z|_e` (e.g. `A` of infinite measure); for `|Z| < c`, whenever
> `|A| > |W| · |Z|`.

*Proof.* `T_Z(W)` is by definition the set of bad translations. ∎

## 3. Compactness, self-contained

> **Lemma B (de Bruijn–Erdős for the plane graph).** Let `k ≥ 1`. If every finite `F ⊆ C` admits
> a `k`-colouring of `G(F)`, then `G(C)` admits a proper `k`-colouring.

*Proof.* `X := ∏_{z ∈ C} {1,…,k}`, a product of finite discrete spaces, is compact (Tychonoff).
For a unit-distance pair `p = {x,y}`, the set `C_p := {f ∈ X : f(x) ≠ f(y)}` is closed: it is the
preimage of the closed set `{(a,b) : a ≠ b}` of the finite discrete space `{1,…,k}²` under the
continuous projection `f ↦ (f x, f y)`.

*Finite intersection property.* Let `P` be a finite set of unit-distance pairs and
`F := ⋃_{p ∈ P} p`, a finite set. By hypothesis there is a colouring `c_0` of `G(F)`; extend
`c_0` arbitrarily to `f ∈ X`. Then `f ∈ ⋂_{p ∈ P} C_p`. So every finite subfamily of
`{C_p : p}` has nonempty intersection.

In a compact space, a family of closed sets with the finite intersection property has nonempty
total intersection; so `⋂_p C_p ≠ ∅`, and any `f` in it is a proper `k`-colouring of `G(C)`. ∎

> **Corollary (finite witness, (W)).** If `G(C)` has no proper `k`-colouring, there is a finite
> `F ⊆ C` such that `G(F)` has none. ∎

(W) is exactly the step used in the paper's Corollary 1.5 (`delta = 1/|E(H)|`), where `H` is
this finite witness.

## 4. Proof of Theorem C

Let `Z` be in one of the five classes and let `W` be a finite set with `G(W)` not `k`-colourable,
from (W). Suppose `c : C ∖ Z → {1,…,k}` is a proper colouring. By Lemma A there is `t ∈ C` with
`(W + t) ∩ Z = ∅`. Since translation preserves distances, `x ↦ c(x + t)` (`x ∈ W`) is a
`k`-colouring of `G(W + t)`, and `G(W + t) ≅ G(W)` is not `k`-colourable. Contradiction.

So `C ∖ Z` is not `k`-colourable whenever `C` is not. The converse (restriction of a colouring
of `C` to `C ∖ Z`) is immediate, so `C` is `k`-colourable iff `C ∖ Z` is, for **every** `k`;
taking the infimum over `k` and using `chi(C ∖ Z) ≤ chi(C)` (monotonicity) gives
`chi(C ∖ Z) = chi(C)`. ∎

**Corollary D.** `no_proper_five_coloring` is the case `k = 5`; `properColoring_seven` gives
`chi ≤ 7` for every subset, in particular `chi(C ∖ Z) ∈ {6,7}`. ∎

**Corollary E.** Put `Z = S^c`, so `S = C ∖ Z`. If `chi(S) ≤ 5` then Theorem C forbids `Z` from
lying in any of the five classes (else `S = C ∖ Z` would not be 5-colourable). ∎

**Corollary F.** Fix `W` and put `R_0 := max{|w| : w ∈ W} + 1`. For `R ≥ R_0` the set
`U := {t : W + t ⊆ B(0,R)}` is open and nonempty (it contains `0`), hence `|U|_e > 0`; by
Lemma A′ there is `t ∈ U` with `(W+t) ∩ Z = ∅`. So `W + t ⊆ B(0,R) ∖ Z` and
`chi(B(0,R) ∖ Z) ≥ 6`. ∎

## 5. Examples covered

`Z` a point; any countable set, e.g. `Q²`, `Q(i)`, the rationals on a line; any line, segment or
circle (all null); every countable union of null sets and every countable union of meagre sets
(null resp. meagre); any bounded set, e.g. a closed disk (finite measure); any closed half-plane
(e). Note that Corollary E therefore says: **`chi(S) ≤ 5` forces `S^c` to be unbounded in every
direction, non-null, non-meagre, of cardinality `c` and of infinite outer measure.**

## 6. Sharpness

Let `r = 2/5` and `B = {z : |z| < r}`; then `diam B = 4/5 < 1`, so `B` has no unit pair and
`chi(B) = 1`. Put `Z_0 := C ∖ B`.

* `Z_0` is not null — it contains the open set `{|z| > r}`, so it is non-meagre, of infinite
  outer measure, and `|Z_0| = c`; it is not contained in any closed half-plane. Hence `Z_0` lies
  in none of the five classes of Theorem C, and indeed `chi(C ∖ Z_0) = chi(B) = 1`.
* `Z_0` **is** `σ`-finite for Lebesgue measure: `Z_0 = ⋃_{n≥1} (Z_0 ∩ {|z| ≤ n})` with each
  term of finite measure. So the natural relaxation of (d) to "`σ`-finite outer measure" is
  **false**, and (d) cannot be weakened to it.
* Lemma A itself is sharp: for `W = {0,1}` and `Z_0` as above, no translate of `W` avoids `Z_0`
  — if `{t, t+1} ⊆ B` then `1 = |(t+1) − t| ≤ 2r = 4/5`, absurd. So `T_{Z_0}(W) = C`, and the
  translate lemma genuinely fails for `Z_0`: a condition of the type (a)–(e) is needed.
* A second, stronger sharpness example shows that the obstruction is not about "co-boundedness"
  either. Let `Z_1 := C ∖ ⋃_{n≥1} B(10n, 1/4)`; then `Z_1` is closed, unbounded, contains the
  half-plane `{re < 9.5}`, hence is non-meagre, of infinite outer measure and of cardinality `c`,
  not null, and not contained in any closed half-plane: it violates all five clauses of
  Theorem C. Yet `C ∖ Z_1` is a disjoint union of disks of diameter `1/2 < 1` whose mutual
  distances are at least `9.5 > 1`, so it has **no unit pair at all** and `chi(C ∖ Z_1) = 1`.
  (This also shows that the five clauses cannot be merged into a single "measure of the
  complement" condition.)
* The necessary conditions of Corollary E are compatible with very small 5-colourable sets: a
  line `L` is 2-colourable (`G(L)` is a disjoint union of bi-infinite paths; in arclength
  coordinates `x ↦ ⌊x⌋ mod 2` is proper), `L` is null, and `L^c` is non-meagre, non-null, of
  cardinality `c`, infinite measure, and not contained in any closed half-plane. So Corollary E is not vacuous
  and does not force a 5-colourable `S` to be large in any of the five senses.

## 7. Relation to the rest of the corpus

* Paper Corollary 1.5(i) uses exactly (W): Theorem 1.1 plus compactness yields a finite witness
  `H`, and `delta = 1/|E(H)|`. The present note adds no analytic input; it shows that (W) alone
  already makes the lower bound deletion-stable.
* The swarm's T1 (`algebraic_colorable_iff`, machine-checked) shows that restricting the plane to
  the countable dense algebraic plane `E` preserves `chi`. Theorem C shows that deleting any
  countable set from the plane also preserves `chi`. Hence `chi` is unchanged by passing to `E`
  and by deleting any countable subset of the vertices — but deleting a co-bounded set destroys
  it (§6). So the difficulty lives in the translation-rich part of the plane, not in any
  particular countable or null piece.
* Corollary E constrains any future construction of a 5-colouring of a large subset: it must
  leave a complement that is not contained in any closed half-plane, of infinite outer measure, non-meagre
  and of full cardinality. In particular no 5-colouring exists on any subset whose complement is
  null — the complement-side analogue of "the plane is not 5-colourable".
* The theorem also shows that a *null* (or bounded, or countable, or meagre) deletion can never
  lower the chromatic number: for such `Z`, `chi(C∖Z) = chi(C)` exactly, so if `chi(C) = 7` then
  no null set can be deleted to make the plane 6-chromatic. Dually, the drop can be total for a
  co-bounded deletion (§6). Where the drop can occur is therefore exactly in the gap between
  "finite measure" and "co-bounded", i.e. it is a question about complements whose measure is
  infinite but whose complement contains no ball; the translate criterion of Lemma A,
  `chi(C∖Z) > k` iff some translate of a non-`k`-colourable finite metric pattern avoids `Z`,
  is the exact criterion.
* Combining T1 with Corollary D at the countable set `Z = E` (the algebraic plane): **both `E`
  and its complement `C ∖ E` are not 5-colourable**, i.e. `chi(E) ≥ 6` and `chi(C ∖ E) ≥ 6`. A
  countable set and its co-countable (hence full-measure, co-meagre) complement are both hard;
  by §6 a co-bounded complement is not. So "hardness" is a property of *both* sides of a
  countable cut, but not of a bounded cut — a dichotomy that the measure/category classes alone
  do not predict.

## 8. Machine verification

Environment: Lean 4.34.1 with the pinned Mathlib of `scripts/env4341.sh`, on top of the bundle's
`no_proper_five_coloring` and `exists_properColoring_of_finset`.

```
cd <this directory>
source ../../../scripts/env4341.sh && export LEAN_PATH=$PWD:$LEAN_PATH
lean Robust.lean          # exit 0, no diagnostics
lean Check.lean           # #print axioms
```

Declarations proved in `Robust.lean` (all in `OAI.EuclideanFiveColor`):

| declaration | statement |
|---|---|
| `exists_translate_disjoint_null` | `Z` null ⟹ `∃ t, ∀ w ∈ F, w + t ∉ Z` |
| `exists_translate_disjoint_isMeagre` | `Z` meagre ⟹ same |
| `exists_translate_disjoint_countable` | `Z` countable ⟹ same |
| `exists_translate_disjoint_card_lt` | `mk Z < continuum` ⟹ same |
| `exists_translate_disjoint_halfplane` | `Z ⊆ {re ≤ c}` ⟹ same |
| `exists_translate_disjoint_finite` | `vol Z ≠ ∞` ⟹ same |
| `exists_translate_disjoint_null_mem` | `vol Z = 0`, `vol A ≠ 0` ⟹ `∃ t ∈ A`, `∀ w ∈ F, w + t ∉ Z` |
| `not_properColoring_off_null` / `_isMeagre` / `_countable` / `_card_lt` / `_halfplane` / `_finite` | no `k`-colouring of `C` ⟹ no `k`-colouring of `C ∖ Z`, one per hypothesis class |
| `no_five_coloring_off_null` / `_singleton` / `_isMeagre` / `_countable` / `_card_lt` / `_halfplane` / `_finite` | `C ∖ Z` is not 5-colourable, one per hypothesis class |

All five hypothesis classes (a)–(e) of Lemma A are thus proved, in general form and at `k = 5`,
together with the refinement A′ (null case). Auxiliary: `volume_univ_complex` (`vol C = ∞`,
from the explicit area of balls).

`#print axioms` on all of these, and on the bundle inputs `no_proper_five_coloring`,
`exists_properColoring_of_finset` and `Problem160.properColoring_seven`, reports exactly
`[propext, Classical.choice, Quot.sound]` — no `sorry`, no added axiom, no `native_decide`.
Corollaries E and F are not stated in Lean separately: both follow in one line from the
formalised lemmas and Theorem C, and the arguments are given in §4–§5.
