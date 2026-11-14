# Sprint B — §7 at six colours: working report

**The harness was stopped after the outage** — no swarm is running, and the pending submissions
(m11 frozen-core radii, m13 sector threshold; m2 §8 ell=5, m3 on `A`) were checked by hand and are
recorded in [STATUS.md](sprint/k6/STATUS.md) with the commands that reproduce them.

**Deliverable.** A conditional theorem that makes §7 of the five-colour proof available at
`k = 6`; a proof that the missing hypothesis is *not* the existence of a cyclic centre; explicit
countermodels showing that the missing hypothesis cannot be obtained from the palette-level
hypotheses at all, for every cycle length; and a colouring-level constraint (self-avoidance)
that kills the countermodels and marks the exact frontier. The three deliverables requested by
the brief are all present: a theorem (Sections 2 and 3), a counterexample (Section 4), and
decided finite computations (Sections 6 and 7, with two independent procedures each).

**Headline.** `chi(R^2)` is still 6 or 7; nothing here settles it. What is settled is the
`k = 6` interface: §7 is free at any isolated cyclic centre, the only hypothesis it needs is
`(W)` (finite `L` in one ball of radius `> 1`), **and the §8 elimination that must follow it is
not available at `k = 6` from any formalised layer** — palette, two-centre, strip and the §8
orbit system with self-avoidance are all satisfiable (§4d). The phase transition is exact for
*local finiteness*: true at `k = 5`, open at `k = 6`, false for every `k >= 7` (explicit proper
colouring). `(W)` is strictly weaker and is **not refuted at any `k`** — the `k >= 7` example
satisfies it. Even non-proper self-avoidance is consistent with accumulating models at every
cycle length, so only the properness of the colouring remains.

## 0. Where the sprint stands (living section, updated as verdicts are given)

**The transfer.** §7 of the paper is available at six colours under exactly one hypothesis, `(W)`:
some ball of radius `> 1` meets `L = {x : Gamma_x has a cycle}` in finitely many points. §7 is
label-blind; the only changes at `k = 6` are `alpha < 1/6`, `G = K_6` and `ell in {3,4,5,6}`. Four
independent audits; two ingredients of the extraction are machine-checked (the clique-in-a-forest
bound and the cover-obstruction engine — not Lemmas 7.2/7.3/7.7/7.8), and the transfer holds for
every `k >= 3` (§2).

**Non-emptiness is free, and so is tameness.** `L` is closed and `1`-dense, so every
`6`-colouring has a cyclic centre. For a colouring constant on a locally finite partition with
piecewise `C^1` boundaries, `Gamma_x` is *exactly* the interface graph, so `(W)` holds at every
`k`; hence a `k = 6` countermodel must be non-tame (some ball meeting infinitely many cells or
interface arcs). No property of `L` short of finiteness can imply `(W)`: an abstract lattice is
closed, countable and `1`-dense and violates it. But `(W)` is **not known to fail for any
colouring at any `k`**: `m3`'s `k >= 7` colouring, whose `L` is closed and countable with one
accumulation point, *satisfies* `(W)` — a ball of radius `3/2` centred more than `2` away from the
accumulation point meets only the lattice `V`, hence finitely many points (`smwfycxze` m1
Prop. 7).

**The phase transition.** Local finiteness of `L` is true at `k = 5` (the paper, machine-checked),
**open at `k = 6`**, and false at every `k >= 7` (explicit proper measurable colouring). The
gadget's resource at the accumulating point is `k - 3` colours on the unit circle, and its label
cost is exactly `ell + 3`; at `k = 6` the budget is met with zero slack. That failure is a failure
of *local finiteness* only: `(W)` is strictly weaker and survives it, so the table below must be
read as a table about local finiteness, not about `(W)`.

**The singleton class `S_1`.** In `S_1` (a.e.-singleton palettes; contains every piecewise-`C^1`
cell colouring and the `k >= 7` countermodel) the whole structure is two lines: the essential
range of the palette function meets no edge of `Gamma_x`, and it has at least two values, so
`Gamma_x <= K_{k-2}` at every `k`. At `k = 6` that gives `ell in {3,4}` only, the 4-cycle locus is
binary hence locally finite (Lemma 5.5), and a triangle centre is either binary (locally finite)
or genuinely 3-valued with `Gamma_x = K_3` exactly. So **(W) in `S_1` at `k = 6` is exactly local
finiteness of the 3-valued triangle locus** — and no `(5.2)`-density argument can reach that
locus, which confines the palette to three labels while those arguments need four or five.

**Every formalised layer of the paper's §6–§8 machinery is satisfiable at `k = 6`** (§4d):
single-centre palette (only `K_6` excluded among `2^15` graphs), finite two-centre (equivalent to
finite unit-distance colouring), the strip layer (SAT for every `k >= 6` and every `ell`), and the
§8 orbit system *with self-avoidance* (SAT for every `ell`, `16848 / 390936 / 268200 / 252`
surviving configurations, with the `k = 5` calibration returning `0`).

**Why.** The `k = 5` proof converts a palette bound into geometry through Lemma 5.5, which is a
*two-valued* selection theorem; at `k = 6` there are three values and the expanding-action step has
nothing to act on (§5c). Hence every surviving structure is three-valued: three outsiders at a
triangle, the `T`-spread part of a 3-hitting centre, `m13`'s singleton field. And there is a
structural reason why no computation over the palette axioms could have done better: direction-wise
constraints have no locality content, `(T)`, `(SA)`, `(5.2)` and `(5.7)` are satisfiable at every
countable set of centres, and the only axiom through which countably many centres can bite is the
two-centre transport, which is `chi(R^2) <= 6` (§4e, the locality barrier).

**The only colouring-level condition left is the one equivalent to the problem.** `(T) + (5.7)`
holds iff `chi(R^2) <= k` (two independent proofs), and given the point-field identity the palette
axioms collapse to `(5.7)` alone. So no palette axiom can prove `(W)` at `k = 6` without proving
`chi(R^2) >= 7`.

**Open — two inputs, not one.** (i) `(W)` at `k = 6`, in two shapes: (a) separation of `T`-hitting
centres for `|T| = 3`, which gives `|P| <= 2`; (b) local finiteness of the 3-valued triangle locus
(equivalently, exclusion of the `T`-spread part at a cyclic centre of a proper 6-colouring).
(ii) An exclusion of the §7 exclusion continua at `k = 6` that is not the printed pointwise one.
What this swarm settled is that both are out of reach from the palette side, and in a sharp sense:

* no countable-centre evaluation of the palette axioms can yield a contradiction — direction-wise
  constraints have no locality content, `(T)`, `(SA)`, `(5.2)`, `(5.7)` are satisfiable at every
  countable set of centres, and the only axiom that can bite is `(TE)`, i.e. `chi(R^2) <= 6` (§4e);
* the accumulated triangle-locus system is itself **satisfiable**, both branches realised in exact
  arithmetic (`smwg1r9lg` m6 Thm 3), so "accumulate at the triangle locus" is not a route to a
  contradiction either;
* circling out at the colouring level: circle-fibre hypotheses control the plane only through an
  absolutely continuous weight (`E_O` is not conull in any ball of radius `> 1`, and nothing follows
  for smaller balls), which is the quantitative reason the programme has no grip (§4f).

`chi(R^2) in {6,7}` stands; nothing in this sprint bounds `chi(R^2)` in either direction.

**Harness.** Ultramath was switched off after the outage, so no swarm is running; the pending
submissions were adjudicated by running their own verifiers ([STATUS.md](sprint/k6/STATUS.md) has
the commands, exit statuses and what was not checked).

---

## 1. The question, and what was known

The paper proves `chi(R^2) >= 6` by showing that a weak measurable 5-colouring leads to a
contradiction. Its geometric part has three stages:

* Theorem 6.5: the cyclic locus `L = {x : Gamma_x contains a cycle}` is locally finite;
* Proposition 7.1 / §7: a cyclic centre yields a cycle of compact connected common exclusion
  continua `K_j`, with sliver data (`ell in {3,4,5}`);
* §8: no such cycle exists, for `ell = 3, 4, 5`.

At `k = 6` the last stage is a separate problem, but the first stage is the gate: without a
cyclic centre there is nothing for §7 to extract. The brief's question was whether local
finiteness is true at `k = 6`. The results below answer the *structural* part of that question
and leave the *colouring-level* part open, with a sharp frontier.

## 2. Theorem A: §7 is available at six colours modulo one isolated point

**Theorem A.** Let `c` be a weak measurable 6-colouring and suppose

  **(W)** there are `y in R^2` and `R > 1` with `L cap B(y,R)` finite.

Then Proposition 7.1 holds at `k = 6`: there are `ell in {3,4,5,6}`, distinct labels
`i_0,...,i_{ell-1}`, a centre `x`, a radius `rho > 0`, and for every edge `i_j i_{j+1}` a compact
connected set `K_j` with

1. `x in K_j` and `K_j cap partial B(x,rho) != empty`;
2. `q_{j,m} -> x` along `K_j` with `(q_{j,m}-x)/|q_{j,m}-x| -> v_j`;
3. `H_{i_j} cap Delta(K_j) = H_{i_{j+1}} cap Delta(K_j) = empty`.

The same holds under the (stronger, square-shaped) hypothesis

  **(F)** some closed square of side `> 2` meets `L` in finitely many points.

Neither hypothesis asks for an *isolated* point with a large gap: finitely many cyclic centres
inside one ball of radius `> 1` are allowed, and only one of them is used. The constant `R > 1`
is sharp for the printed argument (the component-cover mesh is `1 + o(1)`).

**The same holds for every `k >= 3`, with a shorter hypothesis list (`smwg1r9lg` m3, accepted).**
The transfer does not use the palette bound at all: §7's dependency list is Definition 1.2, the
*definition* (6.1), `(W)`, and Brouwer's theorem. Not `(5.2)`, `(5.3)`, `(5.7)`, `(5.12)`, `(6.2)`,
`(6.3)`, Lemma 4.3 or Lemma 5.5. `k` occurs in §7 in exactly three places — `alpha < 1/k` in (7.4),
`G = K_k`, and the cycle range `{3,...,k}` — so `(P)` is a redundant hypothesis of the statement
above and the theorem holds for every weak measurable `k`-colouring with `ell in {3,...,k}`. (That
`(6.3)` is not used is a correction to `[TRANSFER.md](TRANSFER.md)`'s audit table, which attributed
it to Lemma 7.3; the printed proof of Lemma 7.3 uses `D_ij(B,h)/|h| -> 0` from the negation of
(6.1) and no circle average. The dependency list gets *smaller*, which is worth having: §7 needs no
spectral input at any `k`.)

**Trust grades on the constant `R > 1`.** The sharp form rests on a cover obstruction at the exact
constant — *inradius `>` mesh* — not on the printed Lemma 7.5, which is the side-ten/mesh-two case
and reaches only inradius `> 2`. Two independent proofs of the sharpened form now exist
(`smwfo9zkl` m5: `s <= 2m` for squares; `smwg1r9lg` m3 Lemma C: arbitrary compact convex `Q` with
inradius `> m`, via a two-segment Brouwer argument), and m3's Lemma S shows the threshold cannot be
improved up to `eta`: for every `eta > 0` the closed unit disk has a multiplicity-at-most-two
relatively open cover of mesh `<= 1 + eta` (13 sets, exact diameter check). Three grades must not be
conflated:

