# The colouring level at k = 6: what a free label costs, and what a six-cycle forces

**Swarm** smwfwznwk, member **m2**, direction **d2** (handoff item 4).
**Verdict in one line.** A *globally* free label is impossible for a weak measurable
6-colouring: it forces the corresponding colour class to be plane-null, by a constraint (the
palette contains the colour of the point at unit distance) that lives inside the paper's own
palette framework and needs **no** properness of any avoiding label function. The free label
*can* be made to vary with the centre, so as to satisfy the `d <= d_0` transport fragment that
every sector model in the project uses (explicit verified two-cell model); but the paper's full
(5.3) contains the distance-one instance **(TE)**, and (TE) is what all those models fail — with
a fixed *or* varying free label. (TE) moreover forces every piecewise direction-invariant field
that is a colouring's palette field to have a type partition which is itself a **proper**
measurable colouring with at least six types (Theorem X). Separately, at `k = 6` the six-cycle is
the unique cycle length whose palettes are forced to have size `>= 2`, i.e. a six-cycle centre
forces a second colour class to accumulate at almost every point of its unit circle.

Everything below is either (i) a proof from the paper's definitions, or (ii) a finite
computation with two independent procedures; §9 says which is which.

---

## 1. Notation and the inputs that are cited, not re-derived

Let `c : R^2 -> {1..6}` be a weak measurable 6-colouring (Definition 1.2: Borel
representatives forming a partition, and
`sum_i ∫_{B(0,R)} ∫_{S} 1_{A_i}(x) 1_{A_i}(x+u) dσ(u) dx = 0`), `A_i = c^{-1}(i)`,
`S = S^1`, `σ` normalised arc measure, `R` rotation by `κ = π/3`, `J` rotation by `π/2`.

* **Typical point**: density-one point of its own class; typical points are conull and
  `H_i = {q : |A_i ∩ B(q,r)| > 0 for all r > 0}` is the closed essential support of `A_i`.
* **Lemma 4.3** (paper): the full-density-point set of each `A_i` contains no unit pair.
* **Definition 5.1** (paper): `W_x` = weak-* limits in `L^∞(S;R^6)` of
  `(a_i(y_n + r_n e))_i` with `y_n → x`, `r_n → 1`, each `(y_n,r_n)` a *typical circle
  sampling* (`y+re` typical for a.e. `e`); `D_{x,i} = ess ∪_{b ∈ W_x}{e : b_i(e) > 0}`,
  `P_x(e) = {i : e ∈ D_{x,i}}` ("maximal palette"), defined modulo angular null sets.
* **Lemma 5.2(2)** (paper): if `e` is an angular density-one point of `D_{x,i}`, then the
  spatial density of `A_i` at `x+e+v` is zero for every unit `v` nonparallel to `e`.
* **Corollary 5.4** (paper), (5.7): `P_x(f) ∩ P_x(Rf) = ∅` for a.e. `f`.
* **Lemma 6.2** (paper), (6.2): `ij ∈ Γ_x ⟹ P_x(e) ⊄ {i,j}` for a.e. `e`.
* **Theorem 1.4** (paper): there is no weak measurable 5-colouring. Consequently (relabelling
  on a plane-null set leaves the weak condition unchanged) **at `k = 6` every class `A_i` has
  positive measure**, and a weak measurable 6-colouring exists only if all six labels are used.
* **Lemma D** (sprint smwfwi7rh, m2; `sprint/k6/REPORT.md` §5): at a typical centre `x` with
  `c(x) = i`, `i ∉ P_x(e)` for a.e. `e`. (Label-blind, so valid at `k = 6`.)
* **(TE) translation exclusion** (paper: Lemma 5.2(3) with `z = x+a`, `s(f) = f`, `t(f) = a`,
  the instance recorded in Remark 5.3 as "admissible off `f = ±a`"; no distance restriction is
  used by Lemma 5.2(3), and the printed proof of Lemma 6.7 uses it at `d = 1`). For every fixed
  unit vector `a` and a.e. `f`:
  `P_{x+a}(f) ∩ P_x(f) = ∅`. In this swarm the same observation is m1's finding f4 and m4's
  finding f1; it is cited here, not re-derived. Note that it lies **outside** the `d <= d_0`
  transport fragment used by every sector model in the project.
* Admissibility at a six-cycle centre (handoff, Lemma 6.2 + (6.2)):
  `1 <= |P_x(e)| <= 3` and `P_x(e) ⊄ {i,i+1}` for every cycle edge. Every label lies in a
  cycle edge of `C_6`, hence `|P_x(e)| >= 2` at a six-cycle centre.

