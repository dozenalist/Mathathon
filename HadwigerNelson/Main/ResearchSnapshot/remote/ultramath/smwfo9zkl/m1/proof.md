# What the palette system knows at one centre at k = 6: exactly one bit

**Member m1, direction d12.** A theorem with a complete proof, a decided finite computation
with two independent decision procedures, an end-to-end object-level verification, and a
precisely delimited class. It is **not** a proof of `chi(R^2) >= 7` and does not claim one.

---

## 0. Result in one line

Let `x` be a centre of a weak measurable `k`-colouring (paper, Definition 1.2) and `Gamma_x`
its transition graph (paper, Definition 6.1). Consider the **single-centre palette system** at
`x`, i.e. the constraints on the pair `(P_x, Gamma_x)` that the paper's own inputs impose
*without using a second centre*:

* **(P)** `1 <= |P_x(e)| <= k-3` for a.e. `e` (palette bound, general `k`);
* **(57)** `P_x(e) cap P_x(R e) = empty` for a.e. `e`, `R` = rotation by `pi/3` (paper (5.7));
* **(T1)** no two palette *values* `A, B` with `A cup B = I` both occupy positive angular measure;
* **(62)** `ij in Gamma_x  =>  P_x(e)` is not a subset of `{i,j}` for a.e. `e` (paper Lemma 6.2).

**Theorem (classification).** For `k >= 6`, `(P),(57),(T1),(62)` are simultaneously satisfiable
for a graph `G` on `k` labels **if and only if** `G != K_k`. Equivalently:

> at `k = 6` exactly **one** of the `2^15 = 32768` graphs on the six labels is excluded by the
> single-centre palette system, namely the complete graph `K_6`; at every `k >= 7` **no** graph
> is excluded; at `k = 5` exactly 76 of the 1024 graphs are excluded and the condition is an
> Erdős–Ko–Rado condition on the non-edges.

Two consequences that bear directly on the sprint:

1. **No single-centre argument can prove local finiteness of the cyclic locus at `k = 6`.**
   All six cycle lengths `3,4,5,6` — in particular the six-cycle `C_6` that has no `k = 5`
   analogue — are compatible with the entire single-centre system. Any proof of local
   finiteness, or any exclusion of the six-cycle stratum, **must use at least two centres.**
2. **The `k = 6` palette inequalities of the barrier analysis are sharp and cannot be
   improved at one centre.** The orbit bound `sigma(E_x) <= pi` and the mean bound
   `(1/2pi) int |P_x| dsigma <= 5/2` are *both attained simultaneously*, by an explicit
   palette system on which, moreover, `C_6` survives. So the palette bound `|P_x(e)| <= 2`
   (K6-BARRIER, item 1 of its "what a six-colour proof needs") is unreachable by
   single-centre means, and no strengthening of the palette inequalities can exclude `C_6`.

The "exactly one bit" of the title is the sharp form: the only `k`-sensitive single-centre
information at `k = 6` is the statement `Gamma_x != K_6`.

---

## 1. Cited inputs (not re-derived)

Throughout `I = {1,...,k}`, `S` is the unit circle of directions with normalised angular
measure `sigma`, `R` is rotation of directions by `kappa = pi/3`, and `P_x(e)` is the maximal
palette of Definition 5.1 at the centre `x`.

* **(P)**, `3 <= k`, every centre: `1 <= |P_x(e)| <= k-3` a.e. This is Proposition 5.6 at
  `k = 5` (`EuclideanFiveColor.palette_cardinality`,
  `lean/OAI/Geometry/PlaneColoring/BinaryPalettes.lean`) and `results/K6-BARRIER.md` §1 in
  general.
* **(57)**, every `k`, every `x`: `Disjoint (P_x f) (P_x (f + sixty))` a.e. Machine-checked as
  `EuclideanFiveColor.palette_sixty_disjoint`,
  `lean/OAI/Geometry/PlaneColoring/PaletteTransport.lean`. Paper: Corollary 5.4, (5.7).
* **(52)**, every `k`, every `x`: `c (angularSum x 1 p) ∉ P_x p.1 ∪ P_x p.2` for a.e. pair `p`.
  Machine-checked as `EuclideanFiveColor.palette_transfer_pair`,
  `lean/OAI/Geometry/PlaneColoring/PaletteDensity.lean`. Paper: Lemma 5.2(1), display (5.2),
  verified against two further extractions of the rendered page.
