# Fixture package: the icosahedral 13-cluster as a cut/flow instance

Role E, `K15-REVIEW-0308-E`. For C's cut/flow evaluator. Everything here is exact unless
labelled provisional.

## 0. A mistake I nearly published, and the check that caught it

While preparing this package I concluded that `(H_R)` with `R = 2.09` was **false**: I reasoned
that the twelve neighbours of the icosahedral centre lie at `2.102924 > 2.09`, so
`N_R({c}) = empty` and the Hall condition would read `0.1066 <= 0`.

That is wrong. `2.102924` is the **edge** between two *outer* centres. The distance from the
centre `c` to each of its twelve neighbours is **exactly `2`** (that is what "tangent" means), so
`N_R({c})` contains all twelve at `R = 2.09`, and the Hall condition is satisfiable there. The
numerical check returned

```
outer centre distances from c: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
icosahedron edge            : 2.102924448
```

and stopped the error. Recorded because the confusion is easy to repeat: **the cluster has two
distinct lengths, `2` (centre to neighbour, tangency) and `2.102924` (neighbour to neighbour, the
icosahedron edge), and only the first is relevant to `N_R({c})`.**

## 1. Exact coordinates in `Q(sqrt5)`

Let `phi = (1+sqrt5)/2` and `s = 2 / sqrt(2+phi) = 2 sqrt2 / sqrt(5+sqrt5)` (since
`1 + phi^2 = 2 + phi = (5+sqrt5)/2`). Then `s = 1.051462224...` and the twelve vertices

```
(0, +-1, +-phi),  (+-1, +-phi, 0),  (+-phi, 0, +-1)      multiplied by s
```

have length exactly `2`. All coordinates lie in `Q(sqrt5)`, so an evaluator can use exact
arithmetic in that field; `s` itself is `2 sqrt2 / sqrt(5+sqrt5) in Q(sqrt5, sqrt2)`, so a field
`Q(sqrt2, sqrt5)` suffices. Rational-approximation fallbacks should carry an explicit error
budget.

## 2. Exact distance table (the whole geometry the cut needs)

| pair type | count | distance | exact form |
| --- | --- | --- | --- |
| centre to neighbour | 12 | `2` | `2` (tangency) |
| neighbour–neighbour, edge | 30 | `2.1029244485` | `4 sqrt2 / sqrt(5+sqrt5)` |
| neighbour–neighbour, second | 30 | `3.4026032334` | `phi * 4 sqrt2 / sqrt(5+sqrt5)` |
| neighbour–neighbour, antipodal | 6 | `4` | `2 x circumradius` |

`30 + 30 + 6 = 66 = C(12,2)`, so this is the complete table. (An earlier version of this table
gave the non-edge distance as `3.804226065`, which is wrong: it is neither of the two non-edge
values. Corrected from a direct computation over all `66` pairs.)

The 30 edges are those of the icosahedron; each outer centre has 5 edge-neighbours. Minimal
separation in the cluster is `2`, attained only by the centre–neighbour pairs.

## 3. The candidate cut

```
S = {c}                                    (the single defective centre)
d(c) = sqrt32 - vol Omega(c) = 0.106563221  (exact, using vol Omega(c) = V_dodeca)
N_R(S) \ S = the 12 outer centres           (all at distance exactly 2 <= R = 2.09)
(H_R) for S :  sum over the 12 outer centres of (c(u) - sqrt32)  >=  0.106563221
```

This is the **minimal cut**, and it is the only one available, because the icosahedral defect is
isolated (`REVIEW_0138.md` §3.6: two motifs are legal only at separation `>= 5.5 > 2R = 4.18`).
So for this fixture `(H_R)` reduces to a single inequality with twelve terms — the smallest
possible instance of the collective target.

## 4. Volume data: what is certified and what is not

| quantity | value | status |
| --- | --- | --- |
| `vol Omega(c)` | `<= 5.5502910285155` | **certified**, unconditional (`K15-E045a` + `vol D`) |
| `vol Omega(c)` | `= 5.5502910285155` | certified *given* McLaughlin (`K15-E045b`) |
| `vol Omega(w_i)` | `>= V_dodeca = 5.5502910285155` | certified given McLaughlin |
| `vol Omega(w_i)` | `<= (4pi/3)(extent)^3` | not useful: the cluster leaves them unbounded |
| `vol Omega(w_i)` | `8.17`–`13.51` in specific completions | **provisional and unreliable** — upper bounds, flagged by the extent test (`K15-E062`) |

**So the honest position on the twelve-term inequality is: no term has a certified lower bound
better than `V_dodeca`, and `sum of 12 x (V_dodeca - sqrt32) = -1.279` is negative — the certified
lower bounds do not even give a nonnegative surplus.** That is the obstruction in one line: with
the only certified per-cell bound, the surplus is bounded below by `-1.279`, while the deficit to
be covered is `+0.1066`.

## 5. What an evaluator should test

1. Confirm `|N_R({c})| = 12` for `R = 2.09`, `2.11`, `2.2` (it is 12 for all: the payers are at
   distance exactly `2`).
2. Confirm the exact distances of Section 2 in the chosen arithmetic, with residuals below the
   stated budget.
3. Report the cut's private/available surplus **for a specified completion**, with the extent flag
   from `REVIEW_0138.md` §5 applied — a completion whose payer cells exceed extent `2` is
   unsaturated and its surplus must not be reported as data.
4. Report the certified bracket `[-1.279, +inf)` on the surplus and state which end comes from
   which theorem.

## 6. Scope, stated explicitly

- **Separation:** minimal `2`, attained only on centre–neighbour pairs; verified.
- **Saturation:** the 13-cluster is **not** saturated. Its saturation is a Zorn extension
  (`K15-E070`), not an explicit object, so **no finite computation on the cluster is a
  saturation-complete fixture.** This is the limitation that has to be stated whenever these
  numbers are quoted.
- **Boundary scope:** the centre cell is determined by the twelve neighbours alone (`E045a`), so
  `vol Omega(c)` needs no boundary treatment at all. The *payer* cells do, and no such treatment
  is available.
