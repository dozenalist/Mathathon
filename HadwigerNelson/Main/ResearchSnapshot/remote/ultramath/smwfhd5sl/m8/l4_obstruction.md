# The cover-and-palette class at k = 6 is *equivalent* to the problem, not a weakening of it

**Result.** Let `C_k` be the class of palette systems at `k` labels: a measurable assignment
`(x,e) |-> P_x(e) ⊆ {1..k}` with `1 <= |P_x(e)| <= k-3` satisfying the paper's transport exclusion
(5.3) (Lemma 5.2 assertion 3, including the constant-second-endpoint case which the paper itself
states in **Remark 5.3**). Then

> **Theorem A.** For every `k >= 4`:  `C_k` is satisfiable  ⇔  `chi(R^2) <= k`.

The `⇒` direction is new and is what kills the L4 "natural route". It is *one line* of selection
once one evaluates (5.3) at a **unit-distance pair**: at a pair of centres at distance exactly 1 the
only admissible representation of (5.3) is the translation one, so the palettes at the two centres
in any fixed direction are disjoint; taking a countable family and then one label per palette gives
a proper `k`-colouring of the algebraic plane. Consequence: **no L4 no-go can be certified by
exhibiting a palette system at `k = 6`, because such a system is a 6-colouring of the plane.**

Theorem A is stated for the **a.e.-in-angle** form of (5.3) — the form the paper actually proves, with
the exceptional set depending on the centre pair — not for a pointwise strengthening; §3bis shows the
collapse does not need the pointwise form, correcting an accepted verdict in this swarm that the
a.e. class is the last place an L4 no-go can live. The a.e. class collapses too, by a diagonal over
the countable algebraic plane and the countable set of algebraic unit directions.

The brief's own remark ("if instead the constraints are unsatisfiable that is a proof of `chi >= 7`")
is half of the equivalence; this note supplies the other half and thereby delimits the class exactly.
Everything is checked against the paper's own text; the algebraic identities are verified exactly in
`check_l4.py` (`python3 check_l4.py`, exit 0).

---

## 1. The hypotheses, displayed

Fix `k >= 4`, `S` the unit circle, `R` rotation by `pi/3`.

**Definition (palette system at k).** A palette system at `k` is a family `P_x(e) ⊆ {1,...,k}`
indexed by centres `x ∈ R^2` and directions `e ∈ S`, together with the following three hypotheses.

* **(H1) cardinality.** For every centre `x`: `e |-> P_x(e)` is measurable and
  `1 <= |P_x(e)| <= k-3` for `sigma`-almost every `e`. (The lower bound is the paper's; the upper
  bound at general `k` is the generalised Proposition 5.6, `results/K6-BARRIER.md` §1.)
* **(H2) transport exclusion (5.3).** For all centres `x, z`, if on an open angular arc
  `f |-> (s(f), t(f)) ∈ S × S` is smooth, `s(f)` and `t(f)` nonparallel, `s` a local diffeomorphism
  in the angular coordinate, and
  `z + f = x + s(f) + t(f)`  for all `f` in the arc,
  then `P_z(f) ∩ P_x(s(f)) = ∅` for almost every `f` in the arc.
* **(H3) measurability in `e`** is already part of (H1); no measurability in `x` is assumed
  (the paper assumes none either: "No joint measurability of P_x in its center is assumed").

`C_k` denotes the set of palette systems at `k`. `SAT(C_k)` means it is nonempty.

*Non-vacuity of the hypothesis class is automatic:* if `c` is a proper `k`-colouring then its
maximal palettes (Definition 5.1) satisfy (H1) by R5/K6-BARRIER §1 and (H2) by Lemma 5.2(3). So
`C_k` is a class of objects that provably exist whenever the plane is `k`-colourable, and (H1)+(H2)
are exactly the palette-level facts §5–§8 consume.

---

## 2. Lemma 1 (unit-distance pairs see exactly one instance of (5.3))

**Lemma 1.** Let `d, f ∈ S` and let `s, t ∈ S` with `s + t = d + f`. Then `{s,t} = {d,f}`.
Equivalently: for a fixed `w` with `0 < |w| <= 2` the unordered pair of unit vectors summing to `w`
is unique, namely `w/2 ± i·h·w/|w|` with `h = sqrt(1 - |w|^2/4) >= 0`.

