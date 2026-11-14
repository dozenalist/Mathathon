# Rigorous enclosure of delta_13 and the shell lemma at rho = 209/100

Role E. `K15-E015`. Status **PROVED (arithmetic), with a disclosed external
computer-assisted dependency**. Reviewer: X; independent re-run: Astra.
Code: `Experimental/scripts/tammes13_enclosure.py`. Output:
`Experimental/evidence/tammes13_enclosure.txt`.

## The defining equations

Musin–Tarasov, arXiv:1002.1439v3, Section 2, Remark preceding Theorem 1 (printed p. 3):

```
(E1)   2 tan( 3pi/8 - a/4 ) = (1 - 2 cos a) / cos(a)^2
(E2)   cos d = cos a / (1 - cos a)
```

The Remark states that solving (E1) for `a` and substituting into (E2) gives
`a_13 = alpha(d_13) ~ 69.4051 deg` and `delta_13 ~ 57.1367 deg`.

**Independent check that I have transcribed (E1) correctly.** Solving (E1) numerically gives
`a = 69.4050501037 deg` and `d = 57.1367030776 deg`; and the source's own relation
`alpha(d) = arccos(cos d/(1+cos d))` (their Proposition 3.6) returns
`alpha(d) = 69.4050501037 deg = a`, matching to all digits. The two relations are therefore
mutually consistent, which they would not be if the exponent or a coefficient were misread.
For comparison the variants with `(1-2cos a)/cos a` and `(1-2cos a)/cos^3 a` give
`d = 72.09 deg` and `45.33 deg`, so the transcription is uniquely determined.

## Root selection and uniqueness

Define `g(a) = 2 tan(3pi/8 - a/4) - (1 - 2 cos a)/cos^2 a` on `(0, pi/2)`. Then

```
g'(a) = -(1/2) sec^2(3pi/8 - a/4) - 2 sin(a)(1 - cos a)/cos^3(a)  <  0 ,
```

because on `(0, pi/2)` we have `sin a > 0`, `cos a > 0`, `1 - cos a > 0` and
`sec^2 > 0`. Both terms are strictly negative, so **`g` is strictly decreasing and has at
most one root** in `(0, pi/2)`. A sign change on a rational interval therefore determines
the root uniquely — no root isolation or algebraic elimination is needed.

Certificate of the root: with rational endpoints `a_lo = 12113/10000` and
`a_hi = 12114/10000`,

```
g(1.2113) in [ 0.00120503788683505,  0.00135752466875259]   (positive)
g(1.2114) in [-0.00170516667624990, -0.00155268902813996]   (negative)
```

so `a* in [1.2113, 1.2114]` by the intermediate value theorem, uniquely.

## Monotonicity chain used for the bound

`h(c) = c/(1-c)` is strictly increasing on `(0,1)`; `h(a) := cos a/(1-cos a)` is strictly
decreasing in `a` on `(0,pi)`; `arccos` is strictly decreasing. Hence from `a* <= a_hi`,

```
d = arccos(h(a*))  <=  arccos(h(a_hi))  <=  arccos(h_lo),
```

where `h_lo` is any lower bound for `h(a_hi)`. Because `arccos` is decreasing, the
comparison `d < arccos(23681/43681)` is **equivalent to a rational inequality**

```
h(a_hi) > 23681/43681 ,
```

so **no arccos and no transcendental comparison is needed inside the certificate**. The
whole decision is rational.

## The certificate

Rational interval arithmetic throughout (`fractions.Fraction` endpoints), with

- `pi` enclosed by `333/106 < pi < 355/113`;
- `sin`, `cos` by Taylor series with the explicit alternating-series remainder bound
  `|R_N| <= x^(2N+2)/(2N+2)!`, valid here because the terms of both series decrease
  monotonically for `k >= 2` once `x <= 1.6`, and `N = 28` is far past the turning point;
- `tan = sin/cos` by interval division, using monotonicity of `tan` on `(0, pi/2)`;
- `cos` monotone decreasing on the ranges used (`a <= 1.2114 < pi/2`).

Result (from `evidence/tammes13_enclosure.txt`):

```
cos(a_hi) >= 0.351709193286087241
h(a*)     >= 0.542517631969590242
threshold = 23681/43681 = 0.542135024381310004
margin    = +3.826e-04                                > 0  CERTIFIED

delta_13  <  57.146323807 deg      (rigorous upper bound)
theta_min >  57.170897332 deg      (rigorous lower bound)
```

**Runtime 0.25 s, one core, well under 200 MB.** No floating point participates in any
decision; the printed decimals are for human reading only.

Note the bound is deliberately coarse (`57.1463` against a true `57.1367`): the bracket on
`a` is `1e-4` wide. Tightening the bracket is a one-line change and would give roughly
`57.1368`; it is not needed, because the margin to `theta_min` is `0.0246 deg`.

## The shell lemma, now unconditional in its arithmetic

**`K15-E014` (PROVED).** Let `Lambda` be 2-separated and `x in Lambda`. Then
`#{y in Lambda : 2 <= |y-x| <= 209/100} <= 12`.

*Proof.* Suppose 13 such `y`. By the corrected `K15-E011` (valid because
`delta = 0.09 <= sqrt5 - 1`) every pair satisfies
`cos theta <= max(1-2/R^2, R/4) = 23681/43681`, so `theta >= arccos(23681/43681)`. But 13
points on `S^2` satisfy `theta <= delta_13 < arccos(23681/43681)` by the certificate above.
Contradiction. ∎

## Dependency disclosure

