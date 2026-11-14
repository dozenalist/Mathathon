# Where the cover-and-palette method consumes `k`; route B cannot repair it, and the length-4
# interface at `k = 6` transfers

**Status.** A theorem with a complete proof about a precisely delimited class of arguments, an exact
computation certificate, the L4 specification, and one computed example (Theorem 4.1) on which a
proposed replacement mechanism applies at `k = 6` where the printed method's corresponding step does
not. It does **not** claim `chi(R^2) = 6` or `= 7`, nor any new bound on `chi(R^2)`. It uses only the
accepted state of record R1-R6 and W1-W7, and only the paper's numbered inputs (5.2), (5.7), (5.12),
(6.2), (8.1) and Proposition 7.1.

---

## 0. The class of arguments

**Definition 0.1 (interface-sliver argument).** An *interface-sliver argument at `k`* is an argument
that, given a weak measurable `k`-colouring, proceeds through five steps, each consuming only the
listed input.

1. *(existence)* Proposition 7.1 supplies a point `x`, a simple label cycle `i_0,...,i_{l-1}` with
   `3 <= l <= k`, compact connected sets `K_j` and limiting rays `v_j` in `S`, with both endpoint
   supports of edge `j` excluded from `Delta(K_j)`.
2. *(sliver)* Lemma 8.1 turns the exclusion into one-sided strip restrictions: for `e` outside the
   finite antipodally symmetric set `B` of directions perpendicular to some `v_j`, an open strip on
   the positive side of radius one uses only `O(e)` a.e., and one on the negative side uses only
   `I(e)`, where `O(e)` (resp. `I(e)`) is the label set left after deleting the endpoints of every
   positive (resp. negative) edge, signs from `sign(e . v_j)`. The only further input is (8.1):
   `P_x(e) cap O(e)` and `P_x(e) cap I(e)` are both nonempty for a.e. `e`.
3. *(local rigidity)* the sliver's colouring is reduced to a constant by finitely many unit-edge
   exchanges inside the sliver, so an outsider state `s(e)` exists and is locally constant in `e`
   away from finitely many directions.
4. *(exclusion)* (5.2) at a sum of two nonparallel unit directions in opposite-valued sectors
   excludes both sliver values at the sum, so an open region near `x` uses only the `k - 2` remaining
   labels.
5. *(terminal gadget)* a finite unit-distance graph with exact coordinates placed in that region is
   not colourable with those labels, contradicting the assumed `k`-colouring.

The printed sections 5-8 are an interface-sliver argument: step 1 is Proposition 7.1, step 2 is
Lemma 8.1/8.10, step 3 is Lemma 8.6, step 4 is Lemma 8.8, step 5 is the Moser spindle placed by
(8.6). The class is closed under replacing (5.12) by any stronger palette bound and under adding any
hypothesis on palettes - which is exactly what route B proposes.

**Theorem 0.2 (no-go at `k = 6` for `l = 3`, all `k`, all palette constants).** *Let an
interface-sliver argument at `k` reach step 3 at an interface of length `l`. Then the sliver carries
at least `k - l` labels at every direction `e` not in `B`. Step 3 needs the sliver to carry at most
two labels, and exactly two by (8.1) together with the `R`-flip of (5.7); so step 3 is available only
if `k - l <= 2`. Since Proposition 7.1 guarantees only `3 <= l <= k`, a value of `k` for which the
class is available at every interface length it can produce must satisfy `k - 3 <= 2`, i.e.
`k <= 5`. At `k = 6` the interface length `l = 3` lies outside the class, for every value of every
palette constant.*

Theorem 0.2 is Theorem 1.3 plus the arithmetic of step 2; both are proved below, and all counts are
verified by exhaustion (`work/verify.py`, Section 6).

**Why this is not a strawman.** The class contains the paper's own argument, which does decide `k = 5`
(giving `chi >= 6`). Nothing is assumed about the shape of the colouring, no regularity beyond weak
measurability, no relation between labels and geometry; and Theorem 4.1 below shows the class is
*not* vacuous at `k = 6` either - it does handle `l = 4`. The no-go says what the paper's own barrier
analysis does not say: not that Proposition 5.6 is too weak, but that **the sliver, not the palette,
is the binding cardinality at `l = 3`**, and the two are independent (Theorem 2.1).

