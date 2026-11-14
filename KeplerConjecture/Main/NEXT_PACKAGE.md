# Next research package (for the block after K15-REVIEW-0138-M)

Written by M. This is the concrete target the withdrawal leaves standing: after
`K15-C035`/`C036`/`C044`/`C045`, the whole geometric route reduces to **one
analytic inequality**, and this file says exactly which one, with the constants.

## The inequality

For a saturated packing `Λ` and every "blob" `U` (a union of Voronoi cells
containing a ball, so that `|∂U| = O(|U|^{2/3})`):

```
Σ_{v∈U} vol Ω(v)  ≥  √32 · |U|  −  C · |U|^{2/3},        √32 = 5.656854249…
```

Equivalently, in the transfer language of `K15-C044`: the cut condition
`Σ_U b ≤ Φ|δ⁺(U)|` with `b = √32 − vol Ω` and `Φ` fixed.

## The constants, and what each would buy

| cell-volume constant `V_0` | density bound `(4π/3)/V_0` | status |
| --- | --- | --- |
| `4.188790` | — | the inscribed ball (trivial) |
| `5.372754` | `0.779636` | Rogers' simplex bound, `σ₃ = 0.779635570044…` |
| `5.550291` | `0.754697` | dodecahedral (Hales–McLaughlin), the best known |
| `5.656854` | `0.740480` | Kepler |

So the required improvement over Rogers is `5.29%`, and over the dodecahedral
theorem `1.92%`. **A bound at `5.550291` alone changes nothing**; the target is
`> 5.550291`, and anything at `√32` is the theorem.

## What a block should attempt, in order

1. **A cluster-averaged improvement over Rogers.** Take the icosahedral
   13-cluster and prove `Σ_{v∈K} vol Ω(v) ≥ 13 V` for some `V > 5.372754` — even
   `V = 5.40` would be a new cluster inequality (not yet a density bound, but a
   step). Tools: Rogers' simplex decomposition restricted to the cluster; the
   angular/`t`-bounding device of E's `outer_cell_angular_bound.py` with the
   `K15-E048` ceiling removed by using a *body that is not star-shaped about w*.
2. **A stability statement.** Cells with `vol Ω ≤ V_dod + ε` force a near-
   icosahedral neighbourhood; if the neighbourhood is exactly icosahedral the
   cluster cannot be periodic (frustration), so the neighbours must pay. Make
   `ε ↦` the neighbours' excess explicit (`K15-C029r` is the bookkeeping form).
3. **Falsification test first.** Before proving anything, search for a *periodic*
   packing with a blob where `Σ_U b > 0` and `|δ⁺(U)|` small — that would refute
   the cut condition at bounded `Φ`. Any such packing is a publishable
   obstruction; a search finding none is weak evidence, not proof.

## What not to do

- Do not attempt the pointwise inequality by computation (`K15-C036`).
- Do not reuse the withdrawn `K15-C029` in any form.
- Do not claim that a saturated/finite search "closes" a family.

## Deliverable boundary

A block that produces (1) with an explicit `V` and a proof over all clusters of
diameter `D ≤ 4`, or (3) with a concrete periodic witness, has succeeded. A block
that only restates the ladder has not.