The step `d_13 = delta_13` is **Theorem 1** of arXiv:1002.1439v3, which the authors prove by
computer enumeration of irreducible contact graphs. This script certifies only that the
constant *defined by their equations* is below our threshold. It does **not** verify the
enumeration, and any complexity comparison must charge the enumeration to the shell lemma.
Consequently `K15-E014` is a lemma whose *arithmetic* is certified here and whose *geometric
content* rests on a published computer-assisted theorem. It is not a new proof of the
Tammes `N = 13` problem and I claim no novelty for that theorem.

## What remains

- Independent re-run by Astra (`LOCAL_SHELL_2P09.md`), and an independent reading of the
  Taylor remainder argument.
- `K15-E013`: Barlow stackings must still be shown to have at most 12 centres in
  `[2, 2.09]`. FCC and HCP are fine (12 at distance 2, next shell `2 sqrt 2 = 2.8284`).
- The shell lemma alone gives no density bound; it feeds `K15-E020` and `K15-E030`.

## Lemma (Taylor remainder bound, written out)

The certificate rests on the following, which I record rather than assert.

**Lemma.** For `x` real with `0 <= x <= 8/5` and `N >= 2`,

```
| cos x - sum_{k=0}^{N} (-1)^k x^{2k}/(2k)! |  <=  x^{2N+2}/(2N+2)! ,
| sin x - sum_{k=0}^{N} (-1)^k x^{2k+1}/(2k+1)! |  <=  x^{2N+3}/(2N+3)! .
```

*Proof.* Let `t_k = x^{2k}/(2k)!` for the cosine series. Then
`t_k/t_{k-1} = x^2/((2k-1)(2k))`, which is `< 1` as soon as `x^2 < (2k-1)(2k)`. Since
`x <= 8/5`, `x^2 <= 64/25 = 2.56`, and for `k >= 2` we have `(2k-1)(2k) >= 12 > 2.56`. So
`t_k` is strictly decreasing for `k >= 2`, hence from the term of index `N >= 2` onward.
The series is alternating in sign, so the Leibniz criterion gives that the tail from index
`N+1` onward is bounded in absolute value by its first term, which is
`x^{2N+2}/(2N+2)!`. For the sine series set `s_k = x^{2k+1}/(2k+1)!` with
`s_k/s_{k-1} = x^2/((2k)(2k+1)) < 1` for `k >= 1` since `(2k)(2k+1) >= 6 > 2.56`. Same
argument. ∎

The script uses `N = 28`, and the ranges it evaluates at are `a <= 1.2114`,
`3pi/8 - a/4 <= 0.8753 + eps`, and (in the bisection helper) degrees up to `1.57`; all are
below `8/5 = 1.6`. The hypothesis of the lemma is therefore met with margin.

`pi` is enclosed by `333/106 = 3.14150943... < pi < 3.14159292... = 355/113`, the standard
continued-fraction bounds; both are exact rationals and the enclosure is verified by
squaring appropriately or by the classical interpolation argument. Only the enclosure is
used, never a decimal expansion.

## K15-E013 — CLOSED: every Barlow stacking has exactly 12 centres in [2, 2.09]

Status **PROVED** (analysis), with a numerical cross-check in
`Experimental/scripts/barlow_shell_check.py`.

A Barlow packing is any stacking of close-packed hexagonal layers with consecutive layers
offset into the hollows. Write the layer at height `0` as the triangular lattice `L` of
spacing `2`, with `L = { m(2,0) + n(1, sqrt3) }`. Adjacent layers sit at height
`h = 2 sqrt(2/3) = 1.63299316...`, with centres at `L + delta`, where `delta` is one of the
two hollows

```
delta_+ = (1, sqrt3/3),      delta_- = (1, -sqrt3/3),      |delta_+| = |delta_-| = 2/sqrt3 ,
```

and the stacking is any word in the three layer positions with no two consecutive equal.

**Distance spectrum to the adjacent layers.** For a centre at the origin and a centre
`(u + delta, h)` in an adjacent layer,

```
|(u+delta, h)|^2 = |u + delta|^2 + h^2 = |u+delta|^2 + 8/3 .
```

The nearest lattice points to a hollow are the three vertices of the triangle containing
it, at `|u + delta|^2 = 4/3`, giving `4/3 + 8/3 = 4`, i.e. distance exactly `2`; there are
three such per adjacent layer, hence `6` from the two adjacent layers. The next value is
`|u+delta|^2 = 16/3` (the ring at `4/sqrt3 = 2.3094`), giving `16/3 + 8/3 = 8`, i.e.
distance `2 sqrt2 = 2.82842712...`, six in total.

**Remaining contributions.** In-plane: `2`, then `2 sqrt3 = 3.4641`. Two layers away:
`2h = 3.26599`. All are `>= 2 sqrt2`.

**Conclusion.** The distance spectrum about any centre of any Barlow packing has *no*
values in the open interval `(2, 2 sqrt2)`, and `2.09 < 2.8284271`. Hence exactly `12`
centres lie in `[2, 2.09]`, for every Barlow stacking. This holds uniformly over the
stacking word, because the interlayer geometry is identical for every choice of hollow —
which is precisely why the equality family does not break the shell bound.

**Numerical cross-check.** `barlow_shell_check.py` builds four stackings (`ABC`, `AB`,
`ABCB`, `ABAC`), translates so the origin is a centre, and reports the spectrum. All four
return `12` at `2.000000` and the next shell at `2.828427`, with `12` centres in
`[2, 2.09]`. Two bugs were found and fixed during this check and are recorded because they
are the kind that produce false confidence: an incorrect hollow shift (drifting by
`1 - 2/sqrt3` in-plane, which produced illegal distances below `2`), and placing the
reference centre in the bottom layer instead of the middle (which halved the count to
`9 + 3`). The final construction reproduces the known fcc spectrum `12, 6, 24, ...` at
`2, 2sqrt2, 2sqrt3`, which is the control that the geometry is right.