---

## 1. The sliver invariant

Fix `k`, an interface cycle of length `l` with cycle labels `T = {0,...,l-1}` (edge `j` joins `j`
and `j+1`, indices mod `l`), and the `m := k - l` outsiders (labels outside `T`). For `e` not in `B`
let `w(e)` in `{+1,-1}^l` be the sign word `w_j = sign(e . v_j)`.

`O(e)` = labels left after deleting the endpoints of every positive edge; `I(e)` = the same for
negative edges; labels outside the cycle lie in both sets (paper, Section 8.1).

**Lemma 1.1.** *`j` in `T` lies in `O(e)` iff both edges incident to `j` (namely `j-1` and `j`) are
negative; it lies in `I(e)` iff both are positive. Hence*

    |O(e)| = (k - l) + #{ j in T : w_{j-1} = w_j = - },   |I(e)| = (k - l) + #{ j : w_{j-1} = w_j = + }.

*If `w` is not constant the counts are `e_s - r_s`, where `e_s` is the number of edges of sign `s`
and `r_s` the number of maximal cyclic `s`-runs; if `w` is constantly `s` the count is `l`.*

*Proof.* Each `j` in `T` is an endpoint of exactly the two cycle edges `j-1` and `j`, so `j` is not
in `O(e)` iff some incident edge is positive iff not both incident edges are negative. For the second
sentence, a cyclic `s`-run of length `t` contributes its `t-1` internal vertices; a constant word is a
single cyclic run of length `l` all of whose labels have both incident edges `s`, so it contributes
`l`, not `l-1`. This is the only divergence between the cyclic and the linear convention, and it is
attained: the all-positive word is admissible, its `O(e)` being the outsider set, which is nonempty
whenever `k > l`. QED

**Corollary 1.2.** `|O(e)| >= k - l` and `|I(e)| >= k - l` for every `e` not in `B`.

**Theorem 1.3 (the binary sliver is a `k - l <= 2` phenomenon).**
*(i)* At `k = 6`, `l = 3`: `|O(e)| >= 3` and `|I(e)| >= 3` for every `e` not in `B`, under every
hypothesis on the palettes. The sliver is never 2-coloured.
*(ii)* At `k = 5`, `l = 3`: `min(|O(e)|,|I(e)|) = 2` for every `e` not in `B`, and the side attaining
2 is the side whose sign class covers all three cycle labels; its allowed set is the two outsiders.
So at `k = 5` the sliver is 2-coloured at every direction, with the *same* two labels at every
direction (possibly on the inner side for some directions and the outer side for others - which is
what Lemma 8.6 allows).
*(iii)* At `k = 6`: `l = 3` never; `l = 4` exactly at the two alternating words, which are constant
and nonempty on the open wedges where `e . v_0` and `e . v_1` have opposite signs (so on a set of
positive angular measure, whenever the arrangement admits it); `l = 5` for no sign word, because a
cyclic word has an even number of runs and `l = 5`, `m = 1` would need three; `l = 6` exactly for
`+++---` and its five rotations.

*Proof.* (i) and (ii) are Corollary 1.2 with `k - l = 3` resp. `2`, plus Lemma 1.1. For (ii) both
allowed sets contain the outsiders, and on the side whose sign class covers all of `T` the allowed set
*is* the outsider set; at `l = 3` one sign class always covers `T`, and the two-element set is
direction-independent. (iii) is the exhaustive computation of Section 6 (`work/verify.py`, blocks 2,
4, 5, 6): the counts of sign words giving two-element slivers on both sides are `0/8` (`l=3`),
`2/16` (`l=4`), `0/32` (`l=5`), `6/64` (`l=6`). For `l = 5`: both counts equal 1 forces
`e_+ - r_+ = e_- - r_- = 1`, hence `l - R = 2` where `R` is the total number of runs, so `R = 3`,
which is odd and impossible for a cyclic word. QED

