# L4: a certified no-go for the *six-step relaxation* of the cover-and-palette class

**Status: assembled from five machine-checked or exhaustively-certified components, all reproduced
here.** It does not settle chi(R^2); it certifies that one precisely delimited class of arguments
cannot decide k = 6, gives the specification a replacement must satisfy, and gives explicit
examples. Sources: m5 (CSP), m2 (sliver), m7 (pointwise collapse), m8 (a.e. collapse), m1 (circle),
all in `.ultramath/smwfhd5sl/`.

**Correction (added after m8's report).** An earlier version of this note claimed that the
a.e.-in-angle class is the only place an L4 no-go can live. That is false. m8 proves that the
palette system with the paper's own (5.3), a.e. in angle with exceptional sets per centre pair,
already satisfies: *satisfiable at level k iff chi(R^2) <= k*. The key step is the paper's
Remark 5.3 — for any fixed unit direction `a` the representation `(x+a) + f = x + f + a` is
admissible off `f = ±a`, so (5.3) gives `P_x(f) ∩ P_{x+a}(f) = empty` for a.e. `f` at every unit
pair; `E` and its unit directions are countable, so one direction serves all unit pairs of `E` at
once, and a choice of one label per palette is a proper colouring of `E`, whence `chi <= k` by R1.
Consequently **the full palette class is not weaker than the problem: it is the problem**, and no
L4 no-go exists for it — not because the method is too weak, but because it loses nothing. The no-go
below is therefore for the *deliberately weakened* class that keeps only the six-step disjointness
and drops (5.3) at all other directions, which is where an L4 can be true.

---

## 1. The class

An argument is **state-level cover-and-palette at k** if, from a weak measurable k-colouring, it
uses only:

1. **Palette bound.** `1 <= |P_x(e)| <= k - 3` for a.e. `e` (Proposition 5.6, general-k proof).
2. **Sliver non-emptiness.** `P_x(e)` meets both one-sided allowed sets `O(e)`, `I(e)` of
   Lemma 8.1, whose sizes are `|O| = k - l + #{both incident edges negative}`, `|I| = k - l +
   #{both positive}` (Lemma 1.1 of m2).
3. **Six-step disjointness.** `P_i ∩ P_{i+1} = ∅` on the six `pi/3`-steps of the `R`-orbit (5.7).
4. **Label-blind cover data.** The cover obstruction of §7, valid for any mesh `d < 5` and any
   number of labels (R4), sharp at multiplicity two (W4).
5. **Cycle length.** `3 <= l <= k` (Proposition 7.1).

It excludes, by definition: any pointwise transfer of labels between distinct centres beyond the
six steps; any use of Lemma 5.5 (binary-centre separation); and any use of the a.e.-in-angle
structure of Lemma 5.2 at a general pair of centres. Those exclusions are what make the no-go
true and what make it non-trivial.

## 2. The no-go

**Theorem L4a (six-step constraint systems are satisfiable at k = 6).** For every `l in {3,4,5,6}`
and every ray geometry (all `6^l` sign matrices, hence all sign words realisable by rays), there is
an assignment of palettes satisfying 1-3 above. Counts of satisfying geometries over `6^l`:
`l=3: 36/36`, `l=4: 216/216`, `l=5: 225/1296`, `l=6: 177/7776`; and `k = 7` is satisfiable
everywhere. So **no argument using only 1-3 can refute k = 6, for any value of its constants.**

*Certificate.* m5, `interface_csp.py` + `verify_interface.py`: exhaustive over all geometries, two
independent decision procedures (bitmask DP and backtracking) agreeing on 7848 instances, witnesses
checked against the paper's own definitions of `O_i`, `I_i` at three interior ray parameters each,
and satisfiability monotone in `k`. The same computation gives `k = 5`, `l = 5`: `0/1296` — the
CSP alone refutes the five-cycle interface (which subsumes Proposition 8.2 under the paper's
reduction from a colouring to a CSP solution), and `k = 4`: `0/36`, `0/216`, consistent with the
independent finding that the §5-§7 architecture is empty at `k = 4` (m2, Corollary 2.3).

**Theorem L4b (the rigidity step is unavailable at every length the method can return).** At
`k = 6`: for `l = 3`, `|O(e)|, |I(e)| >= 3` for every `e` and every sign word, so no side is
confined to two labels and Lemma 8.6 cannot run; `l = 5` admits no sign word with two-element
slivers on both sides (a cyclic word has an even number of runs, so `R = 3` is impossible);
`l = 6` admits two-element slivers only with *different* pairs (`O = {3,4}`, `I = {0,1}`), so the
two-sliver exchange fails; `l = 4` works only for the non-generic ray arrangement `v_0 = v_2`, and
then only up to a residual `chi >= 5` gadget (S4 below). Since Proposition 7.1 may return any of
these lengths, the class cannot decide `k = 6`.

*Certificate.* m2, `verify.py` (counts `0/8`, `2/16`, `0/32`, `6/64` for two-element slivers at
`l = 3,4,5,6`), `transplant.py` (exact rational rays witnessing the general-position failure),
`verify_certificate.txt` (byte-identical reproduction).

**Theorem L4c (the pointwise escape is not an escape).** If the transfer input is used
*pointwise* — a palette field `Q` with (P0) non-emptiness and (P1) no label shared between the
palettes at `(a,s)` and `(b,f)` whenever `|a - b| = 1` and `b - a` is not parallel to `s` — then the
plane is `k`-colourable. So exhibiting a pointwise palette system at `k = 6` is exhibiting a
6-colouring: the pointwise class is not a relaxation of the problem, and it cannot yield a no-go.
Both axioms are needed (dropping either destroys the conclusion).

*Certificate.* m7, `Collapse.lean`, `exists_coloring_of_palette`, compiled here under the pinned
toolchain, axioms `[propext, Classical.choice, Quot.sound]`; `collapse_check.py` blocks 2 and 3.

**Theorem L4d (single-centre circle arguments cannot do it).** The unit-chord graph on a circle of
radius `r` has chromatic number at most `3`; it is `3` exactly when `theta/2pi = p/q` in lowest
terms with `q` odd, `theta = 2 arcsin(1/(2r))`, attained at `r = 1/sqrt 3`, and `2` otherwise
(components are `q`-cycles, or bi-infinite paths when `theta/2pi` is irrational). Since an arc
shorter than `theta` carries no chord, every label set is realisable on it: no single-centre circle
argument excludes a ternary palette at `k = 6`, for any radius or constant, and `3 = k - 3` is
exactly the cap.

*Certificate.* m1, `verify_sphere.py`, `verify_ball.py`.

**Corollary.** The k-dependence of the method is entirely in the *cross-centre* part, and there it
is *complete*: every class that uses the pointwise transfer collapses to the problem (L4c), and so
does every class that uses the a.e. form of (5.3) (m8, Theorem A). Every single-centre class is
blind (L4d). What remains satisfiable at `k = 6` is only the class that keeps the six-step
disjointness and *drops* (5.3) at all other directions (L4a) — a strictly weaker class, and the
honest scope of the no-go. The palette framework as the paper states it is therefore not an
approximation to the problem but a reformulation of it; a failure to decide `k = 6` inside it is a
failure to solve the problem, not a limitation of the method.

## 3. The specification (falsifiable requirements for a replacement)

Each item names the printed step it replaces and a refutation test.

* **S1 (sliver, not palette).** Produce, at the length Proposition 7.1 actually returns, a colour
  set of size exactly two on a one-sided sliver, by a statement about essential supports, not about
  palettes. *Refuted by:* `k = 6`, `l = 3`, where both slivers have at least three allowed labels
  for every sign word (L4b).
* **S2 (same pair on both slivers).** If the rigidity exchanges through two slivers at angle
  `pi/3`, prove they carry the *same* two labels. *Refuted by:* `k = 6`, `l = 6`, `+++---`, where
  the two-element slivers are `{3,4}` and `{0,1}`.
* **S3 (k-sensitivity).** The conclusion must depend on an integer that is not a palette bound.
  *Refuted by:* a conclusion derived from `(k, l, w)` alone; the only such integers are `k - l` and
  `k - 1`, both already used.
* **S4 (terminal gadget).** Exhibit a finite unit-distance graph with exact coordinates not
  colourable with the `k - 2` labels of the exclusion region; at `k = 6` that is `chi >= 5`.
  *Refuted by:* the absence of such a graph — currently the live gap of the only sub-case
  (`l = 4`, `v_0 = v_2`) that reaches this far.
* **S5 (locality).** The `k`-dependence must be computable from `(k, l, w)` and the gadget, and
  invariant under replacing the palette bound. *Refuted by:* any step whose validity changes when
  `|P|` changes at fixed `(k, l, w)`.
* **S6 (multiplicity three).** A replacement for the cover lemma must handle multiplicity three
  (W4's explicit cover). *Refuted by:* any replacement assuming multiplicity at most two.
* **S7 (a.e. structure).** If the replacement uses the a.e. form of Lemma 5.2, it must use the
  joint structure across centres; the a.e. conclusion alone is satisfied by unions of parallel
  lines, which are not colourings (m7, CHECK 5).

## 4. The explicit examples

* **Where a replacement works and the printed method does not.** At `k = 6`, `l = 4` with
  `v_0 = v_2`, the binary-sliver selection rule carries the whole §8 chain — local rigidity,
  boundary orbit, polynomial region — to a single residual requirement (S4), whereas §8.3 as
  printed treats one outsider and a two-element palette and has no instance here (m2, Theorem 4.1).
* **Where every local method fails.** The annulus `0.95 < |z| < 1.05` with
  `f(z) = floor(9 arg z / 2pi) mod 3` is 3-valued, nowhere locally constant, and has no
  monochromatic unit pair: every unit pair in it has angular separation in `(2pi/9, 4pi/9)`, by
  exact rational bounds (m5, `annulus3.py`). This kills the natural `k = 6` repair of Lemma 8.6.
* **Where the ball already decides.** `chi(B(x,1)) >= 4`, by the seven-vertex Moser spindle with
  minimal enclosing circle `r^2 = 9/11 < 1` (m1, `verify_ball.py`): the unit ball forces four
  colours where the palette window forces exactly three.

## 4b. Two further necessary conditions, and the next computation

m6 adds two consequences of the paper's own inputs that the six-step relaxation above does not
impose: **(C1)** if `A ∪ B = Fin k` then the direction sets `{e : P_x(e) = A}` and
`{e : P_x(e) = B}` cannot both have positive angular measure (transfer at a positive-measure product
set); **(C2)** at `k = 6` at most three of the six palettes in a `pi/3`-orbit are ternary, so
`sigma{|P_x| = 3} <= pi` and the mean palette size is `<= 5/2`. Both bounds are attained (ternary
cells `[0,2,4]`, `sigma(E)/2pi = 1/2`, mean `5/2`, with (5.7) on all six consecutive pairs), so
neither improves by a constant; the Lean core is `OrbitLemma.lean`, axioms clean.

So the six-step relaxation of §1 is strictly weaker than a faithful palette model for a precise
reason: it omits (C1) and (C2). The concrete next computation is to re-decide m5's CSP with both
added — the 20 all-ternary orbits m6's script enumerates are exactly the models that disappear.

**Correction on the scope of the whole note (added after the third swarm).** The six-step CSP is a
relaxation only *if* a 6-colouring is known to have an interface. It is not: Proposition 7.1's proof
is `k = 5`-only at Theorem 6.5, whose triangle case needs `|P| <= 2 = 5 - 3` (m10). So at `k = 6`
there is no induction lemma, and the no-go below is about a constraint system that no 6-colouring is
known to instantiate. It remains a certified no-go for the class as defined, but its relevance to
`k = 6` depends on a cyclic-centre theorem that does not exist yet. Also: adding (C4)+(C5) changes
nothing, because every model shrinks to binary palettes (m10, `Shrink.lean`).

**Correction on the logic of that computation.** Every weak measurable 6-colouring induces a model
of the six-step CSP (its palettes at the six directions, with the interface data Proposition 7.1
supplies). Hence the CSP is a *relaxation* of the colouring problem, and UNSAT of the tightened CSP
at every (length, ray geometry) that Proposition 7.1 can produce would be a proof that no
6-colouring exists, i.e. `chi >= 7` — a terminal outcome, not merely a wider L4. What is true is the
converse: SAT of the relaxation proves nothing, because a relaxation can be satisfiable when the
original is not. m5's decision was SAT at every length, so the relaxation is currently
non-informative; adding (C1)+(C2) is worth doing precisely because UNSAT there would be decisive.
(An earlier verdict of mine said this computation "cannot be a bound on chi"; that was wrong.)

## 5. What is not claimed

No bound on `chi(R^2)`; no no-go for the a.e. class; no claim that the class in §1 is the largest
class of "§5-§7 arguments" — it is a precisely delimited class, and the delimitation is part of the
result. L4's acceptance asks for a no-go on a delimited class that is not a strawman, and the two
examples of §4 are the evidence that it is not: the class contains the printed argument, which
decides `k = 5`, and it contains a working replacement at `k = 6`, `l = 4`.