* **(T1)**: [prior swarm `smwfhd5sl/m6`, Theorem 1] for `k >= 2`, `x`, and `A, B` with
  `A cup B = I`, not both `{e : P_x(e) = A}` and `{e : P_x(e) = B}` have positive `sigma`-measure.
  Immediate from (52) (see §2 below) plus measurability of `{e : P_x(e) = A}`
  (`paletteSet_measurable`, `lean/OAI/Geometry/PlaneColoring/Palettes.lean`).
* **(62)**, every `k`: if `ij in Gamma_x` then `P_x(e)` is not a subset of `{i,j}` for a.e. `e`.
  Paper Lemma 6.2 and display (6.2). Its proof uses (6.1), (6.3) and the trace construction;
  **it does not use the palette bound**, so it is valid at every `k`.
* **Orbit bound and mean bound** `[smwfhd5sl/m6, Theorem 2]`, `k = 6`: at most three of the six
  palettes of an `R`-orbit are ternary; hence `sigma(E_x) <= pi` and mean `<= 5/2`. Both are
  *consequences* of (P), (57), (T1), so they add nothing to the system in §0, but they are the
  quantities item 2 above shows to be sharp.

I checked the extraction of (5.2) and (5.7) against three independent extractions of the PDF
(`pdftotext -layout`, `mutool draw -F txt`, and the repo's LaTeX transcription
`results/COMPRESSED-PROOF.md`); all three agree, so no extraction artifact is involved.

---

## 2. Lemma (T1) is the complete single-centre content of (5.2)

**Lemma 2.1.** *Fix `x` and let `P : S -> 2^I \ {empty}` be any measurable palette function
(allowing all `k` values). Then (5.2), read as a constraint on `c` at the points `x + e + v`,
is satisfiable for some `c : R^2 -> I` if and only if (T1) holds for `P`.*

*Proof.* (=>) is (T1) as in the citation: if `A, B` with `A cup B = I` both have positive
measure, the product has positive measure, so some `(e,v)` with `P(e) = A`, `P(v) = B` is
outside the null set of (5.2), giving `c(x+e+v) ∉ A cup B = I`, impossible.
(<=) Suppose (T1). For a.e. pair `(e,v)` the set `I \ (P(e) cup P(v))` is nonempty; choose
`c(x+e+v)` from it. This is well defined: the map `Phi(e,v) = e+v` from `S x S` to the closed
disc of radius `2` has fibres of size exactly `2`, the swap `(e,v) |-> (v,e)`, for
`0 < |e+v| < 2`, and size `1` for `|e+v| = 2`; the pairs with `e = ±v` (where `Phi` is
singular, and which are not independent-angle pairs) form a `sigma`-null set. Since
`P(e) cup P(v)` is symmetric, the two members of a fibre prescribe the same value, so the
assignment is consistent. QED

Therefore no constraint on `P_x` alone, beyond (T1), can be extracted from (5.2). Together
with (P), (57) and (62) this makes the system of §0 the complete single-centre system generated
by the paper's inputs.

---

## 3. Theorem (the reduction)

**Theorem 3.1.** *Let `k >= 6`, let `G` be a graph on `I`, and let `E(P) = {ij : sigma{e :
P(e) <= {i,j}} = 0}`. Then there is a measurable `P : S -> 2^I` satisfying (P), (57), (T1)
with `G <= E(P)` if and only if there exist nonempty `S, T <= I` with*

  `|S| <= k-3`, `|T| <= k-3`, `S cap T = empty`, `S cup T != I`,

*and neither `S` nor `T` a subset of an edge of `G`.*

(Recall `G <= E(P)` is exactly constraint **(62)** for every edge of `G`, so Theorem 3.1 is a
statement about the system `(P),(57),(T1),(62)`.)

*Proof.* (=>) Let `P` satisfy (P), (57), (T1) and `G <= E(P)`. `P` takes finitely many values,
so writing `A_S = {e : P(e) = S}` for a value `S`, the finitely many `A_S` cover the circle and
some `A_S` has `sigma(A_S) > 0`.
Since `G <= E(P)`, for every edge `ij` of `G` the set `{e : P(e) <= {i,j}}` is null; hence
`A_S` is not contained in it, i.e. `S` is not a subset of `{i,j}`. By (57), for `e in A_S` we
have `P(Re) cap S = empty`, so `R(A_S)` is contained in `{e : P(e) cap S = empty}`, a set of
positive measure. That set is the finite union of the `A_T` over values `T` with `T cap S =
empty`, so some such `T` has `sigma(A_T) > 0`; it is not a subset of any edge of `G` by the
same argument; and `S cup T != I` by (T1). (<=) Given `S, T`, put
`A = [0,pi/3) cup [2pi/3,pi) cup [4pi/3,5pi/3)` (in angular units of `pi`), which satisfies
`R(A) = A^c` and `R^2(A) = A`, and define `P(e) = S` on `A`, `T` on `A^c`. Then `P` is
measurable, takes only the two values `S, T`, so (P) and (T1) hold by hypothesis; and
`P(Re) cap P(e) = S cap T = empty` when `e in A` and `= T cap S = empty` when `e in A^c`, so
(57) holds (after discarding the finitely many sector endpoints). Finally `G <= E(P)` is
exactly the last hypothesis, since the values are `S` and `T`. QED