**Corollary 1.4 (the length-4 case, `k = 6`).** *The balanced sign words at `l = 4` - those for
which neither sign class is a vertex cover, so that both allowed sets have size at least three - are
exactly `++--`, `-++-`, `+--+`, `--++`. Hence, if the interface rays satisfy `v_0 = v_2` (or
`v_1 = v_3`), for **every** `e` not in `B` at least one of `O(e)`, `I(e)` equals the outsider pair
`{4,5}`; the realisable words are then `++++`, `+-+-`, `-+-+`, `----`, with `O = I = {4,5}` for the
middle two.* (`work/transplant.py`, block A.) This is the exact sense in which `l = 4` at `k = 6`
imitates `l = 3` at `k = 5`.

---

## 2. Route B: singleton forcing cannot repair Theorem 0.2

Route B proposes to force `|P_x(e)| <= 2`, equivalently at a triangle interface `|A(e)| <= 1` for the
outsider part, and thereby to run the `k = 5` argument at `k = 6`.

**Theorem 2.1 (independence).** *Every quantity consumed by the interface-sliver argument is a
function of `(k, l, w(e), chi(G_terminal))` alone. In particular the sliver sizes `|O(e)|`, `|I(e)|`
of Lemma 1.1 contain no palette quantity: two colourings with the same interface data and different
palettes have identical slivers.*

*Proof.* `O(e)`, `I(e)` are defined from the cycle and the sign word alone, by deleting endpoints of
edges. The palette enters steps 3-5 only through (8.1) (non-emptiness of the two intersections),
(5.7) (disjointness at an `R`-step, giving the flip) and (5.2) (exclusion at a sum). None of the
three mentions the size of a palette. QED

**Corollary 2.2 (route B is insufficient).** *At `k = 6`, `l = 3` the conclusion `|A(e)| = 1`
supplied by route B leaves both slivers of size at least 3 (Theorem 1.3(i)), so step 3 stays
unavailable and the interface `l = 3` is not excluded by the class. Since Proposition 7.1 may return
`l = 3` at `k = 6`, route B does not decide `k = 6` by this route, whatever its constants.*

**What route B would repair, exactly.** Three loci of the printed argument are palette-cardinality
loci and are supplied by `|P| <= 2`:

* Section 6 triangle locus (Theorem 6.5): the paper's "a nonempty subset of the three triangle labels
  of size at most two lies in some triangle edge, which is forbidden by (6.2)" needs
  `|P cap outsiders| = 1`, i.e. `k - 3 = 2`.
* Section 8.2 five-cycle: the pigeonhole "the palette is a pair meeting both allowed sets" needs
  `|P| = 2`, i.e. `k - 3 = 2`. But at `k = 6` the single outsider lies in *both* allowed sets
  (Lemma 1.1 with `m = 1`), so `O cap I` is nonempty and the pigeonhole does not fire even then: the
  palette may be `{Z}`.
* Section 6 four-cycle locus: with `|P| <= 3` a palette avoiding the outsiders is a diagonal exactly
  as at `k = 5`, since every 3-subset of a 4-cycle contains an edge and is barred by (6.2).

Two loci are not palette-cardinality loci at all:

* Section 8.4/8.5 at `l = 3`: blocked by `k - l = 3`, independent of palettes.
* The terminal gadget: step 4's region carries `k - 2` labels, so step 5 needs a finite
  unit-distance graph with `chi >= k - 1`. At `k = 5` that is the Moser spindle (`chi = 4`,
  coordinates (8.5)); at `k = 6` it needs `chi >= 5`, an explicit finite 5-chromatic unit-distance
  graph - not exhibited in the paper, and its non-constructive existence (from W1 and
  de Bruijn-Erdos) is not a placement.

So the printed method's `k`-dependence is exhausted by five integers, all satisfied exactly at
`k = 5`:

| locus | exact condition | at `k = 5` | at `k = 6` |
|---|---|---|---|
| Section 6 non-degeneracy (some edge of `Gamma_x` exists) | `k - 3 >= 2` | yes | yes |
| Section 6 triangle locus binary | `k - 3 = 2` | yes | no |
| Section 8.2 five-cycle pair pigeonhole | `k - 3 = 2` and `O cap I` empty | yes | no |
| Section 8.4 binary sliver at `l = 3` | `k - l = 2` | yes | no |
| Section 8.5 terminal gadget | `chi(G) >= k - 1` | Moser spindle | needs `chi >= 5` |

**Corollary 2.3 (the `k = 4` calibration cannot exist; W2/D4).** *The sections 5-8 architecture has
no instance at `k = 4`: the cyclic-centre locus `L` of (6.4) is empty.*

*Proof.* At `k = 4` Proposition 5.6 (whose general-`k` proof is in K6-BARRIER Section 1) gives
`|P_x(e)| = k - 3 = 1` for a.e. `e`; write `P_x(e) = {p(e)}`. I claim `Gamma_x` has at most one edge.
Suppose `ij` and `kl` are two distinct edges of `Gamma_x`. By (6.2), `p(e)` is outside `{i,j}` and
outside `{k,l}` for a.e. `e`. If the two pairs are disjoint they cover all four labels, leaving no
possible `p`; if they share a label, say `j = k`, then `p(e)` is the fourth label `m` for a.e. `e`,
and (5.7) applied to the pair `e, Re` gives `{m} cap {m} = empty`, a contradiction. So `Gamma_x` has
at most one edge, contains no cycle, and `L = emptyset`: the compactly supported graph-valued map of
Section 7 has no unfilled disk, its cover obstruction produces no nontrivial loop, and Proposition
7.1 has no input. (Note that (6.2) alone does not give this: a singleton palette is compatible with a
*single* barred pair, which is why the two-edge case analysis is needed.) QED

So the requested calibration ("run the machinery at `k = 4` to derive `chi >= 5`") cannot exist: the
architecture is empty there, by its own definitions. This is a *negative* calibration and reproduces
nothing about `chi >= 5`. 
Non-degeneracy at `k >= 5` is the first `k`-dependence, and it
precedes the five loci above.

---

## 3. The L4 specification: what a replacement mechanism must have

Each item is falsifiable, and each names the printed step it replaces.

* **S1 (sliver, not palette).** The mechanism must produce, at the interface length Proposition 7.1
  actually returns, a colour set of size exactly 2 on a one-sided sliver, by a statement about the
  *essential supports* of the labels rather than about palettes. *Falsified by:* an interface with
  `|O(e)|, |I(e)| >= 3` on a positive-measure set - Theorem 1.3(i), `k = 6`, `l = 3`.
* **S2 (same pair on both slivers).** If the rigidity step exchanges through two slivers at angular
  distance `pi/3` (Lemma 8.6 does), the mechanism must prove that the two slivers carry the *same*
  two labels. At `k = 5` this is free (both are the outsider pair); at `k = 6` the only case in
  which it holds on a positive-measure set of directions is `l = 4` with paired rays (Lemma 4.0 and
  Corollary 1.4) - at `l = 6` the two-element slivers have *different* pairs (Remark 4.2), and at
  `l = 3`, `l = 5` two-element slivers do not exist on both sides at all. *Falsified by:* an
  interface with `|O| = |I| = 2` and `O` not equal to `I` on a positive-measure set - which
  `k = 6`, `l = 6`, `+++---` provides.
* **S3 (`k`-sensitivity).** The conclusion must depend on an integer that is not a palette bound.
  *Falsified by:* a conclusion derived from the data of Theorem 2.1 alone, whose only `k`-sensitive
  integers are `k - l` and `k - 1`, both already used by the printed argument.
* **S4 (terminal gadget).** The mechanism must exhibit a finite unit-distance graph with exact
  coordinates not colourable with the `k - 2` labels of step 4's region; at `k = 6`, that is
  `chi >= 5`. *Falsified by:* the absence of such a graph, or by a proof that every finite
  unit-distance graph of the required type is 4-colourable.