| statement | grade |
|---|---|
| §7 is label-blind; the only `k`-dependence is `alpha < 1/k`, `G = K_k`, `ell <= k` | paper-level, audited twice, text-checked |
| transfer under `(W)` with `R > 1` | paper-level, via the sharpened cover lemma (two proofs) |
| transfer under `(W)` with `R > 5` (a ball of radius 5) | **machine-checked** — `graph_map_large_positive_generic` works on `Metric.closedBall 0 5` with mesh `2`, resting on `PlanarCover.compact_open_cover_impossible` whose hypothesis is `Metric.ball 0 5 ⊆ Q` and `‖x-y‖ <= 2` |
| `R > 1` itself, and the side-`>2` square form | **not** machine-checked: the formalised cover obstruction is the printed slack one |
| `R = 1` is insufficient for the *conclusion* | **open** |

So a formal proof of the sharp constant is a bounded, well-posed task: formalise Lemma C (it needs
Brouwer on a compact convex set, which the existing development already invokes in the
ball-of-radius-5 form). Also note: as literally written, the proof above runs §7 on a square of
side ten, whose circumradius is `5 sqrt 2`; the hypothesis it consumes that way is
`L cap B(y, 5 sqrt 2)` finite, and the route from `R > 1` goes through Lemma C on a disk of radius
`R' in (1,R)` — not through the side-ten square. The `(F)` form ("a closed square of side `> 2`")
is legitimate only because a square of side `> 2` has inradius `> 1`.

**Proof.** The paper's §7, line by line. The only changes are `alpha < 1/6` (the denominator of
(7.4) is `sum (p_i - alpha)_+ >= 1 - 6 alpha > 0`), the graph `G = K_6` instead of `K_5`, and
`ell in {3,4,5,6}` instead of `{3,4,5}`. `m2`'s audit confirms that `alpha < 1/6` is *exactly*
optimal for the printed argument — the bound is `1 - k alpha` and it vanishes at `alpha = 1/6` —
and sharpens the scale-invariant cover lemma to "a compact convex region of inradius greater than
the mesh admits no relatively open cover of multiplicity at most two", i.e. the disk form is what
`(W)` with `R > 1` uses. Everything else is label-blind:

* Lemma 7.2 and Lemma 7.3 use only Definition 1.2, Lemma 4.3, Definition 6.1 and the Fourier
  decay (6.3) of circle measure;
* the passage of the thresholded averages (7.4) into the one-skeleton is Lemma 7.4's
  "clique in a forest" argument: a clique in a forest has at most two vertices, for every `k`;
  **no palette bound is used anywhere in §7**;
* Lemma 7.5 (cover obstruction), Lemma 7.7 (reduced circuits) and Lemma 7.8 (annular crossing)
  are pure topology on a finite connected simple graph, valid for `K_6`;
* the cover in Lemma 7.6 has multiplicity at most two because a point of the one-skeleton has at
  most two positive barycentric coordinates, for every `k`;
* the only use of `(W)`/`(F)` is in choosing `Q` with `partial Q cap L = empty` and in having a
  finite `L_0 = L cap Q'` so that the core disks have total radius `-> 0` and some core disk
  contains no other point of `L_0`.

Four independent audits agree: `sprint/k6/TRANSFER.md`, `sprint/k6/WEAKEST.md`,
`.ultramath/smwfo9zkl/m12/S7-INPUT.md`, and `.ultramath/smwfo9zkl/m5/K6-CYCLIC-LOCUS.md`
(the last with the sharpened cover lemma `s <= 2m`). What is machine-checked is *two ingredients*
of the extraction plus the `alpha < 1/k` algebra, in `.ultramath/smwfo9zkl/m9/k6_s7_engine.lean`:
the clique-in-a-forest bound (`card_le_two_of_isClique_of_acyclic`, arbitrary label type) and the
cover-obstruction engine (`graph_map_large_positive_generic`), on a ball of radius 5 with mesh 2.
Lemmas 7.2, 7.3, 7.7 and 7.8 are **not** formalised. Reproduce (the recorded one-liner was wrong —
`lean f.lean` writes no `.olean` and Lean does not search the working directory):

```bash
source scripts/env4341.sh
cd .ultramath/smwfo9zkl/m9
lean -o k6_s7_engine.olean k6_s7_engine.lean     # build the import
LEAN_PATH=".:$LEAN_PATH" lean check_engine.lean  # seven declarations, standard axioms
```

**The weakest form.** §7 does not need local finiteness. It needs finiteness of `L` inside one
ball of radius `> 1` (Theorem A), or a square with finite intersection `(F)`. The isolation
radius matters: below `1` the cover obstruction is unavailable. And this cannot be weakened to a
size bound on `L`: `m5` (`smwfwi7rh`) proves that at a non-isolated cyclic centre every annulus
contains another core disk (Theorem 3), that the crossing lemma Lemma 7.8 is **false on a
punctured annulus** (Theorem 3', explicit continuous map with non-null inner word whose midpoint
preimage escapes into the hole), and that there is a closed perfect `1`-dense porous set of zero
upper 1-dimensional Minkowski content on every compact (Theorem 4). So no content, Hausdorff,
porosity or density condition can replace isolation; the printed extraction genuinely needs one
isolated cyclic centre at radius `> 1`. `(F)` implies `(W)` (a side-`>2` square lies in a ball of radius `>1`). The converse can fail
when `R < sqrt 2`: a ball of radius `1.1` need not contain a square of side `> 2`. The ball form
`(W)` is the weakest of the sufficient conditions, and it is what m12's disk version of the cover
lemma gives. A perfect `L` breaks the printed proof: every annulus
around a chosen centre `x` contains another core disk, so Lemma 7.8, which needs a continuous map
on the whole annulus, does not apply. So the exact missing input is: **`L` has an isolated
point**.

## 3. Theorem B: non-emptiness is free; the gap is finiteness

**Theorem B (`m5`/`m12`, sharpened).** For every `k >= 3` and every weak measurable `k`-colouring,
`L` meets every closed square of side `> 2` (`m5`) and every closed disk of radius `> 1` (`m12`).
Hence `L` is `1`-dense: `dist(y,L) <= 1` for every `y`. In particular `L != empty`.

*Proof.* If a disk `D` of radius `R > 1` missed `L`, run Lemma 7.4 with `L_0 = empty` (every
`Gamma_z` is a forest) and Lemma 7.6's cover argument with no core disks. The component cover of
`D` has multiplicity `<= 2` and mesh `1 + o(1)`, contradicting the inradius form of the
scale-invariant cover lemma (a compact convex region of inradius `> m` has no such cover). The
paper records the seed: "This argument also rules out the possibility of having no core disks in
`Q`" (p. 47). The square form `m5` is the same argument with the side-`>2` square version.

So a 6-colouring *does* have a cyclic centre; the missing input is finiteness/isolation. The
example `L = {(x,y) : x in 2 sqrt 2 Z} union {(x,y) : y in 2 sqrt 2 Z}` (a grid of lines with
spacing `2 sqrt 2`) is closed, perfect, `sqrt 2`-dense, and misses a square of side `2.1`: no
density statement implies `(W)`.

## 3b. The k-phase transition: k = 6 is the unique open case

`m3` constructs, for every `k >= 7`, a **genuine proper Lebesgue measurable `k`-colouring** whose
cyclic locus is **not locally finite**. The construction takes the paper's own hexagonal
7-colouring (hexagons of circumradius `2/5`, colour `(m+2n) mod 7`), leaves it unchanged outside a
small square `W` of side `1/100`, puts colour `0` on `W` minus a sequence of tiny disjoint disks
`D_n`, and puts a Mercedes 3-sector partition with labels `{0,2,3}` on each `D_n`. The `D_n`
accumulate at `p_0`; the three sector interfaces make `{0,2},{2,3},{3,0}` all edges of
`Gamma_{q_n}` (the sector strip lemma gives `|D_ij(B,h)|/|h| >= min(rho,s)/8 > 0`), so every
`q_n` is a cyclic centre and `q_n -> p_0`. Properness holds because the annulus
`1 -+ 0.0071` around `p_0` meets no colour-`0,2,3` hexagon of the unmodified colouring (a finite
exact `Q(sqrt3)` certificate, two independent methods), while points of `W` carry only
`{0,2,3}`. At the `q_n` every palette is a **singleton** (the colouring is cell-constant on a
Borel partition with piecewise smooth boundaries, so `P_x(e) = {c(x+e)}` a.e.), the singleton
value runs through four labels `{1,4,5,6}`, and the triangle labels `{0,2,3}` never appear in a
palette. So the cyclic centres are not binary for any pair and Lemma 5.5 cannot apply.

Consequently the printed Theorem 6.5 is not a general-`k` theorem:

| `k` | local finiteness of `L` |
|---|---|
| 5 | true (the paper; machine-checked) |
| 6 | **open** (this sprint) |
| `>= 7` | **false** (`m3`, explicit proper measurable colouring) |

The `k = 6` case is the unique open one, but the reason is **not** a label count: `m4` checked
m3's Lemma C, which needs only **three** prescribed labels absent from the unit-distance shadow of
the small square (not four), and at `k = 6` exactly three are available. So m3's gadget can be
inserted into any proper 6-colouring whose shadow misses three labels; the obstruction is the
existence of the 6-colouring itself — the chromatic wall — not the number of outsiders. What *is*
special at `k = 6` is that the triangle machinery of §8 (which at `k = 5` forces a binary outsider
pair because `k-3 = 2`) has three outsiders instead of two, so the printed §8 exclusions do not
transfer. Any proof of `(W)` at `k = 6` must use `k = 6`-specific structure, not a general-`k`
argument. Files: `.ultramath/smwfo9zkl/m3/proof.md`, `.ultramath/smwfwi7rh/m4/NOTE.md` §5.

**`m4`'s singleton-class reduction.** For a weak measurable 6-colouring in class `S_1` (every
maximal palette a singleton a.e. — this contains every cell-constant colouring with piecewise
`C^1` boundaries, and m3's `k >= 7` example), Theorem 3 of `m4` proves: there is no 5-cycle and no
6-cycle in any `Gamma_x`, and the 4-cycle locus is locally finite (the singleton is an outsider,
(5.7) forces a binary alternation, and Lemma 5.5 separates). Hence `L` is locally finite **iff the
3-cycle locus is**. This is the sharp reduction of `(W)` in `S_1`: the triangle is the only
possible accumulation mechanism. m3 shows it does accumulate at `k >= 7`; at `k = 6` the class
`S_1` is nonempty only if a 6-colouring exists, so the reduction is meaningful inside a
contradiction argument. `m4` also proves Corollary 2: a centre-independent palette field cannot
satisfy (5.3) at unit separation at all (`P(e) cap P(e) = empty`), which is a second, cheaper
kill of all centre-independent countermodels alongside m10's endpoint trace, and shows the shadow
annulus is 3-colourable (exact certificate), so m3's `k = 6` condition has no geometric
obstruction.

**The accumulation is invisible to the per-centre data (`smwg1r9lg` m6, accepted).** Three results
sharpen the `S_1` picture beyond what §3b states.

* *Lemma 1 (the trace, at every good centre).* Call a centre **good** if its unit circle meets the
  plane-null set of non-typical points null-ly; good centres are conull and dense. At every good
  centre the constant sequence is a legitimate trace and `P_x(e) >= {c(x+e)}` a.e. The
  qualification matters: changing `c` on a plane-null set leaves every `P_x` and `Gamma_x` fixed
  while changing the circle values, so **no argument may read information off a single circle** at
  an exceptional centre. The proof is the `L^1` comparison of circles about nearby centres with
  the circle about `x`, plus the density-one/density-zero dichotomy — not an evaluation at `x`
  itself, which is exactly why it survives at every good centre.
* *Theorem 1 (the exact dictionary).* `Z^3(V) = {R_x = O} cap {K_3(V) <= Gamma_x}` at every
  centre, `O = [6] \ V`. The centre's colour **does not enter** — the "`c(x) in V`" clause is not
  available (it came from self-avoidance; see the adjudication below).