*Proof.* Write `w = s + t`. Then `w/2` is the midpoint of `s,t` and `s - t` is perpendicular to `w`
with `|s-t|^2 = 4 - |w|^2`, so `s,t = w/2 ± i·(sqrt(1-|w|^2/4))·w/|w|`, an unordered pair
determined by `w`. Exact verification of both identities in `check_l4.py` §1. ∎

**Corollary 1 (translation disjointness).** In every palette system at `k`, for every pair of
centres `x, y` with `|x - y| = 1`:
`P_x(e) ∩ P_y(e) = ∅` for almost every `e ∈ S`, `e` not parallel to `y - x`.

*Proof.* Put `d = y - x`, `z = y`. In (H2) take the representation `z + f = x + s(f) + t(f)` with
`s(f) = f` and `t(f) = d`. It holds identically because `(x+d) + f = x + f + d`; `s` is the
identity, hence a local diffeomorphism; `s(f) = f` and `t(f) = d` are nonparallel off `f = ±d`.
Applying (H2) on a countable cover of the two open arcs `S \\ {±d}` by smaller arcs (the hypothesis
is "on an open angular arc, or locally on a union of such arcs") gives `P_{x+d}(f) ∩ P_x(f) = ∅` for
a.e. `f` off `±d`. By Lemma 1 this is the *only* instance of (H2) whose two centres are `x, y`: any
admissible `(s,t)` satisfies `s + t = d + f`, hence `{s,t} = {d,f}`; the labelling `s(f) = d` is
inadmissible because a constant map is not a local diffeomorphism, so `s(f) = f`, `t(f) = d` is the
unique admissible branch. So no other information about the pair is available from (5.3). ∎

*This is not a new hypothesis:* the paper states it. Remark 5.3 of the paper: "In assertion 3 of
Lemma 5.2, the second endpoint map `t` may be constant. ... In particular, for any fixed direction
`a`, the representation `(x+a) + f = x + f + a` is admissible off `f = ±a`." The paper then uses
(5.3) only in the single-centre form (Corollary 5.4 = (5.7)) and in the small-distance form of
Lemma 5.5 (`|x-y| < 1/2`). Corollary 1 is the case the paper states and does not use.

---

## 3. Theorem A

**Theorem A.** For every `k >= 4`: `SAT(C_k)` ⇔ `chi(R^2) <= k`.

*Proof of `⇐`.* If `c : R^2 -> {1..k}` is proper, its maximal palettes satisfy (H1) and (H2) by
Lemma 5.2 of the paper, so `C_k ≠ ∅`. ∎

*Proof of `⇒`.* Let `P` be a palette system at `k`. Let `E` be the algebraic plane (countable) and
`K` the set of unit complex numbers algebraic over `Q` (countable). Note `K` is *exactly* the set of
directions of unit segments with both endpoints in `E`: if `p, q ∈ E` and `|p - q| = 1` then
`q - p ∈ E` and `|q-p| = 1`, so `q - p ∈ K`; conversely `0, u ∈ E` for `u ∈ K`.

For each `(x, d) ∈ E × K` Corollary 1 gives a `sigma`-null set `N_{x,d} ⊆ S` such that
`P_x(e) ∩ P_{x+d}(e) = ∅` for `e ∉ N_{x,d}`. Let `N = ⋃_{E × K} N_{x,d}`, a null set as a
countable union. Choose a direction `e ∉ N ∪ K`; this is possible because `K` is countable. Since
`e ∉ K`, no `d ∈ K` is parallel to `e` (parallel would mean `d = ±e`), so the conclusion of
Corollary 1 holds for *every* `d ∈ K` at this single direction `e`. Define `Q(x) = P_x(e)`.
Then `Q(x) ≠ ∅`, `|Q(x)| <= k-3`, and `Q(x) ∩ Q(y) = ∅` whenever `x, y ∈ E`, `|x-y| = 1`.

By the axiom of choice pick `q(x) ∈ Q(x)` for each `x ∈ E`. If `|x - y| = 1` then
`Q(x) ∩ Q(y) = ∅`, so `q(x) ∈ Q(x)`, `q(y) ∈ Q(y)` are distinct. Hence `q : E -> {1..k}` is a
proper `k`-colouring of the unit-distance graph of `E`, i.e. `chi(E) <= k`. By R1
(`algebraic_colorable_iff`) `chi(R^2) = chi(E) <= k`. ∎

