# Sprint B synthesis: §7 at six colours, and where the route dies

> **Status: superseded.** This note was written before the results of `smwfwi7rh`, `smwfwznwk` and
> `smwfycxze`; `REPORT.md` is the living document and takes precedence. Three statements below are
> now corrected there: (i) "the isolated point is the whole cost" — §8's elimination at `k = 6` is
> a second, independent input, and it is not obtainable from the printed single-centre hypotheses
> (REPORT §4d); (ii) `(W)` is **not** refuted at any `k` — `m3`'s `k >= 7` colouring satisfies it
> (REPORT §0); (iii) the number of independent audits, the density constant (`1`-dense, not
> `sqrt 2`-dense) and the status of the colouring-realizability kill have all been updated in
> `REPORT.md`.

**One page.** The printed extraction of the interface (§7 of the paper) is a `k`-independent
machine that consumes exactly one geometric input: an **isolated point of the cyclic locus**
`L = {x : Gamma_x contains a cycle}` (equivalently, a side-`>2` square meeting `L` finitely).
Everything else in §7 — disk averaging, the cover obstruction, the non-null core loop, midpoint
detection — is label-blind; at `k = 6` the only changes are `alpha < 1/6`, the complete graph
`K_6`, and cycle lengths `ell in {3,4,5,6}`. This is proved three times independently below
(and the combinatorial core is machine-checked in Lean). So **§7 is available at six colours
modulo one hypothesis**, and that hypothesis is not non-emptiness: `L` meets every closed square
of side `> 2`, for every `k`.

The second half of the sprint is negative and, we think, decisive. The palette-level hypotheses
that the paper's own triangle case of Theorem 6.5 uses — the general-`k` palette bound, (5.7),
the exact two-centre transport (5.3) below a fixed distance, the edge traces, and the
complementary-triple exclusion — are **satisfiable at `k = 6` with the triangle locus equal to
the whole plane**. The model is explicit:
`P_z(e^{it}) = {4 + (floor(9t/2pi) mod 3)}`, independent of `z`. Hence no proof of the triangle
case, and therefore no proof of the isolated point, can use only those hypotheses. The model is
not induced by any colouring: it violates the **self-avoidance** lemma (a typical point's own
colour is absent from its palette a.e.), and any proper label function that avoids its palettes
would be a 3-colouring of the plane. Since a proper 6-colouring is exactly what the whole
problem asks for, the frontier is sharp:

  * palette-level data: **dead**, by an explicit countermodel;
  * colouring-level data: **the problem itself**, but now with a concrete first constraint
    (self-avoidance) and a concrete extremal model to test any future argument against.

Nothing here proves or refutes `chi(R^2) = 7`. What is settled is the shape of the `k = 6`
interface: §7 is free, the isolated point is the whole cost, and the printed palette machinery
cannot pay it.

---

## 1. The conditional §7 theorem

**Theorem 1.1 (transfer).** Let `c` be a weak measurable 6-colouring and suppose

  **(W)** there are `x_0 in L` and `r > 0` with `L cap B(x_0,r) = {x_0}`.

Then the conclusion of Proposition 7.1 holds at `k = 6`: there are `ell in {3,4,5,6}`, distinct
labels `i_0,...,i_{ell-1}`, a centre `x`, a radius `rho`, and for each edge `i_j i_{j+1}` a compact
connected `K_j` with the four properties of the paper's Proposition 7.1 (common centre, boundary
contact, limiting directions, exclusion of both endpoint essential supports from `Delta(K_j)`).

**Theorem 1.2 (square form, strictly weaker).** Let `(F)` be: some closed square of side `> 2`
meets `L` in finitely many points. Then Proposition 7.1 holds at `k = 6`. `(F)` implies `(W)`
(inside the square, one of the finitely many points is interior, hence isolated in `L`).

**Proof and audit.** `sprint/k6/TRANSFER.md` (line-by-line audit), `sprint/k6/WEAKEST.md` (the
isolated-point reduction), `.ultramath/smwfo9zkl/m12/S7-INPUT.md` (independent audit with the
rendered paper; `(W)` with isolation radius `3`), `.ultramath/smwfo9zkl/m5/K6-CYCLIC-LOCUS.md`
(`(F)`, with the sharpened cover lemma `s <= 2m`). The three proofs agree on every step; the two
`k`-dependencies are `alpha < 1/k` and `ell <= k`. The passage of the thresholded disk averages
into the one-skeleton is **not** a palette step: a clique in a forest has at most two vertices,
for every `k`; the paper's palette bound is never used in §7.

