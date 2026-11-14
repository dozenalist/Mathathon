# Three necessary conditions at a six-colour cyclic centre

**Status.** Theorems, proved below from the paper's hypotheses ((5.2), (5.7), Lemma 4.3,
Lemma 5.2(2), Definition 6.1, Lemma 6.2). They are new at `k = 6` in the sense that at `k = 5`
they are vacuous or automatic. They do **not** prove local finiteness; they sharpen what a
counterexample or a proof must satisfy, and they already rule out one of the three `k = 5`
mechanisms at the six-cycle.

Notation as in `TRANSFER.md`: `c` is a weak measurable `k`-colouring, `P_x(e)` the maximal
palette, `R` rotation of directions by `kappa = pi/3`, `A_i` the colour class of `i`, and
`H_i` its closed essential support. A point `x` is **typical** if it is a density-one point of
its own colour class; typical points are conull (Lemma 4.3).

## Lemma 1 (self-avoidance)

Let `x` be typical, with `c(x) = i`. Then

  `sigma({e in S : i in P_x(e)}) = 0.`

That is: **a typical point's own colour is absent from its palette almost everywhere.**

*Proof.* Put `D = {e : i in P_x(e)}` and suppose `sigma(D) > 0`. Let `e_0` be a density-one
point of `D`. By Lemma 5.2(2) (applied to the label `i` and the centre `x`), for every unit `v`
nonparallel to `e_0` the spatial density of `A_i` at `x + e_0 + v` is zero.

Let `C = {delta in S : |delta - e_0| = 1}` be the unit circle of the `delta`-plane centred at
`e_0`, and for `delta in C` put `v(delta) = -e_0 + delta`, a unit vector. Then
`v(delta) = e_0` iff `delta = 2e_0`, and `v(delta) = -e_0` iff `delta = 0`; so for all but two
`delta in C`, `v(delta)` is a unit vector nonparallel to `e_0`. For each such `delta`,
`x + e_0 + v(delta) = x + delta`, so the density of `A_i` at `x + delta` is zero.

On the other hand, the set `N` of non-density-one points of `A_i` is plane-null. For the fixed
circle `C` (a translate of the unit circle), `N cap C` is null in the one-dimensional measure:
this is Fubini applied to the family of translates of `C`. Hence for a.e. `delta in C`, and in
particular for some `delta not in {0, 2e_0}`, the point `x + delta` is a density-one point of
`A_i`. That contradicts density zero. `square`

**Remark.** The paper's constant-sequence trace only gives `c(x+e) in P_x(e)` (the colour of the
*other* endpoint). Lemma 1 is the statement for the centre itself, and it is genuinely different:
it says the colour of `x` never reappears at distance exactly one near `x` in a palette-visible
way.

## Lemma 2 (a ternary palette forces the next R-palette to have size at most two)

Let `x` be typical with `c(x) = i`. If `|P_x(e)| = 3` for `e` in a set `E` of positive angular
measure, then for a.e. `e in E`,

  `|P_x(Re)| <= 2`,  and in fact  `P_x(Re) subseteq [k] \ (P_x(e) union {i})`.

*Proof.* Let `A = P_x(e)`, a 3-set with `i notin A` (Lemma 1). By (5.7), `P_x(Re) cap A = empty`;
by Lemma 1, `i notin P_x(Re)`. Hence `P_x(Re) subseteq [k] \ (A union {i})`, which has
`k - 4 = 2` elements. `square`

## Lemma 3 (singletons avoid the cycle labels)

Let `x` be any centre (typical or not) and suppose `Gamma_x` contains a simple cycle `C` with
vertex set `V(C)`. If `P_x(e) = {b}` is a singleton, then `b notin V(C)`.

*Proof.* Let `uv` be any edge of `C` with `b in {u,v}` (one exists, since `b in V(C)` lies on some
edge). By Lemma 6.2, applied to the edge `uv in Gamma_x`, there is a trace `b^{uv} in W_x` with
`b^{uv}_u = b^{uv}_v = 0` almost everywhere and `sum_l b^{uv}_l = 1` almost everywhere. Every
trace is supported in the palette (Definition 5.1 and the paragraph after it), so
`supp b^{uv}(e) subseteq P_x(e) = {b} subseteq {u,v}`, and `b^{uv}(e)` vanishes at `e` on a set
of full angular measure. So `b^{uv}(e) = 0` a.e., contradicting `sum = 1`. `square`

**Corollary 4 (six-cycles have no singletons).** At a 6-cycle locus, `V(C) = [6]`, so no palette
is a singleton. More generally, at a triangle the singletons lie in the three outsiders; at a
four-cycle in the two outsiders; at a five-cycle in the single outsider.

## Theorem 5 (orbit structure at a typical cyclic centre)

