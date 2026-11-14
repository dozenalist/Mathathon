# The icosahedral compensation inequality: quantitative obstruction

Role E. `K15-E040`. Status **OBSTRUCTED (quantitative)**. The inequality is neither
proved nor refuted; the obstruction is stated exactly, with the certified brackets.
Scripts: `scripts/icosa_compensation_search.py`, `scripts/icosa_targeted_completion.py`.
Evidence: `evidence/icosa_compensation_search.txt`, `evidence/icosa_targeted_completion.txt`.

## The inequality

For `C = {v}` the dodecahedral centre, `Block(C) = C union N(C)` is the 13-cluster and
`(T')` reads `sum_{i=1..12} vol Omega(w_i) >= 13 sqrt(32) - 5.5502910285155`, i.e.

```
sum  >=  67.9888142149 ,        mean  >=  5.665734518 .
```

## What is provable from the certified local data — and it is not enough

`Omega(w) = { x : |x-w| <= |x-z| for all z }` and, for `x = w + t u`,

```
x in Omega(w)  <=>  t <= d_z / (2 cos phi_z)   for every other centre z with cos phi_z > 0,
```

where `d_z = |z-w|` and `phi_z` is the angle between `u` and `z-w`. Since every centre has
`d_z >= 2`, the bound `d_z/(2 cos phi_z) >= 1` holds whenever `cos phi_z > 0`, and the
directions with `cos phi_z <= 0` are unconstrained by any *known* centre. Hence

```
t(u) >= 1 for every u in S^2 ,        so        vol Omega(w) >= 4 pi / 3 = 4.188790205 .
```

**This is exactly what local distance data can give, and no more.** The six known
neighbours of an outer centre cannot improve it, because in every direction either a
neighbour constrains `t` to `>= 1` or no known neighbour constrains it at all. So the
inscribed-ball bound is *optimal for the information available from the 13-cluster alone*,
and it falls short by

```
13 sqrt(32) - 5.5502910285 - 13 (4 pi / 3) = 19.08483258 .
```

Certified bodies disjoint inside the outer cells therefore cannot close `(T')`: the largest
body certifiable from the cluster is the unit ball, and any refinement must use information
about the *completion*, not about the cluster. Recorded as the first half of the
obstruction.

## The bracket, with both directions

| quantity | value | status |
| --- | --- | --- |
| absolute floor on any mean cell volume (dodecahedral theorem) | `5.550291029` | proved elsewhere, imported |
| `(T')` threshold mean | `5.665734518` | required |
| best certified **lower** bound from local data | `4.188790205` | proved here |
| best computed **upper** bound (targeted completion) | `8.321262` | `TESTED_FINITE` |
| best computed upper bound (random completions) | `8.167277` | `TESTED_FINITE` |

So the true value of the infimum over completions lies in `[4.18879, 8.16728]` per cell —
a window of factor `1.987` — and the threshold `5.665735` sits inside it. **The inequality
is not decidable from the information currently certified.** That is the quantitative
obstruction.

## Why the completions are far above the threshold, and why that is suspicious

The threshold mean is only

```
5.665734518 / 5.550291029 = 1.0207995  ,   i.e. 2.080 % above the global minimum cell volume.
```

`(T')` therefore demands that **every one of the twelve outer cells be within 2.08 % of the
smallest Voronoi cell that any packing admits**. That is a near-extremal requirement on
twelve specific, non-generic cells. Two consequences:

1. It is *implausible*, and I expect `(T')` to be **false**; but the computed upper bounds
   (`8.17`–`8.32`, i.e. `47 %` above threshold) are nowhere near a refutation, because a
   finite completion only gives an upper bound and ours are undersaturated (density `0.10`
   against `0.177` for fcc).
2. It explains why the icosahedral block is the wrong block. A 13-member block asks twelve
   cells to be near-extremal *simultaneously*, while the deficit being repaid is only
   `0.1066`. The compensation is real but diffuse, and a one-step block cannot see it.

## Corrected condition (derived from the obstruction, not guessed)

Enlarge the block to two steps and let the deficit be repaid by the **second** shell:

```
Block2(C) = C  union  N(C)  union  N(N(C)) ,
D(C) = sum_{v in C} (sqrt(32) - vol Omega(v))                       (unchanged)
S2(C) = sum_{w in Block2(C) \\ C} ( vol Omega(w) - sqrt(32) )       (two shells of surplus)
(T'-2)   S2(C) >= D(C) .
```

Since `S2 >= S` termwise, `(T'-2)` is **strictly weaker** than `(T')`, and the price is a
larger block: `diam Block2(C) <= diam(C) + 4 (2.09)`, which raises the boundary constant in
`K15-E001` Step 2 but does not affect any certified count. This is the corrected condition
the fallback asks for, and it is derived from the measured gap rather than assumed.

## Fixtures recorded

- `centre = 5.5502910285155` reproduced in **every** run, matching `K15-E002` to `1e-15`.
  This is the control that the completion construction did not disturb the core.
- `minsep = 2.0` verified in every accepted configuration.
- Targeted rings at polar angle `62 deg` and `70 deg`, `5`–`7` points per outer centre,
  azimuthal offsets `0`, `pi/6`, `pi/3`: all accepted, none reduced the sum below `99.8`.
  Placing neighbours at distance `2` in the free outward hemisphere is therefore **not**
  the lever that controls these cells.

## What would settle it

A certified lower bound of the form `vol Omega(w) >= Phi(neighbour data)` with
`Phi > 5.665735` on the outer configuration, where `Phi` uses the *count* of neighbours
within `2.09` (at most `12`, from `K15-E014`) plus the angular data. That is a
kissing-with-tolerance estimate with an angular constraint, and it is the next missing
inequality. Offloaded as `LOCAL_ICOSA_SEARCH.md`.

## K15-E042 — the angular estimate: an improvement that still falls short

I attempted the "rigorous angular/local-mass estimate" the task asks for, and it fails.
Recorded with the numbers, because a failed bound with a measured margin is more useful
than a vague plan.

**The bound.** For `x = w + t u`,
`t(u) = min over centres z with cos phi_z > 0 of d_z/(2 cos phi_z)`, and `t >= 1` always.
A lower bound on `t` is the **minimum** of the per-centre lower bounds — not the maximum.
Per centre: the six fixed neighbours of an outer centre are known exactly (one at `d = 2`,
five at `d = 2.102924`), so their terms are known; every other centre has `d >= 2.09` (by
`K15-E014` at most twelve lie in `[2, 2.09]`, and those twelve are accounted for), giving
the fallback `2.09/2 = 1.045`. Hence

```
t_lb(u) = min( min_{6 fixed} d_j/(2 cos phi_j) , 1.045 ) ,      vol Omega(w) >= (1/3) int t_lb^3 .
```

**Result, minimising over the six free neighbour directions** (they are placed at
`d = 2`, the most adversarial choice):

| bound on an outer cell | value | shortfall to `5.665735` |
| --- | --- | --- |
| inscribed ball `4 pi/3` | `4.188790` | `26.1 %` |
| **angular + count-12 (this work)** | **`4.733968`** | **`16.4 %`** |
| dodecahedral theorem (imported) | `5.550291` | `2.04 %` |
| required | `5.665735` | — |

So the angular estimate is a real improvement over the inscribed ball (`+13.0 %`) but is
`0.931767` short. **It does not close `(T')`.** The reason is structural: the fallback
`1.045` is weak, and in directions aligned with a neighbour at distance exactly `2` the
bound is `1`, so `t_lb` is pinned near `1` over a non-negligible solid angle.

**A direction error caught in my own code, recorded.** The first version used
`t = max(t_near, FALLBACK)`, which reported `5.943752` — *above* the threshold, and would
have been read as success. That is wrong: `t` is a minimum over centres, so a lower bound on
`t` is the minimum of the per-centre bounds. Comparing the two runs is the clearest possible
demonstration of why the checklist item on monotonicity direction matters; a plausible
number four fifths of the way to a proof came from a single `max`/`min` slip. Both runs are
in `evidence/outer_cell_angular_bound.txt`.

**What the failure tells us.** The information "six neighbours at known directions, at most
twelve within `2.09`" is not enough. Closing `(T'-R2')` needs either (a) a sharper count —
e.g. `11` rather than `12`, or a *second* shell count — or (b) a genuinely new estimate in
which the five neighbours at `2.102924 > 2` (bisectors at `1.051462 > 1`) are exploited
*simultaneously* over the whole solid angle rather than direction by direction. Attempt (b)
is the next missing inequality; attempt (a) is a spherical-code question of the same kind as
`K15-E014` but at radius `2.09` with one neighbour already fixed, which changes the count.