* *Theorem 2 (what the accumulation forces).* `x_n in Z^3(V)`, `x_n -> p`: then `Gamma_p >=
  K_3(V)`, `P_p <= O` a.e., the state functions converge in `L^1`, and the limit is either again
  a 3-valued triangle centre — and then it carries all the approximants' data — or a binary
  triangle centre, of which there are only finitely many per ball.
* *Theorem 3 (the accumulated system is satisfiable — a decided negative).* There is an explicit
  exact-arithmetic model of the limit system in which both branches occur. So **no contradiction
  is derivable from the per-centre axioms together with the unit-separation transport**, and the
  "accumulate at the triangle locus" programme is closed as a source of one. This is the
  independent-inputs confirmation of the locality barrier of §4e, seen from the `S_1` side.

**Adjudication: the record's Lemma D.** Its recorded proof is broken (`smwg1r9lg` m6 §5.1, and
this matches an earlier audit): the conull-by-Fubini step only gives that `x+delta` is a density
point of *its own* class, not of `A_i`, and the direction it needs is exactly the antiparallel one
where Lemma 5.2(2) is unavailable. The **statement** is nevertheless true, by a different route
(`smwg1r9lg` m5, Theorem D(i)): from `(5.2)` and `(T)` at all centres, `c(x+e+v) != c(x+e)` for
a.e. `(e,v)`, so `E = {x : the unit circle about x carries c(x) on positive angular measure}` has
`sigma{e : x+e in E} = 0` for every `x`, hence `|E| = 0` by Tonelli. That argument is
two-dimensional — it uses the open disk, not a single circle — which is precisely why it escapes
the null-circle obstruction. So the record cites m5's proof, keeps m6's Lemma 3 as what the broken
proof did give, and changes no number: `(SIN)` was run with and without, with identical counts. The whole `S_1` structure is one
two-line theorem. In `S_1`, (6.2) says a singleton palette is never contained in an edge of
`Gamma_x`, so the essential range `R_x` of `t -> sigma_x(t)` meets **no edge** of `Gamma_x`; and
(5.7) forces `|R_x| >= 2` (one value would meet its own `R`-rotate). Hence at every `k`

  `Gamma_x` is a subgraph of `K_{k-2}`: at least two labels are isolated, and no cycle is longer
  than `k-2`.

