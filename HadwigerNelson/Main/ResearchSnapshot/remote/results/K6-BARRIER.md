# Why the method stops at five labels (and what a six-colour proof would need)

**Corrections (added after the third swarm).** (i) §2 below overstates the §7 failure: the
one-skeleton map is label-blind (Lemma 7.3 plus the cliques in the forest), so the positive-coordinate
cover has multiplicity at most two at *every* `k`, and the only `k`-dependent ingredient of §7 is the
local finiteness of cyclic centres. (ii) §3's bound `|A(e)| <= k - 4` is **false**: a palette equal
to the whole outsider set `T^c` gives `|A| = 3` at `k = 6`, and such palettes are admissible in all
216 geometries at `l = 4`. (iii) The deeper obstruction is that Proposition 7.1 itself is a
`k = 5` statement: its proof uses Theorem 6.5, whose triangle case needs `|P| <= 2 = 5 - 3`. So at
`k = 6` a colouring is not even known to have an interface.

**Status: analysis, not a theorem about `chi(R^2)`.** It shows that the printed argument of the
paper is a `k <= 5` argument: two of its inferences are false as stated at `k = 6`. It does not
show that six colours are possible, nor that `chi(R^2) != 7`.

Throughout, `k` is the number of labels, `P_x(e) ⊂ {1,...,k}` is the maximal palette at centre
`x` in direction `e` (paper, Definition 5.1), `R` is rotation by `pi/3`, and `sigma` is angular
measure on `S^1`.

## 1. The palette bound for general k

**Proposition (general-k palette bound).** For every weak measurable `k`-colouring with `k >= 3`,
and every centre `x`,
`1 <= |P_x(e)| <= k − 3` for `sigma`-almost every `e`.

*Proof.* The lower bound is the paper's. For the upper bound, suppose `|P_x(e)| >= k − 2` on a
set `B` of positive angular measure. There are finitely many `(k−2)`-element subsets of the label
set, so some fixed `A` with `|A| = k − 2` is contained in `P_x(e)` for all `e` in a
positive-measure subset of `B`. Paper (5.2) and Fubini give that, for almost every such `e`, the
exact circle `v ↦ x + e + v` is coloured, almost everywhere, by the complement `{1,...,k} \\ A`,
which has exactly two elements. Hence the palette at the centre `x + e` meets that pair; paper
(5.7) (`P_x(f) ∩ P_x(Rf) = empty`) forces it to be a singleton, alternating at an `R`-step: the
centre `x + e` is *binary* for that fixed pair. Lemma 5.5 (binary-centre separation) then makes
`{x + e : e ∈ B}` uniformly separated, hence finite; but it is the image of a positive-measure set
of directions under an injective map into a compact circle, a contradiction. ∎

At `k = 5` this is Proposition 5.6 (`k − 3 = 2`), which is what §5.4 and §6 use. At `k = 6` it
gives only `|P_x(e)| <= 3`.

The bound is sharp at `k = 5` in the only sense the argument needs: it is exactly the statement
that a palette is a pair. It is *not* a statement about colourings of the circle: the unit-distance
graph on a circle of radius one is a disjoint union of six-cycles, hence 2-colourable (verified
numerically, zero violations over `10^6` unit chords), so a centre whose circle is coloured by a
*triple* is not by itself contradictory.

## 2. Why three labels in a palette break §7

The disk-averaging construction of §7 turns the colouring into a continuous map into the geometric
realisation of the complete graph on the labels. The paper states this in the form "these modified
vectors have at most two positive coordinates, so they lie in the complete graph on the five
labels" — that is, the target is the **one**-skeleton of a simplex, and the covering argument that
follows (Lemma 7.5) has the hypothesis *multiplicity at most two* and *mesh at most two*:

> Lemma 7.5. A closed square of side ten has no relatively open cover of multiplicity at most two
> and mesh at most two.

Both hypotheses are essential. Multiplicity three cannot be excluded: a cover of the square by
tiny disks has mesh tending to zero and multiplicity one. So if palettes can carry three labels,
the smoothed vectors can have three positive coordinates, the component cover can have multiplicity
three, and Lemma 7.5 does not apply. The obstruction genuinely fails at `k = 6`; this is not a
matter of constants.

Precisely where it fails matters. The cover lemma itself is blind to the number of labels: a point
of the metric graph on `k` vertices has at most two positive barycentric coordinates for *every*
`k`, and a swarm audit (m3) proves the cover obstruction for any `k` with the constant `R`, not
`2`. What fails at `k = 6` is the *passage from labels to the graph*: with three positive labels
at a palette the thresholded vector has three positive coordinates, which is not a point of the
graph space but of the two-skeleton of the simplex. So the k-dependence is entirely in Proposition
5.6, not in §7.

## 3. A second, independent failure: the triangle interface

At a length-three interface (paper, Proposition 7.1), let `T` be the three cycle labels and put
`A(e) = P_x(e) ∩ (I \\ T)`, the set of *outsiders* present at direction `e`. The paper's §8.4 and
§8.6 need `A(e)` to be a singleton: "a three-cycle forces six alternating sectors for the two
outside labels". The general bound is `1 <= |A(e)| <= k − 4`, so it is a singleton exactly when
`k = 5`; at `k = 6` it can be a two-element set of the three outsiders, and the state has six values
rather than two. The detailed state analysis — including the claim that the resulting disjointness
graph is non-bipartite — is in the swarm artifact
`.ultramath/smwfcr56i/m2/k6_nogo.md` (Theorems B and C and their certificates); I have checked the
count `k − 4` and the count `k − 3`, not every state transition.

## 4. The third k-dependent input: a new cycle length

Proposition 7.1 supplies a simple cycle of the complete graph on the label set, of length
`ell` with `3 <= ell <= k`. At `k = 5` the lengths are `3, 4, 5` and the paper excludes each. At
`k = 6` there is a fourth case, `ell = 6`, for which the paper contains no argument. The cycle
exclusions of §8 are where a six-label proof would have to do genuinely new work: the five-cycle
argument uses that five signs split into one positive and one negative run (a count specific to
five), the four-cycle argument uses a parity rule on two diagonals, and the three-cycle argument
uses a two-element outside set.

## 5. Conclusion

The architecture decomposes as

* a `k`-independent transfer (Sections 2–4), which is where the mathematical novelty lies;
* a `k`-dependent geometric obstruction (Sections 5–8), which is a proof for `k = 5` and only for
  `k = 5`.

A proof of `chi(R^2) >= 7` by this route needs at least one of:

1. a palette bound `|P_x(e)| <= 2` for six-colourings, proved by an argument that does not pass
   through the complement of a `(k−2)`-set (the printed one cannot, since the complement is a
   triple and ternary circles exist);
2. a replacement for Lemma 7.5 that handles multiplicity three on the two-skeleton of a simplex
   (the planar-cover obstruction would have to become a `2`-dimensional obstruction);
3. an exclusion of six-cycles, together with the state analysis at triangle and square interfaces
   at `k = 6`.

Conversely, a proof of `chi(R^2) <= 6` must exhibit a proper six-colouring, and by Theorem 1.3 of
the paper (and `results/T1-algebraic-plane.md`) it is enough to colour the countable algebraic
plane `E` — but `E` is exactly the graph on which the transfer and the rigidity theorem operate, so
no measurability or regularity shortcut is available.