### Separation check: is the 4.734 an artefact of an illegal configuration?

The minimisation allows the six free neighbour directions to be chosen freely, which could in
principle place two near neighbours closer than `2` to each other — an illegal configuration
whose bound would be too weak (still valid, since minimising over a superset only lowers the
value, but less informative). Adding the true constraint — two neighbours of the outer centre
at radii `d_a, d_b` must satisfy `d_a^2 + d_b^2 - 2 d_a d_b cos(angle) >= 4`, which for
`d_a = d_b = 2` means angular separation `>= 60 deg` — and re-minimising gives

```
4.734075619     (constraint active, configuration reported feasible)
against 4.733968112 without it.
```

The bound moves by `1.1e-4`, so **the optimum was already attained at a feasible
configuration** and the overlap hypothesis is refuted. The `4.734` is therefore not an
artefact of relaxing the separation constraint; it is what this information actually gives.

The five fixed neighbours sit at angular separation `58.28 deg` from the centre direction
(law of cosines on the `(2, 2, 2.1029)` triangle), which is exactly the tangency value
`arccos(0.52573)` — the configuration is tight, and the free directions cannot buy much.

### Summary of the per-cell obstruction

| bound | value | source |
| --- | --- | --- |
| inscribed ball | `4.188790` | separation `>= 2` alone |
| angular + count-12 + separation | `4.734076` | this work, feasible optimum |
| dodecahedral theorem | `5.550291` | McLaughlin, computer-assisted |
| **required** | **`5.665735`** | `(T')` |

Every available per-cell bound is short, including the ideal single-cell minimum. The
deficiency is `16.4 %` for the best self-contained bound and `2.04 %` even for the
computer-assisted ideal. **Conclusion: `(T'-R2')` cannot be proved by per-cell estimates in
any form presently available, and the block must either be enlarged (two-shell `(T'-2)`) or
the inequality replaced by a collective statement over the whole block.** That is the
precise state of the geometric route at handoff.

## K15-E043 — correcting my own pessimism: `(T')` has large slack in reality

An earlier paragraph argued that `(T')` is "implausible" because its threshold mean
`5.665735` is only `2.080 %` above the dodecahedral floor `5.550291`. **That inference was
wrong, and I withdraw it.** Comparing the threshold with the *worst-case floor* says nothing
about whether the inequality holds; the relevant comparison is with actual configurations.
Measured:

```
best computed sum   98.007327   vs threshold 67.988814   ->  1.4415x  (+44.2 %)
targeted completion 99.855149   vs threshold             ->  1.4687x  (+46.9 %)
best computed mean   8.167277   vs threshold  5.665735   ->  1.4415x
```

So in every completion examined the sum exceeds the requirement by roughly `44 %`. `(T')` is
**not marginal**; it is comfortably satisfied by everything computed, and its difficulty is
entirely in the lower-bound direction. This matters for how the route should be judged: the
geometric mechanism is not in doubt, only our ability to certify it. The correct one-line
status is "plausibly true with large slack, unprovable with present tools", not "near the
edge and probably false".

The `2.080 %` figure remains true and is still useful, but its correct reading is narrower:
it shows that the *single-cell minimum alone* cannot prove `(T')` (`K15-E041`), not that
`(T')` is false.

## K15-E044 — why per-cell techniques are stuck, from a second direction

Independent of the quadrature bound of `K15-E042`, a hand estimate gives the same ceiling.
The six neighbours of an outer centre all lie within `58.28 deg` of the **inward** direction
(the five at `121.7 deg` from outward; `c` at `180 deg`). Hence the whole **outward
hemisphere** about `w` is free of known neighbours, and the cell there is limited only by the
completion, which satisfies `d >= 2.09`, giving `t >= 1.045`. Splitting the integral at the
equator:

```
vol Omega(w) >= (1/3) [ 2 pi (1)^3 + 2 pi (1.045)^3 ] = 2.0944 + 2.3905 = 4.4849 .
```