**Machine-checked core.** `.ultramath/smwfo9zkl/m9/k6_s7_engine.lean` contains
`card_le_two_of_isClique_of_acyclic` and `graph_map_large_positive_generic` for an arbitrary
finite label type, with standard axioms only. This is the only non-topological combinatorial
ingredient of the passage; the rest of §7 is the paper's topology (Lemmas 7.5, 7.7, 7.8), which
is label-blind.

## 2. Non-emptiness is not the gap

**Theorem 2.1 (`m5`, sharp).** For every `k >= 3` and every weak measurable `k`-colouring, `L`
meets every closed square of side `> 2`. Hence `L` is `sqrt 2`-dense: every closed disk of radius
`> sqrt 2` meets `L`. In particular `L != empty`.

*Proof.* If a square `Q_0` of side `> 2` missed `L`, run Lemma 7.4 with `L_0 = empty` (every
`Gamma_z` is then a forest) and Lemma 7.6's cover argument with no core disks; the component cover
of a slightly smaller square `Q` has multiplicity `<= 2` and mesh `1+o(1)`, contradicting the
scale-invariant cover lemma (`s <= 2m`). The paper itself records the seed: "This argument also
rules out the possibility of having no core disks in `Q`" (p. 47). `square`

So existence is free at every `k`; the whole cost of the `k = 6` interface is the *finiteness /
isolation* in `(W)`. The example `L = {x = 2 sqrt 2 k} union {y = 2 sqrt 2 k}` (two orthogonal
line families) is closed, `sqrt 2`-dense, perfect, and misses a square of side `2.1`: it shows
that no density statement implies `(W)` (`m5`, Theorem 5.3).

## 3. The palette-level no-go at `k = 6`

**Theorem 3.1 (`m13`, independently verified here).** Fix `k = 6`, `T = {1,2,3}`,
`O = {4,5,6}`, and `0 < eps <= 1/50`. Define, for every centre `z` and every angle `t`,

  `P_z(e^{it}) = { 4 + ( floor(9t/(2pi)) mod 3 ) }`,   `W_z = { t |-> e_{4 + (floor(9t/(2pi)) mod 3)} }`.

Then the triple `(Z, P, W) = (R^2, P, W)` satisfies:

* **(P1)** `1 <= |P_z(e)| <= 3`;
* **(P2)** `P_z(e) cap P_z(Re) = empty` for every `e`;
* **(P3)** for all `z != z'` with `|z-z'| <= eps` and every unit `w`, and every decomposition
  `s + t' = (z'-z) + w` into unit vectors, `P_{z'}(w) cap P_z(s) = P_{z'}(w) cap P_z(t') = empty`
  (the exact two-centre transport form used in the proof of Lemma 5.5);
* **(P4)** `P_z(e)` is not contained in any edge of the triangle `T`;
* **(P5)** the declared traces are supported in `P_z` and kill the three triangle labels;
* **(P6)** no two complementary 3-sets both have positive angular measure (vacuous here).

Moreover **every** point of the plane is a `T`-triangle point, so the `T`-triangle locus is the
whole plane: it is not locally finite, is perfect, and has no isolated point.

*Proof.* `(P2)`: `floor(u + 3/2) - floor(u) = floor(x + 3/2) in {1,2}` for `u = n + x`,
`x in [0,1)`, and neither is `0 mod 3`. `(P3)`: the two-angle decomposition deviates from
`w +- pi/3` by at most `4d <= 4/50`; then `beta = 9(arg s - arg w)/(2pi)` lies in
`[1.3854, 1.6146]` or its negative, both inside `(1,2)` or `(-2,-1)`, where
`floor(u+beta) - floor(u) in {1,2}` (never `0 mod 3`). `(P4)-(P6)` are immediate because all
palettes are singletons in `O`. The full proof, with exact rational bounds
`333/106 < pi < 22/7` and two independent code paths, is `.ultramath/smwfo9zkl/m13/no-go.md`
and `model_check.py`; this synthesis re-verified the three inequalities independently
(`.scratch/sprintB/verify_m13.py`, all checks pass).

