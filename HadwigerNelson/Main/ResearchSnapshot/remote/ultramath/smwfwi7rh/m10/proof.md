# Where the `k = 6` palette frontier actually is

**Swarm `smwfwi7rh`, member `m10`, direction `d5`** (four-cycle binary outsider pair and the
minimal colouring-level condition that would force it).

**Summary.** The paper's machinery at `k = 6` is gated by the maximal palette field `P_x(e)`. This
note proves three things about that object, all of them one-line consequences of two facts the
paper already contains, and none of which is in the record of `sprint/k6/`:

* **(T1) The dual constraint.** For almost every `(y,e) in R^2 x S`,
  `c(y) in P_{y-e}(e)` **and** `c(y) notin P_y(e)`. The palette at the centre one unit away in
  direction `e` contains the *colour of `y`*; the palette at `y` itself does not.
* **(T2) No centre-independent palette field.** Hence no weak measurable colouring (any `k`) has a
  palette field that is independent of the centre, or constant on a ball of radius `> 1`, or
  invariant under translation by a vector of length `1/n`. This excludes, uniformly and with no
  computation, *every* palette-level countermodel in the record — Theorem C's four block fields,
  the singleton triangle model, and all free-label sector fields of `FREE-LABEL.md` — and it
  therefore answers the "six-cycle free-label" question at the level that matters: the whole
  sector ansatz of direction `d1` is not realizable by a colouring, whatever the search returns.
* **(T3) The frontier has no middle.** (endpoint trace) + (5.7) already forces the trace to be a
  proper colouring. So "add trace-consistency to the palette axioms" is not an intermediate
  axiomatisation: at `k = 6` it is *equivalent* to `chi(R^2) <= 6`. Combined with Theorem C
  (palette axioms alone: satisfiable for every cycle length) the `k = 6` palette programme has
  exactly two sides and nothing in between.

Plus, for the four-cycle: the palette-level answer to direction `d5` is **no** (an explicit
non-binary model satisfies every palette-side constraint of record including self-avoidance and
the unit-triangle bound), the models are removed by **(T1)**, which is *strictly weaker than
properness*, and **(T3)** shows that any trace-type hypothesis strong enough to remove them is
already strong enough to be a proper 6-colouring. So a future proof of binarity must use
properness of the colouring itself, not a weaker trace axiom. Also recorded:
one error in `sprint/k6/FREE-LABEL.md`'s six-cycle witness (a ternary palette, excluded by the
unit-triangle bound), and its exact repair to a pair-valued witness.

Everything decidable here is decided by two independent programs: `python3 verify.py` and
`python3 verify_indep.py` (both exit `0`; see §8).

---

## 0. Setting, and exactly what is taken from the paper

Labels `[k] = {1,...,k}`; `c : R^2 -> [k]` measurable with classes `A_i`, `a_i = 1_{A_i}`;
**weak measurable**: `int int a_i(x) a_i(x+u) dx dsigma(u) = 0` for every `i`. `S = S^1` with
normalised angular measure `sigma`; `kappa = pi/3`; `R` = rotation of `S` by `kappa`; directions
are unit vectors and their angles interchangeably. A point is **typical** if it is a density-one
point of its own colour class. `P_x(e)` is the maximal palette at centre `x` (Definition 5.1),
`W_x` the family of circle traces at `x`, and `D_{x,i} = {e : i in P_x(e)}`.

Quoted from `attachments/here-are-three-files-ni5n/paper.pdf` (page numbers of the printed
paper):

* **(C1)** Definition 5.1 and the two paragraphs after it (pp. 26–27): every `b in W_x` has
  `b >= 0` and `sum_i b_i = 1` almost everywhere, and — this is the sentence *"This proves that
  every individual trace has its positive coordinates in the palette almost everywhere"* — for
  each label `i`, `{e : b_i(e) > 0} <= D_{x,i}` up to an angular null set. Constant sequences are
  permitted in the defining limit. `W_x` is nonempty and compact.