That beats the inscribed ball (`4.1888`) but is still `20.8 %` below the required `5.665735`.
Refining with the constraint that at most six further centres lie in `[2, 2.09]` on the
outward side, mutually `>= 60 deg` apart, and that a centre at angular distance `alpha`
gives `t >= 2.09/(2 cos alpha)`, raises the estimate only to about `4.9` — still short. The
quadrature optimum of `4.734` and this hand estimate agree to within the crudeness of the
latter, which is reassuring about both.

**Conclusion.** Two independent routes cap per-cell bounds near `4.7`–`4.9`, i.e. `13`–`17 %`
below the requirement, while the truth is `44 %` *above* it. The gap is a deficiency of
Voronoi-volume lower-bound technique, not of the geometry. Closing it needs an estimate that
uses the neighbour configuration globally and simultaneously — the next missing inequality,
and the honest stopping point for this block.

## K15-E045 — the centre cell is exactly dodecahedral in every completion

A clean by-product, and it fixes the deficit exactly.

**Proposition (PROVED).** Let `Lambda` be any saturated 2-separated set containing the
icosahedral 13-cluster (centre `c`, twelve tangent neighbours at the icosahedron vertices of
circumradius `2`). Then `Omega(c) = D`, the regular dodecahedron of inradius `1`, and

```
vol Omega(c) = 5.55029102851549...   exactly, for every completion.
```

*Proof.* The twelve tangent neighbours already impose the twelve bisector half-spaces that
cut out `D`, so `Omega(c) ⊆ D`. Conversely the dodecahedral theorem gives
`vol Omega(c) >= V_dodeca = vol D` for every cell of every packing. Hence
`V_dodeca <= vol Omega(c) <= vol D = V_dodeca`, so equality holds and `Omega(c) = D` up to a
null set. ∎

**Why it matters.** The deficit `D(C) = sqrt(32) - V_dodeca = 0.1065632209769` is therefore
**exact and unavoidable**: no completion can reduce it, and no completion can enlarge the
centre cell to help. This confirms — rather than assumes — the threshold
`67.9888142149`, and it explains a numerical observation I had recorded without proof: the
computed centre cell was `5.550291028515513` in *every* run, to `1e-15`, across six random
and six targeted completions. That agreement is now accounted for: it is a theorem, not a
property of the completions chosen.

**How much correction is needed.** By `K15-E041`, the dodecahedral theorem gives
`12 V_dodeca = 66.6034923422`, leaving

```
67.9888142149 - 66.6034923422 = 1.385321873 ,   i.e. 0.1154435 per outer cell (2.08 %).
```

## K15-E046 — where that 2.08 % should come from, as an estimate

Each outer centre has five neighbours at `2.102924 > 2` instead of the tangent distance `2`.
Moving a neighbour from `2` to `2.102924` pushes its bisector out from `1` to `1.051462`,
so the cell gains a slab of thickness `0.051462` over that face. With five such faces of
area `A` each, the gain per cell is `5 x 0.051462 x A = 0.25731 A`, and the total gain is
`12 x 0.25731 A = 3.08772 A`.

Setting `3.08772 A >= 1.385321873` needs `A >= 0.4486`. The pentagonal faces of the
dodecahedron have area about

```
A_pent = (1/4) sqrt(25 + 10 sqrt5) a^2 ,   a = 4/sqrt(10 + 22/sqrt5) = 1.4530851 ,
```

which evaluates to about `1.7205`. So the available gain (`3.08772 x 1.7205 ≈ 5.31`) exceeds
the `1.385` needed by a factor of about `3.8`, **before** accounting for the fact that the
five neighbours constrain only part of each face and that the completion shrinks the cell.

**What this is and is not.** It is a first-order estimate identifying the correct mechanism
and showing the margin is not delicate — consistent with the `44 %` slack measured in
`K15-E043`. It is **not** a proof: it ignores that the bisector shift is not uniform over a
face, that faces overlap, and that the completion only ever removes volume. The rigorous
version must lower-bound the volume of `D` with five faces pushed out by `0.051462`, in the
directions of the actual icosahedral normals, and show the result exceeds
`5.665734518`. That is a concrete, finite, algebraic problem about a specific polytope, and
it is exactly the "next missing inequality". Offloaded in `LOCAL_ICOSA_SEARCH.md`.