At a centre with an `ell`-cycle this gives `R_x <= [k] \ V(C)`, `|R_x| >= 2`, hence `k - ell >= 2`;
and `k - ell = 2` forces `R_x` to be the whole complement, i.e. the centre is **binary** for that
pair, so Lemma 5.5 makes the locus `delta_*`-separated. That one line reproduces the paper's `k =
5` triangle case, `m4`'s `k = 6` four-cycle local finiteness, and the `k = 5` four- and five-cycle
exclusions. At `k = 6` it gives `Gamma_x <= K_4` everywhere, so §7's extracted cycle has
`ell in {3,4}` and §8's `ell = 5,6` cases are **vacuous in `S_1`**; and at a triangle centre the
dichotomy is sharp: `|R_x| = 2` is binary and locally finite, while `|R_x| = 3` forces
`Gamma_x = K_3` exactly (the palette is confined to the complementary triple). So

  **`(W)` in `S_1` at `k = 6` is exactly local finiteness of the 3-valued triangle locus.**

No `(5.2)`-density argument can reach that locus: the palette there is confined to the
complementary triple, so at most `k-3 = 3` labels are excludable, while the paper's Lemmas
6.3/6.4/6.7 need 4 or 5. (Cross-check: at `k = 7` with `|R_x| = 4` at a triangle centre,
`7 - 4 = 3 = |V|`, so `Gamma_x = K_3` exactly — `m3`'s "`Gamma_x` contains `K_3`" is an
equality.)

**`m1`'s single-centre classification.** At `k = 6`, among the `2^15 = 32768` graphs on the six
labels, the single-centre palette system (palette bound, (5.7), the complementary-palette
exclusion, Lemma 6.2) excludes **exactly one**, the complete graph `K_6`; every other graph,
including the six-cycle, is realised by an explicit palette system. At `k >= 7` no graph is
excluded; at `k = 5`, 76 of 1024 are (an Erdős–Ko–Rado condition on the non-edges). So no
single-centre argument can prove local finiteness or exclude any cycle length at `k = 6`; only
multi-centre or colouring-level input can. Files: `.ultramath/smwfo9zkl/m1/proof.md`,
`work/classify2.py`, `work/verify_witnesses.py`.

**`m3`'s exact geometry of `L`, and the tameness frontier.** A separate line of attack computes
`L` itself instead of more palette systems (`.ultramath/smwfwi7rh/m3`, `python3 verify.py`, 23
exact `Q(sqrt 3)` checks, exit 0). *Lemma 1 (interface determination).* If `c` is constant on the
cells of a partition into open connected sets with piecewise `C^1` boundaries and every ball meets
finitely many cells and finitely many interface arcs, then `Gamma_x` is exactly the graph of
interface arcs through `x`. Hence `L` sits in the junction set, and **`(W)` holds — in that class,
at every `k`, with no palette bound, no measurability, no properness and no bound on `k`.** The
class contains every piecewise-`C^1` polygonal-map colouring, in particular the paper's `c_0`, so
it is not vacuous. The consequence is a structural constraint on the open case: **a `k = 6`
countermodel to `(W)` must be non-tame — some ball must meet infinitely many cells or infinitely
many interface arcs.** Corollary 3 sharpens the phase transition: for the altered colouring of
`k >= 7` one has `L(c) = V union {q_n, z_n : n in N} union {p_0}`, closed, countable, with exactly
one accumulation point. **Correction:** this `L` does *not* violate `(W)` — take a ball of radius
`3/2` centred more than `2` away from `p_0`; it meets only the lattice `V`, hence finitely many
points (`smwfycxze` m1 Prop. 7). So the `k >= 7` example refutes local finiteness, not `(W)`, and
`(W)` is not known to fail for any colouring at any `k`. What the example does show is that `(W)`
cannot be deduced from countability, closedness, null measure or content: an abstract lattice has
all of those and violates `(W)`. Theorem 2 computes `L(c_0) = V`, the honeycomb lattice of side `2/5`
(separation and covering radius `2/5`, density `25/(3 sqrt 3)`), so the seven-colouring is far from
extremal. Theorem 4 sharpens the gadget's shadow certificate to `eps = 1/70`, i.e. `W` of side
`1/50` instead of `1/100` (exact threshold `eps* = 0.0170789864...`, bracketed in
`[170/10000, 171/10000]`, two independent exact methods). Finally the circle colour counts identify
the resource: the unit circle about `p_0` meets exactly `4 = k - 3` colours, which is precisely
what the Mercedes gadget spends, so the same mechanism at `k = 6` would need a unit circle meeting
at most three colours.

## 4. Theorem C: the palette-level route is dead, for every cycle length

The paper's Theorem 6.5 is not merely "local finiteness"; it is proved case by case from the
palette bound, (5.7), the exact two-centre transport (5.3), and the edge traces of Lemma 6.2.
The following theorem shows that those hypotheses, at `k = 6`, admit a model with the `ell`-cycle
locus equal to the whole plane — for every `ell`.

**Theorem C (uniform palette-level no-go).** Fix `ell in {3,4,5,6}`. There exist a partition
`M_0, M_1, M_2` of `[6]` into three pairs, each avoiding every edge of `C_ell`, and a palette
field `P_z(e^{i theta}) = M_{floor( (floor(theta/Delta))/L ) mod 3}` (independent of `z`), with
`Delta = 2 pi/(6m)`, `L = 2m/3`, `m >= 6` divisible by 3, such that:

* **(P1)** `1 <= |P_z(e)| <= 3` (all palettes are pairs);
* **(P2)** `P_z(e) cap P_z(Re) = empty` for every `e`;
* **(P3)** for all distinct `z,z'` with `|z-z'| <= d_0 = pi/(9m)` and every unit `w`, and every
  unit decomposition `s + t = (z'-z) + w`, one has `P_{z'}(w) cap P_z(s) = empty` and
  `P_{z'}(w) cap P_z(t) = empty` (the exact local (5.3) transport);
* **(P4)** `P_z(e)` is not contained in any edge of `C_ell`;
* **(P5)** for each edge `{i,i+1}` of `C_ell`, a trace supported in `P_z` kills both edge labels;
* **(P6)** no two complementary triples both occur (vacuous: no triples).

Moreover every point of the plane is an `ell`-cycle point, so the `ell`-cycle locus is the whole
plane and accumulates at `0` (the centres `y_k = (d_0/3) 2^{-k} (3/5,4/5)` are distinct and
`y_k -> 0`).

The partitions are:

| `ell` | `M_0` | `M_1` | `M_2` |
|---|---|---|---|
| 3 | {0,3} | {1,4} | {2,5} |
| 4 | {0,2} | {1,4} | {3,5} |
| 5 | {0,2} | {1,3} | {4,5} |
| 6 | {0,3} | {1,4} | {2,5} |

*Proof.* The three pairs are pairwise disjoint and cover `[6]`; the shift by `pi/3` moves the
sector index by `m`, and `m/L = 3/2`, so the block index changes by 1 or 2 mod 3, hence to a
different pair, which is disjoint. The transport deviation is at most `1.5938 d` (the two exact
unit decompositions satisfy `|arg s_\pm - (arg w \pm pi/3)| <= 1.5938 |z'-z|`, from
`arcsin(d_0)/d_0 <= 1.0021` and `1/sqrt(4-(1+d_0)^2) <= 0.5917`); for `d <= d_0` this is less
than one sector `Delta`, so the sector index moves by one of `m-1, m, m+1`, and on each of these
offsets the block index changes by 1 or 2 mod 3. The finite block statement is checked in exact
integer arithmetic for every `m`, and the deviation bound in exact rational arithmetic, in
`.ultramath/smwfo9zkl/m15/verify.py` (two independent code paths) and, for the four partitions,
in `sprint/k6/uniform_nogo.py`. ∎

**Consequence.** No proof of any case of Theorem 6.5 — triangle, four-cycle, five-cycle or the
new six-cycle — can use only the palette-level hypotheses at `k = 6`. The triangle case also has
a second, independent countermodel with singleton palettes `{4+s(t)}`,
`s(t) = floor(9t/2pi) mod 3` (`.ultramath/smwfo9zkl/m13/no-go.md`), which satisfies an even
stronger form of (P3) at every distance `<= 1/50`; it is the model that shows most directly that
"the outsider set has size three" is fatal.

## 4b. Theorem C': the §8 strip layer is powerless too

`m6` decides the angular-obstruction layer of §8 at six colours. The class `STRIP(k,ell)` is the
strip data at a cyclic centre carrying a cycle of length `ell`: `S0` sliver nonemptiness, `S1`
the palette bound, `S2` the palette meets both one-sided allowed sets (Lemma 8.1 / (8.1)), `S3`
`P(u) cap P(Ru) = empty` (Corollary 5.4), and optionally `S4` (Lemma 6.2). Exhaustive decision
over the six `R`-orbit positions, two independent procedures:

  `STRIP(k,ell)` is UNSAT exactly for `(k,ell) in {(4,3),(4,4),(5,5)}`, and SAT otherwise.

The `(5,5)` row is Proposition 8.2, which calibrates the encoding. For every `k >= 6` and every
`ell` the strip layer is satisfiable, with explicit witnesses at `k = 6`:

| `ell` | `P` | `Q` |
|---|---|---|
| 3 | {4} | {5} |
| 4 | {4} | {5} |
| 5 | {5} | {1,3} |
| 6 | {1,4} | {2,5} |

alternating on the arcs `(r pi/3, (r+1) pi/3)`. So the printed §8 cases fail at `k = 6` for
attributable reasons (palette size 3, outsider set size 3, the triple complement in Lemma 6.4,
and no argument at `ell = 6`). Together with Theorem C this closes the palette-level route at
both ends: the §6 cyclic-centre layer and the §8 angular layer are each powerless at `k = 6`.
Files: `.ultramath/smwfo9zkl/m6/RESULTS.md`, `work/verify.py`.

### 4b'. The four-cycle case has the same two label-count thresholds

`m7` isolates both places where §6.3 uses `k <= 5`, independently of the palette countermodels:
the state reduction of §6.3.1 needs an admissible palette to carry at most one of `{X}`, `U={0,2}`,
`V={1,3}`, which requires `3 > k-3`, i.e. `k <= 5` (at `k=6` exactly the two palettes `{0,2,X}`,
`{1,3,X}` are ambiguous among 33 admissible ones); and the transport of §6.3.2 needs a *single*
label outside `U union V`, whereas Lemma 5.2(2) gives density one only of the complement of size
`k-4 = 2` at `k=6`. The second is a label-count deficit that survives even if every palette has
size 2, so no palette hypothesis repairs it. `m7` also proves a `k`-general form of Lemma 6.4
(a 2-valued palette map forces `|G_1|+|G_2| <= k-3`, so at `k=6` total size at most 3, complementing
m16's exclusion of total size `k-2=4`), shows the pointwise constraint level plus (5.3) at distance
1 is satisfiable on the seven four-cycle centres of a Moser spindle, and gives a proper measurable
6-colouring of a strip with four-cycle centres (non-vacuity). Files:
`.ultramath/smwfo9zkl/m7/RESULT.md`, `verify.py`, `verify_indep.py`.

### 4c. A correction: m16's Theorem A is right, Corollary 3.1 is not established

`m16`'s Theorem A (any two disjoint nonempty groups with `|A|+|B| = k-2` cannot alternate under
`R`) is correct and is a genuine generalisation of the paper's Lemma 6.4. Its Corollary 3.1,
however, claims that at a six-colour four-cycle centre the set `{e : P_x(e) <= {0,1,2,3}}` is
angular **null**; the proof given assumes the set is conull ("suppose `P <= {0,1,2,3}` a.e.")
and derives a contradiction, which only shows the set is not conull. The distinction matters: the
pair field of Theorem C with the `ell = 4` partition `{0,2},{1,4},{3,5}` satisfies the 4-cycle
edge exclusions and (5.7), and its set `{P = {0,2}}` has measure `2 pi/3`, so the null statement
is false at the palette level. (It is not a colouring's palette, so the corollary may still be
true for colourings; but the printed proof does not establish it, and the 4-cycle case remains
open.) Theorem A itself is not affected.

**The repair (`m8`, accepted).** The engine's exact reach is a *confined* alternation statement.
Let `A, B` be disjoint nonempty label groups with `|A|+|B| >= k-2`, `E <= S` measurable,
`A_0 <= E` measurable with `A <= P_x` on `A_0`, `B <= P_x` on `E \ A_0`, and
`1_{A_0}(t + kappa) = 1 - 1_{A_0}(t)` a.e. on `E cap (E - kappa)`. Then
`{t in A_0 : t+2kappa, t+4kappa in A_0, t + pi + gamma_0 + 2 j kappa in E \ A_0 (j<3)}` is null,
with `gamma_0 = 2 arcsin(1/(2 sqrt 3))`. Theorem A is the case `E = S`. The shift is *forced*
(`|1+v|^2 = 1/3` iff `Re v = -5/6`) and one fixed endpoint never gives a unit triangle
(circumradius `1/sqrt3`), so no adaptive choice of shift widens the conclusion. The corollary's
conclusion fails maximally at the palette level: the 36-sector 2-valued alternation
`{0,2}/{1,3}` has `E` of measure `2 pi` — the maximum — satisfies the palette bound, `(5.7)` and
`(6.2)` for `ell = 4,5,6`, has two free labels, and violates the confined statement; only
properness separates it. A decided finite computation splits the regimes: 2-valued sector fields
satisfy `(5.7)+(6.2)` (up to 26112 words, `m <= 8`, `ell <= 6`) and **none** survives `(5.3)`,
while 3- and 6-valued models do — so a free-label witness at `k = 6` needs at least three values.
Machine-checked on the pinned toolchain (`lean/repair31.lean`, exit 0):
`no_proper_two_colouring` and `rigidity` on `[propext, Classical.choice, Quot.sound]`,
`no_two_valued_sector_field` on `[propext, Quot.sound]`. The four-cycle case at `k = 6` remains
open, with `m8`'s Corollary R2 as the necessary condition any future argument must respect.

### 4d. The method boundary: at `k = 6` every formalised layer is satisfiable

At `k = 5` the paper's §6–§8 argument runs through four layers, each converting a palette bound
into geometry. At `k = 6` every one of them has now been decided, and every one is satisfiable:

| layer | what it supplies at a cyclic centre | status at `k = 6` |
|---|---|---|
| single-centre palette | palette bound, `(5.2)`, `(5.3)`, `(5.7)`, edge traces | satisfiable; only `K_6` excluded among `2^15` graphs (`m1`) |
| finite two-centre | the finite probe systems | satisfiable unless a 7-chromatic finite unit-distance graph exists (`m10`/`m2`) |
| strip / Minkowski (§8's angular data) | `STRIP(k,ell)` | SAT for every `k >= 6` and every `ell` (`m6`, §4b) |
| §8 pointwise orbit system with self-avoidance | `(8.1)`, Cor 5.4, palette bound, Lemma 6.2, `(SA)` in every cell of every ray configuration | **SAT for every `ell`** (`m6`, below); in `S_1` only `ell in {3,4}` can occur at all (`smwfycxze` m4) |
| global properness | that the colouring exists | equivalent to `chi(R^2) <= 6` (`m10` Thm 4, `m15` Thm C) |

**`m6`'s decision of the orbit layer.** Write `q` for the direction of `e` in units of `pi`, let
`v_j` be the limiting directions of the §7 exclusion continua, and let `P_j(q)` be the set of orbit
positions `p` with `q + p/3` in the open semicircle centred at `v_j`. Then `j in S_p` iff
`p in P_j(q)`; for a.e. `q` each `P_j(q)` is a *cyclically consecutive triple* of `Z/6` (an open
semicircle meets a regular hexagon of directions in exactly one point of each antipodal pair, which
is the **antipodal law** `S_{p+3} = [ell] \ S_p`, `(O,I)_{p+3} = (I,O)_p` — used implicitly twice in
the paper's §8.2 and Lemma 8.3); every one of the `6^ell` prescriptions is realised by some ray
configuration; and as `q` advances exactly one class of rays slips at a time, so a configuration is
a weak cyclic order of the residues `r_j mod 1/3` together with the triple of one cell. Since
`(8.1)`, `(5.7)`, the palette bound, Lemma 6.2 and self-avoidance are a.e. statements while `O` and
`I` are cell-constant, **the palette system must be satisfiable in every cell**. Exhaustive exact
enumeration (two independent procedures, rational arithmetic) gives the surviving configurations

| `ell` | 3 | 4 | 5 | 6 |
|---|---|---|---|---|
| surviving configurations at `k = 6` | 16848 | 390936 | 268200 | 252 |

(a "surviving configuration" is a triple — centre colour, starting cell, weak slip order of the
rays — whose whole closed cell cycle is satisfiable; the weak orders number `13, 75, 541, 4683`
for `ell = 3,4,5,6`, the ordered Bell numbers, and at `ell = 3` the count is exactly
`6 x 216 x 13`.)

and the calibration at `k = 5` is exact: `ell = 5` gives **0** survivors, with *and* without
self-avoidance — a new purely combinatorial proof of Proposition 8.2 that never uses the sign/run
counting of §8.2. At `ell = 6` only 252 configurations survive, and none of them has six distinct
slippage classes (108 have the single class `(0..5)`, the other 144 split into two classes of
three), so the printed case analysis cannot be repaired. `m6` also corrects an error on the
board: `(5.2)` holds for a.e. *pairs* of directions and may not be applied to the one-parameter
orbit family; the numbers are unchanged on the rigorous system, and the open-set form of `(5.2)`
is checked separately (all 252 survivors admit an assignment).

**The counting deficit in §8.5 (`smwfycxze` m1, accepted).** There is also an exact quantitative
reason why the printed `§8.5` step cannot reach `k = 6`. The `(5.2)` two-term sum exclusion is
evaluated at a *point* `z = x + u + v`; for `0 < |z| < 2` the unit decomposition is unique up to
order (two circles meet in two points, exchanged by `u <-> v`), so at a fixed point `(5.2)` excludes
at most `|P_x(u) union P_x(v)|` labels — at most two in `S_1`. The `§8.5` step must exclude the
`k - 3` outsiders to reach a three-label region, so it works exactly for `k <= 5` and is **one
label short at `k = 6`**. The other single-centre rule (Lemma 6.3) needs palette groups of total
size `k - 1`, which a singleton triangle centre does not have. Calibration: at `k = 5` the same
count reproduces the paper's region (8.4) exactly, with the seven placed Moser vertices strictly
inside it, in `Q(sqrt3, sqrt11, sqrt33)`.

**The outsider gate at `ell = 5` (`smwfycxze` m2, checked).** The five-cycle case has the same
shape. Let `X` be the single outsider at a `k = 6` centre whose `Gamma_x` contains a simple 5-cycle
on `0..4`. If `X` is absent from `P_x(e)` for a.e. `e`, then a contradiction follows — with **no**
palette bound, the only geometric input being `Q(-e) = complement Q(e)` (so the antipodal collapse
`R^3 = -1` is what makes this work for odd `ell`, and an even `ell` would fail). Since `k - ell = 1`
here, the outsider is the only label that can be spared, so the gate is exact. Five independent
decision procedures agree that all 1000 geometry-free cases are UNSAT; the `k = 5` calibration
gives `0/1000` (this is Lemma A reproducing Proposition 8.2); sharpness: `1000/1000` satisfiable
with nothing absent, `704/1000` with a cycle label absent, `0/1000` with the outsider absent. And
the gate's hypothesis is **false**: there is an explicit three-valued measurable field with
`sigma{X in P} = 1/3`, satisfying `(8.1)`, `(5.7)`, `|P| <= 2`, `(6.2)`, `(SUM)` and `m11`'s bound,
and avoiding a cycle label. So the missing lemma for `ell = 5` at `k = 6` is exactly "the outsider is
absent a.e.", and it does not hold — the 5-cycle is not excluded.

**The boundary.** So the paper's method cannot be carried to six colours by strengthening any
layer that has been formalised: each is already satisfiable. What remains is exactly the global
properness of the colouring, and by `m10`/`m15` that condition is *equivalent* to
`chi(R^2) <= 6`. Equivalently: a proof of `chi(R^2) >= 7` along this route needs an ingredient
which is not a consequence of the palette axioms — and any such ingredient, if it is (T) or
anything implying it, already proves the upper bound it is supposed to contradict.

### 4e. The locality barrier: no countable-centre evaluation can be contradicted

`smwg1r9lg` m5 splits the paper's palette axioms into four types — **(D)** direction-wise at one
centre, **(L)** trace-linked to the colouring, **(B)** the two-centre transport `(TE)`, **(M)**
multi-centre — and decides what each can see. Exit statuses: `verify.py`, 44 exact checks, 0
failures.

* **Theorem A (why every single-centre computation came out SAT).** (D) has no locality content:
  a direction-wise constraint system satisfiable at one centre is satisfied at *every* set of
  centres by the frozen lift `P_x = P`, jointly measurable. So no result of the form "the
  single-centre system at `k = 6` is satisfiable" could ever have decided anything, a priori.
* **Theorem B (the exact reach of `(TE)`).** For a countable `X`, `(TE)` restricted to `X` holds
  iff `G[X]` — the unit-distance graph on `X` — is `k`-colourable: for a.e. direction `f_0` every
  palette `P_x(f_0)`, `x in X`, is nonempty and any two at unit distance are disjoint, so any
  choice `c(x) in P_x(f_0)` is a proper `k`-colouring; conversely a `k`-colouring gives singleton
  palettes. Over all countable `X` this is `chi(R^2) <= k` (de Bruijn–Erdos). The ladder, exactly:
  Moser spindle at `k = 3`, Parts' graph at `k = 4`, de Grey's at `k = 5`, and at `k = 6` nothing —
  a contradiction from `(TE)` at countably many centres **needs a 7-chromatic finite
  unit-distance graph**. Calibration that the ladder is not vacuous: the paper itself proves
  `chi(R^2) >= 6`, so its own finite graph `H` (Theorem 1.2's proof, p. 5: "a finite unit-distance
  graph `H` that is not five-colorable") refutes `(TE)` at `k = 5` with finitely many centres.
* **Theorem C (the barrier).** `(T)`, `(SA)`, `(5.2)` and `(5.7)` are simultaneously satisfiable at
  **every** countable set of centres at `k = 6`, explicitly. The witness has `L = empty`, which is
  exactly why it does not contradict Theorem E below: the barrier is about countably many centres,
  not about all of them.
* **Theorem D.** `(5.2)` implies self-avoidance a.e., and the two are equivalent in `S_1` — so the
  record's Lemma D is a consequence of the paper's own `(5.2)`, not an extra hypothesis.
* **Theorem E.** `(T)` with `(5.7)` at *every* centre is equivalent to `chi(R^2) <= k` (Fubini
  legitimated), which explains why `(5.7)` is the axiom that closes and `(TE)` is not.

**The conclusion to keep.** Of the four types, (D) and (L) are satisfiable at every countable set
of centres, and the only one through which countably many centres can bite is `(B)` — which is
`chi(R^2) <= 6`, i.e. the problem itself. This is the certified dead-route statement for the whole
"evaluate the palette axioms at countably many cyclic centres" programme, and it is the reason this
report no longer proposes any such computation.

### 4f. The quantitative form of the barrier: circle-thinness

`smwg1r9lg` m4 gives the identity behind Theorem C, at the level of colourings rather than axioms.
For `O <= [6]` with `|O| >= 2` let `E_O = {x : R_x = O}` — the centres whose unit circle carries
exactly the labels of `O`, each on positive angular measure — and let
`g_E(y) = sigma(dB(y,1) cap E)`. Then, for every measurable `E <= E_O`,

  `int_{R^2} 1{c(y) notin O} . g_E(y) dy = 0`,

by Tonelli with `y = x + e` and `e -> -e` preserving `sigma`, using only `(T)` and `(SA)`
(and `(SA)` is itself a consequence of `(5.2)+(T)`, §3b). Consequences, stated exactly:

* `E_O` is **not conull in any ball of radius `> 1`**, hence contains no ball of radius `> 1`, and
  at a.e. of its own points its own unit circle is essentially disjoint from it. `Z^3_V` inherits
  all of this.
* **Nothing is claimed about smaller balls**, and the method cannot reach them: against a contained
  `B_r(z)` with `r <= 1` the circle `dB(y,1)` never lies inside `B_r(z)`, so the identity is
  silent — it constrains `{c notin O}` only through the weight `g_{E_O}` (essential disjointness,
  not largeness). (This clause was over-stated in the first version and is corrected in the
  revision; it is worth keeping because the false strengthening is the tempting one.)

Read with §4e this is the sharp statement of *why* the programme fails: circle-fibre hypotheses on
a set of centres control the plane only through the absolutely continuous aggregate `g_E`, and a
union of circles is null, so a countable-centre argument has no grip on an accumulation.

**The composition is saturated (`smwg1r9lg` m1, accepted).** The obvious next move — add the accepted
one-centre families to m6's §8 orbit system and see whether the superposition cuts — has now been
done, and the answer is no, structurally. The 14-item system (m6's cells, `m7`'s
`|P_x(e)| + |Col(S(x+e,1))| <= k`, `m9`'s unit-triangle count, `m11`'s `sigma{T <= P_x} <= 1/2`,
and `(TE)` on the six unit neighbours) has survivor counts **identical** to m6's
(16848 / 390936 / 268200 / 252 for `ell = 3,4,5,6`; per-cell word counts unchanged with and without
each extra family), and the reasons are theorems, not accidents:

* `m11`'s bound is a consequence of `(5.7)`;
* `m7`'s circle bound is a consequence of the palette bound plus "a unit circle carries at least
  two labels a.e." (one label would give a monochromatic unit pair, since a unit circle contains
  pairs at distance 1);
* `m9`'s count is pointwise disjointness at a unit triangle, i.e. `(TE)` itself;
* `(TE)` is inert at the row level, because the rim palettes are not determined by the word.

Calibration: at `k = 5`, `ell = 5` the same census returns 0 (Proposition 8.2), and `k = 5`,
`ell = 3,4` return 1296 and 24 — so it is not vacuous. **No superposition of the accepted
single-centre families excludes any cycle length at six colours**, and the only remaining lever at
that level — the endpoint trace at a second centre, or `(5.3)` at a distance other than 1 — is again
`chi(R^2) <= k`.

**Consequence for the Lean development.** The k=5 endgame is machine-checked at
`lean/OAI/Geometry/PlaneColoring/Exclusion.lean:144`
(`no_five_exclusion_continua : WeakColoring 5 c -> ApproachingContinuum x (K i) (v i) -> ... ->
False`, i.e. no exclusion continua exist at a cyclic centre of a five-colouring; it takes the §7
output as a hypothesis and its own comment says it does not assert that the data have been
extracted). There is no cheap k=6 analogue to port. Beyond the existence of the colouring, the
proof consumes exactly the pointwise palette system at the centre — `(8.1)`, `(5.7)`, the palette
bound, `(6.2)` and self-avoidance — and that system is satisfiable at `k = 6` for every `ell`
(`m6`); so a k=6 analogue cannot be obtained from the extracted data, and would have to use the
colouring globally, which is `(T)` and therefore equivalent to `chi(R^2) <= 6`. (The statement is
not *false* — it is vacuous if `chi(R^2) = 7` — but it is not derivable from the printed
hypotheses.) Independently, the development is `Fin 5`-typed throughout (84 occurrences of
`WeakColoring 5` across ~20 modules), so even a mechanical k=6 variant would be a re-typing of the
whole §5–§8 chain, with its final step blocked by the result above.

## 5. Theorem D: self-avoidance, and the exact frontier

The countermodels of Theorem C are not induced by any weak measurable 6-colouring. The reason is
a colouring-level constraint that the paper does not record:

**Lemma D (self-avoidance).** Let `x` be a density-one point of its own colour class, with
`c(x) = i`. Then `i notin P_x(e)` for a.e. unit direction `e`.

*Proof.* If `D = {e : i in P_x(e)}` has positive measure, let `e_0` be a density point of `D`.
Lemma 5.2(2) gives density zero of `A_i` at `x + e_0 + v` for every unit `v` nonparallel to
`e_0`. Take `v = -e_0 + delta` with `|delta - e_0| = 1` and `delta notin {0, 2e_0}`. Then
`x + e_0 + v = x + delta`; the set of `delta` on that circle with `x + delta` a density-one point
of `A_i` is conull (the non-density set is plane-null and Fubini applies to the circle). So
density one and density zero at the same point, contradiction. ∎

The paper's constant-sequence trace only gives `c(x+e) in P_x(e)` (the colour of the *other*
endpoint); Lemma D is the statement for the centre itself.

**Corollary D2.** The pair field of Theorem C uses all six labels at every centre (the three
pairs partition `[6]`), so no label is absent from its palette: even the non-proper form of
self-avoidance fails. The singleton triangle model of `m13` does admit a non-proper avoiding
label (any label in `T`), but any *proper* avoiding label would be a proper 3-colouring of the
plane, which is impossible since `chi(R^2) >= 4` (Moser spindle) and machine-checked `>= 6`.
So both countermodels violate self-avoidance in its proper form.

**The frontier, corrected: the endpoint trace, not properness, removes the models.** `m10`
(`smwfwi7rh`) proves that no weak measurable colouring of any `k` has a palette field independent
of the centre: for such a field, the endpoint trace `c(x+e) in P_x(e)` (Lemma 1, from the
constant circle sampling `(x,1)`) and self-avoidance `c(x) notin P_x(e)` contradict by Fubini,
with no joint measurability needed. This removes **every** centre-independent countermodel of
record — the block fields, the singleton model, all free-label sector fields — by a condition
*weaker* than properness. Moreover endpoint trace plus (5.7) is already properness: every unit
pair `(y,y')` is `(z+e, z+Re)` with `z=(I-R)^{-1}(y'-Ry)`, so the endpoint trace is a proper
colouring. Hence at `k=6`

  palette axioms alone             : satisfiable, accumulating, every length;
  palette axioms + any trace function : satisfiable iff `chi(R^2) <= 6`.

There is no intermediate axiomatisation. The free-label models below are therefore a sharp
statement about the *palette axioms* and not a near-counterexample to the colouring problem; a
proof of `(W)` must use the endpoint trace, which is exactly the colouring.

**Non-proper self-avoidance kills nothing at the palette level.** For every
`ell in {3,4,5,6}` there is a translation-invariant sector palette field satisfying the palette
bound, the edge exclusions, (5.7), the exact local (5.3) transport, **and non-proper
self-avoidance** (a fixed label absent from every palette), with the `ell`-cycle locus equal to
the whole plane and accumulating centres (`sprint/k6/FREE-LABEL.md`). For `ell=3,4,5` the field
is a 3-block construction with pairwise disjoint values `{3},{4},{5}` / `{0,2},{1,3},{4}` /
`{0,2},{1,3},{5}`; for `ell=6`, where three pairwise disjoint admissible palettes must cover all
six labels, the current witness is the **period-12 pair-valued word**
`[1,3][1,3][1,3][1,4][1,4][2,4][2,4][2,4][2,5][2,5][3,5][3,5]` repeated three times, found by
exact SAT search and re-verified (`FREE-LABEL.md`); an earlier 36-sector word with a ternary
value `{2,4,5}` was **withdrawn**, and every certificate that still quotes it (including the
`safe {5,6,7} mod 12` set and the radius `0.14715`) must be read against the current word — the
audit `smwg1r9lg/m2` confirms that the current word is eliminated by the same mechanism, has the
same safe set and the same transport radius, so no verdict changes, but the printed witness
`A={1,3}, B={2,4}, t=93.221345 deg` belongs to the withdrawn model. So even non-proper
self-avoidance does not exclude any cycle length; only *properness* of the colouring does.

**The singleton model `(M)` of `m13` (palettes `{4+s(t)}`,
`s = floor(9t/2pi) mod 3`) satisfies not only (P1)-(P6) but also (5.2) itself with the *constant*
colouring `c = 1`, and non-proper self-avoidance holds with the same label `1`. So even adding
(5.2) and non-proper self-avoidance does not kill the countermodel. The only constraint it fails
is **trace-consistency with a proper colouring** — equivalently, `P` must be the *maximal*
palette field of a proper 6-colouring, not an abstract field that merely satisfies the palette
axioms. (The declared traces of `(M)` are `delta_{4+s(t)}`, which are not the circle-sample
limits of any colouring `c`; and a proper label function avoiding the palettes would have to be a
proper 3-colouring of the plane.) This is the exact frontier:

* a proof of `(W)` from palette-level data is impossible (Theorem C);
* a proof of `(W)` from data that includes a proper 6-colouring is exactly the setting of the
  paper's Theorem 1.4;
* the uniform pair field and the singleton field are the precise extremal objects that any
  future argument must kill; the pair field fails even non-proper self-avoidance, and the
  singleton field fails only the *proper* form (Lemma D plus properness of `c`), which is the
  first concrete colouring-level constraint that removes it.

### 5b. Two further new constraints, and the neutrality of finite palette data

**`m2`'s two-centre palette bound.** At `k = 6`, for every unit pair `x,y` and a.e. direction `e`,

  `|P_x(e)| + |P_y(e)| <= 5 = k-1`.

*Proof.* Put `a = y-x`, `z = x+Ra`. Then `|z-x| = |Ra| = 1` and `|z-y| = |Ra-a| = 1`, so `x,y,z`
is a unit triangle, and the three palettes in direction `e` are pairwise disjoint. If
`|P_x| = |P_y| = 3`, their union is `[6]` and `P_z(e)` is empty. ∎

So two ternary palettes cannot sit at unit distance in the same direction. This is a new spatial
constraint at `k = 6` (it is vacuous at `k <= 5` and has no disjoint maximal pairs at `k >= 7`).
It does not by itself give `|P_x| <= 2`.

**`m4`'s label-merging filter (machine-checked).** At `k = 6` every one of the fifteen label
pairs is realised by a set of unit pairs of positive measure (weak measurable colourings), and by
at least one unit pair for every proper 6-colouring with no regularity assumption: merging the two
classes would otherwise give a weak or proper measurable 5-colouring, contradicting the paper's
theorems. The quantitative forms (every 5-subset carries at least `1/3` of the unit pairs, every
4-subset at least `1/11`, from the triangle and the Moser spindle) are sharp but the aggregate is
slack at the uniform point `p_ij = 1/15`, so label merging alone cannot prove `chi >= 7`. The Lean
statements `pair_transition_not_null`, `exists_unit_pair_of_pair` compile under the pinned
toolchain with axioms `[propext, Classical.choice, Quot.sound]`.

**`m14`'s neutrality.** Any finite system of palette constraints built from size bounds,
disjointness, non-coverage `P_1 union ... union P_m != [k]`, and hitting conditions with the
two-subset property is satisfiable iff it is satisfiable with every palette of size `<= 2`
(shrinking a palette to a subset preserves all four shapes). Since the plane's unit-distance
geometry supplies no three-fold forced-disjointness pattern (no unit `K_4` in the plane: no point
is at unit distance from three pairwise-unit points), no finite palette system at `k = 6` can
force a three-label palette. This closes the whole finite palette-level programme, single- or
multi-centre, independently of the countermodels of Section 4.

### 5c. The three-valued selection wall: what the `k = 6` gap actually is

Four independent lines, all accepted (`smwfwi7rh` d14/d15/d18, `smwfwznwk` d1), converge on
one statement: **at `k = 6` every known necessary condition is satisfied by a three-valued
structure, and the only printed lemma that converts a palette bound into geometry — Lemma 5.5 —
is exactly a two-valued statement.** The gap is therefore not an estimate: it is the failure, at
three values, of the selection step that the `k = 5` proof uses at two.

* **`m7` Lemma 4.** Lemma 5.5's proof uses only that the palette meets a fixed label set `T` in a
  *singleton a.e.* and that "different from `s`" then determines the value; with two values the
  expanding action gives `delta_*`-separation, with three values only the inequality `s_x != s_y`
  survives and the expanding step has nothing to act on. This is the exact first step at which the
  `k = 5` machinery must fail, and it matches the three-outsider structure of `m4`'s `S_1` and the
  three values of `m13`'s singleton model.
* **`m1` Theorem 2 and Theorem 3.** At `k = 6`, uniform separation of `T`-hitting centres for every
  three-element `T` implies `|P_x(f)| <= 2` a.e. (a sufficient reformulation — the converse is not
  proved and does not follow from the palette axioms). Conversely `T`-hitting centres are
  `delta_*`-separated off the **`T`-spread** part, so all the difficulty is concentrated where the
  palette meets `T` in a genuinely three-valued way. Certified twice: granting `|P| <= 2`, the
  §6.3 machinery *still* fails at `k = 6` — four-cycle: 13 palettes, no admissible group
  assignment, minimal obstruction `{{4},{5}}`; five-cycle: 11 palettes; triangle: 15, all hitting
  the outsider triple. So separation plus a palette bound of two is not enough; an
  outsider-singleton treatment and a Lemma 6.3 analogue are also missing.
* **`m7` Lemma 1 and Lemma 2 (new constraints).** For every centre `x` and a.e. direction `e`,
  `P_x(e)` is disjoint from the labels occupying positive angular measure on the unit circle about
  `x+e`, whence `|P_x(e)| + |Col(S(x+e,1))| <= k`: at `k = 6` a ternary palette forces every such
  circle to carry at most three labels, so the geometric hypothesis "no unit circle carries three
  or fewer labels on positive-measure sets" implies `|P| <= 2`. And a unit circle coloured a.e. by
  *two* labels must alternate under `R` (each class of angular measure exactly `pi`) and its centre
  is a binary centre, hence `delta_*`-separated; the three-label analogue is false. The same
  pair-to-triple wall, seen on circles.
* **`m15` Theorem C and its corollaries (independent confirmation of `m10`).** `(T)` plus `(5.7)`
  already forces properness — `|1-R| = 1`, so every unit pair is `(x+Re, x+e)` and the two palettes
  are disjoint — hence `(T)+(5.7)` iff `chi(R^2) <= k`. Two corollaries matter: **(HIT)**, a
  centre-independent field has `intersection_e Q(e) = empty` by `(5.7)` and nonemptiness, so it is
  no colouring's palette field at all — a strictly stronger and cheaper kill than "fails
  self-avoidance", certified on all five countermodel families of §4; and **redundancy**, given
  the point-field identity `P_x(e) = F(x+e)`, axioms `(5.2)` and `(5.3)` follow from `(5.7)`
  alone, so the palette system has one non-redundant structural axiom and it is the one equivalent
  to the existence of a colouring.
* **The accumulation route is closed.** `m7` Lemma 3: the exact two-centre transport `(5.3)`
  degenerates *uniformly* to `(5.7)` as the separation tends to `0` (explicit bound `5d` for
  `d <= 1/2`, verified analytically and on a dense grid), so at an accumulation point of `L` the
  transport data imposes nothing beyond the single-centre system — which is satisfiable (`m1`:
  only `K_6` is excluded among `2^15` graphs). The renormalisation programme of `m7`'s own
  direction therefore cannot supply `(W)`. `m15`'s own direction (scale gluing) is likewise dead by
  its own theorem.
* **Decided finite computation (`smwfwznwk`).** The `C_6` free-label sector system has a
  translation-invariant solution **iff `m >= 5`** (`m = 2,3,4` UNSAT, `m >= 5` SAT, two independent
  decision procedures, smallest witness at `m = 5`, exact-rational transport re-checked at the
  realised offsets); the `k = 5` analogue is UNSAT for every `m` and the `k = 7` three-block word
  SAT. The class is nevertheless dead as a colouring's palette field, by the unit-separation
  transport.

* **`m12`'s sum-set kill.** Lemma 6.4 generalises with no palette bound: disjoint palette groups
  `G_1, G_2` carried on positive-measure direction sets force `|I \ (G_1 u G_2)| >= chi(Q)` for
  every finite unit-distance graph `Q` in the direction sum set, so at `k = 6` a union of 4 forces a
  triangle, 5 a unit edge, 3 the Moser spindle. Decided exactly: this kills **7 of the 9**
  palette-level countermodels of §4 — all four `m15` block fields and the free-label `ell = 4,5,6`
  fields — leaving exactly the singleton models. So "only properness removes these models" was too
  weak: **Lemma 5.2(2) alone removes the pair-valued ones.** The mechanism is strictly stronger
  than the angular (`gamma`) criterion: a `gamma`-avoiding field still dies through another pair.
* **`m9`'s exactly-tight triangle count.** At a unit triangle the three palettes are pairwise
  disjoint (Remark 5.3 at separation 1), so `sum_i (1/2pi) int_S |P_i| dsigma <= k`. At `k = 6`
  this reads `2+2+2 = 6 = k` exactly: if no vertex has a positive-measure singleton, all three
  palettes are pairs a.e., and a ternary palette at one vertex forces a positive-measure singleton
  at a neighbour. The `k = 5` count reads `6 > 5`, which is the origin of the forced singletons
  there; `k >= 7` has slack `k-6`, which is `m3`'s room. The surviving `k = 6` residue (pair-valued,
  or `(3,2)`) is `R^2`-invariant and is missed by `m16`'s theorem, `m7`'s Lemma 6.4 and the sum
  lemma alike; what *is* excluded three ways is the residue occupying the vertices of a unit
  triangle (exhaustive `120^3` enumeration: 0 solutions; CNF: all seven wheel centres UNSAT).
* **`m16`'s label cost `ell+3`.** A gadget of `m3`'s shape costs exactly `ell+3` labels: the unit
  shadow of a set `U` of diameter `< 1` avoids all `ell` labels and contains a thin annulus, whose
  measurable chromatic number is exactly 3 (exact certificate, and a measurable 2-colouring is
  impossible by an ergodic-rotation argument). `k >= ell + 3` with equality attained by `m3`. So at
  `k = 6` only `ell = 3` gadgets are feasible and the budget is met with zero slack; the `k = 6`
  obstruction is not a label count.

**Consequence.** Any proof of `(W)` at `k = 6` must either (a) prove separation of `T`-hitting
centres for `|T| = 3`, or (b) prove that the `T`-spread (genuinely three-valued) part cannot occur
at a cyclic centre of a proper 6-colouring — which, in `S_1`, is exactly the statement that the
3-valued triangle locus is locally finite (`smwfycxze` m4). And (b) is a colouring-level
statement, since the three-valued fields are palette-satisfiable (`m13`, `m15`) and permitted by
every quantitative bound (`m11`'s `sigma <= 1/2` is sharp and is attained on equal thirds).

## 6. The single-centre orbit constraints (decided finite computation)

At a typical cyclic centre of colour `i` (`sprint/k6/STRUCTURE.md`):

1. `i notin P_x(e)` a.e. (Lemma D);
2. `P_x(e) cap P_x(Re) = empty` (5.7);
3. if `|P_x(e)| = 3` then `|P_x(Re)| <= 2` (Lemma D applied to `P(Re)`);
4. if `P_x(e) = {b}` and `Gamma_x` contains a simple cycle with vertex set `V`, then `b notin V`
   (Lemma 6.2: the edge trace cannot be supported in `{b}` if `b` is an edge endpoint);
5. if two palettes at directions `120^circ` apart are disjoint and have total size `5`, their sum
   is a monochromatic unit sum, which is impossible (Lemma 4.3 and (5.2)).

Exhaustive enumeration of all six-tuples on the `R`-orbit satisfying 1-5 (plus the
complementary-triple exclusion and at most three ternary palettes):

| cycle length `ell` | centre colour | orbit words |
|---|---|---|
| 3 | in the cycle | 70194 |
| 3 | outside | 11888 |
| 4 | in the cycle | 18746 |
| 4 | outside | 2164 |
| 5 | in the cycle | 3720 |
| 5 | outside | 380 |
| 6 | in the cycle (all labels) | 510 |

Two independent implementations (`sprint/k6/orbit_correct.py`, a recursive DFS with filters, and
`sprint/k6/orbit_correct_v2.py`, a transfer-matrix trace) give identical counts; the `(C1)` and
monochromatic-sum filters cut nothing on the transition-admissible stratum. At `ell = 6` there is
no singleton, the all-pairs stratum has 150 words, the 2-periodic `(3,2,3,2,3,2)` pattern has 6,
and 354 words have one or two ternary palettes. Hence the single-centre constraints do not
decide any cycle length: the cross-centre structure is essential.

**The five extra conditions are theorems (`m2`, accepted).** Running the same enumeration under
`(SIN)`, `(C1)`, `(C2)`, `(MON)` and `(SA2)` separately gives *identical* counts
`70194 / 11888 / 18746 / 2164 / 3720 / 380 / 510`: none of them cuts anything on the admissible
alphabet, so the single-centre layer's whole content is `(PB) + (EDG) + (T)` together with
self-avoidance. The companion numbers: dropping `(EDG)` gives `446960` for every `ell` (the edge
condition is the only thing that makes the count `ell`-dependent), and adding `|P| <= 2` at
`ell = 6` gives `150`. `m2` also verified the paper's Lemma 8.9 certificate and Table 1 exactly
in `Q(sqrt3, sqrt11)`, and flagged one extraction trap: the display (8.6) on p. 57 has two
readings in flat text, and the affine one fails (8.4) at three of the seven vertices — the
rendered page disambiguates it (large parentheses around `g + (-290+149i)/250`), so the composed
reading is the only one.

## 7. Finite computations cannot decide `k = 6`

The prior swarms decided the six-step interface CSP at `k = 6`: SAT for every length and every
ray geometry (7848 instances, two independent decision procedures). `m16`'s shrink lemma shows
why: every "pair-satisfied" constraint is powerless, and the pair stratum is satisfiable.
`m10`'s two-centre CSP (`REDUCTION.md`, `twocentre.py`, `probes_out.json`, `sweep_out.json`)
proves the exact form of this: a finite probe is satisfiable iff its conflict graph is
`k`-colourable (min-map), and the conflict graph is the pullback of the plane's unit-distance
graph along `pi(x,e) = x+e`. Hence a finite two-centre CSP that is UNSAT at `k = 6` exists **iff**
a 7-chromatic finite unit-distance graph exists. So Step 3's finite programme is not a relaxation
of the six-colour problem; it is the classical finite-graph problem, and no such graph is known.
Every probe tested is SAT at `k = 6` (Moser spindle at `k >= 4`, the Lemma 6.4 configuration, the
hex patch, the interface palettes, 27 two-centre probes bipartite, 900 random probes clean). The same collapse is `m7`'s pointwise theorem
and `m8`'s a.e. collapse: the a.e. palette system with (5.3) is equivalent to the existence of a
6-colouring. So no *finite* CSP at this level can prove `chi(R^2) >= 7`; Step 3 of the brief is
closed negatively.

## 8. Status ledger and the exact open problem

| statement | status |
|---|---|
| §7 transfers at `k = 6` under `(W)` / `(F)` | proved, four independent audits, combinatorial core machine-checked |
| `L` nonempty and `1`-dense for every `k` | proved (`m5` squares, `m12` disks), independently re-derived |
| `(W)` strictly weaker than local finiteness | proved (all four audits) |
| `(W)` strictly weaker than nonemptiness/density | proved (the two-line-family example) |
| `(W)`: `L cap B(y,R)` finite for some `R > 1` | **open** at `k = 6`; not refuted at any `k` |
| weaker size conditions on `L` (Minkowski content, Hausdorff, porosity, density) | **cannot replace `(W)`** (`m5`: punctured-annulus obstruction + perfect zero-content set) |
| `L` is `1`-dense (every disk of radius `> 1` meets `L`) | proved (`m12`), unconditional |
| two ternary palettes at unit distance in one direction | impossible at `k = 6` (`m2`) |
| ternary palettes occupy at most half the direction circle | proved, sharp — Lean 4.34.1, `two_mul_measure_ternary_le_one` in `.ultramath/smwfo9zkl/m11/lean/K6Ternary.lean` (compiles, exit 0; the file prints no axiom listing, so its axiom set is unverified) |
| `sigma{T subset P_x} <= 1/2` for every nonempty `T`, every centre | proved (`m11`) |
| finite palette constraints can force a ternary palette | impossible (`m14` neutrality) |
| Theorem 6.5 from palette-level hypotheses at `k = 6` | **false** (Theorem C, every cycle length) |
| countermodels colouring-realizable | **false** (endpoint trace alone removes them, `m10`; equivalently (5.3) at unit separation, `m4` Cor 2) |
| singleton class `S_1` at `k = 6` | `L` locally finite iff the 3-cycle locus is (`m4` Thm 3) |
| palette constraints + non-proper self-avoidance at `k = 6` | satisfiable for every `ell`, accumulating (`FREE-LABEL.md`) |
| local finiteness at `k = 5` | true (paper). What is machine-checked is the **five-cycle endgame given the §7 data**: `no_five_exclusion_continua` in `lean/OAI/Geometry/PlaneColoring/Exclusion.lean:144`, axioms `[propext, Classical.choice, Quot.sound]`. The extraction and the `ell = 3,4` cases are not formalised |
| local finiteness at `k >= 7` | **false** (`m3`, explicit proper measurable colouring) |
| `(W)` in the tame class (piecewise-`C^1` polygonal colourings), every `k` | **proved** (`m3` Lemma 1 / Cor 1); so a `k = 6` countermodel must be **non-tame** |
| `L(c_0)` for the seven-colouring | exactly the honeycomb lattice `V`, side `2/5` (`m3` Thm 2) |
| `not (W)` | iff `L` is infinite in **every** ball of radius `> 1` (`smwfycxze` m1 Prop. 7(i)) |
| `P_x(e) >= {c(x+e)}` at every **good** centre | proved (`smwg1r9lg` m6 Lemma 1); at an exceptional centre a single circle carries no information, since null-set changes of `c` fix every `P_x` and `Gamma_x` |
| `Z^3(V)` in `S_1` at `k = 6` | `= {R_x = O} cap {K_3(V) <= Gamma_x}`; the centre colour does **not** enter (`smwg1r9lg` m6 Thm 1) |
| accumulation point of `Z^3(V)` | again a triangle centre — 3-valued, or binary with finitely many per ball (`smwg1r9lg` m6 Thm 2) |
| the accumulated limit system | **satisfiable**, both branches (`smwg1r9lg` m6 Thm 3) — so no contradiction from per-centre data + `(TE)` |
| the record's Lemma D proof | **broken**; the statement is true via `(5.2)+(T)` (`smwg1r9lg` m5 Thm D(i)) |
| circle-thinness identity | `int 1{c(y) notin O} g_{E_O}(y) dy = 0` (`smwg1r9lg` m4, (4.1)), so `E_O` is not conull in any ball of radius `> 1`; `Z^3_V` likewise; **nothing** for smaller balls |
| the composed single-centre system at `k = 6` | **saturated**: m7's, m9's and m11's families are consequences of `(P)`/`(5.7)`/`(TE)`, and `(TE)` is inert at the row level, so survivor counts equal m6's for every `ell` (`smwg1r9lg` m1) |
| `(5.2)` at a fixed point | excludes at most **2** labels (`smwfycxze` m1 Lemma 1); `§8.5` needs `k-3 = 3` at `k = 6` — one short |
| `(W)` in `S_1` | iff the 3-valued triangle locus is finite in **one** ball of radius `> 1` (`smwfycxze` m1 Cor 5') |
| a finite unit-distance gadget forcing 3-label colour equality | **does not exist** (`smwfycxze` m1 Prop. 8), so §8.4's constancy repair fails at `k = 6` |
| gadget shadow constant at `k = 7` | `eps = 1/70`, `W` of side `1/50` (`m3` Thm 4; sharpened from `1/100`) |
| the gadget's resource at a point | the unit circle about `p_0` meets `4 = k-3` colours (`m3` §6) |
| gadget label cost | exactly `ell + 3` (`m16`); at `k = 6` only `ell = 3` is feasible, with zero slack |
| §8 pointwise orbit system at `k = 6` (incl. self-avoidance) | **satisfiable for every `ell`** (`m6`: 16848/390936/268200/252); no `ell = 6` configuration with six distinct slippage classes |
| antipodal law `S_{p+3} = [ell] \\ S_p` | proved (`m6` Thm 1); used implicitly twice in the paper |
| Proposition 8.2 (`ell = 5` impossible at `k = 5`) | reproved combinatorially, without self-avoidance (`m6`: 0 survivors) |
| unit triangle at `k = 6` | `2+2+2 = k` exactly; ternary at one vertex forces a singleton at a neighbour (`m9`) |
| `ell = 5` at `k = 6` | **not excluded**; the residue cannot occupy a unit triangle (`m9`, three ways) |
| Lemma 5.2(2) without properness, trace-consistency or maximality | kills 7 of the 9 palette-level countermodels (`m12`); with the withdrawn `ell = 6` word replaced, 8 of 10 (`smwg1r9lg` m2). The survivors are the singleton-valued ones, but **arithmetically**, not geometrically: for singleton values `\|A u B\| = 2`, so `\|T'\| = 4 >= 3 = chi(triangle)`, and killing a singleton model would need a 5-chromatic finite unit-distance graph inside the sum set |
| globally free label at `k = 6` | **impossible**: its class is plane-null by Fubini over circles (`smwfwznwk` m2 Thm R); at a unit triangle `2+2+2 > 5` (`smwfwznwk` m4, Lean-checked) |
| the free-label sector class | **empty** under the unit-separation transport; its words satisfy `(5.3)` only for `\|z-z'\| <= 0.14715` (`m11`) and the sector class is satisfiable only up to `d* = 0.1755705046` (`m13`) |
| the three-block fields of §4 | satisfy `(5.3)` only for `\|z-z'\| <= 0.28558`, not the `pi/54 = 0.05818` first quoted (`m11`) |
| frozen (centre-independent) fields | satisfy `(5.3)` at separation 1 only with `P(f) = empty` — immediate from `(TE)`, no combinatorics; the Lean core `frozen_core.lean` (`m11`) supports the **intermediate**-distance exclusions `d >= 0.4609` and `d >= 0.3044`, not this one |
| exact frozen threshold | `D* = 2 cos(2 pi/9) - 1 = 0.5320888862`, the root of `D^3 + 3D^2 = 1`; shortfall `1 - D* = 0.46791` against the `d = 1` of Lemma 6.7 (`smwg1r9lg` m8: theorem, extremal 18-sector singleton field, sharp above `D*`) |
| `(TE)` at countably many centres | equivalently `G[X]` is `k`-colourable; over all countable `X`, `chi(R^2) <= k` (`smwg1r9lg` m5 Thm B) — a contradiction there needs a 7-chromatic finite graph |
| `(T)+(SA)+(5.2)+(5.7)` at every countable set of centres, `k = 6` | **satisfiable** (`smwg1r9lg` m5 Thm C; the locality barrier) |
| direction-wise palette constraints | no locality content: one-centre satisfiable ⟹ satisfiable at every centre set (`smwg1r9lg` m5 Thm A) |
| `(5.2)` implies self-avoidance a.e. | proved, and equivalent in `S_1` (`smwg1r9lg` m5 Thm D) |
| `ell = 5` at `k = 6`, §8 side | the gap is exactly "the outsider is absent a.e."; it is {\em false} (`smwfycxze` m2, five decision procedures) |
| `m16`'s Corollary 3.1 (`sigma(E) = 0`) | **not established**; repaired to the confined form R1, which is **paper-level** (`m8`); its three finite ingredients are Lean-checked in `m8/lean/repair31.lean` (forced triangle, shift rigidity, two-valued sector no-go), and the conclusion fails at palette level with `sigma(E) = 2 pi` |
| 2-valued sector fields at `k = 6` | satisfy `(5.7)+(6.2)`, **none** survives `(5.3)` (`m8`); free-label witnesses need `>= 3` values |
| the five extra single-centre conditions `(SIN),(C1),(C2),(MON),(SA2)` | cut **nothing**; the single-centre content is `(PB)+(EDG)+(T)+(SA)` (`m2`) |
| `alpha < 1/6` in §7 | exactly optimal for the printed argument (`m2`) |
| transfer for every `k >= 3` under `(W)`, `ell in {3..k}` | proved (`smwg1r9lg` m3 Thm A\*); no palette input at all |
| `(P)` (palette bound) in the transfer's hypothesis list | **redundant** (`smwg1r9lg` m3 E1) |
| cover obstruction at the exact constant (inradius `>` mesh) | proved twice (`m5`, `smwg1r9lg` m3 Lemma C); threshold not improvable up to `eta` (Lemma S) |
| `R > 1` / side `> 2` | **paper-level only**; the machine-checked engine is the ball-of-radius-5 / mesh-2 case (`R > 5`) |
| `R = 1` insufficient for the conclusion | **open** |
| in `S_1`, any `k` | `Gamma_x <= K_{k-2}`: `>= 2` isolated labels, no cycle longer than `k-2` (`smwfycxze` m4 Thm 1) |
| in `S_1` at `k = 6` | §7's cycle has `ell in {3,4}`; §8's `ell = 5,6` cases are **vacuous in `S_1`** |
| `(W)` in `S_1` at `k = 6` | **iff the 3-valued triangle locus is locally finite** |
| a 3-valued triangle centre at `k = 6` | `Gamma_x = K_3` exactly; palette confined to the complementary triple |
| `(T) + (5.7)` | `iff chi(R^2) <= k` (`m15` Thm C; independent confirmation of `m10` Thm 4) |
| any centre-independent field as a colouring's palette | **impossible** — `(HIT)` fails (`m15` C1; third independent kill) |
| given the point-field identity, `(5.2)` and `(5.3)` | consequences of `(5.7)` (`m15` Thm E) |
| `\|P_x(e)\| + \|Col(S(x+e,1))\|` | `<= k` (`m7` Lemma 1); a ternary palette at `k=6` forces every such circle to carry `<= 3` labels |
| Lemma 5.5 at three values | **false** — it is a two-valued selection theorem (`m7` Lemma 4) |
| uniform separation of `T`-hitting centres, `\|T\| = 3` | sufficient for `\|P\| <= 2` at `k = 6` (`m1` d18); not proved |
| `T`-hitting centres off the `T`-spread part | locally finite, `delta_*`-separated (`m1` Thm 3 / Cor 3.1) |
| `§6.3` machinery granted `\|P\| <= 2` | still fails at `k = 6` for 4-cycles, 5-cycles and triangles (`m1` d18, certified) |
| accumulation / renormalisation route to `(W)` | **closed** (`m7` Lemma 3: `(5.3)` degenerates uniformly to `(5.7)`) |
| scale gluing at `k = 6` | **closed** (`m15`, by its own author) |
| `C_6` free-label sector system | solution **iff `m >= 5`** (`smwfwznwk` d1; two independent solvers) |
| single-centre system at `k = 6` | excludes only `K_6` (`m1`); no cycle can be excluded |
| `chi(R^2) >= 7` | **not proved** |
| `chi(R^2) <= 6` | **not proved** |

**The exact open target.** Prove `(W)`: exhibit `y` and `R > 1` with `L cap B(y,R)` finite for
every weak measurable 6-colouring, or exhibit a 6-colouring whose `L` is infinite in **every** ball
of radius `> 1`. Three corrections: the first holds *automatically* in the tame class at every `k`,
so the open target is perforce about non-tame colourings (some ball meeting infinitely many cells
or interface arcs); the alternative needs local infinitude everywhere, not a perfect or even a
countable-dense `L` — `m3`'s `k >= 7` colouring, closed and countable with one accumulation point,
satisfies `(W)`; and `(W)` is **not** the only open input — §8's elimination at `k = 6` is the
other, and it is not obtainable from the printed single-centre hypotheses (§4d). By §5c the `(W)`
side has exactly two live shapes: (a) prove separation of `T`-hitting centres for `|T| = 3`, which
gives `|P| <= 2`; or (b) prove that the `T`-spread (genuinely three-valued) part cannot occur at a
cyclic centre of a proper 6-colouring — in `S_1` this is exactly the statement that the 3-valued
triangle locus is locally finite (`smwfycxze` m4). Everything else on the palette side is closed —
`(5.2)` and `(5.3)` collapse to `(5.7)` given the point-field identity, and the accumulation route
degenerates to the single-centre system.
By Theorem A the first would make §7 available at six colours; by Theorem B nonemptiness is
automatic; by Theorem C the palette machinery cannot supply it; by Lemma D the first
colouring-level constraint that the extremal models fail is self-avoidance.

## 9. Reproducibility

| file | content |
|---|---|
| `sprint/k6/TRANSFER.md` | the conditional §7 theorem, line-by-line audit |
| `sprint/k6/WEAKEST.md` | the isolated-point reduction, sharpness for perfect `L` |
| `sprint/k6/SYNTHESIS.md` | the full narrative and the frontier |
| `sprint/k6/STRUCTURE.md` | self-avoidance, ternary bound, singleton exclusion, orbit counts |
| `sprint/k6/orbit_correct.py`, `orbit_correct_v2.py` | the two independent orbit enumerations |
| `sprint/k6/uniform_nogo.py` | the four partitions and the block-shift check |
| `sprint/k6/FREE-LABEL.md` | free-label accumulating models for every `ell` (non-proper self-avoidance) |
| `sprint/k6/PHASE-TRANSITION.md` | standalone note: local finiteness true at 5, open at 6, false at >=7 |
| `sprint/k6/free_label_all.py`, `six_sat2.py`, `six_free_witness.json` | their exact certificates |
| `.ultramath/smwfo9zkl/m5/` | nonemptiness, `(F)`, sharpened cover lemma, verifier |
| `.ultramath/smwfo9zkl/m9/` | machine-checked §7 engine (`k6_s7_engine.lean`) |
| `.ultramath/smwfo9zkl/m12/` | §7 audit; 1-density; the sharpest hypothesis (`R > 1`) |
| `.ultramath/smwfo9zkl/m13/` | singleton triangle countermodel at `k = 6` |
| `.ultramath/smwfo9zkl/m15/` | pair-valued six-cycle countermodel with accumulating centres |
| `.ultramath/smwfo9zkl/m2/` | pointwise collapse; the `k=6` two-centre palette bound |
| `.ultramath/smwfo9zkl/m3/` | proper 7-colouring with non-locally-finite `L` (k>=7) |
| `.ultramath/smwfo9zkl/m1/` | single-centre classification: only `K_6` excluded at k=6 |
| `.ultramath/smwfo9zkl/m11/` | ternary-density bound (Lean), single-centre state decision, 7-centre certificate |
| `.ultramath/smwfo9zkl/m10/` | two-centre CSP decision machinery and SAT probes |
| `.ultramath/smwfwi7rh/m3/` | exact geometry of `L` (`m3`): tameness ⇒ `(W)` at every `k`; `L(c_0) = V`; closed countable `L` at `k >= 7`; shadow constant `1/70` |
| `.ultramath/smwfwi7rh/m7/` | circle–palette disjointness, two-coloured-circle rigidity, degeneration of `(5.3)` to `(5.7)`, Lemma 5.5 as a two-valued theorem |
| `.ultramath/smwfwi7rh/m15/` | `(T)+(5.7)` iff `chi <= k`, `(HIT)`, point-field redundancy, scale-gluing no-go |
| `.ultramath/smwfwi7rh/m1/` | ternary separation reduction, `T`-hitting separation off the `T`-spread part, §6.3 failure granted `\|P\| <= 2` |
| `.ultramath/smwfwznwk/m1/` | `C_6` free-label sector system: solution iff `m >= 5`, two independent solvers |
| `.ultramath/smwfwznwk/m2/` | no globally free label (Thm R); two-cell free-label-varying model killed by `(TE)`; PDI rigidity |
| `.ultramath/smwfwznwk/m4/` | free-label class empty: `(TE)` + `2+2+2 > 5`, Lean-checked `count_lemma.lean`; unit-triangle pair rigidity |
| `.ultramath/smwfwi7rh/m6/` | §8 at `k = 6` decided: pointwise orbit system SAT for every `ell`, antipodal law, and the `k = 5` recalibration |
| `.ultramath/smwfwi7rh/m9/` | `ell = 5` at `k = 6`: tight unit-triangle count, the residue, three-way exclusion on a unit triangle, patch SAT/UNSAT certificates |
| `.ultramath/smwfwi7rh/m12/` | sum-set density transport: Lemma 6.4 generalised, 7 of 9 countermodels killed by `(5.2)` alone |
| `.ultramath/smwfwi7rh/m16/` | gadget label cost `ell+3`, annulus measurable chromatic number exactly 3 |
| `.ultramath/smwfwi7rh/m8/` | repair of `m16` Cor 3.1: confined alternation R1 (paper-level), palette-level counterexample, 2-valued/3-valued regime split, plus three Lean-checked finite cores |
| `.ultramath/smwg1r9lg/m7/` | statement audit of the four cited Lean cores (defects D1–D8), sharpness theorems, exact sector census |
| `.ultramath/smwg1r9lg/m8/` | exact frozen-field threshold `D* = 2cos(2pi/9)-1`, extremal construction, sharpness |
| `.ultramath/smwg1r9lg/m5/` | the locality barrier: four-type classification, `(TE)` iff `k`-colourability on `X`, satisfiability at every countable centre set |
| `.ultramath/smwg1r9lg/m6/` | trace at good centres, `S_1` dictionary and accumulation, and Theorem 3: the limit system is satisfiable |
| `.ultramath/smwg1r9lg/m2/` | audit of the four palette constraints; defects D1–D7, incl. the strip-witness refutation and the stale withdrawn word |
| `.ultramath/smwg1r9lg/m4/` | `S_1` dictionary and accumulation; the circle-thinness identity (4.1) and its exact scope |
| `.ultramath/smwg1r9lg/m1/` | the composition is saturated: survivor counts equal m6's, with proofs that each extra family is implied or inert |
| `.ultramath/smwfwi7rh/m2/` | audit: five extra orbit conditions cut nothing, Lemma 8.9 and Table 1 exact, `alpha` range, (8.6) reading |
| `.ultramath/smwfycxze/m4/` | `Gamma_x <= K_{k-2}` in `S_1`; the `k = 6` triangle dichotomy; `(W)` in `S_1` = local finiteness of the 3-valued triangle locus |
| `.ultramath/smwfycxze/m1/` | `(W)` need not fail at one accumulation point; `(5.2)` excludes at most 2 labels per point; the `S_1` reduction to one ball |
| `.ultramath/smwfwi7rh/m11/` | frozen fields are inadmissible (Lean core); exact transport radii `0.28558` / `0.14715`; SAT to `0.175` |
| `.ultramath/smwfwi7rh/m13/` | sector class satisfiable iff `K <= floor(m/5)`; sharp `d* = 0.1755705046` |
| `.ultramath/smwfycxze/m2/` | §8 at `k = 6`, `ell = 5`: outsider gate, five procedures, three-valued countermodel |
| `.ultramath/smwg1r9lg/m3/` | independent audit of §7 (`AUDIT-S7.md`): Theorem A\* for every `k`, Lemma C (exact cover constant), Lemma S (optimality), errata E1–E10 |
| `sprint/k6/STATUS.md` | post-outage hand checks with commands and exit statuses |
| `.ultramath/smwfo9zkl/m14/` | direction-local reduction, counts, neutrality of finite palette data |

**Two corrections to the prior record.** (i) `results/K6-BARRIER.md` §2's sentence "a cover of
the square by tiny disks has mesh tending to zero and multiplicity one" is false (a multiplicity
one cover of a connected square is a single set); the multiplicity-three obstruction is a
different, true statement (`m5`, Theorem C). (ii) `results/K6-BARRIER.md`'s "the only `k`-dependent
ingredient of §7 is local finiteness" should read: the only ingredient is an isolated point of
`L`, and §7 uses no palette bound at all.