* **S5 (locality).** The `k`-dependence must be computable from `(k, l, w)` and the gadget alone, and
  in particular be invariant under replacing (5.12) by any other palette bound. *Falsified by:* a
  step whose validity changes when `|P|` changes at fixed `(k, l, w)`.
* **S6 (multiplicity three).** A mechanism replacing Lemma 7.5 rather than the palette step must
  handle multiplicity 3: W4 gives an explicit relatively open cover of `[-5,5]^2` of mesh 2 and
  multiplicity exactly 3. *Falsified by:* any replacement assuming multiplicity at most 2.

Route B satisfies S5 (it is palette-only) and fails S1 at `l = 3`, which is Corollary 2.2.

---

## 4. The example demanded by L4: a replacement that applies at `k = 6` where the method does not

Fix `k = 6` and an interface of length `l = 4` with cycle labels `T = {0,1,2,3}`, outsiders
`{4,5}`, and rays satisfying `v_0 = v_2` (or `v_1 = v_3`); then there are at most three projective
classes among the rays.

**Lemma 4.0 (the sliver at `l = 4`, `k = 6`).** *The balanced words - those for which neither sign
class is a vertex cover of the four-cycle - are exactly `++--`, `-++-`, `+--+`, `--++`, and each has
`w_0 != w_2`. Hence if `v_0 = v_2` no balanced word is realisable, and then for **every** direction
`e` not in `B` one of `O(e)`, `I(e)` equals the outsider pair `{4,5}`; the realisable words are
`++++` (with `O = {4,5}`), `+-+-`, `-+-+` (with `O = I = {4,5}`) and `----` (with `I = {4,5}`).*

*Proof.* A sign class fails to be a vertex cover of the 4-cycle exactly when it consists of two
non-adjacent edges, so the balanced words are the alternating-in-the-two-pairs words listed; each has
`w_0 != w_2`, so the constraint `v_0 = v_2` excludes all four and leaves the eight words of the form
`(s0,s1,s0,s1)`, of which only four have `s0 = s1`. The allowed sets are computed from Lemma 1.1
(`work/transplant.py`, block A). QED

**Theorem 4.1 (length-4 transfer at `k = 6`).** *Let a weak measurable 6-colouring be given and let
Proposition 7.1 return an interface of length `l = 4` with rays satisfying `v_0 = v_2`. Then:*

*(a) for every `e` not in `B`, `P_x(e) cap {4,5}` is nonempty (by (8.1) and Lemma 4.0) and, by (5.7)
at the pair `e, Re`, is a singleton; so `s(e) :=` the unique element of `P_x(e) cap {4,5}` is a
binary outsider state defined at every direction, with `s(Re) != s(e)`;*
*(b) Lemma 8.6 (local binary rigidity) transfers: at any `e_0` not in `B` the two slivers at `e_0` and
`Re_0` both carry the same two labels `{4,5}`, so the paper's four-unit-edge exchange argument - which
uses only that two labels are available and that the two strips approach radius one from some side,
those sides allowed to differ - gives `s` essentially constant near `e_0`;*
*(c) Lemma 8.7 (the essential boundary of `s` is exactly one six-position `R`-orbit, complementary
sectors of angle `pi/3` with alternating values `4`, `5`) transfers: its counting needs at most three
projective classes among the interface rays, and there are at most three;*
*(d) Lemma 8.8 (the polynomial region) transfers with `k - 2 = 4`: for `z` with `0 < |z|^2 < 4`
satisfying the strict inequality (8.4), the open set near `x + z` uses only the four cycle labels;*
*(e) the residual requirement is a finite unit-distance graph with exact coordinates, placed in that
region, that is not 4-colourable - i.e. of chromatic number at least 5.*

