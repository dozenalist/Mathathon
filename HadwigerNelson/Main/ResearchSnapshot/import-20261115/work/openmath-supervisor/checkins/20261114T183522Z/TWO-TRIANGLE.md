# Referee-derived: the supplied input package forces a two-equilateral-triangle configuration
# and eliminates 4 and 5 distinct approach directions

**Status: REFEREE-DERIVED, NOT MEMBER-DELIVERED, NOT INDEPENDENTLY VERIFIED.** It arose while
refereeing m1's second submission (swarm smwgphe8q, direction d1, second rejection). The main
step is a one-line consequence of inputs the person supplied, so treat it as needing an
independent check before it goes anywhere. Exact arithmetic checks are in
`referee_check3.py` and the witnesses below were recomputed exactly.

## Setting

Six slots `i in Z/6` carry the interfaces `E_i = {i, i+1} subset Fin 6`; weak colouring `c`,
`k = 6`. Continua `K_i` approach one centre `x` in signed unit directions `v_i`. Supplied input:

* (C1) CC60: every closed arc of length `pi/3` has label union `<= 3`.
* (C2) MC120(a): a label union of size `>= 5` cannot fit a STRICT cone of width `< 120 deg`.
* (C3) MC120(b): a subset with residual exactly 2 colours (label union of size 4) cannot have a
  common positive OUTER arc wider than `60 deg`.

## Lemma 1 (the reduction)

(C1)-(C3) hold **iff** every one of the nine non-consecutive (prism) pairs satisfies
`dist(v_i, v_j) >= 120 deg`.

*Proof.* (=>) Take a non-consecutive pair `{i,j}`. Then `|E_i union E_j| = 4` (exhaustive check:
`|union| <= 3` iff the pair is cyclically consecutive), so its residual is exactly 2 colours.
The common positive outer arc of the pair has measure `pi - span(v_i,v_j)` when the directions
differ and `pi` when they coincide, so (C3) gives `span >= 120 deg`, i.e. `dist >= 120`.
(<=) If all prism pairs are `>= 120 deg`: any set of slots with label union `>= 4` has at least
two slots and — since any three slots contain a non-consecutive pair, `C_6` being triangle-free —
contains a non-consecutive pair, so its span is `>= 120 deg`; this gives (C2) and (C3). And a
closed `pi/3` arc holding two non-consecutive slots would give distance `<= 60 < 120`, so (C1). QED

## Theorem (the classification)

Under (C1)-(C3) there are `theta in T` and `delta in [0, 120 deg]` with

    v_i = theta + 120 deg * floor(i/2) + delta * (i mod 2)      (i = 0..5),

up to the mirror symmetry `i -> -i`. The number of distinct directions is **3** when
`delta = 0` or `delta = 120 deg`, and **6** when `0 < delta < 120 deg`. In particular
**4 and 5 distinct approach directions are impossible.**

*Proof.* The triples `{0,2,4}` and `{1,3,5}` are pairwise non-consecutive, so by Lemma 1 each is
an equilateral triple: three points cutting the circle into arcs `g_1+g_2+g_3 = 360` with
`min(g_k, 360-g_k) >= 120` forces every `g_k >= 120`, hence all exactly 120. Writing the first as
`theta, theta+120, theta+240` and the second as `theta+delta, theta+delta+120, theta+delta+240`,
the matching pair `{0,3}` gives `dist(0, delta+120) >= 120`, i.e. `delta in [0,120]`. The other two
matching pairs then hold automatically. Distinctness follows from the formula. QED

## Consequences

1. The paired configuration (`delta = 0` or `120`) is the exact equilateral `120 deg` case, which
   matches the supplied statement that three paired directions force exact equilateral `120`.
2. `delta = 60 deg` is the regular hexagon, i.e. the alternating grid — a member of the family.
3. The family is 1-parameter, so no arc of directions is excluded outright; what is excluded is
   **de-pairing into an odd number of clusters**: 4 and 5 distinct directions do not occur.
4. Therefore m1's T3 family is a genuine CC60 family, but only its diagonal `a = b = c` survives
   (C3). Its off-diagonal points are excluded, with exact witnesses:
   `(pi/4,0,0)` pair `{1,3}` distance 75 deg, outer arc 105 deg, residual `{0,5}`;
   `(0,pi/4,0)` pair `{3,5}` and `(0,0,pi/4)` pair `{1,5}`, same numbers.

## Caution recorded from this block

Computing the span of a cluster union is not the same as computing a pairwise distance: in m1's
family the far cluster pins `span{0, 240, 240+c}` at exactly 120 deg even though
`dist(0, 240+c) = 120 - c`. I first read the MC120(a) condition as violated by that pair distance
and was wrong; the exact span computation corrected it. Any future check of these conditions must
compute the minimal containing arc, not a pair distance.