* **(C2)** Lemma 4.3 (p. 25): typical points are conull; no unit pair of typical points shares a
  colour.
* **(C3)** Lemma 5.2(2) (p. 27): if `e` is an angular density-one point of `D_{x,i}` then for
  every `v` nonparallel to `e` the spatial density of `A_i` at `x+e+v` is zero.
* **(C4)** (5.2) (p. 27), (5.3) (Lemma 5.2(3), p. 27), (5.7) (Corollary 5.4, p. 29).
* **(C5)** Definition 6.1 and Lemma 6.2/(6.2) (pp. 34–35).
* **(C6)** Lemma 6.3 (p. 36), Lemma 6.4 (p. 37).

Taken from the previous swarm's record (not re-derived): `m2`'s unit-triangle palette bound
(`sprint/k6/REPORT.md` §5b), `m11`'s `sigma{T <= P_x} <= 1/2` and the ternary half-circle bound
(same report), `m1`'s single-centre classification, Theorem C and `FREE-LABEL.md`'s models, `m16`'s
Theorem A. The two facts I prove below — Lemma 1 and Lemma 2 — are *restatements* of statements
already used or proved in the record ((C1) used in Proposition 5.6's proof; Lemma 2 is Lemma D of
`sprint/k6/REPORT.md` §5, reproduced for self-containedness). What is new is T1–T3 and their
consequences.

---

## 1. Two lemmas

> **Lemma 1 (endpoint trace).** For **every** centre `x in R^2` and almost every `e in S`,
> `c(x+e) in P_x(e)`.

*Proof.* Put `b_i(e) := a_i(x+e)`, so `b` is the vector of colour indicators sampled on the unit
circle around `x`. I claim `b in W_x`. By Definition 5.1 it suffices that `(y_n,r_n) = (x,1)` is a
typical circle sampling, i.e. that `x+e` is typical for almost every `e`. Let `N` be the set of
non-typical points; by (C2), `N` is plane-null, and `e |-> x+e` is an isometry of `S` onto the
circle `x+S`, a `C^1` curve, so `{e : x+e in N}` is angular-null. Constant sequences are
permitted, so `b in W_x`. Now fix a label `i`. By (C1), `{e : b_i(e) > 0} <= D_{x,i}` up to null.
If `c(x+e) = i` then `b_i(e) = 1 > 0`, hence `i in P_x(e)`. Taking the union over the finitely
many `i` gives the claim. `square`

> **Lemma 2 (self-avoidance; = Lemma D of the report).** For almost every `x in R^2` and almost
> every `e in S`, `c(x) notin P_x(e)`.

*Proof.* Let `x` be typical with `c(x) = i`, and put `D = D_{x,i}`. Suppose `sigma(D) > 0`. Then
`D` has an angular density-one point `e_0`. By (C3), for every `v` nonparallel to `e_0` the
spatial density of `A_i` at `x+e_0+v` is zero. Let `C = {delta in S : |delta - e_0| = 1}`; for
`delta in C` the vector `v(delta) = delta - e_0` is unit and equals `e_0` only at `delta = 2e_0`
and `-e_0` only at `delta = 0`, so it is nonparallel to `e_0` off two points. Hence the density of
`A_i` at `x + e_0 + v(delta) = x + delta` is zero for every `delta in C` off two points. On the
other hand the set of non-density-one points of `A_i` is plane-null, so its intersection with the
circle `C` is angular-null and, for some such `delta`, `x+delta` is a density-one point of `A_i`,
a contradiction. Hence `sigma(D) = 0`. Varying `i` over the finitely many labels and `x` over the
conull typical set gives the claim. `square`

## 2. T1: the dual constraint