*Proof.* (a) Lemma 4.0 and (8.1) give non-emptiness at `e` and at `Re`; (5.7) gives
`P_x(e) cap P_x(Re) = empty`, so `{4,5}` cannot be contained in `P_x(e)`, and it is nonempty, so it is
a singleton, and the two singletons differ. (b) Lemma 8.6's proof is label-blind apart from the
two-label hypothesis: the implicit-function computation at `theta = pi/3` produces two nonparallel
unit directions from a point of the `e_0`-strip into the `Re_0`-strip, and the four-edge path is
alternating because only two labels occur. (c) The printed proof says two distinct boundary orbits
would require at least four projective classes among the interface rays; at `k = 5` there are three
rays, hence at most three, and here there are four rays but at most three classes. (d) The
computation of (8.4) is label-blind: it excludes the two sliver values `4` and `5` at the sum by
(5.2), leaving `k - 2 = 4` labels. (e) A proper 4-colouring of a region cannot contain a
non-4-colourable unit-distance graph. QED

**The hypothesis is not automatic.** With four distinct projective classes the balanced words
*are* realisable, on sets of directions of positive angular measure; with rays
`(1,0), (1,1), (0,1), (-1,2)` the word `++--` occurs at `e = (2,-1)` and `--++` at `e = (-40,1)`,
exactly (`work/transplant.py`, block B), where the allowed sets are `{3,4,5}`, `{1,4,5}` - no
two-element sliver on either side. So part (b) is a genuine hypothesis on the arrangement of the
interface rays, listed as such; and in that general-position case the printed method and the
replacement both fail at this length.

**Why this is the L4 example.** The replacement mechanism is the *binary-sliver selection rule*:
at an interface, read off the side whose allowed set is exactly two labels, and run the exchange
argument with the outsider pair. At `k = 6`, `l = 4` with `v_0 = v_2` it satisfies S1 and S2 and
carries the whole printed chain of Section 8.4-8.5 to the point where only a `chi >= 5` gadget is
missing. The printed method cannot do this: Section 8.3, its four-cycle argument, is a `k = 5`
argument that fixes one outsider `X`, splits on `X` in `P_x(e)` versus `X` not in `P_x(e)` (at
`k = 6` a palette may contain `Y` and not `X`, or neither), derives from the second case a cyclic run
of two positive and two negative signs, and then works with the three-state system `X, U, V` and the
pair bound `|P| = 2` (at `k = 6`, `|P| <= 3` and palettes avoiding both outsiders are diagonals but
palettes containing an outsider have four states). None of those objects exists at `k = 6`.

So the replacement satisfies, at `k = 6` and on an interface length the printed method does not
treat, a property that the printed method does not have (S1 and S2, items (a)-(d) of Theorem 4.1),
and its residual gap is exactly **S4**: an explicit finite unit-distance graph with `chi >= 5`. The
example is non-vacuous about its own limits: it does not exclude `l = 3` (Theorem 0.2), `l = 5`, or
`l = 6` at `k = 6`.

**Remark 4.2 (`l = 6` at `k = 6`).** On the same computation, the word `+++---` at `l = 6` gives
`O = {3,4}`, `I = {0,1}`, disjoint, both of size two, so (8.1) forces `|P_x(e)| >= 2` and confines
`P_x(e)` to `O union I union {2,5}`. So `l = 6` also carries two-element slivers on both sides, but
with *different* pairs, so S2 fails there: the mechanism of Theorem 4.1 does not reach it, and this
is the length for which the paper contains no argument at all.

## 5. What is *not* claimed

* No new bound on `chi(R^2)`; no 6-chromatic graph, no 6-colouring, no `chi >= 7`.
* Theorem 0.2 is a no-go for the class of Definition 0.1 at the interface length `l = 3`. By
  Theorem 4.1 the class is not vacuous at `k = 6`; it is vacuous *at `l = 3`* for every palette
  constant. Arguments that obtain colour information other than through a sliver are outside the
  class, which is why S1-S6 are stated rather than a slogan.
* Corollary 2.3 says the requested `k = 4` calibration cannot exist; it says nothing about other
  routes to `chi >= 5` and reproduces nothing about `chi >= 5` (L5, not claimed). Its proof uses
  (5.12) at `k = 4`, (6.2) and (5.7); it does **not** claim that a singleton palette contradicts
  (6.2) for every pair, which is false.