---

## 4. Theorem (the classification)

**Theorem 4.1.** *(i) `k = 6`: `G` is compatible with (P),(57),(T1),(62) iff `G != K_6`.
(ii) `k >= 7`: every `G` is compatible.
(iii) `k = 5`: `G` is compatible iff the family consisting of the non-edges of `G` together
with the isolated vertices of `G` has two disjoint members; equivalently iff it is not an
intersecting family. Exactly 76 of the 1024 graphs on 5 labels are incompatible.*

*Proof.* Write `V(G)` for the set of admissible values, i.e. nonempty `S` with
`|S| <= k-3` and `S` not a subset of an edge of `G`. Note that a set of size `>= 3` is never
a subset of a 2-element set, so **every `3`-set is admissible whenever `k >= 6`.**

(i) For `G = K_6` every pair is an edge, so an admissible value of size `<= 2` would be a
subset of a pair, i.e. of an edge; hence `V(K_6)` is exactly the set of 20 triples. By
Theorem 3.1 a good pair needs two disjoint triples in a 6-element set, which forces them to
be complementary, i.e. `S cup T = I`, which is excluded. So `K_6` is incompatible.
Conversely let `G != K_6` and pick a non-edge `{a,b}`. Take `S = {a,b}` (admissible: `{a,b}`
is a subset only of `{a,b}`, which is not an edge) and `T` any 3-subset of `I \ {a,b}`
(admissible, as noted). Then `S cap T = empty` and `|S cup T| = 5 != 6`. Theorem 3.1 gives
compatibility.
(ii) Two disjoint 3-sets are always admissible (as noted, and `3 <= k-3` for `k >= 6`) and
their union has 6 elements, which is `< k`. Theorem 3.1 gives compatibility for every `G`.
(iii) `k = 5` gives `k-3 = 2`, so admissible values are exactly the non-edges (2-sets) and the
isolated vertices (1-sets); the only further requirement of Theorem 3.1 is disjointness, since
`|S cup T| <= 4 < 5`. This is the stated intersecting-family condition. QED

**The 76 at `k = 5`, enumerated** (this is the EKR structure, checked exactly):
`0` non-edges and `0` isolated vertices: `1` graph (`K_5`); `1` non-edge: `10`; `2` pairwise
intersecting non-edges: `30`; `3` pairwise intersecting non-edges (`30 = 10` triangles `+ 20`
three-edge stars); `4` non-edges, necessarily a 4-edge star, with the star's centre as the
unique isolated vertex: `5`. Total `1+10+30+30+5 = 76`. (A family of 2-subsets of a 5-set is
pairwise intersecting iff it is a star or a triangle — EKR for `n = 5, r = 2`.)

**Sharpness of the maximum at `k = 6`.** `E(P)` has at most 14 edges: 15 would force
`|P(e)| = 3` a.e. (by (62) for all pairs), hence `P(Re) = I \ P(e)` a.e. by (57), hence (T1)
is violated on a set of positive product measure. 14 is attained, by `P = {1,2,3}` on `A`,
`{4,5}` on `A^c`, where `E(P) = K_6` minus the single edge `{4,5}`.

---

## 5. Theorem (sharpness of the `k = 6` palette inequalities)

**Theorem 5.1.** *Let `k = 6`, `A` as in Theorem 3.1, and `P(e) = {1,3,5}` for `e in A`,
`P(e) = {2,4}` for `e in A^c`. Then:*

1. *(P), (57), (T1) hold exactly;*
2. *the orbit bound is attained: exactly `3` of the `6` palettes in every `R`-orbit are
   ternary, so `sigma(E_x) = pi`;*