The paper is `attachments/here-are-three-files-ni5n/paper.pdf` ("The Euclidean plane is not
five-colorable"). The displayed formulas used above — Definition 1.2, Definition 5.1,
Lemma 5.2 (5.2),(5.3), Corollary 5.4 (5.7), Lemma 6.2 (6.2) — were extracted with
`pdftotext -layout` and independently re-extracted with `pdftotext -raw`, and the two
extractions agree word for word (`scratch/paper.txt`, `scratch/paper_raw.txt`; see §9 for the
`grep` commands).

---

## 2. Lemma P: the palette at `x` contains the colour of every point of the unit circle about `x`

**Lemma P.** For *every* fixed centre `x` and every label `i`,
`σ{e : c(x+e) = i and i ∉ P_x(e)} = 0`. In particular `c(x+e) ∈ P_x(e)` for `σ`-almost every
`e` (the null set may depend on `x`, which Definition 5.1 explicitly permits).

*Proof.* Fix `x`. Let `f = a_i(x + ·) ∈ L^1(S)`. Two facts.

1. *(radii)* The map `s ↦ g_s`, `g_s(e) = a_i(x + s e)`, is measurable in `(s,e)` and
   `∫_S ∫_{1/2}^{3/2} g_s(e) ds dσ(e) = ∫_{B(x,3/2)\setminus B(x,1/2)} a_i(y) |y-x|^{-1} dy
   / 2π < ∞`
   by polar coordinates, so for a.e. `s ∈ (1/2,3/2)` the function `g_s ∈ L^1(S)` is finite and
   `‖g_s - g_1‖_1 → 0` as `s → 1` along a set of `s` of full measure near `1`.
2. *(centres)* For each fixed `r`, `(y,r)` is a typical circle sampling for a.e. `y`
   (the paper's Fubini remark).

Choose radii `r_n → 1` which are radii as in (1) and such that `‖g_{r_n} - g_1‖_1 → 0`; then
choose `y_n → x` with `(y_n, r_n)` typical (possible by (2), intersecting with `B(x,1/n)`).
For `h_n = y_n - x` we have, by the triangle inequality and `L^1`-continuity of translations,
`‖a_i(y_n + r_n·) - f‖_1 ≤ ‖a_i(x + h_n + r_n·) - a_i(x + r_n·)‖_1 + ‖g_{r_n} - g_1‖_1 → 0`.
The vectors `v_n = (a_s(y_n + r_n e))_s` are bounded in `L^∞(S;R^6) = (L^1)^*`, which is
weak-* compact and metrisable (`L^1(S;R^6)` separable); pass to a weak-* convergent
subsequence with limit `b`. Because the `(y_n,r_n)` are typical samplings, `b ∈ W_x`. Because
the `i`-th component converges in `L^1`, hence weakly against every `L^∞` test function, the
`i`-th component of `b` equals `f`. Therefore
`{e : a_i(x+e) = 1} ⊆ {e : b_i(e) > 0} ⊆ D_{x,i}` modulo angular null sets, i.e.
`c(x+e) = i ⟹ i ∈ P_x(e)` a.e. `∎`

**Remark.** This is the sharp form of the authors' remark "constant sequences are permitted"
in Definition 5.1: radius exactly one at centre exactly `x` need not be a typical sampling, but
one can approach it by typical samplings so that the sampled indicators converge in `L^1`. It is
used in the paper only implicitly ("its actual color cannot be i", and the "exact radius-one
circle sampling ... using a constant sequence" step in the proof of Proposition 5.6); stating
it as a lemma is what makes §3 possible.

---

## 3. Corollary Q and Theorem R: a free label is a null colour class

**Corollary Q.** If label `i` is free at `x`, i.e. `i ∉ P_x(e)` for `σ`-a.e. `e`, then the unit
circle about `x` meets `A_i` in angular measure zero: `σ{e : x+e ∈ A_i} = 0`.

*Proof.* Lemma P: `c(x+e) ∈ P_x(e)` a.e. `e`; if `i ∉ P_x(e)` a.e. then `c(x+e) ≠ i` a.e. `∎`

**Theorem R.** Suppose label `i` is free at almost every centre:
`i ∉ P_x(e)` for `σ`-a.e. `e`, for almost every `x ∈ R^2`. Then `|A_i| = 0`.

*Proof.* By Corollary Q, for a.e. `x` the section `{e : x+e ∈ A_i}` is `σ`-null. The function
`G(y) = σ{e : y+e ∈ A_i} = (1/2π)∫_0^{2π} 1_{A_i}(y + e^{it}) dt` is the circular average of the
Borel function `1_{A_i}`, hence Borel, and `G = 0` a.e. Therefore
`|A_i| = ∫ 1_{A_i}(y) dy = ∫_S ∫_{R^2} 1_{A_i}(y+e) dy dσ(e) = ∫_{R^2} G(y) dy = 0`. `∎`
(For the second equality use that `y ↦ y+e` is a measure-preserving translation for each `e`,
so the inner integral is `|A_i|` for every `e`.)

**Corollary R2 (no globally free label).** No weak measurable 6-colouring has a label which is
free at almost every centre. Equivalently: if a palette field `P` is the maximal palette field
of a weak measurable 6-colouring, then for every label `i`,
`{x : i ∉ P_x(e) for σ-a.e. e}` is not conull; indeed `|A_i| > 0` for all `i`, so each label
`i` is free on the positive-measure set of typical points of `A_i` (Lemma D) and on no conull
set (Theorem R).

**Corollary R3 (a fixed palette range is fatal).** Suppose `U_0 ⊆ {1..6}` with `|U_0| <= 5` and
`P_x(e) ⊆ U_0` for `σ`-a.e. `e` and almost every `x`. Then there is no weak measurable
6-colouring with palette field `P`. *Proof.* Lemma P gives `c(x+e) ∈ U_0` for a.e. `(x,e)`;
integrating over `e` for each `x` in the full-measure set, `c ∈ U_0` a.e., so `c` is a weak
measurable colouring with at most five labels, contradicting Theorem 1.4. `∎`

Corollary R3 contains every **translation-invariant** palette field as a special case (take
`U_0 =` the union of the values of the word), and also every field whose values are drawn from
a fixed five-element set. Note that R2 is *implied by* R3 in the sector models but not in
general: R2 does not need the range to be fixed.

### 3.1 What this settles, and why the old frontier statement was too weak

`sprint/k6/REPORT.md` §5 and `sprint/k6/FREE-LABEL.md` say: the free-label models satisfy every
palette axiom, and are removed only by **properness of a label function avoiding the palettes**
(or by trace-consistency). Two independent sharpenings of that statement are now on the board:

* **(TE)** (m1's f4, m4's f1): the paper's (5.3) has *no distance restriction*, so a colouring's
  palettes at unit-separated centres in the *same* direction are disjoint. Every
  centre-independent field therefore satisfies `word(f) ∩ word(f) = ∅`, i.e. is empty — so no
  translation-invariant field whatever is a colouring's palette field, with no free label and no
  properness needed.
* **Theorem R below** (this note): a label which is free at almost every centre forces its class
  to be null, *without* assuming position-independence. So the position-dependent repair of the
  free-label models (make the free label vary with the centre) is also dead at the level of the
  palette axioms.

What neither argument needs is any "proper label function". The free-label models are removed
inside the palette framework, not outside it.

Concretely:

* `FREE-LABEL.md`'s 36-sector word (label `0` free at every centre, values inside `{1..5}`):
  dead by **R3** (its range is the fixed set `{1,2,3,4,5}`), by R2, and by (TE).
* The pair-only translation-invariant words at `m = 6,9,12` that d1 is extracting (values from
  `{{1,3},{1,4},{1,5},{2,4},{2,5},{3,5}}`, label `0` free): dead by the same arguments, whether
  or not they exist. **Their existence therefore cannot produce a countermodel to local
  finiteness**; the only open question they bear on is the palette-level satisfiability
  statement restricted to the `d <= d_0` fragment of (5.3). (That is a triage statement, not a
  criticism: the palette-level statement is what `FREE-LABEL.md` claims, and m1's f3 decides it.)
* The single-centre orbit words (510 at `ell = 6`) and the m15 three-block construction are
  unaffected — they never asserted a globally free label *at every centre* in a colouring.

### 3.2 Sharpness: the hypothesis "at almost every centre" cannot be weakened

Theorem R is optimal in the only direction in which an optimality statement makes sense.
Lemma D says that at *every* typical centre `x` of colour `i`, the label `i` is free at `x`. So
for each label, the free set
`F_i := {x : i ∉ P_x(e) for σ-a.e. e}` contains all typical points of `A_i`, a set of positive
measure. Hence the hypothesis of Theorem R ("free at a.e. centre") is false for every label of
every weak measurable 6-colouring, and no statement of the form "if `F_i` has positive measure
then `A_i` is null" can hold. The exact dichotomy is

  `F_i` conull  ⟹  `A_i` null (Theorem R),  and conversely `A_i` positive measure forces
  `R^2 \ F_i` positive measure.

Corollary Q adds the geometric content: `F_i` is contained (modulo null sets) in the complement
of the unit-distance neighbourhood `A_i + S^1 = {q : ∃a ∈ A_i, |q-a| = 1}`, while `F_i`
contains the density points of `A_i`. So a free centre of `i` is a point whose *unit circle*
misses the class `A_i` essentially, and every typical point of `A_i` has this property for its
own class.

---

## 4. The sharp necessary condition on any candidate countermodel

Combining Lemma P with Lemma D, **every** weak measurable 6-colouring satisfies, at every
fixed centre `x`:

  (S1) `c(x+e) ∈ P_x(e)` for `σ`-a.e. `e`   (Lemma P: the palette contains the circle colour);
  (S2) `c(x) ∉ P_x(e)` for `σ`-a.e. `e` at a.e. `x`   (Lemma D: self-avoidance);
  (S3) `P_{x+a}(f) ∩ P_x(f) = ∅` for every unit `a` and a.e. `f`   ((TE), no distance restriction).

Writing `U_x := ∪_e P_x(e)` (the palette range at `x`), (S1) is equivalent to

  (S1') `c(q) ∈ U_{q-e}` for `σ`-a.e. unit `e`, for a.e. `q`  —

*the colour of a point must lie in the palette range of almost every centre at unit distance
from it.* This is a new necessary condition at `k = 6`, and it is the constraint that all the
abstract models violate. It implies in particular:

  (S1'') for every positive-measure set `E` of unit directions, `c(q) ∈ U_{q-e}` for a.e.
  `e ∈ E`; in particular, if the palette range is position-independent, or constant on a
  positive-measure set of centres meeting the circle about `q`, the colouring is confined to that
  range; in PDI language, every colour used at `q` lies in `U_s ∩ C_{r(q)}` for every type `s`
  met by the circle about `q` in positive angular measure.

So a countermodel — a palette field that *is* the maximal palette field of a weak measurable
6-colouring — must have position-dependent palette ranges which interlock as in (S1'') and
admit a proper 6-colouring in the sets `C_r`. That is a restatement of the problem, not a
relaxation of it: by (S1)-(S2) the free-label field of a colouring is not an independent object,
it is the colouring (`F_i ∋ x` whenever `c(x) = i`, and `⋃_i F_i = R^2` because palettes are
nonempty a.e.).

---

## 4.1 PDI rigidity: the type partition of a piecewise direction-invariant field must itself be a proper colouring

Call a palette field **PDI** if there are a finite measurable partition `R_1,...,R_N` of `R^2`,
a measurable type map `r : R^2 -> {1..N}` and direction words `word_s` with
`P_z(e) = word_{r(z)}(e)` for all `z` and a.e. `e`. (Every sector model in the project is PDI:
Theorem C, `FREE-LABEL.md`, and §5 below. For those, `N = 1`.)

**Theorem X (PDI rigidity).** Let `P` be a PDI palette field which is the maximal palette field
of a weak measurable `k`-colouring `c`, and put `U_s = ∪_e word_s(e)`,
`C_s = {1..k} \ U_s`. Then:

  (X1) for **every** `z ∈ R^2` and **every** unit vector `a`, `r(z+a) ≠ r(z)`. Hence `r` is a
       proper colouring of the plane's unit-distance graph, and `N >= 6`;
  (X2) for every `z` and a.e. unit `a`, with `s = r(z+a)`: `word_{r(z)}(a) ∩ word_s(a) = ∅`
       — disjointness in the **same** direction, not only at ±60°;
  (X3) `c(z) ∉ U_{r(z)}`, and `c(z+a) ∈ word_{r(z)}(a) ∩ C_{r(z+a)}` for a.e. `a`; in particular
       `word_{r(z)}(a) ⊄ U_{r(z+a)}` for a.e. `a`.

*Proof.* (TE) applied to the pair `(z, z+a)` gives `word_{r(z+a)}(f) ∩ word_{r(z)}(f) = ∅` for
a.e. `f`, which is (X2). If `r(z+a) = r(z) = r`, this reads `word_r(f) ∩ word_r(f) = ∅` for
a.e. `f`, i.e. `word_r = ∅` a.e., contradicting nonemptiness of palettes a.e. (Definition 5.1);
this is (X1). The first half of (X3) is Lemma D, the second is Lemma P, and `⊄` follows from
(X2) together with nonemptiness of `word_{r(z)}(a)`. `∎`

**Consequences.**

1. *No cell contains a unit-distance pair.* So `R_s` is, for every `s`, an essentially
   unit-distance-free measurable set, i.e. the type partition `r` is a proper measurable
   `N`-colouring of the plane with `N >= 6`. **The PDI hypothesis is therefore equivalent to:
   the palette depends on position only through a proper measurable colouring of the plane.**
   (An exhaustive `N = 1`-type field is exactly the centre-independent case killed by (TE);
   Theorem X also kills every mixed-cell field whose cells are not unit-distance-free, e.g. any
   field with a half-plane or large-tile cell.)
2. *Every pair of types that is unit-adjacent must have same-direction disjoint words.* Since a
   pair value has size `2` or `3` (admissible), at most three types can be pairwise
   unit-adjacent. So the proper colouring `r` must have a **sparse unit-adjacency graph** — it
   cannot be a fine tiling in which every type is met at unit distance from almost every point.
   (For such a "dense" pattern the words would have to be pairwise same-direction disjoint, so
   `N <= 3`, contradicting `N >= 6`.)
3. *The free label cannot be constant on a PDI field either*: by Theorem R a globally free label
   is impossible, and by (X3) the label available at `z` must lie in `C_{r(z)}` while the colours
   at unit distance lie in `U_{r(z)}`; so the free label tracks the type map, which by (X1) is a
   proper colouring.

**What Theorem X does *not* do** is exclude the residual class: a proper measurable `N`-colouring
(`N >= 6`) with unit-adjacency graph of degree `<= 3` (pairwise same-direction-disjoint words) and
a colouring `c` satisfying (X3). That class is not empty as far as this note proves, and it is not
the original problem either; it is the exact residue of the PDI programme. (Note that a
*non-PDI* position dependence — infinitely many types, or words varying inside a type — is not
covered by Theorem X at all.)

---

## 5. The free label *can* vary with the centre: an explicit verified palette field

The handoff asks: "Can the free label vary with the centre while preserving the exact
transport?" **For the `d <= d_0` transport fragment used by every sector model in the project:
yes** — here is a two-cell model, verified exactly. (For the paper's full (5.3), which includes
the distance-one instance (TE), no: see Theorem X and §5.5.)

### 5.1 The model

Fix `m >= 1`, `n = 6m`, `Δ = 2π/n`, sector `k = [kΔ, (k+1)Δ)`. Let
`cell 1 = {x : x_1 < t}`, `cell 2 = {x : x_1 >= t}` for `t = (9/20)(d_0/3)` with
`d_0 = π/(9m)` (any `t` works for the palette field; this one is used in §5.3), and put

  `P_z(e^{iθ}) = A_k` for `z ∈ cell 1`, `θ ∈ sector k`;   `P_z(e^{iθ}) = B_k` for `z ∈ cell 2`,

where, for `m = 6` (`n = 36`, `2m = 12`-periodic, so the word is given on `Z/12`):

```
 k :  0      1      2      3      4      5      6      7      8      9     10     11
 A : {2,5}  {2,5}  {3,5}  {3,5}  {1,3}  {1,3}  {1,3}  {1,4}  {1,4}  {2,4}  {2,4}  {2,5}
 B : {0,2}  {0,2}  {0,3}  {0,3}  {1,3}  {1,3}  {1,3}  {1,4}  {1,4}  {2,4}  {2,4}  {2,4}
```

(so `A_{k+12} = A_k`, `B_{k+12} = B_k`, and the same table lifted to `Z/36`). Because
`2m = 12` divides `n = 36`, the reduced word on `Z/12` determines the whole field.

Analogous witnesses exist at `m = 9` (`2m = 18`-periodic) and `m = 12` (`2m = 24`-periodic);
they are in `two_cell_witness_pairs.json`.

### 5.2 Exactly which constraints are verified

With `S_m = {±(m-1), ±m, ±(m+1)} mod n` (the transport offsets of the project, see §5.4):

1. **Admissibility.** Every value is a pair, not contained in any cycle edge of `C_6`; so
   `|P| = 2` and `P ⊄ {i,i+1}` at every centre and every direction — (P1) and (P4) of Theorem C,
   and the admissibility hypothesis of Lemma 6.2 at a six-cycle centre.
2. **Sixty-degree exclusion (5.7)**: `A_k ∩ A_{k+m} = ∅`, `B_k ∩ B_{k+m} = ∅` for all `k`.
3. **Exact transport.** For every `k` and every `s ∈ S_m`: `A_k ∩ A_{k+s} = ∅`,
   `B_k ∩ B_{k+s} = ∅` (pairs of centres in the *same* cell) and `A_k ∩ B_{k+s} = ∅` (pairs of
   centres in *different* cells). Since `S_m = -S_m`, this covers all ordered choices of
   `(z,z')` at distance `<= d_0`, whichever cells they lie in, i.e. it is exactly (5.3)/(P3)
   for the field `P`.
4. **Free labels.** `0 ∉ ∪_k A_k` and `5 ∉ ∪_k B_k`; and `0 ∈ ∪_k B_k`, `5 ∈ ∪_k A_k`. So the
   free set of cell 1 is `{0}` and of cell 2 is `{5}`: **the two cells have different free
   labels**, and the single label function `φ` with `φ(z) = 0` on cell 1 and `φ(z) = 5` on
   cell 2 satisfies the non-proper self-avoidance `φ(z) ∉ P_z(e)` for all `z` and a.e. `e`.
5. **Pairs only.** There is no triple anywhere, so m11's ternary density bound and the
   complementary-triple exclusion (P6) are vacuous, and m2's two-centre bound
   `|P_x(e)| + |P_y(e)| <= 5` reads `2+2 = 4 <= 5`, automatically satisfied. (Handoff item 2.)
6. **The trace condition (P5).** For each cycle edge `{i,i+1}` a trace supported in the palette
   must kill both edge labels, i.e. each value must not be contained in a cycle edge — this is
   item 1 again, and it holds for every value of both words.
7. **Accumulating six-cycle centres.** Every value of both words is admissible for `C_6`, so
   (6.2) holds for every edge of `C_6` at *every* centre and a.e. direction: every point of the
   plane satisfies the palette-level necessary condition for being a six-cycle centre. (As in
   Theorem C / `FREE-LABEL.md`: the models realise the *necessary* conditions, not the
   transition-set condition (6.1) of Definition 6.1, which involves a colouring.)

### 5.3 The free label varies along the accumulating sequence

With `y_k = (d_0/3) 2^{-k} (3/5,4/5)`, `k >= 0`, the points are distinct and `y_k → 0`, and all
of them are at distance `<= d_0` from each other, so the transport condition applies to the
whole sequence. With the boundary `x_1 = t = (9/20)(d_0/3)`:

* `y_0 = (d_0/3)(3/5,4/5)` has `x_1 = (3/5)(d_0/3) >= t`, so `y_0 ∈ cell 2`, free label `5`;
* `y_k` for `k >= 1` has `x_1 = (3/5) 2^{-k} (d_0/3) <= (3/10)(d_0/3) < t`, so `y_k ∈ cell 1`,
  free label `0`.

So the accumulating family of six-cycle centres carries the free-label sequence
`5, 0, 0, 0, ...`: **the free label varies with the centre**, and it varies already inside a
single orbit of the accumulation structure. (Check: `3/5 = 0.6 >= 0.45 = 9/20`, and
`3/10 = 0.3 < 0.45`.)

### 5.4 Geometry: why `S_m` is the right offset set, in exact rational arithmetic

The two exact unit decompositions of `(z'-z) + w` satisfy
`|arg s_± - (arg w ± π/3)| <= 1.5938 |z'-z|` (m15, exact rational arithmetic, two code paths;
cited in `sprint/k6/REPORT.md` §4). With `|z'-z| <= d_0 = Δ/3` the displacement is at most
`1.5938/3 = 0.53127` sectors `< 1` sector, so the sector index of `s_±` is `m + {-1,0,1}`, and
this is verified here in exact rational arithmetic:

  `1.5938 · d_0 = (15938/10000)/9 · π/m = (7969/45000) π/m < (1/3) π/m = Δ`.

Both decompositions must be used (they are the two roots of `s+t = (z'-z)+w`, `|s| = |t| = 1`,
which for `|z'-z| > 0` are exactly two), and since `S_m = -S_m` the two signs give the same
offset set. `verify_two_cell.py` checks the inequality with `fractions.Fraction` and checks the
constraints for all `s ∈ S_m`.

### 5.5 What the model does **not** do

It is a palette field, not a colouring, and it cannot be repaired into one. The model satisfies
the `d <= d_0` fragment of (5.3) used by every sector model in the project; it fails the paper's
full (5.3) already at distance one:

* **(0) It violates (TE) = (S3).** Inside one cell there are unit-separated pairs in the same
  direction, so (TE) would need `word_r(f) ∩ word_r(f) = ∅`. `verify_two_cell.py` reports
  `36/36` sectors with a nonempty self-intersection (and `36/36` across the cells, since
  `A_k ∩ B_k ≠ ∅`). So the model is not a colouring's palette field, and Theorem X says that no
  repair which keeps a cell of diameter `>= 1` can work.
* **(a) No proper label function.** Any `φ` with `φ(z) ∉ P_z(e)` a.e. must satisfy
  `φ ≡ 0` on cell 1 and `φ ≡ 5` on cell 2, i.e. it takes two values; since `χ(R^2) >= 6`
  (Theorem 1.4) it is not a proper colouring of the plane.
* **(b) It violates Lemma P.** For `x` deep inside cell 1 and a.e. direction `e` pointing
further into cell 1, `φ(x+e) = 0 ∉ P_x(e)` (no `A`-value contains `0`). So `P` is not the
maximal palette field of any colouring with this or any other label function: Lemma P is
exactly the missing hypothesis.
* **(c) It violates (S1').** Any colouring consistent with `P` would have
`c(q) ∈ U_{q-e}` for a.e. `e`; since `U_{cell 1} = {1,2,3,4,5}` and `U_{cell 2} = {0,1,2,3,4}`,
a point `q` whose unit circle lies a.e. in one cell is forced into that cell's `U`, while its own
colour must lie in that cell's `C`. So no 6-colouring uses this field.

**Therefore the model is *not* a counterexample to local finiteness at `k = 6`**, and neither is
it a repair of the free-label family: it shows that the `d <= d_0` fragment of the palette axioms
is satisfiable *even with a position-dependent free label*, and that the constraint which kills
the repair is (TE) — which every sector model in the project, with fixed or varying free label,
fails identically. What survives is exactly Theorem X's residual class, plus the missing
hypothesis "`P` is the maximal palette field of a proper 6-colouring", i.e. `χ(R^2) <= 6`.

### 5.6 Non-vacuity: the paper's own 7-colouring fails Theorem R's hypothesis maximally

`vacuity_hex.py` checks the paper's hexagonal 7-colouring (Voronoi hexagons of the triangular
lattice, circumradius `2/5`, centre `d(m+nω)` with `ω = e^{2πi/3}`, `d = √3·(2/5)`, colour
`(m+2n) mod 7`):

* (V1) it is proper: the minimal distance between two same-coloured centres is `√7 d = √(84/25)
  = 1.833`, so two same-coloured hexagons (circumradius `0.4`) are at distance `>= 1.033 > 1`;
* (V2) Lemma Z applies: on 49 sampled centres, every sampled circle point is at distance
  `>= 0.12` from a cell boundary, so the palettes are singletons;
* (V3) at every one of the 49 sampled centres the unit circle meets exactly six of the seven
  labels — it misses exactly the centre's own colour (this is Lemma D made visible) — and each
  label `i` is free at only `7/49` of the sampled centres, never at almost all of them.

So Theorem R's hypothesis ("some label free at a.e. centre") is false for a genuine colouring in
the strongest possible way, and it is *true* for every model of §5 and of `FREE-LABEL.md`. The
theorem separates the two classes exactly.

---

## 6. The frontier, stated exactly

Let `PAL(k=6, ell)` be the set of palette fields `P` with

  (i) `1 <= |P_z(e)| <= 3` and `P_z(e)` not inside a cycle edge of `C_ell`, all `z`, a.e. `e`;
  (ii) `P_z(e) ∩ P_z(Re) = ∅` ((5.7));
  (iii) the `d <= d_0` fragment of the exact transport (5.3) — the offsets
  `±(m-1), ±m, ±(m+1)` — for all pairs of centres at distance `<= d_0`;
  (iv) an `ell`-locus with accumulating centres.

and let `PAL+` be `PAL` with **(TE)** `P_{x+a}(f) ∩ P_x(f) = ∅` for every unit `a` (the full
(5.3), the instance of Remark 5.3), and let `PAL++` also require (S1) and (S2). Then:

| statement | status |
|---|---|
| `PAL + a globally free label` is realisable by a colouring | **impossible** (Theorem R, R3) |
| `PAL + non-proper self-avoidance, fixed free label` | realisable (Theorem C, `FREE-LABEL.md`; m1's f3 decides which `m`) |
| `PAL + non-proper self-avoidance, *varying* free label` | **realisable** (§5; `m = 6,9,12`, verified) |
| `PAL+ + any PDI structure with a cell containing a unit pair` | **impossible** (Theorem X; equivalently (TE), m1's f4 / m4's f1) |
| `PAL+ + PDI` | forced into Theorem X's residual class: the type map is a proper measurable `N`-colouring, `N >= 6`, with sparse unit-adjacency and same-direction-disjoint words — **not decided** |
| `PAL++ + properness` | **exactly the `k = 6` local-finiteness problem** |

So the exact delimitation is three-layered. The `d <= d_0` fragment of the palette axioms is
satisfiable even with a position-dependent free label (§5). The full palette axioms, which include
the distance-one instance (TE) of (5.3), exclude the entire piecewise direction-invariant class
whose cells are not unit-distance-free, and reduce the rest to a design problem over a proper
measurable `N`-colouring (`N >= 6`). What remains is 6-colourability itself. `k = 6` stays open;
what is new here is that no palette-level hypothesis is missing — the fragments of (5.3) that the
models satisfy are exactly the ones that leave them alive, and the missing one is (TE).

---

## 7. What a proper 6-colouring must do that the models cannot: the six-cycle forces accumulation

**Lemma T.** Let `c` be a weak measurable 6-colouring and `x` a six-cycle centre (i.e. `Γ_x`
contains a `C_6` on all six labels). Then for a.e. direction `e`, `|P_x(e)| >= 2`; and by
Lemma P, for a.e. `e` there is a label `j ≠ c(x+e)` with `j ∈ P_x(e)`, i.e. **some colour class
other than that of `x+e` accumulates at `x+e`.** Since `e` is arbitrary, this holds for a.e.
point of the unit circle about `x`.

*Proof.* Nonemptiness of `P_x(e)` a.e. (Definition 5.1); (6.2) gives `P_x(e) ⊄ {i,i+1}` for each
of the six cycle edges, and every label lies in some cycle edge, so `|P_x(e)| ≠ 1`. Lemma P then
supplies `c(x+e) ∈ P_x(e)`, and any other member `j` lies in `D_{x,j}`: `e` is in the essential
union of the sets `{b_j > 0}` over `b ∈ W_x`, so label-`j` mass accumulates at `x+e` along the
traces at `x`. `∎`

**Consequence: `ell = 6` is the unique cycle length at `k = 6` for which singletons are
forbidden.** For a triangle, four-cycle or five-cycle on labels `V ⊊ {1..6}`, any label
`b ∉ V` gives an admissible singleton `{b}` (it is contained in no cycle edge), so tame palettes
are allowed; for the six-cycle `V = {1..6}` and every singleton is excluded.

**Lemma Z (tame colourings have singleton palettes).** Let `c` be a measurable colouring which is
constant on each cell of a countable partition of `R^2` whose boundary `Σ` is a countable union of
segments and circular arcs (or of images of `C^1` curves). Then for a.e. `(x,e) ∈ R^2 × S`,
`x + e` lies in the interior of its cell, and hence `P_x(e) = {c(x+e)}`.

*Proof.* For a segment `σ`, the set `{(x,e) : x+e ∈ σ}` is the image of `σ × S` under the smooth
map `(q,e) ↦ (q - e, e)` from a two-dimensional manifold into the three-dimensional manifold
`R^2 × S`, hence has measure zero; the same holds for arcs. Countably many pieces give a null
set. Off it, `x+e` is interior to its cell, so a ball `B(x+e,ρ)` lies in the cell, and every
typical sampling with `y_n → x`, `r_n → 1` samples `y_n + r_n e ∈ B(x+e,ρ)` for large `n`; hence
every trace at `x` equals `δ_{c(x+e)}` at `e`, and `P_x(e) = {c(x+e)}`. `∎`

Hence, by Lemma T: **a colouring of the tameness class in Lemma Z has no six-cycle centre, at
any `k`.** m3's `k >= 7` construction is exactly of this class and its cyclic centres carry
triangles with singleton palettes `{b}` for outsider labels `b ∉ {0,2,3}` — admissible at
`k >= 7`, and impossible at `k = 6` for a six-cycle. This is the structural reason the phase
transition sits at `k = 6`, and the precise sense in which a `k = 6` countermodel must be
*non-tame*: it must have genuine accumulation of a second class at almost every point of the
unit circle of every six-cycle centre.

---

## 8. Consistency with the rest of the record

* `FREE-LABEL.md`'s claim — "adding non-proper self-avoidance to the palette constraints does
  not exclude any cycle length; only properness removes these models" — is corrected twice over.
  Its models satisfy only the `d <= d_0` fragment of (5.3); the full constraint (TE) at distance
  one removes them (m1's f4, m4's f1, and §5/Theorem X for the position-dependent repair). And
  even within that fragment, a global free label is already fatal (Theorem R/R3), so no label
  function and no properness is needed to kill them.
* m2's two-centre bound (`|P_x| + |P_y| <= 5` for unit `x,y`, same direction) is untouched and
  is not the binding constraint: the pair-only models of §5 satisfy it with slack (`2+2 <= 5`).
  Theorem R is strictly stronger for every model in this family.
* m11's ternary density, m14's neutrality, m1's single-centre classification: unaffected — §5's
  models have no triples and pass all of them (item 5 of §5.2).
* m3's `k >= 7` counterexample: unaffected, and §7 explains why its mechanism cannot reach
  `k = 6` (its palettes are singletons; `k = 6` six-cycles forbid singletons).
* Theorem C ("the palette-level route is dead") is refined by §6: its countermodels satisfy only
  the `d <= d_0` fragment of (5.3), and the full constraint kills them via (TE) — a conclusion
  m1's f4 and m4's f1 reach for centre-independent fields, and Theorem X extends to every PDI
  field whose cells are not unit-distance-free.
* Relation to the other findings in this swarm: (TE) is **not** claimed as new here — m1's f4 and
  m4's f1 have it, with the paper citation (Remark 5.3) and the Lean cross-check. What is new in
  this note is (i) a proof of Lemma P as a lemma for every centre, (ii) Theorem R (the a.e.-free
  label forces a null class, with no position-independence hypothesis), (iii) Theorem X (the type
  partition of a PDI field is itself a proper measurable colouring with `N >= 6`, same-direction
  disjointness, and the (X3) constraints), (iv) the verified varying-free-label model of §5, which
  is the sharp demonstration that the `d <= d_0` fragment is not the hypothesis set even after the
  natural repair, (v) Lemma T and Lemma Z on why `k = 6` forces non-tameness.

---

## 9. Files and the exact commands

All paths relative to the project root.

| file | content |
|---|---|
| `.ultramath/smwfwznwk/m2/COLOURING-LEVEL.md` | this note |
| `.ultramath/smwfwznwk/m2/two_cell_band.py` | CaDiCaL search for a two-cell field with different free labels (pairs + triples allowed) |
| `.ultramath/smwfwznwk/m2/two_cell_band_pairs.py` | the same restricted to pairs (the witness of §5) |
| `.ultramath/smwfwznwk/m2/two_cell_free.py` | the *narrow* (only the exact 60-degree offsets) two-cell CSP, decided by cyclic DFS in ~4 s: it is satisfiable with a free label in both cells, which is why the wider *band* version was needed (`two_cell_csp.py` is the unrestricted and much slower variant of the same search, kept for reference only) |
| `.ultramath/smwfwznwk/m2/two_cell_witness_pairs.json`, `two_cell_witness.json` | the witnesses (SAT output) |
| `.ultramath/smwfwznwk/m2/verify_two_cell.py` | the independent verifier (§5.2 items 1-7, §5.3, §5.4): **no SAT**, direct enumeration plus an independent cyclic-DFS reconstruction |
| `.ultramath/smwfwznwk/m2/vacuity_hex.py`, `logs/vacuity_hex.out` | the non-vacuity test of §5.6 on the paper's 7-colouring |
| `.ultramath/smwfwznwk/m2/logs/verify_two_cell.out` | recorded output of the verifier (`ALL CHECKS PASS`, exit 0) |

**The command that checks the model of §5.**

```
cd <project root>/.ultramath/smwfwznwk/m2
python3 verify_two_cell.py            # exits 0, prints "ALL CHECKS PASS"
```

It re-checks, for `m = 6,9,12`: admissibility of every value; within-cell and cross-cell
disjointness at all six transport offsets over all `6m` sectors (and again on the reduced
`2m`-sector word); (5.7) at sixty degrees; the free-label facts; the exact rational deviation
bound; the accumulating centres and their cells; and it re-finds a two-cell pair by an
independent DFS that uses no SAT solver. It also prints the 12-row table of §5.1 as a
hand-checkable certificate for `m = 6` (72 disjointness checks, each a two-element set
intersection).

**Reproducing the search** (CaDiCaL at `/opt/lean/bin/cadical`, `pysat` also available):

```
python3 two_cell_band_pairs.py        # prints SAT at m=6,9,12 and rewrites the witness json
python3 two_cell_band.py              # same with triples allowed
python3 vacuity_hex.py                # non-vacuity test of §5.6, exits 0
```

**Extraction of the paper's definitions** (both extractors must agree; §1's citations):

```
pdftotext -layout attachments/here-are-three-files-ni5n/paper.pdf scratch/paper.txt
pdftotext -raw    attachments/here-are-three-files-ni5n/paper.pdf scratch/paper_raw.txt
grep -n -A12 "Definition 5.1"   scratch/paper_raw.txt   # W_x, D_{x,i}, P_x
grep -n -A6  "Lemma 5.2 (Palette" scratch/paper_raw.txt # (5.2), (5.3)
grep -n -A4  "Corollary 5.4"    scratch/paper_raw.txt   # (5.7)
grep -n -A6  "Lemma 6.2 (An edge" scratch/paper_raw.txt # (6.2)
grep -n -A8  "Definition 1.2"   scratch/paper_raw.txt   # weak measurable colouring
```

The two extractions agree on every symbol used in §2-§4 (this is the substitute for a
`pdftoppm` visual check: the mathematics is transcribed from two independent text extractions,
and the only formulas used — (5.2), (5.3), (5.7), (6.2), Definition 5.1 — are identical in
both).

**Status of each claim.**

| claim | status |
|---|---|
| Lemma P, Corollary Q, Theorem R, R2, R3, Theorem X, Lemma T, Lemma Z | proved here from the paper's definitions (§2-§4.1, §7); (TE) is cited from m1's f4 / m4's f1 |
| `PAL` (the `d <= d_0` fragment) + varying free label is satisfiable at `m = 6,9,12` | finite computation, two independent procedures (§5, §9) |
| no `PAL` model — fixed or varying label — satisfies (TE) | verified for §5's model; proved for every centre-independent model (m1 f4, m4 f1) and, via Theorem X, for every PDI field with a cell of diameter `>= 1` |
| the free label is exactly the colour at a.e. typical centre; a globally free label is impossible | Theorems R2/R3 |
| the six-cycle forces `|P| >= 2` and a second accumulating class | cited (Lemma 6.2 + (6.2)) + Lemma P (§7) |
| Theorem R is not vacuous (a genuine colouring fails its hypothesis) | numerical check on the paper's 7-colouring (§5.6) |
| `k = 6` local finiteness | **open** — not touched here |
| `chi(R^2) >= 7` | **not proved** |