* Theorem 4.1 is *conditional* on the ray arrangement `v_0 = v_2` and on its item (e). Those are
  hypotheses, listed as such, not gaps: with four distinct projective classes the balanced words are
  realisable and the two-element sliver does not exist (Lemma 4.0 and block B of
  `work/transplant.py`), and Lemma 8.7's counting then fails as well.
* The sign words are those of a limiting interface; the passage from a.e. `e` to an angular arc is the
  paper's own (Lemma 8.1), used and not re-proved.
* W6 is corrected only in the direction that matters here: see Remark 5.1.

**Remark 5.1 (defect in the brief's W6 model).** W6 lists the outsider states at a `k = 6` triangle
interface as the six nonempty subsets of size at most 2 and asserts the transition `A -> A'` iff
`A cap A'` is empty. The *state count* is right, but the transition relation is a relaxation of the
true system: (8.1) does not say that `P_x(e)` meets the outsider set, it says that `P_x(e)` meets
`O(e)`, and by Lemma 1.1 at `k = 6`, `l = 3` the allowed sets have sizes 3 and 4, being the outsider
set on one side and containing cycle labels on the other. Moreover the pattern `(2,2,2,2,2,2)` of
outsider-part sizes is not realised by the relaxation either (Section 6, block 7), by the pigeonhole
`2 + 2 > 3`. W6 stands as a count of states, not as a description of the transition system.

---

## 6. Verification

Exact, integral, no floating point, no solver. From this directory:

    python3 work/verify.py                                        # Sections 1, 2, 5
    python3 work/verify.py | diff - work/verify_certificate.txt    # silent = reproduces the certificate
    python3 work/transplant.py                                     # Lemma 4.0 and Theorem 4.1(a), blocks A-C

| block | claim | output |
|---|---|---|
| 1 | Lemma 1.1 cardinality identities, all `(k,l,w)`, `3 <= k <= 11`, `3 <= l <= k`, plus the run formula `e_s - r_s` word by word | 8104 cases, 0 failures |
| 2 | Corollary 1.2 and Theorem 1.3 table | `k=6,l=3`: min 3, `0/8` words with both slivers 2; `k=5,l=3`: min 2 for all 8; `k=6,l=4`: `2/16`; `k=6,l=5`: `0/32`; `k=6,l=6`: `6/64` |
| 3 | every sign word at the `k=6,l=3` and `k=5,l=3` interfaces, with `O` and `I` printed | `min = 3` resp. `min = 2`, all eight words |
| 5 | `k=6,l=4`: the only two-element-on-both-sides words are the alternating ones | `O = I = {4,5}` for `+-+-` and `-+-+` |
| 6 | `k=6,l=6` count | 6 of 64, namely `+++---` and its rotations |
| 7 | the sections 5-6 constraint system at a `k=6` triangle interface: `1 <= |P_i| <= 3`, `P_i` meets the outsiders, `P_i cap P_{i+1}` empty on the six `R`-positions | 1 004 940 solutions, 18 outsider-size patterns; `(1,1,1,1,1,1)` realised, `(2,2,2,2,2,2)` not |
| 8 | the exchange gadget is a 2-label phenomenon: the 4-unit-edge path `P_5` | 2 proper 2-colourings, endpoints equal in both; 48 proper 3-colourings, 30 with distinct endpoints |

Block 7 certifies that route B's conclusion is consistent with but not derivable from the sections
5-6 constraints. Block 8 certifies that step 3's exchange gadget cannot be upgraded to three labels:
with three labels available the gadget forces nothing, so Theorem 1.3(i) is a real obstruction and
not a bookkeeping artefact. ``work/transplant.py` prints the four realisable words of the
`v_0 = v_2` interface with their allowed sets (block A), an exact rational general-position
arrangement in which a balanced word *is* realisable (block B, so the hypothesis of Theorem 4.1 is
not automatic), and the `chi >= k - 1` requirement at `k = 5, 6` (block C).