> **Theorem 1.** Assume in addition that `(x,e) |-> P_x(e)` is (Borel) measurable. Then for almost
> every `(y,e) in R^2 x S`,
>
>     c(y) in P_{y-e}(e)      and      c(y) notin P_y(e);
>
> in particular `P_{y-e}(e) \ P_y(e) != empty`. Equivalently, for almost every unit pair
> `(y,z)` and the direction `e = z - y`: `c(y) in P_z(e)` and `c(y) notin P_y(e)`.

*Proof.* By Lemma 1 at the centre `x = y-e`: for a.e. `(y,e)`, `c(y) in P_{y-e}(e)`. By Lemma 2
at the centre `y`: for a.e. `(y,e)`, `c(y) notin P_y(e)`. Joint measurability is what is needed to
put the two almost-everywhere statements on the same null set (both are measurable sets in
`R^2 x S`, and each has all its sections null on a conull set of centres, so each is null by
Fubini). `square`

**Remark 1 (the paper's own convention).** The paper explicitly does not assume joint
measurability of `P_x` in `x` ("No joint measurability of `P_x` in its center is assumed"), and
every statement in it is about finitely many fixed centres with null sets depending on them. The
two *per-centre* halves of Theorem 1 are exactly of that kind and need nothing more:

  for every centre `x` and a.e. `e`: `c(x+e) in P_x(e)`;   for every typical `x` and a.e. `e`:
  `c(x) notin P_x(e)`.

Theorem 2 below needs only the case in which the field is independent of the centre, where joint
measurability is automatic (the field is a measurable function of `e` alone). So nothing in the
main applications rests on the extra hypothesis.

**Remark 2 (it is not the same as (5.7)).** (5.7) is `P_x(e) cap P_x(Re) = empty` at *one*
centre and two directions; Theorem 1 relates *two* centres at unit distance and one direction, and
it identifies a specific label: the colour of the other endpoint. Both are consequences of (C1)
plus properness; neither implies the other.

## 3. T2: no centre-independent palette field

> **Theorem 2.** Let `c` be a weak measurable `k`-colouring and suppose there is a measurable
> `P : S -> 2^[k]` with `P_x(e) = P(e)` for almost every `e in S`, for **every** centre `x`.
> Then contradiction. In particular no weak measurable colouring of any `k` has a palette field
> that is independent of the centre.

*Proof.* Write `V = {A <= [k] : sigma{e : P(e) = A} > 0}`, a finite nonempty family, and
`A_* = intersection V`.

*Step 1: `c(y) in A_*` for a.e. `y`.* By Lemma 1 at each centre `x`, `c(x+e) in P_x(e) = P(e)` for
a.e. `e`. The set `W = {(x,e) : c(x+e) notin P(e)}` is measurable (`c` Borel, `P` measurable in
`e` alone) and each of its `x`-sections is null, so `W` is null by Fubini. The shear
`(x,e) |-> (x+e, e)` is a measure-preserving diffeomorphism of `R^2 x S`, so
`W' = {(y,e) : c(y) notin P(e)}` is null as well. Hence for a.e. `y`, `c(y) in P(e)` for a.e.
`e`; and since `{P = A}` has positive measure for each `A in V`, `c(y) in A` for every `A in V`,
i.e. `c(y) in A_*`.

*Step 2: `c(y) notin A_*` for a.e. `y`.* By Lemma 2 at each typical centre `y`,
`c(y) notin P_y(e) = P(e)` for a.e. `e`; as `A_*` is the intersection of the values taken on
positive-measure sets, `c(y) notin A_*`. (Measurability of the set
`{(y,e) : c(y) in P(e)}` is the same as in Step 1, so Fubini applies.)

The two conull sets of `y` meet; at a common point both `c(y) in A_*` and `c(y) notin A_*` hold.
`square`

### 3.1 What Theorem 2 excludes (this is the whole palette-countermodel programme)

Each model below is centre-independent and therefore, by Theorem 2, is not the maximal palette
field of any weak measurable colouring — *regardless* of which palette axioms it satisfies, of
whether it carries a free label, and of whether a search satisfies the exact transport shifts.

| model | source | free label for non-proper self-avoidance | excluded by |
|---|---|---|---|
| `{0,3},{1,4},{2,5}` (all `ell`) | Theorem C | none | Theorem 2 |
| `{0,2},{1,4},{3,5}` (`ell=4`) | Theorem C | none | Theorem 2 |
| `{0,2},{1,3},{4,5}` (`ell=5`) | Theorem C | none | Theorem 2 |
| `{3},{4},{5}` (`ell=3`) | `FREE-LABEL.md` | `0,1,2` | Theorem 2 |
| `{0,2},{1,3},{4}` (`ell=4`) | `FREE-LABEL.md` | `5` | Theorem 2 |
| `{0,2},{1,3},{5}` (`ell=5`) | `FREE-LABEL.md` | `4` | Theorem 2 |
| 36-sector six-cycle word | `FREE-LABEL.md` | `0` | Theorem 2 (and §5) |

`verify.py` §A re-checks, exactly: admissibility of every value for the cycle, pairwise
disjointness of the blocks, the free label, and — the point of Theorem 2 — that **the intersection
of all palette values of each field is empty**. That intersection is `A_*`, and the property
"`c(y) in P(e)` for a.e. `e`" forces `c(y) in A_*`; so for these fields there is no label function
`c` and no point `y` at which the endpoint trace of Lemma 1 can hold even in the weaker
"for a.e. `e`" sense. (Theorem 2 itself only needs that failure on a set of `y` of full measure.)

**Consequence for direction `d1` (the six-cycle free-label decision).** The question "can a
translation-invariant sector field with a free label satisfy (5.7) and the exact shifts" has a
decided answer at the palette level — `FREE-LABEL.md` exhibits such a field, and §5 below repairs
its one defect — but **no answer of that question can bear on the six-colour problem**: whatever
the search returns, the field is centre-independent, hence by Theorem 2 it is not a colouring's
palette, and the self-avoidance it realises is not the self-avoidance of a colouring at its
typical points. The same verdict applies to any *piecewise*-constant-in-the-centre variant: §3.2.

### 3.2 Spatial constancy: what exactly is excluded, and sharpness

> **Corollary 3 (no ball of radius `> 1`, in the jointly measurable class).** Let `Z <= R^2` be a
> measurable set of centres and `Q : S -> 2^[k]` measurable, with `P_x(e) = Q(e)` for a.e.
> `(x,e) in Z x S`, and suppose the field `(x,e) |-> P_x(e)` is jointly measurable. If
> `{y : y + S <= Z}` has positive measure then contradiction. In particular `Z` contains no
> closed ball of radius `> 1`.

*Proof.* Same Fubini argument as Theorem 2 with `R^2` replaced by `Z`: the set
`{(x,e) : x in Z, c(x+e) notin Q(e)}` is null, its image under the shear is null, so for a.e.
`(y,e)` with `y-e in Z` we have `c(y) in Q(e)`. Choose `y` in `{y : y+S <= Z}` which is typical
*and* outside the null set `{y : (y,e) in W' for a positive-measure set of e}` (that set is null by
Fubini applied to `W'`), and take `y-e in Z`, valid for every `e`. Then `c(y) in Q(e)` for a.e.
`e`, while Lemma 2 gives `c(y) notin Q(e)` for a.e. `e`. `square`

**Sharpness of the statements.**

1. *Centre-dependence is genuinely needed, and is compatible with everything else.* Let `c` be
   any proper `k`-colouring with cell size bounded below, e.g. the paper's hexagonal 7-colouring at
   `k = 7` (so that Lemma 1 and Lemma 2, being theorems about every weak measurable colouring,
   apply to it). Its palette field is `P_x(e) = {c(x+e)}` a.e. — a singleton field, which
   satisfies Lemma 1 and Lemma 2 and is *not* centre-independent. So the class of palette fields
   of colourings is nonempty and Theorem 2 separates two nonempty classes.
2. *The length `1` is exactly what the proof uses.* The proof only needs the identification
   `P_{y-e}(e) = P_y(e)`, i.e. that `-e` is a period. Hence the same argument also excludes a
   period of length `1/n` for any `n >= 1` (a period `h` with `|h| = 1/n` is also a period
   `nh` of length `1`), and excludes nothing about periods of other lengths. Periods of other
   lengths are not claimed.
3. *The "stationary" ansatz `P_x(e) = Q(x+e)` is not excluded*, and must not be: a proper
   colouring with singleton palettes has exactly that form. So Theorem 2 is not a blanket
   impossibility for palette fields; it locates the obstruction precisely at spatial constancy.
   Note that this does **not** touch `d3`'s class of fields that are constant on each cell of a
   lattice but vary between cells: those are not centre-independent, and Theorem 2 says nothing
   about them.

## 4. T3: the frontier has no middle

> **Theorem 4.** Let `P : R^2 x S -> 2^[k]` be any palette field (jointly measurable) and
> `c : R^2 -> [k]` measurable with
>
>   (i) **endpoint trace** `c(x+e) in P_x(e)` for a.e. `(x,e)`;
>   (ii) **(5.7)** `P_x(e) cap P_x(Re) = empty` for a.e. `(x,e)`.
>
> Then `c(y) != c(y')` for almost every pair `(y,y')` of unit distance: `c` is a proper
> `k`-colouring of the plane's unit-distance graph. Conversely, if `c` is a proper `k`-colouring
> then `P_x(e) := {c(x+e)}` satisfies (i) and (ii).

*Proof.* Let `(y,y')` be a unit pair and put `d = y' - Ry`. Since `I - R` is invertible (its
determinant is `1`, `verify.py` §D), `z := (I-R)^{-1} d` is the unique point with `z + Ry = y'`.
Put `e := y - z`, a unit vector. Then `z + e = y` and `z + Re = z + R(y-z) = z + Ry - Rz = y'`, and
`|e - Re| = |e|` identically, so both `e` and `Re` are unit directions. Applying (ii) at the
centre `z`: `P_z(e) cap P_z(Re) = empty`; applying (i) at the centre `z` in the two directions:
`c(y) = c(z+e) in P_z(e)` and `c(y') = c(z+Re) in P_z(Re)`. Hence `c(y) != c(y')`. The exact
algebra (`z+e = y`, `z+Re = y'`, `|e-Re|^2 = |e|^2`, `det(I-R) = 1`) is verified symbolically in
`verify.py` §D. The converse is immediate from properness, since `|e - Re| = 1`. `square`

**Consequences.**

1. *Every unit pair is an `R`-pair.* That is the content of the algebra in Theorem 4: the map
   `(z,e) |-> (z+e, z+Re)` is a bijection onto the set of ordered unit pairs
   `(y,y')`, with inverse `y' - Ry = (I-R)z`, `e = y - z`. So (5.7) is not a partial properness
   condition: applied at a variable centre it is properness.
2. *Trace-consistency is not an intermediate axiomatisation.* Let `S` be any set of axioms for a
   palette field that contains (i) and (ii), and let `Sat_6(S)` be its satisfiability at `k = 6`.
   Then `Sat_6(S)` implies `chi(R^2) <= 6`. Since `chi(R^2) <= 6` is open, `Sat_6(S)` cannot be
   established without settling `chi(R^2) = 6`; and by the converse, `Sat` holds at `k` whenever a
   proper `k`-colouring exists. At `k = 6`, therefore,

     `{palette axioms}`                    : satisfiable, accumulating, every cycle length (Theorem C)
     `{palette axioms + a trace function}` : satisfiable  <=>  `chi(R^2) <= 6`.

   There is no axiomatisation strictly in between: adding *any* trace function, proper or not,
   already collapses to the original problem.
3. *Relation to the record's "chromatic wall" (direction `d12`).* The colouring-level version of
   this collapse is the observation of `d12`: exhibiting a genuine `k = 6` countermodel (an actual
   colouring with non-locally-finite `L`) would give `chi(R^2) <= 6`. Theorem 4 is the
   *palette-level* form of the same wall and is strictly stronger as a barrier: the object that
   collapses to `chi(R^2) <= 6` need not be a colouring at all, nor even a proper one — a palette
   field plus *any* measurable label function satisfying (i) suffices, because (ii) then makes that
   label function proper on every unit pair.
4. *A correction to the record's frontier sentence.* `sprint/k6/REPORT.md` §5 says that "the only
   constraint [the countermodels] fail is trace-consistency with a **proper** 6-colouring".
   Theorem 2 shows that a strictly weaker condition already removes all of them: the endpoint
   trace of Lemma 1 alone, together with self-avoidance (Lemma 2), which every colouring
   satisfies. The countermodels therefore fail a condition *weaker* than properness, and the
   correct statement of the frontier is: *the countermodels are removed by Lemma 1, and Lemma 1 +
   (5.7) is already properness.*

## 5. The unit-triangle bound, and the six-cycle free-label witness

> **Proposition 5 (unit-triangle bound; `m2`'s bound, in the form used here).** At `k = 6`, for
> every centre `x`, every `a in S` and almost every `e in S` that is not parallel to `a`, `Ra` or
> `Ra - a`: the three palettes `P_x(e)`, `P_{x+a}(e)`, `P_{x+Ra}(e)` are pairwise disjoint.

*Proof.* The three points `x`, `x+a`, `x+Ra` are pairwise at unit distance
(`|a| = 1`, `|Ra| = 1`, `|Ra - a| = 2 sin(pi/6) = 1`). For each of the three pairs `(z,z')`, put
`w = z' - z` (so `|w| = 1`) and apply (5.3) with `f = e`, `s(f) = e`, `t(f) = w`; read as the
smooth local branch of the two exact unit decompositions of `f + w` near `f = e`, this satisfies
the hypotheses of (5.3) (nonparallel unit endpoints, `s` a local diffeomorphism with `s(e) = e`),
and `e` is outside the exceptional null set because we excluded the three directions parallel to
`a`, `Ra` and `Ra - a`. The conclusion is `P_{z'}(e) cap P_z(e) = empty` for each of the three
pairs, which is the claim. `square` (The same computation underlies `m2`'s
`|P_x(e)| + |P_{x+e}(e)| <= 5`; the three-way form is what Corollary 6 needs.)

> **Corollary 6.** In a centre-independent field at `k = 6`, `3|P(e)| <= 6`, so `|P(e)| <= 2`
> for almost every `e`.

*Consequence 1 (a defect in `FREE-LABEL.md`).* The 36-sector six-cycle free-label word of
`sprint/k6/FREE-LABEL.md` contains the ternary value `{2,4,5}` (sector 16). At that sector
`3|P| = 9 > 6`, so the word violates the unit-triangle bound and is not a palette field of the
class it is offered for. (It satisfies the palette axioms, (5.7) and all six transport offsets;
the defect is only the palette size.) `verify.py` §B reports it.

*Consequence 2 (repair: the pair-valued system is satisfiable).* Restricting to pairs — which is
forced in this class by Corollary 6 — the six-cycle free-label system over `Z/n` sectors with
palettes admissible for `C_6` (there are exactly `9` such pairs, `6` of them avoiding a fixed free
label) and disjointness at the transport offsets `{+-(m-1), +-m, +-(m+1)}`, `m = n/6`, is
**satisfiable for `n = 36`** with the period-12 word (free label `0`)

```
[1,3] [1,3] [1,3] [1,4] [1,4] [2,4] [2,4] [2,4] [2,5] [2,5] [3,5] [3,5]   (repeated 3x)
```

and also for `n = 30, 42, 48, 60, 72` (periods `n/3`), while it is **unsatisfiable for
`n = 12, 18, 24`** — the coarsest three resolutions, where the transport offsets `{+-1,+-2,+-3}`,
`{+-2,+-3,+-4}`, `{+-3,+-4,+-5}` are too dense for the disjointness graph of the six admissible
pairs. Both verdicts are produced by two independent complete searches (`verify.py` §C: positional
DFS with forward checking; `verify_indep.py`: dynamic min-domain DFS over integer bitmasks, no
forward checking) which agree on every `n` and on all six choices of free label, and every SAT
witness is re-verified by a third code path. So `m13`'s six-cycle free-label conclusion survives
in the stronger pair-valued form — and Theorem 2 nevertheless removes the whole family.

## 6. The four-cycle at `k = 6` (direction `d5`)

The question. Let `x` be a typical four-cycle centre with cycle labels `0,1,2,3` in cyclic order
and outsiders `4,5`. Is `P_x(e) cap {4,5} != empty` for almost every `e` — i.e. is `x` **binary**
for the outsider pair? If yes at every four-cycle centre, (5.7) makes the intersection a singleton
a.e. and Lemma 5.5 gives local finiteness of the four-cycle locus at `k = 6`. This is exactly
`m16`'s Corollary 3.1, whose printed proof has the known gap (it assumes
`P_x(e) <= {0,1,2,3}` a.e.).

**Answer at the palette level: no.** `FREE-LABEL.md`'s `ell = 4` model — values `{0,2}`, `{1,3}`,
`{4}` on three blocks of angular length `2pi/3`, independent of the centre — satisfies

* `1 <= |P| <= 3` and `P` is not contained in any edge of `C_4` (Lemma 6.2);
* `P(e) cap P(Re) = empty` (5.7), and the exact two-centre transport (5.3) for all pairs of
  centres at distance `<= d_0` (three code paths, `sprint/k6/uniform_nogo.py` and `m15`);
* non-proper self-avoidance with free label `5`, and `m11`'s bounds
  (`sigma{|P|=3} = 0`, `sigma{T <= P} <= 2pi/3 <= pi`);
* the unit-triangle bound: `2 + 2 + 2 = 6` (Corollary 6 is sharp on this model);
* the two-centre bound `|P_x(e)| + |P_{x+e}(e)| = 4 <= 5` (`m2`);

and it is **not** binary: `P cap {4,5} = empty` on the two pair-valued blocks, i.e. on `4pi/3` of
the direction circle. So no argument from the palette axioms, however many cross-centre palette
constraints are added, can prove binarity at `k = 6`.

**What removes it: T1, not properness.** The model is centre-independent, so Theorem 2 excludes
it. And this is *not* a restatement of "it fails properness": the condition it fails (Lemma 1
together with Lemma 2) is strictly weaker than properness as a condition on a pair `(P,c)` — for
instance `c ≡ 1`, `P_x(e) = {{1,2}}` satisfies Lemma 1 and fails properness — while Theorem 4
shows that Lemma 1 + (5.7) already forces properness.

The precise conclusion for direction `d5` is therefore this.

* Binarity cannot follow from the palette axioms together with any condition that the record's
  block models satisfy: they satisfy every palette axiom recorded so far, including self-avoidance
  and the unit-triangle bound, and they fail binarity (`verify.py` §A, §B).
* The smallest colouring-level condition they *do* fail is the endpoint trace (Lemma 1); and by
  Theorem 4, the endpoint trace together with (5.7) already yields a proper 6-colouring.
* Hence any hypothesis strong enough to remove the block models is strong enough to contain a
  proper 6-colouring, and a proof of binarity from such a hypothesis is a proof about a
  `k = 6` colouring — the original setting. There is no intermediate hypothesis on which to build
  the four-cycle case.

**What survives of the record, and what is open.**

* The correct statement proved by `m16`'s Corollary 3.1 argument is the weaker one:
  `{e : P_x(e) <= {0,1,2,3}}` is **not conull** (the proof assumes conullity and derives the
  Theorem A contradiction). The step "an outsider appears a.e." is not established, and by the
  model above it cannot follow from palette hypotheses.
* Local finiteness of the four-cycle locus at `k = 6` is **open**, as is `(W)`.
* The search space for a countermodel is now constrained in a way it was not before: by Theorem 2
  and Corollary 3, the palette field of any `k = 6` colouring is **not** constant on any ball of
  radius `> 1`, in particular is neither a sector field nor periodic with period `1/n`. Every
  palette-level countermodel in the record has one of those two forms. A countermodel therefore
  has to be "position-dependent at scale `1`", like `m3`'s `k >= 7` construction (whose cyclic
  centres accumulate at `p_0` through disks of diameter `~ 10^{-n}`) — and `m3`'s construction needs
  `k - 3 = 4` outsider labels, which is exactly the label count that does not exist at `k = 6`.