**Corollary 3.2.** The triangle case of Theorem 6.5 is not derivable at `k = 6` from the
palette-level hypotheses (P1)-(P6). Hence no proof of `(W)` can consist only of those
hypotheses plus the edge-trace argument.

**Delimitation.** (P1)-(P6) are exactly the palette-level consequences used in the printed
triangle case: the palette bound (Theorem A of `results/K6-BARRIER.md`), (5.7), the exact
transport (5.3) in the form Lemma 5.5 uses, the edge traces of Lemma 6.2, and the
complementary-triple exclusion of (5.2). The class contains the printed `k = 5` argument as a
theorem (at `k = 5` it proves separation at `min(delta_*, eps)`), so it is not a strawman.
It does not contain (5.2) in colouring form, because that is exactly the existence of a
6-colouring.

### 3b. The uniform palette-level no-go: every cycle length

The construction behind Theorem 3.1 generalises to a single template that kills **all four**
cycle lengths. Fix `ell in {3,4,5,6}` and let `M_0, M_1, M_2` be any partition of `[6]` into
three pairs, each of which avoids every edge of the cycle `C_ell`. Such partitions exist for
every `ell`; explicit choices:

| `ell` | `M_0` | `M_1` | `M_2` |
|---|---|---|---|
| 3 | {0,3} | {1,4} | {2,5} |
| 4 | {0,2} | {1,4} | {3,5} |
| 5 | {0,2} | {1,3} | {4,5} |
| 6 | {0,3} | {1,4} | {2,5} |

Fix `m >= 6` divisible by 3, `n = 6m`, `Delta = 2 pi/n`, `L = 2m/3`, and put

  `sigma(i) = M_{floor(i/L) mod 3}`,  `P_z(e^{i theta}) = sigma(floor(theta/Delta))`,

independent of `z`. Then:

1. every palette is one of the pairs `M_0, M_1, M_2`, so `|P| = 2` and no palette is contained in
   any edge of `C_ell`;
2. `P_z(e) cap P_z(Re) = empty` for every `e`: the shift by `pi/3` moves the sector index by `m`,
   and `m/L = 3/2`, so the block index changes by 1 or 2 mod 3, i.e. to a different, disjoint
   pair;
3. for every two centres at distance `d <= d_0 = pi/(9m)` the exact two-centre transport holds:
   the two unit decompositions of `(z'-z) + f` have arguments within `1.5938 d < Delta` of
   `arg f +- pi/3`, so the sector index moves by one of `m-1, m, m+1`, and on each of these six
   offsets the block index (hence the pair) changes by 1 or 2 mod 3, so the palettes are disjoint.
   Part 1 of `.ultramath/smwfo9zkl/m15/verify.py` checks the finite block statement in exact
   integer arithmetic for each `m`, and Part 2 the deviation bound in exact rational arithmetic;
4. for each edge `{i,i+1}` of `C_ell` and each pair `M_j`, the set `M_j \ {i,i+1}` is nonempty,
   so the trace `delta_b` for any `b` in it is supported in `M_j` and kills both edge labels;
   this gives (P5) at every centre;
5. the centres `y_k = (d_0/3) 2^{-k} (3/5, 4/5)` are distinct, converge to `0`, and every pair
   is at distance `< d_0`, so the transport exclusion holds between all of them.

Hence, for **every** `ell in {3,4,5,6}`, the palette-level hypotheses (palette bound, (5.7), the
exact local (5.3) transport, the edge exclusions of `C_ell`, the edge traces, and the
complementary-triple exclusion) admit a member whose `ell`-cycle locus is the whole plane and
accumulates at `0`. The triangle no-go of Theorem 3.1 is the special case `ell = 3` with a
different (singleton) palette field; the pair field above is a second, independent triangle
countermodel as well. So **the entire Theorem 6.5 is not a palette-level theorem at `k = 6`**,
not merely its triangle case. The full proof for `ell = 6`, with two independent verifiers, is
`.ultramath/smwfo9zkl/m15/construction.py` + `verify.py`; the partitions for the other three
lengths are checked in `sprint/k6/uniform_nogo.py`.

The pair field uses all six labels at every centre (the three pairs partition `[6]`), so it
violates even the non-proper form of self-avoidance: no label is absent from the palette. This
is in contrast with the singleton triangle model of Theorem 3.1, which does admit a non-proper
avoiding label (any label in `T`); both are killed by the proper form of self-avoidance
(Section 4).

