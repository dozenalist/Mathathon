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

## K15-E011 — radius conversion without putting centres on one sphere

**Statement (PROVED).** Let `y, z` be two points with `|y|, |z| in [2, 2+delta]` and
`|y - z| >= 2`, and let `theta` be the angle at the origin. By the law of cosines

```
4 <= |y|^2 + |z|^2 - 2|y||z| cos(theta),   i.e.   cos(theta) <= (r^2 + s^2 - 4)/(2rs)
```

for `r = |y|, s = |z|`. Writing `t = max(r,s) <= 2+delta`, the right-hand side is
maximised when `r = s = t`, where it equals `1 - 2/t^2`, and `d/dt (1 - 2/t^2) = 4/t^3 > 0`.

**Consequence, stated as a necessary condition.** No assumption that the centres share a
sphere is needed. Because `(r^2+s^2-4)/(2rs) <= 1 - 2/(2+delta)^2` for all admissible
`r, s`, every pair in the shell satisfies

```
theta >= theta_min(delta) := arccos( 1 - 2/(2+delta)^2 ).
```

`theta_min` is strictly decreasing on `[0, inf)`, with `theta_min(0) = 60 deg` and
`theta_min(delta) -> 0` as `delta -> inf`. This is the exact conversion the assignment
asks for: it is a bound on the angle in terms of the *largest* radius in the shell, and
mixed-radius configurations only make the constraint weaker, so using
`theta_min(delta)` is valid (necessary) for every configuration in the shell.

## K15-E012 — an explicit thin-shell count (PROVISIONAL)

**Statement.** Fix `theta_13` an upper bound for the minimal angular separation of 13
points on `S^2` (the Tammes `N = 13` value). Then for

```
delta < delta_0 := sqrt( 2 / (1 - cos theta_13) ) - 2
```

every 2-separated set has **at most 12** points in the closed shell `[2, 2+delta]` about
any centre.

*Proof.* If 13 points lay in the shell, they would be `theta`-separated with
`theta >= theta_min(delta)` by `K15-E011`, and `theta <= theta_13` by definition of
`theta_13`. So the claim holds whenever `theta_min(delta) > theta_13`, which rearranges
to the displayed inequality because `theta_min` is strictly decreasing. ∎

**Numerical status.** With the commonly quoted `theta_13 = 57.1367 deg` (Tammes
`N = 13`) this gives `delta_0 = 0.0911455`. With the cap bound of `K15-E010`
(`64.408 deg`) the formula gives `delta_0 = -0.1236 < 0`, i.e. no information, exactly
matching the diagnosis above.

**This is PROVISIONAL, and the reason is explicit.** I did **not** verify the value
`57.1367 deg` from a primary source in this block. The conversion, the monotonicity and
the algebraic form of `delta_0` are proved; the *number* `0.0911` is only as good as the
Tammes constant fed into it. Per the assignment I am **not** claiming a new threshold:
`delta_0` is a derived function of a classical spherical-code constant. X should pin the
exact primary locator for the Tammes `N = 13` value (Schutte–van der Waerden tradition)
and re-evaluate. If the correct `theta_13` is smaller than `57.1367 deg`, `delta_0` grows
and the bound improves; if it is not available in a citable form, `K15-E012` should be
replaced by C013(a)'s unconditional volume count.

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
short next shell could in principle have more than 12 centres inside `[2, 2+0.09]`. That
is a concrete finite question for C/X (`CLAIMS_FOR_X.md`, `K15-E013`), and it must be
settled before the bound is used. I make no claim about it in this block.
