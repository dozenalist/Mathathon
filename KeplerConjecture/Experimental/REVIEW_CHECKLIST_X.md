# Independent review checklist — X

For the frozen pair `K15-E014`/`K15-E015` (commit `8aca235e`, extended at this block) and
the Barlow result `K15-E013`. Each item is checkable in under a minute and each is a place
where a wrong assumption would silently produce a valid-looking certificate.

## A. Primary source and root identification

1. **Theorem locator.** arXiv:1002.1439v3, Section 2, Theorem 1 (printed p. 3) asserts that
   the Fig. 1 arrangement is optimal for 13 points, uniquely up to isometry, and that
   `d_13 = delta_13`. Confirm this is the statement we rely on; confirm we do **not** rely on
   any other theorem in the paper.
2. **Equations.** The Remark *preceding* Theorem 1 gives
   `2 tan(3pi/8 - a/4) = (1 - 2 cos a)/cos^2 a` and `cos d = cos a/(1 - cos a)`.
   Confirm both, character by character, especially the exponent `2` and the `a/4`.
3. **Transcription cross-check.** Solving those equations must give
   `a = 69.4050501037 deg` and `d = 57.1367030776 deg`, and the paper's own relation
   `alpha(d) = arccos(cos d/(1+cos d))` must return `a`. Confirm all three.
4. **Uniqueness/selection.** Confirm `g'(a) < 0` on `(0, pi/2)`: both terms
   `-(1/2)sec^2(3pi/8 - a/4)` and `-2 sin a (1-cos a)/cos^3 a` are strictly negative there
   (`sin > 0`, `cos > 0`, `1 - cos > 0`). Hence at most one root, and the sign change on
   `[12113/10000, 12114/10000]` pins it. Confirm no root is being silently ignored.
5. **Dependency.** Confirm that `d_13 = delta_13` is the computer-assisted step and that our
   certificate covers only the arithmetic of the constant.

## B. Rational `pi` and trigonometric bounds

6. **`pi` enclosure.** `333/106 < pi < 355/113`. Verify both inequalities exactly
   (standard continued-fraction convergents); no decimal is used.
7. **Taylor remainder lemma.** For `0 <= x <= 8/5` and `N >= 2`, remainder bounded by the
   first omitted term. Check the ratio computation: `t_k/t_{k-1} = x^2/((2k-1)(2k)) < 1`
   requires `x^2 < (2k-1)(2k)`, true for `k >= 2` since `x^2 <= 2.56 < 12`. Confirm the
   Leibniz criterion is being applied to a tail that starts at `N = 28 >= 2`, and that all
   evaluated arguments are `< 1.6`: `a_hi = 1.2114`, `3pi/8 - a/4 <= 0.8753`, and the
   degree-conversion bisection which runs up to `1.57`.
8. **Sine series separately.** Confirm `s_k/s_{k-1} = x^2/((2k)(2k+1)) < 1` for `k >= 1`
   since `(2k)(2k+1) >= 6 > 2.56`. The sine case has a different turning point; check it was
   not simply copied from the cosine case.

## C. Interval direction assumptions (the highest-risk items)

9. **`cos` monotonicity.** `cos_iv(lo,hi)` returns `[cos(hi), cos(lo)]`. Confirm `lo <= hi`
   and `hi < pi/2` always hold at the call sites.
10. **`sin` monotonicity.** `sin_iv(lo,hi)` returns `[sin(lo), sin(hi)]`. Confirm arguments
    are in `[0, pi/2)`.
11. **`tan` monotonicity.** `tan_iv` is called on the interval
    `[3pi/8 - a_hi/4, 3pi/8 - a_lo/4]` **in the correct order** (subtracting `hi` gives the
    lower endpoint). Confirm the endpoints are not swapped; a swap would invert the
    enclosure silently and still produce a plausible number.
12. **Interval division.** `Iv.inv` asserts the divisor does not contain `0`. Confirm
    `cos a > 0` on every interval divided by, in particular `cos^2 a` and `cos^3 a`.
13. **`g` enclosure.** `g_iv(lo,hi)` takes `lhs` from `tan` over the arg-interval and `rhs`
    from `cos_iv(lo,hi)`; confirm both are enclosures on the *same* interval `[lo,hi]` and
    that the subtraction `lhs - rhs` is the correct directed form (`[lhs.lo - rhs.hi,
    lhs.hi - rhs.lo]`).
14. **Comparison in cos-space.** `d < arccos(thr)` iff `h(a_hi) > thr`, using `h` increasing,
    `h(a)` decreasing in `a`, `arccos` decreasing. Confirm the composition of three
    monotonicities gives the claimed direction, and that using `a_hi` (upper bound on `a*`)
    rather than `a_lo` is correct.
15. **`h` enclosure.** `h_lo_val = c_lo/(1 - c_lo)` with `c_lo` a *lower* bound for
    `cos(a_hi)`. Confirm `h` is increasing in `c` so a lower bound on `c` gives a lower
    bound on `h`, and that the comparison `h_lo_val > thr` is therefore the right direction.

## D. Barlow result (`K15-E013`)

16. The open shell is `(2, 2 sqrt2)`. Confirm the two computations: adjacent-layer
    `|u+delta|^2 = 4/3` gives `4/3 + 8/3 = 4` (distance `2`), and `16/3` gives
    `16/3 + 8/3 = 8` (distance `2 sqrt2`). Confirm no lattice point of the triangular
    lattice lies at an intermediate `|u+delta|^2` in `(4/3, 16/3)`.
17. Confirm `2.09 < 2 sqrt2 = 2.8284271`, and that in-plane (`2`, `2 sqrt3`) and
    two-layers-away (`2h = 3.266`) values are all `>= 2 sqrt2`.
18. Confirm the argument is uniform over the stacking word: the interlayer geometry depends
    only on "adjacent layer offset into a hollow", not on which hollow.

## E. Numeric fixtures (verify, do not trust)

19. `centre_cell_volume = 5.5502910285155` must reproduce in every completion run — it is the
    control that the core was not perturbed.
20. Every accepted configuration must have `minsep >= 2`. The scripts report this; check it
    was actually enforced against the *core*, not only among added points (this was a real
    bug in an earlier version).
21. The computed sums (`8.17`–`8.32` per cell) are **upper** bounds and must not be quoted
    as evidence for or against `(T')`. Confirm no document does so.