3. *the mean bound is attained: `(1/2pi) int |P_x| dsigma = 5/2` exactly;*
4. *`C_6 <= E(P)`, where `C_6` is the six-cycle `12,23,34,45,56,61`.*

*Proof.* (1) `{1,3,5} cap {2,4} = empty`, both sizes lie in `[1,3]`, and the two values do not
cover `I` (their union misses `6`). `A` is `R^2`-invariant with `R(A) = A^c`, so `P(Re)` is
always the *other* value and (57) holds. (2) The `R`-orbit alternates the two values, so it
contains three copies of the triple and three of the pair. (3) The mean of `|P|` over two
values of sizes 3 and 2 taken on sets of angular measure `pi` each is `(3+2)/2 = 5/2`. (4)
`{1,3,5}` is a triple, hence not a subset of any pair; `{2,4}` is a subset only of the pair
`{2,4}`, which is a diagonal and not an edge of `C_6`. QED

Theorem 5.1 is the exact sense in which item 1 of `results/K6-BARRIER.md` §5 ("a palette bound
`|P_x(e)| <= 2` for six-colourings") cannot be obtained from one centre: the extremal object
for every published single-centre inequality is realised, and still carries `C_6`.

---

## 6. What is and is not claimed

**Class covered.** Arguments that, at a single centre `x`, use the palette function `P_x` and
the transition graph `Gamma_x` only through the paper's inputs (5.2), (5.7), Lemma 6.2 and the
palette bound. By Lemma 2.1 the constraint set of §0 is complete for that class in the
palette direction.

**Not claimed.**
* No bound on `chi(R^2)`.
* The converse of Theorem 3.1 is a statement about the constraint *system*, not about
  colourings: it exhibits a measurable palette function, not a colouring with `Gamma_x = G`.
  (By `smwfhd5sl/m8`, the *full* system including (5.3) at all centre pairs is equivalent to
  `chi <= k`; that equivalence is exactly what the single-centre system lacks, and the point
  of Theorem 4.1 is to say what is lost.)
* Nothing about two-centre constraints. Theorem 4.1 is what forces every remaining step to
  use at least two centres.

**Vacuity tests run.**
* At `k = 5` the mechanism of Theorem 4.1(i) is *vacuous*, because `2(k-3) = 4 < 5` so two
  admissible values can never cover `I`; and indeed at `k = 5` the exclusion of `K_5` has a
  different cause (no admissible value exists at all). This confirms that the `k = 6`
  exclusion is a genuine `k = 6` phenomenon, not an artifact.
* At `k >= 7` the same computation excludes nothing, so Theorem 4.1(i) is `k`-sensitive in
  the strongest possible sense.
* The exhaustive enumeration at `k = 6` finds `K_6` and nothing else, so the theorem is not
  over-strong.

---

## 7. Files and how to check

| file | content |
|---|---|
| `work/classify2.py` | exhaustive classification for `k = 5, 6` by **two** independent decision procedures plus a closed-form decision; sampled cross-check for `k = 7, 8`; `k = 5` characterisation; maximum `|E(P)|`; exact verification of five witnesses |
| `work/verify_witnesses.py` | **third, object-level** code path: for all `32767` graphs `G != K_6` constructs the witness `(S,T)` and verifies (P), (57), (T1), (62) directly on an exact rational subdivision of the circle; and exhaustively confirms that no witness exists for `K_6` |
| `work/classify.c` | **fourth** check, in C with a different data representation (bitmasks, integer loops): exhaustive decision at `k = 6` and a direct *count* of the 210 value pairs at `K_6` (0 good) |
| `proof.md` | this document |
| `work/paper.txt`, `work/pages/` | the extraction used, and the rendered pages 27–28 |

Commands:

```
cd .ultramath/smwfo9zkl/m1/work
python3 classify2.py        # ~9 s, exit 0, prints "all cross-checks agree; no mismatches"
python3 verify_witnesses.py # ~10 s, exit 0, prints "failures: 0" and "any admissible one? False"
cc -O2 -o classify classify.c && ./classify   # <1 s, exit 0
```

Output summary of record:

```
k=5: 1024 graphs, 76 incompatible
k=6: 32768 graphs, 1 incompatible          the incompatible graph is K_6: True
k=7: 3000 random graphs, mismatches=0, satisfiable=3000/3000
k=8: 3000 random graphs, mismatches=0, satisfiable=3000/3000
k=6: witnesses constructed and verified end-to-end for 32767 graphs (G != K_6), failures: 0
K_6: 820 value pairs tested, any admissible one? False
C  : graphs = 32768, compatible = 32767, incompatible = 1 (15 edges)
K_6: admissible values = 20 (the triples); value pairs = 210; good pairs = 0
```

---

## 8. Corollaries for the `k = 6` route, and a falsification test

**Corollary 8.1 (no single-centre exclusion of any stratum).** *At `k = 6` the single-centre
palette system `(P),(57),(T1),(62)` excludes no cycle stratum: `C_3, C_4, C_5` and `C_6` are all
compatible, and more generally every graph on six labels other than `K_6` is compatible.*
So the triangle case, the square case, the five-cycle case and the six-cycle case of Theorem 6.5
all require **at least two centres**; none of them can be settled by palette data at one centre,
and neither can local finiteness of `L` itself.

**Corollary 8.2 (the palette bound 2 is not reachable at one centre).** *No constraint on
`P_x` alone — in particular no consequence of (5.2), (5.7) and the palette bound — can improve
`|P_x(e)| <= 3` to `|P_x(e)| <= 2` at `k = 6`.* (Theorem 5.1 realises `|P_x| = 3` on a set of
directions of measure exactly `pi`, i.e. the maximum allowed by the orbit bound.)

**Corollary 8.3 (falsification test for any proposed extra input).** Let `X` be any proposed
additional input at `k = 6` intended to open the §7 route. If `X` is satisfied by every member
of the following explicit family, then `X` cannot decide anything:

> for any two disjoint nonempty `S, T <= I = {1,...,6}` with `|S|, |T| <= 3` and
> `S cup T != I`, the palette function `P^S,T` with `P(e) = S` on
> `A = [0,pi/3) cup [2pi/3,pi) cup [4pi/3,5pi/3)` and `P(e) = T` on `A^c`.

Every such `P^S,T` satisfies (P), (57), (T1), has mean palette size `(|S|+|T|)/2 <= 5/2` and
at most three ternary palettes per `R`-orbit, and satisfies (62) for every graph whose edge set
avoids all pairs containing `S` and all pairs containing `T` — in particular for `C_6` with
`S = {1,3,5}`, `T = {2,4}`. This is a one-line test: a proposed input that does not fail on
some `P^S,T` is inside the powerless region.

---

## 9. Where this leaves the direction

`d12` asked which transition graphs a cyclic centre can have at `k = 6`. The answer is
complete: **all of them except `K_6`**. That is a negative answer to the question "can the
single-centre object that d2/d5/d7 consume be classified usefully", and it is sharp in the
sense that `K_6` really is excluded (and `K_k` is not excluded for any `k >= 7`).

The route that remains open, and that this document does not touch, is the two-centre one:
by `smwfhd5sl/m8` the full palette system with (5.3) at all centre pairs is *equivalent* to
`chi <= k`, so no finite amount of single-centre data can decide `k = 6` — Theorem 4.1 is the
exact statement of that blindness for the `k = 6` palette system, including all the
inequalities that the barrier analysis introduced.

**Corollary 8.4 (every `k = 6` centre has a positive-measure binary palette value, and it is
not a transition).** *At `k = 6`, for every centre `x` there is a pair `{i,j}` of labels with*

  `sigma{e : P_x(e) <= {i,j}} > 0`,   *and*   `{i,j}` is **not** an edge of `Gamma_x`.

*Moreover, if `Gamma_x` contains the six-cycle `C_6`, that pair can be taken among the nine
diagonals of `C_6`.*

*Proof.* By `Gamma_x <= E(P_x)` and Theorem 4.1(i), `E(P_x) != K_6`, so some pair `{i,j}` is not
in `E(P_x)`; by the definition of `E(P)` this says exactly `sigma{e : P_x(e) <= {i,j}} > 0`, and
`{i,j} not in E(P_x)` together with `Gamma_x <= E(P_x)` gives `{i,j} not in Gamma_x`. If
`Gamma_x` contains `C_6` then the six edges of `C_6` lie in `Gamma_x <= E(P_x)`, so the missing
pair is not one of them, i.e. it is a diagonal. QED

The first half is equivalent to the statement that not all palettes at `x` are ternary, which is
also [smwfhd5sl/m6, Theorem 2]; the point of the corollary is the conjunction: the pair that
carries a positive-measure binary palette value is *never* a transition, and for a six-cycle
centre it is forced into the nine diagonals. That is the only structural consequence the
single-centre system yields at `k = 6`, and it is what a two-centre argument for the six-cycle
stratum (`d2`) has to build on.
