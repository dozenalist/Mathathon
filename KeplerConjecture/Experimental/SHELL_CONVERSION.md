# Thin-shell counting: repairing the cap inequality and converting radii

Role E (Experimental). Claims `K15-E010` (cap direction, **PROVED**),
`K15-E011` (radius conversion, **PROVED**), `K15-E012` (explicit thin-shell bound,
**PROVISIONAL** — depends on an unverified external constant). Reviewer: X.
Script: `Experimental/scripts/shell_conversion.py` (exact arithmetic, <1 s, output in
`Experimental/evidence/shell_conversion.txt`).

Source context: Main `K15-C013` at `a08f378be6a03f80ac075b34f8ba99aeb8201d9e`,
`Main/CLAIMS.md` lines 236–260. The review of 27616 reports that C013's cap inequality
has its direction reversed. That is correct, and the repair is below.

## K15-E010 — the cap inequality, with the direction fixed

**Statement (PROVED).** Let `theta` be the minimal angular separation of `k` points on
`S^2`. Then the spherical caps of angular radius `theta/2` about them are disjoint, each
has area `2pi(1 - cos(theta/2))`, so

```
k * 2pi(1 - cos(theta/2)) <= 4pi     <=>     theta <= 2 arccos(1 - 2/k).
```

This is an **upper** bound on `theta`. For `k = 13` it gives
`theta <= 2 arccos(11/13) = 1.12413960601... rad = 64.40845... deg`, and the identity is
exact: `13 * 2pi * (1 - 11/13) = 4pi` with ratio `1` (verified symbolically).

**What C013 said and why it is wrong.** C013's *Open* bullet reads "the crude
spherical-cap area bound ... only forces `theta >= 64.4 deg`, whereas one needs
`theta > 57.1 deg`". The bound is an upper bound on `theta`, not a lower bound; and the
conclusion that it "gives nothing" is right for a different reason than the one given.
The correct diagnosis is:

> The forced lower bound from the radius conversion (see `K15-E011`) is
> `theta >= arccos(1 - 2/(2+delta)^2)`, which is **decreasing** in `delta` and equals
> `60 deg` at `delta = 0`. Hence it never exceeds `60 deg`, while the cap bound only
> says `theta <= 64.408 deg`. Since `64.408 > 60`, no value of `delta >= 0` can produce
> a contradiction from the cap bound. The cap bound is vacuous here **because it is too
> weak an upper bound**, not because it is a lower bound.

## K15-E011 — radius conversion, corrected for wide shells

**Correction accepted (hourly review 2026-11-14 00:08).** My previous version asserted
`cos theta <= 1 - 2/(2+delta)^2` for all `delta >= 0`. That is false for wide shells.

**Statement (PROVED).** Let `y, z` have `|y|, |z| in [2, R]` with `R = 2 + delta` and
`|y - z| >= 2`, and let `theta` be the angle at the origin. By the law of cosines
`cos theta <= f(r,s) := (r^2+s^2-4)/(2rs)` with `r = |y|, s = |z|`. On the square
`[2,R]^2` the maximum of `f` is attained on the boundary, and

```
f(R,R) = 1 - 2/R^2 ,        f(2,R) = f(R,2) = R/4 ,
```

so

```
cos theta <= max( 1 - 2/R^2 , R/4 ),    theta >= arccos( max(1 - 2/R^2, R/4) ).
```

The comparison is exact:

```
1 - 2/R^2 >= R/4   <=>   R^3 - 4R^2 + 8 <= 0   <=>   (R-2)(R^2-2R-4) <= 0
                    <=>   2 <= R <= 1 + sqrt5 .
```

**Allowed range for the equal-radius formula.** Hence

```
cos theta <= 1 - 2/(2+delta)^2     is valid exactly for   0 <= delta <= sqrt5 - 1 = 1.2360679...
```

and **not** beyond. For `delta > sqrt5 - 1` the binding pair is one centre at radius `2`
and the other at radius `2+delta`, and the bound becomes `cos theta <= (2+delta)/4`.