## 4. The self-avoidance barrier

**Lemma 4.1 (self-avoidance).** Let `x` be a density-one point of its own colour class, with
`c(x) = i`. Then `i notin P_x(e)` for a.e. unit direction `e`.

*Proof.* Suppose `D = {e : i in P_x(e)}` has positive measure and let `e_0` be a density point
of `D`. Lemma 5.2(2) gives density zero of `A_i` at `x + e_0 + v` for every unit `v` nonparallel
to `e_0`. Take `v = -e_0 + delta` with `|delta - e_0| = 1` and `delta notin {0, 2e_0}`. Then
`x + e_0 + v = x + delta`, and the set of `delta` on that circle with `x + delta` a density-one
point of `A_i` is conull (the non-density set is plane-null, and Fubini applies to the circle).
So density one and density zero at the same point, a contradiction. `square`

This is genuinely different from the paper's constant-sequence trace, which only gives
`c(x+e) in P_x(e)` (the colour of the other endpoint). It is a consequence of the colouring, not
of the palette: it relates the palette at `x` to the colour of `x` itself.

**Corollary 4.2 (the model is not colouring-realizable).** In the model of Theorem 3.1, at every
centre `z` the palette takes all three values `{4}`, `{5}`, `{6}` on positive-measure direction
sets. So any label `i(z)` with `i(z) notin P_z(e)` a.e. must lie in `T = {1,2,3}`. If the model
came from a weak measurable 6-colouring `c`, Lemma 4.1 would give `c(z) in T` for a.e. `z`; then
`c` would be a proper 3-colouring of the plane (Lemma 4.3: density-one points of different classes
are disjoint, and unit pairs of typical points have different colours). But `chi(R^2) >= 4`
already follows from the Moser spindle, and the project's machine-checked bound is `>= 6`.
Contradiction. So the model violates the colouring-level constraints in the sharpest possible way.

**The frontier.** Any class of palette data that excludes the model must impose a constraint the
model violates; the only such constraint visible in the paper's framework is self-avoidance, and
self-avoidance with a *proper* label function already presupposes a 6-colouring. Thus:

* a proof of `(W)` from palette-level data is impossible (Theorem 3.1);
* a proof of `(W)` from data that includes a proper 6-colouring is a proof about 6-colourings,
  i.e. exactly the setting of the paper's Theorem 1.4;
* the model of Theorem 3.1 is the precise extremal object that any future argument must kill;
  `m13`'s structural check S4b shows that it satisfies (5.2) with the non-proper colouring `c=1`
  and non-proper self-avoidance with the same label, so the *only* constraint it fails is
  trace-consistency with a proper colouring (equivalently, maximality of the palettes). That is
  the exact frontier: the maximal palette field of a proper 6-colouring.

## 4b. The §8 strip layer is also powerless at `k = 6`

`m6` decides the angular-obstruction layer of §8 at six colours. The class `STRIP(k,ell)` is the
paper's strip data at a cyclic centre carrying a cycle of length `ell`: `S0` the sliver sets are
nonempty, `S1` the palette bound `1 <= |P| <= k-3`, `S2` the palette meets both one-sided allowed
sets `O(u)` and `I(u)` (Lemma 8.1 / (8.1)), `S3` `P(u) cap P(Ru) = empty` (Corollary 5.4), and
optionally `S4` the palette is not contained in a cycle edge (Lemma 6.2). Exhaustive decision
over the six `R`-orbit positions, two independent procedures:

  `STRIP(k,ell)` is UNSAT exactly for `(k,ell) in {(4,3), (4,4), (5,5)}`, and SAT otherwise.

The `(5,5)` row is exactly Proposition 8.2 (the five-cycle exclusion), which calibrates the
encoding; the `(4,*)` rows match the independently known emptiness of the k=4 architecture. For
**every** `k >= 6` and every `ell in {3,...,k}` the strip layer is satisfiable, with explicit
closed-form witnesses. At `k = 6`:

| `ell` | witness `P` | witness `Q` |
|---|---|---|
| 3 | {4} | {5} |
| 4 | {4} | {5} |
| 5 | {5} | {1,3} |
| 6 | {1,4} | {2,5} |