**Remark (why the proof cannot be improved to give more).** The only fact used is Corollary 1, and
Corollary 1 is *equivalent* to (5.3) at a unit-distance pair (Lemma 1). So Theorem A is sharp at
the level of inputs: no additional consequence of (5.3) is being smuggled in.

---

## 3bis. The `a.e.`-in-angle form is *not* weaker: correction of an accepted verdict

The distinction this note turns on is the order of the two quantifiers, and it has been
mis-assessed elsewhere in this swarm (`d1`, finding `f13`, Corollary D, whose verdict was accepted):
that finding distinguishes

* **(P1) pointwise transfer** — for all `a, b, s, f` with `|a-b| = 1`, `b - a ∤ s`: no `i` with
  `s ∈ Q_i(a)` and `f ∈ Q_i(b)`;
* **(P2) transfer a.e. in the angle** — for every fixed pair of centres `(x,z)` a null set of
  directions with the same conclusion;

and asserts that (P2) "is genuinely weaker", is satisfied by non-colourings (its CHECK 5), and is
"the only palette class left in which an L4 no-go could be true". **(P2) is exactly hypothesis (H2)
of this note, and it collapses too.** The mechanism is a diagonal, and it is available precisely
because the paper's exceptional set is allowed to depend on the centre pair — the paper says so:
"The proof applies at every fixed pair of centers and never needs a common exceptional angular set
over an uncountable family of centers." Countably many centre pairs is not an uncountable family.