**The counterexample that killed the old statement.** At `delta = 2` (`R = 4`) the two
bounds read `1 - 2/16 = 0.875` and `4/4 = 1`. Two centres at radii `2` and `4` on the same
ray have separation exactly `2` and angle `0`, so `cos theta = 1 = R/4`; the equal-radius
value `0.875 < 1` would wrongly assert `theta >= 29.0 deg`. This is the review's example
and it is decisive.

**Consequence at the radii we use.** Every thin-shell statement below uses
`delta <= 0.09 < sqrt5 - 1`, so the equal-radius formula is available there. The range
restriction is recorded so the lemma is not misapplied to thick shells.

**Necessary-condition status.** `max(1-2/R^2, R/4)` is the *weakest* per-pair constraint
over the shell, so `theta >= arccos(max(...))` holds for every configuration in the
shell and may be used as a necessary condition. Both functions are decreasing where they
bind, and the maximum of two decreasing functions is decreasing.

## K15-E012 — explicit thin-shell bound (PROVISIONAL)

**Statement.** Let `theta_13^+` be a certified upper bound for the minimal angular
separation of 13 points on `S^2`. Then for `delta` in the range where the equal-radius
formula applies,

```
delta < delta_0 := sqrt( 2 / (1 - cos theta_13^+) ) - 2
```

every 2-separated set has **at most 12** points in the closed shell `[2, 2+delta]`.

*Proof.* 13 points in the shell would be `theta`-separated with
`theta >= arccos(1 - 2/(2+delta)^2)` by `K15-E011`, and `theta <= theta_13^+` by
definition. Contradiction whenever `arccos(1-2/(2+delta)^2) > theta_13^+`, which
rearranges to the displayed inequality because both sides are decreasing. ∎

**Status: PROVISIONAL.** `delta_0 = 0.0911455` was computed from the *rounded* value
`57.1367 deg`, and a rounded decimal is **not** an upper enclosure. The correct input is a
directed enclosure from Musin–Tarasov; see `Experimental/SHELL_2P09.md`, which replaces
this provisional statement by the specific choice `rho = 209/100`.

## Comparison with the existing unconditional bound (C013(a))

C013(a) gives `n <= (3+delta)^3 - 1`, unconditionally. At the exact crossing
`delta = 28^(1/3) - 3 = 0.0365889718757` one has `(3+delta)^3 = 28` identically
(verified to `1e-12`), so `n <= 27`. That is unconditional and needs no spherical-code
input, but 27 is far weaker than 12. The review's repair ("replace rounded
`delta < 0.0366` by `delta < 28^(1/3) - 3`") is therefore purely a precision fix; the
substantive improvement from 27 to 12 requires `K15-E012` and its Tammes input.

Note also that C013(a) is vacuous for `n <= 12`: `13^(1/3) - 3 = -0.6487 < 0`. The
volume count can never produce a 12-shell; a count bound, not a volume bound, is
genuinely required, as C013's own reviewer note says.

## Equality fixtures (FCC / HCP / Barlow)

The bound "at most 12 centres in `[2, 2+delta]`" must be satisfied by the whole equality
family, otherwise it is wrong. In FCC and in HCP a centre has exactly 12 neighbours at
distance `2` and the next shell at `2 sqrt 2 = 2.8284271`, so the 12-count holds for
every `delta < 2 sqrt 2 - 2 = 0.8284271`, comfortably above `delta_0`. Equilibrium is
therefore not disturbed by the bound, and `K15-E012` does not exclude any packing that
attains `pi/sqrt(18)`.

**Scope caveat.** Barlow stackings are not analysed here; a stacking with an unusually
short next shell could in principle have more than 12 centres inside `[2, 2.09]`. That
is a concrete finite question for C/X (`CLAIMS_FOR_X.md`, `K15-E013`), and it must be
settled before the bound is used. I make no claim about it in this block.