## 7. Ledger

| statement | status | where |
|---|---|---|
| endpoint trace `c(x+e) in P_x(e)` a.e., every centre | proved (from Definition 5.1) | Lemma 1 |
| self-avoidance `c(x) notin P_x(e)` a.e. | proved (paper's Lemma 5.2(2)) | Lemma 2 |
| dual constraint `P_{y-e}(e) \\ P_y(e)` nonempty | proved, jointly measurable class | Theorem 1 |
| no centre-independent palette field (any `k`) | **proved, unconditional** | Theorem 2 |
| no palette field constant on a ball of radius `> 1` | proved (jointly measurable class) | Corollary 3 |
| no palette field with a period of length `1/n` | proved (jointly measurable class) | Remark, §3.2 |
| endpoint trace + (5.7) `=>` proper trace | **proved** | Theorem 4 |
| palette axioms at `k = 6` | satisfiable, every `ell`, accumulating | Theorem C (record) |
| palette axioms + trace function at `k = 6` | satisfiable `<=>` `chi(R^2) <= 6` | Theorem 4 |
| every palette-level countermodel in the record | **excluded** | Theorem 2 |
| `ell = 6` free-label field at `k = 6`, pair-valued | satisfiable for `n = 30,36,42,...`, unsat for `n = 12,18,24` | §5 |
| `FREE-LABEL.md`'s `ell = 6` witness | **defective** (ternary palette violates the unit-triangle bound) | §5 |
| four-cycle binary for the outsider pair at `k = 6` | **open**; false at the palette level | §6 |
| `m16` Corollary 3.1 as printed | not established; correct version: the set is not conull | §6 |
| `(W)`: `L cap B(y,R)` finite for some `R > 1` | **open** | — |

## 8. Reproduction

```
cd .ultramath/smwfwi7rh/m10
python3 verify.py          # exact; exits 0; all checks pass
python3 verify_indep.py    # independent second decider; exits 0; "agrees"
```

`verify.py` sections: `[A]` the models of record (admissibility, free label, empty intersection of
all values); `[B]` the unit-triangle bound on each model (and its violation by the `ell = 6`
witness); `[C]` the six-cycle free-label pair system, decided for `n = 12`–`72` by a complete DFS
with forward checking; `[D]` the exact symbolic algebra of Theorem 4 (`sympy`, rational `cos`/`sin`
of `pi/3`). `verify_indep.py` re-decides `[C]` with a different data representation (integer
bitmasks instead of `frozenset`s), a different search order (dynamic min-domain instead of
positional), no forward checking, and all six choices of the free label; it re-verifies the
witnesses through a third code path.

Third-party certificates used and not re-derived here: `sprint/k6/uniform_nogo.py` and
`m15`'s `verify.py` for the exact (5.3) transport of the block models; `m3`'s `verify.py` for the
`k >= 7` construction; `m2`'s and `m11`'s notes for the palette bounds of §5 and §6.