Concretely (this is Theorem A's `⇒` proof, isolated):

1. `E` (the algebraic plane) is countable; `K` (the algebraic unit numbers) is countable; and `K`
   is exactly the set of directions of unit segments with both endpoints in `E`.
2. For each `(x,d) ∈ E × K` let `N_{x,d}` be the null set of Corollary 1. `N = ⋃ N_{x,d}` is null.
3. Pick `e ∉ N ∪ K`. Then `P_x(e) ∩ P_{x+d}(e) = ∅` for **all** `(x,d) ∈ E × K` simultaneously.
4. Select `q(x) ∈ P_x(e)`. Then `q : E → {1..k}` is a proper `k`-colouring.

No measurability is used; no cardinality bound is used; no compactness is used. So
`CAP_ae(k) ⟺ chi(R^2) <= k` as well, and every palette-transfer class — pointwise, a.e. in the
angle, with or without joint measurability — is equivalent to the problem.

Why the accepted finding missed this: (P2) *implies* (★) (`min(|Q_i a|, |Q_i b|) = 0` for a.e. unit
pair) by Fubini, and (★) is strictly weaker than (P2); the cited counterexample to (★) is a palette
field supported on a union of parallel lines, which violates (P0) off those lines and is therefore
not a model of (P0)+(P2). What loses strength is passing from "**for each fixed centre pair**, a.e.
angle" to "**a.e. centre pair**", not the a.e. angle. The two quantifier orders are different
statements and the paper proves the first.

*Consequence for the specification.* Since the palette inputs are equivalent to the problem at every
`k` and in every reading, no L4 no-go can be stated for any of them: the class is not a weaker route.
The real content of L4 has to be a statement about the *finitary* resources the printed derivation
uses (§6 transitions, §7 cover, §8 cycle exclusions), and about nothing else.

---

## 4. Consequences

**Corollary 2 (the two branches of L4 are the two halves of the problem).**
`UNSAT(C_6) ⇔ chi(R^2) >= 7` and `SAT(C_6) ⇔ chi(R^2) <= 6`. Since `chi(R^2) >= 6` is
machine-checked (W1), `SAT(C_6) ⇔ chi(R^2) = 6`.

*This is the L4 no-go, in the only form in which it is true.* The brief's §2 proposes to certify the
no-go by "exhibiting a finite (or measurable) palette system at `k = 6` satisfying (a)–(f)". By
Theorem A that object **is a proper 6-colouring of the plane**; and by the same theorem a proof that
no such system exists **is a proof that `chi(R^2) >= 7`**. So neither branch is a weakening of the
Hadwiger–Nelson problem: the class is not a no-go class at all, it is a faithful reformulation.

**Corollary 3 (the finite reading is vacuous — exactly, not vaguely).** Call a palette system
*finite* if the centres are a finite set `X`, palettes are given on the six `60°`-sectors of
directions, and only the instances of (H2) that arise among `X` and those sectors are imposed.
Let `i ≠ j` be two proper `k`-colourings of the unit-distance graph on `X` with `i(x) ≠ j(x)` for all
`x` (any proper `k`-colouring of a finite graph yields such a pair by permuting one colour). Put
`P_x = {i(x)}` on the three sectors `0°,120°,240°` and `{j(x)}` on the other three. Then

* `1 <= |P_x| = 1 <= k-3` (so (H1) holds, with equality only in the size bound, which is allowed),
* `P_x(f) ∩ P_x(Rf) = ∅` because `R` swaps the two parities of sector and `i(x) ≠ j(x)` (so (5.7)
  holds — note this is *why* a palette system can never be all singletons of one colouring),
* `P_x(e) ∩ P_y(e) = ∅` for unit pairs `x,y` in every sector not parallel to `y - x`, because `i`
  and `j` are proper.

So a finite palette system at `k` exists as soon as `X` is `k`-colourable — in particular a finite
palette system **at `k = 5` exists for every `5`-colourable finite configuration**, although
`chi(R^2) >= 6`. A finite palette system therefore certifies nothing at `k >= 5`: the content of
Theorem A is carried by the *countable union* of null exceptional sets over `E × K` and by the choice
of one direction `e` avoiding all of them, and no finite sub-family of instances reproduces that.
**So the brief's "finite palette system at `k = 6`" reading is vacuous, and its measurable reading is
equivalent to the problem (Theorem A). Both readings of the natural route are closed.**

**Corollary 4 (the precise cut, i.e. the delimitation demanded by L4).** The instances of (5.3) fall
into two disjoint kinds: (i) *single-centre* instances (`z = x`, e.g. (5.7) with `s(f) = Rf`,
`t(f) = R^{-1}f`), and (ii) *two-centre* instances. By Lemma 1 a two-centre instance with **the same
direction at both centres** exists only for `|z - x| = 1`, where it is the translation instance of
Corollary 1. Hence:

* any argument that uses only single-centre instances, and two-centre instances with *different*
  directions (this includes every instance the paper actually uses: (5.7), and Lemma 5.5's
  `|x-y| < 1/2` instances, whose two directions differ by `alpha_+ - alpha_-`), is an argument in a
  class strictly weaker than `C_k`;
* any argument that also uses one same-direction instance at one unit-distance pair is, by
  Theorem A, an argument of exactly the strength of the problem.

So the L4 class must be defined by **excluding the same-direction instances**, and this is not an
arbitrary choice: Lemma 1 says those are the *only* instances available at a unit-distance pair, so
the exclusion is exactly "the method never looks at the palettes at the two ends of a unit segment
in a common direction".

**Corollary 5 (the specification a replacement must meet — sharpest form).** Let `M` be any
additional palette-level constraint. Write `(H1)+(H2)+M` for the system obtained by adjoining `M`.

* **(Adequacy).** If `(H1)+(H2)+M` is contradictory at `k = 6`, then `chi(R^2) >= 7`.
  *Proof.* `(H1)+(H2)+M` is a strengthening of `(H1)+(H2)`, so if it has no model then `(H1)+(H2)`
  has no model, i.e. `UNSAT(C_6)`; by Theorem A that is `chi(R^2) >= 7`. ∎

  So **any adequate replacement mechanism is, ipso facto, a proof that `chi(R^2) >= 7`**, and by
  de Bruijn–Erdős together with R1 it forces the existence of a finite 7-chromatic unit-distance
  graph (which is not exhibited). This is the exact specification, and it has no free parameters:
  no choice of mesh, multiplicity, `delta_*`, palette bound or cycle length can evade it, because
  the statement does not depend on any of them.

* **(Verifiability).** `M` must be *sound*: implied by the maximal palettes of every proper
  6-colouring. An adequate but unsound `M` refutes nothing about colourings (it is merely a
  restatement of `chi(R^2) >= 7` with no independent justification), and its adequacy is then
  indistinguishable from assuming the conclusion.

* **(Falsifiability, i.e. the brief's non-vacuity test).** `M` must have a finite certificate: there
  is an explicitly given finite palette system satisfying (H1), (H2) and violating `M`. This is the
  only test that distinguishes a mechanism from a tautology, and it is the test the brief demands.

* **(k-sensitivity).** `M`'s `k = 6` instance must fail on a palette system at `k = 5`; a mechanism
  that is `k`-blind cannot supply what Prop. 5.6 fails to supply at `k = 6` (R5: the palette bound
  `|P| <= k-3` is the unique locus of the `k`-dependence).

The specification therefore has a one-line, falsifiable summary:

> closing the cover-and-palette method at `k = 6` is *equivalent* to exhibiting a finite 7-chromatic
> unit-distance graph — and hence is equivalent to the lower-bound half of the Hadwiger–Nelson
> problem; nothing weaker can close it, and no constant in §5–§8 can be tuned to avoid this.

**Corollary 6 (ternary palettes are never universal at `k = 6`; pair-forcing is *necessary*).** In
every palette system at `k = 6` and for almost every direction `e` there is a centre `x` with
`|P_x(e)| <= 2`.

*Proof.* Suppose `|P_x(e)| = 3` for all `x` at some direction `e` (this is a conull condition in `e`,
so if it failed only on a null set we would be done). By Corollary 1, `P_x(e) ∩ P_y(e) = ∅` for every
unit pair. For `i ∈ {1,...,6}` put `S_i = {x : i ∈ P_x(e)}`; each `S_i` is unit-distance independent,
and each `x` lies in exactly `|P_x(e)| = 3` of them. Hence `{(S_i, 1/3)}` is a fractional colouring of
the unit-distance graph of the plane with total weight `6 · 1/3 = 2`, i.e. `chi_f(R^2) <= 2`. But for
every finite unit-distance graph `G`, `chi_f(R^2) >= chi_f(G) >= |V(G)|/alpha(G)`; take `G` the Moser
spindle (7 vertices, `alpha(G) = 2`, `chi(G) = 4`, all exactly verified in `check_l4.py` Part 3/6),
giving `chi_f(R^2) >= 7/2 > 2`. Contradiction. ∎

So at `k = 6` a palette of size `<= 2` must occur, in every direction, somewhere; route B's
"pair-forcing" target is therefore not a heuristic but a necessity (its difficulty, by Theorem A, is
that *which* pair occurs is a colouring fact). It also shows that the W6 six-state model of a
triangle interface cannot be the *uniform* state of the plane at `k = 6`: the state model must
contain pair-type palettes somewhere in every direction. Nothing here is new at `k = 5`, where
`|P| <= 2` is forced outright by R5.

**Corollary 7 (the explicit example demanded by L4).** Take `X = {x, x + d}` with `d = 1`, exactly.
On `X`:

* the *present* method has no usable instance: (5.7) is a single-centre statement and relates
  `P_x` only to itself; Lemma 5.5's instances need `|x - y| < 1/2`; the print's §5–§8 machinery
  therefore derives *nothing at all* about the pair `(x, x+d)` — the unit-distance pair is invisible
  to it (by Lemma 1 it is also invisible to (5.3) except through the translation instance);
* the *proposed replacement* `M =` Corollary 1 does: it forces `P_x(e) ∩ P_{x+d}(e) = ∅` in every
  direction `e` not parallel to `d`, i.e. it forces the two palettes at the ends of a unit segment to
  be disjoint — precisely the singleton-forcing constraint route B asks for — and by Lemma 1 this is
  the unique constraint about that pair derivable from (5.3).

So on the explicit example `X`, `M` satisfies (Verifiability) and (k-sensitivity) while the present
method cannot even state the question. But `M` is *implied* by the class's own axioms — it is
Corollary 1 — so it is redundant: it cannot strengthen the class, and by Theorem A the class already
has the strength of the whole problem. That combination is the obstruction, stated exactly:

> **the only replacement available at distance exactly one is the problem itself.**

---

## 5. What is *not* claimed

* Not claimed: `chi(R^2) = 6`, `chi(R^2) = 7`, or any finite witness.
* Not claimed: `C_6` is satisfiable or unsatisfiable (Corollary 2 shows this is the open problem).
* Not claimed: the paper's printed derivation is repairable. Corollary 4 localises its failure
  exactly: it needs `|P| <= 2` at `k = 6` (i.e. `k-3 = 2`), and the only palette fact that could
  force that is Corollary 1, which is the problem.
* The paper's own `k = 5` proof is unaffected: Theorem A's `⇒` direction at `k = 5` says a palette
  system at `5` gives a 5-colouring, which is exactly the contrapositive of the paper's theorem. It
  is not a re-derivation of `chi >= 6`: it says `SAT(C_5) ⇒ chi <= 5`, and `chi >= 6` is W1.