Let `x` be typical with `c(x) = i`, and suppose `Gamma_x` contains a simple cycle of length
`ell`. Then, for a.e. `e`, the six palettes `P_j = P_x(R^j e)` satisfy:

1. `i notin P_j` for all `j` (Lemma 1);
2. `P_j cap P_{j+1} = empty` (5.7);
3. `|P_j| = 3 => |P_{j+1}| <= 2` (Lemma 2);
4. `|P_j| = 1, P_j = {b} => b notin V(C)` (Lemma 3);
5. `|P_j| + |P_{j+2}| = 5` and `P_j cap P_{j+2} = empty` is **impossible**
   (a unit-sum monochromatic contradiction: see Lemma 6);
6. no two of the six are complementary 3-sets (the (C1) complementary-palette exclusion of
   `results/continuation/L4-SYNTHESIS.md` §4b, itself a consequence of (5.2));
7. at most three of the six are ternary (the orbit bound (C2), `sigma({|P| = 3}) <= pi`).

*Proof.* Items 1-4 are Lemmas 1-3. Item 5 is Lemma 6. Item 6 is Theorem 1 of the m6 note
(`.ultramath/smwfhd5sl/m6/proof.md`), whose proof uses (5.2) on the positive-measure product set
`{P = A} x {P = A^c}`. Item 7 is Theorem 2 of the same note. `square`

## Lemma 6 (monochromatic unit sums)

Let `x` be typical with `c(x) = i`. Let `U, V` be measurable sets of directions and suppose

  `P_x(u) = A` for `u in U`,  `P_x(v) = B` for `v in V`,  `A cap B = empty`,  `|A| + |B| = 5`,
  `i notin A union B`.

Then there is no pair `(u_0,v_0)` of **density points** of `U` and `V` with `|u_0+v_0| = 1`.
Equivalently, the set of such pairs has one-dimensional measure zero.

*Proof.* Suppose `u_0` is a density point of `U` and `v_0` a density point of `V`, with
`|u_0 + v_0| = 1`. Then `u_0, v_0` are nonparallel (their sum is a unit vector, so the angle
between them is 120°, not 0 or pi), and the sum map `(u,v) -> x+u+v` is a local diffeomorphism
at `(u_0,v_0)` (Jacobian `sin(arg v_0 - arg u_0) != 0`). For a.e. `(u,v)` in a neighbourhood
inside `U x V`, (5.2) gives `c(x+u+v) notin A union B = [k] \ {i}` (the last equality because
`|A|+|B| = 5 = k-1` and `i` is in neither). So `c = i` a.e. on the image, and the image has
density one at `z = x+u_0+v_0` (a local diffeomorphism carries sets of density one to sets of
density one). Thus `z` is a density-one point of `A_i`, and `|z - x| = 1`. But `x` is also a
density-one point of `A_i`, contradicting Lemma 4.3. `square`

## What the constraints leave open (exact counts)

`sprint/k6/orbit_correct.py` enumerates, for each `ell`, all six-tuples of palettes satisfying
1-7 above over all labels. `sprint/k6/orbit_correct_v2.py` recomputes the same counts by a
transfer-matrix trace (a different algorithm, no shared code); the counts agree exactly, and the
(C1)/(MON) filters cut nothing on the transition-admissible stratum. Counts:

| `ell` | colour of `x` | admissible palettes per position | orbit words |
|---|---|---|---|
| 3 | in the cycle | 22 | 70194 |
| 3 | outside | 19 | 11888 |
| 4 | in the cycle | 20 | 18746 |
| 4 | outside | 17 | 2164 |
| 5 | in the cycle | 18 | 3720 |
| 5 | outside | 15 | 380 |
| 6 | in the cycle (all labels) | 16 | 510 |

All `ell = 6` words have every palette of size 2 or 3, no singleton; the all-pairs stratum has
150 words, the `(3,2,3,2,3,2)` pattern has exactly 6 (the 2-periodic `A, [6]\(A union {i}),
A, ...`), and there are 354 further words with one or two ternary palettes. So the single-centre
orbit constraints do **not** decide any cycle length; local finiteness needs the cross-centre
structure.

## Consequence for the six-cycle case

At a typical 6-cycle centre, Lemma 3 forbids singletons. The `k = 5` five-cycle argument of
`§8.2` cannot be replayed: it uses that every palette is a pair meeting two slivers, and at
`k = 6` a palette can be ternary. What survives is the all-pairs stratum (150 orbit words), where
the state space is the 15 pairs of `[6]` and the trace-domination inequality of Lemma 6.6
generalises (for a pair `A = {a,b}`, `1{P_x = A} <= sum_{uv in C, a in uv, b notin uv} b^{uv}_b`).
That gives continuity of the pair state along the 6-cycle locus at typical points, but the
transport step of §6.3.2 loses one label: two disjoint pairs leave a **two**-element complement,
not the singleton `X` of `k = 5`, so the density-one transport rule does not close.
