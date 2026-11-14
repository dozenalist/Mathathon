# Analytic candidate: a local-mass row outside ordinary Cohn–Elkies

Role E (Experimental). `K15-E020`. Status **SPECIFIED, validity PROVED, strength
UNEVALUATED**. Evaluator: C. Reviewer: X.

## Why a row and not a kernel

Li (Adv. Math. 460 (2024) 110043, arXiv:2206.09876v3, Theorem 6.1) proves the optimal
3D ordinary-CE centre-density bound exceeds `0.18398089 > 2^(-5/2)`. In occupied-volume
units `(4pi/3)(0.18398089) > 0.770`, above `pi/sqrt(18) = 0.740480489693`. Ordinary CE is
an obstructed control. Any candidate must add a constraint not implied by
`f <= 0` off `B_2` and `fhat >= 0`.

**Reconciliation with the 27616 review, which is correct and constrains the design.**
The review objects that "the dodecahedral star plus distant completion is not captured
by a twelve-contact Fourier sum". That objection is decisive against any formulation
that counts *contacts*: a sum over twelve nearest neighbours is blind to everything
beyond them. The candidate below is therefore **not** a contact sum. It is a constraint
on the *mass of the pair-correlation measure in a shell*, which integrates over all
centres, near and distant. A distant completion shifts mass between shells and is
captured by the row at the corresponding radius. This is the only formulation of the
local information I am willing to put forward after that review.

## The auxiliary object

For a packing `Lambda` with separation `>= 2` and a centre `v`, and for `rho >= 2`, let

```
n_v(rho) = #{ w in Lambda \ {v} : |w - v| <= rho }.
```

The **local-mass row** at radius `rho` is the family of constraints

```
n_v(rho) <= N(rho)     for every v in Lambda,
```

where `N(rho)` is any number for which the counting statement is a theorem. Equivalently,
in measure form, `mu(B(0,rho] \ {0}) <= N(rho)` per unit centre, where `mu` is the
pair-difference measure. This is a *linear* functional of the pair measure, hence
admissible as an LP/SDP row, and it is a property of **every** packing: no periodicity,
no lattice hypothesis, no crystallinity.

## Validity: `N(rho)` is already proved, unconditionally

By Main `K15-C013(a)` (`Main/CLAIMS.md`, `a08f378b`), for a 2-separated set and `x` in it,

```
n_x(rho) <= (rho + 1)^3 - 1.
```

This comes from disjointness of the unit balls about the centres inside
`B(x, rho+1) \ B(x,1)`. So the row is **rigorous with `N(rho) = (rho+1)^3 - 1`** and needs
no new theorem. Two remarks:

- The bound is only useful where it beats the trivial counting bound; at `rho = 2` it
  gives `26`, whereas the truth is the kissing number `12`.
- A sharper `N(rho) = 12` holds for small `rho` by `K15-E012` (`SHELL_CONVERSION.md`),
  **provisionally**, because that route needs a cited Tammes `N = 13` constant.

## Admissibility conditions

1. `Lambda` is 2-separated and locally finite. Automatic; no saturation is needed for
   the row itself, though the density argument needs saturation.
2. The row is used at finitely many radii `rho_1 < ... < rho_m` with `m` small, because
   each adds one linear constraint.
3. The evaluator must impose the row on the *unrestricted* packing class. Imposing it
   only on periodic or lattice configurations would reintroduce a lattice hypothesis and
   invalidate the comparison with `CDS22` Table 1.1's `0.741506` lattice column.

## Equality tests

The row must not exclude any packing that attains `pi/sqrt(18)`:

| fixture | contacts at `|y|=2` | next shell | `n_v(2.01)` | `N(2.01)=(3.01)^3-1` | row slack |
| --- | --- | --- | --- | --- | --- |
| FCC | 12 | `2 sqrt 2 = 2.8284` | 12 | 26 | 14 |
| HCP | 12 | `2 sqrt 2 = 2.8284` | 12 | 26 | 14 |
| Barlow stackings | 12 | to be checked | 12 | 26 | 14 |

The equality family is untouched by the row, which is necessary and expected: any
constraint that separated FCC from HCP would be wrong. **But the slack is 14**, which is
the reason this candidate is rated *unevaluated* rather than promising. A row with slack
14 at the contact shell is unlikely to move a bound whose entire remaining gap is
`0.770271 - 0.740480 = 0.029791`.

## Smallest implementable evaluator for C

1. Take C's existing `(f2, f3)` SDP evaluator, which already reproduces the general
   three-point control.
2. Add, for each `rho` in a small grid (e.g. `rho = 2.05, 2.2, 2.5, 3.0, 4.0`), one
   linear row `mu(B(0,rho] \ {0}) <= (rho+1)^3 - 1` in the same variables.
3. Report: SDP status, objective in centre density **and** occupied-volume density
   (`×(4pi/3)`), the gap to `0.740480489693`, and whether the optimum moved at all
   relative to the three-point control.
4. Success criterion for continuation: the objective decreases by more than `0.005` in
   occupied-volume units. A change below `0.001` closes the candidate.

This is small: one extra variable set, five rows, no change to the kernel parametrisation.
It is the smallest test that can distinguish "the local information is too weak" from
"the local information is being used in the wrong direction".

## Hardest unproved item

Not validity — `N(rho)` is proved. The hard item is **strength**: whether any
local-mass row of this form can move the three-point optimum by more than `0.001`. Given
the slack of 14 at the contact shell I expect it cannot, and I would rather record that
expectation than dress the candidate up. The step that would change the picture is a
*kissing-type* row with `N(2+eps) = 12` for an explicit `eps > 0`, i.e. `K15-E012` with a
verified Tammes constant — and even that has slack 0 only at the contact shell, not over
an interval.

## What I am not claiming

No novelty claim. Rows of this type belong to the `DLOV14` family (de Laat–de Oliveira
Filho–Vallentin, Forum Math. Sigma 2 (2014) e23, Section 5), which strengthened the
two-point bound from `0.779747` to `0.773080` using additional local information. My
contribution here is only the *specific* rigorous choice `N(rho) = (rho+1)^3 - 1` from
C013(a), the measure-form statement that survives the review's contact-sum objection, and
the sized evaluation test. No 3D number has been produced; the candidate remains
`UNEVALUATED` until C runs it.
