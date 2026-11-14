# §8 at six colours: the angular layer is powerless for every cycle length

**Deliverable.** A decided finite computation with two independent decision procedures, and
three theorems. The outcome is negative and sharp: at `k = 6` the entire pointwise palette
system of §8 — Lemma 8.1's one-sided restrictions, Corollary 5.4, the palette bound,
Lemma 6.2's edge exclusions, and **self-avoidance at a typical centre** — is *satisfiable
for every cycle length* `ell in {3,4,5,6}`, on a full closed cell cycle of an explicit ray
configuration; and the same configurations also satisfy the open-set form of (5.2) and the
whole open-strip content of Lemma 8.1. So no argument built from those hypotheses can
exclude any cycle length at `k = 6`, and the coordinator's lead (direction 5) fails in its
palette form. Two positive by-products: a new structural law for §8 (the *antipodal law*),
which turns the whole §8 orbit analysis into a finite CSP, and a new purely combinatorial
proof of the paper's Proposition 8.2 (`ell = 5` impossible at `k = 5`) that never uses the
sign/run counting of §8.2.

Everything here is exact: rational arithmetic, no floating point, no sampling in the
decision procedure. Commands are in §9.

---

## 0. Conventions and the hypotheses used

`c` is a weak measurable `k`-colouring in the sense of the paper's §5; `P_x(e)` is the
maximal palette at the centre `x` in the direction `e` (Definition 5.1 and the paragraph
after it: `P_x(e) = {i : e` lies in the essential union `D_{x,i}` of the supports
`{b_i > 0}` over traces `b in W_x`}`). `R` is rotation of directions by `kappa = pi/3`;
`R` has order six. `x` is **typical** if it is a density-one point of its own colour
class; typical points are conull (Lemma 4.3 of the paper).

A centre `x` is a **cyclic centre** if `Gamma_x` contains a simple cycle; by Proposition
7.1 (as transferred to `k = 6`, `sprint/k6/REPORT.md` Theorem A, four audits plus the
machine-checked core `.ultramath/smwfo9zkl/m9/k6_s7_engine.lean`) there are then
`ell in {3,4,5,6}`, labels `0,...,ell-1` in cyclic order with edge `j = {j, j+1}`,
exclusion continua `K_j` and limiting unit directions `v_j`, such that

  `q_{j,n} = x + r_{j,n} w_{j,n} in K_j`, `r_{j,n} > 0`, `r_{j,n} -> 0`,
  `w_{j,n} -> v_j`.

The pointwise palette hypotheses at such an `x` are, with `sigma_j(e) = sign(e . v_j)`:

| name | statement | source |
|---|---|---|
| (S14) | `O(e) = [k]` minus the endpoints of every positive edge, `I(e) = [k]` minus the endpoints of every negative edge; both nonempty, and `P_x(e) cap O(e) != empty`, `P_x(e) cap I(e) != empty` a.e. | Lemma 8.1, (8.1) |
| (5.7) | `P_x(e) cap P_x(Re) = empty` a.e. | Corollary 5.4 |
| (PB) | `1 <= |P_x(e)| <= k-3` a.e. At `k = 5` this is Prop 5.6; at `k = 6` the same proof gives `<= 3` (a 4-set in the palette forces a binary centre on a positive-measure arc, and Lemma 5.5 forbids a non-discrete family of those) | Prop 5.6 |
| (E) | `P_x(e) not<= {j,j+1}` for every edge `j` of the cycle | Lemma 6.2, (6.2) |
| (SA) | if `x` is typical of colour `i` then `i notin P_x(e)` a.e. | Lemma 1 below |
| (5.2) | `c(x+u+v) notin P_x(u) cup P_x(v)` for a.e. independent-angle pair `(u,v)` | Lemma 5.2(1) |

`(S14)` above means Lemma 8.1; the label is only a shorthand. **What (5.2) does and does
not give.** (5.2) holds for almost every *pair* `(u,v) in S x S`, so it can be applied to
products of positive-measure sets of directions, but **not** to the six orbit positions of
one base direction: those form a one-dimensional family, a null subset of `S x S`, and
Fubini does not reach it. The rigorous consequences are therefore:

  (5.2i) for `A, B subset [k]` with `A cup B = [k]`, the two direction sets
         `{u : P_x(u) = A}` and `{v : P_x(v) = B}` cannot both have positive measure
         (otherwise `c(x+u+v) notin [k]` on a positive-measure product). Given (SA) every
         palette lies in the five-element set `[k] - {i}`, and two subsets of a five-element
         set cannot have union `[k]`, so **at a typical centre (5.2i) is automatic**;
  (5.2ii) if `A cup B = [k] - {i}` occurs on a product of arcs `U x V`, then
         `c = i` a.e. on `x + U + V`; if in addition the interior of `U + V` meets the
         circle of radius one about `x`, that gives two density-one points of colour `i` at
         distance one, contradicting Lemma 4.3. This is a geometric condition on the two
         arcs (the unit circle is met exactly at angular separation `2pi/3`), not a
         cell-combinatorial one; it is checked separately in §6.

Consequently the per-cell system decided in §3 uses exactly five families,
**(S14), (5.7), (PB), (E), (SA)** — the paper's palette axioms plus self-avoidance — and
(5.2) is handled outside it.

**(SA) Lemma 1** (this is Lemma 1 of `sprint/k6/STRUCTURE.md`; reproduced because it is
load-bearing). Let `x` be typical with `c(x) = i`. Then `sigma({e : i in P_x(e)}) = 0`.
*Proof.* Suppose `D = {e : i in P_x(e)}` has positive measure and let `e_0` be a density
point of `D`. Lemma 5.2(2) says the spatial density of `A_i` at `x + e_0 + v` is zero for
every unit `v` nonparallel to `e_0`. Put `v(delta) = -e_0 + delta` for `delta` on the
circle `C` of radius one about `e_0`; then `x + e_0 + v(delta) = x + delta`, and
`v(delta)` is parallel to `e_0` only for `delta in {0, 2e_0}`. The non-density-one points
of `A_i` form a plane-null set, so Fubini gives `sigma(C cap N) = 0`; hence for a.e.
`delta in C` the point `x + delta` is a density-one point of `A_i`. Choose such a
`delta` outside `{0, 2e_0}`: density zero and density one at the same point. `square`

Note the paper's constant-sequence trace only gives `c(x+e) in P_x(e)`, the colour of the
*other* endpoint; (SA) is the statement for the centre itself, and it is what the
countermodels of Theorem C fail.

---

## 1. Theorem 1 (the antipodal law)

Fix a cyclic centre `x` with cycle `0,1,...,ell-1`. Let `B` be the finite set of
directions perpendicular to some `v_j`. Then for every `e` with
`e, Re, ..., R^5 e` outside `B`,

  `sigma_j(R^{p+3} e) = -sigma_j(R^p e)` for every `j < ell` and `p`,
  i.e. `S_{p+3} = [ell] \ S_p`, and consequently `(O, I)_{p+3} = (I, O)_p`.

*Proof.* `sigma_j(e) = sign(e . v_j)`, so `sigma_j` is `+1` exactly on the open
semicircle `I_j = {e : e . v_j > 0}`. The six directions `R^p e` are equally spaced, so
`R^{p+3}e` is the antipode of `R^p e`; an open semicircle contains exactly one point of
any antipodal pair, hence `R^{p+3}e in I_j` iff `R^p e notin I_j`. Reading off
`O(e) = [k] \ (union of the positive edges' endpoints)` gives the second claim, because
complementing every sign replaces "positive endpoints" by "negative endpoints". `square`

The paper uses two instances of this without stating it: `S_{p+3} = S_p^c` at `ell = 5`
("reversing every sign interchanges the two allowed sets and preserves these options",
§8.2) and "splitting is antipodally invariant" at `ell = 4` (Lemma 8.3). Theorem 1 is the
general statement, and it is what makes the decision finite: the orbit tuple
`(S_0, ..., S_5)` is determined by `(S_0, S_1, S_2)`.

Verified numerically against explicit exact configurations in §9 step 3: 70848 checks, no
exception.

---

## 2. Theorem 2 (the §8 orbit analysis is an explicit finite CSP)

Write `q` for the direction angle of `e` in units of `pi`, so that the `p`-th orbit
position has angle `pi(q + p/3)`. For a ray `v_j` (angle `pi r_j`) define

  `P_j(q) = {p in Z/6 : q + p/3 in (r_j - 1/2, r_j + 1/2) mod 2}`.

Then:

1. **(row form)** `j in S_p` iff `p in P_j(q)`.
2. **(row shape)** for a.e. `q`, `P_j(q)` is a cyclically consecutive triple
   `{m-1, m, m+1}` of `Z/6`. (The arc `I_j` has angular length `pi`, exactly half a
   turn, and the six orbit directions form a regular hexagon, i.e. three antipodal
   pairs; an open half-circle contains exactly one point of each antipodal pair.)
3. **(achievability)** conversely *every* prescription of a consecutive triple to each ray
   is realised by some configuration: choose `r_j` in the corresponding cell.
   So the achievable orbit sign tuples are exactly the `6^ell` tuples
   `S_p = {j : p in P_j}`.
4. **(cells and slippage)** the sign tuple is constant on the cells of the arrangement of
   the `<= 6 ell` critical directions `q = r_j - p/3 +- 1/2`; as `q` increases, exactly one
   *class* of rays slips at a time, each slipping ray's triple advancing by one, and two
   rays slip together exactly when `r_i = r_j mod (1/3)` (their directions differ by a
   multiple of `pi/3`). Over `q in [0,2pi)` each ray slips six times and every index
   returns. There are at least two cells.

So a configuration is exactly (a weak cyclic order of the residues `r_j mod (1/3)`, and
the triple assigned to each ray in one cell), and — this is the point — the palette system
has to be satisfiable **in every cell**, because (S14), (5.7), (PB), (E) and (SA) all
hold for a.e. `e`, hence simultaneously a.e. in every cell, while `O` and `I`
are cell-constant. ((5.2) is not of this form; see §0 and §6b.)

Consequently: *a weak measurable `k`-colouring has a cyclic centre with a cycle of length
`ell` only if some configuration has every cell of its cycle satisfiable.*

Parts 1-4 were verified against exact rational ray configurations, independently of the
row abstraction: 400 configurations for part 1 and the antipodal law (0 mismatches,
70848 antipodal-law checks) and 11408 cell transitions for part 4, every one with each
differing ray advancing by exactly one (up to 4 rays slipped together). See §9 step 3.

---

## 3. The decision, and the exact ledger

The decision per cell is the following system on six palettes `P_0, ..., P_5`, with
`[k] = {0,...,k-1}`, and `i` the centre's colour:

    P_p cap O_p != empty,  P_p cap I_p != empty                    (S14)
    P_p cap P_{p+1} = empty,  indices mod 6                        (5.7)
    1 <= |P_p| <= k-3                                              (PB)
    P_p not a subset of any edge of the cycle                      (E)
    i notin P_p                                                    (SA)

These are the only families used. As explained in §0, (5.2) cannot be applied to the
one-parameter orbit family; its rigorous form (5.2i) is automatic given (SA), and (5.2ii)
is checked separately in §6. In particular the six palettes of an orbit are *not* required
to have pairwise non-covering unions — that requirement is not available, and the entries
of Table B below are correspondingly the honest ones. (Recorded for comparison: imposing
the unavailable constraints anyway changes nothing at `k = 6` — the counts in Table B for
`ell = 6` are identical — and changes nothing at `ell = 5`, `k = 5` either. But the
rigorous computation does not rely on it.)

Theorem 1 gives `(O,I)_{p+3} = (I,O)_p`, and (S14) is symmetric in `O` and `I`, so the
domain at position `p+3` equals the domain at `p`; the six-position system is therefore a
six-cycle with three repeated domains, decided exactly by a transfer computation.

**Table A — `ell = 5`, `k = 5` (calibration: this must be UNSAT).**

| cycle length | achievable tuples | excluded by (S14) alone | excluded by the palette system | satisfiable |
|---|---|---|---|---|
| 5 | 7776 | 7386 | 390 | **0** |

Hence no configuration has a satisfiable cell at all, so `ell = 5` is impossible at
`k = 5`. This is the paper's Proposition 8.2, obtained **without** the sign/run counting
of §8.2 and without the palette-index parity analysis: the only ingredients are Lemma 8.1
and the palette axioms. Two independent procedures agree (§9).

**Table B — `k = 6`, all four cycle lengths.**

| `ell` | achievable tuples | admissible under (S14)`^1` | satisfiable for some label | satisfiable (label, tuple) pairs | surviving configurations`^2` |
|---|---|---|---|---|---|
| 3 | 216 | 216 | 216 | 216 for each of the six labels | 16848 |
| 4 | 1296 | 1296 | 1296 | 1296 for labels 0-3, 84 for labels 4 and 5 | 390936 |
| 5 | 7776 | 7776 | 1350 | 576 for labels 0-4, 0 for label 5 | 268200 |
| 6 | 46656 | 6234 | 90 | 18 for each of the six labels | 252 |

`^1` Lemma 8.1 alone kills 40422 of the 46656 tuples at `ell = 6` (every tuple has
`O(e) = empty` or `I(e) = empty` for some `e`) and none at `ell <= 5` (there the
outsiders keep both sets nonempty). `^2`"surviving configuration" counts the triples
(centre colour, cell in which the walk starts, weak slip order) whose **whole** closed
cell cycle is satisfiable; the enumeration is exhaustive over the weak linear orders of
the slippages (`4683` for six rays, `541` for five, `75` for four, `13` for three).

For `ell = 6` the 252 survivors are, in slip-block form:

| slip blocks | count |
|---|---|
| `((0,1,2,3,4,5),)` — all six rays slipping together | 108 |
| `((0,1,3),(2,4,5))` | 24 |
| `((0,3,5),(1,2,4))` | 24 |
| `((0,1,4),(2,3,5))` | 24 |
| `((0,3,4),(1,2,5))` | 24 |
| `((0,2,3),(1,4,5))` | 24 |
| `((0,2,5),(1,3,4))` | 24 |

---

## 4. Theorem 3 (main result): the §8 angular layer cannot exclude any cycle length at `k = 6`)

Fix `k = 6` and `ell in {3,4,5,6}`. There exist

* a configuration of `ell` limiting directions `v_0, ..., v_{ell-1}`,
* a label `i` (the centre's colour), and
* a measurable palette field `e |-> P_x(e)` on the direction circle,

such that (S14), (5.7), (PB), (E) and (SA) hold in every cell of the sign arrangement of
the configuration — and, moreover, such that the palette field also satisfies the rigorous
form (5.2ii): for every pair of cells whose palettes have union `[k] - {i}`, the sum of the
two arcs avoids the unit circle (so `c = i` is never forced onto a point at distance one
from `x`). Hence the full rigorous §8 layer at `k = 6` — palette axioms, self-avoidance, and
(5.2) in its open-set form — is satisfiable at a cyclic centre of every cycle length. The
counts of such configurations are those of Table B: `16848`, `390936`, `268200` and `252`
respectively.

In particular, no proof of the impossibility of a `6`-cycle (or of a `3`-, `4`- or
`5`-cycle) at six colours can use only the pointwise palette hypotheses of §8 plus
self-avoidance and the open-set form of (5.2).

**Consequences for the programme.**

1. `sprint/k6/REPORT.md` §5 identifies self-avoidance as "the first concrete
   colouring-level constraint that removes [the countermodels]". Theorem 3 says it does
   not remove them at the level of §8: the surviving configurations satisfy (SA) at a
   typical centre. So the `k = 6` interface is not closed by strengthening the palette
   axioms.
2. Direction 1 of the sprint asks whether a free-label palette field at a six-cycle centre
   can satisfy (5.7) and the exact transport shifts. At the *exact* §8 hypotheses the
   answer is **yes**, and the witnesses are of a very specific shape: the slippage
   structure is degenerate (six rays, or two triples, of directions congruent mod
   `pi/3`), and 40422 of the 46656 tuples are already killed by Lemma 8.1 alone. So the
   six-cycle is *almost* excluded pointwise; the remaining slack is exactly the freedom to
   put the rays at `60`-degree commensurate directions.
3. What is missing is genuinely colouring-level and *not* pointwise: it must use the open
   sets supplied by Lemma 8.1. §6 shows that even that layer is powerless on the
   survivors.

### 4.1 The triangle at `k = 6` (the coordinator's question for `ell = 3`)

The §8.4 mechanism is: at every `e`, two of the three edge signs agree, those two edges
cover all three triangle labels, so the one-sided strip uses only the outsiders; the paper
then concludes "there cannot be two outsiders in such a palette, since (5.7) would leave
no outsider at `Re`", obtaining a *binary* state `s(e) in {X,Y}` with `s(Re) != s(e)`, and
Lemma 8.6 turns that into local constancy and then into the sector structure of Lemma 8.7.
At `k = 6` there are **three** outsiders `X, Y, Z`, and the step fails exactly as stated:
if `P_x(e) supseteq {X,Y}` then (5.7) forces `P_x(Re)` to avoid `X` and `Y`, and (S14)
only requires it to meet the outsiders, which `Z` does. There is no contradiction, so no
binary state is forced. The correct replacement is a three-valued state
`s(e) = P_x(e) cap {X,Y,Z} != empty` with `s(e) cap s(Re) = empty`, whose admissible
value set has six elements; and this is precisely what Table B records: at `ell = 3` and
`k = 6` **every** one of the 216 achievable sign tuples is satisfiable, so the pointwise
layer constrains nothing at all there.

It follows that the Moser endgame cannot run either, for a clean reason independent of any
computation. For `0 < |z| < 2` the equation `z = u + v` with `|u| = |v| = 1` has exactly
two solutions `u = z/2 +- s`, `v = z/2 -+ s` with `s` perpendicular to `z` and
`|s|^2 = 1 - |z|^2/4`. So Lemma 5.2(1) at the single centre `x` can exclude at most the
labels of two palettes at `x+z`; with three outsiders and palettes of size at most three
this does not confine `x+z` to the three triangle labels, and the conclusion of Lemma 8.8
("a neighbourhood of `x+z` uses only the three triangle labels") is unavailable. The
paper's endgame then needs a proper colouring of the Moser graph in four labels; the Moser
spindle is `3`-chromatic-critical and `4`-colourable, so the argument would have to place
a `5`-chromatic unit-distance graph in the region `(8.4)` instead. (This is the precise
content of "the endgame fails at `k = 6`" and matches `sprint/k6/REPORT.md` Theorem C.)

---

## 5. Corollary: Proposition 8.2 by a purely combinatorial route

Table A gives a second, independent proof of the paper's Proposition 8.2. The paper's
proof analyses runs of signs on five edges and then a palette-index walk modulo five. The
route here is: (Theorem 1) the orbit tuple is determined by `(S_0,S_1,S_2)` with
`S_{p+3} = S_p^c`; (Theorem 2) every consecutive triple is achievable; (Table A)
exhaustive decision over the `6^5 = 7776` tuples gives no satisfiable tuple at all, and it
does so **without self-avoidance** (`python3 -c "import rigorous;
rigorous.analyse(5,5,2,use_sa=False)"` reports `{'L81': 7386, 'CSP': 390}`, zero
satisfiable tuples). So this instance uses only Lemma 8.1, Corollary 5.4, the palette
bound and Lemma 6.2 — all printed in the paper. No run structure, no parity of indices, no
"reversing every sign" case split.

I record this as a calibration, not as an improvement: the paper's proof is shorter. What
it establishes is that the decision procedure of §3 reproduces a known UNSAT at `k = 5`
and a known SAT-free answer, so its SAT answers at `k = 6` are not an artefact of a
mis-encoded hypothesis.

---

## 6. The open-set (strip) layer is powerless on the survivors

Lemma 8.1 gives more than (S14): on an angular neighbourhood of `e`, the open strip just
outside radius one *uses only* `O(e)` up to null sets, and the inner strip uses only
`I(e)`. Two elementary consequences:

* **(MS, monochromatic strips)** if `O(e) = {c}` on an arc of angular width `> pi/3`, then
  that strip is essentially monochromatic of colour `c`; two points of it at equal radius
  `r < 1` are at distance one exactly when their angular separation is
  `2 arcsin(1/(2r))`, which tends to `pi/3` from above as `r -> 1`; so the strip contains
  two `c`-coloured points at distance one, contradicting properness of density-one points.
  The same holds for `I` and the inner strip.
* **(unit pairs)** an open strip whose angular width is at most `pi/3` contains **no** two
  points at distance one at all (at radius `r <= 1` the distance is `2r sin(theta/2) <= 1`
  with equality only at `r = 1`, `theta = pi/3`, excluded by openness). So on such an arc
  the strip information is no stronger than the palette information.

Both were checked on all 252 survivors of `ell = 6`, using exact rational ray
reconstructions of the surviving cell sets: **none** has an arc of width `> pi/3` with a
singleton `O` or `I`, so (MS) never fires; the arc widths occurring are `pi/9`
(`864` arcs), `2pi/9` (`864`) and `pi/3` (`648`), so no surviving strip contains a unit
pair. The threshold is sharp and attained: `144` of the `648` arcs of width exactly
`pi/3` do carry a singleton allowed set, and for those the monochromatic strip is exactly
`pi/3` wide, which still contains no unit pair because equality in
`2r sin(theta/2) = 1` needs `r = 1` and `theta = pi/3`, both excluded by openness.

So the §8 angular layer — palette axioms, self-avoidance, and the open-strip
restrictions — is powerless at six colours for every cycle length. Adding the last
rigorous piece of (5.2) does not change this:

**6b. The open-set form of (5.2).** (5.2ii) is a constraint on pairs of cells: if `D, D'`
carry palettes `A, B` with `A cup B = [k] - {i}` and some pair `(u,v) in D x D'` has
`|u+v| = 1`, then `c = i` is forced on a region meeting the unit circle about `x`, which
Lemma 4.3 forbids. For two arcs of directions `(a,b)` and `(a',b')` in units of `pi`, the
achievable separations are the interval `(a'-b, b'-a)`, and `|u+v| = 1` exactly at
separation `+-2/3`. So the question is a small CSP on the `~12` cells: assign to each cell
an admissible palette so that no *unit-capable* pair receives palettes with union
`[k] - {i}`.

Checked exactly (`work/openset.py`): **all 252** `ell = 6` survivors admit such an
assignment (exhaustive), and random samples of `300` of the `16848` `ell = 3` survivors,
`200` of the `390936` `ell = 4` survivors and `200` of the `268200` `ell = 5` survivors all
admit one (0 failures in each sample). So Theorem 3 is not affected by (5.2).

---

## 7. What is and is not claimed

**Claimed.** Theorems 1-3 and Tables A and B, exactly as stated: the pointwise §8 system
at `k = 6` — (S14), (5.7), (PB), (E) and self-avoidance — is satisfiable for each
`ell in {3,4,5,6}` in every cell of an explicit configuration, and the resulting fields
also admit the open-set form (5.2ii) of (5.2); the paper's Proposition 8.2 follows from the
same procedure from printed hypotheses alone; the strip layer is powerless on the
survivors.

**Not claimed.** Nothing here says anything about local finiteness at `k = 6`, about
`(W)`, or about `chi(R^2)`. Theorem 3 is a *negative* result about a method: it says that
the §8 layer, however strengthened by palette axioms and self-avoidance, cannot exclude a
cycle length at six colours. It does not say that cyclic centres with six-cycles exist —
indeed the survivors of Table B need the slippage structure to be degenerate (directions
congruent mod `pi/3`), and whether such a ray configuration can arise from Proposition
7.1's continua is not addressed here. In particular the survivors all require at least
one collision of slip classes; **no configuration whose six slippage classes are all
distinct survives** (the exhaustive enumeration of Table B shows this), so the six-cycle
is excluded pointwise as soon as no two limiting directions are congruent mod `pi/3`.

One further observation from Table B: at an `ell = 5` cyclic centre at `k = 6` the centre's
colour cannot be the unique outsider `5` — for label `5` no tuple is satisfiable. (Reason:
the outsider lies in `O(e) cap I(e)` for every `e`, so avoiding it costs nothing, yet the
palette must also meet the part of `O` or `I` that depends on the signs; the exhaustive
enumeration shows the two demands cannot be met in every cell simultaneously.) This is a
genuine `k = 6` constraint but it does not exclude `ell = 5`.

---

## 8. Files

| file | content |
|---|---|
| `work/s8.py` | signs, allowed sets, palette domains, small CSP |
| `work/rows.py` | the row-interval model; achievable tuples |
| `work/orbit.py` | the six-position orbit system as a transfer computation |
| `work/rigorous.py` | the rigorous per-cell system (S14), (5.7), (PB), (E), (SA) and the closed-cell-walk test |
| `work/openset.py` | the open-set form (5.2ii) of (5.2): the cell CSP |
| `work/walk.py`, `work/decision.py` | the earlier run that additionally imposed the unavailable union/monochromatic-sum constraints; the counts are unchanged |
| `work/independent.py` | procedure B: explicit rational rays, brute-force palettes |
| `work/strips.py` | ray reconstruction from a cell; arc widths; (MS) test |
| `work/check.py` | the two-procedure cross-check |

## 9. Exact commands

All commands run from `.ultramath/smwfwi7rh/m6/work` with plain `python3` (standard
library only). Total run time a few minutes.

```
# 1. calibration: ell = 5 at k = 5 must have no satisfiable tuple  (Table A)
python3 -c "import rigorous; rigorous.walk(5,5,2,True)"
python3 -c "import rigorous; rigorous.analyse(5,5,2,use_sa=False)"

# 2. the ledger of Table B at k = 6
python3 -c "import rigorous; rigorous.walk(3,6,3,True)"
python3 -c "import rigorous; rigorous.walk(4,6,3,True)"
python3 -c "import rigorous; rigorous.walk(5,6,3,True)"
python3 -c "import rigorous; rigorous.walk(6,6,3,True)"

# 3. exact verification of the geometry (row model, antipodal law, slippage)
python3 geomcheck.py

# 4. two-procedure cross-check (procedure A vs procedure B, cell by cell)
python3 -c "import check; check.verify(6,6,3,nrandom=100)"
python3 -c "import check; check.verify(5,5,2,nrandom=80)"

# 5. arc widths and the (MS) test on the ell = 6 survivors
python3 -c "import strips; strips.check()"

# 6. the open-set form (5.2ii) of (5.2)
python3 -c "import openset; openset.main(6,6,3)"
```

Recorded outputs. Step 1: `{'L81': 7386, 'CSP': 390}` and **0** satisfiable tuples, 0
surviving configurations, with and without self-avoidance. Step 2: the "satisfiable tuples
/ surviving configurations" columns of Table B (`ell = 3`: `{'OK': 1296}`, 16848; `ell = 4`:
1296 for labels 0-3 and 84 for labels 4,5, 390936; `ell = 5`: 576 for labels 0-4 and 0 for
label 5, 268200; `ell = 6`: 18 per label, 252). Step 3 (`geomcheck.py`):
`configurations checked : 400`, `row-model mismatches : 0`, `row sizes observed : [3]`,
`antipodal law ok / bad : 70848 / 0`, `cell transitions checked / bad : 11408 / 0`.
Step 4: for `(6,6)`, "A survivors 252, B rejects a cell of 0 survivors, 0 cell-set
mismatches of 40 inspected, 0 of 100 random configurations with every cell satisfiable";
for `(5,5)`, "A survivors 0, 0 disagreements, 0 of 80 random configurations". Step 5:
252 survivors, 0 with a monochromatic strip of width `> pi/3`, arc widths
`{pi/9: 864, 2pi/9: 864, pi/3: 648}`, and `144` of the `648` arcs of width `pi/3` carry a
singleton allowed set. Step 6: `survivors with no admissible assignment for the open-set
(5.2): 0`.

Two independent procedures. Procedure A is the row-interval model with a bitset
transfer/backtracking decision (`rows.py`, `orbit.py`, `rigorous.py`); procedure B rebuilds
explicit exact rational ray configurations from the same combinatorial data, recomputes
the cells from the circle geometry, and decides palette existence by a plain recursive
search over Python sets with a different constraint order (`independent.py`, `check.py`).
`check.py` verifies that A's 252 survivors are accepted by B cell by cell and that the
geometric cell set of the reconstruction equals the walk's cell set; both procedures also
agree that no configuration survives at `ell = 5`, `k = 5`. The two procedures use the
same five constraint families; `check.py`'s solver checks (5.7) and the (5.2)-style union
conditions in a different order and with sets rather than bit masks.