where the field alternates `P`/`Q` on the arcs `(r pi/3, (r+1) pi/3)`, `r` even/odd. So there is
no six-colour analogue of Proposition 8.2, the new `ell = 6` case is not decided by the strip
layer, and the four printed §8 cases each fail for the attributed reason (palette size 3 at
`ell=5`; the complement of `{X} u D` is a triple at `ell=4`; the outsider set has size 3 at
`ell=3`; no argument at all at `ell=6`). Full proof, exact rational certificates and the
`4 <= k <= 40` generalisation: `.ultramath/smwfo9zkl/m6/RESULTS.md`, `work/verify.py`.

**Together with Section 3, this closes the palette-level route at both ends**: the §6
cyclic-centre layer is dead (Theorem C, every length), and the §8 angular layer is dead
(`m6`, every length). A six-colour proof cannot be obtained by any refinement of the printed
palette data; it needs colouring-level input.

## 5. What the single-centre constraints say (exact counts)

At a typical cyclic centre of colour `i`, the following hold (`sprint/k6/STRUCTURE.md`):
palettes avoid `i`; consecutive `R`-palettes are disjoint; a ternary palette forces the next
`R`-palette to have size at most two; a singleton's label is outside the vertex set of every
cycle in `Gamma_x`; a disjoint pair of palettes with total size five at directions `120^circ`
apart would give a monochromatic unit sum, which is impossible. Exhaustive enumeration of all
six-tuples satisfying these constraints (`sprint/k6/orbit_correct.py`, exact integers):

| cycle length `ell` | centre colour | orbit words |
|---|---|---|
| 3 | in the cycle | 70194 |
| 3 | outside | 11888 |
| 4 | in the cycle | 18746 |
| 4 | outside | 2164 |
| 5 | in the cycle | 3720 |
| 5 | outside | 380 |
| 6 | in the cycle (all labels) | 510 |

At `ell = 6` there is no singleton; the all-pairs stratum has 150 words, the 2-periodic
`(3,2,3,2,3,2)` pattern has 6, and the remaining 354 have one or two ternary palettes. So the
single-centre constraints do not decide any cycle length, and none of them can prove `(W)`:
the cross-centre structure is essential. This is the quantitative form of the `k = 5` barrier
recorded in `results/K6-BARRIER.md`.

## 6. Finite computations cannot decide `k = 6`

The prior swarms decided the six-step interface CSP at `k = 6`: SAT for every length and every
ray geometry (`m5`/`m16`, 7848 instances, two independent decision procedures). `m16`'s shrink
lemma shows why: every "pair-satisfied" constraint is powerless, and the pair stratum is
satisfiable. `m10`'s current two-centre sweep (palettes at two centres, translation exclusion at
one displacement) is SAT on every probe. The reason is structural: a *finite* system of
two-centre constraints admits the 3-periodic pair model (shift the phase by one step at the
translated centre), so it cannot be UNSAT. The a.e.-in-angle form of (5.3) is equivalent to the
existence of a 6-colouring (`m8`), so the only finite object that could decide `k = 6` would
already be a 6-colouring. Step 3 of the sprint brief is therefore closed negatively: **no
decidable finite CSP at this level can prove `chi(R^2) >= 7`.**

## 7. Status ledger

| statement | status |
|---|---|
| §7 transfers at `k = 6` under `(W)` / `(F)` | proved, three independent audits; combinatorial core machine-checked |
| `L` nonempty and `sqrt 2`-dense for every `k` | proved (m5), independently re-derived |
| `(W)` is strictly weaker than local finiteness | proved (all three audits) |
| `(W)` for a weak measurable 6-colouring | **open** (the single remaining input) |
| triangle case of Thm 6.5 from palette-level hypotheses | **false** at `k = 6` (m13 model) |
| model is colouring-realizable | **false** (self-avoidance + `chi >= 4`) |
| `chi(R^2) >= 7` | **not proved** |
| `chi(R^2) <= 6` | **not proved** |

**The exact open target.** Prove `(W)`: exhibit `x_0` and `r > 0` with `L cap B(x_0,r) = {x_0}`
for every weak measurable 6-colouring, or exhibit a 6-colouring whose `L` has no isolated point.
By Theorem 1.1 the first would make §7 available at six colours; by Theorem 3.1 the existing
palette machinery cannot supply it; by Lemma 4.1 the first colouring-level constraint that the
extremal model fails is self-avoidance.
